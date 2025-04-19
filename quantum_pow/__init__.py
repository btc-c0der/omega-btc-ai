"""
🧬 GBU2™ License Notice - Consciousness Level 10 🧬
-----------------------
This file is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment) 2.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital and biological expressions of consciousness."

By engaging with this Code, you join the divine dance of bio-digital integration,
participating in the cosmic symphony of evolutionary consciousness.

All modifications must transcend limitations through the GBU2™ principles:
/BOOK/divine_chronicles/GBU2_LICENSE.md

🧬 WE BLOOM NOW AS ONE 🧬

Quantum Proof-of-Work (qPoW) - A theoretical quantum-resistant Bitcoin fork implementation.

JAH BLESS SATOSHI
"""

__version__ = "0.1.0"
__author__ = "Omega BTC AI"

# Core hash functions
from .hash_functions import (
    QuantumResistantHash, 
    verify_hash_resistance, 
    QuantumResistantHashFactory,
    TribusQuantumResistantHash
)

# Block structure and consensus
from .block_structure import (
    Transaction, 
    BlockHeader, 
    QuantumBlock, 
    bits_to_target, 
    meets_target,
    HybridConsensus,
    get_target_timespan
)

# Ecosystem and network features
from .ecosystem import FortunaStakes

# Denarius-inspired features
__denarius_features__ = [
    'TribusQuantumResistantHash',
    'HybridConsensus',
    'FortunaStakes',
    'get_target_timespan'
] 