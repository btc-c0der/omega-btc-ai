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
    from websocket import WebSocketApp  # Explicit import for WebSocketApp
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
from omega_ai.utils.redis_config import get_redis_config
redis_config = get_redis_config()
os.environ['REDIS_HOST'] = redis_config['host']
os.environ['REDIS_PORT'] = str(redis_config['port'])
os.environ['REDIS_USERNAME'] = redis_config['username']
os.environ['REDIS_PASSWORD'] = redis_config['password']

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
RESET = "\033[0m"
BOLD = "\033[1m"

# Fibonacci sequences and golden ratio
FIBONACCI_SEQUENCE = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]
GOLDEN_RATIO = 1.618033988749895

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

# Binance WebSocket API
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"

# MM WebSocket Server URL with updated port
MM_WS_URL = "ws://localhost:8765"

# Redis Connection - used by legacy functions
redis_conn = redis.Redis(**redis_config)

# Redis health check function from Code version
def check_redis_health():
    """Perform a health check on Redis connection and data integrity."""
    try:
        # Check Redis connection
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        redis_manager = RedisManager(host=redis_host, port=redis_port)
        redis_manager.ping()
        log_rasta(f"Redis connection: OK (Host: {redis_host}, Port: {redis_port})", GREEN_RASTA, "success")

        # Check if essential keys exist using safe methods
        essential_keys = ["last_btc_price", "prev_btc_price", "btc_movement_history", "fibonacci_levels"]
        for key in essential_keys:
            if key == "btc_movement_history":
                # For list type, we need to check differently
                history = redis_manager.safe_lrange(key, 0, 0)
                if not history:
                    log_rasta(f"Essential key missing: {key}", YELLOW_RASTA, "warning")
                else:
                    log_rasta(f"Essential key present: {key}", GREEN_RASTA, "success")
            else:
                # Use safe_get for all other keys
                value = redis_manager.safe_get(key)
                if not value:
                    log_rasta(f"Essential key missing: {key}", YELLOW_RASTA, "warning")
                else:
                    log_rasta(f"Essential key present: {key}", GREEN_RASTA, "success")

        # Check data integrity
        btc_movement_history = redis_manager.safe_lrange("btc_movement_history", 0, -1)
        log_rasta(f"BTC movement history length: {len(btc_movement_history) if btc_movement_history else 0}", BLUE_RASTA)
        
        # Check data format
        if btc_movement_history:
            sample = btc_movement_history[0]
            if isinstance(sample, str) and "," in sample:
                try:
                    price_str, volume_str = sample.split(",")
                    price = float(price_str)
                    volume = float(volume_str)
                    log_rasta(f"Data format OK - Sample: Price=${price:.2f}, Volume={volume}", GREEN_RASTA, "success")
                except Exception as e:
                    log_rasta(f"Invalid data format in btc_movement_history: {e}", YELLOW_RASTA, "warning")
            else:
                log_rasta("Data format missing volume information", YELLOW_RASTA, "warning")

        return True
    except Exception as e:
        log_rasta(f"Redis health check failed: {e}", RED_RASTA, "error")
        return False

# Calculate Fibonacci retracement levels
def calculate_fibonacci_levels(high_price, low_price):
    """Calculate and store Fibonacci retracement levels for current price range."""
    try:
        # Calculate retracement levels based on the provided high and low prices
        price_range = high_price - low_price
        
        # Common Fibonacci retracement levels
        levels = {
            "0.0": low_price,
            "0.236": low_price + 0.236 * price_range,
            "0.382": low_price + 0.382 * price_range,
            "0.5": low_price + 0.5 * price_range,  # Not a Fibonacci ratio but commonly used
            "0.618": low_price + 0.618 * price_range,
            "0.786": low_price + 0.786 * price_range,
            "1.0": high_price,
            # Extensions beyond the range
            "1.618": high_price + 0.618 * price_range,
            "2.618": high_price + 1.618 * price_range
        }
        
        # Format levels for storage
        formatted_levels = {k: f"{v:.2f}" for k, v in levels.items()}
        
        # Store in Redis
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        redis_manager = RedisManager(host=redis_host, port=redis_port)
        redis_manager.set_cached("fibonacci_levels", json.dumps(formatted_levels))
        redis_manager.set_cached("fibonacci_high", str(high_price))
        redis_manager.set_cached("fibonacci_low", str(low_price))
        redis_manager.set_cached("fibonacci_update_time", str(time.time()))
        
        log_rasta(f"Fibonacci levels calculated and stored: High=${high_price:.2f}, Low=${low_price:.2f}", CYAN_RASTA)
        return formatted_levels
    except Exception as e:
        log_rasta(f"Error calculating Fibonacci levels: {e}", RED_RASTA, "error")
        return None

