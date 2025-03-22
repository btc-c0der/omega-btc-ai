#!/usr/bin/env python3

"""
OMEGA BTC AI - MM Orders Dashboard Starter
=========================================

This script starts the MM WebSocket server and the dashboard frontend.
It provides a unified way to launch the entire dashboard infrastructure.
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
import socket

# ANSI color codes for Rastafarian-themed colorful output
GREEN_RASTA = "\033[32m"    # Bright green (primary color)
GOLD_RASTA = "\033[33m"    # Gold (secondary color)
RED_RASTA = "\033[31m"     # Red (tertiary color)
YELLOW_RASTA = "\033[33m"   # Yellow (tertiary color)
RESET = "\033[0m"                # Reset to default terminal color

# Find the project root
script_path = Path(__file__).resolve()
project_root = script_path
while not (project_root / "omega_ai").exists() and project_root != project_root.parent:
    project_root = project_root.parent

# Define paths
mm_server_path = project_root / "omega_ai" / "mm_trap_detector" / "mm_websocket_server.py"
frontend_dir = project_root / "omega_ai" / "visualizer" / "frontend" / "orders-dashboard"

# Process tracking
processes = {}

def print_banner():
    """Print a Rastafarian-themed banner."""
    print()
    print(f"{GREEN_RASTA}{'='*80}{RESET}")
    print(f"{GOLD_RASTA}     ⬤ ⬤ ⬤  OMEGA BTC AI - MARKET MAKER DASHBOARD  ⬤ ⬤ ⬤{RESET}")
    print(f"{GREEN_RASTA}{'='*80}{RESET}")
    print()
    print(f"{GREEN_RASTA}JAH BLESS OMEGA FIBONACCI GOLDEN RATIO AI{RESET}")
    print()
    print(f"{GOLD_RASTA}Usage:{RESET}")
    print(f"  python start_mm_dashboard.py [options]")
    print()
    print(f"{GOLD_RASTA}Options:{RESET}")
    print(f"  --backend-port PORT    Port for MM WebSocket server (default: 8765)")
    print(f"  --frontend-port PORT   Port for frontend server (default: 7000)")
    print(f"  --no-browser           Don't open browser automatically")
    print(f"  --use-existing-mm      Use existing MM WebSocket server if running")
    print()
    print(f"{GOLD_RASTA}Features:{RESET}")
    print(f"  • Automatic port conflict detection and resolution")
    print(f"  • Connect to existing MM WebSocket server or start a new one")
    print(f"  • Real-time trading updates with Rastafarian-themed visualization")
    print()
    print(f"{GREEN_RASTA}{'='*80}{RESET}")
    print()

def start_mm_server(port):
    """Start the MM WebSocket server."""
    print(f"{GREEN_RASTA}Starting MM WebSocket server on port {port}...{RESET}")
    
    if not mm_server_path.exists():
        print(f"{RED_RASTA}Error: MM WebSocket server file not found at {mm_server_path}{RESET}")
        return False
    
    try:
        # Make the script executable if it isn't already
        if not os.access(mm_server_path, os.X_OK):
            os.chmod(mm_server_path, 0o755)
        
        # Start the MM WebSocket server
        mm_server_process = subprocess.Popen(
            [sys.executable, str(mm_server_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        processes['mm_server'] = mm_server_process
        
        # Start a thread to monitor the output
        threading.Thread(target=monitor_process_output,
                        args=(mm_server_process, "MM Server", GREEN_RASTA),
                        daemon=True).start()
        
        print(f"{GREEN_RASTA}MM WebSocket server started with PID {mm_server_process.pid}{RESET}")
        
        # Wait a moment for the server to start
        time.sleep(2)
        
        if mm_server_process.poll() is not None:
            print(f"{RED_RASTA}Error: MM WebSocket server failed to start{RESET}")
            return False
        
        return True
        
    except Exception as e:
        print(f"{RED_RASTA}Error starting MM WebSocket server: {str(e)}{RESET}")
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
        
        # Check immediately if the process failed to start (e.g., port already in use)
        time.sleep(0.5)
        if frontend_process.poll() is not None:
            # Process has already terminated, collect any error output
            stderr_output, _ = frontend_process.communicate()
            if "Address already in use" in stderr_output:
                print(f"{RED_RASTA}Error: Port {port} is already in use{RESET}")
                return False
            else:
                print(f"{RED_RASTA}Error starting frontend server: {stderr_output}{RESET}")
                return False
        
        processes['frontend'] = frontend_process
        
        # Start a thread to monitor the output
        threading.Thread(target=monitor_process_output,
                        args=(frontend_process, "Frontend", GOLD_RASTA),
                        daemon=True).start()
        
        print(f"{GOLD_RASTA}Frontend server started with PID {frontend_process.pid} on port {port}{RESET}")
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

def shutdown_servers():
    """Shutdown all running servers."""
    print(f"{GOLD_RASTA}Shutting down servers...{RESET}")
    
    for name, process in processes.items():
        if process.poll() is None:  # Process is still running
            print(f"{GOLD_RASTA}Terminating {name} (PID: {process.pid})...{RESET}")
            try:
                process.terminate()
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                print(f"{RED_RASTA}Process {name} did not terminate, forcing...{RESET}")
                process.kill()
    
    print(f"{GREEN_RASTA}All servers shut down.{RESET}")

def open_browser(url, port):
    """Open a browser to the dashboard."""
    # Add the WebSocket port as a URL parameter if not already in the URL
    if "?" not in url:
        url += "?"
    elif url[-1] != "?" and url[-1] != "&":
        url += "&"
    
    url += f"wsport={port}"
    
    print(f"{GOLD_RASTA}Opening dashboard in browser: {url}{RESET}")
    webbrowser.open(url)

def signal_handler(sig, frame):
    """Handle interrupt signals."""
    print(f"{GOLD_RASTA}Received interrupt signal. Shutting down...{RESET}")
    shutdown_servers()
    sys.exit(0)

def check_mm_server_running(port):
    """Check if the MM WebSocket server is already running on the specified port."""
    try:
        # Try to connect to the port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # 1 second timeout
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        # If port is open, server is likely running
        if result == 0:
            print(f"{GREEN_RASTA}MM WebSocket server already running on port {port}{RESET}")
            return True
        return False
    except Exception:
        return False

def find_available_port(start_port, max_attempts=10):
    """Find an available port starting from the specified port."""
    for port in range(start_port, start_port + max_attempts):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result != 0:  # Port is available
                return port
        except Exception:
            continue
    
    # If we got here, no ports were available in our range
    return None

def check_port_available(port):
    """Check if a port is available."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result != 0  # If result != 0, port is available
    except Exception:
        return False

