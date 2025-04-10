
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


# OMEGA BTC AI - API Credential Tools

This directory contains tools for managing and verifying BitGet API credentials.

## Available Scripts

### 1. `print_api_credentials.sh`

This script displays and validates BitGet API credentials loaded from your environment.

**Features:**

- Display API credentials (masked by default for security)
- Validate API credentials against BitGet's API
- Option to show full credentials (with security warning)

**Usage:**

```bash
# Show masked credentials
./scripts/print_api_credentials.sh

# Show full credentials (use with caution!)
./scripts/print_api_credentials.sh --full

# Validate credentials and show masked credentials
./scripts/print_api_credentials.sh --validate

# Show and validate full credentials
./scripts/print_api_credentials.sh --full --validate

# Show help
./scripts/print_api_credentials.sh --help
```

### 2. `test_ccxt_connection.py`

This script tests the connection to BitGet using the CCXT library, displays account balance, and shows open positions.

**Features:**

- Connect to BitGet using CCXT integration
- Display account balance and open positions
- Option to use testnet or mainnet
- Validates API credentials and provides troubleshooting assistance
- Secure credential display (masked by default)

**Usage:**

```bash
# Test connection with masked credentials
python scripts/test_ccxt_connection.py

# Show full credentials (use with caution!)
python scripts/test_ccxt_connection.py --full

# Force testnet mode (regardless of .env setting)
python scripts/test_ccxt_connection.py --testnet

# Force mainnet mode (regardless of .env setting)
python scripts/test_ccxt_connection.py --mainnet
```

### 3. `run_persona_entry_monitor.sh`

This script runs the Persona-Based Entry Strategy Monitor with optional BitGet API integration.

**Features:**

- Run in foreground or background
- Run in tmux session for persistence
- Use mock data or real BitGet market data
- Configure API credentials via command line or .env files

**Usage:**

```bash
# Run with mock data
./scripts/run_persona_entry_monitor.sh --mock

# Run with real BitGet data (requires valid API credentials)
./scripts/run_persona_entry_monitor.sh

# Run in tmux session
./scripts/run_persona_entry_monitor.sh --tmux

# Run in background
./scripts/run_persona_entry_monitor.sh --background

# Specify API credentials
./scripts/run_persona_entry_monitor.sh --api-key YOUR_KEY --api-secret YOUR_SECRET --passphrase YOUR_PASS

# Show help
./scripts/run_persona_entry_monitor.sh --help
```

## Setting Up API Credentials

You can set up your BitGet API credentials in two ways:

1. **Using Environment Files:**
   - Root `.env` file at `/Users/fsiqueira/Desktop/GitHub/omega-btc-ai/.env`
   - Bot Farm `.env` file at `/Users/fsiqueira/Desktop/GitHub/omega-btc-ai/src/omega_bot_farm/.env`

   The Bot Farm `.env` file takes precedence over the Root `.env` file.

2. **Using the Interactive Setup:**

   ```bash
   python src/omega_bot_farm/bitget_positions_info.py --setup
   ```

## Validating API Credentials

You can validate your API credentials using:

```bash
python src/omega_bot_farm/bitget_positions_info.py --validate
```

or

```bash
./scripts/print_api_credentials.sh --validate
```

or

```bash
python scripts/test_ccxt_connection.py
```

## Security Notice

**IMPORTANT**: Keep your API credentials secure. Do not share them with anyone or include them in logs, screenshots, or public repositories.

When sharing output or logs, always make sure API credentials are masked or removed.
