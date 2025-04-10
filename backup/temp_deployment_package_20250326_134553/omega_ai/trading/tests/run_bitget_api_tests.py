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
BitGet API Test Runner

This script runs the BitGet API test suite with command line arguments
to control which tests to run and which environment to use.
"""

import os
import sys
import argparse
import logging
from tests.test_bitget_api import run_tests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Run BitGet API tests')
    
    # Environment options
    parser.add_argument('--testnet', action='store_true', default=True,
                      help='Use testnet environment (default)')
    parser.add_argument('--mainnet', action='store_true', 
                      help='Use mainnet environment (BE CAREFUL!)')
    
    # API version
    parser.add_argument('--api-version', type=str, default='v1',
                      choices=['v1', 'v2'],
                      help='API version to test (default: v1)')
    
    # Test options
    parser.add_argument('--enable-order-tests', action='store_true',
                      help='Enable tests that place real orders (with minimal amounts)')
    parser.add_argument('--test-amount', type=float, default=0.0001,
                      help='Test amount for order tests (default: 0.0001 BTC)')
    
    # Credentials
    parser.add_argument('--api-key', type=str, default='',
                      help='BitGet API key (default: from .env)')
    parser.add_argument('--secret-key', type=str, default='',
                      help='BitGet secret key (default: from .env)')
    parser.add_argument('--passphrase', type=str, default='',
                      help='BitGet API passphrase (default: from .env)')
    
    # Output options
    parser.add_argument('--verbose', action='store_true',
                      help='Enable verbose output')
    
    return parser.parse_args()


def main():
    """Run BitGet API tests with command line arguments."""
    args = parse_args()
    
    # Set environment variables from command line arguments
    if args.api_key:
        os.environ['BITGET_API_KEY'] = args.api_key
    if args.secret_key:
        os.environ['BITGET_SECRET_KEY'] = args.secret_key
    if args.passphrase:
        os.environ['BITGET_PASSPHRASE'] = args.passphrase
    
    # Set testnet/mainnet
    if args.mainnet:
        os.environ['USE_TESTNET'] = '0'
        logger.warning("Using MAINNET environment - BE CAREFUL!")
    else:
        os.environ['USE_TESTNET'] = '1'
        logger.info("Using TESTNET environment")
    
    # Set API version
    os.environ['API_VERSION'] = args.api_version
    logger.info(f"Using API version: {args.api_version}")
    
    # Set order test options
    if args.enable_order_tests:
        os.environ['ENABLE_ORDER_TESTS'] = '1'
        logger.warning("ORDER TESTS ENABLED - Will place real orders with minimal amounts!")
    else:
        os.environ['ENABLE_ORDER_TESTS'] = '0'
        logger.info("Order tests disabled - Only running read-only tests")
    
    # Set test amount
    os.environ['TEST_AMOUNT'] = str(args.test_amount)
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose output enabled")
        
    # Run tests
    logger.info("Starting BitGet API tests...")
    run_tests()


if __name__ == "__main__":
    main() 