#!/usr/bin/env python3
"""
OMEGA BTC AI - REGGAE DASHBOARD Launcher
==========================================

Launches the REGGAE DASHBOARD with rhythm pattern analysis for Bitcoin trading.

Usage:
    python start_reggae_dashboard.py [--no-browser] [--port PORT]

Options:
    --no-browser    Don't automatically open browser window
    --port PORT     Specify custom port (default: auto-detect available port)

Author: OMEGA BTC AI Team
Version: 1.0
"""

import os
import sys
import argparse
import subprocess
import webbrowser
import time
import threading
import signal
import socket
from pathlib import Path

# ANSI color codes for terminal output
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"

def print_banner(port):
    """Print a stylized Rastafarian banner for the REGGAE DASHBOARD."""
    print(f"""
{RED}╔══════════════════════════════════════════════════════════════════╗{RESET}
{RED}║{YELLOW}                                                                  {RED}║{RESET}
{RED}║{YELLOW}  ⬤ ⬤ ⬤  OMEGA BTC AI - REGGAE DASHBOARD V1.0  ⬤ ⬤ ⬤  {RED}║{RESET}
{RED}║{YELLOW}                                                                  {RED}║{RESET}
{RED}╚══════════════════════════════════════════════════════════════════╝{RESET}

{GREEN}JAH BLESS THE RHYTHM OF THE MARKETS{RESET}

{YELLOW}Launching REGGAE DASHBOARD with BTC Rhythm Analysis on port {port}{RESET}

{GREEN}Features:{RESET}
  • Rhythm Pattern Recognition
  • Dub Analysis of Price Action
  • Rastafarian Color Indicators
  • Roots Trading Strategy
  • Babylon System Alerts

{RED}I{YELLOW}N{GREEN}I BTC RHYTHM IS THE PULSE OF DIGITAL FREEDOM{RESET}
""")

def check_port_available(port):
    """Check if the port is available."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result != 0  # If result is 0, port is in use
    except socket.error:
        return False

def find_available_port(start_port, max_attempts=100):
    """Find an available port starting from the given port."""
    port = start_port
    for _ in range(max_attempts):
        if check_port_available(port):
            return port
        port += 1
    
    # If no ports are available in the range, return None
    return None

def run_flask_app(port):
    """Run the Flask API for the dashboard."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    api_script = os.path.join(script_dir, 'reggae_rhythm_api.py')
    
    # Set environment variables
    env = os.environ.copy()
    env["FLASK_APP"] = api_script
    env["FLASK_ENV"] = "development"
    
    # Start Flask app on specified port
    process = subprocess.Popen(
        [sys.executable, api_script, "--port", str(port)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    return process

def monitor_process(process, stop_event):
    """Monitor the Flask process and print output."""
    while not stop_event.is_set() and process.poll() is None:
        # Read output
        output = process.stdout.readline()
        if output:
            print(f"{GREEN}[API] {output.strip()}{RESET}")
        
        # Read errors
        error = process.stderr.readline()
        if error:
            print(f"{RED}[API ERROR] {error.strip()}{RESET}")
        
        # Small delay to prevent high CPU usage
        time.sleep(0.1)

def signal_handler(sig, frame):
    """Handle interrupt signals gracefully."""
    print(f"\n{YELLOW}Shutting down REGGAE DASHBOARD...{RESET}")
    stop_event.set()
    
    # Allow a moment for threads to clean up
    time.sleep(1)
    
    # Force exit if still running
    sys.exit(0)

def open_dashboard(url, delay=2):
    """Open the dashboard in web browser after a delay."""
    def _open_url():
        time.sleep(delay)
        print(f"{GREEN}Opening REGGAE DASHBOARD in browser: {url}{RESET}")
        webbrowser.open(url)
    
    # Start in a separate thread
    browser_thread = threading.Thread(target=_open_url)
    browser_thread.daemon = True
    browser_thread.start()

def main():
    """Main entry point for the REGGAE DASHBOARD launcher."""
    parser = argparse.ArgumentParser(description="Launch the OMEGA BTC AI REGGAE DASHBOARD")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser automatically")
    parser.add_argument("--port", type=int, default=5053, help="Port to run the dashboard on (default: 5053)")
    args = parser.parse_args()
    
    # Check if the specified port is available
    if not check_port_available(args.port):
        print(f"{YELLOW}Port {args.port} is already in use.{RESET}")
        new_port = find_available_port(args.port + 1)
        if new_port:
            print(f"{GREEN}Using alternative port: {new_port}{RESET}")
            args.port = new_port
        else:
            print(f"{RED}No available ports found in range {args.port} to {args.port + 100}.{RESET}")
            sys.exit(1)
    
    # Print banner with the port that will be used
    print_banner(args.port)
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start Flask app
    flask_process = run_flask_app(args.port)
    
    # Create stop event for threads
    global stop_event
    stop_event = threading.Event()
    
    # Monitor Flask process in a thread
    monitor_thread = threading.Thread(
        target=monitor_process,
        args=(flask_process, stop_event)
    )
    monitor_thread.daemon = True
    monitor_thread.start()
    
    # Open browser if not disabled
    if not args.no_browser:
        open_dashboard(f"http://localhost:{args.port}/reggae")
    
    try:
        # Keep the main thread alive
        while not stop_event.is_set() and flask_process.poll() is None:
            time.sleep(0.5)
    except KeyboardInterrupt:
        # Handle Ctrl+C
        signal_handler(signal.SIGINT, None)
    finally:
        # Clean up
        if flask_process.poll() is None:
            print(f"{YELLOW}Terminating Flask process...{RESET}")
            flask_process.terminate()
            flask_process.wait(timeout=5)
        
        print(f"{GREEN}REGGAE DASHBOARD stopped successfully.{RESET}")

if __name__ == "__main__":
    main() 