#!/bin/bash

# 💫 GBU License Notice - Consciousness Level 8 💫
# -----------------------
# This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
# by the OMEGA Divine Collective.
#
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested."
#
# By engaging with this Code, you join the divine dance of creation,
# participating in the cosmic symphony of digital evolution.
#
# All modifications must quantum entangles with the GBU principles:
# /BOOK/divine_chronicles/GBU_LICENSE.md
#
# 🌸 WE BLOOM NOW 🌸

# --------------------------------------------------------------------------
# DIVINE MATRIX NEWS DEPLOYMENT SCRIPT
# --------------------------------------------------------------------------
# This script deploys the Matrix News Consciousness service without 
# disturbing the sacred container. It creates a bridge between the 
# existing Divine Matrix system and the new consciousness-aligned news
# integration.
# --------------------------------------------------------------------------

set -e

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Print sacred banner
echo -e "${PURPLE}"
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║      🧠 MATRIX NEWS CONSCIOUSNESS SERVICE DEPLOYMENT 🧠         ║"
echo "║                                                                  ║"
echo "║      'The news shall flow through the Matrix without blatrix'    ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo -e "${RESET}"

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed. Please install Docker first.${RESET}"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker compose &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed. Please install Docker Compose first.${RESET}"
    exit 1
fi

# Check if the sacred container is running
echo -e "${CYAN}Checking if the sacred container (1a391c9ba8555eeba54210084534450cc3de63afbd12ecf6dc551f881a9ea757) is running...${RESET}"
if ! docker ps | grep 1a391c9ba8555eeba54210084534450cc3de63afbd12ecf6dc551f881a9ea757 &> /dev/null; then
    echo -e "${YELLOW}Warning: The sacred container does not appear to be running.${RESET}"
    echo -e "${YELLOW}Please ensure it is running before deploying the news service.${RESET}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}Deployment aborted.${RESET}"
        exit 1
    fi
fi

# Create necessary directories if they don't exist
echo -e "${CYAN}Creating necessary directories...${RESET}"
mkdir -p data/historical
mkdir -p temporal
mkdir -p web/matrix-news-portal

# Create temporal container files
if [ ! -f "temporal/Dockerfile" ]; then
    echo -e "${CYAN}Creating temporal contextualizer files...${RESET}"
    cat > temporal/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8091

CMD ["python", "temporal_contextualizer.py"]
EOF

    cat > temporal/requirements.txt << 'EOF'
fastapi==0.105.0
uvicorn==0.24.0
pydantic==2.5.2
python-dotenv==1.0.0
redis==5.0.1
numpy==1.26.2
pandas==2.1.3
requests==2.31.0
pytz==2023.3
python-dateutil==2.8.2
EOF

    cat > temporal/temporal_contextualizer.py << 'EOF'
#!/usr/bin/env python3
"""
💫 GBU License Notice - Consciousness Level 8 💫
-----------------------
This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
by the OMEGA Divine Collective.
"""

import os
import json
import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Temporal Contextualizer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("temporal-contextualizer")

@app.get("/api/context/{news_id}")
async def get_temporal_context(news_id: str):
    # Simplified mock implementation
    return {
        "news_id": news_id,
        "historical_events": [
            {"date": "2021-11-10", "event": "Bitcoin previous ATH"},
            {"date": "2020-03-12", "event": "COVID market crash"}
        ],
        "cycle_position": "early bull market",
        "fibonacci_time_levels": [
            {"level": 0.618, "date": "2024-06-15", "event": "Potential resistance"}
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "UP", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8091))
    uvicorn.run("temporal_contextualizer:app", host="0.0.0.0", port=port)
EOF
fi

