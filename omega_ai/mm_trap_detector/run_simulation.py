#!/usr/bin/env python3

# Copyright (c) 2024 OMEGA BTC AI Team
# Licensed under the GNU Affero General Public License v3.0
# See https://www.gnu.org/licenses/ for more details

"""
Market Maker Trap Continuous Simulation Service
===============================================

This script runs the MM trap continuous simulation service which:
1. Simulates BTC price movements with configurable volatility
2. Detects traps using the actual trap detection logic
3. Stores all simulation data in Redis with 'sim_' prefixes
4. Can run indefinitely or for a specified duration

This provides valuable data for testing trap detection, dashboards,
alerts, and machine learning models without requiring real market data.

The simulation uses a combination of:
- Historical volatility data (if available in Redis)
- Configurable market regimes with different volatility profiles
- Random but realistic price movements
- Dynamically generated trap events with varying confidence levels
- High-frequency mode detection for trap clusters

All data is stored in Redis with 'sim_' prefixes to avoid interfering
with real market data, making it safe to run alongside production systems.

Usage:
    python -m omega_ai.mm_trap_detector.run_simulation [options]

Options:
    --duration HOURS    Run for specified hours (default: indefinite)
    --volatility SCALE  Volatility scale factor (default: 1.0)
    --frequency PROB    Trap frequency (0.0-1.0, default: 0.2)
    --daemon            Run in daemon mode (background)
"""

import sys
import argparse
import time
from omega_ai.mm_trap_detector.trap_simulation_service import TrapSimulator

# Terminal Colors
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"

def main():
    """
    Run the continuous simulation with command line arguments.
    
    This function:
    1. Parses command line arguments for simulation parameters
    2. Displays the configuration settings
    3. Creates and runs a TrapSimulator instance
    4. Handles errors and user interruptions gracefully
    
    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    parser = argparse.ArgumentParser(
        description="MM Trap Continuous Simulation Service",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--duration", 
        type=float, 
        help="Duration in hours (default: indefinite)",
        default=None
    )
    parser.add_argument(
        "--volatility", 
        type=float, 
        help="Volatility scale factor (higher = more volatile)",
        default=1.0
    )
    parser.add_argument(
        "--frequency", 
        type=float, 
        help="Trap frequency 0.0-1.0 (higher = more traps)",
        default=0.2
    )
    parser.add_argument(
        "--sleep", 
        type=float, 
        help="Sleep interval between iterations in seconds",
        default=0.1
    )
    parser.add_argument(
        "--daemon", 
        action="store_true", 
        help="Run in daemon mode (minimal output)"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.frequency < 0.0 or args.frequency > 1.0:
        print(f"{RED}Error: Frequency must be between 0.0 and 1.0{RESET}")
        return 1
        
    if args.volatility <= 0.0:
        print(f"{RED}Error: Volatility must be greater than 0.0{RESET}")
        return 1
        
    if args.sleep <= 0.0:
        print(f"{RED}Error: Sleep interval must be greater than 0.0{RESET}")
        return 1
    
    # Display configuration
    if not args.daemon:
        print(f"{YELLOW}═════════════════════════════════════════════════{RESET}")
        print(f"{CYAN}{BOLD}MARKET MAKER TRAP CONTINUOUS SIMULATION{RESET}")
        print(f"{YELLOW}═════════════════════════════════════════════════{RESET}")
        print(f"{GREEN}Duration: {args.duration if args.duration else 'Indefinite'} hours{RESET}")
        print(f"{GREEN}Volatility Scale: {args.volatility}x{RESET}")
        print(f"{GREEN}Trap Frequency: {args.frequency}{RESET}")
        print(f"{GREEN}Sleep Interval: {args.sleep}s{RESET}")
        print(f"{GREEN}Daemon Mode: {'Yes' if args.daemon else 'No'}{RESET}")
        print(f"{YELLOW}═════════════════════════════════════════════════{RESET}")
    
    try:
        # Create and run the simulator
        simulator = TrapSimulator(
            volatility_scale=args.volatility,
            trap_frequency=args.frequency,
            sleep_interval=args.sleep
        )
        
        simulator.run(duration_hours=args.duration)
        return 0
        
    except KeyboardInterrupt:
        if not args.daemon:
            print(f"\n{YELLOW}Simulation interrupted by user.{RESET}")
            print(f"{CYAN}Simulation data stored in Redis keys with 'sim_' prefix.{RESET}")
        return 0
    except Exception as e:
        if not args.daemon:
            print(f"\n{RED}Error in simulation: {e}{RESET}")
            # Print traceback for debugging
            import traceback
            traceback.print_exc()
        return 2

if __name__ == "__main__":
    sys.exit(main()) 