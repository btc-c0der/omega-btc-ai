#!/usr/bin/env python3
"""
Discord Privileged Intents Test

This script tests Discord connection with privileged intents to verify if they're properly configured.
Specifically targets the "Privileged message content intent is missing" warning.
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
import pytest
import sys
import logging
import asyncio
import argparse
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DiscordIntentsTest")

# Load environment variables
load_dotenv()

# Get Discord credentials
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
DISCORD_APP_ID = os.getenv("DISCORD_APP_ID", os.getenv("CYBER1T4L_APP_ID", ""))

class IntentTester:
    """Class to test various Discord intents configurations."""
    
    def __init__(self, token, app_id=None):
        self.token = token
        self.app_id = app_id
        
@pytest.mark.asyncio
    async def test_with_message_content_intent(self):
        """Test connection with message_content intent enabled."""
        logger.info("=== TESTING WITH MESSAGE_CONTENT INTENT ENABLED ===")
        result = await self._run_test(enable_message_content=True)
        return result
        
@pytest.mark.asyncio
    async def test_without_message_content_intent(self):
        """Test connection with message_content intent disabled."""
        logger.info("=== TESTING WITH MESSAGE_CONTENT INTENT DISABLED ===")
        result = await self._run_test(enable_message_content=False)
        return result
        
@pytest.mark.asyncio
    async def test_all_privileged_intents(self):
        """Test connection with all privileged intents enabled."""
        logger.info("=== TESTING WITH ALL PRIVILEGED INTENTS ENABLED ===")
        result = await self._run_test(
            enable_message_content=True,
            enable_members=True,
            enable_presences=True
        )
        return result
        
    async def _run_test(self, enable_message_content=False, enable_members=False, enable_presences=False):
        """Run a Discord connection test with specified intents."""
        import discord
        
        # Format token for display
        token_preview = f"{self.token[:4]}...{self.token[-4:]}" if len(self.token) > 8 else "Invalid token"
        
        try:
            # Set up intents
            intents = discord.Intents.default()
            intents.message_content = enable_message_content
            intents.members = enable_members
            intents.presences = enable_presences
            
            # Log intent configuration
            logger.info(f"Testing with token: {token_preview}")
            logger.info(f"Intent configuration:")
            logger.info(f"  - message_content: {intents.message_content}")
            logger.info(f"  - members: {intents.members}")
            logger.info(f"  - presences: {intents.presences}")
            
            # Create Discord bot client
            bot = discord.Client(intents=intents)
            
            # Connection status flag
            connected = False
            warning_received = False
            
            # Define event handlers
            @bot.event
            async def on_ready():
                nonlocal connected
                connected = True
                logger.info(f"Connected as {bot.user} (ID: {bot.user.id})")
                
                # Display information about the guilds
                logger.info(f"Connected to {len(bot.guilds)} guilds:")
                for guild in bot.guilds:
                    logger.info(f"  - {guild.name} (ID: {guild.id})")
                
                # Wait a moment then close
                await asyncio.sleep(3)
                await bot.close()
            
            # Create custom handler to catch library warnings
            discord_logger = logging.getLogger('discord')
            original_warning = discord_logger.warning
            
            def custom_warning(msg, *args, **kwargs):
                nonlocal warning_received
                if "Privileged message content intent" in msg:
                    warning_received = True
                    logger.warning("🚨 DETECTED: 'Privileged message content intent is missing' warning")
                original_warning(msg, *args, **kwargs)
            
            # Temporarily replace the warning function
            discord_logger.warning = custom_warning
            
            # Start the bot
            logger.info("Connecting to Discord...")
            try:
                await bot.start(self.token)
            finally:
                # Restore original warning function
                discord_logger.warning = original_warning
            
            # Evaluate results
            if connected:
                logger.info("✅ Successfully connected to Discord")
                if enable_message_content and warning_received:
                    logger.warning("❌ Privileged message_content intent is ENABLED in code but NOT ENABLED in Discord Developer Portal")
                    return {
                        "connected": True,
                        "intent_properly_configured": False,
                        "warning": "message_content intent not enabled in Discord Developer Portal"
                    }
                elif enable_message_content and not warning_received:
                    logger.info("✅ message_content intent is properly configured")
                    return {
                        "connected": True,
                        "intent_properly_configured": True
                    }
                elif not enable_message_content and warning_received:
                    logger.info("✅ Expected warning received (normal behavior when message_content is disabled)")
                    return {
                        "connected": True,
                        "intent_properly_configured": None,  # Not applicable
                        "note": "This is expected behavior when message_content intent is disabled in code"
                    }
                else:
                    return {
                        "connected": True,
                        "intent_properly_configured": None
                    }
            else:
                logger.error("❌ Failed to connect to Discord")
                return {
                    "connected": False,
                    "error": "Failed to connect"
                }
                
        except discord.LoginFailure as e:
            logger.error(f"Discord login failed: {e}")
            logger.error("This means your token is invalid. Please regenerate it in the Discord Developer Portal.")
            return {
                "connected": False,
                "error": f"Login failure: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return {
                "connected": False,
                "error": f"Unexpected error: {str(e)}"
            }

def print_instructions():
    """Print instructions for fixing the privileged intents issue."""
    print("\n" + "="*80)
    print(" INSTRUCTIONS FOR FIXING DISCORD INTENTS ISSUES ".center(80, "="))
    print("="*80)
    print("\n1. Go to the Discord Developer Portal: https://discord.com/developers/applications")
    print("2. Select your application")
    print("3. Navigate to the 'Bot' tab")
    print("4. Scroll down to 'Privileged Gateway Intents' section")
    print("5. Enable 'MESSAGE CONTENT INTENT'")
    print("6. Click 'Save Changes'")
    print("7. Restart your bot\n")
    print("Note: You need to have these intents enabled BOTH in your code AND in the Discord Developer Portal")
    print("="*80 + "\n")

def print_code_example():
    """Print a code example showing how to properly enable intents."""
    print("\n" + "="*80)
    print(" CODE EXAMPLE FOR PROPERLY ENABLING INTENTS ".center(80, "="))
    print("="*80)
    print("""
