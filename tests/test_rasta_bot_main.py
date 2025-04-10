#!/usr/bin/env python3

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

"""
Main tests for RASTA BitGet Discord Bot

These tests focus on the core functionality and ensure we have at least 80% coverage.
"""

import pytest
import unittest.mock as mock
import sys
import os
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

# Create mock versions of the dependencies
class MockBitgetDataManager:
    def __init__(self):
        self.last_positions = []
        
    def get_positions(self):
        return {
            "positions": [
                {
                    "symbol": "BTCUSDT_UMCBL",
                    "side": "long",
                    "contracts": "0.1",
                    "entryPrice": "50000",
                    "markPrice": "51000",
                    "unrealizedPnl": "100",
                    "percentage": "2.0",
                    "leverage": "10",
                    "notional": "5000"
                }
            ],
            "timestamp": "2023-05-01 12:00:00 UTC",
            "account_balance": 1000
        }
        
    def detect_position_changes(self, positions):
        return {
            "new": [],
            "closed": [],
            "changed": []
        }

class MockPositionHarmonyManager:
    def analyze_positions(self, positions, account_balance):
        return {
            "harmony_score": 0.8,
            "harmony_state": "RESONANT",
            "divine_advice": "Your positions are in harmony with cosmic forces",
            "recommendations": [{"description": "Consider adding a 0.618 position"}],
            "ideal_position_sizes": [
                {
                    "fibonacci_relation": "0.618 of account",
                    "absolute_size": 618.0,
                    "size_pct": 0.618,
                    "risk_category": "moderate"
                }
            ]
        }

# Create module-level mocks
sys.modules['bitget_data_manager'] = MagicMock()
sys.modules['bitget_data_manager'].BitgetDataManager = MockBitgetDataManager
sys.modules['position_harmony'] = MagicMock()
sys.modules['position_harmony'].PositionHarmonyManager = MockPositionHarmonyManager
sys.modules['display_utils'] = MagicMock()
sys.modules['display_utils'].RASTA_FRAMES = ["🔴", "🟡", "🟢"]
sys.modules['display_utils'].GREEN = ""
sys.modules['display_utils'].YELLOW = ""
sys.modules['display_utils'].RED = ""
sys.modules['display_utils'].RESET = ""

# Mock Discord
sys.modules['discord'] = MagicMock()
sys.modules['discord.ext'] = MagicMock()
sys.modules['discord.ext.commands'] = MagicMock()
sys.modules['discord.ext.tasks'] = MagicMock()
sys.modules['discord.app_commands'] = MagicMock()

# Mock dotenv
sys.modules['dotenv'] = MagicMock()
sys.modules['dotenv'].load_dotenv = MagicMock()

# Create a mock for the bot module
class MockDiscordBot:
    def __init__(self):
        self.user = MagicMock()
        self.user.name = "RASTA Bot"
        self.user.id = 12345
        self.guilds = [MagicMock(), MagicMock()]
        self.tree = MagicMock()
        self.tree.sync = AsyncMock()
        self.wait_until_ready = AsyncMock()
        self.run = MagicMock()
        self.get_channel = MagicMock()

# Create a simple version of the Discord Interaction class
class MockInteraction:
    def __init__(self):
        self.response = AsyncMock()
        self.response.defer = AsyncMock()
        self.followup = AsyncMock()
        self.followup.send = AsyncMock()
        self.channel_id = 12345

# Import our bot file after setting up mocks
with patch('discord.ext.commands.Bot', return_value=MockDiscordBot()):
    import rasta_discord_bot

@pytest.fixture
def bot():
    """Return the mocked bot instance."""
    rasta_discord_bot.bot = MockDiscordBot()
    return rasta_discord_bot.bot

@pytest.fixture
def data_manager():
    """Return the mocked data manager."""
    return rasta_discord_bot.data_manager

@pytest.fixture
def harmony_manager():
    """Return the mocked harmony manager."""
    return rasta_discord_bot.harmony_manager

@pytest.mark.asyncio
async def test_on_ready(bot):
    """Test the on_ready event handler."""
    # We need to mock the position_checker task
    rasta_discord_bot.position_checker = MagicMock()
    rasta_discord_bot.position_checker.start = MagicMock()
    
    await rasta_discord_bot.on_ready()
    
    # Check that the necessary methods were called
    rasta_discord_bot.position_checker.start.assert_called_once()
    bot.tree.sync.assert_called_once()

