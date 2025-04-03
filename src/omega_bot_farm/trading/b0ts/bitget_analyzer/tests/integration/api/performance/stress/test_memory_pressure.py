"""
Tests for memory pressure handling in the BitgetPositionAnalyzerB0t API.

These tests verify:
- The API handles large payloads and responses efficiently
- Memory usage remains stable under sustained load
- No memory leaks occur during extended operation
- Garbage collection functions correctly
- System behaves predictably under memory-constrained environments
"""

import asyncio
import time
import pytest
import aiohttp
import psutil
import logging
import json
import random
import string
from typing import Dict, List, Any, Tuple
import gc

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Test configuration
TEST_CONFIG = {
    "api_endpoint": "/api/v1/position-analysis",
    "test_duration_seconds": 30,
    "request_interval_ms": 100,
    "small_payload_size_kb": 1,
    "medium_payload_size_kb": 100,
    "large_payload_size_kb": 1000,
    "test_host": "http://localhost:8080",
    "max_memory_increase_percent": 20,  # Maximum acceptable memory increase
    "gc_check_interval_seconds": 5,     # How often to check memory usage
}

# Try to import the real implementation for direct testing, fall back to mock testing
try:
    from omega_bot_farm.trading.b0ts.bitget_analyzer.api.server import check_server_memory_usage
    REAL_IMPLEMENTATION = True
except ImportError:
    REAL_IMPLEMENTATION = False
    
    def check_server_memory_usage():
        """Mock function to check server memory usage."""
        process = psutil.Process()
        memory_info = process.memory_info()
        return {
            "rss": memory_info.rss,
            "vms": memory_info.vms,
            "percent": process.memory_percent(),
            "available": psutil.virtual_memory().available
        }


class MemoryTestResults:
    """Results of a memory pressure test."""
    
    def __init__(self):
        """Initialize the memory test results."""
        self.start_time = None
        self.end_time = None
        self.start_memory = None
        self.end_memory = None
        self.max_memory = None
        self.memory_samples = []
        self.request_count = 0
        self.success_count = 0
        self.error_count = 0
        self.payload_size = 0
        
    def start(self):
        """Start the test and record initial memory usage."""
        self.start_time = time.time()
        self.start_memory = check_server_memory_usage()
        self.max_memory = self.start_memory
        self.memory_samples.append((self.start_time, self.start_memory))
        
    def end(self):
        """End the test and record final memory usage."""
        self.end_time = time.time()
        self.end_memory = check_server_memory_usage()
        self.memory_samples.append((self.end_time, self.end_memory))
        
    def sample_memory(self):
        """Take a memory sample at the current time."""
        current_time = time.time()
        memory_usage = check_server_memory_usage()
        self.memory_samples.append((current_time, memory_usage))
        
        # Update max memory if current usage is higher
        if memory_usage["rss"] > self.max_memory["rss"]:
            self.max_memory = memory_usage
            
    def record_request(self, success: bool, payload_size: int):
        """Record a request result."""
        self.request_count += 1
        self.payload_size = payload_size
        
        if success:
            self.success_count += 1
        else:
            self.error_count += 1
            
    @property
    def duration(self) -> float:
        """Get the test duration in seconds."""
        if self.start_time is None or self.end_time is None:
            return 0.0
        return self.end_time - self.start_time
    
    @property
    def success_rate(self) -> float:
        """Get the success rate as a percentage."""
        if self.request_count == 0:
            return 0.0
        return (self.success_count / self.request_count) * 100
    
    @property
    def memory_growth_bytes(self) -> int:
        """Get the memory growth in bytes."""
        if self.start_memory is None or self.end_memory is None:
            return 0
        return self.end_memory["rss"] - self.start_memory["rss"]
    
    @property
    def memory_growth_percent(self) -> float:
        """Get the memory growth as a percentage."""
        if self.start_memory is None or self.end_memory is None or self.start_memory["rss"] == 0:
            return 0.0
        return (self.memory_growth_bytes / self.start_memory["rss"]) * 100
    
    @property
    def peak_memory_growth_percent(self) -> float:
        """Get the peak memory growth as a percentage."""
        if self.start_memory is None or self.max_memory is None or self.start_memory["rss"] == 0:
            return 0.0
        return ((self.max_memory["rss"] - self.start_memory["rss"]) / self.start_memory["rss"]) * 100
    
    @property
    def memory_per_request_kb(self) -> float:
        """Get the memory used per request in KB."""
        if self.request_count == 0 or self.memory_growth_bytes <= 0:
            return 0.0
        return (self.memory_growth_bytes / self.request_count) / 1024
    
    @property
    def requests_per_second(self) -> float:
        """Get the requests per second."""
        if self.duration == 0:
            return 0.0
        return self.request_count / self.duration
    
    def summary(self) -> str:
        """Get a summary of the memory test results."""
        summary_lines = [
            "Memory Pressure Test Results",
            "---------------------------",
            f"Test Duration: {self.duration:.2f} seconds",
            f"Payload Size: {self.payload_size / 1024:.2f} KB",
            f"Total Requests: {self.request_count}",
            f"Requests Per Second: {self.requests_per_second:.2f}",
            f"Success Rate: {self.success_rate:.2f}%",
            f"Initial Memory (RSS): {self.start_memory['rss'] / (1024 * 1024):.2f} MB",
            f"Final Memory (RSS): {self.end_memory['rss'] / (1024 * 1024):.2f} MB",
            f"Peak Memory (RSS): {self.max_memory['rss'] / (1024 * 1024):.2f} MB",
            f"Memory Growth: {self.memory_growth_bytes / (1024 * 1024):.2f} MB ({self.memory_growth_percent:.2f}%)",
            f"Peak Memory Growth: {(self.max_memory['rss'] - self.start_memory['rss']) / (1024 * 1024):.2f} MB ({self.peak_memory_growth_percent:.2f}%)",
            f"Memory Per Request: {self.memory_per_request_kb:.2f} KB"
        ]
        
        return "\n".join(summary_lines)


