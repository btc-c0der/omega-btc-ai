#!/usr/bin/env python3
"""
Run the Quantum Celebration CLI directly with command line arguments
"""

import sys
import argparse
from omega_bot_farm.ai_model_aixbt.quantum_neural_net.quantum_celebration import QuantumCelebration

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="🧠 vQuB1T-NN Quantum Celebration CLI 🔱"
    )
    parser.add_argument('--cycles', type=int, default=10,
                      help='Number of celebration cycles')
    parser.add_argument('--interval', type=float, default=2.0,
                      help='Time interval between updates (seconds)')
    
    args = parser.parse_args()
    
    # Initialize and run celebration
    celebration = QuantumCelebration()
    celebration.run_celebration(
        cycles=args.cycles,
        interval=args.interval
    )
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 