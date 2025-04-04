#!/usr/bin/env python3
"""
Discord Bot Token Fixer for CyBer1t4L QA Bot

This script validates the Discord bot token and provides instructions
for regenerating the token if it's invalid.
"""

import os
import sys
import logging
import asyncio
import argparse
from dotenv import load_dotenv

# Try to import discord, but don't fail if it's not installed
try:
    import discord
    from discord.ext import commands
    HAVE_DISCORD = True
except ImportError:
    HAVE_DISCORD = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DiscordFixer")

# ANSI color codes for terminal output
class Colors:
    RESET = "\033[0m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    RED = "\033[31m"
    BOLD = "\033[1m"

async def test_discord_token(token):
    """Test if the Discord token is valid by attempting to login."""
    logger.info(f"{Colors.BLUE}Testing Discord token...{Colors.RESET}")
    
    # Return early if Discord is not installed
    if not HAVE_DISCORD:
        logger.error(f"{Colors.RED}Discord.py not installed. Run: pip install discord.py{Colors.RESET}")
        return False
    
    # At this point, discord is definitely imported
    try:
        # Create a discord client
        client = discord.Client(intents=discord.Intents.default())
        
        # Flag to track successful login
        login_successful = False
        
        @client.event
        async def on_ready():
            nonlocal login_successful
            login_successful = True
            logger.info(f"{Colors.GREEN}Successfully logged in as {client.user}{Colors.RESET}")
            await client.close()
        
        # Try to login with a timeout
        try:
            await asyncio.wait_for(client.start(token), timeout=10)
        except asyncio.TimeoutError:
            # If login is taking too long but no error, consider it successful
            if not login_successful:
                logger.warning(f"{Colors.YELLOW}Login is taking longer than expected, but no error yet.{Colors.RESET}")
                await client.close()
        
        return login_successful
    except Exception as e:
        if isinstance(e, discord.LoginFailure):
            logger.error(f"{Colors.RED}Discord login failed: {e}{Colors.RESET}")
        else:
            logger.error(f"{Colors.RED}Unexpected error: {e}{Colors.RESET}")
        return False

def update_token_in_env(new_token):
    """Update the Discord bot token in the .env file."""
    logger.info(f"{Colors.BLUE}Updating token in .env file...{Colors.RESET}")
    
    env_path = os.path.join(os.getcwd(), '.env')
    if not os.path.exists(env_path):
        logger.error(f"{Colors.RED}.env file not found at {env_path}{Colors.RESET}")
        return False
    
    # Read current .env file
    with open(env_path, 'r') as file:
        lines = file.readlines()
    
    # Update the token line
    token_updated = False
    for i, line in enumerate(lines):
        if line.startswith('DISCORD_BOT_TOKEN='):
            lines[i] = f'DISCORD_BOT_TOKEN={new_token}\n'
            token_updated = True
            break
    
    # If token line not found, add it
    if not token_updated:
        lines.append(f'DISCORD_BOT_TOKEN={new_token}\n')
    
    # Write updated .env file
    with open(env_path, 'w') as file:
        file.writelines(lines)
    
    logger.info(f"{Colors.GREEN}Token updated successfully in .env file{Colors.RESET}")
    return True

def show_token_regeneration_instructions():
    """Show instructions for regenerating the Discord bot token."""
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}=== DISCORD BOT TOKEN REGENERATION INSTRUCTIONS ==={Colors.RESET}\n")
    print(f"{Colors.CYAN}Your Discord bot token is invalid or expired. Follow these steps to generate a new one:{Colors.RESET}\n")
    print(f"{Colors.BOLD}1. Go to the Discord Developer Portal:{Colors.RESET} https://discord.com/developers/applications")
    print(f"{Colors.BOLD}2. Select your CyBer1t4L QA Bot application{Colors.RESET}")
    print(f"{Colors.BOLD}3. In the left sidebar, click on 'Bot'{Colors.RESET}")
    print(f"{Colors.BOLD}4. Under the 'TOKEN' section, click 'Reset Token'{Colors.RESET}")
    print(f"{Colors.BOLD}5. Confirm the action and copy the new token{Colors.RESET}")
    print(f"{Colors.BOLD}6. Run this script again with:{Colors.RESET} python -m src.omega_bot_farm.qa.fix_discord_bot --update-token YOUR_NEW_TOKEN\n")
    print(f"{Colors.YELLOW}Note: Make sure the bot has the necessary permissions and is added to your server.{Colors.RESET}")
    print(f"{Colors.YELLOW}Required Bot Permissions: Send Messages, Read Message History, Use Slash Commands{Colors.RESET}\n")

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Fix Discord bot token issues")
    parser.add_argument("--update-token", help="Update with a new Discord bot token")
    parser.add_argument("--test-only", action="store_true", help="Only test the current token without updating")
    return parser.parse_args()

async def main():
    """Main function."""
    args = parse_args()
    
    # Load environment variables
    load_dotenv()
    current_token = os.getenv("DISCORD_BOT_TOKEN", "")
    
    # If updating with new token
    if args.update_token:
        if await test_discord_token(args.update_token):
            update_token_in_env(args.update_token)
            logger.info(f"{Colors.GREEN}Discord bot token validated and updated successfully!{Colors.RESET}")
        else:
            logger.error(f"{Colors.RED}The provided token is invalid. Please check and try again.{Colors.RESET}")
        return
    
    # Test current token
    if current_token:
        token_preview = f"{current_token[:4]}...{current_token[-4:]}" if len(current_token) > 8 else "[EMPTY]"
        logger.info(f"{Colors.BLUE}Current token in .env: {token_preview}{Colors.RESET}")
        
        if await test_discord_token(current_token):
            logger.info(f"{Colors.GREEN}Current Discord bot token is valid!{Colors.RESET}")
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Your Discord bot token is valid and working!{Colors.RESET}")
            print(f"{Colors.GREEN}You should now be able to see your bot online in Discord.{Colors.RESET}\n")
        else:
            logger.error(f"{Colors.RED}Current Discord bot token is invalid!{Colors.RESET}")
            show_token_regeneration_instructions()
    else:
        logger.error(f"{Colors.RED}No Discord bot token found in .env file!{Colors.RESET}")
        show_token_regeneration_instructions()

if __name__ == "__main__":
    asyncio.run(main()) 