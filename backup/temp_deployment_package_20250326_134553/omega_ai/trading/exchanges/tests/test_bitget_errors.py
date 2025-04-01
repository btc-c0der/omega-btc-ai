"""
OMEGA BTC AI - BitGet Error Code Test Suite
=======================================

This module implements tests for BitGet API error codes and responses.
It verifies proper error handling and response codes according to the official documentation.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import unittest
import logging
from typing import Dict, Any
from datetime import datetime
from omega_ai.trading.exchanges.bitget_trader import BitGetTrader
from omega_ai.trading.exchanges.coin_picker import CoinPicker, CoinType

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestBitGetErrors(unittest.TestCase):
    """Test suite for BitGet API error codes and responses."""
    
    def setUp(self):
        """Set up test environment."""
        self.trader = BitGetTrader(
            use_testnet=False,  # Use live environment
            initial_capital=24.0,
            api_version="v2"  # Use v2 API for better compatibility
        )
        self.trader.symbol = "BTCUSDT"  # Set symbol after initialization
        self.coin_picker = CoinPicker(use_testnet=False)
        
    def test_symbol_format(self):
        """Test correct symbol format for live futures trading."""
        # Update coin picker cache
        self.coin_picker.update_coins_cache()
        
        # Test valid symbol
        symbol_info = self.coin_picker.get_symbol_info("BTCUSDT")
        self.assertIsNotNone(symbol_info)
        if symbol_info:
            self.assertEqual(symbol_info.type, CoinType.FUTURES)
            self.assertEqual(symbol_info.base_currency, "BTC")
            self.assertEqual(symbol_info.quote_currency, "USDT")
        
        # Test invalid symbols
        invalid_symbols = [
            "BTCUSDT_UMCBL",  # Old v1 format
            "BTCUSDT_INVALID",  # Invalid suffix
            "BTCUSDT_",  # Trailing underscore
            "_BTCUSDT",  # Leading underscore
            "BTCUSDT_BTCUSDT",  # Duplicate
            "BTCUSDT_SPOT",  # Wrong type
            "BTCUSDT_LEVERAGED",  # Wrong type
            "BTCUSDT_TEST",  # Test suffix
            "BTCUSDT_LIVE",  # Live suffix
            "BTCUSDT_MAINNET",  # Mainnet suffix
        ]
        
        for symbol in invalid_symbols:
            symbol_info = self.coin_picker.get_symbol_info(symbol)
            self.assertIsNone(symbol_info, f"Symbol {symbol} should be invalid")
            
        # Test symbol verification
        self.assertTrue(self.trader.verify_symbol("BTCUSDT"))
        for symbol in invalid_symbols:
            self.assertFalse(self.trader.verify_symbol(symbol))
            
    def test_invalid_symbol(self):
        """Test error response for invalid symbol."""
        # Test with non-existent symbol
        invalid_symbol = "INVALID_SYMBOL"
        positions = self.trader.get_positions(invalid_symbol)
        self.assertIsNone(positions)
        
        # Verify error code in logs
        with self.assertLogs(level='ERROR') as log:
            self.trader.verify_symbol(invalid_symbol)
            self.assertIn("Error verifying symbol", log.output[0])
            
    def test_invalid_order_parameters(self):
        """Test error response for invalid order parameters."""
        # Test with invalid order size
        invalid_size = "invalid_size"
        order_params = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "order_type": "LIMIT",
            "quantity": float(invalid_size),  # Convert to float
            "price": 50000.0,  # Convert to float
            "margin_mode": "crossed",
            "leverage": 20,
            "productType": "USDT-FUTURES",  # Updated parameter name
            "reduce_only": False,
            "post_only": False
        }
        
        # Attempt to place order with invalid parameters
        response = self.trader.place_order(**order_params)
        self.assertIsNone(response)
        
    def test_rate_limit_handling(self):
        """Test rate limit error handling."""
        # Make multiple rapid requests to trigger rate limit
        for _ in range(10):
            self.trader.get_market_ticker("BTCUSDT")
            
        # Verify rate limit handling in logs
        with self.assertLogs(level='WARNING') as log:
            self.trader.get_market_ticker("BTCUSDT")
            self.assertIn("Rate limit", log.output[0])
            
    def test_authentication_errors(self):
        """Test authentication error handling."""
        # Create trader with invalid credentials
        invalid_trader = BitGetTrader(
            use_testnet=False,
            initial_capital=24.0,
            api_key="invalid_key",
            secret_key="invalid_secret",
            passphrase="invalid_passphrase",
            api_version="v2"  # Use v2 API
        )
        invalid_trader.symbol = "BTCUSDT"  # Set symbol after initialization
        
        # Attempt to make authenticated request
        positions = invalid_trader.get_positions("BTCUSDT")
        self.assertIsNone(positions)
        
    def test_position_errors(self):
        """Test position-related error handling."""
        # Test closing non-existent position
        response = self.trader.close_position(
            symbol="BTCUSDT",
            side="LONG"
        )
        self.assertIsNone(response)
        
    def test_market_data_errors(self):
        """Test market data error handling."""
        # Test with invalid market data request
        invalid_symbol = "INVALID_SYMBOL"
        ticker = self.trader.get_market_ticker(invalid_symbol)
        self.assertIsNone(ticker)
        
    def test_leverage_errors(self):
        """Test leverage-related error handling."""
        # Test with invalid leverage value
        invalid_leverage = 100  # Leverage too high
        order_params = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "order_type": "LIMIT",
            "quantity": 0.001,
            "price": 50000.0,
            "margin_mode": "crossed",
            "leverage": invalid_leverage,
            "productType": "USDT-FUTURES",  # Updated parameter name
            "reduce_only": False,
            "post_only": False
        }
        
        response = self.trader.place_order(**order_params)
        self.assertIsNone(response)
        
    def test_margin_mode_errors(self):
        """Test margin mode error handling."""
        # Test with invalid margin mode
        invalid_margin_mode = "INVALID_MODE"
        order_params = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "order_type": "LIMIT",
            "quantity": 0.001,
            "price": 50000.0,
            "margin_mode": invalid_margin_mode,
            "leverage": 20,
            "productType": "USDT-FUTURES",  # Updated parameter name
            "reduce_only": False,
            "post_only": False
        }
        
        response = self.trader.place_order(**order_params)
        self.assertIsNone(response)
        
    def test_order_type_errors(self):
        """Test order type error handling."""
        # Test with invalid order type
        invalid_order_type = "INVALID_TYPE"
        order_params = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "order_type": invalid_order_type,
            "quantity": 0.001,
            "price": 50000.0,
            "margin_mode": "crossed",
            "leverage": 20,
            "productType": "USDT-FUTURES",  # Updated parameter name
            "reduce_only": False,
            "post_only": False
        }
        
        response = self.trader.place_order(**order_params)
        self.assertIsNone(response)
        
    def test_time_in_force_errors(self):
        """Test time in force error handling."""
        # Test with invalid time in force
        invalid_time_in_force = "INVALID_TIF"
        order_params = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "order_type": "LIMIT",
            "quantity": 0.001,
            "price": 50000.0,
            "margin_mode": "crossed",
            "leverage": 20,
            "productType": "USDT-FUTURES",  # Updated parameter name
            "time_in_force": invalid_time_in_force,
            "reduce_only": False,
            "post_only": False
        }
        
        response = self.trader.place_order(**order_params)
        self.assertIsNone(response)

    def test_get_all_positions(self):
        """Test getting all positions."""
        # Test with default product type (USDT-FUTURES)
        positions = self.trader.get_all_positions()
        self.assertIsNotNone(positions)
        if positions:
            # Verify position data structure
            for position in positions:
                self.assertIn("symbol", position)
                self.assertIn("marginMode", position)
                self.assertIn("total", position)
                self.assertIn("available", position)
                self.assertIn("leverage", position)
                self.assertIn("unrealizedPnl", position)
                self.assertIn("marginType", position)
                self.assertIn("entryPrice", position)
                self.assertIn("markPrice", position)
                self.assertIn("liquidationPrice", position)
                
        # Test with invalid product type
        invalid_positions = self.trader.get_all_positions(product_type="INVALID")
        self.assertIsNone(invalid_positions)

    def test_get_historical_positions(self):
        """Test getting historical positions."""
        # Test with valid parameters
        end_time = int(datetime.now().timestamp() * 1000)
        start_time = end_time - (7 * 24 * 60 * 60 * 1000)  # 7 days ago
        
        positions = self.trader.get_historical_positions(
            symbol="BTCUSDT",
            start_time=start_time,
            end_time=end_time,
            limit=100
        )
        self.assertIsNotNone(positions)
        
        # Test with invalid parameters
        invalid_positions = self.trader.get_historical_positions(
            symbol="INVALID_SYMBOL",
            start_time=start_time,
            end_time=end_time,
            limit=100
        )
        self.assertIsNone(invalid_positions)

    def test_order_json_structure(self):
        """Test order JSON structure."""
        order_params = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "order_type": "LIMIT",
            "quantity": 0.001,
            "price": 50000.0,
            "margin_mode": "crossed",
            "leverage": 20,
            "productType": "USDT-FUTURES",  # Updated parameter name
            "reduce_only": False,
            "post_only": False
        }
        
        # Test order structure
        response = self.trader.place_order(**order_params)
        self.assertIsNotNone(response)
        if response and response.get("data"):
            order_data = response["data"]
            self.assertIn("symbol", order_data)
            self.assertIn("side", order_data)
            self.assertIn("orderType", order_data)
            self.assertIn("size", order_data)
            self.assertIn("price", order_data)
            self.assertIn("marginMode", order_data)
            self.assertIn("leverage", order_data)
            self.assertIn("productType", order_data)
            self.assertIn("reduceOnly", order_data)
            self.assertIn("postOnly", order_data)

if __name__ == '__main__':
    unittest.main() 