"""
Fibonacci Strategist Persona - a golden-ratio-guided trader for the OMEGA BTC AI system.

This persona analyzes market movements through the lens of Fibonacci mathematics
and golden ratio harmonics, offering insights based on precise mathematical relationships.
"""

import random
from typing import Dict, Any, List, Optional
import math

from omega_ai.personification.persona_base import BasePersona, PersonaStyle, TradingMood


class FibStrategistPersona(BasePersona):
    """
    Fibonacci Strategist persona - provides market guidance through Fibonacci mathematics.
    
    This persona sees the market as a mathematical harmony, with price movements following
    precise Fibonacci retracement and extension levels. Speaks with wisdom about golden ratio
    principles and natural mathematical order in market movements.
    """
    
    def __init__(self):
        """Initialize the Fibonacci Strategist persona with style elements."""
        style = PersonaStyle(
            primary_color="#FFD700",  # Gold
            secondary_color="#E6E6FA",  # Lavender
            accent_color="#8A2BE2",  # BlueViolet
            font_family="'Quicksand', 'Helvetica Neue', sans-serif",
            avatar_url="/assets/images/personas/fib_strategist_avatar.png",
            background_pattern="/assets/images/patterns/fib_spiral_pattern.png",
            icons={
                "bullish": "/assets/icons/golden_up.svg",
                "bearish": "/assets/icons/golden_down.svg",
                "neutral": "/assets/icons/golden_balanced.svg",
                "alert": "/assets/icons/golden_alert.svg",
                "suggestion": "/assets/icons/golden_idea.svg"
            }
        )
        
        super().__init__(
            name="Fibonacci Strategist",
            description="A mathematical market navigator who sees trading through the lens of "
                       "Fibonacci sequences and golden ratio proportions. Offers insights based "
                       "on precise mathematical relationships in price action.",
            style=style
        )
        
        # Golden ratio constants
        self.PHI = (1 + math.sqrt(5)) / 2  # The golden ratio (approx 1.618)
        self.INV_PHI = 1 / self.PHI  # Inverse golden ratio (approx 0.618)
        
        # Fibonacci levels
        self.fib_levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618, 2.618]
        
        # Vocabulary
        self.golden_terms = [
            "divine proportion",
            "golden spiral",
            "Fibonacci harmony",
            "mathematical perfection",
            "sacred geometry",
            "natural order",
            "cosmic balance",
            "harmonic resonance",
            "ratio convergence",
            "mathematical rhythm"
        ]
        
        self.greetings = [
            f"Greetings. The markets flow in {self.PHI:.3f} harmony today.",
            "Welcome to the mathematical order of market movements.",
            "The Fibonacci sequence reveals the path forward.",
            f"The {self.INV_PHI:.3f} and {self.PHI:.3f} ratios guide us today.",
            "Divine proportion insights are ready for your analysis."
        ]
    
    def get_greeting(self) -> str:
        """Get a randomized Fibonacci-themed greeting."""
        return random.choice(self.greetings)
    
    def analyze_position(self, position_data: Dict[str, Any]) -> str:
        """
        Analyze trading position with Fibonacci mathematics.
        
        Args:
            position_data: Dictionary containing position information
            
        Returns:
            Styled analysis text in the Fibonacci Strategist voice
        """
        side = position_data.get('side', 'unknown')
        entry_price = position_data.get('entry_price', 0)
        current_price = position_data.get('current_price', 0)
        pnl = position_data.get('pnl', 0)
        pnl_percentage = position_data.get('pnl_percentage', 0)
        symbol = position_data.get('symbol', 'BTC')
        
        # Calculate price movement percentage
        price_change_pct = ((current_price - entry_price) / entry_price) * 100
        nearest_fib = self._get_nearest_fib_level(abs(price_change_pct) / 100)
        
        # Price targets based on Fibonacci extensions
        targets = self._calculate_fib_targets(entry_price, side)
        
        # Determine position health
        is_profitable = pnl > 0
        
        # Icon based on status
        if is_profitable:
            status_icon = "✓"
            status_desc = "harmonizing with projected levels"
        else:
            status_icon = "⚠"
            status_desc = "experiencing temporary dissonance"
        
        # Generate analysis
        result = f"📊 POSITION ANALYSIS: {side.upper()} {symbol} | {status_icon}\n\n"
        
        result += f"Entry: ${entry_price:,.2f} | Current: ${current_price:,.2f}\n"
        result += f"Movement: {price_change_pct:+.2f}% ({self._get_fib_descriptor(nearest_fib)} zone)\n"
        result += f"P&L: ${pnl:,.2f} ({pnl_percentage:+.2f}%)\n\n"
        
        result += f"Your position is {status_desc}. "
        
        # Add Fibonacci insight
        if side == 'long':
            if is_profitable:
                next_target = self._get_next_target(current_price, targets)
                result += f"The price is advancing through the Fibonacci sequence, with next resonance at ${next_target:,.2f}. "
                result += f"This represents the {self._get_fib_level_for_price(next_target, entry_price, side)} extension level.\n\n"
            else:
                nearest_support = self._get_nearest_support(current_price, entry_price)
                result += f"Price has retraced to test mathematical support. The key Fibonacci equilibrium level is at ${nearest_support:,.2f}. "
                result += f"This represents the {self._get_fib_level_for_price(nearest_support, entry_price, side)} retracement.\n\n"
        else:  # short
            if is_profitable:
                next_target = self._get_next_target(current_price, targets, is_short=True)
                result += f"The price is descending through the Fibonacci sequence, with next resonance at ${next_target:,.2f}. "
                result += f"This represents the {self._get_fib_level_for_price(next_target, entry_price, side)} extension level.\n\n"
            else:
                nearest_resistance = self._get_nearest_resistance(current_price, entry_price)
                result += f"Price has retraced to test mathematical resistance. The key Fibonacci barrier is at ${nearest_resistance:,.2f}. "
                result += f"This represents the {self._get_fib_level_for_price(nearest_resistance, entry_price, side)} countertrend level.\n\n"
        
        # Add recommendation
        result += "FIBONACCI GUIDANCE:\n"
        result += self._get_position_recommendation(position_data, targets)
        
        return result
    
    def analyze_market(self, market_data: Dict[str, Any]) -> str:
        """
        Analyze market conditions through Fibonacci mathematical lens.
        
        Args:
            market_data: Dictionary containing market information
            
        Returns:
            Styled market analysis text in the Fibonacci Strategist voice
        """
        # Update mood based on market data
        self.update_mood(market_data)
        
        current_price = market_data.get('price', 0)
        change_24h = market_data.get('price_change_24h', 0)
        high = market_data.get('high_24h', current_price * 1.01)
        low = market_data.get('low_24h', current_price * 0.99)
        volume = market_data.get('volume_24h', 0)
        
        # Calculate key Fibonacci levels from recent high/low range
        range_size = high - low
        fib_levels = {
            "0": low,
            "0.236": low + (range_size * 0.236),
            "0.382": low + (range_size * 0.382),
            "0.5": low + (range_size * 0.5),
            "0.618": low + (range_size * 0.618),
            "0.786": low + (range_size * 0.786),
            "1.0": high,
            "1.618": high + (range_size * 0.618)
        }
        
        # Find current price location relative to the Fibonacci levels
        current_fib = "unknown"
        next_fib_up = "unknown"
        next_fib_down = "unknown"
        next_fib_up_price = 0
        next_fib_down_price = 0
        
        sorted_levels = sorted([(float(k), v) for k, v in fib_levels.items()], key=lambda x: x[1])
        
        for i, (level, price) in enumerate(sorted_levels):
            if price > current_price and (next_fib_up == "unknown" or price < next_fib_up_price):
                next_fib_up = str(level)
                next_fib_up_price = price
            if price < current_price and (next_fib_down == "unknown" or price > next_fib_down_price):
                next_fib_down = str(level)
                next_fib_down_price = price
                
            # Identify current position between two levels
            if i < len(sorted_levels) - 1:
                next_level, next_price = sorted_levels[i+1]
                if price <= current_price <= next_price:
                    fib_range = next_price - price
                    if fib_range > 0:
                        position_pct = (current_price - price) / fib_range
                        current_fib = f"between {level} and {next_level} ({position_pct:.1%} of range)"
                    
        # Generate market analysis
        direction_marker = "▲" if change_24h > 0 else "▼"
        
        result = f"{direction_marker} FIBONACCI MARKET ANALYSIS: BTC/USD @ ${current_price:,.2f}\n\n"
        
        result += f"24h Movement: {change_24h:+.2f}% | Volume: ${volume:,.0f}\n\n"
        
        # Current location between Fibonacci levels
        result += f"FIBONACCI POSITION: {current_fib}\n"
        result += f"Next resistance: {next_fib_up} @ ${next_fib_up_price:,.2f}\n"
        result += f"Next support: {next_fib_down} @ ${next_fib_down_price:,.2f}\n\n"
        
        # Golden ratio commentary
        result += "MATHEMATICAL HARMONY ASSESSMENT:\n"
        
        # Commentary based on where price is in the Fibonacci sequence
        if "0.618" in current_fib or "0.5" in current_fib:
            result += f"Price is currently at a golden equilibrium zone. The {self.INV_PHI:.3f} level is a natural point of balance.\n\n"
        elif "0.786" in current_fib:
            result += f"Price has retraced deeply to the 0.786 level, suggesting potential for a stronger reversal.\n\n"
        elif "0.382" in current_fib or "0.236" in current_fib:
            result += f"Price is at a shallow retracement level, indicating strength in the overall trend.\n\n"
        else:
            result += "Price is between primary Fibonacci levels, seeking mathematical harmony.\n\n"
        
        # Market structure based on mood
        if self.current_mood in [TradingMood.EXTREMELY_BULLISH, TradingMood.BULLISH]:
            result += "Market structure shows golden ratio expansion on higher timeframes. "
            result += f"Watch for continuation toward the {self.PHI:.3f} extension at ${fib_levels['1.618']:,.2f}.\n\n"
        elif self.current_mood in [TradingMood.SLIGHTLY_BULLISH, TradingMood.NEUTRAL]:
            result += "Market structure exhibits balanced Fibonacci energy. "
            result += f"Watch for convergence toward the {self.INV_PHI:.3f} level at ${fib_levels['0.618']:,.2f}.\n\n"
        else:
            result += "Market structure shows Fibonacci contraction. "
            result += f"Watch for support tests at the 0.382 and 0.236 levels.\n\n"
        
        # Trading suggestion
        result += "MATHEMATICAL TRADING GUIDANCE:\n"
        
        if next_fib_up_price - current_price < current_price - next_fib_down_price:
            result += f"Favorable risk-reward for long positions targeting the {next_fib_up} level with precise stop placement at the {next_fib_down} support."
        else:
            result += f"Mathematical precision suggests waiting for a retest of the {next_fib_down} support before establishing a new position."
            
        return result
    
    def generate_recommendation(self, data: Dict[str, Any]) -> str:
        """
        Generate trading recommendations based on Fibonacci mathematics.
        
        Args:
            data: Dictionary containing relevant trading data
            
        Returns:
            Styled recommendation text in the Fibonacci Strategist voice
        """
        price = data.get('price', 0)
        trend = data.get('trend', 'neutral')
        strength = data.get('signal_strength', 0.5)
        
        # Calculate Fibonacci entry and target levels
        high = data.get('recent_high', price * 1.05)
        low = data.get('recent_low', price * 0.95)
        range_size = high - low
        
        # Entry levels based on Fibonacci retracements
        if trend == 'bullish':
            entry_level_shallow = high - (range_size * 0.382)
            entry_level_optimal = high - (range_size * 0.618)
            entry_level_deep = high - (range_size * 0.786)
            
            # Target levels based on Fibonacci extensions
            target_1 = high + (range_size * 0.382)
            target_2 = high + (range_size * 0.618)
            target_3 = high + (range_size * 1.0)
            
            # Stop loss based on Fibonacci
            stop_loss = high - (range_size * 1.0)
            
        else:  # bearish or neutral (default to bearish calculation)
            entry_level_shallow = low + (range_size * 0.382)
            entry_level_optimal = low + (range_size * 0.618)
            entry_level_deep = low + (range_size * 0.786)
            
            # Target levels based on Fibonacci extensions
            target_1 = low - (range_size * 0.382)
            target_2 = low - (range_size * 0.618)
            target_3 = low - (range_size * 1.0)
            
            # Stop loss based on Fibonacci
            stop_loss = low + (range_size * 1.0)
        
        # Determine recommendation based on current price relative to Fibonacci levels
        if trend == 'bullish':
            if price <= entry_level_deep:
                action = "BUY"
                entry_quality = "deep value 0.786 Fibonacci accumulation zone"
                emoji = "🟢🟢🟢"
            elif price <= entry_level_optimal:
                action = "BUY"
                entry_quality = "optimal 0.618 golden ratio entry zone"
                emoji = "🟢🟢"
            elif price <= entry_level_shallow:
                action = "BUY"
                entry_quality = "shallow 0.382 Fibonacci entry zone"
                emoji = "🟢"
            else:
                action = "AWAIT RETRACEMENT"
                entry_quality = "extended price beyond optimal Fibonacci entry zones"
                emoji = "⏳"
        else:  # bearish
            if price >= entry_level_deep:
                action = "SELL"
                entry_quality = "deep value 0.786 Fibonacci distribution zone"
                emoji = "🔴🔴🔴"
            elif price >= entry_level_optimal:
                action = "SELL"
                entry_quality = "optimal 0.618 golden ratio entry zone"
                emoji = "🔴🔴"
            elif price >= entry_level_shallow:
                action = "SELL"
                entry_quality = "shallow 0.382 Fibonacci entry zone"
                emoji = "🔴"
            else:
                action = "AWAIT RETRACEMENT"
                entry_quality = "extended price beyond optimal Fibonacci entry zones"
                emoji = "⏳"
        
        # Generate recommendation
        result = f"{emoji} FIBONACCI TRADE RECOMMENDATION: {action} {emoji}\n\n"
        
        result += f"BTC/USD at ${price:,.2f} presents {entry_quality}.\n"
        result += f"Signal strength: {int(strength * 100)}% | Trend: {trend.upper()}\n\n"
        
        result += f"FIBONACCI LEVELS ANALYSIS:\n"
        
        # Add Fibonacci levels based on trend
        if trend == 'bullish':
            result += f"• Entry Zone: ${entry_level_optimal:,.2f} (0.618 retracement)\n"
            result += f"• Target 1: ${target_1:,.2f} (0.382 extension)\n"
            result += f"• Target 2: ${target_2:,.2f} (0.618 extension)\n"
            result += f"• Target 3: ${target_3:,.2f} (1.0 extension)\n"
            result += f"• Stop Loss: ${stop_loss:,.2f} (1.0 retracement)\n\n"
        else:
            result += f"• Entry Zone: ${entry_level_optimal:,.2f} (0.618 retracement)\n"
            result += f"• Target 1: ${target_1:,.2f} (0.382 extension)\n"
            result += f"• Target 2: ${target_2:,.2f} (0.618 extension)\n"
            result += f"• Target 3: ${target_3:,.2f} (1.0 extension)\n"
            result += f"• Stop Loss: ${stop_loss:,.2f} (1.0 retracement)\n\n"
        
        # Calculate risk/reward
        risk = abs(price - stop_loss)
        reward = abs(target_2 - price)
        rr_ratio = reward / risk if risk > 0 else 0
        
        result += f"MATHEMATICAL PRECISION:\n"
        result += f"• Risk:Reward Ratio: 1:{rr_ratio:.2f}\n"
        result += f"• Golden Ratio Target: ${price * (1 + (0.618 if trend == 'bullish' else -0.618)):,.2f}\n"
        result += f"• Position Sizing: {self._calculate_ideal_position_size(rr_ratio)}% of capital\n\n"
        
        # Add warning if trap probability is high
        trap_probability = data.get('trap_probability', 0)
        if trap_probability > 0.5:
            result += f"⚠️ CAUTION: Detected {trap_probability*100:.0f}% probability of market manipulation. "
            result += f"Consider reducing position size by Fibonacci ratio 0.618.\n\n"
        
        # Final recommendation
        result += "STRATEGIC GUIDANCE:\n"
        if action in ["BUY", "SELL"]:
            result += f"Enter {action.lower()} position at current price with precise Fibonacci-based targets. "
            result += f"Scale out at each target level using 38.2%, 61.8%, and 100% of position size, respectively."
        else:
            result += f"Wait for price to reach the optimal Fibonacci entry zone at ${entry_level_optimal:,.2f} before establishing position. "
            result += f"Patience aligns with the mathematical harmony of markets."
            
        return result
    
    def summarize_performance(self, performance_data: Dict[str, Any]) -> str:
        """
        Summarize trading performance through Fibonacci mathematical lens.
        
        Args:
            performance_data: Dictionary containing performance metrics
            
        Returns:
            Styled performance summary in the Fibonacci Strategist voice
        """
        total_pnl = performance_data.get('total_pnl', 0)
        win_rate = performance_data.get('win_rate', 0)
        trade_count = performance_data.get('trade_count', 0)
        avg_win = performance_data.get('avg_win', 0)
        avg_loss = performance_data.get('avg_loss', 0)
        
        # Calculate Fibonacci-relevant metrics
        win_loss_ratio = avg_win / abs(avg_loss) if avg_loss != 0 else float('inf')
        golden_win_ratio = self.PHI  # Ideal win/loss ratio equals the golden ratio (1.618)
        golden_win_rate = self.INV_PHI  # Minimum win rate needed (0.618)
        
        # Compare actual performance to Fibonacci ideals
        win_ratio_alignment = min(1.0, win_loss_ratio / golden_win_ratio) * 100
        win_rate_alignment = min(1.0, win_rate / golden_win_rate) * 100 if golden_win_rate > 0 else 0
        
        # Calculate Fibonacci-based performance score (0-100)
        fib_score = (win_ratio_alignment + win_rate_alignment) / 2
        
        # Performance rating
        if fib_score >= 90:
            rating = "GOLDEN HARMONY"
            emoji = "🌟"
        elif fib_score >= 75:
            rating = "DIVINE PROPORTION"
            emoji = "✨"
        elif fib_score >= 60:
            rating = "MATHEMATICAL BALANCE"
            emoji = "⚖️"
        elif fib_score >= 40:
            rating = "APPROACHING ALIGNMENT"
            emoji = "📐"
        else:
            rating = "REQUIRES REFINEMENT"
            emoji = "📝"
            
        # Generate summary
        result = f"{emoji} FIBONACCI PERFORMANCE ANALYSIS: {rating} {emoji}\n\n"
        
        result += f"Total P&L: ${total_pnl:,.2f} | Trades: {trade_count}\n"
        result += f"Win Rate: {win_rate*100:.1f}% | Golden Ratio Win Rate: {golden_win_rate*100:.1f}%\n"
        result += f"Win/Loss Ratio: {win_loss_ratio:.2f} | Golden Ratio: {golden_win_ratio:.3f}\n\n"
        
        result += f"MATHEMATICAL HARMONY SCORE: {fib_score:.1f}/100\n\n"
        
        # Performance insights
        result += "FIBONACCI INSIGHTS:\n"
        
        if win_rate < golden_win_rate:
            ratio_deficit = golden_win_rate - win_rate
            result += f"• Win rate is {ratio_deficit*100:.1f}% below golden ratio threshold of {golden_win_rate*100:.1f}%.\n"
            result += f"• Recommendation: Improve entry precision using the 0.618 retracement level for enhanced accuracy.\n"
        else:
            result += f"• Win rate exceeds golden ratio threshold of {golden_win_rate*100:.1f}%. Mathematically optimal.\n"
            
        if win_loss_ratio < golden_win_ratio:
            ratio_deficit = golden_win_ratio - win_loss_ratio
            result += f"• Win/Loss ratio is {ratio_deficit:.2f} below golden ratio target of {golden_win_ratio:.3f}.\n"
            result += f"• Recommendation: Extend profit targets to 1.618 Fibonacci extension and tighten stop losses to 0.382 retracement.\n"
        else:
            result += f"• Win/Loss ratio exceeds golden ratio target of {golden_win_ratio:.3f}. Mathematically optimal.\n\n"
        
        # Strategy recommendations
        result += "STRATEGY REFINEMENT:\n"
        
        if total_pnl > 0:
            result += f"• Current strategy shows positive mathematical alignment. Maintain Fibonacci-based entries and exits.\n"
            result += f"• Consider scaling position size by factor of {self.PHI:.3f} to optimize return metrics.\n"
        else:
            result += f"• Current strategy requires mathematical recalibration. Adjust to emphasize entries at 0.618 and 0.786 retracement levels.\n"
            result += f"• Consider reducing position size by factor of {self.INV_PHI:.3f} until alignment improves.\n"
        
        result += f"• Implement precise take-profit levels at 0.382, 0.618, and 1.0 Fibonacci extensions for optimal profit harvesting.\n"
        
        return result
    
    def _get_nearest_fib_level(self, ratio: float) -> float:
        """Find the nearest Fibonacci level to a given ratio."""
        return min(self.fib_levels, key=lambda x: abs(x - ratio))
    
    def _get_fib_descriptor(self, level: float) -> str:
        """Get a descriptive name for a Fibonacci level."""
        if level == 0:
            return "base"
        elif level == 0.236:
            return "shallow retracement"
        elif level == 0.382:
            return "moderate retracement"
        elif level == 0.5:
            return "midpoint balance"
        elif level == 0.618:
            return "golden ratio"
        elif level == 0.786:
            return "deep retracement"
        elif level == 1.0:
            return "full cycle"
        elif level == 1.618:
            return "golden extension"
        elif level == 2.618:
            return "extended projection"
        else:
            return f"{level} ratio"
    
    def _calculate_fib_targets(self, entry_price: float, side: str) -> Dict[str, float]:
        """Calculate Fibonacci-based price targets."""
        # For simplicity, we'll use some basic assumptions for the price range
        if side == 'long':
            targets = {
                "0.382": entry_price * 1.0382,
                "0.618": entry_price * 1.0618,
                "0.786": entry_price * 1.0786,
                "1.0": entry_price * 1.1,
                "1.618": entry_price * 1.1618
            }
        else:  # short
            targets = {
                "0.382": entry_price * 0.9618,
                "0.618": entry_price * 0.9382,
                "0.786": entry_price * 0.9214,
                "1.0": entry_price * 0.9,
                "1.618": entry_price * 0.8382
            }
            
        return targets
    
    def _get_next_target(self, current_price: float, targets: Dict[str, float], is_short: bool = False) -> float:
        """Get the next Fibonacci target level."""
        if is_short:
            next_target = min([t for t in targets.values() if t < current_price], default=current_price * 0.95)
        else:
            next_target = min([t for t in targets.values() if t > current_price], default=current_price * 1.05)
            
        return next_target
    
    def _get_nearest_support(self, current_price: float, entry_price: float) -> float:
        """Calculate the nearest Fibonacci support level."""
        price_diff = abs(entry_price - current_price)
        return current_price - (price_diff * self.INV_PHI)
    
    def _get_nearest_resistance(self, current_price: float, entry_price: float) -> float:
        """Calculate the nearest Fibonacci resistance level."""
        price_diff = abs(entry_price - current_price)
        return current_price + (price_diff * self.INV_PHI)
    
    def _get_fib_level_for_price(self, price: float, entry_price: float, side: str) -> str:
        """Get the Fibonacci level name for a given price."""
        diff_pct = abs((price - entry_price) / entry_price)
        nearest = self._get_nearest_fib_level(diff_pct)
        return self._get_fib_descriptor(nearest)
    
    def _get_position_recommendation(self, position_data: Dict[str, Any], targets: Dict[str, float]) -> str:
        """Generate a position-specific recommendation."""
        side = position_data.get('side', 'unknown')
        pnl = position_data.get('pnl', 0)
        current_price = position_data.get('current_price', 0)
        
        # Find the nearest target
        if side == 'long':
            next_target = self._get_next_target(current_price, targets)
        else:
            next_target = self._get_next_target(current_price, targets, is_short=True)
        
        # Generate recommendation
        if pnl > 0:
            return (f"• Price is advancing toward the next Fibonacci target at ${next_target:,.2f}.\n"
                    f"• Consider taking partial profits at each Fibonacci level: 38.2% at first target, "
                    f"61.8% at second target, and remaining position at final target.\n"
                    f"• Adjust stop loss to maintain golden ratio (1.618) risk-reward balance.")
        else:
            return (f"• Price is currently below ideal trajectory toward Fibonacci targets.\n"
                    f"• Watch for reversal at the {self.INV_PHI:.3f} retracement level.\n"
                    f"• If price holds above the 0.786 retracement level, maintain position. "
                    f"Otherwise, consider reevaluating position sizing according to the Fibonacci sequence.")
    
    def _calculate_ideal_position_size(self, risk_reward_ratio: float) -> float:
        """Calculate ideal position size based on Fibonacci principles."""
        # Base position size on risk-reward ratio relative to golden ratio
        if risk_reward_ratio >= self.PHI:
            # Better than golden ratio - can use larger size
            return 3.0  # Fibonacci number
        elif risk_reward_ratio >= 1.0:
            # Good risk-reward, but not optimal
            return 2.0  # Fibonacci number
        else:
            # Poor risk-reward
            return 1.0  # Fibonacci number 