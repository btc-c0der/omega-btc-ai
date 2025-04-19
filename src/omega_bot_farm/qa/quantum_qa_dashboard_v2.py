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
Quantum 5D QA Dashboard - Entry Point Script
-------------------------------------------

This script provides an entry point to run the Quantum 5D QA Dashboard
from the refactored modular package structure.
"""

import os
import sys
import argparse

# Add the parent directory to the path so we can import the dashboard module
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import the dashboard module
try:
    from quantum_dashboard.app import run_app
except ImportError:
    print("Failed to import dashboard module. Make sure you're in the correct directory.")
    sys.exit(1)


def main():
    """Main entry point for the dashboard."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Quantum 5D QA Dashboard')
    parser.add_argument('--port', type=int, default=8051, 
                        help='Port to run the dashboard on (default: 8051)')
    parser.add_argument('--host', type=str, default='0.0.0.0', 
                        help='Host to run the dashboard on (default: 0.0.0.0)')
    parser.add_argument('--debug', action='store_true', 
                        help='Run in debug mode')
    parser.add_argument('--browser', action='store_true', 
                        help='Open dashboard in browser after starting')
    
    args = parser.parse_args()
    
    # Run the app with auto port detection
    run_app(
        host=args.host,
        port=args.port,
        debug=args.debug,
        open_browser=args.browser
    )


if __name__ == '__main__':
    print("""
 ______                        __                      _____ ____     ________    
/ ____/_  ______ _____  ____ _/ /___  ______ ___     / ___// __ \   / ____/ /_   
/ /_  / / / / __ `/ __ \/ __ `/ __/ / / / __ `__ \    \__ \/ / / /  / /   / __ \  
/ __/ / /_/ / /_/ / / / / /_/ / /_/ /_/ / / / / / /   ___/ / /_/ /  / /___/ / / /  
/_/    \__,_/\__,_/_/ /_/\__,_/\__/\__,_/_/ /_/ /_/   /____/_____/   \____/_/ /_/   
                                                                                 
 ____               __    __                         __
/\  _`\            /\ \  /\ \                       /\ \\
\ \ \L\ \    __    \_\ \ \ \ \____     __    _ __   \_\ \
 \ \ ,  /  /'__`\  /'_` \ \ \ '__`\  /'__`\ /\`'__\ /'_` \\
  \ \ \\ \ /\ \L\.\_\ \L\ \ \ \ \L\ \/\ \L\.\\ \ \/ \ \L\ \\
   \ \_\ \_\ \__/.\_\\\\__,_\ \ \_,__/\ \__/.\_\\\ \_\  \__,_\\
    \/_/\/ /\/__/\/_/\/__,/  \/___/  \/__/\/_/ \/_/  \/__,/
    """)
    main() 