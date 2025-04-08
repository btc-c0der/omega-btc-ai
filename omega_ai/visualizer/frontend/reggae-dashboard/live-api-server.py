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
from flask_socketio import SocketIO, emit
from datetime import datetime, timezone
import redis
import asyncio
import time
import sys

# Add parent directories to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))))
sys.path.insert(0, parent_dir)

try:
    from omega_ai.trading.strategies.enhanced_exit_strategy import EnhancedExitStrategy
    from omega_ai.trading.exchanges.bitget_ccxt import BitGetCCXT
    from ccxt.base.types import OrderType, OrderSide
except ImportError as e:
    print(f"Error importing modules: {e}")
    print(f"Current path: {sys.path}")
    sys.exit(1)

# ANSI color codes for terminal output
GREEN = "\033[92m"
GOLD = "\033[93m"
YELLOW = "\033[93m"
RED = "\033[91m"
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

# Constants for the localhost server
redis_client = None
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)
BACKEND_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000"

# BitGet configuration
BITGET_API_KEY = os.getenv('BITGET_API_KEY', '')
BITGET_SECRET_KEY = os.getenv('BITGET_SECRET_KEY', '')
BITGET_PASSPHRASE = os.getenv('BITGET_PASSPHRASE', '')
STRATEGIC_SUB_ACCOUNT = os.getenv('STRATEGIC_SUB_ACCOUNT_NAME', '')

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

# Initialize Redis client
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

# Initialize BitGet client
bitget_client = None

def init_bitget_client():
    """Initialize the BitGetCCXT client"""
    global bitget_client
    if not bitget_client and BITGET_API_KEY and BITGET_SECRET_KEY and BITGET_PASSPHRASE:
        bitget_client = BitGetCCXT(
            config={
                'api_key': BITGET_API_KEY,
                'api_secret': BITGET_SECRET_KEY,
                'api_password': BITGET_PASSPHRASE,
                'use_testnet': False,
                'sub_account': STRATEGIC_SUB_ACCOUNT
            }
        )
        logger.info(f"{GREEN}BitGet client initialized for sub-account: {STRATEGIC_SUB_ACCOUNT}{RESET}")

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

@app.route('/tp-sl')
def tp_sl_panel():
    """Serve the TP/SL management panel."""
    logger.info("🔍 GET /tp-sl - Serving TP/SL panel")
    return send_from_directory('.', 'tp_sl_panel.html')

