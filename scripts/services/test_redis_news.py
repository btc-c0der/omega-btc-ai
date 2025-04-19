#!/usr/bin/env python3

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
import re
from collections import Counter
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn

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
parser.add_argument("--buzzwords", type=str, nargs="+", help="Specific buzzwords to track in articles")
args = parser.parse_args()

console = Console()

# Define buzzword categories with associated terms
BUZZWORD_CATEGORIES = {
    "bullish": [
        "rally", "surge", "soar", "uptrend", "breakout", "moon", "ath", "all-time high", 
        "bullish", "gains", "outperform", "record high", "adoption", "accumulation"
    ],
    "bearish": [
        "crash", "dip", "plunge", "downtrend", "correction", "bearish", "dump", 
        "sell-off", "losses", "underperform", "capitulation", "fear"
    ],
    "regulation": [
        "sec", "cftc", "regulation", "compliance", "legal", "lawsuit", "ban", "government",
        "regulatory", "authorities", "regulator", "policy", "treasury", "ruling", "court"
    ],
    "innovation": [
        "layer-2", "lightning", "scalability", "protocol", "upgrade", "technology", 
        "solution", "development", "launch", "rollup", "zkp", "zero-knowledge", "taproot",
        "ordinals", "inscriptions", "segwit", "schnorr", "soft fork", "hard fork"
    ],
    "adoption": [
        "adoption", "institutional", "etf", "mainstream", "corporate", "treasury", 
        "integration", "payment", "retail", "merchant", "accept", "spot etf", "custody"
    ],
    "defi": [
        "defi", "yield", "farming", "staking", "liquidity", "amm", "dex", "lending", 
        "borrowing", "protocol", "dao", "governance", "tvl", "swap"
    ],
    "nft": [
        "nft", "collectible", "digital art", "auction", "marketplace", "non-fungible", 
        "opensea", "token", "royalties", "metaverse", "virtual"
    ],
    "mining": [
        "mining", "miner", "hashrate", "difficulty", "asic", "block reward", "halving", 
        "energy", "renewable", "pool", "proof of work", "pow"
    ]
}

# User-provided custom buzzwords
CUSTOM_BUZZWORDS = args.buzzwords if args.buzzwords else []

