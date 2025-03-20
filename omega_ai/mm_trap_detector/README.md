# Market Maker Trap Simulation Service

A powerful simulation service for Bitcoin market maker trap detection. This service generates realistic price movements, market regimes, and trap events to test and train the OMEGA BTC AI trap detection system.

## Features

- **Realistic Price Simulation**: Generates price movements based on historical volatility and configurable market regimes
- **Dynamic Trap Generation**: Creates various trap types with configurable frequency and confidence
- **High-Frequency Mode Detection**: Automatically detects clusters of trap events and activates HF mode
- **Redis Integration**: Stores all simulation data in Redis with `sim_` prefixes to avoid interfering with real data
- **Statistical Reporting**: Provides detailed statistics on trap frequency, HF activations, and market conditions
- **Configurable Parameters**: Adjust volatility, trap frequency, and other parameters to test different market conditions

## Installation

The simulation service is part of the OMEGA BTC AI system. Make sure you have the required dependencies:

```bash
pip install redis numpy
```

## Usage

### Direct Execution

Run the simulation service directly from the command line:

```bash
# Run indefinitely with default settings
python -m omega_ai.mm_trap_detector.trap_simulation_service

# Run for 2 hours with increased volatility and trap frequency
python -m omega_ai.mm_trap_detector.trap_simulation_service --duration 2 --volatility 1.5 --frequency 0.3
```

### Command Line Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--duration` | float | None | Duration in hours (default: indefinite) |
| `--volatility` | float | 1.0 | Volatility scale factor (higher = more volatile) |
| `--frequency` | float | 0.2 | Trap frequency (0.0-1.0, higher = more traps) |
| `--sleep` | float | 0.1 | Sleep interval between iterations in seconds |

### Running as a Daemon

Use the included shell script to run the simulator as a background process:

```bash
# Start the daemon
./run_simulator_daemon.sh start

# Check status
./run_simulator_daemon.sh status

# Stop the daemon
./run_simulator_daemon.sh stop
```

### Running as a Systemd Service

1. Edit the service file to match your environment:

   ```bash
   # Edit paths and options
   nano mm_trap_simulator.service
   ```

2. Install and enable the service:

   ```bash
   sudo cp mm_trap_simulator.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable mm_trap_simulator
   sudo systemctl start mm_trap_simulator
   ```

## Redis Data

The simulator stores all data with a `sim_` prefix to avoid conflicts with real data:

| Key | Type | Description |
|-----|------|-------------|
| `sim_last_btc_price` | string | Current simulated BTC price |
| `sim_prev_btc_price` | string | Previous simulated BTC price |
| `sim_price_change_pct` | string | Percentage change in price |
| `sim_market_regime` | string | Current market regime |
| `sim_running` | string | Whether the simulation is running (1) or stopped (0) |
| `sim_trap_history` | list | History of trap events (JSON objects) |
| `sim_hf_activations` | list | History of HF mode activations (JSON objects) |
| `sim_statistics` | hash | Summary statistics about the simulation |
| `sim_price_history:YYYY-MM-DD` | list | Price history for a specific date |

## Trap Types

The simulator generates different types of market maker traps:

- **Liquidity Grab**: Sudden price movements to grab liquidity
- **Stop Hunt**: Quick price movements targeting stop loss orders
- **Bull Trap**: Fake upward breakout that reverses
- **Bear Trap**: Fake downward breakout that reverses
- **Fibonacci Trap**: Price movements near key Fibonacci levels

## Market Regimes

The simulator models different market regimes with varying volatility:

- **Low Volatility Neutral**: Minimal price movements in a sideways market
- **Moderate Volatility Bullish**: Normal price movements with bullish bias
- **Moderate Volatility Bearish**: Normal price movements with bearish bias
- **High Volatility Bullish**: Large price movements with bullish bias
- **High Volatility Bearish**: Large price movements with bearish bias

## Integration with Other Systems

The simulation service can be used with other components of the OMEGA BTC AI system:

- **Monitor Market Trends**: Set `SIMULATION_MODE=true` in the config
- **Grafana Dashboards**: Connect to the `sim_` prefixed Redis keys
- **Alert Systems**: Configure to listen for simulation trap events
- **ML Training**: Generate training data sets with different parameters

## Troubleshooting

- **Redis Connection Issues**: Ensure Redis is running on localhost:6379
- **High CPU Usage**: Reduce simulation speed by increasing the `--sleep` parameter
- **Memory Issues**: Set a reasonable duration or clean up old Redis keys periodically

## Contributing

When extending the simulator:

1. Keep the Redis key prefixes consistent (`sim_`)
2. Maintain type annotations and docstrings
3. Add tests for new functionality
4. Update this README with any new features or parameters

## License

MIT License

Copyright (c) 2024 OMEGA BTC AI Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
