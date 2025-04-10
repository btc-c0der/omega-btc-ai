
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


# Component Tests for Bitget Position Analyzer

This directory contains component tests for the Bitget Position Analyzer bot. Component tests focus on verifying that multiple units of code work together correctly within their bounded contexts, but without requiring external dependencies like the actual exchange API.

## Test Structure

The component tests are organized by functional areas:

- `test_position_analyzer_pipeline.py`: Tests for the core position analysis pipeline
- `test_harmony_calculations.py`: Tests for harmony score calculation components
- `test_discord_integration.py`: Tests for the Discord bot integration
- `test_visualization_component.py`: Tests for position visualization components

## Running Tests

To run all component tests:

```bash
cd /path/to/omega-btc-ai
pytest src/omega_bot_farm/trading/b0ts/bitget_analyzer/tests/component/
```

To run a specific component test file:

```bash
pytest src/omega_bot_farm/trading/b0ts/bitget_analyzer/tests/component/test_harmony_calculations.py
```

## Fixtures

The `conftest.py` file contains shared fixtures used across multiple component test files. Additional test-specific fixtures are defined within each test file.

The `fixtures/` directory contains static test data files used by the component tests.

## Mocking Strategy

These tests use a combination of:

1. **Mock Objects**: For simulating dependencies like the exchange service
2. **In-Memory Test Doubles**: For simulating components that interact with other components
3. **Importorskip**: To handle potential import paths that might differ in the actual implementation

## Test Data

The test data is designed to cover a variety of scenarios:

- Different position types (long/short)
- Various risk levels
- Multiple symbols (BTCUSDT, ETHUSDT, etc.)
- Edge cases in harmony calculations
- Different Fibonacci patterns

## Adding New Tests

When adding new component tests:

1. Identify the components that interact with each other
2. Create appropriate mocks for external dependencies
3. Define test fixtures that represent realistic data
4. Test both happy paths and error scenarios
5. Verify that component integrations behave as expected

## Continuous Integration

These tests are run as part of the CI pipeline to ensure component-level functionality remains intact across changes.
