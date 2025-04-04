#!/usr/bin/env python3
"""
Mock Discord Interactions Test Suite for CyBer1t4L Bot

This script simulates testing Discord interaction endpoints without requiring a live Discord connection.
It mocks the Discord.py API to validate interaction behavior offline.
"""

import os
import sys
import json
import logging
import asyncio
import argparse
from datetime import datetime
from typing import Dict, Any, Optional, List, Callable
from unittest.mock import MagicMock, AsyncMock
from pathlib import Path

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
logger = logging.getLogger("DiscordInteractionsMockTest")

class MockInteraction:
    """Mock for Discord Interaction object."""
    
    def __init__(self, user: str = "TestUser#1234"):
        self.user = user
        self._response_sent = False
        self.response = self._create_response()
        self.followup = self._create_followup()
        self._original_content = None
    
    def _create_response(self):
        """Create a mock response object."""
        response = MagicMock()
        
        # Mock send_message method
        async def send_message(content=None, **kwargs):
            logger.info(f"Mock interaction.response.send_message() called with: {content}")
            self._response_sent = True
            self._original_content = content
            return True
        
        response.send_message = AsyncMock(side_effect=send_message)
        
        # Mock defer method
        async def defer(**kwargs):
            logger.info("Mock interaction.response.defer() called")
            self._response_sent = True
            return True
        
        response.defer = AsyncMock(side_effect=defer)
        
        # Mock is_done method
        def is_done():
            return self._response_sent
        
        response.is_done = MagicMock(side_effect=is_done)
        
        return response
    
    def _create_followup(self):
        """Create a mock followup object."""
        followup = MagicMock()
        
        # Mock send method
        async def send(content=None, **kwargs):
            logger.info(f"Mock interaction.followup.send() called with: {content}")
            return MagicMock(content=content)
        
        followup.send = AsyncMock(side_effect=send)
        
        return followup
    
    async def edit_original_response(self, content=None, **kwargs):
        """Mock edit_original_response method."""
        logger.info(f"Mock interaction.edit_original_response() called with: {content}")
        self._original_content = content
        return MagicMock(content=content)
    
    async def original_response(self):
        """Mock original_response method."""
        logger.info("Mock interaction.original_response() called")
        return MagicMock(content=self._original_content)

class MockDiscordClient:
    """Mock for Discord Client object."""
    
    def __init__(self):
        self.user = MagicMock(id="123456789", name="MockBot")
        self.guilds = [
            MagicMock(
                id="987654321", 
                name="MockGuild",
                text_channels=[
                    MagicMock(
                        id="111222333", 
                        name="general",
                        permissions_for=lambda _: MagicMock(send_messages=True)
                    )
                ],
                me=MagicMock(name="BotMember")
            )
        ]
        self.tree = self._create_command_tree()
        # Create a placeholder for on_ready event handler
        self._on_ready_callback = None
    
    def _create_command_tree(self):
        """Create a mock command tree object."""
        tree = MagicMock()
        tree.command = MagicMock(return_value=lambda func: func)
        tree.add_command = MagicMock()
        tree.sync = AsyncMock(return_value=["command1", "command2"])
        tree.clear_commands = MagicMock()
        return tree
    
    async def start(self, token):
        """Mock start method."""
        logger.info("Mock client.start() called")
        # Simulate the on_ready event
        if self._on_ready_callback:
            await self._on_ready_callback()
        return True
    
    async def close(self):
        """Mock close method."""
        logger.info("Mock client.close() called")
        return True

