
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


# Behavior-Driven Development Tests for Bitget Position Analyzer

This directory contains BDD tests for the Bitget Position Analyzer bot. These tests use the Behave framework to implement readable test scenarios that document application behavior while verifying functionality.

## Test Structure

- `features/`: Contains feature files with scenarios written in Gherkin syntax
- `steps/`: Contains step implementations that connect scenarios to code
- `environment.py`: Setup and teardown for BDD test runs

## Feature Organization

The features are organized by functional areas:

- `position_analysis.feature`: Analysis of trading positions
- `risk_detection.feature`: Risk assessment and alerts
- `fibonacci_analysis.feature`: Fibonacci-based technical analysis
- `harmony_calculation.feature`: Position harmony and alignment
- `discord_integration.feature`: Discord bot commands and notifications
- `notifications.feature`: Alert generation and delivery
- `visualization.feature`: Chart and report generation

## Running Tests

To run all BDD tests:

```bash
cd /path/to/omega-btc-ai
behave src/omega_bot_farm/trading/b0ts/bitget_analyzer/tests/BDD/features/
```

To run a specific feature:

```bash
behave src/omega_bot_farm/trading/b0ts/bitget_analyzer/tests/BDD/features/position_analysis.feature
```

To generate a report:

```bash
behave src/omega_bot_farm/trading/b0ts/bitget_analyzer/tests/BDD/features/ -f html -o bdd_test_report.html
```

## Tagging

Scenarios are tagged for better organization and selective execution:

- `@position` - Position analysis scenarios
- `@risk` - Risk detection scenarios
- `@fibonacci` - Fibonacci analysis scenarios
- `@harmony` - Harmony calculation scenarios
- `@discord` - Discord integration scenarios
- `@notification` - Alert notification scenarios
- `@visualization` - Report and chart generation scenarios
- `@api` - API integration scenarios
- `@mock` - Scenarios using mock data

To run tests with a specific tag:

```bash
behave src/omega_bot_farm/trading/b0ts/bitget_analyzer/tests/BDD/features/ --tags=@risk
```

## Scenario Examples

The feature files contain scenarios like:

- Analyzing a position's risk level
- Detecting positions near liquidation
- Calculating Fibonacci retracement levels
- Determining position harmony scores
- Processing Discord commands
- Generating alerts for risky positions
- Creating visualization charts

## Adding New Scenarios

When adding new scenarios:

1. Identify the relevant feature file or create a new one
2. Write the scenario in Gherkin syntax (Given-When-Then)
3. Implement any missing step definitions in the steps directory
4. Tag the scenario appropriately
5. Run the tests to verify they pass

## Continuous Integration

These BDD tests are intended to be run as part of the CI/CD pipeline to ensure that the application behavior remains consistent across changes.
