# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    ping_interval=25,  # Send ping every 25 seconds
    ping_timeout=10,  # Wait 10 seconds for pong before disconnect
)

# Create ASGI application
app = socketio.ASGIApp(sio, static_files={
    '/': 'web/index.html',
    '/health': 'web/health/index.json'
})

# HTTP routes would typically be handled with FastAPI or Starlette, 
# but for simplicity we'll use socket.io's static file serving
@sio.on('connect')
async def connect(sid, environ):
    """Handle client connection."""
    client_info = {
        "sid": sid,
        "connected_at": datetime.datetime.now().isoformat(),
        "consciousness_level": 5,  # Default level
        "preferred_language": "en",  # Default language
        "ip": environ.get("REMOTE_ADDR", "unknown"),
        "user_agent": environ.get("HTTP_USER_AGENT", "unknown"),
    }
    
    # Check for language preference in headers or cookies
    accept_language = environ.get("HTTP_ACCEPT_LANGUAGE", "")
    if accept_language:
        # Simple parsing - just get the first language code
        lang_code = accept_language.split(",")[0].strip().split(";")[0].strip().lower()
        if lang_code and len(lang_code) >= 2:
            client_info["preferred_language"] = lang_code[:2]  # Just use the primary language code
    
    # Check cookies for preferred_language
    cookie_header = environ.get("HTTP_COOKIE", "")
    if cookie_header and "preferred_language=" in cookie_header:
        try:
            # Simple cookie parsing
            cookie_parts = cookie_header.split(";")
            for part in cookie_parts:
                if "preferred_language=" in part:
                    lang_value = part.split("=")[1].strip()
                    if lang_value and len(lang_value) >= 2:
                        client_info["preferred_language"] = lang_value
        except:
            pass
    
    active_clients[sid] = client_info
    
    logger.info(f"Client connected: {sid}, language: {client_info['preferred_language']}")
    
    # Send welcome message with quantum entropy
    await sio.emit("connect", {
        "message": "Welcome to the Matrix Neo News Portal WebSocket Sacred Echo Service",
        "quantum_entropy": generate_quantum_entropy(QUANTUM_ENTROPY_LEVEL),
        "timestamp": datetime.datetime.now().isoformat(),
    }, room=sid)

# This will be imported by uvicorn when run as a module
def get_app():
    return app 