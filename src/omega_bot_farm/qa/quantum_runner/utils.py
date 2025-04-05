"""
Utility functions for the Quantum Test Runner.
"""

import logging
import random
import time
import os
import sys
import threading
import shutil
from .types import Colors, TestState

logger = logging.getLogger("0M3G4_B0TS_QA_AUT0_TEST_SUITES_RuNn3R_5D")

# Progress bar styles
PROGRESS_BAR_STYLES = {
    'standard': ('█', '░'),           # Standard blocks
    'dots': ('•', '·'),               # Dots style
    'line': ('━', '─'),               # Line style 
    'blocks': ('▓', '▒'),             # Gradient blocks
    'arrows': ('►', '─'),             # Arrows
    'equals': ('=', '-'),             # Classic equals
    'stars': ('★', '☆'),             # Stars
    'waves': ('∿', '⌒'),             # Waves
    'braille': ('⣿', '⣀'),           # Braille patterns
    'cyber': ('◉', '◎'),             # Cyberpunk style
    'matrix': ('⟪', '⟫'),            # Matrix style
    'quantum': ('⚬', '○'),           # Quantum style
    'bitcoin': ('₿', '○'),           # Bitcoin style
    'hex': ('⬢', '⬡'),               # Hexagon
    'circuit': ('◼', '◻'),           # Circuit style
    'classic': ('#', '.'),            # Classic ASCII
}

# Animated progress bar frames
ANIMATED_PROGRESS_FRAMES = {
    'spinner': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
    'dots': ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷'],
    'pulse': ['[    ]', '[=   ]', '[==  ]', '[=== ]', '[====]', '[ ===]', '[  ==]', '[   =]'],
    'matrix': ['⠉', '⠘', '⠰', '⠤', '⠆', '⠃', '⠉', '⠘', '⠰', '⠤', '⠆', '⠃'],
    'quantum': ['∙', '●', '∘', '○', '◌', '◎', '◉', '⦿'],
    'bar': ['[⣿⣿⣿⣀⣀⣀]', '[⣿⣿⣀⣀⣀⣀]', '[⣿⣀⣀⣀⣀⣀]', '[⣀⣀⣀⣀⣀⣀]', '[⣿⣀⣀⣀⣀⣀]', '[⣿⣿⣀⣀⣀⣀]', '[⣿⣿⣿⣀⣀⣀]'],
    'crypto': ['₿', 'Ξ', '◎', '₿', 'Ξ', '◎'],
    'node': ['⠧', '⠏', '⠛', '⠹'],
}

def create_progress_bar(progress, width=20, style='standard', color=Colors.GREEN, empty_color=Colors.ENDC):
    """Create a stylized progress bar.
    
    Args:
        progress: Float between 0 and 1 representing progress
        width: Width of the progress bar in characters
        style: Style from PROGRESS_BAR_STYLES
        color: ANSI color code for the filled part
        empty_color: ANSI color code for the empty part
        
    Returns:
        Formatted progress bar string
    """
    if style not in PROGRESS_BAR_STYLES:
        style = 'standard'
        
    # Ensure progress is between 0 and 1
    progress = max(0, min(1, progress))
    
    filled_char, empty_char = PROGRESS_BAR_STYLES[style]
    
    # Calculate how many characters should be filled
    filled_length = int(width * progress)
    
    # Create the bar
    filled_part = color + filled_char * filled_length
    empty_part = empty_color + empty_char * (width - filled_length)
    
    return f"{filled_part}{empty_part}{Colors.ENDC}"

