#!/usr/bin/env python3
"""
TKWW CLI Slideshow Demo with tmux
================================

A beautiful CLI slideshow presentation for The Knot Worldwide.
Uses tmux for multi-pane presentation and rich for formatting.
"""

import time
import typer
import sys
import os
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, TaskID
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from rich import box
from typing import List, Dict, Optional
import asyncio
from pathlib import Path

# Platform-specific imports for key input handling
_msvcrt = None
_termios = None
_tty = None

if os.name == 'nt':  # Windows
    try:
        import msvcrt as _msvcrt
    except ImportError:
        pass
else:  # Unix-like
    try:
        import termios as _termios
        import tty as _tty
    except ImportError:
        pass

console = Console()

# Slide content
SLIDES = [
    {
        "title": "✨ Welcome to TKWW QA AI Demo ✨",
        "content": """
        # The Knot Worldwide QA AI Integration
        
        ## Powered by OMEGA BTC AI
        
        *"Where divine code meets wedding planning excellence"*
        """,
        "duration": 3
    },
    {
        "title": "🎯 Key Features",
        "content": """
        - Automated Test Generation
        - AI-Powered Test Execution
        - Real-time Metrics Dashboard
        - Multi-persona Testing
        - Quantum-Resistant Security
        - Divine Code Blessing
        """,
        "duration": 4
    },
    {
        "title": "🤖 AI Personas",
        "content": """
        ## Our Divine Testing Personas
        
        - **Architect**: System design validation
        - **Explorer**: Edge case discovery
        - **Guardian**: Security testing
        - **Artist**: UI/UX validation
        - **Sage**: Performance optimization
        """,
        "duration": 4
    },
    {
        "title": "📊 Metrics & Analytics",
        "content": """
        ## Real-time Quality Metrics
        
        - Test Coverage: 98.7%
        - Defect Detection: 99.2%
        - Performance Score: 9.8/10
        - Security Rating: A+
        - User Satisfaction: 9.9/10
        """,
        "duration": 4
    },
    {
        "title": "🔮 Future Vision",
        "content": """
        ## The Next Evolution
        
        - Quantum Computing Integration
        - Blockchain Test Verification
        - AI-Powered Bug Prediction
        - Automated Documentation
        - Divine Code Blessing 2.0
        """,
        "duration": 4
    },
    {
        "title": "🌸 Thank You",
        "content": """
        # Thank You for Watching!
        
        ## Contact Us
        
        - Email: divine@omega-btc-ai.com
        - Website: https://omega-btc-ai.com
        - GitHub: https://github.com/omega-btc-ai
        
        *"May your code be blessed with divine quality"*
        """,
        "duration": 5
    }
]

def get_key():
    """Get a single keypress from the user."""
    if os.name == 'nt':  # Windows
        if _msvcrt:
            if _msvcrt.kbhit():
                key = _msvcrt.getch()
                try:
                    if key in [b'\xe0']:  # Arrow key prefix
                        key = _msvcrt.getch()
                        if key == b'H':  # Up arrow
                            return 'up'
                        elif key == b'P':  # Down arrow
                            return 'down'
                        elif key == b'K':  # Left arrow
                            return 'left'
                        elif key == b'M':  # Right arrow
                            return 'right'
                    return key.decode('utf-8')
                except:
                    return None
        else:
            console.print("[red]Warning: msvcrt module not available[/red]")
            return None
        return None
    else:  # Unix-like
        if _termios and _tty:
            try:
                fd = sys.stdin.fileno()
                old_settings = _termios.tcgetattr(fd)
                try:
                    _tty.setraw(sys.stdin.fileno())
                    ch = sys.stdin.read(1)
                    if ch == '\x1b':
                        ch = sys.stdin.read(1)
                        if ch == '[':
                            ch = sys.stdin.read(1)
                            if ch == 'A':  # Up arrow
                                return 'up'
                            elif ch == 'B':  # Down arrow
                                return 'down'
                            elif ch == 'D':  # Left arrow
                                return 'left'
                            elif ch == 'C':  # Right arrow
                                return 'right'
                    return ch
                finally:
                    _termios.tcsetattr(fd, _termios.TCSADRAIN, old_settings)
            except _termios.error:
                console.print("[red]Warning: Failed to configure terminal[/red]")
                return None
        else:
            console.print("[red]Warning: termios/tty modules not available[/red]")
            return None

