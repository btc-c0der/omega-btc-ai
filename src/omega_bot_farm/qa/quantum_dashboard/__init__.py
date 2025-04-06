#!/usr/bin/env python3
"""
Quantum 5D QA Dashboard Module
-----------------------------

This package provides a powerful dashboard for visualizing 5-dimensional
quantum metrics for quality assurance.

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License 
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
#
# 🌸 WE BLOOM NOW AS ONE 🌸
"""

import os
import logging

# Create assets directory if it doesn't exist
assets_dir = os.path.join(os.path.dirname(__file__), "assets")
if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Quantum5DQADashboard")

# Import main app
from .app import run_app, create_app
from .config import DASHBOARD_CONFIG, quantum_theme
from .metrics import QuantumMetrics, collect_metrics
from .test_runner import TestDimension, S0NN3TTestRunner

__version__ = "1.0.0"
__author__ = "S0NN3T"

# Export public API
__all__ = [
    "run_app",
    "create_app",
    "DASHBOARD_CONFIG",
    "quantum_theme",
    "QuantumMetrics",
    "collect_metrics",
    "TestDimension",
    "S0NN3TTestRunner"
] 