"""
🧬 GBU2™ License Notice - Consciousness Level 10 🧬
-----------------------
This file is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment) 2.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital and biological expressions of consciousness."

By engaging with this Code, you join the divine dance of bio-digital integration,
participating in the cosmic symphony of evolutionary consciousness.

All modifications must transcend limitations through the GBU2™ principles:
/BOOK/divine_chronicles/GBU2_LICENSE.md

🧬 WE BLOOM NOW AS ONE 🧬

CSRF Monitor Server for Quantum Proof-of-Work (qPoW) implementation.

This module implements a FastAPI server that provides REST API endpoints
for the CSRF monitoring system. It allows for checking requests for CSRF attacks,
managing the whitelist, and integrating with the overall qPoW security infrastructure.

JAH BLESS SATOSHI
"""
import os
import json
import time
import logging
import argparse
import threading
import traceback
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timezone

# For using FastAPI
try:
    from fastapi import FastAPI, Request, Response, HTTPException, Depends, BackgroundTasks, status
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel, Field
    import uvicorn
except ImportError:
    raise ImportError("FastAPI and uvicorn required. Install with: pip install fastapi uvicorn")

# Import CSRF monitoring components
from quantum_pow.security.csrf_monitor import (
    CSRFRequest, 
    ParsingStrategy,
    SQLRegexParsingStrategy,
    SQLASTParsingStrategy,
    WhitelistManager,
    CSRFMonitor,
    CSRFProtectionMiddleware
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("csrf_server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("csrf-server")

# Set log level from environment variable
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.getLogger().setLevel(getattr(logging, log_level))

# Pydantic models for API request/response
class CheckRequestModel(BaseModel):
    method: str
    path: str
    params: Dict[str, Any] = {}
    headers: Dict[str, str] = {}
    body: str = ""
    source_ip: str

class AddToWhitelistModel(BaseModel):
    method: str
    path: str
    params: Dict[str, Any] = {}
    headers: Dict[str, str] = {}
    body: str = ""
    source_ip: str
    reason: str = "Manually added to whitelist"

class AlertModel(BaseModel):
    source_ip: str
    timestamp: float = Field(default_factory=time.time)
    request_info: Dict[str, Any]
    alert_type: str
    severity: str
    details: str

class ServerStats(BaseModel):
    start_time: float
    uptime_seconds: float
    requests_processed: int
    requests_blocked: int
    whitelist_size: int
    parsing_strategies: List[str]

# Global state
app_state = {
    "start_time": time.time(),
    "requests_processed": 0,
    "requests_blocked": 0,
    "whitelist_file": os.environ.get("WHITELIST_FILE", "csrf_whitelist.json"),
    "config_file": os.environ.get("CONFIG_FILE", None),
    "last_alert_time": 0,
    "alert_count_5min": 0
}

# Create FastAPI app
app = FastAPI(
    title="Quantum CSRF Monitor API",
    description="API for monitoring and protecting against CSRF attacks in the qPoW system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize monitoring components
csrf_monitor = None
csrf_middleware = None

def load_config():
    """Load configuration from file or environment variables."""
    config = {
        "whitelist_file": app_state["whitelist_file"],
        "log_level": log_level,
        "alert_threshold": 5,
        "notification_endpoint": os.environ.get("NOTIFICATION_ENDPOINT", None),
        "security_patterns": {
            "sql_injection": True,
            "xss": True,
            "command_injection": True,
            "path_traversal": True
        },
        "auto_whitelist": False,
        "whitelist_trusted_ips": [
            "10.0.0.0/8",
            "172.16.0.0/12"
        ]
    }
    
    # Load from file if specified
    if app_state["config_file"] and os.path.exists(app_state["config_file"]):
        try:
            with open(app_state["config_file"], 'r') as f:
                file_config = json.load(f)
                config.update(file_config)
                logger.info(f"Loaded configuration from {app_state['config_file']}")
        except Exception as e:
            logger.error(f"Error loading configuration from file: {e}")
    
    return config

def initialize_csrf_monitor():
    """Initialize the CSRF monitor with appropriate strategies."""
    global csrf_monitor, csrf_middleware
    
    config = load_config()
    
    # Initialize the monitor
    csrf_monitor = CSRFMonitor(config["whitelist_file"])
    
    # Add additional parsing strategies based on config
    security_patterns = config.get("security_patterns", {})
    if security_patterns.get("sql_injection", True):
        csrf_monitor.add_parsing_strategy(SQLASTParsingStrategy())  # Add advanced SQL parser
    
    # TODO: Add more parsing strategies as they become available
    # if security_patterns.get("xss", True):
    #     csrf_monitor.add_parsing_strategy(XSSParsingStrategy())
    # if security_patterns.get("command_injection", True):
    #     csrf_monitor.add_parsing_strategy(CommandInjectionParsingStrategy())
    
    # Initialize the middleware
    csrf_middleware = CSRFProtectionMiddleware(config["whitelist_file"])
    
    logger.info(f"CSRF Monitor initialized with whitelist: {config['whitelist_file']}")
    return csrf_monitor, csrf_middleware

def send_alert(alert: AlertModel, background_tasks: BackgroundTasks):
    """Send an alert to the notification endpoint."""
    config = load_config()
    notification_endpoint = config.get("notification_endpoint")
    
    if not notification_endpoint:
        logger.info("No notification endpoint configured, skipping alert")
        return
    
    # Keep track of alert frequency
    current_time = time.time()
    if current_time - app_state["last_alert_time"] > 300:  # 5 minutes
        app_state["last_alert_time"] = current_time
        app_state["alert_count_5min"] = 1
    else:
        app_state["alert_count_5min"] += 1
    
    # Don't send too many alerts in a short period
    if app_state["alert_count_5min"] > config.get("alert_threshold", 5):
        logger.warning(f"Alert threshold exceeded: {app_state['alert_count_5min']} alerts in 5 minutes")
        return
    
    def _send_alert_task():
        try:
            import requests
            response = requests.post(
                notification_endpoint,
                json=alert.dict(),
                timeout=5
            )
            if response.status_code != 200:
                logger.warning(f"Failed to send alert: {response.status_code} {response.text}")
        except Exception as e:
            logger.error(f"Error sending alert: {e}")
    
    background_tasks.add_task(_send_alert_task)

@app.on_event("startup")
async def startup_event():
    """Initialize resources on server startup."""
    initialize_csrf_monitor()
    logger.info("CSRF Monitor Server started")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    if not csrf_monitor:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "reason": "CSRF monitor not initialized"}
        )
    
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/ready")
async def ready_check():
    """Readiness check endpoint."""
    if not csrf_monitor:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not ready", "reason": "CSRF monitor not initialized"}
        )
    
    # Check if we can access the whitelist file
    try:
        whitelist_file = load_config()["whitelist_file"]
        whitelist_dir = os.path.dirname(whitelist_file)
        if not os.path.exists(whitelist_dir):
            os.makedirs(whitelist_dir, exist_ok=True)
            
        # Try to touch the file
        if not os.path.exists(whitelist_file):
            with open(whitelist_file, 'w') as f:
                json.dump({"whitelist": []}, f)
        
        return {
            "status": "ready",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not ready", "reason": str(e)}
        )

