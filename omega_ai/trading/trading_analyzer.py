#!/usr/bin/env python3

"""
Trading Analysis Module for OmegaBTC AI

This module handles the decision-making process and analysis for trading operations,
providing detailed debugging information about potential trades before execution.
"""

import json
import time
import datetime
import redis
import numpy as np
from typing import Tuple, Dict, List, Optional, Any

from omega_ai.algos.omega_algorithms import OmegaAlgo

# Terminal colors for visual output
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
BLUE = "\033[94m"
WHITE = "\033[97m"
BOLD = "\033[1m"
LIGHT_BLUE = "\033[94m"
PURPLE = "\033[95m"

class TradingAnalyzer:
    """Analyzes market conditions and provides trading signals with detailed reasoning."""
    
    def __init__(self, debug_mode: bool = True):
        """Initialize the trading analyzer."""
        self.redis_conn = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
        self.debug_mode = debug_mode
        self.last_analysis_time = datetime.datetime.min
        self.analysis_cooldown = 15  # seconds between analyses
        
        # Analysis score thresholds
        self.entry_threshold = 50  # Changed from 70
        
    def log_debug(self, message: str, category: str = "INFO") -> None:
        """Log a debug message if debug mode is enabled."""
        if not self.debug_mode:
            return
            
        category_colors = {
            "INFO": BLUE,
            "SIGNAL": GREEN,
            "WARNING": YELLOW,
            "ANALYSIS": CYAN,
            "PRICE": PURPLE,
            "FIBONACCI": MAGENTA
        }
        
        color = category_colors.get(category, WHITE)
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        print(f"{color}[{timestamp}] [{category}] {message}{RESET}")
    
    def get_current_price(self) -> float:
        """Get the current BTC price from Redis."""
        try:
            price_str = self.redis_conn.get("last_btc_price")
            if price_str:
                return float(price_str)
            return 0.0
        except Exception as e:
            self.log_debug(f"Error getting price: {e}", "WARNING")
            return 0.0
    
    def get_market_context(self) -> Dict[str, Any]:
        """Get comprehensive market context data from various sources."""
        context = {
            "price": self.get_current_price(),
            "timestamp": datetime.datetime.now(datetime.UTC),
            "market_bias": None,
            "fib_levels": {},
            "recent_volatility": 0.0,
            "recent_trap": None,
            "schumann_resonance": None,
            "regime": "unknown"
        }
        
        self.log_debug(f"Current BTC price: ${context['price']:.2f}", "PRICE")
        
        # Get market bias
        try:
            bias_data = self.redis_conn.hgetall("market_bias")
            if bias_data:
                context["market_bias"] = bias_data.get("bias", "Neutral/Sideways")
                context["bullish_score"] = float(bias_data.get("bullish_score", 0))
                context["bearish_score"] = float(bias_data.get("bearish_score", 0))
                
                self.log_debug(f"Market bias: {context['market_bias']} (Bull:{context['bullish_score']:.1f}/Bear:{context['bearish_score']:.1f})", "ANALYSIS")
        except Exception as e:
            self.log_debug(f"Error getting market bias: {e}", "WARNING")
        
        # Get Fibonacci levels
        try:
            fib_data = self.redis_conn.hgetall("realtime_fibonacci_levels")
            if fib_data:
                for level_name, price_str in fib_data.items():
                    if level_name != "timestamp":
                        try:
                            context["fib_levels"][level_name] = float(price_str)
                        except ValueError:
                            continue
                
                level_count = len(context["fib_levels"])
                if level_count > 0:
                    self.log_debug(f"Found {level_count} Fibonacci levels", "FIBONACCI")
                    
                    # Calculate nearest Fibonacci level
                    nearest_level = None
                    nearest_distance = float('inf')
                    
                    for level, price in context["fib_levels"].items():
                        distance = abs(context["price"] - price)
                        if distance < nearest_distance:
                            nearest_distance = distance
                            nearest_level = (level, price)
                    
                    if nearest_level:
                        level_name, level_price = nearest_level
                        distance_pct = (nearest_distance / context["price"]) * 100
                        context["nearest_fib"] = {
                            "level": level_name,
                            "price": level_price,
                            "distance": nearest_distance,
                            "distance_pct": distance_pct
                        }
                        
                        self.log_debug(
                            f"Nearest Fibonacci level: {level_name} at ${level_price:.2f} " +
                            f"(${nearest_distance:.2f}, {distance_pct:.2f}% away)", 
                            "FIBONACCI"
                        )
        except Exception as e:
            self.log_debug(f"Error getting Fibonacci levels: {e}", "WARNING")
        
        # Get MM traps
        try:
            trap_data = self.redis_conn.get("latest_mm_trap")
            if trap_data:
                context["recent_trap"] = json.loads(trap_data)
                trap_time = context["recent_trap"].get("timestamp", 0)
                trap_age = time.time() - trap_time
                
                if trap_age < 900:  # 15 minutes
                    self.log_debug(
                        f"Recent MM trap detected {trap_age:.0f}s ago: " +
                        f"{context['recent_trap'].get('type')} " +
                        f"(Confidence: {context['recent_trap'].get('confidence', 0):.2f})",
                        "WARNING"
                    )
        except Exception as e:
            self.log_debug(f"Error checking MM traps: {e}", "WARNING")
        
        # Get volatility info
        try:
            volatility = self.redis_conn.get("current_dynamic_threshold")
            regime = self.redis_conn.get("current_market_regime")
            
            if volatility:
                context["recent_volatility"] = float(volatility)
                self.log_debug(f"Current volatility threshold: ${context["recent_volatility"]:.2f}", "ANALYSIS")
                
            if regime:
                context["regime"] = regime
                self.log_debug(f"Current market regime: {context["regime"]}", "ANALYSIS")
        except Exception as e:
            self.log_debug(f"Error getting volatility data: {e}", "WARNING")
            
        return context
    
    def analyze_timeframes(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze multiple timeframes and add results to context."""
        try:
            # Get multi-timeframe trend analysis from OmegaAlgo
            trend_data = OmegaAlgo.analyze_multi_timeframe_trends(context["price"])
            
            if not trend_data:
                self.log_debug("No multi-timeframe trend data available", "WARNING")
                return context
                
            context["timeframes"] = trend_data
            
            # Count bullish/bearish timeframes
            bullish_count = 0
            bearish_count = 0
            sideways_count = 0
            valid_timeframes = 0
            
            for timeframe, data in trend_data.items():
                if data.get("valid", False):
                    valid_timeframes += 1
                    trend = data.get("trend", "")
                    
                    if "Bullish" in trend:
                        bullish_count += 1
                    elif "Bearish" in trend:
                        bearish_count += 1
                    else:
                        sideways_count += 1
            
            context["valid_timeframes"] = valid_timeframes
            context["bullish_timeframes"] = bullish_count
            context["bearish_timeframes"] = bearish_count
            context["sideways_timeframes"] = sideways_count
            
            # Calculate trend alignment strength
            if valid_timeframes > 0:
                context["trend_alignment"] = max(
                    bullish_count / valid_timeframes,
                    bearish_count / valid_timeframes
                ) if valid_timeframes > 0 else 0
                
                self.log_debug(
                    f"Timeframe analysis: {valid_timeframes} valid, " +
                    f"{bullish_count} bullish, {bearish_count} bearish, {sideways_count} sideways",
                    "ANALYSIS"
                )
                
                alignment_pct = context["trend_alignment"] * 100
                if alignment_pct > 60:
                    direction = "BULLISH" if bullish_count > bearish_count else "BEARISH"
                    self.log_debug(
                        f"Strong {direction} alignment: {alignment_pct:.1f}% of timeframes", 
                        "SIGNAL"
                    )
        
        except Exception as e:
            self.log_debug(f"Error in timeframe analysis: {e}", "WARNING")
            
        return context
    
    def analyze_short_timeframes(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze shorter timeframes (1m, 3m, 5m) for quick entries."""
        if "timeframes" not in context or "score_components" not in context:
            return context
            
        # Define short timeframes to check
        short_timeframes = ["1m", "3m", "5m"]
        
        # Track alignment
        short_bullish = 0
        short_bearish = 0
        short_sideways = 0
        valid_short_frames = 0
        
        # Check each short timeframe
        for tf in short_timeframes:
            if tf in context["timeframes"] and context["timeframes"][tf].get("valid", False):
                valid_short_frames += 1
                trend = context["timeframes"][tf].get("trend", "")
                
                if "Bullish" in trend:
                    short_bullish += 1
                elif "Bearish" in trend:
                    short_bearish += 1
                else:
                    short_sideways += 1
        
        # Store results in context
        context["short_timeframes_total"] = valid_short_frames
        context["short_timeframes_bullish"] = short_bullish
        context["short_timeframes_bearish"] = short_bearish
        
        # Calculate short-term alignment score
        if valid_short_frames >= 2:  # At least 2 valid short timeframes needed
            if short_bullish == valid_short_frames:
                # All short timeframes are bullish
                context["score_components"]["short_timeframe_bull"] = 15
                self.log_debug(f"All {valid_short_frames} short timeframes bullish: +15 points", "SIGNAL")
            elif short_bearish == valid_short_frames:
                # All short timeframes are bearish
                context["score_components"]["short_timeframe_bear"] = 15
                self.log_debug(f"All {valid_short_frames} short timeframes bearish: +15 points", "SIGNAL")
            elif short_bullish >= 2 and short_bullish > short_bearish:
                # Majority of short timeframes are bullish
                context["score_components"]["short_timeframe_bull"] = 10
                self.log_debug(f"Majority of short timeframes bullish ({short_bullish}/{valid_short_frames}): +10 points", "SIGNAL")
            elif short_bearish >= 2 and short_bearish > short_bullish:
                # Majority of short timeframes are bearish
                context["score_components"]["short_timeframe_bear"] = 10
                self.log_debug(f"Majority of short timeframes bearish ({short_bearish}/{valid_short_frames}): +10 points", "SIGNAL")
        
        return context

    def analyze_volume_acceleration(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Detect volume acceleration that may precede breakouts."""
        if "score_components" not in context:
            context["score_components"] = {}
            
        try:
            # Get recent volumes from Redis
            current_vol_key = "volume_1m:current"
            prev_vol_key = "volume_1m:previous"
            
            current_vol = self.redis_conn.get(current_vol_key)
            prev_vol = self.redis_conn.get(prev_vol_key)
            
            if not current_vol or not prev_vol:
                # Try to get from another source or calculate from tick data
                vol_data = self.redis_conn.lrange("recent_volume_data", -2, -1)
                if len(vol_data) >= 2:
                    try:
                        prev_vol = float(vol_data[0])
                        current_vol = float(vol_data[1])
                    except (ValueError, TypeError):
                        return context
                else:
                    return context
            else:
                current_vol = float(current_vol)
                prev_vol = float(prev_vol)
            
            # Calculate volume delta as percentage change
            if prev_vol > 0:
                vol_delta = (current_vol - prev_vol) / prev_vol
                vol_delta_pct = vol_delta * 100
                
                context["volume_delta"] = vol_delta
                context["volume_delta_pct"] = vol_delta_pct
                
                # Log volume information
                self.log_debug(f"Volume delta: {vol_delta_pct:+.1f}% (Current: {current_vol:.1f}, Previous: {prev_vol:.1f})", "ANALYSIS")
                
                # Score based on volume acceleration
                if vol_delta > 1.0:  # 100%+ increase in volume
                    context["score_components"]["volume_surge"] = 20
                    self.log_debug(f"Major volume surge (+{vol_delta_pct:.1f}%): +20 points", "SIGNAL")
                elif vol_delta > 0.5:  # 50%+ increase
                    context["score_components"]["volume_surge"] = 15
                    self.log_debug(f"Strong volume increase (+{vol_delta_pct:.1f}%): +15 points", "SIGNAL")
                elif vol_delta > 0.2:  # 20%+ increase
                    context["score_components"]["volume_surge"] = 10
                    self.log_debug(f"Volume increasing (+{vol_delta_pct:.1f}%): +10 points", "SIGNAL")
                
                # Check if volume is increasing while price is relatively stable
                # This can indicate accumulation/distribution
                if abs(context.get("price_delta_pct", 0)) < 0.1 and vol_delta > 0.3:
                    context["score_components"]["accumulation_signal"] = 15
                    direction = "bullish" if context.get("market_bias", "").lower() != "bearish" else "bearish"
                    self.log_debug(f"Potential {direction} accumulation on rising volume: +15 points", "SIGNAL")
        
        except Exception as e:
            self.log_debug(f"Error analyzing volume acceleration: {e}", "WARNING")
        
        return context

    def evaluate_fibonacci_entry(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate potential Fibonacci-based entries."""
        if "nearest_fib" not in context:
            return context
            
        nearest_fib = context["nearest_fib"]
        fib_level = float(nearest_fib["level"])
        fib_distance_pct = nearest_fib["distance_pct"]
        
        # Initialize score components dict if not present
        if "score_components" not in context:
            context["score_components"] = {}
            
        # Base score for Fibonacci proximity
        if fib_distance_pct < 0.2:  # Very close (0.2% away)
            fib_score = 35
            self.log_debug(f"Very close to Fibonacci {fib_level} level: +35 points", "FIBONACCI")
        elif fib_distance_pct < 0.5:  # Close (0.5% away)
            fib_score = 25
            self.log_debug(f"Close to Fibonacci {fib_level} level: +25 points", "FIBONACCI")
        elif fib_distance_pct < 1.0:  # Nearby (1% away)
            fib_score = 15
            self.log_debug(f"Near Fibonacci {fib_level} level: +15 points", "FIBONACCI")
        else:
            fib_score = max(0, 10 - int(fib_distance_pct))  # Diminishing points as distance increases
            if fib_score > 0:
                self.log_debug(f"Within range of Fibonacci {fib_level} level: +{fib_score} points", "FIBONACCI")
        
        context["score_components"]["fibonacci_proximity"] = fib_score
        
        # Direction bias based on Fibonacci level
        price = context["price"]
        fib_price = nearest_fib["price"]
        market_bias = context.get("market_bias", "")
        
        # Determine directional bias based on price relative to fib level and market bias
        if price < fib_price and fib_level <= 0.382:
            # Price below a support level - potential long
            if "Bullish" in market_bias:
                # Strong long signal - price below support in bullish market
                context["score_components"]["direction_bias"] = 30
                direction = "LONG"
                self.log_debug(f"Price below 0.382 support in bullish market: +30 points for LONG", "SIGNAL")
            else:
                context["score_components"]["direction_bias"] = 15
                direction = "LONG"
                self.log_debug(f"Price below 0.382 support: +15 points for LONG", "SIGNAL")
                
        elif price > fib_price and fib_level >= 0.618:
            # Price above resistance level - potential short
            if "Bearish" in market_bias:
                # Strong short signal - price above resistance in bearish market
                context["score_components"]["direction_bias"] = 30
                direction = "SHORT"
                self.log_debug(f"Price above 0.618 resistance in bearish market: +30 points for SHORT", "SIGNAL")
            else:
                context["score_components"]["direction_bias"] = 15
                direction = "SHORT"
                self.log_debug(f"Price above 0.618 resistance: +15 points for SHORT", "SIGNAL")
        
        return context
    
    def check_market_conditions(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate overall market conditions."""
        if "score_components" not in context:
            context["score_components"] = {}
            
        # Check for recent MM traps (negative factor)
        if context.get("recent_trap") and time.time() - context["recent_trap"].get("timestamp", 0) < 900:
            context["score_components"]["mm_trap_penalty"] = -40
            self.log_debug("Recent MM trap detected: -40 points", "WARNING")
            
        # Check for excess volatility
        volatility = context.get("recent_volatility", 0)
        if volatility > 500:
            context["score_components"]["excess_volatility"] = -20
            self.log_debug(f"Excess volatility (${volatility:.2f}): -20 points", "WARNING")
        
        # Check timeframe alignment
        if context.get("trend_alignment", 0) > 0.6:  # Lowered from 0.75
            # Strong trend alignment
            alignment_bonus = int(context["trend_alignment"] * 50)  # Increased from 40
            context["score_components"]["trend_alignment"] = alignment_bonus
            self.log_debug(f"Strong trend alignment: +{alignment_bonus} points", "SIGNAL")
            
        # Market regime adjustment
        regime = context.get("regime", "unknown")
        if regime == "trending":
            context["score_components"]["market_regime"] = 10
            self.log_debug("Trending market regime: +10 points", "ANALYSIS")
        elif regime == "ranging":
            context["score_components"]["market_regime"] = 5
            self.log_debug("Ranging market regime: +5 points", "ANALYSIS")
        
        # In check_market_conditions
        if context.get("bullish_timeframes", 0) >= 3 and "Bullish" in context.get("market_bias", ""):
            context["score_components"]["momentum_bonus"] = 20
            self.log_debug("Strong bullish momentum across timeframes: +20 points", "SIGNAL")
            
        return context
    
    def calculate_entry_score(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate final entry score and determine trading action."""
        if "score_components" not in context:
            context["score_components"] = {}
            context["final_score"] = 0
            context["recommendation"] = "NO_ACTION"
            context["reason"] = "Insufficient data for analysis"
            return context
            
        # ✨ DEBUG: Print detailed breakdown of all score components
        self.log_debug("=== SCORE COMPONENT BREAKDOWN ===", "INFO")
        for component, score in sorted(context["score_components"].items()):
            sign = "+" if score > 0 else ""
            self.log_debug(f"{component:25s}: {sign}{score}", "INFO")
        self.log_debug("===============================", "INFO")
            
        # Sum all score components
        total_score = sum(context["score_components"].values())
        context["final_score"] = total_score
        
        # Determine direction preference
        direction_bias = context["score_components"].get("direction_bias", 0)
        trend_bullish = context.get("bullish_timeframes", 0) > context.get("bearish_timeframes", 0)
        
        # Format detailed reasoning
        reasons = []
        for component, score in context["score_components"].items():
            if score != 0:
                sign = "+" if score > 0 else ""
                reasons.append(f"{component}: {sign}{score}")
                
        reason_text = ", ".join(reasons)
        
        # Make recommendation
        if total_score >= self.entry_threshold:
            # High enough score for entry
            if direction_bias > 0:
                # Direction bias from Fibonacci analysis
                direction = "LONG" if trend_bullish else "SHORT"
                leverage = min(5, 1 + int(total_score / 20))  # Scale leverage with confidence
                
                context["recommendation"] = f"{direction}"
                context["leverage"] = leverage
                context["reason"] = f"High confidence entry ({total_score}/100): {reason_text}"
                
                self.log_debug(
                    f"✅ RECOMMENDED {direction} WITH {leverage}x LEVERAGE (Score: {total_score}/100)", 
                    "SIGNAL"
                )
            else:
                # Use timeframe analysis for direction
                if context.get("bullish_timeframes", 0) > context.get("bearish_timeframes", 0) * 1.5:
                    direction = "LONG"
                    leverage = min(3, 1 + int(total_score / 25))
                    
                    context["recommendation"] = f"{direction}"
                    context["leverage"] = leverage
                    context["reason"] = f"Bullish timeframe dominance ({total_score}/100): {reason_text}"
                    
                    self.log_debug(
                        f"✅ RECOMMENDED {direction} WITH {leverage}x LEVERAGE (Score: {total_score}/100)", 
                        "SIGNAL"
                    )
                elif context.get("bearish_timeframes", 0) > context.get("bullish_timeframes", 0) * 1.5:
                    direction = "SHORT"
                    leverage = min(3, 1 + int(total_score / 25))
                    
                    context["recommendation"] = f"{direction}"
                    context["leverage"] = leverage
                    context["reason"] = f"Bearish timeframe dominance ({total_score}/100): {reason_text}"
                    
                    self.log_debug(
                        f"✅ RECOMMENDED {direction} WITH {leverage}x LEVERAGE (Score: {total_score}/100)", 
                        "SIGNAL"
                    )
                else:
                    context["recommendation"] = "NO_ACTION"
                    context["reason"] = f"Unclear directional bias despite high score ({total_score}/100)"
                    
                    self.log_debug(
                        f"❓ NO ACTION - Unclear direction despite high score: {total_score}/100", 
                        "SIGNAL"
                    )
        else:
            context["recommendation"] = "NO_ACTION"
            context["reason"] = f"Insufficient confidence ({total_score}/100): {reason_text}"
            
            self.log_debug(
                f"❌ NO ACTION - Score below threshold: {total_score}/100", 
                "SIGNAL"
            )
            
        return context
    
    def analyze_trading_opportunity(self) -> Tuple[bool, str, int]:
        """Perform full trading opportunity analysis.
        
        Returns:
            Tuple containing:
            - Boolean: Whether to open a position
            - String: Reason/direction
            - Int: Recommended leverage
        """
        # Check if we've analyzed too recently
        now = datetime.datetime.now()
        if (now - self.last_analysis_time).total_seconds() < self.analysis_cooldown:
            return False, "Analysis cooldown in effect", 0
            
        self.last_analysis_time = now
        
        self.log_debug("───────────────────────────────────────", "INFO")
        self.log_debug("🔍 STARTING TRADING OPPORTUNITY ANALYSIS", "INFO")
        self.log_debug("───────────────────────────────────────", "INFO")
        
        # Get market context
        context = self.get_market_context()
        
        # Run analysis components with new components
        context = self.analyze_timeframes(context)
        context = self.analyze_short_timeframes(context)  # NEW: Short timeframe analysis
        context = self.analyze_volume_acceleration(context)  # NEW: Volume acceleration analysis
        context = self.evaluate_fibonacci_entry(context)
        context = self.check_market_conditions(context)
        
        # Calculate final score and recommendation
        context = self.calculate_entry_score(context)
        
        # Print summary
        self.log_debug("───────────────────────────────────────", "INFO")
        self.log_debug(f"ANALYSIS SUMMARY: Score {context.get('final_score', 0)}/100", "INFO")
        self.log_debug(f"Recommendation: {context.get('recommendation', 'NO_ACTION')}", "INFO")
        self.log_debug(f"Reason: {context.get('reason', 'No reason provided')}", "INFO")
        self.log_debug("───────────────────────────────────────", "INFO")
        
        # Return decision
        should_trade = context.get("recommendation", "NO_ACTION") in ["LONG", "SHORT"]
        reason = f"{context.get('recommendation', 'NO_ACTION')} - {context.get('reason', 'No reason provided')}"
        leverage = context.get("leverage", 1)
        
        return should_trade, reason, leverage

    def analyze_timeframe_trend(self, timeframe_minutes, price_data=None):
        """Analyze price trend for a specific timeframe."""
        try:
            # Fetch price data if not provided
            if price_data is None:
                # Try to get from Redis
                key = f"btc_price_{timeframe_minutes}m"
                data_str = self.redis_conn.get(key)
                
                if not data_str:
                    raise ValueError(f"No data available for {timeframe_minutes}m timeframe")
                    
                try:
                    price_data = json.loads(data_str)
                except json.JSONDecodeError:
                    # Maybe it's just a list of floats as strings
                    price_data = [float(x) for x in data_str.split(',') if x.strip()]
            
            # Ensure we have enough data points
            if len(price_data) < 10:
                raise ValueError(f"Insufficient data points for {timeframe_minutes}m analysis")
                
            # Convert all values to floats
            price_data = [safe_float_convert(x) for x in price_data]
            
            # Calculate basic trend indicators
            current = price_data[-1]
            prev = price_data[-2] if len(price_data) > 1 else current
            sma5 = sum(price_data[-5:]) / 5 if len(price_data) >= 5 else current
            sma10 = sum(price_data[-10:]) / 10 if len(price_data) >= 10 else current
            
            # Calculate simple momentum
            momentum = current - price_data[-5] if len(price_data) >= 5 else 0
            
            # Determine trend direction and strength
            if current > sma5 > sma10 and momentum > 0:
                trend = "Bullish"
                strength = min(1.0, abs(current - sma10) / current + 0.2)
            elif current < sma5 < sma10 and momentum < 0:
                trend = "Bearish"
                strength = min(1.0, abs(current - sma10) / current + 0.2)
            else:
                # Mixed signals or sideways
                if abs(momentum) / current < 0.005:  # Less than 0.5% change
                    trend = "Sideways"
                    strength = 0.2
                else:
                    trend = "Mixed"
                    strength = 0.3
                    if momentum > 0:
                        trend = "Weakly Bullish"
                    else:
                        trend = "Weakly Bearish"
            
            # Find key support/resistance levels using simple peak detection
            key_levels = []
            if len(price_data) > 20:
                # Look for recent highs and lows
                for i in range(2, min(20, len(price_data) - 2)):
                    # Check for local maxima (resistance)
                    if price_data[i] > price_data[i-1] and price_data[i] > price_data[i-2] and \
                       price_data[i] > price_data[i+1] and price_data[i] > price_data[i+2]:
                        key_levels.append({
                            "type": "resistance",
                            "price": price_data[i],
                            "strength": 0.7
                        })
                    
                    # Check for local minima (support)
                    if price_data[i] < price_data[i-1] and price_data[i] < price_data[i-2] and \
                       price_data[i] < price_data[i+1] and price_data[i] < price_data[i+2]:
                        key_levels.append({
                            "type": "support",
                            "price": price_data[i],
                            "strength": 0.7
                        })
            
            # Create the trend data result
            trend_data = {
                "trend": trend,
                "strength": strength,
                "price": current,
                "momentum": momentum,
                "sma5": sma5,
                "sma10": sma10,
                "key_levels": key_levels,
                "timeframe": timeframe_minutes,
                "valid": True
            }
            
            return trend_data
            
        except Exception as e:
            # Improved error handling - detailed logging
            error_message = f"Error analyzing {timeframe_minutes}min trend: {str(e)}"
            if hasattr(self, 'logger'):
                self.logger.warning(error_message)
            else:
                print(f"[WARNING] {error_message}")
            
            # Return a default/fallback trend analysis instead of failing
            return {
                "trend": "unknown",
                "strength": 0,
                "key_levels": [],
                "timeframe": timeframe_minutes,
                "valid": False
            }

def safe_float_convert(value):
    """Convert various number representations to float safely."""
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        # Handle numpy string representation
        if "np.float" in value or "numpy.float" in value:
            # Extract the numeric part inside parentheses
            import re
            match = re.search(r'\((.*?)\)', value)
            if match:
                try:
                    return float(match.group(1))
                except ValueError:
                    return 0.0
        try:
            return float(value)
        except ValueError:
            return 0.0
    # For numpy types that need conversion
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0