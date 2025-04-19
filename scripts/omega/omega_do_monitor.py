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
🔱 OMEGA D0T7 DIVINE DIGIT4L 0CE4N Monitor 🔱
=============================================

A sacred CLI-based monitoring tool for OMEGA BTC AI deployments on Digital Ocean.
Provides real-time metrics, health status, and deployment information.

Usage:
    python omega_do_monitor.py [command]

Commands:
    status        - Show current deployment status
    logs          - Stream logs in real-time
    health        - Check application health
    redis         - Test Redis connection
    stats         - Show resource usage statistics
    watch_price   - Watch BTC price updates in real-time
    help          - Show this help message
"""

import os
import sys
import json
import time
import signal
import urllib.request
import urllib.error
import subprocess
import argparse
from datetime import datetime
from typing import Dict, Any, List, Optional, Union

# ANSI color codes for divine styling
BLUE = '\033[0;34m'
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
MAGENTA = '\033[0;35m'
CYAN = '\033[0;36m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Configuration
APP_ID = os.getenv("OMEGA_DO_APP_ID", "f129574c-0fcd-4a97-93bb-32618cbccae2")
APP_URL = os.getenv("OMEGA_DO_APP_URL", "")
DOCTL_PATH = "doctl"

# Helper Functions
def divine_header():
    """Print divine header."""
    print(f"\n{MAGENTA}{'='*75}{RESET}")
    print(f"{MAGENTA}{BOLD}🔱 OMEGA D0T7 DIVINE DIGIT4L 0CE4N Monitor 🔱{RESET}")
    print(f"{MAGENTA}{'='*75}{RESET}")
    print(f"{YELLOW}The sacred path of monitoring the eternal blockchain flow.{RESET}")
    print(f"{MAGENTA}{'='*75}{RESET}\n")

def run_command(cmd: List[str], capture_output: bool = True) -> Dict[str, Any]:
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
            check=False
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout if result.returncode == 0 else result.stderr,
            "code": result.returncode
        }
    except Exception as e:
        return {
            "success": False,
            "output": str(e),
            "code": -1
        }

def format_timestamp(timestamp: str) -> str:
    """Format timestamp for display."""
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    except:
        return timestamp

def handle_sigint(sig, frame):
    """Handle Ctrl+C gracefully."""
    print(f"\n{YELLOW}Divine monitoring session ended by the user.{RESET}")
    print(f"{YELLOW}JAH JAH BLESS THE ETERNAL FLOW OF THE BLOCKCHAIN.{RESET}\n")
    sys.exit(0)

# Command Functions
def show_status():
    """Show current deployment status."""
    print(f"{CYAN}Checking deployment status...{RESET}")
    
    result = run_command([DOCTL_PATH, "apps", "list-deployments", APP_ID, "--format", "ID,Cause,Phase,Progress,Created,Updated"])
    
    if result["success"]:
        lines = result["output"].strip().split('\n')
        
        if len(lines) < 2:
            print(f"{RED}No deployments found.{RESET}")
            return
        
        # Print header
        header = lines[0]
        print(f"\n{YELLOW}{header}{RESET}")
        print(f"{YELLOW}{'-' * len(header)}{RESET}")
        
        # Print deployments with color
        for line in lines[1:]:
            if "ACTIVE" in line:
                print(f"{GREEN}{line}{RESET}")
            elif "ERROR" in line:
                print(f"{RED}{line}{RESET}")
            elif "BUILDING" in line:
                print(f"{YELLOW}{line}{RESET}")
            else:
                print(line)
                
        # Show app URL if available
        if APP_URL:
            print(f"\n{CYAN}App URL: {BOLD}{APP_URL}{RESET}")
    else:
        print(f"{RED}Error getting deployment status: {result['output']}{RESET}")

def stream_logs():
    """Stream application logs in real-time."""
    print(f"{CYAN}Streaming logs in real-time (press Ctrl+C to stop)...{RESET}")
    
    # Run the command without capturing output to stream directly to terminal
    cmd = [DOCTL_PATH, "apps", "logs", APP_ID, "--follow"]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error streaming logs: {e}{RESET}")
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Log streaming stopped.{RESET}")

def check_health():
    """Check application health endpoint."""
    if not APP_URL:
        print(f"{RED}App URL not set. Please set OMEGA_DO_APP_URL environment variable.{RESET}")
        return
    
    health_url = f"{APP_URL.rstrip('/')}/health"
    print(f"{CYAN}Checking health endpoint: {health_url}{RESET}")
    
    try:
        response = urllib.request.urlopen(health_url)
        data = json.loads(response.read().decode('utf-8'))
        
        # Display health status with divine styling
        status = data.get("status", "unknown")
        status_color = GREEN if status == "healthy" else (YELLOW if status == "degraded" else RED)
        
        print(f"\n{BOLD}Health Status: {status_color}{status.upper()}{RESET}")
        print(f"{CYAN}Redis Connected: {GREEN if data.get('redis_connected', False) else RED}{data.get('redis_connected', False)}{RESET}")
        print(f"{CYAN}WebSocket Connected: {GREEN if data.get('websocket_connected', False) else RED}{data.get('websocket_connected', False)}{RESET}")
        
        # Format last update time
        last_update = data.get("last_price_update")
        if last_update:
            print(f"{CYAN}Last Price Update: {YELLOW}{format_timestamp(last_update)}{RESET}")
        
        # Show uptime
        uptime = data.get("uptime", 0)
        days, remainder = divmod(uptime, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"
        print(f"{CYAN}Uptime: {YELLOW}{uptime_str}{RESET}")
        
        # Show additional details
        details = data.get("details", {})
        if details:
            print(f"\n{BOLD}Additional Details:{RESET}")
            for key, value in details.items():
                print(f"{CYAN}{key}: {YELLOW}{value}{RESET}")
                
    except urllib.error.URLError as e:
        print(f"{RED}Error connecting to health endpoint: {e.reason}{RESET}")
    except json.JSONDecodeError:
        print(f"{RED}Invalid JSON response from health endpoint{RESET}")
    except Exception as e:
        print(f"{RED}Error: {str(e)}{RESET}")

def test_redis():
    """Test Redis connection using Digital Ocean app console."""
    print(f"{CYAN}Testing Redis connection...{RESET}")
    
    # Get current active deployment
    deploy_result = run_command([DOCTL_PATH, "apps", "list-deployments", APP_ID, "--format", "ID,Phase"])
    
    if not deploy_result["success"]:
        print(f"{RED}Error getting deployment ID: {deploy_result['output']}{RESET}")
        return
        
    # Find active deployment
    deployment_id = None
    for line in deploy_result["output"].strip().split('\n')[1:]:
        if "ACTIVE" in line:
            deployment_id = line.split()[0]
            break
    
    if not deployment_id:
        print(f"{RED}No active deployment found{RESET}")
        return
    
    # Create console session
    console_cmd = [
        DOCTL_PATH, "apps", "console", APP_ID,
        "--deployment", deployment_id,
        "--component", "btc-live-feed"
    ]
    
    print(f"{YELLOW}Creating console session...{RESET}")
    
    # Execute enhanced Redis test command
    redis_test_cmd = """python3 -c "
