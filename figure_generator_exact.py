"""
Publication-Quality Figure Generator

Generates all figures from the paper with exact styling and values.

Author: Anurag Bhattacharjee
Date: February 2026
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
from pathlib import Path


# Publication-quality settings
plt.rcParams.update({
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 14,
    'lines.linewidth': 2,
    'lines.markersize': 8,
    'axes.linewidth': 1.2,
    'grid.linewidth': 0.8,
    'grid.alpha': 0.3
})


class PaperFigureGenerator:
    """Generates all figures matching the paper exactly."""
    
    def __init__(self, data_dir='data/experimental_results', output_dir='outputs/figures'):
        """Initialize figure generator."""
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # IEEE color scheme
        self.colors = {
            'primary': '#0C5DA5',
            'secondary': '#00B945',
            'accent': '#FF9500',
            'alert': '#FF2C00',
            'gray': '#6B7D8C'
        }
    
    def generate_figure_auth_success(self):
        """
        Generate Figure: Authentication Success Rates
        Matches paper Figure X showing authentication across backends
        """
        print("Generating: Authentication Success Rates...")
        
        # Load data
        df = pd.read_csv(self.data_dir / 'table1_auth_results.csv')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        devices = df['Device_ID'].values
        x = np.arange(len(devices))
        width = 0.25
        
        # Plot bars
        bars1 = ax.bar(x - width, df['Simulator_Success'], width,
                       label='Ideal Simulator', color=self.colors['primary'],
                       yerr=df['Simulator_Std'], capsize=4, alpha=0.8,
                       edgecolor='black', linewidth=0.8)
        
        bars2 = ax.bar(x, df['Noisy_Success'], width,
                       label='Noisy Simulator', color=self.colors['secondary'],
                       yerr=df['Noisy_Std'], capsize=4, alpha=0.8,
                       edgecolor='black', linewidth=0.8)
        
        bars3 = ax.bar(x + width, df['Hardware_Success'], width,
                       label='IBM Hardware', color=self.colors['accent'],
                       yerr=df['Hardware_Std'], capsize=4, alpha=0.8,
                       edgecolor='black', linewidth=0.8)
        
        # Formatting
        ax.set_xlabel('Device ID', fontweight='bold')
        ax.set_ylabel('Authentication Success Rate (%)', fontweight='bold')
        ax.set_title('Quantum Authentication Success Rates Across Execution Environments',
                    fontweight='bold', pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(devices)
        ax.set_ylim([94, 101])
        ax.legend(loc='lower right', frameon=True, shadow=True)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Add average line
        avg_hardware = df['Hardware_Success'].mean()
        ax.axhline(y=avg_hardware, color=self.colors['alert'], 
                  linestyle=':', linewidth=1.5, alpha=0.7,
                  label=f'Hardware Avg ({avg_hardware:.1f}%)')
        
        plt.tight_layout()
        
        # Save in multiple formats
        for fmt in ['png', 'pdf', 'svg']:
            plt.savefig(self.output_dir / f'fig_auth_success_rates.{fmt}',
                       bbox_inches='tight', dpi=300 if fmt=='png' else None)
        
        plt.close()
        print(f"  ✓ Saved to {self.output_dir}/fig_auth_success_rates.*")
    
    def generate_figure_qber_comparison(self):
        """
        Generate Figure: QBER Attack Scenarios
        Matches paper figure showing QBER under different conditions
        """
        print("Generating: QBER Attack Scenarios...")
        
        # Load data
        df = pd.read_csv(self.data_dir / 'table4_qber_attack.csv')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        scenarios = df['Attack_Type'].values
        qber_values = df['Observed_QBER'].values
        qber_stds = df['Std_Dev'].values
        
        # Color code by detection
        colors = [self.colors['primary'], self.colors['alert'], self.colors['alert']]
        
        bars = ax.bar(scenarios, qber_values, yerr=qber_stds,
                     capsize=8, color=colors, alpha=0.8,
                     edgecolor='black', linewidth=1.2)
        
        # Add threshold line
        ax.axhline(y=11, color='red', linestyle='--', linewidth=2.5,
                  label='QBER Threshold (11%)', zorder=0)
        
        # Add safe zone
        ax.axhspan(0, 11, alpha=0.1, color='green', label='Safe Zone')
        ax.axhspan(11, 30, alpha=0.1, color='red', label='Attack Zone')
        
        # Formatting
        ax.set_ylabel('Quantum Bit Error Rate (%)', fontweight='bold')
        ax.set_title('QBER Under Normal Operation and Simulated Attacks',
                    fontweight='bold', pad=15)
        ax.set_ylim([0, 30])
        ax.legend(loc='upper left', frameon=True, shadow=True)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Add value labels on bars
        for i, (bar, val, std) in enumerate(zip(bars, qber_values, qber_stds)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + std + 0.5,
                   f'{val:.1f}% ± {std:.1f}%',
                   ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        plt.tight_layout()
        
        for fmt in ['png', 'pdf', 'svg']:
            plt.savefig(self.output_dir / f'fig_qber_attack_scenarios.{fmt}',
                       bbox_inches='tight', dpi=300 if fmt=='png' else None)
        
        plt.close()
        print(f"  ✓ Saved to {self.output_dir}/fig_qber_attack_scenarios.*")
    
    def generate_figure_bell_fidelity(self):
        """
        Generate Figure: Bell State Fidelity and CHSH
        Combined figure showing fidelity and CHSH violations
        """
        print("Generating: Bell Fidelity & CHSH Violation...")
        
        # Load data
        df_fid = pd.read_csv(self.data_dir / 'table5_bell_fidelity.csv')
        df_chsh = pd.read_csv(self.data_dir / 'table6_chsh_results.csv')
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # === LEFT: Fidelity ===
        bases = df_fid['Basis_Pair'].values
        observed = df_fid['Observed_Hardware'].values
        theoretical = df_fid['Theoretical_Fidelity'].values
        stds = df_fid['Std_Dev'].values
        
        x = np.arange(len(bases))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, theoretical, width,
                       label='Theoretical', color=self.colors['gray'],
                       alpha=0.6, edgecolor='black', linewidth=1)
        
        bars2 = ax1.bar(x + width/2, observed, width,
                       label='IBM Hardware', color=self.colors['accent'],
                       yerr=stds, capsize=5, alpha=0.8,
                       edgecolor='black', linewidth=1)
        
        ax1.axhline(y=85, color='red', linestyle='--', linewidth=2,
                   label='Fidelity Threshold', alpha=0.7)
        
        ax1.set_ylabel('Correlation Fidelity (%)', fontweight='bold')
        ax1.set_title('Bell State Entanglement Fidelity', fontweight='bold', pad=10)
        ax1.set_xticks(x)
        ax1.set_xticklabels(bases, rotation=15, ha='right')
        ax1.set_ylim([40, 105])
        ax1.legend(loc='lower right', frameon=True, shadow=True)
        ax1.grid(axis='y', alpha=0.3, linestyle='--')
        
        # === RIGHT: CHSH ===
        scenarios = df_chsh['Scenario'].values[1:]  # Skip classical bound
        chsh_vals = df_chsh['CHSH_Value'].values[1:]
        chsh_stds = df_chsh['Std_Dev'].values[1:]
        
        colors_chsh = [self.colors['primary'], self.colors['secondary'], self.colors['accent']]
        
        bars = ax2.bar(scenarios, chsh_vals, yerr=chsh_stds,
                      capsize=6, color=colors_chsh, alpha=0.8,
                      edgecolor='black', linewidth=1.2)
        
        # Add bounds
        ax2.axhline(y=2.0, color='red', linestyle='--', linewidth=2.5,
                   label='Classical Bound', zorder=0)
        ax2.axhline(y=2.828, color='blue', linestyle=':', linewidth=2,
                   label='Tsirelson Bound (2√2)', alpha=0.7)
        
        # Shade violation zone
        ax2.axhspan(2.0, 3.0, alpha=0.1, color='green', label='Quantum Zone')
        ax2.axhspan(0, 2.0, alpha=0.1, color='gray', label='Classical Zone')
        
        ax2.set_ylabel('CHSH Value', fontweight='bold')
        ax2.set_title('CHSH Inequality Violation', fontweight='bold', pad=10)
        ax2.set_ylim([1.5, 3.0])
        ax2.legend(loc='upper right', frameon=True, shadow=True, fontsize=9)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Add value labels
        for bar, val, std in zip(bars, chsh_vals, chsh_stds):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + std + 0.02,
                    f'{val:.2f}\n±{std:.2f}',
                    ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        plt.tight_layout()
        
        for fmt in ['png', 'pdf', 'svg']:
            plt.savefig(self.output_dir / f'fig_bell_fidelity_chsh.{fmt}',
                       bbox_inches='tight', dpi=300 if fmt=='png' else None)
        
        plt.close()
        print(f"  ✓ Saved to {self.output_dir}/fig_bell_fidelity_chsh.*")
    
    def generate_figure_scalability_heatmap(self):
        """
        Generate Figure: Scalability Heatmap
        Shows authentication time vs devices and parallel channels
        """
        print("Generating: Scalability Heatmap...")
        
        # Load data
        df = pd.read_csv(self.data_dir / 'table7_scalability.csv')
        
        # Pivot for heatmap
        pivot = df.pivot(index='Parallel_Channels', 
                        columns='Devices',
                        values='Parallel_Time_s')
        
        fig, ax = plt.subplots(figsize=(12, 7))
        
        # Create heatmap
        im = ax.imshow(pivot.values, cmap='YlOrRd_r', aspect='auto')
        
        # Set ticks
        ax.set_xticks(np.arange(len(pivot.columns)))
        ax.set_yticks(np.arange(len(pivot.index)))
        ax.set_xticklabels(pivot.columns)
        ax.set_yticklabels(pivot.index)
        
        # Labels
        ax.set_xlabel('Number of Devices', fontweight='bold', fontsize=12)
        ax.set_ylabel('Parallel Authentication Channels', fontweight='bold', fontsize=12)
        ax.set_title('Authentication Latency Scaling Analysis\n(Parallel vs Sequential)',
                    fontweight='bold', fontsize=14, pad=15)
        
        # Add text annotations
        for i in range(len(pivot.index)):
            for j in range(len(pivot.columns)):
                text = ax.text(j, i, f'{pivot.values[i, j]:.1f}s',
                             ha="center", va="center", color="black",
                             fontsize=9, fontweight='bold')
        
        # Colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Authentication Time (seconds)', rotation=270, 
                      labelpad=20, fontweight='bold')
        
        plt.tight_layout()
        
        for fmt in ['png', 'pdf', 'svg']:
            plt.savefig(self.output_dir / f'fig_scalability_heatmap.{fmt}',
                       bbox_inches='tight', dpi=300 if fmt=='png' else None)
        
        plt.close()
        print(f"  ✓ Saved to {self.output_dir}/fig_scalability_heatmap.*")
    
    def generate_figure_protocol_radar(self):
        """
        Generate Figure: Protocol Security Comparison (Radar)
        Compares different protocol families across security dimensions
        """
        print("Generating: Protocol Security Radar...")
        
        categories = ['MITM\nResistance', 'Replay\nProtection', 
                     'Quantum\nSafe', 'Eavesdrop\nDetection',
                     'Info-Theoretic\nSecurity', 'Tamper\nEvidence']
        
        protocols = {
            'TLS': [3, 4, 0, 0, 0, 0],
            'Post-Quantum': [8, 8, 8, 0, 0, 2],
            'Hybrid Q-C': [9, 9, 7, 5, 5, 5],
            'Quantum-Native\n(This Work)': [10, 10, 10, 10, 10, 9]
        }
        
        num_vars = len(categories)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
        
        colors = ['#FF6B6B', '#FFA500', '#4ECDC4', '#45B7D1']
        markers = ['o', 's', '^', 'D']
        
        for (protocol, scores), color, marker in zip(protocols.items(), colors, markers):
            scores_plot = scores + scores[:1]
            ax.plot(angles, scores_plot, 'o-', linewidth=2.5, 
                   label=protocol, color=color, marker=marker,
                   markersize=8, markeredgecolor='white', markeredgewidth=1.5)
            ax.fill(angles, scores_plot, alpha=0.15, color=color)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, size=11, fontweight='bold')
        ax.set_ylim(0, 10)
        ax.set_yticks([2, 4, 6, 8, 10])
        ax.set_yticklabels(['2', '4', '6', '8', '10'], size=10)
        ax.grid(True, linestyle='--', alpha=0.7, linewidth=1.2)
        
        ax.set_title('Security Protocol Comparison Across Multiple Dimensions\n' +
                    '(Higher Score = Better Security)',
                    size=14, weight='bold', pad=25)
        
        ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.15),
                 frameon=True, shadow=True, fontsize=11)
        
        plt.tight_layout()
        
        for fmt in ['png', 'pdf', 'svg']:
            plt.savefig(self.output_dir / f'fig_protocol_security_radar.{fmt}',
                       bbox_inches='tight', dpi=300 if fmt=='png' else None)
        
        plt.close()
        print(f"  ✓ Saved to {self.output_dir}/fig_protocol_security_radar.*")
    
    def generate_all_figures(self):
        """Generate all paper figures."""
        print("\n" + "=" * 70)
        print(" GENERATING ALL PAPER FIGURES")
        print(" Publication Quality (300 DPI)")
        print("=" * 70)
        print()
        
        self.generate_figure_auth_success()
        self.generate_figure_qber_comparison()
        self.generate_figure_bell_fidelity()
        self.generate_figure_scalability_heatmap()
        self.generate_figure_protocol_radar()
        
        print()
        print("=" * 70)
        print(" ALL FIGURES GENERATED SUCCESSFULLY")
        print("=" * 70)
        print(f"\nOutput directory: {self.output_dir}/")
        print("\nGenerated files (PNG, PDF, SVG):")
        print("  - fig_auth_success_rates.*")
        print("  - fig_qber_attack_scenarios.*")
        print("  - fig_bell_fidelity_chsh.*")
        print("  - fig_scalability_heatmap.*")
        print("  - fig_protocol_security_radar.*")
        print()


def main():
    """Main execution."""
    generator = PaperFigureGenerator()
    generator.generate_all_figures()
    
    print("Next step:")
    print("  Run: python scripts/export_latex_tables.py")
    print()


if __name__ == "__main__":
    main()
