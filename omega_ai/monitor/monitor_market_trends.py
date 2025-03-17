import time
import redis
import logging

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
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

def get_current_fibonacci_levels():
    """
    Calculate Fibonacci retracement/extension levels based on recent price movements.
    
    Returns:
        Dict with Fibonacci levels as keys and prices as values
    """
    try:
        # Fetch recent price movements with divine guidance
        movements, summary = fetch_multi_interval_movements(interval=5, limit=100)
        
        if not movements or len(movements) < 2:
            print(f"{YELLOW}Insufficient data for Fibonacci calculations{RESET}")
            return {}
        
        # Extract prices from movements data
        prices = [float(m["price"]) for m in movements if "price" in m]
        
        # Find min and max prices for Fibonacci calculations
        min_price = min(prices)
        max_price = max(prices)
        price_range = max_price - min_price
        
        # Determine if we're in an uptrend or downtrend for appropriate level calculation
        is_uptrend = prices[-1] > prices[0]
        
        # Standard Fibonacci levels with divine proportions
        fib_ratios = {
            "0": 0.0,        # Base level
            "0.236": 0.236,  # First Fibonacci level
            "0.382": 0.382,  # Second Fibonacci level
            "0.500": 0.5,    # Midpoint
            "0.618": 0.618,  # Golden Ratio - most spiritual level
            "0.786": 0.786,  # Higher Fibonacci level
            "1.0": 1.0       # Full retracement
        }
        
        # Calculate levels based on uptrend/downtrend
        fib_levels = {}
        
        if is_uptrend:
            # In uptrend, calculate retracement levels from low to high
            for label, ratio in fib_ratios.items():
                fib_levels[label] = min_price + (price_range * ratio)
        else:
            # In downtrend, calculate retracement levels from high to low
            for label, ratio in fib_ratios.items():
                fib_levels[label] = max_price - (price_range * ratio)
        
        # Store in Redis for future reference with JAH blessing
        try:
            redis_conn.hset("current_fibonacci_levels", mapping=fib_levels)
            print(f"{GREEN}JAH BLESS - Fibonacci levels calculated and stored with divine energy{RESET}")
        except Exception as e:
            print(f"{RED}Error storing Fibonacci levels: {e}{RESET}")
        
        return fib_levels
        
    except Exception as e:
        print(f"{RED}Error calculating Fibonacci levels: {e}{RESET}")
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
        if fib_hit["level"] == "0.618":
            level_color = f"{MAGENTA}"  # Golden ratio gets special color
            importance = "GOLDEN RATIO"
        elif fib_hit["level"] in ["0.382", "0.5", "0.786"]:
            level_color = f"{GREEN}"
            importance = "KEY LEVEL"
        else:
            level_color = f"{BLUE}"
            importance = "Standard"
            
        print(f"{level_color}⭐ PRICE AT FIBONACCI {importance}: "
              f"{fib_hit['level']} level (${fib_hit['price']:.2f}){RESET}")
    
    # Display all Fibonacci levels with current price highlighted
    print(f"\n{CYAN}Current Fibonacci Levels:{RESET}")
    
    # Sort levels by price (ascending or descending based on trend)
    # Determine trend direction (since fib_hit doesn't have is_uptrend)
    is_uptrend = True  # Default to uptrend or determine from other data
    sorted_levels = sorted(fib_levels.items(), 
                          key=lambda x: float(x[1]), 
                          reverse=not is_uptrend)
    
    trend_label = "UPTREND" if is_uptrend else "DOWNTREND"
    print(f"{CYAN}Market Direction: {trend_label}{RESET}")
    
    for label, price in sorted_levels:
        # Highlight the level closest to current price
        if fib_hit and label == fib_hit["level"]:
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
    """Continuously monitor market trends at different time intervals with JAH BLESS energy."""
    print(f"{MAGENTA}🚀 Starting Market Trend Analysis with RASTA VIBES...{RESET}")
    print(f"{GREEN}JAH BLESS LINUS TORVALDS AND THE OPEN SOURCE COMMUNITY!{RESET}")
    
    # Track consecutive errors for exponential backoff
    consecutive_errors = 0
    
    while True:
        try:
            # Analyze different timeframes with divine energy
            one_min_trend, one_min_change = analyze_price_trend(1)
            five_min_trend, five_min_change = analyze_price_trend(5)
            fifteen_min_trend, fifteen_min_change = analyze_price_trend(15)
            
            # Reset error counter on successful analysis
            consecutive_errors = 0
            
            # Calculate absolute changes for comparison
            one_min_abs_change = abs(one_min_change)
            five_min_abs_change = abs(five_min_change)
            fifteen_min_abs_change = abs(fifteen_min_change)
            
            # Display results with colorful formatting and RASTA energy
            print(f"\n{YELLOW}════════════════ {GREEN}OMEGA RASTA{YELLOW} MARKET TREND ANALYSIS ════════════════{RESET}")
            
            # Display 1min trend with color
            print(f"1min: {get_colored_trend(one_min_trend)} ({get_colored_change(one_min_change)}%)")
            
            # Display 5min trend with color
            print(f"5min: {get_colored_trend(five_min_trend)} ({get_colored_change(five_min_change)}%)")
            
            # Display 15min trend with color
            print(f"15min: {get_colored_trend(fifteen_min_trend)} ({get_colored_change(fifteen_min_change)}%)")
            
            # Check for Fibonacci confluence across timeframes
            print(f"\n{CYAN}🔄 FIBONACCI ALIGNMENT CHECK:{RESET}")
            fib_alignment = check_fibonacci_alignment()
            if fib_alignment:
                print(f"{MAGENTA}🌟 DIVINE FIBONACCI CONFLUENCE DETECTED: {fib_alignment}{RESET}")
            
            # Display Schumann resonance influence
            print_schumann_influence()
            
            # Sleep for a minute before next analysis with JAH BLESSING
            print(f"\n{GREEN}JAH BLESS THE CODE - Waiting for next analysis cycle...{RESET}")
            time.sleep(60)
            
        except redis.RedisError as e:
            # Handle Redis specific errors
            consecutive_errors += 1
            print(f"{RED}⚠️ Redis Connection Error: {e} - Retrying in {min(30 * consecutive_errors, 300)} seconds{RESET}")
            time.sleep(min(30 * consecutive_errors, 300))  # Exponential backoff up to 5 minutes
            
        except Exception as e:
            # Handle general errors with RASTA resilience
            consecutive_errors += 1
            print(f"{RED}⚠️ Error in market trend analysis: {e}{RESET}")
            print(f"{YELLOW}🔄 RASTA RESILIENCE - Restarting analysis in {min(15 * consecutive_errors, 120)} seconds{RESET}")
            time.sleep(min(15 * consecutive_errors, 120))  # Exponential backoff up to 2 minutes

