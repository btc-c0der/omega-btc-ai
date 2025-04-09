#!/usr/bin/env python3
"""
LUCAS SILVEIRA PORTAL - SENEGAL SK8 DONATION DEMO RUNNER
========================================================

Demo runner for the quantum matrix Rubik's cube inspired donation flow.
"""

import os
import sys
import argparse
from typing import Dict, Any, Optional

# Add parent directory to path to ensure imports work correctly
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)

from senegal_sk8_donation import DonationFlow, display_banner

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Senegal SK8 Donation System - Quantum Matrix Rubik's Cube Edition"
    )
    parser.add_argument(
        "--interactive", "-i", 
        action="store_true",
        help="Run in interactive mode"
    )
    parser.add_argument(
        "--stats", "-s", 
        action="store_true",
        help="Display donation statistics"
    )
    parser.add_argument(
        "--config", "-c",
        type=str,
        help="Path to configuration file"
    )
    
    return parser.parse_args()

def main() -> None:
    """Main entry point for the demo runner."""
    args = parse_args()
    
    # Create donation flow system
    config_path = args.config if args.config and os.path.exists(args.config) else None
    donation_flow = DonationFlow(config_path)
    
    # Display the ASCII banner
    display_banner()
    
    # Handle command line arguments
    if args.stats:
        donation_flow.display_donation_stats()
    elif args.interactive:
        donation_flow.start_donation_flow()
    else:
        # Default is to run the demo
        donation_flow.run_demo()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user. JAH BLESS!")
        sys.exit(0) 