import os
import redis
import json
import time
from datetime import datetime

try:
    # Get Redis connection params from environment
    redis_host = os.getenv('REDIS_HOST')
    redis_port = int(os.getenv('REDIS_PORT', 6379))
    redis_username = os.getenv('REDIS_USERNAME')
    redis_password = os.getenv('REDIS_PASSWORD')
    redis_ssl = os.getenv('REDIS_SSL', 'false').lower() == 'true'
    
    # Print connection details (no password)
    print(f'Connecting to Redis at {redis_host}:{redis_port}')
    print(f'SSL enabled: {redis_ssl}')
    print(f'Username: {redis_username}')
    
    # Connect to Redis
    r = redis.Redis(
        host=redis_host,
        port=redis_port,
        username=redis_username,
        password=redis_password,
        ssl=redis_ssl,
        decode_responses=True
    )
    
    # Test connection
    ping_start = time.time()
    ping_result = r.ping()
    ping_time = time.time() - ping_start
    
    print(f'\\nRedis connection test: {'SUCCESS' if ping_result else 'FAILED'}')
    print(f'Ping response time: {ping_time*1000:.2f}ms')
    
    # Get basic Redis stats
    info = r.info()
    print(f'Redis version: {info.get(\"redis_version\")}')
    print(f'Connected clients: {info.get(\"connected_clients\")}')
    print(f'Memory used: {info.get(\"used_memory_human\")}')
    
    # Get last price data
    btc_price = r.get('last_btc_price')
    price_update_time = r.get('last_btc_update_time')
    trade_volume = r.get('btc_24h_volume')
    price_change = r.get('btc_24h_change')
    
    print(f'\\n--- BTC Market Data ---')
    if btc_price:
        print(f'Last BTC price: ${float(btc_price):,.2f}')
    else:
        print('Last BTC price: Not available')
        
    if price_update_time:
        dt = datetime.fromtimestamp(float(price_update_time))
        print(f'Last update time: {dt.strftime(\"%Y-%m-%d %H:%M:%S UTC\")}')
        print(f'Seconds since update: {time.time() - float(price_update_time):.1f}s')
    else:
        print('Last update time: Not available')
    
    if trade_volume:
        print(f'24h Trading volume: {float(trade_volume):,.2f} BTC')
    
    if price_change:
        change = float(price_change)
        change_sign = '+' if change >= 0 else ''
        print(f'24h Price change: {change_sign}{change:.2f}%')
    
    # List all keys in Redis
    print(f'\\n--- Redis Keys ({len(r.keys())}) ---')
    for key in sorted(r.keys())[:15]:  # Limit to first 15 keys
        key_type = r.type(key)
        if key_type == 'string':
            value = r.get(key)
            # Truncate long values
            if len(value) > 50:
                value = value[:47] + '...'
            print(f'  {key} ({key_type}): {value}')
        elif key_type == 'hash':
            print(f'  {key} ({key_type}): {len(r.hkeys(key))} fields')
        elif key_type == 'list':
            print(f'  {key} ({key_type}): {r.llen(key)} items')
        else:
            print(f'  {key} ({key_type})')
    
    if len(r.keys()) > 15:
        print(f'  ... and {len(r.keys()) - 15} more keys')
    
