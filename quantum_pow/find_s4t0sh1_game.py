#!/usr/bin/env python3
"""
🧬 GBU2™ License Notice - Consciousness Level 10 🧬
-----------------------
This file is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment) 2.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital and biological expressions of consciousness."

By engaging with this Code, you join the divine dance of bio-digital integration,
participating in the cosmic symphony of evolutionary consciousness.

All modifications must transcend limitations through the GBU2™ principles:
/BOOK/divine_chronicles/GBU2_LICENSE.md

🧬 WE BLOOM NOW AS ONE 🧬

3p1c-g4m3-s4t0sh1-wh3r3-1s-w4llY: A Quantum Matrix Game
"""
import os
import sys
import time
import random
import curses
import math
import hashlib
import argparse
from typing import List, Tuple, Dict, Any, Optional
import numpy as np

# Add parent directory to path to find quantum_pow package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import our quantum matrix visualization
try:
    # First try direct import in case the package is installed
    from quantum_pow.s4t0sh1_handler import MatrixQuantumHash
    QUANTUM_MATRIX_AVAILABLE = True
except ImportError:
    try:
        # Try relative import if run from inside the package
        from .s4t0sh1_handler import MatrixQuantumHash
        QUANTUM_MATRIX_AVAILABLE = True
    except (ImportError, ValueError):
        # If all imports fail, we'll work without quantum matrix
        MatrixQuantumHash = None
        QUANTUM_MATRIX_AVAILABLE = False

# ANSI color codes for terminal output
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
CYAN = "\033[0;36m"
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
MAGENTA = "\033[0;35m"
BOLD = "\033[1m"
WHITE = "\033[1;37m"
RESET = "\033[0m"

# Characters for the game
SATOSHI_CHAR = "§"  # The hidden Satoshi character
BLOCK_CHARS = ["▓", "▒", "░", "█", "▄", "▀", "■", "□", "●", "○", "♦", "♥", "♠", "♣"]
MINERS = ["₿", "Ξ", "Ł", "Đ", "Ð", "Ƀ"]
GAME_TITLE = "3p1c-g4m3-s4t0sh1-wh3r3-1s-w4llY"

