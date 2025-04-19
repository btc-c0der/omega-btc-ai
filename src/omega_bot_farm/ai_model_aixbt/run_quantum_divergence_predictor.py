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
Run Quantum Divergence Predictor
===============================

Script to run the Mock Quantum Divergence Predictor.
This demonstrates a classical approximation of quantum computing methods
for predicting AIXBT-BTC price divergence.

Usage:
    python -m src.omega_bot_farm.ai_model_aixbt.run_quantum_divergence_predictor
"""

import logging
from datetime import datetime
import os
import sys

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# Import directly from the module to avoid dependency issues with the main __init__.py
from src.omega_bot_farm.ai_model_aixbt.mock_quantum_divergence_predictor import run_mock_quantum_predictor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("quantum-divergence-predictor-runner")

if __name__ == "__main__":
    print(f"\n{'=' * 60}")
    print(f"MOCK QUANTUM DIVERGENCE PREDICTOR - STARTUP {datetime.now()}")
    print(f"{'=' * 60}")
    print("Starting the Mock Quantum Divergence Predictor...")
    print("This simulation showcases classical approximations of quantum computing methods.")
    print(f"{'=' * 60}\n")
    
    # Run the predictor
    run_mock_quantum_predictor()
