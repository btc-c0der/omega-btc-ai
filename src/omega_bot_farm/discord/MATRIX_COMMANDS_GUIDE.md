# Matrix Bot Discord Commands Guide

## Available Commands

The Matrix Bot now supports the following slash commands:

### Core Matrix Visualization Commands

- `/matrix-positions` - Show BitGet positions with Matrix-themed visualization
- `/matrix-account` - Show account overview with Matrix styling
- `/matrix-snapshot` - Take a snapshot of current positions with cyberpunk styling

### Test and Utility Commands

- `/ping` - Check if the bot is online and get latency
- `/test_matrix` - Test the Matrix visualization functionality

## Command Usage Examples

### Viewing Your Trading Positions

To see your BitGet positions with cyberpunk Matrix styling:

1. Type `/matrix-positions` in any channel where the bot has access
2. Press Enter or click the command
3. The bot will respond with a beautifully formatted visualization showing:
   - Position details (symbol, side, size)
   - Entry and mark prices
   - PnL information
   - Liquidation distances
   - Fibonacci levels and quantum harmonic metrics

### Checking Account Overview

To view your overall account summary:

1. Type `/matrix-account` in Discord
2. The bot will respond with:
   - Account balance and equity
   - Exposure metrics (long, short, ratios)
   - Quantum harmony score
   - Schumann resonance visualization

### Taking a Full Snapshot

For a complete cyberpunk snapshot of all your trading data:

1. Type `/matrix-snapshot` in Discord
2. The bot will generate a full report including:
   - ASCII art visualization
   - Account metrics
   - All current positions
   - Matrix-themed visuals

## Troubleshooting

If commands don't appear in Discord:

1. Make sure the bot has been added with proper permissions
   - Bot scope
   - Applications.commands scope
   - Message permissions
2. Try the `/ping` command to confirm the bot is responsive
3. Run the test connection script to verify the bot's status:

   ```
   python -m src.omega_bot_farm.discord.test_connection
   ```

## Running the Bot

The recommended way to run the bot is using:

```bash
python -m src.omega_bot_farm.discord.simple_bot
```

This version doesn't require Redis and includes all Matrix commands.

---

🧬 **CH33RS TO THE B0TS!** 🧬
