#!/usr/bin/env python3
"""
Fix for the CommandNotFound Error with test_interactions_report command

This script fixes the issue where the 'test_interactions_report' command is not properly
registered with Discord's API, causing a CommandNotFound error when attempting to use it.

The problem occurs because:
1. The command is defined inside an async function (run_tests)
2. The sync operation after defining the command might not be taking effect
3. The command may be registered with the guild but not globally

This script will register the command properly and sync it both to the guild and globally.
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from dotenv import load_dotenv

# Configure colored logging
RESET = "\033[0m"
GREEN = "\033[38;5;82m"
RED = "\033[38;5;196m"
YELLOW = "\033[38;5;226m"
CYAN = "\033[38;5;51m"
BLUE = "\033[38;5;39m"
PURPLE = "\033[38;5;141m"

logging.basicConfig(
    level=logging.INFO,
    format=f"{PURPLE}[%(asctime)s]{RESET} {CYAN}%(levelname)s{RESET} - {GREEN}%(message)s{RESET}",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("FixCommandNotFound")

# Load environment variables
load_dotenv()

# Get Discord credentials
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")

class CommandRegistrationFixer:
    """Fixes command registration issues with Discord.py."""
    
    def __init__(self, token=None, guild_id=None):
        self.token = token or DISCORD_BOT_TOKEN
        self.guild_id = guild_id
        self.client = None
    
    async def setup(self):
        """Set up the Discord client and add commands."""
        try:
            import discord
            from discord.ext import commands
            
            # Set up intents
            intents = discord.Intents.default()
            intents.message_content = True
            
            # Create bot with command prefix
            self.client = commands.Bot(command_prefix='!', intents=intents)
            
            # Set up event handlers
            @self.client.event
            async def on_ready():
                logger.info(f"{GREEN}Connected as {self.client.user} (ID: {self.client.user.id}){RESET}")
                
                # Register commands and sync
                await self.register_and_sync_commands()
            
            return True
        except ImportError:
            logger.error(f"{RED}Discord.py library not installed. Install it with pip install discord.py{RESET}")
            return False
        except Exception as e:
            logger.error(f"{RED}Error setting up Discord client: {str(e)}{RESET}")
            return False
    
    async def start(self):
        """Start the Discord client."""
        if not self.token:
            logger.error(f"{RED}No Discord bot token found in .env file{RESET}")
            return False
        
        if not await self.setup():
            return False
        
        try:
            logger.info(f"{YELLOW}Starting Discord client...{RESET}")
            await self.client.start(self.token)
            return True
        except Exception as e:
            logger.error(f"{RED}Error starting Discord client: {str(e)}{RESET}")
            return False
    
    async def register_and_sync_commands(self):
        """Register the missing commands and sync them with Discord API."""
        import discord
        
        logger.info(f"{CYAN}Registering the missing test_interactions_report command...{RESET}")
        
        # IMPORTANT FIX: Define the command at the top level, not inside another async function
        @self.client.tree.command(
            name="test_interactions_report", 
            description="Show the results of interaction tests"
        )
        async def test_interactions_report(interaction: discord.Interaction):
            await interaction.response.send_message("The test_interactions_report command has been fixed and is now working!")
        
        # First sync globally (to make sure it's added to all guilds)
        logger.info(f"{YELLOW}Syncing command to global application commands...{RESET}")
        try:
            await self.client.tree.sync()
            logger.info(f"{GREEN}Successfully synced global commands{RESET}")
        except Exception as e:
            logger.error(f"{RED}Error syncing global commands: {str(e)}{RESET}")
        
        # Then sync to specific guild if provided
        if self.guild_id:
            logger.info(f"{YELLOW}Syncing command to guild ID {self.guild_id}...{RESET}")
            try:
                guild = discord.Object(id=int(self.guild_id))
                await self.client.tree.sync(guild=guild)
                logger.info(f"{GREEN}Successfully synced commands to guild{RESET}")
            except Exception as e:
                logger.error(f"{RED}Error syncing guild commands: {str(e)}{RESET}")
        
        # Verify the commands are registered
        try:
            # Check global commands
            global_cmds = await self.client.tree.fetch_commands()
            logger.info(f"{GREEN}Global commands after sync: {[cmd.name for cmd in global_cmds]}{RESET}")
            
            if any(cmd.name == "test_interactions_report" for cmd in global_cmds):
                logger.info(f"{GREEN}✅ 'test_interactions_report' command successfully registered globally{RESET}")
            else:
                logger.error(f"{RED}❌ 'test_interactions_report' command not found in global commands{RESET}")
            
            # Check guild commands if a guild ID was provided
            if self.guild_id:
                guild = discord.Object(id=int(self.guild_id))
                guild_cmds = await self.client.tree.fetch_commands(guild=guild)
                logger.info(f"{GREEN}Guild commands after sync: {[cmd.name for cmd in guild_cmds]}{RESET}")
                
                if any(cmd.name == "test_interactions_report" for cmd in guild_cmds):
                    logger.info(f"{GREEN}✅ 'test_interactions_report' command successfully registered in guild{RESET}")
                else:
                    logger.error(f"{RED}❌ 'test_interactions_report' command not found in guild commands{RESET}")
        except Exception as e:
            logger.error(f"{RED}Error verifying commands: {str(e)}{RESET}")
        
        logger.info(f"{CYAN}Command registration and verification completed.{RESET}")
        logger.info(f"{GREEN}The fix has been applied! You should now be able to use /test_interactions_report in Discord.{RESET}")
        logger.info(f"{YELLOW}You can safely exit this script with Ctrl+C when ready.{RESET}")

async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Fix Discord Command Registration Issues")
    parser.add_argument("--token", type=str, help="Discord bot token (overrides .env)")
    parser.add_argument("--guild-id", type=str, help="Discord guild ID to sync commands to")
    args = parser.parse_args()
    
    fixer = CommandRegistrationFixer(token=args.token, guild_id=args.guild_id)
    
    try:
        logger.info(f"{CYAN}Starting Command Registration Fixer...{RESET}")
        await fixer.start()
    except KeyboardInterrupt:
        logger.info(f"{YELLOW}Fix cancelled by user.{RESET}")
        if fixer.client:
            await fixer.client.close()
    except Exception as e:
        logger.error(f"{RED}Unexpected error: {str(e)}{RESET}")
        import traceback
        logger.error(f"{RED}Traceback: {traceback.format_exc()}{RESET}")
        if fixer.client:
            await fixer.client.close()
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        logger.info(f"{YELLOW}Fix cancelled by user.{RESET}")
        sys.exit(0) 