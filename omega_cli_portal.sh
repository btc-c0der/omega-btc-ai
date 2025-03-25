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

# Group scripts by category for the menu
declare -A script_groups
script_groups=(
    ["1_CORE_SYSTEMS"]="Core Systems"
    ["2_MONITORS"]="Market Monitors"
    ["3_TRADING"]="Trading Systems"
    ["4_VISUALIZATION"]="Visualization"
    ["5_DIAGNOSTICS"]="Diagnostics & Tools"
    ["6_DIVINE_SPECIAL"]="Divine Special Systems"
)

# Define script commands by group
declare -A script_commands
script_commands=(
    # Core Systems
    ["1_1_RUN_OMEGA_SYSTEM"]="python run_omega_system.py"
    ["1_2_RUN_OMEGA_AUTO_HEAL"]="python run_omega_system.py --auto-heal --background"
    ["1_3_OMEGA_DUMP"]="python scripts/run_omega_dump.py --process-warnings"
    
    # Market Monitors
    ["2_1_MARKET_TRENDS"]="./run_market_trends_tests.py --only-visualize"
    ["2_2_REDIS_ONLY_MONITOR"]="./run_redis_only_monitor.sh"
    ["2_3_DUAL_DIVINE_MONITOR"]="./run_dual_divine_monitor.sh"
    ["2_4_ENHANCED_MARKET_MONITOR"]="python run_enhanced_market_monitor.py --dynamic"
    ["2_5_DUAL_FOCUS_MONITORS"]="./run_dual_focus_monitors.sh"
    ["2_6_MARKET_MONITORS"]="./run_market_monitors.sh"
    
    # Trading Systems
    ["3_1_TRAP_AWARE_DUAL_TRADERS"]="python run_trap_aware_dual_traders.py"
    ["3_2_DUAL_POSITION_TRADERS"]="python run_dual_position_traders.py"
    ["3_3_ELITE_EXIT_TRADER"]="./run_elite_exit_trader.sh"
    ["3_4_FIBONACCI_TRADER"]="./scripts/fibonacci_trader.sh"
    
    # Visualization
    ["4_1_DIVINE_FLOW_DEMO"]="python btcusdt_divine_flow_demo.py"
    ["4_2_SERVE_VISUALIZATION"]="python serve_visualization.py"
    ["4_3_DIVINE_COVERAGE"]="./divine_coverage_visualizer.py"
    
    # Diagnostics & Tools
    ["5_1_CHECK_REDIS_DATA"]="python check_redis_data.py"
    ["5_2_CHECK_WARNINGS"]="python check_warnings.py"
    ["5_3_TEST_TREND_ANALYSIS"]="python test_trend_analysis.py"
    ["5_4_GENERATE_MARKET_DATA"]="python generate_market_data.py"
    
    # Divine Special Systems
    ["6_1_GAMON_TRINITY_ANALYZER"]="./run_gamon_trinity_analyzer.sh"
    ["6_2_GAMON_TRINITY_LIVE"]="./run_gamon_trinity_live.sh"
    ["6_3_GAMON_TRINITY_PREDICTOR"]="./run_gamon_trinity_predictor.sh"
    ["6_4_DIVINE_BLOCKCHAIN"]="python create_omega_genesis_block.py"
)

