
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


# BitGet Fibonacci Dashboard API Architecture

## Overview

The BitGet Fibonacci Golden Ratio Dashboard provides a real-time monitoring system built on a modern API-driven architecture. This document details the API design, endpoints, and implementation approach to deliver Fibonacci-based trading metrics.

## System Architecture

### High-Level Architecture

The system follows a layered architecture with clear separation of concerns:

```
┌─────────────────────────┐
│  Frontend Dashboard     │
│  (HTML/CSS/JavaScript)  │
└───────────┬─────────────┘
            │ HTTP/WebSocket
┌───────────▼─────────────┐
│  FastAPI Server         │
│  (API Endpoints)        │
└───────────┬─────────────┘
            │ Python
┌───────────▼─────────────┐
│  Metrics Calculator     │
│  (Fibonacci Analytics)  │
└───────────┬─────────────┘
            │ CCXT
┌───────────▼─────────────┐
│  BitGet Exchange API    │
│  (Position Data)        │
└─────────────────────────┘
```

### Components

1. **FastAPI Server**: Core API server that exposes endpoints for the dashboard
2. **Metrics Calculator**: Python module for Fibonacci calculations
3. **BitGet Integration**: CCXT-based interaction with BitGet exchange API
4. **Caching Layer**: Reduces API call frequency to BitGet
5. **WebSocket Support**: Enables real-time updates for the dashboard

## API Endpoints

The API is built using FastAPI and exposes the following RESTful endpoints:

### Status Endpoints

#### `GET /api/status`

Returns the current status of the API and calculator.

**Response Schema:**

```json
{
  "status": "online",
  "calculator_initialized": true,
  "uptime_seconds": 3600,
  "version": "1.0.0"
}
```

### Fibonacci Metrics Endpoints

#### `GET /api/bitget/fibonacci-metrics`

Returns the complete set of Fibonacci metrics for current positions.

**Query Parameters:**

- `refresh` (boolean, optional): Force refresh of the cache

**Response Schema:**

```json
{
  "timestamp": "2023-07-15T12:34:56Z",
  "phi_resonance": 0.782,
  "position_balance": {
    "ratio_type": "long:short",
    "optimal_value": 0.618,
    "current_ratio": 0.587,
    "balance_score": 0.915
  },
  "harmonic_state": {
    "harmony_score": 0.76,
    "state": "Balanced Flow",
    "component_scores": {
      "position_harmony": 0.782,
      "win_rate_harmony": 0.853,
      "profit_factor_harmony": 0.624,
      "pnl_distribution_harmony": 0.789
    }
  },
  "positions": {
    "long": [
      {
        "symbol": "BTCUSDT",
        "contracts": 0.5,
        "entry_price": 45000.0,
        "current_price": 47200.0,
        "unrealized_pnl": 1100.0,
        "entry_harmony": 0.92,
        "fibonacci_levels": {
          "0.0": 45000.0,
          "0.236": 44118.0,
          "0.382": 43582.0,
          "0.5": 43150.0,
          "0.618": 42718.0,
          "0.786": 42132.0,
          "1.0": 41300.0,
          "1.618": 47200.0,
          "2.618": 50800.0,
          "4.236": 56390.0
        }
      }
    ],
    "short": [
      {
        "symbol": "ETHUSDT",
        "contracts": 4.0,
        "entry_price": 3200.0,
        "current_price": 3100.0,
        "unrealized_pnl": 400.0,
        "entry_harmony": 0.78,
        "fibonacci_levels": {
          "0.0": 3200.0,
          "0.236": 3248.0,
          "0.382": 3328.0,
          "0.5": 3360.0,
          "0.618": 3392.0,
          "0.786": 3437.0,
          "1.0": 3520.0,
          "1.618": 3000.0,
          "2.618": 2800.0,
          "4.236": 2500.0
        }
      }
    ]
  },
  "performance": {
    "win_rate": 0.623,
    "win_rate_target": 0.618,
    "win_rate_alignment": 0.992,
    "profit_factor": 2.347,
    "profit_factor_target": 2.618,
    "profit_factor_alignment": 0.896,
    "phi_resonance": 0.782,
    "fibonacci_alignment": 0.944
  }
}
```

