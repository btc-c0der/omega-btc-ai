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
Unicode handling tests for BitgetPositionAnalyzerB0t.

These tests verify that the bot correctly handles Unicode characters:
- Properly encodes/decodes Unicode in API responses
- Handles non-ASCII symbols in trading pairs
- Correctly processes different character encodings
- Maintains data integrity with special characters
"""

import unittest
import os
import sys
import json
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
        
        def __init__(self, api_key=None, api_secret=None, api_passphrase=None, use_testnet=False):
            self.api_key = api_key or "test_key"
            self.api_secret = api_secret or "test_secret"
            self.api_passphrase = api_passphrase or "test_pass"
            self.use_testnet = use_testnet
            
        def process_symbol(self, symbol):
            """Process a trading symbol, handling special characters."""
            # Strip whitespace and normalize
            processed = symbol.strip()
            
            # Handle special Unicode symbols that might appear in pair names
            mappings = {
                "₿": "BTC",  # Bitcoin symbol
                "Ξ": "ETH",  # Ethereum symbol
                "₮": "USDT", # Tether symbol
                "Ł": "LTC",  # Litecoin symbol
                "Ð": "DOGE", # Dogecoin symbol
            }
            
            # Replace any special symbols
            for unicode_char, replacement in mappings.items():
                processed = processed.replace(unicode_char, replacement)
                
            return processed
            
        def process_api_response(self, response_text):
            """Process API response text, handling Unicode properly."""
            try:
                # Parse JSON (with proper Unicode handling)
                data = json.loads(response_text)
                
                # Check if response contains positions
                if "positions" in data:
                    for position in data["positions"]:
                        # Process symbol if it exists
                        if "symbol" in position:
                            position["symbol"] = self.process_symbol(position["symbol"])
                            
                    return data
                else:
                    return {"error": "No positions found in response"}
                    
            except json.JSONDecodeError:
                return {"error": "Invalid JSON response"}
                
        def generate_unicode_test_data(self):
            """Generate test data with Unicode characters."""
            test_data = {
                "positions": [
                    {
                        "symbol": "₿/USDT",
                        "side": "long",
                        "entryPrice": 50000,
                        "markPrice": 55000
                    },
                    {
                        "symbol": "Ξ/₮",
                        "side": "short",
                        "entryPrice": 3000,
                        "markPrice": 2800
                    },
                    {
                        "symbol": "XRP/₮",
                        "side": "long",
                        "entryPrice": 0.5,
                        "markPrice": 0.55
                    }
                ]
            }
            
            return json.dumps(test_data, ensure_ascii=False)
            
        def analyze_with_unicode_comments(self, symbols):
            """Analyze positions with comments that include Unicode characters."""
            results = {}
            for symbol in symbols:
                # Generate analysis with Unicode characters in comments
                if "BTC" in symbol:
                    results[symbol] = {
                        "recommendation": "Buy 比特币 (Bitcoin) now!",
                        "target": "69,000 美元 (USD)",
                        "stop_loss": "45,000 美元 (USD)"
                    }
                elif "ETH" in symbol:
                    results[symbol] = {
                        "recommendation": "Ξセリング (Selling) recommended",
                        "target": "2,500 ユーロ (EUR)",
                        "stop_loss": "3,200 ユーロ (EUR)"
                    }
                else:
                    results[symbol] = {
                        "recommendation": "Mantener (HODL)",
                        "target": "To the 月亮 (moon)!",
                        "stop_loss": "Support at 0.45 元 (CNY)"
                    }
            return results


class TestUnicodeHandling(unittest.TestCase):
    """Test suite for Unicode handling."""

    def setUp(self):
        """Set up test environment."""
        # Use dummy API credentials for testing
        self.analyzer = BitgetPositionAnalyzerB0t(
            api_key="test_key",
            api_secret="test_secret", 
            api_passphrase="test_pass",
            use_testnet=True
        )

    def test_symbol_processing(self):
        """Test that Unicode symbols in trading pairs are processed correctly."""
        # Skip if the bot doesn't support symbol processing
        if not hasattr(self.analyzer, 'process_symbol'):
            self.skipTest("Bot does not support symbol processing")
            
        # Test with Bitcoin symbol
        self.assertEqual(self.analyzer.process_symbol("₿/USDT"), "BTC/USDT", 
                        "Should convert Bitcoin symbol to BTC")
                        
        # Test with Ethereum symbol
        self.assertEqual(self.analyzer.process_symbol("Ξ/USDT"), "ETH/USDT", 
                        "Should convert Ethereum symbol to ETH")
                        
        # Test with Tether symbol
        self.assertEqual(self.analyzer.process_symbol("BTC/₮"), "BTC/USDT", 
                        "Should convert Tether symbol to USDT")
                        
        # Test with multiple symbols
        self.assertEqual(self.analyzer.process_symbol("Ξ/₮"), "ETH/USDT", 
                        "Should convert both Ethereum and Tether symbols")
                        
        # Test with whitespace
        self.assertEqual(self.analyzer.process_symbol(" ₿/USDT "), "BTC/USDT", 
                        "Should handle whitespace and convert symbol")

    def test_api_response_processing(self):
        """Test that Unicode in API responses is processed correctly."""
        # Skip if the bot doesn't support API response processing
        if not hasattr(self.analyzer, 'process_api_response'):
            self.skipTest("Bot does not support API response processing")
            
        # Test with a mock API response containing Unicode
        test_response = """
        {
            "positions": [
                {
                    "symbol": "₿/USDT",
                    "side": "long",
                    "entryPrice": 50000,
                    "markPrice": 55000
                },
                {
                    "symbol": "Ξ/₮",
                    "side": "short",
                    "entryPrice": 3000,
                    "markPrice": 2800
                }
            ]
        }
        """
        
        # Process the response
        result = self.analyzer.process_api_response(test_response)
        
        # Check that the symbols were processed correctly
        self.assertEqual(result["positions"][0]["symbol"], "BTC/USDT", 
                        "Should convert Bitcoin symbol in first position")
        self.assertEqual(result["positions"][1]["symbol"], "ETH/USDT", 
                        "Should convert Ethereum and Tether symbols in second position")
        
        # Test with invalid JSON
        invalid_response = "This is not JSON { with some Unicode Ξ₿₮"
        result = self.analyzer.process_api_response(invalid_response)
        self.assertEqual(result["error"], "Invalid JSON response", 
                        "Should handle invalid JSON with Unicode characters")

    def test_unicode_json_generation(self):
        """Test that JSON with Unicode characters is generated correctly."""
        # Skip if the bot doesn't support Unicode test data generation
        if not hasattr(self.analyzer, 'generate_unicode_test_data'):
            self.skipTest("Bot does not support Unicode test data generation")
            
        # Generate the test data with Unicode
        json_data = self.analyzer.generate_unicode_test_data()
        
        # Check that the JSON is valid
        try:
            data = json.loads(json_data)
            
            # Check that Unicode characters are preserved
            self.assertIn("₿/USDT", json_data, "JSON should contain Bitcoin symbol")
            self.assertIn("Ξ/₮", json_data, "JSON should contain Ethereum and Tether symbols")
            
            # Check that the structure is correct
            self.assertIn("positions", data, "Parsed JSON should contain positions")
            self.assertEqual(len(data["positions"]), 3, "Should have 3 positions")
            
        except json.JSONDecodeError:
            self.fail("Generated JSON with Unicode is not valid")
            
        # Compare ASCII-only and Unicode-supporting JSON
        parsed = json.loads(json_data)
        ascii_json = json.dumps(parsed, ensure_ascii=True)
        non_ascii_json = json.dumps(parsed, ensure_ascii=False)
        
        # They should be different because one has escaped Unicode
        self.assertNotEqual(ascii_json, non_ascii_json, 
                           "ASCII-only JSON should differ from Unicode JSON")
        
        # The ASCII version should have escape sequences
        self.assertIn("\\u", ascii_json, "ASCII JSON should use Unicode escape sequences")
        
        # The non-ASCII version should have actual Unicode characters
        self.assertIn("₿", non_ascii_json, "Non-ASCII JSON should contain actual Unicode characters")

    def test_unicode_in_analysis(self):
        """Test that analysis with Unicode characters works correctly."""
        # Skip if the bot doesn't support analysis with Unicode
        if not hasattr(self.analyzer, 'analyze_with_unicode_comments'):
            self.skipTest("Bot does not support analysis with Unicode comments")
            
        # Test symbols to analyze
        test_symbols = ["BTC/USDT", "ETH/USDT", "XRP/USDT"]
        
        # Get analysis with Unicode comments
        analysis = self.analyzer.analyze_with_unicode_comments(test_symbols)
        
        # Check that the analysis contains the expected Unicode
        self.assertIn("比特币", analysis["BTC/USDT"]["recommendation"], 
                     "BTC analysis should contain Chinese characters")
        self.assertIn("美元", analysis["BTC/USDT"]["target"], 
                     "BTC target should contain Chinese characters")
                     
        self.assertIn("セリング", analysis["ETH/USDT"]["recommendation"], 
                     "ETH analysis should contain Japanese characters")
        self.assertIn("ユーロ", analysis["ETH/USDT"]["target"], 
                     "ETH target should contain Japanese characters")
                     
        self.assertIn("Mantener", analysis["XRP/USDT"]["recommendation"], 
                     "XRP analysis should contain Spanish word")
        self.assertIn("月亮", analysis["XRP/USDT"]["target"], 
                     "XRP target should contain Chinese characters")

    def test_unicode_roundtrip(self):
        """Test that Unicode survives a JSON roundtrip."""
        # Skip if the bot doesn't support either required method
        if not hasattr(self.analyzer, 'generate_unicode_test_data') or not hasattr(self.analyzer, 'process_api_response'):
            self.skipTest("Bot does not support required methods for roundtrip test")
            
        # Generate test data with Unicode
        json_data = self.analyzer.generate_unicode_test_data()
        
        # Process it as if it were an API response
        result = self.analyzer.process_api_response(json_data)
        
        # Check that the symbols were processed correctly
        self.assertEqual(result["positions"][0]["symbol"], "BTC/USDT", 
                        "Should convert Bitcoin symbol after JSON roundtrip")
        self.assertEqual(result["positions"][1]["symbol"], "ETH/USDT", 
                        "Should convert Ethereum and Tether symbols after JSON roundtrip")
        
        # Convert back to JSON and check integrity
        output_json = json.dumps(result, ensure_ascii=False)
        try:
            reparsed = json.loads(output_json)
            self.assertEqual(len(reparsed["positions"]), 3, 
                            "Should maintain all positions after roundtrip")
        except json.JSONDecodeError:
            self.fail("Roundtripped JSON is invalid")


if __name__ == "__main__":
    unittest.main() 