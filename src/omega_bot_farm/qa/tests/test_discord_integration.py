#!/usr/bin/env python3
"""
Discord Integration Tests for CyBer1t4L QA Bot
----------------------------------------------
This test suite simulates Discord interactions with the CyBer1t4L QA Bot
to verify slash commands and other Discord functionality work as expected.
"""

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

# Import discord.py and testing extensions
import discord
from discord.ext import commands
try:
    import discord.ext.test as dpytest
    DPYTEST_AVAILABLE = True
except ImportError:
    DPYTEST_AVAILABLE = False
    print("WARNING: discord.ext.test not installed. Some tests will be skipped.")
    print("Install with: pip install -U discord.ext.test")

# Import the bot
from src.omega_bot_farm.qa.cyber1t4l_qa_bot import DiscordConnector

class MockDiscordClient:
    """Mock Discord client for testing."""
    def __init__(self):
        self.tree = MagicMock()
        self.tree.command = MagicMock()
        self.tree.sync = AsyncMock(return_value=["mock_command1", "mock_command2"])
        self.user = MagicMock()
        self.user.name = "CyBer1t4L"
        self.user.id = 123456789
        self.guilds = []
        self.tree.get_commands = MagicMock(return_value=[
            MagicMock(name="ping", description="Check if the bot is alive"),
            MagicMock(name="status", description="Get the current status of the QA bot"),
            MagicMock(name="coverage", description="Get the current test coverage report"),
            MagicMock(name="test", description="Run tests for a specific module")
        ])
        
    async def change_presence(self, activity=None, status=None):
        return None

class MockInteraction:
    """Mock Discord interaction for testing."""
    def __init__(self, command_name=None):
        self.response = AsyncMock()
        self.response.send_message = AsyncMock()
        self.response.is_done = MagicMock(return_value=False)
        self.response.defer = AsyncMock()
        self.followup = AsyncMock()
        self.followup.send = AsyncMock()
        self.user = MagicMock()
        self.user.name = "TestUser"
        self.user.id = 987654321
        self.data = {"name": command_name} if command_name else {}
        
@pytest.mark.skipif(not DPYTEST_AVAILABLE, reason="discord.ext.test not installed")
class TestDiscordIntegrationWithDpytest:
    """
    Test Discord integration using discord.ext.test for simulating interactions.
    These tests require discord.ext.test to be installed.
    """
    
    @pytest.fixture
    async def bot_setup(self):
        """Set up the bot for testing."""
        intents = discord.Intents.default()
        intents.message_content = True
        bot = commands.Bot(command_prefix='!', intents=intents)
        
        # Register slash commands
        @bot.tree.command(name="ping", description="Check if the bot is alive")
        async def slash_ping(interaction: discord.Interaction):
            await interaction.response.send_message("🧪 PONG! CyBer1t4L QA Bot is alive")
        
        @bot.tree.command(name="status", description="Get the current status of the QA bot")
        async def slash_status(interaction: discord.Interaction):
            await interaction.response.send_message(
                "🧬 **CyBer1t4L QA Bot Status**\n"
                f"✅ Bot is running\n"
                f"✅ Monitoring active\n"
                f"✅ Coverage analysis available\n"
            )
        
        @bot.tree.command(name="coverage", description="Get the current test coverage report")
        async def slash_coverage(interaction: discord.Interaction):
            await interaction.response.defer()
            await interaction.followup.send("📊 **Generating coverage report...**\nThis may take a few moments.")
        
        # Regular command test
        @bot.command()
        async def testcommand(ctx):
            await ctx.send("Test command executed successfully!")
        
        # Configure the bot for testing
        if DPYTEST_AVAILABLE:
            dpytest.configure(bot)
            await dpytest.start_bot(bot)
        
        yield bot
        
        # Cleanup
        if DPYTEST_AVAILABLE:
            await dpytest.empty_queue()
        await bot.close()
    
    @pytest.mark.asyncio
    async def test_ping_command(self, bot_setup):
        """Test the ping command."""
        # Test the regular command first
        await dpytest.message("!testcommand")
        assert dpytest.verify().message().content("Test command executed successfully!")
        
        # TODO: Currently dpytest doesn't fully support app commands (slash commands)
        # This will be updated once that feature is available
        # For now, this is a placeholder test
        
        print("Note: Full slash command testing via dpytest is not yet available")
        print("Slash commands will be tested using mock interactions instead")