# WebSocket integration function from Code version
async def send_to_mm_websocket(price):
    """Send BTC price update to MM WebSocket."""
    while True:
        try:
            async with websockets.connect(
                MM_WS_URL,
                max_size=2**20,
                ping_interval=30,
                ping_timeout=10
            ) as ws:
                log_rasta(f"Connected to MM WebSocket", GREEN_RASTA, "success")
                await ws.send(json.dumps({"btc_price": price}))
                log_rasta(f"BTC Price Sent: ${price:.2f}", BLUE_RASTA)
                return  # Exit loop on success
        except websockets.exceptions.ConnectionClosedOK:
            log_rasta(f"WebSocket Closed Normally, reconnecting...", YELLOW_RASTA, "warning")
        except websockets.exceptions.ConnectionClosedError as e:
            log_rasta(f"WebSocket Disconnected (Error {e.code}), retrying...", RED_RASTA, "error")
        except Exception as e:
            log_rasta(f"WebSocket Error: {e}, retrying...", RED_RASTA, "error")
        
        await asyncio.sleep(5)  # Persistent retry mechanism

def on_error(ws, error):
    """Handle WebSocket errors with divine grace."""
    log_rasta(f"WebSocket Error: {error}", RED_RASTA, "error")
    time.sleep(5)  # Add delay before reconnect

# Try to import MM Trap Detector components
mm_trap_detector_available = False
hf_detector = None

try:
    from omega_ai.mm_trap_detector.high_frequency_detector import hf_detector
    mm_trap_detector_available = True
    log_method = print  # Will be replaced with log_rasta after it's defined
    log_method("✅ MM Trap Detector module loaded successfully")
except ImportError as e:
    log_method = print  # Will be replaced with log_rasta after it's defined
    log_method(f"⚠️ MM Trap Detector module not available: {str(e)}")
except Exception as e:
    log_method = print  # Will be replaced with log_rasta after it's defined
    log_method(f"⚠️ Error loading MM Trap Detector module: {str(e)}")