# Import Discord libraries
import discord
from discord.ext import commands

# Set up intents (required for newer Discord.py versions)
intents = discord.Intents.default()
intents.message_content = True  # Enable privileged intent for reading message content

# Create bot with command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)
    """)
    print("="*80 + "\n")

async def run_tests():
    """Run all intent tests and provide a comprehensive report."""
    # Check if token exists
    if not DISCORD_BOT_TOKEN:
        logger.error("No Discord bot token found in .env file")
        return False
    
    # Check if Discord library is available
    try:
        import discord
        from discord.ext import commands
    except ImportError:
        logger.error("Discord library not installed. Please install it with:")
        logger.error("  pip install discord.py")
        return False
    
    # Create tester
    tester = IntentTester(DISCORD_BOT_TOKEN, DISCORD_APP_ID)
    
    # Run tests
    with_intent_result = await tester.test_with_message_content_intent()
    without_intent_result = await tester.test_without_message_content_intent()
    
    # Analyze results
    needs_portal_config = (with_intent_result.get("connected", False) and 
                          not with_intent_result.get("intent_properly_configured", False))
    
    # Print summary
    print("\n" + "="*80)
    print(" DISCORD INTENTS TEST RESULTS ".center(80, "="))
    print("="*80)
    
    print("\nTest with message_content intent enabled:")
    if with_intent_result.get("connected", False):
        if with_intent_result.get("intent_properly_configured", False):
            print("  ✅ Connected successfully with message_content intent")
            print("  ✅ No privileged intent warnings (correctly configured in Discord Portal)")
        else:
            print("  ✅ Connected successfully with message_content intent")
            print("  ❌ Received privileged intent warning - NOT configured in Discord Portal")
    else:
        print(f"  ❌ Failed to connect: {with_intent_result.get('error', 'Unknown error')}")
    
    print("\nTest with message_content intent disabled:")
    if without_intent_result.get("connected", False):
        print("  ✅ Connected successfully without message_content intent")
        print("  ℹ️ Expected warning about missing privileged intent (normal)")
    else:
        print(f"  ❌ Failed to connect: {without_intent_result.get('error', 'Unknown error')}")
    
    print("\nConclusion:")
    if needs_portal_config:
        print("  ❌ message_content intent is ENABLED in your code but NOT in the Discord Developer Portal")
        print("     You need to enable it in the Discord Developer Portal")
        print_instructions()
    elif with_intent_result.get("intent_properly_configured", False):
        print("  ✅ message_content intent is properly configured both in code and Discord Developer Portal")
    elif not with_intent_result.get("connected", False):
        print("  ❌ Connection issues prevented complete testing")
    else:
        print("  ⚠️ Test results inconclusive")
    
    print("\nRecommendations:")
    if needs_portal_config:
        print("  1. Enable message_content intent in Discord Developer Portal")
        print("  2. Restart your bot")
    else:
        print("  - Ensure your code correctly enables the intents you need")
        print_code_example()
    
    return True

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Test Discord privileged intents configuration")
    parser.add_argument("--instructions", action="store_true", help="Show instructions for fixing intent issues")
    parser.add_argument("--code-example", action="store_true", help="Show code example for properly enabling intents")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    
    if args.instructions:
        print_instructions()
        sys.exit(0)
    
    if args.code_example:
        print_code_example()
        sys.exit(0)
    
    try:
        asyncio.run(run_tests())
    except KeyboardInterrupt:
        logger.info("Test cancelled by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)