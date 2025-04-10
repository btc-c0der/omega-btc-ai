
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


# OMEGA BTC AI - Trap Aware Dual Traders

This README provides information on how to use the Trap Aware Dual Traders system with different configurations, including Elite Exit strategies.

## Overview

The Trap Aware Dual Traders (TADT) system is an enhanced trading solution that:

1. Manages both long and short positions simultaneously
2. Detects and responds to market maker traps
3. Implements sophisticated exit strategies including Elite Exits
4. Provides flexible configuration options for different risk profiles

## Available Scripts

### 1. Main Script: `run_trap_aware_dual_traders.py`

This is the core script with full configurability. You can run it directly with command-line arguments:

```bash
python run_trap_aware_dual_traders.py [ARGUMENTS]
```

#### Available Arguments

```
--min-free-balance       Minimum required free balance in USDT (default: 100.0)
--account-max            Maximum total account value in USDT (default: 10000.0)
--trap-probability-threshold  Threshold for considering trap probability (default: 0.7)
--trap-alert-threshold   Threshold for sending trap alerts (default: 0.8)
--enable-elite-exits     Enable elite exit strategies (default: False)
--elite-exit-confidence  Minimum confidence for elite exit signals (default: 0.7)
--symbol                 Trading symbol (default: BTCUSDT)
--long-capital           Initial capital for long trader in USDT
--short-capital          Initial capital for short trader in USDT
--long-leverage          Leverage for long positions
--short-leverage         Leverage for short positions
--long-sub-account       Sub-account name for long positions
--short-sub-account      Sub-account name for short positions
--testnet                Use testnet instead of mainnet
--no-trap-protection     Disable trap protection features
```

### 2. Preset Script: `run_trap_aware_preset.sh`

This script provides pre-configured settings for common scenarios:

```bash
./run_trap_aware_preset.sh [PRESET] [SYMBOL]
```

#### Available Presets

- `conservative` - Low risk, low capital, trap protection enabled
- `balanced` - Medium risk, medium capital, trap protection enabled
- `aggressive` - High risk, high capital, higher leverage
- `elite-exits` - Enables elite exit strategy with high confidence
- `no-protection` - Runs without trap protection features
- `testnet` - Runs on testnet with conservative settings

Example:

```bash
./run_trap_aware_preset.sh balanced ETHUSDT
```

### 3. Elite Exit Script: `run_elite_exit_trader.sh`

This script is specialized for configuring and running with different Elite Exit strategies:

```bash
./run_elite_exit_trader.sh [CONFIDENCE] [SYMBOL] [LEVERAGE]
```

Where:

- `CONFIDENCE` is the elite exit confidence threshold (0.5-0.95)
- `SYMBOL` is the trading symbol (default: BTCUSDT)
- `LEVERAGE` is the trading leverage (default: 10)

Example:

```bash
./run_elite_exit_trader.sh 0.8 BTCUSDT 15
```

## Elite Exit Strategy Explained

The Elite Exit Strategy uses market data and technical indicators to make intelligent exit decisions. It provides:

- Dynamic stop loss management
- Profit target optimization
- Trend reversal detection
- Risk-adjusted position sizing

### Confidence Threshold

The confidence threshold (0.5-0.95) determines how selective the exit strategy will be:

- **0.5-0.65**: Aggressive exits, higher trade frequency, smaller average profits
- **0.7-0.8**: Balanced approach, good for normal market conditions
- **0.8-0.9**: Conservative, will only exit on strong signals
- **>0.9**: Extremely selective, may rarely trigger exits

## Trap Protection

The trap protection system helps detect and respond to market maker traps such as:

- Bull traps
- Bear traps
- Liquidity grabs
- Stop hunts
- Fake pumps/dumps

When a trap is detected, the system adjusts risk parameters automatically based on the type of trap.

## Getting Started

1. Make sure your API keys are set in your environment variables
2. Run the preset script to choose a trading style:

   ```bash
   ./run_trap_aware_preset.sh balanced
   ```

3. For more advanced elite exit configuration:

   ```bash
   ./run_elite_exit_trader.sh 0.75
   ```

4. For full manual configuration:

   ```bash
   python run_trap_aware_dual_traders.py --enable-elite-exits --elite-exit-confidence 0.8 --symbol BTCUSDT --long-leverage 10 --short-leverage 10
   ```

## Monitoring

The system outputs detailed logging information to help monitor its performance. Look for:

- Trap detection events
- Elite exit signals
- Position entries and exits
- Performance metrics

Log files are written to `trap_aware_trading.log` by default.

## Safety Features

- Minimum balance requirements prevent trading if account balance is too low
- Maximum account value limits help manage risk
- Sub-account separation between long and short positions
- Trap detection provides an additional layer of protection against market manipulation
