"""
Multi-Timeframe Market Trend Analysis System
============================================

This module provides real-time monitoring and analysis of Bitcoin price movements
across multiple timeframes to detect market trends, potential market maker (MM)
manipulation, and generate actionable insights for traders.

Objective
---------
The primary objective is to simultaneously analyze multiple timeframes (1min, 5min, 10min)
to identify directional biases, trend strength, price momentum shifts, and potential
manipulation tactics employed by market makers.

Key Features
-----------
1. Multi-Timeframe Analysis: Simultaneously monitors 1min, 5min, and 10min charts
   to provide a comprehensive view of market structure.

2. Price Movement Classification: Categorizes price action based on magnitude and
   speed into classifications like "EXTREMELY AGGRESSIVE", "MODERATE", or "SUBTLE".

3. Market Maker Trap Detection: Identifies potential manipulation patterns including:
   - Liquidity Blocks ($450-$550 price movements)
   - Short-term Liquidity Hunts (rapid moves in small timeframes)
   - Trend Reversals (price moving against established trend)

4. Price Velocity Monitoring: Calculates the speed of price movements relative to
   larger timeframes to detect unusual acceleration.

5. Momentum Indicators: Provides cross-timeframe momentum analysis to identify
   strong directional bias when all timeframes align.

Output Format
------------
The module uses color-coded terminal output to enhance readability:
- GREEN: Bullish/positive movements
- RED: Bearish/negative movements
- YELLOW: Caution/moderate negative changes
- BLUE: Moderate positive changes
- CYAN: Informational/neutral data
- MAGENTA: Timeframe indicators and section headers
- LIGHT_ORANGE: Warning signals and moderate concern

Implementation Details
--------------------
- Continuously polls the database for recent price movements
- Calculates trend characteristics using statistical methods
- Stores potential MM trap events for later analysis
- Provides real-time feedback on market conditions
- Offers visual indicators of market state through color-coding

Usage
-----
The module can be run directly to start continuous monitoring:
```
python -m omega_ai.monitor.monitor_market_trends
````
Or imported and used programmatically:

```
from omega_ai.monitor.monitor_market_trends import monitor_market_trends monitor_market_trends()
````

Dependencies
-----------
- omega_ai.db_manager.database: Database access for price data
- Terminal with ANSI color support for optimal visualization

Author: OmegaBTC Team
Version: 1.0
"""

import time
import redis
import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from omega_ai.db_manager.database import fetch_multi_interval_movements, analyze_price_trend, insert_possible_mm_trap
from omega_ai.mm_trap_detector.fibonacci_detector import get_current_fibonacci_levels, check_fibonacci_level

# Initialize Redis connection
redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)

# Add terminal colors for enhanced visibility
BLUE = "\033[94m"           # Price up
YELLOW = "\033[93m"         # Price down
GREEN = "\033[92m"          # Strongly positive
RED = "\033[91m"            # Strongly negative
CYAN = "\033[96m"           # Info highlight
MAGENTA = "\033[95m"        # Special emphasis
LIGHT_ORANGE = "\033[38;5;214m"  # Warning/moderate negative
RESET = "\033[0m"           # Reset color

def describe_movement(change_pct, abs_change):
    """Describe the price movement characteristics based on percentage and absolute change."""
    # Determine intensity of movement
    if abs(change_pct) > 2.0:
        intensity = f"{RED}EXTREMELY AGGRESSIVE{RESET}"
    elif abs(change_pct) > 1.0:
        intensity = f"{LIGHT_ORANGE}VERY AGGRESSIVE{RESET}"
    elif abs(change_pct) > 0.5:
        intensity = f"{YELLOW}AGGRESSIVE{RESET}"
    elif abs(change_pct) > 0.2:
        intensity = f"{CYAN}MODERATE{RESET}"
    elif abs(change_pct) > 0.1:
        intensity = f"{BLUE}MILD{RESET}"
    else:
        intensity = f"{RESET}SUBTLE{RESET}"
        
    # Determine direction with arrow
    if change_pct > 0:
        direction = f"{GREEN}↑ UP{RESET}"
    elif change_pct < 0:
        direction = f"{RED}↓ DOWN{RESET}"
    else:
        direction = f"{RESET}→ FLAT{RESET}"
        
    return f"{direction} | {intensity} | ${abs_change:.2f} absolute"

