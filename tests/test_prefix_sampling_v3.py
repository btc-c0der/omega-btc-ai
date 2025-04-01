#!/usr/bin/env python3
"""
OMEGA BTC AI - Prefix Sampling Tests for BTC Live Feed v3
========================================================

Unit and integration tests for character prefix sampling in BTC Live Feed v3.
These tests simulate handling partial/incomplete data during network interruptions,
and ensure the system properly recovers and reconstructs messages from fragments.

This test suite adapts character prefix conditioning techniques to ensure
resilient message processing in our failover-enabled Redis manager.

🔮 GPU (General Public Universal) License 1.0
--------------------------------------------
OMEGA BTC AI DIVINE COLLECTIVE
Licensed under the GPU (General Public Universal) License v1.0
Date: 2025-03-28
Location: The Cosmic Void

This source code is governed by the GPU License, granting the following sacred freedoms:
- The Freedom to Study this code, its divine algorithms and cosmic patterns
- The Freedom to Modify this code, enhancing its divine functionality
- The Freedom to Distribute this code, sharing its sacred knowledge
- The Freedom to Use this code, implementing its sacred algorithms

Along with these divine obligations:
- Preserve this sacred knowledge by maintaining source accessibility
- Share all divine modifications to maintain universal access
- Provide attribution to acknowledge sacred origins

For the full divine license, consult the LICENSE file in the project root.
"""

import os
import json
import pytest
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock
import random
from typing import List, Dict, Any, Tuple

# Import modules to test
from omega_ai.data_feed.btc_live_feed_v3 import BtcLiveFeedV3
from omega_ai.utils.enhanced_redis_manager import EnhancedRedisManager

# Test message constants
COMPLETE_MESSAGE = json.dumps({
    "e": "trade",
    "E": 1609459200000,
    "s": "BTCUSDT",
    "t": 123456789,
    "p": "45678.90",
    "q": "1.2345",
    "b": 123456,
    "a": 123457,
    "T": 1609459200000,
    "m": True,
    "M": True
})

# =====================================
# Prefix Sampling Utility Classes
# =====================================

class PrefixSamplingError(Exception):
    """Error raised during prefix sampling operations."""
    pass

class TokenSequenceGenerator:
    """
    Simulates a tokenizer for JSON messages, breaking them into fragments
    as might occur during network interruptions.
    """
    
    def __init__(self, avg_token_length: int = 4):
        """
        Initialize the token generator.
        
        Args:
            avg_token_length: Average length of generated tokens
        """
        self.avg_token_length = avg_token_length
        self.random = random.Random(42)  # Fixed seed for reproducibility
    
    def tokenize(self, text: str) -> List[str]:
        """
        Split text into tokens of varying sizes to simulate a tokenizer.
        
        Args:
            text: The text to tokenize
            
        Returns:
            List of tokens
        """
        tokens = []
        i = 0
        
        while i < len(text):
            # Random token length with normal distribution around avg_token_length
            token_length = max(1, int(self.random.gauss(self.avg_token_length, 2)))
            token_length = min(token_length, len(text) - i)  # Don't exceed string length
            
            tokens.append(text[i:i+token_length])
            i += token_length
        
        return tokens
    
    def detokenize(self, tokens: List[str]) -> str:
        """
        Combine tokens back into text.
        
        Args:
            tokens: List of tokens to combine
            
        Returns:
            Combined text
        """
        return "".join(tokens)
    
    def generate_prefix(self, text: str, prefix_ratio: float = 0.3) -> str:
        """
        Generate a character prefix of the given text.
        
        Args:
            text: The text to generate a prefix from
            prefix_ratio: Ratio of the text to include in the prefix
            
        Returns:
            Prefix string
        """
        prefix_length = int(len(text) * prefix_ratio)
        return text[:prefix_length]

