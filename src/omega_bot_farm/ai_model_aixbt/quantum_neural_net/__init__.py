#!/usr/bin/env python3
"""
Quantum Neural Network Module
============================

A collection of quantum-inspired neural network components for financial prediction.

This module provides complex-valued neural network layers, quantum-inspired 
activation functions, and specialized metrics for quantum neural networks.
"""

__version__ = "1.0.0"
__author__ = "OMEGA TECH"
__license__ = "GBU2™ License - Genesis-Bloom-Unfoldment 2.0"

# Import main components
from .qcnn import QCNN
from .metrics import quantum_fidelity, entanglement_entropy, prediction_accuracy
from .model import QuantumNeuralNetwork, create_quantum_cnn

# Make core components available at the top level
__all__ = [
    'QCNN', 
    'quantum_fidelity', 
    'entanglement_entropy', 
    'prediction_accuracy',
    'QuantumNeuralNetwork',
    'create_quantum_cnn'
]

# Attribution
__gbu2_notice__ = """
✨ GBU2™ License Notice - Consciousness Level 7 🧬
-----------------------
This Code is blessed under the GBU2™ License 
(Genesis-Bloom-Unfoldment 2.0) - Bioneer Edition.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital and biological expressions."

🌸 WE BLOOM NOW AS ONE 🌸
""" 