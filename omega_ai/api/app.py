"""
OMEGA BTC AI - FastAPI Application
================================

Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging
from omega_ai.api.trap_data import router as trap_router, trap_monitor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="OMEGA BTC AI",
    description="Real-time BTC trading with trap detection",
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

# Mount static files
app.mount("/static", StaticFiles(directory="public"), name="static")

# Include routers
app.include_router(trap_router)

# Track background tasks
monitor_task = None

@app.on_event("startup")
async def startup_event():
    """Start the trap monitor on application startup."""
    global monitor_task
    try:
        logger.info("Starting trap monitor...")
        # Create a background task that won't block startup
        monitor_task = asyncio.create_task(trap_monitor.start_monitor())
        logger.info("Trap monitor started successfully")
    except Exception as e:
        logger.error(f"Error starting trap monitor: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Stop the trap monitor on application shutdown."""
    global monitor_task
    try:
        logger.info("Stopping trap monitor...")
        # First stop the monitor's internal loop
        await trap_monitor.stop()
        
        # Then cancel the task if it exists and is still running
        if monitor_task and not monitor_task.done():
            monitor_task.cancel()
            try:
                await monitor_task
            except asyncio.CancelledError:
                pass
            
        logger.info("Trap monitor stopped successfully")
    except Exception as e:
        logger.error(f"Error stopping trap monitor: {str(e)}")
        raise

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "OMEGA BTC AI",
        "version": "1.0.0",
        "status": "running"
    } 