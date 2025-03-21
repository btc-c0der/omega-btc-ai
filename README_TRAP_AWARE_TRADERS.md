# Trap-Aware Dual Position Traders

This module enhances the dual position traders system by integrating market maker trap detection using the Trap Probability Meter and implementing sophisticated elite exit strategies. It provides smarter trading decisions by being aware of potential market manipulation and using multiple factors for optimal exit decisions.

## What it Does

The Trap-Aware Dual Position Traders system:

1. Runs both the Trap Probability Meter and Dual Position Traders simultaneously
2. Continuously monitors for potential market maker traps (liquidity grabs, stop hunts, bull/bear traps, etc.)
3. Adjusts trading behavior based on detected traps
4. Sends alerts when high-probability traps are detected
5. Maintains all the functionality of the regular dual position traders system
6. Implements sophisticated elite exit strategies for optimal position management

## How It Works

The system uses the Trap Probability Meter to analyze various market indicators:

- Price patterns
- Volume spikes
- Fibonacci levels
- Historical pattern matches
- Order book imbalances
- Market regimes

When a potential trap is detected with high probability, the system will:

1. Adjust risk multipliers for both long and short traders
2. Send alerts with information about the detected trap
3. Provide trading recommendations based on the trap type
4. Execute elite exit strategies when conditions are met

For example:

- During a bull trap, it reduces risk for long positions and increases it for shorts
- During a bear trap, it reduces risk for short positions and increases it for longs
- During liquidity grabs or stop hunts, it reduces risk on both sides
- When elite exit conditions are met, it executes sophisticated exit strategies

## Benefits

- **Reduced Losses**: Avoid getting caught in market maker traps
- **Better Entries**: Enter positions at better prices by being aware of manipulation
- **Safer Exits**: Exit positions before potential reversals using elite exit strategies
- **Market Insights**: Gain deeper understanding of market dynamics
- **Reduced Emotional Trading**: Let the system objectively identify manipulation
- **Sophisticated Exit Management**: Use multiple factors for optimal exit decisions

## How to Use

### Prerequisites

1. Make sure Redis is running on localhost:6379
2. Ensure you have the necessary BitGet API credentials set up
3. Verify that both sub-accounts exist on BitGet

### Running the System

Use the provided shell script:

```bash
./run_trap_aware_traders.sh
```

Or run with custom parameters:

```bash
./run_trap_aware_traders.sh --min-free-balance 200 --trap-probability-threshold 0.7
```

### Available Parameters

- `--symbol`: Trading symbol (default: BTCUSDT)
- `--testnet`: Use testnet (default: False)
- `--long-capital`: Initial capital for long trader (default: 24.0 USDT)
- `--short-capital`: Initial capital for short trader (default: 24.0 USDT)
- `--long-leverage`: Leverage for long positions (default: 20)
- `--short-leverage`: Leverage for short positions (default: 20)
- `--no-pnl-alerts`: Disable PnL alerts
- `--account-limit`: Maximum total account value in USDT (0 means no limit)
- `--long-sub-account`: Sub-account name for long positions
- `--short-sub-account`: Sub-account name for short positions (default: fst_short)
- `--trap-probability-threshold`: Threshold for considering trap probability (default: 0.7)
- `--trap-alert-threshold`: Threshold for sending trap alerts (default: 0.8)
- `--no-trap-protection`: Disable trap protection features
- `--min-free-balance`: Minimum free balance to maintain in each account (default: 100.0 USDT)

## Trap Types Detected

The system can detect various types of market maker traps:

- **Bull Trap (🐂)**: A false breakout above resistance to trap buyers
- **Bear Trap (🐻)**: A false breakdown below support to trap sellers
- **Liquidity Grab (💰)**: Sudden price movement to grab liquidity at a key level
- **Stop Hunt (🎯)**: Price pushed to common stop loss levels then reverses
- **Fake Pump (🚀)**: Artificial pump to create FOMO then dump
- **Fake Dump (📉)**: Artificial dump to create panic selling then pump

## Alert Example

When a trap is detected, you'll receive an alert like this:

```
⚠️ MARKET MAKER TRAP DETECTED ⚠️

Type: 🐂 Bull Trap
Probability: 85.5%
Confidence: 78.2%

Trading Recommendations:
- Consider closing long positions
- Be cautious about entering new longs
- Short positions may benefit

Time: 2023-03-21 12:34:56
```

