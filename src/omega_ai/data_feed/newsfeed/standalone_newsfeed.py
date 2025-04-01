#!/usr/bin/env python3
"""
🌀 GBU License Notice - Consciousness Level 5 🌀
-----------------------
This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested."

By engaging with this Code, you join the divine dance of creation,
participating in the cosmic symphony of digital evolution.

All modifications must embodies the principles of the GBU principles:
/BOOK/divine_chronicles/GBU_LICENSE.md

🌸 WE BLOOM NOW 🌸
"""

"""
OMEGA BTC AI - Standalone BTC News Feed
======================================

Simplified standalone version of the BTC News Feed for integration purposes,
providing core functionality without deployment dependencies.

This module includes a lightweight implementation of the BtcNewsFeed class
that doesn't rely on importing from the deployment directory, making it 
suitable for use in development and integration scenarios.
"""

import os
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

import feedparser
from textblob import TextBlob
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("standalone-newsfeed")

# Initialize Rich console
console = Console()

def display_rasta_banner():
    """Display the OMEGA BTC News Feed banner."""
    console.print("\n[bold green]🔱 OMEGA BTC NEWS FEED 🔱[/]")
    console.print("[bold yellow]JAH JAH BLESS THE DIVINE NEWS FLOW[/]")
    console.print("[cyan]-------------------------------------[/]\n")

