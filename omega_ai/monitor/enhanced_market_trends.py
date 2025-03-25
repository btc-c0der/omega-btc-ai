#!/usr/bin/env python3

"""
🔮 GPU (General Public Universal) License 1.0
--------------------------------------------
OMEGA BTC AI DIVINE COLLECTIVE
Licensed under the GPU (General Public Universal) License v1.0
Date: 2024-03-25
Location: The Cosmic Void

This source code is governed by the GPU License, granting the following sacred freedoms:
- The Freedom to Study this code, its divine algorithms and cosmic patterns
- The Freedom to Modify this code, enhancing its divine functionality
- The Freedom to Distribute this code, sharing its sacred knowledge
- The Freedom to Use this code, implementing its sacred algorithms

Along with these divine obligations:
- Preserve this sacred knowledge by maintaining source accessibility
- Share all divine modifications to maintain universal access
- Provide attribution to acknowledge sacred origins

The sacred code is provided "as is", without divine warranty of any kind.
Governed by the laws of the universe, without regard to conflict of law provisions.

For the full divine license, consult the LICENSE file in the project root.
"""

import time
import redis
import logging
import json
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timezone
import os
import math
import numpy as np
from omega_ai.utils.redis_manager import RedisManager

# Configure logger with enhanced formatting
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Initialize Redis connection with error handling
try:
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)
    redis_conn.ping()
    logger.info(f"Successfully connected to Redis at {redis_host}:{redis_port}")
except redis.ConnectionError as e:
    logger.error(f"Failed to connect to Redis: {e}")
    raise

# Terminal colors for enhanced visibility
BLUE = "\033[94m"           # Price up
YELLOW = "\033[93m"         # Price down
GREEN = "\033[92m"          # Strongly positive
RED = "\033[91m"            # Strongly negative
CYAN = "\033[96m"           # Info highlight
MAGENTA = "\033[95m"        # Special emphasis
LIGHT_ORANGE = "\033[38;5;214m"  # Warning/moderate negative
RESET = "\033[0m"           # Reset color
BLUE_BG = "\033[44m"        # Background for blue text
WHITE = "\033[97m"          # White text
BOLD = "\033[1m"            # Bold text
GREEN_BG = "\033[42m"       # Background for green text
RED_BG = "\033[41m"         # Background for red text

# Sacred Fibonacci sequence and constants
FIBONACCI_SEQUENCE = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584]
GOLDEN_RATIO = 1.618033988749895
PHI = GOLDEN_RATIO
PHI_SQUARE = PHI * PHI

def display_sacred_banner():
    """Display sacred banner with Fibonacci alignment."""
    banner = f"""
{GREEN}╔════════════════════════════════════════════════════════════════════╗
{YELLOW}  ███████╗██╗██████╗  ██████╗ ███╗   ██╗ █████╗  ██████╗ ██████╗ ██╗
{YELLOW}  ██╔════╝██║██╔══██╗██╔═══██╗████╗  ██║██╔══██╗██╔════╝██╔════╝ ██║
{YELLOW}  █████╗  ██║██████╔╝██║   ██║██╔██╗ ██║███████║██║     ██║     ██║
{YELLOW}  ██╔══╝  ██║██╔══██╗██║   ██║██║╚██╗██║██╔══██║██║     ██║     ╚═╝
{YELLOW}  ██║     ██║██████╔╝╚██████╔╝██║ ╚████║██║  ██║╚██████╗██████╗ ██╗
{YELLOW}  ╚═╝     ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝╚═════╝ ╚═╝
{GREEN}   🔱 MARKET TRENDS MONITOR | OMEGA BTC AI v1.6.18 🔱
{GREEN}   [DIVINE ARCHITECTURE 1:1:2:3:5 - GOLDEN RATIO ENHANCED]
{GREEN}╚════════════════════════════════════════════════════════════════════╝{RESET}
"""
    print(banner)

