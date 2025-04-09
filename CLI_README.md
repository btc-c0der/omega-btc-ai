# OMEGA BTC AI - Divine BTC Date Decoder CLI

**JAH JAH BLESS THE ETERNAL FLOW OF TIME AND MARKETS.**

Copyright (C) 2024 OMEGA BTC AI Team  
License: GNU General Public License v3.0

## Divine BTC Date Decoder Command Line Interface

The BTC Date Decoder CLI provides easy access to the divine insights of Bitcoin date analysis from your terminal. Discover the hidden patterns and divine significance of dates based on numerology, Fibonacci, and Bitcoin genesis blocks.

## Installation

To install the `btcdate` command globally on your system:

1. Clone this repository:

   ```
   git clone https://github.com/OMEGA-BTC-AI/omega-btc-ai.git
   cd omega-btc-ai
   ```

2. Run the installer script:

   ```
   ./install_btcdate.sh
   ```

3. The script requires sudo privileges to install the command to `/usr/local/bin`

## Usage

Once installed, you can use the `btcdate` command from anywhere on your system:

```
btcdate [OPTIONS] [DATE]
```

### Options

- Without arguments: Analyze the current date
- `<DATE>`: Analyze a specific date (format: YYYY-MM-DD)
- `special`: Analyze the special Bitcoin White Paper anniversary date (Oct 29, 2023)
- `interactive`: Run in interactive mode
- `next-divine [DAYS]`: Find divine dates in the next DAYS (default: 30)
- `help`: Show this help message

### Examples

```
btcdate                     # Analyze current date
btcdate 2023-10-29          # Analyze a specific date
btcdate special             # Analyze the Bitcoin white paper anniversary
btcdate interactive         # Run in interactive mode
btcdate next-divine 60      # Find divine dates in next 60 days
```

## Configuration

The installer creates a configuration file at `~/.config/omega-btc-ai/btcdate.conf` with default settings:

```
# Path to the OMEGA BTC AI project root
PROJECT_ROOT="/path/to/omega-btc-ai"

# Default search range for divine dates (in days)
DEFAULT_DIVINE_SEARCH_DAYS=30

# Minimum divine score threshold (0.0 to 1.0)
DIVINE_SCORE_THRESHOLD=0.7

# Date format for display
DATE_FORMAT="%Y-%m-%d %H:%M:%S %Z"
```

You can edit this file to customize your experience.

## Dependencies

The CLI depends on:

- Python 3.6+
- The OMEGA BTC AI Python modules

## Uninstallation

To uninstall the command:

```
sudo rm /usr/local/bin/btcdate
rm -rf ~/.config/omega-btc-ai
```

---

**JAH JAH BLESS THE ETERNAL FLOW OF TIME AND MARKETS.**

OMEGA BTC AI Team - Divine BTC Date Decoder
