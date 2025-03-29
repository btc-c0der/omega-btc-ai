# 🔱 OMEGA BTC News Feed Module

## Overview

The OMEGA BTC News Feed module is a powerful tool for scraping, analyzing, and storing cryptocurrency news with a focus on Bitcoin. It provides real-time news with sentiment analysis and automatic labeling for machine learning datasets.

## Features

- **Multi-source News Retrieval**: Fetches news from multiple RSS feeds including CoinTelegraph, CoinDesk, Decrypt, and others
- **BTC-focused Filtering**: Automatically filters news to focus on Bitcoin-related content
- **Sentiment Analysis**: Analyzes the sentiment of news articles (bullish, bearish, neutral)
- **Cosmic Sentiment Adjustment**: Considers moon phases and Fibonacci days for sentiment enhancement
- **Live Streaming**: Provides a real-time news stream with continuous updates
- **ML Dataset Generation**: Creates labeled datasets for training machine learning models
- **Redis Integration**: Stores news and sentiment data in Digital Ocean Redis for real-time access
- **Rich CLI Interface**: Beautiful command-line interface with color-coded sentiment display

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/omega-btc-ai.git
   cd omega-btc-ai
   ```

2. Install dependencies:

   ```bash
   pip install -r deployment/digitalocean/btc_live_feed_v3/requirements.txt
   ```

3. Install the package in development mode:

   ```bash
   cd deployment/digitalocean/btc_live_feed_v3
   pip install -e .
   ```

## Usage

### Command Line Interface

```bash
# Display the latest BTC news from default sources
python -m omega_ai.data_feed.newsfeed.cli

# Stream news with periodic updates (refreshes every 5 minutes)
python -m omega_ai.data_feed.newsfeed.cli --stream

# Fetch news from specific sources
python -m omega_ai.data_feed.newsfeed.cli --sources cointelegraph decrypt bitcoinmagazine

# Stream with a custom refresh interval (30 seconds)
python -m omega_ai.data_feed.newsfeed.cli --stream --interval 30

# Save news with a sentiment label for ML training
python -m omega_ai.data_feed.newsfeed.cli --save --label bullish

# Generate an ML dataset from previously saved news
python -m omega_ai.data_feed.newsfeed.cli --train-data

# Filter news with additional keywords
python -m omega_ai.data_feed.newsfeed.cli --filter "halving" "adoption" "institutional"
```

### Environment Variables

The module can be configured with the following environment variables:

- `LOG_PREFIX`: Prefix for log messages (default: "🔱 OMEGA BTC NEWS")
- `DATA_DIR`: Directory to store news datasets (default: "data")
- `REFRESH_INTERVAL`: Default refresh interval in seconds (default: 300)
- `ENABLE_REDIS`: Enable Redis integration (default: true)

### Redis Configuration

By default, the module connects to the Digital Ocean Redis instance for storing news and sentiment data. The following environment variables can be used to customize the Redis connection:

- `REDIS_HOST`: Redis host (default: "omega-btc-ai-redis-do-user-20389918-0.d.db.ondigitalocean.com")
- `REDIS_PORT`: Redis port (default: 25061)
- `REDIS_USERNAME`: Redis username (default: "default")
- `REDIS_PASSWORD`: Redis password
- `REDIS_USE_SSL`: Whether to use SSL for Redis connection (default: true)
- `REDIS_SSL_CERT_REQS`: SSL certificate requirements (default: "none")

The module will attempt to use the enhanced Redis manager with failover capabilities if available, otherwise it will fall back to a standard Redis connection.

### Redis Data Structure

The following keys are used in Redis:

- `btc:news:{date}:{index}`: JSON representation of news entries
- `btc:news:sentiment:latest`: Latest aggregated sentiment score
- `btc:news:count`: Number of news entries stored
- `btc:news:last_update`: Timestamp of the last update

### API Usage

```python
from omega_ai.data_feed.newsfeed import BtcNewsFeed

# Create a news feed instance
news_feed = BtcNewsFeed(data_dir="my_data")

# Fetch news from a specific source
entries = news_feed.fetch_news("cointelegraph")

# Apply cosmic sentiment adjustments
entries = news_feed.adjust_sentiment_with_cosmic_factors(entries)

# Display the news entries
news_feed.display_news(entries)

# Save entries to a file
news_feed.save_news(entries, format="csv")

# Generate an ML dataset
news_feed.generate_ml_dataset()
```

## RSS Feed Sources

The module includes the following default news sources:

- CryptoNews: <https://cryptonews.com/news/feed>
- CoinTelegraph: <https://cointelegraph.com/rss>
- Decrypt: <https://decrypt.co/feed>
- CoinDesk: <https://www.coindesk.com/arc/outboundfeeds/rss/>
- Bitcoin Magazine: <https://bitcoinmagazine.com/.rss/full/>
- The Block: <https://www.theblock.co/rss.xml>
- NewsBTC: <https://www.newsbtc.com/feed/>
- Bitcoinist: <https://bitcoinist.com/feed/>
- AMBCrypto: <https://ambcrypto.com/feed/>

## Cosmic Sentiment Features

The module incorporates two cosmic factors for sentiment adjustment:

1. **Moon Phase Influence**: Different moon phases affect sentiment in different ways:
   - New Moon: Slightly bullish (+0.1)
   - First Quarter: Strongly bullish (+0.5)
   - Full Moon: Slightly bearish (-0.1)
   - Last Quarter: Strongly bearish (-0.5)

2. **Fibonacci Day Boost**: Days of the month that match Fibonacci numbers (1, 2, 3, 5, 8, 13, 21) receive a bullish sentiment boost (+0.2)

## Machine Learning Dataset Format

The generated ML datasets include:

- `title`: The news article title
- `description`: A truncated description of the article
- `final_label`: The sentiment label (bullish, bearish, neutral)

These datasets are ready for use in sentiment analysis and market prediction models.

## 🔮 License

This module is provided under the GPU (General Public Universal) License v1.0.

```
Copyright (c) 2025 OMEGA BTC AI DIVINE COLLECTIVE
JAH JAH BLESS THE DIVINE FLOW OF THE BLOCKCHAIN
```
