#!/usr/bin/env python3
"""
Quantum 5D QA Dashboard
---------------------

A multi-dimensional quality assurance dashboard for monitoring and visualizing 
quantum metrics across 5 dimensions: time, quality, coverage, performance, and security.
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

__version__ = "1.0.0"
__author__ = "Omega BTC AI Team"

# Export public API
__all__ = [
    "run_app",
    "create_app",
    "DASHBOARD_CONFIG",
    "quantum_theme",
    "QuantumMetrics",
    "collect_metrics"
] 