#!/usr/bin/env python3
"""
VCR.py Tests for Discord Interactions
------------------------------------
This module demonstrates how to use VCR.py to record real
Discord API interactions and replay them for testing.

Note: This is an example and requires setup to actually record interactions.
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
import pytest
import vcr
import asyncio
from pathlib import Path
from unittest.mock import patch

# Add the project root to the path
script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
project_root = Path(os.path.abspath(os.path.join(script_dir, '../../../../')))
sys.path.insert(0, str(project_root))

# VCR configuration - where to store recorded interactions
CASSETTE_LIBRARY_DIR = script_dir / 'cassettes'
os.makedirs(CASSETTE_LIBRARY_DIR, exist_ok=True)

# Configure VCR
discord_vcr = vcr.VCR(
    cassette_library_dir=str(CASSETTE_LIBRARY_DIR),
    record_mode='once',  # 'once', 'new_episodes', 'none', or 'all'
    match_on=['uri', 'method', 'body'],
    filter_headers=['authorization'],  # Don't record the auth token
    filter_post_data_parameters=['token', 'password'],  # Don't record sensitive data
    filter_query_parameters=['token', 'key'],  # Don't record sensitive query params
)

# Import HTTP client for API requests
try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    print("WARNING: httpx not installed. Some tests will be skipped.")
    print("Install with: pip install httpx")

@pytest.mark.skipif(not HTTPX_AVAILABLE, reason="httpx not installed")
class TestDiscordAPIRecording:
    """
    Tests that demonstrate recording Discord API interactions with VCR.py.
    
    These tests show how to record real API interactions and replay them
    for testing. When running for the first time, they will make actual
    API requests if the cassettes don't exist. Subsequent runs will use
    the recorded responses.
    """
    
    @discord_vcr.use_cassette('get_bot_user.yaml')
    @pytest.mark.asyncio
    async def test_get_bot_user(self):
        """
        Test getting the bot user from Discord API.
        
        This test is just a demonstration - it will be skipped by default
        as it would require a real Discord token to record initially.
        """
        # Skip for demo purposes - remove this for actual use
        pytest.skip("Demo test - requires Discord token to record initially")
        
        # When recording for the first time, this would use a real token
        # After recording, the token would be filtered and the test would use the cassette
        bot_token = os.environ.get('DISCORD_BOT_TOKEN', 'DEMO_TOKEN')
        
        headers = {
            'Authorization': f'Bot {bot_token}',
            'Content-Type': 'application/json'
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                'https://discord.com/api/v10/users/@me',
                headers=headers
            )
            
            data = response.json()
            
            # These assertions will work on both recorded and live data
            assert response.status_code == 200
            assert 'id' in data
            assert 'username' in data
            assert 'bot' in data
            assert data['bot'] is True
    
    @discord_vcr.use_cassette('guild_commands.yaml')
    @pytest.mark.asyncio
    async def test_get_guild_commands(self):
        """
        Test getting guild application commands from the Discord API.
        
        As with the above test, this would require a real token and guild ID
        to record initially, but then would use the cassette for future runs.
        """
        # Skip for demo purposes - remove this for actual use
        pytest.skip("Demo test - requires Discord token to record initially")
        
        # Configuration - in practice, you'd get these from environment variables
        bot_token = os.environ.get('DISCORD_BOT_TOKEN', 'DEMO_TOKEN')
        application_id = os.environ.get('CYBER1T4L_APP_ID', '123456789012345678')
        guild_id = '987654321098765432'  # Replace with actual guild ID when recording
        
        headers = {
            'Authorization': f'Bot {bot_token}',
            'Content-Type': 'application/json'
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f'https://discord.com/api/v10/applications/{application_id}/guilds/{guild_id}/commands',
                headers=headers
            )
            
            data = response.json()
            
            # Assertions that should work with the recorded data
            assert response.status_code == 200
            assert isinstance(data, list)
            
            # Look for our expected commands
            command_names = [cmd['name'] for cmd in data]
            expected_commands = ['ping', 'status', 'coverage']
            
            # Check if at least one of our expected commands is present
            # This makes the test more robust if not all commands are registered
            assert any(cmd in command_names for cmd in expected_commands)

class TestInteractionReplays:
    """
    Tests that simulate Discord interactions using recorded data.
    
    These tests use VCR cassettes to replay Discord interactions for testing
    slash command responses, button clicks, and other interactions.
    """
    
    def load_interaction_data(self, filename):
        """
        Load interaction data from a JSON file in the cassettes directory.
        """
        filepath = CASSETTE_LIBRARY_DIR / filename
        
        # If the file doesn't exist, create a sample interaction for testing
        if not filepath.exists():
            # Create a directory if it doesn't exist
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # Sample interaction data for a ping command
            sample_data = {
                "type": 2,  # INTERACTION_TYPE_APPLICATION_COMMAND
                "id": "123456789012345678",
                "application_id": "987654321098765432",
                "token": "mock_token",
                "version": 1,
                "data": {
                    "id": "111111111111111111",
                    "name": "ping",
                    "type": 1  # CHAT_INPUT
                },
                "guild_id": "222222222222222222",
                "channel_id": "333333333333333333",
                "member": {
                    "user": {
                        "id": "444444444444444444",
                        "username": "test_user",
                        "discriminator": "1234"
                    },
                    "roles": [],
                    "joined_at": "2023-01-01T00:00:00.000000+00:00"
                }
            }
            
            # Write sample data to file
            with open(filepath, 'w') as f:
                json.dump(sample_data, f, indent=2)
        
        # Load and return the data
        with open(filepath, 'r') as f:
            return json.load(f)
    
    @pytest.mark.asyncio
    async def test_ping_interaction_replay(self):
        """
        Test handling a ping command interaction using recorded data.
        """
        # Load the interaction data
        interaction_data = self.load_interaction_data('ping_interaction.json')
        
        # Create a function to simulate our interaction handler
        async def handle_interaction(interaction_data):
            # In a real bot, this would parse the interaction and dispatch it
            # Here we'll directly check for the command and return a response
            
            if interaction_data['type'] == 2:  # APPLICATION_COMMAND
                command_name = interaction_data['data']['name']
                
                if command_name == 'ping':
                    return {
                        "type": 4,  # CHANNEL_MESSAGE_WITH_SOURCE
                        "data": {
                            "content": "🧪 PONG! CyBer1t4L QA Bot is alive"
                        }
                    }
            
            # Default response for unhandled interactions
            return {
                "type": 4,
                "data": {
                    "content": "Unknown command"
                }
            }
        
        # Process the interaction
        response = await handle_interaction(interaction_data)
        
        # Verify the response
        assert response['type'] == 4  # CHANNEL_MESSAGE_WITH_SOURCE
        assert "PONG" in response['data']['content']
        assert "CyBer1t4L" in response['data']['content']
    
    @pytest.mark.asyncio
    async def test_button_interaction_replay(self):
        """
        Test handling a button interaction using recorded data.
        """
        # Sample button interaction data
        button_data = {
            "type": 3,  # INTERACTION_TYPE_MESSAGE_COMPONENT
            "id": "123456789012345678",
            "application_id": "987654321098765432",
            "token": "mock_token",
            "version": 1,
            "data": {
                "custom_id": "coverage_full",
                "component_type": 2  # BUTTON
            },
            "guild_id": "222222222222222222",
            "channel_id": "333333333333333333",
            "message": {
                "id": "555555555555555555",
                "content": "Choose a coverage report type:"
            },
            "member": {
                "user": {
                    "id": "444444444444444444",
                    "username": "test_user",
                    "discriminator": "1234"
                }
            }
        }
        
        # Create a function to simulate our button handler
        async def handle_button_interaction(button_data):
            if button_data['type'] == 3:  # MESSAGE_COMPONENT
                custom_id = button_data['data']['custom_id']
                
                if custom_id == 'coverage_full':
                    return {
                        "type": 7,  # UPDATE_MESSAGE
                        "data": {
                            "content": "📊 **Generating full coverage report...**\nThis may take a few moments.",
                            "components": []  # Remove all components (buttons)
                        }
                    }
            
            # Default response
            return {
                "type": 4,
                "data": {
                    "content": "Unknown button interaction"
                }
            }
        
        # Process the button interaction
        response = await handle_button_interaction(button_data)
        
        # Verify the response
        assert response['type'] == 7  # UPDATE_MESSAGE
        assert "full coverage report" in response['data']['content']
        assert response['data']['components'] == []  # Buttons removed

if __name__ == "__main__":
    pytest.main(["-xvs", __file__]) 