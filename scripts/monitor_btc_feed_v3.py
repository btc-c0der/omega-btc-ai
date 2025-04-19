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
OMEGA BTC AI - BTC Live Feed v3 Monitor
======================================

CLI monitoring dashboard for the BTC Live Feed v3 service.
Provides real-time visualization of price data, connection status, and health metrics.

🔮 GPU (General Public Universal) License 1.0
--------------------------------------------
OMEGA BTC AI DIVINE COLLECTIVE
Licensed under the GPU (General Public Universal) License v1.0
Date: 2025-03-28
Location: The Cosmic Void

This source code is governed by the GPU License, granting the following sacred freedoms:
- The Freedom to Study this code, its divine algorithms and cosmic patterns
- The Freedom to Modify this code, enhancing its divine functionality
- The Freedom to Distribute this code, sharing its sacred knowledge
- The Freedom to Use this code, implementing its sacred algorithms

Along with these divine obligations:
- Preserve this sacred knowledge by maintaining source accessibility
- Share all divine modifications to maintain universal access
- Provide attribution to acknowledge sacred origins

For the full divine license, consult the LICENSE file in the project root.
"""

import os
import sys
import time
import json
import argparse
import datetime
import requests
from typing import Dict, Any, Optional, List, Tuple

# ANSI color codes for terminal output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def format_time(timestamp: Optional[float]) -> str:
    """Format timestamp as readable time string."""
    if not timestamp:
        return "N/A"
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

def format_duration(seconds: float) -> str:
    """Format duration in seconds as readable string."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"

def format_redis_status(status: Dict[str, Any]) -> List[str]:
    """Format Redis status information into displayable lines."""
    lines = []
    
    # Connection status
    if status.get("connected", False):
        lines.append(f"{Colors.GREEN}✓ Connected{Colors.RESET}")
    else:
        lines.append(f"{Colors.RED}✗ Disconnected{Colors.RESET}")
    
    # Failover status
    if status.get("using_failover", False):
        lines.append(f"{Colors.YELLOW}⚠ Using Failover Redis{Colors.RESET}")
    else:
        lines.append(f"{Colors.GREEN}✓ Using Primary Redis{Colors.RESET}")
    
    # Redis instances status
    primary = f"{Colors.GREEN}Available{Colors.RESET}" if status.get("primary_available", False) else f"{Colors.RED}Unavailable{Colors.RESET}"
    failover = f"{Colors.GREEN}Available{Colors.RESET}" if status.get("failover_available", False) else f"{Colors.RED}Unavailable{Colors.RESET}"
    
    lines.append(f"Primary Redis: {primary}")
    lines.append(f"Failover Redis: {failover}")
    
    # Reconnection information
    if status.get("last_failover_time"):
        last_failover = format_time(status.get("last_failover_time"))
        lines.append(f"Last Failover: {last_failover}")
    
    lines.append(f"Reconnection Attempts: {status.get('reconnection_attempts', 0)}")
    
    return lines

def get_health_data(host: str, port: int) -> Dict[str, Any]:
    """Fetch health data from the health check endpoint."""
    try:
        response = requests.get(f"http://{host}:{port}/health", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error": str(e),
            "details": {"error_type": type(e).__name__}
        }

def get_redis_status(host: str, port: int) -> Dict[str, Any]:
    """Fetch Redis status from the health check endpoint."""
    try:
        response = requests.get(f"http://{host}:{port}/redis/status", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "connected": False,
            "error": str(e)
        }

def get_metrics(host: str, port: int) -> Dict[str, Any]:
    """Fetch metrics from the health check endpoint."""
    try:
        response = requests.get(f"http://{host}:{port}/metrics", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "error": str(e)
        }