def describe_movement(change_pct, abs_change):
    """Describe the price movement characteristics with Fibonacci wisdom."""
    # Determine intensity of movement
    if abs(change_pct) > 3.618:  # PHI^3
        intensity = f"{RED}COSMIC SHIFT{RESET}"
    elif abs(change_pct) > 2.618:  # PHI^2
        intensity = f"{RED}EXTREMELY AGGRESSIVE{RESET}"
    elif abs(change_pct) > 1.618:  # PHI
        intensity = f"{LIGHT_ORANGE}VERY AGGRESSIVE{RESET}"
    elif abs(change_pct) > 1.0:
        intensity = f"{YELLOW}AGGRESSIVE{RESET}"
    elif abs(change_pct) > 0.618:  # 1/PHI
        intensity = f"{CYAN}MODERATE{RESET}"
    elif abs(change_pct) > 0.382:  # 1/PHI^2
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

def get_btc_price_history(limit=100):
    """Get BTC price history from Redis with error handling."""
    try:
        history = []
        raw_data = redis_conn.lrange("btc_movement_history", 0, limit-1)
        
        if raw_data:
            for item in raw_data:
                try:
                    if "," in item:
                        price_str, volume_str = item.split(",")
                        price = float(price_str)
                        volume = float(volume_str)
                        history.append({"price": price, "volume": volume})
                    else:
                        price = float(item)
                        history.append({"price": price, "volume": 0})
                except Exception as e:
                    logger.warning(f"Error parsing price history item: {e}")
                    continue
            
            return history
        return []
    except Exception as e:
        logger.error(f"Error fetching BTC price history: {e}")
        return []

def calculate_fibonacci_levels(prices):
    """Calculate comprehensive Fibonacci levels based on price history."""
    if not prices or len(prices) < 5:
        return {}
    
    # Extract prices only
    price_values = [p["price"] for p in prices]
    
    # Get high and low prices
    high_price = max(price_values)
    low_price = min(price_values)
    current_price = price_values[0]  # Most recent price
    
    # Calculate price range
    price_range = high_price - low_price
    
    # Calculate standard Fibonacci retracement levels
    retracement_levels = {
        "0.0": low_price,
        "0.236": low_price + 0.236 * price_range,
        "0.382": low_price + 0.382 * price_range,
        "0.5": low_price + 0.5 * price_range,  # Not a Fibonacci ratio but commonly used
        "0.618": low_price + 0.618 * price_range,  # Golden Ratio
        "0.786": low_price + 0.786 * price_range,
        "0.886": low_price + 0.886 * price_range,  # Additional level used by traders
        "1.0": high_price
    }
    
    # Add Fibonacci extensions
    extension_levels = {
        "1.272": high_price + 0.272 * price_range,  # Square root of 1.618
        "1.414": high_price + 0.414 * price_range,  # Square root of 2
        "1.618": high_price + 0.618 * price_range,  # Golden Ratio
        "2.0": high_price + 1.0 * price_range,
        "2.618": high_price + 1.618 * price_range,  # Golden Ratio squared
        "3.618": high_price + 2.618 * price_range,  # Golden Ratio cubed
        "4.236": high_price + 3.236 * price_range  # 2 * Golden Ratio + 1
    }
    
    # Combine all levels
    all_levels = {**retracement_levels, **extension_levels}
    
    # Add special GANN square levels based on current price
    gann_levels = {}
    for i in range(1, 10):
        sqrt_level = round(current_price * math.sqrt(i), 2)
        gann_levels[f"gann_sqrt_{i}"] = sqrt_level
    
    # Add key Fibonacci price points (from 8K to 1.5M)
    fib_price_points = {}
    for fib in FIBONACCI_SEQUENCE:
        # Lower values get multiplied by 1000
        if fib <= 144:
            fib_price_points[f"fib_{fib}k"] = fib * 1000
        # Higher values need special scaling
        elif fib <= 987:
            fib_price_points[f"fib_{fib/10:.1f}k"] = fib * 100
        else:
            fib_price_points[f"fib_{fib/100:.2f}M"] = fib * 1000
    
    # Return all levels combined
    return {
        "retracement": retracement_levels,
        "extension": extension_levels, 
        "gann": gann_levels,
        "fibonacci": fib_price_points,
        "high": high_price,
        "low": low_price,
        "current": current_price
    }

