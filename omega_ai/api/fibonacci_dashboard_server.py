"""
OMEGA BTC AI - Fibonacci Dashboard API Server
==========================================

This module implements a FastAPI server for the BitGet Fibonacci Golden Ratio
monitoring dashboard.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import os
import json
import logging
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

from omega_ai.trading.analytics.fibonacci_bitget_metrics import get_calculator_instance, FibonacciMetricsCalculator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="BitGet Fibonacci Dashboard API",
    description="API for BitGet Fibonacci Golden Ratio monitoring dashboard",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Response models
class BioEnergyModel(BaseModel):
    state: str
    fibonacci_resonance: float
    quantum_frequency: float
    emotional_balance: float
    last_update: str

class PositionModel(BaseModel):
    has_position: bool
    size: float = 0.0
    entry_price: float = 0.0
    current_price: float = 0.0
    liquidation_price: float = 0.0
    unrealized_pnl: float = 0.0
    pnl_percentage: float = 0.0
    leverage: int = 0
    margin: float = 0.0
    fibonacci_levels: Dict[str, float] = {}
    error: Optional[str] = None

class PositionBalanceModel(BaseModel):
    long: float
    short: float
    display: str

class PnlModel(BaseModel):
    long: float
    short: float
    total: float

class PerformanceModel(BaseModel):
    win_rate: float
    avg_win_loss: float
    profit_factor: float
    sharpe_ratio: float

class FibonacciMetricsModel(BaseModel):
    timestamp: str
    symbol: str
    current_price: float
    phi_resonance: float
    position_balance: PositionBalanceModel
    entry_harmony: float
    harmonic_state: str
    harmonic_value: float
    long_position: PositionModel
    short_position: PositionModel
    pnl: PnlModel
    bio_energy: Optional[BioEnergyModel] = None
    performance: PerformanceModel
    error: Optional[str] = None

class PositionHistoryModel(BaseModel):
    direction: str
    entry_price: float
    exit_price: float
    size: float
    pnl: float
    entry_time: str
    exit_time: str
    fib_alignment: float

# Global metrics cache to limit API calls
metrics_cache = {
    "last_update": None,
    "data": None
}

# Initialize the calculator
calculator_instance = None

async def initialize_calculator():
    """Initialize the Fibonacci metrics calculator."""
    global calculator_instance
    
    # Get API credentials from environment
    api_key = os.environ.get("BITGET_API_KEY", "")
    secret_key = os.environ.get("BITGET_SECRET_KEY", "")
    passphrase = os.environ.get("BITGET_PASSPHRASE", "")
    use_testnet = os.environ.get("BITGET_USE_TESTNET", "False").lower() == "true"
    symbol = os.environ.get("BITGET_SYMBOL", "BTCUSDT")
    
    # Create calculator
    calculator_instance = await get_calculator_instance(
        api_key=api_key,
        secret_key=secret_key,
        passphrase=passphrase,
        use_testnet=use_testnet,
        symbol=symbol
    )
    
    logger.info(f"Fibonacci metrics calculator initialized for {symbol}")

@app.on_event("startup")
async def startup_event():
    """Run on server startup."""
    await initialize_calculator()

@app.get("/api/status")
async def get_status():
    """Get API status."""
    return {
        "status": "online",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "calculator_initialized": calculator_instance is not None
    }

@app.get("/api/bitget/fibonacci-metrics", response_model=FibonacciMetricsModel)
async def get_fibonacci_metrics(
    refresh: bool = Query(False, description="Force refresh metrics cache")
):
    """
    Get Fibonacci metrics for BitGet positions.
    
    Args:
        refresh: Whether to force a refresh of cached metrics
    
    Returns:
        FibonacciMetricsModel: Fibonacci metrics
    """
    global metrics_cache
    
    try:
        # Check if we need to refresh metrics
        now = datetime.now(timezone.utc)
        
        if (metrics_cache["last_update"] is None or 
            refresh or 
            (now - metrics_cache["last_update"]).total_seconds() > 5):
            
            # Get fresh metrics
            metrics = await calculator_instance.get_fibonacci_metrics()
            
            # Update cache
            metrics_cache["last_update"] = now
            metrics_cache["data"] = metrics
            logger.debug("Refreshed Fibonacci metrics")
        else:
            # Use cached metrics
            metrics = metrics_cache["data"]
            logger.debug("Using cached Fibonacci metrics")
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error getting Fibonacci metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/bitget/position-history", response_model=List[PositionHistoryModel])
async def get_position_history():
    """
    Get position history.
    
    Returns:
        List[PositionHistoryModel]: Position history
    """
    try:
        history = await calculator_instance.get_position_history()
        return history
        
    except Exception as e:
        logger.error(f"Error getting position history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/bitget/bio-energy")
async def get_bio_energy():
    """
    Get bio-energy metrics.
    
    Returns:
        Dict: Bio-energy metrics
    """
    try:
        bio_energy = calculator_instance.get_bio_energy_metrics()
        
        if bio_energy:
            return bio_energy
        else:
            return {"error": "Bio-energy metrics not available"}
        
    except Exception as e:
        logger.error(f"Error getting bio-energy metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/bitget/history/add")
async def add_position_to_history(position: dict):
    """
    Add a closed position to history.
    
    Args:
        position: Position data
        
    Returns:
        Dict: Success message
    """
    try:
        await calculator_instance.add_position_to_history(position)
        return {"status": "success", "message": "Position added to history"}
        
    except Exception as e:
        logger.error(f"Error adding position to history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Serve static files
try:
    dashboard_path = os.path.join(os.path.dirname(__file__), "../../visualizer/frontend/fibonacci-dashboard")
    if os.path.exists(dashboard_path):
        app.mount("/", StaticFiles(directory=dashboard_path, html=True), name="dashboard")
        logger.info(f"Mounted dashboard static files from {dashboard_path}")
except Exception as e:
    logger.error(f"Error mounting static files: {str(e)}")

def start_server(host="0.0.0.0", port=8002):
    """
    Start the FastAPI server.
    
    Args:
        host: Server host
        port: Server port
    """
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_server() 