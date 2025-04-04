#!/usr/bin/env python3
"""
🐞 BUG HUNTER: QA MATRIX CHALLENGE 🐞
-------------------------------------
A cyberpunk-themed game where QA professionals hunt for bugs in the code Matrix.
Created by Claude Sonnet for the OMEGA BTC AI Team.
"""

import os
import sys
import time
import random
import curses
from curses import wrapper
import textwrap
import signal
from typing import List, Dict, Tuple, Any, Optional

# ANSI colors for terminal output
class Colors:
    RESET = "\033[0m"
    NEON_GREEN = "\033[38;5;82m"
    NEON_BLUE = "\033[38;5;39m"
    NEON_PINK = "\033[38;5;213m"
    NEON_YELLOW = "\033[38;5;226m"
    NEON_RED = "\033[38;5;196m"
    NEON_ORANGE = "\033[38;5;208m"
    CYBER_CYAN = "\033[38;5;51m"
    CYBER_PURPLE = "\033[38;5;141m"
    DARK_BG = "\033[48;5;17m"
    BOLD = "\033[1m"

# Cyberpunk ASCII art banner
GAME_BANNER = """
 ██████╗ ██╗   ██╗ ██████╗     ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
 ██╔══██╗██║   ██║██╔════╝     ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
 ██████╔╝██║   ██║██║  ███╗    ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
 ██╔══██╗██║   ██║██║   ██║    ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
 ██████╔╝╚██████╔╝╚██████╔╝    ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
 ╚═════╝  ╚═════╝  ╚═════╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
                                                                                    
 ███╗   ███╗ █████╗ ████████╗██████╗ ██╗██╗  ██╗                                   
 ████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██║╚██╗██╔╝                                   
 ██╔████╔██║███████║   ██║   ██████╔╝██║ ╚███╔╝                                    
 ██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║ ██╔██╗                                    
 ██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║██║██╔╝ ██╗                                   
 ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝                                   
"""

# Bug challenges - each contains code with a bug, a description, and a solution
CHALLENGES = [
    {
        "name": "Discord Bot Command Bug",
        "description": "This Discord bot command handler has a critical bug. Find it and suggest a fix.",
        "code": """
@bot.tree.command(name="status", description="Get the current bot status")
async def slash_status(interaction):
    \"\"\"Return the current status of the bot.\"\"\"
    try:
        # Check bot status
        latency = bot.latency * 1000  # Convert to ms
        uptime = datetime.now() - bot.start_time
        
        # Respond with status info
        response = f"Bot Status: ONLINE\\nLatency: {latency}ms\\nUptime: {uptime}"
        interaction.response.send_message(response)
        
    except Exception as e:
        logger.error(f"Error in status command: {str(e)}")
""",
        "bug_hint": "There's something wrong with the interaction response...",
        "bug_line": 11,
        "bug_description": "The response is not being sent with 'await' - Discord.py requires await for async interaction responses",
        "solution": "await interaction.response.send_message(response)"
    },
    {
        "name": "Quantum Test Coverage Calculation Error",
        "description": "The QA coverage calculation system has a logical error. Find the flaw in the algorithm.",
        "code": """
def calculate_coverage_percentage(covered_lines, total_lines):
    \"\"\"Calculate test coverage percentage.\"\"\"
    # If there are no lines to cover, consider it 100% covered
    if total_lines == 0:
        return 100.0
        
    # Calculate the percentage
    coverage = (covered_lines / total_lines) * 100
    
    # Cap at 100%
    if coverage > 100:
        return 100.0
    
    # Return with 2 decimal precision
    return round(coverage - 0.01, 2)
""",
        "bug_hint": "The calculation precision has an issue...",
        "bug_line": 13,
        "bug_description": "The coverage percentage is being reduced by 0.01 before rounding, causing incorrect results",
        "solution": "return round(coverage, 2)"
    },
    {
        "name": "Matrix Visualization Memory Leak",
        "description": "The matrix data visualization has a subtle bug causing memory leaks. Detect and fix it.",
        "code": """
def render_matrix_visualization(data_points, screen_width, screen_height):
    \"\"\"Render a matrix-style visualization of data points.\"\"\"
    # Initialize matrix grid
    matrix = []
    for y in range(screen_height):
        row = []
        for x in range(screen_width):
            row.append(' ')
        matrix.append(row)
    
    # Plot data points on the matrix
    for point in data_points:
        x, y, value = point
        if 0 <= x < screen_width and 0 <= y < screen_height:
            # Convert value to a character
            char = chr(int(value % 26) + 65)  # A-Z based on value
            matrix[y][x] = char
            
    # Convert matrix to string for rendering
    result = ""
    for row in matrix:
        result += ''.join(row)
        
    return matrix
""",
        "bug_hint": "Check what's being returned from the function...",
        "bug_line": 22,
        "bug_description": "The function builds a 'result' string but then returns the full 'matrix' list, potentially causing memory issues",
        "solution": "return result"
    },
    {
        "name": "Asynchronous Test Execution Race Condition",
        "description": "The async test executor has a race condition. Find and fix it.",
        "code": """
async def run_test_suite_parallel(test_cases, max_workers=5):
    \"\"\"Run test cases in parallel using asyncio.\"\"\"
    results = []
    active_workers = 0
    
    for test in test_cases:
        # Wait if we've reached max workers
        while active_workers >= max_workers:
            await asyncio.sleep(0.1)
            
        # Start the test
        active_workers += 1
        task = asyncio.create_task(run_single_test(test))
        results.append(task)
    
    # Wait for all tests to complete
    final_results = []
    for task in results:
        result = await task
        final_results.append(result)
        active_workers -= 1
        
    return final_results
""",
        "bug_hint": "There's an issue with worker counting...",
        "bug_line": 9,
        "bug_description": "The active_workers counter is incremented but never decremented when a task completes, leading to a deadlock",
        "solution": "Add a callback to decrement active_workers when tasks complete"
    },
    {
        "name": "Discord Bot Authentication Token Leak",
        "description": "This Discord bot code has a security vulnerability. Identify the security risk.",
        "code": """
class DiscordBot:
    \"\"\"Discord bot for the CyBer1t4L QA system.\"\"\"
    def __init__(self, token=None):
        self.token = token or os.getenv("DISCORD_BOT_TOKEN")
        self.app_id = os.getenv("CYBER1T4L_APP_ID")
        self.connected = False
        
        # Print connection info for debugging
        print(f"Initializing Discord bot with token: {self.token}")
        print(f"Bot APP ID: {self.app_id}")
        
    def connect(self):
        \"\"\"Connect the bot to Discord.\"\"\"
        if not self.token:
            raise ValueError("No Discord token provided")
            
        # Log connection attempt
        logging.info(f"Connecting with token {self.token}")
        
        # Connection logic would go here
        self.connected = True
        return True
""",
        "bug_hint": "There's a security issue with sensitive information...",
        "bug_line": 9,
        "bug_description": "The Discord bot token is being printed to console/logs, creating a security vulnerability",
        "solution": "Remove the token print, or mask it like print(f\"Initializing Discord bot with token: {self.token[:4]}...{self.token[-4:]}\")"
    },
]