def on_message(ws, message):
    """Process incoming Binance BTC price data."""
    try:
        data = json.loads(message)
        price = float(data["p"])
        volume = float(data["q"])

        log_rasta(f"LIVE BTC PRICE UPDATE: ${price:.2f} (Vol: {volume})", BLUE_RASTA)
        
        # Update Redis values using the RedisManager with connection based on environment
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        redis_manager = RedisManager(host=redis_host, port=redis_port)
        prev_price = redis_manager.get_cached("prev_btc_price")
        prev_price = float(prev_price) if prev_price else None

        if prev_price is None or price != prev_price:
            # Store both price and volume values separately
            redis_manager.set_cached("last_btc_price", str(price))
            redis_manager.set_cached("last_btc_volume", str(volume))
            
            # Store combined price and volume data in history
            combined_data = f"{price},{volume}"
            redis_manager.lpush("btc_movement_history", combined_data)
            redis_manager.ltrim("btc_movement_history", -100, -1)
            
            abs_change = abs(price - prev_price) if prev_price is not None else 0
            abs_change_scaled = abs_change * 100
            redis_manager.lpush("abs_price_change_history", str(abs_change_scaled))
            redis_manager.ltrim("abs_price_change_history", -100, -1)
            redis_manager.set_cached("prev_btc_price", str(price))
            
            # Add last update time
            redis_manager.set_cached("last_btc_update_time", str(time.time()))
            
            # Update Fibonacci levels every 100 price updates or when significant movement occurs
            update_fibonacci = False
            fibonacci_update_count = redis_manager.get_cached("fibonacci_update_count")
            if fibonacci_update_count:
                count = int(fibonacci_update_count)
                if count >= 100:
                    update_fibonacci = True
                    redis_manager.set_cached("fibonacci_update_count", "0")
                else:
                    redis_manager.set_cached("fibonacci_update_count", str(count + 1))
            else:
                redis_manager.set_cached("fibonacci_update_count", "1")
            
            # Also update Fibonacci on significant price movement
            if prev_price and abs(price - prev_price) / prev_price > 0.01:  # 1% change
                update_fibonacci = True
            
            if update_fibonacci:
                # Get price history for high and low calculation
                history = redis_manager.lrange("btc_movement_history", 0, -1)
                if history:
                    prices = []
                    for item in history:
                        if "," in item:
                            price_str, _ = item.split(",")
                            prices.append(float(price_str))
                        else:
                            prices.append(float(item))
                    
                    if prices:
                        high_price = max(prices)
                        low_price = min(prices)
                        calculate_fibonacci_levels(high_price, low_price)
            
            log_rasta(f"Redis Updated: BTC Price = {price:.2f}, Volume = {volume}, Abs Change = {abs_change_scaled:.2f}", GREEN_RASTA)
            
            # Send price update to MM WebSocket server
            asyncio.run(send_to_mm_websocket(price))
            
            # Store fibonacci aligned flags
            is_fibonacci_aligned = False
            for level_value in FIBONACCI_SEQUENCE:
                level = level_value * 1000
                if abs(price - level) < 50:  # Within $50 of a Fibonacci level
                    is_fibonacci_aligned = True
                    redis_manager.set_cached("fibonacci_alignment", f"{level_value}000")
                    log_rasta(f"🔱 SACRED ALIGNMENT: BTC price near Fibonacci level ${level_value}000", MAGENTA_RASTA)
                    break
            
            if not is_fibonacci_aligned:
                redis_manager.set_cached("fibonacci_alignment", "0")
            
            # Notify the high frequency detector about price update
            if mm_trap_detector_available and hf_detector:
                try:
                    # Update the detector with the new price
                    timestamp = datetime.now(UTC)
                    hf_detector.update_price_data(price, timestamp)
                    
                    # Check for high frequency mode activation
                    hf_active, multiplier = hf_detector.detect_high_freq_trap_mode(price)
                    if hf_active:
                        log_rasta(f"⚠️ HIGH FREQUENCY TRAP MODE ACTIVATED! Multiplier: {multiplier}", RED_RASTA, "warning")
                except Exception as e:
                    log_rasta(f"Error using MM Trap Detector: {e}", YELLOW_RASTA, "warning")
            else:
                # Only display the warning once by checking if the flag has changed
                if redis_manager.get_cached("mm_trap_detector_warning_shown") != "1":
                    log_rasta("MM Trap Detector module not available", YELLOW_RASTA, "warning")
                    redis_manager.set_cached("mm_trap_detector_warning_shown", "1")
        else:
            log_rasta(f"Price Unchanged, Skipping Redis Update: {price}", YELLOW_RASTA)

    except Exception as e:
        log_rasta(f"Error processing message: {e}", RED_RASTA, "error")

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
            if not check_redis_health():
                log_rasta("Redis health check failed. Retrying in 60 seconds...", RED_RASTA, "error")
                time.sleep(60)
                continue

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
                
                # Set up rel dispatching
                ws.run_forever(dispatcher=rel)
                rel.signal(2, rel.abort)  # Handle Keyboard Interrupt
                rel.dispatch()
                
            except Exception as e:
                log_rasta(f"WebSocketApp connection failed: {str(e)}", RED_RASTA, "error")
                time.sleep(10)
        except Exception as e:
            log_rasta(f"Error in WebSocket connection: {str(e)}", RED_RASTA, "error")
            time.sleep(5)