def create_multi_segment_progress_bar(percentages, width=20, colors=None, style='standard'):
    """Create a progress bar with multiple colored segments.
    
    Args:
        percentages: List of values between 0 and 1 for each segment
        width: Width of the progress bar in characters
        colors: List of colors for each segment
        style: Style from PROGRESS_BAR_STYLES
        
    Returns:
        Formatted progress bar string
    """
    if style not in PROGRESS_BAR_STYLES:
        style = 'standard'
        
    filled_char, empty_char = PROGRESS_BAR_STYLES[style]
    
    # Default colors if not provided
    if not colors or len(colors) < len(percentages):
        colors = [Colors.GREEN, Colors.BLUE, Colors.YELLOW, Colors.RED, Colors.PURPLE] * (len(percentages) // 5 + 1)
        colors = colors[:len(percentages)]
    
    # Total progress (should not exceed 1.0)
    total_progress = min(1.0, sum(percentages))
    
    # Calculate character counts for each segment
    segment_lengths = [int(width * p) for p in percentages]
    
    # Adjust to ensure total length is correct (due to rounding)
    total_length = sum(segment_lengths)
    if total_length < int(width * total_progress):
        # Add remaining characters to the first non-zero segment
        for i, p in enumerate(percentages):
            if p > 0:
                segment_lengths[i] += int(width * total_progress) - total_length
                break
    
    # Create segments
    segments = []
    for i, length in enumerate(segment_lengths):
        if length > 0:
            segments.append(f"{colors[i]}{filled_char * length}")
    
    # Calculate empty part
    filled_length = int(width * total_progress)
    empty_part = f"{Colors.ENDC}{empty_char * (width - filled_length)}"
    
    return f"{''.join(segments)}{empty_part}{Colors.ENDC}"

def create_animated_spinner(frame_idx, style='spinner', color=Colors.CYAN):
    """Create an animated spinner for progress indication.
    
    Args:
        frame_idx: Current frame index
        style: Style name from ANIMATED_PROGRESS_FRAMES
        color: ANSI color code
        
    Returns:
        Current frame character of the spinner
    """
    if style not in ANIMATED_PROGRESS_FRAMES:
        style = 'spinner'
        
    frames = ANIMATED_PROGRESS_FRAMES[style]
    return f"{color}{frames[frame_idx % len(frames)]}{Colors.ENDC}"

def create_gradient_progress_bar(progress, width=20, start_color=Colors.GREEN, end_color=Colors.YELLOW):
    """Create a progress bar with gradient color.
    
    Args:
        progress: Float between 0 and 1 representing progress
        width: Width of the progress bar in characters
        start_color: Starting ANSI color
        end_color: Ending ANSI color
        
    Returns:
        Formatted progress bar with gradient
    """
    # This is a simplified version - a true gradient would require 256 color support
    filled_length = int(width * progress)
    half_point = filled_length // 2
    
    # First half with start color, second half with end color
    if filled_length <= 0:
        bar = f"{Colors.ENDC}{'░' * width}"
    elif filled_length >= width:
        bar = f"{end_color}{'█' * width}"
    else:
        first_segment = f"{start_color}{'█' * half_point}"
        second_segment = f"{end_color}{'█' * (filled_length - half_point)}"
        empty_segment = f"{Colors.ENDC}{'░' * (width - filled_length)}"
        bar = f"{first_segment}{second_segment}{empty_segment}"
    
    return f"{bar}{Colors.ENDC}"

def create_completion_bar(value, maximum, width=20, style='quantum', prefix="", suffix="", 
                          show_percent=True, show_values=False, color=Colors.CYAN):
    """Create a full-featured completion bar.
    
    Args:
        value: Current value
        maximum: Maximum value
        width: Width of the progress bar
        style: Bar style to use
        prefix: Text to show before the bar
        suffix: Text to show after the bar
        show_percent: Whether to show percentage
        show_values: Whether to show the actual values
        color: Color for the filled portion
        
    Returns:
        Complete formatted progress bar with labels
    """
    # Calculate progress and create the bar
    try:
        progress = value / maximum if maximum > 0 else 1.0
    except (TypeError, ZeroDivisionError):
        progress = 0.0
        
    bar = create_progress_bar(progress, width, style, color)
    
    # Format percent
    percent = f" {progress*100:.1f}%" if show_percent else ""
    
    # Format values
    values = f" {value}/{maximum}" if show_values else ""
    
    # Combine all parts
    return f"{prefix}{bar}{suffix}{percent}{values}"

def create_fancy_progress_display(title, progress, width=None, style='quantum', color=Colors.CYAN,
                                 show_spinner=True, spinner_style='quantum', elapsed=None, eta=None):
    """Create a fancy progress display with title, bar, spinner, and timing info.
    
    Args:
        title: Title for the progress bar
        progress: Progress value (0-1)
        width: Width of terminal (auto-detected if None)
        style: Bar style
        color: Main color
        show_spinner: Whether to show a spinner
        spinner_style: Style of spinner
        elapsed: Elapsed time in seconds (optional)
        eta: Estimated time remaining in seconds (optional)
        
    Returns:
        Multi-line fancy progress display
    """
    if width is None:
        try:
            width = shutil.get_terminal_size().columns
        except:
            width = 80
    
    # Ensure minimum width
    width = max(40, width)
    
    # Calculate bar width based on terminal width
    bar_width = min(30, width - 25)
    
    # Create progress bar
    progress_bar = create_progress_bar(progress, bar_width, style, color)
    
    # Create spinner if requested
    spinner = ""
    if show_spinner:
        frame_idx = int(time.time() * 10) % len(ANIMATED_PROGRESS_FRAMES[spinner_style])
        spinner = create_animated_spinner(frame_idx, spinner_style, color)
    
    # Format percentage
    percent = f"{progress*100:.1f}%"
    
    # Format time information
    time_info = ""
    if elapsed is not None:
        elapsed_str = format_time_duration(elapsed)
        time_info += f"Elapsed: {elapsed_str}"
    
    if eta is not None:
        eta_str = format_time_duration(eta)
        if time_info:
            time_info += " | "
        time_info += f"ETA: {eta_str}"
    
    # Put it all together
    result = []
    result.append(f"{color}{title}{Colors.ENDC}")
    progress_line = f"{spinner} {progress_bar} {percent}"
    result.append(progress_line)
    
    if time_info:
        result.append(time_info)
    
    return "\n".join(result)

def format_time_duration(seconds):
    """Format seconds into a human-readable duration."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{int(minutes)}m {int(seconds % 60)}s"
    else:
        hours = seconds / 3600
        minutes = (seconds % 3600) / 60
        return f"{int(hours)}h {int(minutes)}m"

def print_progress_bar_demo():
    """Print a demonstration of available progress bar styles."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}🌟 OMEGA QUANTUM PROGRESS BAR STYLES 🌟{Colors.ENDC}\n")
    
    # Show static bar styles
    print(f"{Colors.BOLD}Static Progress Bar Styles:{Colors.ENDC}")
    progress_values = [0.25, 0.5, 0.75, 1.0]
    
    for style, chars in PROGRESS_BAR_STYLES.items():
        demos = []
        for progress in progress_values:
            bar = create_progress_bar(progress, 10, style)
            demos.append(f"{bar} {int(progress*100)}%")
        
        style_name = f"{style.upper()}:"
        print(f"{style_name.ljust(12)} {' '.join(demos)}")
    
    # Show animated spinners
    print(f"\n{Colors.BOLD}Animated Spinner Styles:{Colors.ENDC}")
    for style in ANIMATED_PROGRESS_FRAMES:
        frames = ANIMATED_PROGRESS_FRAMES[style]
        frame_display = ' '.join([f"{Colors.CYAN}{frame}{Colors.ENDC}" for frame in frames])
        style_name = f"{style.upper()}:"
        print(f"{style_name.ljust(12)} {frame_display}")
    
    # Show gradient bar
    print(f"\n{Colors.BOLD}Gradient Progress Bars:{Colors.ENDC}")
    for progress in progress_values:
        bar = create_gradient_progress_bar(progress, 20, Colors.GREEN, Colors.RED)
        print(f"GRADIENT: {bar} {int(progress*100)}%")
    
    # Show multi-segment bar
    print(f"\n{Colors.BOLD}Multi-Segment Progress Bar:{Colors.ENDC}")
    segments = [
        [0.2, 0.3, 0.1],
        [0.1, 0.1, 0.1, 0.2],
        [0.05, 0.15, 0.25, 0.15, 0.1]
    ]
    colors = [
        [Colors.GREEN, Colors.YELLOW, Colors.RED],
        [Colors.GREEN, Colors.YELLOW, Colors.RED, Colors.PURPLE],
        [Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.PURPLE, Colors.RED]
    ]
    
    for i, segs in enumerate(segments):
        bar = create_multi_segment_progress_bar(segs, 20, colors[i])
        print(f"MULTI-SEG: {bar} {sum(segs)*100:.0f}%")
    
    # Show fancy progress display
    print(f"\n{Colors.BOLD}Fancy Progress Display:{Colors.ENDC}")
    fancy = create_fancy_progress_display(
        "MATRIX SYNCHRONIZATION", 0.75, style='matrix', color=Colors.GREEN,
        show_spinner=True, spinner_style='matrix', elapsed=345, eta=115
    )
    print(fancy)
    
    fancy = create_fancy_progress_display(
        "QUANTUM ENTANGLEMENT", 0.42, style='quantum', color=Colors.PURPLE,
        show_spinner=True, spinner_style='quantum', elapsed=67, eta=93
    )
    print(f"\n{fancy}")

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