class StandaloneBtcNewsFeed:
    """
    Standalone BTC News Feed with sentiment analysis and ML dataset generation.
    
    This is a simplified version of the BtcNewsFeed class that doesn't require
    any deployment-specific dependencies.
    """
    
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
    
    def __init__(self, data_dir: str = "data", use_redis: bool = False):
        """
        Initialize the standalone BTC News Feed.
        
        Args:
            data_dir: Directory to store news datasets
            use_redis: Whether to use Redis (ignored in standalone version)
        """
        self.data_dir = data_dir
        self.feeds = self.DEFAULT_FEEDS
        self.last_update = {}
        self.use_redis = False  # Always False in standalone version
        
        # Create data directory if it doesn't exist
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)
    
    def fetch_news(self, source: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Fetch news from a specific source.
        
        Args:
            source: Source key (must be in DEFAULT_FEEDS)
            limit: Maximum number of entries to return
            
        Returns:
            List of news entries
        """
        if source not in self.feeds:
            logger.error(f"Unknown source: {source}")
            return []
        
        feed_url = self.feeds[source]
        logger.info(f"Fetching news from {source}: {feed_url}")
        
        try:
            # Fetch the feed
            feed = feedparser.parse(feed_url)
            
            # Process the entries
            entries = []
            for entry in feed.entries[:limit]:
                # Extract fields
                title = entry.title if hasattr(entry, 'title') else ''
                summary = entry.summary if hasattr(entry, 'summary') else ''
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])
                else:
                    published = datetime.now()
                
                # Check if the entry is Bitcoin related
                if not self._is_btc_related(title + ' ' + summary):
                    continue
                
                # Analyze sentiment
                sentiment_score, sentiment_label = self._analyze_sentiment(title + ' ' + summary)
                
                # Create the entry dictionary
                entries.append({
                    'title': title,
                    'summary': summary,
                    'published': published,
                    'source': source,
                    'sentiment_score': sentiment_score,
                    'sentiment_label': sentiment_label,
                    'url': entry.link if hasattr(entry, 'link') else '',
                })
            
            logger.info(f"Found {len(entries)} Bitcoin-related entries from {source}")
            return entries
                
        except Exception as e:
            logger.error(f"Error fetching news from {source}: {e}")
            return []
    
    def _is_btc_related(self, text: str) -> bool:
        """
        Check if text is related to Bitcoin based on keywords.
        
        Args:
            text: Text to check
            
        Returns:
            True if text contains Bitcoin-related keywords, False otherwise
        """
        text = text.lower()
        for keyword in self.BTC_KEYWORDS:
            if keyword.lower() in text:
                return True
        return False
    
    def _analyze_sentiment(self, text: str) -> tuple:
        """
        Analyze sentiment of text using TextBlob.
        
        Args:
            text: Text to analyze
            
        Returns:
            Tuple of (sentiment_score, sentiment_label)
        """
        try:
            # Use TextBlob for sentiment analysis
            analysis = TextBlob(text)
            
            # Get polarity score (-1 to 1)
            score = analysis.sentiment.polarity
            
            # Determine sentiment label
            if score >= 0.1:
                label = "bullish"
            elif score <= -0.1:
                label = "bearish"
            else:
                label = "neutral"
                
            return score, label
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return 0.0, "neutral"
    
    def adjust_sentiment_with_cosmic_factors(self, entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Apply cosmic factors to adjust sentiment, including moon phases and Fibonacci days.
        
        Args:
            entries: List of news entries with sentiment scores
            
        Returns:
            List of entries with adjusted sentiment scores
        """
        now = datetime.now()
        day_of_month = now.day
        
        # Get moon phase factor (simplified)
        # This is a simplified approximation, in a real implementation
        # we would calculate the actual moon phase
        days_since_new_moon = (now.day % 30)
        moon_phase = days_since_new_moon / 30.0  # 0.0 = new moon, 0.5 = full moon
        
        # Moon phase adjustment
        if moon_phase < 0.1 or moon_phase > 0.9:  # New Moon
            moon_factor = 0.1  # Slightly bullish
        elif 0.45 < moon_phase < 0.55:  # Full Moon
            moon_factor = -0.1  # Slightly bearish
        elif 0.2 < moon_phase < 0.3:  # First Quarter
            moon_factor = 0.5  # Strongly bullish
        elif 0.7 < moon_phase < 0.8:  # Last Quarter
            moon_factor = -0.5  # Strongly bearish
        else:
            moon_factor = 0.0  # Neutral
        
        # Fibonacci day adjustment
        fibonacci_days = [1, 2, 3, 5, 8, 13, 21]
        fib_factor = 0.2 if day_of_month in fibonacci_days else 0.0
        
        # Apply adjustments to each entry
        for entry in entries:
            original_score = entry["sentiment_score"]
            adjusted_score = original_score + moon_factor + fib_factor
            
            # Clamp to range [-1, 1]
            adjusted_score = max(-1.0, min(1.0, adjusted_score))
            
            # Update entry
            entry["sentiment_score"] = adjusted_score
            entry["cosmic_adjustment"] = {
                "moon_factor": moon_factor,
                "fib_factor": fib_factor,
                "original_score": original_score
            }
            
            # Update label based on adjusted score
            if adjusted_score >= 0.1:
                entry["sentiment_label"] = "bullish"
            elif adjusted_score <= -0.1:
                entry["sentiment_label"] = "bearish"
            else:
                entry["sentiment_label"] = "neutral"
        
        logger.info(f"Applied cosmic adjustments: Moon phase ({moon_phase:.2f}, factor: {moon_factor}) and Fibonacci day ({fib_factor})")
        return entries
    
    def display_news(self, entries: List[Dict[str, Any]], limit: int = 10) -> None:
        """
        Display news entries in a rich table.
        
        Args:
            entries: List of news entries to display
            limit: Maximum number of entries to display
        """
        if not entries:
            console.print("[yellow]No news entries found[/]")
            return
        
        # Create a rich table
        table = Table(title=f"📰 Latest Bitcoin News ({len(entries)} entries)")
        table.add_column("Date", style="cyan", width=12)
        table.add_column("Source", style="green", width=12)
        table.add_column("Sentiment", style="yellow", width=10)
        table.add_column("Title", style="white")
        
        # Add rows (limit to the requested number)
        for entry in entries[:limit]:
            # Format the date
            date_str = entry['published'].strftime('%Y-%m-%d')
            
            # Determine sentiment style
            sentiment = entry['sentiment_label']
            score = entry['sentiment_score']
            if sentiment == "bullish":
                sentiment_text = Text(f"📈 {score:.2f}", style="green")
            elif sentiment == "bearish":
                sentiment_text = Text(f"📉 {score:.2f}", style="red")
            else:
                sentiment_text = Text(f"🔄 {score:.2f}", style="yellow")
            
            # Add the row
            table.add_row(
                date_str,
                entry['source'].capitalize(),
                sentiment_text,
                entry['title']
            )
        
        # Display the table
        console.print(table)
    
    def save_news(self, entries: List[Dict[str, Any]], format: str = "csv", label: Optional[str] = None) -> str:
        """
        Save news entries to a file.
        
        Args:
            entries: List of news entries to save
            format: Output format ('csv' or 'json')
            label: Optional sentiment label override
            
        Returns:
            Path to the saved file
        """
        if not entries:
            logger.warning("No entries to save")
            return ""
        
        # Create directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Override labels if specified
        if label:
            for entry in entries:
                entry['sentiment_label'] = label
        
        if format == "csv":
            # Create a DataFrame
            df = pd.DataFrame(entries)
            
            # Save to CSV
            filename = os.path.join(self.data_dir, f"btc_news_{timestamp}.csv")
            df.to_csv(filename, index=False)
            
            logger.info(f"Saved {len(entries)} entries to {filename}")
            console.print(f"[green]✅ Saved {len(entries)} entries to {filename}[/]")
            
            return filename
        
        elif format == "json":
            # Convert datetime objects to strings
            serializable_entries = []
            for entry in entries:
                serializable_entry = entry.copy()
                if isinstance(entry['published'], datetime):
                    serializable_entry['published'] = entry['published'].isoformat()
                serializable_entries.append(serializable_entry)
            
            # Save to JSON
            filename = os.path.join(self.data_dir, f"btc_news_{timestamp}.json")
            with open(filename, 'w') as f:
                json.dump(serializable_entries, f, indent=2)
            
            logger.info(f"Saved {len(entries)} entries to {filename}")
            console.print(f"[green]✅ Saved {len(entries)} entries to {filename}[/]")
            
            return filename
        
        else:
            logger.error(f"Unsupported format: {format}")
            return ""
    
    def generate_ml_dataset(self) -> str:
        """
        Generate a machine learning dataset from saved news files.
        
        Returns:
            Path to the generated dataset file
        """
        # Find all CSV files in the data directory
        csv_files = list(Path(self.data_dir).glob("btc_news_*.csv"))
        
        if not csv_files:
            logger.warning("No CSV files found for ML dataset generation")
            console.print("[yellow]No CSV files found for ML dataset generation[/]")
            return ""
        
        # Read and combine all CSV files
        dfs = []
        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file)
                dfs.append(df)
            except Exception as e:
                logger.error(f"Error reading {csv_file}: {e}")
        
        if not dfs:
            logger.warning("No valid CSV files found")
            return ""
        
        # Combine all dataframes
        combined_df = pd.concat(dfs, ignore_index=True)
        
        # Generate ML dataset with selected columns
        ml_columns = ['title', 'summary', 'sentiment_label', 'sentiment_score', 'source', 'published']
        ml_df = combined_df[ml_columns].copy()
        
        # Add a final_label column based on sentiment_label
        ml_df['final_label'] = ml_df['sentiment_label']
        
        # Save the ML dataset
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.data_dir, f"btc_news_ml_dataset_{timestamp}.csv")
        ml_df.to_csv(output_file, index=False)
        
        logger.info(f"Generated ML dataset with {len(ml_df)} entries saved to {output_file}")
        console.print(f"[green]✅ Generated ML dataset with {len(ml_df)} entries saved to {output_file}[/]")
        
        return output_file


# Alias for compatibility with the original module
BtcNewsFeed = StandaloneBtcNewsFeed

def main():
    """Run the standalone BTC News Feed module."""
    # Display banner
    display_rasta_banner()
    
    # Create a news feed instance
    news_feed = BtcNewsFeed()
    
    # Fetch news from multiple sources
    sources = ["cointelegraph", "decrypt", "bitcoinmagazine"]
    all_entries = []
    
    for source in sources:
        console.print(f"[cyan]Fetching news from {source}...[/]")
        entries = news_feed.fetch_news(source)
        all_entries.extend(entries)
    
    # Apply cosmic adjustments
    all_entries = news_feed.adjust_sentiment_with_cosmic_factors(all_entries)
    
    # Sort by publish date (newest first)
    all_entries.sort(key=lambda x: x['published'], reverse=True)
    
    # Display the news
    news_feed.display_news(all_entries)
    
    # Save the news
    news_feed.save_news(all_entries, format="csv")

if __name__ == "__main__":
    main() 