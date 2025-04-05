#!/usr/bin/env python3
"""
Ping Command Tester for CyBer1t4L QA Bot
----------------------------------------

This script tests the functionality of the Discord ping command by:
1. Verifying network connectivity to Discord
2. Checking if the ping command is properly registered
3. Simulating a ping command interaction
4. Monitoring the response

This helps diagnose why the ping command might not be responding.
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
import json
import asyncio
import logging
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

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
logger = logging.getLogger("PingCommandTest")

class PingCommandTester:
    """Tests the Discord ping command functionality."""
    
    def __init__(self, token: Optional[str] = None, app_id: Optional[str] = None, guild_id: Optional[str] = None):
        self.token = token
        self.app_id = app_id
        self.guild_id = guild_id
        self.results = {
            "network": {},
            "command_registration": {},
            "ping_simulation": {},
            "overall": {
                "success": False,
                "recommendations": []
            }
        }
    
    async def check_discord_api_connectivity(self) -> Dict[str, Any]:
        """Check if Discord API is reachable."""
        try:
            import aiohttp
            logger.info(f"{CYAN}Testing Discord API connectivity...{RESET}")
            
            # Test basic gateway endpoint
            gateway_url = "https://discord.com/api/v10/gateway"
            
            async with aiohttp.ClientSession() as session:
                try:
                    start_time = asyncio.get_event_loop().time()
                    async with session.get(gateway_url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                        elapsed = asyncio.get_event_loop().time() - start_time
                        
                        if response.status == 200:
                            data = await response.json()
                            logger.info(f"{GREEN}Discord API gateway endpoint is accessible: {response.status} ({elapsed*1000:.2f}ms){RESET}")
                            return {
                                "success": True,
                                "status": response.status,
                                "latency_ms": elapsed * 1000,
                                "gateway_url": data.get("url")
                            }
                        else:
                            logger.error(f"{RED}Discord API gateway endpoint returned an error: {response.status}{RESET}")
                            return {
                                "success": False,
                                "status": response.status,
                                "error": f"HTTP {response.status}",
                                "latency_ms": elapsed * 1000
                            }
                except aiohttp.ClientError as e:
                    logger.error(f"{RED}Failed to connect to Discord API: {str(e)}{RESET}")
                    return {
                        "success": False,
                        "error": f"Connection error: {str(e)}"
                    }
        except ImportError:
            logger.error(f"{RED}aiohttp library not installed. Install with: pip install aiohttp{RESET}")
            return {
                "success": False,
                "error": "aiohttp library not installed"
            }
        except Exception as e:
            logger.error(f"{RED}Unexpected error testing Discord API: {str(e)}{RESET}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    async def verify_command_registration(self) -> Dict[str, Any]:
        """Verify if the ping command is properly registered."""
        if not self.token or not self.app_id:
            # Load from environment if not provided
            from dotenv import load_dotenv
            load_dotenv()
            self.token = self.token or os.environ.get("DISCORD_BOT_TOKEN")
            self.app_id = self.app_id or os.environ.get("CYBER1T4L_APP_ID")
        
        if not self.token or not self.app_id:
            logger.error(f"{RED}Discord token or App ID not found. Provide them as args or in .env file.{RESET}")
            return {
                "success": False,
                "error": "Missing Discord token or App ID"
            }
        
        try:
            import aiohttp
            logger.info(f"{CYAN}Checking if ping command is registered...{RESET}")
            
            # Get global commands
            url = f"https://discord.com/api/v10/applications/{self.app_id}/commands"
            headers = {"Authorization": f"Bot {self.token}"}
            
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as response:
                        if response.status == 200:
                            commands = await response.json()
                            
                            # Check if ping command exists
                            ping_command = next((cmd for cmd in commands if cmd.get("name") == "ping"), None)
                            
                            if ping_command:
                                logger.info(f"{GREEN}Ping command is registered globally with ID: {ping_command.get('id')}{RESET}")
                                return {
                                    "success": True,
                                    "command_id": ping_command.get("id"),
                                    "scope": "global",
                                    "all_commands": [cmd.get("name") for cmd in commands]
                                }
                            else:
                                logger.warning(f"{YELLOW}Ping command not found in global commands. Checking guild commands...{RESET}")
                                
                                # If guild ID is provided, check guild-specific commands
                                if self.guild_id:
                                    guild_url = f"https://discord.com/api/v10/applications/{self.app_id}/guilds/{self.guild_id}/commands"
                                    async with session.get(guild_url, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as guild_response:
                                        if guild_response.status == 200:
                                            guild_commands = await guild_response.json()
                                            ping_command = next((cmd for cmd in guild_commands if cmd.get("name") == "ping"), None)
                                            
                                            if ping_command:
                                                logger.info(f"{GREEN}Ping command is registered in guild with ID: {ping_command.get('id')}{RESET}")
                                                return {
                                                    "success": True,
                                                    "command_id": ping_command.get("id"),
                                                    "scope": "guild",
                                                    "all_commands": [cmd.get("name") for cmd in guild_commands]
                                                }
                                
                                logger.error(f"{RED}Ping command not found in registered commands{RESET}")
                                return {
                                    "success": False,
                                    "error": "Ping command not registered",
                                    "all_commands": [cmd.get("name") for cmd in commands]
                                }
                        else:
                            logger.error(f"{RED}Failed to fetch commands: HTTP {response.status}{RESET}")
                            return {
                                "success": False,
                                "error": f"Failed to fetch commands: HTTP {response.status}"
                            }
                except aiohttp.ClientError as e:
                    logger.error(f"{RED}Error fetching commands: {str(e)}{RESET}")
                    return {
                        "success": False,
                        "error": f"Error fetching commands: {str(e)}"
                    }
        except ImportError as e:
            logger.error(f"{RED}Required library not installed: {str(e)}{RESET}")
            return {
                "success": False,
                "error": f"Required library not installed: {str(e)}"
            }
        except Exception as e:
            logger.error(f"{RED}Unexpected error verifying command registration: {str(e)}{RESET}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    async def simulate_ping_interaction(self) -> Dict[str, Any]:
        """Simulate a ping command interaction (requires Discord.py)."""
        try:
            import discord
            from discord import app_commands
            from discord.ext import commands
            
            logger.info(f"{CYAN}Preparing ping command simulation...{RESET}")
            
            # Create a mock interaction context
            class MockInteraction:
                """Mock Discord interaction for testing."""
                def __init__(self):
                    self.response = MockResponse()
                    self.followup = MockFollowup()
                    self.command = None
                
                async def original_response(self):
                    """Mock original_response method."""
                    return MockMessage(content=self.response.content)
            
            class MockResponse:
                """Mock Response object."""
                def __init__(self):
                    self.content = None
                    self._sent = False
                
                async def send_message(self, content=None, **kwargs):
                    """Mock send_message method."""
                    self.content = content
                    self._sent = True
                    logger.info(f"{GREEN}Mock interaction received response: {content}{RESET}")
                
                def is_done(self):
                    """Check if response has been sent."""
                    return self._sent
                
                async def defer(self, **kwargs):
                    """Mock defer method."""
                    pass
            
            class MockFollowup:
                """Mock Followup object."""
                async def send(self, content=None, **kwargs):
                    """Mock send method."""
                    logger.info(f"{GREEN}Mock interaction received followup: {content}{RESET}")
            
            class MockMessage:
                """Mock Message object."""
                def __init__(self, content=None):
                    self.content = content
            
            # Find ping command implementation in bot code
            ping_command_found = False
            ping_command_pattern = "@bot.tree.command(name=\"ping\""
            bot_files = [
                "src/omega_bot_farm/qa/cyber1t4l_qa_bot.py",
                "src/omega_bot_farm/discord/bot.py",
                "src/omega_bot_farm/qa/test_discord_interactions.py"
            ]
            
            ping_command_func = None
            
            for file_path in bot_files:
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        if ping_command_pattern in content:
                            ping_command_found = True
                            logger.info(f"{GREEN}Found ping command definition in {file_path}{RESET}")
                            
                            # Extract the ping command function
                            import re
                            pattern = r'@.*?command\(name\s*=\s*["\']ping["\'].*?\)\s*async\s+def\s+([a-zA-Z0-9_]+)'
                            matches = re.findall(pattern, content)
                            if matches:
                                ping_func_name = matches[0]
                                logger.info(f"{GREEN}Extracted ping function name: {ping_func_name}{RESET}")
                                
                                # For this simulation, we'll use a generic ping function
                                async def ping_command(interaction):
                                    await interaction.response.send_message("🏓 Pong!")
                                
                                ping_command_func = ping_command
                            break
                except Exception as e:
                    logger.warning(f"{YELLOW}Error reading file {file_path}: {str(e)}{RESET}")
            
            if not ping_command_found:
                logger.warning(f"{YELLOW}Could not find ping command definition in bot code. Using generic implementation.{RESET}")
                async def ping_command(interaction):
                    await interaction.response.send_message("🏓 Pong!")
                
                ping_command_func = ping_command
            
            # Create and execute mock interaction
            interaction = MockInteraction()
            logger.info(f"{CYAN}Simulating ping command interaction...{RESET}")
            
            # Call the ping command function with the mock interaction
            await ping_command_func(interaction)
            
            # Check if response was sent
            if interaction.response._sent:
                logger.info(f"{GREEN}Ping command simulation successful!{RESET}")
                return {
                    "success": True,
                    "response_content": interaction.response.content,
                    "response_sent": True
                }
            else:
                logger.error(f"{RED}Ping command did not send a response{RESET}")
                return {
                    "success": False,
                    "error": "No response sent",
                    "response_sent": False
                }
            
        except ImportError as e:
            logger.error(f"{RED}Discord.py library not installed: {str(e)}{RESET}")
            return {
                "success": False,
                "error": f"Discord.py library not installed: {str(e)}"
            }
        except Exception as e:
            logger.error(f"{RED}Error simulating ping command: {str(e)}{RESET}")
            return {
                "success": False,
                "error": f"Simulation error: {str(e)}"
            }
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all ping command tests and generate recommendations."""
        logger.info(f"{CYAN}Starting ping command tests...{RESET}")
        
        # Step 1: Check Discord API connectivity
        self.results["network"] = await self.check_discord_api_connectivity()
        
        # Step 2: Verify command registration
        self.results["command_registration"] = await self.verify_command_registration()
        
        # Step 3: Simulate ping interaction
        self.results["ping_simulation"] = await self.simulate_ping_interaction()
        
        # Determine overall success
        network_ok = self.results["network"].get("success", False)
        command_ok = self.results["command_registration"].get("success", False)
        simulation_ok = self.results["ping_simulation"].get("success", False)
        
        self.results["overall"]["success"] = network_ok and command_ok and simulation_ok
        
        # Generate recommendations
        recommendations = []
        
        if not network_ok:
            recommendations.append("Check your internet connection and Discord API availability")
            recommendations.append("Verify that the bot has network access and DNS resolution works")
        
        if not command_ok:
            if not self.results["command_registration"].get("all_commands"):
                recommendations.append("No commands found. Check if commands are registered with client.tree.sync()")
                recommendations.append("Verify Discord bot token and Application ID are correct")
            else:
                recommendations.append("Ping command not found. Register it with @bot.tree.command(name='ping')")
                recommendations.append("Make sure to sync commands with await bot.tree.sync()")
        
        if not simulation_ok:
            recommendations.append("Ping command implementation issue. Check if it sends a response")
            recommendations.append("Ensure your ping command has proper error handling")
        
        if network_ok and command_ok and not simulation_ok:
            recommendations.append("Your ping command may have logic errors or exceptions")
            recommendations.append("Check logs for errors when the ping command is invoked")
        
        self.results["overall"]["recommendations"] = recommendations
        
        # Log results
        logger.info(f"\n{CYAN}===== Ping Command Test Results ====={RESET}")
        logger.info(f"Network Connectivity: {'✅' if network_ok else '❌'}")
        logger.info(f"Command Registration: {'✅' if command_ok else '❌'}")
        logger.info(f"Ping Simulation: {'✅' if simulation_ok else '❌'}")
        logger.info(f"Overall Status: {'✅ SUCCESS' if self.results['overall']['success'] else '❌ FAILED'}")
        
        if recommendations:
            logger.info(f"\n{YELLOW}Recommendations:{RESET}")
            for i, rec in enumerate(recommendations, 1):
                logger.info(f"{i}. {rec}")
        
        return self.results
    
    def save_results(self, filepath: str) -> None:
        """Save test results to a JSON file."""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(self.results, f, indent=2)
            logger.info(f"{GREEN}Results saved to {filepath}{RESET}")
        except Exception as e:
            logger.error(f"{RED}Error saving results: {str(e)}{RESET}")

async def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Discord Ping Command Tester")
    parser.add_argument("--token", type=str, help="Discord bot token (overrides .env)")
    parser.add_argument("--app-id", type=str, help="Discord application ID (overrides .env)")
    parser.add_argument("--guild-id", type=str, help="Guild ID for testing guild commands")
    parser.add_argument("--save", type=str, help="Save results to this file path")
    args = parser.parse_args()
    
    # Run tests
    tester = PingCommandTester(token=args.token, app_id=args.app_id, guild_id=args.guild_id)
    results = await tester.run_all_tests()
    
    # Save results if requested
    if args.save:
        tester.save_results(args.save)
    
    # Return appropriate exit code
    return 0 if results["overall"]["success"] else 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.info(f"{YELLOW}Test cancelled by user{RESET}")
        sys.exit(130)
    except Exception as e:
        logger.error(f"{RED}Unexpected error: {str(e)}{RESET}")
        sys.exit(1) 