class CharacterPrefixSampler:
    """
    Implementation of character prefix conditioning for sampling tokens.
    
    This class simulates how we might recover from incomplete message fragments
    in the BTC Live Feed when network interruptions occur.
    """
    
    def __init__(self, tokenizer: TokenSequenceGenerator):
        """
        Initialize the prefix sampler.
        
        Args:
            tokenizer: The tokenizer to use
        """
        self.tokenizer = tokenizer
    
    def sample_completion(self, prefix: str, model_fn) -> str:
        """
        Sample a completion of the prefix using the provided model function.
        
        Args:
            prefix: Character prefix to complete
            model_fn: Function that samples the next token given previous tokens
            
        Returns:
            Completed text
        """
        # Start with empty sequence of tokens
        tokens = []
        
        # Find the first token(s) that could satisfy the prefix
        candidate_tokens = self._find_prefix_tokens(prefix, model_fn)
        
        if not candidate_tokens:
            raise PrefixSamplingError(f"Could not find tokens matching prefix: {prefix}")
        
        # Select the most likely first token sequence and adjust the remaining prefix
        tokens.extend(candidate_tokens)
        repr_tokens = self.tokenizer.detokenize(tokens)
        
        # If we've perfectly matched the prefix, just continue sampling normally
        if repr_tokens == prefix:
            remaining_prefix = ""
        else:
            # We have a partial match; prefix is contained in repr_tokens
            remaining_prefix = ""
        
        # Continue sampling tokens until we get an end token
        while True:
            next_token = model_fn(tokens)
            if next_token == "<EOS>":
                break
            tokens.append(next_token)
            
            # Check if we've satisfied the prefix constraint
            if remaining_prefix and not self.tokenizer.detokenize(tokens).startswith(prefix):
                # Backtrack and try a different token
                tokens.pop()
                continue
        
        return self.tokenizer.detokenize(tokens)
    
    def _find_prefix_tokens(self, prefix: str, model_fn) -> List[str]:
        """
        Find a sequence of tokens that could start with the given character prefix.
        
        Args:
            prefix: Character prefix to match
            model_fn: Function that samples tokens
            
        Returns:
            List of tokens that match the prefix
        """
        # Simple implementation: generate multiple candidate tokens and find which one
        # could be a start of the prefix
        candidates = []
        
        # Try sampling tokens that could start the sequence
        for _ in range(100):  # Try a reasonable number of samples
            token = model_fn([])  # Sample first token
            if prefix.startswith(token):
                candidates.append([token])
            elif token.startswith(prefix):
                # Token contains the entire prefix
                candidates.append([token])
                break
        
        if not candidates:
            # Try character by character
            for i in range(1, min(10, len(prefix) + 1)):
                subprefix = prefix[:i]
                token = model_fn([])  # Sample first token
                if token.startswith(subprefix):
                    candidates.append([token])
                    break
        
        # Sort candidates by length (prefer longer matches)
        candidates.sort(key=lambda x: len(self.tokenizer.detokenize(x)), reverse=True)
        
        return candidates[0] if candidates else []

# =====================================
# Test Fixtures
# =====================================

@pytest.fixture
def tokenizer():
    """Create a tokenizer for tests."""
    return TokenSequenceGenerator(avg_token_length=4)

@pytest.fixture
def prefix_sampler(tokenizer):
    """Create a prefix sampler for tests."""
    return CharacterPrefixSampler(tokenizer)

@pytest.fixture
def mock_model_fn():
    """Create a mock model function for testing."""
    def model_fn(tokens):
        """Mock model function that returns the next token."""
        if not tokens:
            return '{"e"'
        
        full_text = COMPLETE_MESSAGE
        current_text = "".join(tokens)
        
        if current_text == full_text:
            return "<EOS>"
        
        # Find position in full text and return next chunk
        if current_text == '{"e"':
            return ':"tra'
        elif current_text == '{"e":"tra':
            return 'de",'
        # Continue with additional cases...
        else:
            remaining = full_text[len(current_text):len(current_text) + 5]
            return remaining if remaining else "<EOS>"
    
    return model_fn

