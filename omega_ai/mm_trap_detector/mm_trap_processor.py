"""
Market Maker Trap Detection Processor
====================================

This module implements a real-time Bitcoin price movement analyzer that identifies potential
market maker (MM) manipulation tactics such as liquidity grabs, fake pumps, and fake dumps.
It uses dynamic thresholds, Fibonacci patterns, and multi-timeframe analysis to distinguish
between organic market movements and manipulated price action.

Objective
---------
The primary objective is to detect market maker manipulation tactics in real-time by analyzing
price movements against dynamically calculated thresholds that adapt to current market volatility
and conditions, while incorporating Schumann resonance data for enhanced detection.

Key Features
-----------
1. Dynamic Threshold Calculation: Adjusts detection sensitivity based on recent market
   volatility, market regime, and Schumann resonance correlations.

2. Multi-Layer Detection System: Identifies several types of MM manipulation:
   - Full Liquidity Grabs (large sudden price movements)
   - Half-Liquidity Grabs (movements exceeding 50% of the threshold)
   - Fake Pumps/Dumps (rapid directional moves with manipulation characteristics)
   - Half-Fake Pumps/Dumps (smaller moves that may be early stages of manipulation)

3. Fibonacci-Organic Analysis: Determines whether price movements follow natural Fibonacci
   patterns or exhibit artificial characteristics typical of market manipulation.

4. Confidence Scoring: Assigns confidence levels to detected manipulations based on
   multiple factors including price velocity, pattern matching, and volume analysis.

5. Historical Movement Storage: Records all price movements, even subtle ones, to build
   datasets for pattern recognition and machine learning.

Visual Interface
---------------
The module provides a rich, color-coded terminal output for real-time monitoring:
- RED: Major manipulations and warnings
- GREEN/BRIGHT_GREEN: Bullish movements and fake pumps
- LIGHT_ORANGE/YELLOW: Caution signals and fake dumps
- BLUE/CYAN: Informational data and stable movements
- MAGENTA: Headers and processing indicators
- Background colors for important alerts and classifications

Technical Implementation
-----------------------
- Pulls real-time BTC price data from Redis
- Calculates dynamic thresholds based on market conditions
- Applies multi-factor analysis to detect manipulation patterns
- Stores detected traps in PostgreSQL database
- Sends alerts through the alerts orchestration system
- Registers events with the high-frequency detector for back-to-back pattern detection
- Stores metrics in Redis for Grafana visualization

Usage
-----
The module can be run directly to start continuous monitoring:
```
python -m omega_ai.mm_trap_detector.mm_trap_processor
````

Dependencies
-----------
- redis: For real-time data storage and retrieval
- numpy: For statistical calculations
- omega_ai.alerts.alerts_orchestrator: For sending alerts
- omega_ai.algos.omega_algorithms: For Fibonacci and market regime analysis
- omega_ai.db_manager.database: For persistent storage of detected traps
- omega_ai.mm_trap_detector.high_frequency_detector: For trap event registration

Author: OmegaBTC Team
Version: 1.0
"""

from datetime import datetime, UTC
import redis
import time
from rq import Queue
import asyncio
from influxdb_client.client.influxdb_client import InfluxDBClient
from omega_ai.algos.omega_algorithms import OmegaAlgo
from omega_ai.db_manager.database import insert_mm_trap, insert_subtle_movement
from omega_ai.mm_trap_detector.high_frequency_detector import register_trap_detection
from omega_ai.config import (
    REDIS_HOST, REDIS_PORT, INFLUXDB_URL, INFLUXDB_TOKEN, 
    INFLUXDB_ORG, INFLUXDB_BUCKET, MONITORING_INTERVAL, 
    ERROR_RETRY_INTERVAL, PRICE_PUMP_THRESHOLD, PRICE_DROP_THRESHOLD,
    BASE_TRAP_THRESHOLD
)
from typing import Optional, Dict, Any, Union