# Description for each script
declare -A script_descriptions
script_descriptions=(
    # Core Systems
    ["1_1_RUN_OMEGA_SYSTEM"]="Main Omega System - Starts all essential services"
    ["1_2_RUN_OMEGA_AUTO_HEAL"]="Auto-healing mode with background processing"
    ["1_3_OMEGA_DUMP"]="Divine log management system for warnings and errors"
    
    # Market Monitors
    ["2_1_MARKET_TRENDS"]="Visualize market trends and cosmic coverage"
    ["2_2_REDIS_ONLY_MONITOR"]="Pure Redis-driven market analysis dashboard"
    ["2_3_DUAL_DIVINE_MONITOR"]="Two-panel divine monitoring dashboard"
    ["2_4_ENHANCED_MARKET_MONITOR"]="Dynamic market monitoring with improved interface"
    ["2_5_DUAL_FOCUS_MONITORS"]="Dual focus monitors optimized for vertical displays"
    ["2_6_MARKET_MONITORS"]="Run multiple market monitors in different modes"
    
    # Trading Systems
    ["3_1_TRAP_AWARE_DUAL_TRADERS"]="Advanced dual traders with trap awareness"
    ["3_2_DUAL_POSITION_TRADERS"]="Classic dual position trading system"
    ["3_3_ELITE_EXIT_TRADER"]="Elite exit trading strategies for optimal positioning"
    ["3_4_FIBONACCI_TRADER"]="Fibonacci-based trading system with automatic levels"
    
    # Visualization
    ["4_1_DIVINE_FLOW_DEMO"]="BTCUSDT Divine Flow Demo with animated whale sonar"
    ["4_2_SERVE_VISUALIZATION"]="Serve visualization dashboard on local web server"
    ["4_3_DIVINE_COVERAGE"]="Divine coverage visualization for market trends"
    
    # Diagnostics & Tools
    ["5_1_CHECK_REDIS_DATA"]="Examine Redis database contents and structure"
    ["5_2_CHECK_WARNINGS"]="Analysis of system warnings and anomalies"
    ["5_3_TEST_TREND_ANALYSIS"]="Test the trend analysis algorithms"
    ["5_4_GENERATE_MARKET_DATA"]="Generate synthetic market data for testing"
    
    # Divine Special Systems
    ["6_1_GAMON_TRINITY_ANALYZER"]="Trinity Analyzer for BTC market states"
    ["6_2_GAMON_TRINITY_LIVE"]="Live Trinity analysis with real-time data"
    ["6_3_GAMON_TRINITY_PREDICTOR"]="Advanced predictive system using trinity models"
    ["6_4_DIVINE_BLOCKCHAIN"]="Generate the Omega Genesis Block for divine tracking"
)

# Function to render the main menu
render_main_menu() {
    display_logo
    
    echo -e "${CYAN}║ SELECT A CATEGORY:${RESET}"
    echo -e "${YELLOW}╠════════════════════════════════════════════════════════════════════════════════════╣${RESET}"
    
    local idx=1
    for group_key in "${!script_groups[@]}"; do
        local group_name="${script_groups[$group_key]}"
        echo -e "${GREEN}║ ${idx})${RESET} ${WHITE}${group_name}${RESET}"
        ((idx++))
    done
    
    echo -e "${YELLOW}╠════════════════════════════════════════════════════════════════════════════════════╣${RESET}"
    echo -e "${CYAN}║ Q)${RESET} ${WHITE}Quit${RESET}"
    echo -e "${YELLOW}╚════════════════════════════════════════════════════════════════════════════════════╝${RESET}"
    echo ""
    echo -e "${MAGENTA}Enter your choice:${RESET} "
}

# Function to render the script menu for a specific group
render_script_menu() {
    local group_key="$1"
    local group_name="${script_groups[$group_key]}"
    
    display_logo
    
    echo -e "${CYAN}║ ${group_name} - SELECT A SCRIPT:${RESET}"
    echo -e "${YELLOW}╠════════════════════════════════════════════════════════════════════════════════════╣${RESET}"
    
    local script_keys=($(echo "${!script_commands[@]}" | tr ' ' '\n' | grep "^${group_key:0:1}_" | sort))
    local idx=1
    
    for script_key in "${script_keys[@]}"; do
        local script_desc="${script_descriptions[$script_key]}"
        echo -e "${GREEN}║ ${idx})${RESET} ${WHITE}${script_desc}${RESET}"
        ((idx++))
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
    for group_key in "${!script_groups[@]}"; do
        local group_name="${script_groups[$group_key]}"
        local window_name=$(echo "$group_name" | tr ' ' '_')
        tmux new-window -t "$SESSION_NAME:" -n "$window_name"
    done
    
    # Set up the control window
    tmux send-keys -t "$SESSION_NAME:CONTROL" 'clear && echo -e "\033[1;35mOMEGA CLI DIVINE PORTAL TO THE OMEGA GRID\033[0m\n\nUse Ctrl+B, N to navigate to next window\nUse Ctrl+B, P to navigate to previous window\nUse Ctrl+B, number to jump to specific window\nUse Ctrl+B, D to detach from session\n\nWelcome to the divine grid. Press any key to display the main menu..."' C-m
    
    # Return to the control window
    tmux select-window -t "$SESSION_NAME:CONTROL"
}

