import json
import time
import logging
import asyncio
import redis
from datetime import datetime, UTC, timedelta
from enum import Enum
from typing import List, Dict, Optional, Union, Any
import threading
import random
import os
import sys

"""
🔱 OMEGA BTC AI - Divine BTC Live Feed V2.1.0 🔱

This module provides a real-time Bitcoin price feed with:
- Automatic reconnection to exchange websockets
- Redis integration for price distribution
- High-frequency trap detection
- Rastafarian divine visualization
- ASCII art price movement representation

Copyright (c) 2025 OMEGA BTC AI Team
GPU (General Public Universal) License 1.0
"""

# Function to check and install required packages
def check_required_packages():
    """Check and install required packages for BTC Live Feed."""
    required_packages = {
        "websocket-client": "websocket",
        "websockets": "websockets",
        "redis": "redis",
        "rel": "rel"
    }
    
    missing_packages = []
    
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"Installing missing packages: {', '.join(missing_packages)}")
        import subprocess
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"Successfully installed {package}")
            except Exception as e:
                print(f"Failed to install {package}: {e}")
                return False
    
    return True

# Check and install required packages
check_required_packages()

# Import websocket-client and related modules
try:
    import websocket
    from websocket import WebSocketApp
    print("Successfully imported websocket-client")
