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
OmegaBTC Trading System Process Manager
=======================================

This script manages all components of the OmegaBTC trading system,
providing a unified interface for starting, stopping, and monitoring
all required processes.

Usage:
    python run_omega_btc_ai.py {start|stop|restart|status}
"""

import argparse
import os
import signal
import subprocess
import sys
import time
import json
from datetime import datetime
from pathlib import Path

# ANSI Colors for terminal output
BLUE = '\033[0;34m'
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
MAGENTA = '\033[0;35m'
CYAN = '\033[0;36m'
WHITE = '\033[0;37m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Directory configurations
BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"
VENV_DIR = BASE_DIR / "venv"  # Assuming you have a virtual environment
PID_FILE = LOG_DIR / "omega_processes.pid"

# List of modules to start in order with dependency information
MODULES = [
    # Core Infrastructure
    {"module": "omega_ai.db_manager.database", 
     "name": "database_setup", 
     "description": "PostgreSQL Database Manager", 
     "dependencies": []},
     
    # Data Feeds & Monitoring
    {"module": "omega_ai.data_feed.schumann_monitor", 
     "name": "schumann_monitor", 
     "description": "Schumann Resonance Monitor",
     "dependencies": ["database_setup"]},
     
    {"module": "omega_ai.data_feed.btc_live_feed", 
     "name": "btc_live_feed", 
     "description": "BTC Price Live Feed", 
     "dependencies": ["database_setup"]},
     
    # Analysis & Detection Components
    {"module": "omega_ai.mm_trap_detector.fibonacci_detector", 
     "name": "fibonacci_detector", 
     "description": "Fibonacci Level Detector", 
     "dependencies": ["btc_live_feed"]},
     
    {"module": "omega_ai.mm_trap_detector.grafana_reporter", 
     "name": "grafana_reporter", 
     "description": "Grafana Metrics Reporter", 
     "dependencies": ["database_setup"]},
     
    {"module": "omega_ai.mm_trap_detector.high_frequency_detector", 
     "name": "hf_detector", 
     "description": "High-Frequency Trap Detector", 
     "dependencies": ["fibonacci_detector", "grafana_reporter"]},
     
    {"module": "omega_ai.mm_trap_detector.mm_trap_detector",
     "name": "mm_trap_detector",
     "description": "Market Maker Trap Detector",
     "dependencies": ["hf_detector"]},
     
    # User-facing Components
    {"module": "omega_ai.monitor.monitor_market_trends", 
     "name": "market_monitor", 
     "description": "Market Trend Monitor", 
     "dependencies": ["hf_detector", "fibonacci_detector"]}
]


def log(message, color=RESET):
    """Log a message with timestamp and color."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{color}[{timestamp}] {message}{RESET}")


def ensure_redis_running():
    """Ensure Redis server is running."""
    log("Checking Redis server status...", BLUE)
    
    try:
        result = subprocess.run(
            ["redis-cli", "ping"], 
            capture_output=True, 
            text=True, 
            check=False
        )
        
        if result.returncode == 0 and result.stdout.strip() == "PONG":
            log("Redis server is already running.", GREEN)
            return True
            
        log("Redis is not running. Starting Redis...", YELLOW)
        subprocess.run(["brew", "services", "start", "redis"], check=False)
        time.sleep(2)
        
        # Check if Redis started successfully
        result = subprocess.run(
            ["redis-cli", "ping"], 
            capture_output=True, 
            text=True, 
            check=False
        )
        
        if result.returncode == 0 and result.stdout.strip() == "PONG":
            log("Redis started successfully.", GREEN)
            return True
        else:
            log("Failed to start Redis! Please start it manually.", RED)
            return False
            
    except Exception as e:
        log(f"Error checking/starting Redis: {e}", RED)
        return False


