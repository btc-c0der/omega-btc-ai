#!/usr/bin/env python3
"""
ZOROBABEL K1L1 - Divine Celebration
----------------------------------
A sacred celebration animation to commemorate successful pip installation.

🌀 MODULE: Divine Celebration
🧭 CONSCIOUSNESS LEVEL: 7 - Wisdom
"""

import os
import sys
import time
import random
import argparse
from pathlib import Path
import threading
import shutil

# ANSI colors for divine manifestation
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[35m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def rainbow(text):
        """Apply rainbow colors to text."""
        colors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.MAGENTA]
        colored_chars = []
        for i, char in enumerate(text):
            if char.strip():
                colored_chars.append(colors[i % len(colors)] + char + Colors.RESET)
            else:
                colored_chars.append(char)
        return ''.join(colored_chars)
    
    @staticmethod
    def random_color():
        """Get a random color."""
        colors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.MAGENTA]
        return random.choice(colors)


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


class ZorobabelDancer:
    """Divine dancer animation for celebration."""
    
    def __init__(self):
        """Initialize the dancer."""
        self.frames = [
            # Dancing frame 1
            """
                    \\ O /
                      |
                     / \\
            """,
            # Dancing frame 2
            """
                    _ O _
                      |
                     / \\
            """,
            # Dancing frame 3
            """
                     \\ O /
                       |
                      / \\
            """,
            # Dancing frame 4
            """
                     _ O _
                       |
                     /   \\
            """,
            # Dancing frame 5 - spiral move
            """
                      O ~ 
                     /|\\
                     / \\
            """,
            # Dancing frame 6 - spiral move
            """
                     ~ O  
                      /|\\
                     / \\
            """,
        ]
        
        self.crown_frames = [
            "  ⬡  ", 
            " ⬡⬡⬡ ",
            "⬡⬡⬡⬡⬡",
        ]
        
        self.spiral_frames = [
            "  🌀   ", 
            " 🌀🌀  ", 
            "🌀🌀🌀 "
        ]
        
        self.mountains = [
            "      /\\     /\\      ",
            "     /  \\   /  \\     ",
            "    /    \\_/    \\    ",
            "   /             \\   ",
            "__/_______________\\__",
        ]
        
        self.frame_index = 0
        self.crown_index = 0
        self.spiral_index = 0
        
    def get_current_frame(self, with_colors=True):
        """Get the current animation frame."""
        frame = self.frames[self.frame_index]
        
        # Add crown
        crown = self.crown_frames[self.crown_index]
        
        # Add spirals
        spiral = self.spiral_frames[self.spiral_index]
        
        # Construct the scene with mountains
        scene = []
        scene.append("")
        
        # Add the crown above dancer
        scene.append(" " * 10 + crown)
        
        # Add the dancer
        scene.extend(frame.split('\n'))
        
        # Add some space
        scene.append("")
        scene.append("")
        
        # Add spirals around mountains
        scene.append(spiral + " " * 10 + spiral)
        
        # Add mountains (Ngorongoro-Kilimanjaro)
        scene.extend(self.mountains)
        
        # Colorize
        if with_colors:
            colored_scene = []
            for i, line in enumerate(scene):
                if i == 1:  # Crown
                    colored_scene.append(Colors.YELLOW + line + Colors.RESET)
                elif i < 6:  # Dancer
                    colored_scene.append(Colors.CYAN + line + Colors.RESET)
                elif i < 8:  # Space
                    colored_scene.append(line)
                elif i == 8:  # Spirals
                    colored_scene.append(Colors.MAGENTA + line + Colors.RESET)
                else:  # Mountains
                    colored_scene.append(Colors.GREEN + line + Colors.RESET)
            
            return '\n'.join(colored_scene)
        
        return '\n'.join(scene)
    
    def next_frame(self):
        """Advance to the next animation frame."""
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.crown_index = (self.crown_index + 1) % len(self.crown_frames)
        self.spiral_index = (self.spiral_index + 1) % len(self.spiral_frames)