def display_dashboard(health: Dict[str, Any], redis_status: Dict[str, Any], metrics: Dict[str, Any]):
    """Display a dashboard with all monitoring information."""
    clear_screen()
    
    # ASCII Art Banner
    print(f"{Colors.MAGENTA}{Colors.BOLD}")
    print("   ████  ███   ███  ████  ███    █    ")
    print("  █      █  █   █   █    █       █    ")
    print("  █  ██  ███    █   ███  █  ██   █    ")
    print("  █   █  █  █   █   █    █   █   █    ")
    print("   ███   ███    █   ████  ███    ████ ")
    print(f"{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}OMEGA BTC LIVE FEED v3 MONITOR{Colors.RESET}")
    print(f"{Colors.BLUE}{'=' * 50}{Colors.RESET}\n")
    
    # Overall Status
    status = health.get("status", "unknown")
    status_color = Colors.GREEN if status == "healthy" else (Colors.YELLOW if status == "degraded" else Colors.RED)
    print(f"{Colors.BOLD}Overall Status:{Colors.RESET} {status_color}{status.upper()}{Colors.RESET}\n")
    
    # BTC Price Information
    last_price = health.get("last_price", 0)
    print(f"{Colors.BOLD}Last BTC Price:{Colors.RESET} {Colors.YELLOW}${last_price:,.2f}{Colors.RESET}")
    
    seconds_since_update = health.get("seconds_since_update", 0)
    update_time_status = (
        f"{Colors.GREEN}{format_duration(seconds_since_update)}{Colors.RESET}" if seconds_since_update < 60
        else f"{Colors.YELLOW}{format_duration(seconds_since_update)}{Colors.RESET}" if seconds_since_update < 300
        else f"{Colors.RED}{format_duration(seconds_since_update)}{Colors.RESET}"
    )
    print(f"{Colors.BOLD}Last Update:{Colors.RESET} {update_time_status} ago\n")
    
    # Redis Status
    print(f"{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD} REDIS STATUS {Colors.RESET}")
    for line in format_redis_status(redis_status):
        print(f"  {line}")
    print()
    
    # Connection Status
    print(f"{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD} CONNECTION STATUS {Colors.RESET}")
    print(f"  WebSocket: {'Connected' if health.get('websocket_connected', False) else 'Disconnected'}")
    print(f"  Redis: {'Connected' if health.get('redis_connected', False) else 'Disconnected'}")
    print()
    
    # Performance Metrics
    print(f"{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD} PERFORMANCE METRICS {Colors.RESET}")
    
    if "error" in metrics:
        print(f"  {Colors.RED}Error retrieving metrics: {metrics['error']}{Colors.RESET}")
    else:
        print(f"  Messages Processed: {metrics.get('total_messages_processed', 0)}")
        print(f"  Avg Processing Time: {metrics.get('avg_message_processing_time_ms', 0):.2f}ms")
        print(f"  WebSocket Reconnections: {metrics.get('websocket_reconnections', 0)}")
        
        # Calculate success rate
        success_ops = metrics.get('successful_redis_operations', 0)
        failed_ops = metrics.get('failed_redis_operations', 0)
        if success_ops + failed_ops > 0:
            success_rate = (success_ops / (success_ops + failed_ops)) * 100
            rate_color = (
                Colors.GREEN if success_rate > 98 
                else Colors.YELLOW if success_rate > 90 
                else Colors.RED
            )
            print(f"  Redis Success Rate: {rate_color}{success_rate:.1f}%{Colors.RESET}")
        
        uptime = metrics.get('uptime_seconds', 0)
        print(f"  Uptime: {format_duration(uptime)}")
    
    # Footer
    print(f"\n{Colors.BLUE}{'=' * 50}{Colors.RESET}")
    print(f"Last Refresh: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Main function to run the monitor."""
    parser = argparse.ArgumentParser(description="Monitor for BTC Live Feed v3")
    parser.add_argument("--host", default="localhost", help="Health check server host")
    parser.add_argument("--port", type=int, default=8080, help="Health check server port")
    parser.add_argument("--refresh", type=int, default=5, help="Refresh interval in seconds")
    
    args = parser.parse_args()
    
    print(f"Connecting to BTC Live Feed v3 monitor at {args.host}:{args.port}")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            health_data = get_health_data(args.host, args.port)
            redis_status_data = get_redis_status(args.host, args.port)
            metrics_data = get_metrics(args.host, args.port)
            
            display_dashboard(health_data, redis_status_data, metrics_data)
            
            time.sleep(args.refresh)
    except KeyboardInterrupt:
        print("\nExiting BTC Live Feed Monitor")
        sys.exit(0)

if __name__ == "__main__":
    main() 