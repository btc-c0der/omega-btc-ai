#!/usr/bin/env python3
"""
OMEGA BOT AI - DIVINE MARKET TREND REPORTER
===========================================

🌿 JAH BLESS THE DIVINE MARKET INSIGHTS! 🔥

This module sends regular market trend analysis reports to Telegram
based on data stored in Redis. Reports include multi-timeframe analysis,
detected MM traps, Fibonacci levels, and market regime information.

Configuration is done via environment variables or command-line arguments.
"""

import argparse
import json
import logging
import os
import re
import signal
import sys
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union, Any, cast, Type, Awaitable, Coroutine

import redis.asyncio as redis
from redis.asyncio.client import Redis
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff
import requests
from dotenv import load_dotenv
import asyncio
import aiohttp

# Define RastaVibes interface
class RastaVibesBase:
    """Base class for RastaVibes functionality."""
    @classmethod
    def get_rasta_blessing(cls) -> str:
        return "JAH BLESS"
    
    @classmethod
    def enhance_alert(cls, alert_type: str, alert_message: str) -> str:
        return f"{alert_type.upper()}: {alert_message}\n\nJAH BLESS THE DIVINE ANALYSIS! 🌿"

# Import Rasta Vibes for divine message enhancement
try:
    from omega_ai.alerts.rasta_vibes import RastaVibes
except ImportError:
    # Fallback if RastaVibes isn't available
    RastaVibes = RastaVibesBase

