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
Test suite for the BaseB0t class.

This module contains tests for the BaseB0t class functionality including:
- Initialization
- Logging
- State management
- Environment loading
- Utility methods
"""

import os
import sys
import json
import logging
import random
import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime
import importlib

# Add the parent directory to sys.path to allow importing the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../')))

# Import the class under test
from src.omega_bot_farm.trading.b0ts.core.base_b0t import BaseB0t
from src.omega_bot_farm.trading.b0ts.core.base_b0t import FIBONACCI_SEQUENCE, PHI, INVERSE_PHI


class TestBaseB0t(unittest.TestCase):
    """Tests for the BaseB0t class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test state files
        self.temp_dir = tempfile.mkdtemp()
        # Create a test bot instance
        self.test_bot = BaseB0t(
            name="TestB0t",
            log_level="INFO",
            seed=42,
            state_dir=self.temp_dir
        )

    def tearDown(self):
        """Tear down test fixtures."""
        # Remove the temporary directory
        shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test the initialization of BaseB0t."""
        # Verify basic attributes
        self.assertEqual(self.test_bot.name, "TestB0t")
        self.assertEqual(self.test_bot.version, "1.0.0")
        self.assertEqual(self.test_bot.seed, 42)
        self.assertEqual(self.test_bot.state_dir, self.temp_dir)
        self.assertTrue(self.test_bot.initialized)
        
        # Check default state entries
        self.assertIn("created_at", self.test_bot.state)
        self.assertIn("version", self.test_bot.state)
        self.assertIn("name", self.test_bot.state)
        self.assertIn("seed", self.test_bot.state)
        self.assertIn("last_updated", self.test_bot.state)
        
        # Test random initialization
        self.assertEqual(self.test_bot.random.random(), random.Random(42).random())
    
    def test_custom_version(self):
        """Test custom version attribute."""
        class CustomVersionB0t(BaseB0t):
            VERSION = "2.1.0"
        
        custom_bot = CustomVersionB0t(name="CustomVersionB0t")
        self.assertEqual(custom_bot.version, "2.1.0")
        self.assertEqual(custom_bot.state["version"], "2.1.0")
    
    def test_default_name(self):
        """Test default name behavior (uses class name)."""
        class NoNameB0t(BaseB0t):
            pass
        
        no_name_bot = NoNameB0t()
        self.assertEqual(no_name_bot.name, "NoNameB0t")
    
    def test_logger_setup(self):
        """Test logger configuration."""
        # Test logger name
        self.assertEqual(self.test_bot.logger.name, "omega_bot_farm.TestB0t")
        
        # Test logger level
        self.assertEqual(self.test_bot.logger.level, logging.INFO)
        
        # Test with different log level
        debug_bot = BaseB0t(name="DebugB0t", log_level="DEBUG")
        self.assertEqual(debug_bot.logger.level, logging.DEBUG)
        
        # Test with invalid log level (should default to INFO)
        invalid_level_bot = BaseB0t(name="InvalidLevelB0t", log_level="INVALID")
        self.assertEqual(invalid_level_bot.logger.level, logging.INFO)
    
    @patch('src.omega_bot_farm.utils.env_loader.load_environment')
    def test_environment_loading_success(self, mock_load_env):
        """Test successful environment loading."""
        # Set up the mock to return True
        mock_load_env.return_value = True
        
        # Call the method
        result = self.test_bot._load_environment()
        
        # Verify the result
        self.assertTrue(result)
        mock_load_env.assert_called_once()
    
    @patch('src.omega_bot_farm.utils.env_loader.load_environment')
    def test_environment_loading_empty(self, mock_load_env):
        """Test environment loading with no .env files."""
        # Set up the mock to return False
        mock_load_env.return_value = False
        
        # Call the method
        result = self.test_bot._load_environment()
        
        # Verify the result
        self.assertFalse(result)
        mock_load_env.assert_called_once()
    
    def test_environment_loading_import_error(self):
        """Test environment loading when env_loader module is not available."""
        # Instead of testing the actual import, let's directly test the behavior
        # by calling the method and making sure it handles ImportError correctly
        original_import = __import__
        
        def mock_import(name, *args, **kwargs):
            if 'src.omega_bot_farm.utils.env_loader' in name:
                raise ImportError("Module not found")
            return original_import(name, *args, **kwargs)
        
        # Patch the built-in import function
        with patch('builtins.__import__', side_effect=mock_import):
            # Create a new bot to trigger the import error
            bot = BaseB0t(name="ImportErrorB0t")
            
            # The bot should still initialize successfully despite the import error
            self.assertTrue(bot.initialized)
    
    def test_state_management(self):
        """Test state update and retrieval."""
        # Update state
        self.test_bot.update_state({
            "test_key": "test_value",
            "number": 42,
            "nested": {"a": 1, "b": 2}
        })
        
        # Test individual key retrieval
        self.assertEqual(self.test_bot.get_state("test_key"), "test_value")
        self.assertEqual(self.test_bot.get_state("number"), 42)
        self.assertEqual(self.test_bot.get_state("nested"), {"a": 1, "b": 2})
        
        # Test default value for non-existent key
        self.assertIsNone(self.test_bot.get_state("non_existent"))
        self.assertEqual(self.test_bot.get_state("non_existent", "default_value"), "default_value")
        
        # Test that last_updated was updated
        original_last_updated = self.test_bot.state["last_updated"]
        
        # Update again
        self.test_bot.update_state({"another_key": "another_value"})
        
        # Verify last_updated was changed
        self.assertNotEqual(self.test_bot.state["last_updated"], original_last_updated)
        
        # Test get_full_state
        full_state = self.test_bot.get_full_state()
        self.assertIn("test_key", full_state)
        self.assertIn("number", full_state)
        self.assertIn("nested", full_state)
        self.assertIn("another_key", full_state)
        self.assertIn("uptime_seconds", full_state)
        self.assertIn("snapshot_time", full_state)
    
    def test_save_and_load_state(self):
        """Test saving and loading state to/from file."""
        # Update state with test data
        self.test_bot.update_state({
            "test_key": "test_value",
            "number": 42,
            "nested": {"a": 1, "b": 2}
        })
        
        # Save state
        result = self.test_bot.save_state()
        self.assertTrue(result)
        
        # Verify file exists
        expected_path = os.path.join(self.temp_dir, "testb0t_state.json")
        self.assertTrue(os.path.exists(expected_path))
        
        # Create a new bot and load the state
        new_bot = BaseB0t(name="TestB0t", state_dir=self.temp_dir)
        result = new_bot.load_state()
        self.assertTrue(result)
        
        # Verify state was loaded correctly
        self.assertEqual(new_bot.get_state("test_key"), "test_value")
        self.assertEqual(new_bot.get_state("number"), 42)
        self.assertEqual(new_bot.get_state("nested"), {"a": 1, "b": 2})
    
    def test_load_state_missing_file(self):
        """Test loading state when file doesn't exist."""
        # Try to load non-existent state file
        result = self.test_bot.load_state("non_existent_state.json")
        self.assertFalse(result)
    
    def test_save_state_directory_creation(self):
        """Test save_state creates directory if it doesn't exist."""
        # Set a non-existent directory
        new_dir = os.path.join(self.temp_dir, "new_dir")
        self.test_bot.state_dir = new_dir
        
        # Save state (should create directory)
        result = self.test_bot.save_state()
        self.assertTrue(result)
        
        # Verify directory was created
        self.assertTrue(os.path.exists(new_dir))
        self.assertTrue(os.path.exists(os.path.join(new_dir, "testb0t_state.json")))
    
    def test_custom_state_filename(self):
        """Test saving and loading with custom filename."""
        # Update state
        self.test_bot.update_state({"custom_key": "custom_value"})
        
        # Save with custom filename
        custom_filename = "custom_state.json"
        result = self.test_bot.save_state(custom_filename)
        self.assertTrue(result)
        
        # Verify file exists
        expected_path = os.path.join(self.temp_dir, custom_filename)
        self.assertTrue(os.path.exists(expected_path))
        
        # Load with custom filename
        self.test_bot.state = {}  # Clear state
        result = self.test_bot.load_state(custom_filename)
        self.assertTrue(result)
        
        # Verify state was loaded
        self.assertEqual(self.test_bot.get_state("custom_key"), "custom_value")
    
    def test_save_state_error_handling(self):
        """Test error handling in save_state."""
        # Mock open to raise an exception
        with patch('builtins.open', side_effect=Exception("Test exception")):
            result = self.test_bot.save_state()
            self.assertFalse(result)
    
    def test_load_state_error_handling(self):
        """Test error handling in load_state."""
        # Create a file but mock open to raise an exception
        with open(os.path.join(self.temp_dir, "testb0t_state.json"), 'w') as f:
            f.write('{"test": "data"}')
            
        with patch('builtins.open', side_effect=Exception("Test exception")):
            result = self.test_bot.load_state()
            self.assertFalse(result)
    
    def test_load_state_json_error(self):
        """Test handling of invalid JSON in state file."""
        # Create a file with invalid JSON
        with open(os.path.join(self.temp_dir, "testb0t_state.json"), 'w') as f:
            f.write('{"invalid json')
            
        result = self.test_bot.load_state()
        self.assertFalse(result)
    
    def test_calculate_divine_proportion(self):
        """Test golden ratio calculations."""
        # Test with value 1.0
        result = self.test_bot.calculate_divine_proportion(1.0)
        self.assertEqual(result["phi"], PHI)
        self.assertEqual(result["inverse_phi"], INVERSE_PHI)
        self.assertEqual(result["phi_squared"], PHI * PHI)
        self.assertEqual(result["phi_cubed"], PHI * PHI * PHI)
        self.assertEqual(result["phi_inverse_squared"], INVERSE_PHI * INVERSE_PHI)
        
        # Test with value 100.0
        result = self.test_bot.calculate_divine_proportion(100.0)
        self.assertEqual(result["phi"], 100.0 * PHI)
        self.assertEqual(result["inverse_phi"], 100.0 * INVERSE_PHI)
        self.assertEqual(result["phi_squared"], 100.0 * PHI * PHI)
        self.assertEqual(result["phi_cubed"], 100.0 * PHI * PHI * PHI)
        self.assertEqual(result["phi_inverse_squared"], 100.0 * INVERSE_PHI * INVERSE_PHI)
    
    def test_format_with_color(self):
        """Test color formatting for values."""
        from src.omega_bot_farm.trading.b0ts.core.base_b0t import GREEN, RED, YELLOW, RESET
        
        # Test positive value (default is_positive_good=True)
        formatted = self.test_bot.format_with_color(42.5)
        self.assertEqual(formatted, f"{GREEN}42.50{RESET}")
        
        # Test negative value (default is_positive_good=True)
        formatted = self.test_bot.format_with_color(-42.5)
        self.assertEqual(formatted, f"{RED}-42.50{RESET}")
        
        # Test zero value
        formatted = self.test_bot.format_with_color(0.0)
        self.assertEqual(formatted, f"{YELLOW}0.00{RESET}")
        
        # Test positive value with is_positive_good=False
        formatted = self.test_bot.format_with_color(42.5, is_positive_good=False)
        self.assertEqual(formatted, f"{RED}42.50{RESET}")
        
        # Test negative value with is_positive_good=False
        formatted = self.test_bot.format_with_color(-42.5, is_positive_good=False)
        self.assertEqual(formatted, f"{GREEN}-42.50{RESET}")
        
        # Test string conversion
        formatted = self.test_bot.format_with_color("42.5")
        self.assertEqual(formatted, f"{GREEN}42.50{RESET}")
        
        # Test invalid string (should return as-is)
        formatted = self.test_bot.format_with_color("not_a_number")
        self.assertEqual(formatted, "not_a_number")
    
    def test_get_name(self):
        """Test the get_name method."""
        # Test with default name
        self.assertEqual(self.test_bot.get_name(), "TestB0t")
        
        # Test with custom name
        custom_bot = BaseB0t(name="CustomNameBot")
        self.assertEqual(custom_bot.get_name(), "CustomNameBot")
        
        # Test with class name as default
        class NoNameB0t(BaseB0t):
            pass
        
        no_name_bot = NoNameB0t()
        self.assertEqual(no_name_bot.get_name(), "NoNameB0t")
    
    def test_get_version(self):
        """Test the get_version method."""
        # Test with default version
        self.assertEqual(self.test_bot.get_version(), "1.0.0")
        
        # Test with custom version
        class CustomVersionB0t(BaseB0t):
            VERSION = "2.1.0"
        
        custom_bot = CustomVersionB0t()
        self.assertEqual(custom_bot.get_version(), "2.1.0")
    
    def test_str_representation(self):
        """Test string representation."""
        self.assertEqual(str(self.test_bot), "TestB0t v1.0.0")
    
    def test_repr_representation(self):
        """Test repr representation."""
        self.assertEqual(repr(self.test_bot), "BaseB0t(name='TestB0t', version='1.0.0')")


if __name__ == '__main__':
    unittest.main() 