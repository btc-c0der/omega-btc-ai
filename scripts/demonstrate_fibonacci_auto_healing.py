#!/usr/bin/env python3

"""
Demonstrate the auto-healing capabilities of the Fibonacci detector.

This script will:
1. Clear any existing Fibonacci data in Redis
2. Generate good Fibonacci data
3. Corrupt the data in various ways
4. Show the system automatically healing itself
5. Verify the system can handle all error scenarios
"""

import json
import time
import redis
import random
import sys
import os
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add parent directory to path to import omega_ai modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

try:
    from omega_ai.mm_trap_detector.fibonacci_detector import (
        get_current_fibonacci_levels,
        update_fibonacci_data,
        check_fibonacci_alignment,
        fibonacci_detector
    )
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error(f"sys.path: {sys.path}")
    logger.error(f"Current directory: {os.getcwd()}")
    logger.error(f"Project root: {project_root}")
    raise

# Initialize Redis connection
redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def clear_fibonacci_data():
    """Clear all Fibonacci-related data from Redis."""
    keys = redis_conn.keys("fibonacci*")
    keys.extend(redis_conn.keys("*fibonacci*"))
    
    if keys:
        redis_conn.delete(*keys)
        logger.info(f"Cleared {len(keys)} Fibonacci-related keys from Redis")
    else:
        logger.info("No Fibonacci-related keys found in Redis")

def initialize_good_data():
    """Initialize Redis with good Fibonacci data."""
    # Generate sample swing points
    fibonacci_detector.recent_swing_high = 60000.0
    fibonacci_detector.recent_swing_low = 50000.0
    
    # Generate levels
    levels = fibonacci_detector.generate_fibonacci_levels()
    
    # Store in Redis
    if levels:
        redis_conn.set("fibonacci_levels", json.dumps(levels))
        logger.info(f"Initialized Redis with good Fibonacci data: {len(levels)} levels")
    else:
        logger.warning("Failed to generate Fibonacci levels")
        
    redis_conn.set("last_btc_price", "55000.0")
    
    return levels or {}

def corrupt_data(corruption_type: str):
    """Corrupt the Fibonacci data in Redis in various ways."""
    if corruption_type == "invalid_json":
        redis_conn.set("fibonacci_levels", "this is not valid json")
        logger.info("Corrupted Fibonacci data with invalid JSON")
    
    elif corruption_type == "missing_data":
        redis_conn.delete("fibonacci_levels")
        logger.info("Deleted Fibonacci levels from Redis")
    
    elif corruption_type == "mixed_types":
        # Get current levels
        levels_str = redis_conn.get("fibonacci_levels")
        if not levels_str:
            logger.error("No Fibonacci levels found in Redis")
            return
        
        # Parse levels safely
        try:    
            levels = json.loads(levels_str)
        except json.JSONDecodeError:
            logger.warning("Cannot corrupt data - current data is already corrupted (invalid JSON)")
            # Generate new valid data as fallback
            fibonacci_detector.recent_swing_high = 60000.0
            fibonacci_detector.recent_swing_low = 50000.0
            levels = fibonacci_detector.generate_fibonacci_levels() or {}
            redis_conn.set("fibonacci_levels", json.dumps(levels))
            
        # Corrupt some values with mixed types
        corrupted = {}
        for key, value in levels.items():
            # Randomly corrupt about 30% of values
            r = random.random()
            if r < 0.1:
                corrupted[key] = str(value)  # Convert to string
            elif r < 0.2:
                corrupted[key] = "not_a_number"  # Invalid string
            elif r < 0.3:
                corrupted[key] = None  # None value
            else:
                corrupted[key] = value  # Keep as is
                
        # Store corrupted data back in Redis
        redis_conn.set("fibonacci_levels", json.dumps(corrupted))
        logger.info(f"Corrupted Fibonacci data with mixed types: {corrupted}")
    
    elif corruption_type == "invalid_swing_points":
        # Set invalid swing points
        fibonacci_detector.recent_swing_high = None
        fibonacci_detector.recent_swing_low = None
        logger.info("Set invalid swing points (None)")

def test_auto_healing(corruption_type: str):
    """Test auto-healing after a specific type of corruption."""
    logger.info(f"\n{'=' * 20} TESTING AUTO-HEALING: {corruption_type} {'=' * 20}")
    
    # First initialize good data
    original_levels = initialize_good_data()
    
    # Verify we can get alignment with good data
    alignment_before = check_fibonacci_alignment()
    if alignment_before:
        logger.info(f"Alignment before corruption: {alignment_before['level']} at ${alignment_before['price']:.2f}")
    else:
        logger.warning("No alignment found before corruption")
    
    # Now corrupt the data
    corrupt_data(corruption_type)
    
    # Try to get levels after corruption
    try:
        levels_after = get_current_fibonacci_levels()
        if levels_after:
            logger.info(f"Successfully retrieved {len(levels_after)} levels after corruption")
            if levels_after == original_levels:
                logger.info("✅ AUTO-HEALING SUCCESS: Recovered original levels")
            else:
                logger.info("✅ AUTO-HEALING SUCCESS: Generated new valid levels")
        else:
            logger.warning("Retrieved empty levels after corruption")
    except Exception as e:
        logger.error(f"Error retrieving levels after corruption: {e}")
    
    # Try to get alignment after corruption
    try:
        alignment_after = check_fibonacci_alignment()
        if alignment_after:
            logger.info(f"Successfully found alignment after corruption: {alignment_after['level']} at ${alignment_after['price']:.2f}")
            logger.info("✅ AUTO-HEALING SUCCESS: Alignment check works despite corruption")
        else:
            logger.warning("No alignment found after corruption")
    except Exception as e:
        logger.error(f"Error checking alignment after corruption: {e}")
    
    logger.info(f"{'=' * 70}\n")
    
    # Clean up for next test
    clear_fibonacci_data()
    time.sleep(1)  # Small delay between tests

def run_all_tests():
    """Run through all auto-healing test scenarios."""
    logger.info("Starting auto-healing demonstration")
    
    # First clean any existing data
    clear_fibonacci_data()
    
    # Test different corruption types
    test_auto_healing("invalid_json")
    test_auto_healing("missing_data")
    test_auto_healing("mixed_types")
    test_auto_healing("invalid_swing_points")
    
    # Test a sequence of corruptions
    logger.info("\n" + "=" * 30 + " TESTING SEQUENTIAL CORRUPTIONS " + "=" * 30)
    initialize_good_data()
    
    # Get alignment before any corruption
    alignment = check_fibonacci_alignment()
    if alignment:
        logger.info(f"Initial alignment: {alignment['level']} at ${alignment['price']:.2f}")
    
    # First corrupt with invalid JSON
    corrupt_data("invalid_json")
    alignment = check_fibonacci_alignment()
    if alignment:
        logger.info(f"Alignment after invalid JSON: {alignment['level']} at ${alignment['price']:.2f}")
    
    # Then corrupt with mixed types
    corrupt_data("mixed_types")
    alignment = check_fibonacci_alignment()
    if alignment:
        logger.info(f"Alignment after mixed types: {alignment['level']} at ${alignment['price']:.2f}")
    
    # Finally delete the data
    corrupt_data("missing_data")
    alignment = check_fibonacci_alignment()
    if alignment:
        logger.info(f"Alignment after missing data: {alignment['level']} at ${alignment['price']:.2f}")
    else:
        logger.warning("No alignment found after sequential corruptions")
    
    logger.info("=" * 80)
    logger.info("Auto-healing demonstration completed")

if __name__ == "__main__":
    run_all_tests() 