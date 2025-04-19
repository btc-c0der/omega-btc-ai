
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

import datetime
import numpy as np
import redis
import traceback  # Missing import for traceback.format_exc()
from omega_ai.db_manager.database import fetch_recent_movements
from omega_ai.mm_trap_detector.high_frequency_detector import check_high_frequency_mode, register_trap_detection
from typing import List, Dict, Union, Optional, Any
import asyncio
from datetime import datetime, timezone
from omega_ai.config import REDIS_HOST, REDIS_PORT

class OmegaAlgo:
    """🔥 OMEGA BTC AI - Market Maker Trap Detection & Fibonacci Validation 🔱"""

    # ✅ Dynamic MM Detection Constants
    SCHUMANN_THRESHOLD = 10.0
    VOLATILITY_MULTIPLIER = 2.5
    MIN_LIQUIDITY_GRAB_THRESHOLD = 250
    PRICE_DROP_THRESHOLD = -0.02
    PRICE_PUMP_THRESHOLD = 0.02
    CHECK_INTERVAL = 30
    ROLLING_WINDOW = 30
    
    # Terminal Colors (deduplicated)
    CYAN = "\033[96m"
    RESET = "\033[0m"
    WHITE = "\033[97m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    RED = "\033[91m"
    YELLOW = "\033[93m"

    # ✅ Initialize Redis Connection
    redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    @staticmethod
    def calculate_fibonacci_levels(high, low):
        """📡 Generate Fibonacci retracement levels for a price range."""
        levels = [0.236, 0.382, 0.5, 0.618, 0.786]
        
        # ✅ Ensure `high` and `low` are floats (fix for Decimal issues)
        high, low = float(high), float(low)
        
        return {level: low + (high - low) * level for level in levels}


    @staticmethod
    def calculate_extended_fibonacci_levels(high, low):
        """Generate both Fibonacci retracement and extension levels for a price range."""
        retracement_levels = [0.236, 0.382, 0.5, 0.618, 0.786]
        extension_levels = [1.272, 1.618, 2.0, 2.618]
        
        levels = {}
        
        # Calculate retracements (price pullbacks)
        for level in retracement_levels:
            levels[f"R{level}"] = low + (high - low) * level
        
        # Calculate extensions (price continuation beyond the high)
        for level in extension_levels:
            levels[f"E{level}"] = high + (high - low) * (level - 1)
        
        return levels

    @classmethod
    async def is_fibo_organic(cls, latest_price: float, previous_price: float, volume: Optional[float] = None) -> str:
        """Enhanced multi-layer Fibonacci analysis for advanced trap detection."""
        
        # Get existing historical data
        historical_data = cls.redis_conn.lrange("btc_movement_history", -100, -1)
        if len(historical_data) < 10:
            print("⚠️ Insufficient data points for Fibonacci analysis")
            return "Insufficient Data"
        
        # Parse historical prices from Redis data
        historical_prices: List[float] = []
        historical_volumes: List[float] = []
        
        for data in historical_data:
            try:
                if ',' in data:
                    price_str, vol_str = data.split(',', 1)
                    price = float(price_str)
                    vol = float(vol_str) if vol_str else 0.0
                    historical_prices.append(price)
                    historical_volumes.append(vol)
                else:
                    price = float(data)
                    historical_prices.append(price)
            except (ValueError, TypeError):
                continue
        
        if len(historical_prices) < 10:
            print("⚠️ Insufficient valid price data points for Fibonacci analysis")
            return "Insufficient Data"

        # Initialize a placeholder for multi-timeframe Fibonacci levels
        multi_fib_levels = {}
        confluence_zones = []
        
        # Multi-timeframe Fibonacci analysis (using both retracements and extensions)
        try:
            multi_fib_levels, confluence_zones = cls.get_multi_timeframe_fibonacci(latest_price)
            
            # Log detected Fibonacci levels for debugging
            if multi_fib_levels:
                print(f"{cls.GREEN}✅ Fibonacci levels calculated successfully{cls.RESET}")
                timeframes = list(multi_fib_levels.keys())
                print(f"Available timeframes: {', '.join(timeframes)}")
            else:
                print(f"{cls.YELLOW}⚠️ No Fibonacci levels detected{cls.RESET}")
            
            # Log any detected confluence zones
            if confluence_zones:
                print(f"{cls.CYAN}🔷 Detected {len(confluence_zones)} Fibonacci confluence zones{cls.RESET}")
                for i, zone in enumerate(confluence_zones[:3], 1):  # Show top 3
                    print(f"  Zone {i}: ${zone:.2f}")
        except Exception as e:
            print(f"{cls.RED}Error calculating Fibonacci levels: {e}{cls.RESET}")
            import traceback
            traceback.print_exc()
            multi_fib_levels, confluence_zones = {}, []
        
        # Volume analysis
        try:
            # Use historical volumes if available, otherwise fallback to basic checks
            if len(historical_volumes) > 5:
                # Calculate volume metrics
                avg_volume = float(np.mean(historical_volumes))
                volume_std = float(np.std(historical_volumes)) if len(historical_volumes) > 1 else 0.0
                
                # Convert current volume to float and handle None case
                current_volume = float(volume) if volume is not None else 0.0
                
                # Calculate z-score (avoid division by zero)
                volume_z_score = ((current_volume - avg_volume) / volume_std 
                                 if volume_std > 0 else 0.0)
                
                # Consider a volume spike if z-score > 2 (95th percentile)
                volume_spike = volume_z_score > 2.0
                
                # Store volume metrics in Redis for monitoring
                cls.redis_conn.hset(
                    "latest_volume_metrics",
                    mapping={
                        "current_volume": str(current_volume),
                        "avg_volume": str(avg_volume),
                        "volume_z_score": str(volume_z_score),
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                )
                
                print(f"{cls.CYAN}📊 Volume Analysis: Current={current_volume:.2f}, Avg={avg_volume:.2f}, Z-Score={volume_z_score:.2f}{cls.RESET}")
                
            else:
                # Not enough volume data
                print(f"{cls.YELLOW}⚠️ Insufficient historical volume data{cls.RESET}")
                volume_spike = False
                if volume is not None and volume > 0 and len(historical_volumes) > 0:
                    # Basic check: is current volume more than 2x the last one?
                    volume_spike = volume > (historical_volumes[-1] * 2.0)
            
        except Exception as e:
            print(f"{cls.RED}❌ Volume analysis error: {e}{cls.RESET}")
            # Fallback to simple comparison
            volume_spike = False
            if volume is not None and len(historical_volumes) > 0:
                volume_spike = volume > (sum(historical_volumes) / len(historical_volumes) * 2)

        # Analyze price movement
        price_change = (latest_price - previous_price) / previous_price if previous_price != 0 else 0
        
        # Log the analysis components
        print(f"{cls.YELLOW}📝 Analysis Components:{cls.RESET}")
        print(f"  Price Change: {price_change:.2%}")
        print(f"  Volume Spike: {'Yes' if volume_spike else 'No'}")
        print(f"  Fibonacci Confluence: {'Yes' if confluence_zones else 'No'}")
        
        # Check for potential manipulation
        if abs(price_change) > 0.02:  # 2% price movement
            if volume_spike:
                return "TRAP: High volume spike with significant price movement"
            elif len(confluence_zones) > 0:
                return "TRAP: Price movement exactly at Fibonacci level suggests manipulation"
            elif len(multi_fib_levels) > 0:
                return "TRAP: Significant price movement at Fibonacci level"
        
        # Check for organic movement
        if 0.001 <= abs(price_change) <= 0.02 and not volume_spike:
            return "Organic: Normal market movement"
        
        return "Insufficient Data"

    @classmethod
    def detect_market_regime(cls):
        """Detect current market regime (trending vs ranging) for dynamic threshold adjustment."""
        try:
            # Get recent price history
            recent_prices = cls.redis_conn.lrange("btc_movement_history", -50, -1)
            
            if len(recent_prices) < 20:
                print("⚠️ [DEBUG] Insufficient price history for regime detection")
                return "unknown", 1.0
                
            parsed_prices = []
            for data in recent_prices:
                try:
                    if ',' in data:
                        price, _ = map(float, data.split(','))
                    else:
                        price = float(data)
                    parsed_prices.append(price)
                except (ValueError, TypeError):
                    continue
            
            if len(parsed_prices) < 20:
                print("⚠️ [DEBUG] Insufficient valid price history for regime detection")
                return "unknown", 1.0
                
            recent_prices = parsed_prices
            
            # Calculate directional movement
            price_changes = np.diff(recent_prices)
            
            # Calculate metrics for regime detection
            volatility = np.std(price_changes)
            
            # Directional strength: consistent positive or negative moves indicate trend
            pos_moves = sum(1 for change in price_changes if change > 0)
            neg_moves = sum(1 for change in price_changes if change < 0)
            directional_strength = abs((pos_moves - neg_moves) / len(price_changes))
            
            # Store directional strength in Redis
            cls.redis_conn.set("directional_strength", str(directional_strength))
            
            # Calculate average absolute move to identify if moves are significant
            avg_abs_move = np.mean(np.abs(price_changes))
            
            # Calculate regime multiplier
            # High directional_strength = trending
            # High volatility + low directional_strength = choppy/ranging
            if directional_strength > 0.6 and avg_abs_move > volatility * 0.5:
                # Strongly trending market - use higher threshold
                regime = "trending"
                regime_multiplier = 1.5
            elif directional_strength < 0.3 and volatility > avg_abs_move * 2:
                # Choppy/ranging market - use lower threshold
                regime = "volatile"
                regime_multiplier = 0.75
            else:
                # Normal market
                regime = "normal"
                regime_multiplier = 1.0
                
            print(f"🔍 Market Regime: {regime.upper()} | Directional Strength: {directional_strength:.2f} | Multiplier: {regime_multiplier}")
                
            return regime, regime_multiplier
            
        except Exception as e:
            print(f"❌ Error detecting market regime: {e}")
            traceback.print_exc()  # Print full traceback for debugging
            return "unknown", 1.0

    @classmethod
    def calculate_dynamic_threshold(cls):
        """Calculate dynamic threshold with enhanced sensitivity for MM traps."""
        try:
            # Get recent price changes for volatility calculation
            recent_changes = cls.redis_conn.lrange("abs_price_change_history", -100, -1)
            if not recent_changes:
                print(f"⚠️ [DEBUG] No price history available! Using minimum threshold: {cls.MIN_LIQUIDITY_GRAB_THRESHOLD}")
                return cls.MIN_LIQUIDITY_GRAB_THRESHOLD

            # Convert to float values
            recent_prices = [float(change) for change in recent_changes]
            
            if len(recent_prices) < 5:
                print(f"⚠️ [DEBUG] Not Enough Price Data for Volatility! Using Minimum: {cls.MIN_LIQUIDITY_GRAB_THRESHOLD}")
                return cls.MIN_LIQUIDITY_GRAB_THRESHOLD

            # Get market regime and adjustment multiplier
            market_regime, regime_multiplier = cls.detect_market_regime()

            # ✅ NEW: Check for high-frequency trap mode
            latest_price = float(cls.redis_conn.get("last_btc_price") or 0)
            hf_mode_active, hf_multiplier = check_high_frequency_mode(latest_price)
            
            # Apply regime multiplier and high-frequency multiplier to volatility calculation
            rolling_std_dev = np.std(np.diff(recent_prices))  
            adjusted_volatility_multiplier = cls.VOLATILITY_MULTIPLIER * regime_multiplier * hf_multiplier
            
            # Calculate dynamic threshold with enhanced sensitivity
            dynamic_threshold = max(rolling_std_dev * adjusted_volatility_multiplier, 
                                   cls.MIN_LIQUIDITY_GRAB_THRESHOLD * hf_multiplier)

            # Enhanced debug information
            hf_mode_status = "ACTIVE ⚠️" if hf_mode_active else "inactive"
            print(f"📡 [DEBUG] Rolling Volatility: ${rolling_std_dev:.2f} | Market Regime: {market_regime} | " 
                  f"HF Mode: {hf_mode_status} ({hf_multiplier:.2f}x) | "
                  f"Adjusted Threshold: ${dynamic_threshold:.2f}")

            # ✅ Store for Grafana Monitoring
            cls.redis_conn.rpush("rolling_std_dev_history", rolling_std_dev)
            cls.redis_conn.set("current_market_regime", market_regime)
            cls.redis_conn.set("regime_multiplier", regime_multiplier)
            cls.redis_conn.set("hf_trap_multiplier", hf_multiplier)
            cls.redis_conn.set("current_dynamic_threshold", dynamic_threshold)
            cls.redis_conn.ltrim("rolling_std_dev_history", -100, -1)

            return dynamic_threshold

        except Exception as e:
            print(f"❌ [DEBUG] Error calculating dynamic threshold: {e}")
            return cls.MIN_LIQUIDITY_GRAB_THRESHOLD  # ✅ Fail-safe to minimum threshold

    @classmethod
    def get_multi_timeframe_fibonacci(cls, price: float) -> tuple[Dict[str, float], List[float]]:
        """Calculate Fibonacci levels across multiple timeframes."""
        try:
            # Get price history for different timeframes
            timeframes = {
                "1h": cls.redis_conn.lrange("btc_movement_history", -60, -1),
                "4h": cls.redis_conn.lrange("btc_movement_history", -240, -1),
                "1d": cls.redis_conn.lrange("btc_movement_history", -1440, -1)
            }
            
            fib_levels = {}
            confluence_zones = []
            
            for timeframe, prices in timeframes.items():
                try:
                    # Convert prices to floats
                    price_list = [float(p.split(',')[0]) for p in prices if ',' in p]
                    if not price_list:
                        continue
                    
                    high = max(price_list)
                    low = min(price_list)
                    
                    # Calculate Fibonacci levels
                    diff = high - low
                    levels = {
                        "0.0": low,
                        "0.236": low + diff * 0.236,
                        "0.382": low + diff * 0.382,
                        "0.5": low + diff * 0.5,
                        "0.618": low + diff * 0.618,
                        "0.786": low + diff * 0.786,
                        "1.0": high
                    }
                    
                    fib_levels[timeframe] = levels
                    
                    # Check for confluence zones
                    for level, value in levels.items():
                        if abs(price - value) < diff * 0.01:  # 1% tolerance
                            confluence_zones.append(value)
                    
                except Exception as e:
                    print(f"Error calculating Fibonacci levels for {timeframe}: {e}")
                    continue
            
            return fib_levels, confluence_zones
            
        except Exception as e:
            print(f"Error in get_multi_timeframe_fibonacci: {e}")
            return {}, []

    @classmethod
    def detect_fibonacci_confluence(cls, multi_fib_levels, latest_price, tolerance=50):
        """Identify price zones where multiple Fibonacci levels converge with enhanced strength scoring."""
        all_levels = []
        
        # Timeframe importance weights
        timeframe_weights = {
            "realtime": 2.5,  # 🔥 NEW: Highest weight for real-time calculations
            "short": 1.0,     # 15 minutes (lowest weight)
            "medium": 1.5,    # 1 hour (medium weight)
            "long": 2.0       # 4 hours (highest weight)
        }
        
        # Collect all Fibonacci levels across timeframes
        for timeframe, levels in multi_fib_levels.items():
            weight = timeframe_weights.get(timeframe, 1.0)
            for ratio, price in levels.items():
                all_levels.append((timeframe, ratio, price, weight))
        
        # Find clusters of Fibonacci levels
        confluence_zones = []
        processed_indices = set()
        
        for i, (tf1, ratio1, price1, weight1) in enumerate(all_levels):
            if i in processed_indices:
                continue
                
            nearby_levels = [(tf1, ratio1, price1, weight1)]
            processed_indices.add(i)
            
            # Find all other levels within tolerance
            for j, (tf2, ratio2, price2, weight2) in enumerate(all_levels):
                if i != j and j not in processed_indices and abs(price1 - price2) < tolerance:
                    nearby_levels.append((tf2, ratio2, price2, weight2))
                    processed_indices.add(j)
            
            # If we found multiple levels in proximity
            if len(nearby_levels) >= 2:
                # Calculate center as weighted average
                total_weight = sum(level[3] for level in nearby_levels)
                center = sum(level[2] * level[3] for level in nearby_levels) / total_weight
                
                # Calculate strength based on number of levels and their weights
                base_strength = len(nearby_levels)
                weighted_strength = sum(level[3] for level in nearby_levels)
                
                # Calculate diversity score (bonus for having levels from different timeframes)
                timeframes_present = set(level[0] for level in nearby_levels)
                timeframe_diversity = len(timeframes_present) / 3.0  # Normalize by max number of timeframes
                
                # Final strength score combines quantity, weights and timeframe diversity
                strength_score = base_strength * (1 + 0.5 * timeframe_diversity)
                
                # Calculate proximity score (how close price is to this zone)
                proximity = 1.0 / (1.0 + abs(latest_price - center) / 100)
                
                confluence_zones.append({
                    "center": center,
                    "levels": nearby_levels,
                    "strength": strength_score,
                    "timeframe_diversity": timeframe_diversity,
                    "proximity_score": proximity,
                    "weighted_strength": weighted_strength
                })
        
        # Sort by weighted strength (more important than just number of levels)
        return sorted(confluence_zones, key=lambda x: x["weighted_strength"], reverse=True)

    @classmethod
    def analyze_multi_timeframe_trends(cls, price=None):
        """Analyze price trends across multiple Fibonacci-based timeframes up to 24h."""
        # Fibonacci-inspired timeframes (in minutes)
        fibonacci_timeframes = {
            "1min": 1,
            "3min": 3, 
            "5min": 5,
            "8min": 8,
            "13min": 13,
            "21min": 21,
            "34min": 34,
            "55min": 55,
            "89min": 89,
            "144min": 144,    # ~2.4 hours
            "233min": 233,    # ~3.9 hours
            "377min": 377,    # ~6.3 hours
            "610min": 610,    # ~10.2 hours
            "987min": 987,    # ~16.5 hours
            "1440min": 1440,  # 24 hours
        }
        
        # Get current price if not provided
        if not price:
            current_price = cls.redis_conn.get("last_btc_price")
            if current_price:
                price = float(current_price)
            else:
                return {}  # No price data available
        
        # Store results for each timeframe
        trend_analysis = {}
        trend_summary = {
            "bullish": 0,
            "bearish": 0,
            "sideways": 0,
            "timeframes_analyzed": 0
        }
        
        print(f"\n{cls.CYAN}{'═' * 20} FIBONACCI MULTI-TIMEFRAME ANALYSIS {'═' * 20}{cls.RESET}")
        
        # Analyze each timeframe
        for name, minutes in fibonacci_timeframes.items():
            try:
                movements = fetch_recent_movements(minutes)
                
                # Debug output
                print(f"\nAnalyzing {name} timeframe:")
                print(f"Retrieved {len(movements)} movements")
                
                if len(movements) < 2:
                    print(f"Insufficient data for {name}")
                    trend_analysis[name] = {
                        "trend": "Insufficient data",
                        "change": 0.0,
                        "earliest_price": 0.0,
                        "latest_price": 0.0,
                        "valid": False
                    }
                    continue
                    
                # Get first and last price points
                earliest_price = float(movements[-1][1])  # btc_price
                latest_price = float(movements[0][1])     # btc_price
                
                print(f"Earliest price: {earliest_price}")
                print(f"Latest price: {latest_price}")
                
                price_change = latest_price - earliest_price
                percentage_change = (price_change / earliest_price) * 100
                
                # Determine trend strength based on percentage change
                if percentage_change > 1.0:
                    trend = "Strongly Bullish"
                    trend_summary["bullish"] += 2
                elif 0.3 < percentage_change <= 1.0:
                    trend = "Moderately Bullish"
                    trend_summary["bullish"] += 1
                elif -0.3 <= percentage_change <= 0.3:
                    trend = "Sideways"
                    trend_summary["sideways"] += 1
                elif -1.0 <= percentage_change < -0.3:
                    trend = "Moderately Bearish"
                    trend_summary["bearish"] += 1
                else:
                    trend = "Strongly Bearish"
                    trend_summary["bearish"] += 2
                
                # Determine color for output
                if "Bullish" in trend:
                    color = cls.GREEN if "Strongly" in trend else cls.BLUE
                elif "Bearish" in trend:
                    color = cls.RED if "Strongly" in trend else cls.YELLOW
                else:
                    color = cls.CYAN
                    
                # Calculate volatility for this timeframe
                if len(movements) > 2:
                    prices = [float(m[1]) for m in movements]
                    volatility = np.std(prices) / np.mean(prices) * 100  # as percentage
                else:
                    volatility = 0
                    
                # Store analysis
                trend_analysis[name] = {
                    "trend": trend,
                    "change": percentage_change,
                    "earliest_price": earliest_price,
                    "latest_price": latest_price,
                    "volatility": volatility,
                    "valid": True
                }
                
                # Update counter for valid timeframes
                trend_summary["timeframes_analyzed"] += 1
                
                # Print nicely formatted output
                direction = "↑" if percentage_change > 0 else "↓" if percentage_change < 0 else "→"
                print(f"{cls.WHITE}{name}: {color}{trend} {direction} ({percentage_change:.2f}%) Vol: {volatility:.2f}%{cls.RESET}")
                
                # Store in Redis for other components to use
                cls.redis_conn.hset(
                    f"trend_analysis:{name}",
                    mapping={
                        "trend": trend,
                        "percentage_change": str(percentage_change),
                        "volatility": str(volatility),
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                )
                
            except Exception as e:
                print(f"{cls.RED}Error analyzing {name} trend: {str(e)}\nTraceback: {traceback.format_exc()}{cls.RESET}")
                trend_analysis[name] = {
                    "trend": "Analysis error",
                    "change": 0.0,
                    "valid": False
                }
        
        # Calculate overall market bias from all timeframes
        if trend_summary["timeframes_analyzed"] > 0:
            bullish_score = trend_summary["bullish"]
            bearish_score = trend_summary["bearish"]
            
            # Compute market bias
            if bullish_score > bearish_score * 2:
                market_bias = "Strongly Bullish"
                bias_color = cls.GREEN
            elif bullish_score > bearish_score:
                market_bias = "Moderately Bullish"
                bias_color = cls.BLUE
            elif bearish_score > bullish_score * 2:
                market_bias = "Strongly Bearish"
                bias_color = cls.RED
            elif bearish_score > bullish_score:
                market_bias = "Moderately Bearish"
                bias_color = cls.YELLOW
            else:
                market_bias = "Neutral/Sideways"
                bias_color = cls.CYAN
                
            # Store overall bias in Redis
            cls.redis_conn.hset(
                "market_bias", 
                mapping={
                    "bias": market_bias,
                    "bullish_score": str(bullish_score),
                    "bearish_score": str(bearish_score),
                    "sideways_count": str(trend_summary["sideways"]),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            )
            
            # Print summary
            print(f"\n{cls.WHITE}Overall Market Bias: {bias_color}{market_bias}{cls.RESET}")
            print(f"{cls.WHITE}Bullish Signals: {cls.GREEN}{trend_summary['bullish']}{cls.RESET} | " + 
                  f"Bearish Signals: {cls.RED}{trend_summary['bearish']}{cls.RESET} | " +
                  f"Sideways: {cls.CYAN}{trend_summary['sideways']}{cls.RESET}")
            
            # Find longest continuous trend direction
            valid_timeframes = [(name, data) for name, data in trend_analysis.items() if data["valid"]]
            valid_timeframes.sort(key=lambda x: int(''.join(filter(str.isdigit, x[0]))))  # Sort by timeframe duration
            
            continuous_bull = 0
            continuous_bear = 0
            max_bull_run = 0
            max_bear_run = 0
            
            for _, data in valid_timeframes:
                if "Bullish" in data["trend"]:
                    continuous_bull += 1
                    continuous_bear = 0
                    max_bull_run = max(max_bull_run, continuous_bull)
                elif "Bearish" in data["trend"]:
                    continuous_bear += 1
                    continuous_bull = 0
                    max_bear_run = max(max_bear_run, continuous_bear)
                else:
                    continuous_bull = 0
                    continuous_bear = 0
            
            if max_bull_run >= 3:
                print(f"{cls.GREEN}⚠️ Strong bullish alignment across {max_bull_run} consecutive timeframes!{cls.RESET}")
            if max_bear_run >= 3:
                print(f"{cls.RED}⚠️ Strong bearish alignment across {max_bear_run} consecutive timeframes!{cls.RESET}")
        
        return trend_analysis
