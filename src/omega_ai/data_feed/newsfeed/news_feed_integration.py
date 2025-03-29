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
OMEGA BTC AI - News Feed Integration Example
==========================================

Demonstrates the integration of the BTC News Feed with market data analysis,
providing sentiment-aware market context for trading strategies.

This module showcases how to use the BtcNewsFeed class to retrieve news data,
analyze sentiment, and integrate it with existing market data analysis.
"""

import os
import sys
import time
import logging
import argparse
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Import the BtcNewsFeed class directly from our standalone implementation
try:
    from .standalone_newsfeed import BtcNewsFeed, display_rasta_banner
except ImportError as e:
    print(f"Error importing BtcNewsFeed from relative path: {e}")
    try:
        # Fallback to absolute import
        from src.omega_ai.data_feed.newsfeed.standalone_newsfeed import BtcNewsFeed, display_rasta_banner
        print("Successfully imported BtcNewsFeed from absolute path")
    except ImportError as e2:
        print(f"Error importing BtcNewsFeed from absolute path: {e2}")
        print("Please make sure the standalone_newsfeed.py file is accessible.")
        sys.exit(1)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("news-integration")

# Initialize rich console
console = Console()

class NewsFeedIntegration:
    """Integration class for incorporating news sentiment into trading strategies."""
    
    def __init__(self, sources=None, use_redis=True, data_dir="data"):
        """
        Initialize the news feed integration.
        
        Args:
            sources: List of news sources to use
            use_redis: Whether to use Redis for caching
            data_dir: Directory to store data
        """
        self.sources = sources or ["cointelegraph", "decrypt", "bitcoinmagazine"]
        self.news_feed = BtcNewsFeed(use_redis=use_redis, data_dir=data_dir)
        
        # Create output directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
    
    def fetch_latest_news(self, limit=10):
        """
        Fetch and process the latest news from all configured sources.
        
        Args:
            limit: Maximum number of news items to return
            
        Returns:
            List of news entries with sentiment analysis
        """
        all_entries = []
        
        for source in self.sources:
            try:
                logger.info(f"Fetching news from {source}...")
                entries = self.news_feed.fetch_news(source)
                all_entries.extend(entries)
            except Exception as e:
                logger.error(f"Error fetching from {source}: {e}")
        
        # Apply cosmic adjustments to sentiment
        all_entries = self.news_feed.adjust_sentiment_with_cosmic_factors(all_entries)
        
        # Sort by publish date (newest first)
        all_entries.sort(key=lambda x: x['published'], reverse=True)
        
        return all_entries[:limit]
    
    def get_sentiment_summary(self, entries):
        """
        Generate a summary of sentiment from news entries.
        
        Args:
            entries: List of news entries with sentiment
            
        Returns:
            Dictionary with sentiment summary data
        """
        if not entries:
            return {"average": 0, "bullish": 0, "bearish": 0, "neutral": 0}
        
        # Count sentiment labels
        sentiment_counts = {"bullish": 0, "bearish": 0, "neutral": 0}
        total_score = 0
        
        for entry in entries:
            total_score += entry.get("sentiment_score", 0)
            label = entry.get("sentiment_label", "neutral")
            sentiment_counts[label] = sentiment_counts.get(label, 0) + 1
        
        # Calculate average sentiment
        average = total_score / len(entries)
        
        return {
            "average": average,
            "bullish": sentiment_counts["bullish"],
            "bearish": sentiment_counts["bearish"],
            "neutral": sentiment_counts["neutral"],
            "total": len(entries)
        }
    
    def display_sentiment_summary(self, summary):
        """Display a rich formatted summary of news sentiment."""
        # Determine overall market sentiment
        avg = summary["average"]
        if avg >= 0.3:
            sentiment = "BULLISH 📈"
            color = "green"
        elif avg <= -0.3:
            sentiment = "BEARISH 📉"
            color = "red"
        else:
            sentiment = "NEUTRAL 🔄"
            color = "yellow"
        
        # Create a nice panel
        panel = Panel(
            f"[bold {color}]Overall Market Sentiment: {sentiment}[/]\n\n"
            f"Average Sentiment Score: [{color}]{avg:.2f}[/]\n"
            f"Bullish News: [green]{summary['bullish']}[/]\n"
            f"Bearish News: [red]{summary['bearish']}[/]\n"
            f"Neutral News: [yellow]{summary['neutral']}[/]\n"
            f"Total News Items: {summary['total']}\n",
            title="📰 News Sentiment Summary",
            border_style=color
        )
        
        console.print(panel)
    
    def create_trading_recommendation(self, sentiment_summary):
        """
        Generate a trading recommendation based on news sentiment.
        
        Args:
            sentiment_summary: Dictionary with sentiment summary
            
        Returns:
            Dictionary with trading recommendation
        """
        avg = sentiment_summary["average"]
        
        # Base recommendation on sentiment score
        if avg >= 0.5:
            action = "BUY"
            confidence = "HIGH"
            message = "Strong bullish sentiment detected in recent news"
        elif avg >= 0.3:
            action = "BUY"
            confidence = "MEDIUM"
            message = "Moderately bullish sentiment in news"
        elif avg <= -0.5:
            action = "SELL"
            confidence = "HIGH"
            message = "Strong bearish sentiment detected in recent news"
        elif avg <= -0.3:
            action = "SELL"
            confidence = "MEDIUM"
            message = "Moderately bearish sentiment in news"
        else:
            action = "HOLD"
            confidence = "MEDIUM"
            message = "Neutral market sentiment in recent news"
        
        return {
            "action": action,
            "confidence": confidence,
            "message": message,
            "sentiment_score": avg,
            "timestamp": datetime.now().isoformat()
        }
    
    def display_trading_recommendation(self, recommendation):
        """Display a trading recommendation based on news sentiment."""
        action = recommendation["action"]
        confidence = recommendation["confidence"]
        
        if action == "BUY":
            color = "green"
            emoji = "🚀"
        elif action == "SELL":
            color = "red"
            emoji = "⚠️"
        else:
            color = "yellow"
            emoji = "⏳"
        
        panel = Panel(
            f"[bold {color}]Recommended Action: {action} {emoji}[/]\n\n"
            f"Confidence: [{color}]{confidence}[/]\n"
            f"Reasoning: {recommendation['message']}\n"
            f"Sentiment Score: {recommendation['sentiment_score']:.2f}\n"
            f"Generated: {recommendation['timestamp']}\n",
            title="🤖 AI Trading Recommendation",
            border_style=color
        )
        
        console.print(panel)
    
    def run_integration_demo(self, save_output=False):
        """Run the complete news feed integration demo."""
        # Display banner
        display_rasta_banner()
        
        console.print("\n[bold cyan]🔍 Fetching latest Bitcoin news...[/]\n")
        
        # Fetch latest news
        entries = self.fetch_latest_news(limit=15)
        
        # Display news entries
        self.news_feed.display_news(entries, limit=10)
        
        # Generate and display sentiment summary
        summary = self.get_sentiment_summary(entries)
        self.display_sentiment_summary(summary)
        
        # Generate and display trading recommendation
        recommendation = self.create_trading_recommendation(summary)
        self.display_trading_recommendation(recommendation)
        
        # Save results if requested
        if save_output:
            # Save news entries
            self.news_feed.save_news(entries, format="csv")
            
            # Save summary and recommendation
            output = {
                "sentiment_summary": summary,
                "trading_recommendation": recommendation,
                "timestamp": datetime.now().isoformat()
            }
            
            output_file = os.path.join(self.news_feed.data_dir, f"news_integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(output_file, "w") as f:
                import json
                json.dump(output, f, indent=2)
            
            console.print(f"\n[green]Results saved to {output_file}[/]")

def main():
    """Main entry point for running the news feed integration demo."""
    parser = argparse.ArgumentParser(description="OMEGA BTC AI - News Feed Integration Demo")
    
    parser.add_argument("--sources", type=str, nargs="+", 
                        default=["cointelegraph", "decrypt", "bitcoinmagazine"],
                        help="News sources to use")
    parser.add_argument("--no-redis", action="store_true", 
                        help="Disable Redis integration")
    parser.add_argument("--data-dir", type=str, default="data",
                        help="Directory for data storage")
    parser.add_argument("--save", action="store_true",
                        help="Save output to file")
    
    args = parser.parse_args()
    
    integration = NewsFeedIntegration(
        sources=args.sources,
        use_redis=not args.no_redis,
        data_dir=args.data_dir
    )
    
    integration.run_integration_demo(save_output=args.save)

if __name__ == "__main__":
    main() 