@pytest.mark.asyncio
async def test_positions_slash():
    """Test the positions slash command."""
    interaction = MockInteraction()
    
    await rasta_discord_bot.positions_slash(interaction)
    
    # Check that necessary methods were called
    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once()
    
    # Check the call parameters
    call_args = interaction.followup.send.call_args
    assert 'embed' in call_args[1]

@pytest.mark.asyncio
async def test_harmony_slash():
    """Test the harmony slash command."""
    interaction = MockInteraction()
    
    await rasta_discord_bot.harmony_slash(interaction)
    
    # Check that necessary methods were called
    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once()
    
    # Check the call parameters
    call_args = interaction.followup.send.call_args
    assert 'embed' in call_args[1]

@pytest.mark.asyncio
async def test_wisdom_slash():
    """Test the wisdom command."""
    interaction = MockInteraction()
    interaction.response.send_message = AsyncMock()
    
    await rasta_discord_bot.wisdom_slash(interaction)
    
    # Check that send_message was called
    interaction.response.send_message.assert_called_once()
    
    # Check the call parameters
    call_args = interaction.response.send_message.call_args
    assert 'embed' in call_args[1]

@pytest.mark.asyncio
async def test_subscribe_slash():
    """Test subscribing to position updates."""
    # Clear existing subscriptions
    rasta_discord_bot.position_update_channels.clear()
    
    # Create an interaction with channel ID
    interaction = MockInteraction()
    interaction.response.send_message = AsyncMock()
    
    await rasta_discord_bot.subscribe_slash(interaction)
    
    # Check that the channel was subscribed
    assert str(interaction.channel_id) in rasta_discord_bot.position_update_channels
    interaction.response.send_message.assert_called_once()

@pytest.mark.asyncio
async def test_unsubscribe_slash():
    """Test unsubscribing from position updates."""
    # Add a channel to subscriptions
    channel_id = str(12345)
    rasta_discord_bot.position_update_channels.add(channel_id)
    
    # Create an interaction with same channel ID
    interaction = MockInteraction()
    interaction.channel_id = int(channel_id)
    interaction.response.send_message = AsyncMock()
    
    await rasta_discord_bot.unsubscribe_slash(interaction)
    
    # Check that the channel was unsubscribed
    assert channel_id not in rasta_discord_bot.position_update_channels
    interaction.response.send_message.assert_called_once()

@pytest.mark.asyncio
async def test_position_checker():
    """Test the position checker task."""
    # Mock the necessary components
    mock_channel = AsyncMock()
    
    # Add a channel to the subscriptions
    channel_id = 12345
    rasta_discord_bot.position_update_channels.add(str(channel_id))
    
    # Mock the bot's get_channel method
    rasta_discord_bot.bot.get_channel.return_value = mock_channel
    
    # Mock the data manager to return changes
    rasta_discord_bot.data_manager.detect_position_changes.return_value = {
        "new": [{"symbol": "BTCUSDT_UMCBL", "side": "long", "contracts": "0.1"}],
        "closed": [],
        "changed": []
    }
    
    # Mock send_position_changes
    with patch('rasta_discord_bot.send_position_changes') as mock_send:
        await rasta_discord_bot.position_checker()
        
        # Check that send_position_changes was called
        mock_send.assert_called_once()
        
    # Clean up
    rasta_discord_bot.position_update_channels.clear()

@pytest.mark.asyncio
async def test_position_checker_no_channels():
    """Test position checker with no subscribed channels."""
    # Clear channel subscriptions
    rasta_discord_bot.position_update_channels.clear()
    
    # The function should return early
    await rasta_discord_bot.position_checker()
    
    # Since there are no channels, it shouldn't try to get positions
    assert not hasattr(rasta_discord_bot.data_manager.get_positions, 'called') or \
           not rasta_discord_bot.data_manager.get_positions.called

@pytest.mark.asyncio
async def test_send_position_changes():
    """Test sending position changes."""
    mock_channel = AsyncMock()
    mock_channel.send = AsyncMock()
    
    changes = {
        "new": [{"symbol": "BTCUSDT_UMCBL", "side": "long", "contracts": "0.1"}],
        "closed": [{"symbol": "ETHUSDT_UMCBL", "side": "short", "contracts": "1.0"}],
        "changed": [
            {
                "position": {"symbol": "SOLUSDT_UMCBL", "side": "long", "contracts": "5.0"},
                "prev_contracts": "2.5"
            }
        ]
    }
    
    await rasta_discord_bot.send_position_changes(mock_channel, changes)
    
    # Check that channel.send was called with an embed
    mock_channel.send.assert_called_once()
    call_args = mock_channel.send.call_args
    assert 'embed' in call_args[1] 