# Direct Redis key access endpoint
@app.route('/api/redis-key')
def redis_key():
    """Access a specific Redis key directly."""
    key = request.args.get('key')
    if not key:
        return jsonify({"error": "Missing key parameter"}), 400
    
    logger.info(f"🔍 GET /api/redis-key?key={key} - Direct Redis key access")
    
    try:
        value = redis_client.get(key)
        if value:
            return jsonify({
                "key": key,
                "value": value,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
        else:
            # For missing keys, return a 200 response with null value instead of 404
            # This helps frontend code handle missing keys more gracefully
            return jsonify({
                "key": key,
                "value": None,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            
    except Exception as e:
        logger.error(f"❌ Error accessing Redis key: {e}")
        return jsonify({
            "error": f"Error accessing Redis key: {str(e)}",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 500

@app.route('/api/close-position', methods=['POST'])
async def close_position():
    """Close the current position."""
    try:
        # Initialize BitGet client if needed
        if not bitget_client:
            init_bitget_client()
            
        if not bitget_client:
            return jsonify({
                "success": False,
                "error": "BitGet client not initialized",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }), 500
            
        # Get current position from Redis
        position_data = redis_client.get('current_position')
        if not position_data:
            return jsonify({
                "success": False,
                "error": "No active position found",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }), 404
            
        position = json.loads(position_data)
        
        # Determine close side
        close_side = 'sell' if position.get('direction') == 'long' else 'buy'
        
        # Close position
        await bitget_client.create_order(
            symbol=position.get('symbol', 'BTC/USDT:USDT'),
            type='market',
            side=close_side,
            amount=float(position.get('position_size', 0)),
            params={'reduceOnly': True}
        )
        
        # Update Redis
        redis_client.delete('current_position')
        
        return jsonify({
            "success": True,
            "message": "Position closed successfully",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Error closing position: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 500

@app.route('/api/update-tp', methods=['POST'])
async def update_take_profit():
    """Update take profit levels."""
    try:
        data = request.get_json()
        if not data or 'price' not in data:
            return jsonify({
                "success": False,
                "error": "Missing price parameter",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }), 400
            
        # Initialize BitGet client if needed
        if not bitget_client:
            init_bitget_client()
            
        if not bitget_client:
            return jsonify({
                "success": False,
                "error": "BitGet client not initialized",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }), 500
            
        # Get current position from Redis
        position_data = redis_client.get('current_position')
        if not position_data:
            return jsonify({
                "success": False,
                "error": "No active position found",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }), 404
            
        position = json.loads(position_data)
        
        # Update take profit
        await bitget_client.create_order(
            symbol=position.get('symbol', 'BTC/USDT:USDT'),
            type='limit',
            side='sell' if position.get('direction') == 'long' else 'buy',
            amount=float(position.get('position_size', 0)),
            price=float(data['price']),
            params={
                'reduceOnly': True,
                'timeInForce': 'GTC',
                'stopPrice': float(data['price']),
                'triggerType': 'market_price',
                'positionId': position.get('id')
            }
        )
        
        # Update position in Redis
        position['take_profit'] = float(data['price'])
        redis_client.set('current_position', json.dumps(position))
        
        return jsonify({
            "success": True,
            "message": "Take profit updated successfully",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Error updating take profit: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 500

@app.route('/api/update-sl', methods=['POST'])
async def update_stop_loss():
    """Update stop loss level."""
    try:
        data = request.get_json()
        if not data or 'price' not in data:
            return jsonify({
                "success": False,
                "error": "Missing price parameter",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }), 400
            
        # Initialize BitGet client if needed
        if not bitget_client:
            init_bitget_client()
            
        if not bitget_client:
            return jsonify({
                "success": False,
                "error": "BitGet client not initialized",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }), 500
            
        # Get current position from Redis
        position_data = redis_client.get('current_position')
        if not position_data:
            return jsonify({
                "success": False,
                "error": "No active position found",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }), 404
            
        position = json.loads(position_data)
        
        # Update stop loss
        await bitget_client.create_order(
            symbol=position.get('symbol', 'BTC/USDT:USDT'),
            type='stop',
            side='sell' if position.get('direction') == 'long' else 'buy',
            amount=float(position.get('position_size', 0)),
            price=float(data['price']),
            params={
                'reduceOnly': True,
                'timeInForce': 'GTC',
                'stopPrice': float(data['price']),
                'triggerType': 'market_price',
                'positionId': position.get('id')
            }
        )
        
        # Update position in Redis
        position['stop_loss'] = float(data['price'])
        redis_client.set('current_position', json.dumps(position))
        
        return jsonify({
            "success": True,
            "message": "Stop loss updated successfully",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Error updating stop loss: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 500

@app.route('/api/toggle-trailing-stop', methods=['POST'])
async def toggle_trailing_stop():
    """Toggle trailing stop for current position."""
    try:
        data = request.get_json()
        if data is None:
            data = {}
        activate = data.get('activate', True)
        
        # Initialize BitGet client if needed
        if not bitget_client:
            init_bitget_client()
            
        if not bitget_client:
            return jsonify({
                "success": False,
                "error": "BitGet client not initialized",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }), 500
            
        # Get position data from Redis
        position_data = redis_client.get('current_position')
        if not position_data:
            return jsonify({
                "success": False,
                "message": "No active position found",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }), 404
            
        position = json.loads(position_data)
        
        # Initialize enhanced exit strategy
        exit_strategy = EnhancedExitStrategy(
            config={
                'base_risk_percent': 1.0,
                'enable_scalping': True,
                'scalping_coefficient': 0.3,
                'strategic_coefficient': 0.6,
                'aggressive_coefficient': 0.1
            }
        )
        
        # Toggle trailing stop
        if activate:
            # Activate trailing stop
            new_stop = await exit_strategy.update_trailing_stop(
                position.get('id'),
                float(position.get('current_price', 0))
            )
            
            if new_stop:
                # Update stop loss with new trailing stop
                await bitget_client.create_order(
                    symbol=position.get('symbol', 'BTC/USDT:USDT'),
                    type='stop',
                    side='sell' if position.get('direction') == 'long' else 'buy',
                    amount=float(position.get('position_size', 0)),
                    price=new_stop,
                    params={
                        'reduceOnly': True,
                        'timeInForce': 'GTC',
                        'stopPrice': new_stop,
                        'triggerType': 'market_price',
                        'positionId': position.get('id')
                    }
                )
                
                # Update position in Redis
                position['trailing_activated'] = True
                position['stop_loss'] = new_stop
                redis_client.set('current_position', json.dumps(position))
        else:
            # Deactivate trailing stop
            position['trailing_activated'] = False
            redis_client.set('current_position', json.dumps(position))
        
        return jsonify({
            "success": True,
            "message": f"Trailing stop {'activated' if activate else 'deactivated'} successfully",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
    except Exception as e:
        logger.error(f"❌ Error toggling trailing stop: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 500

@app.route('/api/position-status')
def get_position_status():
    """Get detailed position status including trap analysis."""
    try:
        # Get position data from Redis
        position_data = redis_client.get('current_position')
        trap_data = redis_client.get('current_trap_probability')
        
        response = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "has_position": False
        }
        
        if position_data:
            position = json.loads(position_data)
            response.update({
                "has_position": True,
                "position": position
            })
            
        if trap_data:
            trap = json.loads(trap_data)
            response["trap_analysis"] = trap
            
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"❌ Error getting position status: {e}")
        return jsonify({
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 500

@app.route('/api/trap-analysis-panel')
def trap_analysis_panel():
    """Serve the trap analysis panel HTML content."""
    try:
        logger.info("🔍 GET /api/trap-analysis-panel - Fetching trap analysis panel")
        
        # Check if trap_analysis_panel.html exists in current directory
        panel_path = os.path.join(current_dir, 'trap_analysis_panel.html')
        if os.path.exists(panel_path):
            with open(panel_path, 'r') as file:
                content = file.read()
                return content
        
        # If file doesn't exist, return a basic panel template
        return """
        <div class="trap-analysis-content">
            <h3>Market Maker Trap Analysis</h3>
            <div class="trap-status">
                <p>No trap data available. Please check Redis connection.</p>
            </div>
        </div>
        """
        
    except Exception as e:
        logger.error(f"❌ Error fetching trap analysis panel: {e}")
        return f"""
        <div class="trap-analysis-content">
            <h3>Market Maker Trap Analysis</h3>
            <div class="trap-status error">
                <p>Error: {str(e)}</p>
            </div>
        </div>
        """

# WebSocket proxy setup at /ws
@app.route('/ws')
def websocket_proxy():
    """Redirect WebSocket connections to the backend."""
    # Just inform the client about WebSocket endpoint
    return jsonify({
        "message": "WebSocket endpoint is at ws://localhost:8000/ws",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# WebSocket event handlers
@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    logger.info(f"{GREEN}Client connected to WebSocket{RESET}")
    emit('connection_status', {'status': 'connected'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    logger.info(f"{GREEN}Client disconnected from WebSocket{RESET}")

@socketio.on('subscribe')
def handle_subscribe(data):
    """Handle subscription to real-time updates."""
    try:
        streams = data.get('streams', [])
        symbol = data.get('symbol', 'BTC/USDT:USDT')
        
        if not bitget_client:
            init_bitget_client()
            
        if not bitget_client:
            emit('error', {'message': 'BitGet client not initialized'})
            return
            
        # Register callbacks for each stream
        valid_streams = [
            'ticker', 'trades', 'orderbook', 'orders', 'positions',
            'balance', 'klines', 'liquidations', 'funding', 
            'market_state', 'system_status'
        ]
        
        for stream in streams:
            if stream in valid_streams:
                bitget_client.add_ws_callback(stream, lambda data: emit(stream, data))
                logger.info(f"{GREEN}Client subscribed to {stream} stream{RESET}")
            
        emit('subscription_status', {
            'status': 'subscribed',
            'streams': streams,
            'symbol': symbol,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
        
    except Exception as e:
        logger.error(f"{RED}Error in subscription: {str(e)}{RESET}")
        emit('error', {'message': str(e)})

@socketio.on('unsubscribe')
def handle_unsubscribe(data):
    """Handle unsubscription from streams."""
    try:
        streams = data.get('streams', [])
        
        if not bitget_client:
            emit('error', {'message': 'BitGet client not initialized'})
            return
            
        # Remove callbacks for each stream
        for stream in streams:
            if stream in bitget_client.ws_callbacks:
                bitget_client.ws_callbacks[stream] = []
                logger.info(f"{GREEN}Client unsubscribed from {stream} stream{RESET}")
            
        emit('subscription_status', {
            'status': 'unsubscribed',
            'streams': streams,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
        
    except Exception as e:
        logger.error(f"{RED}Error in unsubscription: {str(e)}{RESET}")
        emit('error', {'message': str(e)})

@socketio.on_error()
def handle_error(e):
    """Handle WebSocket errors."""
    logger.error(f"{RED}WebSocket error: {str(e)}{RESET}")
    emit('error', {'message': str(e)})

@socketio.on('reconnect')
def handle_reconnect():
    """Handle client reconnection."""
    logger.info(f"{GREEN}Client attempting to reconnect{RESET}")
    emit('connection_status', {'status': 'reconnecting'})

@socketio.on('reconnect_failed')
def handle_reconnect_failed():
    """Handle failed reconnection attempts."""
    logger.warning(f"{YELLOW}Client reconnection failed{RESET}")
    emit('connection_status', {'status': 'reconnect_failed'})

# Add WebSocket route for stream status
@app.route('/api/stream-status')
def get_stream_status():
    """Get status of all WebSocket streams."""
    try:
        if not bitget_client:
            return jsonify({
                "status": "disconnected",
                "streams": {},
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            
        status = {
            "status": "connected" if bitget_client.ws_connected else "disconnected",
            "streams": {},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Get status of each stream
        for stream in bitget_client.ws_callbacks:
            last_message = bitget_client.ws_last_message_time.get(stream, 0)
            time_since_last = time.time() - last_message if last_message > 0 else float('inf')
            
            status["streams"][stream] = {
                "active": time_since_last < bitget_client.ws_heartbeat_interval * 2,
                "last_message": datetime.fromtimestamp(last_message).isoformat() if last_message > 0 else None,
                "subscribers": len(bitget_client.ws_callbacks[stream])
            }
            
        return jsonify(status)
        
    except Exception as e:
        logger.error(f"{RED}Error getting stream status: {str(e)}{RESET}")
        return jsonify({
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 500

# Update the main execution
if __name__ == "__main__":
    # Start the server
    logger.info(f"Starting Reggae Dashboard Frontend Proxy on 0.0.0.0:5001")
    
    # Print colorful banner
    print(f"\n{GREEN}{BOLD}==============================================={RESET}")
    print(f"{GREEN}{BOLD}    OMEGA BTC AI - REGGAE DASHBOARD SERVER    {RESET}")
    print(f"{GREEN}{BOLD}==============================================={RESET}")
    print(f"{GOLD}    JAH BLESS YOUR TRADING JOURNEY    {RESET}")
    print(f"{GREEN}{BOLD}==============================================={RESET}\n")
    
    # Run the app with standard Flask (no SocketIO for now)
    app.run(host="0.0.0.0", port=5001, debug=True)
else:
    # For imported usage, we already have the app instance created above
    pass 