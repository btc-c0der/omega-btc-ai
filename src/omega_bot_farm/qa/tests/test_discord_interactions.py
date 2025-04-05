#!/usr/bin/env python3
"""
Discord Interactions Test Suite for CyBer1t4L Bot

This script provides comprehensive testing for Discord interaction endpoints.
It tests all methods from the Discord.py interactions API that are used by the bot.
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
import json
import logging
import asyncio
import argparse
from datetime import datetime
from typing import Dict, Any, Optional, List
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
logger = logging.getLogger("DiscordInteractionsTest")

# Load environment variables
load_dotenv()

# Get Discord credentials
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")
CYBER1T4L_APP_ID = os.getenv("CYBER1T4L_APP_ID", "")

class DiscordInteractionTester:
    """Tests Discord interaction endpoints using the discord.py library."""
    
    def __init__(self, token: str = None, app_id: str = None):
        self.token = token or DISCORD_BOT_TOKEN
        self.app_id = app_id or CYBER1T4L_APP_ID
        self.client = None
        self.guild_id = None
        self.test_channel_id = None
        self.interaction_responses = {}
        
    async def setup(self):
        """Set up the Discord client with proper intents."""
        try:
            import discord
            from discord.ext import commands
            
            # Set up intents including privileged ones
            intents = discord.Intents.default()
            intents.message_content = True  # Privileged intent for message content
            
            # Create bot with command prefix
            self.client = commands.Bot(command_prefix='!', intents=intents)
            
            # Set up event handlers
            @self.client.event
            async def on_ready():
                logger.info(f"{GREEN}Connected as {self.client.user} (ID: {self.client.user.id}){RESET}")
                
                # Choose first guild/channel for testing
                if len(self.client.guilds) > 0:
                    self.guild_id = self.client.guilds[0].id
                    logger.info(f"Using guild: {self.client.guilds[0].name} (ID: {self.guild_id})")
                    
                    # Find first text channel we can send messages to
                    for channel in self.client.guilds[0].text_channels:
                        if channel.permissions_for(self.client.guilds[0].me).send_messages:
                            self.test_channel_id = channel.id
                            logger.info(f"Using channel: {channel.name} (ID: {self.test_channel_id})")
                            break
                
                # Register command group for the tests
                self.register_test_commands()
                
                # Schedule the test execution
                asyncio.create_task(self.run_tests())
            
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
    
    def register_test_commands(self):
        """Register test commands for the interaction tests."""
        import discord
        from discord import app_commands
        
        # Clear existing commands
        self.client.tree.clear_commands(guild=None)
        
        # Test command group
        test_group = app_commands.Group(name="test_interactions", description="Test interaction endpoints")
        
        # Add commands to the test group
        @test_group.command(name="response_send_message", description="Test sending a direct message response")
        async def response_send_message(interaction: discord.Interaction):
            try:
                logger.info(f"{YELLOW}Testing interaction.response.send_message(){RESET}")
                await interaction.response.send_message("✅ Test response sent successfully!")
                self.interaction_responses["response_send_message"] = "success"
                logger.info(f"{GREEN}interaction.response.send_message() test passed{RESET}")
            except Exception as e:
                logger.error(f"{RED}interaction.response.send_message() test failed: {str(e)}{RESET}")
                self.interaction_responses["response_send_message"] = f"failed: {str(e)}"
        
        @test_group.command(name="response_defer", description="Test deferring a response")
        async def response_defer(interaction: discord.Interaction):
            try:
                logger.info(f"{YELLOW}Testing interaction.response.defer() and followup{RESET}")
                await interaction.response.defer()
                await asyncio.sleep(2)  # Simulate processing time
                await interaction.followup.send("✅ Deferred response followed up successfully!")
                self.interaction_responses["response_defer"] = "success"
                logger.info(f"{GREEN}interaction.response.defer() test passed{RESET}")
            except Exception as e:
                logger.error(f"{RED}interaction.response.defer() test failed: {str(e)}{RESET}")
                self.interaction_responses["response_defer"] = f"failed: {str(e)}"
        
        @test_group.command(name="response_edit", description="Test editing an initial response")
        async def response_edit(interaction: discord.Interaction):
            try:
                logger.info(f"{YELLOW}Testing interaction.response.send_message() then edit_original_response(){RESET}")
                await interaction.response.send_message("Initial response")
                await asyncio.sleep(2)  # Simulate processing time
                await interaction.edit_original_response(content="✅ Edited the initial response successfully!")
                self.interaction_responses["response_edit"] = "success"
                logger.info(f"{GREEN}edit_original_response() test passed{RESET}")
            except Exception as e:
                logger.error(f"{RED}edit_original_response() test failed: {str(e)}{RESET}")
                self.interaction_responses["response_edit"] = f"failed: {str(e)}"
        
        @test_group.command(name="response_is_done", description="Test checking if a response is done")
        async def response_is_done(interaction: discord.Interaction):
            try:
                logger.info(f"{YELLOW}Testing interaction.response.is_done(){RESET}")
                if not interaction.response.is_done():
                    await interaction.response.send_message("✅ Verified response was not yet done")
                    if interaction.response.is_done():
                        await interaction.followup.send("✅ Verified response is now done")
                        self.interaction_responses["response_is_done"] = "success"
                        logger.info(f"{GREEN}interaction.response.is_done() test passed{RESET}")
                    else:
                        await interaction.followup.send("❌ Failed: response should be done but is_done() returned False")
                        self.interaction_responses["response_is_done"] = "failed: incorrect is_done() state after sending"
                else:
                    # This shouldn't happen in a fresh interaction
                    await interaction.followup.send("❌ Failed: response was already done before sending anything")
                    self.interaction_responses["response_is_done"] = "failed: response already done"
                    logger.error(f"{RED}interaction.response.is_done() reported done for a fresh interaction{RESET}")
            except Exception as e:
                logger.error(f"{RED}interaction.response.is_done() test failed: {str(e)}{RESET}")
                self.interaction_responses["response_is_done"] = f"failed: {str(e)}"
        
        @test_group.command(name="error_handling", description="Test error handling during interaction")
        async def error_handling(interaction: discord.Interaction):
            try:
                logger.info(f"{YELLOW}Testing interaction error handling{RESET}")
                # Simulate an error
                if not interaction.response.is_done():
                    try:
                        # Deliberately cause an error
                        logger.info("Simulating an error...")
                        raise ValueError("This is a simulated error")
                    except Exception as e:
                        logger.info(f"{CYAN}Caught error as expected: {str(e)}{RESET}")
                        await interaction.response.send_message(f"✅ Error handled successfully: {type(e).__name__}")
                        self.interaction_responses["error_handling"] = "success"
                        logger.info(f"{GREEN}Error handling test passed{RESET}")
                else:
                    await interaction.followup.send("❌ Failed: response was already done")
                    self.interaction_responses["error_handling"] = "failed: response already done"
            except Exception as e:
                logger.error(f"{RED}Error handling test failed: {str(e)}{RESET}")
                self.interaction_responses["error_handling"] = f"failed: {str(e)}"
        
        @test_group.command(name="original_response", description="Test getting the original response")
        async def original_response(interaction: discord.Interaction):
            try:
                logger.info(f"{YELLOW}Testing interaction.original_response(){RESET}")
                await interaction.response.send_message("Testing original_response()")
                await asyncio.sleep(2)  # Wait for message to be processed
                
                # Get the original response
                original = await interaction.original_response()
                content = original.content
                
                if content == "Testing original_response()":
                    await interaction.followup.send(f"✅ Successfully retrieved original response: '{content}'")
                    self.interaction_responses["original_response"] = "success"
                    logger.info(f"{GREEN}interaction.original_response() test passed{RESET}")
                else:
                    await interaction.followup.send(f"❌ Retrieved incorrect content: '{content}'")
                    self.interaction_responses["original_response"] = f"failed: incorrect content '{content}'"
                    logger.error(f"{RED}interaction.original_response() returned wrong content{RESET}")
            except Exception as e:
                logger.error(f"{RED}interaction.original_response() test failed: {str(e)}{RESET}")
                self.interaction_responses["original_response"] = f"failed: {str(e)}"
        
        # Add the test group to the command tree
        self.client.tree.add_command(test_group)
        logger.info(f"{GREEN}Test commands registered{RESET}")
    
    async def run_tests(self):
        """Run the interaction tests."""
        if not self.guild_id or not self.test_channel_id:
            logger.error(f"{RED}No guild or channel available for testing{RESET}")
            await self.client.close()
            return
        
        logger.info(f"{YELLOW}Syncing commands to guild...{RESET}")
        try:
            import discord
            # Sync commands to the first guild
            guild = discord.Object(id=self.guild_id)
            await self.client.tree.sync(guild=guild)
            logger.info(f"{GREEN}Commands synced successfully{RESET}")
            
            logger.info(f"{CYAN}All interaction test commands have been registered.{RESET}")
            logger.info(f"{CYAN}To test interactions, use the /test_interactions commands in Discord.{RESET}")
            logger.info(f"{CYAN}After testing, use the /test_interactions_report command to view results.{RESET}")
            
            # Add the report command
            @self.client.tree.command(
                name="test_interactions_report", 
                description="Show the results of interaction tests",
                guild=guild
            )
            @pytest.mark.asyncio
            async def test_interactions_report(interaction: discord.Interaction):
                if not self.interaction_responses:
                    await interaction.response.send_message("No tests have been run yet.")
                    return
                
                report = "# Discord Interactions Test Report\n\n"
                for test_name, result in self.interaction_responses.items():
                    status = "✅" if result == "success" else "❌"
                    report += f"{status} **{test_name}**: {result}\n"
                
                await interaction.response.send_message(report)
            
            await self.client.tree.sync(guild=guild)
            
        except Exception as e:
            logger.error(f"{RED}Error syncing commands: {str(e)}{RESET}")
            await self.client.close()
    
    def generate_report(self):
        """Generate a report from the interaction responses."""
        if not self.interaction_responses:
            return "No tests have been run yet."
        
        success_count = sum(1 for result in self.interaction_responses.values() if result == "success")
        total_count = len(self.interaction_responses)
        
        report = [
            f"Discord Interactions Test Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Success Rate: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)\n"
        ]
        
        for test_name, result in self.interaction_responses.items():
            status = "✅ PASS" if result == "success" else "❌ FAIL"
            report.append(f"{status}: {test_name} - {result}")
        
        return "\n".join(report)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Discord Interactions Test Suite")
    
    parser.add_argument("--token", type=str, help="Discord bot token (overrides .env)")
    parser.add_argument("--app-id", type=str, help="Discord application ID (overrides .env)")
    
    return parser.parse_args()

async def main():
    """Main entry point."""
    args = parse_args()
    
    # Create and start the tester
    tester = DiscordInteractionTester(token=args.token, app_id=args.app_id)
    
    try:
        logger.info(f"{CYAN}Starting Discord Interaction Tester...{RESET}")
        logger.info(f"{YELLOW}Press Ctrl+C to exit{RESET}")
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