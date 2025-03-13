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

# ✅ Redis Queue & Connection Setup
redis_conn = redis.Redis(host="localhost", port=6379, db=0)
mm_queue = Queue("mm_trap_queue", connection=redis_conn)

# ✅ Dynamic MM Detection Thresholds
SCHUMANN_THRESHOLD = 10.0
VOLATILITY_MULTIPLIER = 2.5
MIN_LIQUIDITY_GRAB_THRESHOLD = 250
PRICE_DROP_THRESHOLD = -0.02
PRICE_PUMP_THRESHOLD = 0.02
CHECK_INTERVAL = 15
ROLLING_WINDOW = 50

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
    if "Grab" in tag:
        tag_color = f"{RED_BG}{WHITE}{BOLD}"
    elif "Pump" in tag:
        tag_color = f"{GREEN_BG}{BLACK_BG}{BOLD}"
    elif "Dump" in tag:
        tag_color = f"{YELLOW_BG}{BLACK_BG}{BOLD}"
    elif tag == "Stable":
        tag_color = f"{BLUE_BG}{WHITE}{BOLD}"
    else:
        tag_color = f"{CYAN}"
    
    print(f"\n{WHITE}Movement Classification: {tag_color} {tag} {RESET}")

def print_alert(message):
    """Print attention-grabbing alert."""
    print(f"\n{RED_BG}{WHITE}{BOLD}⚠️  ALERT  ⚠️{RESET}")
    print(f"{message}")

