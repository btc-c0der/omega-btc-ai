#!/usr/bin/env python3
"""
AIXBT Dashboard App Module
-----------------------

Main application module for the AIXBT Trading Dashboard, integrating all components
and providing the entry point to run the dashboard.
"""

import os
import sys
import webbrowser
import socket
import logging
from pathlib import Path
import dash
import dash_bootstrap_components as dbc
from typing import Optional, Tuple

from . import logger
from .layout import create_dashboard_layout
from .callbacks import register_callbacks
from .config import DASHBOARD_CONFIG

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

def create_app() -> dash.Dash:
    """
    Create and configure the Dash application.
    
    Returns:
        Configured Dash app instance
    """
    # Create assets folder if it doesn't exist
    assets_dir = Path(__file__).parent / "assets"
    assets_dir.mkdir(exist_ok=True)
    
    # Create Dash app
    app = dash.Dash(
        __name__,
        external_stylesheets=[
            dbc.themes.CYBORG,
            "https://use.fontawesome.com/releases/v5.15.4/css/all.css"
        ],
        suppress_callback_exceptions=True,
        title="AIXBT Trading Dashboard",
        meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
    )
    
    # Set app layout
    app.layout = create_dashboard_layout()
    
    # Register callbacks
    register_callbacks(app)
    
    return app

def run_app(
    host: str = "0.0.0.0",
    port: int = 8051,
    debug: bool = False,
    open_browser: bool = True
) -> None:
    """
    Run the AIXBT Dashboard application.
    
    Args:
        host: Host address to bind to
        port: Port number to bind to
        debug: Whether to run in debug mode
        open_browser: Whether to open a browser tab to the dashboard
    """
    # Create the app
    app = create_app()
    
    # Find an available port if the specified port is not available
    if not is_port_available(host, port):
        logger.warning(f"Port {port} is not available. Finding an available port...")
        port = find_available_port(port)
        logger.info(f"Using port {port} instead")
    
    # Print starting message
    logger.info(f"Starting AIXBT Trading Dashboard on http://{host}:{port}")
    
    # Open browser if requested
    if open_browser:
        webbrowser.open_new_tab(f"http://localhost:{port}")
    
    # Run the app
    app.run(debug=debug, host=host, port=port)

if __name__ == "__main__":
    # Run the app with default settings
    run_app(debug=True)