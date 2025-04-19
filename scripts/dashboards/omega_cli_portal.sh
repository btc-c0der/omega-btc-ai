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


# ╔══════════════════════════════════════════════════════════════════════╗
# ║           "OMEGA CLI DIVINE PORTAL" c/o VIRGIL ABLOH                 ║
# ║           "TECHNICAL INTERFACE" FOR OMEGA BTC AI                     ║
# ║                                                                      ║
# ║           GPU (General Public Universal) License 1.0                 ║
# ║           "OMEGA BTC AI DIVINE COLLECTIVE"                           ║
# ║           Date: "2025-03-26"                                         ║
# ╚══════════════════════════════════════════════════════════════════════╝

# ANSI color codes
BLACK='\033[0;30m'        # OFF-WHITE signature black
WHITE='\033[1;37m'        # OFF-WHITE signature white
ORANGE='\033[0;33m'       # OFF-WHITE signature orange
GREEN='\033[0;32m'        # Accent color
BLUE='\033[0;34m'         # Accent color
RED='\033[0;31m'          # Error color
YELLOW='\033[1;33m'       # Warning color
RESET='\033[0m'           # Reset to default

# Detect terminal size for optimal display
TERM_WIDTH=$(tput cols)
TERM_HEIGHT=$(tput lines)

# Session name
SESSION_NAME="OMEGA_PORTAL"

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo -e "${RED}\"ERROR:\" tmux is not installed. Please install tmux to run the \"OMEGA CLI DIVINE PORTAL\".${RESET}"
    exit 1
fi

# Kill any existing session with the same name
tmux kill-session -t "$SESSION_NAME" 2>/dev/null

# Function to display ASCII art logo in OFF-WHITE style
display_logo() {
    clear
    echo -e "${WHITE}"
    echo "\"OMEGA\""
    echo ""
    echo "      ██████╗ ███╗   ███╗███████╗ ██████╗  █████╗ "
    echo "     ██╔═══██╗████╗ ████║██╔════╝██╔════╝ ██╔══██╗"
    echo "     ██║   ██║██╔████╔██║█████╗  ██║  ███╗███████║"
    echo "     ██║   ██║██║╚██╔╝██║██╔══╝  ██║   ██║██╔══██║"
    echo "     ╚██████╔╝██║ ╚═╝ ██║███████╗╚██████╔╝██║  ██║"
    echo "      ╚═════╝ ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝"
    echo ""
    echo "\"CLI PORTAL\""
    echo ""
    echo -e "${BLACK}${WHITE}                           FOR \"DIVINE GRID\" ACCESS                          ${RESET}"
    echo -e "${BLACK}${WHITE}                           c/o \"VIRGIL ABLOH\"                                ${RESET}"
    echo ""
    echo -e "${ORANGE}          \"TECHNICAL INTERFACE\" \"2025\" \"OFF-WHITE™\" ${RESET}"
    echo ""
}

# Define script groups in OFF-WHITE style
script_groups=(
    "\"CORE SYSTEMS\""
    "\"MARKET MONITORS\""
    "\"TRADING SYSTEMS\""
    "\"VISUALIZATION\""
    "\"DIAGNOSTICS & TOOLS\""
    "\"SPECIAL SYSTEMS\""
    "\"NFT SYSTEMS\""
)

# Define script commands
script_commands=(
    # Core Systems
    "python run_omega_system.py"
    "python run_omega_system.py --auto-heal --background"
    "python scripts/run_omega_dump.py --process-warnings"
    "python run_omega_system.py --divine-mode"
    
    # Market Monitors
    "./run_market_trends_tests.py --only-visualize"
    "./run_redis_only_monitor.sh"
    "./run_dual_divine_monitor.sh"
    "python run_enhanced_market_monitor.py --dynamic"
    
    # Trading Systems
    "python run_trap_aware_dual_traders.py"
    "python run_dual_position_traders.py"
    "./run_elite_exit_trader.sh"
    "./scripts/fibonacci_trader.sh"
    
    # Visualization
    "python btcusdt_divine_flow_demo.py"
    "python serve_visualization.py"
    "./divine_coverage_visualizer.py"
    "python run_divine_3d_visualization.py"
    
    # Diagnostics & Tools
    "python check_redis_data.py"
    "python check_warnings.py"
    "python test_trend_analysis.py"
    "python generate_market_data.py"
    
    # Divine Special Systems
    "./run_gamon_trinity_analyzer.sh"
    "./run_gamon_trinity_live.sh"
    "./run_gamon_trinity_predictor.sh"
    "python create_omega_genesis_block.py"

    # NFT Systems
    "python scripts/generate_whale_nft.py"
    "python scripts/create_custom_nft.py"
    "python scripts/generate_divine_dashboard.py"
    "python scripts/run_omega_dump.py --nft-mode"
)

