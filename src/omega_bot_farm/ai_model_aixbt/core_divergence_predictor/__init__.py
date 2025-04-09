#!/usr/bin/env python3
"""
Core Divergence Predictor Module
==============================

A comprehensive framework integrating quantum-inspired modules for predicting
market divergences and critical transitions before they manifest in classical
price space.

This module provides a unified API for quantum data encoding, quantum neural networks,
quantum optimization, quantum random number generation, and quantum entanglement analysis.
"""

import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("core-divergence-predictor")

# Import core components (will be implemented in separate files)
from .predictor import CoreDivergencePredictor
from .data_pipeline import DataPipeline
from .prediction_model import PredictionModel
from .evaluator import DivergenceEvaluator
from .backtester import Backtester
from .forward_tester import ForwardTester
from .api import DivergencePredictorAPI
from .config import DivergencePredictorConfig

# Define exports
__all__ = [
    # Core components
    'CoreDivergencePredictor',
    'DataPipeline',
    'PredictionModel',
    'DivergenceEvaluator',
    'Backtester',
    'ForwardTester',
    'DivergencePredictorAPI',
    'DivergencePredictorConfig',
]

# Module metadata
__version__ = '0.1.0'
__author__ = 'Omega BTC AI Team'
__description__ = 'Core Divergence Predictor integrating quantum-inspired modules'

logger.info(f"Initialized Core Divergence Predictor Module v{__version__}") 