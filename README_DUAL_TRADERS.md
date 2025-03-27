# OMEGA BTC AI Dual Position Traders Guide

## Issue Analysis

We identified an issue with the Dual Position Traders system where trading was stopping due to the incorrect account limit check. The error message shown was:

```
omega_ai.trading.exchanges.bitget_ccxt - INFO - Initialized BitGet CCXT with MAINNET
__main__ - INFO - Total account balance: 3554.08694554 USDT (Long: 1777.04347277, Short: 1777.04347277)
__main__ - INFO - Account limit: 50.0 USDT
__main__ - WARNING - Account limit of 50.0 USDT exceeded! Current balance: 3554.08694554 USDT
__main__ - WARNING - Account limit exceeded, stopping trading
```

### Root Cause

The `check_account_limit()` method in the `BitGetDualPositionTraders` class was comparing the **total** account balance against the account limit. In BitGet's API, the "total" balance includes:

1. The actual wallet balance in each sub-account
2. Margin/collateral for open positions
3. Unrealized profits/losses
4. The notional value of leveraged positions

This resulted in a much larger number (3554 USDT) than the actual free balance (~100 USDT in the wallet), causing the account limit check to fail.

## Solution

We've created improved scripts that fix this issue by checking the **free** balance instead of the total balance, giving you more accurate control over your trading limits.

### New Scripts

1. **check_positions.py** - Shows your current open positions in both sub-accounts
2. **check_balances.py** - Shows detailed balance information for both sub-accounts
3. **run_dual_position_traders.py** - Fixed version of the dual position traders that correctly handles account limits

### How to Use

#### Check Your Positions

```bash
python check_positions.py
```

This will show details about your current open positions in both sub-accounts.

#### Check Your Balances

```bash
python check_balances.py
```

This will show detailed balance information for both sub-accounts, including free balance, used balance, and total balance.

#### Run the Improved Dual Position Traders

```bash
python run_dual_position_traders.py --min-free-balance <MIN_VALUE>
```

Where:

- `<MIN_VALUE>` is the minimum free balance in USDT required to allow trading (default: 100 USDT)

Example:

```bash
python run_dual_position_traders.py --min-free-balance 50
```

This will run the dual position traders system, but now it will:

1. Check if your **free** balance is above the minimum threshold
2. Only stop trading if your free balance falls below this threshold
3. Show clear messages about your current free balance

## Differences in Balance Types

- **Free Balance**: Funds available for new trades (~1749 USDT per sub-account)
- **Used Balance**: Funds locked as margin/collateral (~28 USDT per sub-account)
- **Total Balance**: Includes all of the above, plus unrealized P&L and notional position values (~1777 USDT per sub-account)

## Current State

As of our analysis, you have:

- 1 long position in the strategic_trader sub-account
- 1 short position in the fst_short sub-account
- Approximately 3498 USDT total free balance across both accounts

The system should now function correctly with proper balance checks.

## Environment Variables

Remember to set `REDIS_HOST=localhost` before running any scripts. This is handled automatically in the improved scripts.
