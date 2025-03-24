#!/usr/bin/env python3

"""
Test script to verify the fix for the error:
'unsupported operand type(s) for -: 'float' and 'str''
when calculating distance between current price and Fibonacci levels
"""

import sys
import os
import json
import logging
from unittest.mock import MagicMock, patch

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from omega_ai.mm_trap_detector.fibonacci_detector import check_fibonacci_alignment

def simulate_error_case():
    """
    Simulate the error case where Fibonacci levels contain string values
    that would cause 'unsupported operand type(s) for -: 'float' and 'str''
    """
    # Mock Redis to return string price
    mock_redis = MagicMock()
    mock_redis.get.side_effect = lambda key: {
        "last_btc_price": "35000.0",
        "fibonacci_levels": json.dumps({
            "0": 30000.0,
            "0.236": "31000.0",  # String value
            "0.382": 32000.0,
            "0.5": "33000.0",    # String value
            "0.618": 34000.0,
            "0.786": 35000.0,  # This will be near the current price
            "1.0": "not a number",    # Invalid string
            "1.618": "37000abc",  # Unparseable string
            "2.618": None   # None value
        })
    }.get(key)
    
    # Apply the mock
    with patch('omega_ai.mm_trap_detector.fibonacci_detector.redis_conn', mock_redis):
        # Run the function that would normally cause the error
        result = check_fibonacci_alignment()
        
        # Check the result
        if result:
            logger.info(f"Successfully found alignment despite problematic values: {result}")
            logger.info(f"Level: {result['level']}, Price: {result['price']}, Distance: {result['distance_pct']:.2%}")
            return True
        else:
            logger.warning("No alignment found")
            return False

if __name__ == "__main__":
    logger.info("Testing Fibonacci error case...")
    success = simulate_error_case()
    
    if success:
        logger.info("✅ Test passed! The error was properly handled.")
        sys.exit(0)
    else:
        logger.error("❌ Test failed! No alignment was found or an error occurred.")
        sys.exit(1) 