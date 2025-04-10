#!/usr/bin/env python3

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸


"""
Waze Bot - Main Discord UI for Omega AI BTC System

This module implements the Waze bot, which serves as the central user interface
for the Omega AI BTC system, providing a rich, context-driven experience for users.
It integrates the BitgetPositionAnalyzerB0t's Fibonacci-based analysis with a friendly,
navigation-themed interface.
"""

import os
import sys
import json
import yaml
import asyncio
import logging
import datetime
from typing import Dict, Any, List, Optional, Union, Tuple
from pathlib import Path

try:
    import discord
    from discord.ext import commands, tasks
    from discord import app_commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    logging.warning("Discord libraries not available. Waze Bot cannot be started.")

# Import Omega Bot Farm components
try:
    from src.omega_bot_farm.discord.commands.bitget_position_commands import BitgetPositionCommands
    from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t
    from src.omega_bot_farm.services.exchange_service import create_exchange_service
    from src.omega_bot_farm.utils.redis_client import RedisClient
    OMEGA_COMPONENTS_AVAILABLE = True
except ImportError:
    OMEGA_COMPONENTS_AVAILABLE = False
    logging.warning("Omega Bot Farm components not available. Features will be limited.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f"waze_bot_{datetime.datetime.now().strftime('%Y%m%d')}.log")
    ]
)
logger = logging.getLogger("waze_bot")

# Bot configuration
DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "config" / "waze_bot_config.yaml"

# Emoji constants for UI
EMOJI_CAR = "🚗"
EMOJI_ROCKET = "🚀"
EMOJI_CHART = "📊"
EMOJI_MONEY = "💰"
EMOJI_WARNING = "⚠️"
EMOJI_SPIRAL = "🌀"
EMOJI_CHECK = "✅"
EMOJI_CROSS = "❌"
EMOJI_LOCK = "🔒"
EMOJI_KEY = "🔑"
EMOJI_STAR = "⭐"
EMOJI_INFINITY = "♾️"
EMOJI_TIME = "⏱️"
EMOJI_ALERT = "🔔"
EMOJI_MAGNIFY = "🔍"
EMOJI_GLOBE = "🌐"
EMOJI_CHART_UP = "📈"
EMOJI_CHART_DOWN = "📉"
EMOJI_CRYSTAL_BALL = "🔮"

