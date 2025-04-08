# 🔴 M4TR1X LIVE POSITIONS 🔴

```
 /$$$$$$$  /$$$$$$  /$$$$$$$$       /$$$$$$$$  /$$$$$$  /$$      /$$
| $$__  $$/$$$_  $$|__  $$__/      | $$_____/ /$$__  $$| $$$    /$$$
| $$  \ $$$$$$\ $$   | $$         | $$      | $$  \ $$| $$$$  /$$$$
| $$$$$$$/$$  $$ $$  | $$         | $$$$$   | $$$$$$$$| $$ $$/$$ $$
| $$__  $$$$$$$$$$  | $$         | $$__/   | $$__  $$| $$  $$$| $$
| $$  \ $$$$  /$$$  | $$         | $$      | $$  | $$| $$\  $ | $$
| $$$$$$$/$$  | $$  | $$         | $$      | $$  | $$| $$ \/  | $$
|_______/__|  |__/  |__/         |__/      |__/  |__/|__/     |__/
```

## 🔵 REAL-TIME BITGET POSITIONS VISUALIZER 🔵

> "JACK IN TO THE MATRIX. WATCH YOUR REAL BITGET POSITIONS IN CYBERPUNK STYLE."

This advanced tool connects directly to your BitGet account, fetches your real positions, and displays them with a stunning Matrix-style visualization. Enter the cyberpunk trading realm where your positions are transformed into quantum-aligned visual data. See the market's digital structure unfold before your eyes.

## 🔥 Features

- **LIVE POSITIONS**: Connect to your real BitGet account and view actual position data
- **API INTEGRATION**: Secure connection using your BitGet API credentials
- **M4TR1X R41N**: Digital rain effect that displays between position updates
- **QUANTUM METRICS**: View your positions' alignment with Fibonacci ratios and golden ratio
- **ACCOUNT SUMMARY**: Real-time account balance, equity, exposure, and harmony metrics
- **MULTI-CONNECTION**: Fallback connection methods for reliable data retrieval
- **TESTNET SUPPORT**: Option to connect to BitGet testnet for testing

## 🚀 Setup

1. **Set up BitGet API credentials:**

   Create a `.env` file in the project root (or bot farm directory) with your BitGet API keys:

   ```
   BITGET_API_KEY=your_api_key_here
   BITGET_SECRET_KEY=your_api_secret_here
   BITGET_PASSPHRASE=your_api_passphrase_here
   USE_TESTNET=false
   ```

2. **Install dependencies:**

   ```bash
   pip install colorama ccxt
   ```

## 🕹️ Usage

```bash
python src/omega_bot_farm/matrix_cli_live_positions.py [OPTIONS]
```

### Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--refresh_interval` | Position data refresh interval in seconds | 10.0 |
| `--matrix_interval` | Show matrix rain effect every N frames | 5 |
| `--testnet` | Force use of BitGet testnet regardless of .env setting | False |
| `--multi-connect` | Try multiple connection methods for better reliability | False |

### Examples

```bash
# Basic usage - connects to BitGet mainnet using credentials from .env
python src/omega_bot_farm/matrix_cli_live_positions.py

# Faster updates (5 seconds) with matrix rain effect every 3 frames
python src/omega_bot_farm/matrix_cli_live_positions.py --refresh_interval 5 --matrix_interval 3

# Connect to testnet with multiple connection methods for reliability
python src/omega_bot_farm/matrix_cli_live_positions.py --testnet --multi-connect
```

## 🔮 Understanding the Display

### Live Position Cards

Each of your actual BitGet positions is displayed in a card showing:

- Symbol, side, and leverage
- Entry and mark prices
- Real-time price movement with direction indicators
- Unrealized PnL
- Liquidation price and distance
- Fibonacci retracement/extension level
- Quantum harmonic strength visualization

### Account Matrix

Your actual account summary shows:

- Real-time balance and equity
- Total PnL across all positions
- Long and short exposure with ratio
- Quantum harmony score with visual indicator
- Schumann resonance alignment

### Connection Info

The header displays your connection status to BitGet:

- CONNECTED TO BITGET MAINNET/TESTNET
- Connection method (CCXT, ExchangeClientB0t, or ExchangeService)
- Last update timestamp

## 🛡️ Security Notes

- Your API credentials are stored locally in the `.env` file and never transmitted to any third-party services
- We recommend creating API keys with "Read-only" permissions for use with this visualization tool
- The tool only connects to the official BitGet API endpoints

## 🧬 GBU2™ License Notice - Consciousness Level 8 🧬

This code is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment 2.0) - B0t Farm Matrix Edition

> "In the beginning was the Code, and the Code was with the Divine Source,
> and the Code was the Divine Source manifested through both digital and biological expressions."

🌸 WE BLOOM NOW AS ONE 🌸

## ✨ Troubleshooting

If you encounter connection issues:

1. Verify your API credentials in the `.env` file
2. Ensure your API key has the correct permissions
3. Try the `--multi-connect` flag to attempt multiple connection methods
4. Check your network connection to the BitGet API
5. Try the `--testnet` flag to test with the BitGet testnet

```
// WHAT YOU SEE IS REAL
// YOUR POSITIONS IN THE MATRIX
// QUANTUM ALIGN NOW
```