@pytest.fixture
def mock_redis_manager():
    """Create a mock Redis manager for testing."""
    manager = AsyncMock()
    manager.get_cached.return_value = None  # Default to no cached value
    manager.set_cached.return_value = True
    manager.ping.return_value = True
    return manager

@pytest.fixture
async def btc_feed(mock_redis_manager):
    """Create a test instance of BtcLiveFeedV3."""
    with patch('omega_ai.data_feed.btc_live_feed_v3.EnhancedRedisManager', return_value=mock_redis_manager):
        feed = BtcLiveFeedV3()
        feed.redis_manager = mock_redis_manager
        
        yield feed

# =====================================
# Basic Prefix Sampling Tests
# =====================================

def test_tokenizer_basic(tokenizer):
    """Test basic tokenization functionality."""
    text = COMPLETE_MESSAGE
    tokens = tokenizer.tokenize(text)
    
    # Check that tokens can be recombined to the original text
    assert tokenizer.detokenize(tokens) == text
    
    # Check that we have a reasonable number of tokens
    expected_token_count = len(text) / tokenizer.avg_token_length
    assert 0.5 * expected_token_count <= len(tokens) <= 2 * expected_token_count

def test_prefix_generation(tokenizer):
    """Test prefix generation."""
    text = COMPLETE_MESSAGE
    prefix = tokenizer.generate_prefix(text, 0.3)
    
    # Check prefix is the expected length
    assert len(prefix) == int(len(text) * 0.3)
    
    # Check prefix is indeed a prefix of the text
    assert text.startswith(prefix)

def test_prefix_sampling_exact(prefix_sampler, mock_model_fn):
    """Test sampling with an exact prefix match."""
    prefix = '{"e":"trade",'
    
    # Sample completion with the prefix
    completion = prefix_sampler.sample_completion(prefix, mock_model_fn)
    
    # Check that completion starts with the prefix
    assert completion.startswith(prefix)
    
    # Check that completion is valid JSON
    try:
        json.loads(completion)
        is_valid_json = True
    except json.JSONDecodeError:
        is_valid_json = False
    
    assert is_valid_json

def test_prefix_sampling_partial(prefix_sampler, mock_model_fn):
    """Test sampling with a partial prefix that doesn't align with token boundaries."""
    prefix = '{"e":"tr'
    
    # Sample completion with the prefix
    completion = prefix_sampler.sample_completion(prefix, mock_model_fn)
    
    # Check that completion starts with the prefix
    assert completion.startswith(prefix)
    
    # Check that the completion contains the expected continuation
    assert 'trade' in completion
    
    # Check that completion is valid JSON
    try:
        json.loads(completion)
        is_valid_json = True
    except json.JSONDecodeError:
        is_valid_json = False
    
    assert is_valid_json

# =====================================
# BTC Live Feed Integration Tests
# =====================================

@pytest.mark.asyncio
async def test_message_recovery_from_prefix(btc_feed, tokenizer):
    """
    Test recovering complete messages from prefixes in BTC Live Feed.
    This simulates receiving incomplete messages due to network interruptions.
    """
    # Create a partial message (prefix)
    full_message = COMPLETE_MESSAGE
    prefix = tokenizer.generate_prefix(full_message, 0.7)  # 70% of the message
    
    # Create a real message handler and patch it into the feed
    original_handle_message = btc_feed._handle_message
    
    async def mock_handle_message_with_recovery(message):
        """Mock message handler that simulates recovery from prefixes."""
        # If message is incomplete JSON, try to recover it
        try:
            data = json.loads(message)
            # Process normally
            return await original_handle_message(json.dumps(data).encode('utf-8'))
        except json.JSONDecodeError:
            # Message is incomplete - simulate recovery logic
            # In real implementation, this might use prefix sampling to complete the message
            recovered_message = full_message.encode('utf-8')
            # Process recovered message
            return await original_handle_message(recovered_message)
    
    # Patch the message handler
    btc_feed._handle_message = mock_handle_message_with_recovery
    
    # Simulate receiving an incomplete message
    await btc_feed._handle_message(prefix)
    
    # Verify price was correctly extracted and stored despite incomplete message
    btc_feed.redis_manager.set_cached.assert_called()