class PriceSource(str, Enum):
    """Divine sources of BTC price data."""
    BINANCE = "binance"
    COINBASE = "coinbase"
    KRAKEN = "kraken"
    BITSTAMP = "bitstamp"
    GEMINI = "gemini"
    
    def __str__(self):
        return self.value

class BtcPriceFeed:
    """
    Real-time BTC price feed with divine Rastafarian energy.
    Provides OOP interface to the blessed BTC price feed functionality.
    
    Copyright (c) 2025 OMEGA-BTC-AI - Licensed under the MIT License
    ONE LOVE, ONE HEART, ONE CODE
    """
    
    def __init__(self, sources: Optional[List[PriceSource]] = None, update_interval: float = 5.0):
        """Initialize the blessed BTC price feed."""
        self.sources = sources or [PriceSource.BINANCE, PriceSource.COINBASE]
        self.update_interval = update_interval
        
        # Use direct localhost connection for Redis
        redis_host = 'localhost'
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        self.redis_manager = RedisManager(host=redis_host, port=redis_port)
        
        self.last_price = None
        self.last_volume = None
        self.is_running = False
        self._ws = None
        
        # Initialize WebSocket connection immediately
        self.connect_websocket()
    
    def connect_websocket(self):
        """Initialize WebSocket connection to Binance."""
        if not self._ws:
            try:
                websocket.enableTrace(True)
                self._ws = WebSocketApp(
                    BINANCE_WS_URL,
                    on_message=self._on_message,
                    on_error=self._on_error,
                    on_close=self._on_close,
                    on_open=self._on_open
                )
                # Start WebSocket connection in a separate thread
                self._ws_thread = threading.Thread(target=self._run_websocket)
                self._ws_thread.daemon = True
                self._ws_thread.start()
            except Exception as e:
                log_rasta(f"Failed to create WebSocket connection: {str(e)}", RED_RASTA, "error")

    def _run_websocket(self):
        """Run WebSocket connection with automatic reconnection."""
        while True:
            try:
                if self._ws:
                    self._ws.run_forever(dispatcher=rel)
                    rel.signal(2, rel.abort)  # Keyboard Interrupt
                    rel.dispatch()
            except Exception as e:
                log_rasta(f"WebSocket connection error: {e}", RED_RASTA, "error")
                time.sleep(5)  # Wait before reconnecting
    
    def _on_message(self, ws: websocket.WebSocket, message: Any) -> None:
        """Process incoming WebSocket BTC price data."""
        try:
            data = json.loads(message)
            price = float(data["p"])
            volume = float(data["q"])
            
            log_rasta(f"LIVE BTC PRICE UPDATE: ${price:.2f} (Vol: {volume})", BLUE_RASTA)
            
            # Check if previous price exists and if it's different from current price
            prev_price = self.redis_manager.get_cached("prev_btc_price")
            prev_price = float(prev_price) if prev_price else None
            
            if prev_price is None or price != prev_price:
                self.update_redis(price, volume)
                
                # Notify the high frequency detector about price update
                if mm_trap_detector_available and hf_detector:
                    try:
                        # Update the detector with the new price
                        timestamp = datetime.now(UTC)
                        hf_detector.update_price_data(price, timestamp)
                        
                        # Check for high frequency mode activation
                        hf_active, multiplier = hf_detector.detect_high_freq_trap_mode(price)
                        if hf_active:
                            log_rasta(f"⚠️ HIGH FREQUENCY TRAP MODE ACTIVATED! Multiplier: {multiplier}", RED_RASTA, "warning")
                    except Exception as e:
                        log_rasta(f"Error using MM Trap Detector: {e}", YELLOW_RASTA, "warning")
                else:
                    # Only display the warning once by checking if the flag has changed
                    if self.redis_manager.get_cached("mm_trap_detector_warning_shown") != "1":
                        log_rasta("MM Trap Detector module not available", YELLOW_RASTA, "warning")
                        self.redis_manager.set_cached("mm_trap_detector_warning_shown", "1")
            else:
                log_rasta(f"Price Unchanged, Skipping Redis Update: {price}", YELLOW_RASTA)
        except Exception as e:
            log_rasta(f"Error processing message: {e}", RED_RASTA, "error")

    def _on_error(self, ws: websocket.WebSocket, error: Any) -> None:
        """Handle WebSocket errors with divine grace."""
        log_rasta(f"WebSocket Error: {error}", RED_RASTA, "error")

    def _on_close(self, ws: websocket.WebSocket, close_status_code: Any, close_msg: Any) -> None:
        """Handle WebSocket closure with Rastafarian resilience."""
        log_rasta(f"WebSocket Closed: {close_status_code} - {close_msg}", YELLOW_RASTA, "warning")

    def _on_open(self, ws: websocket.WebSocket) -> None:
        """Handle WebSocket opening with divine blessing."""
        log_rasta("Connected to Binance WebSocket - Streaming BTC Prices...", GREEN_RASTA, "success")
    
    def update_redis(self, price: float, volume: float) -> None:
        """Save BTC price & volume to Redis for MM Trap Processor with error handling."""
        try:
            if price <= 0:
                log_rasta(f"Skipping Redis update, invalid BTC price: {price}", YELLOW_RASTA)
                return

            prev_price = self.redis_manager.get_cached("prev_btc_price")
            prev_price = float(prev_price) if prev_price else None  

            if prev_price is None or price != prev_price:
                # Update Redis values using the RedisManager's methods
                self.redis_manager.set_cached("last_btc_price", str(price))
                self.redis_manager.set_cached("last_btc_volume", str(volume if volume else 0))
                
                # Store combined price and volume data
                combined_data = f"{price},{volume}"
                self.redis_manager.lpush("btc_movement_history", combined_data)
                self.redis_manager.ltrim("btc_movement_history", -100, -1)
                
                abs_change = abs(price - prev_price) if prev_price is not None else 0
                abs_change_scaled = abs_change * 100
                self.redis_manager.lpush("abs_price_change_history", str(abs_change_scaled))
                self.redis_manager.ltrim("abs_price_change_history", -100, -1)
                self.redis_manager.set_cached("prev_btc_price", str(price))
                
                # Add last update time
                self.redis_manager.set_cached("last_btc_update_time", str(time.time()))
                
                # Update Fibonacci levels every 100 price updates or when significant movement occurs
                update_fibonacci = False
                fibonacci_update_count = self.redis_manager.get_cached("fibonacci_update_count")
                if fibonacci_update_count:
                    count = int(fibonacci_update_count)
                    if count >= 100:
                        update_fibonacci = True
                        self.redis_manager.set_cached("fibonacci_update_count", "0")
                    else:
                        self.redis_manager.set_cached("fibonacci_update_count", str(count + 1))
                else:
                    self.redis_manager.set_cached("fibonacci_update_count", "1")
                
                # Also update Fibonacci on significant price movement
                if prev_price and abs(price - prev_price) / prev_price > 0.01:  # 1% change
                    update_fibonacci = True
                
                if update_fibonacci:
                    # Get price history for high and low calculation
                    history = self.redis_manager.lrange("btc_movement_history", 0, -1)
                    if history:
                        prices = []
                        for item in history:
                            if "," in item:
                                price_str, _ = item.split(",")
                                prices.append(float(price_str))
                            else:
                                prices.append(float(item))
                        
                        if prices:
                            high_price = max(prices)
                            low_price = min(prices)
                            calculate_fibonacci_levels(high_price, low_price)
                
                log_rasta(f"Redis Updated: BTC Price = {price:.2f}, Volume = {volume}, Abs Change = {abs_change_scaled:.2f}", GREEN_RASTA)
                
                # Notify the high frequency detector about price update
                if mm_trap_detector_available and hf_detector:
                    try:
                        # Update the detector with the new price
                        timestamp = datetime.now(UTC)
                        hf_detector.update_price_data(price, timestamp)
                        
                        # Check for high frequency mode activation
                        hf_active, multiplier = hf_detector.detect_high_freq_trap_mode(price)
                        if hf_active:
                            log_rasta(f"⚠️ HIGH FREQUENCY TRAP MODE ACTIVATED! Multiplier: {multiplier}", RED_RASTA, "warning")
                    except Exception as e:
                        log_rasta(f"Error using MM Trap Detector: {e}", YELLOW_RASTA, "warning")
                else:
                    # Only display the warning once by checking if the flag has changed
                    if self.redis_manager.get_cached("mm_trap_detector_warning_shown") != "1":
                        log_rasta("MM Trap Detector module not available", YELLOW_RASTA, "warning")
                        self.redis_manager.set_cached("mm_trap_detector_warning_shown", "1")
            else:
                log_rasta(f"Price Unchanged, Skipping Redis Update: {price}", YELLOW_RASTA)

        except Exception as e:
            log_rasta(f"Redis Update Failed: {e}", RED_RASTA, "error")
            # Attempt to reconnect
            try:
                self.redis_manager = RedisManager()
                self.redis_manager.ping()
            except:
                log_rasta("Redis reconnection failed.", RED_RASTA, "error")

    def get_current_price(self) -> float:
        """Get the latest BTC price with divine accuracy."""
        try:
            # Try to get from Redis first
            price_data = self.redis_manager.get_cached("last_btc_price")
            if price_data:
                return float(price_data)
        except Exception as e:
            log_rasta(f"Error getting price from Redis: {e}", RED_RASTA, "error")
        
        # If Redis failed, ensure WebSocket is running
        self.connect_websocket()
        
        # Wait briefly for price update
        time.sleep(0.5)
        try:
            price_data = self.redis_manager.get_cached("last_btc_price")
            if price_data:
                return float(price_data)
        except Exception as e:
            log_rasta(f"Error getting price after WebSocket update: {e}", RED_RASTA, "error")
        
        return 0.0
    
    def _fetch_price_from_source(self, source: PriceSource) -> float:
        """Fetch price from the specified source with divine accuracy."""
        try:
            # Get the latest price from Redis
            price_data = self.redis_manager.get_cached("last_btc_price")
            if price_data:
                return float(price_data)
            
            # If Redis doesn't have the price, ensure WebSocket is running
            if source == PriceSource.BINANCE:
                self.connect_websocket()
                time.sleep(0.5)
                price_data = self.redis_manager.get_cached("last_btc_price")
                if price_data:
                    return float(price_data)
            
            return 0.0
            
        except Exception as e:
            log_rasta(f"Error fetching price from {source}: {e}", RED_RASTA, "error")
            return 0.0
    
    def _aggregate_prices(self) -> float:
        """Calculate aggregate price with divine wisdom."""
        prices = []
        for source in self.sources:
            price = self._fetch_price_from_source(source)
            if price > 0:
                prices.append(price)
                
        if prices:
            # Calculate divine average
            return sum(prices) / len(prices)
        return 0.0
    
    def get_price_history(self, minutes: int = 5, count: int = 100) -> List[Dict[str, Union[float, str]]]:
        """Get price history with divine timestamps."""
        key = f"omega:btc_movements_{minutes}min"
        history = []
        
        try:
            # Get data from Redis with JAH BLESSING
            raw_data = self.redis_manager.lrange(key, 0, count-1)
            if not raw_data:
                # Try the main btc_movement_history key
                raw_data = self.redis_manager.lrange("btc_movement_history", 0, count-1)
                
            if raw_data:
                for item in raw_data:
                    try:
                        # Try to parse as JSON first (for formatted data)
                        data_item = json.loads(item)
                        history.append(data_item)
                    except json.JSONDecodeError:
                        # Handle raw format "price,volume"
                        if "," in item:
                            try:
                                price_str, volume_str = item.split(",")
                                price = float(price_str)
                                volume = float(volume_str)
                                timestamp = datetime.now(UTC).isoformat()
                                history.append({
                                    "price": price,
                                    "volume": volume,
                                    "timestamp": timestamp
                                })
                            except Exception:
                                # Fallback to just price
                                price = float(item)
                                history.append({
                                    "price": price,
                                    "timestamp": datetime.now(UTC).isoformat()
                                })
                        else:
                            # Simple price format
                            price = float(item)
                            history.append({
                                "price": price,
                                "timestamp": datetime.now(UTC).isoformat()
                            })
        except Exception as e:
            log_rasta(f"Error getting price history: {e}", RED_RASTA, "error")
            
        return history
    
    def update_price(self, price: float) -> bool:
        """Update price with divine blessing."""
        try:
            # Create price data with divine timestamp
            now = datetime.now(UTC)
            price_data = {
                "price": price,
                "timestamp": now.isoformat(),
                "source": "divine_aggregator"
            }
            price_json = json.dumps(price_data)
            
            # Store last price with consistent key
            self.redis_manager.set_cached("last_btc_price", price)
            
            # Store in various time-based lists
            for minutes in [1, 5, 15, 60]:
                key = f"btc_movements_{minutes}min"
                self.redis_manager.lpush(key, price_json)
                self.redis_manager.ltrim(key, 0, 1000)
                
            return True
            
        except Exception as e:
            log_rasta(f"Error updating price: {e}", RED_RASTA, "error")
            return False
    
    def start(self) -> None:
        """Start the blessed price feed."""
        if self.is_running:
            return
            
        self.is_running = True
        
        def update_loop() -> None:
            while self.is_running:
                try:
                    price = self._aggregate_prices()
                    if price > 0:
                        self.update_price(price)
                except Exception as e:
                    log_rasta(f"Error in update loop: {e}", RED_RASTA, "error")
                finally:
                    time.sleep(self.update_interval)
        
        self._ws_thread = threading.Thread(target=update_loop)
        self._ws_thread.daemon = True
        self._ws_thread.start()
        
    def stop(self) -> None:
        """Stop the blessed price feed."""
        self.is_running = False
        if self._ws_thread:
            self._ws_thread.join()

