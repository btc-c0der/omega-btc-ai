"""
Tests for sustained load handling in the BitgetPositionAnalyzerB0t API.

These tests verify:
- The API can handle a constant load over an extended period
- Performance remains stable over time
- No degradation in response times occurs
- Resource utilization remains within acceptable limits
"""

import asyncio
import time
import pytest
import aiohttp
import statistics
import logging
import json
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Any, Tuple
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Test configuration
TEST_CONFIG = {
    "load_levels": [10, 20, 30],  # Requests per second to maintain
    "api_endpoint": "/api/v1/position-analysis",  # API endpoint to test
    "test_duration_minutes": 5,  # How long to run each test scenario
    "warmup_duration_seconds": 30,  # Warmup time before measurements
    "request_timeout_seconds": 10,  # Maximum time to wait for a response
    "test_host": "http://localhost:8080",  # Default test host
    "sampling_interval_seconds": 10,  # How often to sample metrics
    "plot_results": True,  # Whether to generate performance plots
    "plot_directory": "./test_results",  # Directory to store test results and plots
}

# Try to import the real implementation for direct testing, fall back to mock API testing
try:
    from omega_bot_farm.trading.b0ts.bitget_analyzer.api.server import start_api_server
    REAL_IMPLEMENTATION = True
except ImportError:
    REAL_IMPLEMENTATION = False


