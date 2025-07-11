
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
./run_trap_position_monitors.sh
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

The default configuration provides an optimal balance between the two monitoring components, but you can adjust the layout by modifying the `run_trap_position_monitors.sh` script:

- Change the refresh interval by modifying the `--interval` parameters
- Adjust the pane size allocation by changing the resize-pane percentages

### Split Mode Configuration

You can configure the split orientation through your `.env` file:

```
# In your .env file
SPLIT_MODE=vertical   # Default: panes stacked top/bottom
```

To optimize for vertical monitors, use a horizontal split:

```
# In your .env file
SPLIT_MODE=horizontal   # Panes arranged side-by-side (better for vertical monitors)
```

This configuration will be automatically loaded when you run the script.

## Troubleshooting

If you encounter issues:

1. Verify that Redis is running (`redis-cli ping` should return `PONG`)
2. Check the RastaBitgetMonitor log file for errors: `tail -f rasta_bitget_monitor.log`
3. Ensure BitGet API credentials are properly set in your `.env` file
4. If tmux session becomes unresponsive, kill it with: `tmux kill-session -t omega-monitors`