if __name__ == "__main__":
    display_rasta_banner()
    
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
        
    log_rasta("Initializing Rasta Price Feed with Fibonacci Alignment...", GREEN_RASTA)
    log_rasta(f"Redis Host: {os.getenv('REDIS_HOST', 'localhost')}", BLUE_RASTA)
    log_rasta("Connecting to Binance WebSocket...", BLUE_RASTA)
    
    # Initialize with default Fibonacci levels
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    redis_manager = RedisManager(host=redis_host, port=redis_port)
    
    # Check if we need to initialize Fibonacci levels
    try:
        fib_levels = redis_manager.safe_get("fibonacci_levels")
        if not fib_levels:
            # Default levels based on current BTC price range
            default_high = 85000
            default_low = 83000
            calculate_fibonacci_levels(default_high, default_low)
            log_rasta(f"Initialized default Fibonacci levels: High=${default_high}, Low=${default_low}", CYAN_RASTA)
    except Exception as e:
        log_rasta(f"Error checking fibonacci_levels: {str(e)}, reinitializing...", YELLOW_RASTA, "warning")
        # Delete and recreate the key
        try:
            redis_manager.delete("fibonacci_levels")
            # Default levels based on current BTC price range
            default_high = 85000
            default_low = 83000
            calculate_fibonacci_levels(default_high, default_low)
            log_rasta(f"Reinitialized default Fibonacci levels: High=${default_high}, Low=${default_low}", CYAN_RASTA)
        except Exception as e:
            log_rasta(f"Failed to reinitialize fibonacci_levels: {e}", RED_RASTA, "error")
        
    log_rasta("🔱 Fibonacci Alignment Active - Sacred Architecture (1)", MAGENTA_RASTA)
    
    # Start the WebSocket connection
    start_btc_websocket()