def main():
    """Main function to run the dashboard."""
    parser = argparse.ArgumentParser(description="Start the dashboard for OMEGA BTC AI")
    parser.add_argument("--backend-port", type=int, default=8765, 
                        help="Port for the MM WebSocket server")
    parser.add_argument("--frontend-port", type=int, default=7000, 
                        help="Port for the frontend server")
    parser.add_argument("--no-browser", action="store_true", 
                        help="Don't open browser automatically")
    parser.add_argument("--use-existing-mm", action="store_true",
                        help="Use existing MM WebSocket server if running")
    
    args = parser.parse_args()
    
    # Register signal handlers for clean shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Print the banner
    print_banner()
    
    # Check if MM WebSocket server is already running
    mm_server_running = check_mm_server_running(args.backend_port)
    
    if mm_server_running and args.use_existing_mm:
        print(f"{GREEN_RASTA}MM WebSocket server already running on port {args.backend_port}, using existing server{RESET}")
        backend_port = args.backend_port
    elif mm_server_running and not args.use_existing_mm:
        print(f"{YELLOW_RASTA}MM WebSocket server already running on port {args.backend_port}, but --use-existing-mm not specified.{RESET}")
        print(f"{YELLOW_RASTA}Attempting to find another port for a new MM WebSocket server...{RESET}")
        backend_port = find_available_port(args.backend_port + 1)
        if backend_port:
            if not start_mm_server(backend_port):
                print(f"{RED_RASTA}Failed to start MM WebSocket server on port {backend_port}. Exiting.{RESET}")
                return
        else:
            print(f"{RED_RASTA}Could not find an available port for MM WebSocket server. Exiting.{RESET}")
            return
    else:
        backend_port = args.backend_port
        if not start_mm_server(backend_port):
            print(f"{RED_RASTA}Failed to start MM WebSocket server on port {backend_port}. Exiting.{RESET}")
            return
    
    # Check if frontend port is available, find another if not
    frontend_port = args.frontend_port
    if not check_port_available(frontend_port):
        print(f"{YELLOW_RASTA}Port {frontend_port} is already in use. Finding another port for frontend server...{RESET}")
        frontend_port = find_available_port(frontend_port + 1)
        if not frontend_port:
            print(f"{RED_RASTA}Could not find an available port for frontend server. Exiting.{RESET}")
            return
    
    # Start the frontend server
    if not start_frontend(frontend_port):
        print(f"{RED_RASTA}Failed to start frontend server. Exiting.{RESET}")
        shutdown_servers()
        return
    
    # Open the browser
    if not args.no_browser:
        url = f"http://localhost:{frontend_port}"
        threading.Thread(target=open_browser, args=(url, backend_port), daemon=True).start()
    
    print(f"{GREEN_RASTA}Dashboard started successfully!{RESET}")
    print(f"{GREEN_RASTA}Access the dashboard at http://localhost:{frontend_port}{RESET}")
    print(f"{GOLD_RASTA}Press Ctrl+C to stop the servers{RESET}")
    
    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            for name, process in list(processes.items()):
                if process.poll() is not None:
                    print(f"{RED_RASTA}{name} server has stopped unexpectedly (exit code {process.poll()}){RESET}")
                    del processes[name]
            
            # If all processes have stopped, exit
            if not processes:
                print(f"{RED_RASTA}All servers have stopped. Exiting.{RESET}")
                break
                
    except KeyboardInterrupt:
        pass
    finally:
        shutdown_servers()

if __name__ == "__main__":
    sys.exit(main()) 