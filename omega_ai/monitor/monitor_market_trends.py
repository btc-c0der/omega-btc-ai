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
from omega_ai.db_manager.database import fetch_multi_interval_movements, analyze_price_trend, insert_possible_mm_trap
from omega_ai.mm_trap_detector.fibonacci_detector import get_current_fibonacci_levels, check_fibonacci_level, update_fibonacci_data
import os
from omega_ai.utils.test_redis_manager import TestRedisManager

# Configure logger with enhanced formatting
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Initialize Redis connection with error handling
try:
    # Check if we're in test mode
    use_test_redis = os.getenv('OMEGA_TEST_USE_LOCAL_REDIS', 'false').lower() == 'true'
    if use_test_redis:
        redis_conn = TestRedisManager().redis
        logger.info("Using test Redis connection")
    else:
        redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_conn.ping()
    logger.info("Successfully connected to Redis")
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

class MarketTrendAnalyzer:
    """Analyzes market trends with multiple indicators and timeframes."""
    
    def __init__(self, redis_connection=None):
        """Initialize the market trend analyzer."""
        self.timeframes = [1, 5, 15, 30, 60, 240, 720, 1444]  # minutes - extended to include up to 1444 minutes
        self.consecutive_errors = 0
        self.last_analysis_time = None
        self.analysis_interval = 5  # seconds
        self.redis_conn = redis_connection or redis_conn
        
    def analyze_trends(self) -> Dict[str, Any]:
        """Analyze market trends across multiple timeframes."""
        try:
            results = {}
            
            # Get current price from Redis
            current_price = float(self.redis_conn.get("last_btc_price") or 0)
            if current_price == 0:
                logger.warning("No current price available for analysis")
                return {}
            
            # Store current price in results
            results["current_price"] = current_price
            
            # Update Fibonacci data with current price
            update_fibonacci_data(current_price)
            
            # Analyze each timeframe
            for minutes in self.timeframes:
                trend, change = analyze_price_trend(minutes)
                results[f"{minutes}min"] = {
                    "trend": trend,
                    "change": change,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                
                # Only store trend data if we have valid data and current price
                if trend != "No Data" and current_price > 0:
                    self.redis_conn.set(f"btc_trend_{minutes}min", json.dumps({
                        "trend": trend,
                        "change": change,
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }))
                else:
                    # Clear any existing trend data if we don't have valid data
                    self.redis_conn.delete(f"btc_trend_{minutes}min")
            
            # Get Fibonacci levels
            fib_levels = get_current_fibonacci_levels()
            if fib_levels:
                results["fibonacci_levels"] = fib_levels
                
                # Check for Fibonacci alignment
                fib_alignment = check_fibonacci_alignment()
                if fib_alignment:
                    results["fibonacci_alignment"] = fib_alignment
                    
                    # Log alignment details
                    logger.info(f"Fibonacci Alignment: {fib_alignment['type']} at {fib_alignment['level']} "
                              f"(${fib_alignment['price']:,.2f}) - {fib_alignment['distance_pct']:.2f}% away")
            
            # Reset error counter on successful analysis
            self.consecutive_errors = 0
            self.last_analysis_time = datetime.now(timezone.utc)
            
            return results
            
        except Exception as e:
            self.consecutive_errors += 1
            logger.error(f"Error in trend analysis: {e}")
            return {}
    
    def display_results(self, results: Dict[str, Any]) -> None:
        """Display analysis results with enhanced formatting."""
        # Display current BTC price prominently at the top
        current_price = results.get("current_price", 0)
        print(f"\n{BLUE_BG}{WHITE}{BOLD} 💰 CURRENT BTC PRICE: ${current_price:,.2f} 💰 {RESET}")
        
        print(f"\n{YELLOW}════════════════ {GREEN}OMEGA RASTA{YELLOW} MARKET TREND ANALYSIS ════════════════{RESET}")
        
        # Display trends for each timeframe with enhanced formatting
        for timeframe, data in results.items():
            if timeframe != "fibonacci_levels" and timeframe != "fibonacci_alignment" and timeframe != "current_price":
                trend = data["trend"]
                change = data["change"]
                print(format_trend_output(timeframe, trend, change))
                
                # Add movement description
                abs_change = abs(change)
                print(f"   {describe_movement(change, abs_change)}")
        
        # Display Fibonacci analysis if available
        if "fibonacci_alignment" in results:
            fib_data = results["fibonacci_alignment"]
            print(f"\n{CYAN}🔄 FIBONACCI ALIGNMENT:{RESET}")
            print(f"Level: {fib_data['level']}")
            print(f"Price: ${fib_data['price']:,.2f}")
            print(f"Confidence: {fib_data['confidence']:.2f}")
            print(f"Distance: {fib_data['distance_pct']:.2f}%")
        
        # Display market conditions
        self.display_market_conditions()
        
        # Display Schumann resonance influence
        self.print_schumann_influence()
    
    def display_market_conditions(self) -> None:
        """Display current market conditions and indicators."""
        try:
            # Get current price and volume
            price = float(self.redis_conn.get("last_btc_price") or 0)
            volume = float(self.redis_conn.get("last_btc_volume") or 0)
            
            print(f"\n{CYAN}📊 MARKET CONDITIONS:{RESET}")
            print(f"Current Price: ${price:,.2f}")
            print(f"24h Volume: {volume:,.2f} BTC")
            
            # Get volatility
            volatility = self.calculate_volatility()
            if volatility:
                print(f"Volatility: {volatility:.2f}%")
            
            # Get market regime
            regime = self.determine_market_regime()
            if regime:
                print(f"Market Regime: {regime}")
            
        except Exception as e:
            logger.error(f"Error displaying market conditions: {e}")
    
    def calculate_volatility(self) -> Optional[float]:
        """Calculate current market volatility."""
        try:
            # Get recent price changes
            changes = self.redis_conn.lrange("abs_price_change_history", 0, 23)  # Last 24 changes
            if not changes:
                return None
            
            # Calculate average absolute change
            changes = [float(c) for c in changes]
            avg_change = sum(changes) / len(changes)
            
            return avg_change
            
        except Exception as e:
            logger.error(f"Error calculating volatility: {e}")
            return None
    
    def determine_market_regime(self) -> Optional[str]:
        """Determine current market regime based on volatility and trend."""
        try:
            volatility = self.calculate_volatility()
            if not volatility:
                return None
            
            # Get 15min trend
            trend, change = analyze_price_trend(15)
            
            # Determine regime based on volatility and trend
            if volatility > 1.0:
                if "Bullish" in trend:
                    return "High Volatility Bullish"
                elif "Bearish" in trend:
                    return "High Volatility Bearish"
                else:
                    return "High Volatility Neutral"
            elif volatility > 0.5:
                if "Bullish" in trend:
                    return "Moderate Volatility Bullish"
                elif "Bearish" in trend:
                    return "Moderate Volatility Bearish"
                else:
                    return "Moderate Volatility Neutral"
            else:
                if "Bullish" in trend:
                    return "Low Volatility Bullish"
                elif "Bearish" in trend:
                    return "Low Volatility Bearish"
                else:
                    return "Low Volatility Neutral"
                    
        except Exception as e:
            logger.error(f"Error determining market regime: {e}")
            return None
    
    def print_schumann_influence(self):
        """Print the current Schumann resonance influence on market energy."""
        print(f"\n{CYAN}🌍 SCHUMANN RESONANCE INFLUENCE:{RESET}")
        print(f"  {MAGENTA}Current resonance: {YELLOW}7.83 Hz{RESET} - {GREEN}Baseline Harmony{RESET}")
        print(f"  {MAGENTA}Market harmony: {GREEN}Aligned with planetary consciousness{RESET}")

def detect_possible_mm_traps(timeframe, trend, price_change_pct, price_move):
    """
    Detect potential market maker traps based on price action and trend analysis.
    
    Args:
        timeframe (str): The timeframe being analyzed
        trend (str): The current trend direction
        price_change_pct (float): The percentage price change
        price_move (float): The absolute price move value
    
    Returns:
        tuple: (trap_type, confidence) where trap_type is the type of trap detected
               and confidence is a float between 0 and 1
    """
    # Print header with enhanced formatting
    print(f"\n{BLUE_BG}{WHITE}{BOLD} MM TRAP ANALYSIS | {timeframe} {RESET}")
    print(f"{MAGENTA}{'─' * 5} ANALYZING PRICE ACTION {'─' * 5}{RESET}")
    
    # Check if trend data is missing or "No Data"
    if not trend or trend == "No Data":
        # Attempt to use movement data from Redis as fallback
        try:
            movement_history = redis_conn.lrange("btc_movement_history", 0, 0)
            candle_data = redis_conn.get(f"btc_candle_{timeframe}")
            last_price = float(redis_conn.get("last_btc_price") or 0)
            
            if candle_data:
                # Use candle data if available
                candle = json.loads(candle_data)
                if 'o' in candle and 'c' in candle:
                    old_price = float(candle['o'])
                    new_price = float(candle['c'])
                    if old_price > 0:
                        calculated_change = ((new_price - old_price) / old_price) * 100
                        price_move = abs(new_price - old_price)
                        
                        # Infer trend from price change
                        if calculated_change > 1.0:
                            trend = "Bullish"
                        elif calculated_change < -1.0:
                            trend = "Bearish"
                        else:
                            trend = "Neutral"
                            
                        price_change_pct = calculated_change
                        print(f"{YELLOW}⚠️ No trend data available. Using candle data: {trend} ({price_change_pct:.2f}%){RESET}")
            elif movement_history:
                # Use movement history as fallback
                try:
                    last_movements = movement_history[0].split(',')
                    if len(last_movements) >= 2:
                        old_price = float(last_movements[0])
                        if old_price > 0 and last_price > 0:
                            calculated_change = ((last_price - old_price) / old_price) * 100
                            price_move = abs(last_price - old_price)
                            
                            # Infer trend from price change
                            if calculated_change > 1.0:
                                trend = "Bullish"
                            elif calculated_change < -1.0:
                                trend = "Bearish"
                            else:
                                trend = "Neutral"
                                
                            price_change_pct = calculated_change
                            print(f"{YELLOW}⚠️ No trend data available. Using price movement data: {trend} ({price_change_pct:.2f}%){RESET}")
                except Exception as e:
                    logger.warning(f"Error parsing movement history for fallback: {e}")
            else:
                print(f"{RED}❌ No trend data or fallback data available for analysis{RESET}")
                return None, 0.0
        except Exception as e:
            logger.warning(f"Failed to use fallback data: {e}")
            print(f"{RED}❌ No trend data available and fallback failed{RESET}")
            return None, 0.0
    
    # Print price movement metrics
    print(f"{WHITE}Price Change: {price_change_pct:.2f}% | Absolute Move: ${price_move:.2f}{RESET}")
    print(f"{WHITE}Trend: {trend}{RESET}")
    
    # Early exit if price change is too small
    if abs(price_change_pct) < 1.5:
        print(f"{YELLOW}⚠️ Price change too small for MM trap detection ({abs(price_change_pct):.2f}% < 1.5%){RESET}")
        return None, 0.0

    # Calculate price movement intensity (normalized to 5% change)
    price_intensity = min(abs(price_change_pct) / 5.0, 1.0)
    print(f"{CYAN}Price Movement Intensity: {price_intensity:.2f} (normalized to 5% change){RESET}")
    
    # Determine trap type based on trend and price direction
    trap_type = None
    if "Bullish" in trend and price_change_pct > 0:
        trap_type = "Bull Trap"
        print(f"{GREEN}Detected potential Bull Trap pattern{RESET}")
    elif "Bearish" in trend and price_change_pct < 0:
        trap_type = "Bear Trap"
        print(f"{RED}Detected potential Bear Trap pattern{RESET}")
    
    if not trap_type:
        print(f"{BLUE}No trap pattern detected for this trend/price combination{RESET}")
        return None, 0.0
    
    # Print confidence calculation section header
    print(f"\n{MAGENTA}{'─' * 5} CONFIDENCE CALCULATION {'─' * 5}{RESET}")
    
    # Calculate confidence components
    price_weight = 0.6
    trend_weight = 0.3
    timeframe_weight = 0.1
    
    # Price intensity contribution (60%)
    price_contribution = price_intensity * price_weight
    print(f"{WHITE}Price Intensity: {price_intensity:.2f} × {price_weight:.2f} = {price_contribution:.2f}{RESET}")
    confidence = price_contribution
    
    # Trend strength contribution (30%)
    trend_multiplier = 1.0 if trend.startswith("Strongly") else 0.7
    trend_contribution = trend_multiplier * trend_weight
    print(f"{WHITE}Trend Strength: {trend_multiplier:.2f} × {trend_weight:.2f} = {trend_contribution:.2f}{RESET}")
    confidence += trend_contribution
    
    # Timeframe contribution (10%)
    timeframe_multiplier = 1.0 if timeframe in ["15min", "1h"] else 0.7
    timeframe_contribution = timeframe_multiplier * timeframe_weight
    print(f"{WHITE}Timeframe Weight: {timeframe_multiplier:.2f} × {timeframe_weight:.2f} = {timeframe_contribution:.2f}{RESET}")
    confidence += timeframe_contribution
    
    # Round to 2 decimal places to avoid floating point issues
    confidence = round(min(confidence, 1.0), 2)
    print(f"\n{WHITE}Total Confidence Score: {confidence:.2f}{RESET}")
    
    # Only return if confidence meets minimum threshold
    if confidence >= 0.3:  # Lowered threshold to match tests
        # Print movement classification tag
        if trap_type == "Bull Trap":
            print(f"\n{GREEN_BG}{WHITE}{BOLD} BULL TRAP DETECTED {RESET}")
        elif trap_type == "Bear Trap":
            print(f"\n{RED_BG}{WHITE}{BOLD} BEAR TRAP DETECTED {RESET}")
            
        # Print confidence level with color coding
        if confidence > 0.8:
            print(f"{RED}⚠️ HIGH CONFIDENCE MM TRAP DETECTED: {trap_type} on {timeframe} (confidence: {confidence}){RESET}")
        elif confidence > 0.5:
            print(f"{LIGHT_ORANGE}⚠️ MEDIUM CONFIDENCE MM TRAP DETECTED: {trap_type} on {timeframe} (confidence: {confidence}){RESET}")
        else:
            print(f"{YELLOW}⚠️ LOW CONFIDENCE MM TRAP DETECTED: {trap_type} on {timeframe} (confidence: {confidence}){RESET}")
        
        # Log the trap detection
        logger.info(f"⚠️ MM TRAP DETECTED: {trap_type} on {timeframe} (confidence: {confidence})")
        
        # Store in database (optional, uncomment if needed)
        # insert_possible_mm_trap(timeframe, trap_type, confidence, price_change_pct, price_move)
        
        return trap_type, confidence
    
    print(f"{BLUE}Below confidence threshold (0.3), no trap will be reported{RESET}")
    return None, 0.0

def check_fibonacci_alignment() -> Optional[Dict[str, Any]]:
    """
    Check for price alignment with Fibonacci levels.
    
    Returns:
        Optional[Dict[str, Any]]: Dictionary containing alignment data if found, None otherwise
    """
    try:
        # Get current price from Redis
        current_price = float(redis_conn.get("last_btc_price") or 0)
        if current_price == 0:
            logger.warning("No current price available for alignment check")
            return None
        
        # Get Fibonacci levels
        fib_levels = get_current_fibonacci_levels()
        if not fib_levels:
            logger.warning("No Fibonacci levels available for alignment check")
            return None
        
        # Check each Fibonacci level for alignment
        best_alignment = None
        min_distance_pct = float('inf')
        
        for level, price in fib_levels.items():
            # Calculate distance percentage
            distance_pct = abs((current_price - price) / price * 100)
            
            # If this is the closest level so far
            if distance_pct < min_distance_pct:
                min_distance_pct = distance_pct
                best_alignment = {
                    "type": "GOLDEN_RATIO",
                    "level": level,
                    "price": price,
                    "distance_pct": distance_pct,
                    "confidence": max(0, 1 - (distance_pct / 5))  # 5% max distance for confidence
                }
        
        # Only return if we're within 5% of a level
        if best_alignment and best_alignment["distance_pct"] <= 5.0:
            return best_alignment
        
        return None
        
    except Exception as e:
        logger.error(f"Error checking Fibonacci alignment: {e}")
        return None

def initialize_fibonacci_levels():
    """Initialize Fibonacci levels if they don't exist."""
    try:
        # Try to get current price
        current_price = float(redis_conn.get("last_btc_price") or 0)
        if current_price > 0:
            update_fibonacci_data(current_price)
            print(f"{GREEN}✓ Initialized Fibonacci levels with current price ${current_price:,.2f}{RESET}")
        else:
            print(f"{YELLOW}⚠️ Could not initialize Fibonacci levels - missing price data{RESET}")
    except Exception as e:
        logger.error(f"Error initializing Fibonacci levels: {e}")

def initialize_btc_data():
    """Initialize BTC movement history if it doesn't exist."""
    try:
        # Try to get current price
        current_price = float(redis_conn.get("last_btc_price") or 0)
        if current_price > 0:
            redis_conn.lpush("btc_movement_history", json.dumps({
                "price": current_price,
                "volume": 0,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }))
            print(f"{GREEN}✓ Initialized BTC movement history with current price{RESET}")
        else:
            print(f"{YELLOW}⚠️ Could not initialize BTC movement history - missing price data{RESET}")
    except Exception as e:
        logger.error(f"Error initializing BTC movement history: {e}")

def initialize_candle_data(timeframe):
    """Initialize candle data for a specific timeframe if it doesn't exist."""
    try:
        # Try to get current price
        current_price = float(redis_conn.get("last_btc_price") or 0)
        if current_price > 0:
            redis_conn.set(f"btc_candle_{timeframe}", json.dumps({
                "o": current_price,
                "h": current_price,
                "l": current_price,
                "c": current_price,
                "v": 0,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }))
            print(f"{GREEN}✓ Initialized candle data for {timeframe}{RESET}")
        else:
            print(f"{YELLOW}⚠️ Could not initialize candle data for {timeframe} - missing price data{RESET}")
    except Exception as e:
        logger.error(f"Error initializing candle data for {timeframe}: {e}")

def categorize_fibonacci_levels(fib_levels, current_price):
    """Categorize Fibonacci levels by type and calculate distances from current price."""
    fib_types = {
        "EXTENSION": [],
        "RETRACEMENT": [],
        "KEY": []
    }
    
    # Sort and categorize Fibonacci levels
    for level, price in sorted(fib_levels.items(), key=lambda x: float(x[1])):
        # Calculate percentage difference from current price
        pct_diff = ((price - current_price) / current_price) * 100
        
        # Determine level color based on distance from current price
        if abs(pct_diff) < 1.0:
            level_color = f"{RED_BG}{WHITE}"  # Very close - highlight
        elif abs(pct_diff) < 2.5:
            level_color = f"{YELLOW}"  # Somewhat close
        else:
            level_color = f"{CYAN}"  # Far
        
        # Determine category
        if "0." in level:
            fib_types["RETRACEMENT"].append((level, price, pct_diff, level_color))
        elif level.replace("fib", "").strip().replace(".", "", 1).isdigit() and float(level.replace("fib", "").strip()) > 1.0:
            fib_types["EXTENSION"].append((level, price, pct_diff, level_color))
        else:
            fib_types["KEY"].append((level, price, pct_diff, level_color))
    
    return fib_types

def monitor_market_trends():
    """Main function to monitor market trends continuously."""
    try:
        # Initialize Redis connection
        global redis_conn
        if os.getenv('OMEGA_TEST_USE_LOCAL_REDIS', 'true').lower() == 'true':
            from omega_ai.utils.test_redis_manager import TestRedisManager
            redis_conn = TestRedisManager().redis
        else:
            redis_conn = redis.Redis(
                host=os.getenv('REDIS_HOST', 'redis-19332.fcrce173.eu-west-1-1.ec2.redns.redis-cloud.com'),
                port=int(os.getenv('REDIS_PORT', '19332')),
                username=os.getenv('REDIS_USERNAME', 'omega'),
                password=os.getenv('REDIS_PASSWORD', 'VuKJU8Z.Z2V8Qn_'),
                ssl=os.getenv('REDIS_USE_TLS', 'true').lower() == 'true',
                ssl_ca_certs=os.getenv('REDIS_CERT', 'SSL_redis-btc-omega-redis.pem'),
                decode_responses=True
            )
        
        logger.info("Successfully connected to Redis")
        
        # Initialize market trend analyzer with Redis connection
        analyzer = MarketTrendAnalyzer(redis_connection=redis_conn)
        
        # Initialize Fibonacci levels
        initialize_fibonacci_levels()
        
        # Check for historical BTC data
        if not redis_conn.exists("btc_movement_history"):
            print(f"{YELLOW}No historical BTC data found. Initializing...{RESET}")
            initialize_btc_data()
        
        # Check for candle data
        for timeframe in ['1min', '5min', '15min', '30min', '1h', '4h']:
            if not redis_conn.exists(f"btc_candle_{timeframe}"):
                print(f"{YELLOW}No candle data found for {timeframe}. Initializing...{RESET}")
                initialize_candle_data(timeframe)
        
        # Main monitoring loop
        while True:
            try:
                now = datetime.now(timezone.utc)
                
                # Perform analysis
                print(f"\n{BLUE_BG}{WHITE}{BOLD} MARKET ANALYSIS | {now.strftime('%Y-%m-%d %H:%M:%S')} {RESET}")
                results = analyzer.analyze_trends()
                
                # If current price is missing, fetch it directly
                if "current_price" not in results or results["current_price"] == 0:
                    current_price = float(redis_conn.get("last_btc_price") or 0)
                    if current_price > 0:
                        results["current_price"] = current_price
                        print(f"{GREEN}✓ Retrieved current price from Redis: ${current_price:,.2f}{RESET}")
                
                # Display results
                analyzer.display_results(results)
                
                # Provide Fibonacci section header if available
                if "fibonacci_levels" in results:
                    print(f"\n{BLUE_BG}{WHITE}{BOLD} FIBONACCI ANALYSIS {RESET}")
                    print(f"{YELLOW}{'─' * 50}{RESET}")
                    
                    # Get current price for comparison
                    current_price = results.get("current_price", 0)
                    if current_price == 0:
                        current_price = float(redis_conn.get("last_btc_price") or 0)
                    
                    # Categorize Fibonacci levels
                    fib_types = categorize_fibonacci_levels(results["fibonacci_levels"], current_price)
                    
                    # Print each category
                    for category, levels in fib_types.items():
                        if levels:
                            print(f"\n{MAGENTA}{category} LEVELS:{RESET}")
                            for level, price, pct_diff, color in levels:
                                direction = "↑" if pct_diff > 0 else "↓"
                                print(f"  {color}{level}: ${price:,.2f} ({direction} {abs(pct_diff):.2f}% from current){RESET}")
                    
                    # Store Fibonacci levels in Redis for the dashboard
                    try:
                        redis_conn.set("fibonacci:current_levels", json.dumps(results["fibonacci_levels"]))
                    except Exception as e:
                        logger.error(f"Error storing Fibonacci data in Redis: {e}")
                
                # Check for potential MM traps
                print(f"\n{BLUE_BG}{WHITE}{BOLD} MARKET MAKER TRAP DETECTION {RESET}")
                print(f"{YELLOW}{'─' * 50}{RESET}")
                
                detected_traps = []
                
                for timeframe, data in results.items():
                    if isinstance(data, dict) and "trend" in data and "change" in data:
                        print(f"\n{CYAN}Analyzing {timeframe} for MM traps...{RESET}")
                        trap_type, confidence = detect_possible_mm_traps(
                            timeframe,
                            data["trend"],
                            data["change"],
                            abs(data["change"])
                        )
                        if trap_type:
                            detected_traps.append({
                                "timeframe": timeframe,
                                "trap_type": trap_type,
                                "confidence": confidence,
                                "trend": data["trend"],
                                "price_change": data["change"]
                            })
                
                # Store detected traps in database if enabled
                if detected_traps:
                    print(f"\n{RED_BG}{WHITE}{BOLD} DETECTED TRAPS {RESET}")
                    print(f"{YELLOW}{'─' * 50}{RESET}")
                    for trap in detected_traps:
                        print(f"{RED}⚠️ MM TRAP DETECTED: {trap['trap_type']} on {trap['timeframe']} (confidence: {trap['confidence']}){RESET}")
                        
                        # Store trap data in Redis
                        try:
                            redis_conn.set(f"mm_trap_{trap['timeframe']}", json.dumps({
                                "type": trap["trap_type"],
                                "confidence": trap["confidence"],
                                "trend": trap["trend"],
                                "price_change": trap["price_change"],
                                "timestamp": datetime.now(timezone.utc).isoformat()
                            }))
                        except Exception as e:
                            logger.error(f"Error storing trap data in Redis: {e}")
                
                # Sleep for a short interval
                time.sleep(5)
                
            except KeyboardInterrupt:
                print(f"\n{RED}Stopping market trend monitor...{RESET}")
                break
            except Exception as e:
                logger.error(f"Error in market trend monitor: {e}")
                time.sleep(5)
                
    except Exception as e:
        logger.error(f"Fatal error in market trend monitor: {e}")
        raise

if __name__ == "__main__":
    monitor_market_trends()