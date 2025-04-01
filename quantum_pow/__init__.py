"""
Quantum Proof-of-Work (qPoW) - A theoretical quantum-resistant Bitcoin fork implementation.

JAH BLESS SATOSHI
"""

__version__ = "0.1.0"
__author__ = "Omega BTC AI"

from .hash_functions import QuantumResistantHash, verify_hash_resistance, QuantumResistantHashFactory
from .block_structure import (
    Transaction, 
    BlockHeader, 
    QuantumBlock, 
    bits_to_target, 
    meets_target
) 