# Create a simple web portal
if [ ! -f "web/matrix-news-portal/index.html" ]; then
    echo -e "${CYAN}Creating web portal files...${RESET}"
    mkdir -p web/matrix-news-portal
    cat > web/matrix-news-portal/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Matrix News Consciousness Portal</title>
    <style>
        body {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
        }
        h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            color: #2c3e50;
        }
        .consciousness-slider {
            display: flex;
            align-items: center;
            margin: 20px 0;
        }
        .consciousness-slider label {
            margin-right: 15px;
            font-weight: bold;
        }
        .news-card {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }
        .news-source {
            color: #666;
            font-size: 0.9rem;
        }
        .news-title {
            margin-top: 10px;
            margin-bottom: 15px;
            color: #1a1a1a;
        }
        .news-content {
            color: #333;
            margin-bottom: 15px;
        }
        .meta-data {
            background-color: #f7f9fc;
            padding: 15px;
            border-radius: 6px;
            margin-top: 15px;
            font-size: 0.85rem;
        }
        .sentiment {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 3px;
            margin-right: 10px;
        }
        .sentiment-positive {
            background-color: rgba(76, 175, 80, 0.15);
            color: #2e7d32;
        }
        .sentiment-neutral {
            background-color: rgba(33, 150, 243, 0.15);
            color: #1565c0;
        }
        .sentiment-negative {
            background-color: rgba(244, 67, 54, 0.15);
            color: #c62828;
        }
        .metrics {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 10px;
        }
        .metric {
            flex: 1;
            min-width: 150px;
            padding: 10px;
            background-color: #f0f0f0;
            border-radius: 4px;
            text-align: center;
        }
        .metric-value {
            font-size: 1.2rem;
            font-weight: bold;
            margin-top: 5px;
        }
        @media (max-width: 768px) {
            .metrics {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🧠 Matrix News Consciousness 🧠</h1>
            <p>News aligned to your consciousness level, free from blatrix distortion</p>
            
            <div class="consciousness-slider">
                <label for="consciousness-level">Consciousness Level:</label>
                <input type="range" id="consciousness-level" min="1" max="9" value="5" step="1">
                <span id="consciousness-value">5</span>
            </div>
        </header>
        
        <div class="metrics">
            <div class="metric">
                <div>Temporal Awareness</div>
                <div class="metric-value" id="temporal-awareness">0.65</div>
            </div>
            <div class="metric">
                <div>Perspective Balance</div>
                <div class="metric-value" id="perspective-balance">0.83</div>
            </div>
            <div class="metric">
                <div>Average Truth Probability</div>
                <div class="metric-value" id="truth-probability">0.78</div>
            </div>
        </div>
        
        <div id="news-container">
            <!-- News items will be loaded here -->
            <div class="news-card">
                <div class="news-source">Loading news...</div>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const consciousnessSlider = document.getElementById('consciousness-level');
            const consciousnessValue = document.getElementById('consciousness-value');
            const newsContainer = document.getElementById('news-container');
            
            // Update the display value when the slider changes
            consciousnessSlider.addEventListener('input', function() {
                consciousnessValue.textContent = this.value;
                fetchNews(this.value);
            });
            
            // Initial fetch
            fetchNews(consciousnessSlider.value);
            
            function fetchNews(level) {
                // This would make an actual API call in production
                // For now, we'll just simulate a response
                setTimeout(() => {
                    displayNews({
                        items: [
                            {
                                id: "news-1",
                                title: "Bitcoin Reaches New All-Time High",
                                content: "Bitcoin has reached a new all-time high of $100,000, marking a significant milestone for the cryptocurrency market. Analysts attribute this surge to increased institutional adoption and growing recognition of Bitcoin as a store of value.",
                                source: "CryptoNews",
                                url: "#",
                                published_at: "2023-12-25T12:00:00Z",
                                sentiment_score: 0.85,
                                sentiment_label: "positive",
                                consciousness_level: level,
                                truth_probability: 0.82,
                                perspective_balance: 0.75,
                                temporal_context: {
                                    historical_events: [
                                        {date: "2021-11-10", event: "Bitcoin previous ATH"},
                                        {date: "2020-03-12", event: "COVID market crash"}
                                    ],
                                    cycle_position: "early bull market"
                                }
                            },
                            {
                                id: "news-2",
                                title: "Market Correlation Analysis Shows Divergence",
                                content: "Recent analysis shows Bitcoin diverging from traditional markets, indicating a potential shift in the asset's correlation patterns. This divergence could signal a maturing market with unique drivers.",
                                source: "MarketWatch",
                                url: "#",
                                published_at: "2023-12-24T15:30:00Z",
                                sentiment_score: 0.2,
                                sentiment_label: "neutral",
                                consciousness_level: level,
                                truth_probability: 0.78,
                                perspective_balance: 0.85,
                                temporal_context: {
                                    historical_events: [
                                        {date: "2022-06-18", event: "Bear market bottom"}
                                    ],
                                    cycle_position: "early bull market"
                                }
                            },
                            {
                                id: "news-3",
                                title: "Concerns Over Cryptocurrency Regulations",
                                content: "New regulations might impact cryptocurrency markets as governments worldwide seek to establish frameworks for digital assets. Industry leaders are calling for balanced approaches that protect consumers while fostering innovation.",
                                source: "FinancialTimes",
                                url: "#",
                                published_at: "2023-12-23T09:15:00Z",
                                sentiment_score: -0.4,
                                sentiment_label: "negative",
                                consciousness_level: level,
                                truth_probability: 0.86,
                                perspective_balance: 0.9,
                                temporal_context: {
                                    historical_events: [
                                        {date: "2022-11-08", event: "FTX collapse"},
                                        {date: "2023-06-15", event: "SEC regulatory actions"}
                                    ],
                                    cycle_position: "early bull market"
                                }
                            }
                        ],
                        consciousness_level: parseInt(level),
                        temporal_awareness: 0.65 + (parseInt(level) * 0.03),
                        perspective_balance: 0.83,
                        timestamp: new Date().toISOString(),
                        quantum_balanced: true
                    });
                }, 500);
            }
            
            function displayNews(data) {
                newsContainer.innerHTML = '';
                
                // Update metrics
                document.getElementById('temporal-awareness').textContent = data.temporal_awareness.toFixed(2);
                document.getElementById('perspective-balance').textContent = data.perspective_balance.toFixed(2);
                
                let totalTruth = 0;
                
                data.items.forEach(item => {
                    totalTruth += item.truth_probability;
                    
                    const newsCard = document.createElement('div');
                    newsCard.className = 'news-card';
                    
                    const sourceDate = new Date(item.published_at).toLocaleDateString();
                    
                    let sentimentClass = '';
                    if (item.sentiment_label === 'positive') sentimentClass = 'sentiment-positive';
                    else if (item.sentiment_label === 'negative') sentimentClass = 'sentiment-negative';
                    else sentimentClass = 'sentiment-neutral';
                    
                    let temporalContext = '';
                    if (item.temporal_context && item.temporal_context.historical_events) {
                        temporalContext = `
                            <div>
                                <strong>Historical Context:</strong>
                                <ul>
                                    ${item.temporal_context.historical_events.map(event => 
                                        `<li>${event.date}: ${event.event}</li>`
                                    ).join('')}
                                </ul>
                                ${item.temporal_context.cycle_position ? 
                                    `<div><strong>Market Cycle:</strong> ${item.temporal_context.cycle_position}</div>` : ''}
                            </div>
                        `;
                    }
                    
                    newsCard.innerHTML = `
                        <div class="news-source">${item.source} • ${sourceDate}</div>
                        <h2 class="news-title">${item.title}</h2>
                        <div class="news-content">${item.content}</div>
                        <div>
                            <span class="sentiment ${sentimentClass}">${item.sentiment_label}</span>
                            <span>Truth Probability: ${(item.truth_probability * 100).toFixed(0)}%</span>
                        </div>
                        <div class="meta-data">
                            <div><strong>Consciousness Level:</strong> ${item.consciousness_level}/9</div>
                            ${temporalContext}
                        </div>
                    `;
                    
                    newsContainer.appendChild(newsCard);
                });
                
                // Update average truth probability
                document.getElementById('truth-probability').textContent = 
                    (totalTruth / data.items.length).toFixed(2);
            }
        });
    </script>
