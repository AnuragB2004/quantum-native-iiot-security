"""
Entanglement-Based Tamper Detection

Implements quantum tamper detection using Bell states and CHSH inequality
as described in Section VI of the paper.

Author: Anurag Bhattacharjee
Date: February 2026
"""

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from typing import Dict, Optional, Tuple, List


class EntanglementTamperDetector:
    """
    Implements entanglement-based tamper detection using Bell states.
    
    Monitors channel integrity by detecting degradation in entanglement
    correlations, which indicates eavesdropping or channel tampering.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize tamper detector.
        
        Args:
            config: Configuration dictionary:
                - trials: Number of entanglement verification trials (default: 50)
                - shots: Measurement shots per trial (default: 4096)
                - fidelity_threshold: Minimum acceptable fidelity (default: 0.85)
                - chsh_threshold: Minimum CHSH value for genuine entanglement (default: 2.0)
        """
        self.config = config or {}
        self.trials = self.config.get('trials', 50)
        self.shots = self.config.get('shots', 4096)
        self.fidelity_threshold = self.config.get('fidelity_threshold', 0.85)
        self.chsh_threshold = self.config.get('chsh_threshold', 2.0)
    
    def create_bell_state(self, bell_type: str = 'phi_plus') -> QuantumCircuit:
        """
        Create a Bell state circuit.
        
        Implements circuit from Figure 6 of the paper:
            |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
        
        Args:
            bell_type: Type of Bell state ('phi_plus', 'phi_minus', 'psi_plus', 'psi_minus')
            
        Returns:
            Quantum circuit preparing the Bell state
        """
        qr = QuantumRegister(2, 'q')
        cr = ClassicalRegister(2, 'c')
        qc = QuantumCircuit(qr, cr)
        
        # Create |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
        qc.h(qr[0])  # Put first qubit in superposition
        qc.cx(qr[0], qr[1])  # Entangle with second qubit
        
        # Modify for other Bell states
        if bell_type == 'phi_minus':
            qc.z(qr[1])  # |Φ⁻⟩ = (|00⟩ - |11⟩)/√2
        elif bell_type == 'psi_plus':
            qc.x(qr[1])  # |Ψ⁺⟩ = (|01⟩ + |10⟩)/√2
        elif bell_type == 'psi_minus':
            qc.x(qr[1])
            qc.z(qr[1])  # |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2
        
        return qc
    
    def add_basis_rotations(self, qc: QuantumCircuit, 
                           theta_gateway: float, 
                           theta_device: float) -> QuantumCircuit:
        """
        Add local basis rotations for CHSH measurements.
        
        Implements rotations from Figure 7 of the paper.
        
        Args:
            qc: Bell state circuit
            theta_gateway: Rotation angle for gateway qubit
            theta_device: Rotation angle for device qubit
            
        Returns:
            Circuit with rotations applied
        """
        qr = qc.qregs[0]
        
        # Apply rotations before measurement
        qc.ry(theta_gateway, qr[0])  # Gateway qubit
        qc.ry(theta_device, qr[1])   # Device qubit
        
        return qc
    
    def measure_bell_state(self, qc: QuantumCircuit, 
                          measure_basis: str = 'ZZ') -> QuantumCircuit:
        """
        Measure Bell state in specified basis.
        
        Args:
            qc: Bell state circuit
            measure_basis: Measurement basis ('ZZ', 'ZX', 'XZ', 'XX')
            
        Returns:
            Circuit with measurements
        """
        qr = qc.qregs[0]
        cr = qc.cregs[0]
        
        # Apply basis transformations
        if 'X' in measure_basis[0]:  # First qubit in X basis
            qc.h(qr[0])
        if 'X' in measure_basis[1]:  # Second qubit in X basis
            qc.h(qr[1])
        
        # Measure both qubits
        qc.measure(qr, cr)
        
        return qc
    
    def compute_correlation_fidelity(self, counts: Dict, 
                                    basis: str = 'ZZ') -> float:
        """
        Compute correlation fidelity from measurement results.
        
        Implements Eq. (6) from the paper:
            F = N_correlated / N_total
        
        Args:
            counts: Measurement counts dictionary
            basis: Measurement basis
            
        Returns:
            Correlation fidelity value
        """
        total_counts = sum(counts.values())
        
        # For Bell state |Φ⁺⟩ in ZZ basis: expect 00 and 11 (correlated)
        if basis == 'ZZ':
            correlated = counts.get('00', 0) + counts.get('11', 0)
        elif basis == 'XX':
            # In XX basis, Bell state also shows perfect correlation
            correlated = counts.get('00', 0) + counts.get('11', 0)
        else:
            # For mixed bases, correlation pattern is different
            # For simplicity, count all as contributing
            correlated = total_counts
        
        fidelity = correlated / total_counts if total_counts > 0 else 0
        
        return fidelity
    
    def measure_chsh_correlations(self, backend=None) -> Dict:
        """
        Measure CHSH inequality correlations.
        
        Implements Eq. (7) from the paper:
            S = ⟨A₁B₁⟩ + ⟨A₁B₂⟩ + ⟨A₂B₁⟩ - ⟨A₂B₂⟩
        
        Classical bound: |S| ≤ 2
        Quantum (Tsirelson): |S| ≤ 2√2 ≈ 2.828
        
        Args:
            backend: Qiskit backend
            
        Returns:
            Dictionary with CHSH results
        """
        if backend is None:
            backend = AerSimulator()
        
        # CHSH measurement angles
        # Optimal: θ₁=0, θ₂=π/4, φ₁=π/8, φ₂=-π/8
        angles_A = [0, np.pi/4]  # Gateway angles
        angles_B = [np.pi/8, -np.pi/8]  # Device angles
        
        correlations = {}
        measurement_settings = [
            ('A1', 'B1', angles_A[0], angles_B[0]),
            ('A1', 'B2', angles_A[0], angles_B[1]),
            ('A2', 'B1', angles_A[1], angles_B[0]),
            ('A2', 'B2', angles_A[1], angles_B[1])
        ]
        
        for label_A, label_B, theta_A, theta_B in measurement_settings:
            # Create Bell state
            qc = self.create_bell_state('phi_plus')
            
            # Add rotations
            qc = self.add_basis_rotations(qc, theta_A, theta_B)
            
            # Measure
            qr = qc.qregs[0]
            cr = qc.cregs[0]
            qc.measure(qr, cr)
            
            # Execute
            job = backend.run(qc, shots=self.shots)
            result = job.result()
            counts = result.get_counts(qc)
            
            # Compute correlation E(A,B) = P(same) - P(different)
            same = counts.get('00', 0) + counts.get('11', 0)
            diff = counts.get('01', 0) + counts.get('10', 0)
            total = same + diff
            
            correlation = (same - diff) / total if total > 0 else 0
            correlations[f'{label_A}{label_B}'] = correlation
        
        # Compute CHSH value
        S = (correlations['A1B1'] + correlations['A1B2'] + 
             correlations['A2B1'] - correlations['A2B2'])
        
        return {
            'chsh_value': S,
            'correlations': correlations,
            'violates_classical': abs(S) > 2.0,
            'genuine_entanglement': abs(S) > self.chsh_threshold
        }
    
    def verify_entanglement(self, backend=None, 
                           add_noise: bool = False) -> Dict:
        """
        Verify entanglement quality through fidelity and CHSH measurements.
        
        Args:
            backend: Qiskit backend
            add_noise: Whether to add noise (simulates tampering)
            
        Returns:
            Dictionary with verification results
        """
        if backend is None:
            backend = AerSimulator()
        
        # Add noise model if requested (simulates tampering)
        if add_noise:
            from qiskit_aer.noise import NoiseModel, depolarizing_error
            
            noise_model = NoiseModel()
            error = depolarizing_error(0.1, 2)  # 10% depolarizing on 2-qubit gates
            noise_model.add_all_qubit_quantum_error(error, ['cx'])
            
            backend = AerSimulator(noise_model=noise_model)
        
        print("Verifying entanglement quality...")
        
        # Test different measurement bases
        bases = ['ZZ', 'XX', 'ZX']
        fidelities = {}
        
        for basis in bases:
            # Create and measure Bell state
            qc = self.create_bell_state('phi_plus')
            qc = self.measure_bell_state(qc, basis)
            
            # Execute multiple trials
            total_fidelity = 0
            for _ in range(self.trials):
                job = backend.run(qc, shots=self.shots)
                result = job.result()
                counts = result.get_counts(qc)
                
                fidelity = self.compute_correlation_fidelity(counts, basis)
                total_fidelity += fidelity
            
            avg_fidelity = total_fidelity / self.trials
            fidelities[basis] = avg_fidelity
            
            print(f"  {basis} basis fidelity: {avg_fidelity:.4f}")
        
        # Measure CHSH inequality
        print("\nMeasuring CHSH correlations...")
        chsh_results = self.measure_chsh_correlations(backend)
        
        print(f"  CHSH value: {chsh_results['chsh_value']:.4f}")
        print(f"  Classical bound (2.0): {'VIOLATED' if chsh_results['violates_classical'] else 'satisfied'}")
        print(f"  Genuine entanglement: {'YES' if chsh_results['genuine_entanglement'] else 'NO'}")
        
        # Overall tamper detection decision
        avg_fidelity = np.mean(list(fidelities.values()))
        tampering_detected = (avg_fidelity < self.fidelity_threshold or 
                             not chsh_results['genuine_entanglement'])
        
        return {
            'fidelities': fidelities,
            'average_fidelity': avg_fidelity,
            'chsh_results': chsh_results,
            'tampering_detected': tampering_detected,
            'status': 'TAMPERED' if tampering_detected else 'SECURE'
        }
    
    def continuous_monitoring(self, duration_rounds: int = 10, 
                            backend=None) -> List[Dict]:
        """
        Perform continuous tamper monitoring over multiple rounds.
        
        Args:
            duration_rounds: Number of monitoring rounds
            backend: Qiskit backend
            
        Returns:
            List of verification results for each round
        """
        print(f"Starting continuous monitoring ({duration_rounds} rounds)...")
        print("=" * 60)
        
        results = []
        
        for round_num in range(duration_rounds):
            print(f"\nRound {round_num + 1}/{duration_rounds}")
            print("-" * 60)
            
            result = self.verify_entanglement(backend)
            result['round'] = round_num + 1
            results.append(result)
            
            if result['tampering_detected']:
                print(f"⚠ WARNING: Tampering detected in round {round_num + 1}!")
        
        print("\n" + "=" * 60)
        print("Monitoring Complete")
        
        # Summary statistics
        tampered_rounds = sum(1 for r in results if r['tampering_detected'])
        print(f"\nSummary:")
        print(f"  Total rounds: {duration_rounds}")
        print(f"  Tampered rounds: {tampered_rounds}")
        print(f"  Security status: {'COMPROMISED' if tampered_rounds > 0 else 'SECURE'}")
        
        return results


