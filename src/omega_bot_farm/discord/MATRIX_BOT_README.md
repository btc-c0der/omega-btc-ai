# Matrix Discord Bot Integration

## Overview

The Matrix Discord Bot provides a cyberpunk-styled visualization of BitGet trading positions directly in Discord. It brings the aesthetic and functionality of the CLI Matrix Bot to your Discord server with beautifully formatted messages and embedded visualizations.

## Bot Status

- **App ID**: 1358189845931098130
- **Bot Name**: 0m3g4_B1Tg3T_b0t
- **Commands**:
  - `/matrix-positions` - Show BitGet positions with Matrix-themed visualization
  - `/matrix-account` - Show account overview with Matrix styling
  - `/matrix-snapshot` - Take a snapshot of current positions with cyberpunk styling
  - `/ping` - Simple ping command to check if the bot is online
  - `/test_matrix` - Test the Matrix visualization

## Startup and Usage

### Running the Bot

1. Start the bot with:

   ```bash
   python -m src.omega_bot_farm.discord.bot
   ```

   If you have Redis connection issues, you can use the simplified bot:

   ```bash
   python -m src.omega_bot_farm.discord.simple_bot
   ```

2. The bot should show as online in your Discord server
3. Use the slash commands to interact with the bot

### Environment Setup

The bot requires a valid Discord token in your `.env` file:

```
DISCORD_TOKEN=your_bot_token_here
```

If you need to update your token, you can use:

```bash
python -m src.omega_bot_farm.discord.update_token
```

## Troubleshooting

### Connection Issues

If the bot shows offline, check:

1. First verify the token with the test script:

   ```bash
   python -m src.omega_bot_farm.discord.test_connection
   ```

2. If the token test works but the main bot fails, try the simple bot version which doesn't depend on Redis:

   ```bash
   python -m src.omega_bot_farm.discord.simple_bot
   ```

3. Check Discord Developer Portal for any issues with your bot application

### Command Issues

If slash commands don't appear:

1. Make sure the bot has the correct permissions
2. Reinvite the bot using the OAuth2 URL Generator in the Discord Developer Portal
   - Required Scopes: `bot`, `applications.commands`
   - Required Permissions: Send Messages, Embed Links, Attach Files, Use Slash Commands

## Live API Integration

By default, the bot uses mock data for demonstration. To connect to your actual BitGet account:

1. Add your BitGet API credentials to the `.env` file:

   ```
   BITGET_API_KEY=your_api_key
   BITGET_API_SECRET=your_api_secret
   BITGET_API_PASSPHRASE=your_passphrase
   ```

2. Modify the Matrix Bot initialization in `matrix_bot_commands.py` to use real API data

---

🧬 **CH33RS TO THE B0TS!** 🧬
