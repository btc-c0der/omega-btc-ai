#!/usr/bin/env python3

"""
Discord commands for BitGet position analysis.

This module provides commands to interact with the BitgetPositionAnalyzerB0t,
allowing users to analyze their BitGet positions, get Fibonacci levels,
and receive portfolio recommendations directly in Discord.

Copyright (c) 2024 OMEGA BTC AI
Licensed under the GBU2 License - see LICENSE file for details
"""

import os
import json
import asyncio
import logging
import discord
from discord import app_commands
from discord.ext import commands
from typing import Dict, List, Any, Optional, Tuple, TYPE_CHECKING

try:
    import ccxt
    CCXT_AVAILABLE = True
except ImportError:
    CCXT_AVAILABLE = False
    logging.warning("CCXT not available. Features will be limited.")

# Import BitgetPositionAnalyzerB0t for type checking
if TYPE_CHECKING:
    from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t

# Try to import BitgetPositionAnalyzerB0t for runtime
try:
    from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t
    from src.omega_bot_farm.services.exchange_service import create_exchange_service
    ANALYZER_AVAILABLE = True and CCXT_AVAILABLE
except ImportError:
    ANALYZER_AVAILABLE = False
    logging.warning("BitgetPositionAnalyzerB0t not available. Features will be limited.")

# Configure logging
logger = logging.getLogger("discord.bitget_position_commands")

# Emoji constants for better visual presentation
EMOJI_GREEN_CIRCLE = "🟢"
EMOJI_RED_CIRCLE = "🔴"
EMOJI_BLUE_CIRCLE = "🔵"
EMOJI_CHART = "📊"
EMOJI_MONEY = "💰"
EMOJI_WARNING = "⚠️"
EMOJI_ROCKET = "🚀"
EMOJI_LOCK = "🔒"
EMOJI_KEY = "🔑"
EMOJI_INFO = "ℹ️"
EMOJI_CHECK = "✅"
EMOJI_CROSS = "❌"
EMOJI_STAR = "⭐"
EMOJI_FIRE = "🔥"
EMOJI_CHART_UP = "📈"
EMOJI_CHART_DOWN = "📉"
EMOJI_MEDITATION = "🧘"
EMOJI_INFINITY = "♾️"
EMOJI_SPIRAL = "🌀"