def beautify_log_header():
    """
    Create a custom, stylized logger that replaces the standard boring timestamp with
    something more cyberpunk and visually appealing.
    
    This configures the root logger to use our custom formatter.
    """
    import logging
    import datetime
    import random
    
    class QuantumLogFormatter(logging.Formatter):
        """Custom log formatter with cyberpunk styling."""
        
        def __init__(self):
            super().__init__()
            self.quantum_header = "0M3G4_B0TS_QA_AUT0_TEST_SUITES_RuNn3R_5D"
            self.last_header_time = 0
            self.header_interval = 60  # Show fancy header once per minute max
            
            # Random cool prefixes for log entries
            self.prefix_options = [
                "QUANTUM",
                "MATRIX",
                "COSMIC",
                "CYBER",
                "NEURAL",
                "DIGITAL",
                "BITCOIN",
                "WAVE",
                "QUBIT",
                "NEXUS"
            ]
            
            # Colors for different log levels
            self.level_colors = {
                logging.DEBUG: Colors.BLUE,
                logging.INFO: Colors.GREEN,
                logging.WARNING: Colors.YELLOW,
                logging.ERROR: Colors.RED,
                logging.CRITICAL: Colors.PURPLE + Colors.BOLD
            }
            
            # Header colors that cycle
            self.header_colors = [
                Colors.CYAN,
                Colors.GREEN,
                Colors.BLUE,
                Colors.PURPLE,
            ]
            self.header_color_idx = 0
        
        def format(self, record):
            # Get the current time
            now = datetime.datetime.now()
            timestamp = now.strftime("%H:%M:%S")
            
            # Get color for the log level
            level_color = self.level_colors.get(record.levelno, Colors.ENDC)
            
            # Choose a random prefix for variety
            prefix = random.choice(self.prefix_options)
            
            # Format log content with colors
            content = f"{level_color}{record.getMessage()}{Colors.ENDC}"
            
            # Decide whether to show fancy header based on time
            current_time = time.time()
            if current_time - self.last_header_time >= self.header_interval:
                # It's time for a fancy header
                self.last_header_time = current_time
                
                # Cycle through header colors
                header_color = self.header_colors[self.header_color_idx]
                self.header_color_idx = (self.header_color_idx + 1) % len(self.header_colors)
                
                # Create fancy divider
                divider = f"{header_color}{'═' * 80}{Colors.ENDC}"
                
                # Create the fancy header with date and the quantum header
                date_str = now.strftime("%Y-%m-%d")
                header = f"{Colors.BOLD}{header_color}┤ {date_str} ⟨ {self.quantum_header} ⟩ {timestamp} ├{Colors.ENDC}"
                
                # Return with fancy header
                return f"\n{divider}\n{header}\n{divider}\n{Colors.CYAN}[{prefix}]{Colors.ENDC} {content}"
            else:
                # Return with simple format
                return f"{Colors.CYAN}[{timestamp} {prefix}]{Colors.ENDC} {content}"
    
    # Apply our custom formatter to the root logger
    root_logger = logging.getLogger()
    
    # Remove any existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create console handler and set formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(QuantumLogFormatter())
    root_logger.addHandler(console_handler)
    
    # Also apply to our specific logger
    quantum_logger = logging.getLogger("0M3G4_B0TS_QA_AUT0_TEST_SUITES_RuNn3R_5D")
    quantum_logger.handlers = []  # Clear existing handlers
    quantum_logger.addHandler(console_handler)
    
    return True

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
    
    # Top border
    top_border = f"┌{'─' * (table_width - 2)}┐"
    
    # Content line with centered title
    title_padding = max(0, (table_width - 2 - len(title)) // 2)
    content_line = f"│{' ' * title_padding}{title}{' ' * (table_width - 2 - len(title) - title_padding)}│"
    
    # Bottom border
    bottom_border = f"└{'─' * (table_width - 2)}┘"
    
    # Validate and fix any table inconsistencies
    fixed_top, [fixed_content], fixed_bottom = ensure_table_consistency(
        top_border, [content_line], bottom_border, table_width
    )
    
    # Print the fixed table
    print(fixed_top)
    print(fixed_content)
    print(fixed_bottom)
    print()

def print_quantum_divider():
    """Print a quantum-themed divider."""
    divider = f"{Colors.PURPLE}{'═' * 80}{Colors.ENDC}"
    logger.info(divider)

def print_enhanced_header(title, subtitle=None):
    """Print an enhanced header with a title and optional subtitle."""
    table_width = 80  # Fixed table width for consistency
    
    print()
    
    # Top border
    top_border = f"╔{'═' * (table_width - 2)}╗"
    
    # Title line with centered text
    title_padding = max(0, (table_width - 2 - len(title)) // 2)
    title_line = f"║{' ' * title_padding}{title}{' ' * (table_width - 2 - len(title) - title_padding)}║"
    
    # Content lines (just title or title+subtitle)
    content_lines = [title_line]
    
    if subtitle:
        # Add subtitle line with centered text
        subtitle_padding = max(0, (table_width - 2 - len(subtitle)) // 2)
        subtitle_line = f"║{' ' * subtitle_padding}{subtitle}{' ' * (table_width - 2 - len(subtitle) - subtitle_padding)}║"
        content_lines.append(subtitle_line)
    
    # Bottom border
    bottom_border = f"╚{'═' * (table_width - 2)}╝"
    
    # Validate and fix any table inconsistencies
    fixed_top, fixed_content, fixed_bottom = ensure_table_consistency(
        top_border, content_lines, bottom_border, table_width
    )
    
    # Print the fixed table
    print(fixed_top)
    for line in fixed_content:
        print(line)
    print(fixed_bottom)
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

def validate_and_fix_table_width(table_str, expected_width):
    """
    Validates a table string and fixes it if the width is incorrect.
    
    Args:
        table_str: The table string to validate
        expected_width: The expected width of the table
        
    Returns:
        Fixed table string
    """
    lines = table_str.strip().split('\n')
    fixed_lines = []
    
    for line in lines:
        # Calculate visible width (excluding ANSI color codes)
        visible_chars = remove_ansi_codes(line)
        current_width = len(visible_chars)
        
        if current_width == expected_width:
            # Line is correct width, keep as is
            fixed_lines.append(line)
        else:
            # Line needs fixing
            if '║' in line or '│' in line:
                # It's a content line, needs padding in the middle
                fixed_line = fix_content_line(line, expected_width)
                fixed_lines.append(fixed_line)
            elif '╔' in line or '╚' in line or '┌' in line or '└' in line:
                # It's a top/bottom border, fix it
                fixed_line = fix_border_line(line, expected_width)
                fixed_lines.append(fixed_line)
            else:
                # Keep other lines as they are
                fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def remove_ansi_codes(text):
    """Remove ANSI color codes from a string to get visible length."""
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def fix_content_line(line, expected_width):
    """Fix a content line to match the expected width."""
    import re
    
    # Extract all ANSI color codes to preserve them
    ansi_codes = []
    ansi_pattern = re.compile(r'(\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~]))')
    for match in ansi_pattern.finditer(line):
        ansi_codes.append((match.start(), match.group(0)))
    
    # Remove ANSI codes to work with visible content
    visible_line = remove_ansi_codes(line)
    current_width = len(visible_line)
    
    # Determine border characters
    if '║' in visible_line:
        left_border, right_border = '║', '║'
    else:
        left_border, right_border = '│', '│'
    
    # Find the position of borders
    left_pos = visible_line.find(left_border)
    right_pos = visible_line.rfind(right_border)
    
    if left_pos == -1 or right_pos == -1 or left_pos == right_pos:
        # Can't determine borders properly, fallback to simple padding
        if current_width < expected_width:
            # Add padding to match expected width
            padding = ' ' * (expected_width - current_width)
            return line + padding
        else:
            # Truncate
            return line[:expected_width]
    
    # Extract content between borders
    content = visible_line[left_pos + 1:right_pos]
    
    # Determine if content contains an alignment hint 
    # (e.g., title is centered, content is left/right aligned)
    alignment = 'center'  # Default
    
    if content.strip() and content.startswith(' ') and content.endswith(' '):
        # Check if spaces are balanced on both sides
        left_spaces = len(content) - len(content.lstrip())
        right_spaces = len(content) - len(content.rstrip())
        
        if abs(left_spaces - right_spaces) <= 1:  # Allow 1 space difference
            alignment = 'center'
        elif left_spaces > right_spaces:
            alignment = 'right'
        else:
            alignment = 'left'
    
    # Calculate required content width
    required_content_width = expected_width - 2  # -2 for the borders
    
    # Adjust content based on alignment
    content_text = content.strip()
    if alignment == 'center':
        padding = (required_content_width - len(content_text)) // 2
        new_content = ' ' * padding + content_text + ' ' * (required_content_width - len(content_text) - padding)
    elif alignment == 'left':
        new_content = content_text + ' ' * (required_content_width - len(content_text))
    else:  # right
        new_content = ' ' * (required_content_width - len(content_text)) + content_text
    
    # Reconstruct the line
    new_visible_line = left_border + new_content + right_border
    
    # Reinsert ANSI codes
    offset = 0
    result = new_visible_line
    for pos, code in sorted(ansi_codes, key=lambda x: x[0]):
        # Adjust position for previously inserted codes
        result = result[:pos + offset] + code + result[pos + offset:]
        offset += len(code)
    
    return result

def fix_border_line(line, expected_width):
    """Fix a border line to match the expected width."""
    # Remove ANSI color codes for processing
    visible_line = remove_ansi_codes(line)
    
    # Determine the border characters
    border_type = None
    for char_set in [('╔', '═', '╗'), ('╚', '═', '╝'), ('┌', '─', '┐'), ('└', '─', '┘')]:
        if char_set[0] in visible_line and char_set[2] in visible_line:
            border_type = char_set
            break
    
    if not border_type:
        # Can't determine border type, return the line unchanged
        return line
    
    left_char, fill_char, right_char = border_type
    
    # Extract ANSI color code if present
    color_code = ""
    reset_code = ""
    
    import re
    color_match = re.search(r'(\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~]))', line)
    reset_match = re.search(r'(\x1B\[0m)', line)
    
    if color_match:
        color_code = color_match.group(0)
    if reset_match:
        reset_code = reset_match.group(0)
    
    # Create the corrected border line
    fixed_line = f"{color_code}{left_char}{fill_char * (expected_width - 2)}{right_char}{reset_code}"
    
    return fixed_line

def ensure_table_consistency(top_border, content_lines, bottom_border, expected_width=80):
    """
    Ensures that a table's borders and content lines are consistent in width.
    
    Args:
        top_border: The top border line of the table
        content_lines: List of content lines in the table
        bottom_border: The bottom border line of the table
        expected_width: The expected width of the table (default: 80)
        
    Returns:
        Tuple of (fixed_top_border, fixed_content_lines, fixed_bottom_border)
    """
    # Fix top border
    fixed_top = fix_border_line(top_border, expected_width)
    
    # Fix content lines
    fixed_content = [fix_content_line(line, expected_width) for line in content_lines]
    
    # Fix bottom border
    fixed_bottom = fix_border_line(bottom_border, expected_width)
    
    return fixed_top, fixed_content, fixed_bottom

def create_table_safe(headers, rows, width=80, style='fancy', colors=None):
    """
    Creates a consistently formatted table with headers and rows.
    Ensures the table maintains proper width regardless of content.
    
    Args:
        headers: List of column headers
        rows: List of rows (each row is a list of column values)
        width: Total width of the table
        style: 'fancy' or 'simple'
        colors: Optional dict mapping column indices to color codes
        
    Returns:
        String representation of the table
    """
    if not headers or not rows:
        return ""
    
    num_cols = len(headers)
    
    # Calculate column widths
    total_borders = num_cols + 1  # Number of vertical borders
    total_spacing = num_cols * 2   # Two spaces per column for padding
    available_width = width - total_borders - total_spacing
    
    # Default equal column widths
    col_widths = [available_width // num_cols] * num_cols
    
    # Distribute remaining width to columns
    remaining = available_width - sum(col_widths)
    for i in range(remaining):
        col_widths[i % num_cols] += 1
    
    # Characters for different table styles
    if style == 'fancy':
        top_left = '╔'
        top_right = '╗'
        bottom_left = '╚'
        bottom_right = '╝'
        horizontal = '═'
        vertical = '║'
        top_separator = '╦'
        bottom_separator = '╩'
        cross = '╬'
        left_separator = '╠'
        right_separator = '╣'
        row_separator = '═'
    else:  # simple
        top_left = '┌'
        top_right = '┐'
        bottom_left = '└'
        bottom_right = '┘'
        horizontal = '─'
        vertical = '│'
        top_separator = '┬'
        bottom_separator = '┴'
        cross = '┼'
        left_separator = '├'
        right_separator = '┤'
        row_separator = '─'
    
    # Build the table
    result = []
    
    # Top border
    top_border = top_left
    for i, w in enumerate(col_widths):
        top_border += horizontal * (w + 2)  # +2 for padding
        if i < num_cols - 1:
            top_border += top_separator
    top_border += top_right
    result.append(top_border)
    
    # Header row
    header_line = vertical
    for i, (header, width) in enumerate(zip(headers, col_widths)):
        # Truncate header if too long
        if len(header) > width:
            display_header = header[:width-1] + '…'
        else:
            display_header = header
        
        # Center the header
        padding = width - len(display_header)
        left_pad = padding // 2
        right_pad = padding - left_pad
        
        # Apply color if specified
        if colors and i in colors:
            color_code = colors[i]
            reset_code = Colors.ENDC
            header_line += f" {color_code}{' ' * left_pad}{display_header}{' ' * right_pad}{reset_code} "
        else:
            header_line += f" {' ' * left_pad}{display_header}{' ' * right_pad} "
        
        header_line += vertical
    result.append(header_line)
    
    # Separator after header
    separator = left_separator
    for i, w in enumerate(col_widths):
        separator += row_separator * (w + 2)  # +2 for padding
        if i < num_cols - 1:
            separator += cross
    separator += right_separator
    result.append(separator)
    
    # Data rows
    for row in rows:
        row_line = vertical
        for i, (cell, width) in enumerate(zip(row, col_widths)):
            # Convert cell to string
            cell_str = str(cell)
            
            # Check if the cell contains ANSI color codes
            has_ansi = "\033[" in cell_str or "\x1b[" in cell_str
            
            if has_ansi:
                # For cells with ANSI codes, we need to get the visible length
                visible_text = remove_ansi_codes(cell_str)
                visible_len = len(visible_text)
                
                # Truncate the visible text if needed
                if visible_len > width:
                    # Extract ANSI codes
                    import re
                    ansi_pattern = re.compile(r'(\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~]))')
                    
                    # Find all ANSI codes and their positions
                    ansi_codes = [(m.start(), m.group(0)) for m in ansi_pattern.finditer(cell_str)]
                    
                    # Find the position in the original string that corresponds to 
                    # width-1 visible characters
                    visible_pos = 0
                    actual_pos = 0
                    
                    while visible_pos < width - 1 and actual_pos < len(cell_str):
                        # Check if current position is part of an ANSI code
                        is_ansi = False
                        for code_start, _ in ansi_codes:
                            if actual_pos == code_start:
                                # Skip this ANSI code
                                code_match = ansi_pattern.search(cell_str[actual_pos:])
                                if code_match:
                                    actual_pos += len(code_match.group(0))
                                    is_ansi = True
                                    break
                        
                        if not is_ansi:
                            # Regular character
                            visible_pos += 1
                            actual_pos += 1
                    
                    # Add ellipsis and ensure ANSI reset if needed
                    truncated = cell_str[:actual_pos] + '…'
                    if '\033[' in truncated and not truncated.endswith(Colors.ENDC):
                        truncated += Colors.ENDC
                    
                    display_cell = truncated
                else:
                    display_cell = cell_str
            else:
                # No ANSI codes, simple truncation
                if len(cell_str) > width:
                    display_cell = cell_str[:width-1] + '…'
                else:
                    display_cell = cell_str
            
            # Calculate the visible length for padding
            visible_length = len(remove_ansi_codes(display_cell))
            padding = width - visible_length
            
            # Apply color if specified and not already colored
            if colors and i in colors and not has_ansi:
                color_code = colors[i]
                reset_code = Colors.ENDC
                row_line += f" {color_code}{display_cell}{' ' * padding}{reset_code} "
            else:
                row_line += f" {display_cell}{' ' * padding} "
            
            row_line += vertical
        result.append(row_line)
    
    # Bottom border
    bottom_border = bottom_left
    for i, w in enumerate(col_widths):
        bottom_border += horizontal * (w + 2)  # +2 for padding
        if i < num_cols - 1:
            bottom_border += bottom_separator
    bottom_border += bottom_right
    result.append(bottom_border)
    
    return '\n'.join(result) 