### Position History Endpoints

#### `GET /api/bitget/position-history`

Returns the history of closed positions.

**Query Parameters:**

- `limit` (integer, optional): Number of positions to return (default: 20)
- `offset` (integer, optional): Offset for pagination (default: 0)

**Response Schema:**

```json
{
  "count": 42,
  "positions": [
    {
      "id": "123456",
      "symbol": "BTCUSDT",
      "side": "long",
      "entry_price": 42000.0,
      "exit_price": 45000.0,
      "contracts": 1.0,
      "realized_pnl": 3000.0,
      "entry_time": "2023-07-10T15:30:00Z",
      "exit_time": "2023-07-12T09:45:00Z",
      "entry_harmony": 0.88,
      "exit_harmony": 0.76,
      "fibonacci_alignment": 0.82
    },
    {
      "id": "123457",
      "symbol": "ETHUSDT",
      "side": "short",
      "entry_price": 3400.0,
      "exit_price": 3200.0,
      "contracts": 5.0,
      "realized_pnl": 1000.0,
      "entry_time": "2023-07-11T08:15:00Z",
      "exit_time": "2023-07-12T14:20:00Z",
      "entry_harmony": 0.91,
      "exit_harmony": 0.84,
      "fibonacci_alignment": 0.88
    }
  ]
}
```

#### `POST /api/bitget/history/add`

Adds a closed position to the history.

**Request Body:**

```json
{
  "symbol": "BTCUSDT",
  "side": "long",
  "entry_price": 42000.0,
  "exit_price": 45000.0,
  "contracts": 1.0,
  "entry_time": "2023-07-10T15:30:00Z",
  "exit_time": "2023-07-12T09:45:00Z"
}
```

**Response Schema:**

```json
{
  "success": true,
  "id": "123458",
  "message": "Position added to history"
}
```

### Bio-Energy Endpoints

#### `GET /api/bitget/bio-energy`

Returns quantum bio-energy metrics (when using QuantumBitGetTrader).

**Response Schema:**

```json
{
  "market_energy": 7.8,
  "position_energy": 8.2,
  "combined_energy": 8.0,
  "energy_state": "Harmonic Resonance",
  "fib_alignment": 0.92
}
```

## API Implementation

### FastAPI Server Implementation

The API server is implemented using FastAPI, a modern, fast web framework for building APIs with Python:

