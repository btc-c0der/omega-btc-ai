#!/usr/bin/env python3
"""
Simplified Frontend Server for OMEGA BTC AI Dashboard
Serves the HTML/static assets and proxies API requests to the backend
"""

import logging
import os
import requests
import json
from flask import Flask, jsonify, send_from_directory, request, Response
from flask_cors import CORS
from datetime import datetime, timezone

# ANSI color codes for terminal output
GREEN = "\033[92m"
GOLD = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("reggae_dashboard.log")
    ]
)
logger = logging.getLogger("live_api_server")

# Backend server URL
BACKEND_URL = "http://localhost:8001"

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": True,
        "max_age": 600
    }
})

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# API routes - serve dashboard HTML
@app.route('/')
def index():
    """Serve the dashboard HTML."""
    logger.info("🔍 GET / - Serving dashboard HTML")
    return send_from_directory('.', 'live-dashboard.html')

@app.route('/backup')
def backup_dashboard():
    """Backup endpoint for data recovery."""
    logger.info("🔍 GET /backup - Backup request received")
    return send_from_directory('.', 'backup-dashboard.html')

# Add route for static files in the src directory
@app.route('/src/<path:filename>')
def serve_static(filename):
    """Serve static files from the src directory."""
    logger.info(f"🔍 GET /src/{filename} - Serving static file")
    return send_from_directory('src', filename)

# Add route for node_modules
@app.route('/node_modules/<path:filename>')
def serve_node_modules(filename):
    """Serve files from node_modules directory."""
    logger.info(f"🔍 GET /node_modules/{filename} - Serving node module file")
    return send_from_directory('node_modules', filename)

# Direct Redis key access endpoint
@app.route('/api/redis-key')
def redis_key():
    """Access a specific Redis key directly (proxied to backend redis-get endpoint)."""
    key = request.args.get('key')
    if not key:
        return jsonify({"error": "Missing key parameter"}), 400
    
    logger.info(f"🔍 GET /api/redis-key?key={key} - Direct Redis key access")
    
    # Forward the request to the backend using the correct endpoint
    # Note: Backend expects /api/redis-get?key={key} format
    backend_url = f"{BACKEND_URL}/api/redis-get?key={key}"
    logger.info(f"🔗 Forwarding Redis request to backend: {backend_url}")
    
    try:
        resp = requests.get(
            url=backend_url,
            headers={k: v for (k, v) in request.headers if k != 'Host'},
            cookies=request.cookies,
            allow_redirects=False,
            verify=False
        )
        
        if resp.status_code == 200:
            logger.info(f"✅ Redis key {key} successfully retrieved")
            
            try:
                # Try to parse response text as JSON
                return jsonify({
                    "key": key,
                    "value": resp.text,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
            except json.JSONDecodeError:
                # Return as plain text if not JSON
                return jsonify({
                    "key": key,
                    "value": resp.text,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
        else:
            logger.error(f"❌ Redis key access failed with status: {resp.status_code}")
            logger.error(f"❌ Response content: {resp.text}")
            return jsonify({
                "error": f"Redis key access failed: {resp.status_code}",
                "key": key,
                "details": resp.text,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }), resp.status_code
            
    except Exception as e:
        logger.error(f"❌ Error accessing Redis key: {e}")
        return jsonify({
            "error": f"Error accessing Redis key: {str(e)}",
            "key": key,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 500

# Proxy all API requests to the backend server
@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_api(path):
    """Proxy all API requests to the backend server."""
    logger.info(f"🔄 {request.method} /api/{path} - Proxying request to backend")
    
    # Build the URL for the backend API
    backend_url = f"{BACKEND_URL}/api/{path}"
    logger.info(f"🔗 Backend URL: {backend_url}")
    
    try:
        # Forward the request to the backend
        resp = requests.request(
            method=request.method,
            url=backend_url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            params=dict(request.args),
            allow_redirects=False,
            verify=False
        )
        
        logger.info(f"✅ Backend responded with status: {resp.status_code}")
        
        # Create the Flask response object
        response = Response(
            resp.content,
            resp.status_code,
            {key: value for (key, value) in resp.headers.items() if key != 'Transfer-Encoding'}
        )
        
        return response
        
    except requests.exceptions.ConnectionError:
        logger.error(f"❌ Failed to connect to backend at {backend_url}")
        return jsonify({
            "error": "Backend server connection failed",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 503
    except Exception as e:
        logger.error(f"❌ Error proxying request: {e}")
        return jsonify({
            "error": f"Proxy error: {str(e)}",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 500

# WebSocket proxy setup at /ws
@app.route('/ws')
def websocket_proxy():
    """Redirect WebSocket connections to the backend."""
    # Just inform the client about WebSocket endpoint
    return jsonify({
        "message": "WebSocket endpoint is at ws://localhost:8001/ws",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

if __name__ == "__main__":
    # Start the server
    logger.info(f"Starting Reggae Dashboard Frontend Proxy on 0.0.0.0:5001")
    
    # Print colorful banner
    print(f"\n{GREEN}{BOLD}==============================================={RESET}")
    print(f"{GREEN}{BOLD}    OMEGA BTC AI - REGGAE DASHBOARD SERVER    {RESET}")
    print(f"{GREEN}{BOLD}==============================================={RESET}")
    print(f"{GOLD}    JAH BLESS YOUR TRADING JOURNEY    {RESET}")
    print(f"{GREEN}{BOLD}==============================================={RESET}\n")
    
    # Run the app with Flask's development server on port 5001
    app.run(host="0.0.0.0", port=5001)
else:
    # For imported usage, we already have the app instance created above
    pass 