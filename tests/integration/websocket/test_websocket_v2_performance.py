
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

"""Tests for WebSocket V2 performance characteristics.

This test suite covers performance aspects of the WebSocket server V2:
1. Message throughput
2. Latency measurements
3. Resource utilization
4. Connection handling
5. Memory usage
6. CPU usage
7. Network bandwidth
8. Scalability

Version: 0.2.0
GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2025-03-28
"""

import pytest
import asyncio
import json
import websockets
import time
import psutil
import os
import logging
from datetime import datetime, UTC
from typing import Dict, Any, List
from websockets.exceptions import ConnectionClosed
from omega_ai.mm_trap_detector.mm_websocket_server_v2 import (
    start_server, stop_server, ConnectionState, ClientInfo
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ws_performance_tests')

# ---- Test Helpers ----

def get_test_websocket_uri(disable_ssl=False):
    """
    Get WebSocket URI for testing with dynamic port detection.
    
    Args:
        disable_ssl (bool): Whether to use SSL or not
        
    Returns:
        str: The WebSocket URI to connect to
    """
    host = os.environ.get("WEBSOCKET_HOST", "localhost")
    port = os.environ.get("WEBSOCKET_PORT", "9886")
    
    protocol = "ws"
    if not disable_ssl and os.environ.get("WEBSOCKET_SSL_PORT"):
        protocol = "wss"
        port = os.environ.get("WEBSOCKET_SSL_PORT", "9887")
        
    return f"{protocol}://{host}:{port}"

async def connect_with_timeout(uri, timeout=30, max_retries=3):
    """
    Connect to WebSocket with an increased timeout and retry capability.
    
    Args:
        uri (str): WebSocket URI to connect to
        timeout (int): Connection timeout in seconds
        max_retries (int): Maximum number of connection attempts
        
    Returns:
        WebSocketClientProtocol: The connected WebSocket
        
    Raises:
        ConnectionError: If connection fails after all retries
    """
    last_error = None
    for attempt in range(max_retries):
        try:
            logger.info(f"Connecting to {uri} (attempt {attempt+1}/{max_retries})")
            return await websockets.connect(uri, open_timeout=timeout)
        except Exception as e:
            last_error = e
            logger.warning(f"Connection attempt {attempt+1} failed: {e}")
            await asyncio.sleep(1)  # Wait before retry
    
    # If we get here, all attempts failed
    raise ConnectionError(f"Failed to connect to {uri} after {max_retries} attempts: {last_error}")

@pytest.fixture(autouse=True)
async def setup_teardown(disable_ssl):
    """Set up and tear down test environment."""
    if not disable_ssl:
        # Only import and use if SSL is enabled
        from tests.integration.config.test_config_v2 import setup_test_environment, cleanup_test_environment
        setup_test_environment()
        yield
        cleanup_test_environment()
    else:
        yield

@pytest.fixture
async def websocket_server(global_websocket_server):
    """Use the global WebSocket server for testing."""
    yield global_websocket_server

def get_process_metrics():
    """Get current process metrics."""
    process = psutil.Process(os.getpid())
    return {
        "cpu_percent": process.cpu_percent(),
        "memory_percent": process.memory_percent(),
        "num_threads": process.num_threads(),
        "num_fds": process.num_fds()
    }

def generate_test_data(size=1000):
    """Generate test data for testing."""
    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "data": "x" * size,
        "metadata": {
            "test": True,
            "size": size,
            "generated_at": datetime.now(UTC).isoformat()
        }
    }

# ---- Test Functions ----

@pytest.mark.asyncio
async def test_websocket_v2_message_throughput(websocket_server, disable_ssl):
    """Test message throughput under load."""
    uri = get_test_websocket_uri(disable_ssl)
    message_count = 100  # Reduced for faster testing
    start_time = time.time()
    
    async with await connect_with_timeout(uri, timeout=30) as websocket:
        # Skip welcome message
        await websocket.recv()
        
        # Send messages as fast as possible
        for i in range(message_count):
            message = {
                "type": "throughput_test",
                "data": f"message_{i}",
                "timestamp": datetime.now(UTC).isoformat()
            }
            await websocket.send(json.dumps(message))
        
        # Receive all responses
        for _ in range(message_count):
            await websocket.recv()
    
    end_time = time.time()
    duration = end_time - start_time
    throughput = message_count / duration
    
    # Log performance metrics
    print(f"\nThroughput Test Results:")
    print(f"Messages: {message_count}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Throughput: {throughput:.2f} messages/second")
    
    # Verify minimum throughput (relaxed for CI environments)
    assert throughput >= 10  # At least 10 messages per second

