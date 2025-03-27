"""
OMEGA BTC AI - BitGet API Test Suite
===================================

Test suite for BitGet production API endpoints.
Validates all endpoints used in our trading system.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import pytest
import os
import requests
import logging
from typing import Dict, Any
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
API_URL = "https://api.bitget.com"
SYMBOL = "BTCUSDT_UMCBL"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

@pytest.fixture(scope="session", autouse=True)
def load_env():
    """Load environment variables for testing."""
    load_dotenv()

def test_contracts_endpoint():
    """Test the contracts endpoint for symbol verification."""
    logger.info(f"{GREEN}Testing contracts endpoint...{RESET}")
    
    endpoint = "/api/mix/v1/market/contracts"
    params = {"productType": "umcbl"}
    
    try:
        response = requests.get(API_URL + endpoint, params=params)
        logger.info(f"Response: {response.text}")
        response.raise_for_status()
        data = response.json()
        
        assert data.get("code") == "00000", "API returned error code"
        assert data.get("data"), "No data in response"
        
        contracts = data["data"]
        symbol_exists = any(contract["symbol"] == SYMBOL for contract in contracts)
        assert symbol_exists, f"Symbol {SYMBOL} not found in available contracts"
        
        logger.info(f"{GREEN}✓ Contracts endpoint test passed{RESET}")
        
    except Exception as e:
        pytest.fail(f"Error testing contracts endpoint: {str(e)}")

def test_market_ticker():
    """Test the market ticker endpoint."""
    logger.info(f"{GREEN}Testing market ticker endpoint...{RESET}")
    
    endpoint = "/api/mix/v1/market/ticker"
    params = {"symbol": SYMBOL}
    
    try:
        response = requests.get(API_URL + endpoint, params=params)
        logger.info(f"Response: {response.text}")
        response.raise_for_status()
        data = response.json()
        
        assert data.get("code") == "00000", "API returned error code"
        assert data.get("data"), "No data in response"
        
        ticker = data["data"]
        assert "last" in ticker, "Ticker missing 'last' price"
        assert float(ticker["last"]) > 0, "Invalid ticker price"
        assert "high24h" in ticker, "Ticker missing 24h high"
        assert "low24h" in ticker, "Ticker missing 24h low"
        assert "baseVolume" in ticker, "Ticker missing base volume"
        
        logger.info(f"{GREEN}✓ Market ticker test passed{RESET}")
        
    except Exception as e:
        pytest.fail(f"Error testing market ticker: {str(e)}")

def test_orderbook():
    """Test the orderbook endpoint."""
    logger.info(f"{GREEN}Testing orderbook endpoint...{RESET}")
    
    endpoint = "/api/mix/v1/market/depth"
    params = {
        "symbol": SYMBOL,
        "limit": "100",
        "type": "step0"
    }
    
    try:
        response = requests.get(API_URL + endpoint, params=params)
        logger.info(f"Response: {response.text}")
        response.raise_for_status()
        data = response.json()
        
        assert data.get("code") == "00000", "API returned error code"
        assert data.get("data"), "No data in response"
        
        orderbook = data["data"]
        assert "bids" in orderbook, "Orderbook missing bids"
        assert "asks" in orderbook, "Orderbook missing asks"
        assert len(orderbook["bids"]) > 0, "No bid orders in orderbook"
        assert len(orderbook["asks"]) > 0, "No ask orders in orderbook"
        
        # Verify orderbook structure
        first_bid = orderbook["bids"][0]
        first_ask = orderbook["asks"][0]
        assert len(first_bid) >= 2, "Invalid bid order structure"
        assert len(first_ask) >= 2, "Invalid ask order structure"
        assert float(first_bid[0]) > 0, "Invalid bid price"
        assert float(first_ask[0]) > 0, "Invalid ask price"
        
        logger.info(f"{GREEN}✓ Orderbook test passed{RESET}")
        
    except Exception as e:
        pytest.fail(f"Error testing orderbook: {str(e)}")

def test_recent_trades():
    """Test the recent trades endpoint."""
    logger.info(f"{GREEN}Testing recent trades endpoint...{RESET}")
    
    endpoint = "/api/mix/v1/market/fills"
    params = {
        "symbol": SYMBOL,
        "limit": "100"
    }
    
    try:
        response = requests.get(API_URL + endpoint, params=params)
        logger.info(f"Response: {response.text}")
        response.raise_for_status()
        data = response.json()
        
        assert data.get("code") == "00000", "API returned error code"
        assert data.get("data"), "No data in response"
        
        trades = data["data"]
        assert len(trades) > 0, "No recent trades returned"
        
        # Verify trade structure
        first_trade = trades[0]
        assert "price" in first_trade, "Trade missing price"
        assert "size" in first_trade, "Trade missing size"
        assert "side" in first_trade, "Trade missing side"
        assert "timestamp" in first_trade, "Trade missing timestamp"
        
        logger.info(f"{GREEN}✓ Recent trades test passed{RESET}")
        
    except Exception as e:
        pytest.fail(f"Error testing recent trades: {str(e)}")

def test_market_candles():
    """Test the market candles endpoint."""
    logger.info(f"{GREEN}Testing market candles endpoint...{RESET}")
    
    import time
    current_time = int(time.time() * 1000)
    one_hour_ago = current_time - (60 * 60 * 1000)
    
    endpoint = "/api/mix/v1/market/candles"
    params = {
        "symbol": SYMBOL,
        "granularity": "60",
        "startTime": str(one_hour_ago),
        "endTime": str(current_time),
        "limit": "100"
    }
    
    try:
        response = requests.get(API_URL + endpoint, params=params)
        logger.info(f"Response: {response.text}")
        response.raise_for_status()
        candles = response.json()
        
        assert isinstance(candles, list), "Response should be a list of candles"
        assert len(candles) > 0, "No candles returned"
        
        # Verify candle structure
        first_candle = candles[0]
        assert len(first_candle) >= 6, "Invalid candle structure"
        assert float(first_candle[1]) > 0, "Invalid open price"
        assert float(first_candle[2]) > 0, "Invalid high price"
        assert float(first_candle[3]) > 0, "Invalid low price"
        assert float(first_candle[4]) > 0, "Invalid close price"
        assert float(first_candle[5]) > 0, "Invalid volume"
        
        logger.info(f"{GREEN}✓ Market candles test passed{RESET}")
        
    except Exception as e:
        pytest.fail(f"Error testing market candles: {str(e)}")

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 