except ImportError as e:
    print(f"Error importing websocket-client: {e}")
    print("Attempting to install websocket-client...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "websocket-client"])
        import websocket
        from websocket import WebSocketApp
        print("Successfully installed and imported websocket-client")
    except Exception as e:
        print(f"Failed to install websocket-client: {e}")
        sys.exit(1)

# Import rel for WebSocket dispatching
try:
    import rel
    print("Successfully imported rel")
except ImportError:
    print("Attempting to install rel...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "rel"])
        import rel
        print("Successfully installed and imported rel")
    except Exception as e:
        print(f"Failed to install rel: {e}")
        sys.exit(1)

# Import websockets for async WebSocket support
try:
    import websockets
    import websockets.exceptions
    print("Successfully imported websockets")
except ImportError:
    print("Attempting to install websockets...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "websockets"])
        import websockets
        import websockets.exceptions
        print("Successfully installed and imported websockets")
    except Exception as e:
        print(f"Failed to install websockets: {e}")
        sys.exit(1)

# Set Redis host environment variable
redis_host = os.environ.get('REDIS_HOST', 'localhost')
os.environ['REDIS_HOST'] = redis_host

from omega_ai.utils.redis_manager import RedisManager

# Configure logging with Rasta colors
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Rasta color constants
GREEN_RASTA = "\033[92m"  # Jah Green
YELLOW_RASTA = "\033[93m"  # Gold
RED_RASTA = "\033[91m"    # Babylon Red
BLUE_RASTA = "\033[94m"   # Zion Blue
MAGENTA_RASTA = "\033[95m"  # Royal Purple
CYAN_RASTA = "\033[96m"   # Ocean Blue
WHITE_RASTA = "\033[97m"  # Pure White
ORANGE_RASTA = "\033[38;5;208m"  # Fire Orange
RESET = "\033[0m"
BOLD = "\033[1m"

# ASCII Art Constants for Bitcoin Visualization
BTC_LOGO = f"""
{ORANGE_RASTA}           ,.=ctE55ttt553tzs.,
          ,,c5;z==!!::::  ::==7253.,
         ,xC;z!::::::    ::::::::==7251
        ,czz!:::::  ::;;..:::======253.
        {{'::::::::;;=====::.:::::::=3=.'}}
       ,{{'::::::::;=======:::::::::c=3x'}}
       ,{{'::::::::=========:::::::z=3z.'}}
       ,{{'::::::::==========:::::t3z.'}}
       ,{{'::::::::::===========::=37.'}}      {WHITE_RASTA}╔══════════════════════╗
       ,{{'::::::::;===P5===========z35;'}}  {WHITE_RASTA}  ║ {ORANGE_RASTA}₿{WHITE_RASTA} BITCOIN LIVE FEED {ORANGE_RASTA}₿{WHITE_RASTA} ║
       ,{{'::::::::zP53P===========333.'}} {WHITE_RASTA}  ╚══════════════════════╝
       ,{{'::::::::==P5P==========c=j'}}   
       ,{{'::::::::=======P5k3P=c=j7'}}
       ,{{'::::::::=====Pc==cz=c=z7'}}      {BLUE_RASTA}ONE LOVE - ONE HEART - ONE CODE
       ,{{'z:::::::=====Pz=c=z=3='}}       
       ,{{'3x::::::z====c===c=37'}}        
       ,{{'33t::::::z===33333=;'}}         
       ,{{'3zzz=:::::z=c33335C;'}}         
       ,{{'3=============z3==5.'}}
       ,{{'33==============5.'}}
       ,{{'3333=========c=7'}}
       ,{{'33335========C;'}}
       ,{{'3333=======z7'}}
       ,{{'33=========k'}}
       .{{'==========={{'}}
{RESET}"""

# Price movement arrows
UP_ARROW = f"{GREEN_RASTA}▲{RESET}"
DOWN_ARROW = f"{RED_RASTA}▼{RESET}"
SIDEWAYS_ARROW = f"{YELLOW_RASTA}◄►{RESET}"

# Version information
VERSION = "2.1.0"
BUILD_DATE = "2025-03-28"

# Fibonacci sequences and golden ratio
FIBONACCI_SEQUENCE = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]
GOLDEN_RATIO = 1.618033988749895

# Global variables for price tracking
prev_price = None
price_history = []

def display_price_header():
    """Display a beautiful header with version information."""
    header = f"""
{MAGENTA_RASTA}╔══════════════════════════════════════════════════════════════════╗
{MAGENTA_RASTA}║ {ORANGE_RASTA}₿{WHITE_RASTA} OMEGA BTC AI - DIVINE LIVE FEED {ORANGE_RASTA}₿ {CYAN_RASTA}v{VERSION} {YELLOW_RASTA}({BUILD_DATE}){MAGENTA_RASTA} ║
{MAGENTA_RASTA}╚══════════════════════════════════════════════════════════════════╝{RESET}
    """
    print(header)

def display_price_chart(current_price: float, price_history: list, width: int = 40, height: int = 10):
    """Generate an ASCII art chart of Bitcoin price movements."""
    if not price_history:
        return
    
    # Convert price history to float values
    prices = [float(price.split(',')[0]) for price in price_history if ',' in price]
    if not prices:
        return
    
    min_price = min(prices)
    max_price = max(prices)
    price_range = max_price - min_price
    
    if price_range == 0:
        return
    
    # Create the chart
    chart = []
    for i in range(height):
        row = []
        for price in prices:
            normalized = (price - min_price) / price_range
            y = int(normalized * (height - 1))
            if i == height - 1 - y:
                row.append(f"{GREEN_RASTA}█{RESET}")
            else:
                row.append(" ")
        chart.append("".join(row))
    
    # Add price labels
    print(f"\n{BLUE_RASTA}Price Chart:{RESET}")
    print(f"Min: ${min_price:.2f} | Max: ${max_price:.2f} | Current: ${current_price:.2f}")
    for row in chart:
        print(row)
    print(f"{GREEN_RASTA}█{RESET} Price Movement")

def price_movement_indicator(current_price: float, prev_price: float | None) -> str:
    """Generate a visual indicator of price movement."""
    if prev_price is None:
        return f"{YELLOW_RASTA}→{RESET} Initial Price"
    
    # Ensure both prices are float
    current = float(current_price)
    previous = float(prev_price)
    
    change = current - previous
    change_pct = (change / previous) * 100
    
    if abs(change_pct) < 0.01:
        return f"{YELLOW_RASTA}→{RESET} {change_pct:.2f}%"
    elif change_pct > 0:
        return f"{GREEN_RASTA}↑{RESET} {change_pct:.2f}%"
    else:
        return f"{RED_RASTA}↓{RESET} {change_pct:.2f}%"

# Rasta logging functions
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

# Binance WebSocket API
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"

# MM WebSocket Server URL with updated port
MM_WS_URL = "ws://localhost:8765"

# Mock MM Trap Detector implementation for fallback use
class MockHighFrequencyTrapDetector:
    """Mock implementation of the MM Trap Detector for testing."""
    
    def __init__(self):
        self.price_history = []
        self.time_history = []
        self.window_size = 20
        log_rasta("🔄 Mock MM Trap Detector initialized", BLUE_RASTA)
    
    def update_price_data(self, price: float, timestamp: datetime) -> None:
        """Update the detector with new price data."""
        self.price_history.append(price)
        self.time_history.append(timestamp)
        
        # Keep only the window size
        if len(self.price_history) > self.window_size:
            self.price_history.pop(0)
            self.time_history.pop(0)
    
    def detect_high_freq_trap_mode(self, current_price: float) -> tuple[bool, float]:
        """Detect if high frequency trap mode is active."""
        if len(self.price_history) < self.window_size:
            return False, 0.0
            
        # Calculate price changes
        price_changes = [abs(b - a) / a for a, b in zip(self.price_history[:-1], self.price_history[1:])]
        
        # Calculate time differences
        time_diffs = [(b - a).total_seconds() for a, b in zip(self.time_history[:-1], self.time_history[1:])]
        
        # Calculate average price change and time difference
        avg_price_change = sum(price_changes) / len(price_changes)
        avg_time_diff = sum(time_diffs) / len(time_diffs) if time_diffs else 1.0
        
        # Calculate volatility score
        volatility_score = avg_price_change / avg_time_diff
        
        # Detect trap mode based on volatility
        is_trap_mode = volatility_score > 0.001  # Threshold for high frequency mode
        multiplier = volatility_score * 1000 if is_trap_mode else 0.0
        
        return is_trap_mode, multiplier

async def send_to_mm_websocket(price):
    """Send BTC price update to MM WebSocket."""
    while True:
        try:
            async with websockets.connect(
                MM_WS_URL,
                max_size=2**20,
                ping_interval=30,
                ping_timeout=10,
                ssl=None  # Disable SSL for local testing
            ) as ws:
                log_rasta(f"Connected to MM WebSocket", GREEN_RASTA, "success")
                # Convert to properly encoded string for JSON
                message = json.dumps({"btc_price": price})
                await ws.send(message)
                log_rasta(f"BTC Price Sent: ${price:.2f}", BLUE_RASTA)
                return  # Exit loop on success
        except websockets.exceptions.ConnectionClosedOK:
            log_rasta(f"WebSocket Closed Normally, reconnecting...", YELLOW_RASTA, "warning")
        except websockets.exceptions.ConnectionClosedError as e:
            log_rasta(f"WebSocket Disconnected (Error {e.code}), retrying...", RED_RASTA, "error")
        except Exception as e:
            log_rasta(f"WebSocket Error: {e}, retrying...", RED_RASTA, "error")
        
        await asyncio.sleep(5)  # Persistent retry mechanism

def main():
    """Main function to run the BTC Live Feed."""
    global hf_detector
    
    # Initialize the mock trap detector
    hf_detector = MockHighFrequencyTrapDetector()
    
    # Display startup banner
    print(BTC_LOGO)
    display_price_header()
    
    # Connect to Binance WebSocket
    ws = websocket.WebSocketApp(
        "wss://stream.binance.com:9443/ws/btcusdt@trade",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    
    # Set up dispatcher
    rel.signal(2, rel.abort)  # Properly handle Ctrl+C
    rel.dispatch()
    
    # Start WebSocket connection
    ws.run_forever()

def on_message(ws, message):
    """Process incoming Binance BTC price data."""
    global prev_price, price_history
    
    try:
        data = json.loads(message)
        price = float(data["p"])
        volume = float(data["q"])

        log_rasta(f"LIVE BTC PRICE UPDATE: ${price:.2f} (Vol: {volume})", BLUE_RASTA)
        
        # Use mock detector for price analysis
        if hf_detector is not None:
            try:
                timestamp = datetime.now(UTC)
                hf_detector.update_price_data(price, timestamp)
                
                # Check for high frequency mode activation
                hf_active, multiplier = hf_detector.detect_high_freq_trap_mode(price)
                if hf_active:
                    log_rasta(f"⚠️ HIGH FREQUENCY TRAP MODE ACTIVATED! Multiplier: {multiplier}", RED_RASTA, "warning")
                    
                    # Display special HF mode banner when activated
                    hf_banner = f"""
{RED_RASTA}╔══════════════════════════════════════════════╗
{RED_RASTA}║ {YELLOW_RASTA}⚡ HIGH FREQUENCY TRAP MODE ACTIVATED ⚡{RED_RASTA} ║
{RED_RASTA}║ {WHITE_RASTA}Multiplier: {multiplier:.2f}                        {RED_RASTA}║
{RED_RASTA}╚══════════════════════════════════════════════╝{RESET}
                    """
                    print(hf_banner)
            except Exception as e:
                log_rasta(f"Error using MM Trap Detector: {e}", YELLOW_RASTA, "warning")
        
        # Display price movement indicator
        movement = price_movement_indicator(price, prev_price)
        print(f"{CYAN_RASTA}[PRICE MOVEMENT] {movement}")
        
        # Update price history
        price_history.append(price)
        if len(price_history) > 100:  # Keep last 100 prices
            price_history.pop(0)
        
        # Update previous price
        prev_price = price
        
        # Periodically display the ASCII chart
        if random.random() < 0.05:  # ~5% chance to display chart
            print(BTC_LOGO)
            display_price_chart(price, price_history, width=40, height=10)
            
        # Send price update to MM WebSocket server
        asyncio.run(send_to_mm_websocket(price))

    except Exception as e:
        log_rasta(f"Error processing message: {e}", RED_RASTA, "error")

def on_error(ws, error):
    """Handle WebSocket errors with divine grace."""
    log_rasta(f"WebSocket Error: {error}", RED_RASTA, "error")
    time.sleep(5)  # Add delay before reconnect

def on_close(ws, close_status_code, close_msg):
    """Handle WebSocket closure with Rastafarian resilience."""
    log_rasta(f"WebSocket Closed: {close_status_code} - {close_msg}", YELLOW_RASTA, "warning")
    time.sleep(5)  # Add delay before reconnect
    start_btc_websocket()

def on_open(ws):
    """Handle WebSocket opening with divine blessing."""
    log_rasta("Connected to Binance WebSocket - Streaming BTC Prices...", GREEN_RASTA, "success")

def start_btc_websocket():
    """Start WebSocket connection to Binance BTC Live Feed."""
    while True:
        try:
            # Create the WebSocket connection
            try:
                log_rasta("Creating WebSocketApp connection to Binance...", GREEN_RASTA)
                
                # Create WebSocketApp with explicit handlers
                ws = WebSocketApp(
                    BINANCE_WS_URL,
                    on_message=on_message,
                    on_error=on_error,
                    on_close=on_close,
                    on_open=on_open
                )
                
                log_rasta("Running WebSocketApp with dispatcher...", GREEN_RASTA)
                
                # Fix the rel dispatcher issue - don't pass the module as dispatcher
                ws.run_forever()  # Don't pass rel as dispatcher
                # Manually use rel for event loop
                rel.signal(2, rel.abort)  # Handle Keyboard Interrupt
                rel.dispatch()
                
            except Exception as e:
                log_rasta(f"WebSocketApp connection failed: {str(e)}", RED_RASTA, "error")
                time.sleep(10)
        except Exception as e:
            log_rasta(f"Error in WebSocket connection: {str(e)}", RED_RASTA, "error")
            time.sleep(5)

if __name__ == "__main__":
    # Display versions for debugging
    print(f"Python version: {sys.version}")
    
    try:
        print(f"websocket-client version: {websocket.__version__}")
    except:
        print("Could not detect websocket-client version")
        
    try:
        print(f"rel version: {rel.__version__}")
    except:
        print("Could not detect rel version")
    
    # Verify all required packages are installed
    if not check_required_packages():
        log_rasta("Failed to install required packages. Exiting...", RED_RASTA, "error")
        sys.exit(1)
    
    # Display divine header
    display_price_header()
    print(BTC_LOGO)
        
    log_rasta("Initializing Rasta Price Feed V2 with Mock MM Trap Detector...", GREEN_RASTA)
    log_rasta(f"Redis Host: {os.getenv('REDIS_HOST', 'localhost')}", BLUE_RASTA)
    log_rasta("Connecting to Binance WebSocket...", BLUE_RASTA)
    
    # Start the WebSocket connection
    main() 