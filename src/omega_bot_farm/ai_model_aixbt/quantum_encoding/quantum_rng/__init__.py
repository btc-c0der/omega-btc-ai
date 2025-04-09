#!/usr/bin/env python3
"""
Quantum Random Number Generator Module
=====================================

A module for generating truly random numbers using quantum-inspired methods.
This module is part of the AIXBT quantum encoding system and provides
quantum supremacy in sampling random numbers from coherent quantum states.

Version: 0.1.0
"""

import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("quantum-rng")

# Import core components
from .quantum_rng import QuantumRNG
from .coherent_state_sampler import CoherentStateSampler
from .market_regime_predictor import MarketRegimePredictor
from .stochastic_models import StochasticVolatilityModel, JumpDiffusionModel
from .util import visualize_distribution, entropy_test, nist_test_suite

# Define exports
__all__ = [
    # RNG Components
    'QuantumRNG',
    'CoherentStateSampler',
    
    # Predictors
    'MarketRegimePredictor',
    
    # Stochastic Models
    'StochasticVolatilityModel',
    'JumpDiffusionModel',
    
    # Utilities
    'visualize_distribution',
    'entropy_test',
    'nist_test_suite',
]

# Module metadata
__version__ = '0.1.0'
__author__ = 'Omega BTC AI Team'
__description__ = 'Quantum-inspired random number generation for stochastic models'

logger.info(f"Initialized Quantum Random Number Generator Module v{__version__}") 