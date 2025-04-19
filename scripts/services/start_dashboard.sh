#!/bin/bash

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


# ======================================================
# 🌟🌟🌟 OMEGA RASTA BTC DASHBOARD LAUNCHER 🌟🌟🌟
# ======================================================
# This script sets up and launches the divine OMEGA RASTA BTC DASHBOARD
# with all necessary dependencies and cosmic energy alignment.

echo "🌿🌿🌿 INITIALIZING OMEGA RASTA BTC DASHBOARD 🌿🌿🌿"
echo "JAH BLESS THE DIVINE TRADING ENERGIES!"

# Set up color codes for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check if running in virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${YELLOW}⚠️ No virtual environment detected! Creating one...${NC}"
    
    # Check if pipenv is installed
    if ! command -v pipenv &> /dev/null; then
        echo -e "${CYAN}Installing pipenv...${NC}"
        pip install pipenv
    fi
    
    # Setup virtual environment
    echo -e "${CYAN}Setting up virtual environment...${NC}"
    pipenv install
    
    echo -e "${GREEN}✅ Virtual environment created!${NC}"
    echo -e "${YELLOW}⚠️ Please run: pipenv shell${NC}"
    echo -e "${YELLOW}⚠️ Then run this script again inside the virtual environment${NC}"
    exit 1
fi

# Install required packages
echo -e "${CYAN}📦 Installing divine dependencies...${NC}"
pip install -r requirements.txt

# Ensure Redis is running
echo -e "${CYAN}🔄 Checking Redis connection...${NC}"
redis-cli ping > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️ Redis not running, attempting to start...${NC}"
    
    # Check if redis-server is installed
    if command -v redis-server &> /dev/null; then
        redis-server --daemonize yes
        echo -e "${GREEN}✅ Redis server started!${NC}"
    else
        echo -e "${RED}❌ Redis not installed or not in PATH!${NC}"
        echo -e "${YELLOW}Please install Redis or ensure it's in your PATH${NC}"
        echo -e "Visit: https://redis.io/download"
        exit 1
    fi
fi

# Create necessary directories
echo -e "${CYAN}📂 Creating log directories...${NC}"
mkdir -p logs

# Set environment variables
export PYTHONPATH=$PYTHONPATH:$(pwd)
export OMEGA_BTC_HOME=$(pwd)
export OMEGA_ENV="production"

# Initialize mock data if needed
echo -e "${CYAN}🔢 Initializing mock data...${NC}"
python -c "
import redis
import json
from omega_ai.visualization.dashboard import RedisKeys

try:
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    
    # Check if data exists
    if not r.exists(RedisKeys.LIVE_BATTLE_STATE):
        print('Initializing mock battle state...')
        battle_state = {
            'btc_price': 55000.0,
            'btc_history': [52000.0, 53000.0, 54000.0, 55000.0],
            'day': 1,
            'session': 1,
        }
        r.set(RedisKeys.LIVE_BATTLE_STATE, json.dumps(battle_state))
    
    if not r.exists(RedisKeys.LIVE_TRADER_DATA):
        print('Initializing mock trader data...')
        trader_data = {
            'strategic': {
                'pnl': 1250.0,
                'trades': [{'profit': 250}, {'profit': 1000}],
                'emotional_state': 'confident',
                'confidence': 0.8,
                'achievements': ['fibonacci_master', 'zen_trader'],
                'bio_energy': 85
            },
            'aggressive': {
                'pnl': -500.0, 
                'trades': [{'profit': 750}, {'profit': -1250}],
                'emotional_state': 'fearful',
                'confidence': 0.4,
                'achievements': ['risk_taker'],
                'bio_energy': 65
            },
            'newbie': {
                'pnl': -1000.0,
                'trades': [{'profit': -500}, {'profit': -500}],
                'emotional_state': 'panicked',
                'confidence': 0.2,
                'achievements': [],
                'bio_energy': 40
            },
            'scalper': {
                'pnl': 800.0,
                'trades': [{'profit': 100}, {'profit': 200}, {'profit': 200}, {'profit': 300}],
                'emotional_state': 'neutral',
                'confidence': 0.7,
                'achievements': ['quick_scalper'],
                'bio_energy': 75
            }
        }
        r.set(RedisKeys.LIVE_TRADER_DATA, json.dumps(trader_data))
    
    if not r.exists(RedisKeys.SCHUMANN_RESONANCE):
        print('Initializing Schumann resonance data...')
        r.set(RedisKeys.SCHUMANN_RESONANCE, '7.83')
    
    print('Redis mock data initialization complete!')
except Exception as e:
    print(f'Error initializing mock data: {e}')
"

# Launch the dashboard
echo -e "${GREEN}🚀 LAUNCHING OMEGA RASTA BTC DASHBOARD 🚀${NC}"
echo -e "${YELLOW}MAY JAH GUIDE YOUR TRADING DECISIONS!${NC}"
echo -e "${CYAN}Starting server on port 8051...${NC}"

# Run the dashboard
python -m omega_ai.visualization.dashboard

# This line will only execute if the dashboard crashes or is stopped
echo -e "${RED}📉 DASHBOARD STOPPED 📉${NC}"
echo -e "${YELLOW}Check the logs for any issues.${NC}" 