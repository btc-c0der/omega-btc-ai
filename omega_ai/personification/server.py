"""
OMEGA BTC AI - Bot Personification Server

This module provides a FastAPI server to serve the bot personification dashboard.
"""

import os
import logging
import uvicorn
import re
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from starlette.middleware.base import BaseHTTPMiddleware
from omega_ai.personification.api_routes import router as api_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewlineSanitizerMiddleware(BaseHTTPMiddleware):
    """Middleware to sanitize responses and remove problematic newline characters."""
    
    async def dispatch(self, request, call_next):
        # Get the original response
        response = await call_next(request)
        
        # Check for response types we can handle
        # Only process HTML responses with a body attribute
        if (isinstance(response, HTMLResponse) and 
            hasattr(response, 'body') and
            'text/html' in response.headers.get('content-type', '')):
            
            # Get response body
            body = response.body.decode('utf-8')
            
            # Fix any remaining literal newlines
            body = body.replace('\\n', '<br>')
            body = body.replace('\n', '<br>')
            
            # Replace multiple newlines with proper spacing
            body = re.sub(r'<br>\s*<br>\s*<br>', '<br><br>', body)
            
            # Replace any remaining literal backslashes
            body = body.replace('\\\\', '\\')
            
            # Create a new response with the sanitized body
            response_media_type = response.media_type or "text/html"
            return Response(
                content=body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response_media_type
            )
        
        # If it's not a response type we can handle, return it unmodified
        return response

# Create FastAPI app
app = FastAPI(title="OMEGA BTC AI - Bot Personification")

# Add the newline sanitizer middleware
app.add_middleware(NewlineSanitizerMiddleware)

# Include API routes
app.include_router(api_router)

# Base directory for static files
base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, "static")
sandbox_dir = os.path.join(base_dir, "sandbox")

# Create static directory if it doesn't exist
os.makedirs(static_dir, exist_ok=True)

# Mount static files directory
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """Serve the bot personification dashboard."""
    dashboard_path = os.path.join(sandbox_dir, "persona_dashboard.html")
    
    if os.path.exists(dashboard_path):
        with open(dashboard_path, "r") as f:
            return f.read()
    else:
        return HTMLResponse("<h1>Dashboard not found</h1>")

@app.get("/favicon.ico")
async def get_favicon():
    """Serve the favicon."""
    favicon_path = os.path.join(static_dir, "favicon.ico")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    else:
        return HTMLResponse("")

def main(port: int = 5042):
    """
    Run the server.
    
    Args:
        port: Port number to run the server on (default: 5042)
    """
    logger.info(f"Starting OMEGA BTC AI - Bot Personification Server on port {port}")
    uvicorn.run(
        "omega_ai.personification.server:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )

if __name__ == "__main__":
    main() 