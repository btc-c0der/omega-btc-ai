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
    if trend == "Insufficient Data":
        color_trend = f"{YELLOW}{trend}{RESET}"
        sign = ""
        color_pct = YELLOW
    elif "Bullish" in trend:
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
            color_trend = f"{YELLOW}{trend}{RESET}"
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
        # Get price history - increased multiplier for longer timeframes
        # Use a variable multiplier based on timeframe to handle limited data
        if minutes <= 60:
            multiplier = 2  # For shorter timeframes, get 2x the data
        elif minutes <= 240:
            multiplier = 1.5  # For medium timeframes, get 1.5x data
        else:
            multiplier = 1.2  # For longer timeframes, be more flexible
            
        history = get_btc_price_history(limit=int(minutes*multiplier))
        
        # For longer timeframes, we'll be more flexible with data requirements
        # For 4h+ timeframes, require at least 50% of the requested data
        min_required = minutes
        if minutes > 240:  # For timeframes > 4 hours
            min_required = int(minutes * 0.5)  # Only require 50% of data points
        elif minutes > 60:  # For timeframes > 1 hour
            min_required = int(minutes * 0.75)  # Require 75% of data points
            
        if not history or len(history) < min_required:
            return "No Data", 0.0
        
        # Calculate relevant price points
        current_price = history[0]["price"]
        
        # For longer timeframes where we don't have full history,
        # use the oldest available price we have
        comparison_index = min(minutes, len(history)-1)
        past_price = history[comparison_index]["price"]
        
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
                    alignment_type = "STRONG" if confidence > 0.8 else "MODERATE" if confidence > 0.5 else "WEAK"
                    
                    # Special handling for Golden Ratio (0.618)
                    if "618" in level_name:
                        confidence += 0.1  # Boost confidence for Golden Ratio
                        alignment_type = "GOLDEN_RATIO"
                        
                    all_alignments.append({
                        "category": category,
                        "level": level_name,
                        "price": level_price,
                        "diff_pct": diff_pct,
                        "confidence": confidence,
                        "type": alignment_type
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

def display_fibonacci_analysis(current_price, fib_levels):
    """Display current Fibonacci levels and check for price alignment."""
    print(f"\n{CYAN}🔄 FIBONACCI ANALYSIS{RESET}")
    print("=" * 40)
    
    if not fib_levels:
        print(f"{YELLOW}⚠️ Insufficient data for Fibonacci analysis{RESET}")
        return
    
    # Check if current price is at a Fibonacci level
    alignment = detect_fibonacci_alignment(current_price, fib_levels)
    
    if alignment:
        # Highlight the current level with color based on its importance
        if alignment["type"] == "GOLDEN_RATIO":
            level_color = f"{MAGENTA}"  # Golden ratio gets special color
            importance = "GOLDEN RATIO"
        elif alignment["confidence"] > 0.8:
            level_color = f"{GREEN}"
            importance = "KEY LEVEL"
        else:
            level_color = f"{BLUE}"
            importance = "Standard"
            
        print(f"{level_color}⭐ PRICE AT FIBONACCI {importance}: "
              f"{alignment['level']} level (${alignment['price']:.2f}){RESET}")
        print(f"  {YELLOW}Confidence: {alignment['confidence']:.2f} | Distance: {alignment['diff_pct']:.3f}%{RESET}")
    
    # Display all Fibonacci levels with current price highlighted
    print(f"\n{CYAN}Current Fibonacci Levels:{RESET}")
    
    # Show retracement levels
    print(f"{MAGENTA}Retracement Levels:{RESET}")
    for level, price in fib_levels["retracement"].items():
        # Highlight the level closest to current price
        if alignment and level == alignment["level"] and alignment["category"] == "retracement":
            print(f"  {GREEN}→ {level}: ${price:.2f} [CURRENT PRICE]{RESET}")
        else:
            # Color code by proximity to current price
            proximity = abs(current_price - price) / price * 100
            if proximity < 0.5:  # Very close but not quite at the level
                color = YELLOW
            elif proximity < 2:  # Somewhat close
                color = BLUE
            else:
                color = RESET
                
            print(f"  {color}{level}: ${price:.2f}{RESET}")
    
    # Show extension levels
    print(f"\n{MAGENTA}Extension Levels:{RESET}")
    for level, price in fib_levels["extension"].items():
        # Highlight the level closest to current price
        if alignment and level == alignment["level"] and alignment["category"] == "extension":
            print(f"  {GREEN}→ {level}: ${price:.2f} [CURRENT PRICE]{RESET}")
        else:
            # Color code by proximity to current price
            proximity = abs(current_price - price) / price * 100
            if proximity < 0.5:  # Very close but not quite at the level
                color = YELLOW
            elif proximity < 2:  # Somewhat close
                color = BLUE
            else:
                color = RESET
                
            print(f"  {color}{level}: ${price:.2f}{RESET}")

class DivineFibonacciMonitor:
    """Sacred market monitor that integrates with Fibonacci-aligned architecture."""
    
    def __init__(self, analysis_interval=5):
        """Initialize the divine monitor."""
        self.timeframes = [1, 5, 15, 30, 60, 240, 720, 1444]  # Fibonacci-inspired timeframes
        self.last_analysis_time = None
        self.analysis_interval = analysis_interval  # seconds, now configurable
        self.redis_manager = RedisManager(host=redis_host, port=redis_port)
        self.consecutive_errors = 0
        self.previous_price = None  # Track previous price for up/down comparison
        self.last_btc_price = 0  # Store last BTC price
    
    def analyze_market(self):
        """Perform comprehensive market analysis with Fibonacci alignment."""
        try:
            results = {}
            
            # Get current price directly from Redis
            self.last_btc_price = float(redis_conn.get("last_btc_price") or 0)
            if self.last_btc_price == 0:
                logger.warning("No current price available for analysis")
                return {}
            
            results["current_price"] = self.last_btc_price
            
            # Calculate Fibonacci levels
            history = get_btc_price_history(limit=100)
            if history:
                fib_levels = calculate_fibonacci_levels(history)
                results["fibonacci_levels"] = fib_levels
                
                # Check for Fibonacci alignment
                alignment = detect_fibonacci_alignment(self.last_btc_price, fib_levels)
                if alignment:
                    results["fibonacci_alignment"] = alignment
            
            # Analyze each timeframe - capture data availability info
            available_minutes = len(history)
            available_hours = available_minutes / 60
            
            # Add data availability information to results
            results["data_availability"] = {
                "minutes": available_minutes,
                "hours": available_hours,
                "oldest_price": history[-1]["price"] if history else None,
                "newest_price": history[0]["price"] if history else None
            }
            
            # Only analyze timeframes where we might have reasonable data
            analyzed_timeframes = []
            for minutes in self.timeframes:
                # Only process timeframes that make sense with our data
                # For timeframes > 4h, require at least 50% of data
                if minutes > 240 and len(history) < minutes * 0.5:
                    results[f"{minutes}min"] = {
                        "trend": "Insufficient Data",
                        "change": 0.0,
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                    continue
                    
                trend, change = analyze_price_trend(minutes)
                results[f"{minutes}min"] = {
                    "trend": trend,
                    "change": change,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                analyzed_timeframes.append(minutes)
                
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
                    
                # Store data availability info
                self.redis_manager.set_cached("divine:data_availability",
                                             json.dumps(results["data_availability"]))
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
        
        # Get current BTC price and compare with previous price
        current_price = results.get("current_price", 0)
        price_direction = ""
        color_indicator = ""
        
        if self.previous_price is not None:
            if current_price > self.previous_price:
                price_direction = "↑ UP"
                color_indicator = BLUE
            elif current_price < self.previous_price:
                price_direction = "↓ DOWN"
                color_indicator = MAGENTA
            else:
                price_direction = "→ FLAT"
                color_indicator = CYAN
        
        # Store current price for next comparison
        self.previous_price = current_price
        
        # Display current BTC price with direction indicator
        print(f"\n{BLUE_BG}{WHITE}{BOLD} 💰 CURRENT BTC PRICE: ${current_price:,.2f} 💰 {RESET} {color_indicator}{price_direction}{RESET}")
        print(f"{CYAN}Last Redis Key Update: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC{RESET}")
        
        # Display data availability if available
        if "data_availability" in results:
            availability = results["data_availability"]
            print(f"{YELLOW}Available price history: {availability['minutes']} minutes ({availability['hours']:.1f} hours){RESET}")
        
        # Display trends for each timeframe
        print(f"\n{YELLOW}══════════════ {GREEN}MARKET TREND ANALYSIS{YELLOW} ══════════════{RESET}")
        
        for timeframe, data in results.items():
            if timeframe.endswith("min"):
                trend = data["trend"]
                change = data["change"]
                print(format_trend_output(timeframe, trend, change))
                if trend != "Insufficient Data":
                    print(f"   {describe_movement(change, abs(change))}")
                else:
                    print(f"   {YELLOW}Not enough historical data for this timeframe{RESET}")
        
        # Display Fibonacci analysis if levels are present
        if "fibonacci_levels" in results:
            display_fibonacci_analysis(current_price, results["fibonacci_levels"])
        
        # Display Fibonacci alignment if present
        if "fibonacci_alignment" in results:
            alignment = results["fibonacci_alignment"]
            print(f"\n{CYAN}🔱 DIVINE FIBONACCI ALIGNMENT:{RESET}")
            print(f"  Level: {alignment['level']} ({alignment['category']})")
            print(f"  Price: ${alignment['price']:,.2f}")
            print(f"  Confidence: {alignment['confidence']:.2f}")
            print(f"  Distance: {alignment['diff_pct']:.3f}%")
            
            # Special message for golden ratio alignment
            if alignment["type"] == "GOLDEN_RATIO":
                print(f"\n  {MAGENTA}🌟 GOLDEN RATIO ALIGNMENT DETECTED - SACRED HARMONIC POINT 🌟{RESET}")
        
        # Display MM traps if detected
        if "mm_traps" in results and results["mm_traps"]:
            print(f"\n{RED_BG}{WHITE}{BOLD} ⚠️ MARKET MAKER TRAPS DETECTED ⚠️ {RESET}")
            for trap in results["mm_traps"]:
                confidence_color = RED if trap["confidence"] > 0.8 else LIGHT_ORANGE if trap["confidence"] > 0.5 else YELLOW
                print(f"  {confidence_color}{trap['type']} | {trap['timeframe']} | Confidence: {trap['confidence']:.2f}{RESET}")
                print(f"  {WHITE}Trend: {trap['trend']} | Change: {trap['price_change']:.2f}%{RESET}")
        
        # Display divine wisdom footer
        print(f"\n{GREEN}══════════════ {YELLOW}SACRED ALIGNMENT{GREEN} ══════════════{RESET}")
        print(f"{MAGENTA}May your trades be guided by the Divine Fibonacci Sequence{RESET}")
        print(f"{YELLOW}Last update: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC{RESET}")
        print(f"\n{YELLOW}Next update in {self.analysis_interval} seconds...{RESET}")

def run_divine_monitor(interval=5):
    """Run the divine market monitor continuously with configurable interval."""
    monitor = DivineFibonacciMonitor(analysis_interval=interval)
    
    print(f"\n{GREEN}Initializing Divine Fibonacci Market Monitor...{RESET}")
    print(f"{BLUE}🔱 Connected to Redis at {redis_host}:{redis_port}{RESET}")
    print(f"{YELLOW}Monitoring interval set to {interval} seconds{RESET}")
    
    while True:
        try:
            # Get current BTC price directly for display
            try:
                btc_price = float(redis_conn.get("last_btc_price") or 0)
                if btc_price > 0:
                    monitor.last_btc_price = btc_price
            except Exception as e:
                print(f"{RED}Error reading from Redis: {e}{RESET}")
                
            # Perform analysis
            results = monitor.analyze_market()
            
            # Display results
            if results:
                monitor.display_results(results)
            else:
                print(f"{RED}⚠️ No results from analysis - checking Redis connection...{RESET}")
                # Get current BTC price directly from Redis for a basic display
                try:
                    btc_price = float(redis_conn.get("last_btc_price") or 0)
                    if btc_price > 0:
                        print(f"{YELLOW}Current BTC Price (from Redis): ${btc_price:,.2f}{RESET}")
                    else:
                        print(f"{RED}Unable to get current BTC price from Redis{RESET}")
                except Exception as e:
                    print(f"{RED}Error reading from Redis: {e}{RESET}")
            
            # Sleep for the specified interval
            time.sleep(interval)
            
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
    import argparse
    
    parser = argparse.ArgumentParser(description="Divine Fibonacci Market Monitor")
    parser.add_argument("-i", "--interval", type=int, default=5, 
                      help="Analysis interval in seconds (default: 5)")
    args = parser.parse_args()
    
    display_sacred_banner()
    print(f"{GREEN}🌟 DIVINE FIBONACCI MONITOR ACTIVATED 🌟{RESET}")
    run_divine_monitor(interval=args.interval) 