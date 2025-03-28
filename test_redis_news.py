#!/usr/bin/env python3
"""
OMEGA BTC AI - BTC News Feed Test
=================================

This script demonstrates the BTC News Feed module functionality.
Supports running without database connection using the --nodatabase flag.

Copyright (c) 2025 OMEGA-BTC-AI - Licensed under the GPU License
"""

import os
import sys
import time
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Ensure the package is in the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'deployment/digitalocean/btc_live_feed_v3/src')
sys.path.insert(0, src_path)

# Parse command line arguments
parser = argparse.ArgumentParser(description="Test BTC News Feed functionality")
parser.add_argument("--nodatabase", action="store_true", help="Run without database connection")
parser.add_argument("--source", type=str, default="cointelegraph", help="News source to fetch from")
parser.add_argument("--limit", type=int, default=5, help="Maximum number of news items to display")
args = parser.parse_args()

console = Console()

def run_test():
    """Run the BTC News Feed test."""
    try:
        # Import the module
        from omega_ai.data_feed.newsfeed import BtcNewsFeed, display_rasta_banner
        
        # Display banner
        display_rasta_banner()
        
        console.print(f"[bold cyan]Testing BTC News Feed with source: {args.source}[/]")
        
        # Create news feed instance
        news_feed = BtcNewsFeed(data_dir="./data", use_redis=not args.nodatabase)
        
        # Display database status
        if args.nodatabase:
            console.print("[yellow]Running in no-database mode. Redis connectivity disabled.[/]")
        elif news_feed.redis_client:
            console.print("[green]✅ Connected to Redis database[/]")
        else:
            console.print("[red]❌ Not connected to Redis database (but was attempted)[/]")
        
        # Fetch news
        console.print(f"\n[bold cyan]Fetching news from {args.source}...[/]")
        entries = news_feed.fetch_news(args.source)
        
        if not entries:
            console.print("[yellow]No news entries found. Check your internet connection or try a different source.[/]")
            return
        
        console.print(f"[green]✅ Found {len(entries)} news entries[/]")
        
        # Apply cosmic adjustments
        console.print("\n[bold cyan]Applying cosmic sentiment adjustments...[/]")
        entries = news_feed.adjust_sentiment_with_cosmic_factors(entries)
        
        # Display the cosmic factors
        moon_phase, moon_factor = news_feed._get_moon_phase_sentiment()
        fib_factor = news_feed._get_fibonacci_bias()
        
        cosmic_table = Table(title="Cosmic Factors")
        cosmic_table.add_column("Factor", style="cyan")
        cosmic_table.add_column("Value", style="green")
        
        cosmic_table.add_row("Moon Phase", moon_phase)
        cosmic_table.add_row("Moon Factor", f"{moon_factor:+.2f}")
        cosmic_table.add_row("Fibonacci Factor", f"{fib_factor:+.2f}")
        
        console.print(cosmic_table)
        
        # Display the news
        console.print("\n[bold cyan]Bitcoin News with Cosmic Sentiment Analysis:[/]")
        news_feed.display_news(entries[:args.limit])
        
        # Store in Redis if enabled
        if not args.nodatabase and news_feed.redis_client:
            console.print("\n[bold cyan]Storing news in Redis...[/]")
            news_feed._store_in_redis(entries[:args.limit])
            console.print("[green]✅ News entries stored in Redis[/]")
            
            # Display example Redis keys
            try:
                if hasattr(news_feed.redis_client, 'keys'):
                    keys = news_feed.redis_client.keys("btc:news:*")
                    if keys and len(keys) > 0:
                        if isinstance(keys[0], bytes):
                            keys = [k.decode('utf-8') for k in keys]
                        
                        keys_table = Table(title="Sample Redis Keys")
                        keys_table.add_column("Key", style="cyan")
                        
                        for key in keys[:5]:  # Show up to 5 keys
                            keys_table.add_row(key)
                        
                        console.print(keys_table)
            except Exception as e:
                console.print(f"[yellow]Could not list Redis keys: {e}[/]")
        
        # Save to file
        console.print("\n[bold cyan]Saving news to file...[/]")
        output_file = news_feed.save_news(entries[:args.limit], format="csv")
        console.print(f"[green]✅ News saved to {output_file}[/]")
        
        console.print("\n[bold green]✅ Test completed successfully![/]")
        
    except ImportError as e:
        console.print(f"[bold red]Error importing BtcNewsFeed: {e}[/]")
        console.print("Make sure you've installed the required packages:")
        console.print("  pip install -e ./deployment/digitalocean/btc_live_feed_v3")
        console.print("  pip install feedparser rich textblob pandas nltk")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/]")
        sys.exit(1)

if __name__ == "__main__":
    run_test() 