# ✅ Enhanced Terminal Colors for better visualization
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
BRIGHT_GREEN = "\033[96m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
GOLD = "\033[93m"
YELLOW = "\033[93m"
LIGHT_ORANGE = "\033[38;5;214m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BLACK_BG = "\033[40m"
BLUE_BG = "\033[44m"
GREEN_BG = "\033[42m"
RED_BG = "\033[41m"
YELLOW_BG = "\033[43m"
BOLD = "\033[1m"

# ✅ Redis Queue & Connection Setup
redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
mm_queue = Queue("mm_trap_queue", connection=redis_conn)

# ✅ Dynamic MM Detection Thresholds
SCHUMANN_THRESHOLD = 10.0
VOLATILITY_MULTIPLIER = 2.5
MIN_LIQUIDITY_GRAB_THRESHOLD = 250

# Initialize Redis connection
redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def initialize_influxdb() -> None:
    """Initialize InfluxDB connection."""
    global influxdb_client
    try:
        influxdb_client = InfluxDBClient(
            url=INFLUXDB_URL,
            token=INFLUXDB_TOKEN,
            org=INFLUXDB_ORG
        )
        # Test the connection
        influxdb_client.ping()
    except Exception as e:
        print(f"❌ Error connecting to InfluxDB: {str(e)}")
        raise

def get_current_btc_price() -> float:
    """Get the current BTC price from Redis."""
    try:
        price = redis_conn.get("last_btc_price")
        if price is None:
            raise ValueError("No BTC price available in Redis")
        return float(price)
    except (ValueError, TypeError) as e:
        print(f"❌ Error getting BTC price: {str(e)}")
        return 0.0

def get_current_volume() -> float:
    """Get the current trading volume from Redis."""
    try:
        volume = redis_conn.get("last_btc_volume")
        if volume is None:
            return 0.0
        return float(volume)
    except (ValueError, TypeError):
        return 0.0

def check_high_frequency_mode() -> bool:
    """Check if high-frequency mode is active."""
    try:
        hf_mode = redis_conn.get("high_frequency_mode")
        return bool(int(hf_mode)) if hf_mode is not None else False
    except (ValueError, TypeError):
        return False

def calculate_dynamic_threshold(hf_mode: bool) -> float:
    """Calculate dynamic threshold based on market conditions."""
    try:
        # Get rolling volatility from Redis
        volatility = redis_conn.get("rolling_volatility")
        base_threshold = float(volatility) if volatility else BASE_TRAP_THRESHOLD
        
        # Get market regime from Redis
        market_regime = redis_conn.get("market_regime")
        regime = str(market_regime) if market_regime else "normal"
        
        # Adjust threshold based on market regime
        regime_multiplier = {
            "trending": 1.5,
            "volatile": 0.75,
            "normal": 1.0
        }.get(regime, 1.0)
        
        # Calculate directional strength
        directional_strength_str = redis_conn.get("directional_strength")
        directional_strength = float(directional_strength_str) if directional_strength_str else 0.5
        
        # Apply adjustments
        adjusted_threshold = base_threshold * regime_multiplier
        if hf_mode:
            adjusted_threshold *= 0.5  # More sensitive in HF mode
        
        # Debug output
        print(f"📡 [DEBUG] Rolling Volatility: ${base_threshold:.2f} | Market Regime: {regime} | HF Mode: {'active' if hf_mode else 'inactive'} ({regime_multiplier:.2f}x) | Adjusted Threshold: ${adjusted_threshold:.2f}")
        
        return adjusted_threshold
        
    except Exception as e:
        print(f"❌ Error calculating dynamic threshold: {str(e)}")
        return BASE_TRAP_THRESHOLD  # Default threshold

def register_trap_detection(price: float, volume: float, price_change: float = 0.0) -> None:
    """Register a trap detection event."""
    try:
        timestamp = datetime.now(UTC).isoformat()
        redis_conn.hset(
            f"trap_detection:{int(datetime.now(UTC).timestamp())}",
            mapping={
                "price": str(price),
                "volume": str(volume),
                "price_change": str(price_change),
                "timestamp": timestamp
            }
        )
    except Exception as e:
        print(f"❌ Error registering trap detection: {str(e)}")

# ✅ UI Helper Functions
def print_header(text):
    """Print a nicely formatted header."""
    width = 70
    print(f"\n{BLUE_BG}{WHITE}{BOLD} {text} {' ' * (width - len(text) - 2)}{RESET}")

def print_section(title):
    """Print a section divider with title."""
    print(f"\n{CYAN}{'═' * 25} {title} {'═' * 25}{RESET}")

def print_price_update(price, prev_price, abs_change, pct_change):
    """Print price update with visual indicators."""
    direction = "↑" if price > prev_price else "↓" if price < prev_price else "→"
    color = GREEN if price > prev_price else RED if price < prev_price else BLUE
    
    print_section("PRICE UPDATE")
    print(f"{WHITE}Current BTC: {color}${price:.2f} {direction}{RESET}")
    print(f"{WHITE}Previous:    ${prev_price:.2f}{RESET}")
    print(f"{WHITE}Abs Change:  {color}${abs_change:.2f}{RESET}")
    print(f"{WHITE}% Change:    {color}{pct_change:.4%}{RESET}")

async def analyze_movement(current_btc_price: float, prev_btc_price: float, volume: float) -> str:
    """Analyze the current price movement for potential market manipulation."""
    try:
        # Get the analysis result from OmegaAlgo
        analysis = await OmegaAlgo.is_fibo_organic(current_btc_price, prev_btc_price, volume)
        return analysis
    except Exception as e:
        print(f"❌ Error in analyze_movement: {str(e)}")
        return "Error in analysis"

async def print_analysis_result(analysis: str, threshold: float) -> None:
    """Print the analysis result with appropriate formatting."""
    try:
        if "Organic" in analysis:
            print(f"{GREEN}✅ ORGANIC MOVEMENT - No manipulation detected{RESET}")
        elif "Insufficient" in analysis:
            print(f"{YELLOW}⚠️  {analysis}{RESET}")
        else:
            print(f"{RED}⛔️ POTENTIAL MANIPULATION DETECTED - {analysis}{RESET}")
            
        print(f"\nCurrent Threshold: ${threshold:.2f}")
    except Exception as e:
        print(f"❌ Error in print_analysis_result: {str(e)}")

async def process_mm_trap() -> None:
    """Main function to process market maker trap detection."""
    try:
        # Initialize InfluxDB connection
        initialize_influxdb()
        print("✅ Connected to InfluxDB\n")
        
        print("\n 🚀 MM TRAP DETECTOR v1.0 ")
        print("Watching for market manipulation... Babylon can't hide! 🔱\n")
        
        # Get initial BTC price
        current_btc_price = get_current_btc_price()
        prev_btc_price = current_btc_price
        print(f"🔰 Last Recorded BTC Price: ${current_btc_price:.2f}\n")
        
        while True:
            try:
                current_time = datetime.now(UTC)
                print(f"\n BTC CHECK | {current_time.strftime('%Y-%m-%d %H:%M:%S')} \n")
                print("═" * 17 + " PRICE UPDATE " + "═" * 17)
                
                # Get current BTC price
                current_btc_price = get_current_btc_price()
                
                # Calculate price changes
                abs_change = current_btc_price - prev_btc_price
                pct_change = (abs_change / prev_btc_price) * 100 if prev_btc_price != 0 else 0
                
                # Print price information
                print(f"Current BTC: ${current_btc_price:.2f} {'↑' if abs_change > 0 else '↓' if abs_change < 0 else '→'}")
                print(f"Previous:    ${prev_btc_price:.2f}")
                print(f"Abs Change:  ${abs_change:.2f}")
                print(f"% Change:    {pct_change:.4f}%")
                
                print(f"ℹ Updating prev_btc_price: {prev_btc_price:.2f} → {current_btc_price:.2f}")
                
                # Update previous price for next iteration
                prev_btc_price = current_btc_price
                
                # Get current volume
                volume = get_current_volume()
                
                # Check for high-frequency mode
                hf_mode = check_high_frequency_mode()
                
                # Calculate dynamic threshold based on market conditions
                dynamic_liquidity_grab_threshold = calculate_dynamic_threshold(hf_mode)
                
                print("\n═" * 17 + " MOVEMENT ANALYSIS " + "═" * 17)
                
                # Analyze the movement
                movement_analysis = await analyze_movement(current_btc_price, prev_btc_price, volume)
                
                # Print analysis result
                await print_analysis_result(movement_analysis, dynamic_liquidity_grab_threshold)
                
                # Register trap detection if needed
                if "TRAP" in movement_analysis:
                    register_trap_detection(current_btc_price, volume, pct_change)
                
                # Sleep for the monitoring interval
                await asyncio.sleep(MONITORING_INTERVAL)
                
            except Exception as e:
                print(f"❌ Error in main loop: {str(e)}")
                await asyncio.sleep(ERROR_RETRY_INTERVAL)
                
    except KeyboardInterrupt:
        print("\n👋 Gracefully shutting down MM Trap Detector...")
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(process_mm_trap())
