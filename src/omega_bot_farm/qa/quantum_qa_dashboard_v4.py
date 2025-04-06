#!/usr/bin/env python3
"""
S0NN3T 5D Quantum QA Cyberpunk Matrix Dashboard v4
------------------------------------------------

Enhanced entry point for the Quantum 5D QA Dashboard with version management
and improved connection handling.

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
import webbrowser
from typing import Dict, Any, Optional, Tuple

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

# Import connection manager
try:
    from quantum_dashboard.connection import ConnectionManager
except ImportError:
    print("Failed to import connection manager. Using built-in port detection.")
    ConnectionManager = None

# Check for version management
try:
    from quantum_dashboard.version_check import check_version
    HAS_VERSION_CHECK = True
except ImportError:
    print("Version check module not found. Skipping version checking.")
    HAS_VERSION_CHECK = False

# Import the dashboard module
try:
    from quantum_dashboard.app import run_app
except ImportError:
    print("Failed to import dashboard module. Make sure you're in the correct directory.")
    sys.exit(1)


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'


def display_matrix_boot_sequence():
    """Display a Matrix-style boot sequence."""
    print("\033[2J\033[H")  # Clear screen and move cursor to home position
    
    text = f"""
    {Colors.GREEN}
     _______  _______  _        _        _______  _______    _______  ______  
    (  ____ \\(  ___  )( (    /|( (    /|(  ____ \\(  ____ )  (  ____ \\(  __  \\ 
    | (    \\/| (   ) ||  \\  ( ||  \\  ( || (    \\/| (    )|  | (    \\/| (  \\  )
    | (_____ | |   | ||   \\ | ||   \\ | || (__    | (____)|  | (__    | |   ) |
    (_____  )| |   | || (\\ \\) || (\\ \\) ||  __)   |     __)  |  __)   | |   | |
          ) || |   | || | \\   || | \\   || (      | (\\ (     | (      | |   ) |
    /\\____) || (___) || )  \\  || )  \\  || (____/\\| ) \\ \\__  | )      | (__/  )
    \\_______)(_______)|/    )_)|/    )_)(_______/|/   \\__/  |/       (______/ 
                                                                            
     ______   _______  _______           ______   _______  _______           
    (  ___ \\ (  ___  )(  ___  )|\\     /|(  ___ \\ (  ___  )(  ____ \\|\\     /|
    | (   ) )| (   ) || (   ) || )   ( || (   ) )| (   ) || (    \\/| )   ( |
    | (__/ / | |   | || (___) || |   | || (__/ / | |   | || (_____ | (___) |
    |  __ (  | |   | ||  ___  || |   | ||  __ (  | |   | |(_____  )|  ___  |
    | (  \\ \\ | |   | || (   ) || |   | || (  \\ \\ | |   | |      ) || (   ) |
    | )___) )| (___) || )   ( || (___) || )___) )| (___) |/\\____) || )   ( |
    |/ \\___/ (_______)|/     \\|(_______)|/ \\___/ (_______)\\______)|/     \\|
                                                                          
                                     
         🧬 🌸 ✨ QUANTUM TRANSCENDENCE INITIALIZED ✨ 🌸 🧬
    {Colors.ENDC}
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
        time.sleep(random.uniform(0.2, 0.5))
        print(f"{Colors.GREEN}[✓] {item}{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}🌀 S0NN3T 5D QUANTUM QA CYBERPUNK MATRIX DASHBOARD READY 🌀{Colors.ENDC}\n")
    time.sleep(0.5)


def check_dependencies() -> bool:
    """
    Check for required packages.
    
    Returns:
        True if all dependencies are met, False otherwise.
    """
    dependencies_ok = True
    
    try:
        import plotly
        logger.info(f"Using Plotly version: {plotly.__version__}")
    except ImportError:
        logger.error("Plotly package is required. Please install it with 'pip install plotly'")
        print(f"{Colors.RED}ERROR: Plotly package is required. Please install it with 'pip install plotly'{Colors.ENDC}")
        dependencies_ok = False
    
    try:
        from dash import dcc
        logger.info("Dash component check passed")
    except ImportError:
        logger.error("Dash components are required. Please install with 'pip install dash'")
        print(f"{Colors.RED}ERROR: Dash components are required. Please install with 'pip install dash'{Colors.ENDC}")
        dependencies_ok = False
    
    return dependencies_ok


def handle_connection(args) -> Tuple[str, int]:
    """
    Handle connection details and port availability.
    
    Args:
        args: Command line arguments
        
    Returns:
        Tuple of (host, port)
    """
    if ConnectionManager:
        # Use ConnectionManager for advanced connection handling
        connection = ConnectionManager(
            host=args.host,
            port=args.port,
            max_port_tries=10
        )
        
        # Get connection info
        host, port = connection.get_connection_info()
        
        # Print connection info
        if port != args.port:
            print(f"{Colors.YELLOW}Requested port {args.port} is unavailable. Using port {port} instead.{Colors.ENDC}")
        
        connection.print_connection_info()
        
        # Open browser if requested
        if args.browser:
            connection.open_dashboard()
        
        return host, port
    else:
        # Fallback to basic connection handling
        return args.host, args.port


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
    parser.add_argument('--auto-archive', action='store_true',
                        help='Automatically archive changes if detected')
    parser.add_argument('--version-type', choices=["major", "minor", "patch"],
                        default="patch", help='Version increment type if auto-archive')
    
    args = parser.parse_args()
    
    # Display boot sequence if not disabled
    if not args.no_matrix_boot:
        display_matrix_boot_sequence()
    
    # Check version if version check is available
    if HAS_VERSION_CHECK:
        version_info = check_version()
        
        # If auto-archive is enabled and changes detected, update the entry point
        if args.auto_archive and version_info.get("changes_detected", False):
            print(f"{Colors.YELLOW}Changes detected in dashboard files. Updating version...{Colors.ENDC}")
            try:
                from quantum_dashboard.version_manager import get_dashboard_version_manager
                version_manager = get_dashboard_version_manager()
                
                # Create a new version
                release_info = version_manager.create_dashboard_release(
                    version_type=args.version_type,
                    commit=True
                )
                
                print(f"{Colors.GREEN}Successfully created version {release_info['version']}{Colors.ENDC}")
                print(f"{Colors.BLUE}Changelog:{Colors.ENDC}\n{release_info['changelog']}")
            except ImportError:
                print(f"{Colors.YELLOW}Version manager not available. Skipping version update.{Colors.ENDC}")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Handle connection
    host, port = handle_connection(args)
    
    # Run the app
    try:
        run_app(
            host=host,
            port=port,
            debug=args.debug,
            open_browser=args.browser
        )
    except Exception as e:
        logger.error(f"Error starting dashboard: {e}")
        print(f"{Colors.RED}ERROR: Failed to start dashboard: {e}{Colors.ENDC}")
        print(f"{Colors.YELLOW}Try running with --debug flag for more information{Colors.ENDC}")
        if "already in use" in str(e).lower():
            print(f"{Colors.YELLOW}Try a different port with: --port 8052{Colors.ENDC}")
        sys.exit(1)


if __name__ == '__main__':
    main() 