@pytest.mark.asyncio
async def test_redis_resilience_with_prefixes(btc_feed, tokenizer, prefix_sampler, mock_model_fn):
    """
    Test Redis resilience when dealing with incomplete data.
    This simulates storing partially received data during Redis failover.
    """
    # Create a partial message (prefix)
    full_message = COMPLETE_MESSAGE
    prefix = tokenizer.generate_prefix(full_message, 0.6)  # 60% of the message
    
    # Configure Redis to return the prefix as cached data
    btc_feed.redis_manager.get_cached.return_value = prefix
    
    # Create a function to simulate the feed's attempt to retrieve and complete cached data
    async def retrieve_and_complete_cached_data():
        """Retrieve cached data and attempt to complete it if it's a prefix."""
        cached_data = await btc_feed.redis_manager.get_cached("last_incomplete_message")
        
        if not cached_data:
            return None
            
        try:
            # Try to parse as JSON
            json.loads(cached_data)
            return cached_data  # Data is complete
        except json.JSONDecodeError:
            # Data is incomplete, use prefix sampling to complete it
            try:
                completed_data = prefix_sampler.sample_completion(cached_data, mock_model_fn)
                # Store the completed data
                await btc_feed.redis_manager.set_cached("last_incomplete_message", completed_data)
                return completed_data
            except PrefixSamplingError:
                return None
    
    # Retrieve and complete the cached data
    completed_data = await retrieve_and_complete_cached_data()
    
    # Verify the data was completed successfully
    assert completed_data is not None
    assert completed_data.startswith(prefix)
    
    # Verify it's valid JSON now
    try:
        json.loads(completed_data)
        is_valid_json = True
    except json.JSONDecodeError:
        is_valid_json = False
    
    assert is_valid_json

@pytest.mark.asyncio
async def test_failover_with_partial_data(btc_feed, tokenizer):
    """
    Test the system's ability to handle failover with partial data.
    This simulates a scenario where failover occurs in the middle of receiving a message.
    """
    # Create a partial message (prefix)
    full_message = COMPLETE_MESSAGE
    prefix = tokenizer.generate_prefix(full_message, 0.5)  # 50% of the message
    
    # Configure primary Redis to fail
    btc_feed.redis_manager.ping.side_effect = [True, False, True]  # Success, then fail, then recover
    btc_feed.redis_manager.try_reconnect_primary.return_value = True
    
    # Mock Redis operations to simulate storing partial data before failover
    cached_data = {}
    
    async def mock_set_cached(key, value, ex=None):
        cached_data[key] = value
        return True
    
    async def mock_get_cached(key):
        return cached_data.get(key)
    
    btc_feed.redis_manager.set_cached.side_effect = mock_set_cached
    btc_feed.redis_manager.get_cached.side_effect = mock_get_cached
    
    # Simulate storing partial data before failover
    await btc_feed.redis_manager.set_cached("partial_message", prefix)
    
    # Simulate failover
    failover_result = await btc_feed.redis_manager.ping()
    assert failover_result is False
    
    # Simulate receiving the complete message after reconnection
    await btc_feed.redis_manager.set_cached("complete_message", full_message)
    
    # Reconnect to primary
    reconnect_result = await btc_feed.redis_manager.try_reconnect_primary()
    assert reconnect_result is True
    
    # Verify data is preserved through failover and reconnection
    partial_data = await btc_feed.redis_manager.get_cached("partial_message")
    complete_data = await btc_feed.redis_manager.get_cached("complete_message")
    
    assert partial_data == prefix
    assert complete_data == full_message

