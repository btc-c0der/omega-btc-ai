# End-to-End Tests for Bitget Position Analyzer

This directory contains end-to-end tests for the Bitget Position Analyzer bot. These tests verify the complete functionality of the bot in a realistic environment, simulating actual usage scenarios.

## Test Structure

The end-to-end tests are organized by test scenarios:

- `test_full_analysis_workflow.py`: Tests the entire analysis pipeline from data retrieval to recommendations
- `test_discord_integration.py`: Tests integration with Discord for commands and notifications
- `test_real_time_processing.py`: Tests processing of real-time market data updates

## Test Environment

These tests use a combination of real and mock components:

- Real implementation code is used when available
- External dependencies (like exchange APIs) are mocked for reliability and repeatability
- Market data is simulated with realistic scenarios

## Running Tests

To run all end-to-end tests:

```bash
cd /path/to/omega-btc-ai
pytest src/omega_bot_farm/trading/b0ts/bitget_analyzer/tests/end_to_end/ -v
```

To run specific end-to-end test files:

```bash
pytest src/omega_bot_farm/trading/b0ts/bitget_analyzer/tests/end_to_end/test_full_analysis_workflow.py -v
```

## Test Configuration

Test configuration is managed through the `e2e_config` fixture in `conftest.py`. You can provide a custom configuration by setting the `E2E_CONFIG_PATH` environment variable:

```bash
E2E_CONFIG_PATH=/path/to/custom_config.json pytest src/omega_bot_farm/trading/b0ts/bitget_analyzer/tests/end_to_end/
```

## Fixtures and Test Data

- `fixtures/` directory contains test data and configuration files
- `fixtures/mock_data/` contains mock exchange data
- `fixtures/scenarios/` contains market data scenarios for simulation
- `fixtures/output/` is used for test-generated files

## Market Data Simulator

The tests include a market data simulator that can:

1. Load predefined price movement scenarios
2. Generate synthetic market data scenarios
3. Simulate real-time market updates

## Test Scenarios

These tests cover the following scenarios:

1. **Full Analysis Workflow**: Tests the complete pipeline from data fetching to recommendations
2. **Risk Detection**: Tests detection of high-risk positions and appropriate alerts
3. **Multiple Timeframe Analysis**: Tests analysis across different timeframes
4. **Harmony Threshold Impact**: Tests how different harmony thresholds affect recommendations
5. **Discord Command Handling**: Tests processing Discord commands and generating responses
6. **Alert Notifications**: Tests generating and sending alert notifications
7. **Real-Time Data Processing**: Tests continuous monitoring and analysis of changing market data

## Creating Custom Scenarios

You can create custom test scenarios by adding JSON files to the `fixtures/scenarios/` directory. Each scenario should include a sequence of market data updates that simulates a specific market condition.

## Continuous Integration

These tests are intended to be run as part of the CI/CD pipeline to ensure the complete functionality of the bot remains intact across changes.
