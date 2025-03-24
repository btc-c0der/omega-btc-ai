#!/usr/bin/env python3
# filepath: /Users/fsiqueira/Desktop/Code/omega_btc_ai/tools/redis_monitor.py

"""
OmegaBTC Redis Monitor
======================

Comprehensive Redis monitoring tool for diagnosing issues with price feeds,
queue processing, and system performance.

Usage:
    python redis_monitor.py [options]

Options:
    --keys-only       Only show key monitoring
    --stats-only      Only show Redis server statistics
    --queues-only     Only show queue monitoring
    --watch=PATTERN   Watch specific key pattern (e.g. *btc* or last_*)
    --interval=SECS   Update interval in seconds (default: 2)
"""

import argparse
import datetime
import json
import os
import redis
import signal
import sys
import time
from collections import defaultdict

# ANSI colors for terminal output
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Redis connection
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

# Keys of interest for BTC price tracking
PRICE_KEYS = [
    "last_btc_price",
    "sim_last_btc_price",
    "prev_btc_price",
    "btc_price_1min",
    "hf_trap_mode_active",
    "volatility_1min",
    "price_acceleration_1min"
]

# Performance and health keys
HEALTH_KEYS = [
    "hf_trap_count",
    "grafana:high_confidence_traps",
    "grafana:liquidity_grab_count",
    "schumann_resonance"
]

# Queue keys to monitor
QUEUE_KEYS = [
    "queue:*",
    "processing:*",
    "*queue*",
    "tasks:*",
    "pending:*",
    "jobs:*",
    "rq:*"  # Redis Queue (RQ) keys
]

