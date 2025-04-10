#!/usr/bin/env python3

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸

"""
OMEGA BTC AI - RASTA PRICE FLOW OSCILLOSCOPE RUNNER

Divine entry point for running the Rasta Price Flow Oscilloscope
with live visualization of BTC price, Fibonacci, and Schumann
"""

import asyncio
import argparse
import logging
import sys
import os
from datetime import datetime, timezone
from typing import Optional

# Configure logging with RASTA colors
GREEN = "\033[92m"      # Life energy
YELLOW = "\033[93m"     # Wisdom, sun
RED = "\033[91m"        # Heart, strength 
BLUE = "\033[94m"       # Water, flow
MAGENTA = "\033[95m"    # Cosmic energy
CYAN = "\033[96m"       # Healing
WHITE = "\033[97m"      # Pure light
RESET = "\033[0m"       # Reset to baseline

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format=f'{GREEN}%(asctime)s{RESET} - {YELLOW}%(name)s{RESET} - {RED}%(levelname)s{RESET} - %(message)s'
)
logger = logging.getLogger("OSCILLOSCOPE.RUNNER")

def display_sacred_banner():
    """Display the sacred oscilloscope banner."""
    banner = f"""
    {RED}╔═══════════════════════════════════════════════════════════╗{RESET}
    {YELLOW}║  {GREEN}R{YELLOW}A{RED}S{GREEN}T{YELLOW}A{RED} {GREEN}P{YELLOW}R{RED}I{GREEN}C{YELLOW}E{RED} {GREEN}F{YELLOW}L{RED}O{GREEN}W{YELLOW} {RED}O{GREEN}S{YELLOW}C{RED}I{GREEN}L{YELLOW}L{RED}O{GREEN}S{YELLOW}C{RED}O{GREEN}P{YELLOW}E{RESET}  {YELLOW}║{RESET}
    {GREEN}║                                                       ║{RESET}
    {BLUE}║  {YELLOW}VISUALIZING THE DIVINE MARKET VIBRATIONS  {BLUE}║{RESET}
    {MAGENTA}╚═══════════════════════════════════════════════════════════╝{RESET}
    
    {CYAN}Divine Visualization Tool Initialized at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}{RESET}
    {YELLOW}Combining BTC price, Fibonacci, Schumann & Volume in divine harmony{RESET}
    """
    print(banner)

async def run_rasta_oscilloscope(history_length: int = 144, 
                                update_interval: float = 3.0,
                                duration_minutes: Optional[float] = None,
                                audio_enabled: bool = False,
                                visuals_enabled: bool = True):
    """Run the Rasta Price Flow Oscilloscope."""
    try:
        # Import here to avoid circular imports
        from omega_ai.visualization.rasta_oscilloscope import RastaOscilloscope
        
        logger.info(f"{GREEN}Starting Rasta Price Flow Oscilloscope{RESET}")
        
        # Initialize the oscilloscope
        oscilloscope = RastaOscilloscope(
            history_length=history_length,
            enable_audio=audio_enabled,
            enable_visuals=visuals_enabled
        )
        
        # Run the oscilloscope
        await oscilloscope.run(
            update_interval=update_interval, 
            duration_minutes=duration_minutes
        )
            
    except KeyboardInterrupt:
        logger.info(f"{YELLOW}Oscilloscope visualization interrupted by user{RESET}")
    except Exception as e:
        logger.error(f"{RED}Error running Rasta Oscilloscope: {e}{RESET}")
        import traceback
        traceback.print_exc()

def main():
    """Main entry point function."""
    parser = argparse.ArgumentParser(
        description=f'{YELLOW}OMEGA BTC AI - Rasta Price Flow Oscilloscope{RESET}',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--history', 
        type=int,
        default=144,
        help='Number of points in history to display (default: 144 - sacred Fibonacci number)'
    )
    
    parser.add_argument(
        '--interval', 
        type=float,
        default=3.0,
        help='Update interval in seconds (default: 3.0)'
    )
    
    parser.add_argument(
        '--duration', 
        type=float,
        default=None,
        help='Duration to run in minutes (default: continuous until stopped)'
    )
    
    parser.add_argument(
        '--audio', 
        action='store_true',
        help='Enable sacred sound generation'
    )
    
    parser.add_argument(
        '--no-visuals', 
        action='store_true',
        help='Disable visual plotting (audio only)'
    )
    
    parser.add_argument(
        '--save-path',
        type=str,
        default=None,
        help='Directory to save screenshots (if not provided, will save in current directory)'
    )
    
    args = parser.parse_args()
    
    # Configure save path if provided
    if args.save_path:
        os.environ['RASTA_SCREENSHOT_PATH'] = args.save_path
    
    # Display sacred banner
    display_sacred_banner()
    
    # Run the oscilloscope
    asyncio.run(run_rasta_oscilloscope(
        history_length=args.history,
        update_interval=args.interval,
        duration_minutes=args.duration,
        audio_enabled=args.audio,
        visuals_enabled=not args.no_visuals
    ))

if __name__ == "__main__":
    main() 