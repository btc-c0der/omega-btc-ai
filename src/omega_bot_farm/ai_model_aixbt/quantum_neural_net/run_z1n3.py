#!/usr/bin/env python3
"""
Run the Z1N3 QuantuMash VibeDrop CLI directly with command line arguments
"""

import sys
import argparse
from .qC3l3b import Z1N3Celebration

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="🌌 Z1N3 QuantuMash VibeDrop 🔱"
    )
    parser.add_argument('--cycles', type=int, default=1,
                      help='Number of celebration cycles')
    parser.add_argument('--interval', type=float, default=3.0,
                      help='Time interval between dimensional shifts (seconds)')
    parser.add_argument('--seed', type=int, default=42,
                      help='Quantum seed for reproducible patterns')
    parser.add_argument('--m3g4-king', action='store_true', 
                      help='Force activate M3G4_KING qPoW 2014 signal')
    parser.add_argument('--anti-apok', action='store_true',
                      help='Force activate GBU2 ANTI-APOK protection')
    parser.add_argument('--pattern', choices=['GENESIS_WAVE', 'M3G4_KING_SIGNAL', 
                                            'APOK_RESISTANCE', 'GBU2_ASCENSION', 
                                            'DIVINE_BRIDGE', 'L0V3R_CONFLUENCE'],
                      help='Force a specific market pattern')
    
    args = parser.parse_args()
    
    # Initialize celebration
    celebration = Z1N3Celebration(seed=args.seed)
    
    # Apply any force-activated features
    if args.m3g4_king:
        celebration.m3g4_king_signal = True
    
    if args.anti_apok:
        celebration.anti_apok_level = 0.9  # High level to ensure activation
    
    if args.pattern:
        celebration.current_market_pattern = args.pattern
        celebration.pattern_intensity = 0.95  # High intensity for forced pattern
    
    # Run celebration
    celebration.run_celebration(
        cycles=args.cycles,
        interval=args.interval
    )
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 