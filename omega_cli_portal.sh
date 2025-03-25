#!/bin/bash

# ╔══════════════════════════════════════════════════════════════════════╗
# ║           OMEGA CLI DIVINE PORTAL TO THE OMEGA GRID                  ║
# ║           A Total H4xor Interface to the OMEGA BTC AI                ║
# ║                                                                      ║
# ║           GPU (General Public Universal) License 1.0                 ║
# ║           OMEGA BTC AI DIVINE COLLECTIVE                             ║
# ║           Date: 2025-03-26                                           ║
# ╚══════════════════════════════════════════════════════════════════════╝

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
RESET='\033[0m'

# Detect terminal size for optimal display
TERM_WIDTH=$(tput cols)
TERM_HEIGHT=$(tput lines)

# Session name
SESSION_NAME="OMEGA_PORTAL"

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo -e "${RED}ERROR: tmux is not installed. Please install tmux to run the OMEGA CLI DIVINE PORTAL.${RESET}"
    exit 1
fi

# Kill any existing session with the same name
tmux kill-session -t "$SESSION_NAME" 2>/dev/null

# Function to display ASCII art logo
display_logo() {
    clear
    echo -e "${MAGENTA}"
    echo "  ██████╗ ███╗   ███╗███████╗ ██████╗  █████╗     ██████╗  ██████╗ ██████╗ ████████╗██╗  ██╗██╗     "
    echo " ██╔═══██╗████╗ ████║██╔════╝██╔════╝ ██╔══██╗    ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██║  ██║██║     "
    echo " ██║   ██║██╔████╔██║█████╗  ██║  ███╗███████║    ██████╔╝██║   ██║██████╔╝   ██║   ███████║██║     "
    echo " ██║   ██║██║╚██╔╝██║██╔══╝  ██║   ██║██╔══██║    ██╔═══╝ ██║   ██║██╔══██╗   ██║   ██╔══██║██║     "
    echo " ╚██████╔╝██║ ╚═╝ ██║███████╗╚██████╔╝██║  ██║    ██║     ╚██████╔╝██║  ██║   ██║   ██║  ██║███████╗"
    echo "  ╚═════╝ ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝    ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝"
    echo -e "${GREEN}                           DIVINE PORTAL TO THE OMEGA GRID                               ${RESET}"
    echo ""
}

# Define script groups
script_groups=(
    "Core Systems"
    "Market Monitors"
    "Trading Systems"
    "Visualization"
    "Diagnostics & Tools"
    "Divine Special Systems"
)

# Define script commands
script_commands=(
    # Core Systems
    "python run_omega_system.py"
    "python run_omega_system.py --auto-heal --background"
    "python scripts/run_omega_dump.py --process-warnings"
    
    # Market Monitors
    "./run_market_trends_tests.py --only-visualize"
    "./run_redis_only_monitor.sh"
    "./run_dual_divine_monitor.sh"
    "python run_enhanced_market_monitor.py --dynamic"
    "./run_dual_focus_monitors.sh"
    "./run_market_monitors.sh"
    
    # Trading Systems
    "python run_trap_aware_dual_traders.py"
    "python run_dual_position_traders.py"
    "./run_elite_exit_trader.sh"
    "./scripts/fibonacci_trader.sh"
    
    # Visualization
    "python btcusdt_divine_flow_demo.py"
    "python serve_visualization.py"
    "./divine_coverage_visualizer.py"
    
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
)

# Define script descriptions
script_descriptions=(
    # Core Systems
    "Main Omega System - Starts all essential services"
    "Auto-healing mode with background processing"
    "Divine log management system for warnings and errors"
    
    # Market Monitors
    "Visualize market trends and cosmic coverage"
    "Pure Redis-driven market analysis dashboard"
    "Two-panel divine monitoring dashboard"
    "Dynamic market monitoring with improved interface"
    "Dual focus monitors optimized for vertical displays"
    "Run multiple market monitors in different modes"
    
    # Trading Systems
    "Advanced dual traders with trap awareness"
    "Classic dual position trading system"
    "Elite exit trading strategies for optimal positioning"
    "Fibonacci-based trading system with automatic levels"
    
    # Visualization
    "BTCUSDT Divine Flow Demo with animated whale sonar"
    "Serve visualization dashboard on local web server"
    "Divine coverage visualization for market trends"
    
    # Diagnostics & Tools
    "Examine Redis database contents and structure"
    "Analysis of system warnings and anomalies"
    "Test the trend analysis algorithms"
    "Generate synthetic market data for testing"
    
    # Divine Special Systems
    "Trinity Analyzer for BTC market states"
    "Live Trinity analysis with real-time data"
    "Advanced predictive system using trinity models"
    "Generate the Omega Genesis Block for divine tracking"
)

