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
OMEGA BTC AI - Divine Visualization Server
------------------------------------------
This script serves the divine coverage visualization files via a local HTTP server.
"""

import os
import sys
import glob
import webbrowser
import http.server
import socketserver
import threading
import time
import socket
from datetime import datetime

# ANSI colors for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_cosmic_banner():
    """Display a cosmic banner for the server."""
    print(f"{MAGENTA}{BOLD}╔══════════════════════════════════════════════════════════╗{RESET}")
    print(f"{MAGENTA}{BOLD}║      OMEGA DIVINE VISUALIZATION HTTP SERVER             ║{RESET}")
    print(f"{MAGENTA}{BOLD}║     🧠 COSMIC QUANTUM SERVER ACTIVATION 🧠             ║{RESET}")
    print(f"{MAGENTA}{BOLD}╚══════════════════════════════════════════════════════════╝{RESET}")
    print(f"{YELLOW}Manifesting the divine HTTP server for cosmic visualization...{RESET}")
    print()

def find_latest_visualization():
    """Find the latest divine visualization files."""
    # Find visualization directories
    viz_dirs = glob.glob("omega_viz_*")
    if not viz_dirs:
        return None
    
    # Sort by creation time (newest first)
    viz_dirs.sort(key=lambda x: os.path.getctime(x), reverse=True)
    latest_dir = viz_dirs[0]
    
    # Find HTML files
    html_files = glob.glob("omega_divine_coverage_*.html")
    if not html_files:
        return None
    
    # Sort by creation time (newest first)
    html_files.sort(key=lambda x: os.path.getctime(x), reverse=True)
    latest_html = html_files[0]
    
    return {
        "directory": latest_dir,
        "html_file": latest_html,
        "components": sorted(glob.glob(f"{latest_dir}/*.html"))
    }

def is_port_available(port):
    """Check if a port is available for use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return True
        except socket.error:
            return False

def find_available_port(start_port=8000, max_attempts=100):
    """Find the next available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        if is_port_available(port):
            return port
    
    # If no port is found after max_attempts, return None
    return None

def start_server(port=None):
    """Start the HTTP server on the specified port or find an available one."""
    visualization = find_latest_visualization()
    
    if not visualization:
        print(f"{RED}Error: No visualization files found.{RESET}")
        print(f"{YELLOW}Run the visualization first with: ./run_market_trends_tests.py --only-visualize{RESET}")
        return 1
    
    # If no port is specified, find an available one
    if port is None:
        port = find_available_port()
        if port is None:
            print(f"{RED}Error: Could not find an available port after multiple attempts.{RESET}")
            return 1
    else:
        # If a specific port was requested but is not available, find the next one
        if not is_port_available(port):
            print(f"{YELLOW}Requested port {port} is not available. Finding next available port...{RESET}")
            port = find_available_port(port + 1)
            if port is None:
                print(f"{RED}Error: Could not find an available port after multiple attempts.{RESET}")
                return 1
    
    print_cosmic_banner()
    print(f"{CYAN}Latest visualization found:{RESET}")
    print(f"{BLUE}- Main File: {visualization['html_file']}{RESET}")
    print(f"{BLUE}- Components Directory: {visualization['directory']}{RESET}")
    print(f"{BLUE}- Component Files:{RESET}")
    for comp in visualization['components']:
        print(f"{BLUE}  - {comp}{RESET}")
    print()
    
    # Start HTTP server
    handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            server_url = f"http://localhost:{port}"
            viz_url = f"{server_url}/{visualization['html_file']}"
            
            print(f"{GREEN}{BOLD}Divine HTTP Server activated on port {port}{RESET}")
            print(f"{CYAN}Server Root URL: {server_url}{RESET}")
            print(f"{CYAN}Visualization URL: {viz_url}{RESET}")
            print(f"{YELLOW}Press Ctrl+C to stop the server{RESET}")
            print()
            
            # Open browser in a separate thread after a short delay
            threading.Thread(target=lambda: open_browser_delayed(viz_url)).start()
            
            # Start server
            httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Divine server stopped by cosmic intervention.{RESET}")
    except Exception as e:
        print(f"\n{RED}Error: {str(e)}{RESET}")
        print(f"{YELLOW}Please try again or specify a different port: {sys.argv[0]} <port_number>{RESET}")
        return 1
    
    return 0

def open_browser_delayed(url, delay=1):
    """Open browser with a delay to allow server to start."""
    time.sleep(delay)
    print(f"{GREEN}Opening visualization in browser...{RESET}")
    webbrowser.open(url)

def main():
    """Main function to start the server."""
    port = None  # Default to auto-detection
    
    # Check if port is specified as command-line argument
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
            print(f"{CYAN}Attempting to use specified port: {port}{RESET}")
        except ValueError:
            print(f"{RED}Error: Invalid port number.{RESET}")
            print(f"{YELLOW}Usage: {sys.argv[0]} [port_number]{RESET}")
            print(f"{YELLOW}Falling back to auto port detection...{RESET}")
    
    # Start server
    return start_server(port)

if __name__ == "__main__":
    sys.exit(main()) 