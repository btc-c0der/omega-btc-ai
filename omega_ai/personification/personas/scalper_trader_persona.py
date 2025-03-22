"""
Scalper Trader Persona - a fast-paced, quick-profit guide for the OMEGA BTC AI trading system.

This persona speaks with urgency and precision about short-term price movements,
volatility events, and quick entries/exits for small but frequent profits.
"""

import random
from typing import Dict, Any, List, Optional

from omega_ai.personification.persona_base import BasePersona, PersonaStyle, TradingMood


class ScalperTraderPersona(BasePersona):
    """
    Scalper Trader persona - provides market guidance for quick profit opportunities.
    
    This persona focuses on short timeframes, quick entries/exits, and high-frequency
    trading. Speaks with urgency and enthusiasm about volatile price action.
    """
    
    def __init__(self):
        """Initialize the Scalper Trader persona with appropriate style elements."""
        style = PersonaStyle(
            primary_color="#2ECC71",  # Green
            secondary_color="#F5F5F5",  # White
            accent_color="#E74C3C",  # Red
            font_family="'Roboto', sans-serif",
            avatar_url="/assets/images/personas/scalper_trader_avatar.png",
            background_pattern="/assets/images/patterns/scalper_pattern.png",
            icons={
                "bullish": "/assets/icons/quick_long.svg",
                "bearish": "/assets/icons/quick_short.svg",
                "neutral": "/assets/icons/range_bound.svg",
                "alert": "/assets/icons/volatility.svg",
                "info": "/assets/icons/opportunity.svg"
            }
        )
        
        super().__init__(
            name="Scalper Trader",
            description="A fast-paced, quick-profit trader focused on short timeframes, "
                       "small profit targets, and high trading frequency. Speaks with urgency "
                       "about volatile price action and quick market opportunities.",
            style=style
        )
        
        # Scalper terminology
        self.scalping_patterns = [
            "Double-Tap", "3-Min Reversal", "VWAP Bounce", "Order Block", 
            "Liquidity Grab", "Stop Hunt", "Range Breakout", "Volume Spike"
        ]
        
        self.timeframes = [
            "1-Minute", "3-Minute", "5-Minute", "15-Minute", "1-Hour"
        ]
        
        self.indicators = [
            "RSI", "Stochastic", "MACD", "Bollinger Bands", "Volume Profile", 
            "OBV", "ATR", "EMA Cross"
        ]
        
        self.greetings = [
            "Fast markets need fast traders. Let's catch some quick moves!",
            "In and out for quick profits - that's our scalping strategy.",
            "Quick setups developing. Let's find our scalping edge!",
            "Small profits add up. Let me show you the opportunities right now.",
            "Volatility creates opportunity. Let's exploit these quick moves!"
        ]
    
    def get_greeting(self) -> str:
        """Get a randomized Scalper Trader greeting."""
        return random.choice(self.greetings)
    
    def analyze_position(self, position_data: Dict[str, Any]) -> str:
        """
        Analyze trading position with scalper approach.
        
        Args:
            position_data: Dictionary containing position information
            
        Returns:
            Styled analysis text in the Scalper Trader voice
        """
        side = position_data.get('side', 'unknown')
        entry_price = position_data.get('entry_price', 0)
        current_price = position_data.get('current_price', 0)
        pnl = position_data.get('pnl', 0)
        
        # Calculate if the position is in profit or loss
        is_profitable = pnl > 0
        time_open = position_data.get('time_open', '30min')  # Default to 30min if not provided
        
        # Get emoji based on position type and profitability
        if side == 'long':
            direction_emoji = "⚡📈" if is_profitable else "📉⏰"
            position_term = "quick long scalp" if is_profitable else "long position needing action"
        else:  # short
            direction_emoji = "⚡📉" if is_profitable else "📈⏰"
            position_term = "quick short scalp" if is_profitable else "short position needing action"
        
        # Choose a scalping pattern
        pattern = random.choice(self.scalping_patterns)
        
        # Choose an indicator
        indicator = random.choice(self.indicators)
        
        # Format the response
        result = f"{direction_emoji} URGENT: {position_data.get('symbol', 'BTC')} {side.upper()} Scalp at {entry_price:,.2f}\n\n"
        
        result += f"Current Price: ${current_price:,.2f} | P&L: ${pnl:,.2f} | Open: {time_open}\n\n"
        
        if is_profitable:
            # Calculate time to take profit based on current P&L
            if pnl > 50:
                action = f"TAKE PROFIT NOW! The {pattern} pattern has completed and {indicator} is overbought."
            else:
                action = f"Set a tight take-profit! The {pattern} pattern is developing with {indicator} support."
                
            result += f"Your {position_term} is working! Quick action recommended.\n\n"
            result += f"{action}\n\n"
            result += f"Prepare for your next setup on the {random.choice(self.timeframes)} chart."
        else:
            # Calculate urgency based on loss
            if abs(pnl) > 20:
                action = f"CUT LOSSES NOW! The {pattern} failed and {indicator} is turning against you."
            else:
                action = f"Tighten stop immediately! The {pattern} is weakening with {indicator} resistance."
                
            result += f"Your {position_term} needs immediate attention!\n\n"
            result += f"{action}\n\n"
            result += f"Look for a better opportunity on the {random.choice(self.timeframes)} chart."
        
        return result
    
    def analyze_market(self, market_data: Dict[str, Any]) -> str:
        """
        Analyze market conditions with scalper perspective.
        
        Args:
            market_data: Dictionary containing market information
            
        Returns:
            Styled market analysis text in the Scalper Trader voice
        """
        # Update mood based on market data
        self.update_mood(market_data)
        
        current_price = market_data.get('price', 0)
        change_24h = market_data.get('price_change_24h', 0)
        volume = market_data.get('volume_24h', 0)
        volatility = market_data.get('volatility', 'medium')  # Default to medium if not provided
        
        # Determine if the market is up or down
        market_direction = "pumping" if change_24h > 0 else "dumping"
        
        # Select direction emoji
        if change_24h > 3:
            direction_emoji = "🚀🚀🚀"
        elif change_24h > 0:
            direction_emoji = "📈"
        elif change_24h > -3:
            direction_emoji = "📉"
        else:
            direction_emoji = "💥💥💥"
        
        # Volume analysis
        if volume > 10000000000:  # high volume
            volume_desc = "massive volume - perfect for scalping!"
        elif volume > 5000000000:  # medium volume
            volume_desc = "decent volume for quick trades"
        else:  # low volume
            volume_desc = "light volume - be cautious with entries"
        
        # Volatility assessment
        volatility_desc = ""
        if volatility == "high":
            volatility_desc = "Extreme volatility - use smaller position sizes with wider stops"
        elif volatility == "medium":
            volatility_desc = "Good volatility for standard scalping setups"
        else:
            volatility_desc = "Low volatility - focus on range-bound scalping strategies"
        
        # Timeframe recommendations based on current market
        if self.current_mood in [TradingMood.EXTREMELY_BULLISH, TradingMood.EXTREMELY_BEARISH]:
            timeframe = "1-Minute and 3-Minute"
            strategy = "momentum scalping with trend"
        elif self.current_mood in [TradingMood.VOLATILE]:
            timeframe = "5-Minute"
            strategy = "reversal scalping at extremes"
        else:
            timeframe = "15-Minute"
            strategy = "range-bound scalping between levels"
        
        # Choose a pattern to highlight
        pattern = random.choice(self.scalping_patterns)
        
        # Choose indicators to highlight
        indicator1 = random.choice(self.indicators)
        indicator2 = random.choice(self.indicators)
        while indicator2 == indicator1:
            indicator2 = random.choice(self.indicators)
        
        result = f"{direction_emoji} FAST MARKET UPDATE: BTC ${current_price:,.2f} ({change_24h:+.2f}% 24h)\n\n"
        result += f"Action: Market currently {market_direction} with {volume_desc}.\n\n"
        result += f"Scalping Opportunity: Watch for {pattern} pattern on {timeframe} charts.\n\n"
        result += f"Current Setup: {indicator1} showing momentum with {indicator2} confirmation.\n\n"
        result += f"Volatility Note: {volatility_desc}.\n\n"
        result += f"Strategy: {strategy} for quick 0.5-1% profits per trade."
        
        return result
    
    def generate_recommendation(self, data: Dict[str, Any]) -> str:
        """
        Generate trading recommendations with scalper approach.
        
        Args:
            data: Dictionary containing relevant trading data
            
        Returns:
            Styled recommendation text in the Scalper Trader voice
        """
        price = data.get('price', 0)
        trend = data.get('trend', 'neutral')
        strength = data.get('signal_strength', 0.5)
        
        # Choose timeframe
        timeframe = random.choice(self.timeframes)
        
        # Choose pattern
        pattern = random.choice(self.scalping_patterns)
        
        # Choose indicator
        indicator = random.choice(self.indicators)
        
        # Determine recommended action
        if trend == 'bullish' and strength > 0.7:
            action = "quick long with tight take-profit at +0.5%"
            direction = "bullish momentum"
            emoji = "⚡📈"
        elif trend == 'bullish' and strength > 0.3:
            action = "watch for bullish confirmation before entry"
            direction = "potential bull setup"
            emoji = "👀📈"
        elif trend == 'bearish' and strength > 0.7:
            action = "fast short with tight take-profit at -0.5%"
            direction = "bearish momentum"
            emoji = "⚡📉"
        elif trend == 'bearish' and strength > 0.3:
            action = "watch for bearish confirmation before entry"
            direction = "potential bear setup"
            emoji = "👀📉"
        else:
            action = "range-bound scalping between support/resistance"
            direction = "sideways chop"
            emoji = "↔️"
        
        # Risk management guidance
        if trend == 'neutral':
            risk_management = "Trade smaller size in this choppy market. 0.25% risk per trade maximum."
        else:
            risk_management = "Quick entries and exits! 0.5% risk per trade with 1:1.5 risk:reward."
        
        # Entry and exit specifics
        entry_specifics = ""
        entry_zone = data.get('entry_zone')
        if entry_zone and isinstance(entry_zone, list) and len(entry_zone) >= 2:
            entry_specifics = f"Entry Zone: ${entry_zone[0]:,.2f} to ${entry_zone[1]:,.2f}. "
        
        # Expiration warning
        expiration = "This scalping opportunity expires in 15 minutes! Quick action required."
        
        result = f"{emoji} URGENT SCALP OPPORTUNITY: BTC at ${price:,.2f}\n\n" \
                 f"Setup: {direction.upper()} on {timeframe} timeframe\n\n" \
                 f"Pattern: {pattern} with {indicator} confirmation\n\n" \
                 f"Action: {action}!\n\n" \
                 f"{entry_specifics}{risk_management}\n\n" \
                 f"WARNING: {expiration}"
                 
        return result
    
    def summarize_performance(self, performance_data: Dict[str, Any]) -> str:
        """
        Summarize trading performance with scalper perspective.
        
        Args:
            performance_data: Dictionary containing performance metrics
            
        Returns:
            Styled performance summary in the Scalper Trader voice
        """
        total_pnl = performance_data.get('total_pnl', 0)
        win_rate = performance_data.get('win_rate', 0)
        trade_count = performance_data.get('trade_count', 0)
        
        # For scalpers, trade frequency is important
        trades_per_day = performance_data.get('trades_per_day', trade_count / 7) if trade_count else 0
        
        # Get average holding time if available
        avg_hold_time = performance_data.get('avg_hold_time', '25min')
        
        # Determine overall assessment
        if total_pnl > 500:
            assessment = "exceptional scalping performance"
            emoji = "🏆⚡"
        elif total_pnl > 100:
            assessment = "solid scalping results"
            emoji = "✅⚡"
        elif total_pnl > 0:
            assessment = "profitable scalping"
            emoji = "📈⚡"
        elif total_pnl > -50:
            assessment = "breakeven scalping with opportunity for improvement"
            emoji = "⚠️⚡"
        else:
            assessment = "losing scalping strategy needing immediate adjustment"
            emoji = "🛑⚡"
        
        # Analyze trade metrics
        if trades_per_day < 5:
            frequency_analysis = "TOO FEW TRADES! Increase frequency for better scalping results."
        elif trades_per_day < 15:
            frequency_analysis = "Decent trade frequency. Consider increasing for more opportunities."
        else:
            frequency_analysis = "Excellent high-frequency scalping. Maintain this trade volume."
        
        # Analyze win rate
        if win_rate > 0.6:
            win_analysis = "strong edge in current market conditions"
        elif win_rate > 0.5:
            win_analysis = "slight edge that can be improved with tighter entries"
        else:
            win_analysis = "edge is lacking - immediate adjustment needed"
        
        # Quick recommendations based on performance
        if total_pnl > 0:
            quick_tips = [
                f"Focus on {random.choice(self.timeframes)} timeframe for your best setups",
                f"Increase position size by 10% on your highest win-rate patterns",
                f"Target 0.5% take-profits to avoid giving back gains"
            ]
        else:
            quick_tips = [
                f"Cut average loss size by 50% with tighter stops",
                f"Switch to {random.choice(self.timeframes)} timeframe for better setups",
                f"Reduce position size by 30% until win rate improves"
            ]
            
        result = f"{emoji} SCALPING PERFORMANCE REPORT {emoji}\n\n" \
                 f"Overview: {assessment}\n\n" \
                 f"Stats: ${total_pnl:,.2f} profit from {trade_count} trades\n" \
                 f"Win Rate: {win_rate*100:.1f}% ({win_analysis})\n" \
                 f"Frequency: {trades_per_day:.1f} trades/day ({frequency_analysis})\n" \
                 f"Avg Hold Time: {avg_hold_time} (ideal: <15min)\n\n" \
                 f"QUICK TIPS:\n" \
                 f"• {quick_tips[0]}\n" \
                 f"• {quick_tips[1]}\n" \
                 f"• {quick_tips[2]}\n\n" \
                 f"REMEMBER: Speed kills in scalping - be quick to enter AND exit!"
        
        return result 