## Monitoring

The system logs detailed information in `trap_aware_trading.log`. You can monitor this file to see what's happening:

```bash
tail -f trap_aware_trading.log
```

## Configuration

You can adjust risk thresholds and other parameters in the script to fit your trading style. The default configuration is:

- Trap probability threshold: 0.7 (70%)
- Trap alert threshold: 0.8 (80%)
- Risk multipliers: 0.5x to 1.2x depending on trap type

## Elite Exit Strategy

The system includes a sophisticated elite exit strategy that uses multiple factors to determine optimal exit points:

1. **Fibonacci Levels**: Exits based on key Fibonacci retracement levels
2. **Pattern Recognition**: Identifies reversal patterns for exit signals
3. **Trap Detection**: Exits when high-probability traps are detected
4. **Market Regime**: Adapts exits based on current market regime
5. **Trailing Stops**: Dynamic trailing stops to protect profits
6. **Risk Management**: Position sizing and risk adjustment based on market conditions

The elite exit strategy can be enabled with the `--enable-elite-exits` flag and configured with `--elite-exit-confidence` to set the minimum confidence required for exit signals.

Example exit conditions:

- Price reaches key Fibonacci levels
- Reversal patterns form with high confidence
- Market regime shifts significantly
- High-probability traps are detected
- Trailing stop is hit
- Risk management thresholds are reached

### Elite Exit Configuration

The elite exit strategy can be configured with the following parameters:

- `--enable-elite-exits`: Enable the elite exit strategy (default: False)
- `--elite-exit-confidence`: Minimum confidence required for exit signals (default: 0.7)
- `--base-risk-percent`: Base risk percentage for position sizing (default: 1.0)
- `--enable-trailing-stop`: Enable trailing stops (default: True)
- `--trailing-stop-distance`: Distance for trailing stop in percentage (default: 0.5)
- `--trailing-stop-step`: Step size for trailing stop adjustments (default: 0.1)
- `--enable-fibonacci-exits`: Enable Fibonacci-based exits (default: True)
- `--enable-pattern-exits`: Enable pattern-based exits (default: True)
- `--enable-trap-exits`: Enable trap-based exits (default: True)

### Elite Exit Signals

The elite exit strategy generates exit signals based on multiple factors:

1. **Fibonacci-Based Exits**:
   - Exits when price reaches key Fibonacci retracement levels
   - Adjusts exit points based on market context
   - Uses multiple timeframes for confirmation

2. **Pattern-Based Exits**:
   - Identifies reversal patterns (head and shoulders, double tops/bottoms, etc.)
   - Confirms patterns with volume and momentum
   - Uses multiple timeframes for pattern validation

3. **Trap-Based Exits**:
   - Exits when high-probability traps are detected
   - Adjusts exit timing based on trap type
   - Uses trap probability for position sizing

4. **Market Regime Exits**:
   - Adapts exits based on current market regime
   - Uses multiple indicators for regime identification
   - Adjusts risk parameters based on regime

5. **Trailing Stop Management**:
   - Dynamic trailing stops to protect profits
   - Adjusts stop distance based on volatility
   - Uses step-based adjustments for smoother exits

### Example Usage

To enable and configure the elite exit strategy:

```bash
./run_trap_aware_traders.sh \
  --enable-elite-exits \
  --elite-exit-confidence 0.8 \
  --base-risk-percent 1.5 \
  --enable-trailing-stop \
  --trailing-stop-distance 0.7 \
  --trailing-stop-step 0.2
```

This configuration:

- Enables the elite exit strategy
- Sets a high confidence threshold (80%)
- Uses a 1.5% base risk per trade
- Enables trailing stops with 0.7% distance
- Uses 0.2% steps for trailing stop adjustments

The system will then use these parameters to make sophisticated exit decisions based on multiple market factors.

## Troubleshooting

If you encounter issues:

1. Ensure Redis is running: `redis-cli ping`
2. Check the Trap Probability Meter is functioning: `python -m omega_ai.tools.trap_probability_meter --debug`
3. Verify your BitGet API credentials
4. Check log files for specific errors
