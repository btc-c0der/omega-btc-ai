#!/usr/bin/env python3
"""
FastAPI application for OMEGA GRID PORTAL - Off-White™ Edition
=============================================================

A REST API for the OMEGA GRID PORTAL integration, serving CLI functionality
to the web dashboard with Virgil Abloh-inspired design.

Copyright (c) 2024 OMEGA BTC AI
"""

import os
import json
import asyncio
from pathlib import Path
from typing import Optional, Dict, List, Any, Union

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import our grid portal component
from components.omega_grid_portal import (
    get_commands, 
    get_bots, 
    execute_command
)

# Set up the app
app = FastAPI(
    title="OMEGA GRID PORTAL API",
    description="REST API for the OMEGA GRID PORTAL with Virgil Abloh design aesthetic",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, set this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up static files and templates
current_dir = Path(__file__).parent
static_dir = current_dir / "static"
templates_dir = current_dir / "templates"

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

# Main routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Serve the main index.html file"""
    return FileResponse(current_dir / "index.html")

# OMEGA GRID PORTAL API endpoints
@app.get("/api/grid/commands")
async def grid_commands():
    """Get all available grid commands"""
    return await get_commands()

@app.get("/api/grid/bots")
async def grid_bots():
    """Get all available bots"""
    return await get_bots()

@app.post("/api/grid/execute")
async def grid_execute(request: Request):
    """Execute a grid command"""
    try:
        data = await request.json()
        command_id = data.get("commandId")
        param = data.get("param")
        
        if not command_id:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "output": "Command ID is required"}
            )
        
        result = await execute_command(command_id, param)
        return result
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "output": f"Error: {str(e)}"}
        )

# Startup event to log information
@app.on_event("startup")
async def startup_event():
    """Log startup information"""
    print("🌐 OMEGA GRID PORTAL API starting up")
    print(f"📂 Static files directory: {static_dir}")
    print(f"📝 Templates directory: {templates_dir}")

# Run the application when executed directly
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting OMEGA GRID PORTAL API on port {port}")
    uvicorn.run("fastapi_app:app", host="0.0.0.0", port=port, reload=True) 