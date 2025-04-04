#!/usr/bin/env python3
"""
Test Discord Connection for CyBer1t4L QA Bot

This script tests Discord connection independently to diagnose
why the bot appears offline in the Discord UI.
"""

import os
import sys
import logging
import asyncio
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DiscordTest")

# Load environment variables
load_dotenv()

# Get Discord credentials with defaults to avoid None issues
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
CYBER1T4L_APP_ID = os.getenv("CYBER1T4L_APP_ID", "")
CYBER1T4L_PUBLIC_KEY = os.getenv("CYBER1T4L_PUBLIC_KEY", "")

def check_discord_credentials():
    """Check if Discord credentials are set properly."""
    issues = []
    
    if not DISCORD_BOT_TOKEN:
        issues.append("DISCORD_BOT_TOKEN is not set or empty")
    elif DISCORD_BOT_TOKEN == "DISABLED":
        issues.append("DISCORD_BOT_TOKEN is set to 'DISABLED'")
    
    if not CYBER1T4L_APP_ID:
        issues.append("CYBER1T4L_APP_ID is not set or empty")
    elif CYBER1T4L_APP_ID == "DISABLED":
        issues.append("CYBER1T4L_APP_ID is set to 'DISABLED'")
    
    if not CYBER1T4L_PUBLIC_KEY:
        issues.append("CYBER1T4L_PUBLIC_KEY is not set or empty")
    elif CYBER1T4L_PUBLIC_KEY == "DISABLED":
        issues.append("CYBER1T4L_PUBLIC_KEY is set to 'DISABLED'")
    
    return issues

async def test_discord_connection():
    """Test Discord connection and diagnose issues."""
    logger.info("Starting Discord connection test...")
    
    # Check Discord library availability
    try:
        import discord
        from discord.ext import commands
        logger.info("Discord library is installed: discord.py")
    except ImportError:
        logger.error("Discord library is not installed. Run: pip install discord.py")
        return False
    
    # Check credentials
    issues = check_discord_credentials()
    if issues:
        for issue in issues:
            logger.error(f"Credential issue: {issue}")
        return False
    
    token_preview = f"{DISCORD_BOT_TOKEN[:4]}...{DISCORD_BOT_TOKEN[-4:]}" if len(DISCORD_BOT_TOKEN) > 8 else DISCORD_BOT_TOKEN
    logger.info(f"Using Discord token: {token_preview}")
    logger.info(f"Using App ID: {CYBER1T4L_APP_ID}")
    
    # Create Discord bot with detailed logging
    try:
        # Enable Discord library's internal debug logging
        discord_logger = logging.getLogger('discord')
        discord_logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        discord_logger.addHandler(handler)
        
        # Set up intents
        intents = discord.Intents.default()
        intents.message_content = True
        
        # Create bot with command prefix
        bot = commands.Bot(command_prefix='!', intents=intents)
        
        # Define bot events
        @bot.event
        async def on_ready():
            logger.info(f"Bot connected as {bot.user} with ID {bot.user.id}")
            logger.info(f"Bot appears online: {bot.status == discord.Status.online}")
            
            # Set bot status
            await bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching, 
                    name="code quality 🧪"
                ),
                status=discord.Status.online
            )
            logger.info("Set bot status to 'online'")
            
            # Log information about connected guilds
            logger.info(f"Connected to {len(bot.guilds)} guilds:")
            for guild in bot.guilds:
                logger.info(f"  - {guild.name} (ID: {guild.id})")
            
            # Keep bot running for 60 seconds then exit
            logger.info("Bot will disconnect in 60 seconds...")
            await asyncio.sleep(60)
            await bot.close()
        
        # Start the bot
        logger.info("Starting Discord bot...")
        await bot.start(DISCORD_BOT_TOKEN)
        
    except discord.LoginFailure as e:
        logger.error(f"Discord login failed: {e}")
        logger.error("This usually means your token is invalid. Check your .env file.")
        return False
    except Exception as e:
        logger.error(f"Discord error: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False
    
    return True

if __name__ == "__main__":
    issues = check_discord_credentials()
    if issues:
        logger.error("Discord credentials check failed:")
        for issue in issues:
            logger.error(f"  - {issue}")
        sys.exit(1)
    
    try:
        asyncio.run(test_discord_connection())
    except KeyboardInterrupt:
        logger.info("Test cancelled by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1) 