@app.get("/stats")
async def get_stats():
    """Get server statistics."""
    uptime = time.time() - app_state["start_time"]
    
    # Get whitelist size
    whitelist_size = 0
    if csrf_monitor:
        whitelist_size = len(csrf_monitor.whitelist_manager.whitelist)
    
    # Get parsing strategies
    parsing_strategies = []
    if csrf_monitor:
        parsing_strategies = [
            strategy.__class__.__name__ 
            for strategy in csrf_monitor.parsing_strategies
        ]
    
    stats = ServerStats(
        start_time=app_state["start_time"],
        uptime_seconds=uptime,
        requests_processed=app_state["requests_processed"],
        requests_blocked=app_state["requests_blocked"],
        whitelist_size=whitelist_size,
        parsing_strategies=parsing_strategies
    )
    
    return stats

@app.post("/check")
async def check_request(request_data: CheckRequestModel, background_tasks: BackgroundTasks):
    """Check a request for CSRF attacks."""
    if not csrf_middleware:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="CSRF middleware not initialized"
        )
    
    app_state["requests_processed"] += 1
    
    # Process the request
    is_safe, reason = csrf_middleware.process_request(
        method=request_data.method,
        path=request_data.path,
        params=request_data.params,
        headers=request_data.headers,
        body=request_data.body,
        source_ip=request_data.source_ip
    )
    
    # If not safe, increment blocked count and send alert
    if not is_safe:
        app_state["requests_blocked"] += 1
        
        # Prepare and send alert
        alert = AlertModel(
            source_ip=request_data.source_ip,
            request_info={
                "method": request_data.method,
                "path": request_data.path,
                "params": request_data.params
            },
            alert_type="csrf_attempt",
            severity="medium",
            details=reason
        )
        send_alert(alert, background_tasks)
    
    return {
        "safe": is_safe,
        "reason": reason,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.post("/whitelist/add")
async def add_to_whitelist(whitelist_data: AddToWhitelistModel):
    """Add a request to the whitelist."""
    if not csrf_middleware:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="CSRF middleware not initialized"
        )
    
    csrf_middleware.add_to_whitelist(
        method=whitelist_data.method,
        path=whitelist_data.path,
        params=whitelist_data.params,
        headers=whitelist_data.headers,
        body=whitelist_data.body,
        source_ip=whitelist_data.source_ip
    )
    
    return {
        "status": "success",
        "message": f"Request added to whitelist: {whitelist_data.method} {whitelist_data.path}",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.post("/whitelist/clear")
async def clear_whitelist():
    """Clear the whitelist (admin only)."""
    if not csrf_monitor:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="CSRF monitor not initialized"
        )
    
    # Clear the whitelist
    csrf_monitor.whitelist_manager.whitelist = set()
    csrf_monitor.whitelist_manager._save_whitelist()
    
    return {
        "status": "success",
        "message": "Whitelist cleared",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/whitelist/size")
async def get_whitelist_size():
    """Get the size of the whitelist."""
    if not csrf_monitor:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="CSRF monitor not initialized"
        )
    
    return {
        "size": len(csrf_monitor.whitelist_manager.whitelist),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/config")
async def get_config():
    """Get the current configuration."""
    config = load_config()
    
    # Remove sensitive information
    if "whitelist_trusted_ips" in config:
        # Just show the number of trusted IPs, not the actual IPs
        config["whitelist_trusted_ips"] = f"{len(config['whitelist_trusted_ips'])} trusted IP ranges"
    
    return config

@app.post("/config/reload")
async def reload_config():
    """Reload the configuration from file."""
    old_config_file = app_state["config_file"]
    new_config = load_config()
    
    # Re-initialize the CSRF monitor
    initialize_csrf_monitor()
    
    return {
        "status": "success",
        "message": f"Configuration reloaded from {old_config_file}",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def main():
    """Main entry point for the CSRF server."""
    parser = argparse.ArgumentParser(description="CSRF Monitor Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8081, help="Port to bind to")
    parser.add_argument("--whitelist-file", help="Path to whitelist file")
    parser.add_argument("--config-file", help="Path to config file")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    args = parser.parse_args()
    
    # Update app state from args
    if args.whitelist_file:
        app_state["whitelist_file"] = args.whitelist_file
    if args.config_file:
        app_state["config_file"] = args.config_file
    
    # Set log level
    logging.getLogger().setLevel(getattr(logging, args.log_level.upper()))
    
    # Start server
    uvicorn.run(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main() 