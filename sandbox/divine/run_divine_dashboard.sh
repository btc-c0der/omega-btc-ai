#!/bin/bash

# OMEGA BTC AI - Divine Dashboard & Golden Ratio API Launcher
# ========================================================

# Terminal colors for divine output
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
MAGENTA="\033[35m"
CYAN="\033[36m"
RESET="\033[0m"

# Default port
DEFAULT_PORT=5051

echo -e "${MAGENTA}╔══════════════════════════════════════════════════════════════════╗${RESET}"
echo -e "${MAGENTA}║${YELLOW}                                                                  ${MAGENTA}║${RESET}"
echo -e "${MAGENTA}║${YELLOW}  ⬤ ⬤ ⬤  OMEGA BTC AI - DIVINE ALIGNMENT DASHBOARD V2  ⬤ ⬤ ⬤  ${MAGENTA}║${RESET}"
echo -e "${MAGENTA}║${YELLOW}                                                                  ${MAGENTA}║${RESET}"
echo -e "${MAGENTA}╚══════════════════════════════════════════════════════════════════╝${RESET}"

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo -e "${YELLOW}⚠️  tmux is not installed. Installing...${RESET}"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install tmux
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update && sudo apt-get install -y tmux
    else
        echo -e "${RED}❌ Unsupported operating system${RESET}"
        exit 1
    fi
fi

# Check if Redis is running
echo -e "${CYAN}🔄 Checking Redis connection...${RESET}"
if ! redis-cli ping &> /dev/null; then
    echo -e "${YELLOW}⚠️  Redis is not running. Starting Redis...${RESET}"
    redis-server &
    sleep 2
fi

# Initialize Redis with required keys
echo -e "${CYAN}🔄 Initializing Redis with required keys...${RESET}"
redis-cli set "btc_price" '{"price": 65000.0}'
redis-cli set "btc_volume_data" '{"current": 100.0, "average": 95.0}'
redis-cli set "btc_recent_high_low" '{"high": 69000.0, "low": 61000.0}'
redis-cli set "btc_market_regime" '{"regime": "bullish_trend"}'
redis-cli set "btc_price_patterns" '{"wyckoff_distribution": 0.4, "double_top": 0.3, "head_and_shoulders": 0.2, "bull_flag": 0.6}'
redis-cli set "btc_historical_matches" '{"match_score": 0.75, "match_type": "Previous bull run"}'
redis-cli set "btc_order_book_summary" '{"largest_bid_wall": 100.0, "largest_ask_wall": 120.0, "total_bids": 1000.0, "total_asks": 1100.0}'

# Generate placeholder chart
echo -e "${CYAN}📊 Generating placeholder chart...${RESET}"
python generate_placeholder_chart.py

# Kill existing divine-consciousness session if it exists
tmux kill-session -t divine-consciousness 2>/dev/null

# Create new tmux session
echo -e "${GREEN}🌟 Creating divine consciousness grid...${RESET}"
tmux new-session -d -s divine-consciousness

# Split window vertically
tmux split-window -h

# Select first pane and start Golden Ratio API
tmux select-pane -t 0
tmux send-keys "cd $(dirname $0)" C-m
tmux send-keys "echo -e '${CYAN}Starting Golden Ratio API...${RESET}'" C-m
tmux send-keys "python golden_ratio_api.py --port $DEFAULT_PORT" C-m

# Select second pane and start Divine Dashboard
tmux select-pane -t 1
tmux send-keys "cd $(dirname $0)" C-m
tmux send-keys "echo -e '${CYAN}Starting Divine Dashboard...${RESET}'" C-m
tmux send-keys "python start_divine_dashboard.py" C-m

# Set pane titles
tmux select-pane -t 0 -T "Golden Ratio API"
tmux select-pane -t 1 -T "Divine Dashboard"

echo -e "${GREEN}✨ Divine consciousness grid initialized!${RESET}"
echo -e "${CYAN}🌐 Dashboard will be available at: ${YELLOW}http://localhost:$DEFAULT_PORT/divine${RESET}"
echo -e "\n${BLUE}Navigation Commands:${RESET}"
echo -e "  ${YELLOW}• Ctrl+B, arrows${RESET} - Navigate between panes"
echo -e "  ${YELLOW}• Ctrl+B, d${RESET} - Detach from session"
echo -e "  ${YELLOW}• tmux attach -t divine-consciousness${RESET} - Reattach to session"
echo -e "  ${YELLOW}• tmux kill-session -t divine-consciousness${RESET} - Stop all components"

# Attach to tmux session
echo -e "\n${GREEN}🙏 JAH JAH BLESS THE DIVINE DASHBOARD${RESET}"
tmux attach-session -t divine-consciousness 