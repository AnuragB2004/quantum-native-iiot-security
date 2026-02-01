"""
Complete Quantum-Native IIoT Security Protocol

Integrates quantum authentication, BB84 QKD, and entanglement-based tamper
detection into a unified security protocol.

Author: Anurag Bhattacharjee
Date: February 2026
"""

import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from quantum_auth import QuantumAuthenticator
from bb84_qkd import BB84Protocol
from entanglement_tamper import EntanglementTamperDetector


class QuantumNativeIIoTProtocol:
    """
    Complete quantum-native security protocol for IIoT systems.
    
    Implements Algorithm 1 from the paper, integrating:
    1. Quantum Authentication (Phase 1)
    2. BB84 Key Distribution (Phase 2)
    3. Entanglement-Based Tamper Detection (Phase 3)
    4. Encrypted Classical Communication (Phase 4)
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the complete protocol.
        
        Args:
            config: Configuration dictionary for all protocol phases
        """
        self.config = config or self._load_default_config()
        
        # Initialize protocol components
        self.authenticator = QuantumAuthenticator(
            config=self.config.get('authentication', {})
        )
        self.qkd = BB84Protocol(
            config=self.config.get('bb84', {})
        )
        self.tamper_detector = EntanglementTamperDetector(
            config=self.config.get('entanglement', {})
        )
        
        # Protocol state
        self.session_active = False
        self.session_key = None
        self.authenticated_devices = set()
        
    def _load_default_config(self) -> Dict:
        """Load default configuration."""
        return {
            'authentication': {
                'rounds': 100,
                'threshold': 0.05,
                'shots': 1024
            },
            'bb84': {
                'key_length': 256,
                'qber_threshold': 0.11,
                'test_fraction': 0.5,
                'shots': 1024
            },
            'entanglement': {
                'trials': 50,
                'shots': 4096,
                'fidelity_threshold': 0.85,
                'chsh_threshold': 2.0
            },
            'execution': {
                'mode': 'simulator',
                'backend': None,
                'optimization_level': 3
            }
        }
    
    def run_complete_protocol(self, device_id: str, 
                             backend=None,
                             attack_model: Optional[str] = None) -> Dict:
        """
        Execute the complete quantum-native security protocol.
        
        Implements Algorithm 1 from Section VI of the paper.
        
        Args:
            device_id: Device to authenticate and establish session with
            backend: Qiskit backend for execution
            attack_model: Attack type to simulate (None, 'eavesdrop', 'tamper')
            
        Returns:
            Dictionary with complete protocol results
        """
        print("\n" + "=" * 70)
        print(" QUANTUM-NATIVE IIoT SECURITY PROTOCOL")
        print("=" * 70)
        print(f"\nDevice: {device_id}")
        print(f"Mode: {self.config['execution']['mode']}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if attack_model:
            print(f"⚠ Attack Model: {attack_model}")
        print("=" * 70)
        
        protocol_results = {
            'device_id': device_id,
            'timestamp': datetime.now().isoformat(),
            'attack_model': attack_model,
            'phases': {}
        }
        
        # ====================================================================
        # PHASE 1: QUANTUM AUTHENTICATION
        # ====================================================================
        print("\n" + "▶" * 35)
        print("PHASE 1: QUANTUM AUTHENTICATION")
        print("▶" * 35)
        
        start_time = time.time()
        
        auth_result = self.authenticator.authenticate_device(
            device_id, 
            backend=backend,
            use_noise=(attack_model == 'tamper')
        )
        
        auth_time = time.time() - start_time
        protocol_results['phases']['authentication'] = {
            **auth_result,
            'execution_time_seconds': auth_time
        }
        
        print(f"\n{'✓' if auth_result['success'] else '✗'} Authentication: "
              f"{'PASSED' if auth_result['success'] else 'FAILED'}")
        print(f"  Time: {auth_time:.2f} seconds")
        
        if not auth_result['success']:
            print("\n✗ PROTOCOL ABORTED: Authentication failed")
            protocol_results['overall_success'] = False
            protocol_results['abort_reason'] = 'Authentication failure'
            return protocol_results
        
        self.authenticated_devices.add(device_id)
        
        # ====================================================================
        # PHASE 2: BB84 QUANTUM KEY DISTRIBUTION
        # ====================================================================
        print("\n" + "▶" * 35)
        print("PHASE 2: BB84 QUANTUM KEY DISTRIBUTION")
        print("▶" * 35)
        
        start_time = time.time()
        
        qkd_result = self.qkd.run_protocol(
            backend=backend,
            attack_model='eavesdrop' if attack_model == 'eavesdrop' else None
        )
        
        qkd_time = time.time() - start_time
        protocol_results['phases']['qkd'] = {
            **qkd_result,
            'execution_time_seconds': qkd_time
        }
        
        print(f"\nTime: {qkd_time:.2f} seconds")
        
        if not qkd_result['success']:
            print("\n✗ PROTOCOL ABORTED: QKD failed (possible eavesdropping)")
            protocol_results['overall_success'] = False
            protocol_results['abort_reason'] = qkd_result.get('reason', 'QKD failure')
            return protocol_results
        
        self.session_key = qkd_result['final_key']
        
        # ====================================================================
        # PHASE 3: ENTANGLEMENT-BASED TAMPER DETECTION
        # ====================================================================
        print("\n" + "▶" * 35)
        print("PHASE 3: ENTANGLEMENT-BASED TAMPER DETECTION")
        print("▶" * 35)
        
        start_time = time.time()
        
        tamper_result = self.tamper_detector.verify_entanglement(
            backend=backend,
            add_noise=(attack_model == 'tamper')
        )
        
        tamper_time = time.time() - start_time
        protocol_results['phases']['tamper_detection'] = {
            **tamper_result,
            'execution_time_seconds': tamper_time
        }
        
        print(f"\n{'✓' if not tamper_result['tampering_detected'] else '⚠'} Status: "
              f"{tamper_result['status']}")
        print(f"  Time: {tamper_time:.2f} seconds")
        
        if tamper_result['tampering_detected']:
            print("\n⚠ WARNING: Tampering detected - Invalidating session key")
            self.session_key = None
            protocol_results['overall_success'] = False
            protocol_results['abort_reason'] = 'Tampering detected'
            return protocol_results
        
        # ====================================================================
        # PHASE 4: ENCRYPTED CLASSICAL COMMUNICATION
        # ====================================================================
        print("\n" + "▶" * 35)
        print("PHASE 4: ENCRYPTED CLASSICAL COMMUNICATION")
        print("▶" * 35)
        
        print(f"\n✓ Session established successfully")
        print(f"  Session key: {len(self.session_key)}-bit AES key")
        print(f"  Encryption: AES-256-GCM with quantum-derived key")
        print(f"  Status: READY for secure IIoT traffic")
        
        self.session_active = True
        
        protocol_results['phases']['encrypted_communication'] = {
            'status': 'ready',
            'key_length_bits': len(self.session_key),
            'encryption_algorithm': 'AES-256-GCM'
        }
        
        # ====================================================================
        # PROTOCOL SUMMARY
        # ====================================================================
        total_time = (auth_time + qkd_time + tamper_time)
        
        print("\n" + "=" * 70)
        print(" PROTOCOL EXECUTION SUMMARY")
        print("=" * 70)
        print(f"  Phase 1 (Authentication):     {auth_time:.2f}s")
        print(f"  Phase 2 (QKD):                 {qkd_time:.2f}s")
        print(f"  Phase 3 (Tamper Detection):    {tamper_time:.2f}s")
        print(f"  Total Time:                    {total_time:.2f}s")
        print("=" * 70)
        print(f"\n{'✓' * 3} SECURE SESSION ESTABLISHED {'✓' * 3}\n")
        
        protocol_results['overall_success'] = True
        protocol_results['total_execution_time_seconds'] = total_time
        
        return protocol_results
    
    def save_results(self, results: Dict, output_dir: str = 'outputs'):
        """Save protocol results to JSON file."""
        output_path = Path(output_dir) / 'logs'
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = output_path / f"protocol_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n✓ Results saved to: {filename}")
        
        return filename


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description='Quantum-Native IIoT Security Protocol',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run on simulator
  python run_protocol.py --mode simulator --device-id Device01
  
  # Run with eavesdropping attack
  python run_protocol.py --mode simulator --attack eavesdrop
  
  # Run on IBM hardware
  python run_protocol.py --mode hardware --backend ibm_brisbane --device-id Device01
        """
    )
    
    parser.add_argument('--device-id', type=str, default='Device01',
                       help='Device ID to authenticate')
    parser.add_argument('--mode', type=str, 
                       choices=['simulator', 'noisy', 'hardware'],
                       default='simulator',
                       help='Execution mode')
    parser.add_argument('--backend', type=str, default=None,
                       help='IBM Quantum backend name (for hardware mode)')
    parser.add_argument('--attack', type=str, 
                       choices=['eavesdrop', 'tamper', None],
                       default=None,
                       help='Attack model to simulate')
    parser.add_argument('--config', type=str, default=None,
                       help='Path to custom configuration file')
    parser.add_argument('--save-results', action='store_true',
                       help='Save results to JSON file')
    
    args = parser.parse_args()
    
    # Load configuration
    if args.config:
        with open(args.config, 'r') as f:
            import yaml
            config = yaml.safe_load(f)
    else:
        config = None
    
    # Initialize protocol
    protocol = QuantumNativeIIoTProtocol(config=config)
    
    # Register devices
    print("Registering devices...")
    for i in range(1, 6):
        device_id = f"Device{i:02d}"
        device_serial = f"IIoT-SN-{1000 + i}"
        protocol.authenticator.register_device(device_id, device_serial)
    
    # Get backend
    backend = None
    if args.mode == 'hardware':
        if args.backend is None:
            print("Error: --backend required for hardware mode")
            return
        
        try:
            from qiskit_ibm_runtime import QiskitRuntimeService
            service = QiskitRuntimeService()
            backend = service.backend(args.backend)
            print(f"Using backend: {args.backend}")
        except Exception as e:
            print(f"Error loading backend: {e}")
            return
    elif args.mode == 'noisy':
        from qiskit_ibm_runtime.fake_provider import FakeManilaV2
        backend = FakeManilaV2()
        print("Using noisy simulator (FakeManilaV2)")
    
    # Run protocol
    results = protocol.run_complete_protocol(
        device_id=args.device_id,
        backend=backend,
        attack_model=args.attack
    )
    
    # Save results if requested
    if args.save_results:
        protocol.save_results(results)


if __name__ == "__main__":
    main()