# Define script descriptions in OFF-WHITE style
script_descriptions=(
    # Core Systems
    "\"MAIN OMEGA SYSTEM\" - Starts essential services"
    "\"AUTO-HEALING MODE\" - Background processing"
    "\"LOG MANAGEMENT\" - Process warnings and errors"
    "\"DIVINE MODE\" - Enhanced system capabilities"
    
    # Market Monitors
    "\"MARKET TRENDS\" - With cosmic visualization"
    "\"REDIS MONITOR\" - Pure data analysis dashboard"
    "\"DUAL DISPLAY\" - Two-panel monitoring system"
    "\"DYNAMIC INTERFACE\" - Responsive market monitoring"
    
    # Trading Systems
    "\"TRAP AWARE\" - Advanced dual trading system"
    "\"POSITION TRADING\" - Classic dual position system"
    "\"ELITE EXIT\" - Strategic position exit management"
    "\"FIBONACCI TRADER\" - Golden ratio based trading"
    
    # Visualization
    "\"DIVINE FLOW\" - BTCUSDT with whale detection"
    "\"WEB DASHBOARD\" - Browser-based visualization"
    "\"COVERAGE VISUALIZER\" - Market pattern display"
    "\"3D VISUALIZATION\" - Immersive market display"
    
    # Diagnostics & Tools
    "\"REDIS CHECK\" - Database structure examination"
    "\"WARNING ANALYSIS\" - System anomaly detection"
    "\"TREND TESTING\" - Algorithm validation tool"
    "\"DATA GENERATOR\" - Create synthetic market data"
    
    # Divine Special Systems
    "\"TRINITY ANALYZER\" - BTC state analysis"
    "\"TRINITY LIVE\" - Real-time market analysis"
    "\"TRINITY PREDICTOR\" - Advanced forecasting"
    "\"GENESIS BLOCK\" - Create tracking foundation"

    # NFT Systems
    "\"WHALE NFT\" - Generate divine whale NFTs"
    "\"CUSTOM NFT\" - Create personalized divine NFTs"
    "\"NFT DASHBOARD\" - Divine NFT visualization"
    "\"NFT MODE\" - Enhanced NFT tracking system"
)

# Function to render the main menu in OFF-WHITE style
render_main_menu() {
    display_logo
    
    echo -e "${WHITE}╔══ \"CATEGORIES\" ═══════════════════════════════════════╗${RESET}"
    
    for i in "${!script_groups[@]}"; do
        echo -e "${WHITE}║  ${BLACK}${WHITE} $((i+1)) ${RESET}${WHITE} ${script_groups[$i]} ${RESET} "
    done
    
    echo -e "${WHITE}╠═══════════════════════════════════════════════════════╣${RESET}"
    echo -e "${WHITE}║  ${BLACK}${WHITE} Q ${RESET}${WHITE} \"QUIT\" ${RESET} "
    echo -e "${WHITE}╚═══════════════════════════════════════════════════════╝${RESET}"
    echo ""
    echo -e "${ORANGE}\"SELECT CATEGORY:\"${RESET} "
}

# Function to render the script menu for a specific group in OFF-WHITE style
render_script_menu() {
    local group_index=$1
    local group_name="${script_groups[$group_index]}"
    
    display_logo
    
    echo -e "${WHITE}╔══ ${group_name} ════════════════════════════════════════╗${RESET}"
    
    # Calculate start and end indices for this group
    local start_idx=$((group_index * 4))
    local end_idx=$((start_idx + 4))
    
    for ((i=start_idx; i<end_idx; i++)); do
        if [ -n "${script_descriptions[$i]}" ]; then
            echo -e "${WHITE}║  ${BLACK}${WHITE} $((i-start_idx+1)) ${RESET}${WHITE} ${script_descriptions[$i]} ${RESET} "
        fi
    done
    
    echo -e "${WHITE}╠═══════════════════════════════════════════════════════╣${RESET}"
    echo -e "${WHITE}║  ${BLACK}${WHITE} B ${RESET}${WHITE} \"BACK\" ${RESET} "
    echo -e "${WHITE}║  ${BLACK}${WHITE} Q ${RESET}${WHITE} \"QUIT\" ${RESET} "
    echo -e "${WHITE}╚═══════════════════════════════════════════════════════╝${RESET}"
    echo ""
    echo -e "${ORANGE}\"SELECT OPTION:\"${RESET} "
}

