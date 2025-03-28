#!/usr/bin/env python3
"""
OMEGA BTC AI - BTC News Feed CLI
===============================

Command-line interface for the BTC News Feed module.

🔮 GPU (General Public Universal) License 1.0
--------------------------------------------
OMEGA BTC AI DIVINE COLLECTIVE
Licensed under the GPU (General Public Universal) License v1.0
Date: 2025-03-28
Location: The Cosmic Void

This source code is governed by the GPU License, granting the following sacred freedoms:
- The Freedom to Study this code, its divine algorithms and cosmic patterns
- The Freedom to Modify this code, enhancing its divine functionality
- The Freedom to Distribute this code, sharing its sacred knowledge
- The Freedom to Use this code, implementing its sacred algorithms

Along with these divine obligations:
- Preserve this sacred knowledge by maintaining source accessibility
- Share all divine modifications to maintain universal access
- Provide attribution to acknowledge sacred origins

For the full divine license, consult the LICENSE file in the project root.

Copyright (c) 2025 OMEGA-BTC-AI - Licensed under the GPU License
JAH JAH BLESS THE DIVINE FLOW OF THE BLOCKCHAIN
"""

from omega_ai.data_feed.newsfeed.btc_newsfeed import BtcNewsFeed, display_rasta_banner
import argparse
import logging
from rich.console import Console

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("btc-newsfeed-cli")

console = Console()

def main():
    """Main entry point for CLI execution."""
    parser = argparse.ArgumentParser(description="🔱 OMEGA BTC NEWS FEED - Cryptocurrency News Analyzer")
    
    # Main arguments
    parser.add_argument("--sources", type=str, nargs="+", default=["cointelegraph", "cryptonews", "decrypt"],
                      help="News source keys (default: cointelegraph cryptonews decrypt)")
    parser.add_argument("--limit", type=int, default=10,
                      help="Number of news items to fetch (default: 10)")
    parser.add_argument("--data-dir", type=str, default="data",
                      help="Directory to store datasets (default: 'data')")
    
    # Action flags
    parser.add_argument("--stream", action="store_true",
                      help="Stream news with periodic updates")
    parser.add_argument("--interval", type=int, default=300,
                      help="Refresh interval in seconds for streaming (default: 300)")
    parser.add_argument("--label", type=str, choices=["bullish", "bearish", "neutral"],
                      help="Manual sentiment label override")
    parser.add_argument("--save", action="store_true",
                      help="Save output with optional label")
    parser.add_argument("--format", type=str, choices=["csv", "json"], default="csv",
                      help="Output format (default: csv)")
    parser.add_argument("--train-data", action="store_true",
                      help="Generate ML training dataset from saved news")
    parser.add_argument("--filter", type=str, nargs="+",
                      help="Additional keywords to filter news by")
    parser.add_argument("--no-redis", action="store_true",
                      help="Disable Redis integration")
    parser.add_argument("--show-redis-status", action="store_true",
                      help="Show Redis connection status")
    
    args = parser.parse_args()
    
    # Display banner
    display_rasta_banner()
    
    # Create the news feed instance
    news_feed = BtcNewsFeed(data_dir=args.data_dir, use_redis=not args.no_redis)
    
    # Show Redis status if requested
    if args.show_redis_status:
        if news_feed.redis_client:
            console.print("[green]✅ Connected to Redis at:[/]")
            if hasattr(news_feed.redis_client, 'connection_pool'):
                # Standard Redis client
                host = news_feed.redis_client.connection_pool.connection_kwargs.get('host', 'unknown')
                port = news_feed.redis_client.connection_pool.connection_kwargs.get('port', 'unknown')
                console.print(f"[cyan]   Host:[/] {host}")
                console.print(f"[cyan]   Port:[/] {port}")
                console.print(f"[cyan]   SSL Enabled:[/] {news_feed.redis_client.connection_pool.connection_kwargs.get('ssl', False)}")
            else:
                # EnhancedRedisManager
                console.print("[cyan]   Using Enhanced Redis Manager with failover capabilities[/]")
            
            # Check if we can read/write to Redis
            try:
                test_key = "btc:news:test"
                if hasattr(news_feed.redis_client, 'set'):
                    news_feed.redis_client.set(test_key, "Connected", ex=60)
                    value = news_feed.redis_client.get(test_key)
                else:
                    news_feed.redis_client.execute_command('SET', test_key, "Connected", 'EX', 60)
                    value = news_feed.redis_client.execute_command('GET', test_key)
                    
                if value and (value == "Connected" or value.decode('utf-8') == "Connected"):
                    console.print("[green]✅ Redis read/write test successful[/]")
                else:
                    console.print("[yellow]⚠️ Redis read/write test returned unexpected value[/]")
            except Exception as e:
                console.print(f"[red]❌ Redis read/write test failed: {e}[/]")
        else:
            console.print("[red]❌ Not connected to Redis[/]")
        
        console.print()
    
    # Add custom keywords if provided
    if args.filter:
        news_feed.BTC_KEYWORDS.extend(args.filter)
    
    # Stream mode
    if args.stream:
        console.print(f"[bold green]Starting BTC news stream from {', '.join(args.sources)}...[/]")
        console.print("[yellow]Press Ctrl+C to exit[/]")
        news_feed.stream_news(args.sources, interval=args.interval, limit=args.limit)
        return
    
    # Generate ML dataset
    if args.train_data:
        console.print("[bold green]Generating ML training dataset from saved news data...[/]")
        news_feed.generate_ml_dataset()
        return
    
    # Default mode: fetch and display news
    all_entries = []
    
    for source in args.sources:
        console.print(f"[cyan]Fetching from {source}...[/]")
        entries = news_feed.fetch_news(source)
        all_entries.extend(entries)
    
    # Apply cosmic adjustments
    all_entries = news_feed.adjust_sentiment_with_cosmic_factors(all_entries)
    
    # Sort by publish date (newest first)
    all_entries.sort(key=lambda x: x['published'], reverse=True)
    
    # Display the news entries
    news_feed.display_news(all_entries, limit=args.limit)
    
    # Save if requested
    if args.save:
        news_feed.save_news(all_entries[:args.limit], label=args.label, format=args.format)

if __name__ == "__main__":
    main() 