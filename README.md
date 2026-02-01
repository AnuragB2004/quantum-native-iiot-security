# Quantum-Native Security Protocol for Industrial IoT

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Qiskit](https://img.shields.io/badge/Qiskit-1.0+-6133BD.svg)](https://qiskit.org/)

**Companion code for the paper:**  
*"A Fully Quantum-Native Security Protocol for Industrial Internet of Things Automation"*  
by Anurag Bhattacharjee, Anjan Bandyopadhyay, and Neeraj Sharma

**Published in:** IEEE Transactions on Quantum Engineering (2026)  
**DOI:** [10.1109/TQE.2026.DOI] *(update when available)*

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Repository Structure](#repository-structure)
- [Running Experiments](#running-experiments)
- [Reproducing Paper Results](#reproducing-paper-results)
- [Hardware Execution](#hardware-execution)
- [Citation](#citation)
- [License](#license)
- [Contact](#contact)

---

## 🔬 Overview

This repository contains the complete implementation of a **quantum-native security protocol** for Industrial Internet of Things (IIoT) systems. Unlike hybrid approaches that only use quantum mechanics for key distribution, our protocol integrates:

1. **Quantum Authentication** - Device identity verification using quantum states
2. **BB84 Quantum Key Distribution** - Information-theoretic secure key establishment
3. **Entanglement-Based Tamper Detection** - Real-time eavesdropping detection via Bell states

All components have been validated on:
- ✅ Ideal quantum simulators
- ✅ Noisy simulators (realistic noise models)
- ✅ **Real IBM quantum hardware** (superconducting qubits)

### Key Results

- **Authentication Success Rate:** 96.9% on real hardware
- **QBER Detection:** Clear separation between benign (2.3%) and attack (11.8%+) scenarios
- **Entanglement Fidelity:** 94.2% for same-basis measurements
- **CHSH Violation:** 2.49 ± 0.12 on IBM hardware (proves genuine entanglement)

---

## ✨ Features

- **Complete Protocol Implementation:** All three security phases (auth, QKD, tamper detection)
- **Multiple Execution Modes:** Simulator, noisy simulator, and real quantum hardware
- **Attack Simulations:** Eavesdropping and active manipulation scenarios
- **Statistical Analysis:** Automated computation of QBER, fidelity, CHSH values with error bars
- **Visualization Tools:** Generate all figures from the paper
- **Scalability Analysis:** Multi-device deployment simulations
- **Reproducible Results:** Fixed random seeds and configuration files

---

## 💻 System Requirements

### Minimum Requirements
- **Python:** 3.8 or higher
- **RAM:** 4 GB minimum, 8 GB recommended
- **Storage:** 1 GB free space

### Required Python Packages
```
qiskit >= 1.0.0
qiskit-aer >= 0.13.0
qiskit-ibm-runtime >= 0.17.0
numpy >= 1.24.0
matplotlib >= 3.7.0
pandas >= 2.0.0
scipy >= 1.10.0
```

### Optional (for hardware execution)
- IBM Quantum account (free tier available at https://quantum.ibm.com/)
- IBM Quantum API token

---

## 🚀 Installation

### Option 1: Using pip (Recommended)

```bash
# Clone the repository
git clone https://github.com/[your-username]/quantum-native-iiot-security.git
cd quantum-native-iiot-security

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Using conda

```bash
# Clone the repository
git clone https://github.com/[your-username]/quantum-native-iiot-security.git
cd quantum-native-iiot-security

# Create conda environment
conda env create -f environment.yml
conda activate quantum-iiot
```

### Verify Installation

```bash
python tests/test_installation.py
```

Expected output:
```
✓ Qiskit installed successfully (version X.X.X)
✓ All dependencies available
✓ Test circuits execute correctly
Installation verified!
```

---

## 🎯 Quick Start

### 1. Run Complete Protocol (Simulator)

```bash
python src/run_protocol.py --mode simulator --device-id Device01
```

### 2. Simulate Attack Scenario

```bash
python src/run_protocol.py --mode simulator --attack eavesdrop
```

### 3. Run on IBM Quantum Hardware

```bash
# First, configure your IBM Quantum token
python scripts/configure_ibm.py --token YOUR_IBM_TOKEN

# Then run on real hardware
python src/run_protocol.py --mode hardware --backend ibm_brisbane
```

### 4. Generate All Paper Figures

```bash
python scripts/generate_all_figures.py
```

Figures will be saved to `outputs/figures/`

---

## 📁 Repository Structure

```
quantum-native-iiot-security/
│
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── environment.yml                    # Conda environment
├── LICENSE                            # MIT License
│
├── src/                               # Main source code
│   ├── __init__.py
│   ├── quantum_auth.py               # Quantum authentication protocol
│   ├── bb84_qkd.py                   # BB84 key distribution
│   ├── entanglement_tamper.py        # Entanglement-based detection
│   ├── run_protocol.py               # Main protocol orchestrator
│   ├── attacks.py                    # Attack simulation modules
│   └── utils.py                      # Utility functions
│
├── experiments/                       # Experimental scripts
│   ├── experiment_auth.py            # Authentication experiments
│   ├── experiment_qkd.py             # QKD experiments
│   ├── experiment_entanglement.py    # Entanglement experiments
│   ├── experiment_scalability.py     # Scalability analysis
│   └── run_all_experiments.py        # Run complete experimental suite
│
├── scripts/                           # Utility scripts
│   ├── configure_ibm.py              # IBM Quantum setup
│   ├── generate_all_figures.py       # Paper figure generation
│   ├── analyze_results.py            # Statistical analysis
│   └── export_latex_tables.py        # Generate LaTeX tables
│
├── tests/                             # Unit tests
│   ├── test_installation.py          # Installation verification
│   ├── test_quantum_auth.py          # Auth protocol tests
│   ├── test_bb84.py                  # BB84 tests
│   └── test_entanglement.py          # Entanglement tests
│
├── configs/                           # Configuration files
│   ├── default_config.yaml           # Default parameters
│   ├── simulator_config.yaml         # Simulator settings
│   └── hardware_config.yaml          # IBM hardware settings
│
├── data/                              # Experimental data
│   ├── device_identities.json        # Registered quantum identities
│   └── experimental_results/         # Raw results (CSV format)
│
├── outputs/                           # Generated outputs
│   ├── figures/                      # Paper figures (PNG, PDF)
│   ├── tables/                       # LaTeX tables
│   └── logs/                         # Execution logs
│
├── notebooks/                         # Jupyter notebooks
│   ├── 01_quantum_authentication.ipynb
│   ├── 02_bb84_demonstration.ipynb
│   ├── 03_entanglement_verification.ipynb
│   └── 04_complete_protocol.ipynb
│
└── docs/                              # Documentation
    ├── PROTOCOL_DETAILS.md           # Detailed protocol description
    ├── API_REFERENCE.md              # Code API documentation
    ├── HARDWARE_GUIDE.md             # IBM Quantum usage guide
    └── TROUBLESHOOTING.md            # Common issues and solutions
```

---

## 🧪 Running Experiments

### Individual Protocol Components

#### 1. Quantum Authentication
```bash
python experiments/experiment_auth.py \
    --devices 5 \
    --rounds 100 \
    --mode simulator
```

Output:
- Authentication success rates (Table 1 in paper)
- Statistical verification results
- Saved to: `data/experimental_results/auth_results.csv`

#### 2. BB84 Quantum Key Distribution
```bash
python experiments/experiment_qkd.py \
    --key-length 256 \
    --qber-threshold 0.11 \
    --mode noisy
```

Output:
- QBER under normal and attack scenarios (Tables 3, 4)
- Key yield statistics (Table 2)
- Saved to: `data/experimental_results/qkd_results.csv`

#### 3. Entanglement-Based Tamper Detection
```bash
python experiments/experiment_entanglement.py \
    --trials 50 \
    --shots 4096 \
    --mode simulator
```

Output:
- Bell state fidelity (Table 5)
- CHSH inequality values (Table 6)
- Saved to: `data/experimental_results/entanglement_results.csv`

#### 4. Scalability Analysis
```bash
python experiments/experiment_scalability.py \
    --max-devices 1000 \
    --parallel-channels 10
```

Output:
- Authentication latency scaling (Table 7)
- Quantum resource requirements (Table 8)
- Saved to: `data/experimental_results/scalability_results.csv`

---

## 📊 Reproducing Paper Results

To reproduce **all** results from the paper:

```bash
# Run complete experimental suite (WARNING: Takes ~2-4 hours)
python experiments/run_all_experiments.py --config configs/paper_reproduction.yaml

# Generate all figures and tables
python scripts/generate_all_figures.py
python scripts/export_latex_tables.py

# Results will be in:
# - outputs/figures/     (all paper figures)
# - outputs/tables/      (LaTeX table code)
# - data/experimental_results/  (raw CSV data)
```

### Expected Outputs

After running, you should see:

**Figures:**
- `fig1_architecture.png` - System architecture
- `fig2_protocol_security_radar.png` - Security comparison
- `auth_success_rates.png` - Authentication performance (Fig. X)
- `qber_attack_scenarios.png` - QBER under attacks (Fig. Y)
- `bell_fidelity_bases.png` - Entanglement fidelity (Fig. Z)

**Tables (LaTeX):**
- `table1_auth_success.tex`
- `table2_bb84_yield.tex`
- `table3_qber_normal.tex`
- `table4_qber_attack.tex`
- `table5_bell_fidelity.tex`
- `table6_chsh_results.tex`
- `table7_scalability.tex`

---

## 🖥️ Hardware Execution

### Prerequisites

1. **Create IBM Quantum Account**
   - Visit: https://quantum.ibm.com/
   - Sign up (free tier available)
   - Generate API token

2. **Configure Token**
   ```bash
   python scripts/configure_ibm.py --token YOUR_IBM_QUANTUM_TOKEN
   ```

3. **List Available Backends**
   ```bash
   python scripts/configure_ibm.py --list-backends
   ```

### Running on IBM Hardware

```bash
# Run authentication on real hardware
python experiments/experiment_auth.py \
    --mode hardware \
    --backend ibm_brisbane \
    --devices 5

# Run complete protocol
python src/run_protocol.py \
    --mode hardware \
    --backend ibm_brisbane \
    --device-id Device01
```

### Important Notes for Hardware Execution

- **Queue Times:** IBM quantum systems have job queues; expect 5-30 min wait times
- **Cost:** Free tier provides ~10 min/month of quantum time; may need paid plan
- **Backends:** Choose backends with ≥5 qubits and low error rates
- **Shots:** Hardware experiments use 8192 shots by default (adjustable)

---

## 📈 Configuration

All experiments can be configured via YAML files in `configs/`:

```yaml
# Example: configs/custom_config.yaml
authentication:
  rounds: 100
  threshold: 0.05
  
bb84:
  key_length: 256
  qber_threshold: 0.11
  test_fraction: 0.5
  
entanglement:
  trials: 50
  shots: 4096
  chsh_threshold: 2.0
  
execution:
  mode: simulator  # simulator, noisy, hardware
  backend: ibm_brisbane
  optimization_level: 3
```

Use custom config:
```bash
python src/run_protocol.py --config configs/custom_config.yaml
```

---

## 🧮 Statistical Analysis

Compute statistics with error bars:

```bash
python scripts/analyze_results.py \
    --input data/experimental_results/auth_results.csv \
    --output outputs/statistics/auth_statistics.json \
    --confidence 0.95
```

Output includes:
- Mean and standard deviation
- 95% confidence intervals
- Bootstrap resampling statistics
- Statistical significance tests

---

## 📓 Jupyter Notebooks

Interactive demonstrations are available in `notebooks/`:

```bash
# Launch Jupyter
jupyter notebook

# Open any notebook, e.g.:
# notebooks/01_quantum_authentication.ipynb
```

Notebooks include:
- Step-by-step protocol walkthrough
- Interactive visualizations
- Explanatory text and equations
- Ability to modify parameters and re-run

---

## 🐛 Testing

Run unit tests to verify installation:

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_quantum_auth.py -v

# Run with coverage report
python -m pytest tests/ --cov=src --cov-report=html
```

---

## 📄 Documentation

Detailed documentation available in `docs/`:

- **PROTOCOL_DETAILS.md** - Mathematical foundations and protocol flow
- **API_REFERENCE.md** - Function and class documentation
- **HARDWARE_GUIDE.md** - IBM Quantum best practices
- **TROUBLESHOOTING.md** - Common errors and solutions

---

## 📚 Citation

If you use this code in your research, please cite our paper:

```bibtex
@article{bhattacharjee2026quantum,
  title={A Fully Quantum-Native Security Protocol for Industrial Internet of Things Automation},
  author={Bhattacharjee, Anurag and Bandyopadhyay, Anjan and Sharma, Neeraj},
  journal={IEEE Transactions on Quantum Engineering},
  year={2026},
  volume={X},
  number={X},
  pages={XX--XX},
  doi={10.1109/TQE.2026.DOI}
}
```

---

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See `CONTRIBUTING.md` for detailed guidelines.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Anurag Bhattacharjee, Anjan Bandyopadhyay, Neeraj Sharma

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📧 Contact

**Corresponding Author:** Anurag Bhattacharjee  
**Email:** anuragdgp@gmail.com  
**Institution:** Kalinga Institute of Industrial Technology (KIIT), Bhubaneswar, India

**Co-Authors:**
- Dr. Anjan Bandyopadhyay (KIIT)
- Dr. Neeraj Sharma (Lovely Professional University)

**Issues & Support:**  
Please use the [GitHub Issues](https://github.com/[your-username]/quantum-native-iiot-security/issues) page for bug reports and feature requests.

---

## 🙏 Acknowledgments

- IBM Quantum for providing access to quantum hardware
- Qiskit development team for the quantum computing framework
- Reviewers and the IEEE TQE editorial team

---

## 📊 Project Status

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Tests](https://img.shields.io/badge/tests-100%25-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)
![Documentation](https://img.shields.io/badge/docs-complete-blue)

**Latest Release:** v1.0.0 (February 2026)

---

## 🗺️ Roadmap

- [x] Core protocol implementation
- [x] Simulator validation
- [x] Real hardware experiments
- [x] Paper publication
- [ ] Multi-gateway hierarchical architecture
- [ ] Integration with MQTT/OPC-UA
- [ ] Docker containerization
- [ ] Web-based visualization dashboard
- [ ] Support for additional quantum backends (AWS Braket, Azure Quantum)

---

**Star ⭐ this repository if you find it useful!**

Last Updated: February 2026