def format_trend_output(interval, trend, change_pct):
    """Format trend output with colors based on direction and intensity."""
    if "Bullish" in trend:
        if "Strongly" in trend:
            color_trend = f"{GREEN}{trend}{RESET}"
        else:
            color_trend = f"{BLUE}{trend}{RESET}"
        sign = "+"
        color_pct = GREEN
    elif "Bearish" in trend:
        if "Strongly" in trend:
            color_trend = f"{RED}{trend}{RESET}"
        else:
            color_trend = f"{LIGHT_ORANGE}{trend}{RESET}"
        sign = ""
        color_pct = RED
    else:
        color_trend = f"{CYAN}{trend}{RESET}"
        sign = "" if change_pct < 0 else "+"
        color_pct = BLUE if change_pct > 0 else YELLOW if change_pct < 0 else RESET
        
    return f"📈 {MAGENTA}{interval}{RESET} Trend: {color_trend} ({color_pct}{sign}{change_pct:.2f}%{RESET})"

def detect_possible_mm_traps(
    timeframe: str,
    trend: str,
    price_change: float,
    price_move: float
) -> Tuple[Optional[str], float]:
    """Detect potential market maker traps."""
    try:
        # Trap detection logic
        if abs(price_change) > 1.5 and "Strong" in trend:
            confidence = min(abs(price_change) / 5.0, 1.0)
            trap_type = "Bull Trap" if "Bullish" in trend else "Bear Trap"
            
            # Record trap detection
            trap_data = {
                "type": trap_type,
                "timeframe": timeframe,
                "confidence": confidence,
                "price_change": price_change,
                "price_move": price_move,
                "detected_at": datetime.now().isoformat()
            }
            insert_possible_mm_trap(trap_data)
            
            return trap_type, confidence
            
        return None, 0.0
        
    except Exception as e:
        logging.error(f"Error detecting MM traps: {e}")
        return None, 0.0

def get_current_fibonacci_levels() -> Dict[str, float]:
    """Calculate current Fibonacci levels."""
    try:
        # Get recent movements for Fibonacci calculation
        movements = fetch_multi_interval_movements(interval=5, limit=100)
        if not movements:
            return {}
            
        prices = [m["price"] for m in movements if "price" in m]
        if len(prices) < 2:
            return {}
            
        high, low = max(prices), min(prices)
        range_size = high - low
        
        return {
            "0.236": low + (range_size * 0.236),
            "0.382": low + (range_size * 0.382),
            "0.500": low + (range_size * 0.500),
            "0.618": low + (range_size * 0.618),
            "0.786": low + (range_size * 0.786)
        }
        
    except Exception as e:
        logging.error(f"Error calculating Fibonacci levels: {e}")
        return {}

def check_fibonacci_level(current_price: float) -> Optional[Dict]:
    """Check if price is at a Fibonacci level."""
    try:
        fib_levels = get_current_fibonacci_levels()
        if not fib_levels:
            return None
            
        # Check each level with 0.1% tolerance
        for level, price in fib_levels.items():
            tolerance = price * 0.001
            if abs(current_price - price) <= tolerance:
                return {
                    "level": level,
                    "price": price
                }
                
        return None
        
    except Exception as e:
        logging.error(f"Error checking Fibonacci level: {e}")
        return None