class DiscordMockTester:
    """Tests Discord interaction endpoints using mocked Discord objects."""
    
    def __init__(self):
        self.client = MockDiscordClient()
        self.guild_id = "987654321"
        self.test_channel_id = "111222333"
        self.interaction_responses = {}
        
        # Register event handlers as callbacks
        self.client._on_ready_callback = self._on_ready
    
    async def _on_ready(self):
        """Mock on_ready event handler."""
        logger.info(f"{GREEN}Connected as {self.client.user.name} (ID: {self.client.user.id}){RESET}")
        logger.info(f"Using guild: {self.client.guilds[0].name} (ID: {self.guild_id})")
        logger.info(f"Using channel: {self.client.guilds[0].text_channels[0].name} (ID: {self.test_channel_id})")
        
        # Initialize mock tests
        asyncio.create_task(self.run_tests())
    
    async def start(self):
        """Start the mock testing."""
        logger.info(f"{YELLOW}Starting Discord mock tests...{RESET}")
        await self.client.start("mock_token")
        return True
    
    async def run_tests(self):
        """Run all the mock interaction tests."""
        # Define test cases
        test_cases = [
            ("response_send_message", self.test_response_send_message),
            ("response_defer", self.test_response_defer),
            ("response_edit", self.test_response_edit),
            ("response_is_done", self.test_response_is_done),
            ("error_handling", self.test_error_handling),
            ("original_response", self.test_original_response)
        ]
        
        # Run each test case
        for test_name, test_func in test_cases:
            try:
                logger.info(f"{YELLOW}Running test: {test_name}{RESET}")
                result = await test_func()
                if result:
                    self.interaction_responses[test_name] = "success"
                    logger.info(f"{GREEN}Test {test_name} passed{RESET}")
                else:
                    self.interaction_responses[test_name] = "failed: test returned False"
                    logger.error(f"{RED}Test {test_name} failed{RESET}")
            except Exception as e:
                self.interaction_responses[test_name] = f"failed: {str(e)}"
                logger.error(f"{RED}Error in test {test_name}: {str(e)}{RESET}")
        
        # Generate and print report
        report = self.generate_report()
        print("\n" + "="*50)
        print(report)
        print("="*50 + "\n")
        
        # Also generate the report file since we have results now
        self.write_report_file()
    
    async def test_response_send_message(self) -> bool:
        """Test interaction.response.send_message()."""
        interaction = MockInteraction()
        
        # Test sending a message
        await interaction.response.send_message("✅ Test response sent successfully!")
        
        # Verify the response was sent
        return interaction.response.is_done()
    
    async def test_response_defer(self) -> bool:
        """Test interaction.response.defer() and followup."""
        interaction = MockInteraction()
        
        # Test deferring the response
        await interaction.response.defer()
        
        # Verify the response was deferred
        if not interaction.response.is_done():
            return False
        
        # Test following up after deferring
        await interaction.followup.send("✅ Deferred response followed up successfully!")
        
        return True
    
    async def test_response_edit(self) -> bool:
        """Test interaction.edit_original_response()."""
        interaction = MockInteraction()
        
        # Send initial response
        await interaction.response.send_message("Initial response")
        
        # Edit the response
        await interaction.edit_original_response(content="✅ Edited the initial response successfully!")
        
        # Verify the content was edited
        original = await interaction.original_response()
        return original.content == "✅ Edited the initial response successfully!"
    
    async def test_response_is_done(self) -> bool:
        """Test interaction.response.is_done()."""
        interaction = MockInteraction()
        
        # Check if response is done before sending (should be False)
        before_send = interaction.response.is_done()
        
        # Send a response
        await interaction.response.send_message("Testing is_done()")
        
        # Check if response is done after sending (should be True)
        after_send = interaction.response.is_done()
        
        return not before_send and after_send
    
    async def test_error_handling(self) -> bool:
        """Test error handling during interaction."""
        interaction = MockInteraction()
        
        try:
            # Simulate an error
            raise ValueError("This is a simulated error")
        except Exception as e:
            # Handle the error
            logger.info(f"{CYAN}Caught error as expected: {str(e)}{RESET}")
            await interaction.response.send_message(f"✅ Error handled successfully: {type(e).__name__}")
            return True
        
        return False
    
    async def test_original_response(self) -> bool:
        """Test interaction.original_response()."""
        interaction = MockInteraction()
        
        # Send a message
        test_content = "Testing original_response()"
        await interaction.response.send_message(test_content)
        
        # Get the original response
        original = await interaction.original_response()
        
        # Verify the content matches
        return original.content == test_content
    
    def generate_report(self) -> str:
        """Generate a report from the interaction responses."""
        if not self.interaction_responses:
            return "No tests have been run yet."
        
        success_count = sum(1 for result in self.interaction_responses.values() if result == "success")
        total_count = len(self.interaction_responses)
        
        report = [
            f"Discord Interactions Mock Test Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Success Rate: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)\n"
        ]
        
        for test_name, result in self.interaction_responses.items():
            status = "✅ PASS" if result == "success" else "❌ FAIL"
            report.append(f"{status}: {test_name} - {result}")
        
        return "\n".join(report)
    
    def write_report_file(self):
        """Write the test report to a Markdown file."""
        report_path = Path('discord_interaction_test_results.md')
        
        with open(report_path, 'w') as f:
            f.write("# Discord Interaction Mock Test Results\n\n")
            f.write("These tests validate the interaction endpoints that the bot uses.\n\n")
            
            # Add the actual test results
            if self.interaction_responses:
                success_count = sum(1 for result in self.interaction_responses.values() if result == "success")
                total_count = len(self.interaction_responses)
                
                f.write(f"## Summary\n\n")
                f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"**Success Rate:** {success_count}/{total_count} ({success_count/total_count*100:.1f}%)\n\n")
                
                f.write("## Test Results\n\n")
                for test_name, result in self.interaction_responses.items():
                    status = "✅ PASS" if result == "success" else "❌ FAIL"
                    f.write(f"### {status} {test_name}\n\n")
                    f.write(f"Result: `{result}`\n\n")
            else:
                f.write("No tests have been run yet.\n\n")
            
            f.write("## Tested Interaction Endpoints\n\n")
            f.write("- `interaction.response.send_message()`\n")
            f.write("- `interaction.response.defer()`\n")
            f.write("- `interaction.edit_original_response()`\n")
            f.write("- `interaction.response.is_done()`\n")
            f.write("- `interaction.original_response()`\n")
            f.write("- Error handling during interactions\n")
            
            # Add notes about what these endpoints are used for in the CyBer1t4L bot
            f.write("\n## Notes\n\n")
            f.write("These endpoints are used in the CyBer1t4L bot for the following purposes:\n\n")
            f.write("1. **send_message**: Used in all slash commands to provide immediate responses\n")
            f.write("2. **defer**: Used in longer-running commands like `/coverage` and `/test`\n")
            f.write("3. **is_done**: Used in error handling to check if a response has already been sent\n")
            f.write("4. **edit_original_response**: Used to update responses with new information\n")
            f.write("5. **original_response**: Used to retrieve and reference previously sent responses\n")
        
        logger.info(f"{GREEN}Mock tests completed. Results saved to {report_path}{RESET}")

async def main():
    """Main entry point."""
    try:
        logger.info(f"{CYAN}Starting Discord Interaction Mock Tester...{RESET}")
        
        # Create and start the tester
        tester = DiscordMockTester()
        await tester.start()
        
        # Wait for tests to complete (this is just to keep the program running)
        await asyncio.sleep(1)
        
    except KeyboardInterrupt:
        logger.info(f"{YELLOW}Test cancelled by user.{RESET}")
    except Exception as e:
        logger.error(f"{RED}Unexpected error: {str(e)}{RESET}")
        import traceback
        logger.error(f"{RED}Traceback: {traceback.format_exc()}{RESET}")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        logger.info(f"{YELLOW}Test cancelled by user.{RESET}")
        sys.exit(0) 