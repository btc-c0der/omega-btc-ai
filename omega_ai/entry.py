#!/usr/bin/env python3
"""
OMEGA BTC AI - EXODUS ALGORITHM ENTRY POINT

Divine entry point for running either the original EXODUS Algorithm
or the Enhanced EXODUS with multi-cycle awareness and bio-energy sensing
"""

import asyncio
import argparse
import logging
import sys
import os
from datetime import datetime, timezone

# Configure logging with RASTA colors
GREEN = "\033[92m"       # Life energy
YELLOW = "\033[93m"      # Wisdom, sun
RED = "\033[91m"         # Heart, strength 
BLUE = "\033[94m"        # Water, flow
MAGENTA = "\033[95m"     # Cosmic energy
CYAN = "\033[96m"        # Healing
WHITE = "\033[97m"       # Pure light
RESET = "\033[0m"        # Reset to baseline

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format=f'{GREEN}%(asctime)s{RESET} - {YELLOW}%(name)s{RESET} - {RED}%(levelname)s{RESET} - %(message)s'
)
logger = logging.getLogger("EXODUS.ENTRY")

def display_sacred_banner():
    """Display the sacred EXODUS banner."""
    banner = f"""
    {RED}╔═══════════════════════════════════════════════════════════╗{RESET}
    {YELLOW}║  {GREEN}O{YELLOW}M{RED}E{GREEN}G{YELLOW}A{RED} {GREEN}B{YELLOW}T{RED}C{GREEN} {YELLOW}A{RED}I{GREEN} - {YELLOW}E{RED}X{GREEN}O{YELLOW}D{RED}U{GREEN}S{YELLOW} {RED}A{GREEN}L{YELLOW}G{RED}O{GREEN}R{YELLOW}I{RED}T{GREEN}H{YELLOW}M{RED}S{RESET}  {YELLOW}║{RESET}
    {GREEN}║                                                       ║{RESET}
    {BLUE}║  {YELLOW}MOVEMENT OF JAH AI AND JAH JAH PEOPLE  {BLUE}║{RESET}
    {MAGENTA}╚═══════════════════════════════════════════════════════════╝{RESET}
    
    {CYAN}Divine Flow Initialized at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}{RESET}
    {YELLOW}Sacred Fibonacci Sequence: 1,1,2,3,5,8,13,21,34,55,89,144...{RESET}
    """
    print(banner)

async def run_exodus_original(duration_minutes=144, continuous=False):
    """Run the original EXODUS Algorithm."""
    try:
        # Import here to avoid circular imports
        from omega_ai.algos.exodus_algorithms import ExodusFlow
        
        logger.info(f"{GREEN}Starting Original EXODUS Algorithm{RESET}")
        
        # Initialize the flow
        exodus = ExodusFlow()
        
        # Run for specified duration
        if continuous:
            logger.info(f"{YELLOW}Running in continuous mode until manually stopped{RESET}")
            while True:
                await exodus.run_exodus_flow(duration_minutes=duration_minutes)
                logger.info(f"{GREEN}Cycle completed, starting next cycle{RESET}")
        else:
            logger.info(f"{YELLOW}Running for {duration_minutes} minutes{RESET}")
            await exodus.run_exodus_flow(duration_minutes=duration_minutes)
            
    except KeyboardInterrupt:
        logger.info(f"{YELLOW}EXODUS flow interrupted by user{RESET}")
    except Exception as e:
        logger.error(f"{RED}Error running EXODUS: {e}{RESET}")
        import traceback
        traceback.print_exc()

async def run_exodus_enhanced(duration_minutes=144, continuous=False, audio=False):
    """Run the Enhanced EXODUS Algorithm with all divine upgrades."""
    try:
        # Import here to avoid circular imports
        from omega_ai.algos.exodus_enhancements import ExodusEnhanced
        
        logger.info(f"{GREEN}Starting Enhanced EXODUS Algorithm with Divine Upgrades{RESET}")
        
        # Initialize the enhanced flow
        exodus = ExodusEnhanced()
        
        # Set audio mode if requested
        if exodus.redis and audio:
            exodus.redis.set("EXODUS_AUDIO", "TRUE")
            exodus.audio_enabled = True
            logger.info(f"{MAGENTA}🎵 Sacred Sound Generation enabled{RESET}")
        
        # Set continuous mode if requested
        if exodus.redis and continuous:
            exodus.redis.set("EXODUS_CONTINUOUS", "TRUE")
            exodus.continuous_mode = True
            logger.info(f"{YELLOW}Running in continuous mode until manually stopped{RESET}")
        else:
            logger.info(f"{YELLOW}Running for {duration_minutes} minutes{RESET}")
            
        # Run the enhanced flow
        await exodus.run_enhanced_exodus_flow(duration_minutes=duration_minutes)
            
    except KeyboardInterrupt:
        logger.info(f"{YELLOW}Enhanced EXODUS flow interrupted by user{RESET}")
    except Exception as e:
        logger.error(f"{RED}Error running Enhanced EXODUS: {e}{RESET}")
        import traceback
        traceback.print_exc()

def main():
    """Main entry point function."""
    parser = argparse.ArgumentParser(
        description=f'{YELLOW}OMEGA BTC AI - EXODUS Algorithm Runner{RESET}',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--mode', 
        choices=['original', 'enhanced'],
        default='enhanced',
        help='Run mode: original EXODUS or enhanced version with divine upgrades'
    )
    
    parser.add_argument(
        '--duration', 
        type=int,
        default=144,
        help='Duration in minutes to run (default: 144 - sacred Fibonacci number)'
    )
    
    parser.add_argument(
        '--continuous', 
        action='store_true',
        help='Run in continuous mode until manually stopped'
    )
    
    parser.add_argument(
        '--audio', 
        action='store_true',
        help='Enable sacred sound generation (enhanced mode only)'
    )
    
    args = parser.parse_args()
    
    # Display sacred banner
    display_sacred_banner()
    
    if args.mode == 'original':
        asyncio.run(run_exodus_original(
            duration_minutes=args.duration, 
            continuous=args.continuous
        ))
    else:
        asyncio.run(run_exodus_enhanced(
            duration_minutes=args.duration, 
            continuous=args.continuous,
            audio=args.audio
        ))

if __name__ == "__main__":
    main() 