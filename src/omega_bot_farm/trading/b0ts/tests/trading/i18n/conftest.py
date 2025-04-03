#!/usr/bin/env python3

"""
Fixtures for internationalization (i18n) tests in Omega Bot Farm Trading.

This module provides common fixtures for testing i18n functionality
across the trading components.
"""

import pytest
import os
from unittest.mock import patch, MagicMock, AsyncMock

# Try to import CCXT to determine if it's available
try:
    import ccxt
    HAVE_CCXT = True
except ImportError:
    HAVE_CCXT = False
    

@pytest.fixture
def mock_ccxt_ticker():
    """Create a mock CCXT ticker object."""
    ticker = MagicMock()
    ticker.symbol = "BTC/USDT:USDT"
    ticker.last = 30000.0
    ticker.bid = 30000.0
    ticker.ask = 30100.0
    
    # Add a to_dict method that returns a dictionary representation
    ticker.to_dict = MagicMock(return_value={
        "symbol": "BTC/USDT:USDT",
        "last": 30000.0,
        "bid": 30000.0,
        "ask": 30100.0
    })
    
    return ticker


@pytest.fixture
def ticker_dict():
    """Return a dictionary representation of a ticker."""
    return {
        "symbol": "BTC/USDT:USDT",
        "last": 30000.0,
        "bid": 30000.0,
        "ask": 30100.0
    }


@pytest.fixture
def mock_ccxt_position():
    """Create a mock CCXT position object."""
    position = MagicMock()
    position.symbol = "BTC/USDT:USDT"
    position.contracts = 0.01
    position.contractSize = 1.0
    position.entryPrice = 30000.0
    position.side = "long"
    position.info = {"symbolId": "BTCUSDT_UMCBL"}
    
    # Add a to_dict method that returns a dictionary representation
    position.to_dict = MagicMock(return_value={
        "symbol": "BTC/USDT:USDT",
        "contracts": 0.01,
        "contractSize": 1.0,
        "entryPrice": 30000.0,
        "side": "long",
        "info": {"symbolId": "BTCUSDT_UMCBL"}
    })
    
    return position


@pytest.fixture
def position_dict():
    """Return a dictionary representation of a position."""
    return {
        "symbol": "BTC/USDT:USDT",
        "contracts": 0.01,
        "contractSize": 1.0,
        "entryPrice": 30000.0,
        "side": "long",
        "info": {"symbolId": "BTCUSDT_UMCBL"}
    }


@pytest.fixture
def mock_i18n_translations():
    """Return mock translations for testing."""
    return {
        'en_US': {
            'exchange_initialized': 'Initialized {exchange} with {network}',
            'market_order_created': 'Created market {side} order for {amount} {symbol}',
            'leverage_set': 'Set leverage for {symbol} to {leverage}x',
            'exchange_error': 'Error in exchange operation: {error}',
            'position_closed': 'Closed position for {symbol}'
        },
        'es_ES': {
            'exchange_initialized': 'Inicializado {exchange} con {network}',
            'market_order_created': 'Orden de mercado {side} creada para {amount} {symbol}',
            'leverage_set': 'Apalancamiento establecido para {symbol} a {leverage}x',
            'exchange_error': 'Error en la operación de intercambio: {error}',
            'position_closed': 'Posición cerrada para {symbol}'
        },
        'ja_JP': {
            'exchange_initialized': '{exchange}を{network}で初期化しました',
            'market_order_created': '{symbol}の{amount}の{side}市場注文を作成しました',
            'leverage_set': '{symbol}のレバレッジを{leverage}倍に設定しました',
            'exchange_error': '取引所操作でエラーが発生しました：{error}',
            'position_closed': '{symbol}のポジションを閉じました'
        }
    }


@pytest.fixture
def mock_number_formatters():
    """Return mock number formatters for different locales."""
    return {
        'en_US': lambda n: f"{n:,.2f}",
        'es_ES': lambda n: f"{str(n).replace('.', ','):,}",
        'ja_JP': lambda n: f"{n:,.2f}"
    }


@pytest.fixture
def mock_currency_formatters():
    """Return mock currency formatters for different locales."""
    return {
        'en_US': lambda amount, currency: f"${amount:,.2f}" if currency == "USD" else f"{amount:,.2f} {currency}",
        'es_ES': lambda amount, currency: f"{amount:,.2f} €" if currency == "EUR" else f"{amount:,.2f} {currency}",
        'ja_JP': lambda amount, currency: f"¥{amount:,.0f}" if currency == "JPY" else f"{amount:,.2f} {currency}"
    }


@pytest.fixture
def mock_datetime_formatters():
    """Return mock datetime formatters for different locales."""
    return {
        'en_US': lambda dt: dt.strftime('%m/%d/%Y %I:%M:%S %p'),  # MM/DD/YYYY hh:mm:ss AM/PM
        'es_ES': lambda dt: dt.strftime('%d/%m/%Y %H:%M:%S'),     # DD/MM/YYYY HH:mm:ss
        'ja_JP': lambda dt: dt.strftime('%Y年%m月%d日 %H:%M:%S')   # YYYY年MM月DD日 HH:mm:ss
    }


@pytest.fixture
def ccxt_client():
    """Create a mock CCXT client for testing."""
    with patch('src.omega_bot_farm.trading.exchanges.ccxt_b0t.ccxt'):
        with patch('src.omega_bot_farm.trading.exchanges.ccxt_b0t.ccxt_async'):
            with patch('src.omega_bot_farm.trading.exchanges.ccxt_b0t.HAVE_CCXT', True):
                from src.omega_bot_farm.trading.exchanges.ccxt_b0t import ExchangeClientB0t
                client = ExchangeClientB0t(exchange_id='bitget')
                client.exchange = AsyncMock()
                return client


def requires_ccxt(cls_or_func=None):
    """
    Decorator to skip tests if CCXT is not available.
    
    Can be applied to classes or individual test functions.
    """
    skip_reason = "CCXT is not installed"
    
    if cls_or_func is None:
        # Called with parameters
        return pytest.mark.skipif(not HAVE_CCXT, reason=skip_reason)
    else:
        # Called without parameters
        if not HAVE_CCXT:
            # If it's a class, decorate each test method
            if isinstance(cls_or_func, type):
                for attr_name in dir(cls_or_func):
                    if attr_name.startswith('test_'):
                        attr = getattr(cls_or_func, attr_name)
                        if callable(attr):
                            setattr(cls_or_func, attr_name, 
                                    pytest.mark.skip(reason=skip_reason)(attr))
                return cls_or_func
            # If it's a function, skip it
            else:
                return pytest.mark.skip(reason=skip_reason)(cls_or_func)
        else:
            # CCXT is available, no need to skip
            return cls_or_func 