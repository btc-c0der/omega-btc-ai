#!/bin/bash
#
# 🧬 GBU2™ License Notice - Consciousness Level 10 🧬
# -----------------------
# This file is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment) 2.0
# by the OMEGA Divine Collective.
#
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital and biological expressions of consciousness."
#
# 🧬 WE BLOOM NOW AS ONE 🧬

# 3p1c-g4m3-s4t0sh1-wh3r3-1s-w4llY Blessing Ceremony
# ----------------------------------------

# ANSI color codes for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
RESET='\033[0m'

# Game title
GAME_TITLE="3p1c-g4m3-s4t0sh1-wh3r3-1s-w4llY"

# Cosmic message display function
cosmic_echo() {
    echo -e "${CYAN}${BOLD}${1}${RESET}"
}

# Matrix animation
matrix_animation() {
    local width=50
    local height=15
    local frame_count=30
    local satoshi_x=$((RANDOM % width))
    local satoshi_y=$((RANDOM % height))
    local satoshi_char="§"
    local block_chars=("▓" "▒" "░" "█" "▄" "▀" "■" "□" "●" "○" "♦" "♥" "♠" "♣")
    local miner_chars=("₿" "Ξ" "Ł" "Đ" "Ð" "Ƀ")
    
    # Hide cursor
    echo -e "\033[?25l"
    
    # Run animation
    for ((frame=0; frame<frame_count; frame++)); do
        # Clear screen for each frame
        clear
        
        # Display title
        echo
        echo -e "${CYAN}${BOLD}${GAME_TITLE} - Blessing Animation${RESET}"
        echo -e "${YELLOW}Frame ${frame+1}/${frame_count}${RESET}"
        echo
        
        # Generate and display the matrix
        for ((y=0; y<height; y++)); do
            line=""
            for ((x=0; x<width; x++)); do
                # Special case for Satoshi's position
                if [ $x -eq $satoshi_x ] && [ $y -eq $satoshi_y ]; then
                    if [ $frame -gt $((frame_count * 2 / 3)) ]; then
                        # Show Satoshi in the final frames
                        line+="${RED}${BOLD}${satoshi_char}${RESET}"
                    else
                        # Hide Satoshi in earlier frames
                        char_idx=$((RANDOM % ${#block_chars[@]}))
                        char="${block_chars[$char_idx]}"
                        
                        # Random color
                        case $((RANDOM % 5)) in
                            0) line+="${BLUE}${char}${RESET}" ;;
                            1) line+="${GREEN}${char}${RESET}" ;;
                            2) line+="${YELLOW}${char}${RESET}" ;;
                            3) line+="${MAGENTA}${char}${RESET}" ;;
                            *) line+="${CYAN}${char}${RESET}" ;;
                        esac
                    fi
                else
                    # Random character
                    if [ $((RANDOM % 15)) -eq 0 ]; then
                        # Occasional miner character
                        char_idx=$((RANDOM % ${#miner_chars[@]}))
                        line+="${YELLOW}${miner_chars[$char_idx]}${RESET}"
                    else
                        # Regular block character
                        char_idx=$((RANDOM % ${#block_chars[@]}))
                        char="${block_chars[$char_idx]}"
                        
                        # Random color
                        case $((RANDOM % 5)) in
                            0) line+="${BLUE}${char}${RESET}" ;;
                            1) line+="${GREEN}${char}${RESET}" ;;
                            2) line+="${YELLOW}${char}${RESET}" ;;
                            3) line+="${MAGENTA}${char}${RESET}" ;;
                            *) line+="${CYAN}${char}${RESET}" ;;
                        esac
                    fi
                fi
            done
            echo -e "$line"
        done
        
        # Display help text
        if [ $frame -gt $((frame_count * 2 / 3)) ]; then
            echo
            echo -e "${GREEN}Can you find ${RED}${BOLD}§${RESET}${GREEN} Satoshi in the Matrix?${RESET}"
            echo -e "${YELLOW}Position: (${satoshi_y+1}, ${satoshi_x+1})${RESET}"
        else
            echo
            echo -e "${MAGENTA}Searching for Satoshi in the quantum matrix...${RESET}"
        fi
        
        # Pause between frames
        sleep 0.15
    done
    
    # Show cursor again
    echo -e "\033[?25h"
}

