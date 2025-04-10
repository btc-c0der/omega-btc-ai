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
Run BitGet sub-account validation tests against the mainnet API.
"""

import os
import unittest
import sys
import logging

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import the test case
from tests.test_bitget_sub_account import TestLiveSubAccountValidation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Check for environment variables
    api_key = os.environ.get("BITGET_API_KEY", "")
    secret_key = os.environ.get("BITGET_SECRET_KEY", "")
    passphrase = os.environ.get("BITGET_PASSPHRASE", "")
    
    if not api_key or not secret_key or not passphrase:
        logger.error("ERROR: Missing BitGet API credentials in environment variables")
        logger.error("Please set BITGET_API_KEY, BITGET_SECRET_KEY, and BITGET_PASSPHRASE")
        sys.exit(1)
    
    # Check for sub-account name
    sub_account_name = os.environ.get("STRATEGIC_SUB_ACCOUNT_NAME", "")
    if sub_account_name:
        logger.info(f"Using sub-account: {sub_account_name}")
    else:
        logger.warning("No STRATEGIC_SUB_ACCOUNT_NAME set, will use default 'strategic_trader'")
    
    # Run only the live tests
    logger.info("Running live sub-account validation tests against BitGet mainnet...")
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLiveSubAccountValidation)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    
    # Exit with error code if tests failed
    if not result.wasSuccessful():
        sys.exit(1) 