#!/usr/bin/env python3
"""
Test Command Registration - Verifies that Discord slash commands are properly registered

This script helps debug the CommandNotFound error for 'test_interactions_report' command
by checking command registration and synchronization.
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
logger = logging.getLogger("CommandRegistrationTest")

# Load environment variables
load_dotenv()

# Get Discord credentials
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
GUILD_ID = os.getenv("TEST_GUILD_ID", "")  # You can set this in .env or pass as arg

class CommandRegistrationTester:
    """Tests command registration and synchronization with Discord."""
    
    def __init__(self, token=None, guild_id=None):
        self.token = token or DISCORD_BOT_TOKEN
        self.guild_id = guild_id or GUILD_ID
        self.client = None
    
    async def setup(self):
        """Set up the Discord client with proper intents."""
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
                
                # Run verification
                asyncio.create_task(self.verify_commands())
            
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
    
    async def verify_commands(self):
        """Verify registered commands both locally and on Discord."""
        try:
            import discord
            
            # 1. Check local command tree
            logger.info(f"{CYAN}Checking local command tree...{RESET}")
            local_commands = {cmd.name: cmd for cmd in self.client.tree.get_commands()}
            logger.info(f"{GREEN}Local commands: {list(local_commands.keys())}{RESET}")
            
            # 2. Check if test_interactions_report exists locally
            if "test_interactions_report" in local_commands:
                logger.info(f"{GREEN}✅ 'test_interactions_report' command exists locally{RESET}")
            else:
                logger.error(f"{RED}❌ 'test_interactions_report' command NOT found locally{RESET}")
                logger.info(f"{YELLOW}Creating test_interactions_report command for debugging...{RESET}")
                
                # Create a debugging command
                guild = discord.Object(id=int(self.guild_id)) if self.guild_id else None
                
                @self.client.tree.command(
                    name="test_interactions_report", 
                    description="Debug command for testing registration",
                    guild=guild
                )
@pytest.mark.asyncio
                async def test_interactions_report(interaction: discord.Interaction):
                    await interaction.response.send_message("Debug command registered successfully")
            
            # 3. Check global commands on Discord API
            logger.info(f"{CYAN}Fetching global commands from Discord API...{RESET}")
            global_cmds = await self.client.tree.fetch_commands()
            logger.info(f"{GREEN}Global Discord commands: {[cmd.name for cmd in global_cmds]}{RESET}")
            
            # 4. Check guild-specific commands if guild ID is provided
            if self.guild_id:
                try:
                    logger.info(f"{CYAN}Fetching guild commands for guild ID {self.guild_id}...{RESET}")
                    guild = discord.Object(id=int(self.guild_id))
                    guild_cmds = await self.client.tree.fetch_commands(guild=guild)
                    logger.info(f"{GREEN}Guild commands: {[cmd.name for cmd in guild_cmds]}{RESET}")
                    
                    # Check if test_interactions_report exists in guild commands
                    if any(cmd.name == "test_interactions_report" for cmd in guild_cmds):
                        logger.info(f"{GREEN}✅ 'test_interactions_report' command exists in guild commands{RESET}")
                    else:
                        logger.error(f"{RED}❌ 'test_interactions_report' command NOT found in guild commands{RESET}")
                        logger.info(f"{YELLOW}Attempting to sync commands to guild...{RESET}")
                        
                        # Sync commands to guild
                        await self.client.tree.sync(guild=guild)
                        
                        # Verify sync worked
                        guild_cmds_after = await self.client.tree.fetch_commands(guild=guild)
                        logger.info(f"{GREEN}Guild commands after sync: {[cmd.name for cmd in guild_cmds_after]}{RESET}")
                        
                        if any(cmd.name == "test_interactions_report" for cmd in guild_cmds_after):
                            logger.info(f"{GREEN}✅ 'test_interactions_report' command successfully synced to guild{RESET}")
                        else:
                            logger.error(f"{RED}❌ 'test_interactions_report' command still missing after sync{RESET}")
                except Exception as e:
                    logger.error(f"{RED}Error fetching guild commands: {str(e)}{RESET}")
            
            # 5. Sync commands globally as a backup
            logger.info(f"{YELLOW}Syncing all commands globally...{RESET}")
            await self.client.tree.sync()
            
            logger.info(f"{CYAN}Command verification completed. You can now safely exit with Ctrl+C{RESET}")
            
        except Exception as e:
            logger.error(f"{RED}Error verifying commands: {str(e)}{RESET}")
            import traceback
            logger.error(f"{RED}Traceback: {traceback.format_exc()}{RESET}")
        finally:
            # Keep bot running to allow manually checking commands in Discord
            logger.info(f"{YELLOW}Press Ctrl+C to exit when testing is complete{RESET}")

async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Discord Command Registration Tester")
    parser.add_argument("--token", type=str, help="Discord bot token (overrides .env)")
    parser.add_argument("--guild-id", type=str, help="Discord guild ID for testing")
    args = parser.parse_args()
    
    tester = CommandRegistrationTester(token=args.token, guild_id=args.guild_id)
    
    try:
        logger.info(f"{CYAN}Starting Command Registration Tester...{RESET}")
        await tester.start()
    except KeyboardInterrupt:
        logger.info(f"{YELLOW}Test cancelled by user.{RESET}")
        if tester.client:
            await tester.client.close()
    except Exception as e:
        logger.error(f"{RED}Unexpected error: {str(e)}{RESET}")
        import traceback
        logger.error(f"{RED}Traceback: {traceback.format_exc()}{RESET}")
        if tester.client:
            await tester.client.close()
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        logger.info(f"{YELLOW}Test cancelled by user.{RESET}")
        sys.exit(0)