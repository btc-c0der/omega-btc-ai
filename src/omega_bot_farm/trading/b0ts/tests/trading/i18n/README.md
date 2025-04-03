# Internationalization (i18n) Tests for Omega Bot Farm Trading

This directory contains tests for the internationalization (i18n) functionality across the Omega Bot Farm trading components.

## Overview

The i18n tests ensure that the trading system can properly handle different languages, locales, currencies, and formatting preferences. These tests verify that the trading system can be used globally with proper localization.

## Test Structure

The tests are organized into several classes that focus on different aspects of internationalization:

1. **TestTradingI18n** - Core trading functionality with different locales
   - Client initialization with different locales
   - Market order creation with localized messages
   - Number formatting according to locale standards
   - Error messages in different languages
   - Position closing with localized feedback

2. **TestDateTimeI18n** - Date and time handling with different locales
   - Datetime formatting according to locale conventions
   - Timezone handling

3. **TestCurrencyI18n** - Currency handling with different locales
   - Currency formatting according to locale
   - Currency symbol positioning
   - Decimal separators and grouping

## Supported Locales

The tests currently cover the following locales:

- **en_US** - English (United States)
- **es_ES** - Spanish (Spain)
- **ja_JP** - Japanese (Japan)

## Fixtures

Common test fixtures are defined in `conftest.py`:

- `mock_ccxt_ticker` - Mock CCXT ticker object
- `ticker_dict` - Dictionary representation of a ticker
- `mock_ccxt_position` - Mock CCXT position object
- `position_dict` - Dictionary representation of a position
- `mock_i18n_translations` - Mock translations for different locales
- `mock_number_formatters` - Number formatters for different locales
- `mock_currency_formatters` - Currency formatters for different locales
- `mock_datetime_formatters` - Datetime formatters for different locales
- `ccxt_client` - Mock CCXT client for testing
- `requires_ccxt` - Decorator to skip tests if CCXT is not available

## Running the Tests

To run the i18n tests:

```bash
# Run all i18n tests
pytest src/omega_bot_farm/tests/trading/i18n/

# Run specific test class
pytest src/omega_bot_farm/tests/trading/i18n/test_i18n.py::TestTradingI18n

# Run specific test method
pytest src/omega_bot_farm/tests/trading/i18n/test_i18n.py::TestTradingI18n::test_number_formatting_by_locale
```

## Test Environment Variables

The tests use these environment variables:

- `LOCALE` - The locale to use for formatting (default: en_US)
- `TZ` - The timezone to use for datetime operations (default: UTC)

## Adding Support for New Locales

To add support for a new locale:

1. Add the locale to the translations dictionary in `mock_i18n_translations`
2. Add locale-specific formatters to `mock_number_formatters`, `mock_currency_formatters`, and `mock_datetime_formatters`
3. Add test assertions for the new locale in the test functions

## Integration with Exchange Clients

The i18n tests are designed to work with the CCXT exchange clients. The tests mock the CCXT interactions to verify that:

1. Error messages are properly translated
2. Numbers, currencies, and dates are formatted according to locale
3. User feedback is provided in the appropriate language

## Future Improvements

Planned enhancements for the i18n test suite:

1. **Additional Locales** - Add support for more languages and regions
2. **RTL Language Support** - Test right-to-left language formatting (e.g., Arabic)
3. **Currency Conversion** - Test locale-aware currency conversion
4. **Message Catalog Management** - Test loading and switching message catalogs
5. **Unicode Handling** - Ensure proper handling of non-ASCII characters in all contexts
