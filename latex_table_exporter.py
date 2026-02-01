"""
LaTeX Table Exporter

Converts CSV data to LaTeX table format matching the paper style.

Author: Anurag Bhattacharjee
Date: February 2026
"""

import pandas as pd
from pathlib import Path


class LaTeXTableExporter:
    """Exports data tables to LaTeX format."""
    
    def __init__(self, data_dir='data/experimental_results', output_dir='outputs/tables'):
        """Initialize exporter."""
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_table1_auth(self):
        """Export Table 1: Authentication Success Rates."""
        print("Exporting Table 1: Authentication Success Rates...")
        
        df = pd.read_csv(self.data_dir / 'table1_auth_results.csv')
        
        latex = r"""\begin{table}[t]
\centering
\begin{tabular}{lccc}
\toprule
\textbf{Device ID} & \textbf{Simulator (\%)} & \textbf{Noisy (\%)} & \textbf{IBM HW (\%)} \\
\midrule
"""
        
        for _, row in df.iterrows():
            latex += f"{row['Device_ID']} & ${row['Simulator_Success']:.1f} \\pm {row['Simulator_Std']:.1f}$ & "
            latex += f"${row['Noisy_Success']:.1f} \\pm {row['Noisy_Std']:.1f}$ & "
            latex += f"${row['Hardware_Success']:.1f} \\pm {row['Hardware_Std']:.1f}$ \\\\\n"
        
        latex += r"""\midrule
\textbf{Average} & """
        latex += f"$\\mathbf{{{df['Simulator_Success'].mean():.1f} \\pm {df['Simulator_Std'].mean():.1f}}}$ & "
        latex += f"$\\mathbf{{{df['Noisy_Success'].mean():.1f} \\pm {df['Noisy_Std'].mean():.1f}}}$ & "
        latex += f"$\\mathbf{{{df['Hardware_Success'].mean():.1f} \\pm {df['Hardware_Std'].mean():.1f}}}$ \\\\\n"
        
        latex += r"""\bottomrule
\end{tabular}
\caption{Authentication success rate across simulation, noisy simulation, and real hardware. Error bars represent one standard deviation over 50 independent trials per device. Each trial consists of $N=100$ authentication rounds.}
\label{tab:auth_success}
\end{table}"""
        
        with open(self.output_dir / 'table1_auth.tex', 'w') as f:
            f.write(latex)
        
        print("  ✓ Exported to table1_auth.tex")
    
    def export_table4_qber_attack(self):
        """Export Table 4: QBER Under Attack."""
        print("Exporting Table 4: QBER Under Attack...")
        
        df = pd.read_csv(self.data_dir / 'table4_qber_attack.csv')
        
        latex = r"""\begin{table*}[!t]
\centering
\begin{tabular}{lccc}
\toprule
\textbf{Attack Type} & \textbf{Theoretical QBER} & \textbf{Observed QBER} & \textbf{Detected} \\
\midrule
"""
        
        for _, row in df.iterrows():
            latex += f"{row['Attack_Type']} & {row['Theoretical_QBER']:.1f}\\% & "
            latex += f"${row['Observed_QBER']:.1f} \\pm {row['Std_Dev']:.1f}$\\% & "
            latex += f"{row['Detected']} \\\\\n"
        
        latex += r"""\bottomrule
\end{tabular}
\caption{Quantum bit error rate (QBER) observed under eavesdropping and active attack scenarios. Error margins represent $\pm 1\sigma$ over 20 attack simulations. Detection threshold: QBER $> 11\%$.}
\label{tab:qber_attack}
\end{table*}"""
        
        with open(self.output_dir / 'table4_qber_attack.tex', 'w') as f:
            f.write(latex)
        
        print("  ✓ Exported to table4_qber_attack.tex")
    
    def export_table7_scalability(self):
        """Export Table 7: Scalability."""
        print("Exporting Table 7: Scalability...")
        
        df = pd.read_csv(self.data_dir / 'table7_scalability.csv')
        
        # Get unique device counts and k values
        devices = sorted(df['Devices'].unique())
        k_values = sorted(df['Parallel_Channels'].unique())
        
        latex = r"""\begin{table}[t]
\centering
\caption{Authentication latency scaling for varying device counts and parallelization levels. Single-device authentication time $T_{\text{auth}} = 650$~ms (average experimental value).}
\label{tab:scalability_auth}
\begin{tabular}{c""" + "c" * len(k_values) + r"""}
\toprule
\textbf{Devices} & """ + " & ".join([f"\\textbf{{$k={k}$}}" for k in k_values]) + r""" \\
\textbf{($n$)} & """ + " & ".join([f"\\textbf{{(sec)}}" for _ in k_values]) + r""" \\
\midrule
"""
        
        for n in devices:
            row_data = df[df['Devices'] == n].sort_values('Parallel_Channels')
            values = [f"{row['Parallel_Time_s']:.1f}" for _, row in row_data.iterrows()]
            latex += f"{n:4d}   & " + "   & ".join(values) + r"   \\" + "\n"
        
        latex += r"""\bottomrule
\end{tabular}
\end{table}"""
        
        with open(self.output_dir / 'table7_scalability.tex', 'w') as f:
            f.write(latex)
        
        print("  ✓ Exported to table7_scalability.tex")
    
    def export_all_tables(self):
        """Export all tables."""
        print("\n" + "=" * 70)
        print(" EXPORTING ALL TABLES TO LATEX")
        print("=" * 70)
        print()
        
        self.export_table1_auth()
        self.export_table4_qber_attack()
        self.export_table7_scalability()
        
        print()
        print("=" * 70)
        print(" ALL LATEX TABLES EXPORTED")
        print("=" * 70)
        print(f"\nOutput directory: {self.output_dir}/")
        print("\nTo use in your paper:")
        print("  \\input{outputs/tables/table1_auth.tex}")
        print()


def main():
    """Main execution."""
    exporter = LaTeXTableExporter()
    exporter.export_all_tables()


if __name__ == "__main__":
    main()
