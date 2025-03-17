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

import datetime
import redis
import time
import json
import traceback
from typing import Tuple, Dict, Any, Optional

from rq import Queue
import numpy as np

from omega_ai.alerts.alerts_orchestrator import send_alert
from omega_ai.algos.omega_algorithms import OmegaAlgo
from omega_ai.db_manager.database import insert_mm_trap, insert_subtle_movement
from omega_ai.mm_trap_detector.high_frequency_detector import register_trap_detection

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

# ✅ Redis Connection & Queue Setup
redis_conn = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
mm_queue = Queue("mm_trap_queue", connection=redis_conn)

# ✅ Dynamic MM Detection Thresholds
SCHUMANN_THRESHOLD = 10.0
VOLATILITY_MULTIPLIER = 2.5
MIN_LIQUIDITY_GRAB_THRESHOLD = 250
PRICE_DROP_THRESHOLD = -0.02  # 2% drop
PRICE_PUMP_THRESHOLD = 0.02   # 2% pump
CHECK_INTERVAL = 15
ROLLING_WINDOW = 50

# ✅ UI Helper Functions
def print_header(text):
    """Print a nicely formatted header."""
    print(f"\n{BLUE_BG}{WHITE}{BOLD} {text} {RESET}")

def print_section(title):
    """Print a section divider with title."""
    print(f"\n{MAGENTA}{'─' * 5} {title} {'─' * 5}{RESET}")

def print_price_update(price, prev_price, abs_change, pct_change):
    """Print price update with visual indicators."""
    # Format percentage change with color and arrow
    if pct_change > 0:
        pct_str = f"{GREEN}↑ {pct_change:.2%}{RESET}"
    elif pct_change < 0:
        pct_str = f"{RED}↓ {pct_change:.2%}{RESET}"
    else:
        pct_str = f"{BLUE}→ {pct_change:.2%}{RESET}"
        
    # Print formatted price info
    print(f"{WHITE}BTC Price: ${price:.2f} ({pct_str}) | Change: ${abs_change:.2f}{RESET}")

def print_analysis_result(analysis, threshold):
    """Print analysis results in a formatted block."""
    print_section("MOVEMENT ANALYSIS")
    
    if "Organic" in analysis:
        confidence = "HIGH" if "High" in analysis else "MEDIUM"
        print(f"{GREEN}✓ {analysis}{RESET}")
        print(f"{GREEN}✓ Confidence: {confidence}{RESET}")
    elif "Trap" in analysis or "Manipulation" in analysis:
        print(f"{RED}⚠ {analysis}{RESET}")
        print(f"{RED}⚠ Detection Threshold: ${threshold:.2f}{RESET}")
    else:
        print(f"{BLUE}ℹ {analysis}{RESET}")

def print_movement_tag(tag):
    """Print movement classification tag with appropriate color."""
    if "Pump" in tag:
        print(f"\n{GREEN_BG}{WHITE}{BOLD} {tag} {RESET}")
    elif "Dump" in tag:
        print(f"\n{RED_BG}{WHITE}{BOLD} {tag} {RESET}")
    elif "Liquidity" in tag:
        print(f"\n{YELLOW_BG}{BLACK_BG}{BOLD} {tag} {RESET}")
    elif "Organic" in tag:
        print(f"\n{BLUE_BG}{WHITE}{BOLD} {tag} {RESET}")
    else:
        print(f"\n{CYAN} {tag} {RESET}")

def print_alert(message):
    """Print attention-grabbing alert."""
    print(f"\n{RED_BG}{WHITE}{BOLD} ALERT! {RESET} {message}")

