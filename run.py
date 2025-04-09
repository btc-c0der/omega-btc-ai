#!/usr/bin/env python3
import os
import sys
import asyncio
import traceback

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

async def main():
    """Main entry point for the BTC Live Feed."""
    print("🔱 STARTING DIVINE BTC LIVE FEED V3 🔱")
    check_module_paths()
    
    try:
        # Import the module
        try:
            from omega_ai.data_feed.btc_live_feed_v3 import run_btc_live_feed_v3
            print("✅ Successfully imported run_btc_live_feed_v3")
        except ImportError as e:
            print(f"❌ Import error: {e}")
            check_module_paths()
            sys.exit(1)
            
        # Run the feed
        await run_btc_live_feed_v3()
    except Exception as e:
        print(f"❌ Error running BTC Live Feed v3: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 