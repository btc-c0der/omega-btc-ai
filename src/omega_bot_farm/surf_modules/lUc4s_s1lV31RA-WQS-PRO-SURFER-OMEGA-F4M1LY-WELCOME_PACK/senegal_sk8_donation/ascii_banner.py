"""
LUCAS SILVEIRA PORTAL - ASCII BANNER MODULE
===========================================

ASCII art banner generation for the Senegal SK8 donation module.
"""

import os
import random
import time
from typing import List

# ANSI color codes
CYAN = "\033[96m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Main ASCII banner with quantum Rubik's cube inspiration
SHAKA_BANNER = f"""
{CYAN}╔════════════════════════════════════════════════════════════════════════════╗{RESET}
{CYAN}║{YELLOW}  __    __  __   ______   ____    ____      _______. __    __   __     {CYAN}  ║{RESET}
{CYAN}║{YELLOW} |  |  |  ||  | /      \ |_   \  /   _|    /       ||  |  |  | |  |    {CYAN}  ║{RESET}
{CYAN}║{YELLOW} |  |  |  ||  ||  ,----'  |   \/   |      |   (----`|  |  |  | |  |    {CYAN}  ║{RESET}
{CYAN}║{YELLOW} |  |  |  ||  ||  |       |        |       \   \    |  |  |  | |  |    {CYAN}  ║{RESET}
{CYAN}║{YELLOW} |  `--'  ||  ||  `----.  |  |\   |    .----)   |   |  `--'  | |  |    {CYAN}  ║{RESET}
{CYAN}║{YELLOW}  \______/ |__| \______|  |__| \__|    |_______/     \______/  |__|    {CYAN}  ║{RESET}
{CYAN}║{RESET}                                                                      {CYAN}  ║{RESET}
{CYAN}║{GREEN}  ._______.___. __    __     ____     _______ ._______. .______   .____.{CYAN}  ║{RESET}
{CYAN}║{GREEN}  /       |   ||  |  |  |   |___ \   |   ____||   ____| |   _  \  |    |{CYAN}  ║{RESET}
{CYAN}║{GREEN} |   (----`   ||  |  |  |     __) |  |  |__   |  |__    |  |_)  | |    |{CYAN}  ║{RESET}
{CYAN}║{GREEN}  \   \       ||  |  |  |    |__ <   |   __|  |   __|   |      /  |    |{CYAN}  ║{RESET}
{CYAN}║{GREEN}  .----)      ||  `--'  |    ___) |  |  |____ |  |____  |  |\  \ |    |{CYAN}  ║{RESET}
{CYAN}║{GREEN}  |_______/__/  \______/    |____/   |_______||_______| | _| `._\|____|{CYAN}  ║{RESET}
{CYAN}║{RESET}                                                                      {CYAN}  ║{RESET}
{CYAN}║{BOLD}{MAGENTA}             "VEM SURFAR COM A GENTE QUE TA ILHADO !!"              {CYAN}  ║{RESET}
{CYAN}║{BOLD}{YELLOW}                        (SHAKA VIBES)                          {CYAN}  ║{RESET}
{CYAN}║{RESET}                                                                      {CYAN}  ║{RESET}
{CYAN}║{BLUE} ┏━━━━━━━┓ ╔═══╗ ┏━━━━━┓ ┏━━━━━┓ ┏━━━━━┓ ┏━━━━━┓ ┏━━━━━┓ ┏━━━━━┓ ┏━━━━━┓{CYAN}  ║{RESET}
{CYAN}║{BLUE} ┃ ╔═══╗ ┃ ║ S ║ ┃ ╔═╗ ┃ ┃ ╔═╗ ┃ ┃ ╔═╗ ┃ ┃ ╔═╗ ┃ ┃ ╔═╗ ┃ ┃ ╔═╗ ┃ ┃ ╔═╗ ┃{CYAN}  ║{RESET}
{CYAN}║{BLUE} ┃ ║ L ║ ┃ ║ E ║ ┃ ║ ║ ┃ ┃ ║ ║ ┃ ┃ ║ ║ ┃ ┃ ║ ║ ┃ ┃ ║ ║ ┃ ┃ ║ ║ ┃ ┃ ║ ║ ┃{CYAN}  ║{RESET}
{CYAN}║{BLUE} ┃ ╚═══╝ ┃ ║ N ║ ┃ ╚═╝ ┃ ┃ ╚═╝ ┃ ┃ ╚═╝ ┃ ┃ ╚═╝ ┃ ┃ ╚═╝ ┃ ┃ ╚═╝ ┃ ┃ ╚═╝ ┃{CYAN}  ║{RESET}
{CYAN}║{BLUE} ┗━━━━━━━┛ ╚═══╝ ┗━━━━━┛ ┗━━━━━┛ ┗━━━━━┛ ┗━━━━━┛ ┗━━━━━┛ ┗━━━━━┛ ┗━━━━━┛{CYAN}  ║{RESET}
{CYAN}║{RED}                "QUANTUM MATRIX RUBRIK CUBE"                          {CYAN}  ║{RESET}
{CYAN}║{YELLOW}                    "JAH BLESS !!!!"                                 {CYAN}  ║{RESET}
{CYAN}║{MAGENTA}           "YOU ARE ALIVE ON OUR HEART(S)"                           {CYAN}  ║{RESET}
{CYAN}║{GREEN}              c/o SENEGAL SURFER ONG AND SK8                         {CYAN}  ║{RESET}
{CYAN}║{BLUE}                 THAT VIRGIL ABLOH BUILT                             {CYAN}  ║{RESET}
{CYAN}╚════════════════════════════════════════════════════════════════════════════╝{RESET}
"""

