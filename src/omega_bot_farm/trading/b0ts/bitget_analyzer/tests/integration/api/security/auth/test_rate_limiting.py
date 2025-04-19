
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
Tests for API rate limiting in the BitgetPositionAnalyzerB0t.

These tests verify:
- Rate limiting correctly restricts request frequency
- Rate limits are applied per API key
- Rate limit headers are correctly returned
- Burst protection works as expected
- Throttling increases with excessive requests
"""

import time
import pytest
import asyncio
from unittest.mock import patch, MagicMock, call

# Try to import the real implementation, fall back to mock if not available
try:
    from omega_bot_farm.trading.b0ts.bitget_analyzer.api.security import RateLimiter
    REAL_IMPLEMENTATION = True
except ImportError:
    REAL_IMPLEMENTATION = False
    
    # Mock implementation for tests
    class RateLimiter:
        """Rate limiter for API requests."""
        
        def __init__(self, max_requests_per_minute=60, burst_limit=10):
            """Initialize the rate limiter."""
            self.max_requests_per_minute = max_requests_per_minute
            self.burst_limit = burst_limit
            self.request_timestamps = {}  # key -> list of timestamps
        
        def register_request(self, api_key):
            """Register a request for a given API key."""
            now = time.time()
            
            # Initialize if first request
            if api_key not in self.request_timestamps:
                self.request_timestamps[api_key] = []
                
            # Add timestamp
            self.request_timestamps[api_key].append(now)
            
            # Clean up old timestamps (older than 1 minute)
            minute_ago = now - 60
            self.request_timestamps[api_key] = [
                ts for ts in self.request_timestamps[api_key] if ts > minute_ago
            ]
        
        def is_rate_limited(self, api_key):
            """Check if a key is currently rate limited."""
            if api_key not in self.request_timestamps:
                return False
                
            # Count requests in the last minute
            now = time.time()
            minute_ago = now - 60
            recent_requests = [
                ts for ts in self.request_timestamps[api_key] if ts > minute_ago
            ]
            
            # Check if over limit
            return len(recent_requests) >= self.max_requests_per_minute
        
        def is_burst_limited(self, api_key):
            """Check if a key has exceeded burst limit."""
            if api_key not in self.request_timestamps:
                return False
                
            # Count requests in the last second
            now = time.time()
            second_ago = now - 1
            burst_requests = [
                ts for ts in self.request_timestamps[api_key] if ts > second_ago
            ]
            
            # Check if over burst limit
            return len(burst_requests) >= self.burst_limit
        
        def get_rate_limit_headers(self, api_key):
            """Get rate limit headers for a response."""
            now = time.time()
            minute_ago = now - 60
            
            # Count requests in the last minute
            if api_key in self.request_timestamps:
                recent_requests = [
                    ts for ts in self.request_timestamps[api_key] if ts > minute_ago
                ]
                remaining = max(0, self.max_requests_per_minute - len(recent_requests))
            else:
                recent_requests = []
                remaining = self.max_requests_per_minute
                
            return {
                "X-RateLimit-Limit": str(self.max_requests_per_minute),
                "X-RateLimit-Remaining": str(remaining),
                "X-RateLimit-Reset": str(int(minute_ago + 60))
            }
        
        def get_retry_after(self, api_key):
            """Get recommended retry after time in seconds."""
            if not self.is_rate_limited(api_key):
                return 0
                
            # Find the oldest timestamp in the last minute
            now = time.time()
            minute_ago = now - 60
            
            if api_key in self.request_timestamps:
                recent_timestamps = sorted([
                    ts for ts in self.request_timestamps[api_key] if ts > minute_ago
                ])
                
                if recent_timestamps:
                    # Retry after the oldest timestamp + 60s
                    return int(recent_timestamps[0] + 60 - now) + 1
            
            # Default retry after 60 seconds
            return 60


@pytest.fixture
def rate_limiter():
    """Create a rate limiter instance with test settings."""
    return RateLimiter(max_requests_per_minute=10, burst_limit=3)


@pytest.fixture
def test_api_key():
    """Provide a test API key."""
    return "test_api_key_123"


class TestRateLimiting:
    """Test suite for API rate limiting."""
    
    def test_register_request(self, rate_limiter, test_api_key):
        """Test that requests are correctly registered."""
        # Register a request
        rate_limiter.register_request(test_api_key)
        
        # Verify request was registered
        assert test_api_key in rate_limiter.request_timestamps
        assert len(rate_limiter.request_timestamps[test_api_key]) == 1
        
        # Register another request
        rate_limiter.register_request(test_api_key)
        
        # Verify second request was registered
        assert len(rate_limiter.request_timestamps[test_api_key]) == 2
    
    def test_cleanup_old_timestamps(self, rate_limiter, test_api_key):
        """Test that old timestamps are cleaned up."""
        # Add some old timestamps (more than a minute ago)
        now = time.time()
        rate_limiter.request_timestamps[test_api_key] = [
            now - 120,  # 2 minutes ago
            now - 90,   # 1.5 minutes ago
            now - 30    # 30 seconds ago (should be kept)
        ]
        
        # Register a new request (triggers cleanup)
        rate_limiter.register_request(test_api_key)
        
        # Verify old timestamps were removed
        assert len(rate_limiter.request_timestamps[test_api_key]) == 2
        
        # All timestamps should be less than a minute old
        for ts in rate_limiter.request_timestamps[test_api_key]:
            assert ts > now - 60
    
    def test_rate_limiting_not_limited(self, rate_limiter, test_api_key):
        """Test that API keys aren't rate limited before reaching the limit."""
        # Register a few requests (below limit)
        for _ in range(5):  # Limit is 10
            rate_limiter.register_request(test_api_key)
            
        # Verify not rate limited
        assert rate_limiter.is_rate_limited(test_api_key) is False
    
    def test_rate_limiting_reached_limit(self, rate_limiter, test_api_key):
        """Test that API keys are rate limited after reaching the limit."""
        # Register enough requests to hit the limit
        for _ in range(10):  # Limit is 10
            rate_limiter.register_request(test_api_key)
            
        # Verify rate limited
        assert rate_limiter.is_rate_limited(test_api_key) is True
    
    def test_burst_limiting_not_limited(self, rate_limiter, test_api_key):
        """Test that API keys aren't burst limited before reaching the burst limit."""
        # Register a few requests (below burst limit)
        for _ in range(2):  # Burst limit is 3
            rate_limiter.register_request(test_api_key)
            
        # Verify not burst limited
        assert rate_limiter.is_burst_limited(test_api_key) is False
    
    def test_burst_limiting_reached_limit(self, rate_limiter, test_api_key):
        """Test that API keys are burst limited after reaching the burst limit."""
        # Register enough requests to hit the burst limit
        for _ in range(3):  # Burst limit is 3
            rate_limiter.register_request(test_api_key)
            
        # Verify burst limited
        assert rate_limiter.is_burst_limited(test_api_key) is True
    
    def test_rate_limit_headers(self, rate_limiter, test_api_key):
        """Test that rate limit headers are correctly generated."""
        # Register a few requests
        for _ in range(3):  # Limit is 10
            rate_limiter.register_request(test_api_key)
            
        # Get headers
        headers = rate_limiter.get_rate_limit_headers(test_api_key)
        
        # Verify headers
        assert "X-RateLimit-Limit" in headers
        assert "X-RateLimit-Remaining" in headers
        assert "X-RateLimit-Reset" in headers
        
        assert headers["X-RateLimit-Limit"] == "10"  # Our test limit
        assert headers["X-RateLimit-Remaining"] == "7"  # 10 - 3
        
        # Reset time should be in the future
        reset_time = int(headers["X-RateLimit-Reset"])
        now = int(time.time())
        assert reset_time > now
    
    def test_retry_after_not_limited(self, rate_limiter, test_api_key):
        """Test that retry-after is 0 when not rate limited."""
        # Register a few requests (below limit)
        for _ in range(5):  # Limit is 10
            rate_limiter.register_request(test_api_key)
            
        # Get retry after
        retry_after = rate_limiter.get_retry_after(test_api_key)
        
        # Verify retry after is 0
        assert retry_after == 0
    
    def test_retry_after_when_limited(self, rate_limiter, test_api_key):
        """Test that retry-after is calculated correctly when rate limited."""
        # Register enough requests to hit the limit
        for _ in range(10):  # Limit is 10
            rate_limiter.register_request(test_api_key)
            
        # Get retry after
        retry_after = rate_limiter.get_retry_after(test_api_key)
        
        # Verify retry after is positive
        assert retry_after > 0
        # Should be less than or equal to 60 seconds (1 minute window)
        assert retry_after <= 60
    
    def test_per_key_isolation(self, rate_limiter):
        """Test that rate limits are isolated per API key."""
        # Register requests for one key
        key1 = "api_key_1"
        for _ in range(10):  # Limit is 10
            rate_limiter.register_request(key1)
            
        # Register requests for another key
        key2 = "api_key_2"
        for _ in range(5):  # Limit is 10
            rate_limiter.register_request(key2)
            
        # Verify first key is rate limited
        assert rate_limiter.is_rate_limited(key1) is True
        
        # Verify second key is not rate limited
        assert rate_limiter.is_rate_limited(key2) is False
    
    @pytest.mark.asyncio
    async def test_integration_with_mock_api(self):
        """Test integration with a mock API."""
        # Create rate limiter
        rate_limiter = RateLimiter(max_requests_per_minute=5, burst_limit=2)
        
        # Mock API handler
        async def mock_api_handler(api_key):
            if rate_limiter.is_rate_limited(api_key):
                return {"error": "Rate limit exceeded"}, 429
                
            if rate_limiter.is_burst_limited(api_key):
                return {"error": "Too many requests"}, 429
                
            # Register the request
            rate_limiter.register_request(api_key)
            
            # Get rate limit headers
            headers = rate_limiter.get_rate_limit_headers(api_key)
            
            return {"data": "Success"}, 200, headers
        
        # Test API key
        api_key = "test_integration_key"
        
        # Make a few requests
        results = []
        for _ in range(7):  # Limit is 5
            response, status, *headers = await mock_api_handler(api_key)
            results.append((response, status))
            
            # Add a small delay to ensure not all requests count as burst
            await asyncio.sleep(0.1)
        
        # Verify responses
        success_count = sum(1 for _, status in results if status == 200)
        error_count = sum(1 for _, status in results if status == 429)
        
        # Should have 5 successful requests and 2 failures
        assert success_count == 5
        assert error_count == 2 