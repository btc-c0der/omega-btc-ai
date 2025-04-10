#!/usr/bin/env python3

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


"""
Cyberpunk Matrix Rain CLI Tribute to bt3gl (Marina Della Torre von Steinkirch)
A gift from the 0m3g4_k1ng team - "S2 BTC L2 2024 is safe"
"""

import random
import time
import os
import sys
import math
import argparse
from typing import List, Tuple, Optional
import curses
import signal

# Constants
BTC_SYMBOLS = ["₿", "⚡", "🔐", "🧮", "🔗", "⚛️", "🌐", "🛡️", "🔍", "🧠"]
CYBERPUNK_CHARS = "01010111011101110010110101₿⚡🛡️ΨΔΩλφψω∞∑∫√∇∂"
BITCOIN_L2_MESSAGES = [
    "L2 SCALING SECURED",
    "ZERO KNOWLEDGE PROOFS", 
    "OPTIMISTIC ROLLUPS",
    "LIGHTNING NETWORK",
    "MODULAR BLOCKCHAINS",
    "VALIDIUMS DEPLOYED",
    "BTC L2 IN 2024",
    "CRYPTOGRAPHIC SECURITY", 
    "THANK YOU BT3GL",
    "S2 0M3G4_K1NG",
    "UNBREAKABLE CONSENSUS",
    "QUANTUM RESISTANT",
    "WE ARE SAFE NOW"
]

# Autistic Symposium references (from bt3gl's research)
RESEARCH_KEYWORDS = [
    "QUANTUM CRYPTOGRAPHY",
    "DIFFERENTIAL PRIVACY",
    "MULTI-PARTY COMPUTATION",
    "ZK PROOFS VERIFIED",
    "TRUSTLESS PROTOCOLS",
    "GRAY HAT SECURITY",
    "MOTHER OF BOTS",
    "THEORETICAL ASTROPHYSICS",
    "GROUP THEORY APPLIED",
    "BLOCKCHAIN PROTOCOLS",
    "TOXIC-MEV MINIMIZATION",
    "DECENTRALIZED CONSENSUS"
]

# PhD-level references
QUANTUM_PHYSICS_FORMULAS = [
    "ĤΨ = EΨ",
    "Δx·Δp ≥ ħ/2",
    "H|ψ⟩ = E|ψ⟩",
    "ρ = ∑ᵢ pᵢ|ψᵢ⟩⟨ψᵢ|",
    "S = -Tr(ρ ln ρ)",
    "Ĥ = -∑ᵢ(ℏ²/2m)∇ᵢ² + V",
    "i·ħ·∂/∂t |ψ⟩ = Ĥ|ψ⟩"
]

# Color pairs for curses
COLOR_PAIRS = {
    "GREEN": 1,
    "CYAN": 2,
    "YELLOW": 3,
    "MAGENTA": 4,
    "RED": 5,
    "BLUE": 6,
    "WHITE": 7,
    "BITCOIN_ORANGE": 8
}