# ✅ Enhanced Price Fetching with Multiple Fallbacks
def get_resilient_btc_price() -> Tuple[float, float, bool]:
    """
    Get BTC price with multi-level fallback mechanisms for high resilience.
    
    Returns:
        Tuple of (current_price, prev_price, is_fallback)
    """
    current_price = None
    prev_price = None
    is_fallback = False
    
    # Try to get current price (last_btc_price)
    try:
        latest_price_bytes = redis_conn.get("last_btc_price")
        if latest_price_bytes:
            current_price = float(latest_price_bytes)
    except (ValueError, TypeError):
        print(f"{YELLOW}⚠️ Warning: Invalid data in last_btc_price{RESET}")
    
    # If current price not available, try fallbacks
    if current_price is None:
        # Fallback 1: Try prev_btc_price
        try:
            prev_price_bytes = redis_conn.get("prev_btc_price")
            if prev_price_bytes:
                current_price = float(prev_price_bytes)
                is_fallback = True
                print(f"{YELLOW}⚠️ Using prev_btc_price as fallback: ${current_price}{RESET}")
        except (ValueError, TypeError):
            print(f"{YELLOW}⚠️ Warning: Invalid data in prev_btc_price{RESET}")
    
        # Fallback 2: Try btc_movement_history
        if current_price is None:
            try:
                # Get latest movement
                movements = redis_conn.lrange("btc_movement_history", 0, 0)
                if movements:
                    movement_data = json.loads(movements[0])
                    current_price = float(movement_data.get("price", 0))
                    is_fallback = True
                    print(f"{YELLOW}⚠️ Using btc_movement_history as fallback: ${current_price}{RESET}")
            except (json.JSONDecodeError, ValueError, TypeError, IndexError):
                print(f"{YELLOW}⚠️ Warning: Invalid data in btc_movement_history{RESET}")
        
        # Fallback 3: Try timeframe data
        if current_price is None:
            for timeframe in ['1m', '5m', '15m', '1h']:
                try:
                    # Get latest price data for this timeframe
                    key = f"btc_price_data:{timeframe}"
                    data = redis_conn.lrange(key, -1, -1)
                    if data:
                        price_data = json.loads(data[0])
                        current_price = float(price_data.get('close', 0))
                        is_fallback = True
                        print(f"{YELLOW}⚠️ Using {timeframe} data as fallback: ${current_price}{RESET}")
                        break
                except (json.JSONDecodeError, ValueError, TypeError, IndexError):
                    continue
    
    # Get previous price with fallbacks
    if prev_price is None:
        # Try getting from Redis directly
        try:
            prev_price_bytes = redis_conn.get("prev_btc_price")
            if prev_price_bytes:
                prev_price = float(prev_price_bytes)
        except (ValueError, TypeError):
            pass
        
        # Fallback: Use history or generate synthetic
        if prev_price is None and current_price is not None:
            try:
                # Try to get from movements history
                movements = redis_conn.lrange("btc_movement_history", 0, 1)
                if len(movements) >= 2:
                    movement_data = json.loads(movements[1])  # Second most recent
                    prev_price = float(movement_data.get("price", 0))
                else:
                    # Generate synthetic previous price
                    prev_price = current_price * 0.999
            except (json.JSONDecodeError, ValueError, TypeError, IndexError):
                # Last resort: synthetic price
                if current_price is not None:
                    prev_price = current_price * 0.999
    
    # If all fallbacks failed, return zeros with warning
    if current_price is None:
        print(f"{RED}❌ ERROR: Could not obtain BTC price from any source{RESET}")
        return 0.0, 0.0, True
        
    return current_price, prev_price or (current_price * 0.999), is_fallback

