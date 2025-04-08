import os
import pytest
from src.omega_bot_farm.trading.b0ts.core.exchange_client import ExchangeClient


def test_bitget_trading_symbol_btc(monkeypatch):
    """Test BitGet symbol formatting with BTCUSDT_UMCBL trading symbol."""
    # Mock the environment variable
    monkeypatch.setenv('TRADING_SYMBOL', 'BTCUSDT_UMCBL')
    
    # Create client instance with mock to bypass env_loader
    client = ExchangeClient(exchange_id='bitget', auto_connect=False)
    
    # Mock the _get_env_var method to return our test value
    monkeypatch.setattr(client, "_get_env_var", lambda key: 'BTCUSDT_UMCBL' if key == 'TRADING_SYMBOL' else None)
    client.trading_symbol = 'BTCUSDT_UMCBL'
    
    # Test formatting
    formatted_symbol = client._format_symbol()
    assert formatted_symbol == 'BTC/USDT:USDT'


def test_bitget_trading_symbol_eth(monkeypatch):
    """Test BitGet symbol formatting with ETHUSDT_UMCBL trading symbol."""
    # Mock the environment variable
    monkeypatch.setenv('TRADING_SYMBOL', 'ETHUSDT_UMCBL')
    
    # Create client instance with mock to bypass env_loader
    client = ExchangeClient(exchange_id='bitget', auto_connect=False)
    
    # Mock the _get_env_var method to return our test value
    monkeypatch.setattr(client, "_get_env_var", lambda key: 'ETHUSDT_UMCBL' if key == 'TRADING_SYMBOL' else None)
    client.trading_symbol = 'ETHUSDT_UMCBL'
    
    # Test formatting
    formatted_symbol = client._format_symbol()
    assert formatted_symbol == 'ETH/USDT:USDT'


def test_bitget_trading_symbol_sol(monkeypatch):
    """Test BitGet symbol formatting with SOLUSDT_UMCBL trading symbol."""
    # Mock the environment variable
    monkeypatch.setenv('TRADING_SYMBOL', 'SOLUSDT_UMCBL')
    
    # Create client instance with mock to bypass env_loader
    client = ExchangeClient(exchange_id='bitget', auto_connect=False)
    
    # Mock the _get_env_var method to return our test value
    monkeypatch.setattr(client, "_get_env_var", lambda key: 'SOLUSDT_UMCBL' if key == 'TRADING_SYMBOL' else None)
    client.trading_symbol = 'SOLUSDT_UMCBL'
    
    # Test formatting
    formatted_symbol = client._format_symbol()
    assert formatted_symbol == 'SOL/USDT:USDT'


def test_bitget_trading_symbol_regular(monkeypatch):
    """Test BitGet symbol formatting with a regular trading symbol (without _UMCBL suffix)."""
    # Mock the environment variable
    monkeypatch.setenv('TRADING_SYMBOL', 'BTCUSDT')
    
    # Create client instance with mock to bypass env_loader
    client = ExchangeClient(exchange_id='bitget', auto_connect=False)
    
    # Mock the _get_env_var method to return our test value
    monkeypatch.setattr(client, "_get_env_var", lambda key: 'BTCUSDT' if key == 'TRADING_SYMBOL' else None)
    client.trading_symbol = 'BTCUSDT'
    
    # Test formatting - special case for BTCUSDT with Bitget
    formatted_symbol = client._format_symbol('BTCUSDT')
    assert formatted_symbol == 'BTCUSDT/USDT:USDT'


def test_binance_trading_symbol(monkeypatch):
    """Test Binance symbol formatting."""
    # Mock the environment variable
    monkeypatch.setenv('TRADING_SYMBOL', 'BTCUSDT')
    
    # Create client instance with mock to bypass env_loader
    client = ExchangeClient(exchange_id='binance', auto_connect=False)
    
    # Mock the _get_env_var method to return our test value
    monkeypatch.setattr(client, "_get_env_var", lambda key: 'BTCUSDT' if key == 'TRADING_SYMBOL' else None)
    client.trading_symbol = 'BTCUSDT'
    
    # Test formatting
    formatted_symbol = client._format_symbol()
    assert formatted_symbol == 'BTC/USDT'


def test_kucoin_trading_symbol(monkeypatch):
    """Test KuCoin symbol formatting."""
    # Mock the environment variable
    monkeypatch.setenv('TRADING_SYMBOL', 'BTCUSDT')
    
    # Create client instance with mock to bypass env_loader
    client = ExchangeClient(exchange_id='kucoin', auto_connect=False)
    
    # Mock the _get_env_var method to return our test value
    monkeypatch.setattr(client, "_get_env_var", lambda key: 'BTCUSDT' if key == 'TRADING_SYMBOL' else None)
    client.trading_symbol = 'BTCUSDT'
    
    # Test formatting
    formatted_symbol = client._format_symbol()
    assert formatted_symbol == 'BTC/USDT'


def test_format_symbol_custom(monkeypatch):
    """Test formatting with a custom symbol parameter."""
    # Create client instance with mock to bypass env_loader
    client = ExchangeClient(exchange_id='bitget', auto_connect=False)
    
    # Test formatting with custom symbol
    formatted_symbol = client._format_symbol("DOTUSDT_UMCBL")
    assert formatted_symbol == 'DOT/USDT:USDT'


def test_no_symbol_defaults(monkeypatch):
    """Test when no trading_symbol is available and no custom symbol is provided."""
    # Create client instance with mock to bypass env_loader
    client = ExchangeClient(exchange_id='binance', auto_connect=False)
    
    # Mock the _get_env_var method to return None
    monkeypatch.setattr(client, "_get_env_var", lambda key: None)
    client.trading_symbol = None
    
    # Test formatting - should use default behavior
    formatted_symbol = client._format_symbol()
    assert formatted_symbol == "BTC/USDT"


if __name__ == "__main__":
    # Run tests directly when file is executed
    pytest.main(["-v", __file__]) 