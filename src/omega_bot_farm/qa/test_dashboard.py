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
Test script for the Quantum 5D QA Dashboard module.
This validates that the module can be imported correctly.
"""

import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestQuantumDashboard")

# Add the parent directory to the path to find the quantum_dashboard module
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(parent_dir)

try:
    # Try importing the dashboard module
    from quantum_dashboard import (
        QuantumMetrics, DASHBOARD_CONFIG, quantum_theme, collect_metrics
    )
    
    # Print success message
    logger.info("✅ Successfully imported quantum_dashboard module")
    
    # Create a test metric
    metrics = QuantumMetrics()
    
    # Print metrics info
    logger.info(f"📊 Created test metrics: {metrics.to_dict()}")
    
    # Print dashboard config
    logger.info(f"⚙️ Dashboard config: {DASHBOARD_CONFIG}")
    
    # Print theme
    logger.info(f"🎨 Dashboard theme: {quantum_theme}")
    
    # Try collecting metrics
    logger.info("🔄 Collecting metrics...")
    collected_metrics = collect_metrics()
    logger.info(f"✅ Successfully collected metrics: {collected_metrics.to_dict()}")
    
    logger.info("🎉 All tests passed!")

except Exception as e:
    # Print error message
    logger.error(f"❌ Error importing quantum_dashboard module: {e}")
    sys.exit(1)

# Exit with success
sys.exit(0) 