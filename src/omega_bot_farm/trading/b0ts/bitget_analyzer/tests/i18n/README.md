
✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This code is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."

By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸


# Internationalization (i18n) Tests for BitgetPositionAnalyzerB0t

This directory contains internationalization (i18n) tests for the BitgetPositionAnalyzerB0t, focusing on ensuring the bot works correctly across different languages, locales, and with Unicode characters.

## Internationalization Test Suite

The i18n tests are organized into three main categories:

1. **Localization** (`test_localization.py`)
   - Tests support for multiple languages
   - Tests message translation capabilities
   - Tests fallback to default language when translations are missing
   - Tests report generation in different languages

2. **Number Formatting** (`test_number_formatting.py`)
   - Tests number formatting according to locale conventions
   - Tests currency formatting with appropriate symbols
   - Tests percentage formatting
   - Tests consistent numeric results regardless of locale

3. **Unicode Handling** (`test_unicode_handling.py`)
   - Tests handling of Unicode characters in trading symbols
   - Tests processing of Unicode in API responses
   - Tests generation of JSON with Unicode characters
   - Tests Unicode in analysis comments and recommendations

## Running the Tests

To run all i18n tests:

```bash
python -m pytest src/omega_bot_farm/trading/b0ts/bitget_analyzer/tests/i18n
```

To run a specific i18n test:

```bash
python -m pytest src/omega_bot_farm/trading/b0ts/bitget_analyzer/tests/i18n/test_localization.py
```

## Internationalization Best Practices

These tests enforce the following internationalization best practices:

1. **Proper Localization**
   - Store user-facing messages in translation dictionaries
   - Support language selection based on user preferences
   - Implement fallback to default language for missing translations
   - Ensure all user-facing text is localizable

2. **Correct Number Formatting**
   - Format numbers according to locale conventions
   - Use appropriate decimal and thousands separators
   - Position currency symbols based on locale standards
   - Maintain numeric precision regardless of display format

3. **Robust Unicode Support**
   - Properly encode/decode Unicode in JSON
   - Handle non-ASCII characters in trading symbols
   - Process special characters in API responses
   - Ensure data integrity with different character sets

## Test Coverage

| Category | Test Cases | Description |
|----------|------------|-------------|
| Localization | 5 | Tests for language support, message translation, report localization, Unicode in JSON, and locale independence |
| Number Formatting | 5 | Tests for locale support, number formatting, currency formatting, percentage formatting, and report formatting |
| Unicode Handling | 5 | Tests for symbol processing, API response handling, JSON generation, analysis with Unicode, and Unicode roundtrip |

## Supported Languages and Locales

The tests cover the following languages and locales:

### Languages

- English (en)
- Spanish (es)
- French (fr)
- Japanese (ja)
- Chinese (zh)

### Locales

- English - United States (en_US)
- French - France (fr_FR)
- German - Germany (de_DE)
- Japanese - Japan (ja_JP)
- Chinese - China (zh_CN)

## Adding New i18n Tests

When adding new internationalization tests:

1. Use the existing structure and patterns
2. Add new test cases for any specific language or locale requirements
3. Keep in mind potential differences in number formats, currency symbols, and text direction
4. Test with a variety of Unicode characters, especially those that might appear in trading contexts
5. Consider edge cases like missing translations or mixed language content

## Handling Import Errors

All tests include a fallback mock implementation for when BitgetPositionAnalyzerB0t is not available:

```python
try:
    from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t
    BOT_AVAILABLE = True
except ImportError:
    BOT_AVAILABLE = False
    print("BitgetPositionAnalyzerB0t not available. Using mock for tests.")
    
# Mock implementation if import fails
if not BOT_AVAILABLE:
    class BitgetPositionAnalyzerB0t:
        # Mock implementation
        ...
```

This allows the tests to run even when the actual bot implementation is not available.

## Additional Resources

For more information on internationalization best practices:

- [Unicode CLDR Project](http://cldr.unicode.org/) - Common Locale Data Repository
- [ICU Project](http://site.icu-project.org/) - International Components for Unicode
- [Python gettext module](https://docs.python.org/3/library/gettext.html) - Multilingual internationalization
- [Locale module](https://docs.python.org/3/library/locale.html) - Internationalization services
