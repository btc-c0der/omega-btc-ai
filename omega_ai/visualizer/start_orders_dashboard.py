#!/usr/bin/env python3

"""
OMEGA BTC AI - Start Orders Dashboard Script
===========================================

This script starts both the backend and frontend servers for the Orders Dashboard.
The backend runs the FastAPI server for WebSocket data streaming, and the frontend
serves the HTML/JS/CSS dashboard UI.
"""

import os
import sys
import argparse
import subprocess
import time
import signal
import threading
import webbrowser
from pathlib import Path

# Terminal colors for blessed output
GREEN_RASTA = "\033[38;5;34m"    # Bright green (primary color)
GOLD_RASTA = "\033[38;5;220m"    # Gold/Yellow (secondary color)
RED_RASTA = "\033[38;5;196m"     # Bright red (tertiary color)
CYAN_INFO = "\033[38;5;51m"      # Cyan for information
RESET = "\033[0m"                # Reset formatting

# Find the project root
project_root = Path(__file__).parent.parent.parent.absolute()

# Define paths
backend_path = project_root / "omega_ai" / "visualizer" / "backend" / "rasta_orders_dashboard_server.py"
frontend_dir = project_root / "omega_ai" / "visualizer" / "frontend" / "orders-dashboard"

# Dict to store running processes
processes = {}

def print_rasta_banner():
    """Print a Rasta-themed banner."""
    print(f"""
{GREEN_RASTA}██████╗ ███╗   ███╗███████╗ ██████╗  █████╗     ██████╗ ████████╗ ██████╗{RESET}
{GREEN_RASTA}██╔═══██╗████╗ ████║██╔════╝██╔════╝ ██╔══██╗    ██╔══██╗╚══██╔══╝██╔════╝{RESET}
{GOLD_RASTA}██║   ██║██╔████╔██║█████╗  ██║  ███╗███████║    ██████╔╝   ██║   ██║     {RESET}
{GOLD_RASTA}██║   ██║██║╚██╔╝██║██╔══╝  ██║   ██║██╔══██║    ██╔══██╗   ██║   ██║     {RESET}
{RED_RASTA}╚██████╔╝██║ ╚═╝ ██║███████╗╚██████╔╝██║  ██║    ██████╔╝   ██║   ╚██████╗{RESET}
{RED_RASTA} ╚═════╝ ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝    ╚═════╝    ╚═╝    ╚═════╝{RESET}
                                                                              
{GREEN_RASTA}████████╗██████╗  █████╗ ██████╗ ██╗███╗   ██╗ ██████╗{RESET}
{GREEN_RASTA}╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║██╔════╝{RESET}
{GOLD_RASTA}   ██║   ██████╔╝███████║██║  ██║██║██╔██╗ ██║██║  ███╗{RESET}
{GOLD_RASTA}   ██║   ██╔══██╗██╔══██║██║  ██║██║██║╚██╗██║██║   ██║{RESET}
{RED_RASTA}   ██║   ██║  ██║██║  ██║██████╔╝██║██║ ╚████║╚██████╔╝{RESET}
{RED_RASTA}   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝ {RESET}

{GOLD_RASTA}ORDER DASHBOARD | JAH BLESS OMEGA FIBONACCI GOLDEN RATIO AI{RESET}
    """)

def start_backend(port):
    """Start the backend FastAPI server."""
    print(f"{GREEN_RASTA}Starting backend server on port {port}...{RESET}")
    
    if not backend_path.exists():
        print(f"{RED_RASTA}Error: Backend file not found at {backend_path}{RESET}")
        return False
    
    try:
        # Make the script executable if it isn't already
        if not os.access(backend_path, os.X_OK):
            os.chmod(backend_path, 0o755)
        
        # Start the backend process using the module name directly for uvicorn
        backend_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "omega_ai.visualizer.backend.rasta_orders_dashboard_server:app", 
             "--host", "0.0.0.0", "--port", str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        processes['backend'] = backend_process
        
        # Start a thread to monitor the output
        threading.Thread(target=monitor_process_output,
                        args=(backend_process, "Backend", GREEN_RASTA),
                        daemon=True).start()
        
        print(f"{GREEN_RASTA}Backend server started with PID {backend_process.pid}{RESET}")
        
        # Wait a moment for the server to start
        time.sleep(2)
        
        if backend_process.poll() is not None:
            print(f"{RED_RASTA}Error: Backend server failed to start{RESET}")
            return False
        
        return True
        
    except Exception as e:
        print(f"{RED_RASTA}Error starting backend server: {str(e)}{RESET}")
        return False

