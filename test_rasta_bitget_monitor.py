#!/usr/bin/env python3
"""
Test Suite for RASTA BitGet Position Monitor
Tests the divine streaming monitor functionality
"""

import unittest
import io
import sys
import os
import json
from unittest.mock import patch, MagicMock, call
from datetime import datetime

# Import the module to test
import simple_bitget_positions as monitor

# Constants for testing
PHI = 1.618034  # Golden Ratio
INV_PHI = 0.618034  # Inverse Golden Ratio
SCHUMANN_BASE = 7.83  # Base Schumann resonance frequency

class TestRastaBitgetMonitor(unittest.TestCase):
    """Test cases for the RastaBitgetMonitor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Sample test positions
        self.phi_position = {
            'symbol': 'BTC/USDT:USDT',
            'side': 'long',
            'contracts': str(PHI),  # Divine position size using PHI
            'notional': str(PHI * 10000),  # PHI * $10,000
            'entryPrice': '40000',
            'markPrice': '42000',
            'unrealizedPnl': '1618.034', # Divine position size using PHI
            'percentage': '4.0',
            'leverage': '8.0',
            'liquidationPrice': '32000'
        }
        
        self.schumann_position = {
            'symbol': 'ETH/USDT:USDT',
            'side': 'short',
            'contracts': str(SCHUMANN_BASE),  # Earth frequency contracts
            'notional': '7830',  # SCHUMANN_BASE * $1000
            'entryPrice': '3000',
            'markPrice': '2900',
            'unrealizedPnl': '78.3',  # 1% of notional
            'percentage': '1.0',
            'leverage': '13',
            'liquidationPrice': '4000'
        }
        
        self.quantum_position = {
            'symbol': 'SOL/USDT:USDT',
            'side': 'long',
            'contracts': '0.000000001',  # Quantum small position
            'notional': '0.000000100',
            'entryPrice': '100',
            'markPrice': '101',
            'unrealizedPnl': '0.000000042',  # The answer to everything
            'percentage': '0.042',
            'leverage': '21',
            'liquidationPrice': '50'
        }
        
        # Settings for the monitor
        self.test_settings = {
            'interval': 1,
            'use_color': True,
            'debug': False
        }
        
        # Create a test monitor instance
        self.test_monitor = monitor.RastaBitgetMonitor(**self.test_settings)
    
    def test_initialization(self):
        """Test monitor initialization"""
        # Verify default settings
        self.assertEqual(self.test_monitor.interval, 1)
        self.assertTrue(self.test_monitor.use_color)
        self.assertFalse(self.test_monitor.debug)
        self.assertEqual(self.test_monitor.frame_counter, 0)
        self.assertEqual(self.test_monitor.previous_positions, [])
        self.assertEqual(self.test_monitor.previous_notional, 0)
    
    def test_phi_circle_display(self):
        """Test PHI circle display with animation"""
        # Test all frames
        for i in range(4):
            self.test_monitor.frame_counter = i
            phi_circle = self.test_monitor.display_phi_circle()
            # Check for PHI symbol in the display
            self.assertIn("φ", phi_circle)
    
    def test_fibonacci_bar(self):
        """Test Fibonacci bar generation"""
        # Test positive percentage
        positive_bar = self.test_monitor.fibonacci_bar(50, width=10)
        self.assertEqual(len(positive_bar.strip()), 19)  # Updated expected width
        
        # Test negative percentage
        negative_bar = self.test_monitor.fibonacci_bar(-50, width=10)
        self.assertEqual(len(negative_bar.strip()), 19)  # Updated expected width
        
        # Test percentage > 100
        large_bar = self.test_monitor.fibonacci_bar(150, width=10)
        self.assertEqual(len(large_bar.strip()), 19)  # Updated expected width
    
    def test_animated_fibonacci_bar(self):
        """Test animated Fibonacci bar generation"""
        # Test with different frame counters
        for i in range(8):  # Test all animation frames
            self.test_monitor.frame_counter = i
            
            # Positive percentage
            positive_bar = self.test_monitor.animated_fibonacci_bar(50, width=10)
            self.assertEqual(len(positive_bar.strip()), 19)  # Updated expected width
            
            # Negative percentage
            negative_bar = self.test_monitor.animated_fibonacci_bar(-50, width=10)
            self.assertEqual(len(negative_bar.strip()), 19)  # Updated expected width
            
            # Zero percentage
            zero_bar = self.test_monitor.animated_fibonacci_bar(0, width=10)
            self.assertEqual(len(zero_bar.strip()), 10)  # Expected width for zero bar is 10
    
    @patch('os.getenv')
    def test_get_positions_missing_credentials(self, mock_getenv):
        """Test handling of missing API credentials"""
        # Mock missing API keys
        mock_getenv.return_value = ""
        
        # Call the method
        result = self.test_monitor.get_positions()
        
        # Verify error response
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Missing credentials")
    
    @patch('os.getenv')
    @patch('ccxt.bitget')
    def test_get_positions_success(self, mock_bitget, mock_getenv):
        """Test successful position retrieval"""
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default="": {
            "BITGET_API_KEY": "test_api_key",
            "BITGET_SECRET_KEY": "test_secret_key",
            "BITGET_PASSPHRASE": "test_passphrase"
        }.get(key, default)
        
        # Mock exchange object
        mock_exchange = MagicMock()
        mock_exchange.fetchPositions.return_value = [
            self.phi_position,
            self.schumann_position,
            self.quantum_position,
            # Add a zero-contract position which should be filtered out
            {
                'symbol': 'DOGE/USDT:USDT',
                'side': 'long',
                'contracts': '0',
                'notional': '0',
                'entryPrice': '0.1',
                'markPrice': '0.1',
                'unrealizedPnl': '0',
                'percentage': '0',
                'leverage': '10',
                'liquidationPrice': '0.05'
            }
        ]
        mock_bitget.return_value = mock_exchange
        
        # Call the method
        result = self.test_monitor.get_positions()
        
        # Verify result
        self.assertTrue(result["success"])
        self.assertEqual(len(result["positions"]), 3)  # Zero-contract position filtered out
        self.assertIn("timestamp", result)
        self.assertEqual(result["connection"], "CONNECTED TO BITGET MAINNET")
        
        # Verify exchange creation with correct parameters
        mock_bitget.assert_called_once_with({
            'apiKey': 'test_api_key',
            'secret': 'test_secret_key',
            'password': 'test_passphrase',
            'options': {
                'defaultType': 'swap',
            }
        })
    
    @patch('os.getenv')
    def test_get_positions_import_error(self, mock_getenv):
        """Test handling of ccxt import error"""
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default="": {
            "BITGET_API_KEY": "test_api_key",
            "BITGET_SECRET_KEY": "test_secret_key",
            "BITGET_PASSPHRASE": "test_passphrase"
        }.get(key, default)
        
        # Original import function
        original_import = __import__
        
        # Replace import with mock that raises ImportError for ccxt
        def mock_import(name, *args, **kwargs):
            if name == 'ccxt':
                raise ImportError("ccxt not found")
            return original_import(name, *args, **kwargs)
        
        # Patch the import function
        with patch('builtins.__import__', side_effect=mock_import):
            # Call the method
            result = self.test_monitor.get_positions()
            
            # Verify error response
            self.assertIn("error", result)
            self.assertEqual(result["error"], "ccxt module not installed")
    
    @patch('os.getenv')
    @patch('ccxt.bitget')
    def test_get_positions_api_error(self, mock_bitget, mock_getenv):
        """Test handling of API errors"""
        # Mock environment variables
        mock_getenv.side_effect = lambda key, default="": {
            "BITGET_API_KEY": "test_api_key",
            "BITGET_SECRET_KEY": "test_secret_key",
            "BITGET_PASSPHRASE": "test_passphrase"
        }.get(key, default)
        
        # Mock exchange object that raises an exception
        mock_exchange = MagicMock()
        mock_exchange.fetchPositions.side_effect = Exception("API error")
        mock_bitget.return_value = mock_exchange
        
        # Call the method
        result = self.test_monitor.get_positions()
        
        # Verify error response
        self.assertIn("error", result)
        self.assertEqual(result["error"], "API error")
    
    def test_detect_position_changes_first_run(self):
        """Test position change detection on first run"""
        # Initialize with empty previous positions
        self.test_monitor.previous_positions = []
        
        # Current positions
        current_positions = [self.phi_position, self.schumann_position]
        
        # Detect changes
        changes = self.test_monitor.detect_position_changes(current_positions)
        
        # Should return None on first run
        self.assertIsNone(changes)
        
        # Verify previous positions are set
        self.assertEqual(self.test_monitor.previous_positions, current_positions)
    
    def test_detect_position_changes_new_position(self):
        """Test detection of new positions"""
        # Initialize with existing positions
        self.test_monitor.previous_positions = [self.phi_position]
        
        # Current positions with a new one
        current_positions = [self.phi_position, self.schumann_position]
        
        # Detect changes
        changes = self.test_monitor.detect_position_changes(current_positions)
        
        # Verify new position detected
        self.assertIsNotNone(changes)
        self.assertEqual(len(changes["new"]), 1)
        self.assertEqual(changes["new"][0], self.schumann_position)
        self.assertEqual(len(changes["closed"]), 0)
        self.assertEqual(len(changes["changed"]), 0)
    
    def test_detect_position_changes_closed_position(self):
        """Test detection of closed positions"""
        # Initialize with existing positions
        self.test_monitor.previous_positions = [self.phi_position, self.schumann_position]
        
        # Current positions with one removed
        current_positions = [self.phi_position]
        
        # Detect changes
        changes = self.test_monitor.detect_position_changes(current_positions)
        
        # Verify closed position detected
        self.assertIsNotNone(changes)
        self.assertEqual(len(changes["closed"]), 1)
        self.assertEqual(changes["closed"][0], self.schumann_position)
        self.assertEqual(len(changes["new"]), 0)
        self.assertEqual(len(changes["changed"]), 0)
    
    def test_detect_position_changes_modified_position(self):
        """Test detection of modified positions"""
        # Initialize with existing positions
        self.test_monitor.previous_positions = [self.phi_position]
        
        # Modified position with different contracts and PnL
        modified_position = dict(self.phi_position)
        modified_position['contracts'] = str(float(self.phi_position['contracts']) * 1.1)  # 10% increase
        modified_position['unrealizedPnl'] = str(float(self.phi_position['unrealizedPnl']) * 1.2)  # 20% increase
        
        # Current positions with the modified one
        current_positions = [modified_position]
        
        # Detect changes
        changes = self.test_monitor.detect_position_changes(current_positions)
        
        # Verify modified position detected
        self.assertIsNotNone(changes)
        self.assertEqual(len(changes["changed"]), 1)
        self.assertEqual(changes["changed"][0]["position"], modified_position)
        self.assertEqual(len(changes["new"]), 0)
        self.assertEqual(len(changes["closed"]), 0)
    
    def test_detect_position_changes_no_changes(self):
        """Test detection when there are no changes"""
        # Initialize with existing positions
        self.test_monitor.previous_positions = [self.phi_position]
        
        # Current positions same as previous
        current_positions = [dict(self.phi_position)]  # Use dict to create a copy
        
        # Detect changes
        changes = self.test_monitor.detect_position_changes(current_positions)
        
        # Should return None when no changes
        self.assertIsNone(changes)
    
    def test_generate_fibonacci_levels_long(self):
        """Test Fibonacci level generation for long positions"""
        # Test with a base price of 100
        base_price = 100
        levels = self.test_monitor.generate_fibonacci_levels(base_price, "LONG")
        
        # Verify correct number of levels
        self.assertEqual(len(levels), 8)
        
        # Verify specific levels
        self.assertEqual(levels[0][0], "Entry")
        self.assertEqual(levels[0][1], 100)
        
        self.assertEqual(levels[4][0], "0.618 Fib Ext")
        self.assertAlmostEqual(levels[4][1], 100 * (1 + 0.618), delta=0.01)
        
        self.assertEqual(levels[7][0], "1.618 Fib Ext")
        self.assertAlmostEqual(levels[7][1], 100 * (1 + 1.618), delta=0.01)
    
    def test_generate_fibonacci_levels_short(self):
        """Test Fibonacci level generation for short positions"""
        # Test with a base price of 100
        base_price = 100
        levels = self.test_monitor.generate_fibonacci_levels(base_price, "SHORT")
        
        # Verify correct number of levels
        self.assertEqual(len(levels), 6)
        
        # Verify specific levels
        self.assertEqual(levels[0][0], "Entry")
        self.assertEqual(levels[0][1], 100)
        
        self.assertEqual(levels[4][0], "0.618 Fib Ret")
        self.assertAlmostEqual(levels[4][1], 100 * (1 - 0.618), delta=0.01)
        
        self.assertEqual(levels[5][0], "0.786 Fib Ret")
        self.assertAlmostEqual(levels[5][1], 100 * (1 - 0.786), delta=0.01)
    
    def test_display_market_wisdom(self):
        """Test market wisdom quote generation"""
        # Test multiple frame counters
        for i in range(10):
            self.test_monitor.frame_counter = i
            wisdom = self.test_monitor.display_market_wisdom()
            
            # Verify we got a non-empty string
            self.assertIsInstance(wisdom, str)
            self.assertTrue(len(wisdom) > 0)
    
    @patch('builtins.print')
    def test_print_position(self, mock_print):
        """Test position printing with mocked print function"""
        # Call the method
        self.test_monitor.print_position(self.phi_position)
        
        # Check that print was called
        mock_print.assert_called()
        
        # Get all the calls as a single string
        output = ''.join(call[0][0] for call in mock_print.call_args_list if call[0])
        
        # Check output content
        self.assertIn("POSITION", output.upper())
        self.assertIn("BTC", output)
        self.assertIn("LONG", output.upper())
        self.assertIn("1.618034", output)
        self.assertIn("40000", output)
        self.assertIn("42000", output)
        self.assertIn("1618.03", output)
        self.assertIn("32000", output)
        self.assertIn("FIB", output.upper())  # Check for FIB instead of Fibonacci
    
    @patch('builtins.print')
    def test_print_position_quantum(self, mock_print):
        """Test printing of extremely small position"""
        # Call the method
        self.test_monitor.print_position(self.quantum_position)
        
        # Check that print was called
        mock_print.assert_called()
        
        # Get all the calls as a single string
        output = ''.join(call[0][0] for call in mock_print.call_args_list if call[0])
        
        # Check output content
        self.assertIn("SOL", output)
        self.assertIn("LONG", output.upper())
        self.assertIn("1e-09", output)  # Check for scientific notation instead of raw value
        self.assertIn("$0.00", output)  # Extremely small amount should display as $0.00
        self.assertIn("$101.00", output)
        self.assertIn("$50.00", output)  # Liquidation price
    
    @patch('builtins.print')
    def test_print_changes_empty(self, mock_print):
        """Test printing when there are no position changes"""
        # Call with None changes
        self.test_monitor.print_changes(None)
        
        # Should not call print
        mock_print.assert_not_called()
    
    @patch('builtins.print')
    def test_print_changes_all_types(self, mock_print):
        """Test printing all types of position changes"""
        # Create a changes object with all types
        changes = {
            "new": [self.phi_position],
            "closed": [self.schumann_position],
            "changed": [{
                "position": self.quantum_position,
                "prev_contracts": 0.0000000005,
                "prev_pnl": 0.000000021
            }]
        }
        
        # Call the method
        self.test_monitor.print_changes(changes)
        
        # Verify print was called
        self.assertTrue(mock_print.call_count > 5)
        
        # Get all print calls
        calls = [call_args[0][0] for call_args in mock_print.call_args_list]
        output = '\n'.join(str(call_arg) for call_arg in calls)
        
        # Check for expected content
        self.assertIn("POSITION CHANGES DETECTED", output)
        self.assertIn("NEW POSITIONS", output)
        self.assertIn("CLOSED POSITIONS", output)
        self.assertIn("CHANGED POSITIONS", output)
        self.assertIn("BTC/USDT:USDT", output)
        self.assertIn("ETH/USDT:USDT", output)
        self.assertIn("SOL/USDT:USDT", output)
    
    @patch('os.system')
    @patch('builtins.print')
    def test_display_dashboard_error(self, mock_print, mock_system):
        """Test dashboard display with error data"""
        # Error data
        error_data = {"error": "Test error message"}
        
        # Call the method
        self.test_monitor.display_dashboard(error_data)
        
        # Verify the screen was cleared
        mock_system.assert_called_once()
        
        # Verify error message was printed
        calls = [call_args[0][0] for call_args in mock_print.call_args_list if isinstance(call_args[0][0], str)]
        output = '\n'.join(call_arg for call_arg in calls)
        self.assertIn("ERROR", output)
        self.assertIn("Test error message", output)
    
    @patch('os.system')
    @patch('builtins.print')
    def test_display_dashboard_no_positions(self, mock_print, mock_system):
        """Test dashboard display with no positions"""
        # Data with no positions
        no_positions_data = {
            "success": True,
            "positions": [],
            "timestamp": "2025-01-01 12:00:00",
            "connection": "CONNECTED TO BITGET MAINNET"
        }
        
        # Call the method
        self.test_monitor.display_dashboard(no_positions_data)
        
        # Verify the screen was cleared
        mock_system.assert_called_once()
        
        # Verify message was printed
        calls = [call_args[0][0] for call_args in mock_print.call_args_list if isinstance(call_args[0][0], str)]
        output = '\n'.join(call_arg for call_arg in calls)
        self.assertIn("NO ACTIVE POSITIONS FOUND", output)
    
    @patch('os.system')
    @patch('builtins.print')
    def test_display_dashboard_with_positions(self, mock_print, mock_system):
        """Test dashboard display with active positions"""
        # Data with positions
        positions_data = {
            "success": True,
            "positions": [self.phi_position, self.schumann_position],
            "timestamp": "2025-01-01 12:00:00",
            "connection": "CONNECTED TO BITGET MAINNET"
        }
        
        # Call the method
        self.test_monitor.display_dashboard(positions_data)
        
        # Verify the screen was cleared
        mock_system.assert_called_once()
        
        # Verify required sections were printed
        calls = [call_args[0][0] for call_args in mock_print.call_args_list if isinstance(call_args[0][0], str)]
        output = '\n'.join(call_arg for call_arg in calls)
        
        self.assertIn("PORTFOLIO OVERVIEW", output)
        self.assertIn("Long Positions", output)
        self.assertIn("Short Positions", output)
        self.assertIn("Total Notional", output)
        self.assertIn("DIVINE METRICS", output)
        self.assertIn("RASTA TRADING WISDOM", output)
    
    @patch('time.sleep')
    def test_run_keyboard_interrupt(self, mock_sleep):
        """Test run method handling KeyboardInterrupt"""
        # Mock get_positions to return valid data
        self.test_monitor.get_positions = MagicMock(return_value={
            "success": True,
            "positions": [self.phi_position],
            "timestamp": "2025-01-01 12:00:00",
            "connection": "CONNECTED TO BITGET MAINNET"
        })
        
        # Mock display_dashboard
        self.test_monitor.display_dashboard = MagicMock()
        
        # Mock signal_handler
        self.test_monitor._signal_handler = MagicMock()
        
        # Make sleep raise KeyboardInterrupt after first call
        mock_sleep.side_effect = [None, KeyboardInterrupt()]
        
        # Call the method
        self.test_monitor.run()
        
        # Verify signal handler was called
        self.test_monitor._signal_handler.assert_called_once()
    
    @patch('simple_bitget_positions.argparse.ArgumentParser')
    def test_parse_arguments(self, mock_argparse):
        """Test command line argument parsing"""
        # Mock ArgumentParser
        mock_parser = MagicMock()
        mock_argparse.return_value = mock_parser
        
        # Mock parse_args result
        mock_args = MagicMock()
        mock_args.interval = 10
        mock_args.no_color = True
        mock_args.debug = True
        mock_parser.parse_args.return_value = mock_args
        
        # Call the function
        args = monitor.parse_arguments()
        
        # Verify results
        self.assertEqual(args.interval, 10)
        self.assertTrue(args.no_color)
        self.assertTrue(args.debug)
        
    @patch('simple_bitget_positions.RastaBitgetMonitor')
    @patch('simple_bitget_positions.parse_arguments')
    def test_main(self, mock_parse_args, mock_monitor_class):
        """Test the main function"""
        # Set up mocks
        mock_args = MagicMock()
        mock_args.interval = 10
        mock_args.no_color = True
        mock_args.debug = True
        mock_args.harmony_advisor = False  # Add harmony advisor parameter
        mock_parse_args.return_value = mock_args
        
        # Set up the monitor mock
        mock_monitor = MagicMock()
        mock_monitor.run.return_value = None
        mock_monitor_class.return_value = mock_monitor
        
        # Call the main function
        monitor.main()
        
        # Verify the monitor was created with correct parameters
        mock_monitor_class.assert_called_once_with(
            interval=10,
            use_color=False,
            debug=True,
            harmony_advisor=False  # Include harmony_advisor parameter
        )
        
        # Verify run was called
        mock_monitor.run.assert_called_once()

if __name__ == '__main__':
    unittest.main() 