def ensure_postgres_running():
    """Ensure PostgreSQL server is running."""
    log("Checking PostgreSQL server status...", BLUE)
    
    try:
        # For macOS using Homebrew
        pg_status = subprocess.run(
            ["brew", "services", "info", "postgresql@14"], 
            capture_output=True, 
            text=True, 
            check=False
        )
        
        if "started" in pg_status.stdout.lower():
            log("PostgreSQL server is already running.", GREEN)
            return True
            
        log("PostgreSQL is not running. Starting PostgreSQL...", YELLOW)
        subprocess.run(["brew", "services", "start", "postgresql@14"], check=False)
        time.sleep(3)
        
        # Check if PostgreSQL started
        pg_status = subprocess.run(
            ["brew", "services", "info", "postgresql@14"], 
            capture_output=True, 
            text=True, 
            check=False
        )
        
        if "started" in pg_status.stdout.lower():
            log("PostgreSQL started successfully.", GREEN)
            return True
        else:
            log("Failed to start PostgreSQL! Please start it manually.", RED)
            return False
            
    except Exception as e:
        log(f"Error checking/starting PostgreSQL: {e}", RED)
        log("Continuing anyway as the DB might be running through another method...", YELLOW)
        return True  # Continue anyway as pg might be running through another method


def activate_venv():
    """Get the Python interpreter path with activated venv if it exists."""
    if (VENV_DIR / "bin" / "python").exists():
        return str(VENV_DIR / "bin" / "python")
    return sys.executable  # Use current Python interpreter if no venv


def resolve_dependencies(module_name, started_modules):
    """Recursively resolve and start module dependencies."""
    # Find the module info
    module_info = next((m for m in MODULES if m["name"] == module_name), None)
    if not module_info:
        log(f"Module {module_name} not found!", RED)
        return False
    
    # Check all dependencies
    for dep in module_info["dependencies"]:
        # If dependency not started, try to start it
        if dep not in started_modules:
            if not resolve_dependencies(dep, started_modules):
                return False
    
    return True


def start_module(module, name, description):
    """Start a specific Python module."""
    log(f"Starting {name} ({description})...", BLUE)
    
    # Create log directory if it doesn't exist
    LOG_DIR.mkdir(exist_ok=True)
    log_file = LOG_DIR / f"{name}.log"
    
    # Use venv python if available
    python_path = activate_venv()
    
    # Start process
    try:
        with open(log_file, "w") as log_f:
            process = subprocess.Popen(
                [python_path, "-m", module],
                stdout=log_f,
                stderr=subprocess.STDOUT,
                start_new_session=True  # Detach from parent process
            )
        
        # Check if process started successfully
        time.sleep(2)
        if process.poll() is None:  # Process is still running
            log(f"{name} started with PID {process.pid}", GREEN)
            
            # Store PID
            with open(PID_FILE, "a") as pid_f:
                pid_f.write(f"{name}:{process.pid}\n")
            
            return True
        else:
            log(f"Failed to start {name}! Process exited immediately.", RED)
            log(f"Check logs at {log_file}", RED)
            return False
            
    except Exception as e:
        log(f"Error starting {name}: {e}", RED)
        return False


def stop_process(name, pid):
    """Stop a specific process."""
    log(f"Stopping {name} (PID: {pid})...", YELLOW)
    
    try:
        os.kill(int(pid), signal.SIGTERM)
        time.sleep(1)
        
        # Check if process is still running
        try:
            os.kill(int(pid), 0)  # Signal 0 is used to check if process exists
            log(f"{name} (PID: {pid}) is still running, forcing kill...", YELLOW)
            os.kill(int(pid), signal.SIGKILL)
        except OSError:
            # Process is no longer running
            pass
            
        log(f"{name} stopped.", GREEN)
        return True
        
    except ProcessLookupError:
        log(f"Process {name} (PID: {pid}) is not running", YELLOW)
        return True
    except Exception as e:
        log(f"Error stopping {name} (PID: {pid}): {e}", RED)
        return False


def read_pid_file():
    """Read process information from PID file."""
    if not PID_FILE.exists():
        return []
        
    processes = []
    try:
        with open(PID_FILE, "r") as f:
            for line in f:
                if ":" in line:
                    name, pid = line.strip().split(":", 1)
                    processes.append({"name": name, "pid": int(pid)})
    except Exception as e:
        log(f"Error reading PID file: {e}", RED)
        
    return processes


def is_process_running(pid):
    """Check if a process with the given PID is running."""
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except Exception:
        return False


def find_module_by_name(name):
    """Find module info by name."""
    for module in MODULES:
        if module["name"] == name:
            return module
    return None