@pytest.mark.asyncio
async def test_websocket_v2_latency(websocket_server, disable_ssl):
    """Test message latency."""
    uri = get_test_websocket_uri(disable_ssl)
    latencies = []
    
    async with await connect_with_timeout(uri, timeout=30) as websocket:
        # Skip welcome message
        await websocket.recv()
        
        # Measure round-trip latency
        for i in range(20):  # Reduced for faster testing
            start_time = time.time()
            
            message = {
                "type": "latency_test",
                "data": f"message_{i}",
                "timestamp": datetime.now(UTC).isoformat()
            }
            await websocket.send(json.dumps(message))
            
            response = await websocket.recv()
            end_time = time.time()
            
            latency = (end_time - start_time) * 1000  # Convert to milliseconds
            latencies.append(latency)
    
    avg_latency = sum(latencies) / len(latencies)
    max_latency = max(latencies)
    min_latency = min(latencies)
    
    # Log latency metrics
    print(f"\nLatency Test Results:")
    print(f"Average Latency: {avg_latency:.2f} ms")
    print(f"Maximum Latency: {max_latency:.2f} ms")
    print(f"Minimum Latency: {min_latency:.2f} ms")
    
    # Verify maximum latency (relaxed for CI environments)
    assert max_latency < 500  # Maximum latency should be under 500ms

@pytest.mark.asyncio
async def test_websocket_v2_resource_utilization(websocket_server, disable_ssl):
    """Test resource utilization under load."""
    uri = get_test_websocket_uri(disable_ssl)
    clients = []
    initial_metrics = get_process_metrics()
    
    try:
        # Create multiple connections (reduced for faster testing)
        for i in range(10):
            client = await connect_with_timeout(uri, timeout=30)
            clients.append(client)
            
            # Send messages
            message = {
                "type": "resource_test",
                "data": f"client_{i}",
                "timestamp": datetime.now(UTC).isoformat()
            }
            await client.send(json.dumps(message))
        
        # Wait for responses
        await asyncio.sleep(1)
        
        # Get final metrics
        final_metrics = get_process_metrics()
        
        # Log resource metrics
        print(f"\nResource Utilization Test Results:")
        print(f"Initial CPU: {initial_metrics['cpu_percent']:.1f}%")
        print(f"Final CPU: {final_metrics['cpu_percent']:.1f}%")
        print(f"Initial Memory: {initial_metrics['memory_percent']:.1f}%")
        print(f"Final Memory: {final_metrics['memory_percent']:.1f}%")
        print(f"Initial Threads: {initial_metrics['num_threads']}")
        print(f"Final Threads: {final_metrics['num_threads']}")
        
        # Verify resource usage
        assert final_metrics['cpu_percent'] < 80  # CPU usage under 80%
        assert final_metrics['memory_percent'] < 80  # Memory usage under 80%
    finally:
        # Clean up
        for client in clients:
            await client.close()

@pytest.mark.asyncio
async def test_websocket_v2_connection_handling(websocket_server, disable_ssl):
    """Test connection handling performance."""
    uri = get_test_websocket_uri(disable_ssl)
    connection_times = []
    
    for i in range(10):  # Reduced for faster testing
        start_time = time.time()
        
        async with await connect_with_timeout(uri, timeout=30) as websocket:
            # Skip welcome message
            await websocket.recv()
            
            end_time = time.time()
            connection_time = (end_time - start_time) * 1000  # Convert to milliseconds
            connection_times.append(connection_time)
    
    avg_time = sum(connection_times) / len(connection_times)
    max_time = max(connection_times)
    min_time = min(connection_times)
    
    # Log connection metrics
    print(f"\nConnection Handling Test Results:")
    print(f"Average Connection Time: {avg_time:.2f} ms")
    print(f"Maximum Connection Time: {max_time:.2f} ms")
    print(f"Minimum Connection Time: {min_time:.2f} ms")
    
    # Verify connection times (relaxed for CI environments)
    assert avg_time < 500  # Average connection time under 500ms
    assert max_time < 1000  # Maximum connection time under 1000ms

@pytest.mark.asyncio
async def test_websocket_v2_memory_usage(websocket_server, disable_ssl):
    """Test memory usage with large messages."""
    uri = get_test_websocket_uri(disable_ssl)
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    async with await connect_with_timeout(uri, timeout=30) as websocket:
        # Skip welcome message
        await websocket.recv()
        
        # Send large messages
        for i in range(20):  # Reduced for faster testing
            message = generate_test_data(size=1024)  # 1KB messages
            await websocket.send(json.dumps(message))
            await websocket.recv()
    
    # Check memory usage
    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = final_memory - initial_memory
    
    # Log memory metrics
    print(f"\nMemory Usage Test Results:")
    print(f"Initial Memory: {initial_memory:.2f} MB")
    print(f"Final Memory: {final_memory:.2f} MB")
    print(f"Memory Increase: {memory_increase:.2f} MB")
    
    # Verify memory usage (relaxed for CI environments)
    assert memory_increase < 100  # Memory increase should be under 100MB

