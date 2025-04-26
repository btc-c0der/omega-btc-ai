# Trap Probability Meter ASCII CLI Design

## Overview

This document provides an ASCII CLI mockup design for the Trap Probability Meter, which could serve as an alternative CLI interface to the Gradio web-based UI. The CLI version maintains the same core functionality while optimizing for terminal display.

## ASCII Mockup

```
╔══════════════════════════════════════════════════════════════╗
║                   TRAP PROBABILITY METER                      ║
╚══════════════════════════════════════════════════════════════╝

Current BTC price: $48,751.25 (+1.2%)

OVERALL TRAP PROBABILITY:
██████████████████░░░░░░░░░░░░░░░░  62.5% ▲

Detected pattern: Bull Trap (75% confidence)

PROBABILITY COMPONENTS:
Price Pattern:     ■■■■■■■■■■■■■■■■······  80.0%
  Strong upward reversal
Volume Spike:      ■■■■■■■■■■■········  60.0%
  Volume 1.7x above average
Fib Level:         ■■■■■■■■■■■■■······  70.0%
  Price near Fibonacci level (±0.3%)
Historical Match:  ■■■■■■■■■········  50.0%
  Similar to April 2023 pattern
Order Book:        ■■■■■■■■■■··········  40.0%
  Order book bid weighted (1.5x)
Market Regime:     ■■■■■■■■············  45.0%
  Distribution regime

Trend: Increasing

MARKET DATA:
┌───────────────────────────────┐
│ RSI: 68      MACD: Bullish    │
│ 24H Volume: $3.5B BTC         │
│ S/R Levels: 48.2K, 49.5K      │
│ Large sell wall at $49,200    │
└───────────────────────────────┘

Last updated: 2025-04-26 14:32:45
Press Ctrl+C to exit
```

## Design Elements

### Header
- ASCII box art using box-drawing characters for border
- Centered title text

### Probability Display
- Unicode block characters for progress bar (`█` for filled, `░` for empty)
- Percentage display with trend indicator (▲ for increasing, ▼ for decreasing, ◆ for stable)

### Trap Type Display
- Detected trap pattern with confidence percentage
- Color-coded based on trap type (red for bull trap, green for bear trap)

### Component Display
- Mini progress bars for each probability component
- Description text explaining the factor's current status
- Components sorted by contribution (highest first)

### Market Data Display
- Box-drawn container for market metrics
- Concise display of key technical indicators
- Support/resistance levels and significant market conditions

### Footer
- Timestamp of last update
- User instructions

## Color Scheme

When using ANSI color codes:

- **Green**: Low probability values, decreasing trends, bear traps
- **Yellow**: Moderate probability values, stable trends
- **Red**: High probability values, increasing trends, bull traps
- **Cyan**: Headers and UI elements
- **White**: Standard text and values
- **Bright White**: Important values and highlights

## Implementation Notes

1. Use ANSI escape codes for colors in compatible terminals
2. Provide a `--no-color` option for terminals without color support
3. Scale progress bars based on terminal width
4. Use Unicode characters only when supported; provide ASCII fallbacks
5. Include a "compact mode" for limited height terminals

## Command-Line Options

```
Usage: trap_meter_cli.py [OPTIONS]

Options:
  --interval SECONDS    Update interval in seconds (default: 5)
  --no-color            Disable color output
  --compact             Use compact display mode for smaller terminals
  --debug               Enable debug information
  --verbose             Show additional component details
  --width COLUMNS       Set custom display width
  --theme THEME         Display theme (default, dark, light, matrix)
```

## Related Components

This CLI interface corresponds to the following Gradio UI components:

1. `probability_display.py` → ASCII progress bar
2. `trend_display.py` → Trend indicator symbols
3. `components_display.py` → Component mini-bars and descriptions
4. `trap_type_display.py` → Trap type and confidence display
5. `market_data_display.py` → Box-drawn market data panel