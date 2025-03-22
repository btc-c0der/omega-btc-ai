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
    description="Rasta-inspired BTC trading AI",
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

@app.on_event("startup")
async def startup_event():
    """Start background tasks on app startup."""
    # Start trap monitor
    asyncio.create_task(trap_monitor.start())
    logger.info("Started trap monitor") 