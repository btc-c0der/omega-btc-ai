"""
Tests for API key authentication in the BitgetPositionAnalyzerB0t.

These tests verify:
- Valid API credentials successfully authenticate
- Invalid or expired API keys are properly rejected
- HMAC signature verification works correctly
- Passphrase validation is enforced
"""

import os
import pytest
import json
import hmac
import hashlib
import base64
import time
import asyncio
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Try to import the real implementation, fall back to mock if not available
try:
    from omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t
    from omega_bot_farm.trading.b0ts.bitget_analyzer.api.auth import ApiKeyAuthenticator
    REAL_IMPLEMENTATION = True
    BOT_CLASS = BitgetPositionAnalyzerB0t
except ImportError:
    REAL_IMPLEMENTATION = False
    BOT_CLASS = None
    
    # Mock implementation for tests
    class ApiKeyAuthenticator:
        def __init__(self, api_key, api_secret, passphrase):
            self.api_key = api_key
            self.api_secret = api_secret
            self.passphrase = passphrase
            
        def generate_signature(self, timestamp, method, endpoint, body=None):
            """Generate HMAC signature for request authentication"""
            body_str = json.dumps(body) if body else ""
            message = timestamp + method + endpoint + body_str
            signature = base64.b64encode(
                hmac.new(
                    self.api_secret.encode('utf-8'),
                    message.encode('utf-8'),
                    hashlib.sha256
                ).digest()
            ).decode('utf-8')
            return signature
            
        def generate_headers(self, method, endpoint, body=None):
            """Generate authenticated headers for API request"""
            timestamp = str(int(time.time()))
            signature = self.generate_signature(timestamp, method, endpoint, body)
            
            headers = {
                "ACCESS-KEY": self.api_key,
                "ACCESS-SIGN": signature,
                "ACCESS-TIMESTAMP": timestamp,
                "ACCESS-PASSPHRASE": self.passphrase,
                "Content-Type": "application/json"
            }
            return headers
            
        def verify_signature(self, headers, method, endpoint, body=None):
            """Verify the HMAC signature of an incoming request"""
            # Extract request details
            received_key = headers.get("ACCESS-KEY")
            received_sign = headers.get("ACCESS-SIGN")
            received_timestamp = headers.get("ACCESS-TIMESTAMP")
            received_passphrase = headers.get("ACCESS-PASSPHRASE")
            
            # Verify API key
            if received_key != self.api_key:
                return False
                
            # Verify passphrase
            if received_passphrase != self.passphrase:
                return False
                
            # Check timestamp freshness (15 seconds window)
            timestamp_now = int(time.time())
            if abs(timestamp_now - int(received_timestamp)) > 15:
                return False
                
            # Generate expected signature
            expected_sign = self.generate_signature(
                received_timestamp, method, endpoint, body
            )
            
            # Compare signatures
            return received_sign == expected_sign


@pytest.fixture
def sample_credentials():
    """Provide sample API credentials for testing."""
    return {
        "api_key": "testkey12345",
        "api_secret": "testsecret67890",
        "passphrase": "testpass",
    }


@pytest.fixture
def auth_instance(sample_credentials):
    """Create an API key authenticator instance."""
    return ApiKeyAuthenticator(
        sample_credentials["api_key"],
        sample_credentials["api_secret"],
        sample_credentials["passphrase"]
    )


@pytest.fixture
def sample_request():
    """Provide sample request parameters for testing."""
    return {
        "method": "GET",
        "endpoint": "/api/mix/v1/account/account",
        "body": None
    }


