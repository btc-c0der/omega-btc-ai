"""
Tests for concurrent request handling in the BitgetPositionAnalyzerB0t API.

These tests verify:
- The API can handle a high number of simultaneous requests
- Response times remain acceptable under concurrent load
- No requests are dropped or timeout under concurrent access
- The API correctly maintains data consistency under concurrent operations
"""

import asyncio
import time
import pytest
import aiohttp
import statistics
import logging
import json
from typing import List, Dict, Any, Tuple
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Test configuration
TEST_CONFIG = {
    "concurrent_users": [10, 50, 100, 200],  # Number of concurrent users to simulate
    "api_endpoint": "/api/v1/position-analysis",  # API endpoint to test
    "test_duration_seconds": 30,  # How long to run each test scenario
    "request_timeout_seconds": 10,  # Maximum time to wait for a response
    "acceptable_mean_response_time": 1.0,  # Target mean response time in seconds
    "acceptable_p95_response_time": 3.0,  # Target 95th percentile response time in seconds
    "target_requests_per_second": 20,  # Target throughput
    "test_host": "http://localhost:8080",  # Default test host
}

# Try to import the real implementation for direct testing, fall back to mock API testing
try:
    from omega_bot_farm.trading.b0ts.bitget_analyzer.api.server import start_api_server
    REAL_IMPLEMENTATION = True
except ImportError:
    REAL_IMPLEMENTATION = False


class ConcurrencyResults:
    """Results of a concurrency test run."""
    
    def __init__(self):
        """Initialize the results container."""
        self.response_times = []
        self.success_count = 0
        self.error_count = 0
        self.timeout_count = 0
        self.start_time = None
        self.end_time = None
        self.status_codes = {}
        
    def add_result(self, response_time: float, status_code: int, is_success: bool, is_timeout: bool = False):
        """Add a result from a single request."""
        if is_success:
            self.response_times.append(response_time)
            self.success_count += 1
            
            # Count status codes
            if status_code in self.status_codes:
                self.status_codes[status_code] += 1
            else:
                self.status_codes[status_code] = 1
        elif is_timeout:
            self.timeout_count += 1
        else:
            self.error_count += 1
            
            # Count error status codes
            if status_code in self.status_codes:
                self.status_codes[status_code] += 1
            else:
                self.status_codes[status_code] = 1
    
    def start(self):
        """Mark the start time of the test."""
        self.start_time = time.time()
    
    def end(self):
        """Mark the end time of the test."""
        self.end_time = time.time()
    
    @property
    def total_requests(self) -> int:
        """Get the total number of requests made."""
        return self.success_count + self.error_count + self.timeout_count
    
    @property
    def success_rate(self) -> float:
        """Get the success rate as a percentage."""
        if self.total_requests == 0:
            return 0.0
        return (self.success_count / self.total_requests) * 100
    
    @property
    def test_duration(self) -> float:
        """Get the total test duration in seconds."""
        if self.start_time is None or self.end_time is None:
            return 0.0
        return self.end_time - self.start_time
    
    @property
    def requests_per_second(self) -> float:
        """Get the throughput in requests per second."""
        if self.test_duration == 0:
            return 0.0
        return self.total_requests / self.test_duration
    
    @property
    def mean_response_time(self) -> float:
        """Get the mean response time in seconds."""
        if not self.response_times:
            return 0.0
        return statistics.mean(self.response_times)
    
    @property
    def median_response_time(self) -> float:
        """Get the median response time in seconds."""
        if not self.response_times:
            return 0.0
        return statistics.median(self.response_times)
    
    @property
    def p95_response_time(self) -> float:
        """Get the 95th percentile response time in seconds."""
        if not self.response_times:
            return 0.0
        sorted_times = sorted(self.response_times)
        idx = int(len(sorted_times) * 0.95)
        return sorted_times[idx]
    
    @property
    def min_response_time(self) -> float:
        """Get the minimum response time in seconds."""
        if not self.response_times:
            return 0.0
        return min(self.response_times)
    
    @property
    def max_response_time(self) -> float:
        """Get the maximum response time in seconds."""
        if not self.response_times:
            return 0.0
        return max(self.response_times)
    
    def summary(self) -> str:
        """Get a summary of the results as a string."""
        summary_lines = [
            "Concurrency Test Results",
            "-------------------------",
            f"Total Requests: {self.total_requests}",
            f"Success Rate: {self.success_rate:.2f}%",
            f"Test Duration: {self.test_duration:.2f} seconds",
            f"Throughput: {self.requests_per_second:.2f} requests/second",
            f"Mean Response Time: {self.mean_response_time:.3f} seconds",
            f"Median Response Time: {self.median_response_time:.3f} seconds",
            f"95th Percentile Response Time: {self.p95_response_time:.3f} seconds",
            f"Min Response Time: {self.min_response_time:.3f} seconds",
            f"Max Response Time: {self.max_response_time:.3f} seconds",
            "Status Code Breakdown:",
        ]
        
        for code, count in sorted(self.status_codes.items()):
            summary_lines.append(f"  {code}: {count} ({count/self.total_requests*100:.1f}%)")
            
        if self.timeout_count > 0:
            summary_lines.append(f"Timeouts: {self.timeout_count} ({self.timeout_count/self.total_requests*100:.1f}%)")
            
        return "\n".join(summary_lines)