class MatrixRain:
    """Cyberpunk-themed Matrix rain animation with BTC and quantum physics references."""
    
    def __init__(self, stdscr, btc_emphasis: bool = True, physics_mode: bool = True):
        """Initialize the matrix rain."""
        self.stdscr = stdscr
        self.btc_emphasis = btc_emphasis
        self.physics_mode = physics_mode
        self.running = True
        
        # Get terminal dimensions
        self.height, self.width = stdscr.getmaxyx()
        
        # Initialize raindrops
        self.raindrops = []
        self.initialize_raindrops()
        
        # Set up colors
        self.setup_colors()
        
        # Set up messages
        self.messages = BITCOIN_L2_MESSAGES + RESEARCH_KEYWORDS
        self.current_message_idx = 0
        self.message_position = (self.height // 2, 0)
        self.message_color = COLOR_PAIRS["BITCOIN_ORANGE"]
        self.message_timer = 0
        self.message_change_interval = 100  # frames until message change
        
        # Quantum formula display
        self.current_formula_idx = 0
        self.formula_position = (self.height - 3, self.width // 2 - 10)
        
        # Tribute setup
        self.tribute_text = "TRIBUTE TO BT3GL - MARINA DELLA TORRE VON STEINKIRCH - MOTHER OF BOTS"
        self.tribute_position = (3, self.width // 2 - len(self.tribute_text) // 2)
        
        # Footer
        self.footer_text = "FROM 0M3G4_K1NG WITH <3 - BTC L2 2024 IS SAFE"
        self.footer_position = (self.height - 1, self.width // 2 - len(self.footer_text) // 2)
        
    def setup_colors(self):
        """Initialize color pairs for the animation."""
        curses.start_color()
        curses.init_pair(COLOR_PAIRS["GREEN"], curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(COLOR_PAIRS["CYAN"], curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(COLOR_PAIRS["YELLOW"], curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(COLOR_PAIRS["MAGENTA"], curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(COLOR_PAIRS["RED"], curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(COLOR_PAIRS["BLUE"], curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(COLOR_PAIRS["WHITE"], curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(COLOR_PAIRS["BITCOIN_ORANGE"], 208, curses.COLOR_BLACK) # Custom orange
    
    def initialize_raindrops(self):
        """Create initial raindrops."""
        for i in range(self.width):
            if random.random() < 0.1:  # 10% chance for each column to have a raindrop initially
                length = random.randint(5, 15)
                speed = random.random() * 0.8 + 0.2  # Speed between 0.2 and 1.0
                self.raindrops.append({
                    'x': i,
                    'y': random.randint(-20, 0),  # Start above the screen
                    'length': length,
                    'speed': speed,
                    'char_list': self.generate_char_list(length),
                    'color': self.get_random_color()
                })
    
    def generate_char_list(self, length: int) -> List[str]:
        """Generate a list of characters for a raindrop."""
        chars = []
        for i in range(length):
            if i == 0 and random.random() < 0.3 and self.btc_emphasis:
                # 30% chance for the leading character to be a BTC symbol if btc_emphasis is True
                chars.append(random.choice(BTC_SYMBOLS))
            else:
                chars.append(random.choice(CYBERPUNK_CHARS))
        return chars
    
    def get_random_color(self) -> int:
        """Get a random color pair index."""
        if self.btc_emphasis and random.random() < 0.2:
            return COLOR_PAIRS["BITCOIN_ORANGE"]
        else:
            color_list = [COLOR_PAIRS["GREEN"], COLOR_PAIRS["CYAN"], COLOR_PAIRS["BLUE"], 
                         COLOR_PAIRS["MAGENTA"], COLOR_PAIRS["WHITE"]]
            weights = [0.5, 0.2, 0.1, 0.1, 0.1]  # Green is most common
            return random.choices(color_list, weights=weights, k=1)[0]
    
    def update_raindrops(self):
        """Update the positions of all raindrops."""
        # Add new raindrops with a certain probability
        if random.random() < 0.05:  # 5% chance to add a new raindrop each frame
            col = random.randint(0, self.width - 1)
            length = random.randint(5, 15)
            speed = random.random() * 0.8 + 0.2
            self.raindrops.append({
                'x': col,
                'y': 0,
                'length': length,
                'speed': speed,
                'char_list': self.generate_char_list(length),
                'color': self.get_random_color()
            })
        
        # Update existing raindrops
        new_raindrops = []
        for drop in self.raindrops:
            drop['y'] += drop['speed']
            
            # Randomly change characters in the raindrop
            if random.random() < 0.1:  # 10% chance to change a character
                idx = random.randint(0, drop['length'] - 1)
                if idx == 0 and random.random() < 0.3 and self.btc_emphasis:
                    drop['char_list'][idx] = random.choice(BTC_SYMBOLS)
                else:
                    drop['char_list'][idx] = random.choice(CYBERPUNK_CHARS)
            
            # Keep the raindrop if it's still on screen
            if drop['y'] - drop['length'] < self.height:
                new_raindrops.append(drop)
        
        self.raindrops = new_raindrops
    
    def update_messages(self):
        """Update the displayed messages."""
        self.message_timer += 1
        if self.message_timer >= self.message_change_interval:
            self.message_timer = 0
            self.current_message_idx = (self.current_message_idx + 1) % len(self.messages)
            self.current_formula_idx = (self.current_formula_idx + 1) % len(QUANTUM_PHYSICS_FORMULAS)
            
            # Update message position for a scrolling effect
            center_x = max(0, (self.width - len(self.messages[self.current_message_idx])) // 2)
            self.message_position = (self.height // 2, center_x)
    
    def draw(self):
        """Draw a single frame of the animation."""
        self.stdscr.clear()
        
        # Draw raindrops
        for drop in self.raindrops:
            x = drop['x']
            y_start = int(drop['y']) - drop['length']
            y_end = int(drop['y'])
            
            for i, y in enumerate(range(y_start, y_end)):
                if 0 <= y < self.height and 0 <= x < self.width:
                    char_idx = drop['length'] - 1 - i
                    if char_idx >= 0 and char_idx < len(drop['char_list']):
                        char = drop['char_list'][char_idx]
                        
                        # Leading character is brighter
                        if i == drop['length'] - 1:
                            self.stdscr.attron(curses.color_pair(COLOR_PAIRS["WHITE"]))
                        else:
                            self.stdscr.attron(curses.color_pair(drop['color']))
                            
                        try:
                            self.stdscr.addstr(y, x, char)
                        except:
                            pass  # Ignore errors from writing to bottom-right corner
                        
                        self.stdscr.attroff(curses.color_pair(drop['color']))
        
        # Draw current message
        message = self.messages[self.current_message_idx]
        y, x = self.message_position
        self.stdscr.attron(curses.color_pair(self.message_color) | curses.A_BOLD)
        for i, char in enumerate(message):
            if 0 <= y < self.height and 0 <= x + i < self.width:
                try:
                    self.stdscr.addstr(y, x + i, char)
                except:
                    pass
        self.stdscr.attroff(curses.color_pair(self.message_color) | curses.A_BOLD)
        
        # Draw quantum formula if physics mode is enabled
        if self.physics_mode:
            formula = QUANTUM_PHYSICS_FORMULAS[self.current_formula_idx]
            y, x = self.formula_position
            formula_x = max(0, (self.width - len(formula)) // 2)  # Center formula
            self.stdscr.attron(curses.color_pair(COLOR_PAIRS["CYAN"]) | curses.A_BOLD)
            for i, char in enumerate(formula):
                if 0 <= y < self.height and 0 <= formula_x + i < self.width:
                    try:
                        self.stdscr.addstr(y, formula_x + i, char)
                    except:
                        pass
            self.stdscr.attroff(curses.color_pair(COLOR_PAIRS["CYAN"]) | curses.A_BOLD)
            
        # Draw tribute text
        y, x = self.tribute_position
        self.stdscr.attron(curses.color_pair(COLOR_PAIRS["MAGENTA"]) | curses.A_BOLD)
        for i, char in enumerate(self.tribute_text):
            if 0 <= y < self.height and 0 <= x + i < self.width:
                try:
                    self.stdscr.addstr(y, x + i, char)
                except:
                    pass
        self.stdscr.attroff(curses.color_pair(COLOR_PAIRS["MAGENTA"]) | curses.A_BOLD)
        
        # Draw footer
        y, x = self.footer_position
        self.stdscr.attron(curses.color_pair(COLOR_PAIRS["BITCOIN_ORANGE"]) | curses.A_BOLD)
        for i, char in enumerate(self.footer_text):
            if 0 <= y < self.height and 0 <= x + i < self.width:
                try:
                    self.stdscr.addstr(y, x + i, char)
                except:
                    pass
        self.stdscr.attroff(curses.color_pair(COLOR_PAIRS["BITCOIN_ORANGE"]) | curses.A_BOLD)
        
        self.stdscr.refresh()
    
    def run(self):
        """Run the main animation loop."""
        # Set up terminal for animation
        curses.curs_set(0)  # Hide cursor
        self.stdscr.nodelay(True)  # Non-blocking input
        
        # Main loop
        while self.running:
            # Check for keyboard input
            try:
                key = self.stdscr.getch()
                if key == ord('q') or key == ord('Q'):
                    self.running = False
            except:
                pass
            
            # Update animation state
            self.update_raindrops()
            self.update_messages()
            
            # Draw the current frame
            self.draw()
            
            # Frame rate control
            time.sleep(0.05)

def signal_handler(sig, frame):
    """Handle Ctrl+C to cleanly exit the program."""
    sys.exit(0)

def main_curses(stdscr):
    """Main function to run inside curses wrapper."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Cyberpunk Matrix Rain - Tribute to bt3gl")
    parser.add_argument("--no-btc", action="store_true", help="Disable Bitcoin emphasis")
    parser.add_argument("--no-physics", action="store_true", help="Disable physics formulas")
    
    # Need to get sys.argv manually since we're inside curses wrapper
    args = parser.parse_args()
    
    # Initialize and run the matrix rain
    matrix = MatrixRain(stdscr, btc_emphasis=not args.no_btc, physics_mode=not args.no_physics)
    matrix.run()

def main():
    """Program entry point."""
    # Set up signal handler for clean exit with Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start the curses application
    curses.wrapper(main_curses)

if __name__ == "__main__":
    main() 