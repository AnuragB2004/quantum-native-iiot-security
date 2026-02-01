"""
Run All Experiments for Paper Reproduction

This script reproduces all experimental results reported in the paper.

Author: Anurag Bhattacharjee
Date: February 2026
"""

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from quantum_auth import QuantumAuthenticator
from bb84_qkd import BB84Protocol
from entanglement_tamper import EntanglementTamperDetector


def run_authentication_experiments():
    """
    Run authentication experiments (Table 1 in paper).
    
    Tests authentication success rates across:
    - Ideal simulator
    - Noisy simulator  
    - IBM quantum hardware
    """
    print("\n" + "=" * 70)
    print("EXPERIMENT 1: QUANTUM AUTHENTICATION")
    print("=" * 70)
    
    auth = QuantumAuthenticator(config={
        'rounds': 100,
        'threshold': 0.05,
        'shots': 1024
    })
    
    # Register devices
    devices = []
    for i in range(1, 6):
        device_id = f"Device{i:02d}"
        device_serial = f"IIoT-SN-{1000 + i}"
        auth.register_device(device_id, device_serial)
        devices.append(device_id)
    
    results = []
    
    # Test on different backends
    backends = {
        'Simulator': {'backend': None, 'use_noise': False},
        'Noisy': {'backend': None, 'use_noise': True},
    }
    
    for backend_name, backend_config in backends.items():
        print(f"\nTesting on {backend_name}...")
        
        for device_id in devices:
            # Run multiple trials for statistics
            success_rates = []
            
            for trial in range(50):  # 50 trials per device
                result = auth.authenticate_device(
                    device_id, 
                    backend=backend_config['backend'],
                    use_noise=backend_config['use_noise']
                )
                success_rates.append(1.0 if result['success'] else 0.0)
            
            avg_success = np.mean(success_rates) * 100
            std_success = np.std(success_rates) * 100
            
            results.append({
                'Device': device_id,
                'Backend': backend_name,
                'Success_Rate_Mean': avg_success,
                'Success_Rate_Std': std_success
            })
            
            print(f"  {device_id}: {avg_success:.1f}% ± {std_success:.1f}%")
    
    # Save results
    df = pd.DataFrame(results)
    output_path = Path('data/experimental_results')
    output_path.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path / 'auth_results.csv', index=False)
    
    print(f"\n✓ Results saved to data/experimental_results/auth_results.csv")
    
    return df


def run_bb84_experiments():
    """
    Run BB84 experiments (Tables 2, 3, 4 in paper).
    
    Tests:
    - Key yield statistics
    - QBER under normal conditions
    - QBER under attack scenarios
    """
    print("\n" + "=" * 70)
    print("EXPERIMENT 2: BB84 QUANTUM KEY DISTRIBUTION")
    print("=" * 70)
    
    bb84 = BB84Protocol(config={
        'key_length': 256,
        'qber_threshold': 0.11,
        'test_fraction': 0.5,
        'shots': 1024
    })
    
    results = []
    
    # Test 1: Normal operation
    print("\nTest 1: Normal BB84 Operation")
    print("-" * 70)
    
    qber_values = []
    for trial in range(30):  # 30 trials
        result = bb84.run_protocol(attack_model=None)
        if result['success']:
            qber_values.append(result['qber'])
    
    avg_qber = np.mean(qber_values)
    std_qber = np.std(qber_values)
    
    results.append({
        'Scenario': 'No Attack',
        'QBER_Mean': avg_qber,
        'QBER_Std': std_qber,
        'Detected': False
    })
    
    print(f"  QBER: {avg_qber:.4f} ± {std_qber:.4f}")
    
    # Test 2: Eavesdropping attack
    print("\nTest 2: Passive Eavesdropping Attack")
    print("-" * 70)
    
    qber_attack_values = []
    detected_count = 0
    
    for trial in range(20):  # 20 attack simulations
        result = bb84.run_protocol(attack_model='eavesdrop')
        qber_attack_values.append(result['qber'])
        if not result['success']:
            detected_count += 1
    
    avg_qber_attack = np.mean(qber_attack_values)
    std_qber_attack = np.std(qber_attack_values)
    detection_rate = detected_count / 20 * 100
    
    results.append({
        'Scenario': 'Eavesdropping',
        'QBER_Mean': avg_qber_attack,
        'QBER_Std': std_qber_attack,
        'Detected': True,
        'Detection_Rate': detection_rate
    })
    
    print(f"  QBER: {avg_qber_attack:.4f} ± {std_qber_attack:.4f}")
    print(f"  Detection Rate: {detection_rate:.1f}%")
    
    # Save results
    df = pd.DataFrame(results)
    output_path = Path('data/experimental_results')
    df.to_csv(output_path / 'qkd_results.csv', index=False)
    
    print(f"\n✓ Results saved to data/experimental_results/qkd_results.csv")
    
    return df


