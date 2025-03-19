#!/usr/bin/env python3

"""
OMEGA BTC AI - Live Mode Test
============================

Test script to verify live trading functionality with enhanced safety checks.
"""

import asyncio
import logging
import os
from datetime import datetime, timezone
from typing import Dict, Any
from dotenv import load_dotenv

from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders
from omega_ai.alerts.telegram_market_report import send_telegram_alert

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify_trading_environment() -> bool:
    """Verify that the trading environment is properly configured."""
    required_vars = [
        "BITGET_API_KEY",
        "BITGET_SECRET_KEY",
        "BITGET_PASSPHRASE",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        return False
        
    # Verify Telegram connection
    test_msg = "🔄 Testing live trading environment setup..."
    if not await send_telegram_alert(test_msg):
        logger.error("❌ Failed to send test message to Telegram")
        return False
        
    return True

async def test_live_mode():
    """Test live trading mode with enhanced safety checks."""
    # Load environment variables
    load_dotenv()
    
    # Verify environment before starting
    if not await verify_trading_environment():
        logger.error("❌ Environment verification failed. Aborting live trading test.")
        return
    
    # Initialize live trader with API credentials
    live_trader = BitGetLiveTraders(
        use_testnet=False,  # Live mode
        initial_capital=24.0,
        symbol="BTCUSDT",
        api_key=os.getenv("BITGET_API_KEY", ""),
        secret_key=os.getenv("BITGET_SECRET_KEY", ""),
        passphrase=os.getenv("BITGET_PASSPHRASE", "")
    )
    
    try:
        # Initialize the system
        await live_trader.initialize()
        logger.info("✅ Successfully initialized live trader")
        
        # Send live mode alert
        await send_telegram_alert(
            "🚨 OMEGA BTC AI ENTERING LIVE MODE 🚨\n\n"
            "Initial capital: 24.0 USDT per trader\n"
            "Trading pair: BTCUSDT\n"
            f"Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
            "🙏 JAH BLESS THE DIVINE SIGNALS! 🙏"
        )
        
        # Start trading
        logger.info("🚀 Starting live trading...")
        await live_trader.start_trading()
        
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    except Exception as e:
        logger.error(f"Error in live mode test: {e}")
        # Send error alert
        await send_telegram_alert(
            f"❌ ERROR IN LIVE TRADING:\n{str(e)}\n\n"
            "System will attempt graceful shutdown."
        )
    finally:
        # Ensure proper shutdown
        try:
            await live_trader.stop_trading()
            logger.info("💫 Live trading test completed")
            # Send shutdown alert
            await send_telegram_alert(
                "🛑 OMEGA BTC AI LIVE MODE SHUTDOWN\n\n"
                "All positions have been closed.\n"
                "Trading system stopped safely.\n\n"
                "🙏 JAH PROTECT THE DIVINE GAINS! 🙏"
            )
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

if __name__ == "__main__":
    asyncio.run(test_live_mode()) 