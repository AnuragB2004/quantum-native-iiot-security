"""
Generate All Paper Figures

Creates all figures from the paper using experimental results.

Author: Anurag Bhattacharjee
Date: February 2026
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path


# Set publication-quality style
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
sns.set_palette("husl")


def create_output_dir():
    """Create output directory for figures."""
    output_dir = Path('outputs/figures')
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def generate_auth_success_rates():
    """
    Generate Figure: Authentication Success Rates
    (Bar chart comparing simulator, noisy, and hardware)
    """
    print("Generating: Authentication Success Rates figure...")
    
    # Load data
    df = pd.read_csv('data/experimental_results/auth_results.csv')
    
    # Prepare data for plotting
    backends = df['Backend'].unique()
    devices = ['Device01', 'Device02', 'Device03', 'Device04', 'Device05']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(devices))
    width = 0.25
    
    for i, backend in enumerate(backends):
        backend_data = df[df['Backend'] == backend]
        means = backend_data['Success_Rate_Mean'].values
        stds = backend_data['Success_Rate_Std'].values
        
        ax.bar(x + i*width, means, width, 
               label=backend, yerr=stds, capsize=5)
    
    ax.set_xlabel('Device ID')
    ax.set_ylabel('Authentication Success Rate (%)')
    ax.set_title('Quantum Authentication Success Rates Across Execution Environments')
    ax.set_xticks(x + width)
    ax.set_xticklabels(devices)
    ax.legend()
    ax.set_ylim([90, 100.5])
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    output_dir = create_output_dir()
    plt.savefig(output_dir / 'auth_success_rates.png', bbox_inches='tight')
    plt.savefig(output_dir / 'auth_success_rates.pdf', bbox_inches='tight')
    plt.close()
    
    print("  ✓ Saved: auth_success_rates.png/pdf")


def generate_qber_attack_scenarios():
    """
    Generate Figure: QBER Under Attack Scenarios
    (Bar chart comparing QBER for different scenarios)
    """
    print("Generating: QBER Attack Scenarios figure...")
    
    # Load data
    df = pd.read_csv('data/experimental_results/qkd_results.csv')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    scenarios = df['Scenario'].values
    qber_means = df['QBER_Mean'].values * 100  # Convert to percentage
    qber_stds = df['QBER_Std'].values * 100
    
    colors = ['green', 'red']
    bars = ax.bar(scenarios, qber_means, yerr=qber_stds, 
                  capsize=10, color=colors, alpha=0.7, edgecolor='black')
    
    # Add threshold line
    ax.axhline(y=11, color='orange', linestyle='--', linewidth=2, 
               label='QBER Threshold (11%)')
    
    ax.set_ylabel('QBER (%)')
    ax.set_title('Quantum Bit Error Rate Under Normal and Attack Scenarios')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar, mean, std in zip(bars, qber_means, qber_stds):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + std,
                f'{mean:.2f}%\n±{std:.2f}%',
                ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    output_dir = create_output_dir()
    plt.savefig(output_dir / 'qber_attack_scenarios.png', bbox_inches='tight')
    plt.savefig(output_dir / 'qber_attack_scenarios.pdf', bbox_inches='tight')
    plt.close()
    
    print("  ✓ Saved: qber_attack_scenarios.png/pdf")


def generate_bell_fidelity_comparison():
    """
    Generate Figure: Bell State Fidelity Comparison
    (Bar chart comparing fidelity in normal vs tampered scenarios)
    """
    print("Generating: Bell Fidelity Comparison figure...")
    
    # Load data
    df = pd.read_csv('data/experimental_results/entanglement_results.csv')
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    scenarios = df['Scenario'].values
    fidelities = df['Fidelity_Mean'].values
    fidelity_stds = df['Fidelity_Std'].values
    chsh_values = df['CHSH_Mean'].values
    chsh_stds = df['CHSH_Std'].values
    
    # Fidelity subplot
    colors = ['green', 'red']
    bars1 = ax1.bar(scenarios, fidelities, yerr=fidelity_stds,
                    capsize=10, color=colors, alpha=0.7, edgecolor='black')
    
    ax1.axhline(y=0.85, color='orange', linestyle='--', linewidth=2,
                label='Fidelity Threshold (0.85)')
    ax1.set_ylabel('Correlation Fidelity')
    ax1.set_title('Bell State Entanglement Fidelity')
    ax1.legend()
    ax1.set_ylim([0.5, 1.0])
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar, val, std in zip(bars1, fidelities, fidelity_stds):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + std,
                f'{val:.3f}\n±{std:.3f}',
                ha='center', va='bottom', fontsize=9)
    
    # CHSH subplot
    bars2 = ax2.bar(scenarios, chsh_values, yerr=chsh_stds,
                    capsize=10, color=colors, alpha=0.7, edgecolor='black')
    
    ax2.axhline(y=2.0, color='orange', linestyle='--', linewidth=2,
                label='Classical Bound (2.0)')
    ax2.axhline(y=2.828, color='blue', linestyle=':', linewidth=2,
                label='Tsirelson Bound (2√2)')
    ax2.set_ylabel('CHSH Value')
    ax2.set_title('CHSH Inequality Violation')
    ax2.legend()
    ax2.set_ylim([1.5, 3.0])
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar, val, std in zip(bars2, chsh_values, chsh_stds):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + std,
                f'{val:.3f}\n±{std:.3f}',
                ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    output_dir = create_output_dir()
    plt.savefig(output_dir / 'bell_fidelity_bases.png', bbox_inches='tight')
    plt.savefig(output_dir / 'bell_fidelity_bases.pdf', bbox_inches='tight')
    plt.close()
    
    print("  ✓ Saved: bell_fidelity_bases.png/pdf")


def generate_scalability_heatmap():
    """
    Generate Figure: Scalability Heatmap
    (Heatmap showing authentication time vs devices and parallel channels)
    """
    print("Generating: Scalability Heatmap figure...")
    
    # Load data
    df = pd.read_csv('data/experimental_results/scalability_results.csv')
    
    # Pivot data for heatmap
    pivot_data = df.pivot(index='Parallel_Channels', 
                         columns='Devices', 
                         values='Parallel_Time_s')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.heatmap(pivot_data, annot=True, fmt='.1f', cmap='YlOrRd_r',
                cbar_kws={'label': 'Authentication Time (seconds)'},
                ax=ax)
    
    ax.set_xlabel('Number of Devices')
    ax.set_ylabel('Parallel Authentication Channels')
    ax.set_title('Authentication Latency Scaling Analysis')
    
    plt.tight_layout()
    output_dir = create_output_dir()
    plt.savefig(output_dir / 'scalability_heatmap.png', bbox_inches='tight')
    plt.savefig(output_dir / 'scalability_heatmap.pdf', bbox_inches='tight')
    plt.close()
    
    print("  ✓ Saved: scalability_heatmap.png/pdf")


def generate_protocol_security_radar():
    """
    Generate Figure: Protocol Security Comparison (Radar Chart)
    (Compares TLS, PQC, Hybrid, and Quantum-Native across security dimensions)
    """
    print("Generating: Protocol Security Radar chart...")
    
    categories = ['MITM\nResistance', 'Replay\nProtection', 
                  'Quantum\nSafe', 'Eavesdrop\nDetection',
                  'Info-Theoretic\nSecurity', 'Tamper\nEvidence']
    
    # Security scores (0-10 scale)
    protocols = {
        'TLS': [3, 4, 0, 0, 0, 0],
        'Post-Quantum': [8, 8, 8, 0, 0, 2],
        'Hybrid Q-C': [9, 9, 7, 5, 5, 5],
        'Quantum-Native\n(Proposed)': [10, 10, 10, 10, 10, 9]
    }
    
    # Number of variables
    num_vars = len(categories)
    
    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Complete the circle
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    colors = ['red', 'orange', 'blue', 'green']
    
    for (protocol, scores), color in zip(protocols.items(), colors):
        scores += scores[:1]  # Complete the circle
        ax.plot(angles, scores, 'o-', linewidth=2, label=protocol, color=color)
        ax.fill(angles, scores, alpha=0.15, color=color)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=10)
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10'], size=8)
    ax.grid(True)
    ax.set_title('Security Protocol Comparison\n(Higher is Better)', 
                 size=14, weight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    
    plt.tight_layout()
    output_dir = create_output_dir()
    plt.savefig(output_dir / 'protocol_security_radar.png', bbox_inches='tight')
    plt.savefig(output_dir / 'protocol_security_radar.pdf', bbox_inches='tight')
    plt.close()
    
    print("  ✓ Saved: protocol_security_radar.png/pdf")


def main():
    """Generate all figures."""
    print("\n" + "=" * 70)
    print(" GENERATING ALL PAPER FIGURES")
    print("=" * 70)
    print()
    
    # Check if experimental results exist
    results_dir = Path('data/experimental_results')
    if not results_dir.exists():
        print("ERROR: Experimental results not found!")
        print("Please run: python experiments/run_all_experiments.py first")
        return
    
    # Generate all figures
    generate_auth_success_rates()
    generate_qber_attack_scenarios()
    generate_bell_fidelity_comparison()
    generate_scalability_heatmap()
    generate_protocol_security_radar()
    
    print()
    print("=" * 70)
    print(" FIGURE GENERATION COMPLETE")
    print("=" * 70)
    print(f"\nAll figures saved to: outputs/figures/")
    print("\nGenerated files:")
    print("  - auth_success_rates.png/pdf")
    print("  - qber_attack_scenarios.png/pdf")
    print("  - bell_fidelity_bases.png/pdf")
    print("  - scalability_heatmap.png/pdf")
    print("  - protocol_security_radar.png/pdf")
    print()


if __name__ == "__main__":
    main()