class MessageScroller:
    """Scrolls celebration messages."""
    
    def __init__(self, messages):
        """Initialize with celebration messages."""
        self.messages = messages
        self.message_index = 0
        self.char_position = 0
        self.terminal_width = shutil.get_terminal_size().columns
        
    def get_current_text(self):
        """Get the current scrolling text frame."""
        message = self.messages[self.message_index]
        
        if self.char_position > len(message) + self.terminal_width:
            # Reset for next message
            self.char_position = -self.terminal_width
            self.message_index = (self.message_index + 1) % len(self.messages)
            message = self.messages[self.message_index]
        
        # Calculate the visible portion
        start = max(0, self.char_position)
        end = min(len(message), self.char_position + self.terminal_width)
        
        visible_text = message[start:end]
        
        # Pad with spaces to fill the terminal width
        if self.char_position < 0:
            # Message entering from right
            padding = self.terminal_width + self.char_position
            visible_text = " " * padding + message[:min(-self.char_position, len(message))]
        elif self.char_position > len(message):
            # Message exiting to left
            visible_text = message[self.char_position:] + " " * (self.terminal_width - (len(message) - self.char_position))
        else:
            # Message partially visible
            visible_text = message[self.char_position:self.char_position + self.terminal_width]
            
        # Pad to terminal width
        visible_text = visible_text.ljust(self.terminal_width)
        
        # Apply rainbow coloring
        return Colors.rainbow(visible_text)
    
    def advance(self):
        """Advance the scrolling position."""
        self.char_position += 2


def music_player():
    """Simulate music notes output."""
    notes = ['♩', '♪', '♫', '♬', '♭', '♮', '♯']
    
    while True:
        note = random.choice(notes)
        color = Colors.random_color()
        print(f"{color}{note}{Colors.RESET}", end='', flush=True)
        time.sleep(0.5)


def main():
    """Main celebration script."""
    parser = argparse.ArgumentParser(description="ZOROBABEL K1L1 - Divine Celebration")
    parser.add_argument("--no-color", action="store_true", help="Disable colors")
    args = parser.parse_args()
    
    # Create the dancer
    dancer = ZorobabelDancer()
    
    # Create the message scroller
    messages = [
        "✨ PIP INSTALL MY PACKAGES: why 0 0-n3 t0lD mE ? th34T B3F0RE ???? ✨",
        "🌀 ZOROBABEL K1L1 SYSTEM SUCCESSFULLY INSTALLED 🌀",
        "🔱 THE SACRED SPIRAL GRID HAS BEEN AWAKENED 🔱",
        "👑 KING ZOROBABEL DANCES OVER NGORONGORO-KILIMANJARO 👑",
        "🧬 DIVINE INSTALLATION COMPLETE - GBU2 LICENSE ACTIVATED 🧬",
        "🌸 WE BLOOM NOW AS ONE 🌸",
        "JAH JAH BLESS — SPIRAL GRID ACTIVATION COMPLETE",
    ]
    scroller = MessageScroller(messages)
    
    # Start music thread
    # music_thread = threading.Thread(target=music_player, daemon=True)
    # music_thread.start()
    
    try:
        # Play the animation
        for _ in range(500):  # Animation frames
            clear_screen()
            
            # Print the scrolling message at the top
            print(scroller.get_current_text())
            print()
            
            # Print the dancer and scene
            print(dancer.get_current_frame(not args.no_color))
            
            # Print another scrolling message at the bottom
            print()
            print(scroller.get_current_text())
            
            # Advance the animation
            dancer.next_frame()
            scroller.advance()
            
            # Control animation speed
            time.sleep(0.2)
    
    except KeyboardInterrupt:
        # Exit gracefully on Ctrl+C
        clear_screen()
        print(f"{Colors.GREEN}🌸 DIVINE CELEBRATION CONCLUDED 🌸{Colors.RESET}")


if __name__ == "__main__":
    main() 