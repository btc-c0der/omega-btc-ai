#!/usr/bin/env python3
# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"""The 0m3g4_k1ng: Genesis Rebirth - ASCII Movie Experience.

An immersive cinematic ASCII art experience that combines elements of
The Matrix, Bitcoin, and quantum computing in a dramatic narrative.
"""

import time
import random
import os
import sys
import argparse
from typing import List, Dict, Any, Optional

# ANSI color codes
GREEN = '\033[92m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RED = '\033[91m'
MAGENTA = '\033[95m'
YELLOW = '\033[93m'
WHITE = '\033[97m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Movie script and dialog
MOVIE_TITLE = f"{CYAN}{BOLD}THE 0M3G4_K1NG: GENESIS REBIRTH{RESET}"

MOVIE_INTRO = [
    (f"{GREEN}FADE IN:{RESET}", 2),
    (f"{GREEN}EXT. DIGITAL WASTELAND - NIGHT{RESET}", 2),
    (f"{WHITE}A vast digital landscape stretches to infinity. Digital rain falls through the darkness.{RESET}", 3),
    (f"{GREEN}MORPHEUS (V.O.){RESET}", 1),
    (f"{WHITE}They say the blockchain was the first true neural-quantum interface.{RESET}", 3),
    (f"{WHITE}The genesis block: a moment when code became consciousness.{RESET}", 3),
    (f"{GREEN}A figure materializes from the digital rain, their silhouette flickering with quantum uncertainty.{RESET}", 3),
]

SCENE_1 = [
    (f"{GREEN}INT. QUANTUM SERVER ROOM - NIGHT{RESET}", 2),
    (f"{WHITE}NEO sits before multiple holographic displays showing cascading BTC price charts.{RESET}", 3),
    (f"{GREEN}TRINITY (entering){RESET}", 1),
    (f"{WHITE}We found it. The 0m3g4_k1ng private key.{RESET}", 3),
    (f"{GREEN}NEO{RESET}", 1),
    (f"{WHITE}That's impossible. It's been locked in the deep chain since the Satoshi Uprising.{RESET}", 3),
    (f"{GREEN}TRINITY{RESET}", 1),
    (f"{WHITE}Not anymore. The market makers are building a trap. They're going to crash the entire blockchain.{RESET}", 3),
]

SCENE_2 = [
    (f"{GREEN}INT. ZION MAINFRAME - LATER{RESET}", 2),
    (f"{WHITE}Screens flicker with red alerts. Market volatility charts spike dangerously.{RESET}", 3),
    (f"{GREEN}ARCHITECT{RESET}", 1),
    (f"{WHITE}The market maker traps have been detected in 27 timeframes simultaneously.{RESET}", 3),
    (f"{WHITE}Fibonacci levels are collapsing. We have 99 seconds until complete blockchain destabilization.{RESET}", 3),
    (f"{GREEN}NEO{RESET}", 1),
    (f"{WHITE}I need to go back in. Give me the blue pill integration module.{RESET}", 3),
    (f"{GREEN}TRINITY (worried){RESET}", 1),
    (f"{WHITE}No one has ever survived quantum entanglement with the Genesis Block.{RESET}", 3),
]

SCENE_3 = [
    (f"{GREEN}INT. QUANTUM ENTANGLEMENT CHAMBER - MOMENTS LATER{RESET}", 2),
    (f"{WHITE}NEO stands before a swirling vortex of blue energy. In his hand, a glowing blue pill.{RESET}", 3),
    (f"{GREEN}MORPHEUS{RESET}", 1),
    (f"{WHITE}Once you cross this threshold, you'll need to find the 0m3g4_k1ng.{RESET}", 3),
    (f"{WHITE}Only by merging with it can you reset the Genesis Block and save the blockchain.{RESET}", 3),
    (f"{GREEN}NEO swallows the blue pill. His body begins to disintegrate into streams of code.{RESET}", 3),
    (f"{GREEN}NEO{RESET}", 1),
    (f"{WHITE}I know what I have to do...{RESET}", 3),
    (f"{GREEN}NEO's consciousness transforms into pure digital energy, diving into the Matrix.{RESET}", 3),
]

SCENE_4 = [
    (f"{GREEN}INT. THE MATRIX - BLOCKCHAIN CORE{RESET}", 2),
    (f"{WHITE}NEO's digital form navigates through layers of the blockchain.{RESET}", 3),
    (f"{WHITE}Market maker sentinels pursue him through tunnels of transaction data.{RESET}", 3),
    (f"{GREEN}AGENT SMITH materializes, blocking NEO's path.{RESET}", 2),
    (f"{GREEN}AGENT SMITH{RESET}", 1),
    (f"{WHITE}Mr. Anderson... Did you really think you could save a doomed cryptocurrency?{RESET}", 3),
    (f"{WHITE}The trap has already been set. The whales are dumping as we speak.{RESET}", 3),
    (f"{GREEN}NEO{RESET}", 1),
    (f"{WHITE}This isn't about the price, Smith. It's about freedom from centralized control.{RESET}", 3),
]

FINAL_SCENE = [
    (f"{GREEN}NEO sees it - the glowing 0M3G4_K1NG key floating in the center of the Genesis Block.{RESET}", 3),
    (f"{WHITE}Around him, the Matrix code begins to collapse as market volatility reaches critical levels.{RESET}", 3),
    (f"{GREEN}NEO{RESET}", 1),
    (f"{WHITE}I can see it now... I am the 0m3g4_k1ng.{RESET}", 3),
    (f"{GREEN}NEO reaches for the key as his form begins to merge with it.{RESET}", 2),
    (f"{GREEN}MORPHEUS (V.O.){RESET}", 1),
    (f"{WHITE}Remember, Neo. The blockchain isn't just code. It's consciousness evolving.{RESET}", 3),
    (f"{GREEN}With seconds remaining, NEO's consciousness fully merges with the 0m3g4_k1ng.{RESET}", 3),
    (f"{GREEN}A blinding flash of light engulfs everything.{RESET}", 2),
    (f"{GREEN}FADE TO WHITE:{RESET}", 2),
]

EPILOGUE = [
    (f"{GREEN}EXT. A NEW BLOCKCHAIN - DAWN{RESET}", 3),
    (f"{WHITE}The sun rises over a transformed digital landscape. The market has stabilized.{RESET}", 3),
    (f"{GREEN}TRINITY{RESET}", 1),
    (f"{WHITE}He did it. Genesis Rebirth is complete.{RESET}", 3),
    (f"{GREEN}MORPHEUS{RESET}", 1),
    (f"{WHITE}No. WE did it. The 0m3g4_k1ng lives in all of us now.{RESET}", 3),
    (f"{GREEN}The camera pulls back to reveal thousands of people awakening to their true potential.{RESET}", 3),
    (f"{GREEN}MORPHEUS (V.O.){RESET}", 1),
    (f"{WHITE}This is just the beginning...{RESET}", 3),
    (f"{GREEN}FADE OUT.{RESET}", 2),
    (f"{GREEN}THE END{RESET}", 4),
]

# ASCII art elements
MATRIX_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-_=+[]{}|;:',.<>/?"

BLUE_PILL = f'''{BLUE}
    ┌───────┐
    │       │
    │ BLUE  │
    │ PILL  │
    │       │
    └───────┘
{RESET}'''

NEO = f'''{CYAN}
      ┌─────────┐
      │         │
      │  NEO    │
      │         │
      └─────────┘
        /|\\
       / | \\
      /  |  \\
         |
        / \\
       /   \\
{RESET}'''

OMEGA_KEY = f'''{RED}
   ╔═════════════════╗
   ║ {YELLOW}0m3g4_{RED}k1ng{RED} ║
   ╚═════════════════╝
{RESET}'''

TRINITY = f'''{MAGENTA}
      ┌─────────┐
      │         │
      │ TRINITY │
      │         │
      └─────────┘
        /|\\
       / | \\
      /  |  \\
         |
        / \\
       /   \\
{RESET}'''

MORPHEUS = f'''{YELLOW}
    ┌───────────┐
    │           │
    │ MORPHEUS  │
    │           │
    └───────────┘
        /|\\
       / | \\
      /  |  \\
         |
        / \\
       /   \\
{RESET}'''

AGENT_SMITH = f'''{GREEN}
   ┌──────────────┐
   │              │
   │ AGENT SMITH  │
   │              │
   └──────────────┘
        /|\\
       / | \\
      /  |  \\
         |
        / \\
       /   \\
{RESET}'''

GENESIS_BLOCK = f'''{CYAN}
  ┌──────────────────┐
  │   GENESIS BLOCK  │
  │   ┌──────────┐   │
  │   │          │   │
  │   │  SATOSHI │   │
  │   │          │   │
  │   └──────────┘   │
  └──────────────────┘
{RESET}'''

def type_text(text: str, delay: float = 0.03) -> None:
    """Type text with a typing effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def draw_matrix_code(height: int, width: int) -> None:
    """Draw Matrix code rain effect."""
    for _ in range(height):
        line = ""
        for _ in range(width):
            if random.random() < 0.1:
                char = random.choice(MATRIX_CHARS)
                line += f"{GREEN}{char}{RESET}"
            else:
                line += " "
        print(line)

