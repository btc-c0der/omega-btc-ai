#!/usr/bin/env python3

"""
OMEGA BTC AI - DIVINE REDIS TRAP MONITOR
=======================================

JAH BLESS THE TRAP DETECTION SYSTEM!

This tool monitors Redis for new market maker trap entries and sends alerts
via Telegram, Discord, and email when new traps are detected.

Usage:
    python redis_trap_monitor.py [options]

Options:
    --interval=SECS   Check interval in seconds (default: 10)
    --backfill=MINS   Process traps from last N minutes on startup (default: 60)
    --verbose         Show detailed output
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

# Import the alert system
from omega_ai.alerts.alerts_orchestrator import send_alert
from omega_ai.alerts.rasta_vibes import RastaVibes

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

# Redis connection parameters
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

class RedisTrapMonitor:
    """Divine Redis Trap Monitor for OMEGA BTC AI."""
    
    def __init__(self, check_interval=10, backfill_minutes=60, verbose=False):
        """Initialize the trap monitor."""
        self.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
        self.check_interval = check_interval
        self.backfill_minutes = backfill_minutes
        self.verbose = verbose
        self.processed_traps = set()
        self.running = True
        self.trap_count = 0
        
        # Set up signal handlers for graceful termination
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)
        
        self.log_message(f"{BOLD}{GREEN}OMEGA BTC AI - DIVINE TRAP MONITOR INITIALIZED{RESET}")
        self.log_message(f"Check interval: {check_interval} seconds")
        self.log_message(f"Backfill period: {backfill_minutes} minutes")
        
    def handle_signal(self, sig, frame):
        """Handle termination signals gracefully."""
        self.log_message(f"\n{YELLOW}Shutting down Trap Monitor... JAH BLESS!{RESET}")
        self.running = False
    
    def log_message(self, message):
        """Log a message with timestamp."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def debug_log(self, message):
        """Log debug messages only in verbose mode."""
        if self.verbose:
            self.log_message(f"{BLUE}DEBUG: {message}{RESET}")
    
    def get_trap_timestamp(self, key):
        """Extract timestamp from trap key."""
        try:
            # Extract timestamp from key format like "mm_trap:1647582489"
            parts = key.split(":")
            if len(parts) >= 2:
                timestamp = int(parts[1])
                return datetime.datetime.fromtimestamp(timestamp)
        except (ValueError, IndexError):
            pass
        return None
    
    def is_recent_trap(self, key, cutoff_time):
        """Check if trap is more recent than cutoff time."""
        trap_time = self.get_trap_timestamp(key)
        if trap_time:
            return trap_time >= cutoff_time
        return False
    
    def find_new_traps(self):
        """Find new market maker traps in Redis."""
        try:
            # Scan for mm_trap keys
            cursor = 0
            new_traps = []
            
            while True:
                cursor, keys = self.redis.scan(cursor, match="mm_trap:*", count=100)
                
                for key in keys:
                    # Skip already processed traps
                    if key in self.processed_traps:
                        continue
                    
                    # Get trap data
                    trap_data = self.redis.hgetall(key)
                    
                    if trap_data:
                        self.debug_log(f"Found potential new trap: {key}")
                        new_traps.append((key, trap_data))
                    
                    # Mark as processed
                    self.processed_traps.add(key)
                
                if cursor == 0:
                    break
            
            return new_traps
        
        except Exception as e:
            self.log_message(f"{RED}Error finding traps: {e}{RESET}")
            return []
    
    def process_trap(self, key, trap_data):
        """Process and send alert for a trap."""
        try:
            # Extract trap information
            trap_type = trap_data.get("type", "Unknown Trap")
            confidence = float(trap_data.get("confidence", 0))
            price = float(trap_data.get("price", 0))
            change = float(trap_data.get("change", 0))
            timestamp = trap_data.get("timestamp", "Unknown")
            
            # Format the basic alert message (without Rasta vibes - those will be added by send_alert)
            alert_message = f"""MARKET MAKER TRAP DETECTED!

→ Type: {trap_type}
→ BTC Price: ${price:,.2f}
→ Price Change: {change:.2%}
→ Confidence: {confidence:.2f}
→ Time: {timestamp}

OMEGA BTC AI - Divine Detection System"""

            # Send the alert with appropriate trap type
            self.log_message(f"{MAGENTA}Sending alert for {trap_type} (${price:,.2f}, {change:.2%}){RESET}")
            send_alert(alert_message, trap_type)
            
            self.trap_count += 1
            self.log_message(f"{GREEN}✓ Alert sent successfully! Total alerts sent: {self.trap_count}{RESET}")
            return True
            
        except Exception as e:
            self.log_message(f"{RED}Error processing trap: {e}{RESET}")
            return False
    
    def perform_backfill(self):
        """Process recent traps for backfilling at startup."""
        self.log_message(f"{YELLOW}Performing backfill for last {self.backfill_minutes} minutes...{RESET}")
        
        # Calculate cutoff time
        cutoff_time = datetime.datetime.now() - datetime.timedelta(minutes=self.backfill_minutes)
        
        # Scan for mm_trap keys
        cursor = 0
        backfill_count = 0
        
        while True:
            cursor, keys = self.redis.scan(cursor, match="mm_trap:*", count=100)
            
            for key in keys:
                # Check if trap is recent enough
                if self.is_recent_trap(key, cutoff_time):
                    # Get trap data
                    trap_data = self.redis.hgetall(key)
                    
                    if trap_data:
                        self.processed_traps.add(key)
                        backfill_count += 1
                        
                        # Only process backfilled traps if verbose is True
                        if self.verbose:
                            self.process_trap(key, trap_data)
                else:
                    # Add to processed set so we don't process this trap again
                    self.processed_traps.add(key)
            
            if cursor == 0:
                break
        
        self.log_message(f"{YELLOW}Backfill complete - {backfill_count} traps processed{RESET}")
    
    def display_status(self):
        """Display monitor status."""
        os.system('cls' if os.name == 'nt' else 'clear')
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"{BOLD}{BLUE}═══ OMEGA BTC AI TRAP MONITOR ═══ {now} ═══{RESET}\n")
        print(f"{GREEN}🌿 JAH BLESS THE DIVINE TRAP DETECTION! 🌿{RESET}\n")
        print(f"Monitoring status: {GREEN}ACTIVE{RESET}")
        print(f"Traps processed: {self.trap_count}")
        print(f"Known trap keys: {len(self.processed_traps)}")
        print(f"Check interval: Every {self.check_interval} seconds")
        
        # Display the 5 most recent traps
        recent_traps = []
        for key in sorted(self.processed_traps, reverse=True)[:5]:
            try:
                trap_data = self.redis.hgetall(key)
                if trap_data:
                    recent_traps.append((key, trap_data))
            except:
                pass
        
        if recent_traps:
            print(f"\n{BOLD}{YELLOW}Recent Traps:{RESET}")
            for key, trap in recent_traps:
                trap_time = self.get_trap_timestamp(key)
                trap_type = trap.get("type", "Unknown")
                price = float(trap.get("price", 0))
                confidence = float(trap.get("confidence", 0))
                print(f"• [{trap_time.strftime('%Y-%m-%d %H:%M:%S')}] {trap_type} (${price:,.2f}, {confidence:.2f} confidence)")
        
        print(f"\n{YELLOW}Press Ctrl+C to stop monitoring{RESET}")
    
    def run(self):
        """Run the trap monitor main loop."""
        # Perform backfill of recent traps first
        self.perform_backfill()
        
        # Main monitoring loop
        last_status_update = 0
        while self.running:
            try:
                current_time = time.time()
                
                # Find and process new traps
                new_traps = self.find_new_traps()
                for key, trap_data in new_traps:
                    self.process_trap(key, trap_data)
                
                # Update status display every 5 seconds
                if current_time - last_status_update >= 5:
                    self.display_status()
                    last_status_update = current_time
                
                # Sleep until next check
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                self.running = False
                break
            except Exception as e:
                self.log_message(f"{RED}Error in monitor loop: {e}{RESET}")
                time.sleep(self.check_interval)
        
        self.log_message(f"{GREEN}Monitor stopped after processing {self.trap_count} traps.{RESET}")
        self.log_message(f"{GREEN}JAH BLESS THE DIVINE MONITORING SYSTEM! 🌿{RESET}")

def main():
    """Main entry point for the trap monitor."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="OMEGA BTC AI - Divine Redis Trap Monitor")
    parser.add_argument("--interval", type=int, default=10, help="Check interval in seconds")
    parser.add_argument("--backfill", type=int, default=60, help="Process traps from last N minutes")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    # Start monitoring
    try:
        monitor = RedisTrapMonitor(
            check_interval=args.interval,
            backfill_minutes=args.backfill,
            verbose=args.verbose
        )
        monitor.run()
    except redis.ConnectionError:
        print(f"{RED}Error: Could not connect to Redis at {REDIS_HOST}:{REDIS_PORT}{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()