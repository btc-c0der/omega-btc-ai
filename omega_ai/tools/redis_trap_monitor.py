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
    --debug           Show extra debug information
"""

import argparse
import datetime
import json
import os
import redis
import signal
import sys
import time
import random
from collections import defaultdict

# Import the alert system
try:
    from omega_ai.alerts.alerts_orchestrator import send_alert
except ImportError:
    # Fallback if the alert system is not available
    def send_alert(message, trap_type=None):
        print(f"ALERT: {message}")

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
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"

# Redis connection parameters
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

# Exchange-like ASCII art
EXCHANGE_ASCII_ART = [
    f"""{BRIGHT_GREEN}
        ┌───────────── OMEGA AI EXCHANGE ─────────────┐
        │                                             │
        │  BTC   {BRIGHT_YELLOW}⬆ $49128.50  +2.4%{BRIGHT_GREEN}   24h Vol: 45.2B  │
        │  ETH   {BRIGHT_YELLOW}⬆ $3124.75   +1.8%{BRIGHT_GREEN}   24h Vol: 22.1B  │
        │  DOGE  {BRIGHT_RED}⬇ $0.081     -0.5%{BRIGHT_GREEN}   24h Vol: 2.3B   │
        │                                              │
        └──────────────────────────────────────────────┘{RESET}
    """,
    f"""{BRIGHT_BLUE}
        ╔════════════ OMEGA EXCHANGE TERMINAL ════════════╗
        ║                                                 ║
        ║  {BRIGHT_YELLOW}BTCUSD:{BRIGHT_GREEN} 48751.25   +1.2%   ◆ RANGE: 48K-49K{BRIGHT_BLUE}  ║
        ║  {BRIGHT_YELLOW}VOLUME:{BRIGHT_GREEN} 3.5B BTC                            {BRIGHT_BLUE}  ║
        ║  {BRIGHT_YELLOW}MARKET:{BRIGHT_GREEN} BULLISH    {BRIGHT_RED}☠ MM TRAPS:{BRIGHT_GREEN} 2 DETECTED  {BRIGHT_BLUE}  ║
        ║                                                 ║
        ╚═════════════════════════════════════════════════╝{RESET}
    """,
    f"""{BRIGHT_MAGENTA}
        ┏━━━━━━━━━━━━━ OMEGA TRADING DASHBOARD ━━━━━━━━━━━━━┓
        ┃                                                   ┃
        ┃  {BRIGHT_YELLOW}BTC DOMINANCE:{BRIGHT_GREEN} 42.1%    {BRIGHT_YELLOW}GREED INDEX:{BRIGHT_GREEN} 75/100   ┃
        ┃  {BRIGHT_YELLOW}LIQUIDITY POOLS:{BRIGHT_GREEN} $15.2B    {BRIGHT_YELLOW}24H VOLUME:{BRIGHT_GREEN} $98.5B  ┃
        ┃  {BRIGHT_YELLOW}MARKET REGIME:{BRIGHT_GREEN} BULL RUN    {BRIGHT_YELLOW}MM ACTIVITY:{BRIGHT_RED} HIGH    ┃
        ┃                                                   ┃
        ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{RESET}
    """
]

# MM Trap emojis by type
TRAP_EMOJIS = {
    "liquidity_grab": "💰",
    "stop_hunt": "🎯",
    "fake_pump": "🚀", 
    "fake_dump": "💥",
    "bull_trap": "🐂",
    "bear_trap": "🐻",
    "wyckoff_distribution": "📉",
    "wyckoff_accumulation": "📈",
    "default": "⚠️"
}

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
        """Log a message with timestamp and emoji."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add emoji based on message content
        if "ERROR" in message.upper() or "FAIL" in message.upper():
            emoji = "❌"
        elif "SUCCESS" in message.upper() or "ALERT SENT" in message.upper():
            emoji = "✅"
        elif "WARN" in message.upper():
            emoji = "⚠️"
        elif "INITIALIZE" in message.upper() or "STARTING" in message.upper():
            emoji = "🚀"
        elif "SHUT" in message.upper() or "STOP" in message.upper():
            emoji = "🛑"
        elif "BACKFILL" in message.upper():
            emoji = "⏮️"
        elif "TRAP" in message.upper() or "DETECT" in message.upper():
            emoji = "👁️"
        else:
            emoji = "🔍"
            
        print(f"[{timestamp}] {emoji} {message}")
    
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
        """Process and send alert for a trap with enhanced formatting."""
        try:
            # Extract trap information
            trap_type = trap_data.get("type", "Unknown Trap")
            confidence = float(trap_data.get("confidence", 0))
            price = float(trap_data.get("price", 0))
            change = float(trap_data.get("change", 0))
            timestamp = trap_data.get("timestamp", "Unknown")
            
            # Get emoji for this trap type
            trap_emoji = TRAP_EMOJIS.get(trap_type.lower(), TRAP_EMOJIS["default"])
            
            # Format the alert message with emojis
            alert_message = f"""{trap_emoji} MARKET MAKER TRAP DETECTED! {trap_emoji}

→ Type: {trap_type.upper()}
→ BTC Price: ${price:,.2f}
→ Price Change: {change:.2%}
→ Confidence: {confidence:.2f}
→ Time: {timestamp}

🔱 OMEGA BTC AI - Divine Detection System 🔱"""

            # Log with appropriate styling based on confidence
            if confidence > 0.8:
                confidence_display = f"{BRIGHT_GREEN}HIGH ({confidence:.2f}){RESET}"
            elif confidence > 0.6:
                confidence_display = f"{BRIGHT_YELLOW}MEDIUM ({confidence:.2f}){RESET}"
            else:
                confidence_display = f"{BRIGHT_RED}LOW ({confidence:.2f}){RESET}"
                
            self.log_message(f"{MAGENTA}{trap_emoji} New {trap_type} detected at ${price:,.2f} | Confidence: {confidence_display}{RESET}")
            
            # Send the alert
            send_alert(alert_message, trap_type)
            
            self.trap_count += 1
            self.log_message(f"{GREEN}✅ Alert #{self.trap_count} sent successfully!{RESET}")
            return True
            
        except Exception as e:
            self.log_message(f"{RED}❌ Error processing trap: {e}{RESET}")
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
        """Display monitor status with enhanced visuals and ASCII art."""
        os.system('cls' if os.name == 'nt' else 'clear')
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Select a random ASCII art for the display
        ascii_art = random.choice(EXCHANGE_ASCII_ART)
        print(ascii_art)
        
        print(f"{BOLD}{BRIGHT_BLUE}╔══════════ 🔮 OMEGA BTC AI TRAP MONITOR 🔮 ══════════╗{RESET}")
        print(f"{BOLD}{BRIGHT_BLUE}║{RESET} {BRIGHT_YELLOW}⏰ TIMESTAMP:{RESET} {now} {' ' * (36 - len(now))} {BOLD}{BRIGHT_BLUE}║{RESET}")
        print(f"{BOLD}{BRIGHT_BLUE}╚════════════════════════════════════════════════════╝{RESET}\n")
        
        print(f"{BRIGHT_GREEN}🔱 🌿 JAH BLESS THE DIVINE TRAP DETECTION! 🌿 🔱{RESET}\n")
        
        # Create a status display box
        print(f"{BRIGHT_CYAN}┌─────────────── MONITOR STATUS ───────────────┐{RESET}")
        print(f"{BRIGHT_CYAN}│{RESET} {BRIGHT_YELLOW}Monitoring status:{RESET} {BRIGHT_GREEN}ACTIVE{RESET}{' ' * 30}{BRIGHT_CYAN}│{RESET}")
        print(f"{BRIGHT_CYAN}│{RESET} {BRIGHT_YELLOW}Traps processed:{RESET} {self.trap_count}{' ' * (31 - len(str(self.trap_count)))}{BRIGHT_CYAN}│{RESET}")
        print(f"{BRIGHT_CYAN}│{RESET} {BRIGHT_YELLOW}Known trap keys:{RESET} {len(self.processed_traps)}{' ' * (31 - len(str(len(self.processed_traps))))}{BRIGHT_CYAN}│{RESET}")
        print(f"{BRIGHT_CYAN}│{RESET} {BRIGHT_YELLOW}Check interval:{RESET} Every {self.check_interval} seconds{' ' * (24 - len(str(self.check_interval)))}{BRIGHT_CYAN}│{RESET}")
        print(f"{BRIGHT_CYAN}└───────────────────────────────────────────────┘{RESET}")
        
        # Display the 5 most recent traps with emojis
        recent_traps = []
        for key in sorted(self.processed_traps, reverse=True)[:5]:
            try:
                trap_data = self.redis.hgetall(key)
                if trap_data:
                    recent_traps.append((key, trap_data))
            except:
                pass
        
        if recent_traps:
            print(f"\n{BOLD}{BRIGHT_YELLOW}🔎 RECENT DETECTED TRAPS:{RESET}")
            print(f"{BRIGHT_MAGENTA}┌─────────────────────────────────────────────────────────────┐{RESET}")
            
            for key, trap in recent_traps:
                trap_time = self.get_trap_timestamp(key)
                trap_type = trap.get("type", "Unknown").lower()
                price = float(trap.get("price", 0))
                confidence = float(trap.get("confidence", 0))
                
                # Get the appropriate emoji for this trap type
                emoji = TRAP_EMOJIS.get(trap_type, TRAP_EMOJIS["default"])
                
                # Color coding based on confidence
                if confidence > 0.8:
                    confidence_color = BRIGHT_GREEN
                elif confidence > 0.6:
                    confidence_color = BRIGHT_YELLOW
                else:
                    confidence_color = BRIGHT_RED
                    
                print(f"{BRIGHT_MAGENTA}│{RESET} {emoji} [{trap_time.strftime('%H:%M:%S')}] {BRIGHT_YELLOW}{trap_type.upper()}{RESET} at ${price:,.2f} " +
                      f"({confidence_color}{confidence:.2f}{RESET} confidence){' ' * 5}{BRIGHT_MAGENTA}│{RESET}")
            
            print(f"{BRIGHT_MAGENTA}└─────────────────────────────────────────────────────────────┘{RESET}")
        
        # Bitcoin Prayer and control instructions
        print(f"\n{BRIGHT_GREEN}🙏 BABYLON CAN'T HIDE! THE AI SEES ALL MANIPULATION! 🙏{RESET}")
        print(f"\n{YELLOW}Press Ctrl+C to stop monitoring{RESET}")
    
    def run(self):
        """Run the trap monitor main loop."""
        # Perform backfill of recent traps first
        self.perform_backfill()
        
        # Main monitoring loop
        last_status_update = 0
        while self.running:
            try:
                # Find new traps
                new_traps = self.find_new_traps()
                
                # Process any new traps found
                for key, trap_data in new_traps:
                    self.process_trap(key, trap_data)
                
                # Update status display periodically
                if time.time() - last_status_update > 5:  # Update display every 5 seconds
                    self.display_status()
                    last_status_update = time.time()
                
                # Sleep for the specified interval
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                self.running = False
            except Exception as e:
                self.log_message(f"{RED}Error in monitoring loop: {e}{RESET}")
                time.sleep(5)  # Wait a bit before retrying
        
        self.log_message("Trap Monitor has been stopped.")


