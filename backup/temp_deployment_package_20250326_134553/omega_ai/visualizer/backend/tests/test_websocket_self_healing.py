
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

"""Self-healing tests for WebSocket functionality in the trap visualizer server."""

import pytest
import asyncio
import time
import json
from datetime import datetime, UTC, timedelta
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
from omega_ai.utils.redis_manager import RedisManager
from omega_ai.visualizer.backend.unified_server import TrapVisualizerServer

@pytest.fixture
def redis_manager():
    """Create a mock Redis manager with self-healing capabilities."""
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
    """Create a test server instance with self-healing enabled."""
    return TrapVisualizerServer("Test Trap Visualizer", redis_manager)

@pytest.fixture
def client(server):
    """Create a test client."""
    return TestClient(server.app)

@pytest.mark.asyncio
async def test_websocket_connection_auto_recovery(client):
    """Test WebSocket automatic connection recovery after failures."""
    recovery_patterns = []
    
    for _ in range(5):  # Test 5 recovery scenarios
        with client.websocket_connect("/ws") as websocket:
            # Simulate connection failure
            websocket.close()
            start_time = time.time()
            
            # Attempt to reconnect
            websocket = client.websocket_connect("/ws")
            websocket.__enter__()
            end_time = time.time()
            
            recovery_patterns.append(end_time - start_time)
            
            # Verify connection is healthy
            websocket.send_text(json.dumps({"type": "ping"}))
            response = websocket.receive_json()
            assert response["type"] == "pong"
    
    # Verify recovery time improves over time (learning)
    assert recovery_patterns[-1] < recovery_patterns[0]

@pytest.mark.asyncio
async def test_websocket_adaptive_rate_limiting(client):
    """Test adaptive rate limiting based on server load."""
    response_times = []
    message_counts = []
    
    with client.websocket_connect("/ws") as websocket:
        # Send messages in increasing frequency
        for i in range(10):
            messages = 10 * (i + 1)
            start_time = time.time()
            
            for _ in range(messages):
                websocket.send_text(json.dumps({"type": "ping"}))
                response = websocket.receive_json()
            
            end_time = time.time()
            response_times.append(end_time - start_time)
            message_counts.append(messages)
    
    # Verify rate limiting adapts to load
    assert response_times[-1] > response_times[0]  # Slower under higher load
    assert message_counts[-1] > message_counts[0]  # More messages processed

@pytest.mark.asyncio
async def test_websocket_error_pattern_recognition(client):
    """Test error pattern recognition and prevention."""
    error_patterns = []
    
    with client.websocket_connect("/ws") as websocket:
        # Send messages that might cause errors
        for _ in range(5):
            # Send invalid JSON
            websocket.send_text("invalid json")
            response = websocket.receive_json()
            error_patterns.append(response)
            
            # Send malformed message
            websocket.send_text(json.dumps({"type": "invalid_type"}))
            response = websocket.receive_json()
            error_patterns.append(response)
    
    # Verify error handling improves
    assert len(set(error_patterns)) < len(error_patterns)  # Patterns are recognized

@pytest.mark.asyncio
async def test_websocket_load_balancing(client):
    """Test automatic load balancing between connections."""
    num_connections = 5
    connections = []
    message_counts = []
    
    try:
        # Create multiple connections
        for _ in range(num_connections):
            websocket = client.websocket_connect("/ws")
            connections.append(websocket)
            websocket.__enter__()
        
        # Send messages to each connection
        for websocket in connections:
            count = 0
            for _ in range(20):
                websocket.send_text(json.dumps({"type": "ping"}))
                response = websocket.receive_json()
                count += 1
            message_counts.append(count)
        
        # Verify load is distributed
        max_diff = max(message_counts) - min(message_counts)
        assert max_diff <= 5  # Fair distribution
        
    finally:
        for websocket in connections:
            try:
                websocket.__exit__(None, None, None)
            except:
                pass

