#!/usr/bin/env python3
"""
Basic Discord Connection Test

This script tests Discord connection with minimal intents to verify if the token is valid.
"""
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
logger = logging.getLogger("DiscordBasicTest")

# Load environment variables
load_dotenv()

# Get Discord credentials
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
CYBER1T4L_APP_ID = os.getenv("CYBER1T4L_APP_ID", "")

async def test_basic_discord_connection():
    """Test Discord connection with minimal intents."""
    logger.info("Starting basic Discord connection test...")
    
    # Check if token exists
    if not DISCORD_BOT_TOKEN:
        logger.error("No Discord bot token found in .env file")
        return False
    
    token_preview = f"{DISCORD_BOT_TOKEN[:4]}...{DISCORD_BOT_TOKEN[-4:]}" if len(DISCORD_BOT_TOKEN) > 8 else DISCORD_BOT_TOKEN
    logger.info(f"Using Discord token: {token_preview}")
    
    try:
        # Import Discord library
        import discord
        
        # Set up minimal intents (no privileged intents)
        intents = discord.Intents.default()
        intents.message_content = False  # This is a privileged intent, disable it
        intents.members = False          # This is a privileged intent, disable it
        intents.presences = False        # This is a privileged intent, disable it
        
        # Create a simple client
        client = discord.Client(intents=intents)
        
        # Define event handlers
        @client.event
        async def on_ready():
            logger.info(f"Connected as {client.user} (ID: {client.user.id})")
            logger.info("The token is valid!")
            logger.info("Bot appears online: Yes")
            
            # Display information about the guilds
            logger.info(f"Connected to {len(client.guilds)} guilds:")
            for guild in client.guilds:
                logger.info(f"  - {guild.name} (ID: {guild.id})")
            
            # Wait a moment then close
            await asyncio.sleep(5)
            await client.close()
        
        # Start the client
        logger.info("Connecting to Discord...")
        await client.start(DISCORD_BOT_TOKEN)
        return True
        
    except discord.LoginFailure as e:
        logger.error(f"Discord login failed: {e}")
        logger.error("This means your token is invalid. Please regenerate it in the Discord Developer Portal.")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    try:
        asyncio.run(test_basic_discord_connection())
    except KeyboardInterrupt:
        logger.info("Test cancelled by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1) 