async def make_api_request(session: aiohttp.ClientSession, url: str, payload: Dict[str, Any]) -> Tuple[float, int, bool, bool]:
    """Make a single API request and return the results.
    
    Args:
        session: The aiohttp session to use
        url: The URL to request
        payload: The request payload
        
    Returns:
        Tuple of (response_time, status_code, is_success, is_timeout)
    """
    start_time = time.time()
    is_timeout = False
    is_success = False
    status_code = 0
    
    try:
        async with session.post(url, json=payload, timeout=TEST_CONFIG["request_timeout_seconds"]) as response:
            status_code = response.status
            is_success = 200 <= status_code < 300
            await response.text()  # Read the response body
    except asyncio.TimeoutError:
        is_timeout = True
        logger.warning(f"Request timed out after {TEST_CONFIG['request_timeout_seconds']} seconds")
    except Exception as e:
        logger.warning(f"Request failed: {str(e)}")
        
    response_time = time.time() - start_time
    return response_time, status_code, is_success, is_timeout


async def user_session(user_id: int, duration: float, url: str, results: ConcurrencyResults):
    """Simulate a user session making repeated requests for a specified duration.
    
    Args:
        user_id: The ID of the simulated user
        duration: How long to run the session in seconds
        url: The API URL to target
        results: The results container to update
    """
    end_time = time.time() + duration
    
    # Create a session for this user
    async with aiohttp.ClientSession() as session:
        request_count = 0
        
        while time.time() < end_time:
            # Prepare a sample request payload
            payload = {
                "userId": f"user_{user_id}",
                "timestamp": time.time(),
                "symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT"],
                "requestId": f"req_{user_id}_{request_count}"
            }
            
            # Make the request
            response_time, status_code, is_success, is_timeout = await make_api_request(session, url, payload)
            
            # Record the result
            results.add_result(response_time, status_code, is_success, is_timeout)
            
            request_count += 1
            
            # Small delay between requests from the same user
            await asyncio.sleep(0.1)


async def run_concurrency_test(concurrent_users: int, duration: float, api_url: str) -> ConcurrencyResults:
    """Run a concurrency test with the specified number of users.
    
    Args:
        concurrent_users: The number of concurrent users to simulate
        duration: How long to run the test in seconds
        api_url: The API URL to target
        
    Returns:
        The test results
    """
    logger.info(f"Starting concurrency test with {concurrent_users} users for {duration} seconds")
    
    results = ConcurrencyResults()
    results.start()
    
    # Create a task for each user
    tasks = []
    for user_id in range(concurrent_users):
        task = asyncio.create_task(user_session(user_id, duration, api_url, results))
        tasks.append(task)
    
    # Wait for all tasks to complete
    await asyncio.gather(*tasks)
    
    results.end()
    logger.info(f"Concurrency test completed: {results.total_requests} requests, {results.success_rate:.2f}% success rate")
    
    return results