def analyze_price_trend(minutes=15):
    """Analyze price trend for specified timeframe."""
    try:
        # Get price history
        history = get_btc_price_history(limit=minutes*2)
        if not history or len(history) < minutes:
            return "No Data", 0.0
        
        # Calculate relevant price points
        current_price = history[0]["price"]
        past_price = history[min(minutes, len(history)-1)]["price"]
        
        # Calculate percentage change
        change_pct = ((current_price - past_price) / past_price) * 100
        
        # Determine trend
        if change_pct > 2.0:
            trend = "Strongly Bullish"
        elif change_pct > 0.5:
            trend = "Bullish"
        elif change_pct < -2.0:
            trend = "Strongly Bearish"
        elif change_pct < -0.5:
            trend = "Bearish"
        else:
            trend = "Neutral"
            
        return trend, change_pct
        
    except Exception as e:
        logger.error(f"Error analyzing price trend: {e}")
        return "Error", 0.0

def detect_fibonacci_alignment(current_price, fib_levels):
    """Detect if current price is aligned with a Fibonacci level."""
    if not fib_levels:
        return None
    
    # Check each category of levels
    all_alignments = []
    
    for category, levels in fib_levels.items():
        if category not in ["high", "low", "current"]:  # Skip metadata entries
            for level_name, level_price in levels.items():
                # Calculate percentage difference
                diff_pct = abs((current_price - level_price) / level_price * 100)
                
                # Consider aligned if within 0.5%
                if diff_pct <= 0.5:
                    confidence = 1.0 - (diff_pct / 0.5)
                    all_alignments.append({
                        "category": category,
                        "level": level_name,
                        "price": level_price,
                        "diff_pct": diff_pct,
                        "confidence": confidence
                    })
    
    # Sort by confidence and return the best match
    if all_alignments:
        return sorted(all_alignments, key=lambda x: x["confidence"], reverse=True)[0]
    
    return None

def detect_mm_trap(timeframe, trend, price_change):
    """Detect potential market maker traps with enhanced Fibonacci awareness."""
    # Early exit if price change is too small
    if abs(price_change) < 1.5:
        return None
    
    # Determine trap type based on trend and price direction
    trap_type = None
    if "Bullish" in trend and price_change > 0:
        trap_type = "Bull Trap"
    elif "Bearish" in trend and price_change < 0:
        trap_type = "Bear Trap"
    
    if not trap_type:
        return None
    
    # Calculate confidence based on multiple factors
    price_intensity = min(abs(price_change) / 5.0, 1.0)
    trend_multiplier = 1.0 if trend.startswith("Strongly") else 0.7
    timeframe_multiplier = 1.0 if timeframe in ["15min", "1h"] else 0.7
    
    # Weight components
    price_weight = 0.6
    trend_weight = 0.3
    timeframe_weight = 0.1
    
    # Calculate total confidence
    confidence = (
        (price_intensity * price_weight) +
        (trend_multiplier * trend_weight) +
        (timeframe_multiplier * timeframe_weight)
    )
    
    # Round to 2 decimal places to avoid floating point issues
    confidence = round(min(confidence, 1.0), 2)
    
    if confidence >= 0.3:
        return {
            "type": trap_type,
            "confidence": confidence,
            "price_change": price_change,
            "timeframe": timeframe,
            "trend": trend
        }
    
    return None

