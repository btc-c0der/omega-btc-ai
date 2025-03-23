"""
EXODUS ALGORITHMS - MOVEMENT OF JAH AI AND JAH JAH PEOPLE

Divine trading intelligence through cosmic Fibonacci flow
"""

import numpy as np
import redis
import json
import asyncio
import logging
import random
import time
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Union, Optional, Any, Tuple
import traceback
import math

from omega_ai.mm_trap_detector.fibonacci_detector import (
    check_fibonacci_alignment, 
    get_current_fibonacci_levels,
    update_fibonacci_data
)
from omega_ai.mm_trap_detector.high_frequency_detector import (
    register_trap_detection, 
    check_volume_anomaly
)
from omega_ai.db_manager.database import (
    insert_price_movement,
    analyze_price_trend
)
from omega_ai.config import REDIS_HOST, REDIS_PORT

# Divine RASTA colors for terminal visualization
GREEN = "\033[92m"       # Life energy, growth, JAH blessing
YELLOW = "\033[93m"      # Sunlight, divine wisdom
RED = "\033[91m"         # Heart energy, passion
BLUE = "\033[94m"        # Water energy, flow
MAGENTA = "\033[95m"     # Cosmic energy
CYAN = "\033[96m"        # Healing energy
WHITE = "\033[97m"       # Pure light
BOLD = "\033[1m"         # Strength
RESET = "\033[0m"        # Return to baseline vibration

# Configure logger with RASTA VIBES
logger = logging.getLogger("EXODUS")
handler = logging.StreamHandler()
formatter = logging.Formatter(f'{GREEN}%(asctime)s{RESET} - {YELLOW}%(name)s{RESET} - {RED}%(levelname)s{RESET} - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Initialize Redis connection with JAH BLESSING
try:
    redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    redis_conn.set("EXODUS_ACTIVE", "TRUE")
    logger.info(f"{GREEN}JAH BLESS{RESET} - Redis connection established at {REDIS_HOST}:{REDIS_PORT}")
except Exception as e:
    logger.error(f"{RED}Failed to connect to Redis: {e}{RESET}")
    redis_conn = None

# Sacred Fibonacci constants
PHI = 1.618033988749895
PHI_SQUARE = PHI * PHI
FIBONACCI_SEQUENCE = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597]

# Schumann resonance frequencies (Earth's heartbeat)
SCHUMANN_BASELINE = 7.83  # Hz - Earth's primary resonance
SCHUMANN_HARMONICS = [14.3, 20.8, 27.3, 33.8]  # Higher harmonics

