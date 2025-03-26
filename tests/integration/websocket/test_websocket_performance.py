"""Performance tests for WebSocket functionality in the trap visualizer server."""

import pytest
import asyncio
import time
import statistics
from datetime import datetime, UTC, timedelta
from unittest.mock import Mock, patch, AsyncMock
import json
from fastapi.testclient import TestClient
from omega_ai.utils.redis_manager import RedisManager
from omega_ai.visualizer.backend.unified_server import TrapVisualizerServer

@pytest.fixture
def redis_manager():
    """Create a mock Redis manager."""
    manager = Mock(spec=RedisManager)
    manager.get_cached.return_value = {
        "traps": [
            {
                "id": "1",
                "type": "FAKE_DUMP",
                "timestamp": datetime.now(UTC) - timedelta(hours=2),
                "confidence": 0.92,
                "price": 34500.0,
                "volume": 150.0,
                "description": "Fake dump detected",
                "success": False
            }
        ]
    }
    return manager

@pytest.fixture
def server(redis_manager):
    """Create a test server instance."""
    return TrapVisualizerServer("Test Trap Visualizer", redis_manager)

@pytest.fixture
def client(server):
    """Create a test client."""
    return TestClient(server.app)

@pytest.mark.asyncio
async def test_websocket_connection_time(client):
    """Test WebSocket connection establishment time."""
    connection_times = []
    
    for _ in range(10):  # Test 10 connections
        start_time = time.time()
        with client.websocket_connect("/ws") as websocket:
            end_time = time.time()
            connection_times.append(end_time - start_time)
    
    avg_time = statistics.mean(connection_times)
    max_time = max(connection_times)
    
    # Connection should be established within 100ms
    assert avg_time < 0.1
    assert max_time < 0.2

@pytest.mark.asyncio
async def test_websocket_message_latency(client):
    """Test WebSocket message round-trip latency."""
    latencies = []
    
    with client.websocket_connect("/ws") as websocket:
        for _ in range(50):  # Test 50 messages
            start_time = time.time()
            websocket.send_text(json.dumps({"type": "ping"}))
            response = websocket.receive_json()
            end_time = time.time()
            latencies.append(end_time - start_time)
    
    avg_latency = statistics.mean(latencies)
    p95_latency = statistics.quantiles(latencies, n=20)[-1]  # 95th percentile
    
    # Messages should be processed within 50ms
    assert avg_latency < 0.05
    assert p95_latency < 0.1

@pytest.mark.asyncio
async def test_websocket_concurrent_connections(client):
    """Test server performance with multiple concurrent connections."""
    num_connections = 50
    connections = []
    
    try:
        # Establish multiple connections simultaneously
        start_time = time.time()
        for _ in range(num_connections):
            websocket = client.websocket_connect("/ws")
            connections.append(websocket)
            websocket.__enter__()
        end_time = time.time()
        
        # All connections should be established within 2 seconds
        assert end_time - start_time < 2.0
        
        # Verify all connections are active
        assert len(client.app.connection_manager.active_connections) == num_connections
        
    finally:
        # Clean up connections
        for websocket in connections:
            try:
                websocket.__exit__(None, None, None)
            except:
                pass

@pytest.mark.asyncio
async def test_websocket_message_throughput(client):
    """Test WebSocket message throughput under load."""
    num_messages = 1000
    message_size = 1000  # bytes
    
    with client.websocket_connect("/ws") as websocket:
        # Prepare test message
        test_message = json.dumps({
            "type": "message",
            "data": "A" * message_size
        })
        
        # Send messages and measure throughput
        start_time = time.time()
        for _ in range(num_messages):
            websocket.send_text(test_message)
            websocket.receive_json()  # Wait for response
        end_time = time.time()
        
        # Calculate throughput
        duration = end_time - start_time
        throughput = num_messages / duration  # messages per second
        data_throughput = (num_messages * message_size) / duration  # bytes per second
        
        # Should handle at least 100 messages per second
        assert throughput > 100
        # Should handle at least 100KB/s
        assert data_throughput > 100 * 1024

@pytest.mark.asyncio
async def test_websocket_memory_usage(client):
    """Test WebSocket server memory usage under load."""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Create multiple connections and send messages
    num_connections = 20
    messages_per_connection = 100
    connections = []
    
    try:
        for _ in range(num_connections):
            websocket = client.websocket_connect("/ws")
            connections.append(websocket)
            websocket.__enter__()
            
            for _ in range(messages_per_connection):
                websocket.send_text(json.dumps({"type": "message", "data": "test"}))
                websocket.receive_json()
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be less than 50MB
        assert memory_increase < 50 * 1024 * 1024
        
    finally:
        for websocket in connections:
            try:
                websocket.__exit__(None, None, None)
            except:
                pass

@pytest.mark.asyncio
async def test_websocket_long_running_connection(client):
    """Test WebSocket server stability during long-running connections."""
    duration = 30  # seconds
    message_interval = 0.1  # seconds
    
    with client.websocket_connect("/ws") as websocket:
        start_time = time.time()
        messages_sent = 0
        messages_received = 0
        
        while time.time() - start_time < duration:
            websocket.send_text(json.dumps({"type": "ping"}))
            response = websocket.receive_json()
            messages_sent += 1
            messages_received += 1
            await asyncio.sleep(message_interval)
        
        # Verify connection remained stable
        assert messages_sent == messages_received
        assert messages_sent > 0

@pytest.mark.asyncio
async def test_websocket_burst_handling(client):
    """Test WebSocket server handling of message bursts."""
    burst_size = 100
    message_size = 1000  # bytes
    
    with client.websocket_connect("/ws") as websocket:
        # Prepare test message
        test_message = json.dumps({
            "type": "message",
            "data": "A" * message_size
        })
        
        # Send burst of messages
        start_time = time.time()
        for _ in range(burst_size):
            websocket.send_text(test_message)
        
        # Receive responses
        responses = []
        while len(responses) < burst_size:
            try:
                response = websocket.receive_json()
                responses.append(response)
            except Exception:
                break
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should handle burst within 2 seconds
        assert duration < 2.0
        assert len(responses) == burst_size

@pytest.mark.asyncio
async def test_websocket_error_recovery(client):
    """Test WebSocket server recovery from errors."""
    recovery_times = []
    
    for _ in range(5):  # Test 5 recovery scenarios
        with client.websocket_connect("/ws") as websocket:
            # Send invalid message to trigger error
            websocket.send_text("invalid json")
            start_time = time.time()
            
            # Wait for error response
            response = websocket.receive_json()
            assert response["type"] == "error"
            
            # Send valid message to test recovery
            websocket.send_text(json.dumps({"type": "ping"}))
            response = websocket.receive_json()
            end_time = time.time()
            
            recovery_times.append(end_time - start_time)
    
    avg_recovery_time = statistics.mean(recovery_times)
    # Should recover within 100ms
    assert avg_recovery_time < 0.1

@pytest.mark.asyncio
async def test_websocket_resource_cleanup(client):
    """Test WebSocket server resource cleanup after disconnections."""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Create and close multiple connections
    num_connections = 50
    for _ in range(num_connections):
        with client.websocket_connect("/ws") as websocket:
            websocket.send_text(json.dumps({"type": "ping"}))
            websocket.receive_json()
    
    # Force garbage collection
    import gc
    gc.collect()
    
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    # Memory increase should be minimal after cleanup
    assert memory_increase < 10 * 1024 * 1024  # Less than 10MB increase 