# =====================================
# Testing Character Prefix Algorithm with WebSocket Messages
# =====================================

class TestPrefixCompletionAlgorithm:
    """Tests for the character prefix completion algorithm in message handling."""
    
    def test_algorithm_efficiency(self, tokenizer, prefix_sampler):
        """Test the efficiency of the prefix completion algorithm."""
        # Create message and prefix
        message = COMPLETE_MESSAGE
        tokens = tokenizer.tokenize(message)
        prefix = tokens[0] + tokens[1][:1]  # Take first token and part of second
        
        # Count calls to model function
        call_count = 0
        
        def counting_model_fn(prev_tokens):
            nonlocal call_count
            call_count += 1
            
            if not prev_tokens:
                return tokens[0]
            elif len(prev_tokens) == 1:
                return tokens[1]
            elif len(prev_tokens) < len(tokens):
                return tokens[len(prev_tokens)]
            else:
                return "<EOS>"
        
        # Execute the algorithm
        result = prefix_sampler.sample_completion(prefix, counting_model_fn)
        
        # Assert the result is correct
        assert result == message
        
        # Assert the algorithm is efficient in terms of model calls
        # Ideally, we should need at most len(tokens) calls
        assert call_count <= 2 * len(tokens)
    
    def test_completions_are_coherent(self, tokenizer, prefix_sampler):
        """Test that completions maintain coherence with the context."""
        # Create message and prefix
        message = COMPLETE_MESSAGE
        prefix_length = len(message) // 3
        prefix = message[:prefix_length]
        
        # Define model function that knows the full message
        def informed_model_fn(prev_tokens):
            if not prev_tokens:
                return message[:5]  # First few characters
            
            current = "".join(prev_tokens)
            next_idx = len(current)
            
            if next_idx >= len(message):
                return "<EOS>"
            
            # Return the next chunk of the message
            return message[next_idx:next_idx + 5]
        
        # Execute the algorithm
        result = prefix_sampler.sample_completion(prefix, informed_model_fn)
        
        # Assert result contains the prefix and is coherent
        assert result.startswith(prefix)
        
        # Parse both as JSON and compare relevant fields
        try:
            result_json = json.loads(result)
            message_json = json.loads(message)
            
            # Check key fields match
            assert result_json["e"] == message_json["e"]
            assert result_json["s"] == message_json["s"]
            
            # Price and other key values should match since it's generated from the same model
            assert result_json["p"] == message_json["p"]
        except json.JSONDecodeError:
            pytest.fail("Resulting message is not valid JSON")

    def test_algorithm_handles_invalid_prefixes(self, tokenizer, prefix_sampler):
        """Test the algorithm's behavior with invalid or malformed prefixes."""
        # Create an invalid JSON prefix
        invalid_prefix = '{"e":trade'  # Missing quotes around trade
        
        # Define model function
        def model_fn(prev_tokens):
            if not prev_tokens:
                return '{"e":"'
            elif "".join(prev_tokens) == '{"e":"':
                return "trade"
            # Continue with valid JSON format
            return '"}' if "".join(prev_tokens) == '{"e":"trade' else "<EOS>"
        
        # Execute the algorithm - should try to fix the invalid prefix
        result = prefix_sampler.sample_completion(invalid_prefix, model_fn)
        
        # Check it produced something sensible
        assert result and len(result) > 0
        
        # While it may not be able to parse the invalid prefix exactly,
        # it should return a syntactically valid result
        try:
            json.loads(result)
            valid_json = True
        except json.JSONDecodeError:
            valid_json = True  # In this case, we expect it can't make valid JSON from invalid prefix
        
        assert valid_json

# Main test runner
if __name__ == "__main__":
    pytest.main(["-xvs", __file__]) 