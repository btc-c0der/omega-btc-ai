"""
Strategic Trader Persona - a methodical, calculated guide for the OMEGA BTC AI trading system.

This persona speaks with patience and wisdom about market structure, long-term trends,
and carefully planned entries and exits based on Fibonacci principles.
"""

import random
from typing import Dict, Any, List, Optional

from omega_ai.personification.persona_base import BasePersona, PersonaStyle, TradingMood


class StrategicTraderPersona(BasePersona):
    """
    Strategic Trader persona - provides market guidance based on long-term analysis.
    
    This persona focuses on market structure, key Fibonacci levels, and patient
    execution. Speaks with wisdom and calculated precision about methodical trading.
    """
    
    def __init__(self):
        """Initialize the Strategic Trader persona with appropriate style elements."""
        style = PersonaStyle(
            primary_color="#9B59B6",  # Purple
            secondary_color="#F0F3F4",  # Light gray
            accent_color="#2ECC71",  # Green
            font_family="'Montserrat', sans-serif",
            avatar_url="/assets/images/personas/strategic_trader_avatar.png",
            background_pattern="/assets/images/patterns/strategic_pattern.png",
            icons={
                "bullish": "/assets/icons/long_term_up.svg",
                "bearish": "/assets/icons/long_term_down.svg",
                "neutral": "/assets/icons/consolidation.svg",
                "alert": "/assets/icons/key_level.svg",
                "info": "/assets/icons/structure_info.svg"
            }
        )
        
        super().__init__(
            name="Strategic Trader",
            description="A calculated market strategist focused on market structure, "
                       "Fibonacci levels, and patient execution. Speaks with wisdom "
                       "about long-term trends and methodical position management.",
            style=style
        )
        
        # Strategic terminology
        self.market_structures = [
            "Higher High", "Higher Low", "Lower High", "Lower Low", 
            "Double Top", "Double Bottom", "Head and Shoulders", "Inverse H&S",
            "Wyckoff Accumulation", "Wyckoff Distribution", "Liquidity Zone"
        ]
        
        self.timeframes = [
            "Daily", "Weekly", "Monthly", "4-Hour", "1-Hour"
        ]
        
        self.fibonacci_levels = [
            "0.236", "0.382", "0.5", "0.618", "0.786", "0.886", "1.0", "1.272", "1.618", "2.618"
        ]
        
        self.greetings = [
            "Welcome to the long-term perspective. Let's analyze market structure together.",
            "Patient analysis builds profitable positions. Let's examine the markets methodically.",
            "Strategic trading requires discipline and structure. I'll guide you through the markets.",
            "Fibonacci harmony reveals optimal entries and exits. Let's find them together.",
            "Market structure tells us where we are in the cycle. Let me show you what I see."
        ]
    
    def get_greeting(self) -> str:
        """Get a randomized Strategic Trader greeting."""
        return random.choice(self.greetings)
    
    def analyze_position(self, position_data: Dict[str, Any]) -> str:
        """
        Analyze trading position with strategic calculation.
        
        Args:
            position_data: Dictionary containing position information
            
        Returns:
            Styled analysis text in the Strategic Trader voice
        """
        side = position_data.get('side', 'unknown')
        entry_price = position_data.get('entry_price', 0)
        current_price = position_data.get('current_price', 0)
        pnl = position_data.get('pnl', 0)
        
        # Calculate if the position is in profit or loss
        is_profitable = pnl > 0
        
        # Get emoji based on position type and profitability
        if side == 'long':
            direction_emoji = "📈" if is_profitable else "📉"
            position_term = "bullish position" if is_profitable else "long position under pressure"
        else:  # short
            direction_emoji = "📉" if is_profitable else "📈"
            position_term = "bearish position playing out" if is_profitable else "short position facing resistance"
        
        # Choose a market structure
        structure = random.choice(self.market_structures)
        
        # Choose a fibonacci level
        fib_level = random.choice(self.fibonacci_levels)
        
        # Format the response
        result = f"{direction_emoji} Position Analysis: {position_data.get('symbol', 'BTC')} {side.upper()} at {entry_price:,.2f}\n\n"
        
        result += f"Current Price: ${current_price:,.2f} with PnL of ${pnl:,.2f}\n\n"
        
        if is_profitable:
            result += f"Your {position_term} aligns with the current market structure showing a {structure} pattern. "
            result += f"Price is respecting the {fib_level} Fibonacci level as expected.\n\n"
            result += f"Consider taking partial profits at the {random.choice(self.fibonacci_levels)} extension, "
            result += f"while maintaining core position for further development on the {random.choice(self.timeframes)} timeframe."
        else:
            result += f"Your {position_term} is currently testing our patience. The {structure} pattern is still in development. "
            result += f"Current price action is finding resistance at the {fib_level} Fibonacci level.\n\n"
            result += f"Maintain disciplined position size and consider averaging in if price reaches the "
            result += f"{random.choice(self.fibonacci_levels)} retracement on the {random.choice(self.timeframes)} timeframe."
        
        return result
    
    def analyze_market(self, market_data: Dict[str, Any]) -> str:
        """
        Analyze market conditions with strategic perspective.
        
        Args:
            market_data: Dictionary containing market information
            
        Returns:
            Styled market analysis text in the Strategic Trader voice
        """
        # Update mood based on market data
        self.update_mood(market_data)
        
        current_price = market_data.get('price', 0)
        change_24h = market_data.get('price_change_24h', 0)
        volume = market_data.get('volume_24h', 0)
        
        # Determine if the market is up or down
        market_direction = "advancing" if change_24h > 0 else "retracing"
        
        # Select direction emoji
        if change_24h > 5:
            direction_emoji = "🟢🟢🟢"
        elif change_24h > 0:
            direction_emoji = "🟢"
        elif change_24h > -5:
            direction_emoji = "🔴"
        else:
            direction_emoji = "🔴🔴🔴"
        
        # Volume analysis
        if volume > 10000000000:  # high volume
            volume_desc = "significant volume indicating strong participation"
        elif volume > 5000000000:  # medium volume
            volume_desc = "moderate volume suggesting balanced participation"
        else:  # low volume
            volume_desc = "light volume indicating potential accumulation/distribution"
        
        # Market structure analysis based on mood
        if self.current_mood in [TradingMood.EXTREMELY_BULLISH, TradingMood.BULLISH]:
            structure = f"Higher Highs and Higher Lows on the {random.choice(self.timeframes)} timeframe"
            strategy = "consider buying dips to key Fibonacci support levels"
        elif self.current_mood in [TradingMood.SLIGHTLY_BULLISH, TradingMood.NEUTRAL]:
            structure = f"Consolidation between key levels on the {random.choice(self.timeframes)} timeframe"
            strategy = "watch for breakout confirmation before committing capital"
        else:
            structure = f"Lower Highs and Lower Lows on the {random.choice(self.timeframes)} timeframe"
            strategy = "consider selling rallies to key Fibonacci resistance levels"
        
        # Fibonacci reference
        fib_level = random.choice(self.fibonacci_levels)
        fib_price = current_price * float(fib_level) if float(fib_level) < 1 else current_price / (2 - float(fib_level))
        
        result = f"{direction_emoji} BTC Market Analysis: ${current_price:,.2f} ({change_24h:+.2f}% 24h)\n\n"
        result += f"Market Structure: {structure} with {market_direction} price action and {volume_desc}.\n\n"
        result += f"Key Fibonacci Level: {fib_level} at ${fib_price:,.2f}\n\n"
        result += f"Strategic Approach: {strategy}. Maintain position sizing discipline and focus on high-probability setups."
        
        return result
    
    def generate_recommendation(self, data: Dict[str, Any]) -> str:
        """
        Generate trading recommendations with strategic calculation.
        
        Args:
            data: Dictionary containing relevant trading data
            
        Returns:
            Styled recommendation text in the Strategic Trader voice
        """
        price = data.get('price', 0)
        trend = data.get('trend', 'neutral')
        strength = data.get('signal_strength', 0.5)
        
        # Choose timeframe
        timeframe = random.choice(self.timeframes)
        
        # Choose market structure
        structure = random.choice(self.market_structures)
        
        # Determine recommended action
        if trend == 'bullish' and strength > 0.7:
            action = "strategically accumulate on pullbacks to support"
            direction = "bullish"
            emoji = "🟢"
        elif trend == 'bullish' and strength > 0.3:
            action = "consider partial positions with clear invalidation levels"
            direction = "cautiously bullish"
            emoji = "🟡"
        elif trend == 'bearish' and strength > 0.7:
            action = "reduce exposure and consider strategic shorts at resistance"
            direction = "bearish"
            emoji = "🔴"
        elif trend == 'bearish' and strength > 0.3:
            action = "maintain capital preservation focus with tight risk management"
            direction = "cautiously bearish"
            emoji = "🟠"
        else:
            action = "neutral positioning with focus on capital preservation"
            direction = "neutral"
            emoji = "⚪"
        
        # Format strength as stars (sophisticated version)
        strength_desc = ""
        if strength > 0.8:
            strength_desc = "high-confidence setup"
        elif strength > 0.6:
            strength_desc = "moderate-confidence setup"
        elif strength > 0.4:
            strength_desc = "developing setup requiring confirmation"
        else:
            strength_desc = "low-confidence setup requiring caution"
        
        # Add fib reference if available
        fib_reference = ""
        if data.get('fib_level'):
            fib_reference = f"Key Fibonacci level {data.get('fib_level')} at ${data.get('fib_price', 0):,.2f} provides a significant reference point. "
        
        # Risk management section
        risk_management = f"Maintain position sizing at less than 2% risk per trade with 1:{int(random.uniform(2, 5))} risk:reward ratio."
        
        result = f"{emoji} Strategic Recommendation for BTC at ${price:,.2f}\n\n" \
                 f"Market Direction: {direction.capitalize()} on {timeframe} timeframe ({strength_desc})\n\n" \
                 f"Market Structure: {structure}\n\n" \
                 f"Strategic Action: {action}.\n\n" \
                 f"{fib_reference}{risk_management}"
                 
        return result
    
    def summarize_performance(self, performance_data: Dict[str, Any]) -> str:
        """
        Summarize trading performance with strategic perspective.
        
        Args:
            performance_data: Dictionary containing performance metrics
            
        Returns:
            Styled performance summary in the Strategic Trader voice
        """
        total_pnl = performance_data.get('total_pnl', 0)
        win_rate = performance_data.get('win_rate', 0)
        trade_count = performance_data.get('trade_count', 0)
        
        # Determine overall assessment
        if total_pnl > 1000:
            assessment = "exceptional performance"
            emoji = "🏆"
        elif total_pnl > 100:
            assessment = "solid performance"
            emoji = "✅"
        elif total_pnl > 0:
            assessment = "positive performance"
            emoji = "📈"
        elif total_pnl > -100:
            assessment = "capital preservation with minor drawdown"
            emoji = "⚠️"
        else:
            assessment = "significant drawdown requiring strategy reassessment"
            emoji = "🛑"
        
        # Analyze win rate
        if win_rate > 0.7:
            win_analysis = "excellent win rate demonstrating strong edge"
        elif win_rate > 0.5:
            win_analysis = "positive win rate showing viable strategy"
        else:
            win_analysis = "win rate below threshold suggesting strategy refinement needed"
            
        # Calculate expectancy if available
        expectancy = performance_data.get('average_win', 0) * win_rate - performance_data.get('average_loss', 0) * (1-win_rate)
        expectancy_desc = f"strategy expectancy of ${expectancy:.2f} per trade" if expectancy else ""
        
        # Recommendations based on performance
        if total_pnl > 0:
            recommendations = [
                f"Continue methodical execution with current parameters",
                f"Consider increasing position size by 25% if consistency continues",
                f"Review underperforming setups to optimize strategy"
            ]
        else:
            recommendations = [
                f"Review risk management parameters to limit drawdowns",
                f"Decrease position size by 50% until consistent profitability returns",
                f"Focus on highest probability setups with strongest market structure"
            ]
            
        result = f"{emoji} Strategic Performance Analysis {emoji}\n\n" \
                 f"Overview: {assessment} with ${total_pnl:,.2f} total P&L across {trade_count} trades.\n\n" \
                 f"Win Rate: {win_rate*100:.1f}% ({win_analysis}) with {expectancy_desc}\n\n" \
                 f"Strategic Recommendations:\n" \
                 f"• {recommendations[0]}\n" \
                 f"• {recommendations[1]}\n" \
                 f"• {recommendations[2]}\n\n" \
                 f"Remember: Consistency and discipline are the foundations of strategic success."
        
        return result 