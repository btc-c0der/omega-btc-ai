#!/usr/bin/env python3
"""
OMEGA BTC AI - Start Dashboard with Live Traders Bridge
=======================================================

This script starts the dashboard and bridges it to the bitget_live_traders.py output.
It connects to an existing MM WebSocket server and starts the frontend server.

Usage:
    python start_with_live_traders.py [options]
"""

import os
import sys
import asyncio
import argparse
import subprocess
import signal
import webbrowser
import time
import threading
from pathlib import Path

# Terminal colors
GREEN_RASTA = "\033[32m"
GOLD_RASTA = "\033[33m"
RED_RASTA = "\033[31m"
RESET = "\033[0m"

# Find project root and define paths
script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
project_root = script_dir.parent.parent
frontend_dir = script_dir / "frontend" / "orders-dashboard"

# Track processes to ensure clean shutdown
processes = {}

def print_banner():
    """Print a Rastafarian-themed banner."""
    print()
    print(f"{GREEN_RASTA}{'='*80}{RESET}")
    print(f"{GOLD_RASTA}     ⬤ ⬤ ⬤  OMEGA BTC AI - LIVE TRADING DASHBOARD  ⬤ ⬤ ⬤{RESET}")
    print(f"{GREEN_RASTA}{'='*80}{RESET}")
    print()
    print(f"{GREEN_RASTA}JAH BLESS OMEGA FIBONACCI GOLDEN RATIO AI{RESET}")
    print()
    print(f"{GOLD_RASTA}Usage:{RESET}")
    print(f"  python start_with_live_traders.py [options]")
    print()
    print(f"{GOLD_RASTA}Options:{RESET}")
    print(f"  --ws-port PORT         Port for MM WebSocket server (default: 8765)")
    print(f"  --frontend-port PORT   Port for frontend server (default: 7000)")
    print(f"  --no-bridge            Don't start the bridge to live traders")
    print(f"  --no-browser           Don't open browser automatically")
    print(f"  --trader-cmd CMD       Command to run for live traders (default: None)")
    print()
    print(f"{GOLD_RASTA}Features:{RESET}")
    print(f"  • Connect to existing MM WebSocket server")
    print(f"  • Bridge live trader output to dashboard")
    print(f"  • Real-time trading updates with Rastafarian-themed visualization")
    print()
    print(f"{GREEN_RASTA}{'='*80}{RESET}")
    print()

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

