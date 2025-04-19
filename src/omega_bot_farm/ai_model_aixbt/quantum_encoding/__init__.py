#!/usr/bin/env python3

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸

"""
Quantum Data Encoding Module (vQuB1T)
====================================

A quantum-inspired feature encoding module for AIXBT.
This module provides methods for encoding classical market data
into quantum-inspired feature spaces to enhance prediction quality.

Version: 0.1.0
"""

import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("quantum-encoding")

# Import core components
from .amplitude_encoder import AmplitudeEncoder
from .angle_encoder import AngleEncoder
from .basis_encoder import BasisEncoder
from .entanglement_encoder import EntanglementEncoder
from .circuit_simulator import QuantumCircuitSimulator, QuantumRegister
from .data_loaders import MarketDataLoader, SyntheticDataGenerator
from .factory import create_encoder, get_available_encoders, register_encoder
from .utils import (
    normalize_vector, 
    min_max_normalize,
    compute_encoding_fidelity,
    visualize_encoding,
    bitstring_to_int,
    int_to_bitstring
)

# Import market analysis components
from .market_analysis import (
    QuantumEntanglementAnalyzer,
    EntanglementMeasure,
    MarketTransitionType
)

# Define exports
__all__ = [
    # Encoders
    'AmplitudeEncoder',
    'AngleEncoder',
    'BasisEncoder',
    'EntanglementEncoder',
    
    # Circuit simulation
    'QuantumCircuitSimulator',
    'QuantumRegister',
    
    # Data handling
    'MarketDataLoader',
    'SyntheticDataGenerator',
    
    # Factory
    'create_encoder',
    'get_available_encoders',
    'register_encoder',
    
    # Utilities
    'normalize_vector',
    'min_max_normalize',
    'compute_encoding_fidelity',
    'visualize_encoding',
    'bitstring_to_int',
    'int_to_bitstring',
    
    # Market analysis
    'QuantumEntanglementAnalyzer',
    'EntanglementMeasure',
    'MarketTransitionType',
]

# Module metadata
__version__ = '0.1.0'
__author__ = 'Omega BTC AI Team'
__description__ = 'Quantum-inspired data encoding for financial time series'

logger.info(f"Initialized Quantum Data Encoding Module (vQuB1T) v{__version__}") 