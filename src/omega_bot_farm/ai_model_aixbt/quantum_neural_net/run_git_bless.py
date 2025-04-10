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

# -*- coding: utf-8 -*-

"""
Run the GIT BLESS command directly with command line arguments
"""

import sys
import argparse

# Change from absolute to relative import
from .git_bless import GitBless

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="GIT BLESS - Quantum Code Consecration System"
    )
    parser.add_argument('commit', nargs='?', default=None,
                      help='Commit hash to bless (optional)')
    parser.add_argument('--repo', type=str, help='Path to git repository (default: current directory)')
    parser.add_argument('--consciousness', type=float, default=0.93, 
                      help='Developer consciousness level (0.0-1.0)')
    parser.add_argument('--no-quantum', action='store_true', 
                      help='Disable quantum amplification')
    
    args = parser.parse_args()
    
    print(f"Performing quantum blessing ceremony for commit {args.commit or 'HEAD'} ✨")
    
    # Initialize blessing system
    git_bless = GitBless(
        repo_path=args.repo,
        consciousness_level=args.consciousness,
        quantum_amplification=not args.no_quantum
    )
    
    # Perform blessing ritual
    blessing_message = git_bless.perform_blessing_ritual(args.commit)
    
    # Display blessing message
    print(blessing_message)
    print("✨ The commit has been blessed ✨")
    
    # Return success code based on blessing level
    return 0 if git_bless.blessing_level > 0.3 else 1

if __name__ == "__main__":
    sys.exit(main()) 