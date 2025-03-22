"""
Base Persona Class for OMEGA BTC AI Bot Personification
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from enum import Enum
import json


class TradingMood(Enum):
    """Trading mood/market sentiment classification."""
    EXTREMELY_BULLISH = "extremely_bullish"
    BULLISH = "bullish"
    SLIGHTLY_BULLISH = "slightly_bullish"
    NEUTRAL = "neutral"
    SLIGHTLY_BEARISH = "slightly_bearish"
    BEARISH = "bearish"
    EXTREMELY_BEARISH = "extremely_bearish"
    UNCERTAIN = "uncertain"
    VOLATILE = "volatile"


class PersonaStyle:
    """Style configuration for a persona."""
    
    def __init__(self, 
                 primary_color: str = "#ffffff",
                 secondary_color: str = "#cccccc",
                 accent_color: str = "#ffcc00",
                 font_family: str = "Arial, sans-serif",
                 avatar_url: Optional[str] = None,
                 background_pattern: Optional[str] = None,
                 icons: Optional[Dict[str, str]] = None):
        """
        Initialize persona style configuration.
        
        Args:
            primary_color: Main text color for the persona
            secondary_color: Secondary text color for less important information 
            accent_color: Highlight color for important alerts/information
            font_family: Font family to use for this persona
            avatar_url: URL or path to the persona's avatar image
            background_pattern: URL or path to background pattern/texture
            icons: Dictionary mapping icon names to URLs or paths
        """
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.accent_color = accent_color
        self.font_family = font_family
        self.avatar_url = avatar_url
        self.background_pattern = background_pattern
        self.icons = icons or {}
    
    def to_css(self) -> str:
        """
        Convert the style to CSS variables.
        
        Returns:
            CSS variable definitions as a string
        """
        css = f"""
        --persona-primary-color: {self.primary_color};
        --persona-secondary-color: {self.secondary_color};
        --persona-accent-color: {self.accent_color};
        --persona-font-family: {self.font_family};
        """
        
        if self.avatar_url:
            css += f"--persona-avatar-url: url('{self.avatar_url}');\n"
            
        if self.background_pattern:
            css += f"--persona-background-pattern: url('{self.background_pattern}');\n"
            
        return css
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the style to a dictionary.
        
        Returns:
            Dictionary representation of the style
        """
        return {
            "primary_color": self.primary_color,
            "secondary_color": self.secondary_color,
            "accent_color": self.accent_color,
            "font_family": self.font_family,
            "avatar_url": self.avatar_url,
            "background_pattern": self.background_pattern,
            "icons": self.icons
        }


class BasePersona(ABC):
    """
    Base class for all OMEGA BTC AI bot personas.
    
    Each persona provides a unique way to interact with and interpret trading data,
    with its own personality, language style, and presentation preferences.
    """
    
    def __init__(self, 
                 name: str,
                 description: str,
                 style: Optional[PersonaStyle] = None):
        """
        Initialize a bot persona.
        
        Args:
            name: Display name of the persona
            description: Brief description of the persona's characteristics
            style: Optional style configuration for the persona
        """
        self.name = name
        self.description = description
        self.style = style or PersonaStyle()
        self.current_mood = TradingMood.NEUTRAL
        
    @abstractmethod
    def analyze_position(self, position_data: Dict[str, Any]) -> str:
        """
        Analyze a trading position in this persona's unique style.
        
        Args:
            position_data: Dictionary containing position information
            
        Returns:
            Styled analysis text in the persona's voice
        """
        pass
    
    @abstractmethod
    def analyze_market(self, market_data: Dict[str, Any]) -> str:
        """
        Analyze market conditions in this persona's unique style.
        
        Args:
            market_data: Dictionary containing market information
            
        Returns:
            Styled market analysis text in the persona's voice
        """
        pass
    
    @abstractmethod
    def generate_recommendation(self, data: Dict[str, Any]) -> str:
        """
        Generate trading recommendations in this persona's unique style.
        
        Args:
            data: Dictionary containing relevant trading data
            
        Returns:
            Styled recommendation text in the persona's voice
        """
        pass
    
    @abstractmethod
    def summarize_performance(self, performance_data: Dict[str, Any]) -> str:
        """
        Summarize trading performance in this persona's unique style.
        
        Args:
            performance_data: Dictionary containing performance metrics
            
        Returns:
            Styled performance summary in the persona's voice
        """
        pass
    
    def interpret_mood(self, market_data: Dict[str, Any]) -> TradingMood:
        """
        Interpret the current market mood based on available data.
        
        Args:
            market_data: Dictionary containing market information
            
        Returns:
            TradingMood enum representing the current market sentiment
        """
        # Default implementation - can be overridden by specific personas
        # Simple logic based on price change percentage
        if 'price_change_24h' in market_data:
            change = market_data['price_change_24h']
            
            if change > 10:
                return TradingMood.EXTREMELY_BULLISH
            elif change > 5:
                return TradingMood.BULLISH
            elif change > 1:
                return TradingMood.SLIGHTLY_BULLISH
            elif change < -10:
                return TradingMood.EXTREMELY_BEARISH
            elif change < -5:
                return TradingMood.BEARISH
            elif change < -1:
                return TradingMood.SLIGHTLY_BEARISH
            else:
                return TradingMood.NEUTRAL
        
        return TradingMood.UNCERTAIN
    
    def update_mood(self, market_data: Dict[str, Any]) -> None:
        """
        Update the persona's mood based on market data.
        
        Args:
            market_data: Dictionary containing market information
        """
        self.current_mood = self.interpret_mood(market_data)
    
    def get_greeting(self) -> str:
        """
        Get a greeting message in the persona's style.
        
        Returns:
            Greeting message
        """
        # Default implementation - should be overridden by specific personas
        return f"Hello, I am {self.name}."
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the persona to a dictionary.
        
        Returns:
            Dictionary representation of the persona
        """
        return {
            "name": self.name,
            "description": self.description,
            "style": self.style.to_dict(),
            "current_mood": self.current_mood.value if self.current_mood else None
        }
    
    def to_json(self) -> str:
        """
        Convert the persona to a JSON string.
        
        Returns:
            JSON string representation of the persona
        """
        return json.dumps(self.to_dict(), indent=2) 