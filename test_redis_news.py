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
from rich.text import Text

# Ensure the package is in the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'deployment/digitalocean/btc_live_feed_v3/src')
sys.path.insert(0, src_path)

# Parse command line arguments
parser = argparse.ArgumentParser(description="Test BTC News Feed functionality")
parser.add_argument("--nodatabase", action="store_true", help="Run without database connection")
parser.add_argument("--source", type=str, default="cointelegraph", 
                    choices=["cointelegraph", "decrypt", "coindesk", "bitcoinmagazine", "theblock", 
                             "newsbtc", "bitcoinist", "ambcrypto", "cryptonews", "all"],
                    help="News source to fetch from (or 'all' for all sources)")
parser.add_argument("--limit", type=int, default=5, help="Maximum number of news items to display")
parser.add_argument("--filter", type=str, nargs="+", help="Additional keywords to filter news by")
args = parser.parse_args()

console = Console()

def run_test():
    """Run the BTC News Feed test."""
    try:
        # Import the module
        from omega_ai.data_feed.newsfeed import BtcNewsFeed, display_rasta_banner
        
        # Display banner
        display_rasta_banner()
        
        if args.source == "all":
            console.print("[bold cyan]Testing BTC News Feed with all sources[/]")
        else:
            console.print(f"[bold cyan]Testing BTC News Feed with source: {args.source}[/]")
        
        # Create news feed instance
        news_feed = BtcNewsFeed(data_dir="./data", use_redis=not args.nodatabase)
        
        # Add custom filter keywords if provided
        if args.filter:
            console.print(f"[cyan]Adding custom filter keywords: {', '.join(args.filter)}[/]")
            news_feed.BTC_KEYWORDS.extend(args.filter)
        
        # Display database status
        if args.nodatabase:
            console.print("[yellow]Running in no-database mode. Redis connectivity disabled.[/]")
        elif news_feed.redis_client:
            console.print("[green]✅ Connected to Redis database[/]")
        else:
            console.print("[red]❌ Not connected to Redis database (but was attempted)[/]")
        
        # Fetch news
        console.print("\n[bold cyan]Fetching Bitcoin news...[/]")
        
        all_entries = []
        
        if args.source == "all":
            # Fetch from all sources
            sources = list(news_feed.DEFAULT_FEEDS.keys())
            
            # Create a progress display
            sources_table = Table.grid(padding=(0, 1))
            sources_table.add_column()
            sources_table.add_row(Text("Sources to check:", style="bold"))
            
            for source in sources:
                sources_table.add_row(Text(f"• {source}", style="cyan"))
            
            console.print(sources_table)
            
            # Fetch from each source
            for source in sources:
                console.print(f"[cyan]Fetching from {source}...[/]")
                entries = news_feed.fetch_news(source)
                console.print(f"[green]Found {len(entries)} Bitcoin-related entries")
                all_entries.extend(entries)
        else:
            # Fetch from specified source
            console.print(f"[cyan]Fetching from {args.source}...[/]")
            all_entries = news_feed.fetch_news(args.source)
        
        if not all_entries:
            console.print("[yellow]No news entries found. Check your internet connection or try a different source.[/]")
            return
        
        console.print(f"[green]✅ Found {len(all_entries)} total Bitcoin news entries[/]")
        
        # Sort by date (newest first)
        all_entries.sort(key=lambda x: x['published'], reverse=True)
        
        # Apply cosmic adjustments
        console.print("\n[bold cyan]Applying cosmic sentiment adjustments...[/]")
        all_entries = news_feed.adjust_sentiment_with_cosmic_factors(all_entries)
        
        # Display the cosmic factors
        moon_phase, moon_factor = news_feed._get_moon_phase_sentiment()
        fib_factor = news_feed._get_fibonacci_bias()
        
        cosmic_table = Table(title="🌙 Cosmic Factors Affecting Today's Sentiment")
        cosmic_table.add_column("Factor", style="cyan")
        cosmic_table.add_column("Value", style="green")
        cosmic_table.add_column("Impact", style="yellow")
        
        cosmic_table.add_row("Moon Phase", moon_phase, "Sentiment modifier for all news")
        cosmic_table.add_row("Moon Factor", f"{moon_factor:+.2f}", 
                           "bullish" if moon_factor > 0 else "bearish" if moon_factor < 0 else "neutral")
        cosmic_table.add_row("Fibonacci Day", f"{fib_factor:+.2f}", 
                           "active" if fib_factor > 0 else "inactive")
        
        console.print(cosmic_table)
        
        # Calculate sentiment distribution
        sentiment_counts = {"bullish": 0, "bearish": 0, "neutral": 0}
        cosmic_sentiment_counts = {"bullish": 0, "bearish": 0, "neutral": 0}
        
        for entry in all_entries:
            sentiment_counts[entry['sentiment_label']] += 1
            cosmic_sentiment_counts[entry.get('cosmic_label', entry['sentiment_label'])] += 1
        
        # Display sentiment distribution
        sentiment_table = Table(title="Sentiment Distribution")
        sentiment_table.add_column("Category", style="cyan")
        sentiment_table.add_column("Raw Count", justify="right")
        sentiment_table.add_column("Raw %", justify="right")
        sentiment_table.add_column("Cosmic Count", justify="right")
        sentiment_table.add_column("Cosmic %", justify="right")
        
        total = len(all_entries)
        
        for label in ["bullish", "bearish", "neutral"]:
            raw_count = sentiment_counts[label]
            cosmic_count = cosmic_sentiment_counts[label]
            
            label_style = "green" if label == "bullish" else "red" if label == "bearish" else "yellow"
            
            sentiment_table.add_row(
                Text(label.capitalize(), style=label_style),
                str(raw_count),
                f"{raw_count/total*100:.1f}%",
                str(cosmic_count),
                f"{cosmic_count/total*100:.1f}%"
            )
        
        console.print(sentiment_table)
        
        # Display the news
        console.print("\n[bold cyan]Bitcoin News with Cosmic Sentiment Analysis:[/]")
        news_feed.display_news(all_entries[:args.limit])
        
        # Store in Redis if enabled
        if not args.nodatabase and news_feed.redis_client:
            console.print("\n[bold cyan]Storing news in Redis...[/]")
            news_feed._store_in_redis(all_entries[:args.limit])
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
        output_file = news_feed.save_news(all_entries[:args.limit], format="csv")
        console.print(f"[green]✅ News saved to {output_file}[/]")
        
        # Final status message
        result_panel = Panel(
            f"[green]✅ BTC News Test Completed Successfully![/]\n\n"
            f"[cyan]Total Articles:[/] {len(all_entries)}\n"
            f"[cyan]Saved To:[/] {output_file}\n"
            f"[cyan]Moon Phase:[/] {moon_phase} ({moon_factor:+.2f})\n"
            f"[cyan]Market Sentiment:[/] "
            f"{'[green]Bullish' if cosmic_sentiment_counts['bullish'] > cosmic_sentiment_counts['bearish'] else '[red]Bearish' if cosmic_sentiment_counts['bearish'] > cosmic_sentiment_counts['bullish'] else '[yellow]Neutral'}",
            title="OMEGA BTC News Oracle Summary",
            border_style="green"
        )
        console.print("\n", result_panel)
        
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