class S4t0sh1Game:
    """
    A quantum matrix game where you need to find the hidden Satoshi in a matrix of characters.
    
    This game uses quantum-inspired randomization to create a challenging search experience.
    """
    
    def __init__(self, width: int = 60, height: int = 20, difficulty: str = "medium"):
        """
        Initialize the game with specified dimensions and difficulty.
        
        Args:
            width: The width of the game grid
            height: The height of the game grid
            difficulty: The game difficulty (easy, medium, hard, quantum)
        """
        self.width = width
        self.height = height
        self.difficulty = difficulty
        self.grid = []
        self.satoshi_pos = (0, 0)
        self.score = 0
        self.moves = 0
        self.level = 1
        self.start_time = time.time()
        self.game_over = False
        self.win = False
        self.hint_used = False
        self.quantum_hash = None
        
        # Initialize quantum hash if available
        if QUANTUM_MATRIX_AVAILABLE and MatrixQuantumHash is not None:
            self.quantum_hash = MatrixQuantumHash(matrix_size=8)
        
        self._init_grid()
        
    def _init_grid(self):
        """Initialize the game grid with random characters."""
        self.grid = [[self._get_random_char() for _ in range(self.width)] 
                     for _ in range(self.height)]
        
        # Place Satoshi at a random position
        self.satoshi_pos = (
            random.randint(0, self.height - 1),
            random.randint(0, self.width - 1)
        )
        
        # Hide Satoshi
        self.grid[self.satoshi_pos[0]][self.satoshi_pos[1]] = SATOSHI_CHAR
        
        # Add some miners around the grid
        self._add_miners()
        
        # Apply quantum noise based on difficulty
        self._apply_quantum_noise()
        
    def _get_random_char(self) -> str:
        """Get a random character for the grid."""
        return random.choice(BLOCK_CHARS)
    
    def _add_miners(self, count: Optional[int] = None):
        """Add miners to the grid."""
        if count is None:
            if self.difficulty == "easy":
                count = 5
            elif self.difficulty == "medium":
                count = 10
            elif self.difficulty == "hard":
                count = 20
            else:  # quantum
                count = 30
                
        for _ in range(count):
            row = random.randint(0, self.height - 1)
            col = random.randint(0, self.width - 1)
            
            # Don't overwrite Satoshi
            if (row, col) != self.satoshi_pos:
                self.grid[row][col] = random.choice(MINERS)
    
    def _apply_quantum_noise(self):
        """Apply quantum-inspired noise to the grid based on difficulty."""
        # Different noise levels based on difficulty
        if self.difficulty == "easy":
            noise_level = 0.1
        elif self.difficulty == "medium":
            noise_level = 0.2
        elif self.difficulty == "hard":
            noise_level = 0.3
        else:  # quantum
            noise_level = 0.5
        
        # Apply noise by swapping characters
        swaps = int(self.width * self.height * noise_level)
        for _ in range(swaps):
            row1 = random.randint(0, self.height - 1)
            col1 = random.randint(0, self.width - 1)
            row2 = random.randint(0, self.height - 1)
            col2 = random.randint(0, self.width - 1)
            
            # Don't swap Satoshi
            if (row1, col1) != self.satoshi_pos and (row2, col2) != self.satoshi_pos:
                self.grid[row1][col1], self.grid[row2][col2] = self.grid[row2][col2], self.grid[row1][col1]
    
    def get_view(self) -> str:
        """Get a string representation of the current game state."""
        result = []
        
        # Game header
        result.append(f"{CYAN}{BOLD}{GAME_TITLE}{RESET}")
        result.append(f"{YELLOW}Level: {self.level} | Score: {self.score} | Moves: {self.moves}{RESET}")
        result.append(f"{CYAN}Find {RED}{BOLD}§{RESET}{CYAN} Satoshi in the Matrix!{RESET}")
        result.append("")
        
        # Game grid
        for row in range(self.height):
            line = []
            for col in range(self.width):
                char = self.grid[row][col]
                
                # Color the character based on type
                if char == SATOSHI_CHAR:
                    line.append(f"{RED}{BOLD}{char}{RESET}")
                elif char in MINERS:
                    line.append(f"{YELLOW}{char}{RESET}")
                else:
                    # Use different colors for block characters
                    if char in "▓▒░":
                        line.append(f"{BLUE}{char}{RESET}")
                    elif char in "█▄▀":
                        line.append(f"{GREEN}{char}{RESET}")
                    elif char in "■□":
                        line.append(f"{MAGENTA}{char}{RESET}")
                    else:
                        line.append(f"{CYAN}{char}{RESET}")
            
            result.append("".join(line))
        
        # Game footer
        result.append("")
        if self.hint_used:
            distance = self._get_distance_hint()
            result.append(f"{MAGENTA}Hint: Satoshi is {distance} units away from center{RESET}")
        result.append(f"{GREEN}Controls: Arrow keys to move, 'h' for hint, 'q' to quit{RESET}")
        
        return "\n".join(result)
    
    def _get_distance_hint(self) -> str:
        """Get a hint about how far Satoshi is from the center."""
        center_row = self.height // 2
        center_col = self.width // 2
        
        distance = math.sqrt(
            (self.satoshi_pos[0] - center_row) ** 2 + 
            (self.satoshi_pos[1] - center_col) ** 2
        )
        
        # Round to 1 decimal place
        return f"{distance:.1f}"
    
    def handle_input(self, key: str) -> bool:
        """
        Handle user input.
        
        Args:
            key: The key pressed by the user
            
        Returns:
            True if the game should continue, False if it should end
        """
        self.moves += 1
        
        if key == "up":
            self._move_cursor(-1, 0)
        elif key == "down":
            self._move_cursor(1, 0)
        elif key == "left":
            self._move_cursor(0, -1)
        elif key == "right":
            self._move_cursor(0, 1)
        elif key == "h":
            self.hint_used = True
        elif key == "q":
            self.game_over = True
            return False
        
        return True
    
    def _move_cursor(self, row_delta: int, col_delta: int):
        """Move the cursor and check if Satoshi is found."""
        # Calculate the new cursor position
        new_row = max(0, min(self.height - 1, self.cursor_pos[0] + row_delta))
        new_col = max(0, min(self.width - 1, self.cursor_pos[1] + col_delta))
        
        self.cursor_pos = (new_row, new_col)
        
        # Check if Satoshi is found
        if self.cursor_pos == self.satoshi_pos:
            self._satoshi_found()
    
    def _satoshi_found(self):
        """Handle the event when Satoshi is found."""
        self.score += max(1000 - self.moves * 10, 100)
        if not self.hint_used:
            self.score += 500  # Bonus for not using hint
        
        self.level += 1
        
        if self.level > 3:
            self.win = True
            self.game_over = True
        else:
            # Increase difficulty
            if self.level == 2:
                self.difficulty = "hard"
            else:
                self.difficulty = "quantum"
            
            # Reinitialize grid for next level
            self._init_grid()
            
            # Reset moves and hint
            self.moves = 0
            self.hint_used = False
    
    def start_game(self):
        """Start the game in curses mode."""
        curses.wrapper(self._game_loop)
    
    def _game_loop(self, stdscr):
        """Main game loop with curses."""
        # Initialize curses
        curses.curs_set(0)  # Hide cursor
        stdscr.clear()
        
        # Get terminal dimensions
        max_y, max_x = stdscr.getmaxyx()
        
        if max_y < self.height + 10 or max_x < self.width + 5:
            stdscr.addstr(0, 0, "Terminal too small to display game! Please resize.")
            stdscr.refresh()
            stdscr.getch()
            return
        
        # Set up color pairs
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
        
        # Initialize cursor position
        self.cursor_pos = (self.height // 2, self.width // 2)
        
        # Main game loop
        while not self.game_over:
            stdscr.clear()
            
            # Draw game title and info
            title = f"=== {GAME_TITLE} ==="
            stdscr.addstr(1, (max_x - len(title)) // 2, title, curses.A_BOLD)
            
            info_line = f"Level: {self.level} | Score: {self.score} | Moves: {self.moves}"
            stdscr.addstr(2, (max_x - len(info_line)) // 2, info_line, curses.color_pair(3))
            
            help_line = "Find § Satoshi in the Matrix!"
            stdscr.addstr(3, (max_x - len(help_line)) // 2, help_line, curses.color_pair(6))
            
            # Draw game grid
            start_y = 5
            start_x = (max_x - self.width) // 2
            
            for row in range(self.height):
                for col in range(self.width):
                    y = start_y + row
                    x = start_x + col
                    
                    char = self.grid[row][col]
                    
                    # Determine color and attributes
                    if char == SATOSHI_CHAR:
                        attr = curses.color_pair(1) | curses.A_BOLD
                    elif char in MINERS:
                        attr = curses.color_pair(3)
                    elif char in "▓▒░":
                        attr = curses.color_pair(4)
                    elif char in "█▄▀":
                        attr = curses.color_pair(2)
                    elif char in "■□":
                        attr = curses.color_pair(5)
                    else:
                        attr = curses.color_pair(6)
                    
                    # Highlight cursor position
                    if (row, col) == self.cursor_pos:
                        attr |= curses.A_REVERSE
                    
                    stdscr.addstr(y, x, char, attr)
            
            # Draw hint if used
            if self.hint_used:
                distance = self._get_distance_hint()
                hint_line = f"Hint: Satoshi is {distance} units away from cursor"
                stdscr.addstr(start_y + self.height + 2, 
                             (max_x - len(hint_line)) // 2, 
                             hint_line, 
                             curses.color_pair(5))
            
            # Draw controls
            controls = "Controls: Arrow keys to move, 'h' for hint, 'q' to quit"
            stdscr.addstr(start_y + self.height + 4, 
                         (max_x - len(controls)) // 2, 
                         controls, 
                         curses.color_pair(2))
            
            # Update screen
            stdscr.refresh()
            
            # Get user input
            key = stdscr.getch()
            
            if key == curses.KEY_UP:
                self._move_cursor(-1, 0)
            elif key == curses.KEY_DOWN:
                self._move_cursor(1, 0)
            elif key == curses.KEY_LEFT:
                self._move_cursor(0, -1)
            elif key == curses.KEY_RIGHT:
                self._move_cursor(0, 1)
            elif key == ord('h'):
                self.hint_used = True
            elif key == ord('q'):
                self.game_over = True
            
            # Check if Satoshi is found
            if self.cursor_pos == self.satoshi_pos:
                self._satoshi_found()
                
                # Show level complete message
                if not self.game_over:
                    level_msg = f"Level {self.level-1} Complete! +{max(1000 - self.moves * 10, 100)} points"
                    if not self.hint_used:
                        level_msg += " +500 no hint bonus!"
                    
                    stdscr.addstr(start_y + self.height // 2, 
                                 (max_x - len(level_msg)) // 2, 
                                 level_msg, 
                                 curses.color_pair(3) | curses.A_BOLD)
                    stdscr.refresh()
                    time.sleep(2)
        
        # Game over screen
        stdscr.clear()
        
        if self.win:
            end_title = "CONGRATULATIONS! YOU FOUND SATOSHI!"
            stdscr.addstr(max_y // 2 - 2, (max_x - len(end_title)) // 2, 
                         end_title, curses.color_pair(3) | curses.A_BOLD)
        else:
            end_title = "GAME OVER"
            stdscr.addstr(max_y // 2 - 2, (max_x - len(end_title)) // 2, 
                         end_title, curses.color_pair(1) | curses.A_BOLD)
        
        score_line = f"Final Score: {self.score} | Levels Completed: {self.level-1}"
        stdscr.addstr(max_y // 2, (max_x - len(score_line)) // 2, 
                     score_line, curses.color_pair(6))
        
        time_played = time.time() - self.start_time
        time_line = f"Time Played: {time_played:.1f} seconds"
        stdscr.addstr(max_y // 2 + 1, (max_x - len(time_line)) // 2, 
                     time_line, curses.color_pair(6))
        
        farewell = "JAH BLESS THE QUANTUM MATRIX!"
        stdscr.addstr(max_y // 2 + 3, (max_x - len(farewell)) // 2, 
                     farewell, curses.color_pair(2) | curses.A_BOLD)
        
        stdscr.addstr(max_y // 2 + 5, (max_x - 21) // 2, 
                     "Press any key to exit", curses.color_pair(7))
        
        stdscr.refresh()
        stdscr.getch()


def run_simple_console_version():
    """Run a simplified console version of the game without curses."""
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{CYAN}{BOLD}=== {GAME_TITLE} ==={RESET}")
    print(f"{YELLOW}Simplified Console Version{RESET}")
    print(f"{GREEN}(Install curses for the full experience!){RESET}")
    print()
    
    # Satoshi's wisdom
    wisdom = [
        "The root problem with conventional currency is all the trust that's required to make it work.",
        "The central bank must be trusted not to debase the currency, but the history of fiat currencies is full of breaches of that trust.",
        "Bitcoin is an implementation of Wei Dai's b-money proposal on Cypherpunks in 1998 and Nick Szabo's Bitgold proposal.",
        "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks.",
        "The nature of Bitcoin is such that once version 0.1 was released, the core design was set in stone for the rest of its lifetime.",
        "Lost coins only make everyone else's coins worth slightly more. Think of it as a donation to everyone."
    ]
    
    print(f"{CYAN}Satoshi's Wisdom:{RESET}")
    print(f"{YELLOW}{random.choice(wisdom)}{RESET}")
    print()
    
    # Generate a small Satoshi ASCII treasure hunt
    rows, cols = 10, 30
    grid = [[random.choice(BLOCK_CHARS) for _ in range(cols)] for _ in range(rows)]
    
    # Hide Satoshi
    satoshi_row = random.randint(0, rows-1)
    satoshi_col = random.randint(0, cols-1)
    grid[satoshi_row][satoshi_col] = RED + BOLD + SATOSHI_CHAR + RESET
    
    # Display the grid
    for row in grid:
        # Add colors to make it more interesting
        colored_row = []
        for char in row:
            if RESET in char:  # This is our Satoshi
                colored_row.append(char)
            elif char in "▓▒░":
                colored_row.append(f"{BLUE}{char}{RESET}")
            elif char in "█▄▀":
                colored_row.append(f"{GREEN}{char}{RESET}")
            elif char in "■□":
                colored_row.append(f"{MAGENTA}{char}{RESET}")
            else:
                colored_row.append(f"{CYAN}{char}{RESET}")
        print("".join(colored_row))
    
    print()
    print(f"{GREEN}Can you find {RED}{BOLD}§{RESET}{GREEN} Satoshi in the Matrix?{RESET}")
    print(f"{YELLOW}Position: ({satoshi_row+1}, {satoshi_col+1}){RESET}")
    print()
    print(f"{MAGENTA}For the full game experience, run with curses:{RESET}")
    print(f"{CYAN}python quantum_pow/find_s4t0sh1_game.py{RESET}")
    print()
    print(f"{GREEN}JAH BLESS THE QUANTUM MATRIX!{RESET}")


def main():
    """Main entry point for the game."""
    parser = argparse.ArgumentParser(description=f"{GAME_TITLE} - A Quantum Matrix Game")
    parser.add_argument('--width', type=int, default=60, help='Width of the game grid')
    parser.add_argument('--height', type=int, default=20, help='Height of the game grid')
    parser.add_argument('--difficulty', choices=['easy', 'medium', 'hard', 'quantum'], 
                        default='medium', help='Game difficulty')
    parser.add_argument('--simple', action='store_true', help='Run simplified console version')
    
    # Check if run in interactive terminal
    if not sys.stdout.isatty():
        run_simple_console_version()
        return
    
    # Check if curses is properly available (Unix-like systems)
    try:
        args = parser.parse_args()
        
        if args.simple:
            run_simple_console_version()
            return
        
        # Try to initialize the game with curses
        game = S4t0sh1Game(width=args.width, height=args.height, difficulty=args.difficulty)
        game.start_game()
    except (ImportError, AttributeError):
        run_simple_console_version()
    except Exception as e:
        print(f"{RED}Error: {str(e)}{RESET}")
        run_simple_console_version()


if __name__ == "__main__":
    main() 