def display_fibonacci_analysis(latest_price):
    """Display current Fibonacci levels and check for price alignment."""
    print(f"\n{CYAN}🔄 FIBONACCI ANALYSIS{RESET}")
    print("=" * 40)
    
    # Get current Fibonacci levels
    fib_levels = get_current_fibonacci_levels()
    
    if not fib_levels:
        print(f"{YELLOW}⚠️ Insufficient data for Fibonacci analysis{RESET}")
        return
    
    # Check if current price is at a Fibonacci level
    fib_hit = check_fibonacci_level(latest_price)
    
    if fib_hit:
        # Highlight the current level with color based on its importance
        if fib_hit["level"] == 0.618:
            level_color = f"{MAGENTA}"  # Golden ratio gets special color
            importance = "GOLDEN RATIO"
        elif fib_hit["level"] in [0.382, 0.5, 0.786]:
            level_color = f"{GREEN}"
            importance = "KEY LEVEL"
        else:
            level_color = f"{BLUE}"
            importance = "Standard"
            
        print(f"{level_color}⭐ PRICE AT FIBONACCI {importance}: "
              f"{fib_hit['label']} level (${fib_hit['price']:.2f}){RESET}")
    
    # Display all Fibonacci levels with current price highlighted
    print(f"\n{CYAN}Current Fibonacci Levels:{RESET}")
    
    # Sort levels by price (ascending or descending based on trend)
    is_uptrend = fib_hit["is_uptrend"] if fib_hit else True
    sorted_levels = sorted(fib_levels.items(), 
                          key=lambda x: float(x[1]), 
                          reverse=not is_uptrend)
    
    trend_label = "UPTREND" if is_uptrend else "DOWNTREND"
    print(f"{CYAN}Market Direction: {trend_label}{RESET}")
    
    for label, price in sorted_levels:
        # Highlight the level closest to current price
        if fib_hit and label == fib_hit["label"]:
            print(f"  {GREEN}→ {label}: ${price:.2f} [CURRENT PRICE]{RESET}")
        else:
            # Color code by proximity to current price
            proximity = abs(latest_price - price) / price * 100
            if proximity < 0.5:  # Very close but not quite at the level
                color = YELLOW
            elif proximity < 2:  # Somewhat close
                color = BLUE
            else:
                color = RESET
                
            print(f"  {color}{label}: ${price:.2f}{RESET}")

