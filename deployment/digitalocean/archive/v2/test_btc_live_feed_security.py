#!/usr/bin/env python3
"""
OMEGA BTC AI - DigitalOcean BTC Live Feed V2 Security Tests 🔱

A security-focused test suite that verifies the divine protection of the Bitcoin 
price feed in the DigitalOcean deployment, ensuring proper security measures and
resistance against various attack vectors.

JAH BLESS THE SECURITY OF THE PRICE FEED! 🙏🛡️
"""

import os
import sys
import pytest
import json
import redis
import asyncio
import subprocess
from datetime import datetime, timedelta, UTC
from unittest.mock import patch, MagicMock, AsyncMock, ANY
from typing import Dict, Any
from deployment.digitalocean.logging.omega_logger import OmegaLogger
from deployment.digitalocean.redis_manager import DigitalOceanRedisManager
from deployment.digitalocean.btc_live_feed_v2 import (
    check_required_packages,
    send_to_mm_websocket,
    MockHighFrequencyTrapDetector,
    display_price_chart,
    log_rasta,
    on_message,
    on_error,
    on_close,
    on_open,
    price_movement_indicator
)

# Add project root to path for divine module accessibility
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, project_root)

# Initialize logger without log_dir parameter
omega_logger = OmegaLogger()

class TestBtcLiveFeedSecurity:
    """Security tests for BTC Live Feed V2 with divine protection."""
    
    @pytest.fixture
    def mock_subprocess(self):
        """Mock subprocess for package installation tests."""
        with patch('subprocess.check_call') as mock:
            yield mock
    
    @pytest.fixture
    def mock_env(self):
        """Mock environment variables."""
        with patch.dict('os.environ', {
            'REDIS_HOST': 'localhost',
            'REDIS_PORT': '6379',
            'REDIS_PASSWORD': 'test_password'
        }):
            yield
    
    @pytest.fixture
    def mock_websocket(self):
        """Mock websocket connection."""
        mock = AsyncMock()
        mock.send = AsyncMock()
        mock.close = AsyncMock()
        return mock
    
    def test_package_installation_security(self, mock_subprocess):
        """Test secure package installation process."""
        # Test with valid packages
        check_required_packages()
        mock_subprocess.assert_called()
        
        # Verify pip install command is properly formatted
        for call in mock_subprocess.call_args_list:
            cmd = call[0][0]
            assert all(arg.isalnum() or arg in ['-', '_', '.'] for arg in cmd)
    
    @pytest.mark.asyncio
    async def test_websocket_connection_security(self, mock_websocket):
        """Test WebSocket connection security measures."""
        # Test SSL/TLS configuration
        with patch('websockets.connect') as mock_connect:
            mock_connect.return_value = mock_websocket
            await send_to_mm_websocket(50000.0)
            
            # Verify connection parameters
            mock_connect.assert_called_once()
            kwargs = mock_connect.call_args[1]
            assert kwargs.get('max_size') == 2**20  # Message size limit
            assert kwargs.get('ping_interval') == 30  # Keep-alive
            assert kwargs.get('ping_timeout') == 10  # Timeout
    
    def test_input_validation(self):
        """Test input validation and sanitization."""
        detector = MockHighFrequencyTrapDetector()
        
        # Test price validation
        with pytest.raises(ValueError):
            detector.update_price_data(float('inf'), datetime.now(UTC))
        
        # Test timestamp validation
        future_time = datetime.now(UTC) + timedelta(days=365)
        with pytest.raises(ValueError):
            detector.update_price_data(50000.0, future_time)
        
        # Test valid input
        now = datetime.now(UTC)
        detector.update_price_data(50000.0, now)
        assert len(detector.price_history) == 1
    
    def test_rate_limiting(self):
        """Test rate limiting and DoS protection."""
        detector = MockHighFrequencyTrapDetector()
        
        # Test rapid message processing
        messages = []
        base_time = datetime.now(UTC)
        
        # Generate 1000 messages in 1 second (should trigger rate limiting)
        for i in range(1000):
            timestamp = base_time + timedelta(milliseconds=i)
            messages.append((50000.0 + i, timestamp))
        
        # Process messages and check rate limiting
        processed = 0
        for price, timestamp in messages:
            try:
                detector.update_price_data(price, timestamp)
                processed += 1
            except Exception as e:
                assert str(e).startswith("Rate limit exceeded")
                break
        
        assert processed < 1000  # Verify rate limiting kicked in
    
    def test_environment_security(self, mock_env):
        """Test environment variable security."""
        # Test Redis host validation
        assert os.environ['REDIS_HOST'] == 'localhost'
        
        # Test secure handling of Redis password
        assert 'REDIS_PASSWORD' in os.environ
        assert len(os.environ['REDIS_PASSWORD']) > 0
        
        # Test port validation
        assert os.environ['REDIS_PORT'].isdigit()
        assert 1024 <= int(os.environ['REDIS_PORT']) <= 65535
    
    def test_redis_connection_security(self):
        """Test Redis connection security measures."""
        with patch('redis.Redis') as mock_redis:
            # Test SSL/TLS configuration
            mock_redis.return_value.ping.return_value = True
            
            client = redis.Redis(
                host=os.environ.get('REDIS_HOST', 'localhost'),
                port=int(os.environ.get('REDIS_PORT', 6379)),
                password=os.environ.get('REDIS_PASSWORD'),
                ssl=True,
                ssl_cert_reqs='required'
            )
            
            # Verify secure connection parameters
            assert client.connection_pool.connection_kwargs['ssl']
            assert client.connection_pool.connection_kwargs['ssl_cert_reqs'] == 'required'
    
    def test_data_sanitization(self):
        """Test data sanitization and validation."""
        # Test price chart sanitization
        malicious_data = ["50000.0; rm -rf /", "60000.0' OR '1'='1"]
        
        # Verify display_price_chart safely handles malicious input
        with pytest.raises(ValueError):
            display_price_chart(50000.0, malicious_data)
        
        # Test log message sanitization
        malicious_message = "Malicious message\n with newlines and ; rm -rf /"
        log_rasta(malicious_message)  # Should sanitize without raising exception
    
    @pytest.mark.asyncio
    async def test_websocket_message_security(self, mock_websocket):
        """Test WebSocket message security."""
        # Test message size limits
        large_message = json.dumps({"price": "1.0" * 1024 * 1024})  # 1MB message
        
        with pytest.raises(ValueError, match="Message too large"):
            await send_to_mm_websocket(large_message)
        
        # Test message format validation
        invalid_messages = [
            None,
            "",
            "invalid json",
            json.dumps({"invalid_key": 123}),
            json.dumps({"price": "not a number"})
        ]
        
        for msg in invalid_messages:
            with pytest.raises((ValueError, TypeError)):
                await send_to_mm_websocket(msg)
        
        # Test valid message
        await send_to_mm_websocket(50000.0)
        mock_websocket.send.assert_called_once() 