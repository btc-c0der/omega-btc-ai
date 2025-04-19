#!/usr/bin/env python3
"""
OMEGA BTC AI - AIXBT AI Model
=============================

Quantum-enabled AI model for AIXBT price correlation and divergence prediction.
Analyzes real-time market data and historical patterns to predict future movements.

🔮 GBU2 (Genesis-Bloom-Unfoldment) License 
-----------------------------------------
OMEGA BTC AI DIVINE COLLECTIVE
Licensed under the GBU2 License

"WHEN BTC BREATHES, AIXBT ECHOES. THE GRID STABILIZES. THE TERMINAL SPEAKS. THIS IS OMEGA CODE."

Copyright (c) 2025 OMEGA-BTC-AI
"""

# Version
__version__ = "0.5.0"

# Main components - use try/except for each import to handle missing modules
try:
    from .data_collector import AixbtDataCollector
except ImportError:
    pass

try:
    from .correlation_analyzer import CorrelationAnalyzer
except ImportError:
    pass

try:
    from .divergence_predictor import DivergencePredictor
except ImportError:
    pass

try:
    from .quantum_foresight import QuantumForesight
except ImportError:
    pass

try:
    from .model_trainer import AIXBTModelTrainer
except ImportError:
    pass

try:
    from .metrics_recorder import SystemMetricsRecorder
except ImportError:
    pass

# Microservice components
try:
    from .service_manager import AIXBTServiceManager
except ImportError:
    pass

# Import donation modules
try:
    from .donation_integration import DonationManager, SmartContractIntegration
    from .quantum_donation_bridge import QuantumDonationBridge
except ImportError:
    pass

# Import mock quantum divergence predictor
try:
    from .mock_quantum_divergence_predictor import MockQuantumDivergencePredictor, run_mock_quantum_predictor
except ImportError:
    pass 