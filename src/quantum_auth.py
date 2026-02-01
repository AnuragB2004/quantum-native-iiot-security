"""
Quantum Authentication Protocol Implementation

This module implements the quantum identity-based authentication protocol
described in Section IV of the paper.

Author: Anurag Bhattacharjee
Date: February 2026
"""

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from typing import Tuple, Dict, Optional
import hashlib
import json


class QuantumAuthenticator:
    """
    Implements quantum authentication using quantum identity states.
    
    Each device is assigned a unique quantum identity state:
        |ψ_ID⟩ = α|0⟩ + β|1⟩
    where (α, β) are derived from the device's classical identifier.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the quantum authenticator.
        
        Args:
            config: Configuration dictionary with parameters:
                - rounds: Number of authentication rounds (default: 100)
                - threshold: Acceptance threshold for probability deviation (default: 0.05)
                - shots: Number of measurement shots per round (default: 1024)
        """
        self.config = config or {}
        self.rounds = self.config.get('rounds', 100)
        self.threshold = self.config.get('threshold', 0.05)
        self.shots = self.config.get('shots', 1024)
        
        # Registry of registered device identities
        self.device_registry = {}
        
    def qid_hash(self, device_serial: str, manufacturer_secret: str = "DEFAULT_SECRET") -> Tuple[complex, complex]:
        """
        Generate quantum identity amplitudes from classical identifiers.
        
        Implements Eq. (2) from the paper:
            (α, β) = QID-Hash(Device-Serial, Manufacturer-Secret)
        
        Args:
            device_serial: Device serial number
            manufacturer_secret: Manufacturer's secret key
            
        Returns:
            Tuple of (alpha, beta) complex amplitudes satisfying |α|² + |β|² = 1
        """
        # Create deterministic hash
        combined = f"{device_serial}:{manufacturer_secret}"
        hash_obj = hashlib.sha256(combined.encode())
        hash_bytes = hash_obj.digest()
        
        # Convert first 8 bytes to angle theta in [0, 2π]
        theta = int.from_bytes(hash_bytes[:8], byteorder='big') / (2**64) * 2 * np.pi
        
        # Convert next 8 bytes to phase phi in [0, 2π]
        phi = int.from_bytes(hash_bytes[8:16], byteorder='big') / (2**64) * 2 * np.pi
        
        # Generate normalized amplitudes
        alpha = np.cos(theta / 2) * np.exp(1j * phi)
        beta = np.sin(theta / 2)
        
        # Verify normalization
        assert np.isclose(abs(alpha)**2 + abs(beta)**2, 1.0), "Amplitudes not normalized"
        
        return alpha, beta
    
    def register_device(self, device_id: str, device_serial: str, 
                       manufacturer_secret: str = "DEFAULT_SECRET"):
        """
        Register a new device with its quantum identity.
        
        Args:
            device_id: Human-readable device identifier
            device_serial: Device serial number
            manufacturer_secret: Manufacturer's secret key
        """
        alpha, beta = self.qid_hash(device_serial, manufacturer_secret)
        
        self.device_registry[device_id] = {
            'serial': device_serial,
            'alpha': complex(alpha),  # Convert to standard complex
            'beta': complex(beta),
            'p0': abs(alpha)**2,  # Expected measurement probabilities
            'p1': abs(beta)**2
        }
        
        print(f"✓ Registered device {device_id}")
        print(f"  |α|² = {abs(alpha)**2:.6f}, |β|² = {abs(beta)**2:.6f}")
    
    def prepare_qid_circuit(self, device_id: str) -> QuantumCircuit:
        """
        Prepare quantum circuit for device's quantum identity state.
        
        Implements circuit from Figure 2 of the paper.
        
        Args:
            device_id: Device identifier
            
        Returns:
            Quantum circuit that prepares |ψ_ID⟩
        """
        if device_id not in self.device_registry:
            raise ValueError(f"Device {device_id} not registered")
        
        identity = self.device_registry[device_id]
        alpha, beta = identity['alpha'], identity['beta']
        
        # Create circuit
        qr = QuantumRegister(1, 'q')
        cr = ClassicalRegister(1, 'c')
        qc = QuantumCircuit(qr, cr)
        
        # Calculate rotation angles
        # |ψ⟩ = α|0⟩ + β|1⟩ can be prepared using Ry and Rz gates
        theta = 2 * np.arctan2(abs(beta), abs(alpha))
        phi = np.angle(alpha) - np.angle(beta)
        
        # Apply rotations
        qc.ry(theta, qr[0])
        if abs(phi) > 1e-10:  # Only apply if phase is significant
            qc.rz(phi, qr[0])
        
        qc.measure(qr[0], cr[0])
        
        return qc
    
    def authenticate_device(self, device_id: str, backend=None, 
                           use_noise: bool = False) -> Dict:
        """
        Authenticate a device using quantum identity verification.
        
        Implements the authentication protocol from Section IV.
        
        Args:
            device_id: Device to authenticate
            backend: Qiskit backend (None for default simulator)
            use_noise: Whether to use noisy simulation
            
        Returns:
            Dictionary with authentication results
        """
        if device_id not in self.device_registry:
            raise ValueError(f"Device {device_id} not registered")
        
        identity = self.device_registry[device_id]
        expected_p0 = identity['p0']
        expected_p1 = identity['p1']
        
        # Create authentication circuit
        qc = self.prepare_qid_circuit(device_id)
        
        # Select backend
        if backend is None:
            if use_noise:
                # Use noisy simulator with basic noise model
                try:
                    from qiskit_aer.noise import NoiseModel, depolarizing_error
                    noise_model = NoiseModel()
                    error = depolarizing_error(0.01, 1)
                    noise_model.add_all_qubit_quantum_error(error, ['ry', 'rz'])
                    backend = AerSimulator(noise_model=noise_model)
                except:
                    print("Warning: Could not create noise model, using ideal simulator")
                    backend = AerSimulator()
            else:
                backend = AerSimulator()
        
        # Execute circuit multiple rounds
        total_0_count = 0
        total_1_count = 0
        total_shots = self.rounds * self.shots
        
        # Transpile once for efficiency
        transpiled_qc = transpile(qc, backend)
        
        for _ in range(self.rounds):
            job = backend.run(transpiled_qc, shots=self.shots)
            result = job.result()
            counts = result.get_counts()
            
            total_0_count += counts.get('0', 0)
            total_1_count += counts.get('1', 0)
        
        # Calculate observed probabilities
        observed_p0 = total_0_count / total_shots
        observed_p1 = total_1_count / total_shots
        
        # Calculate deviations
        dev_0 = abs(observed_p0 - expected_p0)
        dev_1 = abs(observed_p1 - expected_p1)
        max_deviation = max(dev_0, dev_1)
        
        # Authentication decision (Eq. 3 - Hoeffding bound)
        success = max_deviation <= self.threshold
        
        result = {
            'device_id': device_id,
            'success': success,
            'observed_p0': observed_p0,
            'observed_p1': observed_p1,
            'expected_p0': expected_p0,
            'expected_p1': expected_p1,
            'deviation_p0': dev_0,
            'deviation_p1': dev_1,
            'max_deviation': max_deviation,
            'threshold': self.threshold,
            'rounds': self.rounds,
            'total_shots': total_shots
        }
        
        return result
    
    def save_registry(self, filename: str):
        """Save device registry to JSON file."""
        # Convert complex numbers to dict for JSON serialization
        registry_json = {}
        for device_id, identity in self.device_registry.items():
            registry_json[device_id] = {
                'serial': identity['serial'],
                'alpha_real': identity['alpha'].real,
                'alpha_imag': identity['alpha'].imag,
                'beta_real': identity['beta'].real,
                'beta_imag': identity['beta'].imag,
                'p0': identity['p0'],
                'p1': identity['p1']
            }
        
        with open(filename, 'w') as f:
            json.dump(registry_json, f, indent=2)
        
        print(f"✓ Saved registry to {filename}")
    
    def load_registry(self, filename: str):
        """Load device registry from JSON file."""
        with open(filename, 'r') as f:
            registry_json = json.load(f)
        
        # Convert dict back to complex numbers
        self.device_registry = {}
        for device_id, identity in registry_json.items():
            self.device_registry[device_id] = {
                'serial': identity['serial'],
                'alpha': complex(identity['alpha_real'], identity['alpha_imag']),
                'beta': complex(identity['beta_real'], identity['beta_imag']),
                'p0': identity['p0'],
                'p1': identity['p1']
            }
        
        print(f"✓ Loaded {len(self.device_registry)} devices from {filename}")


