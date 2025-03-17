from dataclasses import dataclass, field
from typing import Dict, List, Optional
import datetime
import logging
from omega_ai.utils.redis_connection import RedisConnectionManager

@dataclass
class SessionState:
    day_counter: int = 1
    session_counter: int = 0
    price_history: List[float] = field(default_factory=list)
    start_time: datetime.datetime = field(default_factory=lambda: datetime.datetime.now())

class TradingSessionManager:
    def __init__(self, redis_manager: RedisConnectionManager):
        self.redis = redis_manager
        self.state = SessionState()
        
    def update_battle_state(self, traders: Dict, current_price: float):
        """Update battle state in Redis"""
        battle_state = {
            "day": self.state.day_counter,
            "session": self.state.session_counter % 4 + 1,
            "btc_price": current_price,
            "btc_history": self.state.price_history[-100:],
            "battle_active": True,
            "start_time": self.state.start_time.isoformat()
        }
        
        return self.redis.set("omega:live_battle_state", battle_state)
        
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
            return self.redis.get("omega:start_trading") == "1"
        except Exception as e:
            logging.error(f"Error checking trading status: {e}")
            return False