# ✅ Main Process Function
def process_mm_trap():
    """Continuously pulls BTC price, checking for MM traps while storing subtle movements."""
    # Keep last seen price in memory to ensure we always have a different previous price
    last_processed_price = None

    while True:
        # Sleep at the beginning to allow the test to mock it and prevent infinite loops
        time.sleep(CHECK_INTERVAL)
        
        timestamp = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M:%S')
        print_header(f"BTC CHECK | {timestamp}")

        # ✅ Fetch latest BTC price & volume with enhanced resilience
        price, prev_price, is_fallback = get_resilient_btc_price()
        volume = 0
        
        try:
            volume_bytes = redis_conn.get("btc_volume")
            if volume_bytes:
                volume = float(volume_bytes)
        except (ValueError, TypeError):
            pass
            
        # Skip processing if we have no valid data
        if price == 0:
            print(f"{RED}❌ No valid price data available, skipping check{RESET}")
            
            # Check if we're in test mode - if so, exit after this iteration
            if hasattr(process_mm_trap, '_test_single_run') and process_mm_trap._test_single_run:
                return
            continue

        # If we have a last processed price, use that to ensure continuity
        if last_processed_price:
            prev_price = last_processed_price
        
        # ✅ Compute Price Changes
        price_change = (price - prev_price) / prev_price if prev_price != 0 else 0
        absolute_change = abs(price - prev_price)
        
        # Print formatted price update
        print_price_update(price, prev_price, absolute_change, price_change)

        # ✅ Update Redis with current price for other components to use
        redis_conn.set("prev_btc_price", price)
        print(f"{CYAN}ℹ Updating prev_btc_price: {prev_price:.2f} → {price:.2f}{RESET}")

        # ✅ Store absolute price change history
        redis_conn.rpush("abs_price_change_history", absolute_change)
        redis_conn.ltrim("abs_price_change_history", -100, -1)

        # ✅ Compute Dynamic Threshold with Market Regime Awareness
        dynamic_liquidity_grab_threshold = OmegaAlgo.calculate_dynamic_threshold()
        print(f"{WHITE}Current Threshold: ${dynamic_liquidity_grab_threshold:.2f}{RESET}")

        # ✅ Run the Multi-Layer Fibo-Organic Check WITH Volume
        movement_analysis = OmegaAlgo.is_fibo_organic(price, prev_price, volume)
        print_analysis_result(movement_analysis, dynamic_liquidity_grab_threshold)

        # ✅ NEW: Run Fibonacci multi-timeframe trend analysis
        print(f"\n{MAGENTA}⏳ Running Fibonacci multi-timeframe trend analysis...{RESET}")
        timeframe_trends = OmegaAlgo.analyze_multi_timeframe_trends(price)

        # ✅ Always store subtle movement data for historical analysis
        current_timestamp = datetime.datetime.now(datetime.UTC)
        movement_tag = "Stable"  # Default if no major move detected
        trap_type = None  # Initialize trap_type
        trap_confidence = 0  # Initialize trap_confidence
        alert_msg = None  # Initialize alert_msg

        # First check for special patterns
        if "Stealth Accumulation" in movement_analysis:
            movement_tag = "Stealth Accumulation"
            trap_type = "Stealth Accumulation"
            trap_confidence = 0.75
            alert_msg = f"{CYAN}⚠️ STEALTH ACCUMULATION DETECTED! BTC moved ${absolute_change:.2f}{RESET}"
        elif "Fractal Pattern" in movement_analysis:
            movement_tag = "Fractal Trap"
            trap_type = "Fractal Trap"
            trap_confidence = 0.85
            alert_msg = f"{MAGENTA}⚠️ FRACTAL TRAP DETECTED! BTC moved ${absolute_change:.2f}{RESET}"
        elif "Time-Based Pattern" in movement_analysis:
            movement_tag = "Time Dilation Trap"
            trap_type = "Time Dilation Trap"
            trap_confidence = 0.8
            alert_msg = f"{YELLOW}⚠️ TIME DILATION TRAP DETECTED! BTC moved ${absolute_change:.2f}{RESET}"
        # Then check for threshold-based traps if no special pattern was detected
        elif absolute_change > dynamic_liquidity_grab_threshold:
            movement_tag = "Liquidity Grab"
            trap_type = "Liquidity Grab"
            trap_confidence = 0.9
            alert_msg = f"{RED}⚠️ LIQUIDITY GRAB DETECTED! BTC moved ${absolute_change:.2f}{RESET}"
        elif absolute_change > dynamic_liquidity_grab_threshold * 0.5:
            # Check if this could be a half-fake move
            if "Trap" in movement_analysis or "Manipulation" in movement_analysis:
                movement_tag = "Half-Liquidity Grab"
                trap_type = "Half-Liquidity Grab"
                trap_confidence = 0.7
                alert_msg = f"{LIGHT_ORANGE}⚠️ HALF-LIQUIDITY GRAB DETECTED! BTC moved ${absolute_change:.2f}{RESET}"
        elif price_change > PRICE_PUMP_THRESHOLD:
            if "Trap" in movement_analysis or "Manipulation" in movement_analysis:
                movement_tag = "Fake Pump"
                trap_type = "Fake Pump"
                trap_confidence = 0.85
                alert_msg = f"{BRIGHT_GREEN}⚠️ FAKE PUMP DETECTED! BTC jumped {price_change:.2%} rapidly!{RESET}"
            else:
                movement_tag = "Potential Fake Pump"
                trap_type = "Potential Fake Pump"
                trap_confidence = 0.6
                alert_msg = f"{GREEN}⚠️ POTENTIAL FAKE PUMP! BTC jumped {price_change:.2%}{RESET}"
        elif price_change < PRICE_DROP_THRESHOLD:
            if "Trap" in movement_analysis or "Manipulation" in movement_analysis:
                movement_tag = "Fake Dump"
                trap_type = "Fake Dump"
                trap_confidence = 0.85
                alert_msg = f"{RED}⚠️ FAKE DUMP DETECTED! BTC dropped {price_change:.2%} rapidly!{RESET}"
            else:
                movement_tag = "Potential Fake Dump"
                trap_type = "Potential Fake Dump"
                trap_confidence = 0.6
                alert_msg = f"{LIGHT_ORANGE}⚠️ POTENTIAL FAKE DUMP! BTC dropped {price_change:.2%}{RESET}"
        elif 0.01 <= price_change < PRICE_PUMP_THRESHOLD:
            movement_tag = "Half-Fake Pump"
            trap_type = "Half-Fake Pump"
            trap_confidence = 0.5
            alert_msg = f"{GREEN}⚠️ HALF-FAKE PUMP! BTC moved {price_change:.2%}{RESET}"
        elif PRICE_DROP_THRESHOLD < price_change <= -0.01:
            movement_tag = "Half-Fake Dump"
            trap_type = "Half-Fake Dump"
            trap_confidence = 0.5
            alert_msg = f"{LIGHT_ORANGE}⚠️ HALF-FAKE DUMP! BTC moved {price_change:.2%}{RESET}"

        # Store the subtle movement
        insert_subtle_movement(
            timestamp=current_timestamp,
            price=price,
            prev_price=prev_price,
            abs_change=absolute_change,
            price_change=price_change,
            movement_tag=movement_tag,
            volume=volume
        )
        
        # Print movement classification
        print_movement_tag(movement_tag)

        # ✅ Store MM Trap & Trigger Alert if Needed
        if trap_type and alert_msg:
            print_alert(alert_msg)
            # Store trap with confidence level
            insert_mm_trap(price, price_change, trap_type, trap_confidence)
            send_alert(alert_msg, trap_type)
            
            # Register this trap with the high-frequency detector
            register_trap_detection(trap_type, trap_confidence, price_change)
            
            # Store for Grafana visualization
            redis_conn.hset(
                f"mm_trap:{int(time.time())}", 
                mapping={
                    "type": trap_type,
                    "confidence": str(trap_confidence),
                    "price": str(price),
                    "change": str(price_change),
                    "timestamp": timestamp
                }
            )
        else:
            # Store organic movement data if no trap detected
            if "Organic" in movement_analysis:
                redis_conn.hset(
                    f"organic_move:{int(time.time())}", 
                    mapping={
                        "type": "Organic",
                        "confidence": "0.8" if "High" in movement_analysis else "0.6",
                        "price": str(price),
                        "change": str(price_change),
                        "timestamp": timestamp
                    }
                )

        # ✅ Store core metrics for Grafana Monitoring
        redis_conn.rpush("liquidity_grab_history", absolute_change)
        redis_conn.ltrim("liquidity_grab_history", -100, -1)

        redis_conn.rpush("fib_match_history", 1 if "Organic" in movement_analysis else 0)
        redis_conn.ltrim("fib_match_history", -100, -1)

        redis_conn.rpush("price_volatility_history", dynamic_liquidity_grab_threshold)
        redis_conn.ltrim("price_volatility_history", -100, -1)
        
        redis_conn.set("latest_movement_analysis", movement_analysis)
        
        # Footer with next check time
        next_check = (datetime.datetime.now() + datetime.timedelta(seconds=CHECK_INTERVAL)).strftime('%H:%M:%S')
        print(f"\n{BLUE}Next check at {next_check}{RESET}")
        print(f"{BLUE}{'─' * 70}{RESET}")
        
        # Store current price for next run
        last_processed_price = price
        
        # Check if we're in test mode - if so, exit after this iteration
        if hasattr(process_mm_trap, '_test_single_run') and process_mm_trap._test_single_run:
            return

# NOW it's safe to set attributes on the function after it's defined
process_mm_trap._test_single_run = False

# ✅ Main entry point
if __name__ == "__main__":
    print(f"\n{BLUE_BG}{WHITE}{BOLD} 🚀 MM TRAP DETECTOR v1.0 {RESET}")
    print(f"{GOLD}Watching for market manipulation... Babylon can't hide! 🔱{RESET}\n")
    
    # Initialize Last BTC Price
    price, prev_price, is_fallback = get_resilient_btc_price()
    
    if price > 0:
        print(f"{GOLD}🔰 Last Recorded BTC Price: ${price:.2f}{RESET}")
        if is_fallback:
            print(f"{YELLOW}⚠️ Using fallback price source{RESET}")
    else:
        print(f"{GOLD}🔰 No BTC price data available yet. Waiting for first update...{RESET}")

    process_mm_trap()
