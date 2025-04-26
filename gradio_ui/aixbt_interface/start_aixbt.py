#!/usr/bin/env python3
# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"""AIXBT Interface Entry Point.

This script handles:
1. Environment configuration
2. Redis connection setup
3. Interface initialization
4. Error handling and logging
"""

import os
import sys
import logging
from dotenv import load_dotenv
from app import create_interface

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("aixbt")

def main():
    """Initialize and start the AIXBT interface."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Create and launch interface
        interface = create_interface()
        interface.queue().launch(
            server_name="0.0.0.0",
            server_port=int(os.getenv("PORT", 7860)),
            share=os.getenv("SHARE", "true").lower() == "true",
            debug=os.getenv("DEBUG", "true").lower() == "true"
        )
        
    except Exception as e:
        logger.error(f"Failed to start AIXBT interface: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()