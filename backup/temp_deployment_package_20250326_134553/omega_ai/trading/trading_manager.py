
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

from typing import Dict, List
import datetime
from dataclasses import dataclass
from ..utils.redis_manager import RedisManager
from ..mm_trap_detector.high_frequency_detector import check_high_frequency_mode

@dataclass
class FibonacciCheckpoint:
    session: int
    day: int
    type: str
    energy_level: float

class TradingManager:
    def __init__(self, redis_manager: RedisManager):
        self.redis = redis_manager
        self.fibonacci_sequence = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        self.checkpoints: List[FibonacciCheckpoint] = []
        
    def validate_profile_parameters(self, profile: str, capital: float) -> bool:
        """Validate trading profile parameters"""
        valid_profiles = ["strategic", "aggressive", "newbie", "scalper"]
        
        if profile not in valid_profiles:
            print(f"❌ Invalid profile: {profile}")
            return False
            
        if capital <= 0:
            print("❌ Capital must be positive")
            return False
            
        return True
    
    def is_fibonacci_checkpoint(self, session: int, day: int) -> bool:
        """Check if current session/day is a Fibonacci checkpoint"""
        total_sessions = (day - 1) * 4 + session
        return total_sessions in self.fibonacci_sequence
    
    def calculate_energy_state(self, trader_data: Dict) -> float:
        """Calculate trader's energy state based on performance and psychology"""
        if not trader_data:
            return 1.0
            
        # Base energy from win rate and confidence
        base_energy = (
            trader_data.get("win_rate", 0.5) * 0.5 + 
            trader_data.get("confidence", 0.5) * 0.5
        )
        
        # Adjust for emotional state
        emotional_multiplier = {
            "calm": 1.0,
            "confident": 1.1,
            "fearful": 0.8,
            "greedy": 0.7
        }.get(trader_data.get("emotional_state", "calm"), 1.0)
        
        return base_energy * emotional_multiplier
    
    def update_checkpoints(self, session: int, day: int, trader_data: Dict):
        """Update Fibonacci checkpoints with trader state"""
        if self.is_fibonacci_checkpoint(session, day):
            energy = self.calculate_energy_state(trader_data)
            
            checkpoint = FibonacciCheckpoint(
                session=session,
                day=day,
                type="fibonacci_alignment",
                energy_level=energy
            )
            
            self.checkpoints.append(checkpoint)
            
            # Check for market maker traps
            hf_mode, _ = check_high_frequency_mode()
            if hf_mode:
                print(f"⚠️ Market Maker activity detected at Fibonacci checkpoint!")
                print(f"   Energy Level: {energy:.2f}")