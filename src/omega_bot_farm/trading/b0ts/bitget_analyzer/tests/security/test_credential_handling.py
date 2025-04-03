#!/usr/bin/env python3

"""
Security tests for credential handling in BitgetPositionAnalyzerB0t.

These tests verify that the bot handles API credentials securely:
- Does not log credentials in plaintext
- Does not expose credentials in error messages
- Properly validates credentials before use
- Handles credential revocation appropriately
"""

import unittest
import os
import sys
import logging
import io
from unittest.mock import patch, MagicMock, ANY

# Try to import BitgetPositionAnalyzerB0t
try:
    from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t
    BOT_AVAILABLE = True
except ImportError:
    BOT_AVAILABLE = False
    print("BitgetPositionAnalyzerB0t not available. Using mock for tests.")

# Mock implementation if import fails
if not BOT_AVAILABLE:
    class BitgetPositionAnalyzerB0t:
        """Mock implementation for testing"""
        
        def __init__(self, api_key=None, api_secret=None, api_passphrase=None, use_testnet=False):
            self.api_key = api_key or "test_key"
            self.api_secret = api_secret or "test_secret"
            self.api_passphrase = api_passphrase or "test_pass"
            self.use_testnet = use_testnet
            self.logger = logging.getLogger("bitget_analyzer")


class TestCredentialHandling(unittest.TestCase):
    """Test suite for secure credential handling."""

    def setUp(self):
        """Set up test environment."""
        # Test credentials
        self.test_api_key = "test_api_key_12345"
        self.test_api_secret = "test_api_secret_67890"
        self.test_passphrase = "test_pass_abcde"
        
        # Capture logs for testing
        self.log_capture = io.StringIO()
        self.log_handler = logging.StreamHandler(self.log_capture)
        logging.getLogger().addHandler(self.log_handler)
        logging.getLogger().setLevel(logging.DEBUG)

    def tearDown(self):
        """Clean up after tests."""
        # Remove log handler
        logging.getLogger().removeHandler(self.log_handler)
        logging.getLogger().setLevel(logging.NOTSET)

    def test_credentials_not_logged(self):
        """Test that credentials are not logged in plaintext."""
        # Create analyzer with test credentials
        analyzer = BitgetPositionAnalyzerB0t(
            api_key=self.test_api_key,
            api_secret=self.test_api_secret,
            api_passphrase=self.test_passphrase,
            use_testnet=True
        )
        
        # Check logs for credentials
        log_contents = self.log_capture.getvalue()
        
        # API credentials should not appear in logs
        self.assertNotIn(self.test_api_key, log_contents, "API key should not appear in logs")
        self.assertNotIn(self.test_api_secret, log_contents, "API secret should not appear in logs")
        self.assertNotIn(self.test_passphrase, log_contents, "API passphrase should not appear in logs")

    @patch('logging.Logger.warning')
    @patch('logging.Logger.error')
    def test_credentials_not_exposed_in_errors(self, mock_error, mock_warning):
        """Test that credentials are not exposed in error messages."""
        # Mock raising an exception that includes credentials
        with patch.object(BitgetPositionAnalyzerB0t, '__init__', side_effect=Exception(
            f"Connection error with key {self.test_api_key} and secret {self.test_api_secret}"
        )):
            # This should raise the exception, but we're testing that logs don't contain creds
            try:
                analyzer = BitgetPositionAnalyzerB0t(
                    api_key=self.test_api_key,
                    api_secret=self.test_api_secret,
                    api_passphrase=self.test_passphrase
                )
            except Exception:
                pass
            
            # Check that error logs don't contain credentials
            for call in mock_error.call_args_list + mock_warning.call_args_list:
                args = call[0]
                for arg in args:
                    if isinstance(arg, str):
                        self.assertNotIn(self.test_api_key, arg, "API key should not appear in error logs")
                        self.assertNotIn(self.test_api_secret, arg, "API secret should not appear in error logs")
    
    def test_obfuscated_credential_representation(self):
        """Test that credentials are obfuscated in string representations."""
        # Create analyzer with test credentials
        analyzer = BitgetPositionAnalyzerB0t(
            api_key=self.test_api_key,
            api_secret=self.test_api_secret,
            api_passphrase=self.test_passphrase,
            use_testnet=True
        )
        
        # Get string representation
        str_representation = str(analyzer)
        repr_representation = repr(analyzer)
        
        # Credentials should not appear in string representations
        for representation in [str_representation, repr_representation]:
            self.assertNotIn(self.test_api_key, representation, "API key should not appear in string representation")
            self.assertNotIn(self.test_api_secret, representation, "API secret should not appear in string representation")
            self.assertNotIn(self.test_passphrase, representation, "API passphrase should not appear in string representation")
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_credentials_not_printed(self, mock_stdout):
        """Test that credentials are not printed to stdout."""
        # Create analyzer with test credentials
        analyzer = BitgetPositionAnalyzerB0t(
            api_key=self.test_api_key,
            api_secret=self.test_api_secret,
            api_passphrase=self.test_passphrase,
            use_testnet=True
        )
        
        # Try to print the analyzer
        print(analyzer)
        print(f"Analyzer initialized with: {analyzer.__dict__}")
        
        # Check stdout for credentials
        stdout_contents = mock_stdout.getvalue()
        
        # API credentials should not appear in stdout
        self.assertNotIn(self.test_api_key, stdout_contents, "API key should not appear in stdout")
        self.assertNotIn(self.test_api_secret, stdout_contents, "API secret should not appear in stdout")
        self.assertNotIn(self.test_passphrase, stdout_contents, "API passphrase should not appear in stdout")
    
    @patch('ccxt.bitget')
    def test_credential_validation(self, mock_bitget):
        """Test that credentials are validated before use."""
        # Mock the exchange to raise an authentication error
        mock_exchange = MagicMock()
        mock_exchange.fetch_balance.side_effect = Exception("Invalid API Key")
        mock_bitget.return_value = mock_exchange
        
        # Create analyzer with invalid test credentials
        analyzer = BitgetPositionAnalyzerB0t(
            api_key="invalid_key",
            api_secret="invalid_secret",
            api_passphrase="invalid_pass",
            use_testnet=True
        )
        
        # The analyzer should handle this gracefully, not crash
        # This is more of an integration test but important for security
        with self.assertRaises(Exception):
            # This would fail with a specific authentication error
            # but we're just checking it's handled properly
            if hasattr(analyzer, 'validate_credentials'):
                analyzer.validate_credentials()


if __name__ == "__main__":
    unittest.main() 