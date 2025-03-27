"""
🔱 OMEGA BTC AI - WebSocket Test Suite V2 🔱
Enhanced test suite for WebSocket functionality with comprehensive test cases.
"""
import asyncio
import pytest
import json
import websockets
import ssl
from typing import List, Dict, Any
import os
from datetime import datetime, UTC

# Configuration
TEST_SERVER_URL = "ws://localhost:8765"
TEST_SERVER_SSL_URL = "wss://localhost:8766"
SSL_CERT_PATH = os.getenv('SSL_CERT_PATH', 'SSL_redis-btc-omega-redis.pem')

class TestConfig:
    """Test configuration and helper methods."""
    
    @staticmethod
    async def create_test_message(msg_type: str = "test", **kwargs) -> Dict[str, Any]:
        """Create a test message with timestamp."""
        return {
            "type": msg_type,
            "timestamp": datetime.now(UTC).isoformat(),
            **kwargs
        }

    @staticmethod
    def get_ssl_context() -> ssl.SSLContext:
        """Create SSL context for secure connections."""
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        if os.path.exists(SSL_CERT_PATH):
            ssl_context.load_verify_locations(SSL_CERT_PATH)
        return ssl_context

class TestWebSocketV2:
    """Enhanced WebSocket test suite."""

    @pytest.mark.asyncio
    async def test_basic_connection(self):
        """Test basic WebSocket connection and simple message exchange."""
        try:
            async with websockets.connect(TEST_SERVER_URL) as ws:
                test_msg = await TestConfig.create_test_message()
                await ws.send(json.dumps(test_msg))
                response = await asyncio.wait_for(ws.recv(), timeout=5)
                assert response is not None
                response_data = json.loads(response)
                assert "timestamp" in response_data
        except Exception as e:
            pytest.fail(f"❌ Basic WebSocket Connection Failed: {e}")

    @pytest.mark.asyncio
    async def test_multiple_client_broadcast(self):
        """Test broadcasting to multiple connected clients."""
        async def create_listener(client_id: int):
            async with websockets.connect(TEST_SERVER_URL) as ws:
                msg = await asyncio.wait_for(ws.recv(), timeout=5)
                return client_id, json.loads(msg)

        try:
            # Create multiple listeners
            num_clients = 3
            listeners = [create_listener(i) for i in range(num_clients)]
            listener_tasks = [asyncio.create_task(listener) for listener in listeners]
            
            # Give listeners time to connect
            await asyncio.sleep(1)
            
            # Send broadcast message
            async with websockets.connect(TEST_SERVER_URL) as sender:
                test_msg = await TestConfig.create_test_message("broadcast", value=42)
                await sender.send(json.dumps(test_msg))
            
            # Wait for all listeners
            results = await asyncio.gather(*listener_tasks)
            
            # Verify all clients received the message
            for client_id, msg in results:
                assert msg["type"] == "broadcast"
                assert msg["value"] == 42
                
        except Exception as e:
            pytest.fail(f"❌ Multiple Client Broadcast Failed: {e}")

    @pytest.mark.asyncio
    async def test_connection_timeout(self):
        """Test connection timeout handling."""
        with pytest.raises(asyncio.TimeoutError):
            async with websockets.connect(TEST_SERVER_URL) as ws:
                await asyncio.wait_for(ws.recv(), timeout=0.1)

    @pytest.mark.asyncio
    async def test_message_validation(self):
        """Test message format validation."""
        async with websockets.connect(TEST_SERVER_URL) as ws:
            # Test invalid JSON
            try:
                await ws.send("invalid json")
                response = await asyncio.wait_for(ws.recv(), timeout=5)
                # Server should close connection for invalid JSON
                pytest.fail("Server should have closed connection for invalid JSON")
            except websockets.exceptions.ConnectionClosed:
                # This is the expected behavior
                pass
            
            # Test missing required fields
            try:
                await ws.send(json.dumps({"incomplete": "message"}))
                response = await asyncio.wait_for(ws.recv(), timeout=5)
                # Server should close connection for invalid message format
                pytest.fail("Server should have closed connection for invalid message format")
            except websockets.exceptions.ConnectionClosed:
                # This is the expected behavior
                pass
            
            # Test valid message
            test_msg = await TestConfig.create_test_message()
            await ws.send(json.dumps(test_msg))
            response = await asyncio.wait_for(ws.recv(), timeout=5)
            assert response is not None
            response_data = json.loads(response)
            assert "timestamp" in response_data

    @pytest.mark.asyncio
    async def test_reconnection(self):
        """Test client reconnection handling."""
        async def connect_and_disconnect():
            ws = await websockets.connect(TEST_SERVER_URL)
            await ws.close()
            return True

        # Test multiple reconnections
        for _ in range(3):
            assert await connect_and_disconnect()
            await asyncio.sleep(0.1)

    @pytest.mark.asyncio
    async def test_load(self):
        """Test server under load."""
        async def send_messages(num_messages: int):
            async with websockets.connect(TEST_SERVER_URL) as ws:
                for i in range(num_messages):
                    test_msg = await TestConfig.create_test_message("load_test", sequence=i)
                    await ws.send(json.dumps(test_msg))
                    response = await ws.recv()
                    assert response is not None

        # Test with multiple concurrent clients sending messages
        num_clients = 5
        messages_per_client = 10
        tasks = [send_messages(messages_per_client) for _ in range(num_clients)]
        await asyncio.gather(*tasks)

    @pytest.mark.asyncio
    async def test_ssl_connection(self):
        """Test secure WebSocket connection."""
        ssl_context = TestConfig.get_ssl_context()
        try:
            async with websockets.connect(
                TEST_SERVER_SSL_URL,
                ssl=ssl_context
            ) as ws:
                test_msg = await TestConfig.create_test_message("secure")
                await ws.send(json.dumps(test_msg))
                response = await asyncio.wait_for(ws.recv(), timeout=5)
                assert response is not None
        except FileNotFoundError:
            pytest.skip("SSL certificate not found, skipping SSL test")
        except Exception as e:
            pytest.fail(f"❌ Secure WebSocket Connection Failed: {e}")

    @pytest.mark.asyncio
    async def test_btc_price_update(self):
        """Test BTC price update message handling."""
        async def price_listener():
            async with websockets.connect(TEST_SERVER_URL) as ws:
                return await asyncio.wait_for(ws.recv(), timeout=5)

        async with websockets.connect(TEST_SERVER_URL) as sender_ws:
            # Create price listener
            listener_task = asyncio.create_task(price_listener())
            await asyncio.sleep(1)
            
            # Send price update
            price_msg = await TestConfig.create_test_message(
                "btc_price",
                price=90000.00,
                volume=1000.0,
                timestamp=datetime.now(UTC).isoformat()
            )
            await sender_ws.send(json.dumps(price_msg))
            
            # Verify price update
            received_msg = await listener_task
            msg_data = json.loads(received_msg)
            assert msg_data["type"] == "btc_price"
            assert msg_data["price"] == 90000.00
            assert msg_data["volume"] == 1000.0

    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling scenarios."""
        async with websockets.connect(TEST_SERVER_URL) as ws:
            # Test oversized message
            try:
                large_msg = {"data": "x" * 1024 * 1024}  # 1MB message
                await ws.send(json.dumps(large_msg))
                response = await asyncio.wait_for(ws.recv(), timeout=5)
                # Server should close connection for oversized message
                pytest.fail("Server should have closed connection for oversized message")
            except websockets.exceptions.ConnectionClosed as e:
                # This is the expected behavior
                assert "message too big" in str(e)
            
            # Test malformed message
            try:
                await ws.send("}{")
                response = await asyncio.wait_for(ws.recv(), timeout=5)
                # Server should close connection for malformed message
                pytest.fail("Server should have closed connection for malformed message")
            except websockets.exceptions.ConnectionClosed:
                # This is the expected behavior
                pass

if __name__ == "__main__":
    pytest.main(["-v", "tests/test_websocket_v2.py"]) 