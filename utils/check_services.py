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
Service Status Checker

This script checks the status of all OMEGA BTC AI services and reports their status.
It checks for Redis connection, tmux sessions, and process status.
"""

import os
import sys
import subprocess
import json
import time
from typing import Dict, List, Any

# Add the project root to the path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import RedisManager
try:
    from omega_ai.utils.redis_manager import RedisManager
except ImportError:
    print("Error importing RedisManager. Make sure the omega_ai module is available.")
    sys.exit(1)

# ANSI color codes for output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_colored(message: str, color: str = GREEN) -> None:
    """Print a colored message."""
    print(f"{color}{message}{RESET}")

def run_command(command: str) -> str:
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(command, shell=True, check=False, 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)
        return result.stdout
    except Exception as e:
        print_colored(f"Error running command '{command}': {e}", RED)
        return ""

def check_redis_status() -> Dict[str, Any]:
    """Check Redis connection and status."""
    result = {
        "status": "unknown",
        "keys": 0,
        "message": "",
        "error": None
    }
    
    try:
        # Initialize RedisManager
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        redis_manager = RedisManager(host=redis_host, port=redis_port)
        
        # Check connection
        if redis_manager.ping():
            result["status"] = "ok"
            
            # Get key count
            keys = redis_manager.redis.keys("*")
            result["keys"] = len(keys)
            
            # Check essential keys
            essential_keys = ["last_btc_price", "prev_btc_price", "btc_movement_history"]
            missing_keys = []
            
            for key in essential_keys:
                if key == "btc_movement_history":
                    if not redis_manager.lrange(key, 0, 0):
                        missing_keys.append(key)
                else:
                    if not redis_manager.get_cached(key):
                        missing_keys.append(key)
            
            if missing_keys:
                result["status"] = "warning"
                result["message"] = f"Missing essential keys: {', '.join(missing_keys)}"
            else:
                result["message"] = "All essential keys present"
                
                # Check last BTC price update time
                last_update = redis_manager.get_cached("last_btc_update_time")
                if last_update:
                    now = time.time()
                    last_update_time = float(last_update)
                    time_diff = now - last_update_time
                    
                    result["last_update_seconds_ago"] = int(time_diff)
                    
                    if time_diff > 300:  # More than 5 minutes
                        result["status"] = "warning"
                        result["message"] += f". Last price update was {int(time_diff)} seconds ago."
        else:
            result["status"] = "error"
            result["message"] = "Failed to ping Redis"
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        result["message"] = f"Redis connection error: {e}"
    
    return result

def check_tmux_sessions() -> Dict[str, Any]:
    """Check for OMEGA BTC tmux sessions."""
    result = {
        "sessions": [],
        "count": 0,
        "btc_feed_running": False
    }
    
    output = run_command("tmux ls 2>/dev/null || true")
    if not output:
        return result
    
    lines = output.strip().split('\n')
    for line in lines:
        if line:
            session_info = {}
            parts = line.split(':')
            if len(parts) >= 2:
                session_name = parts[0].strip()
                session_info["name"] = session_name
                session_info["details"] = parts[1].strip()
                result["sessions"].append(session_info)
                
                if "gamon_trinity_live" in session_name or "btc_live" in session_name:
                    result["btc_feed_running"] = True
    
    result["count"] = len(result["sessions"])
    return result

def check_process_status() -> Dict[str, Any]:
    """Check for running OMEGA BTC processes."""
    result = {
        "processes": [],
        "count": 0,
        "btc_feed_running": False
    }
    
    output = run_command("ps aux | grep -E 'btc_live|gamon_trinity|OMEGA' | grep -v grep || true")
    if not output:
        return result
    
    lines = output.strip().split('\n')
    for line in lines:
        if line:
            process_info = {}
            parts = line.split(None, 10)
            if len(parts) >= 11:
                process_info["user"] = parts[0]
                process_info["pid"] = parts[1]
                process_info["cpu"] = parts[2]
                process_info["mem"] = parts[3]
                process_info["command"] = parts[10]
                result["processes"].append(process_info)
                
                if "btc_live_feed" in parts[10] or "gamon_trinity_live" in parts[10]:
                    result["btc_feed_running"] = True
    
    result["count"] = len(result["processes"])
    return result

def check_log_files() -> Dict[str, Any]:
    """Check for recent log files."""
    result = {
        "log_files": [],
        "count": 0,
        "recent_logs": False
    }
    
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
    if not os.path.exists(log_dir):
        result["message"] = "Logs directory not found"
        return result
    
    # Find all log files
    log_files = []
    for filename in os.listdir(log_dir):
        if filename.endswith(".log"):
            file_path = os.path.join(log_dir, filename)
            file_stat = os.stat(file_path)
            log_files.append({
                "name": filename,
                "size": file_stat.st_size,
                "modified": file_stat.st_mtime
            })
    
    # Sort by modification time (newest first)
    log_files.sort(key=lambda x: x["modified"], reverse=True)
    
    # Take the 5 most recent logs
    result["log_files"] = log_files[:5]
    result["count"] = len(log_files)
    
    # Check if we have logs from the last hour
    now = time.time()
    for log in result["log_files"]:
        if now - log["modified"] < 3600:  # Within the last hour
            result["recent_logs"] = True
            break
    
    return result

def check_btc_price() -> Dict[str, Any]:
    """Check current BTC price from Redis."""
    result = {
        "price": None,
        "volume": None,
        "status": "unknown"
    }
    
    try:
        # Initialize RedisManager
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        redis_manager = RedisManager(host=redis_host, port=redis_port)
        
        # Get BTC price
        price = redis_manager.get_cached("last_btc_price")
        if price:
            result["price"] = float(price)
            result["status"] = "ok"
            
            # Get BTC volume
            volume = redis_manager.get_cached("last_btc_volume")
            if volume:
                result["volume"] = float(volume)
                
            # Get price movement history
            movement_history = redis_manager.lrange("btc_movement_history", 0, 9)
            if movement_history:
                result["recent_movements"] = []
                for item in movement_history:
                    if "," in item:
                        price_str, volume_str = item.split(",")
                        result["recent_movements"].append({
                            "price": float(price_str),
                            "volume": float(volume_str)
                        })
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
    
    return result

def check_all_services() -> Dict[str, Any]:
    """Check all OMEGA BTC services and return status report."""
    report = {
        "timestamp": time.time(),
        "services": {
            "redis": check_redis_status(),
            "tmux": check_tmux_sessions(),
            "processes": check_process_status(),
            "logs": check_log_files(),
            "btc_price": check_btc_price()
        },
        "overall_status": "unknown"
    }
    
    # Determine overall status
    statuses = []
    
    # Redis status
    statuses.append(report["services"]["redis"]["status"])
    
    # BTC Feed running status
    if report["services"]["tmux"]["btc_feed_running"] or report["services"]["processes"]["btc_feed_running"]:
        statuses.append("ok")
    else:
        statuses.append("error")
    
    # BTC Price status
    statuses.append(report["services"]["btc_price"]["status"])
    
    # Overall status is error if any service is error, warning if any service is warning, else ok
    if "error" in statuses:
        report["overall_status"] = "error"
    elif "warning" in statuses:
        report["overall_status"] = "warning"
    elif "unknown" in statuses:
        report["overall_status"] = "unknown"
    else:
        report["overall_status"] = "ok"
    
    return report

def display_report(report: Dict[str, Any]) -> None:
    """Display the service status report in a colored, formatted way."""
    status_colors = {
        "ok": GREEN,
        "warning": YELLOW,
        "error": RED,
        "unknown": BLUE
    }
    
    # Overall status
    status_color = status_colors.get(report["overall_status"], BLUE)
    print_colored(f"\n{BOLD}OMEGA BTC AI SERVICE STATUS REPORT{RESET}", BLUE)
    print_colored(f"{'='*50}", BLUE)
    print_colored(f"Overall Status: {report['overall_status'].upper()}", status_color)
    print_colored(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(report['timestamp']))}", BLUE)
    print_colored(f"{'='*50}", BLUE)
    
    # Redis status
    redis_status = report["services"]["redis"]
    redis_color = status_colors.get(redis_status["status"], BLUE)
    print_colored(f"\n{BOLD}Redis Status: {redis_status['status'].upper()}{RESET}", redis_color)
    print(f"Keys: {redis_status['keys']}")
    print(f"Message: {redis_status['message']}")
    if "last_update_seconds_ago" in redis_status:
        print(f"Last Update: {redis_status['last_update_seconds_ago']} seconds ago")
    
    # Tmux sessions
    tmux = report["services"]["tmux"]
    tmux_color = GREEN if tmux["btc_feed_running"] else RED
    print_colored(f"\n{BOLD}Tmux Sessions: {tmux['count']}{RESET}", tmux_color)
    for session in tmux["sessions"]:
        session_color = GREEN if "gamon_trinity_live" in session["name"] or "btc_live" in session["name"] else BLUE
        print_colored(f"  {session['name']}: {session['details']}", session_color)
    
    # Processes
    processes = report["services"]["processes"]
    processes_color = GREEN if processes["btc_feed_running"] else RED
    print_colored(f"\n{BOLD}Running Processes: {processes['count']}{RESET}", processes_color)
    for process in processes["processes"]:
        process_color = GREEN if "btc_live_feed" in process["command"] or "gamon_trinity_live" in process["command"] else BLUE
        print_colored(f"  PID {process['pid']} ({process['cpu']}% CPU): {process['command'][:80]}...", process_color)
    
    # BTC Price
    btc_price = report["services"]["btc_price"]
    price_color = status_colors.get(btc_price["status"], BLUE)
    print_colored(f"\n{BOLD}BTC Price Information:{RESET}", price_color)
    if btc_price["price"]:
        print(f"Current Price: ${btc_price['price']:,.2f}")
        if btc_price["volume"]:
            print(f"Volume: {btc_price['volume']}")
        
        if "recent_movements" in btc_price and btc_price["recent_movements"]:
            print("\nRecent Price Movements:")
            for i, movement in enumerate(btc_price["recent_movements"][:5]):
                print(f"  {i+1}. ${movement['price']:,.2f} (Vol: {movement['volume']})")
    else:
        print_colored("BTC Price data not available", RED)
    
    # Logs
    logs = report["services"]["logs"]
    logs_color = GREEN if logs["recent_logs"] else YELLOW
    print_colored(f"\n{BOLD}Log Files: {logs['count']}{RESET}", logs_color)
    for log in logs["log_files"]:
        log_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(log["modified"]))
        print(f"  {log['name']} ({log_time}, {log['size']/1024:.1f}KB)")
    
    print_colored(f"\n{'='*50}", BLUE)
    print_colored(f"End of Report - {time.strftime('%Y-%m-%d %H:%M:%S')}", BLUE)

if __name__ == "__main__":
    print_colored("OMEGA BTC AI Service Status Checker", BLUE)
    print_colored("--------------------------------", BLUE)
    report = check_all_services()
    display_report(report)
    
    # Return exit code based on status
    if report["overall_status"] == "error":
        sys.exit(1)
    elif report["overall_status"] == "warning":
        sys.exit(2)
    else:
        sys.exit(0) 