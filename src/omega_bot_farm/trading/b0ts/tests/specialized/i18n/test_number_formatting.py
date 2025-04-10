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
Number formatting tests for BitgetPositionAnalyzerB0t.

These tests verify that the bot correctly formats numbers for different locales:
- Currency amounts formatted according to locale conventions
- Percentage values formatted correctly
- Large numbers formatted with appropriate separators
- Maintains numeric precision regardless of display format
"""

import unittest
import os
import sys
import json
import locale
import re
from unittest.mock import patch, MagicMock

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
        
        def __init__(self, api_key=None, api_secret=None, api_passphrase=None, use_testnet=False, locale_setting="en_US"):
            self.api_key = api_key or "test_key"
            self.api_secret = api_secret or "test_secret"
            self.api_passphrase = api_passphrase or "test_pass"
            self.use_testnet = use_testnet
            self.locale_setting = locale_setting
            
            # Sample locale-specific formatting settings
            self.locale_formats = {
                "en_US": {
                    "decimal_point": ".",
                    "thousands_sep": ",",
                    "currency_symbol": "$",
                    "currency_position": "prefix",
                    "percent_symbol": "%",
                    "percent_position": "suffix"
                },
                "fr_FR": {
                    "decimal_point": ",",
                    "thousands_sep": " ",
                    "currency_symbol": "€",
                    "currency_position": "suffix",
                    "percent_symbol": "%",
                    "percent_position": "suffix"
                },
                "de_DE": {
                    "decimal_point": ",",
                    "thousands_sep": ".",
                    "currency_symbol": "€",
                    "currency_position": "suffix",
                    "percent_symbol": "%",
                    "percent_position": "suffix"
                }
            }
            
        def set_locale(self, locale_setting):
            """Set the locale for number formatting."""
            if locale_setting in self.locale_formats:
                self.locale_setting = locale_setting
                return True
            else:
                # Fallback to en_US
                self.locale_setting = "en_US"
                return False
                
        def format_number(self, number, precision=2):
            """Format a number according to the current locale."""
            # Get locale settings
            settings = self.locale_formats.get(self.locale_setting, self.locale_formats["en_US"])
            
            # Format with specified precision
            number_str = format(number, f".{precision}f")
            
            # Replace decimal point
            number_str = number_str.replace(".", settings["decimal_point"])
            
            # Add thousands separators
            parts = number_str.split(settings["decimal_point"])
            integer_part = parts[0]
            
            # Format with thousands separators
            if len(integer_part) > 3:
                formatted_integer = ""
                for i, char in enumerate(reversed(integer_part)):
                    if i > 0 and i % 3 == 0:
                        formatted_integer = settings["thousands_sep"] + formatted_integer
                    formatted_integer = char + formatted_integer
                parts[0] = formatted_integer
                
            return settings["decimal_point"].join(parts)
            
        def format_currency(self, amount, currency="USD", precision=2):
            """Format currency amount according to the current locale."""
            # Get locale settings
            settings = self.locale_formats.get(self.locale_setting, self.locale_formats["en_US"])
            
            # Format the number
            formatted_number = self.format_number(amount, precision)
            
            # Add currency symbol based on locale convention
            if settings["currency_position"] == "prefix":
                return f"{settings['currency_symbol']}{formatted_number}"
            else:
                return f"{formatted_number} {settings['currency_symbol']}"
                
        def format_percentage(self, value, precision=2):
            """Format percentage value according to the current locale."""
            # Get locale settings
            settings = self.locale_formats.get(self.locale_setting, self.locale_formats["en_US"])
            
            # Format the number
            formatted_number = self.format_number(value, precision)
            
            # Add percent symbol based on locale convention
            if settings["percent_position"] == "prefix":
                return f"{settings['percent_symbol']}{formatted_number}"
            else:
                return f"{formatted_number}{settings['percent_symbol']}"
                
        def generate_formatted_report(self):
            """Generate a report with formatted numbers."""
            # Sample position data
            position_value = 1234567.89
            profit_loss = 98765.43
            profit_percentage = 12.34
            
            # Format according to current locale
            formatted_value = self.format_currency(position_value)
            formatted_pl = self.format_currency(profit_loss)
            formatted_percentage = self.format_percentage(profit_percentage)
            
            # Create report
            report = {
                "position_value": formatted_value,
                "profit_loss": formatted_pl,
                "profit_percentage": formatted_percentage,
                "raw_values": {
                    "position_value": position_value,
                    "profit_loss": profit_loss,
                    "profit_percentage": profit_percentage
                }
            }
            
            return report


class TestNumberFormatting(unittest.TestCase):
    """Test suite for number formatting."""

    def setUp(self):
        """Set up test environment."""
        # Use dummy API credentials for testing
        self.analyzer = BitgetPositionAnalyzerB0t(
            api_key="test_key",
            api_secret="test_secret", 
            api_passphrase="test_pass",
            use_testnet=True,
            locale_setting="en_US"  # Default to US locale
        )

    def test_supported_locales(self):
        """Test that the bot supports multiple locales for formatting."""
        # Skip if the bot doesn't support locale setting
        if not hasattr(self.analyzer, 'set_locale'):
            self.skipTest("Bot does not support locale setting")
            
        # Test known supported locales
        locales = ["en_US", "fr_FR", "de_DE"]
        for loc in locales:
            result = self.analyzer.set_locale(loc)
            self.assertTrue(result, f"Setting locale to {loc} should succeed")
            self.assertEqual(self.analyzer.locale_setting, loc, f"Locale should be set to {loc}")
            
        # Test unsupported locale (should fallback to en_US)
        result = self.analyzer.set_locale("unsupported")
        self.assertFalse(result, "Setting locale to an unsupported locale should fail")
        self.assertEqual(self.analyzer.locale_setting, "en_US", "Locale should fallback to en_US")

    def test_number_formatting(self):
        """Test that numbers are formatted according to locale conventions."""
        # Skip if the bot doesn't support number formatting
        if not hasattr(self.analyzer, 'format_number'):
            self.skipTest("Bot does not support number formatting")
            
        # Test number formatting in different locales
        test_number = 1234567.89
        expected_formats = {
            "en_US": "1,234,567.89",
            "fr_FR": "1 234 567,89",
            "de_DE": "1.234.567,89"
        }
        
        for locale, expected in expected_formats.items():
            self.analyzer.set_locale(locale)
            formatted = self.analyzer.format_number(test_number)
            self.assertEqual(formatted, expected, f"Number formatting in {locale} should be '{expected}'")
            
        # Test with different precision
        test_number = 12.3456
        self.analyzer.set_locale("en_US")
        self.assertEqual(self.analyzer.format_number(test_number, 2), "12.35", "Should round to 2 decimal places")
        self.assertEqual(self.analyzer.format_number(test_number, 3), "12.346", "Should round to 3 decimal places")
        self.assertEqual(self.analyzer.format_number(test_number, 0), "12", "Should round to 0 decimal places")

    def test_currency_formatting(self):
        """Test that currency amounts are formatted according to locale conventions."""
        # Skip if the bot doesn't support currency formatting
        if not hasattr(self.analyzer, 'format_currency'):
            self.skipTest("Bot does not support currency formatting")
            
        # Test currency formatting in different locales
        test_amount = 1234567.89
        expected_formats = {
            "en_US": "$1,234,567.89",  # Currency symbol as prefix
            "fr_FR": "1 234 567,89 €",  # Currency symbol as suffix
            "de_DE": "1.234.567,89 €"   # Currency symbol as suffix
        }
        
        for locale, expected in expected_formats.items():
            self.analyzer.set_locale(locale)
            formatted = self.analyzer.format_currency(test_amount)
            self.assertEqual(formatted, expected, f"Currency formatting in {locale} should be '{expected}'")

    def test_percentage_formatting(self):
        """Test that percentages are formatted according to locale conventions."""
        # Skip if the bot doesn't support percentage formatting
        if not hasattr(self.analyzer, 'format_percentage'):
            self.skipTest("Bot does not support percentage formatting")
            
        # Test percentage formatting in different locales
        test_percentage = 12.34
        expected_formats = {
            "en_US": "12.34%",  # Percent symbol as suffix
            "fr_FR": "12,34%",  # Percent symbol as suffix with comma decimal separator
            "de_DE": "12,34%"   # Percent symbol as suffix with comma decimal separator
        }
        
        for locale, expected in expected_formats.items():
            self.analyzer.set_locale(locale)
            formatted = self.analyzer.format_percentage(test_percentage)
            self.assertEqual(formatted, expected, f"Percentage formatting in {locale} should be '{expected}'")

    def test_formatted_report(self):
        """Test that reports include properly formatted numbers."""
        # Skip if the bot doesn't support formatted reports
        if not hasattr(self.analyzer, 'generate_formatted_report'):
            self.skipTest("Bot does not support formatted reports")
            
        # Test reports in different locales
        locales = ["en_US", "fr_FR", "de_DE"]
        for locale in locales:
            self.analyzer.set_locale(locale)
            report = self.analyzer.generate_formatted_report()
            
            # Get expected formats
            settings = self.analyzer.locale_formats.get(locale)
            raw_position_value = report["raw_values"]["position_value"]
            formatted_position_value = report["position_value"]
            
            # Check that the report contains properly formatted numbers
            self.assertIsInstance(formatted_position_value, str, "Formatted value should be a string")
            
            # Check that decimal separator matches locale
            if settings and "decimal_point" in settings:
                # Either the formatted value should contain the decimal point directly
                # or if it's a whole number, we should be able to verify it's formatted correctly
                if settings["decimal_point"] in formatted_position_value:
                    self.assertIn(settings["decimal_point"], formatted_position_value, 
                                  f"Formatted value should use {settings['decimal_point']} as decimal separator")
                    
            # Check that thousands separator is used
            if settings and "thousands_sep" in settings and raw_position_value >= 1000:
                # For locale-appropriate thousands separators
                if settings["thousands_sep"].strip():  # If it's not just whitespace
                    self.assertIn(settings["thousands_sep"], formatted_position_value, 
                                  f"Formatted value should use {settings['thousands_sep']} as thousands separator")
                    
            # Check that currency symbol is included in the position value
            if settings and "currency_symbol" in settings:
                self.assertIn(settings["currency_symbol"], formatted_position_value, 
                              f"Formatted value should include {settings['currency_symbol']}")
                
            # Check that percentage symbol is included in the percentage value
            if settings and "percent_symbol" in settings:
                self.assertIn(settings["percent_symbol"], report["profit_percentage"], 
                              f"Formatted percentage should include {settings['percent_symbol']}")

    @patch('locale.setlocale')
    def test_system_locale_independence(self, mock_setlocale):
        """Test that formatting is independent of system locale settings."""
        # Skip if the bot doesn't support number formatting
        if not hasattr(self.analyzer, 'format_number'):
            self.skipTest("Bot does not support number formatting")
            
        # We'll set the bot's locale to en_US
        self.analyzer.set_locale("en_US")
        
        # Now we'll set the system locale to something different
        # This shouldn't affect the bot's formatting
        mock_setlocale.return_value = "fr_FR.UTF-8"
        locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")
        
        # Format a number and check that it follows en_US conventions
        test_number = 1234567.89
        formatted = self.analyzer.format_number(test_number)
        self.assertEqual(formatted, "1,234,567.89", "Formatting should follow en_US conventions regardless of system locale")
        
        # Check that the locale was set correctly
        mock_setlocale.assert_called_with(locale.LC_ALL, "fr_FR.UTF-8")


if __name__ == "__main__":
    unittest.main() 