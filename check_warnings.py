#!/usr/bin/env python3
"""
OMEGA BTC AI - System Warnings Checker
-------------------------------------
Tool to check system warnings stored in Redis.

Usage:
    python check_warnings.py               # Show all warnings (latest 10)
    python check_warnings.py --all         # Show all warnings
    python check_warnings.py --type TYPE   # Show warnings of specific type
    python check_warnings.py --count       # Show warning counts by type
    python check_warnings.py --clear       # Clear all warnings (keeps counts)
    python check_warnings.py --reset       # Reset warning counts
"""

import redis
import json
import argparse
import os
from datetime import datetime
from tabulate import tabulate

# Terminal colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"
BOLD = "\033[1m"

def connect_to_redis():
    """Connect to Redis."""
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    
    try:
        r = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)
        r.ping()  # Test connection
        return r
    except redis.ConnectionError as e:
        print(f"{RED}Failed to connect to Redis: {e}{RESET}")
        exit(1)

def get_warnings(r, warning_type=None, limit=10):
    """Get warnings from Redis."""
    try:
        if warning_type:
            warnings = r.lrange(f"system:warnings:{warning_type}", 0, limit - 1)
            total = r.llen(f"system:warnings:{warning_type}")
        else:
            warnings = r.lrange("system:warnings", 0, limit - 1)
            total = r.llen("system:warnings")
        
        # Parse warnings
        parsed_warnings = []
        for w in warnings:
            try:
                warning_data = json.loads(w)
                parsed_warnings.append(warning_data)
            except:
                continue
                
        return parsed_warnings, total
    except Exception as e:
        print(f"{RED}Error retrieving warnings: {e}{RESET}")
        return [], 0

def get_warning_counts(r):
    """Get warning counts by type."""
    try:
        return r.hgetall("system:warning_counts")
    except Exception as e:
        print(f"{RED}Error retrieving warning counts: {e}{RESET}")
        return {}

def clear_warnings(r):
    """Clear all warnings but keep counts."""
    try:
        warning_types = []
        for key in r.keys("system:warnings:*"):
            if key != "system:warning_counts":
                warning_types.append(key)
        
        # Delete all warning lists
        if warning_types:
            r.delete("system:warnings", *warning_types)
            print(f"{GREEN}Successfully cleared {len(warning_types)} warning types{RESET}")
        else:
            print(f"{YELLOW}No warnings to clear{RESET}")
    except Exception as e:
        print(f"{RED}Error clearing warnings: {e}{RESET}")

def reset_counts(r):
    """Reset warning counts."""
    try:
        r.delete("system:warning_counts")
        print(f"{GREEN}Successfully reset warning counts{RESET}")
    except Exception as e:
        print(f"{RED}Error resetting warning counts: {e}{RESET}")

def format_timestamp(timestamp):
    """Format ISO timestamp to readable format."""
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp

def main():
    parser = argparse.ArgumentParser(description="OMEGA BTC AI - System Warnings Checker")
    parser.add_argument("--type", help="Show warnings of specific type")
    parser.add_argument("--all", action="store_true", help="Show all warnings")
    parser.add_argument("--count", action="store_true", help="Show warning counts by type")
    parser.add_argument("--clear", action="store_true", help="Clear all warnings")
    parser.add_argument("--reset", action="store_true", help="Reset warning counts")
    
    args = parser.parse_args()
    
    # Connect to Redis
    r = connect_to_redis()
    
    # Handle commands
    if args.clear:
        clear_warnings(r)
        return
    
    if args.reset:
        reset_counts(r)
        return
    
    if args.count:
        counts = get_warning_counts(r)
        if counts:
            print(f"\n{CYAN}{BOLD}WARNING COUNTS BY TYPE{RESET}")
            table = [[MAGENTA + type + RESET, GREEN + str(count) + RESET] for type, count in counts.items()]
            print(tabulate(table, headers=[BOLD + "Warning Type" + RESET, BOLD + "Count" + RESET]))
        else:
            print(f"{YELLOW}No warning counts available{RESET}")
        return
    
    # Get warnings
    limit = 1000 if args.all else 10
    warnings, total = get_warnings(r, args.type, limit)
    
    if not warnings:
        print(f"{YELLOW}No warnings found{RESET}")
        return
    
    # Display warnings
    filter_text = f" of type {MAGENTA}{args.type}{RESET}" if args.type else ""
    limit_text = "" if args.all else f" (showing latest {limit}, total: {total})"
    print(f"\n{CYAN}{BOLD}SYSTEM WARNINGS{filter_text}{limit_text}{RESET}")
    
    table = []
    for w in warnings:
        source = w.get("source", "unknown")
        msg = w.get("message", "No message")
        timestamp = format_timestamp(w.get("timestamp", "unknown"))
        w_type = w.get("type", "unknown")
        
        row = [
            BLUE + timestamp + RESET,
            MAGENTA + w_type + RESET,
            YELLOW + source + RESET,
            msg
        ]
        table.append(row)
    
    print(tabulate(table, headers=[BOLD + "Timestamp" + RESET, BOLD + "Type" + RESET, 
                                    BOLD + "Source" + RESET, BOLD + "Message" + RESET]))

if __name__ == "__main__":
    main() 