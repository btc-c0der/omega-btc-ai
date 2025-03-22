"""
OMEGA BTC AI - Trap Data API
===========================

FastAPI endpoint for serving real-time trap data.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging
from omega_ai.trading.exchanges.rasta_trap_monitor import RastaTrapMonitor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Initialize trap monitor
trap_monitor = RastaTrapMonitor(
    symbol="BTC/USDT:USDT",
    update_interval=5.0,
    use_testnet=True
)

@router.get("/api/trap-data")
async def get_trap_data() -> Dict[str, Any]:
    """Get latest trap data."""
    try:
        # Return current trap data
        return trap_monitor.trap_data
        
    except Exception as e:
        logger.error(f"Error getting trap data: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get trap data"
        ) 