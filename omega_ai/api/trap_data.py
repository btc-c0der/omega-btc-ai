"""
OMEGA BTC AI - Trap Data API
===========================

FastAPI endpoint for serving real-time trap data.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
import logging
import asyncio
from omega_ai.trading.exchanges.rasta_trap_monitor import RastaTrapMonitor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/trap",
    tags=["trap"],
    responses={404: {"description": "Not found"}},
)

# Initialize trap monitor
trap_monitor = RastaTrapMonitor(
    symbol="BTC-USDT-UMCBL",  # BitGet mainnet symbol format
    update_interval=5  # 5 second updates
)

# Track the background task
monitor_task = None

@router.get("/data")
async def get_trap_data() -> Dict[str, Any]:
    """Get current trap probability data."""
    try:
        if not hasattr(trap_monitor, 'trap_data'):
            return {
                'probability': 0,
                'type': 'Unknown',
                'trend': 'Neutral',
                'confidence': 0,
                'components': {},
                'timestamp': None
            }
        return trap_monitor.trap_data
    except Exception as e:
        logger.error(f"Error getting trap data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/start")
async def start_monitor(background_tasks: BackgroundTasks) -> Dict[str, str]:
    """Start the trap monitor in the background."""
    global monitor_task
    try:
        # Check if already running
        if monitor_task and not monitor_task.done():
            return {"status": "already_running"}
            
        # Create background task
        background_tasks.add_task(trap_monitor.start_monitor)
        
        return {"status": "started"}
    except Exception as e:
        logger.error(f"Error starting trap monitor: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stop")
async def stop_monitor() -> Dict[str, str]:
    """Stop the trap monitor."""
    try:
        await trap_monitor.stop()
        return {"status": "stopped"}
    except Exception as e:
        logger.error(f"Error stopping trap monitor: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 