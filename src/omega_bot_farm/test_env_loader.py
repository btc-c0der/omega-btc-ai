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
Test script for the environment loader utility.

This script tests loading environment variables from both the root project .env file
and the bot farm's own .env file.
"""

import sys
import logging
import asyncio
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import environment loader
from src.omega_bot_farm.utils.env_loader import (
    get_env_var, get_bool_env_var, get_int_env_var, get_float_env_var
)

# Import BitgetPositionAnalyzerB0t
from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t


async def test_bitget_analyzer():
    """Test BitgetPositionAnalyzerB0t with loaded environment variables."""
    logger.info("Testing BitgetPositionAnalyzerB0t with loaded environment variables")
    
    # Get environment variables
    api_key = get_env_var("BITGET_API_KEY", "")
    api_secret = get_env_var("BITGET_SECRET_KEY", "")
    api_passphrase = get_env_var("BITGET_PASSPHRASE", "")
    use_testnet = get_bool_env_var("USE_TESTNET", False)
    
    # Log environment info
    logger.info(f"API Key available: {'Yes' if api_key else 'No'}")
    logger.info(f"API Secret available: {'Yes' if api_secret else 'No'}")
    logger.info(f"API Passphrase available: {'Yes' if api_passphrase else 'No'}")
    logger.info(f"Using Testnet: {use_testnet}")
    
    # Test BitgetPositionAnalyzerB0t parameters
    history_length = get_int_env_var("POSITION_HISTORY_LENGTH", 10)
    change_threshold = get_float_env_var("SIGNIFICANT_CHANGE_THRESHOLD", 5.0)
    logger.info(f"Position history length: {history_length}")
    logger.info(f"Significant change threshold: {change_threshold}")
    
    # Initialize analyzer with environment variables
    analyzer = BitgetPositionAnalyzerB0t(
        api_key=api_key,
        api_secret=api_secret,
        api_passphrase=api_passphrase,
        use_testnet=use_testnet,
        position_history_length=history_length
    )
    
    logger.info("BitgetPositionAnalyzerB0t initialized successfully")
    
    # Get positions
    positions_data = await analyzer.get_positions()
    
    # Log positions summary
    if "error" in positions_data:
        logger.error(f"Error getting positions: {positions_data['error']}")
    else:
        positions = positions_data.get("positions", [])
        logger.info(f"Found {len(positions)} active positions")
        
        # Log account info
        account = positions_data.get("account", {})
        logger.info(f"Account equity: {account.get('equity', 0)}")
        logger.info(f"Long exposure: {account.get('long_exposure', 0)}")
        logger.info(f"Short exposure: {account.get('short_exposure', 0)}")
        logger.info(f"Long/Short ratio: {account.get('long_short_ratio', 0)}")
        logger.info(f"Harmony score: {account.get('harmony_score', 0)}")
    
    return positions_data


async def main():
    """Main function to test environment loader."""
    logger.info("Starting environment loader test")
    
    # Log loaded environment variables
    logger.info("Environment variables from bot farm .env:")
    logger.info(f"LOG_LEVEL: {get_env_var('LOG_LEVEL', 'Not set')}")
    logger.info(f"REDIS_HOST: {get_env_var('REDIS_HOST', 'Not set')}")
    
    # Get numeric values with proper defaults
    position_history = get_int_env_var('POSITION_HISTORY_LENGTH', 0)
    logger.info(f"POSITION_HISTORY_LENGTH: {position_history if position_history else 'Not set'}")
    
    fibonacci_analysis = get_bool_env_var('ENABLE_FIBONACCI_ANALYSIS', False)
    logger.info(f"FIBONACCI_ANALYSIS: {fibonacci_analysis}")
    
    # Test BitgetPositionAnalyzerB0t
    positions_data = await test_bitget_analyzer()
    
    # Log detailed position information if available
    if "positions" in positions_data:
        positions = positions_data["positions"]
        logger.info("\nDetailed position information:")
        
        for i, position in enumerate(positions):
            symbol = position.get("symbol", "Unknown")
            side = position.get("side", "Unknown")
            entry_price = position.get("entryPrice", 0)
            mark_price = position.get("markPrice", 0)
            contracts = position.get("contracts", 0)
            unrealized_pnl = position.get("unrealizedPnl", 0)
            
            logger.info(f"Position {i+1}: {symbol} {side.upper()}")
            logger.info(f"  Entry: {entry_price}, Mark: {mark_price}")
            logger.info(f"  Size: {contracts}, PnL: {unrealized_pnl}")
            logger.info("---")
    
    logger.info("Environment loader test completed")


if __name__ == "__main__":
    asyncio.run(main()) 