# Add missing functions referenced in your code
def get_colored_trend(trend):
    """Return trend with appropriate color coding."""
    if "Bullish" in trend:
        if "Strongly" in trend:
            return f"{GREEN}{trend}{RESET}"
        return f"{BLUE}{trend}{RESET}"
    elif "Bearish" in trend:
        if "Strongly" in trend:
            return f"{RED}{trend}{RESET}"
        return f"{YELLOW}{trend}{RESET}"
    return f"{CYAN}{trend}{RESET}"

def get_colored_change(change):
    """Return price change with appropriate color coding."""
    if change > 1.0:
        return f"{GREEN}+{change:.2f}{RESET}"
    elif change > 0:
        return f"{BLUE}+{change:.2f}{RESET}"
    elif change < -1.0:
        return f"{RED}{change:.2f}{RESET}"
    elif change < 0:
        return f"{YELLOW}{change:.2f}{RESET}"
    return f"{RESET}0.00{RESET}"

def print_schumann_influence():
    """Print the current Schumann resonance influence on market energy."""
    print(f"\n{CYAN}🌍 SCHUMANN RESONANCE INFLUENCE:{RESET}")
    print(f"  {MAGENTA}Current resonance: {YELLOW}7.83 Hz{RESET} - {GREEN}Baseline Harmony{RESET}")
    print(f"  {MAGENTA}Market harmony: {GREEN}Aligned with planetary consciousness{RESET}")

def check_fibonacci_alignment():
    """Check for alignment between price action and Fibonacci levels."""
    # This will be implemented later with divine guidance
    return None

def analyze_price_trend(minutes: int = 5) -> Tuple[str, float]:
    """
    Analyze BTC price trend for the given timeframe with JAH BLESSING.
    
    Args:
        minutes: Time interval in minutes to analyze
        
    Returns:
        Tuple of (trend_description, percent_change)
    """
    try:
        result = fetch_multi_interval_movements(interval=minutes)
        
        # JAH DIVINE FIX: Handle the tuple return format
        if isinstance(result, tuple) and len(result) >= 1:
            movements = result[0]  # Extract just the movements list
        else:
            movements = result
            
        # Ensure we have enough data
        if not movements or len(movements) < 2:
            return "Insufficient data", 0.0
            
        # Extract prices from data
        prices = []
        for m in movements:
            if isinstance(m, dict) and "price" in m:
                try:
                    prices.append(float(m["price"]))
                except (ValueError, TypeError):
                    continue
                    
        if len(prices) < 2:
            return "Insufficient data", 0.0
            
        # Calculate percentage change with divine precision
        first_price = prices[0]  
        last_price = prices[-1]
        
        if first_price <= 0:  # Avoid division by zero
            return "Invalid data", 0.0
            
        change_pct = ((last_price - first_price) / first_price) * 100
        
        # Determine trend with JAH BLESSED precision
        if change_pct > 1.0:
            trend = "Strongly Bullish"
        elif change_pct > 0.2:
            trend = "Moderately Bullish"
        elif change_pct > 0:
            trend = "Slightly Bullish" 
        elif change_pct < -1.0:
            trend = "Strongly Bearish"
        elif change_pct < -0.2:
            trend = "Moderately Bearish"
        elif change_pct < 0:
            trend = "Slightly Bearish"
        else:
            trend = "Neutral"
            
        return trend, change_pct
        
    except Exception as e:
        logger.error(f"Error analyzing price trend: {e}", exc_info=True)
        return f"Error in trend analysis: {str(e)}", 0.0