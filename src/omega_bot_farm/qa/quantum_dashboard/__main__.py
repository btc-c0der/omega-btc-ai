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
Main entry point for the Quantum 5D QA Dashboard.

This module enables the dashboard to be run as a standalone application or as a Python module.
"""

import argparse
import logging
from .app import run_app

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Quantum5DQADashboard")


def main():
    """Run the Quantum 5D QA Dashboard with command line arguments."""
    parser = argparse.ArgumentParser(description="Quantum 5D QA Dashboard")
    parser.add_argument("--port", type=int, default=8051,
                        help="Port to run the dashboard on (default: 8051)")
    parser.add_argument("--host", type=str, default="0.0.0.0",
                        help="Host to run the dashboard on (default: 0.0.0.0)")
    parser.add_argument("--debug", action="store_true",
                        help="Run in debug mode")
    parser.add_argument("--browser", action="store_true",
                        help="Open dashboard in browser after starting")
    
    args = parser.parse_args()
    
    # Run the app with auto port detection
    run_app(
        host=args.host,
        port=args.port,
        debug=args.debug,
        open_browser=args.browser
    )


if __name__ == "__main__":
    main() 