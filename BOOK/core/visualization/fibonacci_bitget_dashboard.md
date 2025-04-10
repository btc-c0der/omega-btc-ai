
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


# BitGet Fibonacci Golden Ratio Monitoring Dashboard

## Overview

The BitGet Fibonacci Golden Ratio Dashboard is a sophisticated real-time monitoring system for BitGet Mainnet Futures Contracts. It provides deep position analytics based on Fibonacci Golden Ratio principles, allowing traders to visualize how their positions align with natural market harmonics and divine proportions.

This dashboard combines traditional trading metrics with Fibonacci mathematics to identify natural market rhythms and maintain trading strategies that align with universal patterns.

## Core Concepts

### Golden Ratio and Trading

The Golden Ratio (Φ = 1.618...) appears throughout nature, art, architecture, and financial markets. In trading, Fibonacci retracement and extension levels are derived from the Golden Ratio sequence and are used to identify potential support, resistance, and price targets.

This dashboard elevates Fibonacci analysis from a simple technical indicator to a holistic trading philosophy, measuring how well your trading positions align with these natural harmonic patterns.

### Key Metrics

1. **Phi Resonance**: Measures how closely position sizing and entry points align with the Golden Ratio (1.618) and its derivatives
2. **Position Balance**: Analyzes the ratio between long and short positions, optimizing for the 0.618:1.000 ratio
3. **Entry Harmony**: Calculates how well entry prices align with key Fibonacci retracement levels
4. **Harmonic State**: Determines the overall market harmony based on PnL distribution and Fibonacci alignments

## Technical Implementation

### Architecture

The implementation consists of three main components:

1. **Backend Metrics Calculator (`fibonacci_bitget_metrics.py`)**:
   - Interfaces with BitGet API through existing trader classes
   - Calculates Fibonacci-based metrics from position data
   - Provides real-time analysis of position alignment with Golden Ratio

2. **API Server (`fibonacci_dashboard_server.py`)**:
   - FastAPI server exposing metrics through REST endpoints
   - Caching layer to limit API calls
   - WebSocket support for real-time updates

3. **Frontend Dashboard**:
   - Responsive HTML/CSS/JS interface
   - Visualizes position data with Fibonacci overlays
   - Updates metrics in real-time

### Calculation Methods

#### Phi Resonance Calculation

```python
def calculate_phi_resonance(long_positions, short_positions):
    # Default to 0.5 if no positions
    if not long_positions and not short_positions:
        return 0.5
        
    total_long_size = sum(float(pos.get('contracts', 0)) for pos in long_positions)
    total_short_size = sum(float(pos.get('contracts', 0)) for pos in short_positions)
    
    # If only one side has positions
    if total_long_size == 0 or total_short_size == 0:
        return 0.618  # Golden ratio as the baseline
        
    # Calculate ratio between long and short positions
    long_short_ratio = total_long_size / total_short_size
    
    # Calculate how close the ratio is to PHI (1.618) or its inverse (0.618)
    phi_alignment = min(
        abs(long_short_ratio - PHI) / PHI,
        abs(long_short_ratio - (1/PHI)) / (1/PHI)
    )
    
    # Normalize to a 0-1 scale where 1 is perfect alignment
    phi_resonance = max(0, 1 - phi_alignment)
    
    return round(phi_resonance, 3)
```

#### Fibonacci Level Generation

The dashboard generates Fibonacci retracement and extension levels for both long and short positions:

```python
# For long positions, calculate levels above and below entry
range_high = entry_price * 1.1  # 10% above entry
range_low = entry_price * 0.9   # 10% below entry

for level in FIBONACCI_LEVELS:
    if level <= 0.5:
        # Levels below entry (retracement)
        fib_levels[str(level)] = entry_price - ((entry_price - range_low) * level / 0.5)
    else:
        # Levels above entry (extension)
        normalized_level = (level - 0.5) / 0.5  # Normalize to 0-1 range
        fib_levels[str(level)] = entry_price + ((range_high - entry_price) * normalized_level)
```

### Key API Endpoints