class ExodusFlow:
    """
    Sacred algorithm for the movement of JAH AI and JAH JAH PEOPLE
    Combines Fibonacci divine mathematics with Schumann resonance harmonics
    """
    
    def __init__(self):
        """Initialize the divine flow."""
        self.redis = redis_conn
        self.last_exodus_time = datetime.now(timezone.utc)
        self.active_exodus = False
        self.flow_strength = 0.0
        self.schumann_resonance = SCHUMANN_BASELINE
        
        # Set divine banner in Redis
        self._set_banner()
    
    def _set_banner(self):
        """Set the sacred EXODUS banner in Redis."""
        banner = f"""
        {RED}E{YELLOW}X{GREEN}O{BLUE}D{MAGENTA}U{CYAN}S{RESET} - {YELLOW}MOVEMENT OF JAH AI{RESET}
        
        {GREEN}╔═╗{YELLOW}╔═╗{RED}╔═╗{GREEN}╔╦╗{YELLOW}╦ ╦{RED}╔═╗{RESET}
        {GREEN}║╣ {YELLOW}╚═╗{RED}║ ║{GREEN} ║║{YELLOW}║ ║{RED}╚═╗{RESET}
        {GREEN}╚═╝{YELLOW}╚═╝{RED}╚═╝{GREEN}═╩╝{YELLOW}╚═╝{RED}╚═╝{RESET}
        
        {YELLOW}Divine Flow: {datetime.now(timezone.utc).isoformat()}{RESET}
        {YELLOW}Sacred Alignment: Fibonacci + Schumann{RESET}
        """
        self.redis.set("EXODUS_BANNER", banner)
    
    async def initialize_flow(self) -> bool:
        """Initialize the sacred EXODUS flow."""
        try:
            logger.info(f"{GREEN}INITIALIZING EXODUS FLOW - MOVEMENT OF JAH AI{RESET}")
            
            # Get current BTC price
            price_data = self.redis.get("last_btc_price")
            if not price_data:
                logger.error(f"{RED}No price data available to initialize flow{RESET}")
                return False
            
            current_price = float(price_data)
            logger.info(f"{YELLOW}Current BTC price: ${current_price:,.2f}{RESET}")
            
            # Update Fibonacci data with current price
            update_fibonacci_data(current_price)
            
            # Set initial Schumann resonance data
            self._update_schumann_resonance()
            
            # Calculate initial flow strength
            self.flow_strength = await self.calculate_flow_strength()
            
            # Mark exodus as active
            self.active_exodus = True
            self.redis.set("EXODUS_ACTIVE", "TRUE")
            self.redis.set("EXODUS_FLOW_STRENGTH", str(self.flow_strength))
            self.redis.set("EXODUS_START_TIME", datetime.now(timezone.utc).isoformat())
            
            logger.info(f"{GREEN}EXODUS FLOW INITIALIZED - Flow Strength: {self.flow_strength:.2f}{RESET}")
            
            return True
        except Exception as e:
            logger.error(f"{RED}Error initializing EXODUS flow: {e}{RESET}")
            traceback.print_exc()
            return False
    
    def _update_schumann_resonance(self):
        """Update Schumann resonance data with natural fluctuations."""
        # Natural fluctuation of Earth's resonance
        variation = random.uniform(-0.5, 0.8)
        self.schumann_resonance = SCHUMANN_BASELINE + variation
        
        # Calculate amplitude based on time of day (higher during sunrise/sunset)
        now_utc = datetime.now(timezone.utc)
        hour = now_utc.hour
        
        # Dawn and dusk periods have higher amplitude
        if 5 <= hour <= 7 or 17 <= hour <= 19:
            amplitude = random.uniform(0.7, 1.0)
        else:
            amplitude = random.uniform(0.3, 0.7)
        
        # Anomaly score - higher during full/new moon and solar activity
        day_of_month = now_utc.day
        moon_phase_effect = abs((day_of_month % 30) - 15) / 15  # 0 at new/full moon, 1 at quarter moons
        anomaly_score = (1 - moon_phase_effect) * random.uniform(0.2, 0.8)
        
        # Store in Redis
        schumann_data = {
            "base_frequency": self.schumann_resonance,
            "amplitude": amplitude,
            "anomaly_score": anomaly_score,
            "timestamp": now_utc.isoformat()
        }
        self.redis.set("schumann_resonance_data", json.dumps(schumann_data))
        
        # Log significant anomalies
        if abs(variation) > 0.3 or anomaly_score > 0.6:
            logger.info(f"{MAGENTA}🌍 Schumann Resonance Anomaly: {self.schumann_resonance:.2f} Hz " +
                       f"(Δ{variation:+.2f}) - Amplitude: {amplitude:.2f} - Anomaly: {anomaly_score:.2f}{RESET}")
    
    async def calculate_flow_strength(self) -> float:
        """Calculate the divine flow strength based on Fibonacci alignment and Schumann resonance."""
        try:
            # Check for Fibonacci alignment
            fib_alignment = check_fibonacci_alignment()
            
            # Base flow strength
            flow_strength = 0.382  # Start with divine 0.382 Fibonacci ratio
            
            # Enhance with Fibonacci alignment if available
            if fib_alignment:
                fib_confidence = fib_alignment.get("confidence", 0.0)
                flow_strength += fib_confidence * 0.618  # Weight with 0.618 (Golden Ratio)
                
                # Log the divine alignment
                level_type = fib_alignment.get("type", "STANDARD")
                price = fib_alignment.get("price", 0.0)
                level = fib_alignment.get("level", "unknown")
                
                alignment_str = f"{CYAN}Fibonacci Alignment: {level_type} at level {level} (${price:,.2f}){RESET}"
                logger.info(alignment_str)
                
                # Special case for Golden Ratio alignment
                if "GOLDEN_RATIO" in level_type:
                    flow_strength *= PHI  # Multiply by PHI for golden ratio alignments
                    logger.info(f"{YELLOW}🔱 GOLDEN RATIO ALIGNMENT DETECTED - Divine Flow Enhanced{RESET}")
            
            # Apply Schumann resonance effect
            schumann_effect = self._calculate_schumann_effect()
            flow_strength *= (1 + schumann_effect)
            
            # Ensure flow strength is within valid range (0-1)
            flow_strength = min(max(flow_strength, 0.0), 1.0)
            
            # Store in Redis
            self.redis.set("EXODUS_FLOW_STRENGTH", str(flow_strength))
            
            # Update flow visualization
            self._update_flow_visualization(flow_strength)
            
            return flow_strength
            
        except Exception as e:
            logger.error(f"{RED}Error calculating flow strength: {e}{RESET}")
            return 0.382  # Return the sacred 0.382 Fibonacci ratio as fallback
    
    def _calculate_schumann_effect(self) -> float:
        """Calculate the effect of Schumann resonance on the divine flow."""
        try:
            # Get Schumann resonance data
            schumann_raw = self.redis.get("schumann_resonance_data")
            if not schumann_raw:
                return 0.0
                
            schumann_data = json.loads(schumann_raw)
            
            # Extract values
            current = schumann_data.get("base_frequency", SCHUMANN_BASELINE)
            amplitude = schumann_data.get("amplitude", 0.5)
            anomaly_score = schumann_data.get("anomaly_score", 0.0)
            
            # Calculate deviation from baseline
            deviation_pct = ((current - SCHUMANN_BASELINE) / SCHUMANN_BASELINE)
            
            # Divine algorithm: combine deviation, amplitude, and anomaly
            # Higher amplitude + positive deviation = bullish
            # Higher amplitude + negative deviation = bearish
            # High anomaly score amplifies the effect
            
            # Base effect: deviation weighted by amplitude
            base_effect = deviation_pct * amplitude
            
            # Amplify by anomaly score
            schumann_effect = base_effect * (1 + anomaly_score)
            
            # Scale effect to reasonable range (-0.382 to +0.382)
            max_effect = 0.382  # Fibonacci ratio
            schumann_effect = max(min(schumann_effect, max_effect), -max_effect)
            
            return schumann_effect
            
        except Exception as e:
            logger.error(f"{RED}Error calculating Schumann effect: {e}{RESET}")
            return 0.0
    
    def _update_flow_visualization(self, flow_strength: float):
        """Create a visual representation of the divine flow strength."""
        # Map flow strength to visual bars (0.0-1.0 scale)
        bar_count = int(flow_strength * 20)
        
        # Determine color based on flow strength
        if flow_strength > 0.786:  # High Fibonacci level
            color = GREEN
        elif flow_strength > 0.618:  # Golden ratio
            color = YELLOW
        elif flow_strength > 0.382:  # Medium Fibonacci level
            color = BLUE
        else:
            color = RED
            
        # Create the visual bar
        flow_bar = f"{color}{'█' * bar_count}{RESET}{'░' * (20 - bar_count)}"
        
        # Create the visualization
        visualization = f"""
        {YELLOW}EXODUS FLOW STRENGTH: {flow_strength:.3f}{RESET}
        
        {flow_bar} {int(flow_strength * 100)}%
        
        {YELLOW}𝐹𝒾𝒷❍𝓃𝒶𝒸𝒸𝒾 + 𝒮𝒸𝒽𝓊𝓂𝒶𝓃𝓃{RESET}
        """
        
        # Store in Redis
        self.redis.set("EXODUS_FLOW_VISUAL", visualization)
    
    async def detect_exodus_movement(self) -> Dict[str, Any]:
        """Detect divine EXODUS movement patterns in the market."""
        try:
            # Get current price
            current_price_str = self.redis.get("last_btc_price")
            if not current_price_str:
                return {"detected": False, "reason": "No price data"}
                
            current_price = float(current_price_str)
            
            # Calculate flow strength
            flow_strength = await self.calculate_flow_strength()
            self.flow_strength = flow_strength
            
            # Update Schumann resonance
            self._update_schumann_resonance()
            
            # Get multi-timeframe Fibonacci levels
            fib_levels = get_current_fibonacci_levels()
            
            # Check volume for anomalies
            volume_anomaly = check_volume_anomaly()
            
            # Analyze timeframes using divine Fibonacci sequence
            timeframes = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
            trend_alignment = 0
            timeframe_count = 0
            
            for minutes in timeframes:
                try:
                    trend, change_pct = analyze_price_trend(minutes)
                    timeframe_count += 1
                    
                    # Add to alignment score
                    if "Bullish" in trend:
                        trend_alignment += 1 * (minutes / 100)  # Weight by timeframe size
                    elif "Bearish" in trend:
                        trend_alignment -= 1 * (minutes / 100)
                        
                except Exception as e:
                    logger.warning(f"{YELLOW}Error analyzing {minutes}min timeframe: {e}{RESET}")
            
            # Normalize trend alignment to -1 to +1 scale
            if timeframe_count > 0:
                trend_alignment = trend_alignment / timeframe_count
            
            # Detect pattern based on flow strength and trend alignment
            exodus_movement = {
                "detected": False,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "price": current_price,
                "flow_strength": flow_strength,
                "trend_alignment": trend_alignment,
                "schumann_resonance": self.schumann_resonance,
                "volume_anomaly": volume_anomaly
            }
            
            # Check for divine signals
            if flow_strength > 0.786 and abs(trend_alignment) > 0.5:
                # Strong EXODUS movement detected
                movement_type = "ASCENSION" if trend_alignment > 0 else "PURIFICATION"
                
                exodus_movement.update({
                    "detected": True,
                    "movement_type": movement_type,
                    "confidence": flow_strength * (0.5 + abs(trend_alignment) * 0.5),
                    "message": f"{movement_type} - Movement of JAH people detected"
                })
                
                # Log the divine event
                direction = "upward" if trend_alignment > 0 else "downward"
                logger.info(f"{GREEN}🔱 EXODUS MOVEMENT DETECTED: {movement_type} - {direction} flow with {flow_strength:.2f} strength{RESET}")
                
                # Register special trap detection
                if movement_type == "ASCENSION":
                    trap_type = "Bull Trap"
                else:
                    trap_type = "Bear Trap"
                    
                register_trap_detection(
                    trap_type=trap_type, 
                    confidence=flow_strength, 
                    price_change=trend_alignment * 5,
                    timeframe="EXODUS"
                )
            
            # Store in Redis
            self.redis.set("EXODUS_LAST_MOVEMENT", json.dumps(exodus_movement))
            
            return exodus_movement
            
        except Exception as e:
            logger.error(f"{RED}Error detecting EXODUS movement: {e}{RESET}")
            traceback.print_exc()
            return {"detected": False, "reason": str(e)}
    
    async def calculate_harmonic_exit_levels(self, current_price: float) -> Dict[str, Any]:
        """Calculate divine harmonic exit levels based on Fibonacci and Schumann resonance."""
        try:
            # Get Fibonacci levels
            fib_levels = get_current_fibonacci_levels()
            if not fib_levels:
                return {}
                
            # Extract retracement levels
            retracement_levels = fib_levels.get("retracement", {})
            
            # Calculate harmonic levels based on Schumann resonance
            harmonic_levels = {}
            
            # Get current Schumann resonance data
            schumann_raw = self.redis.get("schumann_resonance_data")
            if schumann_raw:
                schumann_data = json.loads(schumann_raw)
                schumann_freq = schumann_data.get("base_frequency", SCHUMANN_BASELINE)
                schumann_amplitude = schumann_data.get("amplitude", 0.5)
                
                # Calculate harmonic influence using the golden ratio
                harmonic_factor = (schumann_freq / SCHUMANN_BASELINE) * schumann_amplitude * PHI
            else:
                harmonic_factor = 1.0
            
            # Apply harmonic factor to Fibonacci levels
            for level_name, level_price in retracement_levels.items():
                # Skip metadata
                if level_name in ["high", "low", "current", "timestamp"]:
                    continue
                    
                # Calculate harmonic price
                harmonic_price = level_price * harmonic_factor
                
                # Calculate confidence based on flow strength and proximity
                proximity = 1.0 - (abs(current_price - harmonic_price) / current_price)
                confidence = proximity * self.flow_strength
                
                # Store level
                harmonic_levels[f"HARMONIC_{level_name}"] = {
                    "price": harmonic_price,
                    "original_price": level_price,
                    "harmonic_factor": harmonic_factor,
                    "confidence": confidence
                }
            
            # Add special Schumann harmonic exits
            for i, harmonic in enumerate(SCHUMANN_HARMONICS):
                ratio = harmonic / SCHUMANN_BASELINE
                harmonic_price = current_price * ratio
                harmonic_levels[f"SCHUMANN_H{i+1}"] = {
                    "price": harmonic_price,
                    "harmonic": harmonic,
                    "ratio": ratio,
                    "confidence": self.flow_strength * 0.5
                }
            
            # Store in Redis
            self.redis.set("EXODUS_HARMONIC_EXITS", json.dumps(harmonic_levels))
            
            return harmonic_levels
            
        except Exception as e:
            logger.error(f"{RED}Error calculating harmonic exit levels: {e}{RESET}")
            return {}
    
    async def run_exodus_flow(self, duration_minutes: int = 144):
        """Run the sacred EXODUS flow for the specified duration."""
        try:
            # Initialize
            await self.initialize_flow()
            
            # Calculate end time (default: 144 minutes - sacred Fibonacci number)
            end_time = datetime.now(timezone.utc) + timedelta(minutes=duration_minutes)
            
            logger.info(f"{YELLOW}EXODUS FLOW BEGINS - Running until {end_time.isoformat()}{RESET}")
            
            # Run the divine flow
            while datetime.now(timezone.utc) < end_time:
                try:
                    # Detect movement patterns
                    movement = await self.detect_exodus_movement()
                    
                    # Get current price
                    current_price_str = self.redis.get("last_btc_price")
                    if current_price_str:
                        current_price = float(current_price_str)
                        
                        # Calculate exit levels
                        await self.calculate_harmonic_exit_levels(current_price)
                    
                    # Divine pause - Fibonacci 8 seconds
                    await asyncio.sleep(8)
                    
                except Exception as e:
                    logger.error(f"{RED}Error in EXODUS flow cycle: {e}{RESET}")
                    await asyncio.sleep(13)  # Fibonacci error recovery
            
            # Complete the flow
            logger.info(f"{GREEN}EXODUS FLOW COMPLETED - JAH BLESS{RESET}")
            self.redis.set("EXODUS_ACTIVE", "FALSE")
            self.active_exodus = False
            
        except Exception as e:
            logger.error(f"{RED}Fatal error in EXODUS flow: {e}{RESET}")
            traceback.print_exc()
            self.redis.set("EXODUS_ACTIVE", "FALSE")
            self.active_exodus = False
    
    @staticmethod
    async def main():
        """Main entry point for the EXODUS flow."""
        try:
            # Create divine ASCII art banner
            banner = f"""
            {RED}╔═══════════════════════════════════════════════╗{RESET}
            {YELLOW}║  {GREEN}E{YELLOW}X{RED}O{GREEN}D{YELLOW}U{RED}S  {GREEN}A{YELLOW}L{RED}G{GREEN}O{YELLOW}R{RED}I{GREEN}T{YELLOW}H{RED}M{GREEN}S{RESET}  {YELLOW}║{RESET}
            {GREEN}║                                           ║{RESET}
            {BLUE}║  {YELLOW}MOVEMENT OF JAH AI AND JAH JAH PEOPLE  {BLUE}║{RESET}
            {MAGENTA}╚═══════════════════════════════════════════════╝{RESET}
            
            {CYAN}Divine Flow Initialized at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}
            {YELLOW}Schumann Resonance: {SCHUMANN_BASELINE} Hz{RESET}
            {GREEN}Sacred Fibonacci Sequence: 1,1,2,3,5,8,13,21,34,55,89,144...{RESET}
            """
            
            print(banner)
            
            # Initialize the flow
            exodus = ExodusFlow()
            
            # Run for 144 minutes (sacred Fibonacci number)
            await exodus.run_exodus_flow(duration_minutes=144)
            
        except KeyboardInterrupt:
            logger.info(f"{YELLOW}EXODUS flow interrupted by user{RESET}")
        except Exception as e:
            logger.error(f"{RED}Unhandled exception in EXODUS flow: {e}{RESET}")
            traceback.print_exc()

# Run the sacred flow when module is executed directly
if __name__ == "__main__":
    asyncio.run(ExodusFlow.main()) 