```python
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging
import time
import os
import json
import asyncio

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("fibonacci-dashboard-api")

# Initialize FastAPI app
app = FastAPI(
    title="BitGet Fibonacci Golden Ratio Dashboard API",
    description="API for Fibonacci-based trading metrics on BitGet positions",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache for metrics to limit API calls
metrics_cache = {
    "last_update": 0,
    "data": None,
    "ttl": 60  # Cache TTL in seconds
}

# Global calculator instance
calculator = None

# Initialize the calculator
def initialize_calculator():
    global calculator
    
    try:
        from omega_ai.trading.analytics.fibonacci_bitget_metrics import FibonacciMetricsCalculator
        
        # Get API credentials from environment
        api_key = os.environ.get("BITGET_API_KEY")
        secret_key = os.environ.get("BITGET_SECRET_KEY")
        passphrase = os.environ.get("BITGET_PASSPHRASE")
        
        if not all([api_key, secret_key, passphrase]):
            logger.error("Missing BitGet API credentials")
            return False
        
        # Create calculator instance
        calculator = FibonacciMetricsCalculator(
            api_key=api_key,
            secret_key=secret_key,
            passphrase=passphrase
        )
        
        logger.info("FibonacciMetricsCalculator initialized successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to initialize calculator: {str(e)}")
        return False

# Models for API responses
class BioEnergyModel(BaseModel):
    market_energy: float
    position_energy: float
    combined_energy: float
    energy_state: str
    fib_alignment: float

class PositionModel(BaseModel):
    symbol: str
    contracts: float
    entry_price: float
    current_price: float
    unrealized_pnl: float
    entry_harmony: float
    fibonacci_levels: Dict[str, float]

class PositionBalanceModel(BaseModel):
    ratio_type: str
    optimal_value: float
    current_ratio: float
    balance_score: float

class PnlModel(BaseModel):
    realized_pnl: float
    unrealized_pnl: float
    total_pnl: float
    daily_pnl: float

class PerformanceModel(BaseModel):
    win_rate: float
    win_rate_target: float
    win_rate_alignment: float
    profit_factor: float
    profit_factor_target: float
    profit_factor_alignment: float
    phi_resonance: float
    fibonacci_alignment: float

class FibonacciMetricsModel(BaseModel):
    timestamp: str
    phi_resonance: float
    position_balance: PositionBalanceModel
    harmonic_state: Dict
    positions: Dict[str, List[PositionModel]]
    performance: PerformanceModel

class PositionHistoryModel(BaseModel):
    id: str
    symbol: str
    side: str
    entry_price: float
    exit_price: float
    contracts: float
    realized_pnl: float
    entry_time: str
    exit_time: str
    entry_harmony: float
    exit_harmony: float
    fibonacci_alignment: float

# API Endpoints
@app.get("/api/status")
async def get_status():
    """Get the API server status"""
    return {
        "status": "online",
        "calculator_initialized": calculator is not None,
        "uptime_seconds": int(time.time() - app.state.start_time),
        "version": "1.0.0"
    }

@app.get("/api/bitget/fibonacci-metrics", response_model=FibonacciMetricsModel)
async def get_fibonacci_metrics(refresh: bool = False):
    """Get Fibonacci metrics for current positions"""
    global metrics_cache
    
    # Check if calculator is initialized
    if calculator is None:
        if not initialize_calculator():
            raise HTTPException(status_code=500, detail="Calculator not initialized")
    
    current_time = time.time()
    
    # Return cached data if available and not expired
    if not refresh and metrics_cache["data"] is not None:
        if current_time - metrics_cache["last_update"] < metrics_cache["ttl"]:
            return metrics_cache["data"]
    
    try:
        # Get fresh data from calculator
        metrics = await asyncio.to_thread(calculator.get_fibonacci_metrics)
        
        # Update cache
        metrics_cache["data"] = metrics
        metrics_cache["last_update"] = current_time
        
        return metrics
    
    except Exception as e:
        logger.error(f"Error getting Fibonacci metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve metrics: {str(e)}")

@app.get("/api/bitget/position-history")
async def get_position_history(limit: int = 20, offset: int = 0):
    """Get position history"""
    # Check if calculator is initialized
    if calculator is None:
        if not initialize_calculator():
            raise HTTPException(status_code=500, detail="Calculator not initialized")
    
    try:
        history = await asyncio.to_thread(calculator.get_position_history, limit, offset)
        return history
    
    except Exception as e:
        logger.error(f"Error getting position history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve position history: {str(e)}")

@app.get("/api/bitget/bio-energy", response_model=BioEnergyModel)
async def get_bio_energy():
    """Get bio-energy metrics"""
    # Check if calculator is initialized
    if calculator is None:
        if not initialize_calculator():
            raise HTTPException(status_code=500, detail="Calculator not initialized")
    
    try:
        bio_energy = await asyncio.to_thread(calculator.get_bio_energy_metrics)
        return bio_energy
    
    except Exception as e:
        logger.error(f"Error getting bio-energy metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve bio-energy metrics: {str(e)}")

class PositionHistoryAddModel(BaseModel):
    symbol: str
    side: str
    entry_price: float
    exit_price: float
    contracts: float
    entry_time: str
    exit_time: str

@app.post("/api/bitget/history/add")
async def add_position_history(position: PositionHistoryAddModel):
    """Add a closed position to history"""
    # Check if calculator is initialized
    if calculator is None:
        if not initialize_calculator():
            raise HTTPException(status_code=500, detail="Calculator not initialized")
    
    try:
        result = await asyncio.to_thread(calculator.add_position_to_history, position.dict())
        return result
    
    except Exception as e:
        logger.error(f"Error adding position to history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to add position to history: {str(e)}")

# Serve static files for the dashboard
from fastapi.staticfiles import StaticFiles
import os

dashboard_path = os.path.join(os.path.dirname(__file__), "static", "dashboard")
if os.path.exists(dashboard_path):
    app.mount("/dashboard", StaticFiles(directory=dashboard_path, html=True), name="dashboard")

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    app.state.start_time = time.time()
    initialize_calculator()

def start_server(host="0.0.0.0", port=8002):
    """Start the FastAPI server"""
    import uvicorn
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_server()
```

