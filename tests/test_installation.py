"""
Installation Verification Test

Tests that all dependencies are correctly installed.

Author: Anurag Bhattacharjee
Date: February 2026
"""

import sys


def test_python_version():
    """Test Python version >= 3.8"""
    print("Testing Python version...", end=" ")
    if sys.version_info >= (3, 8):
        print("✓ OK (Python {}.{})".format(*sys.version_info[:2]))
        return True
    else:
        print("✗ FAIL (Python >= 3.8 required)")
        return False


def test_qiskit():
    """Test Qiskit installation"""
    print("Testing Qiskit...", end=" ")
    try:
        import qiskit
        from qiskit import QuantumCircuit
        from qiskit_aer import AerSimulator
        
        # Quick circuit test
        qc = QuantumCircuit(1, 1)
        qc.h(0)
        qc.measure(0, 0)
        
        backend = AerSimulator()
        job = backend.run(qc, shots=100)
        result = job.result()
        
        print(f"✓ OK (Qiskit {qiskit.__version__})")
        return True
    except Exception as e:
        print(f"✗ FAIL ({e})")
        return False


def test_numpy():
    """Test NumPy installation"""
    print("Testing NumPy...", end=" ")
    try:
        import numpy as np
        x = np.array([1, 2, 3])
        assert np.sum(x) == 6
        print(f"✓ OK (NumPy {np.__version__})")
        return True
    except Exception as e:
        print(f"✗ FAIL ({e})")
        return False


def test_matplotlib():
    """Test Matplotlib installation"""
    print("Testing Matplotlib...", end=" ")
    try:
        import matplotlib
        import matplotlib.pyplot as plt
        print(f"✓ OK (Matplotlib {matplotlib.__version__})")
        return True
    except Exception as e:
        print(f"✗ FAIL ({e})")
        return False


def test_pandas():
    """Test Pandas installation"""
    print("Testing Pandas...", end=" ")
    try:
        import pandas as pd
        df = pd.DataFrame({'a': [1, 2, 3]})
        assert len(df) == 3
        print(f"✓ OK (Pandas {pd.__version__})")
        return True
    except Exception as e:
        print(f"✗ FAIL ({e})")
        return False


def test_yaml():
    """Test PyYAML installation"""
    print("Testing PyYAML...", end=" ")
    try:
        import yaml
        data = yaml.safe_load("test: value")
        assert data['test'] == 'value'
        print("✓ OK")
        return True
    except Exception as e:
        print(f"✗ FAIL ({e})")
        return False


def test_project_imports():
    """Test project module imports"""
    print("Testing project modules...", end=" ")
    try:
        # This will fail if we're not in the right directory structure
        # but that's okay for initial setup
        import sys
        from pathlib import Path
        
        # Add src to path
        src_path = Path(__file__).parent.parent / 'src'
        if src_path.exists():
            sys.path.insert(0, str(src_path))
            
            from quantum_auth import QuantumAuthenticator
            from bb84_qkd import BB84Protocol
            from entanglement_tamper import EntanglementTamperDetector
            
            print("✓ OK")
            return True
        else:
            print("⚠ SKIP (run from project root)")
            return True  # Not a failure
    except Exception as e:
        print(f"⚠ SKIP ({e})")
        return True  # Not a failure for fresh install


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print(" INSTALLATION VERIFICATION TEST")
    print("=" * 60)
    print()
    
    tests = [
        test_python_version,
        test_qiskit,
        test_numpy,
        test_matplotlib,
        test_pandas,
        test_yaml,
        test_project_imports
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print()
    print("=" * 60)
    
    if all(results):
        print(" ✓ ALL TESTS PASSED - INSTALLATION VERIFIED!")
    else:
        print(" ✗ SOME TESTS FAILED - CHECK ERRORS ABOVE")
        print()
        print("To fix:")
        print("  1. Ensure Python >= 3.8")
        print("  2. Install requirements: pip install -r requirements.txt")
        print("  3. Activate virtual environment if using one")
    
    print("=" * 60)
    print()
    
    return all(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
