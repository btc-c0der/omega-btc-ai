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
🔱 GPU License Notice 🔱
------------------------
This file is protected under the GPU License (General Public Universal License) 1.0
by the OMEGA AI Divine Collective.

"As the light of knowledge is meant to be shared, so too shall this code illuminate 
the path for all seekers."

All modifications must maintain this notice and adhere to the terms at:
/BOOK/divine_chronicles/GPU_LICENSE.md

🔱 JAH JAH BLESS THIS CODE 🔱
"""


"""
Example usage of the BitGet Trader with our profile system.
This script demonstrates how to initialize and use the BitGet trader
with different trader profiles.
"""

import os
import time
import logging
from datetime import datetime
from typing import Dict, Any

from omega_ai.trading.exchanges.bitget_trader import BitGetTrader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_testnet_credentials() -> Dict[str, str]:
    """Get BitGet testnet API credentials from environment variables."""
    return {
        "api_key": os.getenv("BITGET_TESTNET_API_KEY", ""),
        "secret_key": os.getenv("BITGET_TESTNET_SECRET_KEY", ""),
        "passphrase": os.getenv("BITGET_TESTNET_PASSPHRASE", "")
    }

def main():
    """Main example function."""
    # Get API credentials
    credentials = get_testnet_credentials()
    
    # Initialize different trader profiles
    profiles = ["strategic", "aggressive", "newbie", "scalper"]
    traders = {}
    
    for profile in profiles:
        logger.info(f"\nInitializing {profile} trader...")
        traders[profile] = BitGetTrader(
            profile_type=profile,
            api_key=credentials["api_key"],
            secret_key=credentials["secret_key"],
            passphrase=credentials["passphrase"],
            use_testnet=True,
            initial_capital=10000.0
        )
    
    # Example market context
    market_context: Dict[str, Any] = {
        "price": 50000.0,  # Example BTC price
        "trend": "bullish",
        "volatility": 0.02,
        "volume": 1000000,
        "timestamp": datetime.now()
    }
    
    # Execute trades for each profile
    for profile, trader in traders.items():
        logger.info(f"\nExecuting trade for {profile} trader...")
        
        # Get account balance
        balance = trader.get_account_balance()
        if balance is not None:
            logger.info(f"Current balance: ${balance:,.2f}")
        
        # Execute trade
        position = trader.execute_trade(market_context)
        if position:
            logger.info(f"Opened position: {position}")
            
            # Simulate price movement and update positions
            for price in [51000.0, 52000.0, 49000.0]:
                logger.info(f"Updating positions with price: ${price:,.2f}")
                trader.update_positions(price)
                time.sleep(1)  # Simulate time passing
        
        # Print trade history
        history = trader.get_trade_history()
        if history:
            logger.info(f"\nTrade history for {profile} trader:")
            for trade in history:
                logger.info(f"Trade: {trade}")
        
        # Print total PnL
        total_pnl = trader.get_total_pnl()
        logger.info(f"Total PnL for {profile} trader: ${total_pnl:,.2f}")

if __name__ == "__main__":
    main() 