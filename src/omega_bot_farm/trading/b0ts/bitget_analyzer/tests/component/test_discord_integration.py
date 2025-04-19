
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
Tests for the Discord bot integration component.

This test suite verifies that the Bitget position analyzer correctly
integrates with Discord for sending alerts and processing commands.
"""
import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

class TestDiscordIntegration:
    """Tests for the Discord integration component."""
    
    @pytest.fixture
    def mock_discord_client(self):
        """Provides a mock Discord client."""
        # Create a mock discord.Client
        mock_client = MagicMock()
        
        # Mock the async event methods
        mock_client.on_ready = AsyncMock()
        mock_client.on_message = AsyncMock()
        mock_client.send_message = AsyncMock()
        
        return mock_client
    
    @pytest.fixture
    def discord_service(self, mock_discord_client, mock_exchange_service):
        """Creates a Discord service instance with mocked dependencies."""
        # Try importing the actual service, skip if not available
        discord_srv = pytest.importorskip(
            "src.omega_bot_farm.trading.b0ts.bitget_analyzer.discord_service"
        ).DiscordService
        
        # Create the service with mocked dependencies
        service = discord_srv(
            discord_client=mock_discord_client,
            exchange_service=mock_exchange_service,
            config={
                "command_prefix": "!",
                "alert_channel_id": "123456789",
                "admin_role_id": "987654321"
            }
        )
        
        # Override the create_client method to return our mock
        service.create_client = MagicMock(return_value=mock_discord_client)
        
        return service
    
    @pytest.mark.asyncio
    async def test_discord_initialization(self, discord_service, mock_discord_client):
        """Test that the Discord service initializes correctly."""
        # Initialize the service
        await discord_service.initialize()
        
        # Verify the client was set up correctly
        assert discord_service.client == mock_discord_client
        assert hasattr(discord_service, "send_alert")
        assert hasattr(discord_service, "process_command")
    
    @pytest.mark.asyncio
    async def test_alert_sending(self, discord_service, mock_discord_client):
        """Test sending position alerts to Discord."""
        # Setup test alert data
        alert_data = {
            "symbol": "BTCUSDT",
            "position_side": "LONG",
            "message": "Position approaching liquidation price!",
            "priority": "HIGH",
            "harmony_score": 0.35
        }
        
        # Send the alert
        await discord_service.send_alert(alert_data)
        
        # Verify that the Discord client's send_message was called
        mock_discord_client.send_message.assert_called_once()
        
        # Verify that the alert channel ID was used
        call_args = mock_discord_client.send_message.call_args[0]
        assert discord_service.config["alert_channel_id"] in str(call_args)
    
    @pytest.mark.asyncio
    async def test_command_processing(self, discord_service, mock_discord_client):
        """Test processing commands from Discord."""
        # Create a mock message with a valid command
        mock_message = MagicMock()
        mock_message.content = "!position BTCUSDT"
        mock_message.author = MagicMock()
        mock_message.author.bot = False
        
        # Mock the command handler
        discord_service.handle_position_command = AsyncMock()
        
        # Process the command
        await discord_service.process_command(mock_message)
        
        # Verify the handler was called with the right arguments
        discord_service.handle_position_command.assert_called_once()
        call_args = discord_service.handle_position_command.call_args[0]
        assert "BTCUSDT" in str(call_args)
    
    @pytest.mark.asyncio
    async def test_position_command_handler(self, discord_service, mock_exchange_service, mock_discord_client):
        """Test the position command handler."""
        # Mock the message and channel
        mock_message = MagicMock()
        mock_message.channel = MagicMock()
        
        # Mock the exchange service to return position data
        mock_position = {
            "symbol": "BTCUSDT",
            "positionSide": "LONG",
            "position": 0.5,
            "entryPrice": 65000,
            "markPrice": 68000,
            "unrealizedProfit": 1500,
            "leverage": 10,
            "liquidationPrice": 59000
        }
        mock_exchange_service.get_position.return_value = mock_position
        
        # Call the handler with a symbol
        await discord_service.handle_position_command(mock_message, "BTCUSDT")
        
        # Verify that we queried the exchange service
        mock_exchange_service.get_position.assert_called_once_with("BTCUSDT")
        
        # Verify we sent a response back to Discord
        mock_message.channel.send.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_analysis_command_handler(self, discord_service, mock_discord_client):
        """Test the analysis command handler."""
        # Mock the message and channel
        mock_message = MagicMock()
        mock_message.channel = MagicMock()
        
        # Mock the analyzer component
        analyzer = MagicMock()
        analyzer.analyze_position = MagicMock(return_value={
            "symbol": "BTCUSDT",
            "risk_level": "LOW",
            "harmony_score": 0.85,
            "fibonacci_levels": {
                "0.618": 65300,
                "0.5": 66000
            },
            "recommendation": "HOLD"
        })
        discord_service.position_analyzer = analyzer
        
        # Call the handler
        await discord_service.handle_analysis_command(mock_message, "BTCUSDT")
        
        # Verify analyzer was called
        analyzer.analyze_position.assert_called_once_with("BTCUSDT")
        
        # Verify we sent a response
        mock_message.channel.send.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_unauthorized_command_handling(self, discord_service, mock_discord_client):
        """Test handling of unauthorized command attempts."""
        # Create a mock message from a user without admin role
        mock_message = MagicMock()
        mock_message.content = "!admin_command"
        mock_message.author = MagicMock()
        mock_message.author.roles = []  # No roles
        
        # Mock the is_admin check
        discord_service.is_admin = MagicMock(return_value=False)
        
        # Process the command
        await discord_service.process_command(mock_message)
        
        # Verify an error message was sent
        mock_message.channel.send.assert_called_once()
        call_args = mock_message.channel.send.call_args[0][0]
        assert "unauthorized" in call_args.lower() or "permission" in call_args.lower() 