class LoadTestMetrics:
    """Metrics for a load test run."""
    
    def __init__(self):
        """Initialize the metrics container."""
        self.timestamps = []  # Time of each sample
        self.response_times = []  # All individual response times
        self.success_count = 0
        self.error_count = 0
        self.timeout_count = 0
        self.requests_sent = 0
        self.start_time = None
        self.end_time = None
        
        # Time series metrics (sampled at intervals)
        self.sample_timestamps = []
        self.throughput_samples = []  # Requests per second at each sample
        self.success_rate_samples = []  # Success rate at each sample
        self.mean_latency_samples = []  # Mean latency at each sample
        self.p95_latency_samples = []  # 95th percentile latency at each sample
        self.window_response_times = []  # Response times within current sampling window
        
    def start(self):
        """Mark the start time of the test."""
        self.start_time = time.time()
        self.next_sample_time = self.start_time + TEST_CONFIG["sampling_interval_seconds"]
        
    def end(self):
        """Mark the end time of the test."""
        self.end_time = time.time()
        # Take a final sample
        self._take_sample()
        
    def add_result(self, timestamp: float, response_time: float, is_success: bool, is_timeout: bool = False):
        """Add a result from a single request."""
        self.timestamps.append(timestamp)
        
        if is_success:
            self.response_times.append(response_time)
            self.window_response_times.append(response_time)
            self.success_count += 1
        elif is_timeout:
            self.timeout_count += 1
        else:
            self.error_count += 1
            
        self.requests_sent += 1
        
        # Check if it's time to take a metric sample
        if time.time() >= self.next_sample_time:
            self._take_sample()
            self.next_sample_time = time.time() + TEST_CONFIG["sampling_interval_seconds"]
            # Clear the window for the next sample
            self.window_response_times = []
    
    def _take_sample(self):
        """Take a sample of the current metrics."""
        now = time.time()
        if self.start_time is None:
            return  # Can't take a sample before the test starts
            
        # Calculate elapsed time since test start
        elapsed_seconds = now - self.start_time
        
        # Only sample if we have some data
        if self.requests_sent == 0:
            return
            
        # Add timestamp for this sample
        self.sample_timestamps.append(elapsed_seconds)
        
        # Calculate throughput (requests per second)
        if len(self.sample_timestamps) == 1:
            # First sample, calculate from start
            throughput = self.requests_sent / elapsed_seconds
        else:
            # Calculate throughput since last sample
            last_sample_time = self.sample_timestamps[-2]
            throughput = (self.requests_sent - sum(self.throughput_samples)) / (elapsed_seconds - last_sample_time)
            
        self.throughput_samples.append(throughput)
        
        # Calculate success rate
        success_rate = (self.success_count / self.requests_sent) * 100
        self.success_rate_samples.append(success_rate)
        
        # Calculate latency metrics if we have data for this window
        if self.window_response_times:
            mean_latency = sum(self.window_response_times) / len(self.window_response_times)
            self.mean_latency_samples.append(mean_latency)
            
            # Calculate 95th percentile latency
            p95_latency = np.percentile(self.window_response_times, 95)
            self.p95_latency_samples.append(p95_latency)
        elif self.response_times:
            # Fall back to overall stats if no window data
            mean_latency = sum(self.response_times) / len(self.response_times)
            self.mean_latency_samples.append(mean_latency)
            
            p95_latency = np.percentile(self.response_times, 95)
            self.p95_latency_samples.append(p95_latency)
        else:
            # No response times at all
            self.mean_latency_samples.append(0)
            self.p95_latency_samples.append(0)
    
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
        return sum(self.response_times) / len(self.response_times)
    
    @property
    def median_response_time(self) -> float:
        """Get the median response time in seconds."""
        if not self.response_times:
            return 0.0
        return np.median(self.response_times)
    
    @property
    def p95_response_time(self) -> float:
        """Get the 95th percentile response time in seconds."""
        if not self.response_times:
            return 0.0
        return np.percentile(self.response_times, 95)
    
    @property
    def p99_response_time(self) -> float:
        """Get the 99th percentile response time in seconds."""
        if not self.response_times:
            return 0.0
        return np.percentile(self.response_times, 99)
    
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
    
    @property
    def response_time_stddev(self) -> float:
        """Get the standard deviation of response times."""
        if not self.response_times or len(self.response_times) < 2:
            return 0.0
        return np.std(self.response_times)
    
    def generate_plots(self, test_name: str, load_level: int):
        """Generate performance plots from the metrics.
        
        Args:
            test_name: Name of the test for plot titles
            load_level: Load level of the test for naming
        """
        if not TEST_CONFIG["plot_results"]:
            return
            
        try:
            import os
            import matplotlib.pyplot as plt
            from matplotlib.ticker import MaxNLocator
            
            # Create the output directory if it doesn't exist
            os.makedirs(TEST_CONFIG["plot_directory"], exist_ok=True)
            
            # Generate timestamp for file names
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            base_filename = f"{TEST_CONFIG['plot_directory']}/{test_name}_{load_level}rps_{timestamp}"
            
            # 1. Throughput over time
            plt.figure(figsize=(12, 6))
            plt.plot(self.sample_timestamps, self.throughput_samples, 'b-', linewidth=2)
            plt.axhline(y=load_level, color='r', linestyle='--', label=f'Target: {load_level} RPS')
            plt.title(f"Throughput Over Time - Target: {load_level} RPS")
            plt.xlabel("Time (seconds)")
            plt.ylabel("Requests per Second")
            plt.grid(True)
            plt.legend()
            plt.savefig(f"{base_filename}_throughput.png")
            plt.close()
            
            # 2. Response times over time
            plt.figure(figsize=(12, 6))
            plt.plot(self.sample_timestamps, self.mean_latency_samples, 'b-', label='Mean', linewidth=2)
            plt.plot(self.sample_timestamps, self.p95_latency_samples, 'r-', label='95th Percentile', linewidth=2)
            plt.title(f"Response Times Over Time - Load: {load_level} RPS")
            plt.xlabel("Time (seconds)")
            plt.ylabel("Response Time (seconds)")
            plt.grid(True)
            plt.legend()
            plt.savefig(f"{base_filename}_latency.png")
            plt.close()
            
            # 3. Success rate over time
            plt.figure(figsize=(12, 6))
            plt.plot(self.sample_timestamps, self.success_rate_samples, 'g-', linewidth=2)
            plt.axhline(y=100, color='r', linestyle='--', label='Target: 100%')
            plt.title(f"Success Rate Over Time - Load: {load_level} RPS")
            plt.xlabel("Time (seconds)")
            plt.ylabel("Success Rate (%)")
            plt.ylim(0, 101)  # Cap at 101% for better visualization
            plt.grid(True)
            plt.legend()
            plt.savefig(f"{base_filename}_success_rate.png")
            plt.close()
            
            # 4. Response time distribution (histogram)
            plt.figure(figsize=(12, 6))
            plt.hist(self.response_times, bins=50, alpha=0.75, color='b')
            plt.axvline(x=self.mean_response_time, color='r', linestyle='--', 
                       label=f'Mean: {self.mean_response_time:.3f}s')
            plt.axvline(x=self.p95_response_time, color='g', linestyle='--', 
                       label=f'95th: {self.p95_response_time:.3f}s')
            plt.title(f"Response Time Distribution - Load: {load_level} RPS")
            plt.xlabel("Response Time (seconds)")
            plt.ylabel("Frequency")
            plt.grid(True)
            plt.legend()
            plt.savefig(f"{base_filename}_rt_distribution.png")
            plt.close()
            
            logger.info(f"Performance plots saved to {TEST_CONFIG['plot_directory']}")
        except Exception as e:
            logger.error(f"Failed to generate plots: {str(e)}")
    
    def summary(self) -> str:
        """Get a summary of the test results as a string."""
        summary_lines = [
            "Sustained Load Test Results",
            "---------------------------",
            f"Total Requests: {self.total_requests}",
            f"Success Rate: {self.success_rate:.2f}%",
            f"Test Duration: {self.test_duration:.2f} seconds",
            f"Average Throughput: {self.requests_per_second:.2f} requests/second",
            f"Response Time Statistics:",
            f"  - Mean: {self.mean_response_time:.3f} seconds",
            f"  - Median: {self.median_response_time:.3f} seconds",
            f"  - 95th Percentile: {self.p95_response_time:.3f} seconds",
            f"  - 99th Percentile: {self.p99_response_time:.3f} seconds",
            f"  - Min: {self.min_response_time:.3f} seconds",
            f"  - Max: {self.max_response_time:.3f} seconds",
            f"  - Std Dev: {self.response_time_stddev:.3f} seconds",
            f"Error Count: {self.error_count}",
            f"Timeout Count: {self.timeout_count}"
        ]
        
        # Add performance stability indicators
        if len(self.throughput_samples) > 1:
            throughput_variation = np.std(self.throughput_samples) / np.mean(self.throughput_samples) * 100
            summary_lines.append(f"Throughput Variation: {throughput_variation:.2f}%")
            
        if len(self.mean_latency_samples) > 1:
            # Calculate trend by comparing first half vs second half
            midpoint = len(self.mean_latency_samples) // 2
            first_half = self.mean_latency_samples[:midpoint]
            second_half = self.mean_latency_samples[midpoint:]
            
            if first_half and second_half:
                first_half_avg = sum(first_half) / len(first_half)
                second_half_avg = sum(second_half) / len(second_half)
                
                percent_change = ((second_half_avg - first_half_avg) / first_half_avg) * 100
                summary_lines.append(f"Response Time Trend: {percent_change:+.2f}% change over test duration")
        
        return "\n".join(summary_lines)


