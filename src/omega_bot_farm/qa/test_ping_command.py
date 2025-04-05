#!/usr/bin/env python3
"""
Discord Bot Ping Test

This script simulates a Discord UI ping to the CyBer1t4L bot to test its availability
and responsiveness. It creates a sample direct message and checks for a response.
"""

import os
import sys
import logging
import asyncio
import argparse
from dotenv import load_dotenv

# Try to import Discord library
try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("PingTester")

# Load environment variables
load_dotenv()

# Get Discord credentials
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
DISCORD_APP_ID = os.getenv("DISCORD_APP_ID", os.getenv("CYBER1T4L_APP_ID", ""))

async def simulate_ping_command():
    """Simulate a Discord ping command by creating a test client and sending a direct message."""
    logger.info("Starting bot ping test...")
    
    # Check if Discord is available
    if not DISCORD_AVAILABLE:
        logger.error("Discord library not installed. Please install it with:")
        logger.error("  pip install discord.py")
        return False
    
    # Check if token exists
    if not DISCORD_BOT_TOKEN:
        logger.error("No Discord bot token found in .env file")
        return False
    
    token_preview = f"{DISCORD_BOT_TOKEN[:4]}...{DISCORD_BOT_TOKEN[-4:]}" if len(DISCORD_BOT_TOKEN) > 8 else "Invalid token"
    logger.info(f"Using Discord token: {token_preview}")
    logger.info(f"Using App ID: {DISCORD_APP_ID}")
    
    try:
        # Set up intents
        intents = discord.Intents.default()
        intents.message_content = True
        
        # Create a test client
        client = discord.Client(intents=intents)
        
        # Flag to track bot response
        bot_responded = False
        target_bot_id = DISCORD_APP_ID
        
        # Message history to check
        messages_received = []
        
        @client.event
        async def on_ready():
            logger.info(f"Test client connected as {client.user}")
            logger.info("Looking for our target bot...")
            
            # Find the bot user from our application ID
            bot_user = None
            for user in client.users:
                logger.info(f"Found user: {user.name} (ID: {user.id})")
                if str(user.id) == target_bot_id:
                    bot_user = user
                    logger.info(f"Found our target bot: {bot_user.name}!")
                    break
            
            # List the guilds where both our test client and the bot are members
            common_guilds = []
            for guild in client.guilds:
                logger.info(f"Checking guild: {guild.name}")
                bot_member = guild.get_member(int(target_bot_id)) if target_bot_id.isdigit() else None
                
                if bot_member:
                    logger.info(f"✅ Bot found in guild: {guild.name}")
                    common_guilds.append(guild)
                    
                    # Find a suitable text channel to send a message to
                    for channel in guild.text_channels:
                        permissions = channel.permissions_for(guild.me)
                        bot_permissions = channel.permissions_for(bot_member)
                        
                        if permissions.send_messages and bot_permissions.read_messages:
                            logger.info(f"Sending ping message in channel: {channel.name}")
                            try:
                                await channel.send("/ping")
                                logger.info("Test message sent (note: slash commands can't be triggered this way)")
                                await channel.send("🔍 Testing bot ping - please ignore")
                            except Exception as e:
                                logger.error(f"Could not send message: {e}")
            
            if not common_guilds:
                logger.warning("❌ No common guilds found with the bot")
                logger.warning("Make sure both the test client and the bot are in the same server")
            
            # Wait a bit for potential responses
            logger.info("Waiting 10 seconds for bot responses...")
            await asyncio.sleep(10)
            
            # Summarize results
            if messages_received:
                logger.info(f"Received {len(messages_received)} messages during the test:")
                for msg in messages_received:
                    logger.info(f"- From {msg.author}: {msg.content}")
                if bot_responded:
                    logger.info("✅ The bot responded to our messages!")
                else:
                    logger.info("❌ The bot did not respond directly to our messages")
            else:
                logger.info("No messages were received during the test")
            
            # Disconnect the client
            await client.close()
        
        @client.event
        async def on_message(message):
            nonlocal bot_responded
            
            # Skip our own messages
            if message.author == client.user:
                return
            
            # Add to received messages
            messages_received.append(message)
            logger.info(f"Message received from {message.author}: {message.content}")
            
            # Check if the message is from our target bot
            if str(message.author.id) == target_bot_id:
                logger.info("✅ Received response from the target bot!")
                bot_responded = True
            
            # Check if mentions our test client
            if client.user in message.mentions:
                logger.info("✅ The message mentions our test client")
        
        # Start the test client
        logger.info("Starting test client...")
        await client.start(DISCORD_BOT_TOKEN)
        
        # Report success based on whether the bot responded
        return bot_responded
        
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

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Test Discord bot ping command")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    
    try:
        asyncio.run(simulate_ping_command())
    except KeyboardInterrupt:
        logger.info("Test cancelled by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1) 