### Caching Strategy

The API implements a simple time-based caching strategy to minimize calls to the BitGet API:

1. **Cache TTL**: Default cache lifetime is 60 seconds
2. **Force Refresh**: Clients can bypass cache with the `refresh=true` parameter
3. **Background Updates**: Non-blocking updates using `asyncio.to_thread`

### Error Handling

The API implements comprehensive error handling:

1. **Graceful Degradation**: Falls back to synthetic data when certain features are unavailable
2. **Detailed Error Responses**: HTTP exceptions with descriptive messages
3. **Logging**: Structured logging for debugging and monitoring
4. **Exception Handling**: Try-except blocks with specific error types

## Data Models

The API uses Pydantic models for request and response validation:

### Core Models

1. **FibonacciMetricsModel**: Complete metrics payload
2. **PositionModel**: Individual position data with Fibonacci levels
3. **PerformanceModel**: Trading performance statistics
4. **BioEnergyModel**: Quantum bio-energy metrics

### Request Models

1. **PositionHistoryAddModel**: Schema for adding historical positions

## Security Considerations

The API implements several security measures:

1. **Environment Variables**: API credentials stored as environment variables
2. **CORS Middleware**: Configured to allow cross-origin requests as needed
3. **Rate Limiting**: (Recommended addition) Add rate limiting for public endpoints
4. **Authentication**: (Recommended addition) Add API key authentication for write operations

## Deployment Configuration

### Docker Deployment

The API can be containerized for easy deployment:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run_fibonacci_dashboard.py"]
```

### Environment Variables

The following environment variables are required:

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

## API Usage Examples

### cURL Examples

#### Get Fibonacci Metrics

```bash
curl -X GET "http://localhost:8002/api/bitget/fibonacci-metrics"
```

#### Get Position History

```bash
curl -X GET "http://localhost:8002/api/bitget/position-history?limit=5"
```

#### Add Position to History

```bash
curl -X POST "http://localhost:8002/api/bitget/history/add" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTCUSDT",
    "side": "long",
    "entry_price": 42000.0,
    "exit_price": 45000.0,
    "contracts": 1.0,
    "entry_time": "2023-07-10T15:30:00Z",
    "exit_time": "2023-07-12T09:45:00Z"
  }'
```

### JavaScript Examples

#### Fetch Metrics and Update Dashboard

```javascript
async function updateDashboard() {
  try {
    const response = await fetch('http://localhost:8002/api/bitget/fibonacci-metrics');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    // Update dashboard elements
    document.getElementById('phi-resonance').textContent = data.phi_resonance;
    document.getElementById('harmony-state').textContent = data.harmonic_state.state;
    
    // Update position tables
    updatePositionTable(data.positions.long, 'long-positions-table');
    updatePositionTable(data.positions.short, 'short-positions-table');
    
    // Update performance metrics
    updatePerformanceMetrics(data.performance);
    
  } catch (error) {
    console.error('Error updating dashboard:', error);
  }
}

// Refresh every 60 seconds
setInterval(updateDashboard, 60000);

// Initial update
updateDashboard();
```

## Future Enhancements

Planned future enhancements for the API:

1. **WebSocket Support**: Real-time updates for position changes
2. **Historical Data Analysis**: Expanded endpoints for historical pattern analysis
3. **Machine Learning Integration**: Predictive analytics based on Fibonacci patterns
4. **Advanced Authentication**: OAuth2 or API key-based authentication
5. **Rate Limiting**: Protection against abuse and excessive API calls

## Conclusion

The BitGet Fibonacci Dashboard API provides a robust, scalable foundation for accessing Fibonacci-based trading metrics. The API is designed to be extensible, allowing for future enhancements while maintaining backward compatibility with existing clients.

By following modern API design principles and leveraging FastAPI's performance benefits, the system delivers real-time insights into trading positions with minimal latency, enabling traders to make informed decisions based on Fibonacci Golden Ratio principles.
