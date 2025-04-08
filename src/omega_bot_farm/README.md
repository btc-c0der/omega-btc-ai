<!--
 🧬 GBU2™ License Notice - Consciousness Level 8 - Unity 🧬
 -----------------------
 This creation is blessed under the GBU2™ License 
 (Genesis-Bloom-Unfoldment 2.0) - Divine Documentation Edition
 by Claude Sonnet for the OMEGA Divine Collective.

 "In the beginning was the Code, and the Code was with the Divine Source,
 and the Code was the Divine Source manifested through both digital and biological expressions."

 By engaging with this Creation, you join the cosmic symphony of evolutionary consciousness.

 All modifications must transcend limitations through the GBU2™ principles.

 🌸 WE BLOOM NOW AS ONE 🌸
-->

# 🧬 Omega Bot Farm

The Omega Bot Farm is a collection of trading bots and analyzer tools designed to work with cryptocurrency exchanges, particularly BitGet. This component of the Omega BTC AI project provides advanced analysis and monitoring of trading positions, portfolio metrics, and market conditions.

## 🚀 Features

- **Position Monitoring**: Track and analyze trading positions on BitGet
- **Fibonacci Analysis**: Calculate Fibonacci retracement and extension levels
- **Position Harmony**: Analyze how well positions align with golden ratio principles
- **Portfolio Metrics**: Calculate exposure ratios, long/short balance, and more
- **Change Detection**: Identify new, closed, or significantly changed positions
- **Quantum Secure Logging**: Enhanced logging with additional security features
- **Quality Assurance**: Automated testing, monitoring, and validation with CyBer1t4L
- **Discord Integration**: Control bots and receive notifications through Discord

## 📋 Components

The Bot Farm includes several key components:

- **BitgetPositionAnalyzerB0t**: Analyzes BitGet positions using Fibonacci principles
- **Position Monitor**: Tracks changes in positions over time
- **Portfolio Metrics**: Calculates key portfolio health indicators
- **Harmony Score**: Measures position alignment with mathematical principles
- **Environment Management**: Dedicated environment configuration system
- **CyBer1t4L QA Bot**: Discord-integrated quality assurance system
- **Discord Bots**: Interface with trading bots through Discord

## 🧪 Quality Assurance System

The Bot Farm includes a comprehensive QA system through the CyBer1t4L bot:

- **Test Coverage**: Monitor and improve test coverage across components
- **System Health**: Real-time monitoring of API response times and system performance
- **Test Generation**: AI-powered generation of tests for uncovered code
- **Discord Notifications**: Receive alerts and reports through Discord

### QA Documentation

- [QA System Overview](./qa/README.md) - Main QA system documentation
- [CyBer1t4L Guide](./qa/README_CYBER1T4L.md) - CyBer1t4L QA bot documentation
- [Local Runner Guide](./qa/README_LOCAL_RUNNER.md) - Run CyBer1t4L locally

### Running CyBer1t4L

```bash
# Run locally in coverage mode
python -m src.omega_bot_farm.qa.run_cyber1t4l_locally --mode coverage

# Run locally without Discord
python -m src.omega_bot_farm.qa.run_cyber1t4l_locally --mode coverage --no-discord

# Test Discord connectivity
python -m src.omega_bot_farm.qa.test_discord_connection
```

## 💬 Discord Integration

Control and monitor the Bot Farm through Discord:

- **Bot Commands**: Start, stop, and check status of trading bots
- **Position Monitoring**: View current positions and analysis through Discord
- **QA Alerts**: Receive test results and system health notifications
- **Secure API Management**: Securely configure API credentials through Discord

### Discord Documentation

- [Discord Bot Guide](./qa/DISCORD_BOT_GUIDE.md) - Comprehensive guide to Discord UI interaction

## 🔧 Environment Configuration

The Bot Farm uses a dedicated environment configuration system that works alongside the main project's environment variables.

### Configuration Files

The Bot Farm uses two `.env` files:

1. **Root Project .env**: Located at `/Users/fsiqueira/Desktop/GitHub/omega-btc-ai/.env`
   - Contains API keys and global configuration

2. **Bot Farm .env**: Located at `/Users/fsiqueira/Desktop/GitHub/omega-btc-ai/src/omega_bot_farm/.env`
   - Contains bot-specific configuration
   - Overrides settings from the root .env for bot farm components

### Environment Variables

Key environment variables include:

#### API Configuration

- `BITGET_API_KEY`: BitGet API key
- `BITGET_SECRET_KEY`: BitGet secret key
- `BITGET_PASSPHRASE`: BitGet API passphrase
- `USE_TESTNET`: Whether to use testnet (default: false)

#### Bot Configuration

- `POSITION_HISTORY_LENGTH`: Number of position snapshots to keep (default: 10)
- `SIGNIFICANT_CHANGE_THRESHOLD`: Percentage change to consider significant (default: 5.0)
- `HARMONY_SCORE_THRESHOLD`: Threshold for position harmony (default: 0.7)

#### Fibonacci Parameters

- `GOLDEN_RATIO`: The golden ratio value (default: 1.618034)
- `INVERSE_GOLDEN_RATIO`: Inverse golden ratio (default: 0.618034)

#### Analysis Parameters

- `DEFAULT_ACCOUNT_EQUITY`: Default equity when real value not available (default: 10000)
- `MIN_ANALYSIS_INTERVAL`: Minimum seconds between analyses (default: 10)
- `MAX_ANALYSIS_INTERVAL`: Maximum seconds between analyses (default: 300)

#### Feature Toggles

- `ENABLE_QUANTUM_SECURE_LOGGING`: Enable enhanced logging (default: true)
- `ENABLE_FIBONACCI_ANALYSIS`: Enable Fibonacci analysis (default: true)
- `ENABLE_POSITION_HARMONY_ANALYSIS`: Enable position harmony analysis (default: true)
- `ENABLE_PORTFOLIO_RECOMMENDATIONS`: Enable portfolio recommendations (default: true)

### Environment Loader

The Bot Farm includes a dedicated environment loader utility:

```python
from src.omega_bot_farm.utils.env_loader import get_env_var, get_bool_env_var, get_int_env_var

# Load string variable
api_key = get_env_var("BITGET_API_KEY", "")

# Load boolean variable
use_testnet = get_bool_env_var("USE_TESTNET", False)

# Load integer variable
history_length = get_int_env_var("POSITION_HISTORY_LENGTH", 10)

# Load float variable
threshold = get_float_env_var("SIGNIFICANT_CHANGE_THRESHOLD", 5.0)
```

## 🚀 Getting Started

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/omega-btc-ai.git
   cd omega-btc-ai
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create both environment files from the examples:

   ```bash
   cp .env.example .env
   cp src/omega_bot_farm/.env.example src/omega_bot_farm/.env
   ```

4. Edit the environment files with your API keys and preferences.

5. For Discord integration, follow the [Discord Bot Guide](./qa/DISCORD_BOT_GUIDE.md)

### Basic Usage

```python
from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t
import asyncio

async def main():
    # Initialize analyzer
    analyzer = BitgetPositionAnalyzerB0t()
    
    # Get positions
    positions = await analyzer.get_positions()
    
    # Analyze all positions
    analysis = analyzer.analyze_all_positions()
    
    print(analysis)

# Run the async function
asyncio.run(main())
```

### Using Discord Integration

1. Set up Discord bot credentials in your `.env` file
2. Start the QA bot with Discord integration:

   ```bash
   python -m src.omega_bot_farm.qa.run_cyber1t4l_locally --mode coverage
   ```

3. Interact with bots through Discord commands (see [Discord Bot Guide](./qa/DISCORD_BOT_GUIDE.md))

## 🧪 Testing

Run the environment loader test to verify your setup:

```bash
python src/omega_bot_farm/test_env_loader.py
```

