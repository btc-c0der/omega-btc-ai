#!/bin/bash

# OMEGA BTC AI - Dual Focus Monitors Launcher
# This script creates a 2-panel tmux session optimized for smaller vertical displays
# with the ability to toggle between different monitor combinations

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print banner
echo -e "${MAGENTA}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                OMEGA BTC AI - DUAL FOCUS MONITORS               ║" 
echo "║                  Optimized for Vertical Displays                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if tmux is available
if ! command -v tmux &> /dev/null; then
    echo -e "${YELLOW}Error: tmux is not installed. Please install tmux to use this script.${NC}"
    exit 1
fi

# Default focus mode (will be overridden by .env if available)
FOCUS_MODE="position-trap"  # position-trap, entry-exit, position-entry, trap-exit

# Source settings from .env file if it exists
if [ -f ".env" ]; then
    echo -e "${CYAN}Loading configuration from .env file...${NC}"
    # Extract focus mode value from .env file
    ENV_FOCUS_MODE=$(grep "^FOCUS_MODE=" .env | cut -d '=' -f2 | tr -d '"' | tr -d "'")
    if [ -n "$ENV_FOCUS_MODE" ]; then
        FOCUS_MODE="$ENV_FOCUS_MODE"
        echo -e "${CYAN}Using FOCUS_MODE=$FOCUS_MODE from .env${NC}"
    else
        echo -e "${CYAN}FOCUS_MODE not found in .env, using default: $FOCUS_MODE${NC}"
    fi
else
    echo -e "${YELLOW}No .env file found, using default configuration${NC}"
fi

# Kill any existing session with the same name
echo -e "${CYAN}Starting tmux session...${NC}"
tmux kill-session -t omega-dual 2>/dev/null

# Create the control functions for toggling views
create_toggle_functions() {
    # Create a helper function to switch between view modes
    cat > /tmp/omega_toggle_functions.sh << 'EOF'
#!/bin/bash

switch_to_position_trap() {
    tmux kill-window -t omega-dual:monitors
    tmux new-window -d -t omega-dual -n "monitors" "python simple_bitget_positions.py --interval 3; bash"
    tmux split-window -v -t omega-dual:monitors.0 "python -m omega_ai.tools.trap_probability_meter --header-style 2 --interval 5; bash"
    tmux resize-pane -t omega-dual:monitors.0 -y 70%
    tmux send-keys -t omega-dual:control "echo -e '\n\033[0;32mSwitched to Position + Trap view\033[0m'" C-m
    tmux select-window -t omega-dual:monitors
}

switch_to_entry_exit() {
    tmux kill-window -t omega-dual:monitors
    tmux new-window -d -t omega-dual -n "monitors" "python scripts/persona_entry_strategy.py --continuous --mock --interval 5; bash"
    tmux split-window -v -t omega-dual:monitors.0 "python scripts/run_persona_exit_monitor.py --mock --interval 5; bash"
    tmux resize-pane -t omega-dual:monitors.0 -y 50%
    tmux send-keys -t omega-dual:control "echo -e '\n\033[0;32mSwitched to Entry + Exit view\033[0m'" C-m
    tmux select-window -t omega-dual:monitors
}

switch_to_position_entry() {
    tmux kill-window -t omega-dual:monitors
    tmux new-window -d -t omega-dual -n "monitors" "python simple_bitget_positions.py --interval 3; bash"
    tmux split-window -v -t omega-dual:monitors.0 "python scripts/persona_entry_strategy.py --continuous --mock --interval 5; bash"
    tmux resize-pane -t omega-dual:monitors.0 -y 70%
    tmux send-keys -t omega-dual:control "echo -e '\n\033[0;32mSwitched to Position + Entry view\033[0m'" C-m
    tmux select-window -t omega-dual:monitors
}

switch_to_trap_exit() {
    tmux kill-window -t omega-dual:monitors
    tmux new-window -d -t omega-dual -n "monitors" "python -m omega_ai.tools.trap_probability_meter --header-style 2 --interval 5; bash"
    tmux split-window -v -t omega-dual:monitors.0 "python scripts/run_persona_exit_monitor.py --mock --interval 5; bash"
    tmux resize-pane -t omega-dual:monitors.0 -y 40%
    tmux send-keys -t omega-dual:control "echo -e '\n\033[0;32mSwitched to Trap + Exit view\033[0m'" C-m
    tmux select-window -t omega-dual:monitors
}
EOF
    chmod +x /tmp/omega_toggle_functions.sh
}

