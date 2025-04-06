#!/usr/bin/env python3
"""
AIXBT Dashboard - WSGI Configuration
----------------------------------

WSGI configuration file for hosting the AIXBT Dashboard with Gunicorn.

Usage:
    gunicorn -w 4 -b 0.0.0.0:8055 src.omega_bot_farm.qa.aixbt_dashboard.wsgi:server
"""

import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] AIXBT.WSGI: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("AIXBTDashboard.WSGI")

# Add parent directory to path for imports if needed
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in os.sys.path:
    os.sys.path.append(str(project_root))

# Import app creation function
from src.omega_bot_farm.qa.aixbt_dashboard.app import create_app

# Create and configure the app
app = create_app()

# WSGI server variable for Gunicorn
server = app.server

if __name__ == '__main__':
    logger.info("Running the app via WSGI module")
    app.run_server(host='0.0.0.0', port=8055, debug=False) 