# Function to run a script in a new tmux window
run_script() {
    local script_key="$1"
    local command="${script_commands[$script_key]}"
    local description="${script_descriptions[$script_key]}"
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
        
        # Convert to lowercase
        choice=$(echo "$choice" | tr '[:upper:]' '[:lower:]')
        
        case "$choice" in
            q|quit|exit)
                echo -e "${YELLOW}Exiting OMEGA CLI DIVINE PORTAL...${RESET}"
                return 0
                ;;
            1|2|3|4|5|6)
                # Find the group key by index
                local idx=1
                local selected_group=""
                for group_key in "${!script_groups[@]}"; do
                    if [ "$idx" -eq "$choice" ]; then
                        selected_group="$group_key"
                        break
                    fi
                    ((idx++))
                done
                
                if [ -n "$selected_group" ]; then
                    if ! handle_script_menu "$selected_group"; then
                        return 1
                    fi
                else
                    echo -e "${RED}Invalid choice. Please try again.${RESET}"
                    sleep 1
                fi
                ;;
            *)
                echo -e "${RED}Invalid choice. Please try again.${RESET}"
                sleep 1
                ;;
        esac
    done
}

# Function to handle the script menu interaction
handle_script_menu() {
    local group_key="$1"
    local choice=""
    
    # Get all script keys for this group
    local script_keys=($(echo "${!script_commands[@]}" | tr ' ' '\n' | grep "^${group_key:0:1}_" | sort))
    
    while true; do
        render_script_menu "$group_key"
        read -r choice
        
        # Convert to lowercase
        choice=$(echo "$choice" | tr '[:upper:]' '[:lower:]')
        
        case "$choice" in
            b|back)
                return 0
                ;;
            q|quit|exit)
                echo -e "${YELLOW}Exiting OMEGA CLI DIVINE PORTAL...${RESET}"
                return 1
                ;;
            [1-9]|[1-9][0-9])
                local idx="$choice"
                if [ "$idx" -ge 1 ] && [ "$idx" -le "${#script_keys[@]}" ]; then
                    local script_key="${script_keys[$((idx-1))]}"
                    echo -e "${CYAN}Running ${WHITE}${script_descriptions[$script_key]}${RESET}"
                    sleep 1
                    run_script "$script_key"
                    
                    # Ask if user wants to continue
                    echo ""
                    echo -e "${YELLOW}Script execution complete. Press Enter to return to the menu...${RESET}"
                    read -r
                else
                    echo -e "${RED}Invalid choice. Please try again.${RESET}"
                    sleep 1
                fi
                ;;
            *)
                echo -e "${RED}Invalid choice. Please try again.${RESET}"
                sleep 1
                ;;
        esac
    done
}

# Function to create the interactive menu system (CLI mode)
interactive_cli_menu() {
    display_logo
    echo -e "${YELLOW}Welcome to the OMEGA CLI DIVINE PORTAL TO THE OMEGA GRID${RESET}"
    echo -e "${CYAN}Loading divine systems...${RESET}"
    sleep 1
    
    # Main menu loop
    handle_main_menu
    
    echo -e "${GREEN}Thank you for using the OMEGA CLI DIVINE PORTAL.${RESET}"
    echo -e "${MAGENTA}JAH BLESS YOUR CODE!${RESET}"
}

# Main function to handle user interaction
main() {
    # Check if we should use tmux or direct CLI
    if [ "$1" = "--cli" ]; then
        # Run in CLI mode without tmux
        interactive_cli_menu
    else
        # Set up the tmux session
        setup_tmux_session
        
        # Attach to the tmux session
        tmux attach-session -t "$SESSION_NAME"
        
        # If we get here, the tmux session has ended
        echo -e "${GREEN}OMEGA CLI DIVINE PORTAL session ended. Harmony restored.${RESET}"
    fi
}

# Start the main function with any passed arguments
main "$@" 