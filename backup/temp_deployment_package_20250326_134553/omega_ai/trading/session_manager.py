
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

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import datetime
import logging
from omega_ai.utils.redis_manager import RedisManager

@dataclass
class SessionState:
    day_counter: int = 1
    session_counter: int = 0
    price_history: List[float] = field(default_factory=list)
    start_time: datetime.datetime = field(default_factory=lambda: datetime.datetime.now())

class TradingSessionManager:
    def __init__(self, redis_manager: RedisManager):
        self.redis = redis_manager
        self.state = SessionState()
        
    def update_battle_state(self, traders: Dict, current_price: float) -> bool:
        """Update battle state in Redis"""
        battle_state = {
            "day": self.state.day_counter,
            "session": self.state.session_counter % 4 + 1,
            "btc_price": current_price,
            "btc_history": self.state.price_history[-100:],
            "battle_active": True,
            "start_time": self.state.start_time.isoformat()
        }
        
        return self.redis.set_with_validation("omega:battle_state", battle_state)
        
    def advance_session(self) -> None:
        """Advance to next trading session"""
        self.state.session_counter += 1
        if self.state.session_counter % 4 == 0:
            self.state.day_counter += 1
            
    def update_price_history(self, price: float) -> None:
        """Update price history with length limit"""
        self.state.price_history.append(price)
        if len(self.state.price_history) > 1000:
            self.state.price_history = self.state.price_history[-1000:]
    
    def check_trading_status(self) -> bool:
        """Check if trading should be active"""
        try:
            value = self.redis.get_cached("omega:start_trading")
            return value == "1" if value is not None else False
        except Exception as e:
            logging.error(f"Error checking trading status: {e}")
            return False