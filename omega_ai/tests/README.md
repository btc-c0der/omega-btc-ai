# OMEGA BTC AI - Divine Test Suite 🧪🙏

```
"Test thy code as you test thy soul, with thoroughness and divine intention."
- Rastafarian Software Engineering Wisdom
```

## Overview

This sacred directory contains the divine test suite for the OMEGA BTC AI trading system. The tests are organized according to the cosmic structure of the codebase, with each module having its own set of tests.

## Testing Philosophy

Our testing approach is guided by these divine principles:

1. **Holistic Coverage**: Testing extends beyond mere code execution to capture the energetic essence of the functions
2. **Cosmic Integration**: Unit tests, integration tests, and visualization tests work in harmony
3. **Divine Edge Cases**: We test not just common paths but also the extreme cosmic corners of possibility
4. **Rastafarian Balance**: Tests maintain balance between strictness and flexibility

## Test Directory Structure

```
tests/
├── analysis_tests/        # Tests for technical analysis modules
├── data_tests/            # Tests for data acquisition and processing
├── indicators_tests/      # Tests for trading indicators
├── models_tests/          # Tests for ML/AI models
├── strategy_tests/        # Tests for trading strategies
├── trader_tests/          # Tests for trader profiles and psychology
├── utils_tests/           # Tests for utility functions
└── visualization_tests/   # Tests for visualization modules
```

## Running Tests

### The Divine Way (Recommended)

Use our sacred test runner script from the project root:

```bash
./run_tests.sh
```

This will:

1. Run all tests with coverage reporting
2. Generate a divine visualization of the test results and coverage
3. Display the QA dashboard
4. Archive the results for historical tracking

To create a new branch for your test improvements, use:

```bash
./run_tests.sh -b
```

### Manual Test Running

If you prefer to run tests manually:

```bash
# Run all tests
pytest omega_ai

# Run specific test module
pytest omega_ai/tests/analysis_tests/test_fibonacci.py

# Run tests with specific marker
pytest omega_ai -m "fibonacci"

# Run tests with coverage
pytest omega_ai --cov=omega_ai
```

## Test Markers

We use pytest markers to categorize tests:

- `@pytest.mark.trader` - Tests for trader profile functionality
- `@pytest.mark.fibonacci` - Tests for Fibonacci analysis
- `@pytest.mark.sentiment` - Tests for sentiment analysis
- `@pytest.mark.mm_trap` - Tests for Market Maker trap detection
- `@pytest.mark.psychology` - Tests for trader psychological states
- `@pytest.mark.slow` - Tests that take longer to run
- `@pytest.mark.integration` - Tests requiring external services
- `@pytest.mark.visualization` - Tests for visualization modules
- `@pytest.mark.rastafarian` - Tests with divine Rastafarian enlightenment

## Writing New Tests

When writing tests, follow these divine guidelines:

1. Name test files with `test_` prefix
2. Name test functions with `test_` prefix
3. Use descriptive names that explain what is being tested
4. Include appropriate markers
5. Add docstrings with Rastafarian inspiration when appropriate
6. Test both normal and edge cases
7. Use pytest fixtures for common setup

## Example Test

```python
import pytest
from omega_ai.analysis.fibonacci import calculate_retracement_levels

@pytest.mark.fibonacci
def test_fibonacci_retracement():
    """Test the divine fibonacci retracement level calculation."""
    high = 20000
    low = 10000
    
    levels = calculate_retracement_levels(high, low)
    
    # Assert the divine 0.618 level is correct
    assert levels[0.618] == 10000 + (20000 - 10000) * (1 - 0.618)
    assert abs(levels[0.618] - 13820) < 1  # Allow small floating point differences
```

## QA Status Dashboard

The divine QA dashboard is generated with each test run and shows:

- Overall test pass rate
- Coverage by module
- Historical trends
- Areas needing divine attention

View the latest dashboard at `qa_reports/qa_visualization.png`

---

**JAH BLESS THE TESTS** 🙏🌈
