#!/usr/bin/env python3
"""
Minimal WebSocket server using FastAPI and socket.io
"""

import os
import json
import datetime
import socketio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True
)

# Create FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Socket.IO app
socket_app = socketio.ASGIApp(sio)
app.mount("/socket.io", socket_app)

# Create a static health endpoint
@app.get("/health")
async def health():
    return {"status": "UP", "service": "websocket-minimal", "timestamp": datetime.datetime.now().isoformat()}

# Socket.IO events
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit('welcome', {"message": "Welcome to the Matrix Neo News Portal"}, room=sid)

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def subscribe_news(sid, data):
    print(f"Client {sid} subscribed to news: {data}")
    # Send a test news item
    test_news = {
        "id": "test-1",
        "title": "Welcome to the Matrix",
        "content": "The Matrix has you...",
        "published_at": datetime.datetime.now().isoformat(),
        "source": "Matrix Neo News Portal"
    }
    await sio.emit('news_update', test_news, room=sid)

# Run the app directly if invoked
if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10095"))
    uvicorn.run("websocket_minimal:app", host="0.0.0.0", port=port, reload=True) 