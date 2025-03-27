import asyncio
import pytest
import json
import websockets

TEST_SERVER_URL = "ws://localhost:8765"

@pytest.mark.asyncio
async def test_websocket_connection():
    """Ensure WebSocket server is running & accepts connections."""
    try:
        async with websockets.connect(TEST_SERVER_URL) as ws:
            await ws.send(json.dumps({"test_message": "Hello, WebSocket!"}))
            response = await asyncio.wait_for(ws.recv(), timeout=5)
            assert response is not None
    except Exception as e:
        pytest.fail(f"❌ WebSocket Connection Failed: {e}")

@pytest.mark.asyncio
async def test_websocket_broadcast():
    """Ensure WebSocket correctly relays messages to multiple clients."""
    async def listener():
        async with websockets.connect(TEST_SERVER_URL) as ws:
            return await asyncio.wait_for(ws.recv(), timeout=5)

    async with websockets.connect(TEST_SERVER_URL) as sender_ws:
        # First establish the listener connection
        listener_task = asyncio.create_task(listener())
        # Give the listener time to connect
        await asyncio.sleep(1)
        # Then send the message
        await sender_ws.send(json.dumps({"btc_price": 90000.00}))
        # Wait for the response
        received_msg = await listener_task
        assert json.loads(received_msg)["btc_price"] == 90000.00

if __name__ == "__main__":
    pytest.main(["-s", "tests/test_websocket.py"])
