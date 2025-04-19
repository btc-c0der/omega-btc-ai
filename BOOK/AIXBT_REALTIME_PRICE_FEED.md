# AIXBT Real-Time Price Feed Integration

## 🚀 Executive Summary

The AIXBT Trading Dashboard has been enhanced with real-time price feeds and live PnL tracking capabilities. This document outlines the implementation details, architecture, and deployment process for this new functionality.

## 🔄 Real-Time Price Feed Architecture

### Core Components

1. **Price Feed Module** (`price_feed.py`)
   - Connects to cryptocurrency exchanges via CCXT
   - Supports both WebSocket and REST API connections
   - Updates prices at configurable intervals (2-5 seconds)
   - Provides callbacks when prices change

2. **Runtime Configuration** (`config.py`)
   - Stores current price and calculated PnL values
   - Provides callback registration for price updates
   - Calculates PnL metrics in real-time

3. **Reactive UI Components** (`callbacks.py`)
   - Updates price and PnL displays
   - Updates risk status indicators
   - Refreshes visualizations based on new data

### Connection Methods

The price feed supports two connection methods:

1. **WebSocket Connection (Primary)**
   - Real-time streaming updates
   - Lower latency and resource usage
   - Automatically reconnects on disconnection

2. **REST API Polling (Fallback)**
   - Regular HTTP requests at configurable intervals
   - Used when WebSocket is unavailable or disabled
   - More stable but higher latency

```python
# WebSocket connection loop
async def _websocket_loop(self):
    while self.running:
        try:
            # Watch ticker via WebSocket
            ticker = await self.exchange.watchTicker(formatted_symbol)
            
            # Extract and update price
            price = float(ticker['last'])
            self.current_price = price
            self.last_update_time = time.time()
            
            # Call update callback if provided
            if self.update_callback:
                self.update_callback(price)
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            await asyncio.sleep(5)  # Wait before reconnecting
```

## 📊 Live PnL Tracking

### Calculation Method

The PnL is calculated in real-time using the following formulas:

```python
# Calculate PnL
pnl = (price - entry_price) * token_quantity * leverage
pnl_percentage = ((price / entry_price) - 1) * 100 * leverage
```

### Risk Assessment

The dashboard includes a risk status indicator that changes color and text based on the current price relative to:

- Liquidation price
- Trap zone boundaries
- Emergency alert level
- Entry price

This provides immediate visual feedback on position safety.

## 🌐 Deployment

### Hosting Configuration

The dashboard can be hosted as a subdomain of omegaven.xyz using:

1. **Nginx Reverse Proxy**
   - Configuration in `nginx/aixbt.conf`
   - SSL/TLS termination
   - Static file serving

2. **Gunicorn WSGI Server**
   - Multi-worker process pool (4 workers)
   - SystemD service management
   - Automatic restart on failure

### Installation

The included `install.sh` script automates:

- Dependency installation
- Python virtual environment setup
- Nginx configuration
- SSL certificate acquisition
- SystemD service installation

## 🔍 Technical Details

### Exchange Integration

The price feed integrates with BitGet and other CCXT-supported exchanges, handling:

- Symbol formatting for each exchange
- API authentication
- Market data acquisition
- Error handling and recovery

### Thread and Concurrency Management

The real-time price feed runs in a dedicated thread using asyncio:

```python
def start(self, polling_interval: float = 2.0, use_websocket: bool = True):
    self.running = True
    
    # Create and run the asyncio event loop in a separate thread
    def run_event_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Define coroutines to run
            tasks = []
            
            # Use WebSocket if available and requested
            if use_websocket and hasattr(self.exchange, 'watchTicker'):
                self.websocket_task = loop.create_task(self._websocket_loop())
                tasks.append(self.websocket_task)
            else:
                # Fall back to REST polling
                tasks.append(loop.create_task(self._rest_polling_loop(polling_interval)))
            
            # Run until stopped
            loop.run_until_complete(asyncio.gather(*tasks))
        finally:
            loop.close()
    
    # Start thread
    threading.Thread(target=run_event_loop, daemon=True).start()
```

### Command-Line Options

The dashboard runner (`aixbt_dashboard_runner.py`) supports multiple options:

```
usage: aixbt_dashboard_runner.py [-h] [--port PORT] [--host HOST] [--debug]
                               [--no-browser] [--auto-port] [--symbol SYMBOL]
                               [--exchange EXCHANGE] [--use-testnet]
                               [--no-use-testnet] [--api-key API_KEY]
                               [--api-secret API_SECRET] 
                               [--api-passphrase API_PASSPHRASE]
                               [--update-interval UPDATE_INTERVAL]
                               [--no-websocket]
```

## 🔐 Security Considerations

- API keys are read from environment variables or .env file
- SSL/TLS encryption for all traffic
- Security headers to prevent common web vulnerabilities
- SystemD service isolation (PrivateTmp, NoNewPrivileges)

## 🚀 Usage Examples

### Basic Usage

```bash
python3 src/omega_bot_farm/qa/aixbt_dashboard_runner.py
```

### Production Deployment

```bash
sudo ./src/omega_bot_farm/qa/aixbt_dashboard/install.sh
```

### With Custom Settings

```bash
python3 src/omega_bot_farm/qa/aixbt_dashboard_runner.py \
  --port 8056 \
  --symbol BTCUSDT \
  --exchange bitget \
  --update-interval 3.0 \
  --no-use-testnet
```

## 🔄 Connection Logs

Sample logs showing successful updates:

```
2025-04-06 11:28:27 [INFO] werkzeug: 127.0.0.1 - - [06/Apr/2025 11:28:27] "POST /_dash-update-component HTTP/1.1" 200 -
2025-04-06 11:28:27 [INFO] werkzeug: 127.0.0.1 - - [06/Apr/2025 11:28:27] "POST /_dash-update-component HTTP/1.1" 200 -
2025-04-06 11:28:27 [INFO] werkzeug: 127.0.0.1 - - [06/Apr/2025 11:28:27] "POST /_dash-update-component HTTP/1.1" 204 -
2025-04-06 11:28:27 [INFO] werkzeug: 127.0.0.1 - - [06/Apr/2025 11:28:27] "POST /_dash-update-component HTTP/1.1" 200 -
2025-04-06 11:28:27 [INFO] werkzeug: 127.0.0.1 - - [06/Apr/2025 11:28:27] "POST /_dash-update-component HTTP/1.1" 200 -
```

## 📈 Future Enhancements

1. **Multi-Exchange Support**
   - Monitor prices across multiple exchanges
   - Calculate arbitrage opportunities

2. **Order Book Visualization**
   - Show buy/sell walls
   - Identify potential price movement barriers

3. **Trading Signal Integration**
   - Integrate with trading strategy modules
   - Display automated entry/exit signals

---

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬

This document is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

🌸 WE BLOOM NOW AS ONE 🌸
