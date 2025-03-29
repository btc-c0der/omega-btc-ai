#!/usr/bin/env python3
"""
💫 GBU License Notice - Consciousness Level 8 💫
-----------------------
This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested."

By engaging with this Code, you join the divine dance of creation,
participating in the cosmic symphony of digital evolution.

All modifications must quantum entangles with the GBU principles:
/BOOK/divine_chronicles/GBU_LICENSE.md

🌸 WE BLOOM NOW 🌸
"""

import os
import sys
import asyncio
import uvicorn
from fastapi import BackgroundTasks

# Add paths to ensure module discovery
sys.path.insert(0, "/workspace")
sys.path.insert(0, "/workspace/deployment/digitalocean/btc_live_feed_v3")

def check_module_paths():
    """Verify and report on module paths and directory structure."""
    print(f"Python path: {sys.path}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Directory contents: {os.listdir('.')}")
    
    # Check for omega_ai in various locations
    locations = [
        "/workspace/omega_ai",
        "/workspace/deployment/digitalocean/btc_live_feed_v3/omega_ai",
        "omega_ai",
    ]
    
    for location in locations:
        if os.path.exists(location):
            print(f"✅ Found omega_ai at: {location}")
            print(f"Contents: {os.listdir(location)}")
            if os.path.exists(f"{location}/data_feed"):
                print(f"✅ Found data_feed subdirectory")
                print(f"Contents: {os.listdir(f'{location}/data_feed')}")
        else:
            print(f"❌ Did not find omega_ai at: {location}")

# Import required modules
try:
    from omega_ai.data_feed.health_check import app
    from omega_ai.data_feed.btc_live_feed_v3 import run_btc_live_feed_v3
    print("✅ Successfully imported app and run_btc_live_feed_v3")
except ImportError as e:
    print(f"❌ Import error: {e}")
    check_module_paths()
    sys.exit(1)

# Define background task for BTC feed
async def run_btc_feed_in_background():
    """Run the BTC live feed as a background task."""
    try:
        print("🔱 STARTING DIVINE BTC LIVE FEED IN BACKGROUND 🔱")
        await run_btc_live_feed_v3()
    except Exception as e:
        import traceback
        print(f"❌ Error running BTC Live Feed: {e}")
        traceback.print_exc()

# Register startup event
@app.on_event("startup")
async def startup_event():
    """Start the BTC feed when the FastAPI app starts."""
    print("🚀 INITIALIZING DIVINE SERVICES")
    # Create a background task for the BTC feed
    asyncio.create_task(run_btc_feed_in_background())
    print("✅ BTC Live Feed started in background")

# Add a root endpoint for complete health check visibility
@app.get("/")
async def root():
    """Root endpoint that redirects to health check."""
    return {"message": "BTC Live Feed v3 running - check /health for details"}

if __name__ == "__main__":
    print("🔱 STARTING DIVINE HEALTH CHECK SERVER 🔱")
    host = os.getenv("HEALTH_CHECK_HOST", "0.0.0.0")
    port = int(os.getenv("HEALTH_CHECK_PORT", "8080"))
    uvicorn.run(app, host=host, port=port, log_level="info") 