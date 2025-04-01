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
BTC News Feed Integration Module
================================

This module integrates the BTC News Feed with market data analysis,
providing sentiment analysis and trading recommendations based on
news sentiment.

Features:
- Multi-source news aggregation (CoinTelegraph, Decrypt, etc.)
- Sentiment analysis with advanced NLP
- Trading recommendations based on sentiment
- Redis integration for data persistence

The integration module acts as a bridge between news data and
trading systems, offering real-time insights into market sentiment.

Copyright (c) 2025 OMEGA-BTC-AI - Licensed under the GBU License
"""

import os
import sys
import json
import logging
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Union, Any, Tuple

# Import the BTC Newsfeed module
from omega_ai.data_feed.newsfeed.btc_newsfeed import BtcNewsFeed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('NewsFeedIntegration')

class NewsFeedIntegration:
    """
    Integrates the BTC News Feed with market data analysis and trading systems.
    
    This class provides methods to fetch news, analyze sentiment, and generate
    trading recommendations based on news sentiment. It also supports Redis
    integration for data persistence.
    """
    
    def __init__(
        self,
        sources: List[str] = None,
        use_redis: bool = True,
        redis_host: str = 'localhost',
        redis_port: int = 6379,
        redis_db: int = 0,
        data_dir: str = 'data'
    ):
        """
        Initialize the news feed integration.
        
        Args:
            sources: List of news sources to use (default: cointelegraph, decrypt)
            use_redis: Whether to use Redis for data persistence
            redis_host: Redis host
            redis_port: Redis port
            redis_db: Redis database
            data_dir: Directory for data storage
        """
        self.sources = sources if sources is not None else ['cointelegraph', 'decrypt']
        self.data_dir = data_dir
        self.use_redis = use_redis
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize the BTC News Feed - using default constructor without sources param
        # as per the existing implementation
        self.news_feed = BtcNewsFeed(data_dir=data_dir, use_redis=use_redis)
        
        # Check if Redis is available through the news feed's client
        self.redis = None
        if self.use_redis and hasattr(self.news_feed, 'redis_client') and self.news_feed.redis_client:
            self.redis = self.news_feed.redis_client
            logger.info(f"Redis integration enabled through BtcNewsFeed")
        else:
            logger.warning("Redis not available or not enabled")
            self.use_redis = False
    
    def fetch_latest_news(self, limit: int = 30) -> pd.DataFrame:
        """
        Fetch the latest news articles from all configured sources.
        
        Args:
            limit: Maximum number of articles to fetch per source
            
        Returns:
            DataFrame containing the news articles with sentiment analysis
        """
        logger.info(f"Fetching latest news from sources: {', '.join(self.sources)}")
        
        # Collect news from all sources
        all_entries = []
        for source in self.sources:
            try:
                # Use the fetch_news method from BtcNewsFeed
                entries = self.news_feed.fetch_news(source)
                if entries:
                    # Add source information if not already present
                    for entry in entries:
                        if 'source' not in entry:
                            entry['source'] = source
                    all_entries.extend(entries)
            except Exception as e:
                logger.error(f"Error fetching news from {source}: {e}")
        
        # Apply sentiment analysis if not already done
        news_data = self.news_feed.adjust_sentiment_with_cosmic_factors(all_entries)
        
        # Convert to DataFrame for easier analysis
        if not news_data:
            logger.warning("No news data returned")
            return pd.DataFrame()
        
        df = pd.DataFrame(news_data)
        
        # Add timestamp for tracking
        df['timestamp'] = datetime.now().isoformat()
        
        # Limit the number of entries if specified
        if limit and len(df) > limit:
            df = df.sort_values('published', ascending=False).head(limit)
        
        logger.info(f"Fetched {len(df)} articles with sentiment analysis")
        return df
    
    def generate_sentiment_summary(self, news_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate a summary of sentiment analysis from news data.
        
        Args:
            news_df: DataFrame containing news articles with sentiment
            
        Returns:
            Dictionary containing sentiment summary
        """
        if news_df.empty:
            logger.warning("No news data to generate sentiment summary")
            return {}
        
        # Calculate average sentiment using the sentiment_score field
        if 'sentiment_score' in news_df.columns:
            sentiment_field = 'sentiment_score'
        elif 'sentiment' in news_df.columns:
            sentiment_field = 'sentiment'
        else:
            logger.warning("No sentiment field found in news data")
            return {}
            
        avg_sentiment = news_df[sentiment_field].mean()
        
        # Calculate sentiment distribution based on labels if available
        if 'sentiment_label' in news_df.columns:
            sentiment_counts = news_df['sentiment_label'].value_counts().to_dict()
        else:
            # Otherwise use numeric thresholds
            sentiment_counts = {
                'positive': len(news_df[news_df[sentiment_field] > 0.2]),
                'neutral': len(news_df[(news_df[sentiment_field] >= -0.2) & (news_df[sentiment_field] <= 0.2)]),
                'negative': len(news_df[news_df[sentiment_field] < -0.2])
            }
        
        # Calculate sentiment by source
        sentiment_by_source = news_df.groupby('source')[sentiment_field].mean().to_dict()
        
        # Generate cosmic factor - a divine adjustment to sentiment based on cosmic alignment
        positive_count = sentiment_counts.get('positive', 0) or sentiment_counts.get('bullish', 0)
        cosmic_factor = abs(avg_sentiment) * (1 + (positive_count / max(1, len(news_df))))
        
        # Create summary
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_articles': len(news_df),
            'average_sentiment': float(avg_sentiment),
            'sentiment_distribution': sentiment_counts,
            'sentiment_by_source': sentiment_by_source,
            'cosmic_factor': float(cosmic_factor),
            'sources': list(news_df['source'].unique())
        }
        
        logger.info(f"Generated sentiment summary with average sentiment: {avg_sentiment:.2f}")
        return summary
    
    def display_sentiment_data(self, news_df: pd.DataFrame) -> None:
        """
        Display sentiment data in a readable format.
        
        Args:
            news_df: DataFrame containing news articles with sentiment
        """
        if news_df.empty:
            print("No news data to display")
            return
        
        # Generate summary
        summary = self.generate_sentiment_summary(news_df)
        if not summary:
            print("Could not generate sentiment summary")
            return
        
        # Display summary
        print("\n🔮 SENTIMENT ANALYSIS SUMMARY 🔮")
        print("================================")
        print(f"Total Articles: {summary['total_articles']}")
        print(f"Average Sentiment: {summary['average_sentiment']:.2f}")
        print(f"Cosmic Factor: {summary['cosmic_factor']:.2f}")
        
        print("\nSentiment Distribution:")
        for sentiment, count in summary['sentiment_distribution'].items():
            percentage = (count / summary['total_articles']) * 100
            print(f"  - {sentiment.capitalize()}: {count} ({percentage:.1f}%)")
        
        print("\nSentiment by Source:")
        for source, sentiment in summary['sentiment_by_source'].items():
            print(f"  - {source}: {sentiment:.2f}")
        
        # Determine sentiment field
        if 'sentiment_score' in news_df.columns:
            sentiment_field = 'sentiment_score'
        elif 'sentiment' in news_df.columns:
            sentiment_field = 'sentiment'
        else:
            print("No sentiment field found in news data")
            return
            
        # Display top positive and negative headlines
        print("\nTop Positive Headlines:")
        top_positive = news_df.sort_values(sentiment_field, ascending=False).head(3)
        for _, row in top_positive.iterrows():
            title = row.get('title', 'No title')
            source = row.get('source', 'Unknown')
            sentiment = row.get(sentiment_field, 0)
            print(f"  - {title} ({sentiment:.2f}) - {source}")
        
        print("\nTop Negative Headlines:")
        top_negative = news_df.sort_values(sentiment_field, ascending=True).head(3)
        for _, row in top_negative.iterrows():
            title = row.get('title', 'No title')
            source = row.get('source', 'Unknown')
            sentiment = row.get(sentiment_field, 0)
            print(f"  - {title} ({sentiment:.2f}) - {source}")
    
    def generate_trading_recommendation(self, sentiment_summary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a trading recommendation based on sentiment analysis.
        
        Args:
            sentiment_summary: Dictionary containing sentiment summary
            
        Returns:
            Dictionary containing trading recommendation
        """
        if not sentiment_summary:
            logger.warning("No sentiment summary to generate trading recommendation")
            return {}
        
        # Extract sentiment data
        avg_sentiment = sentiment_summary['average_sentiment']
        cosmic_factor = sentiment_summary['cosmic_factor']
        sentiment_distribution = sentiment_summary['sentiment_distribution']
        
        # Calculate positivity ratio
        total_articles = sentiment_summary['total_articles']
        positive_count = sentiment_distribution.get('positive', 0) or sentiment_distribution.get('bullish', 0)
        positivity_ratio = positive_count / max(1, total_articles)
        
        # Determine trading action based on sentiment
        if avg_sentiment > 0.3 and positivity_ratio > 0.6:
            action = "BUY"
            confidence = min(0.9, avg_sentiment + cosmic_factor)
            analysis = "Strongly positive sentiment across sources. Multiple bullish indicators."
        elif avg_sentiment > 0.1 and positivity_ratio > 0.4:
            action = "ACCUMULATE"
            confidence = min(0.8, avg_sentiment + (cosmic_factor * 0.5))
            analysis = "Moderately positive sentiment. Good opportunity to accumulate."
        elif avg_sentiment < -0.3 and (sentiment_distribution.get('negative', 0) or sentiment_distribution.get('bearish', 0)) > positive_count:
            action = "SELL"
            confidence = min(0.9, abs(avg_sentiment) + cosmic_factor)
            analysis = "Strongly negative sentiment across sources. Multiple bearish indicators."
        elif avg_sentiment < -0.1 and (sentiment_distribution.get('negative', 0) or sentiment_distribution.get('bearish', 0)) > positive_count:
            action = "REDUCE"
            confidence = min(0.8, abs(avg_sentiment) + (cosmic_factor * 0.5))
            analysis = "Moderately negative sentiment. Consider reducing exposure."
        else:
            action = "HOLD"
            confidence = 0.5 + (abs(avg_sentiment) * 0.2)
            analysis = "Mixed or neutral sentiment. No clear directional bias."
        
        # Create recommendation
        recommendation = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'confidence': float(confidence),
            'analysis': analysis,
            'sentiment_score': float(avg_sentiment),
            'cosmic_factor': float(cosmic_factor),
            'sources': sentiment_summary['sources'],
            'total_articles': sentiment_summary['total_articles']
        }
        
        logger.info(f"Generated trading recommendation: {action} with confidence {confidence:.2f}")
        return recommendation
    
    def store_recommendation_in_redis(self, recommendation: Dict[str, Any]) -> bool:
        """
        Store trading recommendation in Redis.
        
        Args:
            recommendation: Dictionary containing trading recommendation
            
        Returns:
            True if successful, False otherwise
        """
        if not self.use_redis or not recommendation or not self.redis:
            return False
        
        try:
            # Convert recommendation to JSON string
            recommendation_json = json.dumps(recommendation)
            
            # Generate key with timestamp
            timestamp = recommendation.get('timestamp', datetime.now().isoformat())
            key = f"news:recommendation:{timestamp}"
            
            # Store recommendation using the appropriate method
            if hasattr(self.redis, 'set'):
                # Standard Redis client
                self.redis.set(key, recommendation_json)
                
                # Store latest recommendation
                self.redis.set('news:recommendation:latest', recommendation_json)
                
            elif hasattr(self.redis, 'execute_command'):
                # Enhanced Redis Manager
                self.redis.execute_command('SET', key, recommendation_json)
                
                # Store latest recommendation
                self.redis.execute_command('SET', 'news:recommendation:latest', recommendation_json)
                
                # Add to sorted set for time-based retrieval if possible
                try:
                    score = datetime.fromisoformat(timestamp).timestamp()
                    self.redis.execute_command('ZADD', 'news:recommendations', str(score), key)
                except Exception as e:
                    logger.warning(f"Could not add to sorted set: {e}")
            else:
                logger.warning("Redis client doesn't have appropriate methods for storing data")
                return False
            
            logger.info(f"Stored trading recommendation in Redis: {key}")
            return True
        except Exception as e:
            logger.error(f"Failed to store recommendation in Redis: {e}")
            return False
    
    def save_to_file(self, data: Dict[str, Any], file_type: str) -> Optional[str]:
        """
        Save data to a file.
        
        Args:
            data: Data to save
            file_type: Type of data being saved (e.g., 'news', 'sentiment', 'recommendation')
            
        Returns:
            Path to the saved file, or None if saving failed
        """
        if not data:
            return None
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{file_type}_{timestamp}.json"
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Save to file
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Saved {file_type} data to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to save {file_type} data to file: {e}")
            return None
    
    def run_integration_demo(self, save_output: bool = False) -> Optional[Dict[str, Any]]:
        """
        Run a demonstration of the news feed integration.
        
        Args:
            save_output: Whether to save output to files
            
        Returns:
            Dictionary containing trading recommendation, or None if failed
        """
        try:
            # Fetch latest news with sentiment analysis
            news_df = self.fetch_latest_news(limit=30)
            
            if news_df.empty:
                logger.warning("No news data returned, cannot continue")
                return None
            
            # Display sentiment data
            self.display_sentiment_data(news_df)
            
            # Generate sentiment summary
            sentiment_summary = self.generate_sentiment_summary(news_df)
            
            # Generate trading recommendation
            recommendation = self.generate_trading_recommendation(sentiment_summary)
            
            # Display recommendation
            print("\n💹 TRADING RECOMMENDATION 💹")
            print("===========================")
            print(f"Action: {recommendation['action']}")
            print(f"Confidence: {recommendation['confidence']:.2f}")
            print(f"Analysis: {recommendation['analysis']}")
            
            # Store in Redis if available
            if self.use_redis:
                stored = self.store_recommendation_in_redis(recommendation)
                if stored:
                    print("\n✅ Stored recommendation in Redis")
            
            # Save to files if requested
            if save_output:
                # Save news data to CSV
                news_csv_path = os.path.join(self.data_dir, f"news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
                news_df.to_csv(news_csv_path, index=False)
                
                # Save sentiment summary and recommendation to JSON
                self.save_to_file(sentiment_summary, 'sentiment')
                self.save_to_file(recommendation, 'recommendation')
                
                print(f"\n✅ Saved data to {self.data_dir}")
            
            return recommendation
        
        except Exception as e:
            logger.error(f"Error running integration demo: {e}")
            return None

if __name__ == "__main__":
    # Create and run the integration
    integration = NewsFeedIntegration()
    integration.run_integration_demo(save_output=True) 