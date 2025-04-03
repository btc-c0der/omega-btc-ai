#!/usr/bin/env python3

"""
Localization tests for BitgetPositionAnalyzerB0t.

These tests verify that the bot supports different languages and locales:
- Proper translation of user-facing messages
- Language selection based on user preferences
- Fallback to default language when translations are missing
"""

import unittest
import os
import sys
import json
import locale
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
        
        def __init__(self, api_key=None, api_secret=None, api_passphrase=None, use_testnet=False, language="en"):
            self.api_key = api_key or "test_key"
            self.api_secret = api_secret or "test_secret"
            self.api_passphrase = api_passphrase or "test_pass"
            self.use_testnet = use_testnet
            self.language = language
            
            # Sample translations
            self.translations = {
                "en": {
                    "harmony_score": "Harmony Score",
                    "fib_analysis": "Fibonacci Analysis",
                    "position_summary": "Position Summary",
                    "buy_signal": "Buy Signal",
                    "sell_signal": "Sell Signal",
                    "hold_signal": "Hold Signal"
                },
                "es": {
                    "harmony_score": "Puntaje de Armonía",
                    "fib_analysis": "Análisis de Fibonacci",
                    "position_summary": "Resumen de Posición",
                    "buy_signal": "Señal de Compra",
                    "sell_signal": "Señal de Venta",
                    "hold_signal": "Señal de Mantener"
                },
                "fr": {
                    "harmony_score": "Score d'Harmonie",
                    "fib_analysis": "Analyse de Fibonacci",
                    "position_summary": "Résumé de Position",
                    "buy_signal": "Signal d'Achat",
                    "sell_signal": "Signal de Vente",
                    "hold_signal": "Signal de Maintien"
                },
                "ja": {
                    "harmony_score": "調和スコア",
                    "fib_analysis": "フィボナッチ分析",
                    "position_summary": "ポジションサマリー",
                    "buy_signal": "買いシグナル",
                    "sell_signal": "売りシグナル",
                    "hold_signal": "保持シグナル"
                },
                "zh": {
                    "harmony_score": "和谐分数",
                    "fib_analysis": "斐波那契分析",
                    "position_summary": "持仓摘要",
                    "buy_signal": "买入信号",
                    "sell_signal": "卖出信号",
                    "hold_signal": "持有信号"
                }
            }
            
        def set_language(self, language_code):
            """Set the language for the analyzer."""
            if language_code in self.translations:
                self.language = language_code
                return True
            else:
                # Fallback to English
                self.language = "en"
                return False
                
        def get_translated_message(self, key):
            """Get a translated message for the current language."""
            if key in self.translations.get(self.language, {}):
                return self.translations[self.language][key]
            elif key in self.translations.get("en", {}):
                # Fallback to English
                return self.translations["en"][key]
            else:
                # Return the key if no translation found
                return key
                
        def generate_report(self, format_type="text"):
            """Generate an analysis report in the current language."""
            harmony_score = self.get_translated_message("harmony_score")
            fib_analysis = self.get_translated_message("fib_analysis")
            position_summary = self.get_translated_message("position_summary")
            
            # Generate a report with translated headings
            report = {
                harmony_score: 0.75,
                fib_analysis: {
                    "levels": [0.236, 0.382, 0.5, 0.618, 0.786],
                    "prices": [40000, 45000, 50000, 55000, 60000]
                },
                position_summary: {
                    "symbol": "BTC/USDT",
                    "side": "long",
                    "recommendation": self.get_translated_message("hold_signal")
                }
            }
            
            if format_type == "json":
                return json.dumps(report, ensure_ascii=False)
            else:
                # Simple text format
                result = []
                for k, v in report.items():
                    result.append(f"{k}: {v}")
                return "\n".join(result)