def start_bridge(ws_port, cmd=None):
    """Start the stdout to WebSocket bridge."""
    if not cmd:
        print(f"{GOLD_RASTA}No trader command specified, bridge will not be started{RESET}")
        return True
    
    print(f"{GOLD_RASTA}Starting stdout to WebSocket bridge...{RESET}")
    
    bridge_script = script_dir / "stdout_to_ws_bridge.py"
    if not bridge_script.exists():
        print(f"{RED_RASTA}Error: Bridge script not found at {bridge_script}{RESET}")
        return False
    
    try:
        # Start the bridge process
        bridge_process = subprocess.Popen(
            [
                sys.executable, 
                str(bridge_script),
                "--cmd", cmd,
                "--ws-port", str(ws_port),
                "--ws-path", "/ws"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        processes['bridge'] = bridge_process
        
        # Start a thread to monitor the output
        threading.Thread(target=monitor_process_output,
                         args=(bridge_process, "Bridge", GREEN_RASTA),
                         daemon=True).start()
        
        print(f"{GOLD_RASTA}Bridge started with PID {bridge_process.pid}{RESET}")
        return True
        
    except Exception as e:
        print(f"{RED_RASTA}Error starting bridge: {str(e)}{RESET}")
        return False

def monitor_process_output(process, name, color):
    """Monitor and print process output with color coding."""
    while process.poll() is None:
        output = process.stdout.readline().strip()
        if output:
            print(f"{color}[{name}] {output}{RESET}")
    
    # Read any remaining output after process terminates
    remaining_output, remaining_error = process.communicate()
    if remaining_output:
        for line in remaining_output.splitlines():
            if line.strip():
                print(f"{color}[{name}] {line.strip()}{RESET}")
    
    if remaining_error:
        for line in remaining_error.splitlines():
            if line.strip():
                print(f"{RED_RASTA}[{name} ERROR] {line.strip()}{RESET}")
    
    if process.returncode != 0:
        print(f"{RED_RASTA}[{name}] Process exited with code {process.returncode}{RESET}")
    else:
        print(f"{color}[{name}] Process completed successfully{RESET}")

def shutdown_servers():
    """Shutdown all running servers."""
    print(f"{GOLD_RASTA}Shutting down servers...{RESET}")
    
    for name, process in processes.items():
        try:
            if process and process.poll() is None:
                print(f"{GOLD_RASTA}Terminating {name} server (PID: {process.pid})...{RESET}")
                process.terminate()
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    print(f"{RED_RASTA}Forcibly killing {name} server...{RESET}")
                    process.kill()
        except Exception as e:
            print(f"{RED_RASTA}Error shutting down {name} server: {str(e)}{RESET}")
    
    print(f"{GREEN_RASTA}All servers shut down.{RESET}")

def open_browser(url, ws_port):
    """Open a browser to the dashboard."""
    # Add the WebSocket port as a URL parameter if not already in the URL
    if "?" not in url:
        url += "?"
    elif url[-1] != "?" and url[-1] != "&":
        url += "&"
    
    url += f"wsport={ws_port}"
    
    print(f"{GOLD_RASTA}Opening dashboard in browser: {url}{RESET}")
    webbrowser.open(url)

def signal_handler(sig, frame):
    """Handle Ctrl+C and other termination signals."""
    print(f"{GOLD_RASTA}Shutdown signal received, shutting down...{RESET}")
    shutdown_servers()
    sys.exit(0)

def find_available_port(start_port, max_attempts=10):
    """Find an available port starting from the specified port."""
    import socket
    
    for port in range(start_port, start_port + max_attempts):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result != 0:  # Port is available
                return port
        except:
            continue
    
    # If we got here, no ports were available in our range
    return None

def check_port_available(port):
    """Check if a port is available."""
    import socket
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result != 0  # If result != 0, port is available
    except:
        return False

def check_mm_server_running(port):
    """Check if the MM WebSocket server is running on the specified port."""
    import socket
    
    try:
        # Try to create a socket connection to the port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        return result == 0  # If result is 0, port is open
    except:
        return False

def main():
    """Main function to run the dashboard."""
    parser = argparse.ArgumentParser(description="Start the OMEGA BTC AI Live Trading Dashboard")
    parser.add_argument("--ws-port", type=int, default=8765, 
                        help="Port for the MM WebSocket server (default: 8765)")
    parser.add_argument("--frontend-port", type=int, default=7000, 
                        help="Port for the frontend server (default: 7000)")
    parser.add_argument("--no-bridge", action="store_true", 
                        help="Don't start the bridge to live traders")
    parser.add_argument("--no-browser", action="store_true", 
                        help="Don't open browser automatically")
    parser.add_argument("--trader-cmd", type=str, 
                        help="Command to run for live traders")
    
    args = parser.parse_args()
    
    # Register signal handlers for clean shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Print the banner
    print_banner()
    
    # Check if MM WebSocket server is running
    ws_port = args.ws_port
    mm_server_running = check_mm_server_running(ws_port)
    
    if not mm_server_running:
        print(f"{RED_RASTA}MM WebSocket server is not running on port {ws_port}. Please start it first.{RESET}")
        return 1
    
    # Check if frontend port is available, find another if not
    frontend_port = args.frontend_port
    if not check_port_available(frontend_port):
        print(f"{GOLD_RASTA}Port {frontend_port} is already in use for frontend server.{RESET}")
        frontend_port = find_available_port(frontend_port + 1)
        if frontend_port:
            print(f"{GOLD_RASTA}Using alternate port {frontend_port} for frontend server{RESET}")
        else:
            print(f"{RED_RASTA}No available ports found for frontend server. Exiting.{RESET}")
            return 1
    
    # Start the frontend server
    if not start_frontend(frontend_port):
        print(f"{RED_RASTA}Failed to start frontend server. Exiting.{RESET}")
        shutdown_servers()
        return 1
    
    # Start the bridge if requested
    if not args.no_bridge and args.trader_cmd:
        if not start_bridge(ws_port, args.trader_cmd):
            print(f"{RED_RASTA}Failed to start bridge. Exiting.{RESET}")
            shutdown_servers()
            return 1
    
    # Open the browser
    if not args.no_browser:
        url = f"http://localhost:{frontend_port}"
        threading.Thread(target=open_browser, args=(url, ws_port), daemon=True).start()
    
    print(f"{GREEN_RASTA}Dashboard started successfully!{RESET}")
    print(f"{GREEN_RASTA}Access the dashboard at http://localhost:{frontend_port}{RESET}")
    if not args.no_bridge and args.trader_cmd:
        print(f"{GREEN_RASTA}Live trading data is being streamed to the dashboard{RESET}")
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
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 