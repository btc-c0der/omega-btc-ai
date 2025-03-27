"""
Test suite for BitGet market ticker functionality.
Tests the get_market_ticker method with various scenarios.
"""

import pytest
import asyncio
import logging
from typing import Type, Union, Tuple
from unittest.mock import AsyncMock, patch, MagicMock
from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders
from omega_ai.trading.exchanges.bitget_ccxt import BitGetCCXT
from ccxt.base.errors import AuthenticationError, NetworkError, RateLimitExceeded, ExchangeError
from datetime import datetime, timezone
import ccxt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Test configuration
TEST_SYMBOL = "BTC/USDT:USDT"  # CCXT standard format
TEST_PRICE = 50000.0
TEST_VOLUME = 1.0

# Load environment variables
import os
from dotenv import load_dotenv
load_dotenv()

# Get API credentials from environment
TEST_API_KEY = str(os.getenv('BITGET_API_KEY', ''))
TEST_SECRET_KEY = str(os.getenv('BITGET_SECRET_KEY', ''))
TEST_PASSPHRASE = str(os.getenv('BITGET_PASSPHRASE', ''))

# Validate API credentials
if not all([TEST_API_KEY, TEST_SECRET_KEY, TEST_PASSPHRASE]):
    raise ValueError("Missing required API credentials in .env file")

@pytest.fixture
def mock_ccxt(mocker):
    """Create a mock CCXT instance."""
    mock = MagicMock()
    
    async def mock_fetch_ticker(symbol):
        if not symbol or not symbol.strip():
            raise ValueError("Symbol cannot be empty")
        if symbol == "INVALID_SYMBOL":
            raise ccxt.InvalidSymbol("Invalid symbol")
        if symbol == "RATE_LIMIT":
            raise ccxt.RateLimitExceeded("Rate limit exceeded")
        if symbol == "NETWORK_ERROR":
            raise ccxt.NetworkError("Network error")
        if symbol == "AUTH_ERROR":
            raise ccxt.AuthenticationError("Authentication error")
        if symbol == "EXCHANGE_ERROR":
            raise ccxt.ExchangeError("Exchange error")
        return {
            "symbol": symbol,
            "last": TEST_PRICE,
            "baseVolume": TEST_VOLUME,
            "timestamp": int(datetime.now(timezone.utc).timestamp() * 1000)
        }
    
    mock.fetch_ticker = AsyncMock(side_effect=mock_fetch_ticker)
    mock.load_markets = AsyncMock(return_value={})
    mock.fetch_position_mode = AsyncMock(return_value={'hedged': True})
    mock.set_position_mode = AsyncMock(return_value={'success': True})
    mock.fetch_balance = AsyncMock(return_value={'USDT': {'free': 100.0}})
    mock.set_leverage = AsyncMock(return_value={'success': True})
    mock.set_margin_mode = AsyncMock(return_value={'success': True})
    return mock

@pytest.fixture
def bitget_ccxt(mock_ccxt):
    """Create a BitGetCCXT instance with mock CCXT."""
    instance = BitGetCCXT()
    instance.exchange = mock_ccxt
    return instance

@pytest.fixture
def live_traders(mock_ccxt):
    """Create a BitGetLiveTraders instance with mock CCXT."""
    traders = BitGetLiveTraders(
        use_testnet=True,
        initial_capital=24.0,
        symbol="BTC/USDT:USDT",
        strategic_only=False,
        enable_pnl_alerts=True,
        pnl_alert_interval=1,
        leverage=11
    )
    traders.traders["test"] = BitGetCCXT()
    traders.traders["test"].exchange = mock_ccxt
    return traders

@pytest.mark.asyncio
async def test_get_market_ticker_success(live_traders):
    """Test successful market ticker retrieval."""
    logger.info("Testing successful market ticker retrieval")
    ticker = await live_traders.traders["test"].get_market_ticker(TEST_SYMBOL)
    assert ticker['symbol'] == TEST_SYMBOL
    assert ticker['last'] == TEST_PRICE
    assert ticker['baseVolume'] == TEST_VOLUME
    assert 'timestamp' in ticker

@pytest.mark.asyncio
async def test_get_market_ticker_invalid_symbol(live_traders):
    """Test market ticker retrieval with invalid symbol."""
    logger.info("Testing market ticker retrieval with invalid symbol")
    with pytest.raises(ValueError):
        await live_traders.traders["test"].get_market_ticker("INVALID_SYMBOL")

@pytest.mark.asyncio
async def test_get_market_ticker_rate_limit(live_traders):
    """Test market ticker retrieval under rate limiting."""
    logger.info("Testing market ticker retrieval under rate limiting")
    with pytest.raises(RateLimitExceeded):
        await live_traders.traders["test"].get_market_ticker("RATE_LIMIT")