def start_frontend(port):
    """Start a simple HTTP server for the frontend."""
    print(f"{GOLD_RASTA}Starting frontend server on port {port}...{RESET}")
    
    if not frontend_dir.exists():
        print(f"{RED_RASTA}Error: Frontend directory not found at {frontend_dir}{RESET}")
        return False
    
    try:
        # Start the frontend server using Python's built-in HTTP server
        frontend_process = subprocess.Popen(
            [sys.executable, "-m", "http.server", str(port)],
            cwd=str(frontend_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        processes['frontend'] = frontend_process
        
        # Start a thread to monitor the output
        threading.Thread(target=monitor_process_output,
                        args=(frontend_process, "Frontend", GOLD_RASTA),
                        daemon=True).start()
        
        print(f"{GOLD_RASTA}Frontend server started with PID {frontend_process.pid}{RESET}")
        
        # Wait a moment for the server to start
        time.sleep(1)
        
        if frontend_process.poll() is not None:
            print(f"{RED_RASTA}Error: Frontend server failed to start{RESET}")
            return False
        
        return True
        
    except Exception as e:
        print(f"{RED_RASTA}Error starting frontend server: {str(e)}{RESET}")
        return False

def monitor_process_output(process, name, color):
    """Monitor and print the output from a process."""
    for line in iter(process.stdout.readline, ""):
        if line.strip():
            print(f"{color}[{name}] {line.strip()}{RESET}")
    
    for line in iter(process.stderr.readline, ""):
        if line.strip():
            print(f"{RED_RASTA}[{name} ERROR] {line.strip()}{RESET}")

def shutdown():
    """Shutdown all running processes."""
    print(f"{CYAN_INFO}Shutting down servers...{RESET}")
    
    for name, process in processes.items():
        try:
            print(f"{CYAN_INFO}Terminating {name} server (PID: {process.pid})...{RESET}")
            process.terminate()
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print(f"{RED_RASTA}Killing {name} server (PID: {process.pid}) forcefully...{RESET}")
            process.kill()
        except Exception as e:
            print(f"{RED_RASTA}Error shutting down {name} server: {str(e)}{RESET}")
    
    print(f"{GREEN_RASTA}All servers shut down.{RESET}")

def open_browser(url):
    """Open the dashboard in a web browser."""
    print(f"{CYAN_INFO}Opening dashboard in web browser: {url}{RESET}")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"{RED_RASTA}Error opening web browser: {str(e)}{RESET}")

def signal_handler(sig, frame):
    """Handle Ctrl+C and other signals."""
    print(f"{CYAN_INFO}Received signal to shut down...{RESET}")
    shutdown()
    sys.exit(0)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Start the OMEGA BTC AI Orders Dashboard")
    parser.add_argument("--backend-port", type=int, default=8420, help="Port for the backend server (default: 8420)")
    parser.add_argument("--frontend-port", type=int, default=5420, help="Port for the frontend server (default: 5420)")
    parser.add_argument("--no-browser", action="store_true", help="Don't open a browser window")
    
    args = parser.parse_args()
    
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Print banner
    print_rasta_banner()
    
    # Start backend
    backend_success = start_backend(args.backend_port)
    if not backend_success:
        print(f"{RED_RASTA}Failed to start backend server. Exiting.{RESET}")
        shutdown()
        return 1
    
    # Start frontend
    frontend_success = start_frontend(args.frontend_port)
    if not frontend_success:
        print(f"{RED_RASTA}Failed to start frontend server. Exiting.{RESET}")
        shutdown()
        return 1
    
    # Open dashboard in browser if requested
    if not args.no_browser:
        # Use the frontend URL if available, otherwise use the backend
        url = f"http://localhost:{args.frontend_port}"
        open_browser(url)
    
    print(f"""
{GREEN_RASTA}Orders Dashboard is now running!{RESET}

{CYAN_INFO}Backend API: http://localhost:{args.backend_port}{RESET}
{CYAN_INFO}Frontend UI: http://localhost:{args.frontend_port}{RESET}

{GOLD_RASTA}Press Ctrl+C to stop the servers.{RESET}
    """)
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
            
            # Check if any process has died
            for name, process in list(processes.items()):
                if process.poll() is not None:
                    print(f"{RED_RASTA}{name} server stopped unexpectedly with code {process.returncode}{RESET}")
                    del processes[name]
            
            # If all processes are dead, exit
            if not processes:
                print(f"{RED_RASTA}All servers stopped. Exiting.{RESET}")
                return 1
            
    except KeyboardInterrupt:
        pass
    finally:
        shutdown()
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 