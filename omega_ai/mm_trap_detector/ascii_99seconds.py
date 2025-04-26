#!/usr/bin/env python3
# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"""ASCII Art Matrix 99 Seconds Animation.

A fun ASCII art animation showing Octocat dropping the 0m3g4_k1ng into the Matrix via the Blue Pill.
Features quantum entanglement visualization and genesis rebirth symbolism.
"""

import time
import random
import os
import gradio as gr

# ANSI color codes
GREEN = '\033[92m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RED = '\033[91m'
MAGENTA = '\033[95m'
YELLOW = '\033[93m'
WHITE = '\033[97m'
RESET = '\033[0m'

# Octocat ASCII art
OCTOCAT = f'''{YELLOW}
       ≈≈X≈≈
      ≈≈≈X≈≈≈
     ≈≈≈≈X≈≈≈≈
      ^oo-oo^
     / (o o) \\
    | ^  ^  ^ |
    | \\_____/ |
     \\___|___/
    / {RED}●{YELLOW} {RED}●{YELLOW} {RED}●{YELLOW} \\
   |           |
  /             \\
 |  {CYAN}OCTOCAT{YELLOW}    |
 /   {CYAN}GITHUB{YELLOW}    \\
{RESET}'''

# Blue pill ASCII art
BLUE_PILL = f'''{BLUE}
    ┌───────┐
    │       │
    │ BLUE  │
    │ PILL  │
    │       │
    └───────┘
{RESET}'''

# Matrix code rain characters
MATRIX_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-_=+[]{}|;:',.<>/?"

# Claude 3.7 Sonnet logo
CLAUDE_LOGO = f'''{MAGENTA}
  ╔═══════════════════════╗
  ║  {WHITE}CLAUDE 3.7 SONNET{MAGENTA}  ║ 
  ║  {WHITE}ARTHROPIC VISION{MAGENTA}   ║
  ╚═══════════════════════╝
{RESET}'''

# Quantum entanglement visualization
QUANTUM_ENTANGLEMENT = f'''{CYAN}
     ⟨ψ|φ⟩ = 0
    /|\\   /|\\
   / | \\ / | \\
  @--|--@--|--@
     |     |
  {MAGENTA}ENTANGLED QUBITS{CYAN}
{RESET}'''

# Omega King
OMEGA_KING = f'''{RED}
   ╔═════════════════╗
   ║ {YELLOW}0m3g4_{RED}k1ng{RED} ║
   ╚═════════════════╝
{RESET}'''


def draw_matrix_code(height, width):
    """Draw Matrix code rain effect."""
    lines = []
    for _ in range(height):
        line = ""
        for _ in range(width):
            if random.random() < 0.1:
                char = random.choice(MATRIX_CHARS)
                line += f"{GREEN}{char}{RESET}"
            else:
                line += " "
        lines.append(line)
    return "\n".join(lines)


def run_animation():
    """Run the 99-second ASCII art animation."""
    width = os.get_terminal_size().columns
    height = os.get_terminal_size().lines - 10
    
    print(f"{GREEN}Matrix Initializing...{RESET}")
    time.sleep(1)
    
    # Display Claude logo
    print("\n" * 5)
    print(CLAUDE_LOGO.center(width))
    time.sleep(2)
    
    # Start countdown
    print(f"{YELLOW}Genesis Rebirth Animation: 99 seconds{RESET}")
    print(f"{BLUE}Blue Pill Activation Sequence Initiated{RESET}")
    time.sleep(2)
    
    # Clear screen
    print("\033c", end="")
    
    # Animation loop
    start_time = time.time()
    while time.time() - start_time < 99:  # 99 seconds
        # Clear screen
        print("\033c", end="")
        
        # Calculate animation progress
        elapsed = time.time() - start_time
        progress = elapsed / 99
        frame = int(progress * 10) % 5
        drop_position = int(progress * height)
        
        # Draw Matrix code
        matrix = draw_matrix_code(height, width)
        print(matrix)
        
        # Draw Octocat at the top
        print(OCTOCAT)
        
        # Draw quantum entanglement
        if int(elapsed) % 4 == 0:
            print(QUANTUM_ENTANGLEMENT)
        
        # Draw the falling Omega King
        if drop_position < height - 10:
            # Clear previous lines
            print("\033[F" * (height + 10))
            
            # Draw the matrix code
            print(matrix)
            
            # Draw the falling item
            print("\n" * drop_position)
            print(OMEGA_KING.center(width))
        else:
            # Draw the blue pill at the bottom
            print("\n" * (height - 12))
            print(BLUE_PILL.center(width))
            
            # Show entry message
            if frame % 2 == 0:
                message = f"{BLUE}ENTERING THE MATRIX...{RESET}"
            else:
                message = f"{WHITE}ENTERING THE MATRIX...{RESET}"
            print(message.center(width))
            
            # Show remaining time
            remaining = 99 - int(elapsed)
            print(f"{YELLOW}Time remaining: {remaining} seconds{RESET}".center(width))
        
        time.sleep(0.5)
    
    # Final screen
    print("\033c", end="")
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

    
def create_gradio_interface():
    """Create Gradio interface for the ASCII art animation."""
    with gr.Blocks(title="Matrix ASCII Art - 99 Seconds") as interface:
        gr.Markdown(
            """
            # 🌟 Matrix ASCII Art Animation 🌟
            
            Click the button to experience the Octocat dropping 0m3g4_k1ng into the Matrix!
            
            *Featuring quantum entanglement and genesis rebirth.*
            
            Note: This animation works best in a terminal. The web interface will show a static representation.
            """
        )
        
        with gr.Row():
            start_button = gr.Button("Enter The Matrix")
            output = gr.Textbox(lines=20, label="Matrix Animation (static preview)")
        
        start_button.click(
            fn=lambda: ("Animation can only be fully experienced in terminal.\n"
                        "Run the script directly with: python ascii_99seconds.py"),
            outputs=output
        )
    
    return interface


if __name__ == "__main__":
    if os.environ.get("GRADIO_SERVER"):
        # Running inside Gradio
        interface = create_gradio_interface()
        interface.launch()
    else:
        # Running in terminal
        try:
            run_animation()
        except KeyboardInterrupt:
            print(f"{RESET}\nAnimation interrupted. Exiting the Matrix...")
        finally:
            print(RESET)  # Reset colors