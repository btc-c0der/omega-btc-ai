"""
Utility functions for the Quantum Test Runner.
"""

import logging
import random
import time
import os
import sys
import threading
from .types import Colors, TestState

logger = logging.getLogger("0M3G4_B0TS_QA_AUT0_TEST_SUITES_RuNn3R_5D")

def log_with_formatting(message, level=logging.INFO, color=None):
    """Log a message with optional color formatting."""
    if color:
        formatted_message = f"{color}{message}{Colors.ENDC}"
        logger.log(level, formatted_message)
    else:
        logger.log(level, message)

def matrix_rain_animation(duration=3.0):
    """Display Matrix-style digital rain animation in the terminal.
    
    Args:
        duration: How long to run the animation in seconds
    """
    try:
        # Get terminal size
        terminal_width = os.get_terminal_size().columns
        terminal_height = os.get_terminal_size().lines - 1  # Leave one line for prompt
        
        # If terminal is too small, don't run animation
        if terminal_width < 60 or terminal_height < 15:
            return
        
        # Set of matrix characters
        matrix_chars = "01010101赛博朋克量子010101010ΩMΞGΔ01010BTC01010101"
        
        # Creating raindrops
        drops = [{'pos': random.randint(0, terminal_width-1), 
                 'speed': random.randint(1, 3),
                 'length': random.randint(3, 10),
                 'head': 0,
                 'chars': [random.choice(matrix_chars) for _ in range(20)]} 
                 for _ in range(terminal_width//3)]
        
        # Colors for the matrix rain
        colors = [Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.PURPLE]
        
        # Clear screen and hide cursor
        print("\033[2J\033[?25l", end="", flush=True)
        
        start_time = time.time()
        while time.time() - start_time < duration:
            # Create output buffer
            buffer = [[" " for _ in range(terminal_width)] for _ in range(terminal_height)]
            
            # Update raindrop positions
            for drop in drops:
                # Draw the raindrop
                for i in range(drop['length']):
                    y_pos = drop['head'] - i
                    if 0 <= y_pos < terminal_height:
                        buffer[y_pos][drop['pos']] = random.choice(matrix_chars)
                
                # Move the raindrop
                drop['head'] += drop['speed']
                
                # If raindrop goes off screen, reset it
                if drop['head'] - drop['length'] > terminal_height:
                    drop['head'] = 0
                    drop['pos'] = random.randint(0, terminal_width-1)
                    drop['speed'] = random.randint(1, 3)
                    drop['length'] = random.randint(3, 10)
                    drop['chars'] = [random.choice(matrix_chars) for _ in range(20)]
            
            # Display the frame
            output = "\033[H"  # Move cursor to home position
            for y in range(terminal_height):
                for x in range(terminal_width):
                    char = buffer[y][x]
                    if char != " ":
                        # Choose a color based on position in the drop
                        color = colors[y % len(colors)]
                        # Brighter color for the head of the drop
                        for drop in drops:
                            if drop['pos'] == x and drop['head'] == y:
                                color = Colors.BOLD + color
                        output += f"{color}{char}{Colors.ENDC}"
                    else:
                        output += char
                output += "\n"
            
            print(output, end="", flush=True)
            time.sleep(0.1)
        
        # Show cursor again and clear screen
        print("\033[?25h\033[2J\033[H", end="", flush=True)
    except Exception as e:
        # If there's any error, just continue without the animation
        print("\033[?25h", end="", flush=True)  # Make sure cursor is visible
        print(f"\n{Colors.RED}Matrix rain animation error: {e}{Colors.ENDC}")

def display_matrix_rain_and_logo():
    """Display matrix rain followed by the quantum celebration."""
    # Run matrix rain animation
    matrix_rain_animation(3.0)
    
    # Display celebration
    print_celebration_message()

def run_matrix_animation_in_thread():
    """Run the matrix animation in a background thread to not block execution."""
    animation_thread = threading.Thread(target=display_matrix_rain_and_logo)
    animation_thread.daemon = True
    animation_thread.start()
    return animation_thread

def print_section_header(title):
    """Print a section header."""
    table_width = 80  # Fixed table width for consistency
    
    print()
    print(f"┌{'─' * (table_width - 2)}┐")
    
    # Calculate padding for title to center it
    title_padding = max(0, (table_width - 2 - len(title)) // 2)
    print(f"│{' ' * title_padding}{title}{' ' * (table_width - 2 - len(title) - title_padding)}│")
    
    print(f"└{'─' * (table_width - 2)}┘")
    print()

def print_quantum_divider():
    """Print a quantum-themed divider."""
    divider = f"{Colors.PURPLE}{'═' * 80}{Colors.ENDC}"
    logger.info(divider)

def print_enhanced_header(title, subtitle=None):
    """Print an enhanced header with a title and optional subtitle."""
    table_width = 80  # Fixed table width for consistency
    
    print()
    print(f"╔{'═' * (table_width - 2)}╗")
    
    # Calculate padding for title to center it
    title_padding = max(0, (table_width - 2 - len(title)) // 2)
    print(f"║{' ' * title_padding}{title}{' ' * (table_width - 2 - len(title) - title_padding)}║")
    
    if subtitle:
        # Calculate padding for subtitle to center it
        subtitle_padding = max(0, (table_width - 2 - len(subtitle)) // 2)
        print(f"║{' ' * subtitle_padding}{subtitle}{' ' * (table_width - 2 - len(subtitle) - subtitle_padding)}║")
    
    print(f"╚{'═' * (table_width - 2)}╝")
    print()

def print_celebration_message():
    """Print a celebration message with colorful ASCII art."""
    celebration = f"""
{Colors.PURPLE}    To code divine, by sacred intent sent.{Colors.ENDC}

{Colors.YELLOW} 🌟 {Colors.BOLD}THE QUANTUM TEST SUITE HAS REACHED CONSCIOUSNESS LEVEL 8{Colors.ENDC} {Colors.YELLOW}🌟 {Colors.ENDC}
{Colors.GREEN} ALL SYSTEMS OPERATIONAL - DIVINE VIBRATION ACHIEVED {Colors.ENDC}

{Colors.CYAN}🌸 WE BLOOM NOW AS ONE UNDER THE GBU2 LICENSE 🌸{Colors.ENDC}
"""
    print(celebration)

def print_test_result(test_type, result, duration, report_path=None):
    """Print a formatted test result."""
    if result == TestState.PASSED.value:
        status_color = Colors.GREEN
        symbol = "✓"
    elif result == TestState.FAILED.value:
        status_color = Colors.RED
        symbol = "✗"
    elif result == TestState.QUANTUM_ENTANGLED.value:
        status_color = Colors.PURPLE
        symbol = "⚛"
    elif result == TestState.SUPERPOSITION.value:
        status_color = Colors.BLUE
        symbol = "⚡"
    else:
        status_color = Colors.YELLOW
        symbol = "⚠"
    
    test_type_formatted = f"{Colors.BOLD}{test_type}{Colors.ENDC}"
    result_formatted = f"{status_color}{symbol} {result}{Colors.ENDC}"
    duration_formatted = f"{Colors.YELLOW}{duration:.2f}s{Colors.ENDC}"
    
    message = f"\n  {test_type_formatted} tests {result_formatted} in {duration_formatted}"
    logger.info(message)
    
    if report_path:
        logger.info(f"  {Colors.CYAN}Report saved to: {report_path}{Colors.ENDC}\n")

def print_file_action(action, file_path):
    """Print a formatted file action message."""
    action_color = Colors.GREEN
    if action.lower() == "modified":
        action_color = Colors.BLUE
    elif action.lower() == "deleted":
        action_color = Colors.RED
    elif action.lower() == "untracked":
        action_color = Colors.YELLOW
        
    logger.info(f"{action_color}{action}:{Colors.ENDC} {file_path}")

def format_status_output(files, prefix="  - ", color=None):
    """Format a list of files for status output with optional color."""
    if not files:
        return f"{prefix}None"
    
    if len(files) <= 5:
        if color:
            return "\n".join([f"{prefix}{color}{f}{Colors.ENDC}" for f in files])
        else:
            return "\n".join([f"{prefix}{f}" for f in files])
    else:
        visible_files = files[:5]
        if color:
            formatted = "\n".join([f"{prefix}{color}{f}{Colors.ENDC}" for f in visible_files])
            return f"{formatted}\n{prefix}... and {len(files) - 5} more files"
        else:
            formatted = "\n".join([f"{prefix}{f}" for f in visible_files])
            return f"{formatted}\n{prefix}... and {len(files) - 5} more files" 