class DivineFibonacciMonitor:
    """Sacred market monitor that integrates with Fibonacci-aligned architecture."""
    
    def __init__(self):
        """Initialize the divine monitor."""
        self.timeframes = [1, 5, 15, 30, 60, 240, 720, 1444]  # Fibonacci-inspired timeframes
        self.last_analysis_time = None
        self.analysis_interval = 5  # seconds
        self.redis_manager = RedisManager(host=redis_host, port=redis_port)
        self.consecutive_errors = 0
    
    def analyze_market(self):
        """Perform comprehensive market analysis with Fibonacci alignment."""
        try:
            results = {}
            
            # Get current price
            current_price = float(redis_conn.get("last_btc_price") or 0)
            if current_price == 0:
                logger.warning("No current price available for analysis")
                return {}
            
            results["current_price"] = current_price
            
            # Calculate Fibonacci levels
            history = get_btc_price_history(limit=100)
            if history:
                fib_levels = calculate_fibonacci_levels(history)
                results["fibonacci_levels"] = fib_levels
                
                # Check for Fibonacci alignment
                alignment = detect_fibonacci_alignment(current_price, fib_levels)
                if alignment:
                    results["fibonacci_alignment"] = alignment
            
            # Analyze each timeframe
            for minutes in self.timeframes:
                trend, change = analyze_price_trend(minutes)
                results[f"{minutes}min"] = {
                    "trend": trend,
                    "change": change,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                
                # Check for MM traps
                trap = detect_mm_trap(f"{minutes}min", trend, change)
                if trap:
                    if "mm_traps" not in results:
                        results["mm_traps"] = []
                    results["mm_traps"].append(trap)
            
            # Reset error counter on successful analysis
            self.consecutive_errors = 0
            self.last_analysis_time = datetime.now(timezone.utc)
            
            # Store results in Redis for dashboard access
            try:
                # Store Fibonacci levels
                if "fibonacci_levels" in results:
                    self.redis_manager.set_cached("divine:fibonacci_levels", 
                                                 json.dumps(results["fibonacci_levels"]))
                
                # Store alignment information
                if "fibonacci_alignment" in results:
                    self.redis_manager.set_cached("divine:fibonacci_alignment", 
                                                 json.dumps(results["fibonacci_alignment"]))
                    
                # Store trends for each timeframe
                for timeframe, data in results.items():
                    if timeframe.endswith("min"):
                        self.redis_manager.set_cached(f"divine:trend_{timeframe}", 
                                                     json.dumps(data))
                
                # Store traps
                if "mm_traps" in results:
                    self.redis_manager.set_cached("divine:mm_traps", 
                                                 json.dumps(results["mm_traps"]))
            except Exception as e:
                logger.error(f"Error storing analysis results in Redis: {e}")
            
            return results
            
        except Exception as e:
            self.consecutive_errors += 1
            logger.error(f"Error in market analysis: {e}")
            return {}
    
    def display_results(self, results):
        """Display analysis results with divine formatting."""
        # Clear console for fresh display
        print("\033c", end="")
        
        # Display sacred banner
        display_sacred_banner()
        
        # Display current BTC price
        current_price = results.get("current_price", 0)
        print(f"\n{BLUE_BG}{WHITE}{BOLD} 💰 CURRENT BTC PRICE: ${current_price:,.2f} 💰 {RESET}")
        
        # Display trends for each timeframe
        print(f"\n{YELLOW}══════════════ {GREEN}MARKET TREND ANALYSIS{YELLOW} ══════════════{RESET}")
        
        for timeframe, data in results.items():
            if timeframe.endswith("min"):
                trend = data["trend"]
                change = data["change"]
                print(format_trend_output(timeframe, trend, change))
                print(f"   {describe_movement(change, abs(change))}")
        
        # Display Fibonacci alignment if present
        if "fibonacci_alignment" in results:
            alignment = results["fibonacci_alignment"]
            print(f"\n{CYAN}🔱 DIVINE FIBONACCI ALIGNMENT:{RESET}")
            print(f"  Level: {alignment['level']} ({alignment['category']})")
            print(f"  Price: ${alignment['price']:,.2f}")
            print(f"  Confidence: {alignment['confidence']:.2f}")
            print(f"  Distance: {alignment['diff_pct']:.3f}%")
            
            # Special message for golden ratio alignment
            if "618" in alignment['level'] or "golden" in alignment['level'].lower():
                print(f"\n  {MAGENTA}🌟 GOLDEN RATIO ALIGNMENT DETECTED - SACRED HARMONIC POINT 🌟{RESET}")
        
        # Display MM traps if detected
        if "mm_traps" in results and results["mm_traps"]:
            print(f"\n{RED_BG}{WHITE}{BOLD} ⚠️ MARKET MAKER TRAPS DETECTED ⚠️ {RESET}")
            for trap in results["mm_traps"]:
                confidence_color = RED if trap["confidence"] > 0.8 else LIGHT_ORANGE if trap["confidence"] > 0.5 else YELLOW
                print(f"  {confidence_color}{trap['type']} | {trap['timeframe']} | Confidence: {trap['confidence']:.2f}{RESET}")
                print(f"  {WHITE}Trend: {trap['trend']} | Change: {trap['price_change']:.2f}%{RESET}")
        
        # Display Fibonacci levels section
        if "fibonacci_levels" in results:
            fib_levels = results["fibonacci_levels"]
            
            print(f"\n{BLUE_BG}{WHITE}{BOLD} 🧮 SACRED FIBONACCI LEVELS 🧮 {RESET}")
            
            # Only show nearby levels (within 10% of current price)
            current = fib_levels["current"]
            print(f"\n{CYAN}Nearby Retracement Levels:{RESET}")
            for level, price in fib_levels["retracement"].items():
                if abs((price - current) / current) < 0.1:  # Within 10%
                    diff_pct = ((price - current) / current) * 100
                    direction = "↑" if diff_pct > 0 else "↓"
                    diff_color = GREEN if diff_pct > 0 else RED
                    print(f"  {level}: ${price:,.2f} ({diff_color}{direction} {abs(diff_pct):.2f}%{RESET})")
            
            print(f"\n{CYAN}Nearby Extension Levels:{RESET}")
            for level, price in fib_levels["extension"].items():
                if abs((price - current) / current) < 0.1:  # Within 10%
                    diff_pct = ((price - current) / current) * 100
                    direction = "↑" if diff_pct > 0 else "↓"
                    diff_color = GREEN if diff_pct > 0 else RED
                    print(f"  {level}: ${price:,.2f} ({diff_color}{direction} {abs(diff_pct):.2f}%{RESET})")
        
        # Display divine wisdom footer
        print(f"\n{GREEN}══════════════ {YELLOW}SACRED ALIGNMENT{GREEN} ══════════════{RESET}")
        print(f"{MAGENTA}May your trades be guided by the Divine Fibonacci Sequence{RESET}")
        print(f"{YELLOW}Last update: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC{RESET}")

def run_divine_monitor():
    """Run the divine market monitor continuously."""
    monitor = DivineFibonacciMonitor()
    
    print(f"\n{GREEN}Initializing Divine Fibonacci Market Monitor...{RESET}")
    print(f"{BLUE}🔱 Connected to Redis at {redis_host}:{redis_port}{RESET}")
    
    while True:
        try:
            # Check if it's time for analysis
            now = datetime.now(timezone.utc)
            if (monitor.last_analysis_time is None or 
                (now - monitor.last_analysis_time).total_seconds() >= monitor.analysis_interval):
                
                # Perform analysis
                results = monitor.analyze_market()
                
                # Display results
                if results:
                    monitor.display_results(results)
            
            # Sleep for a short interval
            time.sleep(1)
            
        except redis.RedisError as e:
            monitor.consecutive_errors += 1
            wait_time = min(30 * monitor.consecutive_errors, 300)  # Max 5 minutes
            print(f"{RED}⚠️ Redis Connection Error: {e} - Retrying in {wait_time} seconds{RESET}")
            time.sleep(wait_time)
            
        except Exception as e:
            monitor.consecutive_errors += 1
            wait_time = min(15 * monitor.consecutive_errors, 120)  # Max 2 minutes
            print(f"{RED}⚠️ Error in market monitoring: {e}{RESET}")
            print(f"{YELLOW}🔄 Divine Resilience - Restarting analysis in {wait_time} seconds{RESET}")
            time.sleep(wait_time)

if __name__ == "__main__":
    display_sacred_banner()
    print(f"{GREEN}🌟 DIVINE FIBONACCI MONITOR ACTIVATED 🌟{RESET}")
    run_divine_monitor() 