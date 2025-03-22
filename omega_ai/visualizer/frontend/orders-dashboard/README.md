# OMEGA BTC AI - Live Trading Dashboard

## Overview

The OMEGA BTC AI Live Trading Dashboard provides real-time monitoring of BitGet trading activity with a Rastafarian-themed visualization. The dashboard connects to the MM WebSocket server to receive updates about system status, orders, positions, and trader performance.

## Installation

No additional setup is required if you are already using the OMEGA BTC AI system. The dashboard is built with:

- **Backend**: FastAPI WebSocket server
- **Frontend**: HTML, CSS, and JavaScript

## Usage

### Starting the Dashboard

You can launch the dashboard using the provided startup script:

```bash
cd /path/to/omega-btc-ai
python omega_ai/visualizer/start_mm_dashboard.py
```

By default, the script will:

1. Start a new MM WebSocket server on port 8765 (if none is running)
2. Start a frontend server on port 7000
3. Open your default web browser to access the dashboard

### Command-line Options

The startup script supports several options:

```bash
python omega_ai/visualizer/start_mm_dashboard.py [options]
```

Available options:

- `--backend-port PORT`: Specify the port for the MM WebSocket server (default: 8765)
- `--frontend-port PORT`: Specify the port for the frontend server (default: 7000)
- `--no-browser`: Don't automatically open the browser
- `--use-existing-mm`: Use an existing MM WebSocket server if one is running

### Port Conflict Handling

The script now includes intelligent port conflict handling:

- If the MM WebSocket server port is already in use and `--use-existing-mm` is specified, it will connect to the existing server.
- If the MM WebSocket server port is already in use and `--use-existing-mm` is not specified, it will find an available port and start a new server.
- If the frontend server port is already in use, it will automatically find an available port to use.

### MM WebSocket Server Status Tool

A separate tool is provided to check if the MM WebSocket server is running:

```bash
python omega_ai/visualizer/mm_server_status.py --port 8765
```

Output formats:

- Default console output
- JSON format (with `--json` flag)

## Features

- **System Status**: View the current status of the OMEGA BTC AI system
- **Trader Performance**: Monitor metrics like total PnL and active positions
- **Active Positions**: See all open positions with current status
- **Live Order Log**: Real-time updates of all trading activities
- **Performance Charts**: Visual representation of PnL over time

### Order Log Controls

- Pause/resume updates
- Clear the log
- Filter by order type

## Architecture

The dashboard consists of:

1. **MM WebSocket Server**: Provides real-time trading data
2. **Frontend HTTP Server**: Serves the dashboard UI
3. **Client Browser**: Renders the dashboard and connects to the WebSocket

## Customization

The dashboard uses a dark theme with Rastafarian color accents (green, gold, red, and black). You can customize the appearance by modifying the CSS in `static/styles.css`.

## Troubleshooting

### Connection Issues

- Verify the MM WebSocket server is running using the status tool
- Check for network connectivity issues
- Ensure no firewall is blocking the required ports

### Server Already Running

- Use the `--use-existing-mm` flag to connect to an existing server
- Or let the script automatically find an available port

## Dependencies

- Python 3.7+
- HTML5-compatible browser
- Network connectivity between components

## License

This dashboard is part of the OMEGA BTC AI system and follows its licensing terms.
