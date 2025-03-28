#!/usr/bin/env python3
"""
🔱 OMEGA BTC AI - Divine Entry Point
📜 GPU²: General Public Universal + Graphics Processing Unison
🔐 Divine Copyright (c) 2025 - OMEGA Collective
"""

import sys
import argparse
from typing import Optional
from .utils.divine_banner import display_startup_banner, display_help, display_gpu2_license
from . import __version__

def parse_args() -> argparse.Namespace:
    """Parse sacred command line arguments"""
    parser = argparse.ArgumentParser(
        description="🔱 OMEGA BTC AI - Divine Trading System",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--help", "-h",
        action="store_true",
        help="Display divine help message"
    )
    
    parser.add_argument(
        "--version", "-v",
        action="store_true",
        help="Show sacred version number"
    )
    
    parser.add_argument(
        "--gpu2",
        action="store_true",
        help="Display the full GPU² license"
    )
    
    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Hide the sacred startup banner"
    )
    
    parser.add_argument(
        "--ascii",
        action="store_true",
        help="Force ASCII art display for terminals without Unicode support"
    )
    
    return parser.parse_args()

def main() -> None:
    """Divine entry point for the OMEGA BTC AI system"""
    args = parse_args()
    
    if args.help:
        display_help(use_ascii=args.ascii)
        return
    
    if args.version:
        print(f"🔱 OMEGA BTC AI v{__version__}")
        return
    
    if args.gpu2:
        display_gpu2_license(use_ascii=args.ascii)
        return
    
    if not args.no_banner:
        display_startup_banner(__version__, use_ascii=args.ascii)
    
    # Continue with divine system initialization...
    print("Initializing divine system...")

if __name__ == "__main__":
    main() 