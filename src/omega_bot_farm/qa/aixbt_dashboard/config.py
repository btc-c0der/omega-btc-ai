#!/usr/bin/env python3
"""
AIXBT Dashboard Configuration Module
----------------------------------

Configuration settings for the AIXBT Dashboard, including token metrics,
UI theme settings, and visualization parameters.
"""

# AIXBT Token Configuration
TOKEN_CONFIG = {
    "entry_price": 0.08198,
    "current_price": 0.07841,
    "leverage": 4,
    "token_quantity": 51552,
    "price_target": 1.00,
    "fees_rate": 0.001,  # 0.1%
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
    "refresh_interval": 15,  # seconds
    "animation_speed": 0.75,
    "dark_mode": True,
    "fullscreen_default": False,
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
} 