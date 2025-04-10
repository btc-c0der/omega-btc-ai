
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


# Core Components Test Suite

This directory contains comprehensive test cases for the core components of the Omega Bot Farm trading system.

## Test Files

- `test_base_b0t.py`: Tests for the BaseB0t class
- `test_exchange_client.py`: Tests for the ExchangeClient class
- `test_module.py`: Entry point for running all tests

## Running Tests

You can run the tests in several ways:

### Using the Shell Script

```bash
# Make the script executable if needed
chmod +x run_tests.sh

# Run all tests
./run_tests.sh
```

### Using Python Directly

```bash
# Run all tests
python3 test_module.py

# Run specific test file
python3 test_base_b0t.py
python3 test_exchange_client.py
```

### Using unittest Module

```bash
# From the project root directory
python -m unittest discover src/omega_bot_farm/trading/b0ts/core/tests

# Run specific test file
python -m unittest src/omega_bot_farm/trading/b0ts/core/tests/test_base_b0t.py
python -m unittest src/omega_bot_farm/trading/b0ts/core/tests/test_exchange_client.py
```

## Test Coverage

The test suite covers:

- **BaseB0t**:
  - Initialization
  - Logging
  - State management
  - Environment variable loading
  - Utility methods

- **ExchangeClient**:
  - Initialization
  - Connection methods (with fallbacks)
  - Credential management
  - API request methods
  - Symbol formatting
  - Error handling

## Adding New Tests

To add new tests:

1. Create a new file named `test_*.py`
2. Import the necessary modules
3. Create a class that inherits from `unittest.TestCase`
4. Implement test methods that start with `test_`
5. The tests will be automatically discovered when running `test_module.py`
