#!/usr/bin/env python3
"""
OMEGA BTC AI - BTC News Feed Module
===================================

News feed CLI and library for retrieving, analyzing and storing cryptocurrency news
with sentiment analysis and machine learning capabilities.

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

import os
import json
import time
import asyncio
import logging
import argparse
import threading
import csv
import math
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple
from pathlib import Path

import feedparser
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from textblob import TextBlob
import pandas as pd
import nltk
import redis

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("btc-newsfeed")

# Constants
LOG_PREFIX = os.getenv("LOG_PREFIX", "🔱 OMEGA BTC NEWS")
DEFAULT_DATA_DIR = os.getenv("DATA_DIR", "data")
DEFAULT_REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL", "300"))  # 5 minutes
ENABLE_REDIS = os.getenv("ENABLE_REDIS", "false").lower() == "true"

# Rich console for pretty output
console = Console()

class BtcNewsFeed:
    """BTC News Feed with sentiment analysis and ML dataset generation."""
    
    # Default RSS feeds for cryptocurrency news
    DEFAULT_FEEDS = {
        "cryptonews": "https://cryptonews.com/news/feed",
        "cointelegraph": "https://cointelegraph.com/rss",
        "decrypt": "https://decrypt.co/feed",
        "coindesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "bitcoinmagazine": "https://bitcoinmagazine.com/.rss/full/",
        "theblock": "https://www.theblock.co/rss.xml",
        "newsbtc": "https://www.newsbtc.com/feed/",
        "bitcoinist": "https://bitcoinist.com/feed/",
        "ambcrypto": "https://ambcrypto.com/feed/"
    }
    
    # Keywords for filtering BTC-related news
    BTC_KEYWORDS = [
        "bitcoin", "btc", "satoshi", "lightning network", "crypto", "blockchain", 
        "cryptocurrency", "digital gold", "bitcoin price", "btcusd", "hodl",
        "nakamoto", "digital currency", "bitcoin halving", "bitcoin mining"
    ]
    
    def __init__(
        self, 
        data_dir: str = DEFAULT_DATA_DIR,
        feeds: Optional[Dict[str, str]] = None,
        redis_client: Optional[redis.Redis] = None,
        refresh_interval: int = DEFAULT_REFRESH_INTERVAL
    ):
        """
        Initialize the BTC News Feed.
        
        Args:
            data_dir: Directory to store news datasets
            feeds: Dictionary of RSS feeds to monitor
            redis_client: Redis client for caching (optional)
            refresh_interval: Time in seconds between feed refreshes
        """
        self.data_dir = data_dir
        self.feeds = feeds or self.DEFAULT_FEEDS
        self.refresh_interval = refresh_interval
        self.redis_client = redis_client
        self.last_update = {}
        self.streaming = False
        
        # Create data directory if it doesn't exist
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)
        
        # Initialize NLTK for sentiment analysis
        try:
            nltk.data.find('vader_lexicon')
        except LookupError:
            logger.info(f"{LOG_PREFIX} - Downloading NLTK data for sentiment analysis")
            nltk.download('vader_lexicon', quiet=True)
            nltk.download('punkt', quiet=True)
    
    def _connect_redis(self) -> bool:
        """Connect to Redis if enabled."""
        if not ENABLE_REDIS:
            return False
            
        try:
            from omega_ai.utils.enhanced_redis_manager import EnhancedRedisManager
            self.redis_client = EnhancedRedisManager(
                use_failover=True,
                sync_on_reconnect=True
            )
            return True
        except (ImportError, Exception) as e:
            logger.warning(f"{LOG_PREFIX} - Redis connection failed: {e}")
            return False
    
    def fetch_news(self, source: str) -> List[Dict[str, Any]]:
        """
        Fetch news from specified RSS source.
        
        Args:
            source: Key name of feed to fetch from self.feeds
            
        Returns:
            List of news entries with metadata
        """
        feed_url = self.feeds.get(source)
        if not feed_url:
            console.print(f"[red]Unknown source:[/] {source}")
            return []

        try:
            feed = feedparser.parse(feed_url)
            entries = []
            
            for entry in feed.entries:
                # Extract and format data
                title = entry.title
                link = entry.link
                published = datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else datetime.now()
                
                # Get description if available
                description = ""
                if hasattr(entry, 'summary'):
                    description = entry.summary
                elif hasattr(entry, 'description'):
                    description = entry.description
                
                # Strip HTML tags
                description = re.sub(r'<[^>]+>', '', description)
                
                # Check if entry is BTC related
                if not self._is_btc_related(title, description):
                    continue
                
                # Perform sentiment analysis
                sentiment_score, sentiment_label = self._analyze_sentiment(title, description)
                
                entries.append({
                    'title': title,
                    'link': link,
                    'description': description,
                    'published': published,
                    'source': source,
                    'sentiment_score': sentiment_score,
                    'sentiment_label': sentiment_label
                })
            
            # Save the last update time
            self.last_update[source] = datetime.now()
            
            return entries
            
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error fetching {source}: {e}")
            return []
    
    def _is_btc_related(self, title: str, description: str) -> bool:
        """
        Check if an article is related to Bitcoin.
        
        Args:
            title: Article title
            description: Article description
            
        Returns:
            True if the article is Bitcoin-related
        """
        text = (title + " " + description).lower()
        return any(keyword.lower() in text for keyword in self.BTC_KEYWORDS)
    
    def _analyze_sentiment(self, title: str, description: str = "") -> Tuple[float, str]:
        """
        Analyze sentiment of news article.
        
        Args:
            title: Article title
            description: Article description
            
        Returns:
            Tuple of (sentiment_score, sentiment_label)
        """
        # Combine title and description, with more weight to the title
        text = title + " " + description
        
        try:
            # TextBlob sentiment analysis
            analysis = TextBlob(text)
            score = analysis.sentiment.polarity
            
            # Map score to label
            if score > 0.2:
                label = "bullish"
            elif score < -0.2:
                label = "bearish"
            else:
                label = "neutral"
                
            return score, label
            
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Sentiment analysis error: {e}")
            return 0.0, "neutral"
    
    def _get_moon_phase_sentiment(self) -> Tuple[str, float]:
        """Get current moon phase and its sentiment influence factor."""
        # Calculate moon phase (0-1)
        days_since_new_moon = 29.53059 # Synodic month length
        d = datetime.now()
        
        # Approximate moon phase calculation
        lunar_cycle = (d.year + ((d.month - 1) / 12) + (d.day / 365.25)) * 12.3685
        phase = lunar_cycle % 1
        
        # Map phase to label
        if phase < 0.03:
            return "New Moon", 0.1  # Slightly bullish
        elif phase < 0.25:
            return "Waxing Crescent", 0.3  # Moderately bullish
        elif phase < 0.28:
            return "First Quarter", 0.5  # Strongly bullish
        elif phase < 0.47:
            return "Waxing Gibbous", 0.2  # Slightly bullish
        elif phase < 0.53:
            return "Full Moon", -0.1  # Slightly bearish
        elif phase < 0.72:
            return "Waning Gibbous", -0.3  # Moderately bearish
        elif phase < 0.78:
            return "Last Quarter", -0.5  # Strongly bearish
        elif phase < 0.97:
            return "Waning Crescent", -0.2  # Slightly bearish
        else:
            return "New Moon", 0.1  # Slightly bullish
    
    def _get_fibonacci_bias(self) -> float:
        """Calculate Fibonacci-based sentiment bias based on day of month."""
        day = datetime.now().day
        
        # Map day to Fibonacci sequence position
        fib_sequence = [1, 2, 3, 5, 8, 13, 21]
        if day in fib_sequence:
            return 0.2  # Bullish on Fibonacci days
        
        return 0.0
    
    def adjust_sentiment_with_cosmic_factors(self, entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Adjust sentiment scores based on cosmic factors."""
        moon_phase, moon_factor = self._get_moon_phase_sentiment()
        fib_factor = self._get_fibonacci_bias()
        
        for entry in entries:
            # Apply cosmic adjustment to sentiment
            cosmic_score = entry['sentiment_score'] + moon_factor + fib_factor
            
            # Recalculate label based on adjusted score
            if cosmic_score > 0.2:
                cosmic_label = "bullish"
            elif cosmic_score < -0.2:
                cosmic_label = "bearish"
            else:
                cosmic_label = "neutral"
            
            # Add cosmic factors to entry
            entry['cosmic_score'] = cosmic_score
            entry['cosmic_label'] = cosmic_label
            entry['moon_phase'] = moon_phase
            entry['moon_factor'] = moon_factor
            entry['fibonacci_factor'] = fib_factor
        
        return entries
    
    def save_news(self, entries: List[Dict[str, Any]], label: Optional[str] = None, format: str = "csv") -> str:
        """
        Save news entries to file for training data.
        
        Args:
            entries: List of news entries
            label: Optional override for sentiment label
            format: Output format (csv or json)
            
        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format.lower() == "json":
            filename = Path(self.data_dir) / f"btc_news_{timestamp}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(entries, f, indent=2, default=str)
        else:
            filename = Path(self.data_dir) / f"btc_news_{timestamp}.csv"
            with open(filename, "w", encoding="utf-8", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["title", "description", "link", "published", "source", 
                                 "sentiment_score", "sentiment_label", "cosmic_score", 
                                 "cosmic_label", "moon_phase", "user_label"])
                
                for entry in entries:
                    writer.writerow([
                        entry['title'],
                        entry['description'][:200],  # Truncate description
                        entry['link'],
                        entry['published'],
                        entry['source'],
                        entry['sentiment_score'],
                        entry['sentiment_label'],
                        entry.get('cosmic_score', entry['sentiment_score']),
                        entry.get('cosmic_label', entry['sentiment_label']),
                        entry.get('moon_phase', ''),
                        label or ''
                    ])
        
        console.print(f"[green]Saved {len(entries)} entries to {filename}[/]")
        return str(filename)
    
    def display_news(self, entries: List[Dict[str, Any]], limit: int = 10) -> None:
        """
        Display news entries in a rich table.
        
        Args:
            entries: List of news entries
            limit: Maximum number of entries to display
        """
        table = Table(title="🔥 OMEGA BTC NEWS FEED 🔥")
        table.add_column("Time", justify="right", style="cyan")
        table.add_column("Source", style="magenta")
        table.add_column("Title", style="white")
        table.add_column("Sentiment", justify="center")
        table.add_column("Moon Influence", justify="center", style="bright_cyan")

        for entry in entries[:limit]:
            published = entry['published'].strftime('%Y-%m-%d %H:%M')
            
            # Style sentiment based on label
            sentiment_text = f"{entry['sentiment_label']} ({entry['sentiment_score']:.2f})"
            if entry['sentiment_label'] == 'bullish':
                sentiment_style = "[green]" + sentiment_text + "[/]"
            elif entry['sentiment_label'] == 'bearish':
                sentiment_style = "[red]" + sentiment_text + "[/]"
            else:
                sentiment_style = "[yellow]" + sentiment_text + "[/]"
            
            # Moon phase info if available
            moon_info = entry.get('moon_phase', '')
            if moon_info and entry.get('moon_factor'):
                factor = entry['moon_factor']
                if factor > 0:
                    moon_info += f" (+{factor:.2f})"
                else:
                    moon_info += f" ({factor:.2f})"
            
            table.add_row(
                published, 
                entry['source'], 
                entry['title'], 
                sentiment_style,
                moon_info
            )

        console.print(table)
    
    def stream_news(self, sources: List[str], interval: int = 300, limit: int = 10) -> None:
        """
        Stream news continuously with periodic updates.
        
        Args:
            sources: List of source keys to fetch from
            interval: Update interval in seconds
            limit: Maximum number of entries to display
        """
        if not sources:
            sources = list(self.feeds.keys())[:3]  # Default to first 3 sources
        
        self.streaming = True
        seen_links = set()
        all_entries = []
        
        try:
            with Live(Panel("Loading news feed..."), refresh_per_second=4) as live:
                while self.streaming:
                    new_entries = []
                    
                    # Create fetch status display
                    status_table = Table.grid()
                    status_table.add_column()
                    status_table.add_row(Text("🔄 Refreshing OMEGA BTC News Feed...", style="bold cyan"))
                    
                    # Update live display
                    live.update(status_table)
                    
                    # Fetch from all sources
                    for source in sources:
                        entries = self.fetch_news(source)
                        
                        # Filter out already seen entries
                        for entry in entries:
                            if entry['link'] not in seen_links:
                                seen_links.add(entry['link'])
                                new_entries.append(entry)
                    
                    # Apply cosmic adjustments
                    new_entries = self.adjust_sentiment_with_cosmic_factors(new_entries)
                    
                    # Add new entries to the list
                    all_entries = new_entries + all_entries
                    
                    # Keep only the most recent entries
                    all_entries = all_entries[:100]
                    
                    # Display news table
                    if all_entries:
                        # First display cosmic overview
                        moon_phase, moon_factor = self._get_moon_phase_sentiment()
                        fib_factor = self._get_fibonacci_bias()
                        
                        cosmic_panel = Table.grid()
                        cosmic_panel.add_column()
                        cosmic_panel.add_row(Text(f"🔱 OMEGA BTC NEWS PROPHECY TRANSMISSION 🔱", style="bold yellow"))
                        cosmic_panel.add_row(Text(f"Moon Phase: {moon_phase} (Sentiment Factor: {moon_factor:+.2f})", 
                                               style="bright_cyan"))
                        cosmic_panel.add_row(Text(f"Fibonacci Alignment: {fib_factor:+.2f}", 
                                               style="bright_magenta"))
                        cosmic_panel.add_row("")
                        
                        live.update(cosmic_panel)
                        time.sleep(1)  # Dramatic pause
                        
                        # Create and display the news table
                        table = Table(title="🔥 OMEGA BTC LIVE NEWS FEED 🔥")
                        table.add_column("Time", justify="right", style="cyan")
                        table.add_column("Source", style="magenta")
                        table.add_column("Title", style="white")
                        table.add_column("Sentiment", justify="center")
                        table.add_column("Cosmic", justify="center", style="bright_yellow")

                        for entry in all_entries[:limit]:
                            published = entry['published'].strftime('%Y-%m-%d %H:%M')
                            
                            # Style sentiment based on label
                            sentiment_text = f"{entry['sentiment_score']:.2f}"
                            cosmic_text = f"{entry.get('cosmic_score', entry['sentiment_score']):.2f}"
                            
                            if entry['sentiment_label'] == 'bullish':
                                sentiment_style = "[green]" + sentiment_text + "[/]"
                            elif entry['sentiment_label'] == 'bearish':
                                sentiment_style = "[red]" + sentiment_text + "[/]"
                            else:
                                sentiment_style = "[yellow]" + sentiment_text + "[/]"
                                
                            cosmic_label = entry.get('cosmic_label', entry['sentiment_label'])
                            if cosmic_label == 'bullish':
                                cosmic_style = "[green]" + cosmic_text + "[/]"
                            elif cosmic_label == 'bearish':
                                cosmic_style = "[red]" + cosmic_text + "[/]"
                            else:
                                cosmic_style = "[yellow]" + cosmic_text + "[/]"
                            
                            table.add_row(
                                published, 
                                entry['source'], 
                                entry['title'], 
                                sentiment_style,
                                cosmic_style
                            )
                            
                        # Update the live display with the table
                        live.update(Panel(table))
                        
                        # Store in Redis if available
                        if self.redis_client:
                            self._store_in_redis(all_entries[:20])
                    else:
                        live.update(Panel("No BTC-related news found. Waiting for next update..."))
                    
                    # Wait for next update
                    if interval > 10:
                        wait_message = f"Next update in {interval} seconds..."
                        for i in range(interval, 0, -5):
                            live.update(Panel(f"{table}\n\n{wait_message.replace(str(interval), str(i))}"))
                            time.sleep(5)
                    else:
                        time.sleep(interval)
                    
        except KeyboardInterrupt:
            console.print("[yellow]News stream interrupted by user. Exiting...[/]")
            self.streaming = False
    
    def _store_in_redis(self, entries: List[Dict[str, Any]]) -> None:
        """Store news entries in Redis."""
        if not self.redis_client:
            return
            
        try:
            # Store entries as JSON
            for i, entry in enumerate(entries):
                key = f"btc:news:{datetime.now().strftime('%Y%m%d')}:{i}"
                
                # Serialize datetime objects
                entry_copy = entry.copy()
                entry_copy['published'] = entry_copy['published'].isoformat()
                
                self.redis_client.set(key, json.dumps(entry_copy), ex=86400)  # Expire after 1 day
                
            # Store aggregated sentiment
            sentiment_scores = [e['sentiment_score'] for e in entries]
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
            
            self.redis_client.set("btc:news:sentiment:latest", str(avg_sentiment), ex=86400)
            self.redis_client.set("btc:news:count", str(len(entries)), ex=86400)
            self.redis_client.set("btc:news:last_update", datetime.now().isoformat(), ex=86400)
            
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Redis storage error: {e}")
    
    def generate_ml_dataset(self, output_file: Optional[str] = None) -> str:
        """
        Generate a machine learning dataset from saved news data.
        
        Args:
            output_file: Optional output file path
            
        Returns:
            Path to the generated dataset file
        """
        if not output_file:
            output_file = Path(self.data_dir) / f"btc_news_ml_dataset_{datetime.now().strftime('%Y%m%d')}.csv"
        
        # Find all CSV files in the data directory
        data_files = list(Path(self.data_dir).glob("btc_news_*.csv"))
        
        if not data_files:
            console.print("[yellow]No news data files found for ML dataset generation[/]")
            return ""
        
        try:
            # Read and combine all data files
            dfs = []
            for file in data_files:
                df = pd.read_csv(file)
                dfs.append(df)
            
            if not dfs:
                console.print("[yellow]No valid data found in news files[/]")
                return ""
                
            # Combine all dataframes
            combined_df = pd.concat(dfs, ignore_index=True)
            
            # Drop duplicates
            combined_df.drop_duplicates(subset=['title', 'link'], inplace=True)
            
            # Prioritize user labels if available
            combined_df['final_label'] = combined_df['user_label'].fillna(combined_df['cosmic_label'])
            combined_df['final_label'] = combined_df['final_label'].fillna(combined_df['sentiment_label'])
            
            # Select columns for the final dataset
            ml_df = combined_df[['title', 'description', 'final_label']]
            
            # Save the ML dataset
            ml_df.to_csv(output_file, index=False)
            
            console.print(f"[green]Generated ML dataset with {len(ml_df)} entries at {output_file}[/]")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error generating ML dataset: {e}")
            return ""

def display_rasta_banner():
    """Display a Rastafarian-themed banner."""
    banner = """
    ╭─────────────────────────────────────────────────────╮
    │                                                     │
    │  🔥🔥🔥 OMEGA BTC NEWS PROPHECY TRANSMISSION 🔥🔥🔥  │
    │                                                     │
    │        JAH JAH BLESS THE DIVINE DATA FLOW           │
    │                                                     │
    ╰─────────────────────────────────────────────────────╯
    """
    console.print(Panel.fit(banner, style="green on black"))

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
    
    args = parser.parse_args()
    
    # Display banner
    display_rasta_banner()
    
    # Create the news feed instance
    news_feed = BtcNewsFeed(data_dir=args.data_dir)
    
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
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        for source in args.sources:
            task = progress.add_task(f"[cyan]Fetching from {source}...", total=1)
            entries = news_feed.fetch_news(source)
            all_entries.extend(entries)
            progress.update(task, completed=1)
    
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