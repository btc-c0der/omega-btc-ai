# Bitget Exchange Tests

This directory contains tests specific to the Bitget exchange integration in Omega Bot Farm.

## Test Structure

These tests use the DRY approach by extending the base CCXT test classes defined in `../test_ccxt_b0t.py`. The test classes include:

1. `TestBitgetClient`: Tests specific to Bitget that don't require CCXT
2. `TestBitgetClientWithCCXT`: Bitget-specific tests that require CCXT to be installed
3. `TestBitgetClientWithoutCCXT`: Tests for Bitget client when CCXT is not available

## Bitget-Specific Features Tested

- Symbol suffix handling (`_UMCBL`)
- Bitget-specific symbol formatting
- Copy trade functionality
- Bitget-specific position closing

## Running Tests

To run only the Bitget-specific tests:

```bash
# From the project root directory
pytest src/omega_bot_farm/tests/trading/exchanges/bitget/ -v
```

To run tests without CCXT installed:

```bash
pytest src/omega_bot_farm/tests/trading/exchanges/bitget/test_ccxt_b0t.py::TestBitgetClientWithoutCCXT -v
```

To run tests that require CCXT:

```bash
# Ensure CCXT is installed
pip install ccxt

# Then run the tests
pytest src/omega_bot_farm/tests/trading/exchanges/bitget/test_ccxt_b0t.py::TestBitgetClientWithCCXT -v
```

## Fixtures

The tests use the common fixtures defined in `../conftest.py` plus the additional fixture:

- `bitget_client`: A client specifically configured for Bitget testing

## Adding More Tests

When adding more Bitget-specific tests:

1. For tests that can run without CCXT, add them to the `TestBitgetClient` class
2. For tests that require CCXT, add them to the `TestBitgetClientWithCCXT` class
3. For tests that verify behavior when CCXT is not available, add them to `TestBitgetClientWithoutCCXT`
