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
Quantum Market Analysis Module
============================

Collection of tools for analyzing market behavior using quantum-inspired methods.
This module provides advanced analytical tools leveraging quantum principles
to detect and predict market transitions and critical events.
"""

import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("quantum-market-analysis")

# Import components
from .quantum_entanglement_analyzer import (
    QuantumEntanglementAnalyzer,
    EntanglementMeasure,
    MarketTransitionType
)

# Define exports
__all__ = [
    # Analyzers
    'QuantumEntanglementAnalyzer',
    
    # Enums and Types
    'EntanglementMeasure',
    'MarketTransitionType',
]

# Module metadata
__version__ = '0.1.0'
__author__ = 'Omega BTC AI Team'
__description__ = 'Quantum-inspired market analysis for detecting critical transitions'

logger.info(f"Initialized Quantum Market Analysis Module v{__version__}") 