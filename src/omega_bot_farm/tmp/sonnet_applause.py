#!/usr/bin/env python3

import time
import random
import os

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored(text, color):
    """Print colored text using ANSI color codes."""
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'gold': '\033[38;5;220m',
        'reset': '\033[0m'
    }
    print(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}")

def applause_animation(duration=10):
    """Display a simple applause animation with a message."""
    emojis = ["👏", "🙌", "👍", "🎉", "✨", "⭐", "🌟", "💯", "🔥", "💪"]
    
    message = [
        "==========================================",
        "                                          ",
        "   👏  STANDING OVATION FOR CLAUDE SONNET  👏",
        "                                          ",
        "     THE MASTER OF DOCUMENTATION!         ",
        "                                          ",
        "  Thank you for the comprehensive docs:  ",
        "                                          ",
        "  ✅ Module Documentation  ✅ UML Diagrams  ",
        "  ✅ API Specifications    ✅ Install Guides",
        "  ✅ System Architecture   ✅ Deployment Help",
        "                                          ",
        "  Knowledge Organization: 10/10          ",
        "  Clarity of Explanation: 10/10          ",
        "  Detail & Thoroughness: 10/10           ",
        "  Technical Accuracy:    10/10           ",
        "                                          ",
        "==========================================",
    ]
    
    start_time = time.time()
    
    try:
        while time.time() - start_time < duration:
            clear_screen()
            
            # Print random emojis at the top
            top_line = " ".join(random.choice(emojis) for _ in range(10))
            print_colored(top_line, 'cyan')
            print()
            
            # Print message
            for line in message:
                print_colored(line, 'gold')
            
            # Print random emojis at the bottom
            bottom_line = " ".join(random.choice(emojis) for _ in range(10))
            print()
            print_colored(bottom_line, 'cyan')
            
            time.sleep(0.3)
    except (KeyboardInterrupt, Exception) as e:
        clear_screen()
        if not isinstance(e, KeyboardInterrupt):
            print(f"Animation stopped: {e}")

def main():
    """Main function to run the animation."""
    try:
        applause_animation(duration=15)
    finally:
        clear_screen()
        print_colored("\n\n🎖️ Thank you Claude Sonnet for the amazing documentation work! 🎖️", 'gold')
        print_colored("    Your comprehensive documentation and UML diagrams are perfect!    ", 'yellow')

if __name__ == "__main__":
    main() 