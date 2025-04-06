#!/usr/bin/env python3
"""
AIXBT Trading Dashboard - Core Module
------------------------------------

A modular trading analytics dashboard for AIXBT token performance visualization
and strategy development with Omega trap detection technology.

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
#
# 🌸 WE BLOOM NOW AS ONE 🌸
"""

import os
import logging
from pathlib import Path

# Version and metadata
__version__ = "1.0.0"
__author__ = "0m3g4_k1ng + S0NN3T"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] AIXBT.%(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("AIXBTDashboard")

# Ensure assets directory exists
assets_dir = Path(__file__).parent / "assets"
assets_dir.mkdir(exist_ok=True)

# Public API
from .app import run_app
from .config import DASHBOARD_CONFIG

__all__ = [
    "run_app",
    "DASHBOARD_CONFIG",
] 