#!/usr/bin/env python3
"""
Quantum 5D QA Dashboard Application
---------------------------------

This module provides the main Dash application for the Quantum 5D QA Dashboard.
"""

import os
import sys
import logging
import dash
import dash_bootstrap_components as dbc
from dash import html

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Quantum5DQADashboard")

# Import dashboard modules
from .config import DASHBOARD_CONFIG, quantum_theme, INDEX_TEMPLATE
from .layout import create_dashboard_layout
from .callbacks import register_callbacks
from .connection import ConnectionManager


def create_app():
    """Create and configure the Dash application."""
    # Create Dash app
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.DARKLY],
        title="Quantum 5D QA Dashboard",
        update_title="Updating...",
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"}
        ],
        index_string=INDEX_TEMPLATE
    )
    
    # Set layout
    app.layout = create_dashboard_layout()
    
    # Register callbacks
    register_callbacks(app)
    
    return app


def run_app(host='0.0.0.0', port=8051, debug=False, open_browser=False):
    """Run the Dash application with automatic port detection.
    
    Args:
        host: Host IP to listen on
        port: Port to try using (will auto-detect if taken)
        debug: Whether to run in debug mode
        open_browser: Whether to open the dashboard in a browser
    """
    # Create connection manager for auto port detection
    connection = ConnectionManager(host=host, port=port)
    host, port = connection.get_connection_info()
    
    # Create app
    app = create_app()
    
    # Print connection information
    connection.print_connection_info()
    
    # Open in browser if requested
    if open_browser:
        connection.open_dashboard()
    
    # Run server
    try:
        app.run(host=host, port=port, debug=debug)
    except OSError as e:
        if "Address already in use" in str(e):
            logger.error(f"Port {port} is already in use. Please try a different port.")
            sys.exit(1)
        else:
            raise


if __name__ == '__main__':
    # Get port from command line args
    port = 8051
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            logger.warning(f"Invalid port: {sys.argv[1]}. Using default port 8051.")
    
    # Run app
    run_app(port=port) 