def generate_random_payload(size_kb: int) -> Dict[str, Any]:
    """Generate a random payload of approximately the specified size.
    
    Args:
        size_kb: The target size in kilobytes
        
    Returns:
        A dictionary with random data
    """
    # Base payload with required fields
    payload = {
        "userId": f"user_{random.randint(1, 1000)}",
        "timestamp": time.time(),
        "requestId": f"req_{int(time.time() * 1000)}",
        "symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT"],
    }
    
    # Calculate how many characters we need to reach the target size
    # Assuming 1 character is roughly 1 byte and accounting for JSON overhead
    target_bytes = size_kb * 1024
    current_size = len(json.dumps(payload).encode('utf-8'))
    remaining_bytes = max(0, target_bytes - current_size)
    
    # Generate random data to pad the payload
    if remaining_bytes > 0:
        # Add some structured data for realism
        positions = []
        
        # Each position entry is about 200-300 bytes
        num_positions = min(100, remaining_bytes // 250)
        
        for i in range(num_positions):
            position = {
                "symbol": f"COIN{i}USDT",
                "entryPrice": random.uniform(100, 50000),
                "markPrice": random.uniform(100, 50000),
                "size": random.uniform(0.01, 10.0),
                "side": "LONG" if random.random() > 0.5 else "SHORT",
                "leverage": random.randint(1, 100),
                "unrealizedPnl": random.uniform(-1000, 1000),
                "liquidationPrice": random.uniform(100, 50000),
                "marginType": "isolated" if random.random() > 0.5 else "cross",
                "updateTime": int(time.time() * 1000) - random.randint(0, 86400000)
            }
            positions.append(position)
            
        payload["positions"] = positions
        
        # If we still need more bytes, add a large string
        current_size = len(json.dumps(payload).encode('utf-8'))
        remaining_bytes = max(0, target_bytes - current_size)
        
        if remaining_bytes > 0:
            # Generate a random string to reach the target size
            random_string = ''.join(random.choice(string.ascii_letters) 
                                   for _ in range(remaining_bytes))
            payload["additionalData"] = random_string
    
    return payload


async def make_api_request(session: aiohttp.ClientSession, url: str, payload: Dict[str, Any]) -> Tuple[bool, int]:
    """Make a request to the API with the specified payload.
    
    Args:
        session: The aiohttp session to use
        url: The API endpoint URL
        payload: The request payload
        
    Returns:
        A tuple of (success, payload_size_bytes)
    """
    payload_json = json.dumps(payload)
    payload_size = len(payload_json.encode('utf-8'))
    
    try:
        async with session.post(url, json=payload, timeout=30) as response:
            # Read the response to ensure it's fully processed
            response_text = await response.text()
            
            # Consider any 2xx status as success
            success = 200 <= response.status < 300
            return success, payload_size
    except Exception as e:
        logger.warning(f"Request failed: {str(e)}")
        return False, payload_size


async def memory_monitor_task(test_results: MemoryTestResults, stop_event: asyncio.Event):
    """Monitor memory usage in a separate task.
    
    Args:
        test_results: The test results to update with memory samples
        stop_event: Event to signal when to stop monitoring
    """
    while not stop_event.is_set():
        # Sample memory usage
        test_results.sample_memory()
        
        # Wait for the next check interval
        await asyncio.sleep(TEST_CONFIG["gc_check_interval_seconds"])


async def run_memory_test(payload_size_kb: int, duration: float, url: str) -> MemoryTestResults:
    """Run a memory pressure test with the specified payload size.
    
    Args:
        payload_size_kb: The size of each request payload in kilobytes
        duration: How long to run the test in seconds
        url: The API endpoint URL
        
    Returns:
        The test results
    """
    logger.info(f"Starting memory pressure test with {payload_size_kb}KB payloads for {duration} seconds")
    
    # Perform garbage collection before test to establish a clean baseline
    gc.collect()
    
    # Initialize test results
    results = MemoryTestResults()
    results.start()
    
    # Start memory monitoring in a separate task
    stop_monitor = asyncio.Event()
    monitor_task = asyncio.create_task(memory_monitor_task(results, stop_monitor))
    
    # Prepare session for requests
    async with aiohttp.ClientSession() as session:
        end_time = time.time() + duration
        
        # Make requests until the test duration expires
        while time.time() < end_time:
            # Generate a random payload of the specified size
            payload = generate_random_payload(payload_size_kb)
            
            # Make the request
            success, payload_size = await make_api_request(session, url, payload)
            
            # Record the result
            results.record_request(success, payload_size)
            
            # Add a small delay between requests
            await asyncio.sleep(TEST_CONFIG["request_interval_ms"] / 1000)
    
    # Stop memory monitoring
    stop_monitor.set()
    await monitor_task
    
    # Perform garbage collection after test
    gc.collect()
    
    # Wait a moment for memory to stabilize
    await asyncio.sleep(1)
    
    # Finalize test results
    results.end()
    
    logger.info(f"Memory test completed: {results.request_count} requests, {results.memory_growth_percent:.2f}% memory growth")
    logger.info(results.summary())
    
    return results


def mock_api_server(host="localhost", port=8080):
    """Start a mock API server for testing memory pressure.
    
    The server will respond to requests and include the size of the response
    in its response headers for testing purposes.
    """
    import threading
    from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
    
    class MockApiHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            try:
                # Read the request data
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                # Parse JSON data
                request_data = json.loads(post_data.decode('utf-8'))
                
                # Extract request ID if available
                request_id = request_data.get("requestId", "unknown")
                
                # Determine response size based on request size
                # For testing, we'll make the response roughly the same size as the request
                request_size = len(post_data)
                
                # Prepare a response with positions for each symbol
                positions = request_data.get("positions", [])
                if not positions and "symbols" in request_data:
                    # Generate positions for each symbol
                    positions = []
                    for symbol in request_data.get("symbols", []):
                        position = {
                            "symbol": symbol,
                            "score": random.uniform(0, 1),
                            "recommendation": random.choice(["HOLD", "BUY", "SELL"]),
                            "fibonacci": {
                                "levels": [random.uniform(1000, 100000) for _ in range(7)],
                                "current": random.uniform(1000, 100000)
                            },
                            "analysis": {
                                "trend": random.choice(["bullish", "bearish", "neutral"]),
                                "momentum": random.uniform(-1, 1),
                                "volatility": random.uniform(0, 1),
                                "support": random.uniform(1000, 100000),
                                "resistance": random.uniform(1000, 100000)
                            }
                        }
                        positions.append(position)
                
                # Generate a response
                response = {
                    "status": "success",
                    "requestId": request_id,
                    "timestamp": time.time(),
                    "data": {
                        "positions": positions,
                        "overallHarmony": random.uniform(0, 1)
                    }
                }
                
                # If the request had additional data, echo it back to match size
                if "additionalData" in request_data:
                    response["additionalData"] = request_data["additionalData"]
                
                # Convert response to JSON
                response_json = json.dumps(response)
                response_bytes = response_json.encode('utf-8')
                
                # Send the response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(response_bytes)))
                self.send_header('X-Request-Size', str(request_size))
                self.send_header('X-Response-Size', str(len(response_bytes)))
                self.end_headers()
                self.wfile.write(response_bytes)
                
            except Exception as e:
                # Log the error
                logger.error(f"Error processing request: {str(e)}")
                
                # Send error response
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_response = {"status": "error", "message": str(e)}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    server = ThreadingHTTPServer((host, port), MockApiHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    
    logger.info(f"Started mock API server at http://{host}:{port}")
    return server


@pytest.fixture(scope="module")
def api_server():
    """Start an API server for testing."""
    if REAL_IMPLEMENTATION:
        try:
            from omega_bot_farm.trading.b0ts.bitget_analyzer.api.server import start_api_server
            server = start_api_server(test_mode=True)
        except ImportError:
            server = mock_api_server()
    else:
        server = mock_api_server()
        
    yield server
    
    # Clean up
    if not REAL_IMPLEMENTATION:
        server.shutdown()


class TestMemoryPressure:
    """Test suite for API memory pressure handling."""
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("payload_size", [
        TEST_CONFIG["small_payload_size_kb"],
        TEST_CONFIG["medium_payload_size_kb"]
    ])
    async def test_memory_stability(self, api_server, payload_size):
        """Test that memory usage remains stable with different payload sizes."""
        api_url = f"{TEST_CONFIG['test_host']}{TEST_CONFIG['api_endpoint']}"
        
        # Run the memory test
        results = await run_memory_test(
            payload_size,
            TEST_CONFIG["test_duration_seconds"],
            api_url
        )
        
        logger.info(results.summary())
        
        # Assert that memory growth is within acceptable limits
        assert results.memory_growth_percent < TEST_CONFIG["max_memory_increase_percent"], \
            f"Memory growth {results.memory_growth_percent:.2f}% exceeds limit of {TEST_CONFIG['max_memory_increase_percent']}%"
        
        # Assert that most requests succeeded
        assert results.success_rate > 95.0, f"Success rate {results.success_rate:.2f}% is too low"
    
    @pytest.mark.asyncio
    async def test_large_payload_handling(self, api_server):
        """Test that the API can handle large payloads."""
        api_url = f"{TEST_CONFIG['test_host']}{TEST_CONFIG['api_endpoint']}"
        
        # Test with a large payload, but shorter duration
        results = await run_memory_test(
            TEST_CONFIG["large_payload_size_kb"],
            TEST_CONFIG["test_duration_seconds"] // 2,  # Half duration due to payload size
            api_url
        )
        
        logger.info(results.summary())
        
        # Assert that most requests succeeded
        assert results.success_rate > 90.0, f"Success rate {results.success_rate:.2f}% is too low for large payloads"
        
        # Memory growth may be higher for large payloads, but should still be bounded
        assert results.memory_growth_percent < TEST_CONFIG["max_memory_increase_percent"] * 2, \
            f"Memory growth {results.memory_growth_percent:.2f}% is excessive for large payloads"
    
    @pytest.mark.asyncio
    async def test_memory_cleanup(self, api_server):
        """Test that memory is properly released after processing."""
        api_url = f"{TEST_CONFIG['test_host']}{TEST_CONFIG['api_endpoint']}"
        
        # First run with medium payloads
        results_first = await run_memory_test(
            TEST_CONFIG["medium_payload_size_kb"],
            TEST_CONFIG["test_duration_seconds"] // 2,
            api_url
        )
        
        # Force garbage collection
        gc.collect()
        
        # Wait a moment for memory to stabilize
        await asyncio.sleep(2)
        
        # Get memory usage after first test and GC
        post_gc_memory = check_server_memory_usage()
        
        # Run a second test
        results_second = await run_memory_test(
            TEST_CONFIG["medium_payload_size_kb"],
            TEST_CONFIG["test_duration_seconds"] // 2,
            api_url
        )
        
        logger.info(f"First test memory growth: {results_first.memory_growth_percent:.2f}%")
        logger.info(f"Second test memory growth: {results_second.memory_growth_percent:.2f}%")
        
        # Calculate memory growth between tests
        memory_growth_between_tests = (results_second.start_memory["rss"] - post_gc_memory["rss"]) / post_gc_memory["rss"] * 100
        
        logger.info(f"Memory growth between tests: {memory_growth_between_tests:.2f}%")
        
        # Memory should be mostly released between tests
        assert abs(memory_growth_between_tests) < 5.0, \
            f"Memory not properly released between tests: {memory_growth_between_tests:.2f}%"
    
    @pytest.mark.asyncio
    async def test_rapid_gc_behavior(self, api_server):
        """Test behavior with frequent garbage collection."""
        api_url = f"{TEST_CONFIG['test_host']}{TEST_CONFIG['api_endpoint']}"
        
        # Start memory monitoring
        results = MemoryTestResults()
        results.start()
        
        # Prepare session for requests
        async with aiohttp.ClientSession() as session:
            # Make a sequence of requests with GC between each
            for _ in range(20):
                # Generate payload
                payload = generate_random_payload(TEST_CONFIG["medium_payload_size_kb"])
                
                # Make request
                success, payload_size = await make_api_request(session, url=api_url, payload=payload)
                results.record_request(success, payload_size)
                
                # Force garbage collection
                gc.collect()
                
                # Sample memory
                results.sample_memory()
                
                # Small delay
                await asyncio.sleep(0.2)
        
        results.end()
        logger.info(results.summary())
        
        # Memory should be stable with frequent GC
        assert results.memory_growth_percent < 5.0, \
            f"Memory growth {results.memory_growth_percent:.2f}% is too high with frequent GC"


if __name__ == "__main__":
    # This allows the test to be run directly for debugging
    asyncio.run(run_memory_test(
        TEST_CONFIG["medium_payload_size_kb"],
        10,  # 10 seconds duration
        f"http://localhost:8080{TEST_CONFIG['api_endpoint']}"
    )) 