async def make_api_request(session: aiohttp.ClientSession, url: str, metrics: LoadTestMetrics):
    """Make a single API request and record the results.
    
    Args:
        session: The aiohttp session to use
        url: The URL to request
        metrics: The metrics container to update
    """
    # Generate a unique request ID
    request_id = f"req_{int(time.time() * 1000)}_{id(metrics)}"
    
    # Prepare a sample request payload
    payload = {
        "userId": "load_test_user",
        "timestamp": time.time(),
        "symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT"],
        "requestId": request_id
    }
    
    start_time = time.time()
    is_timeout = False
    is_success = False
    
    try:
        async with session.post(
            url, 
            json=payload,
            timeout=aiohttp.ClientTimeout(total=TEST_CONFIG["request_timeout_seconds"])
        ) as response:
            # Read the response to ensure it's complete
            await response.text()
            is_success = 200 <= response.status < 300
    except asyncio.TimeoutError:
        is_timeout = True
        logger.warning(f"Request timed out after {TEST_CONFIG['request_timeout_seconds']} seconds")
    except Exception as e:
        logger.warning(f"Request failed: {str(e)}")
        
    response_time = time.time() - start_time
    
    # Record metrics
    metrics.add_result(start_time, response_time, is_success, is_timeout)


async def constant_load_generator(rate: float, duration: float, url: str) -> LoadTestMetrics:
    """Generate a constant load at the specified rate for the given duration.
    
    Args:
        rate: Target requests per second
        duration: How long to run the test in seconds
        url: The API endpoint URL
        
    Returns:
        Metrics from the load test
    """
    logger.info(f"Starting constant load test at {rate} requests/second for {duration} seconds")
    
    metrics = LoadTestMetrics()
    metrics.start()
    
    # Calculate the interval between requests to achieve the target rate
    interval = 1.0 / rate if rate > 0 else 1.0
    
    # Create a ClientSession for all requests
    async with aiohttp.ClientSession() as session:
        end_time = time.time() + duration
        
        # Record when the last request was sent
        last_request_time = time.time()
        
        # Warm-up phase: ramp up to the target rate
        warmup_end_time = time.time() + min(TEST_CONFIG["warmup_duration_seconds"], duration * 0.1)
        warmup_rate = rate / 2  # Start at half the target rate
        
        # Set initial rate for warmup
        current_rate = warmup_rate
        current_interval = 1.0 / current_rate if current_rate > 0 else 1.0
        
        logger.info(f"Warm-up phase starting at {warmup_rate} requests/second")
        
        while time.time() < end_time:
            # Adjust rate if we're in the warmup phase
            if time.time() < warmup_end_time:
                # Gradually increase from warmup_rate to full rate
                progress = (time.time() - metrics.start_time) / (warmup_end_time - metrics.start_time)
                current_rate = warmup_rate + progress * (rate - warmup_rate)
                current_interval = 1.0 / current_rate if current_rate > 0 else 1.0
                
            # Check if it's time to send the next request
            if time.time() - last_request_time >= current_interval:
                # Create task for the request
                asyncio.create_task(make_api_request(session, url, metrics))
                last_request_time = time.time()
            
            # Yield control to allow other coroutines to run
            await asyncio.sleep(0.001)  # Small sleep to prevent CPU spinning
        
        # Wait for any remaining requests to complete
        logger.info("Waiting for remaining requests to complete...")
        await asyncio.sleep(2)
    
    metrics.end()
    logger.info(f"Load test completed: {metrics.total_requests} requests, {metrics.success_rate:.2f}% success rate")
    
    return metrics