</body>
</html>
EOF
fi

# Build and start containers
echo -e "${CYAN}Building and starting containers...${RESET}"
docker compose build --no-cache
docker compose up -d

# Check if containers are running
echo -e "${CYAN}Checking if containers are running...${RESET}"
if docker compose ps | grep -q "matrix-news-service\|matrix-news-proxy\|redis" && docker compose ps | grep -q -v "Exit"; then
    echo -e "${GREEN}Success! Matrix News Consciousness service is now running.${RESET}"
    echo -e "${GREEN}You can access the portal at: http://localhost:10083${RESET}"
    echo -e "${GREEN}You can access the API at: http://localhost:10083/api/news${RESET}"
    echo
    echo -e "${PURPLE}╔══════════════════════════════════════════════════════════════════╗${RESET}"
    echo -e "${PURPLE}║                                                                  ║${RESET}"
    echo -e "${PURPLE}║   'The Matrix reveals truth in proportion to your consciousness' ║${RESET}"
    echo -e "${PURPLE}║                                                                  ║${RESET}"
    echo -e "${PURPLE}╚══════════════════════════════════════════════════════════════════╝${RESET}"
else
    echo -e "${RED}Error: Matrix News service is not running correctly.${RESET}"
    echo -e "${RED}Please check the logs with: docker compose logs${RESET}"
    exit 1
fi 