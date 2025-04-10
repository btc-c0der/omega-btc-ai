
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


# CCXT Exchange Integration Tests

This directory contains tests for the CCXT exchange integration in Omega Bot Farm.

## Test Structure

The tests are organized using a DRY (Don't Repeat Yourself) approach with:

1. **Base Test Classes**: Common test functionality is defined in `test_ccxt_b0t.py` using the `BaseCCXTClientTests` class
2. **Exchange-Specific Tests**: Exchange-specific tests extend the base classes (e.g., in `bitget/test_bitget_ccxt.py`)
3. **Shared Fixtures**: Common fixtures are defined in `conftest.py` and can be used by all test modules

## Running Tests

### Basic Tests (No CCXT Required)

To run the basic tests that don't require CCXT:

```bash
# From the project root directory
pytest src/omega_bot_farm/tests/trading/exchanges/test_ccxt_b0t.py::TestCCXTClientWithoutCCXT -v
```

This will run only the tests that verify:

- The `to_dict` utility function
- Error handling when CCXT is not available
- Initialization behavior without CCXT

### Complete Tests (CCXT Required)

To run all tests, including those that require CCXT:

```bash
# First, install CCXT
pip install ccxt

# Then run the tests
pytest src/omega_bot_farm/tests/trading/exchanges/ -v
```

### Exchange-Specific Tests

To run tests for a specific exchange:

```bash
# For Bitget tests
pytest src/omega_bot_farm/tests/trading/exchanges/bitget/ -v
```

## Base Test Classes

The `BaseCCXTClientTests` class in `test_ccxt_b0t.py` provides the following test classes:

1. `TestUtilityFunctions`: Tests for utility functions that don't require CCXT
2. `TestWithoutCCXT`: Tests that verify behavior when CCXT is not available
3. `TestWithCCXT`: Tests that require CCXT to be installed

## Exchange-Specific Tests

Exchange-specific tests (like those in `bitget/test_bitget_ccxt.py`) extend the base classes, allowing:

1. Reuse of common test functionality
2. Addition of exchange-specific test cases
3. Specialization for specific exchange behavior

When adding a new exchange, you should:

1. Create a new directory for the exchange (e.g., `binance/`)
2. Create a test file that inherits from the base test classes
3. Add exchange-specific test cases and fixtures

## Test Fixtures

Common fixtures are defined in `conftest.py`:

- `mock_ccxt_order`: Mock CCXT order object
- `mock_ccxt_ticker`: Mock CCXT ticker object
- `mock_ccxt_position`: Mock CCXT position object
- `ccxt_client`: Pre-configured CCXT client for testing
- `no_ccxt_client`: Client configured to simulate CCXT not being available
- And more standardized fixtures

## Current Test Coverage

The current test coverage is approximately 70%. We've structured the tests to provide good coverage of:

1. Base CCXT client functionality in `test_ccxt_b0t.py`
2. Exchange-specific behavior in Bitget implementation
3. Error handling when CCXT is not available
4. Core utility functions like `to_dict`

To see the current test coverage:

```bash
pytest --cov src/omega_bot_farm/tests/trading/exchanges/ -v
```

## Expected Results

### Without CCXT

When running without CCXT installed, you should see:

- Basic utility tests passing
- Tests requiring CCXT displaying appropriate error messages
- Error handling tests passing

### With CCXT

When running with CCXT installed, all 34 tests should pass, including:

1. Core CCXT functionality tests
2. Bitget-specific implementation tests
3. Error handling and utility function tests

## Benefits of the DRY Implementation

Our DRY implementation provides significant benefits:

1. **Code Reuse**: The base test classes in `test_ccxt_b0t.py` are reused by Bitget-specific tests
2. **Maintainability**: Changes to common test logic need to be made in only one place
3. **Consistency**: All exchange implementations follow the same testing pattern
4. **Extensibility**: Adding new exchange implementations is straightforward
5. **Readability**: The test structure clearly shows the relationship between general and specific functionality

## Bitget-Specific Tests

The Bitget-specific tests in `bitget/test_bitget_ccxt.py` demonstrate how to extend the base test classes for a specific exchange. They include:

1. Tests for Bitget's symbol suffix handling
2. Tests for Bitget-specific API endpoints
3. Tests for Bitget's position management

## Future Improvements

While the current test coverage is good at 70%, future improvements could include:

1. More comprehensive tests for WebSocket functionality
2. Additional exchange implementations (Binance, OKX, etc.)
3. Additional tests for rate limiting behavior
4. Stress testing for high-frequency trading scenarios

## Troubleshooting

If you encounter test failures, check:

1. CCXT installation status
2. API key configuration for live tests
3. Network connectivity for exchange API access
4. Pytest configuration in `pytest.ini`
5. Python environment and dependencies