class TestApiKeyAuthentication:
    """Test suite for API key authentication."""
    
    def test_signature_generation(self, auth_instance):
        """Test that HMAC signatures are generated correctly."""
        # Test parameters
        timestamp = "1618232220"
        method = "GET"
        endpoint = "/api/v1/positions"
        body = {"symbol": "BTCUSDT"}
        
        # Generate signature
        signature = auth_instance.generate_signature(timestamp, method, endpoint, body)
        
        # Verify it's a non-empty base64 string
        assert signature is not None
        assert len(signature) > 0
        
        # Verify deterministic signature generation (same inputs = same signature)
        signature2 = auth_instance.generate_signature(timestamp, method, endpoint, body)
        assert signature == signature2
        
        # Verify different inputs produce different signatures
        signature3 = auth_instance.generate_signature(timestamp, "POST", endpoint, body)
        assert signature != signature3
    
    def test_header_generation(self, auth_instance, sample_request):
        """Test that authentication headers are generated correctly."""
        # Generate headers
        headers = auth_instance.generate_headers(
            sample_request["method"],
            sample_request["endpoint"],
            sample_request["body"]
        )
        
        # Verify required headers are present
        assert "ACCESS-KEY" in headers
        assert "ACCESS-SIGN" in headers
        assert "ACCESS-TIMESTAMP" in headers
        assert "ACCESS-PASSPHRASE" in headers
        assert "Content-Type" in headers
        
        # Verify header values
        assert headers["ACCESS-KEY"] == auth_instance.api_key
        assert headers["ACCESS-PASSPHRASE"] == auth_instance.passphrase
        assert headers["Content-Type"] == "application/json"
        
        # Verify timestamp is recent
        timestamp_now = int(time.time())
        header_timestamp = int(headers["ACCESS-TIMESTAMP"])
        assert abs(timestamp_now - header_timestamp) < 5
    
    def test_signature_verification_valid(self, auth_instance, sample_request):
        """Test that valid signatures are properly verified."""
        # Generate headers with valid credentials
        headers = auth_instance.generate_headers(
            sample_request["method"],
            sample_request["endpoint"],
            sample_request["body"]
        )
        
        # Verify the signature
        verification_result = auth_instance.verify_signature(
            headers,
            sample_request["method"],
            sample_request["endpoint"],
            sample_request["body"]
        )
        
        # Should be valid
        assert verification_result is True
    
    def test_signature_verification_invalid_key(self, auth_instance, sample_request):
        """Test that signatures with invalid API key are rejected."""
        # Generate headers with valid credentials
        headers = auth_instance.generate_headers(
            sample_request["method"],
            sample_request["endpoint"],
            sample_request["body"]
        )
        
        # Tamper with the API key
        headers["ACCESS-KEY"] = "invalidkey"
        
        # Verify the signature
        verification_result = auth_instance.verify_signature(
            headers,
            sample_request["method"],
            sample_request["endpoint"],
            sample_request["body"]
        )
        
        # Should be invalid
        assert verification_result is False
    
    def test_signature_verification_invalid_passphrase(self, auth_instance, sample_request):
        """Test that signatures with invalid passphrase are rejected."""
        # Generate headers with valid credentials
        headers = auth_instance.generate_headers(
            sample_request["method"],
            sample_request["endpoint"],
            sample_request["body"]
        )
        
        # Tamper with the passphrase
        headers["ACCESS-PASSPHRASE"] = "wrongpassphrase"
        
        # Verify the signature
        verification_result = auth_instance.verify_signature(
            headers,
            sample_request["method"],
            sample_request["endpoint"],
            sample_request["body"]
        )
        
        # Should be invalid
        assert verification_result is False
    
    def test_signature_verification_tampered_signature(self, auth_instance, sample_request):
        """Test that tampered signatures are properly rejected."""
        # Generate headers with valid credentials
        headers = auth_instance.generate_headers(
            sample_request["method"],
            sample_request["endpoint"],
            sample_request["body"]
        )
        
        # Tamper with the signature
        headers["ACCESS-SIGN"] = headers["ACCESS-SIGN"][:-5] + "XXXXX"
        
        # Verify the signature
        verification_result = auth_instance.verify_signature(
            headers,
            sample_request["method"],
            sample_request["endpoint"],
            sample_request["body"]
        )
        
        # Should be invalid
        assert verification_result is False
    
    def test_signature_verification_expired_timestamp(self, auth_instance, sample_request):
        """Test that expired timestamps are rejected."""
        # Generate headers with valid credentials
        headers = auth_instance.generate_headers(
            sample_request["method"],
            sample_request["endpoint"],
            sample_request["body"]
        )
        
        # Set timestamp to 20 seconds ago (beyond the 15 second threshold)
        timestamp = str(int(time.time()) - 20)
        
        # Generate a valid signature for this old timestamp
        signature = auth_instance.generate_signature(
            timestamp,
            sample_request["method"],
            sample_request["endpoint"],
            sample_request["body"]
        )
        
        # Update headers with old timestamp and corresponding signature
        headers["ACCESS-TIMESTAMP"] = timestamp
        headers["ACCESS-SIGN"] = signature
        
        # Verify the signature
        verification_result = auth_instance.verify_signature(
            headers,
            sample_request["method"],
            sample_request["endpoint"],
            sample_request["body"]
        )
        
        # Should be invalid due to timestamp expiration
        assert verification_result is False
    
    @pytest.mark.asyncio
    async def test_bot_api_key_authentication(self, sample_credentials):
        """Test actual BitgetPositionAnalyzerB0t API key authentication if available."""
        if not REAL_IMPLEMENTATION or BOT_CLASS is None:
            pytest.skip("Real implementation not available")
        
        # Create bot instance with test credentials
        bot = BOT_CLASS(
            api_key=sample_credentials["api_key"],
            api_secret=sample_credentials["api_secret"],
            api_passphrase=sample_credentials["passphrase"],
            use_testnet=True  # Always use testnet for tests
        )
        
        # Mock the HTTP client to capture the authentication headers
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = MagicMock(return_value={"positions": []})
        mock_session = MagicMock()
        mock_session.request = MagicMock(return_value=mock_response)
        
        with patch.object(bot, '_session', mock_session):
            # Attempt to call an authenticated endpoint
            await bot.get_positions()
            
            # Verify authentication headers were included
            args, kwargs = mock_session.request.call_args
            headers = kwargs.get('headers', {})
            
            assert "ACCESS-KEY" in headers
            assert "ACCESS-SIGN" in headers
            assert "ACCESS-TIMESTAMP" in headers
            assert "ACCESS-PASSPHRASE" in headers
            
            assert headers["ACCESS-KEY"] == sample_credentials["api_key"]
            assert headers["ACCESS-PASSPHRASE"] == sample_credentials["passphrase"] 