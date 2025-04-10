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
Simple Discord Bot for Omega Bot Farm

A simplified version of the bot that doesn't rely on Redis - just for connection testing.
"""

import os
import logging
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("simple_discord_bot")

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Try to load from both potential locations
    load_dotenv()  # Root .env file
    bot_farm_env = Path(__file__).parents[2] / '.env'
    if bot_farm_env.exists():
        load_dotenv(dotenv_path=bot_farm_env)
    logger.info("Environment variables loaded from .env file")
except ImportError:
    logger.warning("python-dotenv not installed. Will only use OS environment variables.")

# Import the Matrix Bot commands
try:
    from src.omega_bot_farm.discord.commands.matrix_bot_commands import MatrixBotCommands
    MATRIX_COMMANDS_AVAILABLE = True
    logger.info("Matrix bot commands imported successfully")
except ImportError as e:
    MATRIX_COMMANDS_AVAILABLE = False
    logger.warning(f"Failed to import Matrix Bot Commands: {e}")

class SimpleOmegaBot(commands.Bot):
    """Simple Discord bot without Redis dependency."""
    
    def __init__(self):
        """Initialize the simple Discord bot."""
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        self.synced = False
        
        # Add test commands
        self.add_test_commands()
        
    def add_test_commands(self):
        """Add test commands to the bot."""
        
        @self.tree.command(name="ping", description="Check if the bot is working")
        async def ping(interaction: discord.Interaction):
            """Simple ping command to test if the bot is working."""
            await interaction.response.send_message(
                f"🏓 Pong! Bot is online with latency {round(self.latency * 1000)}ms",
                ephemeral=True
            )

        @self.tree.command(name="test_matrix", description="Test the Matrix Bot visualization")
        async def test_matrix(interaction: discord.Interaction):
            """Test command for Matrix Bot visualization."""
            await interaction.response.defer()
            
            message = """```ansi
╒══════════════════════════════════════════════════════════════╕
│ MATRIX COORDINATES LOCKED                                       │
│ CCXT DIRECT CONNECTED - 2025-04-07 08:04:37 │
╘══════════════════════════════════════════════════════════════╛
```"""
            
            embed = discord.Embed(
                title="🤖 MATRIX TEST 🧮",
                description="_Connection to the Matrix established successfully_",
                color=0x00FF00
            )
            
            embed.add_field(
                name="ℹ️ Status",
                value="Matrix Bot commands are working correctly!",
                inline=False
            )
            
            embed.set_footer(text="NEURAL INTERFACE CONNECTED | OMEGA BOT FARM")
            
            await interaction.followup.send(content=message, embed=embed)
        
    async def setup_hook(self):
        """Set up the bot hooks and add cogs."""
        # Add Matrix bot commands if available
        if MATRIX_COMMANDS_AVAILABLE:
            try:
                await self.add_cog(MatrixBotCommands(self))
                logger.info("Matrix Bot Commands registered successfully")
            except Exception as e:
                logger.error(f"Failed to register Matrix Bot Commands: {e}")
        
    async def on_ready(self):
        """Handle bot ready event."""
        await self.wait_until_ready()
        if not self.synced:
            # Sync slash commands
            try:
                synced = await self.tree.sync()
                logger.info(f"Synced {len(synced)} commands")
                self.synced = True
            except Exception as e:
                logger.error(f"Failed to sync commands: {e}")
        
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        logger.info(f"Connected to {len(self.guilds)} guilds:")
        
        for guild in self.guilds:
            logger.info(f"- {guild.name} (ID: {guild.id})")
            
        logger.info("Bot is ready!")
        
        # Update bot presence
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="Matrix Positions | /matrix-positions"
            )
        )

# Initialize the bot
client = SimpleOmegaBot()

def run_simple_bot():
    """Run the simple Discord bot."""
    # Get token from environment
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        logger.error("DISCORD_TOKEN not set in environment. Bot cannot start.")
        return
        
    # If token is wrapped in quotes, remove them
    token = token.strip("'\"")
    
    logger.info(f"Using token: {token[:10]}...{token[-5:]}")
    logger.info("Starting simple Discord bot (no Redis)...")
    
    # Run the bot
    try:
        client.run(token)
    except discord.errors.LoginFailure as e:
        logger.error(f"Failed to login: {e}")
    except Exception as e:
        logger.error(f"Error running bot: {e}")

if __name__ == "__main__":
    run_simple_bot() 