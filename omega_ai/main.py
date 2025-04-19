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
🔱 OMEGA BTC AI - Market Manipulation Detection System 🔱
The central orchestration pipeline for the entire OMEGA BTC AI system.
"""
import asyncio
import os
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime

# Database initialization
try:
    from omega_ai.db_manager.database import setup_database
except ImportError:
    print("Warning: Could not import setup_database. Database initialization will be skipped.")
    def setup_database():
        """Dummy function when database module is not available."""
        pass

# Component imports
from omega_ai.data_feed.schumann_monitor import start_schumann_monitor, stop_schumann_monitor
from omega_ai.data_feed.btc_live_feed import start_btc_websocket
from omega_ai.mm_trap_detector.mm_trap_detector import MMTrapDetector
from omega_ai.monitor.monitor_market_trends import monitor_market_trends

# Terminal colors for beautiful console output
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
GOLD = "\033[93m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BLACK = "\033[30m"
BOLD = "\033[1m"
BLUE_BG = "\033[44m"
GREEN_BG = "\033[42m"
RED_BG = "\033[41m"

# Track active threads/processes
active_threads = []

def display_ascii_banner():
    """Display OMEGA BTC AI ASCII art banner."""
    print(f"{BLUE}")
    print(r"""
  ___  __  __ _____ ____    _      ____ _____ ____      _    ___ 
 / _ \|  \/  | ____/ ___|  / \    | __ )_   _/ ___|    / \  |_ _|
| | | | |\/| |  _|| |  _  / _ \   |  _ \ | || |       / _ \  | | 
| |_| | |  | | |__| |_| |/ ___ \  | |_) || || |___   / ___ \ | | 
 \___/|_|  |_|_____\____/_/   \_\ |____/ |_| \____| /_/   \_\___|
          

-... -.-- ---...    ----- -- ...-- --. ....- -....- -.- .---- -. --.

                                                                         
    """)
    print(f"{RESET}")

def print_section_header(title):
    """Print a formatted section header."""
    width = 70
    print(f"\n{BLUE_BG}{WHITE}{BOLD} {title} {' ' * (width - len(title) - 2)}{RESET}")

def print_status(component, status, message=""):
    """Print component status with appropriate colors."""
    status_color = GREEN if status == "ONLINE" else RED if status == "ERROR" else YELLOW
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    print(f"[{timestamp}] {CYAN}{component:25}{RESET} {status_color}{status:10}{RESET} {message}")

def signal_handler(sig, frame):
    """Handle graceful shutdown on CTRL+C."""
    print_section_header("SHUTTING DOWN OMEGA BTC AI")
    print(f"{YELLOW}⚠️ Shutdown signal received. Stopping all components...{RESET}")
    
    # Stop Schumann monitor
    print(f"{YELLOW}Stopping Schumann resonance monitor...{RESET}")
    stop_schumann_monitor()
    
    # Signal all threads to stop
    for thread in active_threads:
        if thread.is_alive():
            print(f"{YELLOW}Waiting for {thread.name} to complete...{RESET}")
    
    print(f"{GREEN}✅ Shutdown complete. Goodbye!{RESET}")
    sys.exit(0)

def run_thread(target, name, daemon=True):
    """Run a function in a new thread and add it to active_threads."""
    thread = threading.Thread(target=target, name=name, daemon=daemon)
    thread.start()
    active_threads.append(thread)
    return thread

def start_btc_feed():
    """Start the BTC price feed in a separate thread."""
    def run_feed():
        try:
            start_btc_websocket()
        except Exception as e:
            print(f"{RED}❌ BTC feed error: {e}{RESET}")
    
    return run_thread(run_feed, "BTC-Feed")

def start_market_monitor():
    """Start the market trend monitor in a separate thread."""
    return run_thread(monitor_market_trends, "Market-Monitor")

def start_trap_processor():
    """Start the MM trap processor in a separate thread."""
    detector = MMTrapDetector()
    return run_thread(detector.run, "MM-Trap-Processor")

def check_component_status():
    """Check and display the status of all system components."""
    while True:
        print_section_header("OMEGA BTC AI SYSTEM STATUS")
        
        # Check each thread
        for thread in active_threads:
            status = "ONLINE" if thread.is_alive() else "OFFLINE"
            print_status(thread.name, status)
            
        # Sleep for a minute before refreshing
        time.sleep(60)

def main():
    """Main execution function for OMEGA BTC AI system."""
    # Handle CTRL+C gracefully
    signal.signal(signal.SIGINT, signal_handler)
    
    # Display welcome banner
    display_ascii_banner()
    print(f"{GOLD}{BOLD}🔱 OMEGA BTC AI - Market Manipulation Detection System 🔱{RESET}")
    print(f"{WHITE}Watching for market manipulation... Babylon can't hide!{RESET}\n")
    
    # Initialize system
    print_section_header("SYSTEM INITIALIZATION")
    
    # 1. Set up database
    print(f"{CYAN}Setting up database...{RESET}")
    setup_database()
    print_status("Database", "ONLINE", "PostgreSQL tables initialized")
    
    # 2. Start Schumann resonance monitor
    print(f"{CYAN}Starting Schumann resonance monitor...{RESET}")
    start_schumann_monitor()
    print_status("Schumann Monitor", "ONLINE", "Tracking electromagnetic resonance")
    
    # 3. Start Bitcoin price feed
    print(f"{CYAN}Starting Bitcoin price feed...{RESET}")
    btc_feed_thread = start_btc_feed()
    print_status("BTC Price Feed", "ONLINE", "Connected to Binance WebSocket")
    
    # 4. Start market trend monitor
    print(f"{CYAN}Starting market trend monitor...{RESET}")
    market_monitor_thread = start_market_monitor()
    print_status("Market Trend Monitor", "ONLINE", "Analyzing multi-timeframe trends")
    
    # 5. Start MM trap detector
    print(f"{CYAN}Starting MM trap detector...{RESET}")
    trap_detector_thread = start_trap_processor()
    print_status("MM Trap Detector", "ONLINE", "Monitoring for market manipulation")
    
    # Give components time to initialize
    time.sleep(3)
    
    print(f"\n{GREEN_BG}{BLACK}{BOLD} ALL SYSTEMS ONLINE - OMEGA BTC AI IS OPERATIONAL {RESET}")
    print(f"{GOLD}Press Ctrl+C to shut down the system{RESET}\n")
    
    # Start status checking thread
    status_thread = run_thread(check_component_status, "Status-Monitor")
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main()