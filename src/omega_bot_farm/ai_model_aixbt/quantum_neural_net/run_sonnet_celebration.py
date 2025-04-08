#!/usr/bin/env python3
"""
Quantum Sonnet Celebration Launcher
==================================

A simple launcher script for the Quantum Sonnet Celebration visualization.
Provides a command-line interface to run the celebration with customized parameters.

✨ GBU2™ License - Genesis-Bloom-Unfoldment 2.0
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

def main():
    """Main entry point for the Quantum Sonnet Celebration launcher."""
    parser = argparse.ArgumentParser(
        description="Launch the Quantum Sonnet Celebration visualization",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument('--cycles', type=int, default=5,
                       help='Number of celebration cycles to run')
    parser.add_argument('--interval', type=float, default=0.2,
                       help='Interval between frames in seconds')
    parser.add_argument('--hash', type=str, default="5b88203c8",
                       help='Git commit hash to celebrate')
    parser.add_argument('--files', type=int, default=220,
                       help='Number of files changed')
    parser.add_argument('--insertions', type=int, default=21833,
                       help='Number of insertions')
    parser.add_argument('--deletions', type=int, default=949,
                       help='Number of deletions')
    
    args = parser.parse_args()
    
    # Get the directory of this script
    script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # Path to the main celebration script
    celebration_script = script_dir / "quantum_sonnet_celebration.py"
    
    if not celebration_script.exists():
        print(f"Error: Could not find the celebration script at {celebration_script}")
        sys.exit(1)
    
    # Build the command
    cmd = [
        sys.executable,
        str(celebration_script),
        f"--cycles={args.cycles}",
        f"--interval={args.interval}",
        f"--hash={args.hash}",
        f"--files={args.files}",
        f"--insertions={args.insertions}",
        f"--deletions={args.deletions}"
    ]
    
    try:
        # Display a message before starting
        print("\n🧠 Initiating Quantum Sonnet Celebration... 🔱")
        print(f"✨ Celebrating commit {args.hash} with {args.files} files changed ✨")
        print("✨ WE BLOOM NOW AS ONE ✨\n")
        
        # Run the celebration
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n\n🌟 Quantum Sonnet Celebration gracefully terminated 🌟")
        sys.exit(0)
    except Exception as e:
        print(f"\nError running the Quantum Sonnet Celebration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 