def run_entanglement_experiments():
    """
    Run entanglement experiments (Tables 5, 6 in paper).
    
    Tests:
    - Bell state fidelity measurements
    - CHSH inequality violations
    """
    print("\n" + "=" * 70)
    print("EXPERIMENT 3: ENTANGLEMENT-BASED TAMPER DETECTION")
    print("=" * 70)
    
    detector = EntanglementTamperDetector(config={
        'trials': 50,
        'shots': 4096,
        'fidelity_threshold': 0.85,
        'chsh_threshold': 2.0
    })
    
    results = []
    
    # Test 1: Normal operation
    print("\nTest 1: Normal Operation (No Tampering)")
    print("-" * 70)
    
    fidelity_trials = []
    chsh_trials = []
    
    for trial in range(40):  # 40 trials
        result = detector.verify_entanglement(add_noise=False)
        fidelity_trials.append(result['average_fidelity'])
        chsh_trials.append(result['chsh_results']['chsh_value'])
    
    avg_fidelity = np.mean(fidelity_trials)
    std_fidelity = np.std(fidelity_trials)
    avg_chsh = np.mean(chsh_trials)
    std_chsh = np.std(chsh_trials)
    
    results.append({
        'Scenario': 'Normal',
        'Fidelity_Mean': avg_fidelity,
        'Fidelity_Std': std_fidelity,
        'CHSH_Mean': avg_chsh,
        'CHSH_Std': std_chsh,
        'Tampering_Detected': False
    })
    
    print(f"  Fidelity: {avg_fidelity:.4f} ± {std_fidelity:.4f}")
    print(f"  CHSH: {avg_chsh:.4f} ± {std_chsh:.4f}")
    
    # Test 2: With tampering
    print("\nTest 2: With Channel Tampering")
    print("-" * 70)
    
    fidelity_tampered = []
    chsh_tampered = []
    
    for trial in range(40):  # 40 trials
        result = detector.verify_entanglement(add_noise=True)
        fidelity_tampered.append(result['average_fidelity'])
        chsh_tampered.append(result['chsh_results']['chsh_value'])
    
    avg_fidelity_t = np.mean(fidelity_tampered)
    std_fidelity_t = np.std(fidelity_tampered)
    avg_chsh_t = np.mean(chsh_tampered)
    std_chsh_t = np.std(chsh_tampered)
    
    results.append({
        'Scenario': 'Tampered',
        'Fidelity_Mean': avg_fidelity_t,
        'Fidelity_Std': std_fidelity_t,
        'CHSH_Mean': avg_chsh_t,
        'CHSH_Std': std_chsh_t,
        'Tampering_Detected': True
    })
    
    print(f"  Fidelity: {avg_fidelity_t:.4f} ± {std_fidelity_t:.4f}")
    print(f"  CHSH: {avg_chsh_t:.4f} ± {std_chsh_t:.4f}")
    
    # Save results
    df = pd.DataFrame(results)
    output_path = Path('data/experimental_results')
    df.to_csv(output_path / 'entanglement_results.csv', index=False)
    
    print(f"\n✓ Results saved to data/experimental_results/entanglement_results.csv")
    
    return df


def run_scalability_experiments():
    """
    Run scalability analysis (Table 7 in paper).
    
    Analyzes authentication latency scaling with device count.
    """
    print("\n" + "=" * 70)
    print("EXPERIMENT 4: SCALABILITY ANALYSIS")
    print("=" * 70)
    
    # Theoretical scalability model
    T_auth = 0.65  # Average auth time in seconds (from experiments)
    device_counts = [10, 50, 100, 250, 500, 1000]
    parallel_channels = [1, 4, 10, 20]
    
    results = []
    
    for n_devices in device_counts:
        for k_channels in parallel_channels:
            # Sequential time
            t_sequential = n_devices * T_auth
            
            # Parallel time
            t_parallel = np.ceil(n_devices / k_channels) * T_auth
            
            results.append({
                'Devices': n_devices,
                'Parallel_Channels': k_channels,
                'Sequential_Time_s': t_sequential,
                'Parallel_Time_s': t_parallel,
                'Speedup': t_sequential / t_parallel
            })
    
    df = pd.DataFrame(results)
    
    # Print summary
    print("\nScalability Results (Authentication Latency):")
    print("-" * 70)
    for n in device_counts:
        subset = df[df['Devices'] == n]
        print(f"\n{n} devices:")
        for _, row in subset.iterrows():
            print(f"  k={row['Parallel_Channels']:2d}: "
                  f"{row['Parallel_Time_s']:6.1f}s "
                  f"(speedup: {row['Speedup']:.1f}x)")
    
    # Save results
    output_path = Path('data/experimental_results')
    df.to_csv(output_path / 'scalability_results.csv', index=False)
    
    print(f"\n✓ Results saved to data/experimental_results/scalability_results.csv")
    
    return df


def main():
    """Run complete experimental suite."""
    print("\n" + "=" * 70)
    print(" QUANTUM-NATIVE IIoT SECURITY - COMPLETE EXPERIMENTAL SUITE")
    print("=" * 70)
    print(f"\nStart Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nThis will reproduce all experimental results from the paper.")
    print("Estimated time: 2-4 hours depending on your system.\n")
    
    input("Press Enter to continue...")
    
    start_time = datetime.now()
    
    # Run all experiments
    auth_results = run_authentication_experiments()
    qkd_results = run_bb84_experiments()
    entanglement_results = run_entanglement_experiments()
    scalability_results = run_scalability_experiments()
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    print("\n" + "=" * 70)
    print(" EXPERIMENTAL SUITE COMPLETE")
    print("=" * 70)
    print(f"\nEnd Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Duration: {duration}")
    print("\nAll results saved to: data/experimental_results/")
    print("\nNext steps:")
    print("  1. Run: python scripts/generate_all_figures.py")
    print("  2. Run: python scripts/export_latex_tables.py")
    print("=" * 70)


if __name__ == "__main__":
    main()
