import time
import redis
import logging
import json
import os
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timezone
from omega_ai.ml.market_trends_model import MarketTrendsModel
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
MAGENTA_BG = "\033[45m"     # Background for magenta text

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

class AIEnhancedMarketTrendAnalyzer:
    """Analyzes market trends with multiple indicators, timeframes and AI prediction."""
    
    def __init__(self):
        """Initialize the market trend analyzer with AI enhancement."""
        self.timeframes = [1, 5, 15, 30, 60, 240, 720, 1444]  # minutes - extended to include up to 1444 minutes
        self.consecutive_errors = 0
        self.last_analysis_time = None
        self.analysis_interval = 5  # seconds
        
        # Initialize AI model
        try:
            self.ai_model = MarketTrendsModel(
                redis_host=redis_host,
                redis_port=redis_port
            )
            logger.info("Successfully initialized AI model")
        except Exception as e:
            logger.error(f"Failed to initialize AI model: {e}")
            self.ai_model = None
        
    def analyze_trends(self) -> Dict[str, Any]:
        """Analyze market trends across multiple timeframes with AI enhancement."""
        try:
            results = {}
            
            # Get current price from Redis
            current_price = float(redis_conn.get("last_btc_price") or 0)
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
            
            # Add AI predictions if model is available
            if self.ai_model:
                try:
                    ai_predictions = self.ai_model.generate_predictions()
                    results["ai_predictions"] = ai_predictions
                    logger.info("Added AI predictions to analysis results")
                except Exception as e:
                    logger.error(f"Error generating AI predictions: {e}")
            
            # Reset error counter on successful analysis
            self.consecutive_errors = 0
            self.last_analysis_time = datetime.now(timezone.utc)
            
            return results
            
        except Exception as e:
            self.consecutive_errors += 1
            logger.error(f"Error in trend analysis: {e}")
            return {}
    
    def display_results(self, results: Dict[str, Any]) -> None:
        """Display analysis results with enhanced formatting and AI predictions."""
        # Display current BTC price prominently at the top
        current_price = results.get("current_price", 0)
        print(f"\n{BLUE_BG}{WHITE}{BOLD} 💰 CURRENT BTC PRICE: ${current_price:,.2f} 💰 {RESET}")
        
        print(f"\n{YELLOW}════════════════ {GREEN}OMEGA RASTA{YELLOW} MARKET TREND ANALYSIS ════════════════{RESET}")
        
        # Display trends for each timeframe with enhanced formatting
        for timeframe, data in results.items():
            if timeframe != "fibonacci_levels" and timeframe != "fibonacci_alignment" and timeframe != "current_price" and timeframe != "ai_predictions":
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
        
        # Display AI predictions if available
        if "ai_predictions" in results:
            self.display_ai_predictions(results["ai_predictions"])
    
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
    
    def display_ai_predictions(self, ai_predictions: Dict[str, Any]) -> None:
        """Display AI model predictions with enhanced formatting."""
        print(f"\n{MAGENTA_BG}{WHITE}{BOLD} 🧠 AI MODEL PREDICTIONS 🧠 {RESET}")
        print(f"{YELLOW}{'─' * 60}{RESET}")
        
        try:
            # Display trend prediction
            trend_data = ai_predictions.get("trend", {})
            trend = trend_data.get("trend", "Unknown")
            confidence = trend_data.get("confidence", 0.0)
            
            trend_color = GREEN if trend == "Bullish" else RED if trend == "Bearish" else CYAN
            print(f"{BOLD}📈 AI TREND PREDICTION:{RESET}")
            print(f"  Direction: {trend_color}{trend}{RESET}")
            print(f"  Confidence: {self.format_confidence(confidence)}")
            
            # Display price prediction
            price_data = ai_predictions.get("price", {})
            predicted_price = price_data.get("price", 0.0)
            current_price = price_data.get("current_price", 0.0)
            pct_change = price_data.get("pct_change", 0.0)
            
            price_color = GREEN if pct_change > 0 else RED if pct_change < 0 else CYAN
            print(f"\n{BOLD}💰 AI PRICE PREDICTION:{RESET}")
            print(f"  Current: ${current_price:,.2f}")
            print(f"  Predicted: {price_color}${predicted_price:,.2f} ({pct_change:+.2f}%){RESET}")
            
            # Display trap prediction
            trap_data = ai_predictions.get("trap", {})
            trap_detected = trap_data.get("trap_detected", False)
            trap_confidence = trap_data.get("confidence", 0.0)
            trap_type = trap_data.get("trap_type", None)
            
            print(f"\n{BOLD}⚠️ AI TRAP PREDICTION:{RESET}")
            if trap_detected:
                trap_color = RED if trap_type == "Bull Trap" else YELLOW if trap_type == "Bear Trap" else MAGENTA
                print(f"  {trap_color}TRAP DETECTED: {trap_type}{RESET}")
                print(f"  Confidence: {self.format_confidence(trap_confidence)}")
            else:
                print(f"  {GREEN}No trap detected{RESET}")
                print(f"  Confidence: {self.format_confidence(trap_confidence)}")
            
            # Display divine wisdom if available
            if "divine_wisdom" in ai_predictions:
                wisdom = ai_predictions["divine_wisdom"]
                print(f"\n{MAGENTA}{BOLD}🔮 DIVINE AI WISDOM:{RESET}")
                print(f"  {CYAN}{wisdom}{RESET}")
            
            print(f"\n{YELLOW}AI Timestamp: {ai_predictions.get('timestamp', 'Unknown')}{RESET}")
            
        except Exception as e:
            logger.error(f"Error displaying AI predictions: {e}")
            print(f"{RED}Error displaying AI predictions: {e}{RESET}")
    
    def format_confidence(self, confidence: float) -> str:
        """Format confidence value with color coding."""
        if confidence > 0.8:
            return f"{GREEN}{confidence:.2f}{RESET}"
        elif confidence > 0.6:
            return f"{BLUE}{confidence:.2f}{RESET}"
        elif confidence > 0.4:
            return f"{YELLOW}{confidence:.2f}{RESET}"
        else:
            return f"{RED}{confidence:.2f}{RESET}"
    
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

def monitor_market_trends_with_ai():
    """Main function to monitor market trends continuously with AI enhancement."""
    print(f"\n{BLUE_BG}{WHITE}{BOLD} 🚀 OMEGA MARKET TREND ANALYZER WITH AI v1.0 {RESET}")
    print(f"{MAGENTA}Starting AI-Enhanced Market Trend Analysis with RASTA VIBES...{RESET}")
    print(f"{GREEN}JAH BLESS THE GOLDEN RATIO AND THE DIVINE FIBONACCI SEQUENCE!{RESET}")
    
    analyzer = AIEnhancedMarketTrendAnalyzer()
    
    while True:
        try:
            # Check if it's time for analysis
            now = datetime.now(timezone.utc)
            if (analyzer.last_analysis_time is None or 
                (now - analyzer.last_analysis_time).total_seconds() >= analyzer.analysis_interval):
                
                # Perform analysis
                print(f"\n{BLUE_BG}{WHITE}{BOLD} AI-ENHANCED MARKET ANALYSIS | {now.strftime('%Y-%m-%d %H:%M:%S')} {RESET}")
                results = analyzer.analyze_trends()
                
                # Display results
                analyzer.display_results(results)
                
                # Sleep for a minute before next analysis with JAH BLESSING
                print(f"\n{GREEN}JAH BLESS THE GOLDEN RATIO - Waiting for next analysis cycle...{RESET}")
                print(f"{YELLOW}{'─' * 50}{RESET}")
            
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
    monitor_market_trends_with_ai() 