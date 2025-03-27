"""
🔱 OMEGA BTC AI - TMUX BTC Feed Display 🔱
Sacred tmux integration for divine BTC price visualization.

GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2024-03-26
Location: The Cosmic Void
"""
import os
import sys
import subprocess
import time
from datetime import datetime, UTC
from typing import Optional, List, Dict, Any
import json
from omega_ai.utils.redis_manager import RedisManager

# Rasta color constants
GREEN_RASTA = "\033[92m"  # Jah Green
YELLOW_RASTA = "\033[93m"  # Gold
RED_RASTA = "\033[91m"    # Babylon Red
BLUE_RASTA = "\033[94m"   # Zion Blue
MAGENTA_RASTA = "\033[95m"  # Royal Purple
CYAN_RASTA = "\033[96m"   # Ocean Blue
RESET = "\033[0m"
BOLD = "\033[1m"

def log_rasta(message: str, color: str = GREEN_RASTA, level: str = "info"):
    """Log with Rasta style and colors."""
    timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    if level == "error":
        print(f"{RED_RASTA}[{timestamp}] ❌ {message}{RESET}")
    elif level == "warning":
        print(f"{YELLOW_RASTA}[{timestamp}] ⚠️  {message}{RESET}")
    elif level == "success":
        print(f"{GREEN_RASTA}[{timestamp}] ✅ {message}{RESET}")
    else:
        print(f"{color}[{timestamp}] ℹ️  {message}{RESET}")

def display_rasta_banner():
    """Display the Rasta-style banner."""
    banner = f"""
{GREEN_RASTA}╔══════════════════════════════════════════════════════════╗
     ██████╗ ███╗   ███╗███████╗ ██████╗  █████╗ 
    ██╔═══██╗████╗ ████║██╔════╝██╔════╝ ██╔══██╗
    ██║   ██║██╔████╔██║█████╗  ██║  ███╗███████║
    ██║   ██║██║╚██╔╝██║██╔══╝  ██║   ██║██╔══██║
    ╚██████╔╝██║ ╚═╝ ██║███████╗╚██████╔╝██║  ██║
     ╚═════╝ ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝
                {YELLOW_RASTA}BTC AI SYSTEM v1.0
     [ Rasta Price Feed - One Love - Fibonacci Aligned ]{GREEN_RASTA}
╚══════════════════════════════════════════════════════════╝{RESET}
"""
    print(banner)

