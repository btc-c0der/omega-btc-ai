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