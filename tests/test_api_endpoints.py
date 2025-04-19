#!/usr/bin/env python3

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
Test suite for OMEGA BTC AI Dashboard API endpoints
JAH BLESS! 🙏
"""

import pytest
import requests
import json
from datetime import datetime
import sys
from typing import Dict, Any
import time
from unittest.mock import patch, MagicMock

# Import the functions we want to test
from test_api_endpoints import (
    print_header,
    print_success,
    print_error,
    print_info,
    format_response,
    check_endpoint,
    main,
    ENDPOINTS
)

# Test data
MOCK_RESPONSE = {
    "status": "ok",
    "data": {
        "btc_price": 65000.00,
        "trap_probability": 0.75,
        "position": {
            "has_position": True,
            "entry_price": 64000.00
        }
    }
}

def test_print_header(capsys):
    """Test print_header function"""
    print_header("Test Header")
    captured = capsys.readouterr()
    assert "🔍 Test Header" in captured.out
    assert "=" * 50 in captured.out

def test_print_success(capsys):
    """Test print_success function"""
    print_success("Test Success")
    captured = capsys.readouterr()
    assert "✅ Test Success" in captured.out

def test_print_error(capsys):
    """Test print_error function"""
    print_error("Test Error")
    captured = capsys.readouterr()
    assert "❌ Test Error" in captured.out

def test_print_info(capsys):
    """Test print_info function"""
    print_info("Test Info")
    captured = capsys.readouterr()
    assert "ℹ️  Test Info" in captured.out

def test_format_response():
    """Test format_response function"""
    test_data = {"key": "value"}
    formatted = format_response(test_data)
    assert isinstance(formatted, str)
    assert "key" in formatted
    assert "value" in formatted

@pytest.mark.parametrize("status_code,expected", [
    (200, True),
    (404, False),
    (500, False)
])
def test_check_endpoint_status_codes(status_code, expected):
    """Test check_endpoint function with different status codes"""
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_response.json.return_value = MOCK_RESPONSE
    mock_response.text = "Test Response"
    
    with patch('requests.get', return_value=mock_response):
        success = check_endpoint("/test", "test")
        assert success is expected

def test_check_endpoint_connection_error():
    """Test check_endpoint function with connection error"""
    with patch('requests.get', side_effect=requests.exceptions.ConnectionError):
        success = check_endpoint("/test", "test")
        assert success is False

def test_check_endpoint_timeout():
    """Test check_endpoint function with timeout error"""
    with patch('requests.get', side_effect=requests.exceptions.Timeout):
        success = check_endpoint("/test", "test")
        assert success is False

def test_check_endpoint_general_error():
    """Test check_endpoint function with general error"""
    with patch('requests.get', side_effect=Exception("Test Error")):
        success = check_endpoint("/test", "test")
        assert success is False

def test_main_success():
    """Test main function with successful endpoints"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_RESPONSE
    
    with patch('requests.get', return_value=mock_response):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

def test_main_failure():
    """Test main function with failed endpoints"""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    
    with patch('requests.get', return_value=mock_response):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

def test_endpoints_configuration():
    """Test that all required endpoints are configured"""
    required_endpoints = {
        "health", "trap_probability", "position", 
        "btc_price", "data"
    }
    assert set(ENDPOINTS.keys()) == required_endpoints
    for endpoint in ENDPOINTS.values():
        assert endpoint.startswith("/api/")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=../test_api_endpoints.py", "--cov-report=term-missing", "--cov-fail-under=100"])