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
            initial_capital=24.0
        )
        self.trader.symbol = "BTCUSDT_UMCBL"  # Set symbol after initialization
        self.coin_picker = CoinPicker(use_testnet=False)
        
    def test_symbol_format(self):
        """Test correct symbol format for live futures trading."""
        # Update coin picker cache
        self.coin_picker.update_coins_cache()
        
        # Test valid symbol
        symbol_info = self.coin_picker.get_symbol_info("BTCUSDT_UMCBL")
        self.assertIsNotNone(symbol_info)
        if symbol_info:
            self.assertEqual(symbol_info.type, CoinType.FUTURES)
            self.assertEqual(symbol_info.base_currency, "BTC")
            self.assertEqual(symbol_info.quote_currency, "USDT")
        
        # Test invalid symbols
        invalid_symbols = [
            "BTCUSDT",  # Missing _UMCBL suffix
            "BTCUSDT_UMCBL_INVALID",  # Invalid suffix
            "BTCUSDT_UMCBL_",  # Trailing underscore
            "_BTCUSDT_UMCBL",  # Leading underscore
            "BTCUSDT_UMCBL_UMCBL",  # Duplicate suffix
            "BTCUSDT_UMCBL_SPOT",  # Wrong type
            "BTCUSDT_UMCBL_LEVERAGED",  # Wrong type
            "BTCUSDT_UMCBL_TEST",  # Test suffix
            "BTCUSDT_UMCBL_LIVE",  # Live suffix
            "BTCUSDT_UMCBL_MAINNET",  # Mainnet suffix
        ]
        
        for symbol in invalid_symbols:
            symbol_info = self.coin_picker.get_symbol_info(symbol)
            self.assertIsNone(symbol_info, f"Symbol {symbol} should be invalid")
            
        # Test symbol verification
        self.assertTrue(self.trader.verify_symbol("BTCUSDT_UMCBL"))
        for symbol in invalid_symbols:
            self.assertFalse(self.trader.verify_symbol(symbol))
            
    def test_invalid_symbol(self):
        """Test error response for invalid symbol."""
        # Test with non-existent symbol
        invalid_symbol = "INVALID_SYMBOL_UMCBL"
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
            "symbol": "BTCUSDT_UMCBL",
            "side": "BUY",
            "order_type": "LIMIT",
            "quantity": float(invalid_size),  # Convert to float
            "price": 50000.0,  # Convert to float
            "margin_mode": "crossed",
            "leverage": 20,
            "product_type": "umcbl",
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
            self.trader.get_market_ticker("BTCUSDT_UMCBL")
            
        # Verify rate limit handling in logs
        with self.assertLogs(level='WARNING') as log:
            self.trader.get_market_ticker("BTCUSDT_UMCBL")
            self.assertIn("Rate limit", log.output[0])
            
    def test_authentication_errors(self):
        """Test authentication error handling."""
        # Create trader with invalid credentials
        invalid_trader = BitGetTrader(
            use_testnet=False,
            initial_capital=24.0,
            api_key="invalid_key",
            secret_key="invalid_secret",
            passphrase="invalid_passphrase"
        )
        invalid_trader.symbol = "BTCUSDT_UMCBL"  # Set symbol after initialization
        
        # Attempt to make authenticated request
        positions = invalid_trader.get_positions("BTCUSDT_UMCBL")
        self.assertIsNone(positions)
        
    def test_position_errors(self):
        """Test position-related error handling."""
        # Test closing non-existent position
        response = self.trader.close_position(
            symbol="BTCUSDT_UMCBL",
            side="LONG"
        )
        self.assertIsNone(response)
        
    def test_market_data_errors(self):
        """Test market data error handling."""
        # Test with invalid market data request
        invalid_symbol = "INVALID_SYMBOL_UMCBL"
        ticker = self.trader.get_market_ticker(invalid_symbol)
        self.assertIsNone(ticker)
        
    def test_leverage_errors(self):
        """Test leverage-related error handling."""
        # Test with invalid leverage value
        invalid_leverage = 100  # Leverage too high
        order_params = {
            "symbol": "BTCUSDT_UMCBL",
            "side": "BUY",
            "order_type": "LIMIT",
            "quantity": 0.001,
            "price": 50000.0,
            "margin_mode": "crossed",
            "leverage": invalid_leverage,
            "product_type": "umcbl",
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
            "symbol": "BTCUSDT_UMCBL",
            "side": "BUY",
            "order_type": "LIMIT",
            "quantity": 0.001,
            "price": 50000.0,
            "margin_mode": invalid_margin_mode,
            "leverage": 20,
            "product_type": "umcbl",
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
            "symbol": "BTCUSDT_UMCBL",
            "side": "BUY",
            "order_type": invalid_order_type,
            "quantity": 0.001,
            "price": 50000.0,
            "margin_mode": "crossed",
            "leverage": 20,
            "product_type": "umcbl",
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
            "symbol": "BTCUSDT_UMCBL",
            "side": "BUY",
            "order_type": "LIMIT",
            "quantity": 0.001,
            "price": 50000.0,
            "margin_mode": "crossed",
            "leverage": 20,
            "product_type": "umcbl",
            "time_in_force": invalid_time_in_force,
            "reduce_only": False,
            "post_only": False
        }
        
        response = self.trader.place_order(**order_params)
        self.assertIsNone(response)

    def test_get_all_positions(self):
        """Test getting all positions."""
        # Test with default product type (umcbl)
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
        invalid_positions = self.trader.get_all_positions(product_type="invalid")
        self.assertIsNone(invalid_positions)
        
        # Test with empty product type
        empty_positions = self.trader.get_all_positions(product_type="")
        self.assertIsNone(empty_positions)

    def test_get_historical_positions(self):
        """Test getting historical positions."""
        # Test with default parameters
        positions = self.trader.get_historical_positions()
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
                self.assertIn("holdSide", position)
                self.assertIn("updateTime", position)
                
        # Test with time range
        current_time = int(datetime.now().timestamp() * 1000)
        one_day_ago = current_time - (24 * 60 * 60 * 1000)  # 24 hours in milliseconds
        
        time_range_positions = self.trader.get_historical_positions(
            start_time=one_day_ago,
            end_time=current_time
        )
        self.assertIsNotNone(time_range_positions)
        
        # Test with custom limit
        limited_positions = self.trader.get_historical_positions(limit=50)
        self.assertIsNotNone(limited_positions)
        if limited_positions:
            self.assertLessEqual(len(limited_positions), 50)
            
        # Test with invalid parameters
        invalid_positions = self.trader.get_historical_positions(
            symbol="INVALID_SYMBOL",
            product_type="invalid"
        )
        self.assertIsNone(invalid_positions)
        
        # Test with invalid time range
        invalid_time_positions = self.trader.get_historical_positions(
            start_time=current_time,
            end_time=one_day_ago  # End time before start time
        )
        self.assertIsNone(invalid_time_positions)
        
        # Test with invalid limit
        invalid_limit_positions = self.trader.get_historical_positions(limit=0)
        self.assertIsNone(invalid_limit_positions)

    def test_order_json_structure(self):
        """Test order placement JSON structure according to BitGet API documentation."""
        # Test valid order structure
        valid_order = {
            "symbol": "BTCUSDT_UMCBL",
            "marginMode": "crossed",
            "side": "buy",
            "orderType": "limit",
            "size": "0.001",
            "price": "50000",
            "timeInForceValue": "normal",
            "leverage": "20",
            "reduceOnly": False,
            "postOnly": False,
            "productType": "umcbl"
        }
        
        # Test order with all optional parameters
        full_order = {
            "symbol": "BTCUSDT_UMCBL",
            "marginMode": "crossed",
            "side": "buy",
            "orderType": "limit",
            "size": "0.001",
            "price": "50000",
            "timeInForceValue": "normal",
            "leverage": "20",
            "reduceOnly": False,
            "postOnly": False,
            "productType": "umcbl",
            "clientOid": "test_order_123",
            "force": "normal",
            "closeOnTrigger": False,
            "holdSide": "long"
        }
        
        # Test market order structure
        market_order = {
            "symbol": "BTCUSDT_UMCBL",
            "marginMode": "crossed",
            "side": "buy",
            "orderType": "market",
            "size": "0.001",
            "leverage": "20",
            "reduceOnly": False,
            "postOnly": False,
            "productType": "umcbl"
        }
        
        # Test order with invalid parameters
        invalid_orders = [
            {
                "symbol": "BTCUSDT_UMCBL",
                "marginMode": "invalid_mode",  # Invalid margin mode
                "side": "buy",
                "orderType": "limit",
                "size": "0.001",
                "price": "50000",
                "timeInForceValue": "normal",
                "leverage": "20",
                "reduceOnly": False,
                "postOnly": False,
                "productType": "umcbl"
            },
            {
                "symbol": "BTCUSDT_UMCBL",
                "marginMode": "crossed",
                "side": "invalid_side",  # Invalid side
                "orderType": "limit",
                "size": "0.001",
                "price": "50000",
                "timeInForceValue": "normal",
                "leverage": "20",
                "reduceOnly": False,
                "postOnly": False,
                "productType": "umcbl"
            },
            {
                "symbol": "BTCUSDT_UMCBL",
                "marginMode": "crossed",
                "side": "buy",
                "orderType": "invalid_type",  # Invalid order type
                "size": "0.001",
                "price": "50000",
                "timeInForceValue": "normal",
                "leverage": "20",
                "reduceOnly": False,
                "postOnly": False,
                "productType": "umcbl"
            },
            {
                "symbol": "BTCUSDT_UMCBL",
                "marginMode": "crossed",
                "side": "buy",
                "orderType": "limit",
                "size": "invalid_size",  # Invalid size
                "price": "50000",
                "timeInForceValue": "normal",
                "leverage": "20",
                "reduceOnly": False,
                "postOnly": False,
                "productType": "umcbl"
            },
            {
                "symbol": "BTCUSDT_UMCBL",
                "marginMode": "crossed",
                "side": "buy",
                "orderType": "limit",
                "size": "0.001",
                "price": "invalid_price",  # Invalid price
                "timeInForceValue": "normal",
                "leverage": "20",
                "reduceOnly": False,
                "postOnly": False,
                "productType": "umcbl"
            },
            {
                "symbol": "BTCUSDT_UMCBL",
                "marginMode": "crossed",
                "side": "buy",
                "orderType": "limit",
                "size": "0.001",
                "price": "50000",
                "timeInForceValue": "invalid_tif",  # Invalid time in force
                "leverage": "20",
                "reduceOnly": False,
                "postOnly": False,
                "productType": "umcbl"
            },
            {
                "symbol": "BTCUSDT_UMCBL",
                "marginMode": "crossed",
                "side": "buy",
                "orderType": "limit",
                "size": "0.001",
                "price": "50000",
                "timeInForceValue": "normal",
                "leverage": "invalid_leverage",  # Invalid leverage
                "reduceOnly": False,
                "postOnly": False,
                "productType": "umcbl"
            },
            {
                "symbol": "BTCUSDT_UMCBL",
                "marginMode": "crossed",
                "side": "buy",
                "orderType": "limit",
                "size": "0.001",
                "price": "50000",
                "timeInForceValue": "normal",
                "leverage": "20",
                "reduceOnly": "invalid_reduce",  # Invalid reduce only
                "postOnly": False,
                "productType": "umcbl"
            },
            {
                "symbol": "BTCUSDT_UMCBL",
                "marginMode": "crossed",
                "side": "buy",
                "orderType": "limit",
                "size": "0.001",
                "price": "50000",
                "timeInForceValue": "normal",
                "leverage": "20",
                "reduceOnly": False,
                "postOnly": "invalid_post",  # Invalid post only
                "productType": "umcbl"
            },
            {
                "symbol": "BTCUSDT_UMCBL",
                "marginMode": "crossed",
                "side": "buy",
                "orderType": "limit",
                "size": "0.001",
                "price": "50000",
                "timeInForceValue": "normal",
                "leverage": "20",
                "reduceOnly": False,
                "postOnly": False,
                "productType": "invalid_product"  # Invalid product type
            }
        ]
        
        # Test valid orders
        for order in [valid_order, full_order, market_order]:
            response = self.trader.place_order(**order)
            self.assertIsNotNone(response)
            
        # Test invalid orders
        for order in invalid_orders:
            response = self.trader.place_order(**order)
            self.assertIsNone(response)

if __name__ == '__main__':
    unittest.main() 