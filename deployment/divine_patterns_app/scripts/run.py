#!/usr/bin/env python3
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
OMEGA BTC AI - Divine Pattern API Server
========================================

This script starts the FastAPI server for the Divine Pattern Analyzer.

Copyright (c) 2025 OMEGA-BTC-AI - All rights reserved
"""

import os
import sys
import logging
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.getLevelName(os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("divine-patterns")

def main():
    """Start the FastAPI server."""
    logger.info("Starting Divine Pattern Analyzer API Server")
    
    # Get port from environment or use default
    port = int(os.getenv("PORT", 8080))
    
    # Run server
    uvicorn.run(
        "omega_ai.wavelength.api:app",
        host="0.0.0.0",
        port=port,
        log_level=os.getenv("LOG_LEVEL", "info").lower(),
        reload=os.getenv("ENVIRONMENT", "production").lower() != "production",
    )
    
if __name__ == "__main__":
    main() 