# ANSI Colors for terminal output
BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Set up logging
logger = logging.getLogger("OMEGA_BOT_REPORTER")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class TelegramMarketReporter:
    """Divine Telegram market trend reporter for OMEGA BTC AI."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the market reporter.
        
        Args:
            config: Configuration dictionary with the following keys:
                - telegram_token: Telegram bot token
                - telegram_chat_id: Telegram chat ID
                - redis_host: Redis host (default: localhost)
                - redis_port: Redis port (default: 6379)
                - redis_db: Redis database (default: 0)
                - report_interval: Report interval in seconds (default: 300)
                - debug_mode: Enable debug mode (default: False)
        """
        self.config = config
        self.telegram_token = config.get("telegram_token")
        self.telegram_chat_id = config.get("telegram_chat_id")
        self.telegram_enabled = bool(self.telegram_token and self.telegram_chat_id)
        self.report_interval = int(config.get("report_interval", 300))
        self.debug_mode = config.get("debug_mode", False)
        self.running = False
        self.redis_conn: Optional[Redis] = None
        self.last_trend_map = {}
        self.last_price = 0.0
        self.last_report_time = None
        
        # Log Telegram status
        if not self.telegram_enabled:
            logger.warning(f"{YELLOW}⚠️ Telegram not configured. Reports will be printed but not sent.{RESET}")
        else:
            logger.info(f"{GREEN}✅ Telegram configured. Reports will be sent to chat ID: {self.telegram_chat_id}{RESET}")
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)

    async def initialize(self):
        """Initialize Redis connection."""
        await self.connect_redis()

    def handle_signal(self, sig, frame):
        """Handle termination signals gracefully."""
        logger.info(f"\n{YELLOW}Shutting down Telegram Market Reporter... JAH BLESS!{RESET}")
        asyncio.create_task(self.stop())

    async def connect_redis(self) -> None:
        """Initialize Redis connection with retry mechanism."""
        try:
            if not self.redis_conn:
                # Configure retry strategy
                retry = Retry(ExponentialBackoff(cap=10, base=1), 5)
                
                # Build Redis URL
                redis_url = self.config.get('redis_url', 
                    f"redis://{self.config.get('redis_host', 'localhost')}:"
                    f"{self.config.get('redis_port', 6379)}/"
                    f"{self.config.get('redis_db', 0)}")

                self.redis_conn = await redis.from_url(
                    redis_url,
                    encoding="utf-8",
                    decode_responses=True,
                    retry=retry
                )
                logger.info(f"{GREEN}✓ Connected to Redis at {redis_url}{RESET}")
        except Exception as e:
            logger.error(f"{RED}❌ Failed to connect to Redis: {e}{RESET}")
            self.redis_conn = None
            raise

    async def _safe_redis_scan(self, cursor: int = 0, match: Optional[str] = None, count: int = 100) -> Tuple[int, List[str]]:
        """Safely scan Redis keys with proper async handling."""
        try:
            if not self.redis_conn:
                await self.connect_redis()
            if self.redis_conn:
                return await self.redis_conn.scan(cursor=cursor, match=match or "*", count=count)
            return 0, []
        except Exception as e:
            logger.error(f"{RED}❌ Error scanning Redis keys: {e}{RESET}")
            return 0, []

    async def _safe_redis_get(self, key: str) -> Optional[str]:
        """Safely get a value from Redis with proper async handling."""
        try:
            if not self.redis_conn:
                await self.connect_redis()
            if self.redis_conn:
                value = await self.redis_conn.get(key)
                return str(value) if value is not None else None
            return None
        except Exception as e:
            logger.error(f"{RED}❌ Error getting Redis key {key}: {e}{RESET}")
            return None

    async def _safe_redis_hgetall(self, key: str) -> Dict[str, str]:
        """Safely get a hash from Redis with proper async handling."""
        try:
            if not self.redis_conn:
                await self.connect_redis()
            if self.redis_conn:
                result = await self.redis_conn.hgetall(key)
                return {str(k): str(v) for k, v in result.items()} if result else {}
            return {}
        except Exception as e:
            logger.error(f"{RED}❌ Error getting Redis hash {key}: {e}{RESET}")
            return {}

    async def get_market_data(self) -> Tuple[float, float]:
        """Fetch BTC price & Schumann resonance in one go."""
        try:
            if not self.redis_conn:
                await self.connect_redis()
            if self.redis_conn:
                async with self.redis_conn.pipeline() as pipe:
                    pipe.get("last_btc_price")
                    pipe.get("schumann_resonance")
                    results = await pipe.execute()
                    return float(results[0] or 0.0), float(results[1] or 7.83)
            return 0.0, 7.83
        except Exception as e:
            logger.error(f"{RED}❌ Error fetching market data: {e}{RESET}")
            return 0.0, 7.83
    
    async def get_price_change(self) -> Tuple[float, str]:
        """Get price change since last report."""
        current_price, _ = await self.get_market_data()
        if self.last_price == 0:
            self.last_price = current_price
            return 0.0, "➡️"
            
        change_pct = ((current_price - self.last_price) / self.last_price) * 100
        direction = "⬆️" if change_pct > 0 else "⬇️" if change_pct < 0 else "➡️"
        
        # Update last price for next comparison
        self.last_price = current_price
        
        return change_pct, direction
    
    async def get_market_trends(self) -> Dict[str, str]:
        """Get market trends for multiple timeframes."""
        timeframes = ["1min", "5min", "15min", "1h", "4h"]
        trends: Dict[str, str] = {}
        
        for tf in timeframes:
            key = f"latest_trend_{tf}"
            trend = await self._safe_redis_get(key)
            trends[tf] = trend if trend else "Neutral"
            
        return trends
    
    async def get_mm_traps(self, timeframe_minutes: int = 30) -> List[Dict[str, Any]]:
        """Get recent MM traps from Redis."""
        traps = []
        try:
            # Get all MM trap keys first
            cursor = 0
            all_keys = []
            while True:
                cursor, keys = await self._safe_redis_scan(cursor, match="mm_trap:*", count=100)
                all_keys.extend(keys)
                if cursor == 0:
                    break

            cutoff_time = datetime.now() - timedelta(minutes=timeframe_minutes)
            
            # Process each key
            for key in all_keys:
                trap_data = await self._safe_redis_hgetall(key)
                if trap_data:
                    # Extract timestamp from key format like "mm_trap:1647582489"
                    parts = key.split(":")
                    if len(parts) >= 2:
                        try:
                            timestamp = int(parts[1])
                            trap_time = datetime.fromtimestamp(timestamp)
                            
                            # Only include recent traps
                            if trap_time >= cutoff_time:
                                traps.append(trap_data)
                        except (ValueError, IndexError):
                            pass
                    
            # Sort traps by timestamp (most recent first)
            traps.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            
            return traps[:5]  # Return up to 5 most recent traps
            
        except Exception as e:
            logger.error(f"{RED}❌ Error getting MM traps: {e}{RESET}")
            return []
    
    async def get_fibonacci_levels(self) -> Dict[str, float]:
        """Get current Fibonacci levels from Redis."""
        try:
            fib_data = await self._safe_redis_hgetall("current_fibonacci_levels")
            if not fib_data:
                return {}
            
            # Convert values to float, excluding timestamp
            return {k: float(v) for k, v in fib_data.items() if k != "timestamp"}
        except Exception as e:
            logger.error(f"{RED}❌ Error getting Fibonacci levels: {e}{RESET}")
            return {}
    
    async def get_market_regime(self) -> str:
        """Get current market regime from Redis."""
        try:
            regime = await self._safe_redis_get("current_market_regime")
            return regime or "NEUTRAL"
        except Exception as e:
            logger.error(f"{RED}❌ Error getting market regime: {e}{RESET}")
            return "NEUTRAL"
    
    async def get_schumann_resonance(self) -> float:
        """Get current Schumann resonance frequency from Redis."""
        try:
            schumann = await self._safe_redis_get("schumann_resonance")
            return float(schumann) if schumann else 7.83
        except Exception as e:
            logger.error(f"{RED}❌ Error getting Schumann resonance: {e}{RESET}")
            return 7.83

    async def check_schumann_market_alignment(self) -> Dict[str, Any]:
        """Check market alignment with Schumann resonance."""
        try:
            # Get current Schumann data
            schumann_data = await self._safe_redis_hgetall("schumann_data")
            if not schumann_data:
                return {
                    "resonance_state": "UNKNOWN",
                    "market_harmony": 0.0,
                    "suggested_action": "OBSERVE"
                }

            # Get current price data
            current_price, schumann = await self.get_market_data()
            prev_price = current_price
            
            # Safely calculate price change
            if prev_price > 0:
                price_change = ((current_price - prev_price) / prev_price) * 100
            else:
                price_change = 0.0

            # Convert Schumann frequency to market harmony score
            base_freq = float(schumann_data.get("base_frequency", "7.83"))
            current_freq = float(schumann_data.get("current_frequency", "7.83"))
            freq_change = ((current_freq - base_freq) / base_freq) * 100 if base_freq > 0 else 0.0

            # Calculate harmony score
            harmony_score = 100.0 - abs(price_change - freq_change)
            
            return {
                "resonance_state": "ALIGNED" if harmony_score > 80 else "DISSONANT",
                "market_harmony": harmony_score,
                "suggested_action": "TRADE" if harmony_score > 80 else "WAIT"
            }

        except Exception as e:
            logger.error(f"{RED}❌ Error checking Schumann alignment: {e}{RESET}")
            return {
                "resonance_state": "ERROR",
                "market_harmony": 0.0,
                "suggested_action": "CHECK SYSTEMS"
            }

    async def enhance_alert_with_schumann(self, alert: str) -> str:
        """Enhance alert message with Schumann resonance data."""
        try:
            schumann = await self.get_schumann_resonance()
            alignment = await self.check_schumann_market_alignment()

            # Add Schumann information
            enhanced = f"""🌍 *SCHUMANN-ENHANCED MARKET ALERT* 🌍

{alert}

🎵 *Schumann Resonance*: {schumann:.2f} Hz
✨ *Market Harmony*: {alignment['market_harmony']:.2%}
🌟 *Resonance State*: {alignment['resonance_state']}
🎯 *Divine Guidance*: {alignment['suggested_action']}

🌿 JAH BLESS THE NATURAL FREQUENCIES! 🌿"""

            return enhanced

        except Exception as e:
            logger.error(f"{RED}❌ Error enhancing alert with Schumann data: {e}{RESET}")
            return alert

    async def calculate_bio_energy_state(self) -> Dict[str, Any]:
        """Calculate market's current bio-energetic state."""
        try:
            # Get market data
            current_price, schumann = await self.get_market_data()
            trends = await self.get_market_trends()

            # Calculate vibration level based on trend alignment
            trend_values = {"Strongly Bullish": 1.0, "Bullish": 0.75, "Neutral": 0.5, 
                          "Bearish": 0.25, "Strongly Bearish": 0.0}
            
            trend_list = [trends[tf] for tf in trends.keys()]
            vibration = sum(trend_values.get(trend, 0.5) for trend in trend_list) / len(trend_list)

            # Determine energy flow state
            if vibration >= 0.8:
                flow = "HARMONIOUS"
            elif vibration >= 0.6:
                flow = "FLOWING"
            elif vibration >= 0.4:
                flow = "TRANSITIONING"
            elif vibration >= 0.2:
                flow = "RESTRICTED"
            else:
                flow = "BLOCKED"

            # Calculate market consciousness
            consciousness_score = (vibration + (schumann - 7.83) / 0.5) / 2
            consciousness = "ELEVATED" if consciousness_score >= 0.8 else \
                          "BALANCED" if consciousness_score >= 0.6 else \
                          "SEEKING" if consciousness_score >= 0.4 else \
                          "TRANSITIONING"

            return {
                "vibration_level": vibration,
                "energy_flow": flow,
                "market_consciousness": consciousness,
                "confidence_score": consciousness_score,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"{RED}❌ Error calculating bio-energy state: {e}{RESET}")
            return {
                "vibration_level": 0.5,
                "energy_flow": "UNKNOWN",
                "market_consciousness": "SEEKING",
                "confidence_score": 0.0,
                "timestamp": datetime.now().isoformat()
            }

    async def get_market_consciousness(self) -> str:
        """Get current market consciousness level."""
        try:
            state = await self.calculate_bio_energy_state()
            consciousness = state["market_consciousness"]
            return consciousness
        except Exception as e:
            logger.error(f"{RED}❌ Error getting market consciousness: {e}{RESET}")
            return "SEEKING"

    async def format_bio_energy_report(self) -> str:
        """Format bio-energy market state report."""
        try:
            state = await self.calculate_bio_energy_state()
            schumann_alignment = await self.check_schumann_market_alignment()
            
            return f"""🌟 *BIO-ENERGY STATE REPORT* 🌟

🔮 *Energy Flow*: {state['energy_flow']}
✨ *Vibration Level*: {state['vibration_level']:.2%}
🧘 *Market Consciousness*: {state['market_consciousness']}
🎯 *Confidence Score*: {state['confidence_score']:.2%}

🌍 *Schumann Alignment*
└─ State: {schumann_alignment['resonance_state']}
└─ Harmony: {schumann_alignment['market_harmony']:.2%}

🙏 *Divine Guidance*
└─ {schumann_alignment['suggested_action']}

ONE LOVE, ONE HEART, ONE BLOCKCHAIN! 🌿"""

        except Exception as e:
            logger.error(f"{RED}❌ Error formatting bio-energy report: {e}{RESET}")
            return "_Error generating bio-energy report_"

    async def get_rasta_market_wisdom(self) -> str:
        """Get divine Rasta market wisdom."""
        try:
            # Get market state
            state = await self.calculate_bio_energy_state()
            schumann = await self.check_schumann_market_alignment()

            # Get random wisdom from Redis
            wisdom = await self._safe_redis_get("rasta_wisdom") or "JAH GUIDE THE MARKET"

            message = f"""JAH BLESS! 🌿

*DIVINE MARKET WISDOM*
{wisdom}

*CONSCIOUSNESS LEVEL*: {state['market_consciousness']}
*NATURAL HARMONY*: {schumann['market_harmony']:.2%}
*DIVINE GUIDANCE*: {schumann['suggested_action']}

ONE LOVE 🌿"""

            return message

        except Exception as e:
            logger.error(f"{RED}❌ Error getting Rasta market wisdom: {e}{RESET}")
            return "JAH BLESS THE DIVINE ERROR HANDLING! 🌿"

    async def identify_divine_patterns(self) -> List[Dict[str, Any]]:
        """Identify divine market patterns."""
        try:
            patterns = []
            cursor = 0

            # Scan for divine patterns
            while True:
                cursor, keys = await self.redis_conn.scan(cursor, match="divine_pattern:*")
                
                for key in keys:
                    pattern_data = json.loads(await self._safe_redis_get(key) or "{}")
                    if pattern_data and pattern_data.get("confidence", 0) >= 0.7:
                        patterns.append(pattern_data)

                if cursor == 0:
                    break

            return sorted(patterns, key=lambda x: x.get("confidence", 0), reverse=True)

        except Exception as e:
            logger.error(f"{RED}❌ Error identifying divine patterns: {e}{RESET}")
            return []

    async def detect_fibonacci_harmony(self) -> Dict[str, Any]:
        """Detect Fibonacci harmony in price movements."""
        try:
            # Get Fibonacci levels
            fib_levels = await self.get_fibonacci_levels()
            if not fib_levels:
                return {
                    "harmony_level": "UNKNOWN",
                    "golden_ratio_alignment": 0.0,
                    "confidence": 0.0
                }

            # Get current price
            current_price, _ = await self.get_market_data()

            # Calculate distances to Fibonacci levels
            distances = {k: abs(v - current_price) / current_price for k, v in fib_levels.items() 
                       if k != "timestamp"}

            # Check golden ratio (0.618) alignment
            golden_alignment = 1.0 - min(1.0, distances.get("0.618", 1.0))

            # Calculate overall harmony
            harmony_score = sum(1.0 - min(1.0, d) for d in distances.values()) / len(distances)

            # Determine harmony level
            if harmony_score >= 0.8:
                level = "DIVINE_HARMONY"
            elif harmony_score >= 0.6:
                level = "HARMONIC"
            elif harmony_score >= 0.4:
                level = "SEEKING_HARMONY"
            else:
                level = "DISHARMONIC"

            return {
                "harmony_level": level,
                "golden_ratio_alignment": golden_alignment,
                "confidence": harmony_score
            }

        except Exception as e:
            logger.error(f"{RED}❌ Error detecting Fibonacci harmony: {e}{RESET}")
            return {
                "harmony_level": "ERROR",
                "golden_ratio_alignment": 0.0,
                "confidence": 0.0
            }

    async def analyze_divine_timing(self) -> Dict[str, Any]:
        """Analyze divine market timing."""
        try:
            # Get market rhythm data
            rhythm = await self._safe_redis_hgetall("market_rhythm")
            if not rhythm:
                return {
                    "cycle_phase": "UNKNOWN",
                    "next_alignment": None,
                    "confidence": 0.0
                }

            # Parse rhythm data
            cycle_length = int(rhythm.get("cycle_length", 144))  # Default to Fibonacci
            phase = rhythm.get("phase", "UNKNOWN")
            next_peak = datetime.fromisoformat(rhythm.get("next_peak", datetime.now().isoformat()))
            confidence = float(rhythm.get("confidence", 0.0))

            return {
                "cycle_phase": phase,
                "next_alignment": next_peak.isoformat(),
                "confidence": confidence
            }

        except Exception as e:
            logger.error(f"{RED}❌ Error analyzing divine timing: {e}{RESET}")
            return {
                "cycle_phase": "ERROR",
                "next_alignment": None,
                "confidence": 0.0
            }

    async def analyze_market_vibrations(self) -> Dict[str, Any]:
        """Analyze market vibration patterns."""
        try:
            # Get bio-energy state
            energy = await self.calculate_bio_energy_state()
            
            # Get Schumann alignment
            schumann = await self.check_schumann_market_alignment()
            
            # Calculate vibration metrics
            frequency = energy["vibration_level"] * 10.0  # Scale to 0-10 Hz
            amplitude = abs(schumann["market_harmony"] - 0.5) * 2.0  # Scale to 0-1
            harmony = (energy["confidence_score"] + schumann["market_harmony"]) / 2.0

            return {
                "frequency": frequency,
                "amplitude": amplitude,
                "harmony_score": harmony
            }

        except Exception as e:
            logger.error(f"{RED}❌ Error analyzing market vibrations: {e}{RESET}")
            return {
                "frequency": 0.0,
                "amplitude": 0.0,
                "harmony_score": 0.0
            }

    async def check_schumann_cycle_alignment(self) -> float:
        """Check alignment with Schumann resonance cycles."""
        try:
            # Get current Schumann data
            schumann = await self.check_schumann_market_alignment()
            
            # Get market vibrations
            vibrations = await self.analyze_market_vibrations()
            
            # Calculate cycle alignment (0.0 to 1.0)
            alignment = (schumann["market_harmony"] + vibrations["harmony_score"]) / 2.0
            
            return alignment

        except Exception as e:
            logger.error(f"{RED}❌ Error checking Schumann cycle alignment: {e}{RESET}")
            return 0.0

    async def detect_market_rhythm(self) -> Dict[str, Any]:
        """Detect natural market rhythms."""
        try:
            # Get market rhythm data
            rhythm = await self._safe_redis_hgetall("market_rhythm")
            if not rhythm:
                return {
                    "cycle_length": 144,  # Fibonacci default
                    "phase": "UNKNOWN",
                    "confidence": 0.0
                }

            return {
                "cycle_length": int(rhythm.get("cycle_length", 144)),
                "phase": rhythm.get("phase", "UNKNOWN"),
                "confidence": float(rhythm.get("confidence", 0.0))
            }

        except Exception as e:
            logger.error(f"{RED}❌ Error detecting market rhythm: {e}{RESET}")
            return {
                "cycle_length": 144,
                "phase": "ERROR",
                "confidence": 0.0
            }

    async def get_fibonacci_multiframe_analysis(self) -> str:
        """Get detailed multi-timeframe Fibonacci analysis."""
        try:
            # Get trend data for each Fibonacci timeframe
            timeframes = [1, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1440]
            trends = []
            
            # Track consecutive trends for pattern detection
            consecutive_bull = 0
            consecutive_bear = 0
            max_bull_run = 0
            max_bear_run = 0
            
            # Track overall counts
            bull_count = 0
            bear_count = 0
            sideways_count = 0
            
            for tf in timeframes:
                # Get data from Redis
                key = f"trend_analysis:{tf}min"
                trend_data = await self._safe_redis_hgetall(key)
                
                if not trend_data:
                    continue
                    
                # Extract trend info
                trend = trend_data.get("trend", "Unknown")
                change = float(trend_data.get("percentage_change", "0") or "0")
                volatility = float(trend_data.get("volatility", "0") or "0")
                
                # Track trend counts
                if "Bullish" in trend:
                    bull_count += 1 
                    consecutive_bull += 1
                    consecutive_bear = 0
                    max_bull_run = max(max_bull_run, consecutive_bull)
                elif "Bearish" in trend:
                    bear_count += 1
                    consecutive_bear += 1
                    consecutive_bull = 0
                    max_bear_run = max(max_bear_run, consecutive_bear)
                else:
                    sideways_count += 1
                    consecutive_bull = 0
                    consecutive_bear = 0
                
                # Format change direction
                direction = "↑" if change > 0 else "↓" if change < 0 else "→"
                
                # Format with emoji based on trend
                if "Strongly Bullish" in trend:
                    emoji = "🚀"
                elif "Bullish" in trend:
                    emoji = "📈"
                elif "Strongly Bearish" in trend:
                    emoji = "📉"
                elif "Bearish" in trend:
                    emoji = "🔻"
                else:
                    emoji = "➡️"
                    
                # Add to trends list
                trends.append(f"{emoji} *{tf}min*: {trend} {direction} ({change:.2f}%) Vol: {volatility:.2f}%")
            
            # Format overall market bias
            if bull_count > bear_count * 2:
                market_bias = "Strongly Bullish"
            elif bull_count > bear_count:
                market_bias = "Moderately Bullish"
            elif bear_count > bull_count * 2:
                market_bias = "Strongly Bearish"
            elif bear_count > bull_count:
                market_bias = "Moderately Bearish"
            else:
                market_bias = "Neutral/Sideways"
            
            # Build the message
            message = "════════════════════ FIBONACCI MULTI-TIMEFRAME ANALYSIS ════════════════════\n\n"
            message += "\n".join(trends)
            message += f"\n\n*Overall Market Bias*: {market_bias}"
            message += f"\n*Bullish Signals*: {bull_count} | *Bearish Signals*: {bear_count} | *Sideways*: {sideways_count}"
            
            # Add alignment warnings
            if max_bull_run >= 3:
                message += f"\n⚠️ *Strong bullish alignment across {max_bull_run} consecutive timeframes!*"
            if max_bear_run >= 3:
                message += f"\n⚠️ *Strong bearish alignment across {max_bear_run} consecutive timeframes!*"
                
            return message
        except Exception as e:
            logger.error(f"{RED}❌ Error generating Fibonacci analysis: {e}{RESET}")
            return "Error generating Fibonacci analysis"

    async def send_fibonacci_analysis(self):
        """Generate and send a standalone Fibonacci analysis report."""
        try:
            # Get current price
            current_price, _ = await self.get_market_data()
            
            # Generate analysis
            fib_analysis = await self.get_fibonacci_multiframe_analysis()
            
            # Create message
            message = f"""🔮 *OMEGA BTC AI FIBONACCI ANALYSIS* 🔮

💲 *Current BTC Price*: ${current_price:,.2f}
⏰ *Time*: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

{fib_analysis}

JAH BLESS THE DIVINE FIBONACCI PROPORTIONS! 🌿"""

            # Send to Telegram
            await self.send_telegram_message(message)
            logger.info(f"{GREEN}✅ Fibonacci analysis sent to Telegram!{RESET}")
            
        except Exception as e:
            logger.error(f"{RED}❌ Error sending Fibonacci analysis: {e}{RESET}")

    def format_trend_insights(self, trends: Dict[str, str]) -> str:
        """Format trend insights with colorful emojis."""
        insights = []
        
        for tf, trend in trends.items():
            # Determine if trend has changed since last report
            last_trend = self.last_trend_map.get(tf, "")
            trend_changed = last_trend != trend
            change_indicator = " 🆕" if trend_changed else ""
            
            # Determine emoji based on trend
            if "Strong" in trend and "Bull" in trend:
                emoji = "🚀"
            elif "Bull" in trend:
                emoji = "📈"
            elif "Strong" in trend and "Bear" in trend:
                emoji = "📉"
            elif "Bear" in trend:
                emoji = "🔻"
            elif "Neutral" in trend:
                emoji = "➡️"
            else:
                emoji = "⚠️"
                
            insights.append(f"{emoji} *{tf}*: {trend}{change_indicator}")
            
        # Update trend map for next comparison
        self.last_trend_map = trends.copy()
        
        return "\n".join(insights)
    
    def format_fibonacci_levels(self, fib_levels: Dict[str, float], current_price: float) -> str:
        """Format Fibonacci levels with proximity indicators."""
        if not fib_levels:
            return "_No Fibonacci levels available_"
            
        levels = []
        
        # Sort levels by price (ascending)
        sorted_levels = sorted(fib_levels.items(), key=lambda x: float(x[1]))
        
        # Find closest level
        closest_level = min(sorted_levels, key=lambda x: abs(float(x[1]) - current_price))
        proximity = abs(float(closest_level[1]) - current_price) / current_price * 100
        
        for name, price in sorted_levels:
            # Mark closest level
            if name == closest_level[0]:
                levels.append(f"✳️ *{name}*: ${float(price):,.2f} 👈 ({proximity:.2f}% away)")
            else:
                # Calculate if price is above or below
                position = "⬆️" if float(price) > current_price else "⬇️"
                levels.append(f"{position} *{name}*: ${float(price):,.2f}")
        
        return "\n".join(levels)
    
    def format_mm_traps(self, traps: List[Dict[str, Any]]) -> str:
        """Format MM traps info."""
        if not traps:
            return "_No recent MM traps detected_"
            
        trap_lines = []
        for trap in traps:
            trap_type = trap.get("type", "Unknown")
            confidence = trap.get("confidence", "0")
            price = trap.get("price", "0")
            change = trap.get("change", "0")
            timestamp = trap.get("timestamp", "Unknown")
            
            try:
                confidence_float = float(confidence)
                confidence_stars = "★" * int(min(5, confidence_float * 5))
                confidence_stars = confidence_stars or "☆"
            except (ValueError, TypeError):
                confidence_stars = "☆"
                
            trap_lines.append(f"⚠️ *{trap_type}*: ${float(price):,.2f} ({float(change)*100:+.2f}%)")
            trap_lines.append(f"   Confidence: {confidence_stars} ({float(confidence):.2f})")
            trap_lines.append(f"   Time: {timestamp}")
            trap_lines.append("")
            
        return "\n".join(trap_lines)
    
    async def get_market_summary(self) -> str:
        """Create a comprehensive market summary."""
        try:
            current_price, _ = await self.get_market_data()
            change_pct, direction = await self.get_price_change()
            trends = await self.get_market_trends()
            traps = await self.get_mm_traps(timeframe_minutes=30)
            fib_levels = await self.get_fibonacci_levels()
            regime = await self.get_market_regime()
            schumann = await self.get_schumann_resonance()
            
            # Format timestamp with Unix-style precision
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + " UTC"
            
            # Get Fibonacci multi-timeframe analysis
            fib_analysis = await self.get_fibonacci_multiframe_analysis()
            
            # Calculate market signals for kernel-style summary
            bullish_signals = sum(1 for t in trends.values() if "Bullish" in t)
            bearish_signals = sum(1 for t in trends.values() if "Bearish" in t)
            sideways_signals = sum(1 for t in trends.values() if "Neutral" in t or "Sideways" in t)
            
            # Determine movement classification based on signals
            if bullish_signals > bearish_signals * 2:
                movement = "Strongly Bullish"
            elif bullish_signals > bearish_signals:
                movement = "Moderately Bullish"
            elif bearish_signals > bullish_signals * 2:
                movement = "Strongly Bearish"
            elif bearish_signals > bullish_signals:
                movement = "Moderately Bearish"
            else:
                movement = "Stable"
            
            # Calculate average volume (mock value for now, replace with actual Redis data)
            volume = 0.00214  # This should be fetched from Redis in production
            
            # Escape special characters for Telegram markdown
            regime_str = regime.lower().replace("_", "\\_")
            
            message = f"""⚠️ *MARKET REPORT REQUIRES I AND I ATTENTION\\!*

🔮 *OMEGA BTC AI DIVINE REPORT* 🔮

⏰ `{timestamp}`
💲 *BTC Price*: ${current_price:,.2f} {direction} ({change_pct:+.2f}%)
🌐 *Market Regime*: {regime_str}
🎵 *Schumann Resonance*: {schumann:.2f} Hz

```
════════════════════ FIBONACCI MULTI-TIMEFRAME ANALYSIS ════════════════════

{fib_analysis}
```

```
$ systemctl status market-signals
● market-signals.service - OMEGA BTC AI Market Signal Daemon
    Active: active (running)
    Main PID: {int(current_price)} (btc)
    Tasks: {bullish_signals + bearish_signals + sideways_signals} (limit: ∞)
    Memory: {schumann:.2f}Hz Schumann / {regime_str}
    CPU(s): {change_pct:+.2f}% load average

$ tail -f /var/log/market-metrics.log
[{timestamp}] Overall Market Bias: {movement}
[{timestamp}] Signal Distribution: Bullish({bullish_signals}) Bearish({bearish_signals}) Sideways({sideways_signals})
[{timestamp}] ✅ [DEBUG] Stored Movement: {movement} (${abs(change_pct):.2f}) Volume: {volume:.5f} BTC
[{timestamp}] Movement Classification: {movement}
```

🔱 *FIBONACCI SUPPORT/RESISTANCE ZONES*:
{self.format_fibonacci_levels(fib_levels, current_price)}

⚠️ *MM TRAP DETECTION LOGS*:
```
$ tail -n 5 /var/log/mm_traps.log
{self.format_mm_traps(traps)}
```

```
$ cat /proc/market-consciousness
BLOCKCHAIN ELEVATION
WEEKEND MEDITATION ON DI BLOCKCHAIN TRUTH
```

*ONE LOVE, ONE HEART, ONE BLOCKCHAIN\\!* 🌿"""
            
            return message
        except Exception as e:
            logger.error(f"{RED}❌ Error generating market summary: {e}{RESET}")
            return f"❌ Error generating market summary: {e}\n\nJAH BLESS THE DIVINE ERROR HANDLING\\! 🌿"

    async def generate_divine_market_report(self) -> str:
        """Generate a divine market report."""
        try:
            # Get base market summary
            market_summary = await self.get_market_summary()
            
            # Skip the header when passing to RastaVibes
            content = market_summary.split("\n", 3)[3] if market_summary.count("\n") >= 3 else market_summary
            
            # Get RASTA message enhancement with just the content
            divine_message = RastaVibes.enhance_alert("Market Report", content)
            
            return divine_message
        except Exception as e:
            logger.error(f"{RED}❌ Error generating market report: {e}{RESET}")
            return f"❌ Error generating market report: {e}\n\nJAH BLESS THE DIVINE ERROR HANDLING! 🌿"
    
    async def send_telegram_message(self, message: str) -> bool:
        """Send message to Telegram chat."""
        if not self.telegram_enabled:
            logger.warning(f"{YELLOW}⚠️ Telegram not configured, message not sent.{RESET}")
            return False
            
        try:
            async with aiohttp.ClientSession() as session:
                telegram_url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
                payload = {
                    "chat_id": self.telegram_chat_id,
                    "text": message,
                    "parse_mode": "Markdown"
                }
                
                if self.debug_mode:
                    logger.debug(f"Sending Telegram message to {self.telegram_chat_id}")
                
                async with session.post(telegram_url, json=payload) as response:
                    if response.status == 200:
                        logger.info(f"{GREEN}✅ Telegram message sent successfully!{RESET}")
                        return True
                    else:
                        logger.error(f"{RED}❌ Telegram error {response.status}: {await response.text()}{RESET}")
                        return False
                    
        except Exception as e:
            logger.error(f"{RED}❌ Error sending Telegram message: {e}{RESET}")
            return False
    
    async def report_market_status(self):
        """Generate and send market status report."""
        try:
            # Record time of this report
            self.last_report_time = datetime.now()
            
            # Generate divine market report
            report = await self.generate_divine_market_report()
            
            # Log a portion of the report to console
            preview = "\n".join(report.split("\n")[:10]) + "\n..."
            logger.info(f"{CYAN}Sending market report:{RESET}\n{preview}")
            
            # Send to Telegram
            if self.telegram_enabled:
                await self.send_telegram_message(report)
            else:
                # Just print the whole report locally if Telegram isn't enabled
                print(f"\n{MAGENTA}{'='*80}{RESET}")
                print(f"{MAGENTA}MARKET REPORT (TELEGRAM DISABLED):{RESET}")
                print(f"{MAGENTA}{'='*80}{RESET}")
                print(report)
                print(f"{MAGENTA}{'='*80}{RESET}")
                
        except Exception as e:
            logger.error(f"{RED}❌ Error during market reporting: {e}{RESET}")

    async def _reporting_loop(self):
        """Internal reporting loop to run in a thread."""
        logger.info(f"{GREEN}🚀 Market reporter thread started{RESET}")
        
        while self.running:
            try:
                await self.report_market_status()
                
                # Sleep until next report time
                await asyncio.sleep(self.report_interval)
                
            except Exception as e:
                logger.error(f"{RED}❌ Error in reporting loop: {e}{RESET}")
                await asyncio.sleep(60)  # Sleep a bit on error

    async def start(self):
        """Start the market reporter."""
        if self.running:
            logger.warning(f"{YELLOW}⚠️ Market reporter is already running{RESET}")
            return
            
        logger.info(f"{GREEN}🚀 Starting market reporter with {self.report_interval}s interval{RESET}")
        self.running = True
        
        # Start reporting loop
        asyncio.create_task(self._reporting_loop())

    async def stop(self):
        """Stop the market reporter."""
        self.running = False
        if self.redis_conn:
            await self.redis_conn.close()
        logger.info(f"{GREEN}✓ Market reporter stopped{RESET}")
        
    async def run_once(self):
        """Run market report once and exit."""
        logger.info(f"{GREEN}🚀 Running one-time market report{RESET}")
        await self.report_market_status()