@pytest.mark.asyncio
async def test_get_market_ticker_network_error(live_traders):
    """Test market ticker retrieval with network error."""
    logger.info("Testing market ticker retrieval with network error")
    with pytest.raises(NetworkError):
        await live_traders.traders["test"].get_market_ticker("NETWORK_ERROR")

@pytest.mark.asyncio
async def test_get_market_ticker_authentication_error(live_traders):
    """Test market ticker retrieval with authentication error."""
    logger.info("Testing market ticker retrieval with authentication error")
    with pytest.raises(AuthenticationError):
        await live_traders.traders["test"].get_market_ticker("AUTH_ERROR")

@pytest.mark.asyncio
async def test_get_market_ticker_exchange_error(live_traders):
    """Test market ticker retrieval with exchange error."""
    logger.info("Testing market ticker retrieval with exchange error")
    with pytest.raises(ExchangeError):
        await live_traders.traders["test"].get_market_ticker("EXCHANGE_ERROR")

@pytest.mark.asyncio
async def test_get_market_ticker_empty_symbol(live_traders):
    """Test market ticker retrieval with empty symbol."""
    logger.info("Testing market ticker retrieval with empty symbol")
    with pytest.raises(ValueError):
        await live_traders.traders["test"].get_market_ticker("")

@pytest.mark.asyncio
async def test_get_market_ticker_none_symbol(live_traders):
    """Test market ticker retrieval with None symbol."""
    logger.info("Testing market ticker retrieval with None symbol")
    with pytest.raises(ValueError):
        await live_traders.traders["test"].get_market_ticker(None)

@pytest.mark.asyncio
async def test_get_market_ticker_concurrent_requests(live_traders):
    """Test concurrent market ticker requests."""
    logger.info("Testing concurrent market ticker requests")
    tasks = [live_traders.traders["test"].get_market_ticker(TEST_SYMBOL) for _ in range(3)]
    results = await asyncio.gather(*tasks)
    assert all(result['last'] == TEST_PRICE for result in results)
    assert all(result['symbol'] == TEST_SYMBOL for result in results)

@pytest.mark.asyncio
async def test_get_market_ticker_data_consistency(live_traders):
    """Test market ticker data consistency across multiple requests."""
    logger.info("Testing market ticker data consistency")
    ticker1 = await live_traders.traders["test"].get_market_ticker(TEST_SYMBOL)
    ticker2 = await live_traders.traders["test"].get_market_ticker(TEST_SYMBOL)
    assert ticker1['last'] == ticker2['last']
    assert ticker1['baseVolume'] == ticker2['baseVolume']
    assert ticker1['symbol'] == ticker2['symbol']

@pytest.mark.asyncio
async def test_get_market_ticker_symbol_format(live_traders):
    """Test market ticker symbol format handling."""
    logger.info("Testing market ticker symbol format handling")
    ticker = await live_traders.traders["test"].get_market_ticker(TEST_SYMBOL)
    assert ticker['symbol'] == TEST_SYMBOL

@pytest.mark.asyncio
async def test_format_symbol(bitget_ccxt):
    """Test symbol formatting."""
    logger.info("Testing symbol formatting")
    assert bitget_ccxt._format_symbol("BTC/USDT:USDT") == "BTC/USDT:USDT"
    assert bitget_ccxt._format_symbol("BTCUSDT") == "BTC/USDT:USDT"
    assert bitget_ccxt._format_symbol(None) == "BTC/USDT:USDT"
    assert bitget_ccxt._format_symbol("") == "BTC/USDT:USDT"

@pytest.mark.asyncio
async def test_initialize(bitget_ccxt):
    """Test exchange initialization."""
    logger.info("Testing exchange initialization")
    await bitget_ccxt.initialize()
    assert bitget_ccxt.is_hedge_mode is True

@pytest.mark.asyncio
async def test_set_hedge_mode(bitget_ccxt):
    """Test hedge mode setting."""
    logger.info("Testing hedge mode setting")
    await bitget_ccxt.set_hedge_mode()

@pytest.mark.asyncio
async def test_setup_trading_config(bitget_ccxt):
    """Test trading configuration setup."""
    logger.info("Testing trading configuration setup")
    await bitget_ccxt.setup_trading_config(TEST_SYMBOL, leverage=2)

@pytest.mark.asyncio
async def test_get_balance(bitget_ccxt):
    """Test balance retrieval."""
    logger.info("Testing balance retrieval")
    balance = await bitget_ccxt.get_balance()
    assert balance['USDT']['free'] == 100.0 