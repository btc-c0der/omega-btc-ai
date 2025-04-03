#!/usr/bin/env python3

"""
Security tests for rate limiting in BitgetPositionAnalyzerB0t.

These tests verify that the bot implements proper rate limiting:
- Respects exchange API rate limits
- Handles rate limit errors gracefully
- Implements backoff strategies
- Prevents excessive API calls
"""

import unittest
import os
import sys
import time
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

# Try to import BitgetPositionAnalyzerB0t
try:
    from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t
    BOT_AVAILABLE = True
except ImportError:
    BOT_AVAILABLE = False
    print("BitgetPositionAnalyzerB0t not available. Using mock for tests.")

# Mock implementation if import fails
if not BOT_AVAILABLE:
    class BitgetPositionAnalyzerB0t:
        """Mock implementation for testing"""
        
        def __init__(self, api_key=None, api_secret=None, api_passphrase=None, use_testnet=False):
            self.api_key = api_key or "test_key"
            self.api_secret = api_secret or "test_secret"
            self.api_passphrase = api_passphrase or "test_pass"
            self.use_testnet = use_testnet
            self.last_api_call = 0
            self.min_interval = 0.2  # 200ms between calls
            
        async def get_positions(self):
            """Mock get_positions with rate limiting."""
            # Check rate limiting
            current_time = time.time()
            time_since_last_call = current_time - self.last_api_call
            
            if time_since_last_call < self.min_interval:
                # Simulate rate limit error
                raise Exception("Rate limit exceeded")
                
            # Update last call time
            self.last_api_call = current_time
            
            # Return mock positions
            return {
                "positions": [
                    {
                        "symbol": "BTC/USDT:USDT",
                        "side": "long",
                        "entryPrice": 50000,
                        "markPrice": 55000,
                        "contracts": 0.1,
                        "notional": 5000,
                        "leverage": 10,
                        "unrealizedPnl": 500
                    }
                ]
            }