# Function to create tmux windows for each script category
setup_tmux_session() {
    # Create a new tmux session
    tmux new-session -d -s "$SESSION_NAME" -n "CONTROL"
    
    # Configure tmux appearance in OFF-WHITE style
    tmux set -g status-style "bg=black,fg=white"
    tmux set -g pane-border-style "fg=white"
    tmux set -g pane-active-border-style "fg=colour208" # Orange
    tmux set -g status-left "#[fg=white,bold]\"OMEGA PORT4L\" #[fg=white]\"DIVINE GRID\" #[fg=white]| "
    tmux set -g status-right "#[fg=white]%H:%M:%S #[fg=white]| #[fg=white,bold]\"OFF-WHITE™\" #[fg=default]"
    tmux set -g status-left-length 50
    tmux set -g status-right-length 50
    
    # Create a window for each category
    for i in "${!script_groups[@]}"; do
        local window_name=$(echo "${script_groups[$i]}" | tr -d '"' | tr ' ' '_')
        tmux new-window -t "$SESSION_NAME:" -n "$window_name"
    done
    
    # Set up the control window
    tmux send-keys -t "$SESSION_NAME:CONTROL" "clear && echo -e \"${WHITE}\\\"OMEGA CLI DIVINE PORTAL\\\"${RESET}\\n\\n\\\"Use Ctrl+B, N to navigate to next window\\\"\\n\\\"Use Ctrl+B, P to navigate to previous window\\\"\\n\\\"Use Ctrl+B, number to jump to specific window\\\"\\n\\\"Use Ctrl+B, D to detach from session\\\"\\n\\n\\\"WELCOME TO THE DIVINE GRID\\\"\\n\\\"c/o VIRGIL ABLOH\\\"\\n\\n\\\"Press any key to display the main menu...\\\"\"" C-m
    
    # Return to the control window
    tmux select-window -t "$SESSION_NAME:CONTROL"
}

# Function to run a script in a new tmux window
run_script() {
    local group_index=$1
    local script_index=$2
    local command_index=$((group_index * 4 + script_index - 1))
    local command="${script_commands[$command_index]}"
    local description="${script_descriptions[$command_index]}"
    local window_name=$(echo "$description" | tr -d '"' | cut -d'-' -f1 | tr ' ' '_')
    
    # Check if the script exists
    if [[ -z "$command" ]]; then
        echo -e "${RED}\"ERROR:\" Script not found.${RESET}"
        return 1
    fi
    
    # Create a new window for the script
    local window_id=$(tmux new-window -t "$SESSION_NAME:" -n "$window_name" -P)
    
    # Configure the window in OFF-WHITE style
    tmux send-keys -t "$window_id" "clear && echo -e \"${WHITE}\\\"STARTING:\\\" ${description}${RESET}\\n\\n${WHITE}\\\"COMMAND:\\\" ${command}${RESET}\\n\\n\"" C-m
    tmux send-keys -t "$window_id" "$command" C-m
    
    # Switch to the new window
    tmux select-window -t "$window_id"
    
    return 0
}

# Function to handle the main menu interaction
handle_main_menu() {
    local choice=""
    
    while true; do
        render_main_menu
        read -r choice
        
        case "$choice" in
            [1-7])
                handle_script_menu "$choice"
                ;;
            [Qq])
                echo -e "${WHITE}\"OMEGA CLI DIVINE PORTAL\" session ended. \"HARMONY RESTORED\"${RESET}"
                echo -e "${ORANGE}\"JAH JAH BLESS\"${RESET}"
                echo -e "${WHITE}\"c/o VIRGIL ABLOH\"${RESET}"
                exit 0
                ;;
            *)
                echo -e "${RED}\"INVALID CHOICE\" Please try again.${RESET}"
                ;;
        esac
    done
}

# Function to handle the script menu interaction
handle_script_menu() {
    local group_index=$((choice-1))
    local choice=""
    
    while true; do
        render_script_menu "$group_index"
        read -r choice
        
        case "$choice" in
            [1-4])
                run_script "$group_index" "$choice"
                ;;
            [Bb])
                return
                ;;
            [Qq])
                echo -e "${WHITE}\"OMEGA CLI DIVINE PORTAL\" session ended. \"HARMONY RESTORED\"${RESET}"
                echo -e "${ORANGE}\"JAH JAH BLESS\"${RESET}"
                echo -e "${WHITE}\"c/o VIRGIL ABLOH\"${RESET}"
                exit 0
                ;;
            *)
                echo -e "${RED}\"INVALID CHOICE\" Please try again.${RESET}"
                ;;
        esac
    done
}

# Main execution
setup_tmux_session
handle_main_menu 