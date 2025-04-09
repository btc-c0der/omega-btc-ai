"""
🔱 OMEGA BTC AI - WebSocket Test Suite 🔱

This test suite validates the core WebSocket functionality of the OMEGA BTC AI system.

Version: 1.0.1
GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2025-03-28
"""

import asyncio
import pytest
import json
import websockets

# ASCII Art Banner
print("""
    ⚡ OMEGA BTC AI - WEBSOCKET TEST SUITE ⚡
    
    🔱 TESTING DIVINE CONNECTIONS 🔱
    🔱 VALIDATING COSMIC FLOW 🔱
    🔱 ENSURING QUANTUM HARMONY 🔱
""")

TEST_SERVER_URL = "ws://localhost:8765"

@pytest.mark.asyncio
async def test_websocket_connection():
    """Test the divine connection to the WebSocket server.
    
    This test ensures the WebSocket server is running and accepts connections
    with proper message handling and response validation.
    """
    try:
        async with websockets.connect(TEST_SERVER_URL) as ws:
            await ws.send(json.dumps({"test_message": "Hello, WebSocket!"}))
            response = await asyncio.wait_for(ws.recv(), timeout=5)
            assert response is not None
    except Exception as e:
        pytest.fail(f"❌ WebSocket Connection Failed: {e}")

@pytest.mark.asyncio
async def test_websocket_broadcast():
    """Test the cosmic broadcast functionality of the WebSocket server.
    
    This test validates that messages are correctly relayed to multiple clients
    maintaining data consistency across the divine network.
    """
    async def listener():
        async with websockets.connect(TEST_SERVER_URL) as ws:
            return await asyncio.wait_for(ws.recv(), timeout=5)

    async with websockets.connect(TEST_SERVER_URL) as sender_ws:
        await sender_ws.send(json.dumps({"btc_price": 90000.00}))

        received_msg = await listener()
        assert json.loads(received_msg)["btc_price"] == 90000.00

if __name__ == "__main__":
    pytest.main(["-s", "tests/test_websocket.py"])