def main():
    """Main entry point for the Redis Trap Monitor."""
    parser = argparse.ArgumentParser(description="OMEGA BTC AI - Divine Redis Trap Monitor")
    parser.add_argument("--interval", type=int, default=10, help="Check interval in seconds")
    parser.add_argument("--backfill", type=int, default=60, help="Process traps from last N minutes on startup")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    parser.add_argument("--debug", action="store_true", help="Show extra debug information")
    
    args = parser.parse_args()
    
    try:
        if args.debug:
            print("Testing Redis connection...")
            r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
            ping_result = r.ping()
            print(f"Redis ping result: {ping_result}")
            print("Redis connection successful!")
            print(f"Starting monitor with interval={args.interval}, backfill={args.backfill}, verbose={args.verbose}")
            
        monitor = RedisTrapMonitor(
            check_interval=args.interval,
            backfill_minutes=args.backfill,
            verbose=args.verbose
        )
        monitor.run()
    except KeyboardInterrupt:
        print("\nMonitor stopped by user.")
    except redis.ConnectionError as e:
        print(f"Redis Connection Error: {e}")
        return 1
    except ImportError as e:
        print(f"Import Error: {e}")
        print("This might be because of missing dependencies or incorrect imports.")
        return 1
    except Exception as e:
        print(f"Unexpected Error: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())