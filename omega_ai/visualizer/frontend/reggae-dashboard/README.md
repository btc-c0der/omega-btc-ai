# OMEGA BTC AI - Reggae Dashboard 🌟

A modern, Rastafarian-themed dashboard for real-time Bitcoin trading analysis and visualization.

## Features 🚀

- Real-time Bitcoin price tracking
- Market trap probability analysis
- Position tracking and PnL monitoring
- Live Redis data integration
- Beautiful Reggae-themed UI with animations
- Responsive design for all devices

## Prerequisites 📋

- Python 3.8 or higher
- Redis server (optional - will use fallback data if not available)
- Modern web browser

## Installation 🛠️

1. Clone the repository:

```bash
git clone https://github.com/yourusername/omega-btc-ai.git
cd omega-btc-ai
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install required packages:

```bash
pip install flask redis
```

## Running the Dashboard 🎯

1. **Important**: On macOS, the default port 5000 might be in use by AirPlay. You have two options:

   a. Disable AirPlay Receiver:
   - Go to System Preferences -> General -> AirDrop & Handoff
   - Disable "AirPlay Receiver"

   b. Or use a different port (e.g., 5001) when starting the server:

   ```bash
   cd omega_ai/visualizer/frontend/reggae-dashboard
   python3 live-api-server.py --port 5001
   ```

2. Start the server (default port 5000):

```bash
cd omega_ai/visualizer/frontend/reggae-dashboard
python3 live-api-server.py
```

3. Access the dashboard:

- Open your web browser
- Go to `http://localhost:5000` (or `http://localhost:5001` if using alternate port)
- The dashboard will automatically update every 2 seconds

## Features Guide 🎮

- **Bitcoin Price**: Real-time BTC price with percentage change
- **Connection Status**: Shows Redis connection status and data source
- **Trap Probability**: Market trap analysis with component breakdown
- **Position Data**: Current trading position details and PnL
- **Manual Refresh**: Click the "Refresh Data Now" button to force an update
- **JAH Messages**: Rastafarian wisdom messages with animations

## Troubleshooting 🔧

1. **Port in Use Error**:
   - Follow the instructions above for handling port 5000 conflicts on macOS
   - Or use a different port with the `--port` argument

2. **Redis Connection Issues**:
   - The dashboard will automatically fall back to simulated data
   - Check your Redis server status if you want live data

3. **Data Not Updating**:
   - Check your internet connection
   - Verify the API server is running
   - Try the manual refresh button

## Contributing 🤝

Feel free to contribute to this project! We welcome:

- Bug reports
- Feature requests
- Pull requests
- UI/UX improvements

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## JAH BLESS 🙏

Remember: "JAH LOVE ❤️ GUIDE THE WAY"