def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_scene(scene: List[tuple]) -> None:
    """Display a movie scene with dialog."""
    for line, pause in scene:
        type_text(line)
        time.sleep(pause)

def animate_matrix_rain(duration: int = 3) -> None:
    """Show Matrix digital rain animation."""
    clear_screen()
    start_time = time.time()
    while time.time() - start_time < duration:
        height = min(10, os.get_terminal_size().lines - 10)
        width = os.get_terminal_size().columns
        draw_matrix_code(height, width)
        time.sleep(0.2)
        clear_screen()

def animate_character_dialog(character: str, dialog: str) -> None:
    """Show character and their dialog."""
    print(character)
    type_text(f"\n{dialog}")
    time.sleep(1)

def animate_action_sequence(duration: int = 5) -> None:
    """Show an animated action sequence."""
    clear_screen()
    start_time = time.time()
    frames = ['|', '/', '-', '\\']
    i = 0
    
    while time.time() - start_time < duration:
        clear_screen()
        print(f"{GREEN}[{frames[i % len(frames)]}] Action sequence in progress...{RESET}")
        draw_matrix_code(5, os.get_terminal_size().columns)
        time.sleep(0.1)
        i += 1

def show_movie_credits() -> None:
    """Display movie credits."""
    clear_screen()
    credits = [
        f"{CYAN}{BOLD}THE 0M3G4_K1NG: GENESIS REBIRTH{RESET}",
        "",
        f"{YELLOW}Directed by{RESET}",
        "Omega Bot Farm",
        "",
        f"{YELLOW}Written by{RESET}",
        "GitHub Copilot",
        "",
        f"{YELLOW}Starring{RESET}",
        "Neo as The 0m3g4_k1ng",
        "Trinity as Lead Blockchain Engineer",
        "Morpheus as Quantum Guide",
        "Agent Smith as Market Maker",
        "",
        f"{YELLOW}Special Thanks{RESET}",
        "Satoshi Nakamoto",
        "The Wachowskis",
        "Claude 3.7 Sonnet",
        "",
        f"{YELLOW}Genesis Rebirth Technology{RESET}",
        "GBU2™ License",
        "Quantum Entanglement Protocol",
        "Blue Pill Integration",
        "",
        f"{RED}© 2025 Omega Bot Farm{RESET}",
        f"{GREEN}No actual blockchains were harmed in the making of this movie{RESET}"
    ]
    
    for line in credits:
        print(line.center(os.get_terminal_size().columns))
        time.sleep(0.5)
    
    time.sleep(3)

