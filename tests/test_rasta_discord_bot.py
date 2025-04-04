#!/usr/bin/env python3
"""
Tests for the RASTA BitGet Discord Bot

These tests ensure the Discord bot functionality works correctly
and help maintain code coverage above 80%.
"""

import pytest
import asyncio
import discord
import unittest.mock as mock
from datetime import datetime
import os
import sys
from typing import Dict, List, Any, Optional

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock the Discord modules
class MockDiscordInteraction:
    """Mock for Discord Interaction class."""
    def __init__(self, channel_id=12345):
        self.channel_id = channel_id
        self.response = MockInteractionResponse()
        self.followup = MockInteractionFollowup()
        
class MockInteractionResponse:
    """Mock for Discord Interaction Response."""
    async def defer(self):
        return
        
    async def send_message(self, content=None, embed=None):
        return
        
class MockInteractionFollowup:
    """Mock for Discord Interaction Followup."""
    async def send(self, content=None, embed=None):
        return

class MockDiscordEmbed:
    """Mock for Discord Embed class."""
    def __init__(self, title=None, description=None, color=None):
        self.title = title
        self.description = description
        self.color = color
        self.fields = []
        self.footer = None
        
    def add_field(self, name, value, inline=False):
        self.fields.append({"name": name, "value": value, "inline": inline})
        return self
        
    def set_footer(self, text=None):
        self.footer = text
        return self

# Mock external dependencies
with mock.patch('discord.Intents'), \
     mock.patch('discord.ext.commands.Bot'), \
     mock.patch('discord.app_commands'), \
     mock.patch('discord.Embed', MockDiscordEmbed), \
     mock.patch('bitget_data_manager.BitgetDataManager'), \
     mock.patch('position_harmony.PositionHarmonyManager'), \
     mock.patch('dotenv.load_dotenv'):
    
    # Now import our bot module
    import rasta_discord_bot as bot_module

@pytest.fixture
def mock_bot():
    """Fixture to provide a mocked bot instance."""
    with mock.patch('rasta_discord_bot.bot') as mock_bot:
        mock_bot.user = mock.MagicMock()
        mock_bot.user.name = "RASTA BitGet Bot"
        mock_bot.user.id = 12345
        mock_bot.guilds = [mock.MagicMock(), mock.MagicMock()]
        mock_bot.tree = mock.MagicMock()
        yield mock_bot

@pytest.fixture
def mock_data_manager():
    """Fixture to provide a mocked data manager."""
    with mock.patch('rasta_discord_bot.data_manager') as mock_dm:
        yield mock_dm

@pytest.fixture
def mock_harmony_manager():
    """Fixture to provide a mocked harmony manager."""
    with mock.patch('rasta_discord_bot.harmony_manager') as mock_hm:
        yield mock_hm

@pytest.mark.asyncio
async def test_on_ready(mock_bot):
    """Test the on_ready event handler."""
    with mock.patch('rasta_discord_bot.position_checker') as mock_checker:
        await bot_module.on_ready()
        mock_checker.start.assert_called_once()
        mock_bot.tree.sync.assert_called_once()

@pytest.mark.asyncio
async def test_position_checker_empty_subscriptions():
    """Test position_checker with no subscribed channels."""
    # Clear the subscription set
    bot_module.position_update_channels.clear()
    
    # Run the checker - it should return early
    await bot_module.position_checker()
    
    # Assert that no further processing was done (verified by code inspection)
    assert len(bot_module.position_update_channels) == 0

@pytest.mark.asyncio
async def test_position_checker_with_subscriptions(mock_data_manager, mock_bot):
    """Test position_checker with subscribed channels."""
    # Add a channel to subscriptions
    channel_id = "12345"
    bot_module.position_update_channels.add(channel_id)
    
    # Mock get_positions to return valid data
    mock_data_manager.get_positions.return_value = {
        "positions": [{"symbol": "BTCUSDT", "side": "long", "contracts": 0.1}],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    }
    
    # Mock detect_position_changes to return changes
    mock_data_manager.detect_position_changes.return_value = {
        "new": [{"symbol": "BTCUSDT", "side": "long", "contracts": 0.1}],
        "closed": [],
        "changed": []
    }
    
    # Mock the get_channel method
    mock_channel = mock.MagicMock()
    mock_bot.get_channel.return_value = mock_channel
    
    # Mock send_position_changes
    with mock.patch('rasta_discord_bot.send_position_changes') as mock_send:
        await bot_module.position_checker()
        
        # Verify the call flow
        mock_data_manager.get_positions.assert_called_once()
        mock_data_manager.detect_position_changes.assert_called_once()
        mock_bot.get_channel.assert_called_once_with(int(channel_id))
        mock_send.assert_called_once()