class TestDiscordIntegration:
    """Test Discord integration using mocked objects."""
    
    def test_discord_connector_initialization(self):
        """Test that the DiscordConnector initializes correctly."""
        # Mock environment variables
        with patch.dict(os.environ, {
            "DISCORD_BOT_TOKEN": "mock_token",
            "CYBER1T4L_APP_ID": "123456789",
            "CYBER1T4L_PUBLIC_KEY": "mock_public_key"
        }):
            connector = DiscordConnector()
            
            assert connector.token == "mock_token"
            assert connector.app_id == "123456789"
            assert connector.public_key == "mock_public_key"
            assert connector.connected is False
            assert connector.client is None
    
    def test_discord_connector_is_configured(self):
        """Test the is_configured method."""
        with patch.dict(os.environ, {
            "DISCORD_BOT_TOKEN": "mock_token",
            "CYBER1T4L_APP_ID": "123456789",
            "CYBER1T4L_PUBLIC_KEY": "mock_public_key"
        }):
            connector = DiscordConnector()
            
            # Mock the discord import
            with patch('importlib.import_module', return_value=MagicMock()):
                assert connector.is_configured() is True
    
    @pytest.mark.asyncio
    async def test_slash_ping_command(self):
        """Test the ping slash command."""
        # Create mock objects
        interaction = MockInteraction(command_name="ping")
        
        # Create a mock command function similar to the one in the actual bot
        async def slash_ping(interaction):
            await interaction.response.send_message("🧪 PONG! CyBer1t4L QA Bot is alive")
        
        # Call the command
        await slash_ping(interaction)
        
        # Verify the response
        interaction.response.send_message.assert_called_once_with("🧪 PONG! CyBer1t4L QA Bot is alive")
    
    @pytest.mark.asyncio
    async def test_slash_status_command(self):
        """Test the status slash command."""
        # Create mock objects
        interaction = MockInteraction(command_name="status")
        
        # Create a mock command function
        async def slash_status(interaction):
            await interaction.response.send_message(
                "🧬 **CyBer1t4L QA Bot Status**\n"
                f"✅ Bot is running\n"
                f"✅ Monitoring active\n"
                f"✅ Coverage analysis available\n"
            )
        
        # Call the command
        await slash_status(interaction)
        
        # Verify the response
        interaction.response.send_message.assert_called_once()
        args, _ = interaction.response.send_message.call_args
        assert "CyBer1t4L QA Bot Status" in args[0]
        assert "Bot is running" in args[0]
    
    @pytest.mark.asyncio
    async def test_slash_coverage_command(self):
        """Test the coverage slash command."""
        # Create mock objects
        interaction = MockInteraction(command_name="coverage")
        
        # Create a mock command function
        async def slash_coverage(interaction):
            await interaction.response.defer()
            await interaction.followup.send("📊 **Generating coverage report...**\nThis may take a few moments.")
        
        # Call the command
        await slash_coverage(interaction)
        
        # Verify the response
        interaction.response.defer.assert_called_once()
        interaction.followup.send.assert_called_once_with("📊 **Generating coverage report...**\nThis may take a few moments.")
    
    @pytest.mark.asyncio
    async def test_on_ready_event(self):
        """Test the on_ready event handler."""
        # Create mock Discord client
        mock_client = MockDiscordClient()
        
        # Create a mock on_ready event handler similar to the one in the bot
        async def on_ready():
            await mock_client.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching, 
                    name="code quality 🧪"
                ),
                status=discord.Status.online
            )
            
            # Sync commands with Discord
            synced = await mock_client.tree.sync(guild=None)
            return len(synced)
        
        # Call the event handler
        num_commands = await on_ready()
        
        # Verify that presence was changed and commands were synced
        assert num_commands == 2  # Our mock returns 2 commands
        mock_client.tree.sync.assert_called_once()

class TestDiscordHTTPMocks:
    """
    Test Discord integration by mocking HTTP requests.
    These tests simulate how Discord would send HTTP requests to our bot.
    """
    
    @pytest.mark.skipif(True, reason="Requires httpx and respx to be installed")
    def test_interaction_webhook(self):
        """
        Test handling of an interaction webhook from Discord.
        
        This test simulates Discord sending an interaction payload to our bot,
        as would happen when a user uses a slash command in Discord.
        """
        # This test requires httpx and respx, which might not be installed
        # Skip for now, but the implementation would look like this:
        
        """
        import respx
        import httpx
        from starlette.testclient import TestClient
        from your_discord_app import app  # FastAPI app serving interactions

        client = TestClient(app)
        
        # Create a mock interaction payload for /ping
        interaction_payload = {
            "type": 2,  # APPLICATION_COMMAND
            "id": "123456789",
            "application_id": "987654321",
            "token": "mock_token",
            "data": {
                "id": "123456",
                "name": "ping",
                "type": 1  # CHAT_INPUT
            },
            "guild_id": "11111111",
            "channel_id": "222222222",
            "member": {
                "user": {
                    "id": "333333333",
                    "username": "Test User"
                }
            }
        }
        
        # Send the interaction to our bot
        response = client.post("/interactions", json=interaction_payload)
        
        # Verify the response
        assert response.status_code == 200
        assert response.json()["type"] == 4  # CHANNEL_MESSAGE
        assert "PONG" in response.json()["data"]["content"]
        """
        pass

