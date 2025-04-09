"""Main application entry point for the trap visualizer server."""

import uvicorn
from omega_ai.utils.redis_manager import RedisManager
from omega_ai.visualizer.backend.unified_server import TrapVisualizerServer

def main():
    """Initialize and run the trap visualizer server."""
    # Initialize Redis manager
    redis_manager = RedisManager()
    
    # Create server instance
    server = TrapVisualizerServer(
        name="OMEGA BTC AI Trap Visualizer",
        redis_manager=redis_manager
    )
    
    # Run the server
    uvicorn.run(
        server.app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

if __name__ == "__main__":
    main() 