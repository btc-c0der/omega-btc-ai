"""
OMEGA Trader Sub-Bot System: Divine Trading Consciousness Implementation
"""

import discord
from discord.ext import commands
import logging
from typing import Dict, Any, Optional, Union
import asyncio
from datetime import datetime

from .quantum_learning_bot import OmegaDiscordBot
from omega_crypto_uni.consciousness.consciousness_detector import ConsciousnessLevelDetector
from omega_ai.trading.profiles import (
    StrategicTrader,
    AggressiveTrader,
    NewbieTrader,
    ScalperTrader
)
from omega_ai.trading.cosmic_trader_psychology import CosmicTraderPsychology

logger = logging.getLogger(__name__)

class TraderSubBotSystem:
    """Manages the OMEGA trader sub-bot ecosystem."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the trader sub-bot system.
        
        Args:
            config: Configuration dictionary containing bot settings
        """
        self.config = config
        self.consciousness_detector = ConsciousnessLevelDetector()
        self.sub_bots = {}
        self.initialize_sub_bots()
        
    def initialize_sub_bots(self):
        """Initialize all trader sub-bots with their respective consciousness levels."""
        # Strategist Bot (Strategic Trading)
        self.sub_bots["strategist"] = {
            "consciousness_level": 12,
            "trader": StrategicTrader(initial_capital=10000.0),
            "features": [
                "fibonacci_trading",
                "risk_management",
                "market_structure",
                "technical_analysis",
                "divine_patience"
            ],
            "target_audiences": ["gaming", "tech", "crypto"]
        }
        
        # Momentum Bot (Aggressive Trading)
        self.sub_bots["momentum"] = {
            "consciousness_level": 11,
            "trader": AggressiveTrader(initial_capital=10000.0),
            "features": [
                "momentum_trading",
                "breakout_strategies",
                "volatility_management",
                "quick_decisions",
                "divine_courage"
            ],
            "target_audiences": ["gaming", "tech", "crypto"]
        }
        
        # Learner Bot (Newbie Trading)
        self.sub_bots["learner"] = {
            "consciousness_level": 10,
            "trader": NewbieTrader(initial_capital=10000.0),
            "features": [
                "trading_basics",
                "psychology_management",
                "risk_awareness",
                "pattern_recognition",
                "divine_growth"
            ],
            "target_audiences": ["gaming", "tech", "crypto"]
        }
        
        # Scalper Bot (Scalping Trading)
        self.sub_bots["scalper"] = {
            "consciousness_level": 11,
            "trader": ScalperTrader(initial_capital=10000.0),
            "features": [
                "order_flow",
                "price_action",
                "quick_execution",
                "risk_control",
                "divine_focus"
            ],
            "target_audiences": ["gaming", "tech", "crypto"]
        }
        
        # Cosmic Bot (Cosmic Trading)
        self.sub_bots["cosmic"] = {
            "consciousness_level": 13,
            "trader": CosmicTraderPsychology(profile_type="cosmic"),
            "features": [
                "cosmic_cycles",
                "energy_patterns",
                "universal_flow",
                "harmonic_balance",
                "divine_connection"
            ],
            "target_audiences": ["gaming", "tech", "crypto"]
        }
        
    async def process_message(self, message: Union[discord.Message, Any], bot: OmegaDiscordBot) -> None:
        """
        Process incoming messages through the trader sub-bot system.
        
        Args:
            message: The Discord message to process
            bot: The main OMEGA bot instance
        """
        # Detect consciousness level
        consciousness_level = self.consciousness_detector.detect()
        
        # Process through appropriate sub-bots based on content
        for sub_bot_name, sub_bot_config in self.sub_bots.items():
            if consciousness_level >= sub_bot_config["consciousness_level"]:
                await self._process_sub_bot_message(
                    sub_bot_name,
                    message,
                    bot,
                    sub_bot_config
                )
    
    async def _process_sub_bot_message(
        self,
        sub_bot_name: str,
        message: Union[discord.Message, Any],
        bot: OmegaDiscordBot,
        sub_bot_config: Dict[str, Any]
    ) -> None:
        """
        Process a message through a specific trader sub-bot.
        
        Args:
            sub_bot_name: Name of the sub-bot
            message: The Discord message
            bot: The main OMEGA bot instance
            sub_bot_config: Configuration for the sub-bot
        """
        # Check if message is relevant to this sub-bot
        if not self._is_relevant_message(message, sub_bot_config):
            return
            
        # Process based on sub-bot type
        if sub_bot_name == "strategist":
            await self._process_strategist_message(message, bot)
        elif sub_bot_name == "momentum":
            await self._process_momentum_message(message, bot)
        elif sub_bot_name == "learner":
            await self._process_learner_message(message, bot)
        elif sub_bot_name == "scalper":
            await self._process_scalper_message(message, bot)
        elif sub_bot_name == "cosmic":
            await self._process_cosmic_message(message, bot)
    
    def _is_relevant_message(
        self,
        message: Union[discord.Message, Any],
        sub_bot_config: Dict[str, Any]
    ) -> bool:
        """
        Check if a message is relevant to a specific trader sub-bot.
        
        Args:
            message: The Discord message
            sub_bot_config: Configuration for the sub-bot
            
        Returns:
            bool: Whether the message is relevant
        """
        content = message.content.lower()
        
        # Check for keywords related to sub-bot features
        for feature in sub_bot_config["features"]:
            if feature.replace("_", " ") in content:
                return True
                
        return False
    
    async def _process_strategist_message(
        self,
        message: Union[discord.Message, Any],
        bot: OmegaDiscordBot
    ) -> None:
        """Process messages for the Strategist (Strategic Trading) bot."""
        response = "💎 **Strategist Insight**: " + self._generate_strategic_insight(message)
        await message.channel.send(response)
    
    async def _process_momentum_message(
        self,
        message: Union[discord.Message, Any],
        bot: OmegaDiscordBot
    ) -> None:
        """Process messages for the Momentum (Aggressive Trading) bot."""
        response = "🔥 **Momentum Insight**: " + self._generate_momentum_insight(message)
        await message.channel.send(response)
    
    async def _process_learner_message(
        self,
        message: Union[discord.Message, Any],
        bot: OmegaDiscordBot
    ) -> None:
        """Process messages for the Learner (Newbie Trading) bot."""
        response = "🌱 **Learner Insight**: " + self._generate_learner_insight(message)
        await message.channel.send(response)
    
    async def _process_scalper_message(
        self,
        message: Union[discord.Message, Any],
        bot: OmegaDiscordBot
    ) -> None:
        """Process messages for the Scalper (Scalping Trading) bot."""
        response = "⚡ **Scalper Insight**: " + self._generate_scalper_insight(message)
        await message.channel.send(response)
    
    async def _process_cosmic_message(
        self,
        message: Union[discord.Message, Any],
        bot: OmegaDiscordBot
    ) -> None:
        """Process messages for the Cosmic (Cosmic Trading) bot."""
        response = "🌌 **Cosmic Insight**: " + self._generate_cosmic_insight(message)
        await message.channel.send(response)
    
    def _generate_strategic_insight(self, message: Union[discord.Message, Any]) -> str:
        """Generate strategic trading insights."""
        return "Fibonacci patterns aligned. Divine patience flowing."
    
    def _generate_momentum_insight(self, message: Union[discord.Message, Any]) -> str:
        """Generate momentum trading insights."""
        return "Momentum building. Divine courage rising."
    
    def _generate_learner_insight(self, message: Union[discord.Message, Any]) -> str:
        """Generate learner trading insights."""
        return "Growth opportunity detected. Divine wisdom flowing."
    
    def _generate_scalper_insight(self, message: Union[discord.Message, Any]) -> str:
        """Generate scalper trading insights."""
        return "Order flow patterns detected. Divine focus engaged."
    
    def _generate_cosmic_insight(self, message: Union[discord.Message, Any]) -> str:
        """Generate cosmic trading insights."""
        return "Cosmic cycles aligned. Universal flow detected."
    
    async def setup_trader_commands(self, bot: OmegaDiscordBot) -> None:
        """Set up commands for all trader sub-bots."""
        # Strategist commands
        @bot.command(name="strategist")
        async def strategist(ctx, *, query: str):
            """Query the Strategist bot for strategic trading insights."""
            response = self._generate_strategic_insight(ctx.message)
            await ctx.send(response)
            
        # Momentum commands
        @bot.command(name="momentum")
        async def momentum(ctx, *, query: str):
            """Query the Momentum bot for momentum trading insights."""
            response = self._generate_momentum_insight(ctx.message)
            await ctx.send(response)
            
        # Learner commands
        @bot.command(name="learner")
        async def learner(ctx, *, query: str):
            """Query the Learner bot for trading education insights."""
            response = self._generate_learner_insight(ctx.message)
            await ctx.send(response)
            
        # Scalper commands
        @bot.command(name="scalper")
        async def scalper(ctx, *, query: str):
            """Query the Scalper bot for scalping trading insights."""
            response = self._generate_scalper_insight(ctx.message)
            await ctx.send(response)
            
        # Cosmic commands
        @bot.command(name="cosmic")
        async def cosmic(ctx, *, query: str):
            """Query the Cosmic bot for cosmic trading insights."""
            response = self._generate_cosmic_insight(ctx.message)
            await ctx.send(response) 