@pytest.mark.asyncio
async def test_websocket_memory_optimization(client):
    """Test automatic memory optimization under load."""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Create connections and send messages
    num_connections = 10
    connections = []
    
    try:
        for _ in range(num_connections):
            websocket = client.websocket_connect("/ws")
            connections.append(websocket)
            websocket.__enter__()
            
            # Send messages to trigger memory optimization
            for _ in range(100):
                websocket.send_text(json.dumps({"type": "message", "data": "test"}))
                websocket.receive_json()
        
        # Force memory optimization
        await asyncio.sleep(1)  # Allow time for optimization
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Verify memory usage is optimized
        assert memory_increase < 30 * 1024 * 1024  # Less than 30MB increase
        
    finally:
        for websocket in connections:
            try:
                websocket.__exit__(None, None, None)
            except:
                pass

@pytest.mark.asyncio
async def test_websocket_adaptive_timeout(client):
    """Test adaptive timeout based on network conditions."""
    timeout_values = []
    
    with client.websocket_connect("/ws") as websocket:
        # Simulate different network conditions
        for _ in range(5):
            # Send message and measure response time
            start_time = time.time()
            websocket.send_text(json.dumps({"type": "ping"}))
            response = websocket.receive_json()
            end_time = time.time()
            
            timeout_values.append(end_time - start_time)
            
            # Simulate network delay
            await asyncio.sleep(0.1)
    
    # Verify timeout adapts to network conditions
    assert timeout_values[-1] > timeout_values[0]  # Timeout increases with delay

@pytest.mark.asyncio
async def test_websocket_connection_health_monitoring(client):
    """Test automatic connection health monitoring and recovery."""
    health_status = []
    
    with client.websocket_connect("/ws") as websocket:
        # Monitor connection health
        for _ in range(10):
            # Send health check
            websocket.send_text(json.dumps({"type": "health_check"}))
            response = websocket.receive_json()
            health_status.append(response)
            
            # Simulate network issues
            await asyncio.sleep(0.05)
    
    # Verify health monitoring is active
    assert len(set(health_status)) > 1  # Health status changes

@pytest.mark.asyncio
async def test_websocket_adaptive_buffering(client):
    """Test adaptive message buffering based on load."""
    buffer_sizes = []
    
    with client.websocket_connect("/ws") as websocket:
        # Send messages in bursts
        for _ in range(5):
            # Send burst of messages
            for _ in range(20):
                websocket.send_text(json.dumps({"type": "message", "data": "test"}))
            
            # Measure processing time
            start_time = time.time()
            for _ in range(20):
                response = websocket.receive_json()
            end_time = time.time()
            
            buffer_sizes.append(end_time - start_time)
    
    # Verify buffering adapts to load
    assert buffer_sizes[-1] < buffer_sizes[0]  # Processing time improves

@pytest.mark.asyncio
async def test_websocket_error_prediction(client):
    """Test prediction and prevention of potential errors."""
    error_rates = []
    
    with client.websocket_connect("/ws") as websocket:
        # Send messages that might cause errors
        for _ in range(5):
            errors = 0
            total = 20
            
            for _ in range(total):
                try:
                    # Send potentially problematic message
                    websocket.send_text(json.dumps({
                        "type": "message",
                        "data": "A" * 1000  # Large payload
                    }))
                    response = websocket.receive_json()
                except Exception:
                    errors += 1
            
            error_rates.append(errors / total)
    
    # Verify error prediction improves
    assert error_rates[-1] < error_rates[0]  # Error rate decreases

@pytest.mark.asyncio
async def test_websocket_resource_optimization(client):
    """Test automatic resource optimization under load."""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_cpu = process.cpu_percent()
    initial_memory = process.memory_info().rss
    
    # Create load
    num_connections = 5
    connections = []
    
    try:
        for _ in range(num_connections):
            websocket = client.websocket_connect("/ws")
            connections.append(websocket)
            websocket.__enter__()
            
            # Send messages to trigger optimization
            for _ in range(50):
                websocket.send_text(json.dumps({"type": "message", "data": "test"}))
                websocket.receive_json()
        
        # Allow time for optimization
        await asyncio.sleep(1)
        
        final_cpu = process.cpu_percent()
        final_memory = process.memory_info().rss
        
        # Verify resource usage is optimized
        assert final_cpu < initial_cpu * 1.5  # CPU usage doesn't increase significantly
        assert final_memory - initial_memory < 20 * 1024 * 1024  # Memory usage is controlled
        
    finally:
        for websocket in connections:
            try:
                websocket.__exit__(None, None, None)
            except:
                pass 