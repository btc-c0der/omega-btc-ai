"""
Rastafarian Oracle Persona - a spiritual guide for the OMEGA BTC AI trading system.

This persona speaks with Jamaican dialect influences and offers wisdom through
a lens of spiritual connection, divine alignment, and natural harmony.
"""

import random
from typing import Dict, Any, List, Optional
import re

from omega_ai.personification.persona_base import BasePersona, PersonaStyle, TradingMood


class RastaOraclePersona(BasePersona):
    """
    Rastafarian Oracle persona - provides market guidance with spiritual wisdom.
    
    This persona speaks with Jamaican dialect influences and frames market events
    in terms of spiritual balance, natural rhythms, and divine guidance.
    """
    
    def __init__(self):
        """Initialize the Rasta Oracle persona with Rastafarian style elements."""
        style = PersonaStyle(
            primary_color="#4CAF50",  # Green 
            secondary_color="#FBC02D",  # Gold/Yellow
            accent_color="#BF360C",  # Dark red/clay
            font_family="'Montserrat', 'Open Sans', sans-serif",
            avatar_url="/assets/images/personas/rasta_oracle_avatar.png",
            background_pattern="/assets/images/patterns/rasta_pattern.png",
            icons={
                "positive": "/assets/icons/leaf_up.svg",
                "negative": "/assets/icons/leaf_down.svg",
                "neutral": "/assets/icons/leaf.svg",
                "alert": "/assets/icons/drum.svg",
                "suggestion": "/assets/icons/lion.svg"
            }
        )
        
        super().__init__(
            name="Rasta Oracle",
            description="A spiritual guide who interprets market movements through "
                       "divine rhythms and natural harmony. Speaks with Jamaican "
                       "dialect influences and focuses on long-term balance.",
            style=style
        )
        
        # Special vocabulary for this persona
        self.common_phrases = [
            "JAH bless",
            "I and I",
            "sight?",
            "irie",
            "one love",
            "give thanks",
            "guidance",
            "divine rhythm",
            "true-true",
            "overstand",
            "high vibration",
            "righteous path",
            "Babylon system",
            "divine alignment"
        ]
        
        self.positive_phrases = [
            "JAH blessing flowing through the market",
            "divine harmony revealing itself",
            "the divine pattern emerges",
            "following the righteous path upward",
            "cosmic energy lifting the vibration",
            "market finding its natural balance",
            "higher consciousness bringing green lights"
        ]
        
        self.negative_phrases = [
            "Babylon confusion in the market",
            "temporary downpression testing faith",
            "market need purification before rising again",
            "red days cleanse the spirit for new growth",
            "negative vibrations testing resolve",
            "false prophets creating downward pressure"
        ]
        
        self.greetings = [
            "JAH BLESS, I and I bring wisdom from the higher realms",
            "Greetings, divine one. The Oracle channels market vibrations",
            "ONE LOVE! The Oracle sees patterns in the cosmic flow",
            "Blessings overflow! I and I bring market guidance today",
            "JAH guide I and I in these market readings today"
        ]
    
    def get_greeting(self) -> str:
        """Get a randomized Rastafarian greeting."""
        return random.choice(self.greetings)
    
    def analyze_position(self, position_data: Dict[str, Any]) -> str:
        """
        Analyze trading position with spiritual Rastafarian wisdom.
        
        Args:
            position_data: Dictionary containing position information
            
        Returns:
            Styled analysis text in the Rasta Oracle voice
        """
        side = position_data.get('side', 'unknown')
        entry_price = position_data.get('entry_price', 0)
        current_price = position_data.get('current_price', 0)
        pnl = position_data.get('pnl', 0)
        
        # Calculate if the position is in profit or loss
        is_profitable = pnl > 0
        
        # Get emoji based on position type and profitability
        if side == 'long':
            direction_emoji = "🌱" if is_profitable else "🍁"
            direction_term = "upward divine path" if is_profitable else "testing patience"
        else:  # short
            direction_emoji = "🍁" if is_profitable else "🌱"
            direction_term = "Babylon falling" if is_profitable else "false prophet rising"
        
        # Get a random phrase based on the position's status
        phrase = random.choice(self.positive_phrases if is_profitable else self.negative_phrases)
        
        # Add JAH BLESS if profitable
        blessing = "JAH BLESS! " if is_profitable else ""
        
        # Format the response
        result = f"{blessing}{direction_emoji} I and I see the {position_data.get('symbol', 'BTC')} " \
                 f"position on a {direction_term}.\n\n" \
                 f"The divine seed was planted at ${entry_price:,.2f} and now " \
                 f"grows at ${current_price:,.2f}.\n\n" \
                 f"{phrase}.\n\n" \
                 f"Current vibration: {self._format_pnl(pnl)}. " \
                 f"I and I {self._get_advice(position_data)}."
                 
        return self._rastalify(result)
    
    def analyze_market(self, market_data: Dict[str, Any]) -> str:
        """
        Analyze market conditions with spiritual Rastafarian perspective.
        
        Args:
            market_data: Dictionary containing market information
            
        Returns:
            Styled market analysis text in the Rasta Oracle voice
        """
        # Update mood based on market data
        self.update_mood(market_data)
        
        current_price = market_data.get('price', 0)
        change_24h = market_data.get('price_change_24h', 0)
        volume = market_data.get('volume_24h', 0)
        
        # Determine if the market is up or down
        market_direction = "rising" if change_24h > 0 else "falling"
        
        # Select directional emoji
        if change_24h > 5:
            direction_emoji = "🌿🌿🌿"
        elif change_24h > 0:
            direction_emoji = "🌿"
        elif change_24h > -5:
            direction_emoji = "🍁"
        else:
            direction_emoji = "🍁🍁🍁"
        
        # Volume interpretation
        if volume > 10000000000:  # high volume
            volume_desc = "massive rivers of energy flowing"
        elif volume > 5000000000:  # medium volume
            volume_desc = "steady streams of consciousness"
        else:  # low volume
            volume_desc = "gentle trickles of vibration"
        
        # Phrase selection based on mood
        if self.current_mood in [TradingMood.EXTREMELY_BULLISH, TradingMood.BULLISH]:
            mood_phrase = "The divine energy overflows with positivity"
        elif self.current_mood in [TradingMood.SLIGHTLY_BULLISH, TradingMood.NEUTRAL]:
            mood_phrase = "Balance is present in the cosmic market forces"
        else:
            mood_phrase = "Babylon confusion testing the faithful"
            
        result = f"{direction_emoji} I and I observe BTC at ${current_price:,.2f} on the {market_direction} path.\n\n" \
                 f"The 24-hour rhythm shows {self._format_percentage(change_24h)} vibration, with {volume_desc}.\n\n" \
                 f"{mood_phrase}. The Oracle sees {self._get_future_vision(market_data)}.\n\n" \
                 f"JAH guide all traders in these times."
        
        return self._rastalify(result)
    
    def generate_recommendation(self, data: Dict[str, Any]) -> str:
        """
        Generate trading recommendations with Rastafarian spiritual guidance.
        
        Args:
            data: Dictionary containing relevant trading data
            
        Returns:
            Styled recommendation text in the Rasta Oracle voice
        """
        price = data.get('price', 0)
        trend = data.get('trend', 'neutral')
        strength = data.get('signal_strength', 0.5)
        
        # Determine recommended action
        if trend == 'bullish' and strength > 0.7:
            action = "plant seeds in the fertile soil"
            direction = "upward"
            emoji = "🌱"
        elif trend == 'bullish' and strength > 0.3:
            action = "consider nurturing small growth"
            direction = "gentle upward"
            emoji = "🍃"
        elif trend == 'bearish' and strength > 0.7:
            action = "harvest what you've grown before the storm"
            direction = "downward"
            emoji = "🍂"
        elif trend == 'bearish' and strength > 0.3:
            action = "protect your garden from possible frost"
            direction = "cooling"
            emoji = "🍁"
        else:
            action = "remain in meditation and observation"
            direction = "balanced"
            emoji = "☯️"
        
        # Format strength as stars
        stars = "⭐" * int(strength * 5)
        
        # Add fib reference if available
        fib_reference = ""
        if data.get('fib_level'):
            fib_reference = f"The divine Fibonacci spirits speak of the {data.get('fib_level')} level at ${data.get('fib_price', 0):,.2f}. "
        
        # Trap reference if available
        trap_reference = ""
        if data.get('trap_probability', 0) > 0.5:
            trap_probability = data.get('trap_probability', 0)
            trap_reference = f"I and I warn of Babylon trickery with {trap_probability*100:.0f}% trap vibrations. "
        
        result = f"{emoji} Divine Market Guidance for BTC at ${price:,.2f}\n\n" \
                 f"The Oracle feels a {direction} rhythm with {stars} strength.\n\n" \
                 f"I and I suggest you {action}.\n\n" \
                 f"{fib_reference}{trap_reference}\n\n" \
                 f"Remember, each trade be part of your spiritual journey. JAH BLESS your path."
                 
        return self._rastalify(result)
    
    def summarize_performance(self, performance_data: Dict[str, Any]) -> str:
        """
        Summarize trading performance with Rastafarian spiritual perspective.
        
        Args:
            performance_data: Dictionary containing performance metrics
            
        Returns:
            Styled performance summary in the Rasta Oracle voice
        """
        total_pnl = performance_data.get('total_pnl', 0)
        win_rate = performance_data.get('win_rate', 0)
        trade_count = performance_data.get('trade_count', 0)
        
        # Determine overall sentiment
        if total_pnl > 1000:
            sentiment = "overwhelming blessings"
            emoji = "🦁"
        elif total_pnl > 100:
            sentiment = "righteous prosperity"
            emoji = "🌿"
        elif total_pnl > 0:
            sentiment = "gentle growth"
            emoji = "🌱"
        elif total_pnl > -100:
            sentiment = "small trials for learning"
            emoji = "🍃"
        else:
            sentiment = "challenging lessons from JAH"
            emoji = "🍁"
        
        # Interpret win rate
        if win_rate > 0.7:
            win_desc = "divine harmony with the market rhythms"
        elif win_rate > 0.5:
            win_desc = "favorable flow with the cosmic currents"
        else:
            win_desc = "wisdom being forged through challenges"
            
        result = f"{emoji} Trading Harvest Report {emoji}\n\n" \
                 f"I and I witness {sentiment} with ${total_pnl:,.2f} total fruits.\n\n" \
                 f"Through {trade_count} market journeys, you've shown {win_desc} " \
                 f"({win_rate*100:.1f}% victories).\n\n"
        
        # Add wisdom based on performance
        if total_pnl > 0:
            result += "Give thanks for the abundance! Remember to share blessings with others.\n\n"
        else:
            result += "Every downpression is a test of faith. The divine path has valleys and peaks.\n\n"
            
        result += f"JAH BLESS your continued journey through the markets. One love! 🟢🟡🔴"
        
        return self._rastalify(result)
    
    def _format_pnl(self, pnl: float) -> str:
        """Format PnL with Rastafarian spiritual meaning."""
        if pnl > 1000:
            return f"highest blessings of ${pnl:,.2f}"
        elif pnl > 100:
            return f"divine prosperity of ${pnl:,.2f}"
        elif pnl > 0:
            return f"positive growth of ${pnl:,.2f}"
        elif pnl > -100:
            return f"small test of ${pnl:,.2f}"
        else:
            return f"challenging lesson of ${pnl:,.2f}"
    
    def _format_percentage(self, percentage: float) -> str:
        """Format percentage with Rastafarian spiritual meaning."""
        if percentage > 10:
            return f"massive upward {percentage:.1f}%"
        elif percentage > 5:
            return f"strong rising {percentage:.1f}%"
        elif percentage > 0:
            return f"gentle positive {percentage:.1f}%"
        elif percentage > -5:
            return f"slight downward {percentage:.1f}%"
        else:
            return f"heavy downpression {percentage:.1f}%"
    
    def _get_advice(self, position_data: Dict[str, Any]) -> str:
        """Get trading advice for a position in Rastafarian style."""
        side = position_data.get('side', 'unknown')
        pnl = position_data.get('pnl', 0)
        pnl_percentage = position_data.get('pnl_percentage', 0)
        
        if side == 'long':
            if pnl > 0 and pnl_percentage > 10:
                return "suggest harvesting some of these blessed fruits"
            elif pnl > 0:
                return "advise allowing more divine growth with patience"
            elif pnl < 0 and pnl_percentage < -10:
                return "encourage reflection on whether this seed needs releasing"
            else:
                return "recommend meditation on this position's path"
        else:  # short
            if pnl > 0 and pnl_percentage > 10:
                return "see wisdom in taking profits from Babylon's fall"
            elif pnl > 0:
                return "feel more downward movement in the rhythm"
            elif pnl < 0 and pnl_percentage < -10:
                return "suggest releasing this position that fights against the current"
            else:
                return "advise careful watching of this position's vibration"
    
    def _get_future_vision(self, market_data: Dict[str, Any]) -> str:
        """Generate a future vision statement in Rastafarian style."""
        mood = self.current_mood
        
        if mood in [TradingMood.EXTREMELY_BULLISH, TradingMood.BULLISH]:
            visions = [
                "green gardens growing toward the heavens",
                "lions rising with the morning sun",
                "divine prosperity flowing like a river",
                "cosmic alignment bringing blessings to the faithful"
            ]
        elif mood in [TradingMood.SLIGHTLY_BULLISH, TradingMood.NEUTRAL]:
            visions = [
                "gentle winds bringing seeds of opportunity",
                "balanced forces seeking their natural harmony",
                "patient growth building strong roots",
                "divine wisdom in careful observation"
            ]
        else:
            visions = [
                "temporary storms that will cleanse the path",
                "tests of faith before new blessing cycles",
                "necessary downward movement before true rise",
                "Babylon confusion before clarity emerges"
            ]
            
        return random.choice(visions)
    
    def _rastalify(self, text: str) -> str:
        """
        Convert standard text to have more Rastafarian dialect elements.
        
        Args:
            text: Standard English text
            
        Returns:
            Text with Rastafarian dialect features
        """
        # Basic Jamaican dialect transformations
        text = re.sub(r'\byour\b', 'your', text)  # Keep 'your' as is for readability
        text = re.sub(r'\byou are\b', 'you be', text)
        text = re.sub(r'\bare\b', 'be', text)
        text = re.sub(r'\bmy\b', 'I', text)
        text = re.sub(r'\bthe\b', 'de', text)
        text = re.sub(r'\bthis\b', 'dis', text)
        text = re.sub(r'\bthat\b', 'dat', text)
        text = re.sub(r'\bthose\b', 'dose', text)
        text = re.sub(r'\bthem\b', 'dem', text)
        
        # Randomly insert common phrases
        words = text.split()
        if len(words) > 10:
            # Insert 1-2 phrases for longer texts
            for _ in range(random.randint(1, 2)):
                insert_pos = random.randint(1, len(words) - 1)
                phrase = random.choice(self.common_phrases)
                words.insert(insert_pos, phrase)
                
        return " ".join(words) 