except Exception as e:
    print(f'Error testing Redis connection: {str(e)}')
\""""
    
    console_result = run_command(console_cmd + ["--command", redis_test_cmd])
    
    if console_result["success"]:
        print()
        for line in console_result["output"].split('\n'):
            if "SUCCESS" in line:
                print(f"{GREEN}{line}{RESET}")
            elif "FAILED" in line or "Error" in line:
                print(f"{RED}{line}{RESET}")
            elif "BTC price:" in line:
                print(f"{YELLOW}{line}{RESET}")
            elif "---" in line:
                print(f"{CYAN}{BOLD}{line}{RESET}")
            else:
                print(line)
    else:
        print(f"{RED}Error executing Redis test: {console_result['output']}{RESET}")

def watch_price():
    """Watch BTC price updates in real-time."""
    print(f"{CYAN}Watching BTC price updates in real-time (press Ctrl+C to stop)...{RESET}")
    
    # Get current active deployment
    deploy_result = run_command([DOCTL_PATH, "apps", "list-deployments", APP_ID, "--format", "ID,Phase"])
    
    if not deploy_result["success"]:
        print(f"{RED}Error getting deployment ID: {deploy_result['output']}{RESET}")
        return
        
    # Find active deployment
    deployment_id = None
    for line in deploy_result["output"].strip().split('\n')[1:]:
        if "ACTIVE" in line:
            deployment_id = line.split()[0]
            break
    
    if not deployment_id:
        print(f"{RED}No active deployment found{RESET}")
        return
    
    # Create console session
    console_cmd = [
        DOCTL_PATH, "apps", "console", APP_ID,
        "--deployment", deployment_id,
        "--component", "btc-live-feed"
    ]
    
    print(f"{YELLOW}Creating console session...{RESET}")
    
    # Execute price watch command
    price_watch_cmd = """python3 -c "