# Function to render the main menu
render_main_menu() {
    display_logo
    
    echo -e "${CYAN}║ SELECT A CATEGORY:${RESET}"
    echo -e "${YELLOW}╠════════════════════════════════════════════════════════════════════════════════════╣${RESET}"
    
    for i in "${!script_groups[@]}"; do
        echo -e "${GREEN}║ $((i+1)))${RESET} ${WHITE}${script_groups[$i]}${RESET}"
    done
    
    echo -e "${YELLOW}╠════════════════════════════════════════════════════════════════════════════════════╣${RESET}"
    echo -e "${CYAN}║ Q)${RESET} ${WHITE}Quit${RESET}"
    echo -e "${YELLOW}╚════════════════════════════════════════════════════════════════════════════════════╝${RESET}"
    echo ""
    echo -e "${MAGENTA}Enter your choice:${RESET} "
}

# Function to render the script menu for a specific group
render_script_menu() {
    local group_index=$1
    local group_name="${script_groups[$group_index]}"
    
    display_logo
    
    echo -e "${CYAN}║ ${group_name} - SELECT A SCRIPT:${RESET}"
    echo -e "${YELLOW}╠════════════════════════════════════════════════════════════════════════════════════╣${RESET}"
    
    # Calculate start and end indices for this group
    local start_idx=$((group_index * 4))
    local end_idx=$((start_idx + 4))
    
    for ((i=start_idx; i<end_idx; i++)); do
        if [ -n "${script_descriptions[$i]}" ]; then
            echo -e "${GREEN}║ $((i-start_idx+1)))${RESET} ${WHITE}${script_descriptions[$i]}${RESET}"
        fi
    done
    
    echo -e "${YELLOW}╠════════════════════════════════════════════════════════════════════════════════════╣${RESET}"
    echo -e "${CYAN}║ B)${RESET} ${WHITE}Back to main menu${RESET}"
    echo -e "${CYAN}║ Q)${RESET} ${WHITE}Quit${RESET}"
    echo -e "${YELLOW}╚════════════════════════════════════════════════════════════════════════════════════╝${RESET}"
    echo ""
    echo -e "${MAGENTA}Enter your choice:${RESET} "
}

# Function to create tmux windows for each script category
setup_tmux_session() {
    # Create a new tmux session
    tmux new-session -d -s "$SESSION_NAME" -n "CONTROL"
    
    # Configure tmux appearance
    tmux set -g status-style "bg=black,fg=green"
    tmux set -g pane-border-style "fg=blue"
    tmux set -g pane-active-border-style "fg=magenta"
    tmux set -g status-left "#[fg=magenta,bold][OMEGA PORT4L] #[fg=cyan]Divine Grid Access #[fg=yellow]| "
    tmux set -g status-right "#[fg=cyan]%H:%M:%S #[fg=yellow]| #[fg=green,bold]DIVINE MODE #[fg=default]"
    tmux set -g status-left-length 50
    tmux set -g status-right-length 50
    
    # Create a window for each category
    for i in "${!script_groups[@]}"; do
        local window_name=$(echo "${script_groups[$i]}" | tr ' ' '_')
        tmux new-window -t "$SESSION_NAME:" -n "$window_name"
    done
    
    # Set up the control window
    tmux send-keys -t "$SESSION_NAME:CONTROL" 'clear && echo -e "\033[1;35mOMEGA CLI DIVINE PORTAL TO THE OMEGA GRID\033[0m\n\nUse Ctrl+B, N to navigate to next window\nUse Ctrl+B, P to navigate to previous window\nUse Ctrl+B, number to jump to specific window\nUse Ctrl+B, D to detach from session\n\nWelcome to the divine grid. Press any key to display the main menu..."' C-m
    
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
    local window_name=$(echo "$description" | cut -d'-' -f1 | tr ' ' '_')
    
    # Check if the script exists
    if [[ -z "$command" ]]; then
        echo -e "${RED}Error: Script not found.${RESET}"
        return 1
    fi
    
    # Create a new window for the script
    local window_id=$(tmux new-window -t "$SESSION_NAME:" -n "$window_name" -P)
    
    # Configure the window
    tmux send-keys -t "$window_id" "clear && echo -e \"${YELLOW}Starting: ${WHITE}${description}${RESET}\n\n${CYAN}Command: ${GREEN}${command}${RESET}\n\n\"" C-m
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
            [1-6])
                handle_script_menu "$choice"
                ;;
            [Qq])
                echo -e "${YELLOW}OMEGA CLI DIVINE PORTAL session ended. Harmony restored.${RESET}"
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid choice. Please try again.${RESET}"
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
                echo -e "${YELLOW}OMEGA CLI DIVINE PORTAL session ended. Harmony restored.${RESET}"
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid choice. Please try again.${RESET}"
                ;;
        esac
    done
}

# Main execution
setup_tmux_session
handle_main_menu 