class BugHunterGame:
    """Main game class for Bug Hunter Matrix."""
    
    def __init__(self, stdscr):
        """Initialize the game with the curses screen."""
        self.stdscr = stdscr
        self.max_y, self.max_x = stdscr.getmaxyx()
        self.title_wins = []
        self.challenge_win = None
        self.hint_win = None
        self.input_win = None
        self.score = 0
        self.current_challenge = 0
        self.game_state = "intro"  # intro, challenge, correct, incorrect, game_over
        self.user_answer = ""
        self.time_left = 60  # seconds for each challenge
        self.last_tick = time.time()
        self.hint_used = False
        
        # Setup colors
        self.init_colors()
        
        # Initialize windows
        self.setup_windows()
        
    def init_colors(self):
        """Initialize color pairs for the game."""
        curses.start_color()
        curses.use_default_colors()
        
        # Define color pairs
        curses.init_pair(1, curses.COLOR_GREEN, -1)      # Matrix green
        curses.init_pair(2, curses.COLOR_CYAN, -1)       # Cyan
        curses.init_pair(3, curses.COLOR_YELLOW, -1)     # Yellow
        curses.init_pair(4, curses.COLOR_MAGENTA, -1)    # Magenta
        curses.init_pair(5, curses.COLOR_RED, -1)        # Red
        curses.init_pair(6, curses.COLOR_BLUE, -1)       # Blue
        curses.init_pair(7, curses.COLOR_WHITE, -1)      # White
        curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_RED)  # Highlight for bugs
        
    def setup_windows(self):
        """Setup the game windows."""
        # Title window (multi-line)
        title_height = 10
        title_width = self.max_x - 4
        title_y = 1
        title_x = 2
        self.title_win = curses.newwin(title_height, title_width, title_y, title_x)
        
        # Challenge window (shows code)
        challenge_height = self.max_y - 20
        challenge_width = self.max_x - 4
        challenge_y = title_y + title_height + 1
        challenge_x = 2
        self.challenge_win = curses.newwin(challenge_height, challenge_width, challenge_y, challenge_x)
        
        # Hint window
        hint_height = 3
        hint_width = self.max_x - 4
        hint_y = challenge_y + challenge_height + 1
        hint_x = 2
        self.hint_win = curses.newwin(hint_height, hint_width, hint_y, hint_x)
        
        # Input window
        input_height = 3
        input_width = self.max_x - 4
        input_y = hint_y + hint_height + 1
        input_x = 2
        self.input_win = curses.newwin(input_height, input_width, input_y, input_x)
        
    def draw_title(self):
        """Draw the game title and banner."""
        self.title_win.clear()
        self.title_win.border()
        
        # Split the banner into lines
        banner_lines = GAME_BANNER.split('\n')
        max_line_length = min(self.max_x - 6, max(len(line) for line in banner_lines))
        
        # Draw each line of the banner with appropriate color
        for i, line in enumerate(banner_lines[:8]):  # Limit to max 8 lines
            if i < self.title_win.getmaxyx()[0] - 2:  # Ensure we don't overflow
                x_pos = (self.title_win.getmaxyx()[1] - max_line_length) // 2
                
                # Use different colors for different parts of the banner
                color = curses.color_pair(i % 5 + 1)
                self.title_win.addstr(i + 1, x_pos, line[:max_line_length], color | curses.A_BOLD)
        
        self.title_win.refresh()
        
    def draw_stats(self):
        """Draw the game stats at the top."""
        stats_text = f" SCORE: {self.score} | CHALLENGE: {self.current_challenge + 1}/{len(CHALLENGES)} | TIME: {self.time_left}s "
        x_pos = self.title_win.getmaxyx()[1] - len(stats_text) - 1
        if self.time_left <= 10:  # Warning color when time is low
            self.title_win.addstr(0, x_pos, stats_text, curses.color_pair(5) | curses.A_BOLD)
        else:
            self.title_win.addstr(0, x_pos, stats_text, curses.color_pair(3) | curses.A_BOLD)
        self.title_win.refresh()
        
    def draw_challenge(self):
        """Draw the current challenge code with syntax highlighting."""
        self.challenge_win.clear()
        self.challenge_win.border()
        
        # Get current challenge
        challenge = CHALLENGES[self.current_challenge]
        
        # Draw the challenge name and description
        self.challenge_win.addstr(1, 2, f"CHALLENGE: {challenge['name']}", curses.color_pair(4) | curses.A_BOLD)
        
        # Wrap and draw the description
        desc_wrapped = textwrap.wrap(challenge['description'], self.challenge_win.getmaxyx()[1] - 4)
        for i, line in enumerate(desc_wrapped):
            self.challenge_win.addstr(2 + i, 2, line, curses.color_pair(7))
        
        # Draw the code snippet with line numbers
        code_lines = challenge['code'].strip().split('\n')
        for i, line in enumerate(code_lines):
            # Line number
            self.challenge_win.addstr(4 + i, 2, f"{i+1:2d} | ", curses.color_pair(6))
            
            # Code line with basic syntax highlighting
            code_line = line
            pos = 4 + 5  # After line number
            
            # Very basic syntax highlighting
            if 'def ' in code_line:
                parts = code_line.split('def ')
                self.challenge_win.addstr(4 + i, pos, parts[0], curses.color_pair(7))
                pos += len(parts[0])
                self.challenge_win.addstr(4 + i, pos, 'def ', curses.color_pair(2) | curses.A_BOLD)
                pos += 4
                if len(parts) > 1:
                    self.challenge_win.addstr(4 + i, pos, parts[1], curses.color_pair(3))
            elif 'return ' in code_line:
                parts = code_line.split('return ')
                self.challenge_win.addstr(4 + i, pos, parts[0], curses.color_pair(7))
                pos += len(parts[0])
                self.challenge_win.addstr(4 + i, pos, 'return ', curses.color_pair(5) | curses.A_BOLD)
                pos += 7
                if len(parts) > 1:
                    self.challenge_win.addstr(4 + i, pos, parts[1], curses.color_pair(1))
            elif '#' in code_line:
                parts = code_line.split('#', 1)
                self.challenge_win.addstr(4 + i, pos, parts[0], curses.color_pair(7))
                pos += len(parts[0])
                self.challenge_win.addstr(4 + i, pos, '#' + parts[1], curses.color_pair(6) | curses.A_DIM)
            elif 'import ' in code_line:
                parts = code_line.split('import ')
                self.challenge_win.addstr(4 + i, pos, parts[0], curses.color_pair(7))
                pos += len(parts[0])
                self.challenge_win.addstr(4 + i, pos, 'import ', curses.color_pair(4) | curses.A_BOLD)
                pos += 7
                if len(parts) > 1:
                    self.challenge_win.addstr(4 + i, pos, parts[1], curses.color_pair(2))
            else:
                self.challenge_win.addstr(4 + i, pos, code_line, curses.color_pair(7))
            
            # Highlight the bug line if in feedback mode
            if self.game_state in ["correct", "incorrect"] and i + 1 == challenge["bug_line"]:
                self.challenge_win.addstr(4 + i, 1, "→", curses.color_pair(5) | curses.A_BOLD)
        
        # In feedback mode, show the bug description
        if self.game_state in ["correct", "incorrect"]:
            offset = len(code_lines) + 5
            self.challenge_win.addstr(offset, 2, "BUG DESCRIPTION:", curses.color_pair(5) | curses.A_BOLD)
            desc_wrapped = textwrap.wrap(challenge['bug_description'], self.challenge_win.getmaxyx()[1] - 4)
            for i, line in enumerate(desc_wrapped):
                self.challenge_win.addstr(offset + i + 1, 2, line, curses.color_pair(7))
                
            self.challenge_win.addstr(offset + len(desc_wrapped) + 2, 2, "SOLUTION:", curses.color_pair(2) | curses.A_BOLD)
            self.challenge_win.addstr(offset + len(desc_wrapped) + 3, 2, challenge['solution'], curses.color_pair(3))
        
        self.challenge_win.refresh()
        
    def draw_hint(self):
        """Draw the hint window."""
        self.hint_win.clear()
        self.hint_win.border()
        
        if self.hint_used:
            hint_text = f"HINT: {CHALLENGES[self.current_challenge]['bug_hint']}"
            self.hint_win.addstr(1, 2, hint_text, curses.color_pair(3))
        else:
            self.hint_win.addstr(1, 2, "Press 'H' for a hint (costs 5 points)", curses.color_pair(7))
            
        self.hint_win.refresh()
        
    def draw_input(self):
        """Draw the input window."""
        self.input_win.clear()
        self.input_win.border()
        
        if self.game_state == "intro":
            self.input_win.addstr(1, 2, "Press ENTER to start hunting bugs!", curses.color_pair(2) | curses.A_BOLD)
        elif self.game_state == "challenge":
            prompt = "What line number contains the bug? "
            self.input_win.addstr(1, 2, prompt, curses.color_pair(7))
            self.input_win.addstr(1, 2 + len(prompt), self.user_answer, curses.color_pair(3) | curses.A_BOLD)
        elif self.game_state == "correct":
            self.input_win.addstr(1, 2, "CORRECT! Press ENTER for next challenge", curses.color_pair(2) | curses.A_BOLD)
        elif self.game_state == "incorrect":
            self.input_win.addstr(1, 2, "Study the bug. Press ENTER for next challenge", curses.color_pair(5) | curses.A_BOLD)
        elif self.game_state == "game_over":
            self.input_win.addstr(1, 2, f"GAME OVER! Final Score: {self.score}. Press ENTER to exit", curses.color_pair(4) | curses.A_BOLD)
            
        self.input_win.refresh()
        
    def draw_screen(self):
        """Draw the complete game screen."""
        self.stdscr.clear()
        self.draw_title()
        
        if self.game_state != "intro":
            self.draw_stats()
            self.draw_challenge()
            self.draw_hint()
            
        self.draw_input()
        self.stdscr.refresh()
        
    def process_input(self, key):
        """Process user input."""
        if self.game_state == "intro":
            if key == ord('\n'):  # Enter key
                self.game_state = "challenge"
                self.reset_challenge()
        elif self.game_state == "challenge":
            if key == curses.KEY_BACKSPACE or key == 127:  # Handle backspace
                self.user_answer = self.user_answer[:-1]
            elif key == ord('\n'):  # Enter key
                self.check_answer()
            elif key == ord('h') or key == ord('H'):  # Hint
                if not self.hint_used:
                    self.score = max(0, self.score - 5)  # Reduce score for using hint
                    self.hint_used = True
            elif key in range(48, 58):  # Number keys 0-9
                self.user_answer += chr(key)
        elif self.game_state in ["correct", "incorrect"]:
            if key == ord('\n'):  # Enter key
                self.next_challenge()
        elif self.game_state == "game_over":
            if key == ord('\n'):  # Enter key
                return False  # Exit the game
        
        return True  # Continue the game
    
    def check_answer(self):
        """Check if the user's answer is correct."""
        try:
            answer = int(self.user_answer)
            correct_line = CHALLENGES[self.current_challenge]["bug_line"]
            
            if answer == correct_line:
                self.game_state = "correct"
                # Calculate score based on time left and whether hint was used
                time_bonus = self.time_left // 2
                hint_penalty = 5 if self.hint_used else 0
                self.score += 10 + time_bonus - hint_penalty
            else:
                self.game_state = "incorrect"
                # Small penalty for wrong answers
                self.score = max(0, self.score - 3)
        except ValueError:
            # Invalid number format
            self.game_state = "incorrect"
    
    def next_challenge(self):
        """Move to the next challenge or end the game."""
        self.current_challenge += 1
        
        if self.current_challenge >= len(CHALLENGES):
            self.game_state = "game_over"
        else:
            self.game_state = "challenge"
            self.reset_challenge()
    
    def reset_challenge(self):
        """Reset the state for a new challenge."""
        self.user_answer = ""
        self.time_left = 60
        self.hint_used = False
        self.last_tick = time.time()
    
    def update_time(self):
        """Update the game timer."""
        if self.game_state == "challenge":
            current_time = time.time()
            elapsed = current_time - self.last_tick
            
            if elapsed >= 1.0:  # Update every second
                self.time_left -= int(elapsed)
                self.last_tick = current_time
                
                if self.time_left <= 0:
                    self.time_left = 0
                    self.game_state = "incorrect"
    
    def run(self):
        """Main game loop."""
        try:
            # Setup curses
            curses.curs_set(0)  # Hide cursor
            self.stdscr.timeout(100)  # Non-blocking input
            
            running = True
            while running:
                # Update game state
                self.update_time()
                
                # Draw the screen
                self.draw_screen()
                
                # Get user input
                try:
                    key = self.stdscr.getch()
                    if key != -1:  # -1 means no input
                        running = self.process_input(key)
                except Exception as e:
                    # Handle curses input errors
                    pass
                    
        except KeyboardInterrupt:
            return

