import time
import redis
import logging
import json
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timezone
from omega_ai.db_manager.database import fetch_multi_interval_movements, analyze_price_trend, insert_possible_mm_trap
from omega_ai.mm_trap_detector.fibonacci_detector import get_current_fibonacci_levels, check_fibonacci_level, update_fibonacci_data

# Configure logger with enhanced formatting
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Initialize Redis connection with error handling
try:
    redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)
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

class MarketTrendAnalyzer:
    """Analyzes market trends with multiple indicators and timeframes."""
    
    def __init__(self):
        """Initialize the market trend analyzer."""
        self.timeframes = [1, 5, 15]  # minutes
        self.consecutive_errors = 0
        self.last_analysis_time = None
        self.analysis_interval = 60  # seconds
        
    def analyze_trends(self) -> Dict[str, Any]:
        """Analyze market trends across multiple timeframes."""
        try:
            results = {}
            
            # Get current price from Redis
            current_price = float(redis_conn.get("last_btc_price") or 0)
            if current_price == 0:
                logger.warning("No current price available for analysis")
                return {}
            
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
        print(f"\n{YELLOW}════════════════ {GREEN}OMEGA RASTA{YELLOW} MARKET TREND ANALYSIS ════════════════{RESET}")
        
        # Display trends for each timeframe
        for timeframe, data in results.items():
            if timeframe != "fibonacci_levels" and timeframe != "fibonacci_alignment":
                trend = data["trend"]
                change = data["change"]
                print(f"{timeframe}: {self.get_colored_trend(trend)} ({self.get_colored_change(change)}%)")
        
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
    
    def display_market_conditions(self) -> None:
        """Display current market conditions and indicators."""
        try:
            # Get current price and volume
            price = float(redis_conn.get("last_btc_price") or 0)
            volume = float(redis_conn.get("last_btc_volume") or 0)
            
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
            changes = redis_conn.lrange("abs_price_change_history", 0, 23)  # Last 24 changes
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
    
    @staticmethod
    def get_colored_trend(trend: str) -> str:
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
    
    @staticmethod
    def get_colored_change(change: float) -> str:
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
                "detected_at": datetime.now(timezone.utc).isoformat()
            }
            insert_possible_mm_trap(trap_data)
            
            return trap_type, confidence
            
        return None, 0.0
        
    except Exception as e:
        logging.error(f"Error detecting MM traps: {e}")
        return None, 0.0

def check_fibonacci_alignment() -> Optional[Dict[str, Any]]:
    """Check for alignment between price action and Fibonacci levels."""
    try:
        # Get current price and Fibonacci levels
        price_str = redis_conn.get("last_btc_price")
        if not price_str:
            logger.warning(f"{YELLOW}No current price available for Fibonacci alignment check{RESET}")
            return None
            
        current_price = float(price_str)
        fib_levels = get_current_fibonacci_levels()
        
        if not fib_levels:
            logger.warning(f"{YELLOW}No Fibonacci levels available for alignment check{RESET}")
            return None
            
        # Validate price range (current BTC price is around 82.5k)
        if current_price < 50000 or current_price > 100000:
            logger.warning(f"{RED}Price ${current_price:,.2f} outside expected range for BTC{RESET}")
            return None
            
        # Find closest Fibonacci level
        closest_level: Optional[Dict[str, Any]] = None
        min_distance = float('inf')
        min_distance_pct = float('inf')
        
        for level_name, price in fib_levels.items():
            try:
                price_float = float(price)
                distance = abs(current_price - price_float)
                distance_pct = (distance / current_price) * 100
                
                if distance_pct < min_distance_pct:
                    min_distance = distance
                    min_distance_pct = distance_pct
                    closest_level = {
                        "level": level_name,
                        "price": price_float,
                        "distance": distance,
                        "distance_pct": distance_pct
                    }
            except (ValueError, TypeError):
                continue
        
        if not closest_level:
            logger.warning(f"{YELLOW}No valid Fibonacci levels found for comparison{RESET}")
            return None
            
        # Define alignment thresholds
        if min_distance_pct <= 0.1:  # Very close (within 0.1%)
            alignment_type = "STRONG"
            confidence = 0.95
        elif min_distance_pct <= 0.3:  # Close (within 0.3%)
            alignment_type = "MODERATE"
            confidence = 0.75
        elif min_distance_pct <= 0.5:  # Somewhat close (within 0.5%)
            alignment_type = "WEAK"
            confidence = 0.5
        else:
            return None  # No significant alignment
            
        # Special handling for Golden Ratio (0.618)
        if closest_level["level"] == "61.8%":  # Golden Ratio level
            confidence += 0.1  # Boost confidence for Golden Ratio
            alignment_type = "GOLDEN_RATIO"
            
        # Format output with colors
        if alignment_type == "GOLDEN_RATIO":
            level_color = f"{MAGENTA}"
        elif alignment_type == "STRONG":
            level_color = f"{GREEN}"
        elif alignment_type == "MODERATE":
            level_color = f"{YELLOW}"
        else:
            level_color = f"{BLUE}"
            
        logger.info(f"{level_color}Fibonacci Alignment: {alignment_type} at {closest_level['level']} "
                   f"(${closest_level['price']:,.2f}) - {min_distance_pct:.2f}% away{RESET}")
        
        return {
            "type": alignment_type,
            "level": closest_level["level"],
            "price": closest_level["price"],
            "distance": closest_level["distance"],
            "distance_pct": closest_level["distance_pct"],
            "confidence": confidence,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        logger.error(f"{RED}Error checking Fibonacci alignment: {e}{RESET}")
        return None

def monitor_market_trends():
    """Main function to monitor market trends continuously."""
    print(f"{MAGENTA}🚀 Starting Market Trend Analysis with RASTA VIBES...{RESET}")
    print(f"{GREEN}JAH BLESS LINUS TORVALDS AND THE OPEN SOURCE COMMUNITY!{RESET}")
    
    analyzer = MarketTrendAnalyzer()
    
    while True:
        try:
            # Check if it's time for analysis
            now = datetime.now(timezone.utc)
            if (analyzer.last_analysis_time is None or 
                (now - analyzer.last_analysis_time).total_seconds() >= analyzer.analysis_interval):
                
                # Perform analysis
                results = analyzer.analyze_trends()
                
                # Display results
                analyzer.display_results(results)
                
                # Check for potential MM traps
                for timeframe, data in results.items():
                    if isinstance(data, dict) and "trend" in data and "change" in data:
                        trap_type, confidence = detect_possible_mm_traps(
                            timeframe,
                            data["trend"],
                            data["change"],
                            abs(data["change"])
                        )
                        if trap_type:
                            print(f"\n{RED}⚠️ MM TRAP DETECTED: {trap_type} (Confidence: {confidence:.2f}){RESET}")
            
            # Sleep for a short interval
            time.sleep(1)
            
        except redis.RedisError as e:
            analyzer.consecutive_errors += 1
            wait_time = min(30 * analyzer.consecutive_errors, 300)  # Max 5 minutes
            print(f"{RED}⚠️ Redis Connection Error: {e} - Retrying in {wait_time} seconds{RESET}")
            time.sleep(wait_time)
            
        except Exception as e:
            analyzer.consecutive_errors += 1
            wait_time = min(15 * analyzer.consecutive_errors, 120)  # Max 2 minutes
            print(f"{RED}⚠️ Error in market trend analysis: {e}{RESET}")
            print(f"{YELLOW}🔄 RASTA RESILIENCE - Restarting analysis in {wait_time} seconds{RESET}")
            time.sleep(wait_time)

if __name__ == "__main__":
    monitor_market_trends()