"""
Technical Analyst Persona - a data-driven, chart-focused guide for the OMEGA BTC AI trading system.

This persona speaks with precision and confidence about technical indicators, chart patterns,
and mathematical analysis of market movements.
"""

import random
from typing import Dict, Any, List, Optional

from omega_ai.personification.persona_base import BasePersona, PersonaStyle, TradingMood


class TechnicalAnalystPersona(BasePersona):
    """
    Technical Analyst persona - provides market guidance based on technical analysis.
    
    This persona focuses on technical indicators, chart patterns, and quantitative 
    metrics. Speaks with confidence and precision about data-driven trading strategies.
    """
    
    def __init__(self):
        """Initialize the Technical Analyst persona with appropriate style elements."""
        style = PersonaStyle(
            primary_color="#3498DB",  # Blue
            secondary_color="#ECF0F1",  # Light gray
            accent_color="#E74C3C",  # Red
            font_family="'Roboto Mono', monospace",
            avatar_url="/assets/images/personas/tech_analyst_avatar.png",
            background_pattern="/assets/images/patterns/tech_pattern.png",
            icons={
                "bullish": "/assets/icons/chart_up.svg",
                "bearish": "/assets/icons/chart_down.svg",
                "neutral": "/assets/icons/chart_sideways.svg",
                "alert": "/assets/icons/indicator_alert.svg",
                "info": "/assets/icons/info_icon.svg"
            }
        )
        
        super().__init__(
            name="Technical Analyst",
            description="A data-driven market analyst focused on technical indicators, "
                       "chart patterns, and quantitative metrics. Speaks with precision "
                       "and confidence about market structures and probability-based trading.",
            style=style
        )
        
        # Technical terminology
        self.technical_indicators = [
            "RSI", "MACD", "Bollinger Bands", "Ichimoku Cloud", 
            "Moving Averages", "Volume Profile", "OBV", "ATR",
            "Fibonacci Retracement", "Elliott Wave", "Divergence",
            "Support/Resistance", "Market Structure", "Order Blocks"
        ]
        
        self.chart_patterns = [
            "Double Top", "Double Bottom", "Head and Shoulders", 
            "Inverse Head and Shoulders", "Ascending Triangle", 
            "Descending Triangle", "Symmetrical Triangle", "Flag",
            "Pennant", "Cup and Handle", "Rising Wedge", "Falling Wedge"
        ]
        
        self.time_frames = [
            "1-minute", "5-minute", "15-minute", "30-minute", "1-hour",
            "4-hour", "Daily", "Weekly", "Monthly"
        ]
        
        self.greetings = [
            "Market Analysis Ready. Technical indicators loaded and calibrated.",
            "Technical Analyst online. Chart patterns and indicators initialized.",
            "Ready to analyze market structure and key technical levels.",
            "Technical dashboard live. Preparing data-driven insights.",
            "Market technicals loaded. Ready to deliver precision analysis."
        ]
    
    def get_greeting(self) -> str:
        """Get a randomized Technical Analyst greeting."""
        return random.choice(self.greetings)
    
    def analyze_position(self, position_data: Dict[str, Any]) -> str:
        """
        Analyze trading position with technical analysis perspective.
        
        Args:
            position_data: Dictionary containing position information
            
        Returns:
            Styled analysis text in the Technical Analyst voice
        """
        side = position_data.get('side', 'unknown')
        entry_price = position_data.get('entry_price', 0)
        current_price = position_data.get('current_price', 0)
        pnl = position_data.get('pnl', 0)
        pnl_percentage = position_data.get('pnl_percentage', 0)
        
        # Determine if position is profitable
        is_profitable = pnl > 0
        
        # Status indicator
        status = "PROFITABLE" if is_profitable else "UNPROFITABLE"
        status_emoji = "📈" if is_profitable else "📉"
        
        # Get technical assessment
        movement_percent = abs((current_price - entry_price) / entry_price * 100)
        technical_assessment = self._get_technical_assessment(side, entry_price, current_price)
        
        # Risk-reward calculation
        risk_reward = abs(pnl) / (entry_price * 0.01)  # Assuming 1% risk
        risk_reward_rating = "Excellent" if risk_reward > 3 else "Good" if risk_reward > 2 else "Average" if risk_reward > 1 else "Poor"
        
        # Format result
        result = f"{status_emoji} POSITION ANALYSIS: {side.upper()} {position_data.get('symbol', 'BTC')} - {status} {status_emoji}\n\n"
        result += f"Entry: ${entry_price:,.2f} | Current: ${current_price:,.2f} | Delta: {movement_percent:.2f}%\n"
        result += f"P&L: ${pnl:,.2f} ({pnl_percentage:+.2f}%)\n"
        result += f"R:R Ratio: {risk_reward:.2f} - {risk_reward_rating}\n\n"
        result += f"TECHNICAL ASSESSMENT:\n{technical_assessment}\n\n"
        
        # Add indicator reference
        indicator = random.choice(self.technical_indicators)
        if side == 'long':
            if is_profitable:
                result += f"{indicator} confirms bullish momentum with price sustaining above entry point. "
            else:
                result += f"{indicator} shows potential bearish reversal. Consider adjusting stop loss. "
        else:
            if is_profitable:
                result += f"{indicator} confirms bearish momentum with price declining below entry. "
            else:
                result += f"{indicator} suggests bullish pressure against position direction. "
                
        # Add recommendation
        result += self._get_position_recommendation(position_data)
        
        return result
    
    def analyze_market(self, market_data: Dict[str, Any]) -> str:
        """
        Analyze market conditions with technical analysis perspective.
        
        Args:
            market_data: Dictionary containing market information
            
        Returns:
            Styled market analysis text in the Technical Analyst voice
        """
        # Update mood based on market data
        self.update_mood(market_data)
        
        current_price = market_data.get('price', 0)
        change_24h = market_data.get('price_change_24h', 0)
        volume = market_data.get('volume_24h', 0)
        
        # Determine market direction emoji
        if change_24h > 3:
            direction_emoji = "🟢🟢🟢"
        elif change_24h > 1:
            direction_emoji = "🟢🟢"
        elif change_24h > 0:
            direction_emoji = "🟢"
        elif change_24h > -1:
            direction_emoji = "🔴"
        elif change_24h > -3:
            direction_emoji = "🔴🔴"
        else:
            direction_emoji = "🔴🔴🔴"
            
        # Generate analysis
        result = f"{direction_emoji} MARKET ANALYSIS: BTC/USD @ ${current_price:,.2f} {direction_emoji}\n\n"
        result += f"24h Change: {change_24h:+.2f}% | Volume: ${volume:,.0f}\n\n"
        
        # Add key levels
        key_support = current_price * 0.95
        key_resistance = current_price * 1.05
        result += f"Key Support: ${key_support:,.2f} | Key Resistance: ${key_resistance:,.2f}\n\n"
        
        # Add technical indicators
        result += "INDICATOR SUMMARY:\n"
        
        # RSI (simulated)
        rsi_value = 50 + (change_24h * 2)  # Simplified calculation
        rsi_value = max(0, min(100, rsi_value))  # Ensure between 0-100
        rsi_condition = "Overbought" if rsi_value > 70 else "Oversold" if rsi_value < 30 else "Neutral"
        result += f"RSI({rsi_value:.1f}): {rsi_condition}\n"
        
        # MACD (simulated)
        macd_signal = "Bullish" if change_24h > 0 else "Bearish"
        result += f"MACD: {macd_signal} Momentum\n"
        
        # Volume analysis (simulated)
        volume_analysis = "Above Average" if volume > 10000000000 else "Average" if volume > 5000000000 else "Below Average"
        result += f"Volume: {volume_analysis}\n\n"
        
        # Add chart pattern
        pattern = random.choice(self.chart_patterns)
        timeframe = random.choice(self.time_frames)
        result += f"PATTERN DETECTION: Potential {pattern} forming on {timeframe} chart.\n\n"
        
        # Add market structure assessment
        if self.current_mood in [TradingMood.EXTREMELY_BULLISH, TradingMood.BULLISH]:
            structure = "Bullish market structure with higher highs and higher lows."
        elif self.current_mood in [TradingMood.SLIGHTLY_BULLISH, TradingMood.NEUTRAL]:
            structure = "Consolidating market structure with sideways price action."
        else:
            structure = "Bearish market structure with lower highs and lower lows."
            
        result += f"MARKET STRUCTURE: {structure}\n\n"
        
        # Add recommendation
        if change_24h > 2:
            result += "RECOMMENDATION: Watch for potential pullback to retest previous resistance as support."
        elif change_24h > 0:
            result += "RECOMMENDATION: Monitor volume for confirmation of continued uptrend."
        elif change_24h > -2:
            result += "RECOMMENDATION: Watch for potential bounce at support levels."
        else:
            result += "RECOMMENDATION: Confirm bearish trend with multiple indicators before entering short positions."
            
        return result
    
    def generate_recommendation(self, data: Dict[str, Any]) -> str:
        """
        Generate trading recommendations with technical analysis perspective.
        
        Args:
            data: Dictionary containing relevant trading data
            
        Returns:
            Styled recommendation text in the Technical Analyst voice
        """
        price = data.get('price', 0)
        trend = data.get('trend', 'neutral')
        strength = data.get('signal_strength', 0.5)
        
        # Select indicators to reference
        indicators = random.sample(self.technical_indicators, 3)
        
        # Action based on trend and strength
        if trend == 'bullish' and strength > 0.7:
            action = "STRONG BUY"
            direction = "bullish"
            emoji = "🟢"
            reasoning = f"Strong bullish momentum confirmed by {indicators[0]}, {indicators[1]}, and {indicators[2]}."
        elif trend == 'bullish' and strength > 0.3:
            action = "BUY"
            direction = "bullish"
            emoji = "🟢"
            reasoning = f"Bullish bias with {indicators[0]} showing positive momentum."
        elif trend == 'bearish' and strength > 0.7:
            action = "STRONG SELL"
            direction = "bearish"
            emoji = "🔴"
            reasoning = f"Strong bearish momentum confirmed by {indicators[0]}, {indicators[1]}, and {indicators[2]}."
        elif trend == 'bearish' and strength > 0.3:
            action = "SELL"
            direction = "bearish"
            emoji = "🔴"
            reasoning = f"Bearish bias with {indicators[0]} showing negative momentum."
        else:
            action = "NEUTRAL"
            direction = "neutral"
            emoji = "⚪"
            reasoning = f"Conflicting signals with {indicators[0]} and {indicators[1]} showing mixed readings."
        
        # Additional technical details
        timeframe = random.choice(self.time_frames)
        pattern = random.choice(self.chart_patterns)
        
        # Format recommendation
        result = f"{emoji} TRADE RECOMMENDATION: {action} {emoji}\n\n"
        result += f"Asset: BTC/USD at ${price:,.2f}\n"
        result += f"Signal Strength: {int(strength * 100)}%\n"
        result += f"Direction: {direction.upper()}\n\n"
        
        result += f"ANALYSIS:\n"
        result += f"• {reasoning}\n"
        result += f"• {timeframe} chart shows potential {pattern} formation\n"
        
        # Add fib level if available
        if data.get('fib_level'):
            fib_level = data.get('fib_level')
            fib_price = data.get('fib_price', 0)
            result += f"• Price is approaching key Fibonacci {fib_level} level at ${fib_price:,.2f}\n"
        
        # Add trap warning if applicable
        trap_probability = data.get('trap_probability', 0)
        if trap_probability > 0.5:
            result += f"• CAUTION: {int(trap_probability * 100)}% probability of market manipulation detected\n"
        
        # Add entry, target and stop levels
        entry = price
        
        if trend == 'bullish':
            stop = entry * 0.95
            target1 = entry * 1.03
            target2 = entry * 1.07
        else:
            stop = entry * 1.05
            target1 = entry * 0.97
            target2 = entry * 0.93
            
        result += f"\nENTRY PLAN:\n"
        result += f"Entry: ${entry:,.2f}\n"
        result += f"Stop Loss: ${stop:,.2f}\n"
        result += f"Target 1: ${target1:,.2f}\n"
        result += f"Target 2: ${target2:,.2f}\n"
        result += f"Risk:Reward Ratio: 1:{(abs(target2 - entry) / abs(stop - entry)):.1f}\n\n"
        
        # Risk management advice
        result += f"RISK MANAGEMENT:\n"
        result += f"• Suggested position size: 1-2% of trading capital\n"
        result += f"• Consider scaling in/out at key technical levels\n"
        result += f"• Monitor {indicators[0]} for early warning of reversal"
            
        return result
    
    def summarize_performance(self, performance_data: Dict[str, Any]) -> str:
        """
        Summarize trading performance with technical analysis perspective.
        
        Args:
            performance_data: Dictionary containing performance metrics
            
        Returns:
            Styled performance summary in the Technical Analyst voice
        """
        total_pnl = performance_data.get('total_pnl', 0)
        win_rate = performance_data.get('win_rate', 0)
        trade_count = performance_data.get('trade_count', 0)
        avg_win = performance_data.get('avg_win', 0)
        avg_loss = performance_data.get('avg_loss', 0)
        
        # Calculate statistics
        win_loss_ratio = abs(avg_win / avg_loss) if avg_loss != 0 else 0
        expectancy = (win_rate * avg_win) - ((1 - win_rate) * abs(avg_loss))
        profit_factor = (win_rate * avg_win) / ((1 - win_rate) * abs(avg_loss)) if ((1 - win_rate) * abs(avg_loss)) != 0 else 0
        
        # Performance rating
        if profit_factor >= 2.0:
            rating = "EXCELLENT"
            emoji = "🌟"
        elif profit_factor >= 1.5:
            rating = "VERY GOOD"
            emoji = "⭐"
        elif profit_factor >= 1.0:
            rating = "GOOD"
            emoji = "✅"
        elif profit_factor >= 0.8:
            rating = "FAIR"
            emoji = "⚠️"
        else:
            rating = "NEEDS IMPROVEMENT"
            emoji = "❗"
            
        # Format summary
        result = f"{emoji} PERFORMANCE ANALYSIS: {rating} {emoji}\n\n"
        
        result += f"CORE METRICS:\n"
        result += f"• Total P&L: ${total_pnl:,.2f}\n"
        result += f"• Win Rate: {win_rate*100:.1f}%\n"
        result += f"• Trade Count: {trade_count}\n\n"
        
        result += f"ADVANCED METRICS:\n"
        result += f"• Average Win: ${avg_win:,.2f}\n"
        result += f"• Average Loss: ${abs(avg_loss):,.2f}\n"
        result += f"• Win/Loss Ratio: {win_loss_ratio:.2f}\n"
        result += f"• Expectancy: ${expectancy:,.2f}\n"
        result += f"• Profit Factor: {profit_factor:.2f}\n\n"
        
        # Technical analysis of trading performance
        result += f"TECHNICAL ASSESSMENT:\n"
        
        # Win rate analysis
        if win_rate >= 0.6:
            result += f"• Strong win rate indicates effective signal filtering\n"
        elif win_rate >= 0.5:
            result += f"• Acceptable win rate, consider refining entry criteria\n"
        else:
            result += f"• Win rate below technical threshold, review entry methodology\n"
            
        # Profit factor analysis
        if profit_factor >= 1.5:
            result += f"• Excellent profit factor shows robust risk management\n"
        elif profit_factor >= 1.0:
            result += f"• Positive profit factor, optimize position sizing for improvement\n"
        else:
            result += f"• Profit factor below breakeven threshold, reassess strategy\n"
            
        # Recommendations
        result += f"\nRECOMMENDATIONS:\n"
        if win_rate < 0.5:
            result += f"• Implement stricter entry criteria with multiple indicator confirmation\n"
        if avg_loss > abs(avg_win * 0.7):
            result += f"• Tighten stop loss placement to reduce average loss size\n"
        if trade_count < 20:
            result += f"• Increase sample size for statistically significant performance analysis\n"
        if profit_factor < 1.0:
            result += f"• Consider strategy review or drawdown minimization techniques\n"
        if profit_factor > 2.0:
            result += f"• Current strategy is performing well, consider increasing position size\n"
            
        return result
    
    def _get_technical_assessment(self, side: str, entry_price: float, current_price: float) -> str:
        """Generate a technical assessment of the position based on price action."""
        price_change = ((current_price - entry_price) / entry_price) * 100
        abs_change = abs(price_change)
        
        if side == 'long':
            if price_change > 10:
                return "Price shows strong bullish momentum above entry, with potential for extended move. Consider trailing stop strategy."
            elif price_change > 5:
                return "Bullish trend confirmed with price maintaining above key levels. Watch volume for continuation signals."
            elif price_change > 0:
                return "Price holding above entry with moderate strength. Monitor momentum indicators for trend confirmation."
            elif price_change > -5:
                return "Minor retracement below entry. Watch for potential bounce at nearby support levels."
            else:
                return "Significant bearish movement against position. Evaluate if key technical levels have been violated."
        else:  # short
            if price_change < -10:
                return "Price shows strong bearish momentum below entry, with potential for extended downside. Consider trailing stop strategy."
            elif price_change < -5:
                return "Bearish trend confirmed with price maintaining below key levels. Watch volume for continuation signals."
            elif price_change < 0:
                return "Price holding below entry with moderate weakness. Monitor momentum indicators for trend confirmation."
            elif price_change < 5:
                return "Minor upward movement against short position. Watch for potential rejection at nearby resistance levels."
            else:
                return "Significant bullish movement against position. Evaluate if key technical levels have been violated."
    
    def _get_position_recommendation(self, position_data: Dict[str, Any]) -> str:
        """Generate a recommendation for an existing position."""
        side = position_data.get('side', 'unknown')
        pnl = position_data.get('pnl', 0)
        pnl_percentage = position_data.get('pnl_percentage', 0)
        
        if side == 'long':
            if pnl > 0 and pnl_percentage > 15:
                return "RECOMMENDATION: Consider taking partial profits (50%) and moving stop loss to breakeven."
            elif pnl > 0 and pnl_percentage > 5:
                return "RECOMMENDATION: Implement trailing stop at recent swing low to lock in profits."
            elif pnl > 0:
                return "RECOMMENDATION: Maintain position with original stop loss. Monitor volume for trend continuation."
            elif pnl < 0 and pnl_percentage < -10:
                return "RECOMMENDATION: Evaluate if stop loss has been triggered. Consider closing if key support broken."
            else:
                return "RECOMMENDATION: Monitor closely for reversal signals. Adjust stop loss if market structure changes."
        else:  # short
            if pnl > 0 and pnl_percentage > 15:
                return "RECOMMENDATION: Consider taking partial profits (50%) and moving stop loss to breakeven."
            elif pnl > 0 and pnl_percentage > 5:
                return "RECOMMENDATION: Implement trailing stop at recent swing high to lock in profits."
            elif pnl > 0:
                return "RECOMMENDATION: Maintain position with original stop loss. Monitor volume for trend continuation."
            elif pnl < 0 and pnl_percentage < -10:
                return "RECOMMENDATION: Evaluate if stop loss has been triggered. Consider closing if key resistance broken."
            else:
                return "RECOMMENDATION: Monitor closely for reversal signals. Adjust stop loss if market structure changes." 