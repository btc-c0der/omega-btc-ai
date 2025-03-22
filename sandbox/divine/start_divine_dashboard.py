#!/usr/bin/env python3
"""
OMEGA BTC AI - Divine Alignment Dashboard Launcher
==================================================

Launches the Divine Alignment Dashboard with trader personas on port 5051.

Usage:
    python start_divine_dashboard.py [--no-browser]

Options:
    --no-browser    Don't automatically open browser window

Author: OMEGA BTC AI Team
Version: 2.0
"""

import os
import sys
import argparse
import subprocess
import webbrowser
import time
import threading
import signal
from pathlib import Path

# ANSI color codes for terminal output
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"

def print_banner():
    """Print a stylized banner for the Divine Alignment Dashboard."""
    print(f"""
{MAGENTA}╔══════════════════════════════════════════════════════════════════╗{RESET}
{MAGENTA}║{YELLOW}                                                                  {MAGENTA}║{RESET}
{MAGENTA}║{YELLOW}  ⬤ ⬤ ⬤  OMEGA BTC AI - DIVINE ALIGNMENT DASHBOARD V2  ⬤ ⬤ ⬤  {MAGENTA}║{RESET}
{MAGENTA}║{YELLOW}                                                                  {MAGENTA}║{RESET}
{MAGENTA}╚══════════════════════════════════════════════════════════════════╝{RESET}

{GREEN}JAH BLESS OMEGA FIBONACCI GOLDEN RATIO AI{RESET}

{CYAN}Launching Divine Alignment Dashboard with Trader Personas on port 5051{RESET}

{YELLOW}Features:{RESET}
  • Golden Ratio Price Analysis
  • Trader Personas with Performance Metrics
  • Divine Alignment Signals
  • Fibonacci Retracement Tracking

{CYAN}This assembly is not mechanical—it's rhythmic. Each opcode has intention.{RESET}
""")

def run_flask_app():
    """Run the Flask API for the dashboard."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    api_script = os.path.join(script_dir, 'golden_ratio_api.py')
    
    # Set environment variables
    env = os.environ.copy()
    env["FLASK_APP"] = api_script
    env["FLASK_ENV"] = "development"
    
    # Start Flask app on port 5051
    process = subprocess.Popen(
        [sys.executable, api_script],
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
            print(f"{BLUE}[API] {output.strip()}{RESET}")
        
        # Read errors
        error = process.stderr.readline()
        if error:
            print(f"{RED}[API ERROR] {error.strip()}{RESET}")
        
        # Small delay to prevent high CPU usage
        time.sleep(0.1)

def signal_handler(sig, frame):
    """Handle interrupt signals gracefully."""
    print(f"\n{YELLOW}Shutting down Divine Alignment Dashboard...{RESET}")
    stop_event.set()
    
    # Allow a moment for threads to clean up
    time.sleep(1)
    
    # Force exit if still running
    sys.exit(0)

def open_dashboard(url, delay=2):
    """Open the dashboard in web browser after a delay."""
    def _open_url():
        time.sleep(delay)
        print(f"{GREEN}Opening Divine Alignment Dashboard in browser: {url}{RESET}")
        webbrowser.open(url)
    
    # Start in a separate thread
    browser_thread = threading.Thread(target=_open_url)
    browser_thread.daemon = True
    browser_thread.start()

def main():
    """Main entry point for the Divine Alignment Dashboard launcher."""
    parser = argparse.ArgumentParser(description="Launch the OMEGA BTC AI Divine Alignment Dashboard")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser automatically")
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start Flask app
    flask_process = run_flask_app()
    
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
        open_dashboard("http://localhost:5051/divine")
    
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
        
        print(f"{GREEN}Divine Alignment Dashboard stopped successfully.{RESET}")

if __name__ == "__main__":
    main() 