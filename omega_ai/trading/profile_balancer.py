class ProfileBalancer:
    """Dynamically balance between trading profiles based on performance."""
    
    def __init__(self, redis_client=None, 
                 initial_scalper_coef=0.3, 
                 initial_strategic_coef=0.6, 
                 initial_aggressive_coef=0.1,
                 adaptation_speed=0.1):
        """Initialize the profile balancer."""
        self.redis_client = redis_client or redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.scalper_coefficient = initial_scalper_coef
        self.strategic_coefficient = initial_strategic_coef
        self.aggressive_coefficient = initial_aggressive_coef
        self.adaptation_speed = adaptation_speed
        
        # Performance tracking
        self.performance = {
            'scalper': [],  # List of (trade_result, pnl) tuples
            'strategic': [],
            'aggressive': []
        }
        
        # Logger setup
        self.logger = logging.getLogger('profile_balancer')
        
        # Store initial coefficients in Redis
        self._update_coefficients_in_redis()
    
    def track_trade_result(self, trade_result):
        """Track the result of a trade and adjust profile coefficients."""
        pnl = trade_result.get('pnl', 0)
        duration = trade_result.get('duration', 0)  # In seconds
        entry_reason = trade_result.get('entry_reason', '')
        exit_reason = trade_result.get('exit_reason', '')
        
        # Determine which profile this trade most closely followed
        profile_type = self._categorize_trade(duration, entry_reason, exit_reason)
        
        # Record result
        self.performance[profile_type].append((trade_result, pnl))
        
        # Adjust coefficients based on recent performance
        self._adjust_coefficients()
        
        # Update coefficients in Redis
        self._update_coefficients_in_redis()
        
        self.logger.info(f"Trade tracked: {profile_type}, PnL: {pnl}, " 
                        f"New coefficients: S={self.scalper_coefficient:.2f}, "
                        f"ST={self.strategic_coefficient:.2f}, "
                        f"A={self.aggressive_coefficient:.2f}")
    
    def _categorize_trade(self, duration, entry_reason, exit_reason):
        """Categorize a trade as scalper, strategic, or aggressive."""
        # Scalper trades are short duration
        if duration < 3600:  # Less than 1 hour
            return 'scalper'
            
        # Aggressive trades have specific entry/exit patterns
        if 'momentum' in entry_reason.lower() or 'breakout' in entry_reason.lower():
            return 'aggressive'
            
        # Check for strategic patterns
        if 'fibonacci' in entry_reason.lower() or 'trap' in entry_reason.lower():
            return 'strategic'
            
        # Default to strategic for longer trades
        if duration > 86400:  # More than 24 hours
            return 'strategic'
            
        # Default
        return 'strategic'
    
    def _adjust_coefficients(self):
        """Adjust profile coefficients based on recent performance."""
        # Calculate average PnL for each profile (last 20 trades)
        avg_pnl = {}
        for profile in self.performance:
            trades = self.performance[profile][-20:]
            if trades:
                total_pnl = sum(pnl for _, pnl in trades)
                avg_pnl[profile] = total_pnl / len(trades)
            else:
                avg_pnl[profile] = 0
                
        # Calculate total positive PnL
        total_positive_pnl = sum(max(0, pnl) for pnl in avg_pnl.values())
        
        if total_positive_pnl > 0:
            # Calculate target coefficients based on performance
            target_scalper = max(0.1, min(0.8, (avg_pnl['scalper'] / total_positive_pnl) * 0.9))
            target_strategic = max(0.1, min(0.8, (avg_pnl['strategic'] / total_positive_pnl) * 0.9))
            target_aggressive = max(0.1, min(0.8, (avg_pnl['aggressive'] / total_positive_pnl) * 0.9))
            
            # Normalize to ensure sum = 1.0
            total = target_scalper + target_strategic + target_aggressive
            target_scalper /= total
            target_strategic /= total
            target_aggressive /= total
            
            # Gradual adjustment toward target (controlled by adaptation_speed)
            self.scalper_coefficient += self.adaptation_speed * (target_scalper - self.scalper_coefficient)
            self.strategic_coefficient += self.adaptation_speed * (target_strategic - self.strategic_coefficient)
            self.aggressive_coefficient += self.adaptation_speed * (target_aggressive - self.aggressive_coefficient)
            
            # Ensure coefficients sum to 1.0
            total = self.scalper_coefficient + self.strategic_coefficient + self.aggressive_coefficient
            self.scalper_coefficient /= total
            self.strategic_coefficient /= total
            self.aggressive_coefficient /= total
    
    def get_current_blend(self):
        """Get current blend coefficients."""
        return {
            'scalper': self.scalper_coefficient,
            'strategic': self.strategic_coefficient,
            'aggressive': self.aggressive_coefficient
        }
    
    def _update_coefficients_in_redis(self):
        """Store current coefficients in Redis for UI and monitoring."""
        try:
            coefficients = self.get_current_blend()
            self.redis_client.set('profile_coefficients', json.dumps(coefficients))
        except Exception as e:
            self.logger.error(f"Error updating coefficients in Redis: {e}")