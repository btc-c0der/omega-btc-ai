
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
🔱 OMEGA BTC AI - WebSocket Integration Test Suite 🔱

This test suite validates the integration of WebSocket functionality
with other system components in the OMEGA BTC AI system.

Version: 1.0.1
GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2025-03-28
"""

import asyncio
import pytest
import json
import websockets
import os
from tests.integration.websocket.port_utility import get_websocket_uri

# Test suite header
print("\n" + "="*50)
print("🔱 OMEGA BTC AI - WEBSOCKET INTEGRATION TESTS 🔱")
print("="*50 + "\n")

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def setup_teardown():
    """Setup and teardown for the test environment."""
    # Get the WebSocket port from environment
    port = int(os.environ.get('WEBSOCKET_PORT', 9000))
    return port

@pytest.mark.asyncio
async def test_websocket_connection(setup_teardown):
    """Test basic WebSocket connection."""
    port = setup_teardown
    uri = get_websocket_uri(port)
    
    async with websockets.connect(uri) as websocket:
        # Send a test message
        await websocket.send("test")
        # Receive response
        response = await websocket.recv()
        assert response == "test"

@pytest.mark.asyncio
async def test_websocket_broadcast(setup_teardown):
    """Test WebSocket broadcast functionality."""
    port = setup_teardown
    uri = get_websocket_uri(port)
    
    # Connect multiple clients
    async with websockets.connect(uri) as ws1, websockets.connect(uri) as ws2:
        # Send message from first client
        await ws1.send("broadcast test")
        
        # Both clients should receive the message
        response1 = await ws1.recv()
        response2 = await ws2.recv()
        
        assert response1 == "broadcast test"
        assert response2 == "broadcast test"

if __name__ == "__main__":
    pytest.main(["-s", "tests/test_websocket.py"])
