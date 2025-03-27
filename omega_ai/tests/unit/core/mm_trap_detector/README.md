# 🎯 OMEGA RASTA FIBONACCI DETECTOR TESTS

Divine test suite for the Fibonacci detector module. May the golden ratio be with you! 🚀

## 🏗️ Test Structure

```
omega_ai/tests/mm_trap_detector/
├── test_fibonacci_detector/
│   ├── __init__.py
│   ├── test_swing_points.py        # Swing point detection tests
│   ├── test_fibonacci_levels.py    # Level calculation and validation
│   ├── test_trap_detection.py      # Trap detection and confluence
│   ├── test_fractal_harmony.py     # Fractal and golden ratio tests
│   ├── test_error_handling.py      # Error handling and edge cases
│   └── test_redis_integration.py   # Redis-related tests
├── conftest.py                     # Shared fixtures and configs
└── pytest.ini                      # Test runner configuration
```

## 🚀 Running Tests

### Run All Tests

```bash
cd /path/to/omega-btc-ai
python -m pytest omega_ai/tests/mm_trap_detector -v
```

### Run Specific Test Categories

```bash
# Run only swing point tests
python -m pytest omega_ai/tests/mm_trap_detector -v -m swing_points

# Run only fractal harmony tests
python -m pytest omega_ai/tests/mm_trap_detector -v -m fractal_harmony

# Run only error handling tests
python -m pytest omega_ai/tests/mm_trap_detector -v -m error_handling
```

### Run Tests with Coverage Report

```bash
python -m pytest omega_ai/tests/mm_trap_detector -v --cov=omega_ai.mm_trap_detector.fibonacci_detector --cov-report=term-missing
```

## 🎯 Test Categories

### Swing Point Detection

- Basic swing point detection
- Enhanced rolling window detection
- Edge cases (small ranges, equal points, missing points)

### Fibonacci Levels

- Level calculation accuracy
- Golden ratio validation
- Extension level verification

### Trap Detection

- Market maker fakeout detection
- Wick deviation analysis
- Reversal validation

### Fractal Harmony

- Self-repeating pattern detection
- Multi-timeframe analysis
- Schumann resonance integration

### Error Handling

- Invalid input handling
- Redis connection errors
- Edge case management

## 📊 Coverage Requirements

- Minimum coverage: 79%
- Coverage reports are generated in HTML format
- Coverage reports are available in `htmlcov/index.html`

## 🔧 Configuration

Test configuration is managed in `conftest.py` and includes:

- Minimum swing difference thresholds
- Fibonacci level tolerances
- Confirmation thresholds
- Price history size
- Supported timeframes
- Schumann resonance frequencies

## 🎨 Test Style

- Each test file focuses on a specific aspect of the detector
- Tests are organized by functionality
- Clear test names and descriptions
- Detailed logging for debugging
- Color-coded output for better readability

## 🤝 Contributing

1. Add new tests to the appropriate category
2. Ensure test coverage doesn't decrease
3. Follow the existing test style
4. Update documentation if needed

## 🚀 Future Enhancements

- Add more fractal pattern tests
- Enhance Schumann resonance integration
- Add more multi-timeframe analysis
- Improve error handling coverage
