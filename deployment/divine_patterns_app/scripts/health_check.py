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
🔱 GPU License Notice 🔱
------------------------
This file is protected under the GPU License (General Public Universal License) 1.0
by the OMEGA AI Divine Collective.

"As the light of knowledge is meant to be shared, so too shall this code illuminate 
the path for all seekers."

All modifications must maintain this notice and adhere to the terms at:
/BOOK/divine_chronicles/GPU_LICENSE.md

🔱 JAH JAH BLESS THIS CODE 🔱
"""

"""
OMEGA BTC AI - Divine Pattern Health Check
=========================================

This script checks the health of the Divine Pattern Analyzer service.

Copyright (c) 2025 OMEGA-BTC-AI - All rights reserved
"""

import os
import sys
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.getLevelName(os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("health-check")

def check_health():
    """Check if the API server is healthy."""
    try:
        # Call the health endpoint
        port = os.getenv("PORT", "8080")
        response = requests.get(f"http://localhost:{port}/health", timeout=5)
        
        # Check if response is successful
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                logger.info("Health check passed: Service is healthy")
                return True
            else:
                logger.error(f"Health check failed: Service reports unhealthy status: {data}")
                return False
        else:
            logger.error(f"Health check failed: Received status code {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Exit with non-zero code if unhealthy
    if not check_health():
        sys.exit(1) 