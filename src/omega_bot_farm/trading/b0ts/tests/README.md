# BitgetPositionAnalyzerB0t Tests

This directory contains tests for the BitgetPositionAnalyzerB0t, which is responsible for analyzing Bitget positions using Fibonacci principles.

## Test Structure

The tests are organized as follows:

- `unit/`: Unit tests for individual components of the BitgetPositionAnalyzerB0t
  - `test_fibonacci_levels.py`: Tests for Fibonacci retracement and extension calculations
  - `test_harmony_score.py`: Tests for position harmony score calculations
  - `test_position_monitor.py`: Tests for position monitoring and change detection
  - `test_portfolio_metrics.py`: Tests for portfolio metrics like long-short ratio

- `conftest.py`: Shared test fixtures and utilities
- `README.md`: This file

## Running the Tests

### Prerequisites

Before running the tests, you need to install the required dependencies:

```bash
pip install pytest pytest-asyncio pytest-mock
```

### Running All Tests

To run all tests, execute the following command from the project root:

```bash
python -m pytest src/omega_bot_farm/trading/b0ts/bitget_analyzer/tests
```

### Running Specific Test Files

To run a specific test file:

```bash
python -m pytest src/omega_bot_farm/trading/b0ts/bitget_analyzer/tests/unit/test_fibonacci_levels.py
```

### Running Tests with Verbose Output

For more detailed output:

```bash
python -m pytest -v src/omega_bot_farm/trading/b0ts/bitget_analyzer/tests
```

## Mock Implementation

The tests are designed to work even if the actual `BitgetPositionAnalyzerB0t` is not available. Each test module includes a mock implementation that mimics the behavior of the real bot for testing purposes.

## Test Coverage

The tests cover the following aspects of the bot:

1. **Fibonacci Level Calculations**:
   - Long position Fibonacci levels
   - Short position Fibonacci levels
   - Take profit and stop loss recommendations

2. **Harmony Score Calculations**:
   - Individual position harmony
   - Overall portfolio harmony
   - Golden ratio detection

3. **Position Monitoring**:
   - Detection of new positions
   - Detection of closed positions
   - Detection of significant position changes

4. **Portfolio Metrics**:
   - Long-short ratio calculations
   - Exposure to equity ratio calculations
   - Portfolio recommendations based on metrics

## Contributing New Tests

When adding new tests:

1. Follow the existing structure and naming conventions
2. Ensure tests can run independently
3. Use fixtures from `conftest.py` where possible
4. Include both normal and edge cases
5. Make sure tests run with the mock implementation if the bot is not available

## Test Configuration

The tests use environment variables for configuration. You can set these for integration tests if needed:

```bash
export BITGET_API_KEY="your_test_api_key"
export BITGET_SECRET_KEY="your_test_secret_key"
export BITGET_PASSPHRASE="your_test_passphrase"
export BITGET_TESTNET="true"
```

Note: For normal test runs, you don't need to set these as the tests use mock data.
