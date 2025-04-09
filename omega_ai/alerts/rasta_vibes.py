"""
OMEGA BTC AI - RASTA VIBES MODULE
================================

This module provides divine Rasta-inspired functions for market analysis and alerts.
"""

from typing import Dict, List, Optional
import random
from datetime import datetime

class RastaVibes:
    """Divine Rastafarian wisdom generator for OMEGA BTC AI alerts."""
    
    # Core Rasta phrases
    BLESSINGS = [
        "JAH BLESS",
        "SELASSIE I",
        "RASTAFARI LIVETH",
        "ONE LOVE",
        "IRIE HEIGHTS",
        "DIVINE GUIDANCE",
        "NATURAL MYSTIC",
        "ROOTS AND CULTURE"
    ]
    
    # Babylon (manipulators) references
    BABYLON = [
        "BABYLON SYSTEM",
        "DOWNPRESSORS",
        "MANIPULATORS",
        "SHITSTEM",
        "TRAP SETTERS",
        "MONEY CHANGERS",
        "EXCHANGE VULTURES",
        "DIGITAL TRICKSTERS"
    ]
    
    # Crypto-Rasta fusion concepts
    CRYPTO_WISDOM = [
        "GOLDEN RATIO GUIDANCE",
        "NATURAL FIBONACCI WAY",
        "DIVINE PATTERN RECOGNITION",
        "COSMIC PRICE ALIGNMENT",
        "DIGITAL ROOTS MOVEMENT",
        "BLOCKCHAIN ELEVATION",
        "SATOSHI MEDITATION",
        "NATURAL BTC VIBRATION"
    ]
    
    # Trading wisdom
    TRADING_WISDOM = [
        "HODL WITH PATIENCE AND FAITH",
        "THE CHARTS SPEAK TRUTHS TO THE ENLIGHTENED",
        "TRADE NOT WITH FEAR BUT WITH WISDOM",
        "THE DIVINE PATTERN REVEALS ITSELF TO THE PATIENT",
        "WHEN BABYLON DUMPS, THE RIGHTEOUS STACK SATS",
        "THE GOLDEN RATIO GUIDES THE RIGHTEOUS TRADER",
        "LIQUIDITY TRAPS ARE BABYLON'S DECEPTION",
        "MARKET MANIPULATION CANNOT FOOL THE THIRD EYE"
    ]
    
    # Divine blessings for different performance levels
    BLESSINGS_DICT = {
        "high": [
            "JAH BLESS! Your trading spirit is strong! 🙏",
            "ZION RISE! Your divine profits are flowing! 🌟",
            "RASTA BLESS! Your trades are blessed with wisdom! ✨",
            "ONE LOVE! Your trading path is righteous! 💚",
            "JAH GUIDE! Your market intuition is divine! 🎯"
        ],
        "medium": [
            "Stay strong, trader! JAH is watching! 🌿",
            "Keep the faith, your time will come! 💫",
            "Roots hold strong, profits will follow! 🌱",
            "Patience is divine, stay focused! 🎯",
            "JAH BLESS your trading journey! 🙏"
        ],
        "low": [
            "JAH WARN: Time to reflect and heal! ⚠️",
            "Babylon system testing your faith! 🌪️",
            "Stay strong, this too shall pass! 💪",
            "Divine wisdom comes with experience! 📚",
            "JAH guide you through these times! 🙏"
        ]
    }
    
    # Divine emojis for different sentiments
    EMOJIS = {
        "ZION_RISE": "🚀",
        "RASTA_BLESS": "✨",
        "ROOTS_HOLD": "🌿",
        "BABYLON_FALL": "📉",
        "JAH_WARN": "⚠️"
    }
    
    @classmethod
    def get_rasta_blessing(cls, win_rate: float) -> str:
        """
        Get a divine blessing based on win rate.
        
        Args:
            win_rate: Current win rate (0.0 to 1.0)
            
        Returns:
            A divine blessing message
        """
        if win_rate >= 0.6:
            return random.choice(cls.BLESSINGS_DICT["high"])
        elif win_rate >= 0.4:
            return random.choice(cls.BLESSINGS_DICT["medium"])
        else:
            return random.choice(cls.BLESSINGS_DICT["low"])
    
    @classmethod
    def get_trap_warning(cls):
        """Return a Rasta-styled trap warning."""
        babylon = random.choice(cls.BABYLON)
        return f"{babylon} A SET TRAP, BUT I AND I SEE THROUGH!"
    
    @classmethod
    def get_wisdom(cls):
        """Return trading wisdom in Rasta style."""
        return random.choice(cls.TRADING_WISDOM)
    
    @classmethod
    def get_crypto_insight(cls):
        """Return crypto-Rasta insight."""
        return random.choice(cls.CRYPTO_WISDOM)
    
    @classmethod
    def get_daily_message(cls):
        """Return a message influenced by day of week."""
        day = datetime.now().strftime("%A")
        
        if day == "Monday":
            return "START DI WEEK WITH MEDITATION ON DI GOLDEN RATIO"
        elif day == "Tuesday":
            return "DI COSMIC VIBRATION GUIDE I AND I TRADES"
        elif day == "Wednesday":
            return "MIDDLE OF DI WEEK, STAY STEADY LIKE MOUNT ZION"
        elif day == "Thursday":
            return "CHANNEL DI DIVINE GUIDANCE FOR RIGHTEOUS TRADES"
        elif day == "Friday":
            return "JAH PROVIDE WISDOM FOR DI WEEKEND MARKET"
        elif day == "Saturday":
            return "WEEKEND MEDITATION ON DI BLOCKCHAIN TRUTH"
        else:  # Sunday
            return "SABBATH REFLECTION ON DI DIGITAL FUTURE"
    
    @classmethod
    def enhance_alert(cls, alert_type, alert_message):
        """Enhance an alert with Rastafarian wisdom based on alert type."""
        # Get current hour for time-appropriate greeting
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            greeting = "BLESSED MORNING! "
        elif 12 <= hour < 18:
            greeting = "BLESSED DAY! "
        else:
            greeting = "BLESSED EVENING! "
            
        # Base enhanced message
        enhanced = f"{greeting}{cls.get_rasta_blessing(0.5)}!\n\n"
        
        # Add trap-specific message for different alert types
        if "Liquidity Grab" in alert_type:
            enhanced += f"⚠️ {cls.get_trap_warning()}\n"
            enhanced += f"DI {alert_type.upper()} IS BABYLON TRYING TO STEAL FROM DI RIGHTEOUS!\n"
        elif "Pump" in alert_type:
            enhanced += f"⚠️ WATCH DI {alert_type.upper()}! BABYLON PUMP BEFORE DEM DUMP!\n"
            enhanced += f"{cls.get_wisdom()}\n"
        elif "Dump" in alert_type:
            enhanced += f"⚠️ {alert_type.upper()} DETECTED! STAY STRONG WHEN BABYLON TRY SHAKE OUT!\n"
            enhanced += f"{cls.get_wisdom()}\n"
        else:
            enhanced += f"⚠️ {alert_type.upper()} REQUIRES I AND I ATTENTION!\n"
            
        # Add original alert message
        enhanced += f"\n{alert_message}\n\n"
        
        # Add final blessing and crypto wisdom
        enhanced += f"{cls.get_crypto_insight()}\n"
        enhanced += f"{cls.get_daily_message()}\n\n"
        enhanced += "ONE LOVE, ONE HEART, ONE BLOCKCHAIN! 🌿"
        
        return enhanced

    @classmethod
    def get_rasta_emoji(cls, sentiment: str) -> str:
        """
        Get a divine emoji based on market sentiment.
        
        Args:
            sentiment: Current market sentiment
            
        Returns:
            A divine emoji
        """
        return cls.EMOJIS.get(sentiment, "✨")  # Default to sparkles if sentiment not found