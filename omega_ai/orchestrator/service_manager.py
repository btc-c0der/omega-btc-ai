
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
Service Manager for OMEGA BTC AI System

Handles service lifecycle management, health checks, and dependency management.
"""

import asyncio
import logging
import signal
import sys
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('omega_service.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('ServiceManager')

class ServiceStatus(Enum):
    """Service status enumeration."""
    STOPPED = "STOPPED"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    ERROR = "ERROR"
    SHUTTING_DOWN = "SHUTTING_DOWN"

@dataclass
class ServiceInfo:
    """Information about a service."""
    name: str
    dependencies: Set[str]
    start_func: callable
    stop_func: callable
    health_check_func: Optional[callable] = None
    status: ServiceStatus = ServiceStatus.STOPPED
    last_health_check: Optional[datetime] = None
    error: Optional[str] = None

class ServiceManager:
    """Manages the lifecycle of all OMEGA BTC AI services."""
    
    def __init__(self):
        self.services: Dict[str, ServiceInfo] = {}
        self._shutdown_event = asyncio.Event()
        self._health_check_task = None
        
    def register_service(
        self,
        name: str,
        start_func: callable,
        stop_func: callable,
        dependencies: Set[str] = None,
        health_check_func: Optional[callable] = None
    ) -> None:
        """Register a new service with the manager."""
        if name in self.services:
            raise ValueError(f"Service {name} is already registered")
            
        self.services[name] = ServiceInfo(
            name=name,
            dependencies=dependencies or set(),
            start_func=start_func,
            stop_func=stop_func,
            health_check_func=health_check_func
        )
        logger.info(f"Registered service: {name}")
        
    async def start_service(self, name: str) -> bool:
        """Start a service and its dependencies."""
        if name not in self.services:
            logger.error(f"Service {name} not found")
            return False
            
        service = self.services[name]
        if service.status == ServiceStatus.RUNNING:
            logger.info(f"Service {name} is already running")
            return True
            
        # Start dependencies first
        for dep in service.dependencies:
            if not await self.start_service(dep):
                logger.error(f"Failed to start dependency {dep} for {name}")
                return False
                
        try:
            logger.info(f"Starting service: {name}")
            service.status = ServiceStatus.STARTING
            await service.start_func()
            service.status = ServiceStatus.RUNNING
            service.error = None
            logger.info(f"Service {name} started successfully")
            return True
        except Exception as e:
            service.status = ServiceStatus.ERROR
            service.error = str(e)
            logger.error(f"Failed to start service {name}: {e}")
            return False
            
    async def stop_service(self, name: str) -> bool:
        """Stop a service."""
        if name not in self.services:
            logger.error(f"Service {name} not found")
            return False
            
        service = self.services[name]
        if service.status == ServiceStatus.STOPPED:
            return True
            
        try:
            logger.info(f"Stopping service: {name}")
            service.status = ServiceStatus.SHUTTING_DOWN
            await service.stop_func()
            service.status = ServiceStatus.STOPPED
            logger.info(f"Service {name} stopped successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to stop service {name}: {e}")
            return False
            
    async def health_check(self) -> None:
        """Perform health checks on all services."""
        while not self._shutdown_event.is_set():
            for name, service in self.services.items():
                if service.status == ServiceStatus.RUNNING and service.health_check_func:
                    try:
                        is_healthy = await service.health_check_func()
                        if not is_healthy:
                            service.status = ServiceStatus.ERROR
                            service.error = "Health check failed"
                            logger.error(f"Health check failed for service {name}")
                    except Exception as e:
                        service.status = ServiceStatus.ERROR
                        service.error = str(e)
                        logger.error(f"Health check error for service {name}: {e}")
                    service.last_health_check = datetime.now()
            await asyncio.sleep(30)  # Check every 30 seconds
            
    async def start_all(self) -> bool:
        """Start all registered services."""
        success = True
        for name in self.services:
            if not await self.start_service(name):
                success = False
                break
        return success
        
    async def stop_all(self) -> bool:
        """Stop all registered services."""
        success = True
        for name in reversed(list(self.services.keys())):  # Stop in reverse order
            if not await self.stop_service(name):
                success = False
                break
        return success
        
    def get_service_status(self, name: str) -> Optional[ServiceInfo]:
        """Get the current status of a service."""
        return self.services.get(name)
        
    def get_all_status(self) -> Dict[str, ServiceInfo]:
        """Get the status of all services."""
        return self.services.copy()
        
    async def shutdown(self) -> None:
        """Gracefully shutdown all services."""
        logger.info("Initiating graceful shutdown...")
        self._shutdown_event.set()
        
        if self._health_check_task:
            self._health_check_task.cancel()
            try:
                await self._health_check_task
            except asyncio.CancelledError:
                pass
                
        await self.stop_all()
        logger.info("Shutdown complete")
        
    def setup_signal_handlers(self) -> None:
        """Setup signal handlers for graceful shutdown."""
        for sig in (signal.SIGTERM, signal.SIGINT):
            signal.signal(sig, lambda s, f: asyncio.create_task(self.shutdown())) 