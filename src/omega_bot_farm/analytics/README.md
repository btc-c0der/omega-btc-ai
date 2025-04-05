# Analytics Module

## Overview

The Analytics Module provides advanced data analysis capabilities for the Omega Bot Farm ecosystem. It processes market data, position data, and trading signals to extract meaningful insights and support decision-making processes.

## Components

### Market Analysis

- **Pattern Recognition**: Identifies technical patterns in market data
- **Trend Analysis**: Quantifies strength and direction of market trends
- **Volatility Metrics**: Calculates various volatility indicators

### Position Analysis

- **Performance Metrics**: Calculates ROI, drawdown, and other performance metrics
- **Risk Assessment**: Evaluates position risk relative to market conditions
- **Fibonacci Analysis**: Analyzes positions using Fibonacci retracement and extension levels

### Prediction Models

- **Price Prediction**: Short and medium-term price prediction models
- **Trend Prediction**: Forecasts potential market trend shifts
- **Position Outcome**: Estimates probability of specific position outcomes

## Integration

The Analytics Module integrates with:

1. **Trading Module**: Provides analysis for trading decisions
2. **Services Module**: Supplies data for various services
3. **Discord UI**: Feeds analysis results to user interfaces

## Data Flow

```
Market Data → Analytics Engine → Insights → Trading Bots/UI
     ↑                              ↓
Position Data ←───────────────── Services
```

## Usage

```python
from omega_bot_farm.analytics import market_analyzer

# Analyze market trend
trend_strength = market_analyzer.calculate_trend_strength(market_data)

# Analyze position using Fibonacci levels
fib_analysis = market_analyzer.analyze_position_fibonacci(position_data)
```

## Configuration

The Analytics Module uses configuration settings from:

- `config/analytics_config.yaml`
- Environment variables with `ANALYTICS_` prefix

## Development

When extending the Analytics Module:

1. Follow the established patterns for data input/output
2. Ensure backward compatibility with existing analytics
3. Document new analytics methods thoroughly
4. Add unit tests for any new analysis methods

# Omega Bot Farm Analytics

This directory contains analytics tools and visualizations for the Omega Bot Farm project.

## Quality Metrics

The `quality_metrics_visualization.py` script generates visualizations and metrics about the codebase quality, focusing on test coverage and distribution. This helps track the project's commitment to quality through comprehensive testing.

### Features

- Generates visualizations for test-to-source code ratio
- Visualizes the distribution of test types (unit, integration, component, etc.)
- Creates test coverage metrics by component
- Produces a test pyramid visualization
- Generates a comprehensive summary of quality metrics
- Creates a draft Medium post about the project's testing approach

### Usage

To generate all quality metrics visualizations:

```bash
cd /path/to/omega-btc-ai
python -m src.omega_bot_farm.analytics.quality_metrics_visualization
```

The visualizations will be saved to the `src/omega_bot_farm/analytics/visualizations` directory.

### Outputs

1. `codebase_composition.png` - Donut chart showing the breakdown of the codebase
2. `test_source_ratio.png` - Bar chart comparing test-to-source ratio with industry benchmarks
3. `test_types.png` - Horizontal bar chart showing distribution of different test types
4. `component_coverage.png` - Combined bar and line chart showing test coverage by component
5. `test_pyramid.png` - Test pyramid visualization
6. `quality_metrics_summary.md` - Markdown summary of all quality metrics
7. `medium_post_draft.md` - Draft Medium blog post about the testing approach

## Key Metrics

The project currently has:

- A 2.31:1 test-to-source code ratio (231% test coverage)
- Comprehensive testing across all levels:
  - Unit tests
  - Component tests
  - Integration tests
  - End-to-end tests
  - BDD/Gherkin feature specs
  - Security tests
