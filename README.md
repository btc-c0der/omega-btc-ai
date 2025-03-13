# **OMEGA BTC AI - Advanced Bitcoin Trading & Analysis System**

## **🚀 System Overview**
The **Omega BTC AI** is an advanced cryptocurrency analysis and trading system that:
- Monitors real-time **Bitcoin price movements** across multiple timeframes (1min, 3min, 5min, 15min, 1hr, 4hr)
- Detects **market maker (MM) manipulation tactics** including liquidity grabs, stop hunts, and fake price movements
- Implements **automated trading strategies** with customizable risk parameters and trader profiles
- Integrates **Schumann Resonance electromagnetic data** for enhanced pattern recognition
- Provides dynamic threshold adjustment based on market volatility
- Implements a unique **High-Frequency Trap Mode** for detecting rapid manipulation
- Simulates different **trader psychological profiles** for strategy optimization
- Alerts traders to potential manipulation events in real-time

This system combines statistical analysis, pattern recognition, algorithmic trading, and electromagnetic correlations to identify market opportunities and manipulation with high confidence.

---

## **🧪 Scientific Foundation**

### **Market Maker Manipulation Detection**
- **Price Movement Pattern Analysis**: Identifies characteristic patterns in price movements that correlate with known MM tactics
- **Multi-timeframe Correlation**: Analyzes relationships between short and medium timeframes to detect manipulation
- **Dynamic Volatility Normalization**: Automatically adjusts sensitivity based on current market conditions
- **Fibonacci-Organic Analysis**: Distinguishes between natural market movements and artificial manipulations

### **Trading Strategy Implementation**
- **Multi-timeframe Trend Analysis**: Combines insights from 6+ timeframes for directional bias
- **Fibonacci Entry & Exit Levels**: Uses Fibonacci retracement and extension for key price levels
- **Volume Acceleration Detection**: Identifies early trend moves before significant price action
- **Risk Management Optimization**: Dynamic position sizing and profit targeting based on market conditions

### **Trader Psychology Modeling**
- **Emotional State Simulation**: Models how emotions affect trading decisions 
- **Confidence & Risk Appetite Dynamics**: Simulates changing risk tolerance after wins/losses
- **Discipline Metrics**: Tracks rule adherence, patience, and emotional resilience
- **Performance Analytics**: Measures how psychological factors impact trading outcomes

### **Schumann Resonance Integration**
- **Earth's Electromagnetic Field Monitoring**: Tracks the 7.83Hz (and related) resonances of Earth's electromagnetic field
- **Correlation Analysis**: Examines relationships between electromagnetic anomalies and market movements
- **Pattern Recognition**: Identifies when Schumann spikes coincide with price manipulations
- **Signal Processing**: Filters noise from the Schumann data for cleaner analysis

### **High-Frequency Detection Mechanics**
- **Rapid Pattern Recognition**: Identifies manipulation tactics occurring in timeframes as short as 1-10 minutes
- **Back-to-Back Event Detection**: Recognizes compound manipulation strategies (multiple traps in sequence)
- **Price Acceleration Metrics**: Measures the rate of change in price movements to detect unusual activity
- **Adaptive Thresholds**: Dynamically adjusts detection sensitivity based on current market conditions

---

## **🔥 System Components**
| Component | Purpose | Functional Area |
|-----------|---------|-----------------|
| `btc_feed.py` | Fetches BTC price from Binance and sends to WebSocket & DB | Data Acquisition |
| `mm_websocket_server.py` | Runs the WebSocket server for broadcasting price updates | Data Distribution |
| `mm_trap_processor.py` | Detects MM traps using dynamic thresholds and Fibonacci patterns | Market Analysis |
| `high_frequency_detector.py` | Specialized detector for rapid market manipulations | Market Analysis |
| `trading_analyzer.py` | Analyzes market conditions for trading opportunities | Trading Strategy |
| `btc_futures_trader.py` | Simulates futures trading with risk management | Trading Execution |
| `profiled_futures_trader.py` | Integrates trading profiles with futures trading | Trading Psychology |
| `trader_profiles.py` | Simulates different trader psychology profiles | Trading Psychology |
| `schumann_monitor.py` | Monitors Earth's electromagnetic resonances | Data Analysis |
| `monitor_market_trends.py` | Analyzes multi-timeframe market structure | Market Context |
| `mm_trap_analyzer.py` | Processes detected trap events for patterns | Pattern Recognition |
| `PostgreSQL Database` | Stores BTC prices, MM trap records, and trade history | Data Storage |
| `Redis Cache` | Provides fast access to real-time metrics | In-memory Cache |

---

## **🔍 Core Detection Features**