class RedisMonitor:
    def __init__(self, watch_pattern=None, update_interval=2):
        """Initialize Redis monitor"""
        self.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        self.watch_pattern = watch_pattern or "*"
        self.update_interval = update_interval
        self.previous_values = {}
        self.update_counts = defaultdict(int)
        self.last_updated = {}
        self.running = True
        
        # Set up signal handlers for clean exit
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)
        
    def handle_signal(self, sig, frame):
        """Handle termination signals"""
        print(f"{YELLOW}Shutting down Redis monitor...{RESET}")
        self.running = False
        
    def get_key_info(self, key_pattern="*"):
        """Get information about keys matching pattern"""
        keys = self.redis.keys(key_pattern)
        result = []
        
        for key in keys:
            key_str = key.decode('utf-8')
            key_type = self.redis.type(key).decode('utf-8')
            ttl = self.redis.ttl(key)
            if ttl < 0:
                ttl_str = "No expiration"
            else:
                ttl_str = f"{ttl}s"
                
            value = None
            try:
                if key_type == "string":
                    raw_value = self.redis.get(key)
                    if raw_value:
                        try:
                            # Try to interpret as JSON
                            value = json.loads(raw_value)
                            value = f"{json.dumps(value)[:80]}..." if len(json.dumps(value)) > 80 else json.dumps(value)
                        except (json.JSONDecodeError, UnicodeDecodeError):
                            # Try to interpret as float/number for prices
                            try:
                                value = float(raw_value)
                            except (ValueError, UnicodeDecodeError):
                                # Fall back to string representation
                                value = f"{raw_value}"
                elif key_type == "hash":
                    value = f"Hash with {self.redis.hlen(key)} fields"
                elif key_type == "list":
                    value = f"List with {self.redis.llen(key)} items"
                elif key_type == "set":
                    value = f"Set with {self.redis.scard(key)} members"
                elif key_type == "zset":
                    value = f"Sorted set with {self.redis.zcard(key)} members"
            except Exception as e:
                value = f"Error reading value: {e}"
                
            # Check if value changed
            changed = False
            if key_str in self.previous_values:
                if str(self.previous_values[key_str]) != str(value):
                    changed = True
                    self.update_counts[key_str] += 1
                    self.last_updated[key_str] = datetime.datetime.now()
            else:
                self.previous_values[key_str] = value
                self.last_updated[key_str] = datetime.datetime.now()
                
            result.append({
                "key": key_str,
                "type": key_type,
                "ttl": ttl_str,
                "value": value,
                "changed": changed,
                "updates": self.update_counts.get(key_str, 0),
                "last_update": self.last_updated.get(key_str)
            })
            
            # Save current value for next comparison
            self.previous_values[key_str] = value
            
        return sorted(result, key=lambda k: k['key'])
    
    def get_server_stats(self):
        """Get Redis server statistics"""
        info = self.redis.info()
        
        # Extract the most important metrics
        stats = {
            "version": info.get("redis_version", "Unknown"),
            "uptime": f"{info.get('uptime_in_seconds', 0) // 86400}d {(info.get('uptime_in_seconds', 0) % 86400) // 3600}h {(info.get('uptime_in_seconds', 0) % 3600) // 60}m",
            "connected_clients": info.get("connected_clients", 0),
            "used_memory_human": info.get("used_memory_human", "Unknown"),
            "used_memory_peak_human": info.get("used_memory_peak_human", "Unknown"),
            "mem_fragmentation_ratio": info.get("mem_fragmentation_ratio", 0),
            "total_commands_processed": info.get("total_commands_processed", 0),
            "instantaneous_ops_per_sec": info.get("instantaneous_ops_per_sec", 0),
            "rejected_connections": info.get("rejected_connections", 0),
            "expired_keys": info.get("expired_keys", 0),
            "evicted_keys": info.get("evicted_keys", 0),
            "keyspace_hits": info.get("keyspace_hits", 0),
            "keyspace_misses": info.get("keyspace_misses", 0),
            "hit_rate": info.get("keyspace_hits", 0) / (info.get("keyspace_hits", 0) + info.get("keyspace_misses", 1)) * 100
        }
        
        # Get database stats
        db_stats = {}
        for db_name, db_info in info.items():
            if db_name.startswith("db"):
                db_stats[db_name] = db_info
                
        stats["databases"] = db_stats
        return stats
    
    def display_key_monitoring(self):
        """Display key monitoring section"""
        # Get BTC price keys
        price_keys = self.get_key_info("*btc*price*") + self.get_key_info("*price*")
        price_keys = [k for k in price_keys if any(pk in k['key'] for pk in PRICE_KEYS)]
        
        # Get other important keys
        health_keys = []
        for pattern in HEALTH_KEYS:
            health_keys.extend(self.get_key_info(f"*{pattern}*"))
        
        # Get custom pattern keys if specified
        pattern_keys = []
        if self.watch_pattern != "*":
            pattern_keys = self.get_key_info(self.watch_pattern)
        
        # Clean the terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Display current time
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{BOLD}{BLUE}═══ OmegaBTC Redis Monitor ═══ {now} ═══{RESET}\n")
        
        # Display BTC price keys
        if price_keys:
            print(f"\n{BOLD}{GREEN}■ BTC Price Tracking Keys{RESET}")
            print(f"{'Key':<30} {'Type':<8} {'TTL':<15} {'Updates':<8} {'Last Update':<20} {'Value'}")
            print("─" * 100)
            
            for key in price_keys:
                # Color the changed values
                value_color = RED if key["changed"] else RESET
                key_name = key["key"]
                
                # Format the last update time
                last_update = key.get("last_update", None)
                if last_update:
                    time_diff = (datetime.datetime.now() - last_update).total_seconds()
                    if time_diff < 5:
                        update_str = f"{GREEN}{last_update.strftime('%H:%M:%S')}{RESET}"
                    elif time_diff < 30:
                        update_str = f"{YELLOW}{last_update.strftime('%H:%M:%S')}{RESET}"
                    else:
                        update_str = f"{RED}{last_update.strftime('%H:%M:%S')}{RESET}"
                else:
                    update_str = "Never"
                    
                print(f"{key_name:<30} {key['type']:<8} {key['ttl']:<15} {key['updates']:<8} {update_str:<20} {value_color}{key['value']}{RESET}")
        
        # Display health monitoring keys
        if health_keys:
            print(f"\n{BOLD}{MAGENTA}■ System Health Keys{RESET}")
            print(f"{'Key':<30} {'Type':<8} {'TTL':<15} {'Updates':<8} {'Last Update':<20} {'Value'}")
            print("─" * 100)
            
            for key in health_keys:
                value_color = RED if key["changed"] else RESET
                key_name = key["key"]
                
                # Format the last update time
                last_update = key.get("last_update", None)
                if last_update:
                    time_diff = (datetime.datetime.now() - last_update).total_seconds()
                    if time_diff < 5:
                        update_str = f"{GREEN}{last_update.strftime('%H:%M:%S')}{RESET}"
                    elif time_diff < 30:
                        update_str = f"{YELLOW}{last_update.strftime('%H:%M:%S')}{RESET}"
                    else:
                        update_str = f"{RED}{last_update.strftime('%H:%M:%S')}{RESET}"
                else:
                    update_str = "Never"
                    
                print(f"{key_name:<30} {key['type']:<8} {key['ttl']:<15} {key['updates']:<8} {update_str:<20} {value_color}{key['value']}{RESET}")
        
        # Display custom pattern keys
        if pattern_keys:
            print(f"\n{BOLD}{CYAN}■ Custom Pattern Keys ({self.watch_pattern}){RESET}")
            print(f"{'Key':<30} {'Type':<8} {'TTL':<15} {'Updates':<8} {'Last Update':<20} {'Value'}")
            print("─" * 100)
            
            for key in pattern_keys:
                value_color = RED if key["changed"] else RESET
                key_name = key["key"]
                
                # Format the last update time
                last_update = key.get("last_update", None)
                if last_update:
                    time_diff = (datetime.datetime.now() - last_update).total_seconds()
                    if time_diff < 5:
                        update_str = f"{GREEN}{last_update.strftime('%H:%M:%S')}{RESET}"
                    elif time_diff < 30:
                        update_str = f"{YELLOW}{last_update.strftime('%H:%M:%S')}{RESET}"
                    else:
                        update_str = f"{RED}{last_update.strftime('%H:%M:%S')}{RESET}"
                else:
                    update_str = "Never"
                    
                print(f"{key_name:<30} {key['type']:<8} {key['ttl']:<15} {key['updates']:<8} {update_str:<20} {value_color}{key['value']}{RESET}")
    
    def display_queue_monitoring(self):
        """Display queue monitoring section"""
        queue_keys = []
        
        # Collect all queue keys
        for pattern in QUEUE_KEYS:
            queue_keys.extend(self.get_key_info(pattern))
        
        # Filter to only include list and sorted set types
        queue_keys = [k for k in queue_keys if k['type'] in ['list', 'zset']]
        
        if queue_keys:
            print(f"\n{BOLD}{CYAN}■ Queue Status{RESET}")
            print(f"{'Queue Name':<40} {'Type':<8} {'Size':<8} {'Rate (/min)':<12} {'Last Update':<20}")
            print("─" * 100)
            
            for key in queue_keys:
                key_name = key["key"]
                key_type = key["type"]
                
                # Get queue size
                if key_type == "list":
                    size = self.redis.llen(key_name)
                elif key_type == "zset":
                    size = self.redis.zcard(key_name)
                else:
                    size = 0
                    
                # Calculate processing rate (items per minute)
                rate = "N/A"
                if key_name in self.previous_values and "size" in self.previous_values[key_name]:
                    prev_size = self.previous_values[key_name]["size"]
                    prev_time = self.previous_values[key_name]["time"]
                    current_time = datetime.datetime.now()
                    
                    # Calculate time difference in minutes
                    time_diff = (current_time - prev_time).total_seconds() / 60.0
                    if time_diff > 0:
                        # If size decreased, items were processed
                        if size < prev_size:
                            rate = f"{(prev_size - size) / time_diff:.1f}"
                        # If size increased, items were added
                        elif size > prev_size:
                            rate = f"+{(size - prev_size) / time_diff:.1f}"
                        else:
                            rate = "0.0"
                
                # Store current size and time for next comparison
                self.previous_values[key_name] = {
                    "size": size,
                    "time": datetime.datetime.now()
                }
                
                # Format the last update time
                last_update = key.get("last_update", datetime.datetime.now())
                time_diff = (datetime.datetime.now() - last_update).total_seconds()
                if time_diff < 5:
                    update_str = f"{GREEN}{last_update.strftime('%H:%M:%S')}{RESET}"
                elif time_diff < 30:
                    update_str = f"{YELLOW}{last_update.strftime('%H:%M:%S')}{RESET}"
                else:
                    update_str = f"{RED}{last_update.strftime('%H:%M:%S')}{RESET}"
                
                # Color-code queue size based on magnitude
                if size == 0:
                    size_str = f"{GREEN}{size}{RESET}"
                elif size < 10:
                    size_str = f"{YELLOW}{size}{RESET}"
                else:
                    size_str = f"{RED}{size}{RESET}"
                    
                print(f"{key_name:<40} {key_type:<8} {size_str:<8} {rate:<12} {update_str:<20}")
                
            # Add worker information if using RQ
            try:
                workers = self.redis.smembers("rq:workers")
                if workers:
                    print(f"\n{BOLD}{YELLOW}▶ Active Workers ({len(workers)}){RESET}")
                    for i, worker in enumerate(workers):
                        worker_name = worker.decode('utf-8')
                        state = self.redis.get(f"rq:worker:{worker_name}")
                        state_str = state.decode('utf-8') if state else "Unknown"
                        print(f"Worker {i+1}: {worker_name} - Status: {state_str}")
            except Exception:
                pass
    
    def display_server_stats(self):
        """Display Redis server statistics"""
        stats = self.get_server_stats()
        
        print(f"\n{BOLD}{BLUE}■ Redis Server Statistics{RESET}")
        print(f"Redis Version: {stats['version']}")
        print(f"Uptime: {stats['uptime']}")
        print(f"Connected Clients: {stats['connected_clients']}")
        
        # Memory usage
        print(f"\n{BOLD}{YELLOW}▶ Memory Usage{RESET}")
        print(f"Used Memory: {stats['used_memory_human']}")
        print(f"Peak Memory: {stats['used_memory_peak_human']}")
        print(f"Fragmentation Ratio: {stats['mem_fragmentation_ratio']:.2f}")
        
        # Performance metrics
        print(f"\n{BOLD}{GREEN}▶ Performance Metrics{RESET}")
        print(f"Commands Processed: {stats['total_commands_processed']}")
        print(f"Operations/sec: {stats['instantaneous_ops_per_sec']}")
        print(f"Keyspace Hit Rate: {stats['hit_rate']:.2f}%")
        
        # Warning indicators
        print(f"\n{BOLD}{RED}▶ Warning Indicators{RESET}")
        print(f"Rejected Connections: {stats['rejected_connections']}")
        print(f"Expired Keys: {stats['expired_keys']}")
        print(f"Evicted Keys: {stats['evicted_keys']}")
        
        # Database stats
        print(f"\n{BOLD}{MAGENTA}▶ Database Statistics{RESET}")
        for db_name, db_info in stats["databases"].items():
            print(f"{db_name}: Keys={db_info.get('keys', 0)}, Expires={db_info.get('expires', 0)}")
    
    def run(self, show_keys=True, show_stats=True, show_queues=True):
        """Run the Redis monitor"""
        while self.running:
            if show_keys:
                self.display_key_monitoring()
            
            if show_queues:
                self.display_queue_monitoring()
            
            if show_stats:
                self.display_server_stats()
            
            print(f"\n{YELLOW}Press Ctrl+C to quit. Updating every {self.update_interval} seconds...{RESET}")
            
            try:
                time.sleep(self.update_interval)
            except KeyboardInterrupt:
                self.running = False
                break

def main():
    parser = argparse.ArgumentParser(description="OmegaBTC Redis Monitor")
    parser.add_argument("--keys-only", action="store_true", help="Only show key monitoring")
    parser.add_argument("--stats-only", action="store_true", help="Only show Redis server statistics")
    parser.add_argument("--queues-only", action="store_true", help="Only show queue monitoring")
    parser.add_argument("--watch", default="*", help="Watch specific key pattern (e.g. *btc* or last_*)")
    parser.add_argument("--interval", type=float, default=2.0, help="Update interval in seconds")
    
    args = parser.parse_args()
    
    # Determine what to show
    show_keys = True
    show_stats = True
    show_queues = True
    
    if args.keys_only:
        show_stats = False
        show_queues = False
    if args.stats_only:
        show_keys = False
        show_queues = False
    if args.queues_only:
        show_keys = False
        show_stats = False
    
    try:
        monitor = RedisMonitor(watch_pattern=args.watch, update_interval=args.interval)
        monitor.run(show_keys=show_keys, show_stats=show_stats, show_queues=show_queues)
    except redis.ConnectionError:
        print(f"{RED}Error: Could not connect to Redis at {REDIS_HOST}:{REDIS_PORT}{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()