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
Start BTC Price Feed and MM Trap Detector
This script initializes and runs both components for real-time monitoring
"""

import os
import time
import threading
from datetime import datetime, UTC
import signal
import sys

# Set Redis host environment variable
os.environ['REDIS_HOST'] = 'localhost'

# Import required modules
from omega_ai.data_feed.btc_live_feed import BtcPriceFeed, display_rasta_banner, check_redis_health
from omega_ai.mm_trap_detector.high_frequency_detector import (
    hf_detector, check_high_frequency_mode
)

# Rasta color constants
GREEN_RASTA = "\033[92m"
YELLOW_RASTA = "\033[93m"
RED_RASTA = "\033[91m"
BLUE_RASTA = "\033[94m"
CYAN_RASTA = "\033[96m"
MAGENTA_RASTA = "\033[95m"
RESET = "\033[0m"
BOLD = "\033[1m"

def log_message(message, color=GREEN_RASTA, level="info"):
    """Log with color coding."""
    timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    if level == "error":
        print(f"{RED_RASTA}[{timestamp}] ❌ {message}{RESET}")
    elif level == "warning":
        print(f"{YELLOW_RASTA}[{timestamp}] ⚠️  {message}{RESET}")
    elif level == "success":
        print(f"{GREEN_RASTA}[{timestamp}] ✅ {message}{RESET}")
    else:
        print(f"{color}[{timestamp}] ℹ️  {message}{RESET}")

# Flag to control the main loop
running = True

def signal_handler(sig, frame):
    """Handle interrupt signals gracefully."""
    global running
    log_message("Shutdown signal received! Cleaning up...", YELLOW_RASTA, "warning")
    running = False

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def monitor_trap_detector():
    """Continuously monitor the trap detector for alerts."""
    while running:
        try:
            # Check for high-frequency mode activation
            hf_active, multiplier = check_high_frequency_mode()
            
            if hf_active:
                log_message(f"HIGH FREQUENCY TRAP MODE ACTIVE! Multiplier: {multiplier}", 
                           RED_RASTA, "warning")
            
            # Sleep to avoid excessive CPU usage
            time.sleep(10)  # Check every 10 seconds
            
        except Exception as e:
            log_message(f"Error in trap detector monitoring: {e}", RED_RASTA, "error")
            time.sleep(30)  # Wait longer after an error

def start_monitoring():
    """Start all monitoring components."""
    display_rasta_banner()
    log_message("Starting BTC Monitoring System", MAGENTA_RASTA, "success")
    
    # Check Redis health first
    redis_healthy = check_redis_health()
    if not redis_healthy:
        log_message("Redis health check failed. Please fix Redis issues before continuing.", 
                   RED_RASTA, "error")
        return False
    
    try:
        # Initialize BTC price feed
        log_message("Initializing BTC Price Feed...", BLUE_RASTA)
        price_feed = BtcPriceFeed()
        price_feed.start()
        log_message("BTC Price Feed started successfully", GREEN_RASTA, "success")
        
        # Start trap detector monitoring in a separate thread
        trap_thread = threading.Thread(target=monitor_trap_detector)
        trap_thread.daemon = True
        trap_thread.start()
        log_message("MM Trap Detector monitoring thread started", GREEN_RASTA, "success")
        
        # Main loop to keep the script running
        log_message("All systems operational. Press Ctrl+C to stop.", CYAN_RASTA)
        
        while running:
            # Get current price for status display
            current_price = price_feed.get_current_price()
            log_message(f"Current BTC Price: ${current_price:.2f}", BLUE_RASTA)
            
            # Display trap detector status
            hf_active, multiplier = check_high_frequency_mode()
            status = "🔥 HIGH FREQUENCY MODE" if hf_active else "Normal market mode"
            log_message(f"Trap Detector Status: {status}", 
                      RED_RASTA if hf_active else GREEN_RASTA)
            
            # Sleep for status update interval
            time.sleep(60)  # Update status every minute
        
        # Cleanup when loop exits
        log_message("Shutting down monitoring systems...", YELLOW_RASTA)
        price_feed.stop()
        log_message("Monitoring systems shutdown complete", GREEN_RASTA, "success")
        return True
        
    except KeyboardInterrupt:
        log_message("Manual interrupt received", YELLOW_RASTA, "warning")
        return True
    except Exception as e:
        log_message(f"Error in monitoring system: {e}", RED_RASTA, "error")
        return False

if __name__ == "__main__":
    success = start_monitoring()
    sys.exit(0 if success else 1) 