import os
import redis
import time
import signal
from datetime import datetime

# Handle Ctrl+C gracefully
def signal_handler(sig, frame):
    print('\\nExiting price watch...')
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

try:
    # Connect to Redis
    r = redis.Redis(
        host=os.getenv('REDIS_HOST'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        username=os.getenv('REDIS_USERNAME'),
        password=os.getenv('REDIS_PASSWORD'),
        ssl=os.getenv('REDIS_SSL', 'false').lower() == 'true',
        decode_responses=True
    )
    
    print('Successfully connected to Redis')
    print('Watching for price updates (Ctrl+C to stop)...\\n')
    
    last_price = None
    while True:
        price = r.get('last_btc_price')
        update_time = r.get('last_btc_update_time')
        
        if price and update_time:
            price = float(price)
            dt = datetime.fromtimestamp(float(update_time))
            time_str = dt.strftime('%H:%M:%S')
            
            # Calculate price change if we have a previous price
            if last_price:
                change = price - last_price
                change_pct = (change / last_price) * 100
                change_sign = '+' if change >= 0 else ''
                arrow = '🟢 ↑' if change > 0 else ('🔴 ↓' if change < 0 else '⚪️ →')
                
                print(f'{time_str} | BTC: ${price:,.2f} | {arrow} {change_sign}{change:.2f} ({change_sign}{change_pct:.3f}%)')
            else:
                print(f'{time_str} | BTC: ${price:,.2f}')
            
            last_price = price
        
        time.sleep(5)
except Exception as e:
    print(f'Error in price watch: {str(e)}')
\""""
    
    try:
        # Run the command without capturing output
        subprocess.run(console_cmd + ["--command", price_watch_cmd], check=True)
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error watching price: {e}{RESET}")
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Price watch stopped.{RESET}")

def show_stats():
    """Show resource usage statistics."""
    print(f"{CYAN}Getting resource statistics...{RESET}")
    
    # Get current active deployment
    deploy_result = run_command([DOCTL_PATH, "apps", "list-deployments", APP_ID, "--format", "ID,Phase"])
    
    if not deploy_result["success"]:
        print(f"{RED}Error getting deployment ID: {deploy_result['output']}{RESET}")
        return
        
    # Find active deployment
    deployment_id = None
    for line in deploy_result["output"].strip().split('\n')[1:]:
        if "ACTIVE" in line:
            deployment_id = line.split()[0]
            break
    
    if not deployment_id:
        print(f"{RED}No active deployment found{RESET}")
        return
    
    # Create console session
    console_cmd = [
        DOCTL_PATH, "apps", "console", APP_ID,
        "--deployment", deployment_id,
        "--component", "btc-live-feed"
    ]
    
    print(f"{YELLOW}Creating console session...{RESET}")
    
    # Execute system stats command
    stats_cmd = "python3 -c \"import os, psutil; print('CPU Usage: {:.1f}%'.format(psutil.cpu_percent())); print('Memory Usage: {:.1f}%'.format(psutil.virtual_memory().percent)); print('Disk Usage: {:.1f}%'.format(psutil.disk_usage('/').percent)); print('Network Stats:'); connections = len(psutil.net_connections()); print(f'  Connections: {connections}'); print('Top Processes:'); print('\\n'.join(['  ' + line for line in os.popen('ps aux | sort -nrk 3,3 | head -n 5').read().split('\\n')[:5]]))\""
    
    console_result = run_command(console_cmd + ["--command", stats_cmd])
    
    if console_result["success"]:
        output_lines = console_result["output"].split('\n')
        
        # Find the relevant stats in the output
        stats_line = next((i for i, line in enumerate(output_lines) if "CPU Usage:" in line), None)
        
        if stats_line is not None:
            # Display stats with nice formatting
            i = stats_line
            while i < len(output_lines) and i < stats_line + 20:
                line = output_lines[i]
                
                if "CPU Usage:" in line:
                    usage = float(line.split(':')[1].strip().replace('%', ''))
                    color = GREEN if usage < 50 else (YELLOW if usage < 80 else RED)
                    print(f"{CYAN}CPU Usage: {color}{line.split(':')[1].strip()}{RESET}")
                elif "Memory Usage:" in line:
                    usage = float(line.split(':')[1].strip().replace('%', ''))
                    color = GREEN if usage < 50 else (YELLOW if usage < 80 else RED)
                    print(f"{CYAN}Memory Usage: {color}{line.split(':')[1].strip()}{RESET}")
                elif "Disk Usage:" in line:
                    usage = float(line.split(':')[1].strip().replace('%', ''))
                    color = GREEN if usage < 50 else (YELLOW if usage < 80 else RED)
                    print(f"{CYAN}Disk Usage: {color}{line.split(':')[1].strip()}{RESET}")
                elif "Network Stats:" in line:
                    print(f"\n{BOLD}{CYAN}Network Statistics:{RESET}")
                elif "Connections:" in line:
                    count = int(line.split(':')[1].strip())
                    color = GREEN if count < 100 else (YELLOW if count < 500 else RED)
                    print(f"{CYAN}Connections: {color}{count}{RESET}")
                elif "Top Processes:" in line:
                    print(f"\n{BOLD}{CYAN}Top Processes:{RESET}")
                elif line.strip().startswith("USER") or line.strip().startswith("root"):
                    # Format process line
                    print(f"{YELLOW}{line.strip()}{RESET}")
                else:
                    print(line)
                    
                i += 1
        else:
            print(f"{RED}Could not parse resource statistics{RESET}")
    else:
        print(f"{RED}Error getting resource statistics: {console_result['output']}{RESET}")

def show_help():
    """Show help message."""
    print(f"{CYAN}Available commands:{RESET}")
    print(f"  {YELLOW}status{RESET}      - Show current deployment status")
    print(f"  {YELLOW}logs{RESET}        - Stream logs in real-time")
    print(f"  {YELLOW}health{RESET}      - Check application health")
    print(f"  {YELLOW}redis{RESET}       - Test Redis connection and view data")
    print(f"  {YELLOW}stats{RESET}       - Show resource usage statistics")
    print(f"  {YELLOW}watch_price{RESET} - Watch BTC price updates in real-time")
    print(f"  {YELLOW}help{RESET}        - Show this help message")
    
    print(f"\n{CYAN}Examples:{RESET}")
    print(f"  {MAGENTA}./omega_do_monitor.py status{RESET}")
    print(f"  {MAGENTA}./omega_do_monitor.py watch_price{RESET}")

def main():
    """Main function."""
    signal.signal(signal.SIGINT, handle_sigint)
    
    parser = argparse.ArgumentParser(
        description="🔱 OMEGA D0T7 DIVINE DIGIT4L 0CE4N Monitor 🔱",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        default="help",
        choices=["status", "logs", "health", "redis", "stats", "watch_price", "help"],
        help="Command to execute"
    )
    
    args = parser.parse_args()
    
    divine_header()
    
    if args.command == "status":
        show_status()
    elif args.command == "logs":
        stream_logs()
    elif args.command == "health":
        check_health()
    elif args.command == "redis":
        test_redis()
    elif args.command == "stats":
        show_stats()
    elif args.command == "watch_price":
        watch_price()
    else:
        show_help()
    
    print(f"\n{YELLOW}JAH JAH BLESS THE ETERNAL FLOW OF THE BLOCKCHAIN{RESET}\n")

if __name__ == "__main__":
    main() 