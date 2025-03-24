#!/bin/bash

# OMEGA BTC AI - Quad Monitors Launcher
# This script creates a 4-panel tmux session with:
# 1. Position Monitor (RastaBitget)
# 2. Trap Probability Meter
# 3. Entry Persona Monitor
# 4. Exit Persona Monitor

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Print banner
echo -e "${MAGENTA}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                 OMEGA BTC AI - QUAD MONITORS                    ║" 
echo "║          Positions + Traps + Entry + Exit Personas              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if tmux is available
if ! command -v tmux &> /dev/null; then
    echo -e "${YELLOW}Error: tmux is not installed. Please install tmux to use this script.${NC}"
    exit 1
fi

# Default layout options (will be overridden by .env if available)
LAYOUT_MODE="grid"  # grid, vertical, horizontal

# Source settings from .env file if it exists
if [ -f ".env" ]; then
    echo -e "${CYAN}Loading configuration from .env file...${NC}"
    # Extract layout mode value from .env file
    ENV_LAYOUT_MODE=$(grep "^LAYOUT_MODE=" .env | cut -d '=' -f2 | tr -d '"' | tr -d "'")
    if [ -n "$ENV_LAYOUT_MODE" ]; then
        LAYOUT_MODE="$ENV_LAYOUT_MODE"
        echo -e "${CYAN}Using LAYOUT_MODE=$LAYOUT_MODE from .env${NC}"
    else
        echo -e "${CYAN}LAYOUT_MODE not found in .env, using default: $LAYOUT_MODE${NC}"
    fi
else
    echo -e "${YELLOW}No .env file found, using default configuration${NC}"
fi

# Kill any existing session with the same name
echo -e "${CYAN}Starting tmux session...${NC}"
tmux kill-session -t omega-quad 2>/dev/null

# Create a new tmux session
tmux new-session -d -s omega-quad -n "monitors" "python simple_bitget_positions.py --interval 3; bash"

# Set up the layout based on configuration
case "$LAYOUT_MODE" in
    "vertical")
        echo -e "${CYAN}Using vertical layout (4 stacked panes)${NC}"
        # First split (creates pane 1)
        tmux split-window -v -t omega-quad:monitors.0 "python -m omega_ai.tools.trap_probability_meter --header-style 2 --interval 5; bash"
        # Second split (creates pane 2)
        tmux split-window -v -t omega-quad:monitors.1 "python scripts/persona_entry_strategy.py --continuous --mock --interval 5; bash"
        # Third split (creates pane 3)
        tmux split-window -v -t omega-quad:monitors.2 "python scripts/run_persona_exit_monitor.py --mock --interval 5; bash"
        # Even distribution of space
        tmux select-layout -t omega-quad:monitors even-vertical
        ;;
        
    "horizontal")
        echo -e "${CYAN}Using horizontal layout (4 side-by-side panes)${NC}"
        # First split (creates pane 1)
        tmux split-window -h -t omega-quad:monitors.0 "python -m omega_ai.tools.trap_probability_meter --header-style 2 --interval 5; bash"
        # Second split (creates pane 2)
        tmux split-window -h -t omega-quad:monitors.0 "python scripts/persona_entry_strategy.py --continuous --mock --interval 5; bash"
        # Third split (creates pane 3)
        tmux split-window -h -t omega-quad:monitors.0 "python scripts/run_persona_exit_monitor.py --mock --interval 5; bash"
        # Even distribution of space
        tmux select-layout -t omega-quad:monitors even-horizontal
        ;;
        
    "grid"|*)
        echo -e "${CYAN}Using grid layout (2x2 grid)${NC}"
        # First split (horizontal, creates pane 1)
        tmux split-window -h -t omega-quad:monitors.0 "python -m omega_ai.tools.trap_probability_meter --header-style 2 --interval 5; bash"
        # Second split (vertical split of pane 0, creates pane 2)
        tmux split-window -v -t omega-quad:monitors.0 "python scripts/persona_entry_strategy.py --continuous --mock --interval 5; bash"
        # Third split (vertical split of pane 1, creates pane 3)
        tmux split-window -v -t omega-quad:monitors.1 "python scripts/run_persona_exit_monitor.py --mock --interval 5; bash"
        # Select tile layout (perfect grid)
        tmux select-layout -t omega-quad:monitors tiled
        ;;
esac

# Set tmux styling options
tmux set-option -t omega-quad pane-border-style "fg=magenta"
tmux set-option -t omega-quad pane-active-border-style "fg=cyan,bold"
tmux set-option -t omega-quad status-style "bg=black,fg=green"
tmux set-option -t omega-quad status-right "#[fg=cyan]%H:%M #[fg=yellow]OMEGA BTC AI"
tmux set-option -t omega-quad status-left "#[fg=green,bold]QUAD MONITORS #[fg=blue]| "

# Add navigation message
tmux send-keys -t omega-quad:monitors.0 "echo -e '\n${GREEN}Quad Monitors Active: Ctrl+B ARROW to navigate, Ctrl+B Z to zoom${NC}'" C-m

# Create a control panel in a separate window for quick commands
tmux new-window -t omega-quad:1 -n "control"
tmux send-keys -t omega-quad:control "echo -e '${MAGENTA}OMEGA BTC AI - Control Panel${NC}'" C-m
tmux send-keys -t omega-quad:control "echo -e '${CYAN}Press Ctrl+B 0 to return to monitors${NC}'" C-m
tmux send-keys -t omega-quad:control "echo -e '${CYAN}Press Ctrl+B & to exit session${NC}'" C-m

# Return to the monitors window
tmux select-window -t omega-quad:monitors

# Attach to the session
echo -e "${GREEN}Starting quad monitors. To detach from tmux: press Ctrl+B, then D${NC}"
echo -e "${YELLOW}To exit completely: press Ctrl+B, then &${NC}"
echo -e "${CYAN}To navigate between panes: Ctrl+B, then arrow keys${NC}"
echo -e "${CYAN}To zoom/unzoom a pane: Ctrl+B, then Z${NC}"
sleep 2
tmux attach-session -t omega-quad 