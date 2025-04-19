
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

"""
Base server class for OMEGA BTC AI visualization servers.
Implements common functionality and interfaces for all visualization servers.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import json
from datetime import datetime, timedelta
from omega_ai.utils.redis_manager import RedisManager

class BaseVisualizationServer(ABC):
    """Base class for all visualization servers."""
    
    def __init__(self, title: str, redis_manager: RedisManager):
        """Initialize the base server.
        
        Args:
            title: The title of the server
            redis_manager: Redis manager instance for data access
        """
        self.app = FastAPI(title=title)
        self.redis_manager = redis_manager
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Configure CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # In production, replace with specific origins
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Register routes
        self.register_routes()
    
    @abstractmethod
    def register_routes(self) -> None:
        """Register all routes for the server. Must be implemented by subclasses."""
        pass
    
    def load_latest_dump(self) -> Dict[str, Any]:
        """Load the most recent dump with integrity verification.
        
        Returns:
            Dict containing the latest dump data
            
        Raises:
            HTTPException: If data cannot be loaded or is invalid
        """
        try:
            data = self.redis_manager.get_cached("omega:latest_dump")
            if not data:
                self.logger.error("❌ No dump data found!")
                raise HTTPException(status_code=404, detail="No dump data found")
            
            if isinstance(data, dict):
                return data
                
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                self.logger.error("❌ Invalid JSON data detected!")
                raise HTTPException(status_code=500, detail="Corrupted dump data")
                
        except Exception as e:
            self.logger.error(f"❌ Error loading dump: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    def parse_schumann_value(self, schumann_raw: Any) -> float:
        """Parse Schumann resonance value from raw data.
        
        Args:
            schumann_raw: Raw Schumann resonance data
            
        Returns:
            float: Parsed Schumann resonance value
        """
        default_value = 7.83  # Base Schumann frequency
        
        if not schumann_raw:
            return default_value
            
        try:
            if isinstance(schumann_raw, str):
                try:
                    return float(json.loads(schumann_raw))
                except json.JSONDecodeError:
                    return float(schumann_raw)
            elif isinstance(schumann_raw, dict):
                return float(schumann_raw.get("value", default_value))
            else:
                return float(schumann_raw)
        except (ValueError, TypeError, AttributeError):
            self.logger.warning(f"Could not parse Schumann value from {schumann_raw}, using default")
            return default_value
    
    def run(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        """Run the server.
        
        Args:
            host: Host to bind to
            port: Port to listen on
        """
        import uvicorn
        self.logger.info(f"🚀 Starting {self.__class__.__name__} on {host}:{port}")
        uvicorn.run(self.app, host=host, port=port) 