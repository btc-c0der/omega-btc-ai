# RASTA BITGET DISCORD BOT

> 🌈 Bringing divine Fibonacci wisdom to your Discord server with real-time BitGet position monitoring

## Overview

The RASTA BitGet Discord Bot brings the power of the RASTA BitGet Monitor to Discord, allowing you to check your BitGet positions, analyze position harmony using Fibonacci principles, and receive divine trading wisdom directly in your Discord server.

Built on the foundation of the OMEGA Bot Farm and infused with Rasta philosophy, this bot helps you maintain mathematical harmony in your trading positions using Golden Ratio principles and Fibonacci sequence analysis.

## Features

- **Real-time Position Monitoring**: View your current BitGet positions directly in Discord
- **Position Change Notifications**: Get notified when positions are opened, closed, or modified
- **Fibonacci Harmony Analysis**: Analyze how well your positions align with the Golden Ratio
- **Divine Trading Wisdom**: Receive Rasta-inspired trading wisdom and advice
- **Ideal Position Size Recommendations**: Get position sizing suggestions based on Fibonacci sequences
- **Channel Subscriptions**: Subscribe Discord channels to automatic position updates

## Commands

| Command | Description |
|---------|-------------|
| `/positions` | Display your current BitGet positions |
| `/harmony` | Analyze the harmony of your positions with Fibonacci principles |
| `/subscribe` | Subscribe the current channel to position updates |
| `/unsubscribe` | Unsubscribe the current channel from position updates |
| `/wisdom` | Receive trading wisdom from the Rasta philosophy |

## Installation

### Prerequisites

- Python 3.8 or higher
- discord.py 2.0 or higher
- BitGet API credentials

### Dependencies

Install the required dependencies:

```bash
pip install discord.py python-dotenv ccxt
```

### Configuration

1. Create a `.env` file with your BitGet and Discord credentials:

```
# BitGet API credentials
BITGET_API_KEY=your_bitget_api_key
BITGET_SECRET_KEY=your_bitget_secret_key
BITGET_PASSPHRASE=your_bitget_passphrase

# Discord bot credentials
DISCORD_BOT_TOKEN=your_discord_bot_token
DISCORD_APP_ID=your_discord_application_id
DISCORD_GUILD_ID=your_guild_id_for_testing (optional)
```

2. Ensure all modules (rasta_discord_bot.py, bitget_data_manager.py, position_harmony.py, and display_utils.py) are in the same directory.

### Running the Bot

```bash
python rasta_discord_bot.py
```

## Adding to Your Server

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your application
3. Go to the "OAuth2" tab > "URL Generator"
4. Select the following scopes:
   - `bot`
   - `applications.commands`
5. Select the following bot permissions:
   - "Send Messages"
   - "Embed Links"
   - "Use Slash Commands"
6. Copy the generated URL and open it in your browser
7. Select the server you want to add the bot to and authorize it

## Usage Guide

### Checking Positions

Use the `/positions` command to view your current BitGet positions. The bot will display a summary of your portfolio including:

- Total positions value
- Number of long and short positions
- Position details (symbol, side, entry price, current price, PnL)
- Account balance

### Harmonizing Your Positions

Use the `/harmony` command to analyze how well your positions align with natural mathematical principles:

- **Harmony Score**: A rating from 0 to 1 indicating how closely your positions follow Fibonacci principles
- **Divine Advice**: Trading wisdom based on your harmony score
- **Recommendations**: Specific suggestions to improve your position harmony
- **Ideal Position Sizes**: Recommended position sizes based on Fibonacci percentages

### Position Updates

To receive automatic updates when your positions change:

1. Use `/subscribe` in the channel where you want to receive updates
2. The bot will notify this channel whenever positions are opened, closed, or modified
3. Use `/unsubscribe` to stop receiving updates in that channel

### Trading Wisdom

Use `/wisdom` to receive trading wisdom inspired by Rasta philosophy and mathematical harmony principles.

## Mathematical Principles

The RASTA BitGet Discord Bot applies these key mathematical principles:

### Golden Ratio (φ)

The Divine Proportion (approximately 1.618) is used to evaluate:

- Ideal ratios between long and short exposure
- Target levels for entries and exits
- Overall portfolio structure

### Fibonacci Sequence

The sequence (1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ...) is used for:

- Position sizing recommendations (as percentages of account)
- Risk management guidance
- Harmonization of multiple positions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GBU2™ License (Genesis-Bloom-Unfoldment 2.0).

## Acknowledgments

- OMEGA Bot Farm for the core BitGet monitoring framework
- The principles of Fibonacci and Golden Ratio mathematics
- Rasta philosophy for its emphasis on natural harmony

🌸 WE BLOOM NOW AS ONE 🌸