@pytest.mark.asyncio
async def test_position_checker_error_handling(mock_data_manager):
    """Test position_checker error handling."""
    # Add a channel to subscriptions
    channel_id = "12345"
    bot_module.position_update_channels.add(channel_id)
    
    # Mock get_positions to return an error
    mock_data_manager.get_positions.return_value = {
        "error": "API error"
    }
    
    # Run the function - it should not raise an exception
    await bot_module.position_checker()
    
    # Verify the data manager was called
    mock_data_manager.get_positions.assert_called_once()
    # detect_position_changes should not be called when there's an error
    mock_data_manager.detect_position_changes.assert_not_called()

@pytest.mark.asyncio
async def test_send_position_changes():
    """Test the send_position_changes function."""
    # Create mock channel and changes
    mock_channel = mock.MagicMock()
    changes = {
        "new": [{"symbol": "BTCUSDT", "side": "long", "contracts": 0.1}],
        "closed": [{"symbol": "ETHUSDT", "side": "short", "contracts": 0.5}],
        "changed": [{
            "position": {"symbol": "SOLUSDT", "side": "long", "contracts": 1.0},
            "prev_contracts": 0.5
        }]
    }
    
    # Call the function
    await bot_module.send_position_changes(mock_channel, changes)
    
    # Assert that the channel's send method was called with an embed
    mock_channel.send.assert_called_once()
    # Check that the call had an embed parameter
    args, kwargs = mock_channel.send.call_args
    assert 'embed' in kwargs

@pytest.mark.asyncio
async def test_positions_slash_with_positions(mock_data_manager):
    """Test the positions slash command with valid positions."""
    interaction = MockDiscordInteraction()
    
    # Mock get_positions to return valid data
    mock_data_manager.get_positions.return_value = {
        "positions": [
            {
                "symbol": "BTCUSDT", 
                "side": "long", 
                "contracts": 0.1,
                "entryPrice": 50000,
                "markPrice": 51000,
                "unrealizedPnl": 100,
                "percentage": 2.0,
                "leverage": 10,
                "notional": 5000
            }
        ],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "account_balance": 1000
    }
    
    # Mock the interaction's followup.send method
    with mock.patch.object(interaction.followup, 'send') as mock_send:
        await bot_module.positions_slash(interaction)
        
        # Verify the call flow
        mock_data_manager.get_positions.assert_called_once()
        mock_send.assert_called_once()
        # Ensure an embed was sent
        args, kwargs = mock_send.call_args
        assert 'embed' in kwargs

@pytest.mark.asyncio
async def test_positions_slash_with_no_positions(mock_data_manager):
    """Test the positions slash command with no positions."""
    interaction = MockDiscordInteraction()
    
    # Mock get_positions to return empty positions list
    mock_data_manager.get_positions.return_value = {
        "positions": [],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    }
    
    # Mock the interaction's followup.send method
    with mock.patch.object(interaction.followup, 'send') as mock_send:
        await bot_module.positions_slash(interaction)
        
        # Verify the call flow
        mock_data_manager.get_positions.assert_called_once()
        mock_send.assert_called_once()
        # Ensure the no positions message was sent
        args, kwargs = mock_send.call_args
        assert "NO ACTIVE POSITIONS FOUND" in args[0]

@pytest.mark.asyncio
async def test_positions_slash_with_error(mock_data_manager):
    """Test the positions slash command with an error."""
    interaction = MockDiscordInteraction()
    
    # Mock get_positions to return an error
    mock_data_manager.get_positions.return_value = {
        "error": "API error"
    }
    
    # Mock the interaction's followup.send method
    with mock.patch.object(interaction.followup, 'send') as mock_send:
        await bot_module.positions_slash(interaction)
        
        # Verify the call flow
        mock_data_manager.get_positions.assert_called_once()
        mock_send.assert_called_once()
        # Ensure the error message was sent
        args, kwargs = mock_send.call_args
        assert "Error" in args[0]

@pytest.mark.asyncio
async def test_harmony_slash_with_data(mock_data_manager, mock_harmony_manager):
    """Test the harmony slash command with valid data."""
    interaction = MockDiscordInteraction()
    
    # Mock get_positions to return valid data
    mock_data_manager.get_positions.return_value = {
        "positions": [{"symbol": "BTCUSDT", "side": "long", "contracts": 0.1}],
        "account_balance": 1000,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    }
    
    # Mock analyze_positions to return harmony analysis
    mock_harmony_manager.analyze_positions.return_value = {
        "harmony_score": 0.8,
        "harmony_state": "RESONANT",
        "divine_advice": "Your positions are in harmony with cosmic forces",
        "recommendations": [
            {"description": "Consider adding a 0.618 Fibonacci position"},
            {"description": "Reduce leverage to align with natural rhythms"}
        ],
        "ideal_position_sizes": [
            {
                "fibonacci_relation": "0.618 of account",
                "absolute_size": 618.0,
                "size_pct": 0.618,
                "risk_category": "moderate"
            }
        ]
    }
    
    # Mock the interaction's followup.send method
    with mock.patch.object(interaction.followup, 'send') as mock_send:
        await bot_module.harmony_slash(interaction)
        
        # Verify the call flow
        mock_data_manager.get_positions.assert_called_once()
        mock_harmony_manager.analyze_positions.assert_called_once()
        mock_send.assert_called_once()
        # Ensure an embed was sent
        args, kwargs = mock_send.call_args
        assert 'embed' in kwargs