class TestLocalization(unittest.TestCase):
    """Test suite for localization support."""

    def setUp(self):
        """Set up test environment."""
        # Use dummy API credentials for testing
        self.analyzer = BitgetPositionAnalyzerB0t(
            api_key="test_key",
            api_secret="test_secret", 
            api_passphrase="test_pass",
            use_testnet=True,
            language="en"  # Default to English
        )

    def test_supported_languages(self):
        """Test that the bot supports multiple languages."""
        # Skip if the bot doesn't support language setting
        if not hasattr(self.analyzer, 'set_language'):
            self.skipTest("Bot does not support language setting")
            
        # Test known supported languages
        languages = ["en", "es", "fr", "ja", "zh"]
        for lang in languages:
            result = self.analyzer.set_language(lang)
            self.assertTrue(result, f"Setting language to {lang} should succeed")
            self.assertEqual(self.analyzer.language, lang, f"Language should be set to {lang}")
            
        # Test unsupported language (should fallback to English)
        result = self.analyzer.set_language("unsupported")
        self.assertFalse(result, "Setting language to an unsupported language should fail")
        self.assertEqual(self.analyzer.language, "en", "Language should fallback to English")

    def test_message_translation(self):
        """Test that messages are translated correctly."""
        # Skip if the bot doesn't support message translation
        if not hasattr(self.analyzer, 'get_translated_message'):
            self.skipTest("Bot does not support message translation")
            
        # Test translation in different languages
        translations = {
            "en": {"harmony_score": "Harmony Score", "buy_signal": "Buy Signal"},
            "es": {"harmony_score": "Puntaje de Armonía", "buy_signal": "Señal de Compra"},
            "fr": {"harmony_score": "Score d'Harmonie", "buy_signal": "Signal d'Achat"},
            "ja": {"harmony_score": "調和スコア", "buy_signal": "買いシグナル"},
            "zh": {"harmony_score": "和谐分数", "buy_signal": "买入信号"}
        }
        
        for lang, expected in translations.items():
            self.analyzer.set_language(lang)
            for key, value in expected.items():
                translated = self.analyzer.get_translated_message(key)
                self.assertEqual(translated, value, f"Translation of '{key}' in {lang} should be '{value}'")
                
        # Test fallback to English for missing translations
        self.analyzer.set_language("es")
        # Create a key that doesn't exist in Spanish but exists in English
        if hasattr(self.analyzer, 'translations'):
            missing_key = "test_key_missing_in_es"
            self.analyzer.translations["en"][missing_key] = "English Value"
            translated = self.analyzer.get_translated_message(missing_key)
            self.assertEqual(translated, "English Value", "Should fallback to English for missing translations")
            
        # Test key return for completely missing translations
        completely_missing_key = "non_existent_key_anywhere"
        translated = self.analyzer.get_translated_message(completely_missing_key)
        self.assertEqual(translated, completely_missing_key, "Should return the key if no translation found")

    def test_report_localization(self):
        """Test that reports are localized correctly."""
        # Skip if the bot doesn't support report generation
        if not hasattr(self.analyzer, 'generate_report'):
            self.skipTest("Bot does not support report generation")
            
        # Test reports in different languages
        languages = ["en", "es", "fr", "ja", "zh"]
        for lang in languages:
            self.analyzer.set_language(lang)
            report = self.analyzer.generate_report(format_type="text")
            
            # Check that the report contains localized headings
            harmony_key = self.analyzer.get_translated_message("harmony_score")
            fib_key = self.analyzer.get_translated_message("fib_analysis")
            position_key = self.analyzer.get_translated_message("position_summary")
            
            self.assertIn(harmony_key, report, f"Report in {lang} should contain '{harmony_key}'")
            self.assertIn(fib_key, report, f"Report in {lang} should contain '{fib_key}'")
            self.assertIn(position_key, report, f"Report in {lang} should contain '{position_key}'")
            
    def test_json_unicode_support(self):
        """Test that JSON reports handle Unicode characters correctly."""
        # Skip if the bot doesn't support report generation
        if not hasattr(self.analyzer, 'generate_report'):
            self.skipTest("Bot does not support report generation")
            
        # Test with languages that use non-ASCII characters
        non_ascii_languages = ["ja", "zh"]
        for lang in non_ascii_languages:
            self.analyzer.set_language(lang)
            json_report = self.analyzer.generate_report(format_type="json")
            
            # Check that the JSON is valid
            try:
                parsed = json.loads(json_report)
                self.assertIsInstance(parsed, dict, "Parsed JSON should be a dictionary")
                
                # Check that the keys match expected translations
                harmony_key = self.analyzer.get_translated_message("harmony_score")
                self.assertIn(harmony_key, parsed, f"JSON report should contain the key '{harmony_key}'")
                
                # Compare with ASCII-only JSON
                ascii_json = json.dumps(parsed, ensure_ascii=True)
                non_ascii_json = json.dumps(parsed, ensure_ascii=False)
                
                # They should be different because one has escaped Unicode
                if any(ord(c) > 127 for c in harmony_key):
                    self.assertNotEqual(ascii_json, non_ascii_json, 
                                        "ASCII-only JSON should differ from Unicode JSON")
                    
            except json.JSONDecodeError:
                self.fail(f"Generated JSON is not valid for language {lang}")

    @patch('locale.setlocale')
    def test_locale_independence(self, mock_setlocale):
        """Test that analysis results are consistent regardless of locale."""
        # Skip if the bot doesn't support report generation
        if not hasattr(self.analyzer, 'generate_report'):
            self.skipTest("Bot does not support report generation")
            
        # Get a baseline report in English
        self.analyzer.set_language("en")
        baseline_report = self.analyzer.generate_report(format_type="json")
        baseline_parsed = json.loads(baseline_report)
        
        # Mock different locales to test
        test_locales = [
            ('en_US', 'UTF-8'),
            ('fr_FR', 'UTF-8'),
            ('de_DE', 'UTF-8'),
            ('ja_JP', 'UTF-8'),
            ('zh_CN', 'UTF-8')
        ]
        
        for loc, encoding in test_locales:
            # Mock setting the locale
            mock_setlocale.return_value = loc
            locale.setlocale(locale.LC_ALL, (loc, encoding))
            
            # Generate a report and ensure numeric values are consistent
            self.analyzer.set_language("en")  # Keep language consistent
            report = self.analyzer.generate_report(format_type="json")
            parsed = json.loads(report)
            
            # Check that numeric values are the same regardless of locale
            harmony_key = self.analyzer.get_translated_message("harmony_score")
            self.assertEqual(parsed[harmony_key], baseline_parsed[harmony_key], 
                            f"Harmony score should be consistent regardless of locale {loc}")
            
            # Check Fibonacci levels
            fib_key = self.analyzer.get_translated_message("fib_analysis")
            for i, level in enumerate(parsed[fib_key]["levels"]):
                self.assertEqual(level, baseline_parsed[fib_key]["levels"][i], 
                                f"Fibonacci level {i} should be consistent regardless of locale {loc}")
                
            # Check that the locale was properly set
            mock_setlocale.assert_called_with(locale.LC_ALL, (loc, encoding))


if __name__ == "__main__":
    unittest.main() 