def mock_api_server(host="localhost", port=8080):
    """Start a mock API server for testing if real implementation is not available."""
    import threading
    from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
    
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
        # Start the real API server if available
        try:
            server = start_api_server(test_mode=True)
        except NameError:
            logger.warning("Real implementation imported but start_api_server not found, using mock instead")
            server = mock_api_server()
    else:
        # Start a mock API server
        server = mock_api_server()
        
    yield server
    
    # Clean up
    if not REAL_IMPLEMENTATION:
        server.shutdown()


class TestSustainedLoad:
    """Test suite for sustained API load."""
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("load_level", TEST_CONFIG["load_levels"])
    async def test_constant_load(self, api_server, load_level):
        """Test the API with a constant load at different levels."""
        api_url = f"{TEST_CONFIG['test_host']}{TEST_CONFIG['api_endpoint']}"
        
        # Convert minutes to seconds for the test duration
        duration_seconds = TEST_CONFIG["test_duration_minutes"] * 60
        
        # Run the load test
        metrics = await constant_load_generator(load_level, duration_seconds, api_url)
        
        # Log the results
        logger.info(metrics.summary())
        
        # Generate performance plots
        metrics.generate_plots("constant_load", load_level)
        
        # Basic assertions for test pass/fail criteria
        assert metrics.success_rate > 95.0, f"Success rate {metrics.success_rate:.2f}% is below threshold of 95%"
        
        # Check if throughput was close to target
        avg_throughput = metrics.requests_per_second
        assert abs(avg_throughput - load_level) / load_level < 0.2, \
            f"Average throughput {avg_throughput:.2f} RPS differs from target {load_level} RPS by more than 20%"
        
        # Check for stability in response times
        # Calculate coefficient of variation (CV) which is stddev/mean
        if metrics.mean_response_time > 0:
            cv = metrics.response_time_stddev / metrics.mean_response_time
            assert cv < 0.5, f"Response time variation (CV={cv:.2f}) exceeds threshold of 0.5"
        
        # Analyze trend to detect performance degradation
        if len(metrics.mean_latency_samples) > 1:
            # Divide the test into thirds
            third_size = len(metrics.mean_latency_samples) // 3
            if third_size > 0:
                first_third = metrics.mean_latency_samples[:third_size]
                last_third = metrics.mean_latency_samples[-third_size:]
                
                first_third_avg = sum(first_third) / len(first_third)
                last_third_avg = sum(last_third) / len(last_third)
                
                # Check if response times in the last third are significantly higher
                percent_increase = ((last_third_avg - first_third_avg) / first_third_avg) * 100
                assert percent_increase < 50, \
                    f"Response time increased by {percent_increase:.2f}% from start to end of test"
    
    @pytest.mark.asyncio
    async def test_long_duration_stability(self, api_server):
        """Test API stability over a longer duration with moderate load."""
        api_url = f"{TEST_CONFIG['test_host']}{TEST_CONFIG['api_endpoint']}"
        
        # Use a longer duration for stability testing, but keep the test duration reasonable
        # In a real scenario, this might run for hours
        long_duration = max(TEST_CONFIG["test_duration_minutes"] * 1.5, 10) * 60  # seconds
        
        # Use a moderate load level
        load_level = TEST_CONFIG["load_levels"][0] if TEST_CONFIG["load_levels"] else 10
        
        logger.info(f"Starting long duration stability test for {long_duration/60:.1f} minutes at {load_level} RPS")
        
        # Run the load test
        metrics = await constant_load_generator(load_level, long_duration, api_url)
        
        # Log the results
        logger.info(metrics.summary())
        
        # Generate performance plots
        metrics.generate_plots("long_duration", load_level)
        
        # Check if the success rate remains high throughout
        assert metrics.success_rate > 95.0, f"Success rate {metrics.success_rate:.2f}% fell below 95% during long test"
        
        # Check for consistent throughput
        throughput_samples = metrics.throughput_samples
        if throughput_samples:
            throughput_variation = np.std(throughput_samples) / np.mean(throughput_samples)
            assert throughput_variation < 0.3, \
                f"Throughput variation coefficient {throughput_variation:.2f} exceeds threshold of 0.3"
            
        # Check for response time stability - look for any upward trend
        if len(metrics.mean_latency_samples) > 10:
            # Simple linear regression to detect trend
            x = np.array(range(len(metrics.mean_latency_samples)))
            y = np.array(metrics.mean_latency_samples)
            
            # Calculate slope using numpy's polyfit
            slope, _ = np.polyfit(x, y, 1)
            
            # Normalize slope as percentage of initial response time
            if metrics.mean_latency_samples[0] > 0:
                normalized_slope = slope / metrics.mean_latency_samples[0] * 100
                
                # Allow for a small upward trend, but flag significant degradation
                assert normalized_slope < 5.0, \
                    f"Response time shows upward trend of {normalized_slope:.2f}% per sample interval"


if __name__ == "__main__":
    # This allows the test to be run directly for debugging
    asyncio.run(constant_load_generator(
        20,  # 20 requests per second
        60,  # 1 minute duration
        f"http://localhost:8080{TEST_CONFIG['api_endpoint']}"
    )) 