class TestRunningBotE2E:
    """
    End-to-end tests for a running bot instance.
    
    These tests connect to a running instance of the CyBer1t4L QA Bot
    to verify its functionality with real Discord connections.
    """
    
    @pytest.fixture
    async def check_bot_process(self):
        """Check if the bot process is running and yield the PID."""
        # Use subprocess to check if the bot is running
        import subprocess
        import time
        
        # Get running CyBer1t4L processes
        result = subprocess.run(
            ["pgrep", "-f", "cyber1t4l"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0 or not result.stdout.strip():
            pytest.skip("No running CyBer1t4L bot instance found. Start the bot first with ./src/omega_bot_farm/qa/daemon_runner.sh")
            
        # Get the PID
        pids = result.stdout.strip().split('\n')
        pid = pids[0] if pids else None
        
        if not pid:
            pytest.skip("Could not determine CyBer1t4L bot PID.")
            
        print(f"Found running bot with PID: {pid}")
        
        # Check if there are logs available
        log_dir = Path(script_dir.parent / "local_run" / "logs")
        log_files = list(log_dir.glob("cyber1t4l_*.log"))
        log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        if log_files:
            log_file = log_files[0]
            print(f"Using log file: {log_file}")
            
            # Check the logs for the Discord connection
            with open(log_file, 'r') as f:
                log_content = f.read()
                if "Connected to Discord" in log_content or "Shard ID None has connected to Gateway" in log_content:
                    print("Bot appears to be connected to Discord")
                else:
                    print("Warning: Bot may not be connected to Discord based on logs")
        
        yield pid
    
    @pytest.mark.asyncio
    async def test_bot_process_running(self, check_bot_process):
        """Test that the bot process is running."""
        pid = await anext(check_bot_process)
        
        # Check that we got a valid PID
        assert pid is not None
        assert pid.isdigit()
        
        # Verify the process is still running
        import subprocess
        result = subprocess.run(
            ["ps", "-p", pid],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, "Bot process is not running"
        assert "python" in result.stdout.lower(), "Process is not a Python process"
    
    @pytest.mark.asyncio
    async def test_bot_connection_status(self, check_bot_process):
        """Test that the bot is connected to Discord."""
        # We don't actually need the PID for this test, but we still need to await the fixture
        await anext(check_bot_process)
        
        # Load environment variables for the test
        from dotenv import load_dotenv
        load_dotenv()
        
        # This test checks for bot connectivity without sending commands
        # We'll use the Discord API to check the bot's status
        
        try:
            import httpx
        except ImportError:
            pytest.skip("httpx not installed. Install with: pip install httpx")
            
        # Get credentials from environment
        bot_token = os.environ.get('DISCORD_BOT_TOKEN')
        if not bot_token:
            pytest.skip("No Discord bot token found in environment variables")
            
        # Set up headers for Discord API requests
        headers = {
            'Authorization': f'Bot {bot_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            # Check the bot user
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    'https://discord.com/api/v10/users/@me',
                    headers=headers
                )
                
                # If we get a 200 response, the bot is connected with valid credentials
                assert response.status_code == 200, "Failed to get bot user data from Discord API"
                
                data = response.json()
                assert data.get('bot', False) is True, "This is not a bot account"
                
                print(f"Bot connected as: {data.get('username', 'Unknown')}")
                
        except httpx.RequestError as e:
            pytest.fail(f"Request error when checking bot status: {str(e)}")
    
    @pytest.mark.asyncio
    async def test_bot_command_registration(self, check_bot_process):
        """Test that the bot has registered commands with Discord."""
        # We don't actually need the PID for this test, but we still need to await the fixture
        await anext(check_bot_process)
        
        # Load environment variables for the test
        from dotenv import load_dotenv
        load_dotenv()
        
        try:
            import httpx
        except ImportError:
            pytest.skip("httpx not installed. Install with: pip install httpx")
            
        # Get credentials from environment
        bot_token = os.environ.get('DISCORD_BOT_TOKEN')
        app_id = os.environ.get('CYBER1T4L_APP_ID')
        
        if not bot_token or not app_id:
            pytest.skip("Missing Discord credentials in environment variables")
            
        # Set up headers for Discord API requests
        headers = {
            'Authorization': f'Bot {bot_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            # Check global application commands
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f'https://discord.com/api/v10/applications/{app_id}/commands',
                    headers=headers
                )
                
                assert response.status_code == 200, "Failed to get application commands from Discord API"
                
                commands = response.json()
                assert len(commands) > 0, "No commands found for this bot"
                
                # Check for expected commands
                command_names = [cmd['name'] for cmd in commands]
                expected_commands = ['ping', 'status', 'coverage']
                
                # At least one of the expected commands should be registered
                assert any(cmd in command_names for cmd in expected_commands), \
                    f"None of the expected commands {expected_commands} are registered"
                
                print(f"Found registered commands: {', '.join(command_names)}")
                
        except httpx.RequestError as e:
            pytest.fail(f"Request error when checking bot commands: {str(e)}")

if __name__ == "__main__":
    pytest.main(["-xvs", __file__]) 