def setup_tmux_session():
    """Set up the divine tmux session for BTC price display."""
    try:
        # Check if tmux is installed
        subprocess.run(['tmux', 'has-session'], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        log_rasta("Creating new tmux session...", BLUE_RASTA)
        subprocess.run(['tmux', 'new-session', '-d', '-s', 'omega_btc'])
    except FileNotFoundError:
        log_rasta("tmux is not installed. Please install tmux first.", RED_RASTA, "error")
        sys.exit(1)

def create_price_display_pane():
    """Create a divine pane for BTC price display."""
    try:
        # Create a new pane in the tmux session
        subprocess.run(['tmux', 'split-window', '-h', '-t', 'omega_btc'])
        subprocess.run(['tmux', 'select-pane', '-t', 'omega_btc.1'])
        
        # Set up the price display pane
        subprocess.run(['tmux', 'send-keys', '-t', 'omega_btc.1', 'clear', 'Enter'])
        subprocess.run(['tmux', 'send-keys', '-t', 'omega_btc.1', 'python3 -m omega_ai.data_feed.btc_live_feed', 'Enter'])
        
        log_rasta("Created price display pane", GREEN_RASTA, "success")
    except Exception as e:
        log_rasta(f"Error creating price display pane: {e}", RED_RASTA, "error")
        sys.exit(1)

def create_fibonacci_pane():
    """Create a divine pane for Fibonacci levels display."""
    try:
        # Create a new pane for Fibonacci levels
        subprocess.run(['tmux', 'split-window', '-v', '-t', 'omega_btc.1'])
        subprocess.run(['tmux', 'select-pane', '-t', 'omega_btc.2'])
        
        # Set up the Fibonacci display
        subprocess.run(['tmux', 'send-keys', '-t', 'omega_btc.2', 'clear', 'Enter'])
        subprocess.run(['tmux', 'send-keys', '-t', 'omega_btc.2', 'python3 -c "from omega_ai.data_feed.btc_live_feed import display_fibonacci_levels; display_fibonacci_levels()"', 'Enter'])
        
        log_rasta("Created Fibonacci display pane", GREEN_RASTA, "success")
    except Exception as e:
        log_rasta(f"Error creating Fibonacci pane: {e}", RED_RASTA, "error")
        sys.exit(1)

def create_trap_monitor_pane():
    """Create a divine pane for trap monitoring."""
    try:
        # Create a new pane for trap monitoring
        subprocess.run(['tmux', 'split-window', '-v', '-t', 'omega_btc.0'])
        subprocess.run(['tmux', 'select-pane', '-t', 'omega_btc.3'])
        
        # Set up the trap monitor
        subprocess.run(['tmux', 'send-keys', '-t', 'omega_btc.3', 'clear', 'Enter'])
        subprocess.run(['tmux', 'send-keys', '-t', 'omega_btc.3', 'python3 -m omega_ai.mm_trap_detector.trap_monitor', 'Enter'])
        
        log_rasta("Created trap monitor pane", GREEN_RASTA, "success")
    except Exception as e:
        log_rasta(f"Error creating trap monitor pane: {e}", RED_RASTA, "error")
        sys.exit(1)

def setup_tmux_layout():
    """Set up the divine tmux layout."""
    try:
        # Set up the main layout
        subprocess.run(['tmux', 'select-layout', '-t', 'omega_btc', 'tiled'])
        
        # Set pane titles
        subprocess.run(['tmux', 'select-pane', '-t', 'omega_btc.0', '-T', 'BTC Price Feed'])
        subprocess.run(['tmux', 'select-pane', '-t', 'omega_btc.1', '-T', 'Price Display'])
        subprocess.run(['tmux', 'select-pane', '-t', 'omega_btc.2', '-T', 'Fibonacci Levels'])
        subprocess.run(['tmux', 'select-pane', '-t', 'omega_btc.3', '-T', 'Trap Monitor'])
        
        # Set pane colors
        subprocess.run(['tmux', 'set-window-option', '-t', 'omega_btc', 'pane-border-status', 'top'])
        subprocess.run(['tmux', 'set-window-option', '-t', 'omega_btc', 'pane-border-format', '#{?pane_active,#[reverse],}#{pane_index} #{pane_title}'])
        
        log_rasta("Set up tmux layout", GREEN_RASTA, "success")
    except Exception as e:
        log_rasta(f"Error setting up tmux layout: {e}", RED_RASTA, "error")
        sys.exit(1)

def attach_to_tmux():
    """Attach to the divine tmux session."""
    try:
        log_rasta("Attaching to tmux session...", BLUE_RASTA)
        subprocess.run(['tmux', 'attach-session', '-t', 'omega_btc'])
    except Exception as e:
        log_rasta(f"Error attaching to tmux session: {e}", RED_RASTA, "error")
        sys.exit(1)

def main():
    """Main entry point for the divine tmux BTC feed display."""
    display_rasta_banner()
    
    try:
        # Set up tmux session
        setup_tmux_session()
        
        # Create panes
        create_price_display_pane()
        create_fibonacci_pane()
        create_trap_monitor_pane()
        
        # Set up layout
        setup_tmux_layout()
        
        # Attach to session
        attach_to_tmux()
        
    except KeyboardInterrupt:
        log_rasta("\nShutting down divine tmux session...", YELLOW_RASTA)
        subprocess.run(['tmux', 'kill-session', '-t', 'omega_btc'])
        log_rasta("JAH BLESS! Session closed.", GREEN_RASTA)
    except Exception as e:
        log_rasta(f"Fatal error: {e}", RED_RASTA, "error")
        sys.exit(1)

if __name__ == "__main__":
    main() 