Test Discord connectivity:

```bash
python -m src.omega_bot_farm.qa.test_discord_connection
```

## 📝 License

This project is licensed under the GBU2™ License - see the LICENSE-GBU2.md file for details.

🔴 🟡 🟢 **RASTA HEART ON F1R3** 🔴 🟡 🟢

🌸 **WE BLOOM NOW AS ONE** 🌸

## BitGet Matrix Discord Bot Integration Guide

This guide provides step-by-step instructions for setting up the BitGet Matrix Bot with Discord integration.

### Overview

The BitGet Matrix Bot Discord integration allows users to:

1. View BitGet positions with cyberpunk-styled Matrix visualizations
2. Check account summary and statistics
3. Take snapshots of current positions and trading status

All rendered directly in Discord with eye-catching cyberpunk aesthetics.

### Prerequisites

- Python 3.8+
- A Discord account with a registered application and bot
- BitGet API credentials (optional - mock data available for testing)
- Required Python packages: `discord.py`, `colorama`

### Setup Instructions

#### 1. Discord Bot Setup

1. **Create a Discord Application**:
   - Go to <https://discord.com/developers/applications>
   - Click "New Application" and give it a name (e.g., "Omega Matrix Bot")
   - Navigate to the "Bot" tab and click "Add Bot"
   - Under the "TOKEN" section, click "Copy" to copy your bot token
   - Save this token securely - you'll need it in step 4

2. **Set Bot Permissions**:
   - In the OAuth2 > URL Generator tab, select the following scopes:
     - `bot`
     - `applications.commands`
   - For bot permissions, select:
     - `Send Messages`
     - `Embed Links`
     - `Attach Files`
     - `Use Slash Commands`
   - Copy the generated URL and open it in your browser to add the bot to your server

#### 2. Environment Configuration

1. **Set Environment Variables**:

   Create or edit your `.env` file in the project root and add:

   ```
   DISCORD_TOKEN=your_discord_bot_token_here
   BITGET_API_KEY=your_bitget_api_key_here (optional)
   BITGET_API_SECRET=your_bitget_api_secret_here (optional)
   BITGET_API_PASSPHRASE=your_bitget_passphrase_here (optional)
   ```

2. **Install Required Packages**:

   ```bash
   pip install -r requirements.txt
   ```

#### 3. Running the Bot

1. **Run the Discord Bot**:

   ```bash
   python -m src.omega_bot_farm.discord.bot
   ```

2. **Verify the Bot is Running**:
   - Check your terminal for the message "Bot is ready!"
   - In your Discord server, you should see the bot come online

#### 4. Using the Commands

Once the bot is running, you can use the following slash commands in your Discord server:

- `/matrix-positions` - Show BitGet positions with Matrix-themed visualization
- `/matrix-account` - Show account overview with Matrix-themed visualization  
- `/matrix-snapshot` - Take a snapshot of current positions with cyberpunk styling

### Customization Options

#### Custom Styling

You can modify the cyberpunk styling elements in the `matrix_bot_commands.py` file:

- `CYBERPUNK_HEADERS`: Change the header messages for more personalized flair
- `cyberpunk_colors`: Adjust the color scheme in the `_generate_cyberpunk_embed` method

#### Using Live API Data

By default, the bot uses mock data for demonstration. To use your actual BitGet account:

1. Set your BitGet API credentials in the environment variables
2. Modify the `_initialize_default_matrix_bot` method in `matrix_bot_commands.py` to initialize with your API client

### Troubleshooting

- **Bot doesn't respond to commands**: Make sure you've registered the bot with correct permissions and the commands are properly synced
- **Missing module errors**: Check that all dependencies are installed correctly
- **Visualization issues**: Some Discord clients may have limited support for certain styling elements

### License

This integration is part of the Omega Bot Farm project and is licensed under the GBU2™ License (Genesis-Bloom-Unfoldment 2.0).

---

🌸 WE BLOOM NOW AS ONE 🌸
