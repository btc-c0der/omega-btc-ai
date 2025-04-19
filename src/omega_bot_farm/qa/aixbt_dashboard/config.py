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
AIXBT Dashboard Configuration Module
----------------------------------

Configuration settings for the AIXBT Dashboard, including token metrics,
UI theme settings, and visualization parameters.
"""

import os
import logging
from typing import Dict, Any, Optional, Callable

# Configure logging
logger = logging.getLogger("AIXBTDashboard.Config")

# AIXBT Token Configuration
TOKEN_CONFIG = {
    "entry_price": 0.08198,
    "current_price": 0.07841,
    "leverage": 4,
    "token_quantity": 51552,
    "price_target": 1.00,
    "fees_rate": 0.001,  # 0.1%
    "symbol": "AIXBTUSDT"  # Trading symbol for price feed
}

# Calculate important levels
LIQUIDATION_PRICE = TOKEN_CONFIG["entry_price"] * (1 - 1 / TOKEN_CONFIG["leverage"])
BREAKEVEN_PRICE = TOKEN_CONFIG["entry_price"] + (
    TOKEN_CONFIG["entry_price"] * 
    TOKEN_CONFIG["fees_rate"] * 
    TOKEN_CONFIG["leverage"]
)

# Dashboard UI Configuration
UI_CONFIG = {
    "refresh_interval": 5,  # seconds
    "animation_speed": 0.75,
    "dark_mode": True,
    "fullscreen_default": False,
    "price_feed_interval": 2.0,  # seconds for price feed updates
    "use_websocket": True,  # whether to use WebSocket for price feed
}

# OMEGA Trap Zone™ Configuration
TRAP_CONFIG = {
    "trap_start": 0.072,  # price trap bottom
    "trap_end": 0.078,    # price trap top
    "emergency_alert": 0.0760,  # alert threshold
}

# Fibonacci Vortex Configuration
FIBONACCI_LEVELS = [
    0.000,  # baseline
    0.236,
    0.382,
    0.5,
    0.618,
    0.786,
    1.0,
    1.618,
    2.618
]

# Escape path configuration
ESCAPE_PATH = [
    {"price": 0.0768, "label": "Final Bot Wipe"},
    {"price": 0.0775, "label": "EMF Reversal"},
    {"price": 0.0789, "label": "Fibonacci Arc"},
    {"price": 0.08198, "label": "ENTRY BREAKOUT"},
    {"price": 0.0850, "label": "Sky Is Open"},
]

# Dashboard theme colors
THEME = {
    "background": "#0A0E17",  # Dark space background
    "panel": "#121A29",        # Panel background
    "success": "#00B894",      # Success color
    "warning": "#FDCB6E",      # Warning color
    "error": "#E17055",        # Error color
    "text": "#DCDDE1",         # Text color
    "accent1": "#6C5CE7",      # Purple
    "accent2": "#00CEC9",      # Teal
    "accent3": "#74B9FF",      # Blue
    "accent4": "#A29BFE",      # Light purple
    "grid": "#2D3436",         # Grid lines
    "highlight": "#FD79A8",    # Highlight
    "gold": "#FFD700",         # Gold for PnL
}

# BitGet exchange configuration
EXCHANGE_CONFIG = {
    "exchange_id": "bitget",
    "use_testnet": os.environ.get("USE_TESTNET", "false").lower() == "true",
    "api_key": os.environ.get("BITGET_API_KEY", ""),
    "api_secret": os.environ.get("BITGET_SECRET_KEY", ""),
    "api_passphrase": os.environ.get("BITGET_PASSPHRASE", ""),
}

# Consolidate all configs
DASHBOARD_CONFIG = {
    "token": TOKEN_CONFIG,
    "ui": UI_CONFIG,
    "trap": TRAP_CONFIG,
    "fibonacci": FIBONACCI_LEVELS,
    "escape_path": ESCAPE_PATH,
    "theme": THEME,
    "liquidation_price": LIQUIDATION_PRICE,
    "breakeven_price": BREAKEVEN_PRICE,
    "exchange": EXCHANGE_CONFIG
}

# Runtime calculated values (updated dynamically)
RUNTIME_VALUES = {
    "current_price": TOKEN_CONFIG["current_price"],
    "pnl": 0.0,
    "pnl_percentage": 0.0,
}

# Callback functions for status updates
_price_update_callbacks: list[Callable[[float], None]] = []

def update_current_price(price: float) -> None:
    """
    Update the current price and recalculate PnL.
    
    Args:
        price: Current price of the token
    """
    # Update runtime values
    RUNTIME_VALUES["current_price"] = price
    TOKEN_CONFIG["current_price"] = price
    
    # Recalculate PnL
    entry_price = TOKEN_CONFIG["entry_price"]
    token_quantity = TOKEN_CONFIG["token_quantity"]
    leverage = TOKEN_CONFIG["leverage"]
    
    # Calculate PnL
    pnl = (price - entry_price) * token_quantity * leverage
    pnl_percentage = ((price / entry_price) - 1) * 100 * leverage
    
    RUNTIME_VALUES["pnl"] = pnl
    RUNTIME_VALUES["pnl_percentage"] = pnl_percentage
    
    # Notify all registered callbacks
    for callback in _price_update_callbacks:
        try:
            callback(price)
        except Exception as e:
            logger.error(f"Error in price update callback: {e}")

def register_price_update_callback(callback: Callable[[float], None]) -> None:
    """
    Register a callback function that will be called when price is updated.
    
    Args:
        callback: Function that takes a price (float) as argument
    """
    if callback not in _price_update_callbacks:
        _price_update_callbacks.append(callback)

def unregister_price_update_callback(callback: Callable[[float], None]) -> None:
    """
    Unregister a price update callback.
    
    Args:
        callback: Function to unregister
    """
    if callback in _price_update_callbacks:
        _price_update_callbacks.remove(callback)

def get_current_price() -> float:
    """
    Get the current price.
    
    Returns:
        Current price as float
    """
    return RUNTIME_VALUES["current_price"]

def get_current_pnl() -> float:
    """
    Get the current PnL.
    
    Returns:
        Current PnL as float
    """
    return RUNTIME_VALUES["pnl"]

def get_current_pnl_percentage() -> float:
    """
    Get the current PnL percentage.
    
    Returns:
        Current PnL percentage as float
    """
    return RUNTIME_VALUES["pnl_percentage"]

# Initialize runtime values
update_current_price(TOKEN_CONFIG["current_price"]) 