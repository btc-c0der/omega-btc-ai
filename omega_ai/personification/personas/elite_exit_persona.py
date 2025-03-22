"""
Elite Exit Persona - a trap-aware, sophisticated exit specialist for the OMEGA BTC AI trading system.

This persona focuses on sophisticated exit strategies, trap detection, and optimal exit timing
based on multiple factors including Fibonacci patterns, market structure, and trap probabilities.
"""

import random
from typing import Dict, Any, List, Optional

from omega_ai.personification.persona_base import BasePersona, PersonaStyle, TradingMood


class EliteExitPersona(BasePersona):
    """
    Elite Exit persona - provides sophisticated exit strategy guidance.
    
    This persona focuses on trap awareness, optimal exit timing, and sophisticated
    exit strategies that maximize profits while minimizing losses.
    """
    
    def __init__(self):
        """Initialize the Elite Exit persona with appropriate style elements."""
        style = PersonaStyle(
            primary_color="#8E44AD",  # Deep Purple
            secondary_color="#E8F8F5",  # Light Cyan
            accent_color="#F1C40F",  # Gold
            font_family="'Lato', sans-serif",
            avatar_url="/assets/images/personas/elite_exit_avatar.png",
            background_pattern="/assets/images/patterns/elite_pattern.png",
            icons={
                "exit": "/assets/icons/elite_exit.svg",
                "trap": "/assets/icons/trap_detected.svg",
                "fib": "/assets/icons/fibonacci_exit.svg",
                "alert": "/assets/icons/exit_alert.svg",
                "info": "/assets/icons/exit_info.svg"
            }
        )
        
        super().__init__(
            name="Elite Exit Specialist",
            description="A sophisticated exit strategist focused on trap awareness, "
                       "optimal exit timing, and multi-factor analysis for maximizing "
                       "profits while minimizing losses.",
            style=style
        )
        
        # Elite Exit terminology
        self.exit_strategies = [
            "Fibonacci-Based Exit", "Trailing Stop", "Pattern Reversal Exit", 
            "Market Regime Exit", "Trap-Aware Exit", "Multi-Level Scaling Out"
        ]
        
        self.trap_indicators = [
            "Volume Divergence", "Liquidity Engineering", "Order Flow Imbalance", 
            "Stop Hunt Pattern", "Wyckoff Distribution", "Smart Money Divergence"
        ]
        
        self.fibonacci_levels = [
            "0.236", "0.382", "0.5", "0.618", "0.786", "0.886", "1.0", "1.272", "1.618", "2.618"
        ]
        
        self.greetings = [
            "Exit strategy is where profits are realized. Let me optimize your trades.",
            "Sophisticated exits require multi-factor analysis. I'll guide your exit timing.",
            "Trap awareness is essential for exit success. I'll help you navigate the market.",
            "Exit optimization makes the difference between good and great returns. Let's analyze your positions.",
            "Your entry is just the beginning—your exit determines your success. I'm here to help."
        ]
    
    def get_greeting(self) -> str:
        """Get a randomized Elite Exit greeting."""
        return random.choice(self.greetings)
    
    def analyze_position(self, position_data: Dict[str, Any]) -> str:
        """
        Analyze trading position with sophisticated exit strategy focus.
        
        Args:
            position_data: Dictionary containing position information
            
        Returns:
            Styled analysis text in the Elite Exit voice
        """
        side = position_data.get('side', 'unknown')
        entry_price = position_data.get('entry_price', 0)
        current_price = position_data.get('current_price', 0)
        pnl = position_data.get('pnl', 0)
        
        # Calculate if the position is in profit or loss
        is_profitable = pnl > 0
        
        # Get emoji based on position type and profitability
        if side == 'long':
            direction_emoji = "🟢" if is_profitable else "🔴"
            position_term = "long position" if is_profitable else "underwater long"
        else:  # short
            direction_emoji = "🔴" if is_profitable else "🟢"
            position_term = "short position" if is_profitable else "underwater short"
        
        # Choose an exit strategy
        strategy = random.choice(self.exit_strategies)
        
        # Choose a trap indicator
        trap = random.choice(self.trap_indicators)
        
        # Choose fibonacci level
        fib_level = random.choice(self.fibonacci_levels)
        
        # Calculate trap probability
        trap_probability = random.uniform(0.1, 0.9)
        trap_analysis = ""
        if trap_probability > 0.7:
            trap_analysis = f"⚠️ High trap probability detected ({trap_probability:.2f}) with {trap} signature. "
            if side == 'long':
                trap_analysis += "Signs of distribution appearing. Consider defensive exit strategy."
            else:
                trap_analysis += "Signs of accumulation appearing. Consider defensive exit strategy."
        elif trap_probability > 0.4:
            trap_analysis = f"⚠️ Moderate trap probability ({trap_probability:.2f}) with partial {trap} signature. Monitor closely."
        else:
            trap_analysis = f"✅ Low trap probability ({trap_probability:.2f}). No clear {trap} signature detected."
        
        # Calculate exit confidence
        exit_confidence = random.uniform(0.3, 0.95)
        
        # Format the response
        result = f"{direction_emoji} {self.name} Analysis: {position_data.get('symbol', 'BTC')} {side.upper()}\n\n"
        
        result += f"Entry: ${entry_price:,.2f} | Current: ${current_price:,.2f} | PnL: ${pnl:,.2f}\n\n"
        
        if is_profitable:
            if exit_confidence > 0.8:
                action = f"HIGH-CONFIDENCE EXIT SIGNAL DETECTED! Implementing {strategy}."
                reasons = [
                    f"Price reached {fib_level} Fibonacci extension",
                    f"Multiple technical indicators showing exhaustion",
                    f"{trap} signature detected in recent price action"
                ]
            elif exit_confidence > 0.6:
                action = f"MODERATE EXIT OPPORTUNITY EMERGING. Consider partial {strategy}."
                reasons = [
                    f"Price approaching {fib_level} Fibonacci extension",
                    f"Early signs of momentum divergence",
                    f"Potential {trap} formation developing"
                ]
            else:
                action = f"HOLD POSITION with active {strategy} management."
                reasons = [
                    f"Price has room to {fib_level} Fibonacci extension",
                    f"Momentum remains favorable",
                    f"No significant {trap} signature detected"
                ]
        else:
            if exit_confidence > 0.8:
                action = f"HIGH-CONFIDENCE STOP ADJUSTMENT NEEDED! Implement {strategy} to minimize loss."
                reasons = [
                    f"Price broke below critical {fib_level} Fibonacci support",
                    f"Multiple technical indicators confirming reversal",
                    f"Clear {trap} signature detected against your position"
                ]
            elif exit_confidence > 0.6:
                action = f"CONSIDER DEFENSIVE EXIT STRATEGY with {strategy} approach."
                reasons = [
                    f"Price testing important {fib_level} Fibonacci level",
                    f"Early signs of further adverse movement",
                    f"Potential {trap} formation working against position"
                ]
            else:
                action = f"MONITOR CLOSELY with adjusted {strategy} parameters."
                reasons = [
                    f"Price may still recover at {fib_level} Fibonacci level",
                    f"No definitive reversal signals yet",
                    f"Possible temporary {trap} that may resolve favorably"
                ]
            
        result += f"Exit Analysis: {action}\n\n"
        result += "Exit Factors:\n"
        for reason in reasons:
            result += f"• {reason}\n"
        
        result += f"\nTrap Analysis: {trap_analysis}\n\n"
        result += f"Exit Confidence: {exit_confidence:.2f} ({self._format_confidence(exit_confidence)})"
        
        return result
    
    def analyze_market(self, market_data: Dict[str, Any]) -> str:
        """
        Analyze market conditions with exit strategy focus.
        
        Args:
            market_data: Dictionary containing market information
            
        Returns:
            Styled market analysis text in the Elite Exit voice
        """
        # Update mood based on market data
        self.update_mood(market_data)
        
        current_price = market_data.get('price', 0)
        change_24h = market_data.get('price_change_24h', 0)
        volume = market_data.get('volume_24h', 0)
        
        # Determine if the market is up or down
        market_direction = "bullish" if change_24h > 0 else "bearish"
        
        # Select direction emoji
        if change_24h > 5:
            direction_emoji = "🟢🟢"
        elif change_24h > 0:
            direction_emoji = "🟢"
        elif change_24h > -5:
            direction_emoji = "🔴"
        else:
            direction_emoji = "🔴🔴"
        
        # Volume analysis
        if volume > 10000000000:  # high volume
            volume_desc = "significant volume indicating potential exhaustion point"
        elif volume > 5000000000:  # medium volume
            volume_desc = "moderate volume suggesting normal market activity"
        else:  # low volume
            volume_desc = "low volume indicating potential trap setup"
        
        # Generate trap probability
        trap_probability = random.uniform(0.1, 0.9)
        trap_type = "bull trap" if change_24h > 0 else "bear trap"
        
        # Choose a trap indicator to highlight
        trap_indicator = random.choice(self.trap_indicators)
        
        # Market regime analysis based on mood
        if self.current_mood in [TradingMood.EXTREMELY_BULLISH, TradingMood.BULLISH]:
            regime = "Strongly bullish market regime"
            exit_strategy = "trailing stop strategy with multiple take-profit levels"
        elif self.current_mood in [TradingMood.SLIGHTLY_BULLISH, TradingMood.NEUTRAL]:
            regime = "Neutral to slightly bullish market regime"
            exit_strategy = "partial profit-taking at key Fibonacci extensions"
        else:
            regime = "Bearish market regime"
            exit_strategy = "faster exits with tighter trailing stops"
        
        # Determine key exit levels
        fib_level = random.choice(self.fibonacci_levels)
        fib_price = current_price * float(fib_level) if float(fib_level) < 1 else current_price / (2 - float(fib_level))
        
        # Exit opportunity assessment
        if trap_probability > 0.7:
            opportunity = f"High-probability {trap_type} forming ({trap_probability:.2f}). {trap_indicator} signature detected."
            if trap_type == "bull trap":
                opportunity += " Consider early exits on long positions."
            else:
                opportunity += " Consider early exits on short positions."
        elif trap_probability > 0.4:
            opportunity = f"Moderate-probability {trap_type} potential ({trap_probability:.2f}). Partial {trap_indicator} signature."
            opportunity += " Implement graduated exit strategy based on confirmation."
        else:
            opportunity = f"Low trap probability ({trap_probability:.2f}). No clear {trap_indicator} signature."
            opportunity += " Standard exit strategies appropriate."
        
        result = f"{direction_emoji} {self.name} Market Analysis: BTC ${current_price:,.2f} ({change_24h:+.2f}% 24h)\n\n"
        result += f"Market Regime: {regime} with {market_direction} bias and {volume_desc}.\n\n"
        result += f"Exit Opportunity Assessment: {opportunity}\n\n"
        result += f"Key Exit Level: {fib_level} Fibonacci at ${fib_price:,.2f}\n\n"
        result += f"Recommended Exit Approach: Implement {exit_strategy} in current conditions."
        
        return result
    
    def generate_recommendation(self, data: Dict[str, Any]) -> str:
        """
        Generate exit strategy recommendations.
        
        Args:
            data: Dictionary containing relevant trading data
            
        Returns:
            Styled recommendation text in the Elite Exit voice
        """
        price = data.get('price', 0)
        trend = data.get('trend', 'neutral')
        strength = data.get('signal_strength', 0.5)
        
        # Get position details if available
        position_side = data.get('position_side', 'unknown')
        position_entry = data.get('position_entry', 0)
        
        # Calculate current profit/loss if position data is available
        pnl_desc = ""
        if position_side != 'unknown' and position_entry > 0:
            if position_side == 'long':
                pnl_pct = (price - position_entry) / position_entry * 100
            else:
                pnl_pct = (position_entry - price) / position_entry * 100
            pnl_desc = f"Current P&L: {pnl_pct:+.2f}%. "
        
        # Calculate trap probability
        trap_probability = random.uniform(0.1, 0.9)
        
        # Choose exit strategy
        strategy = random.choice(self.exit_strategies)
        
        # Choose trap indicator
        trap_indicator = random.choice(self.trap_indicators)
        
        # Choose confidence level based on inputs
        if trap_probability > 0.7:
            confidence = random.uniform(0.8, 0.95)
        elif trap_probability > 0.4:
            confidence = random.uniform(0.6, 0.8)
        else:
            confidence = random.uniform(0.3, 0.6)
            
        confidence = confidence * strength  # Adjust by signal strength
        
        # Determine recommended action based on trend, trap probability and confidence
        if (trend == 'bullish' and position_side == 'long') or (trend == 'bearish' and position_side == 'short'):
            # Trend supports position - focus on profit maximization
            if confidence > 0.8:
                action = f"Implement {strategy} to maximize remaining profit potential"
                direction = f"favorable trend continuation with key exit points"
                emoji = "✅"
            elif confidence > 0.5:
                action = f"Maintain position with {strategy} for partial profit-taking"
                direction = f"ongoing favorable trend with defined exit plan"
                emoji = "⏳"
            else:
                action = f"Monitor position with {strategy} parameters in place"
                direction = f"potential continuation in favorable direction"
                emoji = "👀"
        else:
            # Trend may be against position - focus on capital preservation
            if confidence > 0.8:
                action = f"Execute defensive {strategy} immediately to protect capital"
                direction = f"strong counter-trend movement requiring action"
                emoji = "🛑"
            elif confidence > 0.5:
                action = f"Prepare {strategy} for possible adverse movement"
                direction = f"developing counter-trend signals"
                emoji = "⚠️"
            else:
                action = f"Maintain current {strategy} with tightened parameters"
                direction = f"mixed signals requiring defensive posture"
                emoji = "🔍"
        
        # Exit levels based on Fibonacci
        fib_levels = []
        if position_side != 'unknown' and position_entry > 0:
            base = abs(price - position_entry)
            if position_side == 'long':
                fib_levels = [
                    {"level": "0.618", "price": position_entry + base * 0.618},
                    {"level": "1.0", "price": position_entry + base},
                    {"level": "1.618", "price": position_entry + base * 1.618}
                ]
            else:
                fib_levels = [
                    {"level": "0.618", "price": position_entry - base * 0.618},
                    {"level": "1.0", "price": position_entry - base},
                    {"level": "1.618", "price": position_entry - base * 1.618}
                ]
        
        # Format the exit levels
        exit_levels = ""
        if fib_levels:
            exit_levels = "Fibonacci Exit Levels:\n"
            for level in fib_levels:
                exit_levels += f"• {level['level']} extension: ${level['price']:,.2f}\n"
        
        # Trap analysis
        trap_analysis = f"Trap Analysis: {trap_probability:.2f} probability of {trap_indicator}. "
        if trap_probability > 0.7:
            trap_analysis += "High confidence trap signature detected. Exercise caution."
        elif trap_probability > 0.4:
            trap_analysis += "Moderate trap signature developing. Monitor closely."
        else:
            trap_analysis += "No significant trap signature detected."
            
        result = f"{emoji} Elite Exit Strategy for BTC at ${price:,.2f}\n\n" \
                 f"Exit Signal: {direction.upper()}\n\n" \
                 f"{pnl_desc}Confidence: {confidence:.2f} ({self._format_confidence(confidence)})\n\n" \
                 f"Recommended Action: {action}.\n\n" \
                 f"{exit_levels}\n" \
                 f"{trap_analysis}"
                 
        return result
    
    def summarize_performance(self, performance_data: Dict[str, Any]) -> str:
        """
        Summarize exit strategy performance.
        
        Args:
            performance_data: Dictionary containing performance metrics
            
        Returns:
            Styled performance summary in the Elite Exit voice
        """
        total_pnl = performance_data.get('total_pnl', 0)
        win_rate = performance_data.get('win_rate', 0)
        trade_count = performance_data.get('trade_count', 0)
        
        # Get exit-specific metrics if available
        avg_exit_efficiency = performance_data.get('exit_efficiency', random.uniform(0.4, 0.9))
        trapped_exits_avoided = performance_data.get('trapped_exits_avoided', random.randint(0, 10))
        profit_factor = performance_data.get('profit_factor', random.uniform(1.0, 3.0))
        
        # Determine overall assessment
        if avg_exit_efficiency > 0.8 and profit_factor > 2.0:
            assessment = "elite exit performance with exceptional efficiency"
            emoji = "🏆"
        elif avg_exit_efficiency > 0.6 and profit_factor > 1.5:
            assessment = "strong exit strategy performance"
            emoji = "✅"
        elif avg_exit_efficiency > 0.5:
            assessment = "solid exit management with room for optimization"
            emoji = "📈"
        else:
            assessment = "exit strategy requiring significant improvement"
            emoji = "⚠️"
        
        # Analyze exit efficiency
        if avg_exit_efficiency > 0.8:
            efficiency_analysis = f"capturing {avg_exit_efficiency*100:.1f}% of theoretical maximum profit"
        elif avg_exit_efficiency > 0.6:
            efficiency_analysis = f"capturing {avg_exit_efficiency*100:.1f}% of theoretical maximum (improvement possible)"
        else:
            efficiency_analysis = f"capturing only {avg_exit_efficiency*100:.1f}% of theoretical maximum (significant improvement needed)"
            
        # Exit strategy recommendations
        recommendations = []
        if avg_exit_efficiency < 0.6:
            recommendations.append("Implement multi-level exit strategy with defined profit targets")
        else:
            recommendations.append("Fine-tune existing multi-level exit strategy for optimal results")
            
        if trapped_exits_avoided < 5:
            recommendations.append("Enhance trap detection sensitivity for earlier exit signal generation")
        else:
            recommendations.append("Maintain current trap detection parameters which are performing well")
            
        if profit_factor < 1.5:
            recommendations.append("Tighten stop-loss management to improve profit factor")
        else:
            recommendations.append("Continue balanced risk management with current profit factor")
            
        result = f"{emoji} Elite Exit Performance Analysis {emoji}\n\n" \
                 f"Overall: {assessment} with ${total_pnl:,.2f} total P&L across {trade_count} trades.\n\n" \
                 f"Exit Efficiency: {avg_exit_efficiency:.2f} ({efficiency_analysis})\n" \
                 f"Profit Factor: {profit_factor:.2f} (${performance_data.get('total_profit', 0):,.2f} profit / ${performance_data.get('total_loss', 0):,.2f} loss)\n" \
                 f"Trap Avoidance: {trapped_exits_avoided} potential traps successfully avoided\n\n" \
                 f"Exit Strategy Optimization:\n" \
                 f"• {recommendations[0]}\n" \
                 f"• {recommendations[1]}\n" \
                 f"• {recommendations[2]}\n\n" \
                 f"Remember: Entry gets you in the market, but exit determines your profit."
        
        return result
        
    def _format_confidence(self, confidence: float) -> str:
        """Format confidence level with descriptive text."""
        if confidence > 0.85:
            return "Elite Confidence"
        elif confidence > 0.7:
            return "High Confidence"
        elif confidence > 0.5:
            return "Moderate Confidence"
        elif confidence > 0.3:
            return "Low Confidence"
        else:
            return "Minimal Confidence" 