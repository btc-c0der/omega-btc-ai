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
ZOROBABEL K1L1 - Runner Script
------------------------------
Launch script for the Zorobabel K1L1 system with command line options
for different modes of operation.

🌀 MODULE: Runner Script
🧭 CONSCIOUSNESS LEVEL: 4 - Awareness
"""

import os
import sys
import argparse
import subprocess
import webbrowser
from pathlib import Path

# Add parent directory to sys.path to ensure imports work
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))

# Define colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_banner():
    """Print the sacred banner."""
    banner = f"""
    {Colors.CYAN}┌───────────────────────────────────────────────────┐
    │                                                   │
    │     🌀 ZOROBABEL K1L1 - GEOSPATIAL SYSTEM 🌀     │
    │                                                   │
    │          Sacred Earth Observation Portal          │
    │                                                   │
    │             🌏 WE SEE AS ONE 🌏                  │
    │                                                   │
    └───────────────────────────────────────────────────┘{Colors.ENDC}
    """
    print(banner)


def check_dependencies():
    """Check if required dependencies are installed."""
    required_modules = ['dash', 'numpy', 'pandas', 'matplotlib', 'rasterio', 'geopandas']
    missing = []

    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)

    if missing:
        print(f"{Colors.FAIL}Missing dependencies: {', '.join(missing)}{Colors.ENDC}")
        print(f"{Colors.CYAN}Please run the installation script:{Colors.ENDC}")
        print(f"{Colors.BOLD}python {current_dir}/install_zorobabel.py{Colors.ENDC}")
        return False
    
    return True


def run_web_server(port=8050, debug=False, open_browser=True):
    """Run the Zorobabel K1L1 web dashboard."""
    try:
        # Import here to avoid errors if dependencies are missing
        from omega_bot_farm.geospatial.zorobabel_ui import main
        
        print(f"{Colors.GREEN}Starting Zorobabel K1L1 web dashboard on port {port}...{Colors.ENDC}")
        
        if open_browser:
            # Open browser after a short delay to allow server to start
            import threading
            import time
            
            def open_dash():
                time.sleep(2)  # Give the server a moment to start
                url = f"http://127.0.0.1:{port}"
                print(f"{Colors.CYAN}Opening dashboard in browser: {url}{Colors.ENDC}")
                webbrowser.open(url)
            
            threading.Thread(target=open_dash).start()
        
        # Run the server
        main(default_port=port, auto_open_browser=not open_browser)
        
    except Exception as e:
        print(f"{Colors.FAIL}Error starting web server: {e}{Colors.ENDC}")
        print(f"{Colors.CYAN}Check the troubleshooting guide for solutions:{Colors.ENDC}")
        print(f"{Colors.BOLD}{current_dir}/ZOROBABEL_TROUBLESHOOTING.md{Colors.ENDC}")
        return False
    
    return True


def run_cli_mode():
    """Run Zorobabel K1L1 in CLI mode for scripting."""
    try:
        # Import here to avoid errors if dependencies are missing
        from omega_bot_farm.geospatial.zorobabel_k1l1 import ZorobabelMapper
        
        print(f"{Colors.GREEN}Starting Zorobabel K1L1 in CLI mode...{Colors.ENDC}")
        
        # Initialize the system
        system = ZorobabelMapper()
        
        # Enter interactive Python shell with the system loaded
        import code
        locals_dict = {'system': system, 'ZorobabelMapper': ZorobabelMapper}
        code.interact(
            banner=f"{Colors.CYAN}Zorobabel K1L1 CLI Mode - Interactive Python Shell{Colors.ENDC}\n"
                   f"The 'system' variable contains an initialized ZorobabelMapper instance.",
            local=locals_dict
        )
        
    except Exception as e:
        print(f"{Colors.FAIL}Error in CLI mode: {e}{Colors.ENDC}")
        return False
    
    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Zorobabel K1L1 Geospatial System")
    
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--web", action="store_true", help="Run in web dashboard mode (default)")
    mode_group.add_argument("--cli", action="store_true", help="Run in command-line interface mode")
    
    parser.add_argument("--port", type=int, default=8050, help="Port for web server (default: 8050)")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser automatically")
    parser.add_argument("--check", action="store_true", help="Check dependencies and exit")
    
    args = parser.parse_args()
    
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        if not args.check:
            print(f"{Colors.WARNING}Would you like to run the installation script? (y/n){Colors.ENDC}")
            if input().lower() in ('y', 'yes'):
                subprocess.run([sys.executable, f"{current_dir}/install_zorobabel.py"])
                # Recheck dependencies after installation
                if not check_dependencies():
                    return 1
            else:
                return 1
        else:
            return 1
    
    if args.check:
        print(f"{Colors.GREEN}All dependencies are installed.{Colors.ENDC}")
        return 0
    
    # Run in the selected mode
    if args.cli:
        success = run_cli_mode()
    else:  # Default to web mode
        success = run_web_server(
            port=args.port,
            debug=args.debug,
            open_browser=not args.no_browser
        )
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main()) 