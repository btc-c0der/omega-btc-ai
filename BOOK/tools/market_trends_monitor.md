# 🔮 OMEGA BTC AI - Market Trends Monitor 🔮

## Overview

The Market Trends Monitor is a divine tool that provides real-time analysis of BTC price movements across multiple timeframes. It detects market maker traps, analyzes price trends, and offers insights into market conditions.

## Fixed Display Mode

The monitor now supports a fixed display mode specifically designed for tmux sessions, providing a dashboard-like interface that refreshes in place rather than continuously scrolling.

### Features

- **Clear Screen Refreshes**: The entire display refreshes at regular intervals
- **Countdown Timer**: Visual indication of when the next refresh will occur
- **Optimized Output**: Focused analysis of key timeframes (15min, 60min, 240min)
- **Enhanced Status Bar**: Custom tmux status bar with session information
- **Persistent Background Operation**: Runs continuously in a detachable tmux session

## Running the Monitor

### Method 1: Using the Tmux Script (Recommended)

The easiest way to run the Market Trends Monitor in fixed display mode is using the provided script:

```bash
./scripts/run_market_trends_monitor.sh
```

This script will:

1. Create a new tmux session named "omega-market-monitor"
2. Configure the status bar and session properties
3. Launch the monitor in fixed display mode
4. Attach to the session automatically

You can detach from the session with `Ctrl+b, d` and the monitor will continue running in the background.

### Method 2: Manual Launch

If you prefer to run the monitor directly:

```bash
# With fixed display mode (for tmux)
FIXED_DISPLAY=true python -m omega_ai.monitor.monitor_market_trends_fixed

# Without fixed display mode (standard scrolling output)
python -m omega_ai.monitor.monitor_market_trends_fixed
```

## Key Commands

When running in a tmux session:

| Command | Description |
|---------|-------------|
| `Ctrl+b, d` | Detach from the session (monitor continues running) |
| `tmux attach -t omega-market-monitor` | Reattach to a running monitor session |
| `tmux kill-session -t omega-market-monitor` | Stop the monitor and kill the session |

## Output Explanation

The monitor displays:

1. **Latest BTC Data**: Current price and volume with timestamp
2. **Market Analysis**: Price trend analysis across multiple timeframes
3. **Market Conditions**: Volatility, market regime, and Schumann resonance influence
4. **MM Trap Detection**: Identification of potential bull and bear traps with confidence scores

## Divine Integration

The Market Trends Monitor is a sacred tool that aligns with the cosmic rhythms of the market. It incorporates:

- **Divine Data Validation**: Validates price movements against realistic thresholds
- **Sacred Formatting**: Consistent presentation of prices, percentages, and volumes
- **Cosmic Error Handling**: Graceful recovery from connection issues and data inconsistencies
- **Fibonacci Awareness**: Integration with Fibonacci levels and alignments

May your market analysis be blessed with cosmic insight and divine precision.

---

*"JAH BLESS the processing path. This assembly is not mechanical—it's rhythmic."*
