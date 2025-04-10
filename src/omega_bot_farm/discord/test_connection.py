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
Discord Bot Connection Test

Simple script to test if the Discord bot can connect with the provided token.
"""

import os
import sys
import logging
import asyncio
import discord
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("discord_test")

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    logger.info("Environment variables loaded from .env file")
except ImportError:
    logger.warning("python-dotenv not installed. Will only use OS environment variables.")

class TestBot(discord.Client):
    """Simple bot to test Discord connection."""
    
    def __init__(self):
        """Initialize the test bot."""
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        
    async def on_ready(self):
        """Event handler when the bot connects to Discord."""
        logger.info(f"Bot connected! Logged in as {self.user} (ID: {self.user.id})")
        logger.info(f"Bot is in {len(self.guilds)} guilds:")
        
        for guild in self.guilds:
            logger.info(f"- {guild.name} (ID: {guild.id})")
        
        logger.info("Connection test successful!")
        
        # Wait a moment then exit
        await asyncio.sleep(5)
        await self.close()

async def main():
    """Main test function."""
    # Get the token
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        logger.error("DISCORD_TOKEN not set in environment variables!")
        print_token_instructions()
        return False
    
    # If token is wrapped in quotes, remove them
    token = token.strip("'\"")
    
    # Check if token looks like an App ID (mostly numbers)
    if token.isdigit() or (token.isalnum() and len(token) < 30):
        logger.error(f"The provided token appears to be an App ID ({token}) rather than a bot token")
        print_token_instructions()
        return False
    
    logger.info(f"Token found: {token[:10]}...{token[-5:]}")
    
    # Create and run the bot
    bot = TestBot()
    try:
        logger.info("Attempting to connect to Discord...")
        await bot.start(token)
    except discord.errors.LoginFailure as e:
        logger.error(f"Failed to login: {e}")
        print_token_instructions()
        return False
    except Exception as e:
        logger.error(f"Error connecting to Discord: {e}")
        return False
    
    return True

def print_token_instructions():
    """Print instructions for obtaining a valid bot token."""
    print("\n" + "=" * 80)
    print("BOT TOKEN INSTRUCTIONS")
    print("=" * 80)
    print("\nYou need to obtain a valid Discord bot token. Follow these steps:")
    print("\n1. Go to https://discord.com/developers/applications")
    print("2. Select your application (0m3g4_B1Tg3T_b0t, App ID: 1358189845931098130)")
    print("3. Click on the 'Bot' tab in the left sidebar")
    print("4. Under the 'TOKEN' section, click 'Reset Token' if you can't see the token")
    print("5. Copy the new token (looks like: NzkyNzE1NDU0MTk2MDg4ODQy.X-hvzA.Jk2P1PbhCeeY9958qkgWUz78rtQ)")
    print("6. Update your .env file with:")
    print("   DISCORD_TOKEN=your_token_here  (without quotes)\n")
    print("Note: Bot tokens are sensitive! Never share them publicly.")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    # Run the test
    success = asyncio.run(main())
    
    # Exit with appropriate code
    sys.exit(0 if success else 1) 