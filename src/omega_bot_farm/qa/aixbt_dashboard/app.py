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
AIXBT Dashboard - Main Application
----------------------------------

Main application module for the AIXBT Trading Dashboard.
Creates and configures the Dash application with all components.
"""

import os
import sys
import webbrowser
import socket
import logging
from pathlib import Path
import dash
from dash import html
import dash_bootstrap_components as dbc
from typing import Optional, Tuple
from threading import Timer

from . import logger
from .config import DASHBOARD_CONFIG as AIXBT_CONFIG
from .layout import create_dashboard_layout as create_layout
from .callbacks import register_callbacks

# Conditionally import price feed
try:
    from .price_feed import init_price_feed, get_price_feed
    from .config import update_current_price, get_current_price
    HAVE_PRICE_FEED = True
except ImportError:
    logger.warning("Price feed module not available or CCXT not installed")
    HAVE_PRICE_FEED = False

def is_port_available(host: str, port: int) -> bool:
    """
    Check if the specified port is available on the host.
    
    Args:
        host: Host address to check
        port: Port number to check
        
    Returns:
        True if port is available, False otherwise
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return True
        except:
            return False

def find_available_port(start_port: int, max_attempts: int = 10) -> int:
    """
    Find an available port starting from start_port.
    
    Args:
        start_port: Port number to start checking from
        max_attempts: Maximum number of ports to check
        
    Returns:
        Available port number
    """
    host = "0.0.0.0"  # Check on all interfaces
    
    for port in range(start_port, start_port + max_attempts):
        if is_port_available(host, port):
            return port
    
    # If no port found, raise an error
    raise RuntimeError(f"Could not find an available port after {max_attempts} attempts")

def open_browser(host: str, port: int) -> None:
    """
    Open a web browser to the dashboard URL.
    
    Args:
        host: Host address of the dashboard
        port: Port number of the dashboard
    """
    # Get a proper URL based on the host
    if host == "0.0.0.0":
        url = f"http://localhost:{port}"
    else:
        url = f"http://{host}:{port}"
    
    # Open the URL in a new browser tab
    webbrowser.open_new_tab(url)
    logger.info(f"Dashboard opened in browser at {url}")

def create_app():
    """
    Create and configure the Dash application without running it.
    Useful for testing or WSGI deployments.
    
    Returns:
        dash.Dash: Configured Dash application
    """
    # Create Dash app with Bootstrap Cyborg theme
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.CYBORG],
        title="AIXBT Trading Dashboard - OMEGA TRAP ZONE™",
        suppress_callback_exceptions=True,
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"}
        ]
    )
    
    # Set custom CSS directory
    app.css.config.serve_locally = True
    
    # Set up layout
    app.layout = create_layout()
    
    # Register callbacks
    register_callbacks(app)
    
    return app

def run_app(host="0.0.0.0", port=8055, debug=False, open_browser=True):
    """
    Run the AIXBT Dashboard application.
    
    Args:
        host (str): Host to run the dashboard on
        port (int): Port to run the dashboard on
        debug (bool): Whether to run in debug mode
        open_browser (bool): Whether to open browser automatically
    """
    # Create Dash app with Bootstrap Cyborg theme
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.CYBORG],
        title="AIXBT Trading Dashboard - OMEGA TRAP ZONE™",
        suppress_callback_exceptions=True,
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"}
        ]
    )
    
    # Set custom CSS directory
    app.css.config.serve_locally = True
    
    # Initialize real-time price feed if available
    if HAVE_PRICE_FEED:
        logger.info("Initializing real-time price feed...")
        try:
            # Get exchange config
            exchange_config = AIXBT_CONFIG.get("exchange", {})
            token_config = AIXBT_CONFIG.get("token", {})
            ui_config = AIXBT_CONFIG.get("ui", {})
            
            # Define price update callback
            def on_price_update(price: float):
                update_current_price(price)
                logger.debug(f"Price updated: {price:.5f}")
            
            # Initialize price feed
            init_price_feed(
                exchange_id=exchange_config.get("exchange_id", "bitget"),
                symbol=token_config.get("symbol", "AIXBTUSDT"),
                api_key=exchange_config.get("api_key"),
                api_secret=exchange_config.get("api_secret"),
                api_passphrase=exchange_config.get("api_passphrase"),
                use_testnet=exchange_config.get("use_testnet", False),
                update_callback=on_price_update,
                polling_interval=ui_config.get("price_feed_interval", 2.0),
                use_websocket=ui_config.get("use_websocket", True)
            )
            
            logger.info("Real-time price feed started successfully")
        except Exception as e:
            logger.error(f"Failed to initialize price feed: {e}")
    
    # Set up layout
    app.layout = create_layout()
    
    # Register callbacks
    register_callbacks(app)
    
    # Function to open browser
    def open_browser_tab():
        webbrowser.open_new_tab(f"http://localhost:{port}")
    
    # Open browser if requested
    if open_browser:
        Timer(1.5, open_browser_tab).start()
    
    # Run app
    app.run_server(
        host=host,
        port=port,
        debug=debug
    )

if __name__ == "__main__":
    # When run directly, use default parameters
    run_app(debug=True)