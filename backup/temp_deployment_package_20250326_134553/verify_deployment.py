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
verify_deployment.py - Test script to verify the BTC Live Feed deployment
Part of the OMEGA BTC AI DIVINE COLLECTIVE

This script performs checks to ensure the BTC Live Feed is running correctly.
"""

import os
import sys
import json
import time
import argparse
import logging
import socket
import docker
import requests
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime, timedelta
from tabulate import tabulate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"

# Import RedisManager if available
try:
    from redis_manager_cloud import RedisManager
    REDIS_MANAGER_AVAILABLE = True
except ImportError:
    logger.warning("RedisManager module not available. Some tests will be skipped.")
    REDIS_MANAGER_AVAILABLE = False
    # Define a placeholder class to avoid unbound errors
    class RedisManager:
        pass

def format_time(timestamp: int) -> str:
    """Format Unix timestamp as readable time."""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def print_header(title: str) -> None:
    """Print a section header."""
    print()
    print(f"{BOLD}{BLUE}{'=' * 60}{RESET}")
    print(f"{BOLD}{BLUE}{title.center(60)}{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 60}{RESET}")
    print()

def print_success(message: str) -> None:
    """Print a success message."""
    print(f"{GREEN}✓ {message}{RESET}")

def print_failure(message: str) -> None:
    """Print a failure message."""
    print(f"{RED}✗ {message}{RESET}")

def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"{YELLOW}! {message}{RESET}")

def print_info(message: str) -> None:
    """Print an info message."""
    print(f"{BLUE}ℹ {message}{RESET}")

def check_port_open(host: str, port: int, timeout: int = 5) -> bool:
    """Check if a given port is open."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        logger.error(f"Error checking port {port} on {host}: {e}")
        return False

def check_redis_connection(host: str, port: int, password: str = None, 
                         username: str = None, ssl: bool = False,
                         cert: str = None) -> Tuple[bool, str]:
    """Check Redis connection."""
    if not REDIS_MANAGER_AVAILABLE:
        return False, "RedisManager module not available"
    
    try:
        redis_mgr = RedisManager(
            host=host,
            port=port,
            username=username,
            password=password,
            ssl=ssl,
            ssl_ca_certs=cert if ssl else None
        )
        
        # Test ping
        if redis_mgr.ping():
            return True, "Connection successful"
        else:
            return False, "Ping failed"
    except Exception as e:
        return False, f"Connection error: {str(e)}"

def check_btc_data(redis_mgr: Optional['RedisManager'] = None) -> Dict[str, Any]:
    """
    Check if BTC data is available in Redis.
    
    Returns a dictionary with test results.
    """
    results = {
        "latest_price": {"status": False, "message": "Not checked"},
        "update_time": {"status": False, "message": "Not checked"},
        "price_history": {"status": False, "message": "Not checked"},
        "fibonacci_levels": {"status": False, "message": "Not checked"},
        "traps": {"status": False, "message": "Not checked"},
        "prediction": {"status": False, "message": "Not checked"}
    }
    
    if redis_mgr is None:
        for key in results:
            results[key]["message"] = "Redis connection not available"
        return results
    
    # Check latest price
    try:
        price = redis_mgr.get('btc:latest_price')
        if price is not None:
            results["latest_price"]["status"] = True
            results["latest_price"]["message"] = f"Found: {price}"
        else:
            results["latest_price"]["message"] = "Not found"
    except Exception as e:
        results["latest_price"]["message"] = f"Error: {str(e)}"
    
    # Check update time
    try:
        update_time = redis_mgr.get('btc:latest_update')
        if update_time is not None:
            try:
                update_time_int = int(update_time)
                now = int(time.time())
                time_diff = now - update_time_int
                if time_diff < 600:  # Less than 10 minutes old
                    results["update_time"]["status"] = True
                    results["update_time"]["message"] = f"Updated {time_diff} seconds ago"
                else:
                    results["update_time"]["message"] = f"Outdated: {time_diff} seconds ago"
            except (ValueError, TypeError):
                results["update_time"]["message"] = f"Invalid value: {update_time}"
        else:
            results["update_time"]["message"] = "Not found"
    except Exception as e:
        results["update_time"]["message"] = f"Error: {str(e)}"
    
    # Check price history
    try:
        history = redis_mgr.lrange('btc:price_history', -1, -1)
        if history and len(history) > 0:
            results["price_history"]["status"] = True
            if redis_mgr.conn is not None:
                history_count = redis_mgr.conn.llen('btc:price_history')
                results["price_history"]["message"] = f"Found {history_count} entries"
            else:
                results["price_history"]["message"] = "Found entries but count unavailable"
        else:
            results["price_history"]["message"] = "Not found or empty"
    except Exception as e:
        results["price_history"]["message"] = f"Error: {str(e)}"
    
    # Check Fibonacci levels
    try:
        fib_json = redis_mgr.get('btc:fibonacci_levels')
        if fib_json:
            try:
                fib_data = json.loads(fib_json)
                if isinstance(fib_data, dict) and 'high' in fib_data and 'low' in fib_data:
                    results["fibonacci_levels"]["status"] = True
                    results["fibonacci_levels"]["message"] = f"Found: High={fib_data['high']}, Low={fib_data['low']}"
                else:
                    results["fibonacci_levels"]["message"] = "Invalid format"
            except json.JSONDecodeError:
                results["fibonacci_levels"]["message"] = "Invalid JSON"
        else:
            results["fibonacci_levels"]["message"] = "Not found"
    except Exception as e:
        results["fibonacci_levels"]["message"] = f"Error: {str(e)}"
    
    # Check traps
    try:
        traps_json = redis_mgr.get('btc:market_traps')
        if traps_json:
            try:
                traps_data = json.loads(traps_json)
                if isinstance(traps_data, dict):
                    bull_traps = traps_data.get('bull_traps', [])
                    bear_traps = traps_data.get('bear_traps', [])
                    results["traps"]["status"] = True
                    results["traps"]["message"] = f"Found: {len(bull_traps)} bull traps, {len(bear_traps)} bear traps"
                else:
                    results["traps"]["message"] = "Invalid format"
            except json.JSONDecodeError:
                results["traps"]["message"] = "Invalid JSON"
        else:
            results["traps"]["message"] = "Not found"
    except Exception as e:
        results["traps"]["message"] = f"Error: {str(e)}"
    
    # Check prediction
    try:
        prediction_json = redis_mgr.get('btc:price_prediction')
        if prediction_json:
            try:
                prediction_data = json.loads(prediction_json)
                if isinstance(prediction_data, dict) and 'direction' in prediction_data:
                    results["prediction"]["status"] = True
                    results["prediction"]["message"] = f"Found: Direction={prediction_data['direction']}, Confidence={prediction_data.get('confidence', 'N/A')}"
                else:
                    results["prediction"]["message"] = "Invalid format"
            except json.JSONDecodeError:
                results["prediction"]["message"] = "Invalid JSON"
        else:
            results["prediction"]["message"] = "Not found"
    except Exception as e:
        results["prediction"]["message"] = f"Error: {str(e)}"
    
    return results