### **1. Market Maker Trap Detection**
- Liquidity Blocks ($450-$550 price movements)
- Stop Hunts (rapid price spikes followed by reversals)
- Fake Pumps/Dumps (manipulated directional moves)
- Liquidity Accumulation (consecutive small moves in same direction)
- Trend Reversals (price moving against established trend)

### **2. High-Frequency Trap Mode**
Activates when:
- 1min or 5min price change exceeds 0.5% in absolute value
- Rapid back-to-back fake pumps/dumps occur within a short window
- Schumann Resonance spikes above 12Hz while a major price move happens

### **3. Schumann Resonance Correlation**
- Tracks electromagnetic resonances between 7-15Hz
- Identifies anomalies in Earth's electromagnetic field
- Correlates these anomalies with Bitcoin price movements
- Provides additional confirmation of potential manipulation

---

## **📈 Trading Strategy & Psychology**

### **1. Trading Analysis Components**
- **Short Timeframe Analysis**: Enhanced sensitivity to 1m, 3m, and 5m alignments
- **Volume Acceleration Detection**: Identifies early breakouts through volume spikes
- **Market Regime Adaptation**: Adjusts strategy for trending vs. ranging markets
- **Fibonacci Entry Detection**: Identifies key retracement and extension levels for entries
- **Real-time Score Component Analysis**: Detailed breakdown of signal components

### **2. Trader Profile Simulation**
The system simulates different trader personalities to optimize strategies:

#### **Aggressive Momentum Trader**
- Uses high leverage (10x-20x)
- Enters based on momentum indicators and volume spikes
- Implements tight stop-losses (1%)
- Targets 1:1 risk-reward for first targets
- Highly susceptible to emotional trading (FOMO, revenge trading)
- Often overestimates trend strength

#### **Strategic Fibonacci Trader**
- Uses moderate leverage (3x-5x)
- Enters only on confirmed Fibonacci level retests
- Uses wider stop-losses (3%)
- Targets 1:2 risk-reward for first targets
- More disciplined approach with higher patience metrics
- Less prone to emotional decision-making

#### **Newbie YOLO Trader**
- Uses excessive leverage (20x-50x)
- Enters based on social media influence and FOMO
- Inconsistent or missing stop-losses
- No clear take-profit strategy
- Highly emotional decision-making
- Prone to revenge trading after losses

#### **Scalper Trader**
- Uses higher leverage (10x-15x)
- Focuses on order book imbalances
- Uses ultra-tight stop-losses (0.5%)
- Quick profit targets (0.5-1%)
- Low patience, high trade frequency
- Technical rather than emotional approach

### **3. Psychological Modeling**
The system models emotional states and their impact on trading:
- Neutral → Greedy → Neutral → Fearful → Neutral (Psychological cycle)
- Confidence levels (0.1-1.0) affecting position sizing
- Risk appetite dynamics following wins and losses
- Discipline metrics measuring rule adherence and patience

### **4. ProfiledFuturesTrader**
The ProfiledFuturesTrader combines the sophisticated market analysis of BtcFuturesTrader with the behavioral modeling of trader profiles:
- Applies trader psychology to real market conditions
- Modifies decision-making based on profile characteristics
- Tracks emotional state and its impact on trading decisions
- Allows comparative analysis of different trader types on the same market

---

## **🔧 Setup & Installation**

### **Prerequisites**
- Python 3.8+
- PostgreSQL 12+
- Redis 6+
- Node.js 18+ (for web dashboard)

### **Installation Steps**
1. Clone the repository:
```bash
git clone https://github.com/yourusername/omega_btc_ai.git
cd omega_btc_ai

---

## **🩺 Health Check System**

The OmegaBTC AI Trading System includes a robust health check mechanism to ensure the reliability and stability of the BTC live feed and associated components.

### **Features**
- Monitors the BTC live feed process
- Checks Redis data integrity
- Sends email alerts for various error conditions
- Includes a test mode for verifying the alerting system

### **Running the Health Check**
The health check script runs automatically as part of the system startup process. To manually run the health check:

```bash
python health_check.py
```

### **Test Mode**
To test the alerting system without affecting the production environment:

```bash
python health_check.py --test
```

This will simulate a healthy status and send a test alert.

### **Responding to Alerts**
If you receive an alert email, follow these steps:

1. Check the BTC live feed process status
2. Verify Redis connectivity and data integrity
3. Review system logs for any error messages
4. Restart the BTC live feed process if necessary
5. Contact the development team if the issue persists

### **Maintenance**
- Regularly review and update the email configuration in the health check script
- Set up log rotation for the health check script to manage log file sizes
- Periodically test the alerting system using the test mode

For any questions or issues related to the health check system, please contact the system administrator.