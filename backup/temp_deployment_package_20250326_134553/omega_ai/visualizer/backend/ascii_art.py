"""OMEGA BTC AI ASCII Art Module"""

# ANSI Colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"

def display_omega_banner(service_name: str):
    """Display cyberpunk-styled OMEGA BTC AI banner."""
    banner = f"""
{GREEN}╔══════════════════════════════════════════════════════════╗{RESET}
{YELLOW}
     ██████╗ ███╗   ███╗███████╗ ██████╗  █████╗ 
    ██╔═══██╗████╗ ████║██╔════╝██╔════╝ ██╔══██╗
    ██║   ██║██╔████╔██║█████╗  ██║  ███╗███████║
    ██║   ██║██║╚██╔╝██║██╔══╝  ██║   ██║██╔══██║
    ╚██████╔╝██║ ╚═╝ ██║███████╗╚██████╔╝██║  ██║
     ╚═════╝ ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝{RESET}
{MAGENTA}                BTC AI SYSTEM v1.0{RESET}
{CYAN}              [ {service_name} ]{RESET}
{GREEN}╚══════════════════════════════════════════════════════════╝{RESET}

{BLUE}[*] Initializing Quantum Neural Networks...{RESET}
{RED}[*] Loading Advanced Pattern Recognition...{RESET}
{YELLOW}[*] Calibrating Market Manipulation Detection...{RESET}
{GREEN}[*] System Ready - HODL THE LINE 💎{RESET}
"""
    print(banner)

def print_status(message: str, status_type: str = "info"):
    """Print styled status messages."""
    colors = {
        "info": BLUE,
        "success": GREEN,
        "warning": YELLOW,
        "error": RED
    }
    color = colors.get(status_type, BLUE)
    print(f"{color}[*] {message}{RESET}") 