
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

"""Test script for Security WebSocket connection."""

import asyncio
import websockets
import json
from datetime import datetime, UTC
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from omega_ai.visualizer.backend.dashboard_server import DashboardServer
from omega_ai.utils.redis_manager import RedisManager

async def test_security_websocket():
    """Test the Security WebSocket connection and data flow."""
    print("🚀 Starting Security WebSocket test...")
    
    # Initialize Redis manager
    redis_manager = RedisManager()
    
    # Initialize dashboard server
    server = DashboardServer()
    
    # Test WebSocket connection
    uri = "ws://localhost:8000/ws/security"
    print(f"🔌 Connecting to {uri}...")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket connected successfully")
            
            # Receive initial data
            print("📥 Waiting for initial data...")
            data = await websocket.recv()
            response = json.loads(data)
            
            # Verify response structure
            assert response["type"] == "security_dashboard", "Invalid response type"
            assert "data" in response, "Missing data field"
            assert "timestamp" in response, "Missing timestamp field"
            
            print("✅ Received valid initial data")
            print(f"📊 Dashboard type: {response['type']}")
            print(f"🕒 Timestamp: {response['timestamp']}")
            
            # Test data updates
            print("\n🔄 Testing data updates...")
            for _ in range(3):  # Test 3 updates
                data = await websocket.recv()
                response = json.loads(data)
                print(f"📥 Received update {_+1}/3")
                print(f"🕒 Update timestamp: {response['timestamp']}")
                await asyncio.sleep(1)  # Wait between updates
            
            print("\n✨ Security WebSocket test completed successfully!")
            
    except Exception as e:
        print(f"❌ Error during WebSocket test: {e}")
        raise

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_security_websocket()) 