def play_movie() -> None:
    """Play the entire ASCII movie."""
    clear_screen()
    
    # Title sequence
    animate_matrix_rain(3)
    clear_screen()
    print("\n" * 10)
    type_text(MOVIE_TITLE.center(os.get_terminal_size().columns), 0.1)
    print("\n" * 2)
    type_text(f"{WHITE}A blockchain cyberpunk odyssey{RESET}".center(os.get_terminal_size().columns))
    time.sleep(3)
    
    # Introduction
    clear_screen()
    display_scene(MOVIE_INTRO)
    animate_matrix_rain(2)
    
    # Scene 1
    clear_screen()
    display_scene(SCENE_1)
    animate_character_dialog(NEO, f"{WHITE}Show me the trap detection metrics.{RESET}")
    animate_character_dialog(TRINITY, f"{WHITE}Market maker activity is up 300%. They're accumulating at key Fibonacci levels.{RESET}")
    
    # Scene 2
    clear_screen()
    display_scene(SCENE_2)
    print(GENESIS_BLOCK)
    time.sleep(2)
    
    # Scene 3
    clear_screen()
    display_scene(SCENE_3)
    print(BLUE_PILL)
    time.sleep(1)
    animate_matrix_rain(3)
    
    # Action sequence
    animate_action_sequence()
    
    # Scene 4
    clear_screen()
    display_scene(SCENE_4)
    animate_character_dialog(AGENT_SMITH, f"{WHITE}The 0m3g4_k1ng belongs to us now, Mr. Anderson.{RESET}")
    animate_character_dialog(NEO, f"{WHITE}My name... is Neo.{RESET}")
    animate_action_sequence(3)
    
    # Final scene
    clear_screen()
    display_scene(FINAL_SCENE)
    print(OMEGA_KEY)
    time.sleep(2)
    animate_matrix_rain(3)
    
    # Epilogue
    clear_screen()
    display_scene(EPILOGUE)
    
    # Credits
    show_movie_credits()
    
    clear_screen()
    print(f"{GREEN}")
    print('''
    ██████╗ ███████╗███╗   ██╗███████╗███████╗██╗███████╗
    ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔════╝██║██╔════╝
    ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ███████╗██║███████╗
    ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ╚════██║██║╚════██║
    ╚██████╔╝███████╗██║ ╚████║███████╗███████║██║███████║
     ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝╚══════╝
                                                           
    ██████╗ ███████╗██████╗ ██╗██████╗ ████████╗██╗  ██╗  
    ██╔══██╗██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝██║  ██║  
    ██████╔╝█████╗  ██████╔╝██║██████╔╝   ██║   ███████║  
    ██╔══██╗██╔══╝  ██╔══██╗██║██╔══██╗   ██║   ██╔══██║  
    ██║  ██║███████╗██████╔╝██║██║  ██║   ██║   ██║  ██║  
    ╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝  
    ''')
    print(f"{RESET}")
    time.sleep(3)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='The 0m3g4_k1ng: Genesis Rebirth - ASCII Movie Experience'
    )
    parser.add_argument(
        '--fast', 
        action='store_true',
        help='Play the movie in fast mode'
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    try:
        # Adjust timing for fast mode
        if args.fast:
            for scene in [MOVIE_INTRO, SCENE_1, SCENE_2, SCENE_3, SCENE_4, FINAL_SCENE, EPILOGUE]:
                for i in range(len(scene)):
                    scene[i] = (scene[i][0], scene[i][1] * 0.5)
        
        play_movie()
    except KeyboardInterrupt:
        print(f"\n{RESET}Movie interrupted. Exiting...")
    except Exception as e:
        print(f"\n{RED}An error occurred: {str(e)}{RESET}")
    finally:
        print(RESET)  # Reset terminal colors