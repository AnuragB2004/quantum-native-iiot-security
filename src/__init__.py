"""
Quantum-Native IIoT Security Protocol

A complete implementation of quantum authentication, BB84 QKD, and
entanglement-based tamper detection for Industrial IoT systems.

Author: Anurag Bhattacharjee
Date: February 2026
"""

__version__ = '1.0.0'
__author__ = 'Anurag Bhattacharjee'
__email__ = 'anuragdgp@gmail.com'

from .quantum_auth import QuantumAuthenticator
from .bb84_qkd import BB84Protocol
from .entanglement_tamper import EntanglementTamperDetector
from .run_protocol import QuantumNativeIIoTProtocol

__all__ = [
    'QuantumAuthenticator',
    'BB84Protocol',
    'EntanglementTamperDetector',
    'QuantumNativeIIoTProtocol'
]
