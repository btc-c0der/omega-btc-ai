#!/usr/bin/env python3
"""
OMEGA BTC AI - Fibonacci Trader Integration
=========================================

This module integrates the Fibonacci trader with the profile system and BitGetLiveTraders.
It provides functions to add Fibonacci traders to the BitGetLiveTraders system.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import os
import logging
from typing import Dict, List, Any, Optional, Union, cast
from omega_ai.trading.fibonacci_profile_trader import FibonacciProfileTrader
from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders
from omega_ai.exchange.bitget_client import BitGetClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def add_fibonacci_traders(live_traders: BitGetLiveTraders, profile_types: Optional[list] = None) -> Dict[str, Any]:
    """
    Add Fibonacci trader profiles to the BitGetLiveTraders system.
    
    Args:
        live_traders: BitGetLiveTraders instance to add traders to
        profile_types: List of profile types to add (default: ["strategic"])
        
    Returns:
        Dictionary of added traders
    """
    if profile_types is None:
        profile_types = ["strategic"]  # Default to strategic profile only
    
    added_traders = {}
    
    # Get credentials from the live_traders instance
    credentials = {
        "api_key": live_traders.api_key,
        "secret_key": live_traders.secret_key,
        "passphrase": live_traders.passphrase,
        "use_testnet": live_traders.use_testnet
    }
    
    for profile_type in profile_types:
        try:
            # Initialize Fibonacci trader with the profile
            trader = FibonacciProfileTrader(
                api_key=credentials["api_key"],
                api_secret=credentials["secret_key"],
                passphrase=credentials["passphrase"],
                symbol=live_traders.symbol,
                profile_type=profile_type,
                initial_capital=live_traders.initial_capital,
                leverage=live_traders.leverage
            )
            
            # Initialize the trader
            await trader.initialize()
            
            # Register trader with live_traders system
            trader_key = f"fibonacci_{profile_type}"
            
            # Add to custom traders dictionary instead of built-in traders
            if not hasattr(live_traders, 'custom_traders'):
                live_traders.custom_traders = {}
            live_traders.custom_traders[trader_key] = trader
            
            # Add to return dictionary
            added_traders[trader_key] = trader
            
            logger.info(f"Added Fibonacci {profile_type} trader to live traders system as custom trader")
            
        except Exception as e:
            logger.error(f"Error adding Fibonacci {profile_type} trader: {str(e)}")
    
    return added_traders

async def run_standalone_fibonacci_trader(
    symbol: str = "BTCUSDT",
    profile_type: str = "strategic",
    use_testnet: bool = True,
    initial_capital: float = 1000.0,
    leverage: int = 3,
    api_key: str = "",
    api_secret: str = "",
    passphrase: str = ""
) -> None:
    """
    Run a standalone Fibonacci trader with the specified profile.
    
    Args:
        symbol: Trading symbol (default: "BTCUSDT")
        profile_type: Trader profile type (default: "strategic")
        use_testnet: Whether to use testnet (default: True)
        initial_capital: Initial capital (default: 1000.0)
        leverage: Trading leverage (default: 3)
        api_key: BitGet API key (default: look in environment)
        api_secret: BitGet API secret (default: look in environment)
        passphrase: BitGet API passphrase (default: look in environment)
    """
    # Look for API credentials in environment variables if not provided
    api_key = api_key or os.environ.get("BITGET_TESTNET_API_KEY" if use_testnet else "BITGET_API_KEY", "")
    api_secret = api_secret or os.environ.get("BITGET_TESTNET_SECRET_KEY" if use_testnet else "BITGET_SECRET_KEY", "")
    passphrase = passphrase or os.environ.get("BITGET_TESTNET_PASSPHRASE" if use_testnet else "BITGET_PASSPHRASE", "")
    
    trader = None
    try:
        # Initialize Fibonacci trader with the profile
        trader = FibonacciProfileTrader(
            api_key=api_key,
            api_secret=api_secret,
            passphrase=passphrase,
            symbol=symbol,
            profile_type=profile_type,
            initial_capital=initial_capital,
            leverage=leverage
        )
        
        # Initialize and run the trader
        await trader.initialize()
        logger.info(f"Starting standalone Fibonacci {profile_type} trader on {symbol}...")
        await trader.run()
        
    except KeyboardInterrupt:
        if trader:
            logger.info("Stopping trader...")
            await trader.stop()
        logger.info("Trading stopped by user")
    except Exception as e:
        logger.error(f"Error running standalone Fibonacci trader: {str(e)}")
        if trader:
            await trader.stop()

async def initialize_bitget_with_fibonacci(
    symbol: str = "BTCUSDT",
    use_testnet: bool = True,
    initial_capital: float = 10000.0,
    leverage: int = 3,
    api_key: str = "",
    api_secret: str = "",
    passphrase: str = "",
    profile_types: Optional[List[str]] = None
) -> BitGetLiveTraders:
    """
    Initialize BitGetLiveTraders with Fibonacci profile traders.
    
    Args:
        symbol: Trading symbol (default: "BTCUSDT")
        use_testnet: Whether to use testnet (default: True)
        initial_capital: Initial capital (default: 10000.0)
        leverage: Trading leverage (default: 3)
        api_key: BitGet API key (default: look in environment)
        api_secret: BitGet API secret (default: look in environment)
        passphrase: BitGet API passphrase (default: look in environment)
        profile_types: List of profile types to add (default: ["strategic"])
        
    Returns:
        Initialized BitGetLiveTraders instance with Fibonacci traders
    """
    if profile_types is None:
        profile_types = ["strategic"]
    
    # Look for API credentials in environment variables if not provided
    api_key = api_key or os.environ.get("BITGET_TESTNET_API_KEY" if use_testnet else "BITGET_API_KEY", "")
    api_secret = api_secret or os.environ.get("BITGET_TESTNET_SECRET_KEY" if use_testnet else "BITGET_SECRET_KEY", "")
    passphrase = passphrase or os.environ.get("BITGET_TESTNET_PASSPHRASE" if use_testnet else "BITGET_PASSPHRASE", "")
    
    # Initialize BitGetLiveTraders
    live_traders = BitGetLiveTraders(
        use_testnet=use_testnet,
        initial_capital=initial_capital,
        symbol=symbol,
        api_key=api_key,
        secret_key=api_secret,
        passphrase=passphrase,
        leverage=leverage
    )
    
    # Initialize live traders
    await live_traders.initialize()
    
    # Add Fibonacci traders
    fibonacci_traders = await add_fibonacci_traders(live_traders, profile_types)
    
    # Add custom method to live_traders for accessing Fibonacci traders
    live_traders.fibonacci_traders = fibonacci_traders
    
    logger.info(f"BitGetLiveTraders initialized with {len(fibonacci_traders)} Fibonacci profile traders")
    
    return live_traders 