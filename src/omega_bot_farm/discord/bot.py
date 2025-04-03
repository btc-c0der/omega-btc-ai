#!/usr/bin/env python3

"""
Discord Bot for Omega Bot Farm

This module implements the Discord bot for monitoring and controlling the trading bots.
"""

import os
import logging
import asyncio
import discord
from discord import app_commands
from discord.ext import commands, tasks
import json
from typing import Dict, List, Optional, Any
from pathlib import Path

from src.omega_bot_farm.utils.redis_client import RedisClient

# Configure logging
logger = logging.getLogger("discord_bot")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class OmegaBotFarmClient(commands.Bot):
    """Discord bot for Omega Bot Farm command and control."""
    
    def __init__(self, redis_client: Optional[RedisClient] = None):
        """Initialize the Discord bot with Redis client."""
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        
        # Redis client
        self.redis = redis_client or RedisClient()
        
        # Bot state
        self.last_update_time = 0
        self.bot_statuses = {}
        
        # Add commands
        self.setup_commands()
        
    async def setup_hook(self):
        """Set up the bot hooks and tasks."""
        # Start background tasks
        self.update_bot_status.start()
        
        # Sync commands with Discord
        await self.tree.sync()
        logger.info("Commands synced with Discord")
        
    def setup_commands(self):
        """Set up slash commands."""
        # Create command tree
        self.tree = app_commands.CommandTree(self)
        
        # Farm status command
        @self.tree.command(name="farm_status", description="Get the status of all trading bots")
        async def farm_status(interaction: discord.Interaction):
            """Command to get status of all trading bots in the farm."""
            await interaction.response.defer()
            
            embed = discord.Embed(
                title="🌿 Omega Bot Farm Status",
                description="Current status of all trading bots",
                color=discord.Color.blue()
            )
            
            # Get bot statuses from Redis
            bot_keys = self.redis.keys("omega:bot:*")
            
            if not bot_keys:
                embed.add_field(name="Status", value="No active bots found", inline=False)
            else:
                for key in bot_keys:
                    bot_data = self.redis.get(key)
                    if bot_data:
                        bot_name = bot_data.get("name", "Unknown Bot")
                        pnl = bot_data.get("pnl", 0.0)
                        capital = bot_data.get("capital", 0.0)
                        win_rate = bot_data.get("win_rate", 0.0)
                        emotional_state = bot_data.get("emotional_state", "neutral")
                        
                        # Determine status color
                        status_emoji = "🟢" if pnl >= 0 else "🔴"
                        
                        # Format status field
                        status_text = (
                            f"{status_emoji} **Capital**: ${capital:,.2f}\n"
                            f"**PnL**: ${pnl:,.2f}\n"
                            f"**Win Rate**: {win_rate:.1f}%\n"
                            f"**Emotional State**: {emotional_state}"
                        )
                        
                        embed.add_field(name=f"Bot: {bot_name}", value=status_text, inline=True)
            
            await interaction.followup.send(embed=embed)
            
        # Start bot command
        @self.tree.command(name="start", description="Start a specific trading bot")
        @app_commands.describe(bot_name="Name of the bot to start")
        async def start_bot(interaction: discord.Interaction, bot_name: str):
            """Command to start a specific trading bot."""
            await interaction.response.defer()
            
            # Publish command to Redis
            command = {
                "action": "start",
                "bot_name": bot_name,
                "user_id": str(interaction.user.id),
                "user_name": str(interaction.user.name)
            }
            
            result = self.redis.publish("omega:commands", command)
            
            if result:
                await interaction.followup.send(f"✅ Command to start {bot_name} was sent successfully! Bot starting...")
            else:
                await interaction.followup.send(f"❌ Failed to send start command for {bot_name}. Please check logs.")
                
        # Stop bot command
        @self.tree.command(name="stop", description="Stop a specific trading bot")
        @app_commands.describe(bot_name="Name of the bot to stop")
        async def stop_bot(interaction: discord.Interaction, bot_name: str):
            """Command to stop a specific trading bot."""
            await interaction.response.defer()
            
            # Publish command to Redis
            command = {
                "action": "stop",
                "bot_name": bot_name,
                "user_id": str(interaction.user.id),
                "user_name": str(interaction.user.name)
            }
            
            result = self.redis.publish("omega:commands", command)
            
            if result:
                await interaction.followup.send(f"✅ Command to stop {bot_name} was sent successfully! Bot stopping...")
            else:
                await interaction.followup.send(f"❌ Failed to send stop command for {bot_name}. Please check logs.")
                
        # Get bot stats command
        @self.tree.command(name="stats", description="Get detailed statistics for a trading bot")
        @app_commands.describe(bot_name="Name of the bot to get stats for")
        async def bot_stats(interaction: discord.Interaction, bot_name: str):
            """Command to get detailed statistics for a specific bot."""
            await interaction.response.defer()
            
            # Get bot data from Redis
            bot_data = self.redis.get(f"omega:bot:{bot_name}")
            
            if not bot_data:
                await interaction.followup.send(f"❌ Bot '{bot_name}' not found.")
                return
                
            # Create embed with detailed stats
            embed = discord.Embed(
                title=f"📊 {bot_name} Statistics",
                description="Detailed trading statistics",
                color=discord.Color.green() if bot_data.get("pnl", 0) >= 0 else discord.Color.red()
            )
            
            # Basic stats
            embed.add_field(
                name="Performance",
                value=(
                    f"**Capital**: ${bot_data.get('capital', 0):,.2f}\n"
                    f"**Initial Capital**: ${bot_data.get('initial_capital', 0):,.2f}\n"
                    f"**PnL**: ${bot_data.get('pnl', 0):,.2f}\n"
                    f"**ROI**: {(bot_data.get('pnl', 0) / bot_data.get('initial_capital', 1) * 100):.2f}%"
                ),
                inline=True
            )
            
            # Trade stats
            embed.add_field(
                name="Trades",
                value=(
                    f"**Total Trades**: {bot_data.get('trades', 0)}\n"
                    f"**Win Rate**: {bot_data.get('win_rate', 0):.1f}%\n"
                    f"**Consecutive Wins**: {bot_data.get('consecutive_wins', 0)}\n"
                    f"**Consecutive Losses**: {bot_data.get('consecutive_losses', 0)}"
                ),
                inline=True
            )
            
            # Psychological stats
            embed.add_field(
                name="Psychology",
                value=(
                    f"**Emotional State**: {bot_data.get('emotional_state', 'neutral')}\n"
                    f"**Risk Appetite**: {bot_data.get('risk_level', 0.5):.2f}\n"
                    f"**Confidence**: {bot_data.get('confidence', 0.5):.2f}\n"
                    f"**Max Drawdown**: {bot_data.get('max_drawdown', 0):.2f}%"
                ),
                inline=True
            )
            
            await interaction.followup.send(embed=embed)
            
        # Cosmic influence command
        @self.tree.command(name="cosmic_influence", description="Get current cosmic influences affecting trading")
        async def cosmic_influence(interaction: discord.Interaction):
            """Command to get current cosmic influences on trading."""
            await interaction.response.defer()
            
            # Get cosmic data from Redis
            cosmic_data = self.redis.get("omega:cosmic")
            
            if not cosmic_data:
                await interaction.followup.send("❌ Cosmic influence data not available.")
                return
                
            # Create embed with cosmic information
            embed = discord.Embed(
                title="🌌 Cosmic Trading Influences",
                description="Current cosmic factors affecting trading behavior",
                color=discord.Color.purple()
            )
            
            # Moon phase
            embed.add_field(
                name="🌙 Moon Phase",
                value=cosmic_data.get("moon_phase", "Unknown"),
                inline=True
            )
            
            # Schumann resonance
            embed.add_field(
                name="⚡ Schumann Resonance",
                value=f"{cosmic_data.get('schumann_frequency', 'Unknown')} Hz",
                inline=True
            )
            
            # Mercury retrograde
            mercury_retrograde = cosmic_data.get("mercury_retrograde", False)
            embed.add_field(
                name="☿ Mercury",
                value="☢️ Retrograde" if mercury_retrograde else "✅ Direct",
                inline=True
            )
            
            # Market liquidity
            embed.add_field(
                name="💧 Market Liquidity",
                value=cosmic_data.get("market_liquidity", "Normal"),
                inline=True
            )
            
            # Global sentiment
            embed.add_field(
                name="🌐 Global Sentiment",
                value=cosmic_data.get("global_sentiment", "Neutral"),
                inline=True
            )
            
            # Trading tip based on cosmic factors
            embed.add_field(
                name="💫 Cosmic Trading Tip",
                value=cosmic_data.get("trading_tip", "No tip available"),
                inline=False
            )
            
            await interaction.followup.send(embed=embed)
            
    @tasks.loop(seconds=60)
    async def update_bot_status(self):
        """Background task to update bot status."""
        try:
            # Get bot status data from Redis
            bot_keys = self.redis.keys("omega:bot:*")
            for key in bot_keys:
                bot_data = self.redis.get(key)
                if bot_data:
                    self.bot_statuses[key] = bot_data
                    
            # Update bot activity
            total_pnl = sum(bot.get("pnl", 0) for bot in self.bot_statuses.values())
            sign = "+" if total_pnl >= 0 else ""
            status_text = f"{len(self.bot_statuses)} bots | PnL: {sign}${abs(total_pnl):,.2f}"
            
            await self.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name=status_text
                )
            )
            
        except Exception as e:
            logger.error(f"Error updating bot status: {e}")
            
    @update_bot_status.before_loop
    async def before_update_bot_status(self):
        """Wait until bot is ready before starting status update loop."""
        await self.wait_until_ready()
        
    async def on_ready(self):
        """Handle bot ready event."""
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        logger.info("Bot is ready!")
    
def run_bot():
    """Run the Discord bot."""
    # Get token from environment
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        logger.error("DISCORD_TOKEN not set in environment. Bot cannot start.")
        return
        
    # Create bot instance
    redis_client = RedisClient()
    bot = OmegaBotFarmClient(redis_client)
    
    # Run the bot
    bot.run(token)
    
def setup_bitget_commands(bot):
    """
    Set up the BitGet Position Analyzer commands.
    
    Args:
        bot: The Discord bot instance
    """
    try:
        # Import and setup the commands cog
        from src.omega_bot_farm.discord.commands.bitget_position_commands import BitgetPositionCommands
        
        # Register the cog
        bot.add_cog(BitgetPositionCommands(bot))
        logging.info("BitGet Position Commands registered successfully")
        
    except Exception as e:
        logging.error(f"Failed to register BitGet Position Commands: {e}")

if __name__ == "__main__":
    run_bot() 