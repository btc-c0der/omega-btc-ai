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
Test suite for the DivineEnvLoader component.

These tests verify that the environment loader can properly find,
load, and validate environment variables from various locations.
"""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock

# Import the component to test
from omega_bots_bundle.utils.env_loader import DivineEnvLoader, load_environment, validate_exchange_credentials


class TestDivineEnvLoader(unittest.TestCase):
    """Test suite for the DivineEnvLoader component."""

    def setUp(self):
        """Set up test fixtures."""
        # Save original environment
        self.original_environ = os.environ.copy()
        
        # Create a test environment with mock credentials
        self.test_env = {
            "BITGET_API_KEY": "test_api_key",
            "BITGET_SECRET_KEY": "test_secret_key",
            "BITGET_PASSPHRASE": "test_passphrase",
            "BINANCE_API_KEY": "test_binance_key",
            "BINANCE_SECRET_KEY": "test_binance_secret"
        }
        
    def tearDown(self):
        """Tear down test fixtures."""
        # Restore original environment
        os.environ.clear()
        os.environ.update(self.original_environ)
    
    @patch('pathlib.Path.exists')
    @patch('dotenv.load_dotenv')
    def test_load_environment(self, mock_load_dotenv, mock_exists):
        """Test that the environment loader can find and load .env files."""
        # Mock the existence of .env files
        mock_exists.return_value = True
        
        # Mock successful loading of .env files
        mock_load_dotenv.return_value = True
        
        # Create loader and load environment
        loader = DivineEnvLoader(load_immediately=False, verbose=True)
        result = loader.load_environment()
        
        # Verify results
        self.assertTrue(result)
        self.assertTrue(mock_load_dotenv.called)
    
    @patch('os.environ', new_callable=dict)
    def test_validate_credentials(self, mock_environ):
        """Test validation of required credentials."""
        # Set up test environment
        mock_environ.update(self.test_env)
        
        # Create loader
        loader = DivineEnvLoader(load_immediately=False)
        
        # Test valid credentials
        bitget_keys = {"BITGET_API_KEY", "BITGET_SECRET_KEY", "BITGET_PASSPHRASE"}
        self.assertTrue(loader.validate_credentials(bitget_keys))
        
        # Test missing credentials
        missing_keys = {"BITGET_API_KEY", "NONEXISTENT_KEY"}
        self.assertFalse(loader.validate_credentials(missing_keys))
    
    @patch('os.environ', new_callable=dict)
    def test_validate_exchange_credentials(self, mock_environ):
        """Test validation of exchange-specific credentials."""
        # Set up test environment
        mock_environ.update(self.test_env)
        
        # Create loader
        loader = DivineEnvLoader(load_immediately=False)
        
        # Test valid exchange credentials
        self.assertTrue(loader.validate_exchange_credentials("bitget"))
        self.assertTrue(loader.validate_exchange_credentials("binance"))
        
        # Test missing exchange credentials
        self.assertFalse(loader.validate_exchange_credentials("kucoin"))
    
    def test_generate_env_template(self):
        """Test generation of environment templates."""
        # Create loader
        loader = DivineEnvLoader(load_immediately=False)
        
        # Generate template for all exchanges
        template_all = loader.generate_env_template()
        
        # Check that template contains expected sections
        self.assertIn("BITGET_API_KEY", template_all)
        self.assertIn("BINANCE_API_KEY", template_all)
        
        # Generate template for specific exchange
        template_bitget = loader.generate_env_template("bitget")
        
        # Check that template contains only bitget credentials
        self.assertIn("BITGET_API_KEY", template_bitget)
        self.assertNotIn("BINANCE_API_KEY", template_bitget)
    
    @patch('builtins.open', new_callable=mock_open)
    def test_save_env_template(self, mock_file):
        """Test saving environment templates to file."""
        # Create loader
        loader = DivineEnvLoader(load_immediately=False)
        
        # Save template
        result = loader.save_env_template(".env.test", "bitget")
        
        # Verify results
        self.assertTrue(result)
        mock_file.assert_called_once_with(".env.test", "w")
        handle = mock_file()
        self.assertTrue(handle.write.called)


class TestGlobalFunctions(unittest.TestCase):
    """Test suite for the global helper functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Save original environment
        self.original_environ = os.environ.copy()
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Restore original environment
        os.environ.clear()
        os.environ.update(self.original_environ)
    
    @patch('omega_bots_bundle.utils.env_loader.DivineEnvLoader')
    def test_load_environment_global(self, mock_loader_class):
        """Test the global load_environment function."""
        # Mock loader instance
        mock_loader = MagicMock()
        mock_loader.load_environment.return_value = True
        mock_loader_class.return_value = mock_loader
        
        # Call the global function
        result = load_environment(verbose=True)
        
        # Verify results
        self.assertTrue(result)
        mock_loader_class.assert_called_once_with(load_immediately=False, verbose=True)
        mock_loader.load_environment.assert_called_once()
    
    @patch('omega_bots_bundle.utils.env_loader.DivineEnvLoader')
    def test_validate_exchange_credentials_global(self, mock_loader_class):
        """Test the global validate_exchange_credentials function."""
        # Mock loader instance
        mock_loader = MagicMock()
        mock_loader.validate_exchange_credentials.return_value = True
        mock_loader_class.return_value = mock_loader
        
        # Call the global function
        result = validate_exchange_credentials("bitget", verbose=True)
        
        # Verify results
        self.assertTrue(result)
        mock_loader.validate_exchange_credentials.assert_called_once_with("bitget")


if __name__ == '__main__':
    unittest.main() 