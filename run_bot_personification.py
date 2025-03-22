#!/usr/bin/env python3
"""
Run OMEGA BTC AI - Bot Personification Dashboard

This script starts the bot personification dashboard server.
"""

import argparse
from omega_ai.personification.server import main

if __name__ == "__main__":
    # Setup command line argument parser
    parser = argparse.ArgumentParser(description="Run the OMEGA BTC AI Bot Personification Dashboard")
    parser.add_argument("-p", "--port", type=int, default=5042, 
                        help="Port to run the server on (default: 5042)")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run the server with the specified port
    main(port=args.port) 