# Quantum cube ASCII art for animation
QUANTUM_CUBE = [
    f"{BLUE}┏━━━━━┓\n┃ ╔═╗ ┃\n┃ ║ ║ ┃\n┃ ╚═╝ ┃\n┗━━━━━┛{RESET}",
    f"{RED}┏━━━━━┓\n┃ ╔═╗ ┃\n┃ ║ ║ ┃\n┃ ╚═╝ ┃\n┗━━━━━┛{RESET}",
    f"{GREEN}┏━━━━━┓\n┃ ╔═╗ ┃\n┃ ║ ║ ┃\n┃ ╚═╝ ┃\n┗━━━━━┛{RESET}",
    f"{YELLOW}┏━━━━━┓\n┃ ╔═╗ ┃\n┃ ║ ║ ┃\n┃ ╚═╝ ┃\n┗━━━━━┛{RESET}",
    f"{MAGENTA}┏━━━━━┓\n┃ ╔═╗ ┃\n┃ ║ ║ ┃\n┃ ╚═╝ ┃\n┗━━━━━┛{RESET}",
    f"{CYAN}┏━━━━━┓\n┃ ╔═╗ ┃\n┃ ║ ║ ┃\n┃ ╚═╝ ┃\n┗━━━━━┛{RESET}"
]

JAH_BLESSINGS = [
    "JAH BLESS!",
    "ONE LOVE!",
    "ROOTS AND CULTURE!",
    "IRIE HEIGHTS!",
    "DIVINE GUIDANCE!"
]

def display_banner() -> None:
    """Display the ASCII art banner for the Lucas Silveira Portal."""
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Print the banner
    print(SHAKA_BANNER)
    
    # Print a random JAH blessing
    print(f"{YELLOW}{BOLD}{random.choice(JAH_BLESSINGS)}{RESET}\n")

def animate_quantum_cube() -> None:
    """Animate the quantum cube with rotating colors."""
    for _ in range(10):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(random.choice(QUANTUM_CUBE))
        time.sleep(0.2)
    
    # End with the full banner
    display_banner()

if __name__ == "__main__":
    # Test the banner display
    display_banner() 