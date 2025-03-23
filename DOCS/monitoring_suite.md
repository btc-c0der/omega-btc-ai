# OMEGA BTC AI - Integrated Monitoring Suite

The OMEGA BTC AI Integrated Monitoring Suite combines multiple monitoring tools into a unified dashboard, providing comprehensive real-time insights for cryptocurrency trading.

## Features

- **Combined Monitoring**: View RastaBitgetMonitor and TrapProbabilityMeter in a single window
- **Efficient Layout**: Optimized screen space allocation (85/15 split)
- **Real-time Updates**: Position data refreshes every 3 seconds, trap probability every 5 seconds
- **Persistent Logging**: External log file for RastaBitgetMonitor in `rasta_bitget_monitor.log`
- **Clean Interface**: Custom tmux styling with distinctive borders and status bar
- **Session Management**: Detach/reattach functionality via tmux

## Usage

Run the monitoring suite with a single command:

```bash
./run_monitors.sh
```

### Keyboard Controls

- **Detach from session**: `Ctrl+B`, then `D` (leaves the session running in background)
- **Reattach to session**: `tmux attach -t omega-monitors`
- **Exit completely**: `Ctrl+B`, then `&` (confirm with `y`)

## Components

### RastaBitgetMonitor (Top Pane)

Displays real-time information about your BitGet positions:

- Active positions with PnL calculations
- Fibonacci retracement levels
- Golden ratio harmonic analysis
- Position health indicators

### TrapProbabilityMeter (Bottom Pane)

Analyzes market conditions for potential manipulation:

- Overall trap probability percentage
- Component-level analysis (price patterns, volume, order book, etc.)
- Trap type prediction with confidence level
- Trend indicators

## Requirements

- Python 3.7+
- tmux
- redis-server (for data persistence)

## Customization

The default configuration provides an optimal balance between the two monitoring components, but you can adjust the layout by modifying the `run_monitors.sh` script:

- Change the refresh interval by modifying the `--interval` parameters
- Adjust the vertical space allocation by changing the `-y` percentage in the `resize-pane` command
- Modify the styling by editing the `set-option` commands

## Troubleshooting

If you encounter issues:

1. Verify that Redis is running (`redis-cli ping` should return `PONG`)
2. Check the RastaBitgetMonitor log file for errors: `tail -f rasta_bitget_monitor.log`
3. Ensure BitGet API credentials are properly set in your `.env` file
4. If tmux session becomes unresponsive, kill it with: `tmux kill-session -t omega-monitors`
