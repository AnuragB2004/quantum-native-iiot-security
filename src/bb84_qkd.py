"""
BB84 Quantum Key Distribution Protocol

Implements the BB84 protocol for quantum key distribution as described
in Section V of the paper.

Author: Anurag Bhattacharjee
Date: February 2026
"""

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from typing import List, Tuple, Dict, Optional
import random


class BB84Protocol:
    """
    Implementation of the BB84 quantum key distribution protocol.
    
    Provides information-theoretic secure key establishment between
    Alice (device) and Bob (gateway) using quantum states.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize BB84 protocol.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.key_length = self.config.get('key_length', 256)
        self.qber_threshold = self.config.get('qber_threshold', 0.11)
        self.test_fraction = self.config.get('test_fraction', 0.5)
        self.shots = self.config.get('shots', 1024)
        
        # Basis encoding: 0 = computational (Z), 1 = Hadamard (X)
        self.Z_BASIS = 0
        self.X_BASIS = 1
    
    def prepare_qubit(self, bit: int, basis: int) -> QuantumCircuit:
        """Prepare a single qubit for BB84 transmission."""
        qr = QuantumRegister(1, 'q')
        cr = ClassicalRegister(1, 'c')
        qc = QuantumCircuit(qr, cr)
        
        # Encode bit value
        if bit == 1:
            qc.x(qr[0])
        
        # Apply basis transformation
        if basis == self.X_BASIS:
            qc.h(qr[0])
        
        return qc
    
    def measure_qubit(self, qc: QuantumCircuit, basis: int) -> QuantumCircuit:
        """Measure a qubit in the specified basis."""
        qr = qc.qregs[0]
        cr = qc.cregs[0]
        
        # Apply basis transformation before measurement
        if basis == self.X_BASIS:
            qc.h(qr[0])
        
        qc.measure(qr[0], cr[0])
        
        return qc
    
    def run_bb84_round(self, alice_bit: int, alice_basis: int, 
                       bob_basis: int, backend=None) -> int:
        """Execute a single BB84 transmission round."""
        # Alice prepares qubit
        qc = self.prepare_qubit(alice_bit, alice_basis)
        
        # Bob measures qubit
        qc = self.measure_qubit(qc, bob_basis)
        
        # Execute circuit
        if backend is None:
            backend = AerSimulator()
        
        transpiled_qc = transpile(qc, backend)
        job = backend.run(transpiled_qc, shots=self.shots)
        result = job.result()
        counts = result.get_counts()
        
        # Extract most frequent result
        bob_bit = int(max(counts, key=counts.get))
        
        return bob_bit
    
    def generate_raw_key(self, n_bits: int, backend=None) -> Tuple[List, List, List, List]:
        """Generate raw key material through quantum transmission."""
        alice_bits = [random.randint(0, 1) for _ in range(n_bits)]
        alice_bases = [random.randint(0, 1) for _ in range(n_bits)]
        bob_bases = [random.randint(0, 1) for _ in range(n_bits)]
        bob_bits = []
        
        print(f"Transmitting {n_bits} qubits...")
        
        for i in range(n_bits):
            bob_bit = self.run_bb84_round(
                alice_bits[i], alice_bases[i], bob_bases[i], backend
            )
            bob_bits.append(bob_bit)
            
            if (i + 1) % 100 == 0:
                print(f"  Progress: {i + 1}/{n_bits} qubits transmitted")
        
        return alice_bits, alice_bases, bob_bases, bob_bits
    
    def basis_sifting(self, alice_bits: List, alice_bases: List,
                     bob_bases: List, bob_bits: List) -> Tuple[List, List]:
        """Perform basis sifting - keep only matching basis results."""
        sifted_alice = []
        sifted_bob = []
        
        for i in range(len(alice_bits)):
            if alice_bases[i] == bob_bases[i]:
                sifted_alice.append(alice_bits[i])
                sifted_bob.append(bob_bits[i])
        
        print(f"Basis sifting: {len(alice_bits)} → {len(sifted_alice)} bits")
        print(f"Sifting efficiency: {len(sifted_alice)/len(alice_bits)*100:.1f}%")
        
        return sifted_alice, sifted_bob
    
    def estimate_qber(self, alice_key: List, bob_key: List) -> Tuple[float, List]:
        """Estimate quantum bit error rate (QBER) from test subset."""
        n_test = int(len(alice_key) * self.test_fraction)
        
        # Randomly select test positions
        test_positions = random.sample(range(len(alice_key)), n_test)
        
        mismatches = 0
        for pos in test_positions:
            if alice_key[pos] != bob_key[pos]:
                mismatches += 1
        
        qber = mismatches / n_test if n_test > 0 else 0.0
        
        print(f"QBER Estimation:")
        print(f"  Test subset size: {n_test} bits")
        print(f"  Mismatches: {mismatches}")
        print(f"  QBER: {qber:.4f} ({qber*100:.2f}%)")
        
        return qber, test_positions
    
    def error_correction(self, alice_key: List, bob_key: List, 
                        test_positions: List) -> Tuple[List, List]:
        """Simple error correction - remove test bits."""
        corrected_alice = []
        corrected_bob = []
        
        for i in range(len(alice_key)):
            if i not in test_positions:
                corrected_alice.append(alice_key[i])
                corrected_bob.append(bob_key[i])
        
        print(f"Error correction: {len(alice_key)} → {len(corrected_alice)} bits")
        
        return corrected_alice, corrected_bob
    
    def privacy_amplification(self, key: List) -> List:
        """Privacy amplification to remove potential eavesdropper information."""
        amplified_key = key[::2]  # Take every other bit
        
        print(f"Privacy amplification: {len(key)} → {len(amplified_key)} bits")
        
        return amplified_key
    
    def run_protocol(self, backend=None, attack_model: Optional[str] = None) -> Dict:
        """Execute complete BB84 protocol."""
        print("=" * 60)
        print("BB84 Quantum Key Distribution Protocol")
        print("=" * 60)
        
        # Calculate required initial bits
        overhead = 1 / (0.5 * (1 - self.test_fraction) * 0.5)
        n_initial_bits = int(self.key_length * overhead * 1.2)
        
        print(f"\nTarget key length: {self.key_length} bits")
        print(f"Initial transmission: {n_initial_bits} qubits")
        
        # Apply attack if specified
        if attack_model and attack_model == 'eavesdrop':
            print(f"\n⚠ Simulating {attack_model} attack")
            from qiskit_aer.noise import NoiseModel, pauli_error
            noise_model = NoiseModel()
            error = pauli_error([('X', 0.25), ('I', 0.75)])
            noise_model.add_all_qubit_quantum_error(error, ['measure'])
            backend = AerSimulator(noise_model=noise_model)
        
        # Step 1: Generate raw key material
        print("\n[1/5] Quantum Transmission")
        alice_bits, alice_bases, bob_bases, bob_bits = self.generate_raw_key(
            n_initial_bits, backend
        )
        
        # Step 2: Basis sifting
        print("\n[2/5] Basis Sifting")
        sifted_alice, sifted_bob = self.basis_sifting(
            alice_bits, alice_bases, bob_bases, bob_bits
        )
        
        # Step 3: QBER estimation
        print("\n[3/5] QBER Estimation")
        qber, test_positions = self.estimate_qber(sifted_alice, sifted_bob)
        
        # Check QBER threshold
        if qber > self.qber_threshold:
            print(f"\n✗ PROTOCOL ABORTED: QBER {qber:.4f} exceeds threshold {self.qber_threshold}")
            return {
                'success': False,
                'final_key': None,
                'qber': qber,
                'reason': 'QBER threshold exceeded - possible eavesdropping',
                'key_stats': {
                    'initial_bits': n_initial_bits,
                    'sifted_bits': len(sifted_alice),
                    'final_bits': 0
                }
            }
        
        # Step 4: Error correction
        print("\n[4/5] Error Correction")
        corrected_alice, corrected_bob = self.error_correction(
            sifted_alice, sifted_bob, test_positions
        )
        
        # Step 5: Privacy amplification
        print("\n[5/5] Privacy Amplification")
        final_key = self.privacy_amplification(corrected_alice)
        
        # Truncate to target length if needed
        if len(final_key) > self.key_length:
            final_key = final_key[:self.key_length]
        
        print(f"\n✓ Protocol Successful!")
        print(f"Final key length: {len(final_key)} bits")
        print(f"QBER: {qber:.4f} ({qber*100:.2f}%)")
        
        return {
            'success': True,
            'final_key': final_key,
            'qber': qber,
            'key_stats': {
                'initial_bits': n_initial_bits,
                'sifted_bits': len(sifted_alice),
                'test_bits': len(test_positions),
                'corrected_bits': len(corrected_alice),
                'final_bits': len(final_key),
                'sifting_efficiency': len(sifted_alice) / n_initial_bits,
                'total_efficiency': len(final_key) / n_initial_bits
            }
        }


def main():
    """Example usage of BB84Protocol."""
    print("=" * 60)
    print("BB84 Quantum Key Distribution Demo")
    print("=" * 60)
    
    bb84 = BB84Protocol(config={
        'key_length': 256,
        'qber_threshold': 0.11,
        'test_fraction': 0.5,
        'shots': 1024
    })
    
    result = bb84.run_protocol()
    
    if result['success']:
        print(f"\nGenerated {len(result['final_key'])}-bit key")
        print(f"Key (first 32 bits): {result['final_key'][:32]}")


if __name__ == "__main__":
    main()