def monitor_market_trends():
    """Continuously monitor market trends at different time intervals."""
    print(f"{MAGENTA}🚀 Starting Market Trend Analysis...{RESET}")
    
    while True:
        try:
            # Analyze all timeframes
            print(f"\n{CYAN}📊 MULTI-TIMEFRAME ANALYSIS{RESET}")
            print("=" * 40)
            
            # Get trend analysis for different timeframes
            one_min_trend, one_min_change = analyze_price_trend(1)
            five_min_trend, five_min_change = analyze_price_trend(5)
            ten_min_trend, ten_min_change = analyze_price_trend(10)
            
            # Calculate absolute price changes for each timeframe
            one_min_abs_change = abs(one_min_change * 60)  # Scale to absolute USD value
            five_min_abs_change = abs(five_min_change * 300)
            ten_min_abs_change = abs(ten_min_change * 600)
            
            # Format output with color based on trend
            print(format_trend_output("1min", one_min_trend, one_min_change))
            if one_min_change != 0 and one_min_trend != "Insufficient data":
                print(f"   └─ {describe_movement(one_min_change, one_min_abs_change)}")
                # Check for possible MM traps in 1min timeframe
                trap_type, confidence = detect_possible_mm_traps("1min", one_min_trend, one_min_change, one_min_abs_change)
                if trap_type:
                    print(f"   └─ {RED}⚠️ Possible MM Trap: {trap_type} (Confidence: {confidence:.2f}){RESET}")
                    # Store for later analysis
                    insert_possible_mm_trap("1min", trap_type, one_min_change, one_min_abs_change, confidence)
                
            # Repeat for 5min timeframe
            print(format_trend_output("5min", five_min_trend, five_min_change))
            if five_min_change != 0 and five_min_trend != "Insufficient data":
                print(f"   └─ {describe_movement(five_min_change, five_min_abs_change)}")
                # Check for possible MM traps in 5min timeframe
                trap_type, confidence = detect_possible_mm_traps("5min", five_min_trend, five_min_change, five_min_abs_change)
                if trap_type:
                    print(f"   └─ {RED}⚠️ Possible MM Trap: {trap_type} (Confidence: {confidence:.2f}){RESET}")
                    # Store for later analysis
                    insert_possible_mm_trap("5min", trap_type, five_min_change, five_min_abs_change, confidence)
                
            # Repeat for 10min timeframe
            print(format_trend_output("10min", ten_min_trend, ten_min_change))
            if ten_min_change != 0 and ten_min_trend != "Insufficient data":
                print(f"   └─ {describe_movement(ten_min_change, ten_min_abs_change)}")
                # Check for possible MM traps in 10min timeframe
                trap_type, confidence = detect_possible_mm_traps("10min", ten_min_trend, ten_min_change, ten_min_abs_change)
                if trap_type:
                    print(f"   └─ {RED}⚠️ Possible MM Trap: {trap_type} (Confidence: {confidence:.2f}){RESET}")
                    # Store for later analysis
                    insert_possible_mm_trap("10min", trap_type, ten_min_change, ten_min_abs_change, confidence)
            
            # Get detailed movement data
            movements, summary = fetch_multi_interval_movements()
            
            # Price velocity indicator (new feature!)
            if one_min_change != 0 and five_min_change != 0 and one_min_trend != "Insufficient data":
                velocity_ratio = abs(one_min_change / five_min_change) if five_min_change != 0 else 0
                if velocity_ratio > 0.7:
                    print(f"\n{RED}⚠️ HIGH VELOCITY ALERT! {velocity_ratio:.2f}x normal speed{RESET}")
                elif velocity_ratio > 0.4:
                    print(f"\n{YELLOW}⚡ Accelerating price movement detected ({velocity_ratio:.2f}x){RESET}")
            
            # Only show distribution if we have data
            if any(stats.get('count', 0) > 0 for stats in summary.values()):
                print(f"\n{CYAN}📊 MOVEMENT DISTRIBUTION{RESET}")
                print("=" * 40)
                for interval, stats in summary.items():
                    if stats.get('count', 0) > 0:
                        print(f"{MAGENTA}📊 {interval} Movement Types:{RESET}")
                        for move_type, count in stats.get('movement_types', {}).items():
                            # Color-code different movement types
                            if "Grab" in move_type:
                                move_color = RED
                            elif "Pump" in move_type:
                                move_color = GREEN
                            elif "Dump" in move_type:
                                move_color = YELLOW
                            elif "Stable" in move_type:
                                move_color = CYAN
                            else:
                                move_color = RESET
                                
                            print(f"  - {move_color}{move_type}{RESET}: {count}")
            else:
                print(f"\n{YELLOW}⚠️ No movement data available yet. Waiting for price updates...{RESET}")
            
            # Price momentum indicator
            all_trends = [one_min_trend, five_min_trend, ten_min_trend]
            if all(t != "Insufficient data" for t in all_trends):
                bullish_count = sum(1 for t in all_trends if "Bullish" in t)
                bearish_count = sum(1 for t in all_trends if "Bearish" in t)
                
                if bullish_count == 3:
                    print(f"\n{GREEN}🚀 STRONG BULLISH MOMENTUM ACROSS ALL TIMEFRAMES!{RESET}")
                elif bearish_count == 3:
                    print(f"\n{RED}📉 STRONG BEARISH MOMENTUM ACROSS ALL TIMEFRAMES!{RESET}")
                elif bullish_count > bearish_count:
                    print(f"\n{BLUE}📈 Bullish bias detected ({bullish_count}/3 timeframes){RESET}")
                elif bearish_count > bullish_count:
                    print(f"\n{YELLOW}📉 Bearish bias detected ({bearish_count}/3 timeframes){RESET}")
                    
            try:
                # Get current BTC price for Fibonacci analysis
                last_price_bytes = redis_conn.get("last_btc_price")
                if last_price_bytes:
                    last_price = float(last_price_bytes)
                    # Display Fibonacci analysis with current price
                    display_fibonacci_analysis(last_price)
            except Exception as e:
                print(f"{RED}❌ Fibonacci analysis error: {e}{RESET}")
            
            # Sleep for a minute before next analysis
            print(f"\n{CYAN}⏳ Next analysis in 30 seconds...{RESET}")
            time.sleep(30)
            
        except Exception as e:
            print(f"{RED}❌ Analysis error: {e}{RESET}")
            time.sleep(30)

if __name__ == "__main__":
    monitor_market_trends()
````` 