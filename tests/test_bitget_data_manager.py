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
Tests for BitgetDataManager

This module tests the BitgetDataManager class to ensure it properly
handles BitGet position data and provides proper error handling.
"""

import pytest
import unittest.mock as mock
import os
import sys
from datetime import datetime
import json

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the class to test
from bitget_data_manager import BitgetDataManager

class TestBitgetDataManager:
    """Tests for the BitgetDataManager class."""
    
    @pytest.fixture
    def manager(self):
        """Create a BitgetDataManager instance."""
        return BitgetDataManager()
    
    @pytest.fixture
    def mock_response(self):
        """Create a mock HTTP response."""
        mock_resp = mock.MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "code": "00000",
            "data": [
                {
                    "symbol": "BTCUSDT_UMCBL",
                    "holdSide": "long",
                    "total": 0.1,
                    "leverageEr": "10",
                    "margin": 500.0,
                    "averageOpenPrice": 50000.0,
                    "marginRatio": 0.2,
                    "marginMode": "crossed",
                    "unrealizedPL": 100.0,
                    "liquidationPrice": 45000.0,
                    "achievedProfits": 0.0,
                    "marketPrice": 51000.0
                }
            ],
            "msg": "success"
        }
        return mock_resp
    
    @pytest.fixture
    def mock_account_response(self):
        """Create a mock HTTP response for account data."""
        mock_resp = mock.MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "code": "00000",
            "data": {
                "accountEquity": "1000.0",
                "available": "500.0",
                "locked": "500.0"
            },
            "msg": "success"
        }
        return mock_resp
    
    def test_init(self, manager):
        """Test the initialization of BitgetDataManager."""
        assert manager.api_key is not None
        assert manager.api_secret is not None
        assert manager.api_passphrase is not None
        assert manager.last_positions == []
    
    def test_generate_signature(self, manager):
        """Test signature generation."""
        timestamp = "1234567890"
        data = "test_data"
        signature = manager._generate_signature(timestamp, data)
        assert signature is not None
        assert isinstance(signature, str)
    
    def test_get_positions_success(self, manager, mock_response, mock_account_response):
        """Test getting positions successfully."""
        with mock.patch('requests.get', side_effect=[mock_response, mock_account_response]):
            result = manager.get_positions()
            
            # Check the result structure
            assert "positions" in result
            assert "timestamp" in result
            assert "account_balance" in result
            
            # Check the position data
            assert len(result["positions"]) == 1
            position = result["positions"][0]
            assert position["symbol"] == "BTCUSDT_UMCBL"
            assert position["side"] == "long"
            assert float(position["contracts"]) == 0.1
            assert float(position["entryPrice"]) == 50000.0
            assert float(position["markPrice"]) == 51000.0
            assert float(position["unrealizedPnl"]) == 100.0
            
            # Check account balance
            assert float(result["account_balance"]) == 1000.0
    
    def test_get_positions_api_failure(self, manager):
        """Test error handling when the API request fails."""
        with mock.patch('requests.get', side_effect=Exception("API Error")):
            result = manager.get_positions()
            
            # Check the error response
            assert "error" in result
            assert "API Error" in result["error"]
    
    def test_get_positions_error_response(self, manager):
        """Test handling error responses from the API."""
        error_response = mock.MagicMock()
        error_response.status_code = 401
        error_response.json.return_value = {
            "code": "40102", 
            "msg": "Invalid signature"
        }
        
        with mock.patch('requests.get', return_value=error_response):
            result = manager.get_positions()
            
            # Check the error response
            assert "error" in result
            assert "401" in result["error"]
            assert "Invalid signature" in result["error"]
    
    def test_detect_position_changes_no_previous(self, manager):
        """Test detecting changes with no previous positions."""
        # Set up current positions
        current_positions = [
            {"symbol": "BTCUSDT_UMCBL", "side": "long", "contracts": "0.1"}
        ]
        
        # Clear last positions
        manager.last_positions = []
        
        # Detect changes
        changes = manager.detect_position_changes(current_positions)
        
        # All current positions should be new
        assert len(changes["new"]) == 1
        assert changes["new"][0]["symbol"] == "BTCUSDT_UMCBL"
        assert len(changes["closed"]) == 0
        assert len(changes["changed"]) == 0
        
        # Last positions should be updated
        assert manager.last_positions == current_positions
    
    def test_detect_position_changes_with_previous(self, manager):
        """Test detecting changes with previous positions."""
        # Set up previous positions
        manager.last_positions = [
            {"symbol": "BTCUSDT_UMCBL", "side": "long", "contracts": "0.1"},
            {"symbol": "ETHUSDT_UMCBL", "side": "short", "contracts": "1.0"}
        ]
        
        # Set up current positions
        current_positions = [
            {"symbol": "BTCUSDT_UMCBL", "side": "long", "contracts": "0.2"},  # Changed
            {"symbol": "SOLUSDT_UMCBL", "side": "long", "contracts": "5.0"}   # New
        ]
        
        # Detect changes
        changes = manager.detect_position_changes(current_positions)
        
        # Check new positions
        assert len(changes["new"]) == 1
        assert changes["new"][0]["symbol"] == "SOLUSDT_UMCBL"
        
        # Check closed positions
        assert len(changes["closed"]) == 1
        assert changes["closed"][0]["symbol"] == "ETHUSDT_UMCBL"
        
        # Check changed positions
        assert len(changes["changed"]) == 1
        assert changes["changed"][0]["position"]["symbol"] == "BTCUSDT_UMCBL"
        assert changes["changed"][0]["prev_contracts"] == "0.1"
        assert changes["changed"][0]["position"]["contracts"] == "0.2"
        
        # Last positions should be updated
        assert manager.last_positions == current_positions
    
    def test_detect_position_changes_no_changes(self, manager):
        """Test when there are no changes between position updates."""
        # Set up previous positions
        positions = [
            {"symbol": "BTCUSDT_UMCBL", "side": "long", "contracts": "0.1"}
        ]
        manager.last_positions = positions.copy()
        
        # Detect changes with same positions
        changes = manager.detect_position_changes(positions)
        
        # No changes should be detected
        assert len(changes["new"]) == 0
        assert len(changes["closed"]) == 0
        assert len(changes["changed"]) == 0 