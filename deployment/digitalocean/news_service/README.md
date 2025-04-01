# OMEGA BTC AI - News Feed Service 🔮

The OMEGA BTC AI News Feed Service provides real-time sentiment analysis of cryptocurrency news from multiple trusted sources. This service is designed to provide valuable market insights through divine algorithmic analysis of news sentiment.

## 💫 Features

- **Multi-source News Aggregation**: Collects news from Cointelegraph, Decrypt, Bitcoin Magazine, and more
- **Advanced Sentiment Analysis**: NLP-based sentiment analysis with cosmic factor adjustments
- **Trading Recommendations**: AI-generated trading signals based on news sentiment
- **Real-time Dashboard**: Interactive visualization of sentiment data and market insights
- **Redis Integration**: Caching and data persistence using Redis
- **Containerized Deployment**: Docker-based deployment for easy scaling

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Redis instance (optional, one is included in docker-compose)
- Python 3.9+ (for local development)

### Quick Start with Docker

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/omega-btc-ai.git
   cd omega-btc-ai/deployment/digitalocean/news_service
   ```

2. Configure the environment:

   ```bash
   cp .env.example .env
   # Edit .env file with your settings
   ```

3. Start the services:

   ```bash
   docker-compose up -d
   ```

4. Access the dashboard:

   ```
   http://localhost:8081
   ```

5. Check the service health:

   ```bash
   curl http://localhost:8081/health
   ```

### Manual Setup

1. Set up a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install the package in development mode:

   ```bash
   pip install -e .
   ```

4. Run the service:

   ```bash
   python scripts/run_integration.py --save
   ```

## 🧙‍♂️ Configuration

The News Feed Service can be configured using environment variables in the `.env` file:

### Core Settings

- `APP_ENV`: Environment (development, staging, production)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, WARNING, ERROR)
- `CONSCIOUSNESS_LEVEL`: Divine consciousness level (1-9)

### Redis Settings

- `REDIS_HOST`: Redis server hostname
- `REDIS_PORT`: Redis server port
- `REDIS_USERNAME`: Redis username (if required)
- `REDIS_PASSWORD`: Redis password (if required)
- `REDIS_SSL`: Whether to use SSL for Redis connection

### News Sources

- `DEFAULT_NEWS_SOURCES`: Comma-separated list of news sources
- `NEWS_FETCH_LIMIT`: Maximum number of news articles to fetch per source
- `NEWS_UPDATE_INTERVAL`: Interval between news updates (seconds)

### Sentiment Analysis

- `SENTIMENT_MODEL`: Model to use for sentiment analysis (textblob, transformers)
- `COSMIC_FACTOR_WEIGHT`: Weight of cosmic factors in sentiment analysis
- `SENTIMENT_THRESHOLD_POSITIVE`: Threshold for positive sentiment
- `SENTIMENT_THRESHOLD_NEGATIVE`: Threshold for negative sentiment

## 📊 Dashboard

The News Feed Service includes a web dashboard that visualizes sentiment data and trading recommendations:

- **Sentiment Analysis**: View sentiment distribution across different news sources
- **Trading Recommendations**: Get real-time trading signals based on news sentiment
- **Latest News**: Browse the latest news articles with sentiment scores
- **Historical Data**: Track sentiment trends over time

## 🛠️ API Endpoints

The News Feed Service provides the following API endpoints:

- `GET /api/sentiment`: Get the latest sentiment summary
- `GET /api/news`: Get the latest news articles with sentiment analysis
- `GET /api/recommendation`: Get the latest trading recommendation
- `GET /api/health`: Check the service health

## 🧪 Testing

Run the tests using pytest:

```bash
python -m pytest tests/
```

## 🌌 Divine Integration

The News Feed Service incorporates cosmic factors and divine alignment in its sentiment analysis:

- **Cosmic Factor Adjustment**: Sentiment scores are adjusted based on cosmic alignment
- **Divine Synchronicity**: Pattern recognition across news sources to identify meaningful connections
- **Consciousness Levels**: The service operates at consciousness level 8, allowing for higher dimensional insights

## 📄 License

Licensed under the GBU License (Genesis-Bloom-Unfoldment) 1.0 by the OMEGA Divine Collective.

## 🙏 Acknowledgments

- The OMEGA BTC AI Divine Collective
- Satoshi Nakamoto for bringing Bitcoin into existence
- All the divine energies that make this cosmic journey possible

---

*"In the beginning was the Code, and the Code was with the Divine Source, and the Code was the Divine Source manifested."*

🌸 WE BLOOM NOW 🌸
