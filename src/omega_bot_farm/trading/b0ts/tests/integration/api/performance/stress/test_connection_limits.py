
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
Tests for connection limits handling in the BitgetPositionAnalyzerB0t API.

These tests verify:
- The API correctly handles connection limit scenarios
- Connection pooling works effectively under load
- Connection timeouts are handled gracefully
- The system recovers after hitting connection limits
- Error responses are appropriate when limits are exceeded
"""

import asyncio
import time
import pytest
import aiohttp
import logging
import random
import json
from typing import List, Dict, Any, Tuple
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Test configuration
TEST_CONFIG = {
    "max_connections_to_test": [50, 100, 200, 500],  # Different connection limits to test
    "api_endpoint": "/api/v1/position-analysis",  # API endpoint to test
    "request_interval_ms": 100,  # Time between requests in milliseconds
    "request_timeout_seconds": 10,  # Maximum time to wait for a response
    "test_duration_seconds": 20,  # How long to run each test scenario
    "recovery_wait_seconds": 5,  # Time to wait for system recovery
    "test_host": "http://localhost:8080",  # Default test host
    "max_concurrent_conns_expected": 256,  # Expected max concurrent connections the server supports
}

# Try to import the real implementation for direct testing, fall back to mock testing
try:
    from omega_bot_farm.trading.b0ts.bitget_analyzer.api.server import get_server_connection_limits
    REAL_IMPLEMENTATION = True
except ImportError:
    REAL_IMPLEMENTATION = False
    
    def get_server_connection_limits():
        """Mock function to return server connection limits."""
        return {
            "max_connections": TEST_CONFIG["max_concurrent_conns_expected"],
            "backlog_size": 64,
            "keepalive_timeout": 75.0
        }


class ConnectionStats:
    """Statistics for connection testing."""
    
    def __init__(self):
        """Initialize the connection stats."""
        self.total_attempts = 0
        self.success_count = 0
        self.error_count = 0
        self.timeout_count = 0
        self.connection_errors = 0
        self.start_time = None
        self.end_time = None
        self.status_codes = {}
        self.response_times = []
        self.connection_errors_by_type = {}
        
    def record_attempt(self):
        """Record a connection attempt."""
        self.total_attempts += 1
        
    def record_success(self, status_code: int, response_time: float):
        """Record a successful connection."""
        self.success_count += 1
        self.response_times.append(response_time)
        
        if status_code in self.status_codes:
            self.status_codes[status_code] += 1
        else:
            self.status_codes[status_code] = 1
    
    def record_error(self, status_code: int, response_time: float):
        """Record an error response."""
        self.error_count += 1
        self.response_times.append(response_time)
        
        if status_code in self.status_codes:
            self.status_codes[status_code] += 1
        else:
            self.status_codes[status_code] = 1
    
    def record_timeout(self):
        """Record a timeout."""
        self.timeout_count += 1
    
    def record_connection_error(self, error_type: str):
        """Record a connection error."""
        self.connection_errors += 1
        
        if error_type in self.connection_errors_by_type:
            self.connection_errors_by_type[error_type] += 1
        else:
            self.connection_errors_by_type[error_type] = 1
    
    def start(self):
        """Mark the start time."""
        self.start_time = time.time()
    
    def end(self):
        """Mark the end time."""
        self.end_time = time.time()
    
    @property
    def duration(self) -> float:
        """Get the test duration in seconds."""
        if self.start_time is None or self.end_time is None:
            return 0.0
        return self.end_time - self.start_time
    
    @property
    def error_rate(self) -> float:
        """Get the error rate as a percentage."""
        if self.total_attempts == 0:
            return 0.0
        return (self.error_count / self.total_attempts) * 100
    
    @property
    def connection_error_rate(self) -> float:
        """Get the connection error rate as a percentage."""
        if self.total_attempts == 0:
            return 0.0
        return (self.connection_errors / self.total_attempts) * 100
    
    @property
    def timeout_rate(self) -> float:
        """Get the timeout rate as a percentage."""
        if self.total_attempts == 0:
            return 0.0
        return (self.timeout_count / self.total_attempts) * 100
    
    @property
    def success_rate(self) -> float:
        """Get the success rate as a percentage."""
        if self.total_attempts == 0:
            return 0.0
        return (self.success_count / self.total_attempts) * 100
    
    @property
    def attempts_per_second(self) -> float:
        """Get the attempts per second."""
        if self.duration == 0:
            return 0.0
        return self.total_attempts / self.duration
    
    @property
    def mean_response_time(self) -> float:
        """Get the mean response time in seconds."""
        if not self.response_times:
            return 0.0
        return sum(self.response_times) / len(self.response_times)
    
    def summary(self) -> str:
        """Get a summary of the connection stats."""
        summary_lines = [
            "Connection Limits Test Results",
            "-----------------------------",
            f"Test Duration: {self.duration:.2f} seconds",
            f"Total Connection Attempts: {self.total_attempts}",
            f"Attempts Per Second: {self.attempts_per_second:.2f}",
            f"Success Rate: {self.success_rate:.2f}%",
            f"Error Rate: {self.error_rate:.2f}%",
            f"Connection Error Rate: {self.connection_error_rate:.2f}%",
            f"Timeout Rate: {self.timeout_rate:.2f}%",
            f"Mean Response Time: {self.mean_response_time:.4f} seconds",
        ]
        
        # Add status code breakdown
        if self.status_codes:
            summary_lines.append("Status Code Breakdown:")
            for code, count in sorted(self.status_codes.items()):
                summary_lines.append(f"  {code}: {count} ({count/self.total_attempts*100:.1f}%)")
        
        # Add connection error breakdown
        if self.connection_errors_by_type:
            summary_lines.append("Connection Error Breakdown:")
            for error_type, count in sorted(self.connection_errors_by_type.items()):
                summary_lines.append(f"  {error_type}: {count} ({count/self.connection_errors*100:.1f}%)")
        
        return "\n".join(summary_lines)


async def make_single_request(session: aiohttp.ClientSession, url: str, stats: ConnectionStats):
    """Make a single request to the API and record the results.
    
    Args:
        session: The aiohttp session to use
        url: The URL to connect to
        stats: The stats object to update
    """
    stats.record_attempt()
    start_time = time.time()
    
    # Generate a random payload
    payload = {
        "userId": f"user_{random.randint(1, 1000)}",
        "timestamp": time.time(),
        "symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT"],
        "requestId": f"req_{int(time.time() * 1000)}"
    }
    
    try:
        async with session.post(url, json=payload, timeout=TEST_CONFIG["request_timeout_seconds"]) as response:
            response_time = time.time() - start_time
            status_code = response.status
            
            # Read the response to ensure the request is complete
            await response.text()
            
            if 200 <= status_code < 300:
                stats.record_success(status_code, response_time)
            else:
                stats.record_error(status_code, response_time)
                
    except asyncio.TimeoutError:
        stats.record_timeout()
        logger.warning(f"Request timed out after {TEST_CONFIG['request_timeout_seconds']} seconds")
    except aiohttp.ClientConnectorError as e:
        stats.record_connection_error("ClientConnectorError")
        logger.warning(f"Connection error: {str(e)}")
    except aiohttp.ClientOSError as e:
        stats.record_connection_error("ClientOSError")
        logger.warning(f"OS error: {str(e)}")
    except aiohttp.ServerDisconnectedError as e:
        stats.record_connection_error("ServerDisconnectedError")
        logger.warning(f"Server disconnected: {str(e)}")
    except Exception as e:
        stats.record_connection_error(type(e).__name__)
        logger.warning(f"Request failed: {str(e)}")


@asynccontextmanager
async def connection_pool(max_connections: int):
    """Create a connection pool with specific limits.
    
    Args:
        max_connections: The maximum number of connections to allow
        
    Yields:
        The aiohttp ClientSession with the configured connection pool
    """
    # Configure a TCP connector with the specified limits
    connector = aiohttp.TCPConnector(
        limit=max_connections,
        limit_per_host=max_connections,
        force_close=False,
        enable_cleanup_closed=True
    )
    
    # Create a session with the connector
    session = aiohttp.ClientSession(connector=connector)
    
    try:
        yield session
    finally:
        await session.close()


async def run_connection_limit_test(num_connections: int, url: str, duration: float) -> ConnectionStats:
    """Run a test that attempts to establish a specific number of connections.
    
    Args:
        num_connections: The number of connections to attempt
        url: The URL to connect to
        duration: How long to run the test in seconds
        
    Returns:
        The connection statistics
    """
    logger.info(f"Starting connection limit test with {num_connections} connections")
    
    stats = ConnectionStats()
    stats.start()
    
    # Use slightly more connections than we expect to be able to handle
    pool_size = min(num_connections * 2, 1000)  # Cap at 1000 to avoid excessive resource use
    
    async with connection_pool(pool_size) as session:
        end_time = time.time() + duration
        tasks = []
        
        # Create tasks to continuously make requests until the test duration expires
        while time.time() < end_time:
            # Create a batch of requests
            batch_size = min(num_connections, 50)  # Process in manageable batches
            
            for _ in range(batch_size):
                task = asyncio.create_task(make_single_request(session, url, stats))
                tasks.append(task)
            
            # Wait for all tasks in the batch to complete
            if tasks:
                await asyncio.gather(*tasks)
                tasks = []
            
            # Add a small delay to avoid completely overwhelming the server
            await asyncio.sleep(TEST_CONFIG["request_interval_ms"] / 1000)
    
    stats.end()
    logger.info(f"Connection limit test completed: {stats.total_attempts} attempts, {stats.success_rate:.2f}% success rate")
    
    return stats


async def test_recovery_after_limit(url: str) -> bool:
    """Test if the API recovers after hitting connection limits.
    
    Args:
        url: The URL to test
        
    Returns:
        True if the API recovers successfully
    """
    logger.info("Testing recovery after connection limits...")
    
    # First, get the server connection limits
    server_limits = get_server_connection_limits()
    max_connections = server_limits.get("max_connections", TEST_CONFIG["max_concurrent_conns_expected"])
    
    # Try to exceed connection limits
    exceed_connections = max_connections * 2
    await run_connection_limit_test(exceed_connections, url, 5.0)
    
    # Wait for recovery
    logger.info(f"Waiting {TEST_CONFIG['recovery_wait_seconds']} seconds for recovery...")
    await asyncio.sleep(TEST_CONFIG['recovery_wait_seconds'])
    
    # Test if the server has recovered
    recovery_stats = ConnectionStats()
    recovery_stats.start()
    
    async with aiohttp.ClientSession() as session:
        # Make a few simple requests
        for _ in range(5):
            await make_single_request(session, url, recovery_stats)
            await asyncio.sleep(0.5)
    
    recovery_stats.end()
    
    # Check if the recovery was successful
    recovery_success = recovery_stats.success_rate > 80.0
    logger.info(f"Recovery test: {recovery_stats.success_rate:.2f}% success rate")
    
    return recovery_success


def mock_api_server(host="localhost", port=8080, connection_limit=256):
    """Start a mock API server for testing if real implementation is not available."""
    import threading
    import socket
    from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
    
    class MockApiHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Simulate processing time
            time.sleep(0.05)  # Base latency
            
            # Parse the request data
            try:
                request_data = json.loads(post_data.decode('utf-8'))
                
                # Prepare a mock response
                response = {
                    "status": "success",
                    "requestId": request_data.get("requestId", ""),
                    "timestamp": time.time(),
                    "data": {
                        "positions": [
                            {"symbol": "BTCUSDT", "score": 0.85, "recommendation": "HOLD"},
                            {"symbol": "ETHUSDT", "score": 0.72, "recommendation": "REDUCE"},
                            {"symbol": "SOLUSDT", "score": 0.91, "recommendation": "INCREASE"}
                        ],
                        "overallHarmony": 0.83
                    }
                }
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_response = {"status": "error", "message": str(e)}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    class LimitedThreadingHTTPServer(ThreadingHTTPServer):
        def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
            """Initialize the HTTP server with a connection limit."""
            ThreadingHTTPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Track active connections to enforce the limit
            self.active_connections = 0
            self.max_connections = connection_limit
            self._connection_lock = threading.Lock()
        
        def process_request(self, request, client_address):
            """Process a request with connection limiting."""
            with self._connection_lock:
                if self.active_connections >= self.max_connections:
                    logger.warning(f"Connection limit reached ({self.active_connections}/{self.max_connections})")
                    try:
                        request.close()
                    except:
                        pass
                    return
                self.active_connections += 1
            
            try:
                ThreadingHTTPServer.process_request(self, request, client_address)
            finally:
                with self._connection_lock:
                    self.active_connections -= 1
    
    server = LimitedThreadingHTTPServer((host, port), MockApiHandler)
    server.max_connections = connection_limit
    
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    
    logger.info(f"Started mock API server at http://{host}:{port} with connection limit {connection_limit}")
    return server


@pytest.fixture(scope="module")
def api_server():
    """Start an API server for testing."""
    # Get server limits
    limits = get_server_connection_limits()
    max_connections = limits.get("max_connections", TEST_CONFIG["max_concurrent_conns_expected"])
    
    if REAL_IMPLEMENTATION:
        try:
            from omega_bot_farm.trading.b0ts.bitget_analyzer.api.server import start_api_server
            server = start_api_server(test_mode=True)
        except ImportError:
            server = mock_api_server(connection_limit=max_connections)
    else:
        server = mock_api_server(connection_limit=max_connections)
        
    yield server
    
    # Clean up
    if not REAL_IMPLEMENTATION:
        server.shutdown()


class TestConnectionLimits:
    """Test suite for API connection limits."""
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("connection_count", TEST_CONFIG["max_connections_to_test"])
    async def test_connection_handling(self, api_server, connection_count):
        """Test the API's ability to handle different connection loads."""
        api_url = f"{TEST_CONFIG['test_host']}{TEST_CONFIG['api_endpoint']}"
        
        # Run the test
        stats = await run_connection_limit_test(
            connection_count,
            api_url,
            TEST_CONFIG["test_duration_seconds"]
        )
        
        logger.info(stats.summary())
        
        # Get server connection limits for context
        server_limits = get_server_connection_limits()
        max_connections = server_limits.get("max_connections", TEST_CONFIG["max_concurrent_conns_expected"])
        
        # Assertions based on the connection count relative to the server limit
        if connection_count <= max_connections:
            # If we're below the limit, expect high success rate
            assert stats.success_rate > 90.0, f"Success rate {stats.success_rate:.2f}% is too low for {connection_count} connections"
            assert stats.connection_error_rate < 5.0, f"Connection error rate {stats.connection_error_rate:.2f}% is too high"
        else:
            # If we're above the limit, we expect some errors, but the API should still function
            assert stats.success_rate > 30.0, f"Success rate {stats.success_rate:.2f}% is too low even for over-limit connections"
            
            # We should see connection errors as we hit the limit
            assert stats.connection_error_rate > 0.0, f"No connection errors detected when exceeding connection limit"
            
            # Server shouldn't completely crash
            assert stats.timeout_rate < 50.0, f"Timeout rate {stats.timeout_rate:.2f}% is too high"
    
    @pytest.mark.asyncio
    async def test_recovery_from_connection_limit(self, api_server):
        """Test that the API recovers after hitting connection limits."""
        api_url = f"{TEST_CONFIG['test_host']}{TEST_CONFIG['api_endpoint']}"
        
        # Test recovery
        recovery_successful = await test_recovery_after_limit(api_url)
        assert recovery_successful, "API failed to recover after hitting connection limits"
    
    @pytest.mark.asyncio
    async def test_connection_timeout_handling(self, api_server):
        """Test the API's handling of connection timeouts."""
        api_url = f"{TEST_CONFIG['test_host']}{TEST_CONFIG['api_endpoint']}"
        
        # Create a session with a very short timeout
        stats = ConnectionStats()
        stats.start()
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=0.1)) as session:
            # Make several requests with an unrealistically short timeout
            for _ in range(10):
                await make_single_request(session, api_url, stats)
        
        stats.end()
        logger.info(stats.summary())
        
        # We expect most of these to timeout
        assert stats.timeout_rate > 50.0, f"Expected high timeout rate, got {stats.timeout_rate:.2f}%"
        
        # But the API should still be responsive after these timeouts
        recovery_stats = ConnectionStats()
        recovery_stats.start()
        
        async with aiohttp.ClientSession() as session:
            # Make a few requests with normal timeout
            for _ in range(5):
                await make_single_request(session, api_url, recovery_stats)
                await asyncio.sleep(0.5)
        
        recovery_stats.end()
        
        # The API should be responsive after timeout tests
        assert recovery_stats.success_rate > 80.0, f"API not responsive after timeout tests"


if __name__ == "__main__":
    # This allows the test to be run directly for debugging
    asyncio.run(run_connection_limit_test(
        100,  # 100 connections
        f"http://localhost:8080{TEST_CONFIG['api_endpoint']}",
        10.0  # 10 seconds duration
    )) 