# ✅ Start Worker
if __name__ == "__main__":
    print(f"\n{BLUE_BG}{WHITE}{BOLD} 🚀 MM TRAP DETECTOR v1.0 {RESET}")
    print(f"{GOLD}Watching for market manipulation... Babylon can't hide! 🔱{RESET}\n")
    
    # ✅ Initialize Last BTC Price
    last_stored_price = redis_conn.get("last_btc_price")
    last_stored_price = float(last_stored_price) if last_stored_price else None

    if last_stored_price:
        print(f"{GOLD}🔰 Last Recorded BTC Price: ${last_stored_price:.2f}{RESET}")
    else:
        print(f"{GOLD}🔰 No BTC price data available yet. Waiting for first update...{RESET}")

    # Same process_mm_trap function but with updated print statements
    def process_mm_trap():
        """Continuously pulls BTC price, checking for MM traps while storing subtle movements."""
        global last_fluctuation_check, fluctuation_start_price

        # Keep last seen price in memory to ensure we always have a different previous price
        last_processed_price = None

        while True:
            time.sleep(CHECK_INTERVAL)
            timestamp = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M:%S')
            print_header(f"BTC CHECK | {timestamp}")

            # ✅ Fetch latest BTC price & volume from Redis
            latest_price = redis_conn.get("last_btc_price")
            latest_volume = redis_conn.get("last_btc_volume")

            if latest_price:
                price = float(latest_price)
                volume = float(latest_volume) if latest_volume else 0
            else:
                print(f"{BLUE}⏳ Waiting for first BTC price update...{RESET}")
                continue  # Skip if no price data yet

            # ✅ Use our last processed price as prev_price to ensure we always show changes
            if last_processed_price:
                prev_price = last_processed_price
            else:
                # Only get from Redis if we don't have a locally stored price
                prev_price_redis = redis_conn.get("prev_btc_price")
                
                if prev_price_redis is None:
                    price_history = redis_conn.lrange("btc_movement_history", -2, -1)
                    if len(price_history) >= 2:
                        prev_price = float(price_history[0])
                    else:
                        prev_price = price * 0.999  # Slightly different to show initial change
                else:
                    prev_price = float(prev_price_redis)
            
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

            # ✅ Store subtle price movements in DB regardless of movement type
            movement_tag = "Stable"  # Default if no major move detected
            
            # ✅ NEW: Always store subtle movement data for historical analysis
            current_timestamp = datetime.datetime.now(datetime.UTC)
            insert_subtle_movement(
                timestamp=current_timestamp, 
                price=price, 
                prev_price=prev_price, 
                abs_change=absolute_change, 
                price_change=price_change, 
                movement_tag=movement_tag, 
                volume=volume
            )
            
            # ✅ Detect MM Fakeouts with Dynamic Threshold and Half-Trap Detection
            trap_type = None
            alert_msg = None
            trap_confidence = 0
            
            # Calculate half-threshold for detecting subtle manipulation
            half_threshold = dynamic_liquidity_grab_threshold * 0.5

            # Full Liquidity Grab Detection
            if absolute_change > dynamic_liquidity_grab_threshold:
                trap_type = "Liquidity Grab"
                trap_confidence = 0.9
                alert_msg = f"{RED}⚠️ LIQUIDITY GRAB DETECTED! BTC moved ${absolute_change:.2f}{RESET}"
                movement_tag = "Liquidity Grab"

            # Half-Fake Detection (new feature!)
            elif absolute_change > half_threshold:
                # Check if this could be a half-fake move
                if "Trap" in movement_analysis or "Manipulation" in movement_analysis:
                    trap_type = "Half-Liquidity Grab"
                    trap_confidence = 0.7
                    alert_msg = f"{LIGHT_ORANGE}⚠️ HALF-LIQUIDITY GRAB DETECTED! BTC moved ${absolute_change:.2f}{RESET}"
                    movement_tag = "Half-Liquidity Grab"

            # Fake Pump Detection with confidence levels
            elif price_change > PRICE_PUMP_THRESHOLD:
                if "Trap" in movement_analysis or "Manipulation" in movement_analysis:
                    trap_type = "Fake Pump"
                    trap_confidence = 0.85
                    alert_msg = f"{BRIGHT_GREEN}⚠️ FAKE PUMP DETECTED! BTC jumped {price_change:.2%} rapidly!{RESET}"
                    movement_tag = "Fake Pump"
                else:
                    trap_type = "Potential Fake Pump"
                    trap_confidence = 0.6
                    alert_msg = f"{GREEN}⚠️ POTENTIAL FAKE PUMP! BTC jumped {price_change:.2%}{RESET}"
                    movement_tag = "Potential Fake Pump"

            # Fake Dump Detection with confidence levels
            elif price_change < PRICE_DROP_THRESHOLD:
                if "Trap" in movement_analysis or "Manipulation" in movement_analysis:
                    trap_type = "Fake Dump"
                    trap_confidence = 0.85
                    alert_msg = f"{RED}⚠️ FAKE DUMP DETECTED! BTC dropped {price_change:.2%} rapidly!{RESET}"
                    movement_tag = "Fake Dump"
                else:
                    trap_type = "Potential Fake Dump"
                    trap_confidence = 0.6
                    alert_msg = f"{LIGHT_ORANGE}⚠️ POTENTIAL FAKE DUMP! BTC dropped {price_change:.2%}{RESET}"
                    movement_tag = "Potential Fake Dump"

            # Half-Fake Pump Detection (new feature!)
            elif 0.01 <= price_change < PRICE_PUMP_THRESHOLD:
                trap_type = "Half-Fake Pump"
                trap_confidence = 0.5
                alert_msg = f"{GREEN}⚠️ HALF-FAKE PUMP! BTC moved {price_change:.2%}{RESET}"
                movement_tag = "Half-Fake Pump"
                
            # Half-Fake Dump Detection (new feature!)
            elif PRICE_DROP_THRESHOLD < price_change <= -0.01:
                trap_type = "Half-Fake Dump"
                trap_confidence = 0.5
                alert_msg = f"{LIGHT_ORANGE}⚠️ HALF-FAKE DUMP! BTC moved {price_change:.2%}{RESET}"
                movement_tag = "Half-Fake Dump"
                
            # Print movement classification
            print_movement_tag(movement_tag)
                
            # ✅ UPDATE: Update the movement tag and insert again if it changed after analysis
            if movement_tag != "Stable":
                insert_subtle_movement(
                    timestamp=current_timestamp,
                    price=price,
                    prev_price=prev_price,
                    abs_change=absolute_change,
                    price_change=price_change,
                    movement_tag=movement_tag,
                    volume=volume
                )

            # ✅ Store MM Trap & Trigger Alert if Needed
            if trap_type:
                print_alert(alert_msg)
                # Store trap with confidence level
                insert_mm_trap(price, price_change, trap_type, trap_confidence)
                send_alert(alert_msg)
                
                # ✅ NEW: Register this trap with the high-frequency detector
                register_trap_detection(trap_type, trap_confidence, price_change)
                
                # Store for Grafana visualization
                redis_conn.hset(  # 👈 UPDATED: Changed from hmset to hset with mapping parameter
                    f"mm_trap:{int(time.time())}", 
                    mapping={      # 👈 UPDATED: Added explicit mapping parameter
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
                    redis_conn.hset(  # 👈 UPDATED: Changed from hmset to hset with mapping parameter
                        f"organic_move:{int(time.time())}", 
                        mapping={      # 👈 UPDATED: Added explicit mapping parameter
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

            # At the very end of the loop, store current price for next run
            last_processed_price = price

    process_mm_trap()
