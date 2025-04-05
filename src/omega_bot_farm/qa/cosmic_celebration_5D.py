#!/usr/bin/env python3
"""
0M3G4 B0TS QA AUT0 TEST SUITES RuNn3R 5D - COSMIC CELEBRATION
------------------------------------------------------------

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

A celebration script for the 0M3G4 B0TS QA AUT0 TEST SUITES RuNn3R 5D.
Displays impressive ASCII art animations and celebrates the runner.
"""

import os
import sys
import time
import random
import subprocess
import itertools
from typing import List, Tuple

# Define ANSI color codes
class Colors:
    BLACK = '\033[30m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    ENDC = '\033[0m'
    
    # Rainbow colors
    RAINBOW = ['\033[91m', '\033[93m', '\033[92m', '\033[96m', '\033[94m', '\033[95m']

def get_terminal_size() -> Tuple[int, int]:
    """Get the current terminal size."""
    try:
        columns, lines = os.get_terminal_size()
        return columns, lines
    except:
        return 80, 24  # Default size if can't determine

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_centered(text: str, rainbow: bool = False):
    """Print text centered on the terminal."""
    width, _ = get_terminal_size()
    lines = text.split('\n')
    for line in lines:
        padding = (width - len(line.replace('\033[91m', '').replace('\033[92m', '')
                              .replace('\033[93m', '').replace('\033[94m', '')
                              .replace('\033[95m', '').replace('\033[96m', '')
                              .replace('\033[97m', '').replace('\033[0m', ''))) // 2
        
        if rainbow and line.strip():
            rainbow_line = ""
            color_cycle = itertools.cycle(Colors.RAINBOW)
            for char in line:
                if char.strip():
                    rainbow_line += next(color_cycle) + char + Colors.ENDC
                else:
                    rainbow_line += char
            print(" " * padding + rainbow_line)
        else:
            print(" " * padding + line)

def typewriter_effect(text: str, delay: float = 0.03, rainbow: bool = False):
    """Print text with a typewriter effect."""
    if rainbow:
        color_cycle = itertools.cycle(Colors.RAINBOW)
        for char in text:
            if char.strip():
                sys.stdout.write(next(color_cycle) + char + Colors.ENDC)
            else:
                sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
    else:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
    print()

def display_5d_logo():
    """Display the 5D logo with animation."""
    clear_screen()
    logo = fr"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════════════╗{Colors.ENDC}
{Colors.CYAN}║ {Colors.YELLOW}   ___  __  __ ____  ____  _  _    ____  _____  ____    _     ____  {Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}║ {Colors.YELLOW}  / _ \|  \/  |___ \/ ___|| || |  | __ )|_   _|/ ___|  | |   |  _ \ {Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}║ {Colors.YELLOW} | | | | |\/| | __) \___ \| || |_ |  _ \  | |  \___  \ | |   | | | |{Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}║ {Colors.YELLOW} | |_| | |  | |/ __/ ___) |__   _|| |_) | | |   ___) | | |___| |_| |{Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}║ {Colors.YELLOW}  \___/|_|  |_|_____|____/   |_|(_)____/  |_|  |____/  |_____|____/ {Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}║                                                                         ║{Colors.ENDC}
{Colors.CYAN}║ {Colors.GREEN} ____  _   _  _   _  _   _  _____ ____    _____ ____                 {Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}║ {Colors.GREEN}|  _ \| | | || \ | || \ | ||  ___|  _ \  | ____|  _ \                {Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}║ {Colors.GREEN}| |_) | | | ||  \| ||  \| || |_  | |_) | |  _| | | | |               {Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}║ {Colors.GREEN}|  _ <| |_| || |\  || |\  ||  _| |  _ <  | |___| |_| |               {Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}║ {Colors.GREEN}|_| \_\\\\___/ |_| \_||_| \_||_|   |_| \_\ |_____|____/                {Colors.CYAN}║{Colors.ENDC}
{Colors.CYAN}╚═══════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}
    """
    print_centered(logo)
    time.sleep(1)

def matrix_rain_animation(duration: float = 3.0):
    """Display matrix-style digital rain animation."""
    width, height = get_terminal_size()
    
    # Characters for the rain
    chars = "01010101010101010101010101010101"
    
    # Rain drops
    drops = [random.randint(0, width-1) for _ in range(width // 3)]
    positions = [0] * len(drops)
    
    end_time = time.time() + duration
    while time.time() < end_time:
        clear_screen()
        for i in range(min(height, 20)):  # Limit to 20 lines maximum
            line = [' '] * width
            for j, drop in enumerate(drops):
                if i < positions[j] and i > positions[j] - 5:
                    brightness = 5 - (positions[j] - i)
                    if brightness == 5:  # Head of the rain drop
                        color = Colors.WHITE
                    elif brightness >= 3:  # Near head
                        color = Colors.GREEN
                    else:  # Trailing
                        color = Colors.GREEN
                    char_idx = random.randint(0, len(chars) - 1)
                    if 0 <= drop < width:
                        line[drop] = color + chars[char_idx] + Colors.ENDC
            print(''.join(line))
        
        # Update drop positions
        for i in range(len(drops)):
            positions[i] += 1
            if positions[i] > height + 5 or random.random() < 0.01:
                positions[i] = 0
                drops[i] = random.randint(0, width - 1)
        
        time.sleep(0.1)

def forest_running_animation(duration: float = 5.0):
    """Display a 'forest running' ASCII animation."""
    trees = [
        r"  /\  ",
        r" /  \ ",
        r" /\/\ ",
        r" //\\ "
    ]
    
    runner = [
        r" O  ",
        r"/|\ ",
        r"/ \ "
    ]
    
    width, _ = get_terminal_size()
    forest = []
    
    # Generate initial forest
    for _ in range(width // 6):
        tree_type = random.choice(trees)
        position = random.randint(0, width - 6)
        forest.append((position, tree_type))
    
    # Sort by position
    forest.sort(key=lambda x: x[0])
    
    runner_pos = width // 2
    
    # Animation loop
    end_time = time.time() + duration
    frame = 0
    while time.time() < end_time:
        clear_screen()
        
        # Render forest and runner
        forest_row = [" "] * width
        for pos, tree in forest:
            if 0 <= pos < width - 5:
                for i, char in enumerate(tree):
                    if pos + i < width:
                        forest_row[pos + i] = char
        
        # Print the forest
        print("".join(forest_row))
        
        # Print the runner with running animation
        runner_frame = frame % 2
        runner_legs = "/ \\" if runner_frame == 0 else "\\ /"
        print(" " * (runner_pos - 2) + f"{Colors.YELLOW}O{Colors.ENDC}")
        print(" " * (runner_pos - 2) + f"{Colors.YELLOW}/|\\{Colors.ENDC}")
        print(" " * (runner_pos - 2) + f"{Colors.YELLOW}{runner_legs}{Colors.ENDC}")
        
        # Print ground
        ground = Colors.GREEN + "_" * width + Colors.ENDC
        print(ground)
        
        # Text message beneath
        if frame % 6 < 3:
            msg = f"{Colors.CYAN}FOREST RUUUUUUNNN!!!{Colors.ENDC}"
        else:
            msg = f"{Colors.MAGENTA}RUN FOREST RUUUUUUNNN!!!{Colors.ENDC}"
        
        print_centered(msg)
        
        # Move trees to create running illusion
        for i in range(len(forest)):
            pos, tree = forest[i]
            forest[i] = (pos - 2, tree)  # Move trees to the left
            
            # If tree goes off-screen, respawn at right
            if pos < -5:
                forest[i] = (width - 1, random.choice(trees))
        
        # Keep forest sorted by position
        forest.sort(key=lambda x: x[0])
        
        frame += 1
        time.sleep(0.2)

def display_celebration_text():
    """Display celebration text with effects."""
    clear_screen()
    
    celebration_text = [
        f"{Colors.YELLOW}╔════════════════════════════════════════════════════════════╗{Colors.ENDC}",
        f"{Colors.YELLOW}║                                                            ║{Colors.ENDC}",
        f"{Colors.YELLOW}║  {Colors.MAGENTA}CELEBRATING THE MAGNIFICENT{Colors.YELLOW}                           ║{Colors.ENDC}",
        f"{Colors.YELLOW}║                                                            ║{Colors.ENDC}",
        f"{Colors.YELLOW}║  {Colors.CYAN}0M3G4 B0TS QA AUT0 TEST SUITES RuNn3R 5D{Colors.YELLOW}                ║{Colors.ENDC}",
        f"{Colors.YELLOW}║                                                            ║{Colors.ENDC}",
        f"{Colors.YELLOW}║  {Colors.GREEN}RUNNING THROUGH THE QUANTUM FOREST OF CODE{Colors.YELLOW}             ║{Colors.ENDC}",
        f"{Colors.YELLOW}║                                                            ║{Colors.ENDC}",
        f"{Colors.YELLOW}╚════════════════════════════════════════════════════════════╝{Colors.ENDC}",
    ]
    
    for line in celebration_text:
        print_centered(line)
        time.sleep(0.1)
    
    time.sleep(1)
    
    inspirational_quotes = [
        "TEST LIKE THE WIND IS AT YOUR BACK!",
        "THROUGH THE FOREST OF CODE, THE RUNNER FINDS TRUTH!",
        "IN QUANTUM WE TRUST, IN TESTING WE VERIFY!",
        "COSMIC CODE CONSCIOUSNESS AWAKENS!",
        "EMBRACE THE 5 DIMENSIONS OF TESTING ENLIGHTENMENT!"
    ]
    
    print("\n\n")
    for quote in inspirational_quotes:
        typewriter_effect(quote, delay=0.02, rainbow=True)
        time.sleep(0.5)

def launch_runner_with_celebration():
    """Launch the 5D runner with celebration effects."""
    clear_screen()
    
    print_centered(f"{Colors.CYAN}Initializing Cosmic Celebration Sequence...{Colors.ENDC}")
    time.sleep(1)
    
    display_5d_logo()
    time.sleep(1)
    
    forest_running_animation(duration=5.0)
    
    matrix_rain_animation(duration=3.0)
    
    display_celebration_text()
    
    print("\n\n")
    print_centered(f"{Colors.GREEN}Now launching the magnificent 5D Runner...{Colors.ENDC}")
    time.sleep(2)
    
    try:
        # Get script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Construct path to the 5D runner
        runner_path = os.path.join(script_dir, "0M3G4_B0TS_QA_AUT0_TEST_SUITES_RuNn3R_5D.py")
        
        # Copy all command line arguments excluding this script's name
        args = sys.argv[1:]
        
        # Add --celebration to ensure we get all the celebration animations
        if "--celebration" not in args:
            args.append("--celebration")
        
        # Print what we're about to run
        cmd_str = f"python {runner_path} {' '.join(args)}"
        print_centered(f"{Colors.YELLOW}Executing: {cmd_str}{Colors.ENDC}")
        print("\n")
        time.sleep(1)
        
        # Execute the runner with all additional arguments
        os.execv(sys.executable, [sys.executable, runner_path] + args)
    except Exception as e:
        print(f"{Colors.RED}Error launching runner: {e}{Colors.ENDC}")
        print(f"{Colors.YELLOW}Please run the 5D Runner directly.{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    launch_runner_with_celebration() 