def main():
    """Example usage of QuantumAuthenticator."""
    print("=" * 60)
    print("Quantum Authentication Protocol Demo")
    print("=" * 60)
    
    # Initialize authenticator
    auth = QuantumAuthenticator(config={
        'rounds': 100,
        'threshold': 0.05,
        'shots': 1024
    })
    
    # Register test devices (as in paper Table 1)
    print("\n1. Registering Devices...")
    for i in range(1, 6):
        device_id = f"Device{i:02d}"
        device_serial = f"IIoT-SN-{1000 + i}"
        auth.register_device(device_id, device_serial)
    
    # Authenticate devices
    print("\n2. Authenticating Devices...")
    print("-" * 60)
    
    for device_id in list(auth.device_registry.keys())[:2]:  # Test first 2
        print(f"\nAuthenticating {device_id}...")
        
        # Test on simulator
        result = auth.authenticate_device(device_id, use_noise=False)
        
        status = "✓ ACCEPTED" if result['success'] else "✗ REJECTED"
        print(f"  Status: {status}")
        print(f"  Expected: p0={result['expected_p0']:.4f}, p1={result['expected_p1']:.4f}")
        print(f"  Observed: p0={result['observed_p0']:.4f}, p1={result['observed_p1']:.4f}")
        print(f"  Deviation: {result['max_deviation']:.6f} (threshold: {result['threshold']})")
    
    print("\n" + "=" * 60)
    print("Authentication Protocol Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
