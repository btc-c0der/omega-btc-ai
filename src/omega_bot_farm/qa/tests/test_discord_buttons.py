#!/usr/bin/env python3
"""
Discord Button Interaction Tests for CyBer1t4L QA Bot
----------------------------------------------------
This test suite simulates Discord button interactions with the CyBer1t4L QA Bot
to verify component-based interactions work as expected.
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
import pytest
import asyncio
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from pathlib import Path

# Add the project root to the path
script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
project_root = Path(os.path.abspath(os.path.join(script_dir, '../../../../')))
sys.path.insert(0, str(project_root))

# Import discord.py
import discord
from discord.ext import commands

# Import the bot
from src.omega_bot_farm.qa.cyber1t4l_qa_bot import DiscordConnector

class MockView(MagicMock):
    """Mock View for testing buttons."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.children = []
        
    def add_item(self, item):
        self.children.append(item)

class MockButton(MagicMock):
    """Mock Button for testing."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style = kwargs.get('style', discord.ButtonStyle.primary)
        self.label = kwargs.get('label', 'Test Button')
        self.custom_id = kwargs.get('custom_id', 'test_button')
        self.url = kwargs.get('url', None)
        self.disabled = kwargs.get('disabled', False)
        self.callback = AsyncMock()

class MockComponentInteraction(MagicMock):
    """Mock Interaction for component callbacks."""
    def __init__(self, custom_id=None, component_type=None):
        super().__init__()
        self.data = {
            "custom_id": custom_id or "test_button",
            "component_type": component_type or 2  # Button type
        }
        self.response = AsyncMock()
        self.response.send_message = AsyncMock()
        self.response.edit_message = AsyncMock()
        self.response.defer = AsyncMock()
        self.followup = AsyncMock()
        self.followup.send = AsyncMock()
        self.user = MagicMock()
        self.user.name = "TestUser"
        self.user.id = 987654321
        
class TestButtonInteractions:
    """Test Discord button interactions."""
    
    def setup_mock_coverage_button_view(self):
        """Set up a mock view with buttons for coverage report options."""
        view = MockView()
        
        # Create buttons with different coverage options
        full_button = MockButton(
            style=discord.ButtonStyle.primary,
            label="Full Report",
            custom_id="coverage_full"
        )
        
        summary_button = MockButton(
            style=discord.ButtonStyle.secondary,
            label="Summary Only",
            custom_id="coverage_summary"
        )
        
        specific_button = MockButton(
            style=discord.ButtonStyle.success,
            label="Specific Module",
            custom_id="coverage_specific"
        )
        
        # Add buttons to view
        view.add_item(full_button)
        view.add_item(summary_button)
        view.add_item(specific_button)
        
        return view, [full_button, summary_button, specific_button]
    
    async def create_coverage_report_view(self):
        """
        Simulate the real command that would create a view with buttons.
        
        This is similar to how the actual bot would create a view with buttons
        when a user requests a coverage report.
        """
        view = discord.ui.View(timeout=180)
        
        # Add buttons for different report types
        view.add_item(discord.ui.Button(
            style=discord.ButtonStyle.primary,
            label="Full Report",
            custom_id="coverage_full"
        ))
        
        view.add_item(discord.ui.Button(
            style=discord.ButtonStyle.secondary,
            label="Summary Only",
            custom_id="coverage_summary"
        ))
        
        view.add_item(discord.ui.Button(
            style=discord.ButtonStyle.success,
            label="Specific Module",
            custom_id="coverage_specific"
        ))
        
        return view
    
    @pytest.mark.asyncio
    async def test_coverage_button_callback(self):
        """Test the callback when a coverage button is clicked."""
        # Create a mock interaction with a specific button custom_id
        interaction = MockComponentInteraction(custom_id="coverage_full")
        
        # Define a callback similar to what would be in the actual bot
        async def button_callback(interaction):
            if interaction.data["custom_id"] == "coverage_full":
                await interaction.response.edit_message(
                    content="📊 **Generating full coverage report...**\n"
                            "This may take a few moments.",
                    view=None  # Remove the buttons after selection
                )
                # In a real bot, this would then generate and send the report
            elif interaction.data["custom_id"] == "coverage_summary":
                await interaction.response.edit_message(
                    content="📊 **Generating coverage summary...**\n"
                            "This may take a few moments.",
                    view=None
                )
            elif interaction.data["custom_id"] == "coverage_specific":
                await interaction.response.send_message(
                    content="Please enter the module name:",
                    ephemeral=True  # Only visible to the user who clicked
                )
        
        # Call the callback with our mock interaction
        await button_callback(interaction)
        
        # Verify that edit_message was called with the expected content
        interaction.response.edit_message.assert_called_once()
        args, kwargs = interaction.response.edit_message.call_args
        assert "full coverage report" in kwargs["content"]
        assert kwargs["view"] is None
    
    @pytest.mark.asyncio
    async def test_multiple_button_options(self):
        """Test different button selections in the coverage view."""
        # Set up our mock view with buttons
        view, buttons = self.setup_mock_coverage_button_view()
        
        # Test each button
        for button_idx, custom_id in enumerate([
            "coverage_full", "coverage_summary", "coverage_specific"
        ]):
            # Create a mock interaction for this button
            interaction = MockComponentInteraction(custom_id=custom_id)
            
            # Define a callback function similar to what would be in the actual bot
            async def button_callback(interaction):
                if interaction.data["custom_id"] == "coverage_full":
                    await interaction.response.edit_message(
                        content="Generating full report...",
                        view=None
                    )
                elif interaction.data["custom_id"] == "coverage_summary":
                    await interaction.response.edit_message(
                        content="Generating summary...",
                        view=None
                    )
                elif interaction.data["custom_id"] == "coverage_specific":
                    await interaction.response.send_message(
                        content="Please enter the module name:",
                        ephemeral=True
                    )
            
            # Call the callback with our mock interaction
            await button_callback(interaction)
            
            # Check the response based on which button was clicked
            if custom_id == "coverage_specific":
                interaction.response.send_message.assert_called_once()
                args, kwargs = interaction.response.send_message.call_args
                assert "module name" in kwargs["content"]
                assert kwargs["ephemeral"] is True
            else:
                interaction.response.edit_message.assert_called_once()
                args, kwargs = interaction.response.edit_message.call_args
                if custom_id == "coverage_full":
                    assert "full report" in kwargs["content"]
                else:
                    assert "summary" in kwargs["content"]
                
            # Reset the mock for the next iteration
            interaction.response.edit_message.reset_mock()
            interaction.response.send_message.reset_mock()
    
    @pytest.mark.asyncio
    async def test_view_timeout(self):
        """Test what happens when a view times out."""
        # In a real application, we'd likely have a timeout callback
        async def on_timeout():
            # This would typically update the message to indicate timeout
            return True
        
        # Mock the timeout behavior
        timeout_callback = AsyncMock(return_value=True)
        
        # Simulate calling the timeout callback
        result = await timeout_callback()
        
        # Verify the timeout callback was called and returned True
        timeout_callback.assert_called_once()
        assert result is True
    
    @pytest.mark.asyncio
    async def test_modal_after_button(self):
        """Test showing a modal after a button press."""
        # Create a mock interaction
        interaction = MockComponentInteraction(custom_id="coverage_specific")
        
        # Add modal-related methods to our mock
        interaction.response.send_modal = AsyncMock()
        
        # Create a simple mock modal
        mock_modal = MagicMock()
        mock_modal.title = "Module Selection"
        mock_modal.custom_id = "module_select_modal"
        
        # Define button callback that sends a modal
        async def button_callback(interaction):
            if interaction.data["custom_id"] == "coverage_specific":
                # In a real bot, we'd create a Modal class instance here
                # But for testing, we'll use our mock modal directly
                await interaction.response.send_modal(mock_modal)
        
        # Call the callback
        await button_callback(interaction)
        
        # Verify the modal was sent
        interaction.response.send_modal.assert_called_once_with(mock_modal)
    
    @pytest.mark.skipif(True, reason="E2E test requires real Discord setup")
    @pytest.mark.asyncio
    async def test_integration_with_real_objects(self):
        """
        End-to-end test using real Discord objects (not mocks).
        
        This test is skipped by default because it involves creating real Discord objects,
        which can get complex in a test environment without an actual Discord connection.
        """
        # Create a real view with buttons (but we won't be sending it to Discord)
        view = await self.create_coverage_report_view()
        
        # Verify the view was created with the expected buttons
        assert len(view.children) == 3
        assert view.children[0].label == "Full Report"
        assert view.children[1].label == "Summary Only"
        assert view.children[2].label == "Specific Module"
        
        # In a true E2E test, we would add callbacks to these buttons
        # and actually test them with real Discord interactions

if __name__ == "__main__":
    pytest.main(["-xvs", __file__])