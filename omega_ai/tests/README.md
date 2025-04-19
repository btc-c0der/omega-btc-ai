
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


# 🧪 OMEGA BTC AI - Quality Assurance

![RASTA QA SHIELD](https://img.shields.io/badge/RASTA%20QA-BLESSED-52b788?style=for-the-badge&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAADWSURBVHgBrVNbDsFAFJ1JS3yCn4ifSkRYAR+srsTHd1dhB9iBHaywArEDgxdxkzYz7cykZoL4OMnNzD333HM7twC/QMn7KYKDwkPDQcHASkgI2oFL6OEGAhsMGUFwN6BIovFjpOUdO4eIdPwQMdLJPNZs3YnmrGLFBlPJspth5HxZ5QVqkJG7gK7rDTyfj0iKYzSgeOITDlCDdguKaZqw2+0Tz0GxXdvG8/LKtePIWGJll9AlDV2U0yTb7TSu9xdpsysEGjB37vGKikNEJkPtf+QcZ9pGzn+QvwG14CvkQBnwYgAAAABJRU5ErkJggg==)
[![Test Coverage](https://img.shields.io/badge/coverage-87%25-brightgreen.svg)](https://github.com/yourusername/omega-btc-ai/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=yourusername_omega-btc-ai&metric=alert_status)](https://sonarcloud.io/dashboard?id=yourusername_omega-btc-ai)
[![Maintainability](https://api.codeclimate.com/v1/badges/YOUR_CODE_CLIMATE_ID/maintainability)](https://codeclimate.com/github/yourusername/omega-btc-ai/maintainability)

## 📋 Test Directory Structure

```
tests/
├── ai/                    # AI and prediction model tests
├── alerts/               # Alert system tests
├── api/                  # API endpoint tests
├── fibonacci/            # Fibonacci analysis tests
├── mm_trap_detector/     # Market Maker trap detection tests
├── redis/                # Redis integration tests
├── rasta/                # Rasta-related functionality tests
├── runners/              # Test runner scripts
├── security/             # Security and authentication tests
├── trading/              # Trading system tests
├── visualization/        # Visualization component tests
├── websocket/           # WebSocket connection tests
├── conftest.py          # Pytest configuration
└── run_omega_tests.py   # Main test runner
```

## 🎯 Testing Philosophy

Our testing approach is guided by these divine principles:

1. **Holistic Coverage**: Testing extends beyond mere code execution to capture the energetic essence of the functions
2. **Cosmic Integration**: Unit tests, integration tests, and visualization tests work in harmony
3. **Divine Edge Cases**: We test not just common paths but also the extreme cosmic corners of possibility
4. **Rastafarian Balance**: Tests maintain balance between strictness and flexibility

## 🚀 Running Tests

### The Divine Way (Recommended)

Use our sacred test runner script:

```bash
./run_omega_tests.py
```

This will:

1. Run all tests with coverage reporting
2. Generate a divine visualization of the test results
3. Display the QA dashboard
4. Archive the results for historical tracking

### Manual Test Running

```bash
# Run all tests
pytest omega_ai

# Run specific test module
pytest omega_ai/tests/trading/test_trader.py

# Run tests with specific marker
pytest omega_ai -m "fibonacci"

# Run tests with coverage
pytest omega_ai --cov=omega_ai
```

## 🏷 Test Markers

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

## ✍️ Writing New Tests

When writing tests, follow these divine guidelines:

1. Name test files with `test_` prefix
2. Name test functions with `test_` prefix
3. Use descriptive names that explain what is being tested
4. Include appropriate markers
5. Add docstrings with Rastafarian inspiration when appropriate
6. Test both normal and edge cases
7. Use pytest fixtures for common setup

### Example Test

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

## 📊 QA Status Dashboard

The divine QA dashboard is generated with each test run and shows:

- Overall test pass rate
- Coverage by module
- Historical trends
- Areas needing divine attention

View the latest dashboard at `qa_reports/qa_visualization.png`

## 🔄 Continuous Integration

Our CI pipeline includes:

1. **Automated Testing**
   - Unit tests
   - Integration tests
   - Performance tests
   - Security tests

2. **Code Quality Checks**
   - Linting
   - Type checking
   - Complexity analysis
   - Duplicate code detection

3. **Coverage Requirements**
   - Minimum 80% code coverage
   - Branch coverage requirements
   - Mutation testing

## 🛠 Test Environment Setup

1. **Prerequisites**

   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Environment Variables**

   ```bash
   cp .env.test.example .env.test
   # Edit .env.test with your test configuration
   ```

3. **Test Database**

   ```bash
   python scripts/setup_test_db.py
   ```

## 📝 Test Documentation

- [AI Test Documentation](ai/README.md) - Deep dive into our quantum-inspired AI testing approach
- [API Test Documentation](api/README.md)
- [Trading Test Documentation](trading/README.md)
- [Visualization Test Documentation](visualization/README.md)
- [Integration Test Guide](integration_tests/README.md)

## 🤝 Contributing to Tests

1. Fork the repository
2. Create a feature branch
3. Write your tests
4. Ensure all tests pass
5. Submit a Pull Request

## 📈 Test Metrics

We track the following metrics:

- Test coverage percentage
- Number of test cases
- Test execution time
- Failed test trends
- Code quality scores

## 🎯 Test Categories

### Unit Tests

- Individual component testing
- Mock external dependencies
- Fast execution
- High coverage

### Integration Tests

- Component interaction testing
- Real external services
- Slower execution
- Critical path coverage

### Performance Tests

- Load testing
- Stress testing
- Response time verification
- Resource usage monitoring

### Security Tests

- Authentication testing
- Authorization testing
- Input validation
- Vulnerability scanning

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Test-Driven Development Guide](https://www.agilealliance.org/glossary/tdd/)
- [Continuous Integration Guide](https://docs.github.com/en/actions/guides)

---

ONE LOVE, ONE HEART, ONE TEST! 🌟
