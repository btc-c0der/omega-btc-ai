"""
Redis Manager for OMEGA BTC AI.
Handles all Redis operations for price data and market analysis.
"""

import redis
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
from deployment.digitalocean.logging.omega_logger import OmegaLogger

class RedisManager:
    """Redis manager for OMEGA BTC AI."""
    
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        """Initialize Redis connection."""
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.logger = OmegaLogger(log_dir="logs/redis_manager")
        
        # Keys for different data types
        self.price_history_key = "btc:price:history"
        self.current_price_key = "btc:price:current"
        self.analysis_key = "btc:analysis:latest"
        
    def get_price_history(self, minutes: int = 60) -> List[Dict[str, Any]]:
        """Get BTC price history for the specified duration."""
        try:
            # Get raw data from Redis
            raw_history = self.redis.lrange(self.price_history_key, 0, minutes - 1)
            
            # Parse JSON data
            history = []
            for item in raw_history:
                try:
                    data = json.loads(item)
                    history.append(data)
                except json.JSONDecodeError as e:
                    self.logger.log_error(e, context={"item": item})
                    continue
            
            return history
            
        except Exception as e:
            self.logger.log_error(e, context={"minutes": minutes})
            return []
    
    def get_current_price(self) -> float:
        """Get current BTC price."""
        try:
            price_str = self.redis.get(self.current_price_key)
            if price_str is None:
                return 0.0
            return float(price_str)
        except Exception as e:
            self.logger.log_error(e)
            return 0.0
    
    def save_price(self, price: float, timestamp: Optional[datetime] = None) -> bool:
        """Save new price data to Redis."""
        if timestamp is None:
            timestamp = datetime.now(timezone.utc)
        
        try:
            # Create price data
            price_data = {
                "price": price,
                "timestamp": timestamp.isoformat()
            }
            
            # Save to Redis
            self.redis.set(self.current_price_key, str(price))
            self.redis.lpush(self.price_history_key, json.dumps(price_data))
            
            # Trim history to keep last 24 hours (1440 minutes)
            self.redis.ltrim(self.price_history_key, 0, 1439)
            
            return True
            
        except Exception as e:
            self.logger.log_error(e, context={"price": price})
            return False
    
    def save_analysis(self, analysis: Dict[str, Any]) -> bool:
        """Save market analysis results."""
        try:
            self.redis.set(self.analysis_key, json.dumps(analysis))
            return True
        except Exception as e:
            self.logger.log_error(e, context={"analysis": analysis})
            return False
    
    def get_analysis(self) -> Dict[str, Any]:
        """Get latest market analysis results."""
        try:
            analysis_str = self.redis.get(self.analysis_key)
            if analysis_str is None:
                return {}
            return json.loads(analysis_str)
        except Exception as e:
            self.logger.log_error(e)
            return {}
    
    def clear_data(self) -> bool:
        """Clear all data (for testing purposes)."""
        try:
            self.redis.delete(self.price_history_key)
            self.redis.delete(self.current_price_key)
            self.redis.delete(self.analysis_key)
            return True
        except Exception as e:
            self.logger.log_error(e)
            return False 