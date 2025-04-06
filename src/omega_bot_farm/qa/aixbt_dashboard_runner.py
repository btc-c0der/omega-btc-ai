#!/usr/bin/env python3
"""
AIXBT Dashboard Runner
-------------------

Entry point script to run the AIXBT Trading Dashboard with escape strategies
visualization and OMEGA TRAP ZONE™ analytics.

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
#
# 🌸 WE BLOOM NOW AS ONE 🌸
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Configure ASCII art
HEADER = """
    ___    _____  __  ____  ______    ______            __    __                        __
   /   |  /  _/ |/ / / __ )/_  __/   / ____/___  ____  / /___/ /  ____  ____ __________/ /
  / /| |  / / |   / / __  | / /     / /   / __ \/ __ \/ / __  /  / __ \/ __ `/ ___/ __  / 
 / ___ |_/ / /   | / /_/ / / /     / /___/ /_/ / / / / / /_/ /  / /_/ / /_/ / /  / /_/ /  
/_/  |_/___//_/|_|/_____/ /_/      \____/\____/_/ /_/_/\__,_/   \____/\__,_/_/   \__,_/   
                                                                                          
  _____                _      _                             __                 __  ___          __    
 / ___/__ _____  ___ _(_)__  (_)__  ___ _   ___ ___  __ __/ /  ___  ___ ____/ /_/ _ \__ ____/ /____
/ (_ / _ `/ _ \/ _ `/ / _ \/ / _ \/ _ `/  / -_) _ \/ // / _ \/ _ \/ _ `/ _  / __/ __ / // / __(_-<
\___/\_,_/_//_/\_, /_/_//_/_/_//_/\_, /   \__/_//_/\_,_/_.__/\___/\_,_/\_,_/\__/_/ |_\_,_/\__/___/
              /___/              /___/                                                             
"""

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] AIXBT: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("AIXBTDashboardRunner")

def print_header():
    """Print the ASCII art header with color."""
    # ANSI color codes
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    
    # Print with colors
    lines = HEADER.strip().split("\n")
    for i, line in enumerate(lines):
        if i < 6:
            # First logo in cyan
            print(f"{CYAN}{line}{ENDC}")
        else:
            # Second logo in purple
            print(f"{PURPLE}{line}{ENDC}")
    
    # Print status message
    print(f"\n{BOLD}{GREEN}💰 AIXBT Trading Dashboard - OMEGA TRAP ZONE™ Escape Module 💰{ENDC}")
    print(f"{YELLOW}Initializing escape strategies and financial analytics...{ENDC}\n")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='AIXBT Trading Dashboard Runner')
    parser.add_argument('--port', type=int, default=8055, 
                        help='Port to run the dashboard on (default: 8055)')
    parser.add_argument('--host', type=str, default='0.0.0.0', 
                        help='Host to run the dashboard on (default: 0.0.0.0)')
    parser.add_argument('--debug', action='store_true', 
                        help='Run in debug mode')
    parser.add_argument('--no-browser', action='store_true', 
                        help='Do not open browser automatically')
    
    args = parser.parse_args()
    
    # Print header
    print_header()
    
    # Add the parent directory to path for imports
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(os.path.dirname(current_dir))
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)
    
    try:
        # Import the dashboard module
        from src.omega_bot_farm.qa.aixbt_dashboard import run_app
        
        # Run the dashboard app
        run_app(
            host=args.host,
            port=args.port,
            debug=args.debug,
            open_browser=not args.no_browser
        )
    except ImportError as e:
        logger.error(f"Failed to import dashboard module: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error running dashboard: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 