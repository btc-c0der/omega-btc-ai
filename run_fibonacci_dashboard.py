#!/usr/bin/env python3
"""
OMEGA BTC AI - Run Fibonacci Dashboard
====================================

This script starts the BitGet Fibonacci Golden Ratio monitoring dashboard server.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import os
import sys
import argparse
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run BitGet Fibonacci Dashboard")
    
    parser.add_argument(
        "--host", 
        type=str, 
        default="0.0.0.0",
        help="Server host (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=8002,
        help="Server port (default: 8002)"
    )
    
    parser.add_argument(
        "--testnet", 
        action="store_true",
        help="Use BitGet testnet"
    )
    
    parser.add_argument(
        "--symbol", 
        type=str, 
        default="BTCUSDT",
        help="Trading symbol (default: BTCUSDT)"
    )
    
    return parser.parse_args()

def main():
    """Run the Fibonacci Dashboard server."""
    # Load environment variables from .env file
    load_dotenv()
    
    # Parse command line arguments
    args = parse_args()
    
    # Set environment variables
    if args.testnet:
        os.environ["BITGET_USE_TESTNET"] = "True"
        # Use testnet API keys if available
        if "BITGET_TESTNET_API_KEY" in os.environ:
            os.environ["BITGET_API_KEY"] = os.environ["BITGET_TESTNET_API_KEY"]
        if "BITGET_TESTNET_SECRET_KEY" in os.environ:
            os.environ["BITGET_SECRET_KEY"] = os.environ["BITGET_TESTNET_SECRET_KEY"]
        if "BITGET_TESTNET_PASSPHRASE" in os.environ:
            os.environ["BITGET_PASSPHRASE"] = os.environ["BITGET_TESTNET_PASSPHRASE"]
    else:
        os.environ["BITGET_USE_TESTNET"] = "False"
    
    os.environ["BITGET_SYMBOL"] = args.symbol
    
    # Check for API credentials
    if not os.environ.get("BITGET_API_KEY"):
        logger.error("BITGET_API_KEY environment variable not set")
        sys.exit(1)
    
    if not os.environ.get("BITGET_SECRET_KEY"):
        logger.error("BITGET_SECRET_KEY environment variable not set")
        sys.exit(1)
    
    if not os.environ.get("BITGET_PASSPHRASE"):
        logger.error("BITGET_PASSPHRASE environment variable not set")
        sys.exit(1)
    
    # Log configuration
    logger.info("Starting BitGet Fibonacci Dashboard")
    logger.info(f"Host: {args.host}")
    logger.info(f"Port: {args.port}")
    logger.info(f"Testnet: {args.testnet}")
    logger.info(f"Symbol: {args.symbol}")
    
    # Import and start the server
    from omega_ai.api.fibonacci_dashboard_server import start_server
    
    # Start the server
    start_server(host=args.host, port=args.port)

if __name__ == "__main__":
    main() 