#!/usr/bin/env python3
"""
Quantum Neural Network Module for AIXBT (vQuB1T-NN)
==================================================

Advanced quantum-inspired neural network architectures for financial time series prediction.
This module provides classically simulated quantum neural networks that can identify
complex patterns in market data, with a focus on predicting AIXBT-BTC price divergences.

Version: 1.0.0
"""

__version__ = "1.0.0"

# Import core components
from .base import QuantumLayer, QuantumModel, QuantumActivation
from .qcnn import QCNN, QuantumConvolution
from .qlstm import QLSTM, QuantumLSTMCell
from .variational import VariationalQuantumLayer, VariationalQuantumCircuit
from .entanglement import EntanglementLayer, QuantumCorrelation
from .activation import (
    HadamardActivation, 
    PhaseActivation, 
    ParametricRXActivation,
    ToffoliActivation
)
from .utils import quantum_loss, quantum_gradient, load_model, save_model
from .metrics import (
    quantum_fidelity, 
    entanglement_entropy,
    prediction_accuracy, 
    quantum_advantage_factor
)

# Import complete models
from .models import (
    DivergencePredictor,
    MarketPhaseClassifier,
    VolatilityPredictor,
    CorrelationAnalyzer
)

# Package metadata
__author__ = "Omega BTC AI Team"
__email__ = "support@omegabtc.ai"
__status__ = "Experimental"
__license__ = "GBU2 License" 