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
RASTA BitGet Discord Bot

Discord bot integration for the RASTA BitGet Position Monitor.
Allows users to check positions, get harmony analysis, and receive Rasta wisdom directly in Discord.
"""

import os
import asyncio
import discord
from discord.ext import commands, tasks
from discord import app_commands
import io
import random
from datetime import datetime
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Import our monitor modules
from bitget_data_manager import BitgetDataManager
from position_harmony import PositionHarmonyManager
from display_utils import RASTA_FRAMES, GREEN, YELLOW, RED, RESET

# Configure the bot
load_dotenv()  # Load API keys from .env file
TOKEN = os.getenv("DISCORD_BOT_TOKEN", "abef74ec8534cf65c6c81106858e30aaea235f6bba1e43f5e828f01659b0f596")
APP_ID = os.getenv("DISCORD_APP_ID", "1357128992053788822")
GUILD_ID = os.getenv("DISCORD_GUILD_ID", None)  # Optional: for dev testing with a specific guild

# Set up intents for Discord bot
intents = discord.Intents.default()
intents.message_content = True

# Create the bot
bot = commands.Bot(command_prefix="!rasta ", intents=intents)

# Initialize our services
data_manager = BitgetDataManager()
harmony_manager = PositionHarmonyManager()

# Channel subscriptions for automatic updates
position_update_channels = set()

@bot.event
async def on_ready():
    """Event triggered when the bot is ready."""
    print(f"╔════════════════════════════════════════════════════════════════════╗")
    print(f"║   {GREEN}█{YELLOW}█{RED}█{RESET} RASTA BitGet Discord Bot Connected! {GREEN}█{YELLOW}█{RED}█{RESET}")
    print(f"╚════════════════════════════════════════════════════════════════════╝")
    print(f"Logged in as: {bot.user.name}")
    print(f"Bot User ID: {bot.user.id}")
    print(f"Connected to {len(bot.guilds)} servers")
    
    # Start the position checker task
    position_checker.start()
    
    # Sync app commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@tasks.loop(minutes=5)
async def position_checker():
    """Background task to periodically check position changes and send updates."""
    if not position_update_channels:
        return
        
    try:
        # Get positions
        data = data_manager.get_positions()
        
        # Skip if there was an error
        if "error" in data:
            print(f"Error checking positions: {data['error']}")
            return
            
        # Check for position changes
        positions = data.get("positions", [])
        changes = data_manager.detect_position_changes(positions)
        
        # If we have changes, notify subscribed channels
        if changes:
            for channel_id in position_update_channels:
                try:
                    channel = bot.get_channel(int(channel_id))
                    if channel:
                        await send_position_changes(channel, changes)
                except Exception as e:
                    print(f"Error sending update to channel {channel_id}: {e}")
    except Exception as e:
        print(f"Error in position checker: {e}")
        
@position_checker.before_loop
async def before_position_checker():
    """Wait until the bot is ready before starting tasks."""
    await bot.wait_until_ready()

async def send_position_changes(channel, changes):
    """Send position changes to a Discord channel."""
    embed = discord.Embed(
        title=f"{RASTA_FRAMES[0]} POSITION CHANGES DETECTED {RASTA_FRAMES[2]}",
        description="The following position changes were detected on BitGet",
        color=0xFFD700  # Gold color
    )
    
    embed.set_footer(text=f"OMEGA BOT FARM - RASTA MONITOR | {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    # Add fields for new positions
    if changes.get("new", []):
        new_positions_text = "\n".join([
            f"**{p.get('symbol')}**: {p.get('side', '').upper()} {float(p.get('contracts', 0))} contracts" 
            for p in changes["new"]
        ])
        embed.add_field(name="🆕 NEW POSITIONS", value=new_positions_text, inline=False)
    
    # Add fields for closed positions
    if changes.get("closed", []):
        closed_positions_text = "\n".join([
            f"**{p.get('symbol')}**: {p.get('side', '').upper()} {float(p.get('contracts', 0))} contracts" 
            for p in changes["closed"]
        ])
        embed.add_field(name="🚫 CLOSED POSITIONS", value=closed_positions_text, inline=False)
    
    # Add fields for changed positions
    if changes.get("changed", []):
        changed_positions_text = "\n".join([
            f"**{c['position'].get('symbol')}**: {c['position'].get('side', '').upper()} " +
            f"{c['prev_contracts']} → {float(c['position'].get('contracts', 0))} contracts"
            for c in changes["changed"]
        ])
        embed.add_field(name="📊 CHANGED POSITIONS", value=changed_positions_text, inline=False)
    
    await channel.send(embed=embed)

@bot.tree.command(name="positions", description="Show your current BitGet positions")
async def positions_slash(interaction: discord.Interaction):
    """Slash command to show current positions."""
    await interaction.response.defer()
    
    data = data_manager.get_positions()
    
    if "error" in data:
        await interaction.followup.send(f"⚠️ Error: {data['error']}")
        return
    
    positions = data.get("positions", [])
    
    if not positions:
        await interaction.followup.send("🔍 JAH SAYS: NO ACTIVE POSITIONS FOUND")
        return
    
    # Create an embed for positions
    embed = discord.Embed(
        title="RASTA BITGET POSITIONS",
        description=f"Current positions as of {data.get('timestamp')}",
        color=0x00FF00  # Green color
    )
    
    # Add summary field
    total_notional = sum(float(p.get('notional', 0)) for p in positions)
    long_count = sum(1 for p in positions if p.get('side', '').upper() == 'LONG')
    short_count = sum(1 for p in positions if p.get('side', '').upper() == 'SHORT')
    account_balance = data.get("account_balance", 0)
    
    embed.add_field(
        name="💎 Portfolio Summary",
        value=(
            f"Long Positions: {long_count}\n"
            f"Short Positions: {short_count}\n"
            f"Total Value: ${total_notional:.2f}\n"
            f"Account Balance: ${account_balance:.2f}"
        ),
        inline=False
    )
    
    # Add fields for each position (up to 10 to avoid hitting embed limits)
    for position in positions[:10]:
        symbol = position.get('symbol', 'UNKNOWN')
        side = position.get('side', 'UNKNOWN').upper()
        contracts = float(position.get('contracts', 0))
        entry_price = float(position.get('entryPrice', 0))
        mark_price = float(position.get('markPrice', 0))
        unrealized_pnl = float(position.get('unrealizedPnl', 0))
        percentage = float(position.get('percentage', 0))
        leverage = float(position.get('leverage', 0))
        
        # Format field with emojis based on position side and PnL
        emoji = "🟢" if side == "LONG" else "🔴"
        pnl_emoji = "✅" if unrealized_pnl >= 0 else "⚠️"
        
        field_value = (
            f"Side: {side}\n"
            f"Size: {contracts} contracts\n"
            f"Entry: ${entry_price:.2f}\n"
            f"Current: ${mark_price:.2f}\n"
            f"PnL: {pnl_emoji} ${unrealized_pnl:.2f} ({percentage:.2f}%)\n"
            f"Leverage: {leverage}x"
        )
        
        embed.add_field(name=f"{emoji} {symbol}", value=field_value, inline=True)
    
    # Add Rasta wisdom as footer
    wisdom_quotes = [
        "Position sizing aligned with φ creates harmonic trading",
        "When positions resonate with Schumann frequency, profits flow naturally",
        "Babylon system traps fade when Golden Ratio guides your entries",
        "Trust the Fibonacci sequence in every market cycle",
        "Align with natural patterns, not market maker traps",
        "The divine proportion reveals hidden support and resistance",
        "Trade with the rhythm of the Fibonacci spiral",
        "PHI is the divine key to trading success",
        "0.618 retracement offers the perfect entry point",
        "Every position size should honor the Golden Ratio"
    ]
    
    embed.set_footer(text=random.choice(wisdom_quotes))
    
    # Send the embed
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="harmony", description="Analyze the harmony of your positions with Fibonacci principles")
async def harmony_slash(interaction: discord.Interaction):
    """Slash command to analyze position harmony."""
    await interaction.response.defer()
    
    data = data_manager.get_positions()
    
    if "error" in data:
        await interaction.followup.send(f"⚠️ Error: {data['error']}")
        return
    
    positions = data.get("positions", [])
    account_balance = data.get("account_balance", 1000.0)
    
    harmony_analysis = harmony_manager.analyze_positions(positions, account_balance)
    
    if not harmony_analysis:
        await interaction.followup.send("Harmony analysis is disabled or unavailable.")
        return
    
    # Create an embed for harmony analysis
    embed = discord.Embed(
        title="φ POSITION HARMONY ANALYSIS",
        description="Divine mathematical analysis of your BitGet positions",
        color=0xFFD700  # Gold color
    )
    
    # Get key metrics from analysis
    harmony_score = harmony_analysis.get('harmony_score', 0)
    harmony_state = harmony_analysis.get('harmony_state', 'UNKNOWN')
    divine_advice = harmony_analysis.get('divine_advice', '')
    
    # Add harmony score field with progress bar
    score_bar = "█" * int(harmony_score * 10) + "░" * (10 - int(harmony_score * 10))
    embed.add_field(
        name="✨ Harmony Score",
        value=f"{score_bar} {harmony_score:.2f}\nState: **{harmony_state}**",
        inline=False
    )
    
    # Add divine advice field
    embed.add_field(
        name="☯ Divine Advice",
        value=divine_advice,
        inline=False
    )
    
    # Add recommendations if any
    recommendations = harmony_analysis.get('recommendations', [])
    if recommendations:
        rec_text = "\n".join([f"• {rec['description']}" for rec in recommendations[:3]])
        embed.add_field(
            name="🔮 Recommendations",
            value=rec_text,
            inline=False
        )
    
    # Include ideal position sizes
    ideal_sizes = harmony_analysis.get('ideal_position_sizes', [])[:5]  # Get top 5
    if ideal_sizes:
        sizes_text = "\n".join([
            f"• {size['fibonacci_relation']}: ${size['absolute_size']:.2f} ({size['size_pct']*100:.2f}% - {size['risk_category'].upper()})"
            for size in ideal_sizes
        ])
        embed.add_field(
            name="📏 Ideal Fibonacci Position Sizes",
            value=sizes_text,
            inline=False
        )
    
    # Add footer with Fibonacci sequence
    embed.set_footer(text="Fibonacci Sequence: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, ...")
    
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="subscribe", description="Subscribe this channel to position updates")
async def subscribe_slash(interaction: discord.Interaction):
    """Subscribe a channel to position updates."""
    channel_id = str(interaction.channel_id)
    
    if channel_id in position_update_channels:
        await interaction.response.send_message("This channel is already subscribed to position updates.")
        return
    
    position_update_channels.add(channel_id)
    await interaction.response.send_message(f"✅ This channel is now subscribed to BitGet position updates!")

@bot.tree.command(name="unsubscribe", description="Unsubscribe this channel from position updates")
async def unsubscribe_slash(interaction: discord.Interaction):
    """Unsubscribe a channel from position updates."""
    channel_id = str(interaction.channel_id)
    
    if channel_id not in position_update_channels:
        await interaction.response.send_message("This channel is not subscribed to position updates.")
        return
    
    position_update_channels.remove(channel_id)
    await interaction.response.send_message(f"❌ This channel is now unsubscribed from BitGet position updates.")

@bot.tree.command(name="wisdom", description="Receive trading wisdom from the Rasta philosophy")
async def wisdom_slash(interaction: discord.Interaction):
    """Get random Rasta trading wisdom."""
    wisdom_quotes = [
        "Position sizing aligned with φ creates harmonic trading",
        "When positions resonate with Schumann frequency, profits flow naturally",
        "Babylon system traps fade when Golden Ratio guides your entries",
        "Trust the Fibonacci sequence in every market cycle",
        "Align with natural patterns, not market maker traps",
        "The divine proportion reveals hidden support and resistance",
        "Trade with the rhythm of the Fibonacci spiral",
        "PHI is the divine key to trading success",
        "0.618 retracement offers the perfect entry point",
        "Every position size should honor the Golden Ratio",
        "JAH blesses those who respect the divine proportions in their trades",
        "The markets follow cosmic rhythms - observe and align",
        "Let Fibonacci guide your entries, not fear or greed",
        "In the chaos of markets, seek the divine order of PHI",
        "Babylon systems create market manipulation, but natural laws endure",
        "Trading is a spiritual practice when aligned with natural rhythms"
    ]
    
    embed = discord.Embed(
        title="🔮 RASTA TRADING WISDOM",
        description=f"**{random.choice(wisdom_quotes)}**",
        color=0x00FF00  # Green
    )
    
    # Add Rasta colors
    embed.add_field(name=f"{RED}❤️{RESET}", value="Strength", inline=True)
    embed.add_field(name=f"{YELLOW}💛{RESET}", value="Wisdom", inline=True)
    embed.add_field(name=f"{GREEN}💚{RESET}", value="Harmony", inline=True)
    
    await interaction.response.send_message(embed=embed)

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN) 