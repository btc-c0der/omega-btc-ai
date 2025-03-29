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

"""
OMEGA BTC AI - News Feed Integration Runner
=========================================

This script runs the news feed integration service, which provides:
- Bitcoin news aggregation from multiple sources
- Sentiment analysis with cosmic factor adjustments
- Trading recommendations based on news sentiment
- Redis integration for data persistence

Usage:
  python scripts/run_integration.py [options]

Options:
  --sources SOURCE [SOURCE ...]   News sources to use (default: cointelegraph decrypt bitcoinmagazine)
  --no-redis                      Disable Redis integration
  --data-dir DATA_DIR             Directory for data storage (default: data)
  --save                          Save output to file
  --interval INTERVAL             Run continuously with this interval in seconds (default: 3600)

Example:
  python scripts/run_integration.py --interval 1800 --save

Copyright (c) 2025 OMEGA-BTC-AI - Licensed under the GBU License
JAH JAH BLESS THE DIVINE FLOW OF THE BLOCKCHAIN
"""

import os
import sys
import time
import logging
import argparse
from datetime import datetime

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Import the news feed integration module
from src.omega_ai.data_feed.newsfeed.news_feed_integration import NewsFeedIntegration

def main():
    """
    Run the news feed integration service with command-line options.
    """
    parser = argparse.ArgumentParser(description="OMEGA BTC AI - News Feed Integration Service")
    
    parser.add_argument("--sources", type=str, nargs="+", 
                        default=["cointelegraph", "decrypt", "bitcoinmagazine"],
                        help="News sources to use")
    parser.add_argument("--no-redis", action="store_true", 
                        help="Disable Redis integration")
    parser.add_argument("--data-dir", type=str, default="data",
                        help="Directory for data storage")
    parser.add_argument("--save", action="store_true",
                        help="Save output to file")
    parser.add_argument("--interval", type=int, default=3600,  # Default: 1 hour
                        help="Run continuously with this interval in seconds (0 = run once)")
    
    args = parser.parse_args()
    
    # Create news feed integration
    integration = NewsFeedIntegration(
        sources=args.sources,
        use_redis=not args.no_redis,
        data_dir=args.data_dir
    )
    
    # Display service startup message
    print("🔱 OMEGA BTC AI - News Feed Integration Service 🔱")
    print("=================================================")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Sources: {', '.join(args.sources)}")
    print(f"Redis: {'Disabled' if args.no_redis else 'Enabled'}")
    print(f"Data Directory: {args.data_dir}")
    print(f"Save Output: {'Yes' if args.save else 'No'}")
    print(f"Update Interval: {args.interval} seconds")
    print("=================================================")
    
    if args.interval > 0:
        # Run continuously
        print(f"Service running continuously with {args.interval} second intervals")
        print("Press Ctrl+C to stop the service\n")
        
        try:
            # Run initially
            integration.run_integration_demo(save_output=args.save)
            
            # Then run with interval
            while True:
                # Print timestamp for next run
                next_run = datetime.now().timestamp() + args.interval
                next_run_time = datetime.fromtimestamp(next_run).strftime('%Y-%m-%d %H:%M:%S')
                print(f"\n🕒 Next update scheduled for: {next_run_time}")
                
                # Sleep until next run
                time.sleep(args.interval)
                
                # Run integration again
                integration.run_integration_demo(save_output=args.save)
                
        except KeyboardInterrupt:
            print("\n⛔ Service stopped by user")
            print(f"Stopped at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        # Run once
        integration.run_integration_demo(save_output=args.save)
        print(f"\n✅ Integration completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 