def setup_tmux_session():
    """Set up a new tmux session for the presentation."""
    session_name = "tkww-demo"
    
    # Check if session exists
    result = subprocess.run(["tmux", "has-session", "-t", session_name], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        # Session exists, kill it
        subprocess.run(["tmux", "kill-session", "-t", session_name])
    
    # Create new session
    subprocess.run(["tmux", "new-session", "-d", "-s", session_name])
    
    # Split window into three panes
    subprocess.run(["tmux", "split-window", "-h", "-t", session_name])
    subprocess.run(["tmux", "split-window", "-v", "-t", session_name])
    
    # Set up pane 0 (main content)
    subprocess.run(["tmux", "select-pane", "-t", "0"])
    subprocess.run(["tmux", "send-keys", "-t", session_name, "clear", "C-m"])
    
    # Set up pane 1 (notes)
    subprocess.run(["tmux", "select-pane", "-t", "1"])
    subprocess.run(["tmux", "send-keys", "-t", session_name, "clear", "C-m"])
    
    # Set up pane 2 (controls)
    subprocess.run(["tmux", "select-pane", "-t", "2"])
    subprocess.run(["tmux", "send-keys", "-t", session_name, "clear", "C-m"])
    
    # Print instructions for the user
    console.print("\n[green]Tmux session created![/green]")
    console.print("\nTo view the presentation:")
    console.print("1. Open a new terminal window")
    console.print("2. Run: [blue]tmux attach-session -t tkww-demo[/blue]")
    console.print("\nControls:")
    console.print("- Use ←/→ or h/l to navigate slides")
    console.print("- Space to pause/resume")
    console.print("- q to quit")
    console.print("\nPress Ctrl+C in this window to end the presentation\n")
    
    return session_name

def create_slide_layout(slide):
    """Create a layout for a slide with title and content."""
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="content", size=15),
        Layout(name="footer", size=3)
    )
    
    # Calculate optimal width based on content
    content_lines = slide["content"].strip().split('\n')
    max_line_length = max(len(line.strip()) for line in content_lines)
    optimal_width = min(max_line_length + 8, 100)  # Add padding, cap at 100
    
    # Create a centered frame with dynamic width
    frame = Panel(
        Text.from_markup(slide["content"], justify="center"),
        title=slide["title"],
        border_style="bright_white",
        width=optimal_width,
        padding=(1, 2),
        box=box.ROUNDED
    )
    
    # Center the content in the main area
    layout["content"].update(frame)
    
    # Center the footer text
    layout["footer"].update(
        Text.from_markup("Use ←/→ or h/l to navigate • Space to pause • q to quit", justify="center", style="dim")
    )
    
    return layout

class SlideshowState:
    def __init__(self):
        self.current_slide: int = 0
        self.is_paused: bool = False
        self.should_exit: bool = False
        self.progress: int = 0
        self.progress_task: Optional[TaskID] = None
        self.progress_bar: Optional[Progress] = None

async def play_slideshow(show_progress: bool = True):
    """Play the slideshow with interactive controls."""
    state = SlideshowState()
    session_name = setup_tmux_session()
    
    try:
        while not state.should_exit and state.current_slide < len(SLIDES):
            slide = SLIDES[state.current_slide]
            layout = create_slide_layout(slide)
            
            # Update main content pane
            subprocess.run(["tmux", "select-pane", "-t", "0"])
            subprocess.run(["tmux", "send-keys", "-t", session_name, "clear", "C-m"])
            subprocess.run(["tmux", "send-keys", "-t", session_name, str(layout), "C-m"])
            
            # Update notes pane
            subprocess.run(["tmux", "select-pane", "-t", "1"])
            subprocess.run(["tmux", "send-keys", "-t", session_name, "clear", "C-m"])
            subprocess.run(["tmux", "send-keys", "-t", session_name, 
                          f"Notes for Slide {state.current_slide + 1}/{len(SLIDES)}", "C-m"])
            
            # Update controls pane
            subprocess.run(["tmux", "select-pane", "-t", "2"])
            subprocess.run(["tmux", "send-keys", "-t", session_name, "clear", "C-m"])
            subprocess.run(["tmux", "send-keys", "-t", session_name, 
                          "Controls:\n←/→ or h/l: Navigate\nSpace: Pause/Resume\nq: Quit", "C-m"])
            
            start_time = time.time()
            while (time.time() - start_time < slide["duration"]) and not state.should_exit:
                if not state.is_paused:
                    elapsed = time.time() - start_time
                    if show_progress and state.progress_bar and state.progress_task is not None:
                        state.progress_bar.update(state.progress_task, completed=elapsed)
                
                # Check for key input
                key = get_key()
                if key:
                    if key in ['q', 'Q', '\x03']:  # 'q', 'Q' or Ctrl+C
                        state.should_exit = True
                        break
                    elif key == ' ':
                        state.is_paused = not state.is_paused
                    elif key in ['left', 'h']:  # Left arrow or 'h'
                        state.current_slide = max(0, state.current_slide - 1)
                        break
                    elif key in ['right', 'l']:  # Right arrow or 'l'
                        state.current_slide = min(len(SLIDES) - 1, state.current_slide + 1)
                        break
                
                await asyncio.sleep(0.1)  # Small delay to prevent high CPU usage
            
            if not state.should_exit:
                state.current_slide += 1
    
    finally:
        # Clean up tmux session
        subprocess.run(["tmux", "kill-session", "-t", session_name])

def main():
    """Main entry point for the demo script."""
    try:
        asyncio.run(play_slideshow())
    except KeyboardInterrupt:
        console.print("\n[red]Demo interrupted by user[/red]")
        # Clean up tmux session
        subprocess.run(["tmux", "kill-session", "-t", "tkww-demo"])
    except Exception as e:
        console.print(f"\n[red]Error running demo: {e}[/red]")
        # Clean up tmux session
        subprocess.run(["tmux", "kill-session", "-t", "tkww-demo"])

if __name__ == "__main__":
    main() 