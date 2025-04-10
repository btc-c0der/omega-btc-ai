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
Quantum Test Runner V2 Launcher
------------------------------

This script launches the Quantum Test Runner V2 with command-line options
to control IPFS distribution and NFT certification of test results.

Features:
- Git status monitoring (3-minute refresh)
- Automatic file backups on changes
- Code metrics analysis and refactoring alerts
- IPFS content distribution via Pinata (optional)
- NFT-based QA certification (optional)

Usage:
  python run_test_runner_v2.py [options]
  
Options:
  --project-root PATH    Path to project root (default: auto-detect)
  --scan-metrics         Scan code metrics once and exit
  --enable-ipfs          Enable IPFS distribution via Pinata
  --enable-nft           Enable NFT QA certification
  --help                 Show this help message and exit
"""

import os
import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)

# Import the runner
from runner_v2.runner import QuantumRunnerV2


def parse_extended_arguments():
    """Parse command line arguments with extended options."""
    parser = argparse.ArgumentParser(
        description="Quantum Test Runner V2 with IPFS and NFT support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_test_runner_v2.py                        # Run with basic features
  python run_test_runner_v2.py --enable-ipfs          # Enable IPFS distribution
  python run_test_runner_v2.py --enable-ipfs --enable-nft  # Enable both IPFS and NFT
  python run_test_runner_v2.py --scan-metrics         # Scan metrics once and exit
"""
    )
    
    parser.add_argument(
        "--project-root",
        help="Path to project root directory (default: auto-detect)"
    )
    
    parser.add_argument(
        "--scan-metrics",
        action="store_true",
        help="Scan code metrics once and exit"
    )
    
    parser.add_argument(
        "--enable-ipfs",
        action="store_true",
        help="Enable IPFS distribution via Pinata"
    )
    
    parser.add_argument(
        "--enable-nft",
        action="store_true",
        help="Enable NFT QA certification"
    )
    
    parser.add_argument(
        "--api-key",
        help="Pinata API key (can also use PINATA_API_KEY env var)"
    )
    
    parser.add_argument(
        "--api-secret",
        help="Pinata API secret (can also use PINATA_API_SECRET env var)"
    )
    
    parser.add_argument(
        "--gateway",
        help="Custom IPFS gateway URL"
    )
    
    parser.add_argument(
        "--nft-recipient",
        help="Wallet address for NFT certificates (can also use DEFAULT_NFT_RECIPIENT env var)"
    )
    
    return parser.parse_args()


def configure_environment(args):
    """Configure environment variables from arguments."""
    # Set IPFS credentials if provided
    if args.api_key:
        os.environ["PINATA_API_KEY"] = args.api_key
        
    if args.api_secret:
        os.environ["PINATA_API_SECRET"] = args.api_secret
        
    # Set NFT recipient if provided
    if args.nft_recipient:
        os.environ["DEFAULT_NFT_RECIPIENT"] = args.nft_recipient


def print_startup_banner():
    """Print a startup banner with ASCII art."""
    banner = r"""
    ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️
    
           🌌  QUANTUM TEST RUNNER V2 LAUNCHER  🌌
         🔮 IPFS-Enhanced Divine Test Framework 🔮
    
    ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️ ⚛️
    """
    print(banner)


def determine_project_root(specified_path=None):
    """
    Determine the project root directory.
    
    Args:
        specified_path: Path specified by the user
        
    Returns:
        Path to project root
    """
    if specified_path:
        return Path(specified_path).resolve()
    
    # Auto-detect: start from script location and navigate up
    current_path = Path(script_dir).resolve()
    
    # Look for common project identifiers
    for _ in range(5):  # Don't go up more than 5 levels
        # Check for common project indicators
        if (current_path / ".git").exists() or (current_path / "setup.py").exists():
            return current_path
            
        # Check for src directory
        if (current_path / "src").exists() and (current_path / "src").is_dir():
            return current_path
            
        # Move up one level
        parent = current_path.parent
        if parent == current_path:
            # Reached root, can't go further
            break
            
        current_path = parent
    
    # Default to two levels up from the script
    return Path(script_dir).resolve().parent.parent


def main():
    """Main entry point."""
    print_startup_banner()
    
    # Parse command line arguments
    args = parse_extended_arguments()
    
    # Configure environment variables
    configure_environment(args)
    
    # Determine project root
    project_root = determine_project_root(args.project_root)
    print(f"🚀 Using project root: {project_root}")
    
    # Create the runner
    runner = QuantumRunnerV2(
        project_root=project_root,
        enable_ipfs=args.enable_ipfs,
        enable_nft=args.enable_nft
    )
    
    if args.enable_ipfs:
        print("📦 IPFS distribution: ENABLED")
        
    if args.enable_nft:
        print("🏆 NFT certification: ENABLED")
    
    # Handle special run modes
    if args.scan_metrics:
        print("📊 Running metrics scan only...")
        metrics = runner.services["metrics"]
        metrics.watch_directory(str(runner.project_root / "src"), extensions=[".py"])
        metrics.scan_files()
        return
    
    # Run normally
    try:
        runner.run_forever()
    except KeyboardInterrupt:
        print("\n🛑 Quantum Test Runner stopped by user")
    finally:
        print("✨ Shutdown complete")


if __name__ == "__main__":
    main() 