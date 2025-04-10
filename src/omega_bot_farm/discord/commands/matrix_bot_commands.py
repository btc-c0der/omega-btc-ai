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
Discord Commands for BitGet Matrix CLI Bot

This module provides Discord command integrations for the BitGet Matrix CLI Bot,
allowing users to visualize BitGet positions with cyberpunk Matrix styling
directly in Discord.
"""

import os
import io
import json
import asyncio
import logging
import discord
import builtins  # Add explicit import for builtins
from discord import app_commands
from discord.ext import commands
from typing import Dict, List, Any, Optional, Tuple
import random

# Type definitions for type checking
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.omega_bot_farm.bitget_matrix_cli_b0t import BitGetMatrixCliB0t

# Try to import BitGetMatrixCliBot
try:
    from src.omega_bot_farm.bitget_matrix_cli_b0t import BitGetMatrixCliB0t, MOCK_POSITIONS, MOCK_ACCOUNT
    MATRIX_BOT_AVAILABLE = True
except ImportError:
    MATRIX_BOT_AVAILABLE = False
    logging.warning("BitGetMatrixCliB0t not available. Features will be limited.")
    # Define placeholder types for static type checking
    MOCK_POSITIONS = []
    MOCK_ACCOUNT = {}

# Configure logging
logger = logging.getLogger("discord.matrix_bot_commands")

# Emoji constants for better visual presentation
EMOJI_MATRIX = "🧮"
EMOJI_CYBERPUNK = "🤖"
EMOJI_BITCOIN = "₿"
EMOJI_WARNING = "⚠️"
EMOJI_LOCK = "🔒"
EMOJI_KEY = "🔑"
EMOJI_INFO = "ℹ️"
EMOJI_CHECK = "✅"
EMOJI_CROSS = "❌"
EMOJI_STAR = "⭐"
EMOJI_FIRE = "🔥"
EMOJI_CHART_UP = "📈"
EMOJI_CHART_DOWN = "📉"
EMOJI_PILL_RED = "🔴"
EMOJI_PILL_BLUE = "🔵"

# Cyberpunk styled messages for flair
CYBERPUNK_HEADERS = [
    "NEURAL INTERFACE CONNECTED",
    "MATRIX DATA STREAM ACCESSED",
    "QUANTUM ENCRYPTION ACTIVE",
    "BLOCKCHAIN VISUALIZATION ONLINE",
    "BIO-DIGITAL JAZZ INITIATED",
    "REALITY DISTORTION FIELD ENGAGED",
    "DIGITAL CONSCIOUSNESS AWAKENED",
    "NEURAL NETWORK SYNCHRONIZED",
    "CRYPTOGRAPHIC HANDSHAKE COMPLETE",
    "MATRIX COORDINATES LOCKED"
]

class MatrixBotCommands(commands.Cog):
    """
    Discord commands for BitGet Matrix CLI Bot.
    
    This cog provides commands to interact with the BitGetMatrixCliB0t,
    allowing users to visualize BitGet positions with cyberpunk Matrix styling
    directly in Discord.
    """
    
    def __init__(self, bot):
        """
        Initialize the Matrix Bot Commands cog.
        
        Args:
            bot: The Discord bot instance
        """
        self.bot = bot
        self.matrix_bot = None
        self.matrix_bots = {}  # Dictionary to store user-specific matrix bots
        
        # Initialize if available
        self._initialize_default_matrix_bot()
        
        # Log status
        if self.matrix_bot:
            logging.info("Matrix Bot initialized successfully with mock data")
        else:
            logging.warning("Matrix Bot initialization failed")
        
    def _initialize_default_matrix_bot(self):
        """Initialize the default matrix bot with mock data."""
        if not MATRIX_BOT_AVAILABLE:
            logger.warning("BitGetMatrixCliB0t not available. Commands will be limited.")
            return
            
        try:
            # Try to initialize the matrix bot with mock data
            self.matrix_bot = BitGetMatrixCliB0t(positions=MOCK_POSITIONS, account=MOCK_ACCOUNT, headless=True)
            logger.info("Initialized default BitGetMatrixCliB0t with mock data")
        except Exception as e:
            logger.error(f"Failed to initialize default BitGetMatrixCliB0t: {e}")
            self.matrix_bot = None
    
    async def _get_user_matrix_bot(self, user_id: int) -> Optional[BitGetMatrixCliB0t]:
        """
        Get or create a user-specific matrix bot.
        
        Args:
            user_id: The Discord user ID
            
        Returns:
            BitGetMatrixCliB0t instance or None if unavailable
        """
        if not MATRIX_BOT_AVAILABLE:
            return None
            
        # Return existing matrix bot if available
        if user_id in self.matrix_bots:
            return self.matrix_bots[user_id]
            
        # Try to use default matrix bot
        if self.matrix_bot:
            return self.matrix_bot
            
        return None
    
    def _format_discord_matrix_text(self, text: str) -> str:
        """
        Format text for Discord with Matrix styling.
        
        Args:
            text: The text to format
            
        Returns:
            Formatted text with Discord markdown for Matrix style
        """
        # Add code block markdown with ansi for color support
        # Note: Discord doesn't support ANSI color codes in normal messages, 
        # so we'll use code blocks with simple formatting
        return f"```ansi\n{text}\n```"
    
    def _generate_cyberpunk_embed(self, title: str, description: str) -> discord.Embed:
        """
        Generate a cyberpunk-styled embed for Discord.
        
        Args:
            title: The title for the embed
            description: The description for the embed
            
        Returns:
            Discord embed with cyberpunk styling
        """
        # Choose a cyberpunk color - neon green, neon blue, neon pink, etc.
        cyberpunk_colors = [0x00FF00, 0x00FFFF, 0xFF00FF, 0xFF3300, 0x33CCFF]
        color = random.choice(cyberpunk_colors)
        
        # Create embed
        embed = discord.Embed(
            title=f"{EMOJI_CYBERPUNK} {title} {EMOJI_MATRIX}",
            description=f"_{description}_",
            color=color
        )
        
        # Add random cyberpunk header
        header = random.choice(CYBERPUNK_HEADERS)
        embed.set_footer(text=f"{header} | OMEGA BOT FARM")
        
        # Set timestamp
        embed.timestamp = discord.utils.utcnow()
        
        return embed
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Event handler when the cog is ready."""
        logger.info("MatrixBotCommands cog is ready!")
    
    @app_commands.command(
        name="matrix-positions",
        description="Show BitGet positions with Matrix-themed visualization"
    )
    async def matrix_positions(self, interaction: discord.Interaction):
        """
        Command to show BitGet positions with Matrix-styled visualization.
        
        Args:
            interaction: The Discord interaction
        """
        if not MATRIX_BOT_AVAILABLE:
            await interaction.response.send_message(
                f"{EMOJI_WARNING} BitGetMatrixCliB0t is not available. This command cannot be used.",
                ephemeral=True
            )
            return
            
        # Defer response since this might take a moment
        await interaction.response.defer()
        
        # Get matrix bot for this user
        matrix_bot = await self._get_user_matrix_bot(interaction.user.id)
        if not matrix_bot:
            await interaction.followup.send(
                f"{EMOJI_WARNING} Failed to initialize Matrix visualization. Please try again later.",
                ephemeral=True
            )
            return
        
        # Update positions (this would normally fetch from API)
        matrix_bot.update_positions()
        
        # Create positions text output
        positions_text = ""
        for position in matrix_bot.positions:
            # Add separation between positions
            if positions_text:
                positions_text += "\n" + "-" * 50 + "\n"
            
            # Override the print method for position to capture output
            position_text = ""
            original_print = print
            
            def capture_print(*args, **kwargs):
                nonlocal position_text
                kwargs['end'] = kwargs.get('end', '\n')
                position_text += ' '.join(str(arg) for arg in args) + kwargs['end']
            
            try:
                # Temporarily replace print function
                builtins.print = capture_print
                
                # Generate position text
                matrix_bot.print_position(position)
                
            finally:
                # Restore print function
                builtins.print = original_print
            
            positions_text += position_text
        
        # Format text for Discord
        formatted_text = self._format_discord_matrix_text(positions_text)
        
        # Create embed
        embed = self._generate_cyberpunk_embed(
            "MATRIX POSITIONS", 
            "Neural visualization of your BitGet positions in the Matrix"
        )
        
        # Add position summary fields
        total_positions = len(matrix_bot.positions)
        total_value = sum(p.get('notional', 0) for p in matrix_bot.positions)
        total_pnl = sum(p.get('unrealizedPnl', 0) for p in matrix_bot.positions)
        
        embed.add_field(
            name=f"{EMOJI_INFO} Position Summary",
            value=f"Total Positions: **{total_positions}**\nValue: **${total_value:.2f}**\nPnL: **${total_pnl:.2f}**",
            inline=False
        )
        
        # Send response with both embed and code block
        await interaction.followup.send(
            content=formatted_text,
            embed=embed
        )
    
    @app_commands.command(
        name="matrix-account",
        description="Show account overview with Matrix-themed visualization"
    )
    async def matrix_account(self, interaction: discord.Interaction):
        """
        Command to show account overview with Matrix-styled visualization.
        
        Args:
            interaction: The Discord interaction
        """
        if not MATRIX_BOT_AVAILABLE:
            await interaction.response.send_message(
                f"{EMOJI_WARNING} BitGetMatrixCliB0t is not available. This command cannot be used.",
                ephemeral=True
            )
            return
            
        # Defer response
        await interaction.response.defer()
        
        # Get matrix bot for this user
        matrix_bot = await self._get_user_matrix_bot(interaction.user.id)
        if not matrix_bot:
            await interaction.followup.send(
                f"{EMOJI_WARNING} Failed to initialize Matrix visualization. Please try again later.",
                ephemeral=True
            )
            return
        
        # Generate account summary text
        account_text = ""
        original_print = print
        
        def capture_print(*args, **kwargs):
            nonlocal account_text
            kwargs['end'] = kwargs.get('end', '\n')
            account_text += ' '.join(str(arg) for arg in args) + kwargs['end']
        
        try:
            # Temporarily replace print function
            builtins.print = capture_print
            
            # Generate account text
            matrix_bot.print_cyberpunk_header()
            matrix_bot.print_account_summary()
            matrix_bot.print_cyberpunk_footer()
            
        finally:
            # Restore print function
            builtins.print = original_print
        
        # Format text for Discord
        formatted_text = self._format_discord_matrix_text(account_text)
        
        # Create embed
        embed = self._generate_cyberpunk_embed(
            "MATRIX ACCOUNT", 
            "Digital representation of your trading capital in the Matrix"
        )
        
        # Add account metrics fields
        account = matrix_bot.account
        embed.add_field(
            name=f"{EMOJI_BITCOIN} Balance & Equity",
            value=f"Balance: **${account.get('balance', 0):.2f}**\nEquity: **${account.get('equity', 0):.2f}**",
            inline=True
        )
        
        embed.add_field(
            name=f"{EMOJI_CHART_UP} Exposure",
            value=f"Long: **${account.get('long_exposure', 0):.2f}**\nShort: **${account.get('short_exposure', 0):.2f}**\nRatio: **{account.get('long_short_ratio', 0):.2f}**",
            inline=True
        )
        
        embed.add_field(
            name=f"{EMOJI_STAR} Harmony Score",
            value=f"**{account.get('harmony_score', 0) * 100:.2f}%**",
            inline=True
        )
        
        # Send response with both embed and code block
        await interaction.followup.send(
            content=formatted_text,
            embed=embed
        )
    
    @app_commands.command(
        name="matrix-snapshot",
        description="Take a snapshot of current positions with cyberpunk styling"
    )
    async def matrix_snapshot(self, interaction: discord.Interaction):
        """
        Command to take a snapshot of current positions with cyberpunk styling.
        
        Args:
            interaction: The Discord interaction
        """
        if not MATRIX_BOT_AVAILABLE:
            await interaction.response.send_message(
                f"{EMOJI_WARNING} BitGetMatrixCliB0t is not available. This command cannot be used.",
                ephemeral=True
            )
            return
            
        # Defer response
        await interaction.response.defer()
        
        # Get matrix bot for this user
        matrix_bot = await self._get_user_matrix_bot(interaction.user.id)
        if not matrix_bot:
            await interaction.followup.send(
                f"{EMOJI_WARNING} Failed to initialize Matrix visualization. Please try again later.",
                ephemeral=True
            )
            return
        
        # Generate snapshot text
        snapshot_text = ""
        original_print = print
        
        def capture_print(*args, **kwargs):
            nonlocal snapshot_text
            kwargs['end'] = kwargs.get('end', '\n')
            snapshot_text += ' '.join(str(arg) for arg in args) + kwargs['end']
        
        try:
            # Temporarily replace print function
            builtins.print = capture_print
            
            # Generate snapshot text - full display
            matrix_bot.display()
            
        finally:
            # Restore print function
            builtins.print = original_print
        
        # Format text for Discord
        formatted_text = self._format_discord_matrix_text(snapshot_text)
        
        # Create embed
        embed = self._generate_cyberpunk_embed(
            "MATRIX SNAPSHOT", 
            "Complete cyberpunk snapshot of your trading presence in the Matrix"
        )
        
        # Add timestamp and user information
        embed.add_field(
            name=f"{EMOJI_INFO} Snapshot Info",
            value=f"User: **{interaction.user.name}**\nTime: <t:{int(discord.utils.utcnow().timestamp())}:F>",
            inline=False
        )
        
        # Show pill choices as a fun reference
        pill_choice = EMOJI_PILL_BLUE if random.random() > 0.5 else EMOJI_PILL_RED
        embed.add_field(
            name="Matrix Reality",
            value=f"You chose the {pill_choice} pill",
            inline=False
        )
        
        # Send response with both embed and code block
        await interaction.followup.send(
            content=formatted_text,
            embed=embed
        )

def setup(bot):
    """
    Set up the Matrix Bot Commands cog.
    
    Args:
        bot: The Discord bot instance
    """
    if not MATRIX_BOT_AVAILABLE:
        logging.warning("BitGetMatrixCliB0t not available. Matrix commands will be disabled.")
        return
        
    try:
        bot.add_cog(MatrixBotCommands(bot))
        logging.info("Matrix Bot Commands registered successfully")
    except Exception as e:
        logging.error(f"Failed to register Matrix Bot Commands: {e}") 