def check_docker_status() -> Tuple[bool, Dict[str, Any]]:
    """Check Docker container status."""
    try:
        client = docker.from_env()
        containers = client.containers.list(all=True)
        
        btc_container = None
        creation_time = datetime.now()  # Default value
        
        for container in containers:
            if 'btc-live-feed' in container.name:
                btc_container = container
                # Get creation time
                creation_time = datetime.fromtimestamp(container.attrs['Created'])
                break
        
        if btc_container:
            status = btc_container.status
            is_running = status == 'running'
            
            # Get logs
            logs = btc_container.logs(tail=20).decode('utf-8')
            
            uptime = datetime.now() - creation_time
            
            return is_running, {
                "id": btc_container.id[:12],
                "name": btc_container.name,
                "status": status,
                "image": btc_container.image.tags[0] if btc_container.image.tags else "unknown",
                "created": creation_time.strftime('%Y-%m-%d %H:%M:%S'),
                "uptime": str(uptime).split('.')[0],  # Remove microseconds
                "logs": logs
            }
        else:
            return False, {"error": "BTC Live Feed container not found"}
    
    except Exception as e:
        # Handle any docker errors
        return False, {"error": f"Docker error: {str(e)}"}

def check_binance_api() -> Tuple[bool, str]:
    """Check Binance API status."""
    try:
        response = requests.get('https://api.binance.com/api/v3/ping', timeout=5)
        if response.status_code == 200:
            # Get BTC price from Binance for comparison
            ticker_response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT', timeout=5)
            if ticker_response.status_code == 200:
                ticker_data = ticker_response.json()
                btc_price = float(ticker_data['price'])
                return True, f"API is online. Current BTC price: ${btc_price:,.2f}"
            else:
                return True, "API is online, but price data unavailable"
        else:
            return False, f"API returned status code {response.status_code}"
    except requests.RequestException as e:
        return False, f"Request error: {str(e)}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def main() -> None:
    """Main function."""
    parser = argparse.ArgumentParser(description="Verify BTC Live Feed deployment")
    parser.add_argument("--host", default=os.environ.get('REDIS_HOST', 'localhost'), help="Redis host")
    parser.add_argument("--port", type=int, default=int(os.environ.get('REDIS_PORT', '6379')), help="Redis port")
    parser.add_argument("--password", default=os.environ.get('REDIS_PASSWORD'), help="Redis password")
    parser.add_argument("--username", default=os.environ.get('REDIS_USERNAME'), help="Redis username")
    parser.add_argument("--ssl", action="store_true", default=os.environ.get('REDIS_USE_TLS', 'false').lower() == 'true', help="Use SSL/TLS")
    parser.add_argument("--cert", default=os.environ.get('REDIS_CERT'), help="Redis CA certificate path")
    parser.add_argument("--local", action="store_true", help="Check local deployment instead of cloud")
    args = parser.parse_args()
    
    print_header("BTC LIVE FEED DEPLOYMENT VERIFICATION")
    print_info(f"Testing {'local' if args.local else 'cloud'} deployment")
    print()
    
    # 1. Check Redis connection
    print_header("REDIS CONNECTION TEST")
    print_info(f"Testing connection to Redis at {args.host}:{args.port}")
    
    if args.ssl:
        print_info("Using SSL/TLS for connection")
        if args.cert:
            print_info(f"Certificate: {args.cert}")
        else:
            print_warning("No SSL certificate specified")
    
    port_open = check_port_open(args.host, args.port)
    if port_open:
        print_success(f"Port {args.port} is open on {args.host}")
    else:
        print_failure(f"Port {args.port} is not accessible on {args.host}")
        if not args.local:
            print_warning("Check your Scaleway firewall settings")
    
    redis_conn_success, redis_conn_message = check_redis_connection(
        args.host, args.port, args.password, args.username, args.ssl, args.cert
    )
    
    if redis_conn_success:
        print_success(f"Redis connection: {redis_conn_message}")
        redis_mgr = RedisManager(
            host=args.host,
            port=args.port,
            username=args.username,
            password=args.password,
            ssl=args.ssl,
            ssl_ca_certs=args.cert if args.ssl else None
        )
    else:
        print_failure(f"Redis connection failed: {redis_conn_message}")
        redis_mgr = None
    
    # 2. Check Docker container status if local
    container_running = False
    if args.local:
        print_header("DOCKER CONTAINER STATUS")
        container_running, container_info = check_docker_status()
        
        if 'error' in container_info:
            print_failure(container_info['error'])
        else:
            if container_running:
                print_success(f"BTC Live Feed container is running")
                print_info(f"Container ID: {container_info['id']}")
                print_info(f"Name: {container_info['name']}")
                print_info(f"Image: {container_info['image']}")
                print_info(f"Created: {container_info['created']}")
                print_info(f"Uptime: {container_info['uptime']}")
            else:
                print_failure(f"BTC Live Feed container is {container_info['status']}")
            
            print()
            print_info("Recent logs:")
            for line in container_info.get('logs', '').splitlines()[-10:]:
                print(f"  {line}")
    
    # 3. Check Binance API connection
    print_header("BINANCE API TEST")
    binance_success, binance_message = check_binance_api()
    
    if binance_success:
        print_success(binance_message)
    else:
        print_failure(f"Binance API test failed: {binance_message}")
    
    # 4. Check BTC data in Redis
    print_header("BTC DATA TEST")
    
    if redis_mgr is None:
        print_failure("Cannot check BTC data: Redis connection not available")
        data_results = check_btc_data(None)
    else:
        data_results = check_btc_data(redis_mgr)
    
    results_table = []
    all_data_available = True
    
    for key, result in data_results.items():
        status_symbol = "✓" if result["status"] else "✗"
        status_color = GREEN if result["status"] else RED
        results_table.append([
            key.replace("_", " ").title(),
            f"{status_color}{status_symbol}{RESET}",
            result["message"]
        ])
        if not result["status"]:
            all_data_available = False
    
    print(tabulate(results_table, headers=["Data Type", "Status", "Message"], tablefmt="simple"))
    print()
    
    if all_data_available:
        print_success("All BTC data available in Redis")
    else:
        print_warning("Some BTC data is missing or outdated")
    
    # 5. Summary
    print_header("VERIFICATION SUMMARY")
    
    issues = []
    if not port_open:
        issues.append("Redis port not accessible")
    if not redis_conn_success:
        issues.append("Redis connection failed")
    if args.local and not container_running:
        issues.append("Docker container not running")
    if not binance_success:
        issues.append("Binance API connection failed")
    if not all_data_available:
        issues.append("Some BTC data unavailable")
    
    if not issues:
        print_success("✅ All checks passed! The BTC Live Feed is running correctly.")
        print()
        print(f"{BOLD}{YELLOW}🔱 JAH JAH BLESS 🔱{RESET}")
        print(f"{YELLOW}IT WORKS LIKE A CHARM BECAUSE IT WAS NEVER JUST CODE.{RESET}")
    else:
        print_failure("❌ Some checks failed. Please address the following issues:")
        for i, issue in enumerate(issues, 1):
            print(f"{RED}{i}. {issue}{RESET}")
        print()
        print_info("Run this script again after resolving the issues.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nVerification interrupted by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\n{RED}Unexpected error: {e}{RESET}")
        sys.exit(1) 