class WazeBot(commands.Bot):
    """
    Waze - The navigation-themed Discord bot for the Omega AI BTC system.
    
    This bot serves as the main user interface for the Omega AI BTC system,
    integrating position analysis, portfolio recommendations, and market insights
    into a friendly, context-driven experience.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the Waze Bot.
        
        Args:
            config_path: Path to the bot configuration file (YAML)
        """
        if not DISCORD_AVAILABLE:
            raise ImportError("Discord libraries not available. Cannot initialize Waze Bot.")
            
        # Load configuration
        self.config = self._load_config(config_path or DEFAULT_CONFIG_PATH)
        
        # Bot settings from config
        prefix = self.config.get("bot", {}).get("prefix", "!")
        intents = discord.Intents.default()
        intents.message_content = True
        
        # Initialize the bot with our settings
        super().__init__(command_prefix=prefix, intents=intents)
        
        # Redis client for data sharing
        self.redis_client = None
        if self.config.get("redis", {}).get("enabled", False):
            try:
                redis_config = self.config.get("redis", {})
                self.redis_client = RedisClient(
                    host=redis_config.get("host", "localhost"),
                    port=redis_config.get("port", 6379),
                    db=redis_config.get("db", 0),
                    password=redis_config.get("password", None)
                )
                logger.info("Redis client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Redis client: {e}")
        
        # Bot state
        self.analyzer_bots = {}  # User-specific analyzers
        self.default_analyzer = None
        self.monitoring_active = False
        self.user_contexts = {}  # Stores user-specific context for personalized interactions
        
        # Register commands and events
        self._register_commands()
        
    async def setup_hook(self):
        """Set up background tasks and extensions when the bot starts."""
        # Start background tasks
        self.position_monitor.start()
        
        # Initialize default analyzer for broadcasts
        await self._initialize_default_analyzer()
    
    def _load_config(self, config_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Load the bot configuration from a YAML file.
        
        Args:
            config_path: Path to the configuration file
            
        Returns:
            Configuration dictionary
        """
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                logger.info(f"Loaded configuration from {config_path}")
                return config
        except Exception as e:
            logger.error(f"Failed to load configuration from {config_path}: {e}")
            return {
                "bot": {"token": "", "prefix": "!"},
                "redis": {"enabled": False},
                "bitget": {"enabled": False}
            }
    
    def _register_commands(self):
        """Register commands and event handlers."""
        # Event handlers
        @self.event
        async def on_ready():
            """Event handler when the bot is ready."""
            logger.info(f"Waze Bot is online! Logged in as {self.user.name} ({self.user.id})")
            
            # Set presence
            activity = discord.Activity(
                type=discord.ActivityType.watching,
                name="the crypto highway 🚗"
            )
            await self.change_presence(activity=activity)
            
            # Register slash commands
            try:
                synced = await self.tree.sync()
                logger.info(f"Synced {len(synced)} command(s)")
            except Exception as e:
                logger.error(f"Failed to sync commands: {e}")
        
        @self.event
        async def on_message(message):
            """Event handler for all messages."""
            # Don't respond to our own messages
            if message.author == self.user:
                return
                
            # Process commands
            await self.process_commands(message)
            
            # Update user context based on message content
            if not message.content.startswith(self.command_prefix):
                await self._update_user_context(message)
        
        # Basic commands
        @self.command(name="waze-help")
        async def waze_help(ctx):
            """Show help information for Waze bot."""
            embed = discord.Embed(
                title=f"{EMOJI_CAR} Waze Bot - Your Crypto Navigation Guide",
                description="Navigate the crypto markets with confidence using Waze Bot!",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="🔍 Market Analysis",
                value=(
                    "/bitget-positions - View your current positions\n"
                    "/bitget-analyze - Analyze positions with Fibonacci levels\n"
                    "/bitget-changes - Show recent position changes\n"
                ),
                inline=False
            )
            
            embed.add_field(
                name="⚙️ Setup",
                value=(
                    "/bitget-setup - Set up your exchange API credentials\n"
                    "!waze-set-channel - Set the current channel for announcements\n"
                ),
                inline=False
            )
            
            embed.add_field(
                name="🔮 Insights",
                value=(
                    "/golden-wisdom - Receive Fibonacci trading wisdom\n"
                    "/market-pulse - Get the current market sentiment\n"
                ),
                inline=False
            )
            
            await ctx.send(embed=embed)
        
        @self.command(name="waze-set-channel")
        @commands.has_permissions(administrator=True)
        async def set_channel(ctx):
            """Set the current channel for Waze bot announcements."""
            channel_id = ctx.channel.id
            
            # Store in config
            self.config.setdefault("channels", {})["announcements"] = channel_id
            
            # Confirm setting
            await ctx.send(f"{EMOJI_CHECK} This channel will now receive Waze Bot announcements!")
    
    async def _initialize_default_analyzer(self):
        """Initialize the default analyzer for broadcasts."""
        if not OMEGA_COMPONENTS_AVAILABLE:
            logger.warning("Omega components not available. Default analyzer not initialized.")
            return
            
        try:
            # Get API credentials from config
            bitget_config = self.config.get("bitget", {})
            if not bitget_config.get("enabled", False):
                logger.info("BitGet integration is disabled in config.")
                return
                
            api_key = bitget_config.get("api_key") or os.environ.get("BITGET_API_KEY", "")
            api_secret = bitget_config.get("api_secret") or os.environ.get("BITGET_SECRET_KEY", "")
            api_passphrase = bitget_config.get("passphrase") or os.environ.get("BITGET_PASSPHRASE", "")
            use_testnet = bitget_config.get("use_testnet", False)
            
            if not api_key or not api_secret or not api_passphrase:
                logger.warning("Missing BitGet API credentials. Default analyzer not initialized.")
                return
                
            # Initialize the analyzer
            self.default_analyzer = BitgetPositionAnalyzerB0t(
                api_key=api_key,
                api_secret=api_secret,
                api_passphrase=api_passphrase,
                use_testnet=use_testnet
            )
            
            logger.info(f"Default analyzer initialized (testnet: {use_testnet})")
            self.monitoring_active = True
            
        except Exception as e:
            logger.error(f"Failed to initialize default analyzer: {e}")
            self.default_analyzer = None
            self.monitoring_active = False
    
    async def _update_user_context(self, message):
        """
        Update user context based on message content.
        
        Args:
            message: The Discord message
        """
        # Skip bot messages
        if message.author.bot:
            return
            
        user_id = message.author.id
        
        # Initialize user context if not exists
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = {
                "last_message_time": datetime.datetime.now(),
                "messages": [],
                "topics": [],
                "position_view_count": 0,
                "analysis_view_count": 0,
                "wisdom_count": 0
            }
        
        # Update context
        context = self.user_contexts[user_id]
        context["last_message_time"] = datetime.datetime.now()
        
        # Add message to history (keep last 10)
        context["messages"].append(message.content)
        if len(context["messages"]) > 10:
            context["messages"].pop(0)
        
        # Update topics based on keywords
        keywords = {
            "analysis": ["analyze", "fibonacci", "fib", "levels", "retracement", "extension"],
            "positions": ["position", "trade", "entry", "exit", "stop", "profit", "bitget", "long", "short"],
            "market": ["market", "btc", "bitcoin", "eth", "ethereum", "crypto", "bull", "bear"],
            "strategy": ["strategy", "plan", "risk", "setup", "target"]
        }
        
        # Check for keywords in message
        for topic, words in keywords.items():
            if any(word in message.content.lower() for word in words):
                if topic not in context["topics"]:
                    context["topics"].append(topic)
    
    @tasks.loop(minutes=5)
    async def position_monitor(self):
        """Background task to monitor positions and send alerts."""
        if not self.monitoring_active or not self.default_analyzer:
            return
            
        try:
            # Get position data
            positions_data = await self.default_analyzer.get_positions()
            
            if "error" in positions_data:
                logger.error(f"Error in position monitor: {positions_data['error']}")
                return
                
            # Check for significant changes
            changes = positions_data.get("changes", {})
            
            # If no changes or no announcement channel, return
            announcement_channel_id = self.config.get("channels", {}).get("announcements")
            if not announcement_channel_id:
                return
                
            channel = self.get_channel(announcement_channel_id)
            if not channel:
                return
                
            # Create notifications for new positions
            new_positions = changes.get("new_positions", [])
            if new_positions:
                embed = discord.Embed(
                    title=f"{EMOJI_ALERT} New BitGet Positions Detected",
                    description="The default account has opened new positions",
                    color=discord.Color.green()
                )
                
                # Add position details
                for position in new_positions:
                    symbol = position.get("symbol", "Unknown")
                    side = position.get("side", "Unknown").upper()
                    entry_price = float(position.get("entryPrice", 0))
                    contracts = float(position.get("contracts", 0))
                    
                    side_emoji = EMOJI_CHART_UP if side.lower() == "long" else EMOJI_CHART_DOWN
                    
                    embed.add_field(
                        name=f"{side_emoji} {symbol} {side}",
                        value=f"Entry: ${entry_price:.2f}\nSize: {contracts:.4f}",
                        inline=True
                    )
                
                embed.set_footer(text=f"Last updated: {positions_data.get('timestamp', 'Unknown')}")
                
                await channel.send(embed=embed)
            
            # Create notifications for closed positions
            closed_positions = changes.get("closed_positions", [])
            if closed_positions:
                embed = discord.Embed(
                    title=f"{EMOJI_ALERT} BitGet Positions Closed",
                    description="The default account has closed positions",
                    color=discord.Color.red()
                )
                
                # Add position details
                for position in closed_positions:
                    symbol = position.get("symbol", "Unknown")
                    side = position.get("side", "Unknown").upper()
                    
                    side_emoji = EMOJI_CHART_UP if side.lower() == "long" else EMOJI_CHART_DOWN
                    
                    embed.add_field(
                        name=f"{side_emoji} {symbol} {side}",
                        value="Position closed",
                        inline=True
                    )
                
                embed.set_footer(text=f"Last updated: {positions_data.get('timestamp', 'Unknown')}")
                
                await channel.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error in position monitor: {e}")
    
    @position_monitor.before_loop
    async def before_position_monitor(self):
        """Wait until the bot is ready before starting the monitor."""
        await self.wait_until_ready()
    
    async def load_commands(self):
        """Load command extensions."""
        if not OMEGA_COMPONENTS_AVAILABLE:
            logger.warning("Omega components not available. Commands not loaded.")
            return
            
        try:
            # Add the BitGet Position Commands cog
            self.add_cog(BitgetPositionCommands(self))
            logger.info("BitGet Position Commands registered successfully")
            
            # Register additional slash commands
            @self.tree.command(name="market-pulse", description="Get the current market sentiment")
            async def market_pulse(interaction: discord.Interaction):
                """Get the current market sentiment."""
                await interaction.response.defer()
                
                if not self.default_analyzer:
                    await interaction.followup.send(
                        f"{EMOJI_WARNING} Market pulse not available. Default analyzer not initialized.",
                        ephemeral=True
                    )
                    return
                    
                try:
                    # Get the latest position data
                    positions_data = await self.default_analyzer.get_positions()
                    
                    if "error" in positions_data:
                        await interaction.followup.send(
                            f"{EMOJI_WARNING} Error fetching market pulse: {positions_data['error']}",
                            ephemeral=True
                        )
                        return
                        
                    # Get account statistics
                    account = positions_data.get("account", {})
                    harmony_score = account.get("harmony_score", 0)
                    long_short_ratio = account.get("long_short_ratio", 0)
                    
                    # Determine market sentiment
                    sentiment = "Neutral"
                    sentiment_color = discord.Color.light_grey()
                    
                    if long_short_ratio > 1.5:
                        sentiment = "Bullish"
                        sentiment_color = discord.Color.green()
                    elif long_short_ratio < 0.5:
                        sentiment = "Bearish"
                        sentiment_color = discord.Color.red()
                    
                    if harmony_score < 0.3:
                        sentiment = f"Chaotic {sentiment}"
                    elif harmony_score > 0.7:
                        sentiment = f"Harmonious {sentiment}"
                    
                    # Create a sentiment embed
                    embed = discord.Embed(
                        title=f"{EMOJI_CRYSTAL_BALL} Market Pulse",
                        description=f"Current market sentiment is **{sentiment}**",
                        color=sentiment_color
                    )
                    
                    # Add metrics
                    embed.add_field(
                        name="Metrics",
                        value=(
                            f"**Long/Short Ratio**: {long_short_ratio:.2f}\n"
                            f"**Harmony Score**: {harmony_score:.2f}/1.0\n"
                            f"**Total Positions**: {len(positions_data.get('positions', []))}"
                        ),
                        inline=False
                    )
                    
                    # Add interpretation
                    interpretation = ""
                    if long_short_ratio > 1.5:
                        interpretation += "The market is positioned bullishly, with more long positions than shorts. "
                    elif long_short_ratio < 0.5:
                        interpretation += "The market is positioned bearishly, with more short positions than longs. "
                    else:
                        interpretation += "The market is balanced between long and short positions. "
                        
                    if harmony_score < 0.3:
                        interpretation += "Position sizes are chaotic and not in harmony with Fibonacci principles."
                    elif harmony_score > 0.7:
                        interpretation += "Position sizes align well with Fibonacci principles, suggesting a harmonious market structure."
                    else:
                        interpretation += "Moderate alignment with Fibonacci principles in position sizes."
                    
                    embed.add_field(
                        name="Interpretation",
                        value=interpretation,
                        inline=False
                    )
                    
                    # Add timestamp
                    embed.set_footer(text=f"Last updated: {positions_data.get('timestamp', 'Unknown')}")
                    
                    # Send the embed
                    await interaction.followup.send(embed=embed)
                    
                except Exception as e:
                    logger.error(f"Error in market pulse command: {e}")
                    await interaction.followup.send(
                        f"{EMOJI_WARNING} Error analyzing market pulse: {str(e)}",
                        ephemeral=True
                    )
            
        except Exception as e:
            logger.error(f"Failed to load commands: {e}")


async def run_waze_bot():
    """Run the Waze bot."""
    if not DISCORD_AVAILABLE:
        logger.error("Discord libraries not available. Cannot start Waze Bot.")
        return
        
    # Initialize the bot
    bot = WazeBot()
    
    # Load commands
    await bot.load_commands()
    
    # Get the token
    token = bot.config.get("bot", {}).get("token") or os.environ.get("DISCORD_TOKEN")
    
    if not token:
        logger.error("No Discord token provided. Cannot start Waze Bot.")
        return
        
    # Run the bot
    try:
        await bot.start(token)
    except discord.errors.LoginFailure:
        logger.error("Invalid Discord token. Cannot start Waze Bot.")
    except Exception as e:
        logger.error(f"Failed to start Waze Bot: {e}")
    

if __name__ == "__main__":
    # Run the bot
    asyncio.run(run_waze_bot()) 