# Create a control window first
tmux new-session -d -s omega-dual -n "control"
tmux send-keys -t omega-dual:control "echo -e '${MAGENTA}OMEGA BTC AI - DUAL FOCUS MONITORS CONTROL PANEL${NC}'" C-m
tmux send-keys -t omega-dual:control "echo -e '${CYAN}Toggle between different monitoring views:${NC}'" C-m
tmux send-keys -t omega-dual:control "echo -e '${YELLOW}1${NC} - Position + Trap Monitor'" C-m
tmux send-keys -t omega-dual:control "echo -e '${YELLOW}2${NC} - Entry + Exit Personas'" C-m
tmux send-keys -t omega-dual:control "echo -e '${YELLOW}3${NC} - Position + Entry Persona'" C-m
tmux send-keys -t omega-dual:control "echo -e '${YELLOW}4${NC} - Trap + Exit Persona'" C-m
tmux send-keys -t omega-dual:control "echo -e '${RED}q${NC} - Exit Session'" C-m
tmux send-keys -t omega-dual:control "echo" C-m
tmux send-keys -t omega-dual:control "echo -e '${CYAN}Navigation:${NC}'" C-m
tmux send-keys -t omega-dual:control "echo -e '${CYAN}• Ctrl+b 0 - Return to monitors${NC}'" C-m
tmux send-keys -t omega-dual:control "echo -e '${CYAN}• Ctrl+b d - Detach (session keeps running)${NC}'" C-m
tmux send-keys -t omega-dual:control "echo -e '${CYAN}• Ctrl+b z - Zoom/unzoom current pane${NC}'" C-m
tmux send-keys -t omega-dual:control "echo -e '${CYAN}• Ctrl+b arrow - Navigate between panes${NC}'" C-m

# Create the toggle functions
create_toggle_functions

# Create function bindings in the control window
tmux send-keys -t omega-dual:control "source /tmp/omega_toggle_functions.sh" C-m
tmux send-keys -t omega-dual:control "bind -x '\"1\":switch_to_position_trap'" C-m
tmux send-keys -t omega-dual:control "bind -x '\"2\":switch_to_entry_exit'" C-m
tmux send-keys -t omega-dual:control "bind -x '\"3\":switch_to_position_entry'" C-m
tmux send-keys -t omega-dual:control "bind -x '\"4\":switch_to_trap_exit'" C-m
tmux send-keys -t omega-dual:control "bind -x '\"q\":tmux kill-session -t omega-dual'" C-m

# Create the monitors window with the initial layout based on FOCUS_MODE
case "$FOCUS_MODE" in
    "position-trap")
        tmux new-window -d -t omega-dual -n "monitors" "python simple_bitget_positions.py --interval 3; bash"
        tmux split-window -v -t omega-dual:monitors.0 "python -m omega_ai.tools.trap_probability_meter --header-style 2 --interval 5; bash"
        tmux resize-pane -t omega-dual:monitors.0 -y 70%
        ;;
        
    "entry-exit")
        tmux new-window -d -t omega-dual -n "monitors" "python scripts/persona_entry_strategy.py --continuous --mock --interval 5; bash"
        tmux split-window -v -t omega-dual:monitors.0 "python scripts/run_persona_exit_monitor.py --mock --interval 5; bash"
        tmux resize-pane -t omega-dual:monitors.0 -y 50%
        ;;
        
    "position-entry")
        tmux new-window -d -t omega-dual -n "monitors" "python simple_bitget_positions.py --interval 3; bash"
        tmux split-window -v -t omega-dual:monitors.0 "python scripts/persona_entry_strategy.py --continuous --mock --interval 5; bash"
        tmux resize-pane -t omega-dual:monitors.0 -y 70%
        ;;
        
    "trap-exit")
        tmux new-window -d -t omega-dual -n "monitors" "python -m omega_ai.tools.trap_probability_meter --header-style 2 --interval 5; bash"
        tmux split-window -v -t omega-dual:monitors.0 "python scripts/run_persona_exit_monitor.py --mock --interval 5; bash"
        tmux resize-pane -t omega-dual:monitors.0 -y 40%
        ;;
        
    *)
        # Default to position-trap
        tmux new-window -d -t omega-dual -n "monitors" "python simple_bitget_positions.py --interval 3; bash"
        tmux split-window -v -t omega-dual:monitors.0 "python -m omega_ai.tools.trap_probability_meter --header-style 2 --interval 5; bash"
        tmux resize-pane -t omega-dual:monitors.0 -y 70%
        ;;
esac

# Set tmux styling options
tmux set-option -t omega-dual pane-border-style "fg=magenta"
tmux set-option -t omega-dual pane-active-border-style "fg=cyan,bold"
tmux set-option -t omega-dual status-style "bg=black,fg=green"
tmux set-option -t omega-dual status-right "#[fg=cyan]%H:%M #[fg=yellow]OMEGA BTC AI"
tmux set-option -t omega-dual status-left "#[fg=green,bold]DUAL FOCUS #[fg=blue]| "

# Select the monitors window
tmux select-window -t omega-dual:monitors

# Attach to the session
echo -e "${GREEN}Starting dual focus monitors with $FOCUS_MODE view${NC}"
echo -e "${YELLOW}Switch views using the control panel (Ctrl+b 1)${NC}"
echo -e "${CYAN}Navigate between panes: Ctrl+b, then arrow keys${NC}"
echo -e "${CYAN}Zoom/unzoom a pane: Ctrl+b, then z${NC}"
sleep 2
tmux attach-session -t omega-dual 