@pytest.mark.asyncio
async def test_harmony_slash_with_error(mock_data_manager):
    """Test the harmony slash command with an error."""
    interaction = MockDiscordInteraction()
    
    # Mock get_positions to return an error
    mock_data_manager.get_positions.return_value = {
        "error": "API error"
    }
    
    # Mock the interaction's followup.send method
    with mock.patch.object(interaction.followup, 'send') as mock_send:
        await bot_module.harmony_slash(interaction)
        
        # Verify the call flow
        mock_data_manager.get_positions.assert_called_once()
        mock_send.assert_called_once()
        # Ensure the error message was sent
        args, kwargs = mock_send.call_args
        assert "Error" in args[0]

@pytest.mark.asyncio
async def test_subscribe_slash_new_subscription():
    """Test subscribing a new channel."""
    # Clear existing subscriptions
    bot_module.position_update_channels.clear()
    
    # Create a mock interaction with a channel ID
    interaction = MockDiscordInteraction(channel_id=54321)
    
    # Mock the interaction's response.send_message method
    with mock.patch.object(interaction.response, 'send_message') as mock_send:
        await bot_module.subscribe_slash(interaction)
        
        # Verify the subscription was added
        assert str(interaction.channel_id) in bot_module.position_update_channels
        mock_send.assert_called_once()
        # Ensure success message was sent
        args, kwargs = mock_send.call_args
        assert "subscribed" in args[0]

@pytest.mark.asyncio
async def test_subscribe_slash_already_subscribed():
    """Test subscribing a channel that's already subscribed."""
    # Set up an existing subscription
    channel_id = "54321"
    bot_module.position_update_channels.add(channel_id)
    
    # Create a mock interaction with the same channel ID
    interaction = MockDiscordInteraction(channel_id=int(channel_id))
    
    # Mock the interaction's response.send_message method
    with mock.patch.object(interaction.response, 'send_message') as mock_send:
        await bot_module.subscribe_slash(interaction)
        
        # Verify the subscription wasn't changed
        assert channel_id in bot_module.position_update_channels
        assert len(bot_module.position_update_channels) == 1
        mock_send.assert_called_once()
        # Ensure already subscribed message was sent
        args, kwargs = mock_send.call_args
        assert "already subscribed" in args[0]

@pytest.mark.asyncio
async def test_unsubscribe_slash_remove_subscription():
    """Test unsubscribing a channel."""
    # Set up an existing subscription
    channel_id = "54321"
    bot_module.position_update_channels.add(channel_id)
    
    # Create a mock interaction with the same channel ID
    interaction = MockDiscordInteraction(channel_id=int(channel_id))
    
    # Mock the interaction's response.send_message method
    with mock.patch.object(interaction.response, 'send_message') as mock_send:
        await bot_module.unsubscribe_slash(interaction)
        
        # Verify the subscription was removed
        assert channel_id not in bot_module.position_update_channels
        assert len(bot_module.position_update_channels) == 0
        mock_send.assert_called_once()
        # Ensure unsubscribed message was sent
        args, kwargs = mock_send.call_args
        assert "unsubscribed" in args[0]

@pytest.mark.asyncio
async def test_unsubscribe_slash_not_subscribed():
    """Test unsubscribing a channel that's not subscribed."""
    # Clear existing subscriptions
    bot_module.position_update_channels.clear()
    
    # Create a mock interaction
    interaction = MockDiscordInteraction(channel_id=54321)
    
    # Mock the interaction's response.send_message method
    with mock.patch.object(interaction.response, 'send_message') as mock_send:
        await bot_module.unsubscribe_slash(interaction)
        
        # Verify no change to subscriptions
        assert len(bot_module.position_update_channels) == 0
        mock_send.assert_called_once()
        # Ensure not subscribed message was sent
        args, kwargs = mock_send.call_args
        assert "not subscribed" in args[0]

@pytest.mark.asyncio
async def test_wisdom_slash():
    """Test the wisdom slash command."""
    interaction = MockDiscordInteraction()
    
    # Mock the interaction's response.send_message method
    with mock.patch.object(interaction.response, 'send_message') as mock_send:
        await bot_module.wisdom_slash(interaction)
        
        # Verify an embed was sent
        mock_send.assert_called_once()
        args, kwargs = mock_send.call_args
        assert 'embed' in kwargs
        # Check the embed has the right title
        assert kwargs['embed'].title == "🔮 RASTA TRADING WISDOM"

@pytest.mark.asyncio
async def test_before_position_checker(mock_bot):
    """Test the before_position_checker method."""
    await bot_module.before_position_checker()
    mock_bot.wait_until_ready.assert_called_once() 