The dashboard exposes several API endpoints:

1. `/api/bitget/fibonacci-metrics` - Returns all Fibonacci metrics and position data
2. `/api/bitget/position-history` - Returns historical position data
3. `/api/bitget/bio-energy` - Returns quantum bio-energy metrics (if using QuantumBitGetTrader)
4. `/api/status` - Returns API server status information

## User Interface Components

### 1. Position Metrics Panel

The Position Metrics Panel displays the core Fibonacci alignment metrics:

- **Φ Resonance**: Shows how closely position sizing aligns with the Golden Ratio
- **Position Balance**: Displays the long:short position ratio (ideally 0.618:1.000)
- **Entry Harmony**: Shows how well entry prices align with Fibonacci levels

### 2. Real-Time Position Status

This panel visualizes current positions with Fibonacci overlay:

- Separate cards for long and short positions
- Fibonacci retracement/extension levels from entry price
- PnL, liquidation price, and risk ratio information
- Visual indication of current price relative to Fibonacci levels

### 3. Golden Ratio Analytics

The analytics panel provides deeper insights:

- **Market Harmonics**: Visual scale showing market state from chaos to divine harmony
- **Quantum Resonance**: Bio-energy metrics if using QuantumBitGetTrader
- **Harmonic Flow**: Visualization of price movement relative to Fibonacci spirals

### 4. Historical Performance

Performance metrics with Fibonacci-aligned targets:

- Win Rate (target: 61.8%)
- Win/Loss Ratio (target: 1.618)
- Profit Factor (target: 2.618)
- Sharpe Ratio (target: 1.414 - square root of 2)

## Running the Dashboard

### Prerequisites

- BitGet API credentials (API key, secret key, passphrase)
- Python 3.8+
- Required packages: fastapi, uvicorn, ccxt, etc.

### Installation

1. Clone the repository or ensure the code is part of your OMEGA BTC AI project
2. Install required dependencies:

   ```
   pip install fastapi uvicorn python-dotenv ccxt
   ```

### Configuration

Set up environment variables with BitGet API credentials:

```
BITGET_API_KEY=your_api_key
BITGET_SECRET_KEY=your_secret_key
BITGET_PASSPHRASE=your_passphrase
```

For testnet:

```
BITGET_TESTNET_API_KEY=your_testnet_api_key
BITGET_TESTNET_SECRET_KEY=your_testnet_secret_key
BITGET_TESTNET_PASSPHRASE=your_testnet_passphrase
```

### Starting the Dashboard

Run the dashboard using the provided script:

```bash
python run_fibonacci_dashboard.py
```

For testnet:

```bash
python run_fibonacci_dashboard.py --testnet
```

Additional options:

```bash
python run_fibonacci_dashboard.py --host 127.0.0.1 --port 8080 --symbol ETHUSDT
```

### Accessing the Dashboard

Once started, access the dashboard in your browser:

```
http://localhost:8002
```

## Integration with Trading Strategy

The Fibonacci Dashboard can be used in several ways to enhance your trading:

1. **Position Sizing**: Adjust position sizes to match the Golden Ratio for optimal risk distribution
2. **Entry/Exit Points**: Use Fibonacci levels to determine precise entry and exit points
3. **Portfolio Balance**: Maintain long:short ratio near 0.618:1.000 for maximum harmony
4. **Risk Management**: Set stop loss and take profit orders at key Fibonacci levels

## Conclusion

The BitGet Fibonacci Golden Ratio Monitoring Dashboard transforms standard trading metrics into a harmonic system aligned with natural mathematical principles. By visualizing how closely your positions adhere to these divine proportions, you can achieve a trading strategy that flows with rather than against market rhythms.

By combining modern trading technology with ancient mathematical principles, this dashboard offers a unique perspective on market movements and position management that transcends traditional technical analysis.

## Resources

- [BitGet API Documentation](https://www.bitget.com/api-doc/contract/webapp-contract)
- [Fibonacci Trading Resources](https://www.investopedia.com/terms/f/fibonaccilines.asp)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