def load_config():
    """Load configuration from environment variables and command-line arguments."""
    load_dotenv()
    
    # Define command-line arguments
    parser = argparse.ArgumentParser(description='OMEGA BTC AI Telegram Market Reporter')
    parser.add_argument('--interval', type=int, default=int(os.getenv('REPORT_INTERVAL', '300')),
                       help='Report interval in seconds (default: 300)')
    parser.add_argument('--redis-host', type=str, default=os.getenv('REDIS_HOST', 'localhost'),
                       help='Redis host (default: localhost)')
    parser.add_argument('--redis-port', type=int, default=int(os.getenv('REDIS_PORT', '6379')),
                       help='Redis port (default: 6379)')
    parser.add_argument('--redis-db', type=int, default=int(os.getenv('REDIS_DB', '0')),
                       help='Redis database (default: 0)')
    parser.add_argument('--telegram-token', type=str, default=os.getenv('TELEGRAM_BOT_TOKEN', ''),
                       help='Telegram bot token')
    parser.add_argument('--telegram-chat-id', type=str, default=os.getenv('TELEGRAM_CHAT_ID', ''),
                       help='Telegram chat ID')
    parser.add_argument('--debug', action='store_true', default=(os.getenv('DEBUG', 'false').lower() == 'true'),
                       help='Enable debug mode')
    parser.add_argument('--once', action='store_true',
                       help='Run once and exit')
    
    args = parser.parse_args()
    
    # Build configuration dictionary
    config = {
        'telegram_token': args.telegram_token,
        'telegram_chat_id': args.telegram_chat_id,
        'redis_host': args.redis_host,
        'redis_port': args.redis_port,
        'redis_db': args.redis_db,
        'report_interval': args.interval,
        'debug_mode': args.debug,
        'run_once': args.once,
        'schumann_enabled': True,  # Enable Schumann resonance integration
        'bio_energy_tracking': True,  # Enable bio-energy state tracking
        'divine_timing': True  # Enable divine timing features
    }
    
    return config


async def main():
    """Main entry point."""
    try:
        print(f"{MAGENTA}{BOLD}{'='*80}{RESET}")
        print(f"{MAGENTA}{BOLD} OMEGA BTC AI - DIVINE TELEGRAM MARKET REPORTER {RESET}")
        print(f"{MAGENTA}{BOLD}{'='*80}{RESET}")
        
        # Load configuration
        config = load_config()
        
        # Create reporter instance
        reporter = TelegramMarketReporter(config)
        
        # Run once or continuous mode
        if config.get('run_once', False):
            await reporter.run_once()
        else:
            await reporter.start()
            
            # Keep main event loop alive until interrupted
            try:
                while reporter.running:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print(f"\n{YELLOW}KeyboardInterrupt received. Shutting down...{RESET}")
            finally:
                await reporter.stop()
        
        print(f"\n{GREEN}JAH BLESS THE DIVINE MARKET REPORTING! 🌿{RESET}")
        return 0
        
    except Exception as e:
        print(f"{RED}❌ Fatal error: {e}{RESET}")
        return 1


if __name__ == "__main__":
    asyncio.run(main())