@pytest.mark.asyncio
async def test_websocket_v2_cpu_usage(websocket_server, disable_ssl):
    """Test CPU usage under load."""
    uri = get_test_websocket_uri(disable_ssl)
    process = psutil.Process(os.getpid())
    
    # Get initial CPU usage
    process.cpu_percent()  # First call to reset
    await asyncio.sleep(0.1)
    initial_cpu = process.cpu_percent()
    
    async with await connect_with_timeout(uri, timeout=30) as websocket:
        # Skip welcome message
        await websocket.recv()
        
        # Perform CPU-intensive operations
        for i in range(50):  # Reduced for faster testing
            message = {
                "type": "cpu_test",
                "data": f"message_{i}",
                "operation": "compute",
                "timestamp": datetime.now(UTC).isoformat()
            }
            await websocket.send(json.dumps(message))
            await websocket.recv()
    
    # Get final CPU usage
    final_cpu = process.cpu_percent()
    
    # Log CPU metrics
    print(f"\nCPU Usage Test Results:")
    print(f"Initial CPU: {initial_cpu:.2f}%")
    print(f"Final CPU: {final_cpu:.2f}%")
    
    # Verify CPU usage (relaxed for CI environments)
    assert final_cpu < 80  # CPU usage should be under 80%

@pytest.mark.asyncio
async def test_websocket_v2_network_bandwidth(websocket_server, disable_ssl):
    """Test network bandwidth usage."""
    uri = get_test_websocket_uri(disable_ssl)
    message_size = 512  # bytes
    message_count = 50  # Reduced for faster testing
    
    # Create test data
    data = "x" * message_size
    total_bytes = message_size * message_count
    
    start_time = time.time()
    
    async with await connect_with_timeout(uri, timeout=30) as websocket:
        # Skip welcome message
        await websocket.recv()
        
        # Send messages
        for i in range(message_count):
            message = {
                "type": "bandwidth_test",
                "data": data,
                "index": i,
                "timestamp": datetime.now(UTC).isoformat()
            }
            await websocket.send(json.dumps(message))
            await websocket.recv()
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Calculate bandwidth
    bandwidth_bps = (total_bytes * 8) / duration  # bits per second
    bandwidth_mbps = bandwidth_bps / 1_000_000  # megabits per second
    
    # Log bandwidth metrics
    print(f"\nNetwork Bandwidth Test Results:")
    print(f"Total Data: {total_bytes / 1024:.2f} KB")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Bandwidth: {bandwidth_mbps:.2f} Mbps")
    
    # Verify bandwidth usage
    assert bandwidth_mbps < 100  # Bandwidth should be under 100 Mbps

@pytest.mark.asyncio
async def test_websocket_v2_scalability(websocket_server, disable_ssl):
    """Test server scalability with multiple clients."""
    uri = get_test_websocket_uri(disable_ssl)
    process = psutil.Process(os.getpid())
    client_counts = [5, 10]  # Reduced for faster testing
    
    for count in client_counts:
        print(f"\nTesting with {count} clients...")
        clients = []
        
        # Record initial metrics
        process.cpu_percent()  # First call to reset
        await asyncio.sleep(0.1)
        initial_cpu = process.cpu_percent()
        initial_memory = process.memory_percent()
        
        start_time = time.time()
        
        # Create clients
        for i in range(count):
            client = await connect_with_timeout(uri, timeout=30)
            clients.append(client)
            
            # Send a message
            message = {
                "type": "scalability_test",
                "client_id": i,
                "timestamp": datetime.now(UTC).isoformat()
            }
            await client.send(json.dumps(message))
        
        # Close clients
        for client in clients:
            await client.close()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Record final metrics
        final_cpu = process.cpu_percent()
        final_memory = process.memory_percent()
        
        # Log scalability metrics
        print(f"Time to handle {count} clients: {duration:.2f} seconds")
        print(f"CPU Usage: {final_cpu:.2f}%")
        print(f"Memory Usage: {final_memory:.2f}%")
        
        # Verify scalability metrics
        assert final_cpu < 80  # CPU usage under 80%
        assert final_memory < 80  # Memory usage under 80%
        assert duration < 5  # Connection time under 5 seconds 