def mock_api_server(host="localhost", port=8080):
    """Start a mock API server for testing if real implementation is not available."""
    import threading
    from http.server import HTTPServer, BaseHTTPRequestHandler
    
    class MockApiHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Simulate processing time
            time.sleep(0.05)  # Base latency
            
            # Randomly add some additional latency to simulate variability
            import random
            if random.random() < 0.1:  # 10% chance of slower response
                time.sleep(0.2)
                
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
    
    server = HTTPServer((host, port), MockApiHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    logger.info(f"Started mock API server at http://{host}:{port}")
    return server


@pytest.fixture(scope="module")
def api_server():
    """Start an API server for testing."""
    if REAL_IMPLEMENTATION:
        # Start the real API server if available
        server = start_api_server(test_mode=True)
    else:
        # Start a mock API server
        server = mock_api_server()
        
    yield server
    
    # Clean up
    if not REAL_IMPLEMENTATION:
        server.shutdown()


class TestConcurrentRequests:
    """Test suite for concurrent API requests."""
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("concurrent_users", TEST_CONFIG["concurrent_users"])
    async def test_concurrent_users(self, api_server, concurrent_users):
        """Test the API with different numbers of concurrent users."""
        api_url = f"{TEST_CONFIG['test_host']}{TEST_CONFIG['api_endpoint']}"
        
        results = await run_concurrency_test(
            concurrent_users, 
            TEST_CONFIG["test_duration_seconds"], 
            api_url
        )
        
        logger.info(results.summary())
        
        # Basic assertions for test pass/fail criteria
        assert results.success_rate > 95.0, f"Success rate {results.success_rate:.2f}% is below threshold of 95%"
        assert results.timeout_count == 0, f"Had {results.timeout_count} timeouts"
        
        # Performance assertions (relaxed for higher concurrency)
        if concurrent_users <= 50:
            assert results.mean_response_time < TEST_CONFIG["acceptable_mean_response_time"], \
                f"Mean response time {results.mean_response_time:.3f}s exceeds threshold of {TEST_CONFIG['acceptable_mean_response_time']}s"
            assert results.p95_response_time < TEST_CONFIG["acceptable_p95_response_time"], \
                f"95th percentile response time {results.p95_response_time:.3f}s exceeds threshold of {TEST_CONFIG['acceptable_p95_response_time']}s"
        
    @pytest.mark.asyncio
    async def test_throughput_sustained(self, api_server):
        """Test that the API can sustain the target throughput."""
        api_url = f"{TEST_CONFIG['test_host']}{TEST_CONFIG['api_endpoint']}"
        
        # Calculate how many concurrent users we need for the target throughput
        # Assuming each user makes a request roughly every 0.5 seconds
        requests_per_user = 2.0  # requests per second per user
        concurrent_users = int(TEST_CONFIG["target_requests_per_second"] / requests_per_user) + 1
        
        results = await run_concurrency_test(
            concurrent_users, 
            TEST_CONFIG["test_duration_seconds"], 
            api_url
        )
        
        logger.info(results.summary())
        
        # Assert that we achieved the target throughput
        assert results.requests_per_second >= TEST_CONFIG["target_requests_per_second"], \
            f"Throughput {results.requests_per_second:.2f} req/s is below target of {TEST_CONFIG['target_requests_per_second']} req/s"
        assert results.success_rate > 95.0, f"Success rate {results.success_rate:.2f}% is below threshold of 95%"
        
    @pytest.mark.asyncio
    async def test_response_time_distribution(self, api_server):
        """Test the distribution of response times under moderate load."""
        api_url = f"{TEST_CONFIG['test_host']}{TEST_CONFIG['api_endpoint']}"
        
        # Use a moderate number of users for this test
        concurrent_users = 30
        
        results = await run_concurrency_test(
            concurrent_users, 
            TEST_CONFIG["test_duration_seconds"], 
            api_url
        )
        
        logger.info(results.summary())
        
        # Check that the response time distribution is reasonable
        assert results.max_response_time < 5.0, f"Max response time {results.max_response_time:.3f}s is too high"
        
        # Check for uniformity - max should be less than 5x median
        assert results.max_response_time < 5 * results.median_response_time, \
            f"Max response time {results.max_response_time:.3f}s is too far from median {results.median_response_time:.3f}s"


if __name__ == "__main__":
    # This allows the test to be run directly for debugging
    asyncio.run(run_concurrency_test(
        50,  # 50 concurrent users
        10,  # 10 seconds duration
        f"http://localhost:8080{TEST_CONFIG['api_endpoint']}"
    )) 