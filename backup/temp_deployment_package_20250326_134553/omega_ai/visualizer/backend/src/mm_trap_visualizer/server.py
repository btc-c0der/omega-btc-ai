
# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸

"""Market Maker Trap Visualizer Server."""

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import json
import logging
import asyncio

class MMTrapVisualizerServer:
    """Server for visualizing market maker traps."""
    
    def __init__(self, title: str, redis_manager):
        """Initialize the server."""
        self.title = title
        self.redis_manager = redis_manager
        self.app = FastAPI(title=title)
        self.active_connections: List[WebSocket] = []
        
        # Setup CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Mount static files
        static_dir = Path(__file__).parent.parent / "static"
        if static_dir.exists():
            self.app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
        
        # Setup routes
        self.setup_routes()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def setup_routes(self):
        """Setup API routes."""
        @self.app.get("/")
        async def root():
            """Root endpoint."""
            return {"title": self.title, "status": "running"}
        
        @self.app.get("/api/traps")
        async def get_traps():
            """Get all traps from Redis."""
            try:
                data = self.redis_manager.get_cached()
                return JSONResponse(content=data)
            except Exception as e:
                self.logger.error(f"Error getting traps: {e}")
                return JSONResponse(
                    status_code=500,
                    content={"error": "Failed to get traps"}
                )
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time updates."""
            await websocket.accept()
            self.active_connections.append(websocket)
            try:
                while True:
                    data = await websocket.receive_text()
                    # Broadcast to all connected clients
                    for connection in self.active_connections:
                        await connection.send_text(data)
            except Exception as e:
                self.logger.error(f"WebSocket error: {e}")
            finally:
                self.active_connections.remove(websocket)
    
    async def broadcast_trap(self, trap_data: Dict[str, Any]):
        """Broadcast trap data to all connected clients."""
        for connection in self.active_connections:
            try:
                await connection.send_json(trap_data)
            except Exception as e:
                self.logger.error(f"Error broadcasting trap: {e}")
                self.active_connections.remove(connection)

 