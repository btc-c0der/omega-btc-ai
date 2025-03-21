# Trap-Aware Dual Position Traders

This module enhances the dual position traders system by integrating market maker trap detection using the Trap Probability Meter. It provides smarter trading decisions by being aware of potential market manipulation.

## What it Does

The Trap-Aware Dual Position Traders system:

1. Runs both the Trap Probability Meter and Dual Position Traders simultaneously
2. Continuously monitors for potential market maker traps (liquidity grabs, stop hunts, bull/bear traps, etc.)
3. Adjusts trading behavior based on detected traps
4. Sends alerts when high-probability traps are detected
5. Maintains all the functionality of the regular dual position traders system

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

For example:

- During a bull trap, it reduces risk for long positions and increases it for shorts
- During a bear trap, it reduces risk for short positions and increases it for longs
- During liquidity grabs or stop hunts, it reduces risk on both sides

## Benefits

- **Reduced Losses**: Avoid getting caught in market maker traps
- **Better Entries**: Enter positions at better prices by being aware of manipulation
- **Safer Exits**: Exit positions before potential reversals
- **Market Insights**: Gain deeper understanding of market dynamics
- **Reduced Emotional Trading**: Let the system objectively identify manipulation

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

## Troubleshooting

If you encounter issues:

1. Ensure Redis is running: `redis-cli ping`
2. Check the Trap Probability Meter is functioning: `python -m omega_ai.tools.trap_probability_meter --debug`
3. Verify your BitGet API credentials
4. Check log files for specific errors
