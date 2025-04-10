
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
End-to-end tests for Discord integration.

These tests verify that the Bitget position analyzer correctly
integrates with Discord in a real-world-like environment.
"""
import os
import json
import pytest
import asyncio
import logging
from unittest.mock import patch, MagicMock, AsyncMock

logger = logging.getLogger('e2e_tests.discord')

@pytest.fixture
async def discord_bot_handler(exchange_service, notification_service, e2e_config):
    """Create a Discord bot handler for end-to-end testing."""
    try:
        from src.omega_bot_farm.trading.b0ts.bitget_analyzer.discord_bot import DiscordBotHandler
        
        # Create the handler with mocked dependencies
        handler = DiscordBotHandler(
            exchange_service=exchange_service,
            notification_service=notification_service,
            config={
                "command_prefix": "!",
                "alert_channel_id": "123456789",
                "admin_role_id": "987654321",
                "symbols": e2e_config["test_symbols"],
                "test_mode": True
            }
        )
        
        # Mock Discord client
        mock_client = AsyncMock()
        mock_client.user = MagicMock()
        mock_client.user.name = "BitgetAnalyzerBot"
        
        # Patch the handler's discord client
        handler.client = mock_client
        
        return handler
    except ImportError:
        # Create a mock handler if we can't import the actual one
        pytest.skip("DiscordBotHandler not available")
        return None

@pytest.mark.asyncio
@pytest.mark.e2e
async def test_discord_bot_command_handling(discord_bot_handler, position_analyzer_bot):
    """
    Test Discord bot command handling.
    
    This test verifies that the Discord bot correctly processes commands
    and returns appropriate responses.
    """
    # Skip if we couldn't create the handler or bot
    if discord_bot_handler is None or position_analyzer_bot is None:
        pytest.skip("Required components not available")
    
    logger.info("Starting Discord command handling test")
    
    # Set up a mock Discord message
    mock_message = AsyncMock()
    mock_message.content = "!position BTCUSDT"
    mock_message.author = MagicMock()
    mock_message.author.bot = False
    mock_message.author.name = "TestUser"
    mock_message.channel = AsyncMock()
    
    # Connect the position analyzer bot
    discord_bot_handler.position_analyzer = position_analyzer_bot
    
    # Process the command
    logger.info("Processing position command")
    await discord_bot_handler.on_message(mock_message)
    
    # Verify response was sent
    mock_message.channel.send.assert_called_once()
    
    # Test analysis command
    mock_message.content = "!analyze BTCUSDT"
    mock_message.channel.send.reset_mock()
    
    logger.info("Processing analysis command")
    await discord_bot_handler.on_message(mock_message)
    
    # Verify analysis response was sent
    mock_message.channel.send.assert_called_once()
    
    # Test help command
    mock_message.content = "!help"
    mock_message.channel.send.reset_mock()
    
    logger.info("Processing help command")
    await discord_bot_handler.on_message(mock_message)
    
    # Verify help response was sent
    mock_message.channel.send.assert_called_once()
    
    logger.info("Discord command handling test completed successfully")

@pytest.mark.asyncio
@pytest.mark.e2e
async def test_discord_alert_notifications(discord_bot_handler, exchange_service, notification_service):
    """
    Test Discord alert notifications.
    
    This test verifies that the Discord bot correctly sends alert
    notifications when triggered.
    """
    # Skip if we couldn't create the handler
    if discord_bot_handler is None:
        pytest.skip("Discord bot handler not available")
    
    logger.info("Starting Discord alert notifications test")
    
    # Create a test alert
    test_alert = {
        "symbol": "BTCUSDT",
        "message": "Test alert notification",
        "priority": "HIGH",
        "type": "RISK_ALERT",
        "details": {
            "risk_level": "HIGH",
            "liquidation_distance_percent": 5.0,
            "current_price": 61000,
            "liquidation_price": 60000
        }
    }
    
    # Send the alert
    logger.info("Sending test alert")
    await discord_bot_handler.send_alert(test_alert)
    
    # Verify the alert was sent to Discord
    discord_bot_handler.client.get_channel.assert_called_once()
    channel = discord_bot_handler.client.get_channel.return_value
    channel.send.assert_called_once()
    
    # Verify alert content
    call_args = channel.send.call_args[0][0]
    assert "BTCUSDT" in call_args, "Alert should contain symbol"
    assert "HIGH" in call_args, "Alert should contain priority"
    
    logger.info("Discord alert notifications test completed successfully")

@pytest.mark.asyncio
@pytest.mark.e2e
async def test_discord_event_handlers(discord_bot_handler):
    """
    Test Discord event handlers.
    
    This test verifies that the Discord bot correctly handles Discord events.
    """
    # Skip if we couldn't create the handler
    if discord_bot_handler is None:
        pytest.skip("Discord bot handler not available")
    
    logger.info("Starting Discord event handlers test")
    
    # Test on_ready handler
    logger.info("Testing on_ready handler")
    await discord_bot_handler.on_ready()
    
    # No assertions needed, just make sure it doesn't error
    
    # Test on_guild_join handler
    mock_guild = MagicMock()
    mock_guild.name = "Test Guild"
    mock_guild.id = "123456789"
    
    logger.info("Testing on_guild_join handler")
    await discord_bot_handler.on_guild_join(mock_guild)
    
    # No assertions needed, just make sure it doesn't error
    
    logger.info("Discord event handlers test completed successfully")

@pytest.mark.asyncio
@pytest.mark.e2e
async def test_discord_admin_commands(discord_bot_handler, exchange_service):
    """
    Test Discord admin commands.
    
    This test verifies that the Discord bot correctly handles admin commands
    and restricts access appropriately.
    """
    # Skip if we couldn't create the handler
    if discord_bot_handler is None:
        pytest.skip("Discord bot handler not available")
    
    logger.info("Starting Discord admin commands test")
    
    # Set up mock admin message
    mock_admin_message = AsyncMock()
    mock_admin_message.content = "!admin refresh_markets"
    mock_admin_message.author = MagicMock()
    mock_admin_message.author.bot = False
    mock_admin_message.author.name = "AdminUser"
    mock_admin_message.channel = AsyncMock()
    
    # Mock roles
    admin_role = MagicMock()
    admin_role.id = discord_bot_handler.config["admin_role_id"]
    mock_admin_message.author.roles = [admin_role]
    
    # Process admin command as admin
    logger.info("Processing admin command with admin privileges")
    
    # Mock the is_admin check
    discord_bot_handler.is_admin = MagicMock(return_value=True)
    
    await discord_bot_handler.on_message(mock_admin_message)
    
    # Verify response was sent
    mock_admin_message.channel.send.assert_called_once()
    
    # Set up mock non-admin message
    mock_non_admin_message = AsyncMock()
    mock_non_admin_message.content = "!admin refresh_markets"
    mock_non_admin_message.author = MagicMock()
    mock_non_admin_message.author.bot = False
    mock_non_admin_message.author.name = "RegularUser"
    mock_non_admin_message.channel = AsyncMock()
    mock_non_admin_message.author.roles = []
    
    # Process admin command as non-admin
    logger.info("Processing admin command without admin privileges")
    
    # Mock the is_admin check
    discord_bot_handler.is_admin = MagicMock(return_value=False)
    
    await discord_bot_handler.on_message(mock_non_admin_message)
    
    # Verify error response was sent
    mock_non_admin_message.channel.send.assert_called_once()
    
    # Check for unauthorized message
    call_args = mock_non_admin_message.channel.send.call_args[0][0]
    assert "permission" in call_args.lower() or "unauthorized" in call_args.lower()
    
    logger.info("Discord admin commands test completed successfully") 