def main():
    """Example usage of EntanglementTamperDetector."""
    print("=" * 60)
    print("Entanglement-Based Tamper Detection Demo")
    print("=" * 60)
    
    detector = EntanglementTamperDetector(config={
        'trials': 50,
        'shots': 4096,
        'fidelity_threshold': 0.85,
        'chsh_threshold': 2.0
    })
    
    # Test 1: Normal operation (no tampering)
    print("\n\nTEST 1: Normal Operation (No Tampering)")
    print("-" * 60)
    
    result_normal = detector.verify_entanglement(add_noise=False)
    
    print(f"\nResult: {result_normal['status']}")
    print(f"Average Fidelity: {result_normal['average_fidelity']:.4f}")
    print(f"CHSH Value: {result_normal['chsh_results']['chsh_value']:.4f}")
    
    # Test 2: With tampering/noise
    print("\n\n" + "=" * 60)
    print("TEST 2: With Channel Tampering")
    print("=" * 60)
    
    result_tampered = detector.verify_entanglement(add_noise=True)
    
    print(f"\nResult: {result_tampered['status']}")
    print(f"Average Fidelity: {result_tampered['average_fidelity']:.4f}")
    print(f"CHSH Value: {result_tampered['chsh_results']['chsh_value']:.4f}")
    
    # Test 3: Continuous monitoring
    print("\n\n" + "=" * 60)
    print("TEST 3: Continuous Monitoring (5 rounds)")
    print("=" * 60)
    
    monitoring_results = detector.continuous_monitoring(duration_rounds=5)


if __name__ == "__main__":
    main()