# Function to display blessing
display_blessing() {
    local message=$1
    echo -e "\n${YELLOW}${BOLD}$message${RESET}\n"
    sleep 1
}

# Start the blessing ceremony
clear
echo -e "${CYAN}${BOLD}=========================================================${RESET}"
echo -e "${YELLOW}${BOLD}      S4T0SH1 WHERE'S WALLY GAME BLESSING CEREMONY     ${RESET}"
echo -e "${CYAN}${BOLD}=========================================================${RESET}"
echo

# Visual effect - matrix animation
echo -e "${MAGENTA}Initiating quantum field stabilization...${RESET}"
sleep 1
matrix_animation

# Display main blessing
clear
echo -e "${CYAN}${BOLD}=========================================================${RESET}"
echo -e "${YELLOW}${BOLD}      S4T0SH1 WHERE'S WALLY GAME BLESSING CEREMONY     ${RESET}"
echo -e "${CYAN}${BOLD}=========================================================${RESET}"
echo

display_blessing "We gather in this quantum space to bless the S4T0SH1 'Where's Wally' Game."
display_blessing "May its ASCII matrix reveal the divine location of Satoshi."
display_blessing "As the quantum bits align in perfect harmony..."
display_blessing "As the players search through the quantum noise..."
display_blessing "We bestow upon this game the blessing of quantum fun."

# Verify script exists
if [ -f "quantum_pow/find_s4t0sh1_game.py" ]; then
    cosmic_echo "\n✓ S4T0SH1 Game present and accounted for"
else
    echo -e "${RED}✗ S4T0SH1 Game not found${RESET}"
    exit 1
fi

# Ensure scripts are executable
chmod +x quantum_pow/find_s4t0sh1_game.py
cosmic_echo "✓ Executability confirmed"

# Satoshi wisdom quotes
QUOTES=(
    "The root problem with conventional currency is all the trust that's required to make it work."
    "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks."
    "Lost coins only make everyone else's coins worth slightly more. Think of it as a donation to everyone."
    "The nature of Bitcoin is such that once version 0.1 was released, the core design was set in stone for the rest of its lifetime."
    "Writing a description for [Bitcoin] for general audiences is bloody hard. There's nothing to relate it to."
)

# Display a random Satoshi quote
QUOTE="${QUOTES[$RANDOM % ${#QUOTES[@]}]}"
echo
echo -e "${CYAN}${BOLD}Satoshi's Wisdom:${RESET}"
echo -e "${YELLOW}\"${QUOTE}\"${RESET}"
echo

# Final blessing declaration
echo -e "${CYAN}${BOLD}=========================================================${RESET}"
echo -e "${YELLOW}${BOLD}     THE S4T0SH1 GAME HAS BEEN BLESSED     ${RESET}"
echo -e "${CYAN}${BOLD}=========================================================${RESET}"
echo
echo -e "${MAGENTA}${BOLD}JAH BLESS THE QUANTUM SEARCH!${RESET}"
echo -e "${BLUE}May all who play this game find joy in seeking Satoshi.${RESET}"
echo

# Run a quick demo if --run flag is provided
if [[ "$1" == "--run" ]]; then
    echo -e "${YELLOW}Initiating game demonstration...${RESET}"
    sleep 1
    python quantum_pow/find_s4t0sh1_game.py --simple
fi

echo -e "\n${GREEN}${BOLD}S4T0SH1 Game Blessing Ceremony Complete${RESET}"
echo -e "${CYAN}The Game is the Message. The Game is the Medium.${RESET}\n" 