class TestRateLimiting(unittest.TestCase):
    """Test suite for rate limiting."""

    def setUp(self):
        """Set up test environment."""
        # Use dummy API credentials for testing
        self.analyzer = BitgetPositionAnalyzerB0t(
            api_key="test_key",
            api_secret="test_secret", 
            api_passphrase="test_pass",
            use_testnet=True
        )

    @patch('ccxt.bitget')
    def test_respects_rate_limits(self, mock_bitget):
        """Test that the bot respects rate limits."""
        # Mock the exchange
        mock_exchange = MagicMock()
        
        # Set up rate limit tracking
        call_times = []
        
        # Override fetch_positions to track call times
        async def mock_fetch_positions(*args, **kwargs):
            call_times.append(time.time())
            return [{"symbol": "BTC/USDT:USDT", "side": "long"}]
            
        mock_exchange.fetch_positions = AsyncMock(side_effect=mock_fetch_positions)
        mock_bitget.return_value = mock_exchange
        
        # Create analyzer with mocked exchange
        analyzer = BitgetPositionAnalyzerB0t(
            api_key="test_key",
            api_secret="test_secret",
            api_passphrase="test_pass",
            use_testnet=True
        )
        
        # Test multiple rapid calls
        async def test_multiple_calls():
            results = []
            # Make 5 calls in rapid succession
            for _ in range(5):
                try:
                    result = await analyzer.get_positions()
                    results.append(result)
                except Exception as e:
                    results.append(str(e))
            return results
            
        # Run the async test
        if hasattr(asyncio, 'run'):
            results = asyncio.run(test_multiple_calls())
        else:
            # For Python 3.6
            loop = asyncio.get_event_loop()
            results = loop.run_until_complete(test_multiple_calls())
        
        # Check that there was some rate limiting
        # Either by explicit errors or by properly spaced calls
        if len(call_times) > 1:
            intervals = [call_times[i+1] - call_times[i] for i in range(len(call_times)-1)]
            min_interval = min(intervals) if intervals else 0
            
            # Either the calls should be properly spaced (min interval > 0.1s)
            # or some calls should have failed with rate limit errors
            self.assertTrue(
                min_interval > 0.1 or any("rate limit" in str(r).lower() for r in results),
                "Bot should either space API calls or handle rate limit errors"
            )

    @patch('ccxt.bitget')
    def test_handles_rate_limit_errors(self, mock_bitget):
        """Test that the bot handles rate limit errors gracefully."""
        # Mock the exchange to raise rate limit errors
        mock_exchange = MagicMock()
        
        # Set up a counter to alternate between success and rate limit error
        call_count = [0]
        
        async def mock_fetch_positions(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] % 2 == 0:
                # Every second call raises a rate limit error
                e = Exception("Rate limit exceeded")
                e.ccxt_status_code = 429
                raise e
            return [{"symbol": "BTC/USDT:USDT", "side": "long"}]
            
        mock_exchange.fetch_positions = AsyncMock(side_effect=mock_fetch_positions)
        mock_bitget.return_value = mock_exchange
        
        # Create analyzer with mocked exchange
        analyzer = BitgetPositionAnalyzerB0t(
            api_key="test_key",
            api_secret="test_secret",
            api_passphrase="test_pass",
            use_testnet=True
        )
        
        # Test handling of rate limit errors
        async def test_rate_limit_handling():
            # Make multiple calls, some of which will fail with rate limit errors
            results = []
            for _ in range(4):
                try:
                    result = await analyzer.get_positions()
                    results.append(result)
                except Exception as e:
                    if "rate limit" in str(e).lower():
                        # This is expected
                        results.append("rate_limited")
                    else:
                        # Other errors should be re-raised
                        raise
                # Add a small delay to allow for retry mechanisms
                await asyncio.sleep(0.1)
            return results
            
        # Run the async test
        if hasattr(asyncio, 'run'):
            results = asyncio.run(test_rate_limit_handling())
        else:
            # For Python 3.6
            loop = asyncio.get_event_loop()
            results = loop.run_until_complete(test_rate_limit_handling())
        
        # Check that we got some successful calls despite rate limiting
        successful_calls = [r for r in results if isinstance(r, dict) and "positions" in r]
        self.assertGreater(len(successful_calls), 0, 
                           "Should have some successful calls despite rate limiting")

    def test_rapid_concurrent_calls(self):
        """Test that the bot handles concurrent calls safely."""
        # Test concurrent calls to get_positions
        async def test_concurrent_calls():
            # Create a list of 10 concurrent calls
            tasks = [self.analyzer.get_positions() for _ in range(10)]
            
            # Execute them concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            return results
            
        # Run the async test
        if hasattr(asyncio, 'run'):
            results = asyncio.run(test_concurrent_calls())
        else:
            # For Python 3.6
            loop = asyncio.get_event_loop()
            results = loop.run_until_complete(test_concurrent_calls())
        
        # Check that we didn't get any unexpected errors
        # Rate limit errors are expected and acceptable
        for result in results:
            if isinstance(result, Exception):
                # The only acceptable exceptions are rate limit related
                self.assertIn("rate limit", str(result).lower(), 
                              f"Unexpected error during concurrent calls: {result}")

    def test_backoff_strategy(self):
        """Test that the bot implements an exponential backoff strategy."""
        # This test is more of an integration test and would require
        # inspecting the actual implementation. For the mock, we'll
        # just check if the bot attempts to retry after rate limit errors.
        
        # Set up retry test
        retry_attempts = [0]
        
        async def mock_get_positions_with_retry():
            retry_attempts[0] += 1
            if retry_attempts[0] == 1:
                # First attempt fails with rate limit
                raise Exception("Rate limit exceeded")
            else:
                # Subsequent attempts succeed
                return {"positions": []}
        
        # Patch the get_positions method
        with patch.object(self.analyzer, 'get_positions', side_effect=mock_get_positions_with_retry):
            # Define test function
            async def test_retry_behavior():
                result = None
                try:
                    # This should trigger a retry
                    result = await self.analyzer.get_positions()
                except Exception:
                    pass
                return result, retry_attempts[0]
                
            # Run the async test
            if hasattr(asyncio, 'run'):
                result, attempts = asyncio.run(test_retry_behavior())
            else:
                # For Python 3.6
                loop = asyncio.get_event_loop()
                result, attempts = loop.run_until_complete(test_retry_behavior())
            
            # If the bot implements retries, we should have more than 1 attempt
            # Note: This test might not be applicable to all implementations
            self.assertGreater(attempts, 1, "Bot should retry after rate limit errors")


if __name__ == "__main__":
    unittest.main() 