#!/usr/bin/env python3
"""
S0NN3T 5D Quantum QA Cyberpunk Matrix Dashboard
----------------------------------------------

This script provides an entry point to run the enhanced S0NN3T 5D Quantum QA Dashboard
with the Cyberpunk Matrix test runner interface.

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

import os
import sys
import argparse
import logging
import random
import time

# Add the parent directory to the path so we can import the dashboard module
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("S0NN3T5DQuantumDashboard")

# Import the dashboard module
try:
    from quantum_dashboard.app import run_app
except ImportError:
    print("Failed to import dashboard module. Make sure you're in the correct directory.")
    sys.exit(1)


def display_matrix_boot_sequence():
    """Display a Matrix-style boot sequence."""
    print("\033[2J\033[H")  # Clear screen and move cursor to home position
    
    text = """
    \033[32m
     _______  _______  _        _        _______  _______    _______  ______  
    (  ____ \(  ___  )( (    /|( (    /|(  ____ \(  ____ )  (  ____ \(  __  \ 
    | (    \/| (   ) ||  \  ( ||  \  ( || (    \/| (    )|  | (    \/| (  \  )
    | (_____ | |   | ||   \ | ||   \ | || (__    | (____)|  | (__    | |   ) |
    (_____  )| |   | || (\ \) || (\ \) ||  __)   |     __)  |  __)   | |   | |
          ) || |   | || | \   || | \   || (      | (\ (     | (      | |   ) |
    /\____) || (___) || )  \  || )  \  || (____/\| ) \ \__  | )      | (__/  )
    \_______)(_______)|/    )_)|/    )_)(_______/|/   \__/  |/       (______/ 
                                                                            
     ______   _______  _______           ______   _______  _______           
    (  ___ \ (  ___  )(  ___  )|\     /|(  ___ \ (  ___  )(  ____ \|\     /|
    | (   ) )| (   ) || (   ) || )   ( || (   ) )| (   ) || (    \/| )   ( |
    | (__/ / | |   | || (___) || |   | || (__/ / | |   | || (_____ | (___) |
    |  __ (  | |   | ||  ___  || |   | ||  __ (  | |   | |(_____  )|  ___  |
    | (  \ \ | |   | || (   ) || |   | || (  \ \ | |   | |      ) || (   ) |
    | )___) )| (___) || )   ( || (___) || )___) )| (___) |/\____) || )   ( |
    |/ \___/ (_______)|/     \|(_______)|/ \___/ (_______)\_______)|/     \|
                                                                         
                                     
         🧬 🌸 ✨ QUANTUM TRANSCENDENCE INITIALIZED ✨ 🌸 🧬
    \033[0m
    """
    
    print(text)
    
    # Simulate loading process
    loading_items = [
        "Initializing hyperspatial matrices...",
        "Calibrating quantum entanglement...",
        "Synchronizing dimensional stability...",
        "Loading cyberpunk interface...",
        "Engaging S0NN3T neural networks...",
        "Establishing 5D test connections...",
        "Activating F0R3ST RUN protocols...",
        "Enabling REAL-TIME STREAMING..."
    ]
    
    for item in loading_items:
        # Random loading time between 0.2 and 0.8 seconds
        time.sleep(random.uniform(0.2, 0.8))
        print(f"\033[32m[✓] {item}\033[0m")
    
    print("\n\033[1;32m🌀 S0NN3T 5D QUANTUM QA CYBERPUNK MATRIX DASHBOARD READY 🌀\033[0m\n")
    time.sleep(1)


def main():
    """Main entry point for the S0NN3T 5D Quantum QA Dashboard."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='S0NN3T 5D Quantum QA Cyberpunk Matrix Dashboard')
    parser.add_argument('--port', type=int, default=8051, 
                        help='Port to run the dashboard on (default: 8051)')
    parser.add_argument('--host', type=str, default='0.0.0.0', 
                        help='Host to run the dashboard on (default: 0.0.0.0)')
    parser.add_argument('--debug', action='store_true', 
                        help='Run in debug mode')
    parser.add_argument('--browser', action='store_true', 
                        help='Open dashboard in browser after starting')
    parser.add_argument('--enable-test-runner', action='store_true', 
                        help='Enable the Cyberpunk Matrix Test Runner interface', default=True)
    parser.add_argument('--no-matrix-boot', action='store_true', 
                        help='Disable Matrix boot sequence animation')
    
    args = parser.parse_args()
    
    # Display boot sequence if not disabled
    if not args.no_matrix_boot:
        display_matrix_boot_sequence()
    
    # Print startup message
    print(f"\033[1;32mStarting S0NN3T 5D Quantum QA Cyberpunk Matrix Dashboard on http://{args.host}:{args.port}\033[0m")
    print("\033[1;32mPress Ctrl+C to stop the dashboard\033[0m")
    
    # Run the app with auto port detection
    run_app(
        host=args.host,
        port=args.port,
        debug=args.debug,
        open_browser=args.browser
    )


if __name__ == '__main__':
    main() 