def start_all():
    """Start all OmegaBTC AI components."""
    log("=== Starting OmegaBTC AI Trading System ===", BLUE)
    
    # Remove previous PID file
    if PID_FILE.exists():
        PID_FILE.unlink()
    
    # Ensure Redis is running
    if not ensure_redis_running():
        return False
        
    # Ensure PostgreSQL is running (for database-dependent services)
    if not ensure_postgres_running():
        log("Continuing anyway as the database might be accessible...", YELLOW)
    
    # Start components in order of dependencies
    success = True
    started_modules = set()
    
    # First pass - start modules with no dependencies
    for module_info in MODULES:
        if not module_info["dependencies"]:
            if start_module(module_info["module"], module_info["name"], module_info["description"]):
                started_modules.add(module_info["name"])
            else:
                log(f"Failed to start {module_info['name']}", RED)
                success = False
            # Pause between starting core services
            time.sleep(3)
    
    # Second pass - start remaining modules in dependency order
    remaining_modules = [m for m in MODULES if m["name"] not in started_modules]
    retries = 0
    
    while remaining_modules and retries < 3:
        modules_started_this_round = 0
        
        for module_info in remaining_modules[:]:
            # Check if all dependencies are started
            if all(dep in started_modules for dep in module_info["dependencies"]):
                if start_module(module_info["module"], module_info["name"], module_info["description"]):
                    started_modules.add(module_info["name"])
                    remaining_modules.remove(module_info)
                    modules_started_this_round += 1
                else:
                    log(f"Failed to start {module_info['name']}", RED)
                    success = False
                time.sleep(2)
        
        if modules_started_this_round == 0:
            retries += 1
            time.sleep(2)
    
    # Report on any modules that couldn't be started
    if remaining_modules:
        log("Some modules could not be started due to dependency issues:", RED)
        for module_info in remaining_modules:
            # Find which dependencies weren't met
            missing_deps = [dep for dep in module_info["dependencies"] if dep not in started_modules]
            log(f"- {module_info['name']}: missing dependencies: {', '.join(missing_deps)}", RED)
    
    if success:
        log("All components started successfully.", GREEN)
        log(f"View logs in {LOG_DIR}", YELLOW)
        log("To stop all processes, run: python run_omega_btc_ai.py stop", YELLOW)
    else:
        log("Some components failed to start. Check logs for details.", RED)
    
    return success


def stop_all():
    """Stop all OmegaBTC AI components."""
    log("=== Stopping OmegaBTC AI Trading System ===", BLUE)
    
    processes = read_pid_file()
    if not processes:
        log("No PID file found. No processes to stop.", YELLOW)
        return True
    
    # Stop processes in reverse order (assuming order in PID file matches startup order)
    success = True
    for process in reversed(processes):
        if not stop_process(process["name"], process["pid"]):
            success = False
    
    # Remove PID file
    if PID_FILE.exists():
        PID_FILE.unlink()
    
    if success:
        log("All processes stopped.", GREEN)
    else:
        log("Some processes failed to stop. Check logs for details.", RED)
    
    return success


def visualize_dependencies():
    """Visualize module dependencies in a tree-like structure."""
    log("\nSystem Component Dependencies:", MAGENTA)
    
    def print_tree(module_name, depth=0, visited=None):
        if visited is None:
            visited = set()
        
        if module_name in visited:
            print(f"{' ' * (depth * 4)}└── {YELLOW}[Circular ref: {module_name}]{RESET}")
            return
        
        visited.add(module_name)
        
        # Get module info
        module = find_module_by_name(module_name)
        if not module:
            print(f"{' ' * (depth * 4)}└── {RED}[Unknown: {module_name}]{RESET}")
            return
        
        # Print this module
        running = False
        pid = None
        for proc in read_pid_file():
            if proc["name"] == module_name:
                pid = proc["pid"]
                running = is_process_running(pid)
                break
        
        status = f"{GREEN}[RUNNING: {pid}]{RESET}" if running else f"{RED}[STOPPED]{RESET}"
        print(f"{' ' * (depth * 4)}{'└── ' if depth > 0 else ''}{BOLD}{module_name}{RESET} - {module['description']} {status}")
        
        # Find modules that depend on this one
        dependents = [m for m in MODULES if module_name in m["dependencies"]]
        for i, dep in enumerate(dependents):
            is_last = i == len(dependents) - 1
            print_tree(dep["name"], depth + 1, visited.copy())
    
    # Find root modules (those with no dependencies)
    roots = [m["name"] for m in MODULES if not m["dependencies"]]
    for root in roots:
        print_tree(root)


