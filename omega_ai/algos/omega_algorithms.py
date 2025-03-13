import datetime
import numpy as np
import redis
from omega_ai.db_manager.database import fetch_recent_movements
from omega_ai.mm_trap_detector.high_frequency_detector import check_high_frequency_mode, register_trap_detection

class OmegaAlgo:
    """🔥 OMEGA BTC AI - Market Maker Trap Detection & Fibonacci Validation 🔱"""

    # ✅ Dynamic MM Detection Constants
    SCHUMANN_THRESHOLD = 10.0
    VOLATILITY_MULTIPLIER = 2.5  # ✅ Adjusts dynamically with BTC market conditions
    MIN_LIQUIDITY_GRAB_THRESHOLD = 250  # ✅ Minimum absolute price move to trigger detection
    PRICE_DROP_THRESHOLD = -0.02  # ✅ 2% BTC price drop
    PRICE_PUMP_THRESHOLD = 0.02  # ✅ 2% BTC price pump
    CHECK_INTERVAL = 30  # ✅ Frequency of checks (in seconds)
    ROLLING_WINDOW = 30  # ✅ Number of price points for volatility calculations
    CYAN = "\033[96m"
    RESET = "\033[0m"
    WHITE = "\033[97m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"


    # ✅ Initialize Redis Connection
    redis_conn = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

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
    def is_fibo_organic(cls, latest_price, previous_price, volume):
        """Enhanced multi-layer Fibonacci analysis for advanced trap detection."""
        
        # Get existing historical data
        historical_prices = cls.redis_conn.lrange("btc_movement_history", -100, -1)
        if len(historical_prices) < 10:
            return "Insufficient Data"
        
        historical_prices = [float(price) for price in historical_prices]

        # Multi-timeframe Fibonacci analysis (using both retracements and extensions)
        try:
            multi_fib_levels, confluence_zones = cls.get_multi_timeframe_fibonacci(latest_price)
        except Exception as e:
            print(f"{cls.RED}Error calculating Fibonacci levels: {e}{cls.RESET}")
            multi_fib_levels, confluence_zones = {}, []
        
        # Get recent movements for volume analysis
        recent_movements = fetch_recent_movements(minutes=15)
        if not recent_movements or len(recent_movements) < 5:
            return "Insufficient Data"
        
        # Store multi-fib analysis results in Redis for Grafana monitoring
        if confluence_zones:
            cls.redis_conn.hset(
                "latest_fibonacci_confluence",
                mapping={
                    "center": str(confluence_zones[0]["center"]),
                    "strength": str(confluence_zones[0]["strength"]),
                    "weighted_strength": str(confluence_zones[0].get("weighted_strength", 0)),
                    "timeframe_diversity": str(confluence_zones[0].get("timeframe_diversity", 0)),
                    "proximity": str(confluence_zones[0].get("proximity_score", 0)),
                    "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
                }
            )
        
        # Enhanced volume analysis with anomaly detection - FIX: Convert Decimal to float
        try:
            # Fix: Use correct index (5) for volume and convert to float
            volumes = [float(row[5]) for row in recent_movements]  # Index 5 is volume
            
            # Convert values to float to avoid type mismatches
            volume = float(volume)
            avg_volume = float(np.mean(volumes))
            volume_std = float(np.std(volumes))
            
            # Now all values are floats
            volume_z_score = (volume - avg_volume) / volume_std if volume_std > 0 else 0
            
            # Store volume metrics in Redis for monitoring
            cls.redis_conn.hset(
                "latest_volume_metrics",
                mapping={
                    "current_volume": str(volume),
                    "avg_volume": str(avg_volume),
                    "volume_z_score": str(volume_z_score),
                    "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
                }
            )
            
            # Consider a volume spike if z-score > 2 (95th percentile)
            volume_spike = volume_z_score > 2
        except (IndexError, ZeroDivisionError, TypeError) as e:
            print(f"❌ Volume analysis error: {e}. Falling back to simple comparison.")
            # Fallback if volume data is incomplete or type error occurs
            avg_volume = float(sum(float(row[5]) for row in recent_movements) / len(recent_movements)) if recent_movements else 0
            volume_spike = float(volume) > avg_volume * 2
        
        # Original functionality continues from here unchanged
        # Enhanced decision logic with advanced scoring system
        organic_score = 0
        detailed_analysis = {}
        
        if confluence_zones:
            strongest_zone = confluence_zones[0]
            
            # Check if price is near the strongest confluence zone
            proximity_threshold = 100
            is_near_confluence = abs(latest_price - strongest_zone["center"]) < proximity_threshold
            proximity_factor = 1.0 - min(abs(latest_price - strongest_zone["center"]) / proximity_threshold, 1.0)
            
            # Calculate score based on multiple factors with more nuance
            organic_score += 2 * proximity_factor  # Up to 2 points based on proximity
            organic_score += 2 if not volume_spike else -1.5  # Volume assessment
            
            # Add timeframe diversity bonus
            timeframe_diversity = strongest_zone.get("timeframe_diversity", 0)
            organic_score += timeframe_diversity * 1.5  # Up to 1.5 bonus points for timeframe diversity
            
            # Add weighted strength (confluence strength weighted by timeframe importance)
            weighted_strength = strongest_zone.get("weighted_strength", strongest_zone["strength"])
            organic_score += (weighted_strength / 5.0)  # Normalize to ~1-3 points
            
            # Store detailed analysis for debugging and monitoring
            detailed_analysis = {
                "proximity_score": proximity_factor * 2,
                "volume_score": 2 if not volume_spike else -1.5,
                "diversity_score": timeframe_diversity * 1.5,
                "strength_score": weighted_strength / 5.0,
                "final_score": organic_score
            }
            
            # Store analysis in Redis for monitoring
            cls.redis_conn.hset(
                "latest_organic_analysis", 
                mapping={k: str(v) for k, v in detailed_analysis.items()}
            )
            
            print(f"📡 [DEBUG] Multi-Fibonacci Analysis: Organic Score = {organic_score:.2f}")
            print(f"📡 [DEBUG] Strongest confluence at ${strongest_zone['center']:.2f} with strength {weighted_strength:.2f}")
            print(f"📡 [DEBUG] Analysis Details: {detailed_analysis}")
            
            # Enhanced classification with more granular outcomes
            if organic_score >= 4:
                return "High-Confidence Organic Movement"
            elif organic_score >= 3:
                return "Multi-Fibonacci Organic"
            elif organic_score >= 1.5:
                return "Likely Organic"
            else:
                return "Complex MM Trap Pattern"
        else:
            # Fall back to single-timeframe analysis if no confluence zones found
            prices = [float(row[1]) for row in recent_movements]  # Convert to float
            high, low = max(prices), min(prices)
            fib_levels = cls.calculate_fibonacci_levels(high, low)
            
            # Check for both retracement and extension levels
            extended_fib_levels = cls.calculate_extended_fibonacci_levels(high, low)
            all_levels = {}
            all_levels.update(fib_levels)
            
            # Check if the price is near any Fibonacci level
            fib_matches = [(level_name, abs(latest_price - level_value)) 
                          for level_name, level_value in all_levels.items() 
                          if abs(latest_price - level_value) < 50]
            
            if fib_matches:
                closest_level, distance = min(fib_matches, key=lambda x: x[1])
                proximity_factor = 1.0 - min(distance / 50.0, 1.0)
                
                basic_score = 1.5 * proximity_factor
                basic_score += 1 if not volume_spike else -1
                
                print(f"📡 [DEBUG] Basic Fibonacci Analysis: Level={closest_level}, Distance=${distance:.2f}, Score={basic_score:.2f}")
                
                if basic_score >= 1.5:
                    return "Fibonacci Organic"
                else:
                    return "Potential MM Trap"
            else:
                return "MM Manipulation"

    @classmethod
    def detect_market_regime(cls):
        """Detect current market regime (trending vs ranging) for dynamic threshold adjustment."""
        try:
            # Get recent price history
            recent_prices = cls.redis_conn.lrange("btc_movement_history", -50, -1)
            
            if len(recent_prices) < 20:
                print("⚠️ [DEBUG] Insufficient price history for regime detection")
                return "unknown", 1.0
                
            recent_prices = [float(p) for p in recent_prices]
            
            # Calculate directional movement
            price_changes = np.diff(recent_prices)
            
            # Calculate metrics for regime detection
            volatility = np.std(price_changes)
            
            # Directional strength: consistent positive or negative moves indicate trend
            pos_moves = sum(1 for change in price_changes if change > 0)
            neg_moves = sum(1 for change in price_changes if change < 0)
            directional_strength = abs((pos_moves - neg_moves) / len(price_changes))
            
            # Calculate average absolute move to identify if moves are significant
            avg_abs_move = np.mean(np.abs(price_changes))
            
            # Calculate regime multiplier
            # High directional_strength = trending
            # High volatility + low directional_strength = choppy/ranging
            if directional_strength > 0.6 and avg_abs_move > volatility * 0.5:
                print(f"📡 [DEBUG] TRENDING Market Detected (Directional Strength: {directional_strength:.2f})")
                return "trending", 1.5  # Higher threshold for trending market
            elif volatility > 0 and directional_strength < 0.3:
                print(f"📡 [DEBUG] RANGING Market Detected (Directional Strength: {directional_strength:.2f})")
                return "ranging", 0.8  # Lower threshold for ranging market
            else:
                print(f"📡 [DEBUG] MIXED Market Detected (Directional Strength: {directional_strength:.2f})")
                return "mixed", 1.0  # Default multiplier
                
        except Exception as e:
            print(f"❌ [DEBUG] Error detecting market regime: {e}")
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
    def get_multi_timeframe_fibonacci(cls, latest_price):
        """Calculate Fibonacci levels across multiple timeframes for confluence detection."""
        timeframes = {
            "short": 15,     # 15 minutes
            "medium": 60,    # 1 hour
            "long": 240      # 4 hours
        }
        
        # 🔥 NEW: Always recalculate using real-time Redis data first
        latest_prices = cls.redis_conn.lrange("btc_movement_history", -100, -1)
        realtime_fib_levels = {}
        
        if (latest_prices and len(latest_prices) >= 10):
            # Convert string prices to float
            latest_prices = [float(price) for price in latest_prices]
            high, low = max(latest_prices), min(latest_prices)
            
            # Calculate real-time Fibonacci levels
            realtime_fib_levels = cls.calculate_fibonacci_levels(high, low)
            
            # Add real-time levels as a special timeframe
            print(f"📡 [DEBUG] Adjusted Fibonacci Levels | High: {high}, Low: {low}")
            
            # Store real-time Fibonacci levels in Redis for other components
            for level, price in realtime_fib_levels.items():
                cls.redis_conn.hset("realtime_fibonacci_levels", str(level), str(price))
                
            # Add timestamp for monitoring
            cls.redis_conn.hset("realtime_fibonacci_levels", "timestamp", 
                               datetime.datetime.now(datetime.UTC).isoformat())
        
        # Continue with standard multi-timeframe calculations
        multi_fib_levels = {}
        if realtime_fib_levels:
            # Add real-time levels as highest priority timeframe
            multi_fib_levels["realtime"] = realtime_fib_levels
        
        for timeframe_name, minutes in timeframes.items():
            movements = fetch_recent_movements(minutes=minutes)
            if movements and len(movements) >= 5:
                prices = [float(row[1]) for row in movements]
                high, low = max(prices), min(prices)
                multi_fib_levels[timeframe_name] = cls.calculate_fibonacci_levels(high, low)
        
        # Find confluence zones where Fibonacci levels from multiple timeframes align
        confluence_zones = cls.detect_fibonacci_confluence(multi_fib_levels, latest_price)

        # Enhanced logging for all timeframes
        for tf, levels in multi_fib_levels.items():
            print(f"📡 [DEBUG] {tf.upper()} Fibonacci | Levels: {len(levels)}")
        
        print(f"📡 [DEBUG] Multi-Timeframe Fibonacci Levels: {multi_fib_levels}")
        print(f"📡 [DEBUG] Confluence Zones: {confluence_zones}")
        
        # 🔥 NEW: Add real-time Fibonacci status check
        if realtime_fib_levels:
            # Find closest Fibonacci level to current price
            closest_level = min(realtime_fib_levels.items(), 
                               key=lambda x: abs(latest_price - x[1]))
            distance = abs(latest_price - closest_level[1])
            
            print(f"📡 [DEBUG] Current Price ${latest_price} is ${distance:.2f} away from {closest_level[0]} level")
            print(f"📡 [DEBUG] {tf.upper()} Fibonacci | Levels: {len(levels)}")
            
            # Store distance to closest Fib level for monitoring
            cls.redis_conn.set("distance_to_nearest_fib", distance)
            cls.redis_conn.set("nearest_fib_level", closest_level[0])
        
        return multi_fib_levels, confluence_zones

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
                        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
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
                    "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
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