def handle_exit(signum, frame):
    """Handle exit signals to restore terminal."""
    curses.endwin()
    sys.exit(0)

def display_terminal_intro():
    """Display an intro in the terminal before starting the curses game."""
    print(f"\n{Colors.NEON_GREEN}{GAME_BANNER}{Colors.RESET}\n")
    
    print(f"{Colors.NEON_RED}🔴 {Colors.NEON_YELLOW}🟡 {Colors.NEON_GREEN}🟢 {Colors.CYBER_PURPLE}BUG HUNTER: QA MATRIX CHALLENGE{Colors.NEON_RED} 🔴 {Colors.NEON_YELLOW}🟡 {Colors.NEON_GREEN}🟢{Colors.RESET}")
    print(f"{Colors.NEON_BLUE}┌───────────────────────────────────────────────────┐{Colors.RESET}")
    print(f"{Colors.NEON_BLUE}│{Colors.NEON_PINK} 🐞 Hunt bugs in the code Matrix!                 {Colors.NEON_BLUE}│{Colors.RESET}")
    print(f"{Colors.NEON_BLUE}│{Colors.NEON_GREEN} 🧪 Test your QA skills with cyberpunk challenges {Colors.NEON_BLUE}│{Colors.RESET}")
    print(f"{Colors.NEON_BLUE}│{Colors.CYBER_CYAN} 🧬 Find the line number containing each bug      {Colors.NEON_BLUE}│{Colors.RESET}")
    print(f"{Colors.NEON_BLUE}│{Colors.NEON_YELLOW} 🌟 Score points for each bug you catch!          {Colors.NEON_BLUE}│{Colors.RESET}")
    print(f"{Colors.NEON_BLUE}└───────────────────────────────────────────────────┘{Colors.RESET}")
    
    print(f"\n{Colors.CYBER_PURPLE}Starting the game in 3 seconds...{Colors.RESET}")
    print(f"{Colors.NEON_ORANGE}May your QA instincts guide you through the Matrix!{Colors.RESET}\n")
    time.sleep(3)

def main(stdscr):
    """Main function to run the bug hunter game."""
    game = BugHunterGame(stdscr)
    game.run()

if __name__ == "__main__":
    # Register signal handlers
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    
    # Show terminal intro
    display_terminal_intro()
    
    # Start curses application
    try:
        wrapper(main)
    except KeyboardInterrupt:
        print(f"\n{Colors.NEON_GREEN}Thanks for playing Bug Hunter: QA Matrix Challenge!{Colors.RESET}")
        print(f"\n{Colors.NEON_PINK}Remember: QA professionals are the true heroes of software development!{Colors.RESET}")
        print(f"{Colors.NEON_ORANGE}~ Created by Claude Sonnet for the OMEGA BTC AI Team ~{Colors.RESET}\n") 