def check_status():
    """Check status of all OmegaBTC AI components."""
    log("=== OmegaBTC AI Trading System Status ===", BLUE)
    
    # Check Redis first
    redis_running = ensure_redis_running()
    
    # Check PostgreSQL
    pg_running = ensure_postgres_running()
    
    processes = read_pid_file()
    if not processes:
        log("No PID file found. System appears to be stopped.", YELLOW)
        
        # Still offer to visualize the system architecture
        print(f"\n{CYAN}Would you like to see the system architecture? (y/n){RESET}")
        choice = input().strip().lower()
        if choice == 'y':
            visualize_dependencies()
        return
    
    log("Process status:", BLUE)
    # Group by running state for clearer output
    running_procs = []
    stopped_procs = []
    
    for process in processes:
        running = is_process_running(process["pid"])
        # Find module info for description
        module_info = find_module_by_name(process["name"])
        description = module_info["description"] if module_info else "Unknown component"
        
        if running:
            running_procs.append((process["name"], process["pid"], description))
        else:
            stopped_procs.append((process["name"], process["pid"], description))
    
    # Print running processes first
    if running_procs:
        log("RUNNING Processes:", GREEN)
        for name, pid, description in running_procs:
            log(f"✅ {name} (PID: {pid}) - {description}", GREEN)
    
    # Then print stopped processes
    if stopped_procs:
        log("\nSTOPPED Processes:", RED)
        for name, pid, description in stopped_procs:
            log(f"❌ {name} (PID: {pid}) - {description}", RED)
    
    # Show system health summary
    total = len(running_procs) + len(stopped_procs)
    if running_procs:
        health_percent = (len(running_procs) / total) * 100
        if health_percent >= 90:
            health_status = f"{GREEN}EXCELLENT{RESET}"
        elif health_percent >= 75:
            health_status = f"{CYAN}GOOD{RESET}"
        elif health_percent >= 50:
            health_status = f"{YELLOW}DEGRADED{RESET}"
        else:
            health_status = f"{RED}CRITICAL{RESET}"
            
        log(f"\nSystem Health: {health_status} ({len(running_procs)}/{total} components running - {health_percent:.1f}%)", BLUE)

    # Get disk space and memory usage for extra system info
    log("\nSystem Resources:", MAGENTA)
    try:
        df = subprocess.run(["df", "-h", "/"], capture_output=True, text=True, check=False)
        if df.returncode == 0:
            disk_lines = df.stdout.strip().split('\n')
            if len(disk_lines) > 1:
                log(f"Disk Usage: {disk_lines[1].split()[4]} used", CYAN)
    except Exception:
        pass
        
    try:
        # Get memory info on macOS
        vm_stat = subprocess.run(["vm_stat"], capture_output=True, text=True, check=False)
        if vm_stat.returncode == 0:
            lines = vm_stat.stdout.strip().split('\n')
            if len(lines) > 1:
                log(f"Memory Status: {lines[0]}", CYAN)
    except Exception:
        pass

    # Add logs status
    log("\nLog Files:", MAGENTA)
    for module_info in MODULES:
        log_file = LOG_DIR / f"{module_info['name']}.log"
        if log_file.exists():
            size = log_file.stat().st_size / 1024  # KB
            last_modified = datetime.fromtimestamp(log_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            log(f"{module_info['name']}: {size:.1f} KB (Last updated: {last_modified})", CYAN)
    
    # Visualize dependencies if requested
    print(f"\n{CYAN}Would you like to see the system dependency structure? (y/n){RESET}")
    choice = input().strip().lower()
    if choice == 'y':
        visualize_dependencies()


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="OmegaBTC Trading System Process Manager")
    parser.add_argument("action", choices=["start", "stop", "restart", "status", "deps"],
                        help="Action to perform")
    
    args = parser.parse_args()
    
    if args.action == "start":
        start_all()
    elif args.action == "stop":
        stop_all()
    elif args.action == "restart":
        stop_all()
        time.sleep(2)
        start_all()
    elif args.action == "status":
        check_status()
    elif args.action == "deps":
        visualize_dependencies()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
    except Exception as e:
        log(f"Unexpected error: {e}", RED)
        sys.exit(1)