class BitgetPositionCommands(commands.Cog):
    """
    Discord commands for BitGet position analysis.
    
    This cog provides commands to interact with the BitgetPositionAnalyzerB0t,
    allowing users to analyze their BitGet positions, get Fibonacci levels,
    and receive portfolio recommendations directly in Discord.
    """
    
    def __init__(self, bot: commands.Bot):
        """
        Initialize the BitGet Position Commands cog.
        
        Args:
            bot: The Discord bot instance
        """
        self.bot = bot
        self.analyzer = None
        self.analyzers: Dict[int, 'BitgetPositionAnalyzerB0t'] = {}
        
        # Initialize if available
        self._initialize_default_analyzer()
        
    def _initialize_default_analyzer(self) -> Optional['BitgetPositionAnalyzerB0t']:
        """Initialize the default BitgetPositionAnalyzerB0t instance."""
        if not ANALYZER_AVAILABLE:
            logger.warning("BitgetPositionAnalyzerB0t not available")
            return None
            
        try:
            # Create config dictionary with required parameters
            config = {
                'api_key': os.getenv('BITGET_API_KEY', ''),
                'api_secret': os.getenv('BITGET_SECRET_KEY', ''),
                'api_password': os.getenv('BITGET_PASSPHRASE', ''),
                'use_testnet': os.getenv('BITGET_USE_TESTNET', 'true').lower() == 'true',
                'symbol': os.getenv('BITGET_SYMBOL', 'BTC/USDT'),
                'position_history_length': int(os.getenv('BITGET_POSITION_HISTORY_LENGTH', '10'))
            }
            
            # Initialize the analyzer with the config
            analyzer = BitgetPositionAnalyzerB0t(config=config)
            logger.info("Successfully initialized BitgetPositionAnalyzerB0t")
            return analyzer
            
        except Exception as e:
            logger.error(f"Failed to initialize default BitgetPositionAnalyzerB0t: {str(e)}")
            return None
    
    async def _get_user_analyzer(self, user_id: int) -> Optional['BitgetPositionAnalyzerB0t']:
        """
        Get or create a user-specific analyzer.
        
        Args:
            user_id: The Discord user ID
            
        Returns:
            BitgetPositionAnalyzerB0t instance or None if unavailable
        """
        if not ANALYZER_AVAILABLE:
            return None
            
        # Return existing analyzer if available
        if user_id in self.analyzers:
            return self.analyzers[user_id]
            
        # Try to use default analyzer
        if self.analyzer:
            return self.analyzer
            
        return None
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Event handler when the cog is ready."""
        logger.info("BitgetPositionCommands cog is ready!")
    
    @app_commands.command(
        name="bitget-setup",
        description="Set up your BitGet API credentials (securely via DM only)"
    )
    async def setup_credentials(self, interaction: discord.Interaction):
        """
        Command to set up BitGet API credentials (securely via DM).
        
        Args:
            interaction: The Discord interaction
        """
        if not ANALYZER_AVAILABLE:
            await interaction.response.send_message(
                f"{EMOJI_WARNING} BitgetPositionAnalyzerB0t is not available. This command cannot be used.",
                ephemeral=True
            )
            return
            
        # Initial response in the channel
        await interaction.response.send_message(
            f"{EMOJI_LOCK} I'll send you a DM to securely set up your BitGet API credentials.",
            ephemeral=True
        )
        
        # Send DM for secure credential setup
        try:
            # Create DM channel
            dm_channel = await interaction.user.create_dm()
            
            # Send instructions
            await dm_channel.send(
                f"{EMOJI_KEY} **BitGet API Setup**\n\n"
                f"To analyze your BitGet positions, I need your API credentials. "
                f"These will be stored securely for your Discord user only.\n\n"
                f"Please provide your credentials in this format:\n"
                f"```\n"
                f"!setup-bitget\n"
                f"API_KEY: your_api_key_here\n"
                f"SECRET_KEY: your_secret_key_here\n"
                f"PASSPHRASE: your_passphrase_here\n"
                f"```\n"
                f"You can also specify `TESTNET: true` if you want to use the testnet.\n\n"
                f"{EMOJI_WARNING} Keep your credentials secure! Never share them in public channels."
            )
            
        except discord.Forbidden:
            # Cannot send DM
            await interaction.followup.send(
                f"{EMOJI_WARNING} I couldn't send you a DM. Please ensure your privacy settings allow DMs from server members.",
                ephemeral=True
            )

    @commands.command(name="setup-bitget")
    async def process_credentials(self, ctx):
        """
        Process BitGet API credentials from DM.
        
        Args:
            ctx: The command context
        """
        if not ANALYZER_AVAILABLE:
            await ctx.send(f"{EMOJI_WARNING} BitgetPositionAnalyzerB0t is not available. This command cannot be used.")
            return
            
        # Only process in DM channel
        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.send(f"{EMOJI_WARNING} This command can only be used in a DM for security reasons.")
            return
            
        # Parse credentials from message
        try:
            lines = ctx.message.content.split('\n')
            
            # Extract credentials
            api_key = next((line.split('API_KEY:', 1)[1].strip() for line in lines if 'API_KEY:' in line), None)
            secret_key = next((line.split('SECRET_KEY:', 1)[1].strip() for line in lines if 'SECRET_KEY:' in line), None)
            passphrase = next((line.split('PASSPHRASE:', 1)[1].strip() for line in lines if 'PASSPHRASE:' in line), None)
            testnet = next((line.split('TESTNET:', 1)[1].strip().lower() == 'true' for line in lines if 'TESTNET:' in line), False)
            
            # Validate credentials
            if not api_key or not secret_key or not passphrase:
                await ctx.send(f"{EMOJI_WARNING} Missing required credentials. Please provide API_KEY, SECRET_KEY, and PASSPHRASE.")
                return
                
            # Initialize user-specific analyzer
            self.analyzers[ctx.author.id] = BitgetPositionAnalyzerB0t(
                api_key=api_key,
                api_secret=secret_key,
                api_passphrase=passphrase,
                use_testnet=testnet
            )
            
            # Delete the message with credentials for security
            await ctx.message.delete()
            
            # Confirm setup
            await ctx.send(
                f"{EMOJI_CHECK} BitGet API credentials set up successfully!\n"
                f"Environment: {'**TESTNET**' if testnet else '**MAINNET**'}\n\n"
                f"You can now use the `/bitget-positions` and other BitGet commands."
            )
            
        except Exception as e:
            logger.error(f"Error processing credentials: {e}")
            await ctx.send(
                f"{EMOJI_CROSS} Error setting up credentials. Please ensure the format is correct.\n"
                f"Error: {str(e)}"
            )

    @app_commands.command(
        name="bitget-positions",
        description="Show your current BitGet positions"
    )
    async def show_positions(self, interaction: discord.Interaction):
        """
        Command to show current BitGet positions.
        
        Args:
            interaction: The Discord interaction
        """
        await interaction.response.defer(ephemeral=True)
        
        # Get analyzer for the user
        analyzer = await self._get_user_analyzer(interaction.user.id)
        
        if not analyzer:
            await interaction.followup.send(
                f"{EMOJI_WARNING} BitGet position analyzer is not available. Please set up your credentials with `/bitget-setup`.",
                ephemeral=True
            )
            return
            
        try:
            # Get positions
            positions_data = await analyzer.get_positions()
            
            if "error" in positions_data:
                await interaction.followup.send(
                    f"{EMOJI_WARNING} Error fetching positions: {positions_data['error']}",
                    ephemeral=True
                )
                return
                
            positions = positions_data.get("positions", [])
            
            if not positions:
                await interaction.followup.send(
                    f"{EMOJI_INFO} You currently have no open positions on BitGet.",
                    ephemeral=True
                )
                return
                
            # Create embed for positions
            embed = discord.Embed(
                title=f"{EMOJI_CHART} BitGet Positions",
                description=f"You have {len(positions)} open positions",
                color=discord.Color.gold()
            )
            
            # Account stats
            account = positions_data.get("account", {})
            embed.add_field(
                name="Account Overview",
                value=(
                    f"**Balance**: ${account.get('balance', 0):.2f}\n"
                    f"**Equity**: ${account.get('equity', 0):.2f}\n"
                    f"**Total PnL**: ${account.get('total_pnl', 0):.2f}\n"
                    f"**Long/Short Ratio**: {account.get('long_short_ratio', 0):.2f}\n"
                    f"**Exposure/Equity**: {account.get('exposure_to_equity_ratio', 0):.2f}\n"
                    f"**Harmony Score**: {account.get('harmony_score', 0):.2f}/1.0"
                ),
                inline=False
            )
            
            # Add position details
            for position in positions:
                symbol = position.get("symbol", "Unknown")
                side = position.get("side", "Unknown")
                entry_price = float(position.get("entryPrice", 0))
                mark_price = float(position.get("markPrice", 0))
                contracts = float(position.get("contracts", 0))
                notional = float(position.get("notional", 0))
                pnl = float(position.get("unrealizedPnl", 0))
                
                # Calculate PnL percentage
                pnl_percentage = 0
                if notional != 0:
                    pnl_percentage = (pnl / notional) * 100
                
                # Set emoji and color based on side and PnL
                side_emoji = EMOJI_CHART_UP if side.lower() == "long" else EMOJI_CHART_DOWN
                pnl_emoji = EMOJI_GREEN_CIRCLE if pnl > 0 else EMOJI_RED_CIRCLE
                
                embed.add_field(
                    name=f"{side_emoji} {symbol} {side.upper()}",
                    value=(
                        f"**Entry**: ${entry_price:.2f}\n"
                        f"**Current**: ${mark_price:.2f}\n"
                        f"**Size**: {contracts:.4f} (${notional:.2f})\n"
                        f"{pnl_emoji} **PnL**: ${pnl:.2f} ({pnl_percentage:.2f}%)"
                    ),
                    inline=True
                )
            
            # Add timestamp
            embed.set_footer(text=f"Last updated: {positions_data.get('timestamp', 'Unknown')}")
            
            # Send the embed
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except Exception as e:
            logger.error(f"Error showing positions: {e}")
            await interaction.followup.send(
                f"{EMOJI_WARNING} Error fetching positions: {str(e)}",
                ephemeral=True
            )

    @app_commands.command(
        name="bitget-analyze",
        description="Analyze your BitGet positions with Fibonacci levels"
    )
    async def analyze_positions(self, interaction: discord.Interaction):
        """
        Command to analyze BitGet positions with Fibonacci levels.
        
        Args:
            interaction: The Discord interaction
        """
        await interaction.response.defer(ephemeral=True)
        
        # Get analyzer for the user
        analyzer = await self._get_user_analyzer(interaction.user.id)
        
        if not analyzer:
            await interaction.followup.send(
                f"{EMOJI_WARNING} BitGet position analyzer is not available. Please set up your credentials with `/bitget-setup`.",
                ephemeral=True
            )
            return
            
        try:
            # Get comprehensive analysis
            analysis = analyzer.analyze_all_positions()
            
            # If it's a coroutine (when using exchange_service), run it
            if asyncio.iscoroutine(analysis):
                analysis = await analysis
            
            if "error" in analysis:
                await interaction.followup.send(
                    f"{EMOJI_WARNING} Error analyzing positions: {analysis['error']}",
                    ephemeral=True
                )
                return
                
            position_analyses = analysis.get("position_analyses", [])
            
            if not position_analyses:
                await interaction.followup.send(
                    f"{EMOJI_INFO} No positions to analyze on BitGet.",
                    ephemeral=True
                )
                return
                
            # Create main embed for analysis overview
            overview_embed = discord.Embed(
                title=f"{EMOJI_SPIRAL} BitGet Position Analysis",
                description=(
                    f"**Harmony Score**: {analysis.get('harmony_score', 0):.2f}/1.0\n"
                    f"**Total Positions**: {analysis.get('total_positions', 0)}\n"
                ),
                color=discord.Color.purple()
            )
            
            # Add recommendations
            recommendations = analysis.get("recommendations", [])
            if recommendations:
                overview_embed.add_field(
                    name=f"{EMOJI_STAR} Recommendations",
                    value="\n".join([f"• {rec}" for rec in recommendations]),
                    inline=False
                )
            
            # Add account stats
            account_stats = analysis.get("account_stats", {})
            if account_stats:
                overview_embed.add_field(
                    name="Account Overview",
                    value=(
                        f"**Balance**: ${account_stats.get('balance', 0):.2f}\n"
                        f"**Equity**: ${account_stats.get('equity', 0):.2f}\n"
                        f"**Long Exposure**: ${account_stats.get('long_exposure', 0):.2f}\n"
                        f"**Short Exposure**: ${account_stats.get('short_exposure', 0):.2f}\n"
                        f"**Long/Short Ratio**: {account_stats.get('long_short_ratio', 0):.2f}\n"
                        f"**Exposure/Equity**: {account_stats.get('exposure_to_equity_ratio', 0):.2f}\n"
                    ),
                    inline=False
                )
            
            # Send the overview embed
            await interaction.followup.send(embed=overview_embed, ephemeral=True)
            
            # Create and send a separate embed for each position analysis
            for pos_analysis in position_analyses:
                position = pos_analysis.get("position", {})
                analysis_data = pos_analysis.get("analysis", {})
                
                symbol = position.get("symbol", "Unknown")
                side = position.get("side", "Unknown").upper()
                
                # Emoji based on side
                side_emoji = EMOJI_CHART_UP if side == "LONG" else EMOJI_CHART_DOWN
                
                # Create embed for this position
                position_embed = discord.Embed(
                    title=f"{side_emoji} {symbol} {side}",
                    description="Fibonacci Analysis",
                    color=discord.Color.blue() if side == "LONG" else discord.Color.red()
                )
                
                # Add position details
                entry_price = float(position.get("entryPrice", 0))
                mark_price = float(position.get("markPrice", 0))
                position_embed.add_field(
                    name="Position Details",
                    value=(
                        f"**Entry Price**: ${entry_price:.2f}\n"
                        f"**Current Price**: ${mark_price:.2f}\n"
                        f"**Size**: {float(position.get('contracts', 0)):.4f}\n"
                        f"**Notional**: ${float(position.get('notional', 0)):.2f}\n"
                        f"**Leverage**: {float(position.get('leverage', 0)):.2f}x\n"
                        f"**PnL**: ${float(position.get('unrealizedPnl', 0)):.2f} ({analysis_data.get('pnl_percentage', 0):.2f}%)\n"
                    ),
                    inline=True
                )
                
                # Add Fibonacci levels
                fib_levels = analysis_data.get("fibonacci_levels", {})
                if fib_levels:
                    # Format the Fibonacci levels
                    fib_text = ""
                    for level_name, level_data in fib_levels.items():
                        price = level_data.get("price", 0)
                        percentage = level_data.get("percentage", 0)
                        fib_text += f"**{level_name}**: ${price:.2f} ({percentage:.1f}%)\n"
                    
                    position_embed.add_field(
                        name="Fibonacci Levels",
                        value=fib_text,
                        inline=True
                    )
                
                # Add recommendations
                tp = analysis_data.get("recommended_take_profit")
                sl = analysis_data.get("recommended_stop_loss")
                
                recommendations = []
                if tp:
                    recommendations.append(f"**Take Profit**: ${tp[1]:.2f} ({tp[0]})")
                if sl:
                    recommendations.append(f"**Stop Loss**: ${sl[1]:.2f} ({sl[0]})")
                
                if recommendations:
                    position_embed.add_field(
                        name=f"{EMOJI_STAR} Recommendations",
                        value="\n".join(recommendations),
                        inline=False
                    )
                
                # Add harmony score
                harmony = analysis_data.get("harmony_score", 0)
                position_embed.add_field(
                    name=f"{EMOJI_INFINITY} Position Harmony",
                    value=f"**Score**: {harmony:.2f}/1.0",
                    inline=False
                )
                
                # Send this position's analysis
                await interaction.followup.send(embed=position_embed, ephemeral=True)
            
        except Exception as e:
            logger.error(f"Error analyzing positions: {e}")
            await interaction.followup.send(
                f"{EMOJI_WARNING} Error analyzing positions: {str(e)}",
                ephemeral=True
            )

    @app_commands.command(
        name="bitget-changes",
        description="Show recent changes in your BitGet positions"
    )
    async def show_position_changes(self, interaction: discord.Interaction):
        """
        Command to show recent changes in BitGet positions.
        
        Args:
            interaction: The Discord interaction
        """
        await interaction.response.defer(ephemeral=True)
        
        # Get analyzer for the user
        analyzer = await self._get_user_analyzer(interaction.user.id)
        
        if not analyzer:
            await interaction.followup.send(
                f"{EMOJI_WARNING} BitGet position analyzer is not available. Please set up your credentials with `/bitget-setup`.",
                ephemeral=True
            )
            return
            
        try:
            # Get positions to access change data
            positions_data = await analyzer.get_positions()
            
            if "error" in positions_data:
                await interaction.followup.send(
                    f"{EMOJI_WARNING} Error fetching position changes: {positions_data['error']}",
                    ephemeral=True
                )
                return
                
            changes = positions_data.get("changes", {})
            
            if not changes or all(len(changes.get(k, [])) == 0 for k in changes):
                await interaction.followup.send(
                    f"{EMOJI_INFO} No recent changes detected in your BitGet positions.",
                    ephemeral=True
                )
                return
                
            # Create embed for changes
            embed = discord.Embed(
                title=f"{EMOJI_CHART} BitGet Position Changes",
                description="Recent changes in your positions",
                color=discord.Color.blue()
            )
            
            # Add new positions
            new_positions = changes.get("new_positions", [])
            if new_positions:
                new_text = ""
                for pos in new_positions:
                    symbol = pos.get("symbol", "Unknown")
                    side = pos.get("side", "Unknown").upper()
                    entry_price = float(pos.get("entryPrice", 0))
                    size = float(pos.get("contracts", 0))
                    
                    side_emoji = EMOJI_CHART_UP if side.lower() == "long" else EMOJI_CHART_DOWN
                    new_text += f"{side_emoji} **{symbol} {side}** - ${entry_price:.2f} x {size:.4f}\n"
                
                embed.add_field(
                    name=f"{EMOJI_GREEN_CIRCLE} New Positions",
                    value=new_text or "None",
                    inline=False
                )
            
            # Add closed positions
            closed_positions = changes.get("closed_positions", [])
            if closed_positions:
                closed_text = ""
                for pos in closed_positions:
                    symbol = pos.get("symbol", "Unknown")
                    side = pos.get("side", "Unknown").upper()
                    entry_price = float(pos.get("entryPrice", 0))
                    
                    side_emoji = EMOJI_CHART_UP if side.lower() == "long" else EMOJI_CHART_DOWN
                    closed_text += f"{side_emoji} **{symbol} {side}** - ${entry_price:.2f}\n"
                
                embed.add_field(
                    name=f"{EMOJI_RED_CIRCLE} Closed Positions",
                    value=closed_text or "None",
                    inline=False
                )
            
            # Add changed positions
            changed_positions = changes.get("changed_positions", [])
            if changed_positions:
                changed_text = ""
                for change in changed_positions:
                    old_pos = change.get("old", {})
                    new_pos = change.get("new", {})
                    
                    symbol = new_pos.get("symbol", "Unknown")
                    side = new_pos.get("side", "Unknown").upper()
                    old_size = float(old_pos.get("contracts", 0))
                    new_size = float(new_pos.get("contracts", 0))
                    
                    size_change = new_size - old_size
                    change_text = f"+{size_change:.4f}" if size_change > 0 else f"{size_change:.4f}"
                    
                    side_emoji = EMOJI_CHART_UP if side.lower() == "long" else EMOJI_CHART_DOWN
                    changed_text += f"{side_emoji} **{symbol} {side}** - Size: {old_size:.4f} → {new_size:.4f} ({change_text})\n"
                
                embed.add_field(
                    name=f"{EMOJI_BLUE_CIRCLE} Changed Positions",
                    value=changed_text or "None",
                    inline=False
                )
            
            # Add timestamp
            embed.set_footer(text=f"Last updated: {positions_data.get('timestamp', 'Unknown')}")
            
            # Send the embed
            await interaction.followup.send(embed=embed, ephemeral=True)
            
        except Exception as e:
            logger.error(f"Error showing position changes: {e}")
            await interaction.followup.send(
                f"{EMOJI_WARNING} Error fetching position changes: {str(e)}",
                ephemeral=True
            )

    @app_commands.command(
        name="golden-wisdom",
        description="Receive trading wisdom based on Fibonacci principles"
    )
    async def golden_wisdom(self, interaction: discord.Interaction):
        """
        Command to receive trading wisdom based on Fibonacci principles.
        
        Args:
            interaction: The Discord interaction
        """
        # Fibonacci-inspired trading wisdom
        wisdom_quotes = [
            "As above, so below; the market follows patterns seen throughout nature.",
            "The whole is greater than the sum of its parts. See the market as a living organism.",
            "Like the golden spiral, markets expand and contract in predictable sequences.",
            "Embrace the natural rhythm of the market - periods of growth followed by necessary retracement.",
            "The strongest support and resistance often appear at Fibonacci levels.",
            "Trade in harmony with the market's natural flow, not against it.",
            "Your position size should reflect the inverse golden ratio of your equity.",
            "True trading mastery comes from alignment with natural proportions.",
            "The spiral of market cycles repeats at different scales, from minute to decade.",
            "Balance between action and patience creates the most harmonious trading.",
            "Divine proportion exists in markets; learn to see it and profit will follow.",
            "Perfect harmony in trading comes not from perfection, but from balanced imperfection.",
            "The Fibonacci sequence teaches that each step builds upon previous foundations.",
            "Like nature's patterns, market patterns are self-similar at different scales.",
            "The price tells a story of human emotion that repeats in golden proportions.",
        ]
        
        # Randomly select wisdom
        import random
        wisdom = random.choice(wisdom_quotes)
        
        # Create embed for wisdom
        embed = discord.Embed(
            title=f"{EMOJI_SPIRAL} Fibonacci Trading Wisdom",
            description=f"*\"{wisdom}\"*",
            color=discord.Color.gold()
        )
        
        embed.set_footer(text="Inspired by the Golden Ratio (φ) - 1.618034...")
        
        # Send the wisdom
        await interaction.response.send_message(embed=embed)

# Discord setup function to add the cog
def setup(bot):
    """
    Add the BitgetPositionCommands cog to the bot.
    
    Args:
        bot: The Discord bot
    """
    bot.add_cog(BitgetPositionCommands(bot)) 