#!/usr/bin/env python3
"""
OMEGA BTC AI - Divine Alignment Dashboard Launcher
==================================================

Launches the Divine Alignment Dashboard with trader personas on port 5051.

Usage:
    python start_divine_dashboard.py [--no-browser] [--port PORT]

Options:
    --no-browser    Don't automatically open browser window
    --port PORT     Specify custom port (default: 5051)

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
    """Print a stylized banner for the Divine Alignment Dashboard."""
    print(f"""
{MAGENTA}╔══════════════════════════════════════════════════════════════════╗{RESET}
{MAGENTA}║{YELLOW}                                                                  {MAGENTA}║{RESET}
{MAGENTA}║{YELLOW}  ⬤ ⬤ ⬤  OMEGA BTC AI - DIVINE ALIGNMENT DASHBOARD V2  ⬤ ⬤ ⬤  {MAGENTA}║{RESET}
{MAGENTA}║{YELLOW}                                                                  {MAGENTA}║{RESET}
{MAGENTA}╚══════════════════════════════════════════════════════════════════╝{RESET}

{GREEN}JAH BLESS OMEGA FIBONACCI GOLDEN RATIO AI{RESET}

{CYAN}Launching Divine Alignment Dashboard with Trader Personas on port {port}{RESET}

{YELLOW}Features:{RESET}
  • Golden Ratio Price Analysis
  • Trader Personas with Performance Metrics
  • Divine Alignment Signals
  • Fibonacci Retracement Tracking

{CYAN}This assembly is not mechanical—it's rhythmic. Each opcode has intention.{RESET}
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
    api_script = os.path.join(script_dir, 'golden_ratio_api.py')
    
    # Set environment variables
    env = os.environ.copy()
    env["FLASK_APP"] = api_script
    env["FLASK_ENV"] = "development"
    env["PYTHONUNBUFFERED"] = "1"  # Ensure output is not buffered
    
    try:
        # Start Flask app on specified port
        process = subprocess.Popen(
            [sys.executable, api_script, "--port", str(port)],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1  # Line buffered
        )
        
        return process
        
    except Exception as e:
        print(f"{RED}Error starting Flask app: {e}{RESET}")
        return None

def monitor_process(process, stop_event):
    """Monitor the Flask process and handle output."""
    while not stop_event.is_set():
        try:
            # Read output line by line
            stdout_line = process.stdout.readline()
            if stdout_line:
                if "[API]" in stdout_line:
                    print(f"{GREEN}{stdout_line.strip()}{RESET}")
                else:
                    print(stdout_line.strip())
            
            stderr_line = process.stderr.readline()
            if stderr_line:
                if "WARNING" in stderr_line:
                    print(f"{YELLOW}[API WARNING] {stderr_line.strip()}{RESET}")
                else:
                    print(f"{RED}[API ERROR] {stderr_line.strip()}{RESET}")
            
            # Check if process has terminated
            if process.poll() is not None:
                print(f"{RED}Flask process terminated unexpectedly{RESET}")
                break
                
            time.sleep(0.1)  # Small delay to prevent CPU spinning
            
        except Exception as e:
            print(f"{RED}Error monitoring process: {e}{RESET}")
            break

def signal_handler(sig, frame):
    """Handle graceful shutdown on CTRL+C."""
    print(f"\n{YELLOW}Stopping Divine Alignment Dashboard...{RESET}")
    stop_event.set()
    
    if flask_process:
        try:
            flask_process.terminate()
            flask_process.wait(timeout=5)  # Wait up to 5 seconds
        except subprocess.TimeoutExpired:
            flask_process.kill()  # Force kill if not terminated
        except Exception as e:
            print(f"{RED}Error stopping Flask process: {e}{RESET}")
    
    print(f"{GREEN}Divine Alignment Dashboard stopped successfully.{RESET}")
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
    """Main function."""
    global flask_process, stop_event
    
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5051)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    
    # Find available port
    port = find_available_port(args.port)
    if not port:
        print(f"{RED}No available ports found!{RESET}")
        return 1
    
    # Print banner
    print_banner(port)
    
    # Start Flask app
    flask_process = run_flask_app(port)
    if not flask_process:
        return 1
    
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create stop event
    stop_event = threading.Event()
    
    # Start monitor thread
    monitor_thread = threading.Thread(
        target=monitor_process,
        args=(flask_process, stop_event),
        daemon=True
    )
    monitor_thread.start()
    
    # Open dashboard in browser
    if not args.no_browser:
        url = f"http://localhost:{port}/divine"
        print(f"Opening Divine Alignment Dashboard in browser: {url}")
        threading.Thread(target=open_dashboard, args=(url,), daemon=True).start()
    
    try:
        # Keep main thread alive
        while not stop_event.is_set():
            time.sleep(0.1)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
    
    return 0

if __name__ == "__main__":
    flask_process = None
    stop_event = None
    sys.exit(main()) 