def extract_buzzwords(title, description):
    """
    Extract buzzwords from news article text.
    
    Args:
        title: Article title
        description: Article description
    
    Returns:
        Dictionary with buzzword categories and matching words
    """
    text = (title + " " + description).lower()
    
    buzzword_matches = {}
    
    # Check each category
    for category, words in BUZZWORD_CATEGORIES.items():
        matches = []
        for word in words:
            # Use word boundary to match whole words
            pattern = r'\b' + re.escape(word) + r'\b'
            if re.search(pattern, text):
                matches.append(word)
        
        if matches:
            buzzword_matches[category] = matches
    
    # Check custom buzzwords
    if CUSTOM_BUZZWORDS:
        custom_matches = []
        for word in CUSTOM_BUZZWORDS:
            pattern = r'\b' + re.escape(word.lower()) + r'\b'
            if re.search(pattern, text):
                custom_matches.append(word)
        
        if custom_matches:
            buzzword_matches["custom"] = custom_matches
    
    return buzzword_matches

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
        
        # Display custom buzzwords if provided
        if CUSTOM_BUZZWORDS:
            console.print(f"[cyan]Tracking custom buzzwords: {', '.join(CUSTOM_BUZZWORDS)}[/]")
        
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
        
        # Extract buzzwords
        console.print("\n[bold cyan]Analyzing buzzwords and topics...[/]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task("[cyan]Processing buzzwords...", total=len(all_entries))
            
            for entry in all_entries:
                buzzwords = extract_buzzwords(entry['title'], entry['description'])
                entry['buzzwords'] = buzzwords
                progress.update(task, advance=1)
        
        # Count buzzword categories
        category_counts = Counter()
        buzzword_counts = Counter()
        
        for entry in all_entries:
            for category in entry.get('buzzwords', {}):
                category_counts[category] += 1
                for word in entry['buzzwords'][category]:
                    buzzword_counts[word] += 1
        
        # Display buzzword statistics
        if category_counts:
            console.print("\n[bold cyan]Buzzword Categories Found:[/]")
            
            # Create category distribution table
            category_table = Table(title="🔍 Topic Categories", border_style="cyan")
            category_table.add_column("Category", style="green")
            category_table.add_column("Count", justify="right", style="cyan")
            category_table.add_column("% of Articles", justify="right", style="cyan")
            
            for category, count in category_counts.most_common():
                percentage = count / len(all_entries) * 100
                category_style = "green" if category == "bullish" else "red" if category == "bearish" else "yellow"
                category_table.add_row(
                    Text(category.title(), style=category_style),
                    str(count),
                    f"{percentage:.1f}%"
                )
            
            console.print(category_table)
            
            # Display top buzzwords
            buzzword_table = Table(title="📊 Most Common Buzzwords", border_style="cyan")
            buzzword_table.add_column("Buzzword", style="yellow")
            buzzword_table.add_column("Count", justify="right", style="cyan")
            buzzword_table.add_column("Category", style="green")
            
            # Get the category for each buzzword
            buzzword_to_category = {}
            for category, words in BUZZWORD_CATEGORIES.items():
                for word in words:
                    buzzword_to_category[word] = category
            
            # Add custom buzzwords to the mapping
            for word in CUSTOM_BUZZWORDS:
                buzzword_to_category[word.lower()] = "custom"
            
            # Add top buzzwords to table
            for word, count in buzzword_counts.most_common(10):  # Show top 10
                category = buzzword_to_category.get(word, "unknown")
                category_style = "green" if category == "bullish" else "red" if category == "bearish" else "yellow"
                
                buzzword_table.add_row(
                    word,
                    str(count),
                    Text(category.title(), style=category_style)
                )
            
            console.print(buzzword_table)
        
        # Apply buzzword labels to news entries
        for entry in all_entries:
            categories = entry.get('buzzwords', {}).keys()
            if categories:
                # Add buzzword labels to title field
                labels = []
                for category in categories:
                    if category == "bullish":
                        labels.append("[green]BULLISH[/]")
                    elif category == "bearish":
                        labels.append("[red]BEARISH[/]")
                    elif category == "regulation":
                        labels.append("[blue]REG[/]")
                    elif category == "innovation":
                        labels.append("[purple]TECH[/]")
                    elif category == "adoption":
                        labels.append("[cyan]ADOPT[/]")
                    elif category == "defi":
                        labels.append("[yellow]DEFI[/]")
                    elif category == "nft":
                        labels.append("[magenta]NFT[/]")
                    elif category == "mining":
                        labels.append("[orange3]MINING[/]")
                    elif category == "custom":
                        labels.append("[bright_white]CUSTOM[/]")
                
                if labels:
                    entry['title_with_labels'] = f"{entry['title']} {' '.join(labels)}"
                else:
                    entry['title_with_labels'] = entry['title']
            else:
                entry['title_with_labels'] = entry['title']
        
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
        
        # Display the news with buzzword labels
        console.print("\n[bold cyan]Bitcoin News with Cosmic Sentiment and Topic Labels:[/]")
        
        # Create custom news display with buzzword information
        news_table = Table(title="🔥 OMEGA BTC NEWS FEED 🔥", width=console.width)
        news_table.add_column("Time", style="bright_blue")
        news_table.add_column("Source", style="bright_cyan")
        news_table.add_column("Title & Topics", style="white")
        news_table.add_column("Sentiment", justify="right")
        news_table.add_column("Moon Influence", justify="right")
        
        for i, entry in enumerate(all_entries[:args.limit]):
            # Format time
            time_str = entry['published'].strftime('%Y-%m-%d %H:%M')
            
            # Format sentiment
            sentiment_value = entry.get('cosmic_sentiment', entry['sentiment_score'])
            sentiment_label = entry.get('cosmic_label', entry['sentiment_label'])
            
            sentiment_text = f"{sentiment_label} ({sentiment_value:.2f})"
            if sentiment_label == "bullish":
                sentiment_style = "green"
            elif sentiment_label == "bearish":
                sentiment_style = "red"
            else:
                sentiment_style = "yellow"
            
            # Format moon influence
            moon_text = f"{moon_phase} ({moon_factor:+.2f})"
            
            # Add row to table
            news_table.add_row(
                time_str,
                entry['source'],
                entry['title_with_labels'],
                Text(sentiment_text, style=sentiment_style),
                Text(moon_text, style="bright_magenta")
            )
            
            # Add buzzword details for each entry
            if entry.get('buzzwords') and i < args.limit:
                buzzword_rows = []
                for category, words in entry['buzzwords'].items():
                    category_style = "green" if category == "bullish" else "red" if category == "bearish" else "yellow"
                    buzzword_rows.append(f"[{category_style}]{category.title()}:[/] {', '.join(words)}")
                
                if buzzword_rows:
                    buzzword_text = " | ".join(buzzword_rows)
                    news_table.add_row("", "", Text(f"Keywords: {buzzword_text}", style="dim"), "", "")
        
        console.print(news_table)
        
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
        
        # Save to file with buzzword data
        console.print("\n[bold cyan]Saving news to file...[/]")
        
        # Prepare data for saving with buzzword info
        for entry in all_entries:
            # Convert buzzwords dict to string for CSV storage
            if 'buzzwords' in entry:
                buzzword_str = "; ".join([
                    f"{category}: {', '.join(words)}" 
                    for category, words in entry['buzzwords'].items()
                ])
                entry['buzzword_categories'] = buzzword_str
        
        output_file = news_feed.save_news(all_entries[:args.limit], format="csv")
        console.print(f"[green]✅ News saved to {output_file}[/]")
        
        # Final status message
        result_panel = Panel(
            f"[green]✅ BTC News Test Completed Successfully![/]\n\n"
            f"[cyan]Total Articles:[/] {len(all_entries)}\n"
            f"[cyan]Saved To:[/] {output_file}\n"
            f"[cyan]Moon Phase:[/] {moon_phase} ({moon_factor:+.2f})\n"
            f"[cyan]Top Topic:[/] {category_counts.most_common(1)[0][0].title() if category_counts else 'None'}\n"
            f"[cyan]Top Buzzword:[/] {buzzword_counts.most_common(1)[0][0] if buzzword_counts else 'None'}\n"
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