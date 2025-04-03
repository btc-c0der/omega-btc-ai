# Omega BTC AI - Bot Farm

## Overview

The Omega Bot Farm is a specialized environment for algorithmic trading bots powered by artificial intelligence. The farm includes various bots for market analysis, trading execution, position monitoring, and user interaction.

## Key Components

- **Trading B0ts**: Core algorithmic traders using various strategies
- **Analytics**: Tools for market analysis and prediction
- **Services**: Shared functionality across bots
- **Discord UI**: User interface via Discord for monitoring and control

## Waze Bot - Discord UI

The Waze Bot is the primary user interface for the Omega AI BTC system, providing a rich, context-driven experience for monitoring and analyzing BitGet positions through Discord.

### Features

- **Position Monitoring**: Track open positions on BitGet with real-time updates
- **Fibonacci Analysis**: Analyze positions using Fibonacci retracement and extension levels
- **Position Harmony**: Evaluate how well positions align with the golden ratio principles
- **Portfolio Recommendations**: Get actionable insights for portfolio management
- **Context-Aware Interaction**: Personalized responses based on user context
- **Automated Notifications**: Get alerts for significant position changes

### Setup Instructions

#### Prerequisites

1. Python 3.8+
2. BitGet API credentials
3. Discord Bot Token
4. Redis (optional, for data sharing)

#### Installation

1. Install required dependencies:

```bash
pip install discord.py redis python-dotenv pyyaml ccxt
```

2. Configure environment variables:

```bash
# Discord bot token
export DISCORD_TOKEN="your_discord_bot_token"

# BitGet API credentials (for default analyzer)
export BITGET_API_KEY="your_bitget_api_key"
export BITGET_SECRET_KEY="your_bitget_secret_key"
export BITGET_PASSPHRASE="your_bitget_passphrase"

# Redis configuration (optional)
export REDIS_HOST="localhost"
export REDIS_PORT="6379"
```

3. Configure the bot settings in `config/waze_bot_config.yaml`

4. Run the Waze Bot:

```bash
python -m src.omega_bot_farm.discord.waze_bot
```

### Discord Commands

#### Setup Commands

- `/bitget-setup` - Set up BitGet API credentials (securely via DM)
- `!waze-set-channel` - Set the current channel for Waze bot announcements

#### Analysis Commands

- `/bitget-positions` - Show your current BitGet positions
- `/bitget-analyze` - Analyze your BitGet positions with Fibonacci levels
- `/bitget-changes` - Show recent changes in your BitGet positions

#### Insight Commands

- `/golden-wisdom` - Receive trading wisdom based on Fibonacci principles
- `/market-pulse` - Get the current market sentiment

#### Help Command

- `!waze-help` - Show help information for Waze bot

### Integration with BitgetPositionAnalyzerB0t

The Waze Bot integrates directly with the `BitgetPositionAnalyzerB0t`, bringing its powerful Fibonacci-based position analysis to Discord. Key integration points:

1. **Personal Analysis**: Users can set up their own BitGet API credentials for personalized position analysis
2. **Shared Analysis**: A default analyzer can provide general market insights to all users
3. **Automated Monitoring**: The bot monitors positions and notifies users of significant changes
4. **Harmony Insights**: The bot provides insights into position harmony based on golden ratio principles

### Security

- API credentials are handled securely through direct messages
- Each user's API credentials are stored separately and not shared
- Sensitive position data is sent as ephemeral messages visible only to the requesting user

## Contributing

To contribute to the Omega Bot Farm:

1. Create a new branch for your feature
2. Implement and test your changes
3. Submit a pull request with a detailed description of your implementation

## License

This project is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.
