# Quick Start Guide

## Installation (5 minutes)

```bash
# Clone repository
git clone https://github.com/AnuragB2004/quantum-native-iiot-security.git
cd quantum-native-iiot-security

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python tests/test_installation.py
```

## Run Your First Experiment (2 minutes)

### Option 1: Complete Protocol Demo
```bash
python src/run_protocol.py --device-id Device01 --mode simulator
```

Expected output: Full protocol execution with authentication, QKD, and tamper detection.

### Option 2: Individual Components

**Quantum Authentication:**
```bash
python src/quantum_auth.py
```

**BB84 QKD:**
```bash
python src/bb84_qkd.py
```

**Entanglement Tamper Detection:**
```bash
python src/entanglement_tamper.py
```

## Reproduce Paper Results (2-4 hours)

```bash
# Run all experiments
python experiments/run_all_experiments.py

# Generate figures
python scripts/generate_all_figures.py

# Results will be in:
# - data/experimental_results/ (CSV files)
# - outputs/figures/ (PNG and PDF figures)
```

## Run on IBM Quantum Hardware

```bash
# 1. Get API token from https://quantum.ibm.com/
# 2. Configure token
python scripts/configure_ibm.py --token YOUR_IBM_TOKEN

# 3. List available backends
python scripts/configure_ibm.py --list-backends

# 4. Run on hardware
python src/run_protocol.py --mode hardware --backend ibm_brisbane --device-id Device01
```

## Interactive Jupyter Notebooks

```bash
jupyter notebook

# Open: notebooks/04_complete_protocol.ipynb
```

## Common Issues

**Issue:** `ModuleNotFoundError: No module named 'qiskit'`  
**Solution:** Activate virtual environment and install requirements

**Issue:** IBM Quantum connection errors  
**Solution:** Check API token and internet connection

**Issue:** Slow execution on simulator  
**Solution:** Reduce shots in config (trade accuracy for speed)

## Next Steps

- Read `docs/PROTOCOL_DETAILS.md` for mathematical foundations
- Explore `notebooks/` for interactive tutorials
- Check `docs/API_REFERENCE.md` for API documentation
- Customize `configs/default_config.yaml` for your experiments

## Need Help?

- GitHub Issues: https://github.com/[your-username]/quantum-native-iiot-security/issues
- Email: anuragdgp@gmail.com
- Paper: [DOI link when available]
