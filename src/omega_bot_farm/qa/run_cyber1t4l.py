#!/usr/bin/env python3
"""
CyBer1t4L QA Command Line Interface

The main entry point for the CyBer1t4L QA Bot that provides a cyberpunk-themed
interface for running test coverage analysis, real-time monitoring, and test generation.
"""

import os
import sys
import time
import argparse
import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any

# Determine the project root
PROJECT_ROOT = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Add the project root to the path
sys.path.insert(0, str(PROJECT_ROOT))

try:
    # Import the CyBer1t4L components
    from src.omega_bot_farm.qa.cyber1t4l_qa_bot import (
        CyBer1t4L, TestCoverageMonitor, RealTimeQAMonitor, 
        TestGenerator, Colors, setup_logging
    )
    
    DIRECT_IMPORT = True
except ImportError:
    # If direct import fails, we'll execute the scripts as subprocesses
    DIRECT_IMPORT = False

# ANSI color codes for the terminal interface if not directly imported
if not DIRECT_IMPORT:
    class Colors:
        RESET = "\033[0m"
        NEON_GREEN = "\033[38;5;82m"
        NEON_BLUE = "\033[38;5;39m"
        NEON_PINK = "\033[38;5;213m"
        NEON_YELLOW = "\033[38;5;226m"
        NEON_ORANGE = "\033[38;5;208m"
        NEON_RED = "\033[38;5;196m"
        CYBER_CYAN = "\033[38;5;51m"
        CYBER_PURPLE = "\033[38;5;141m"
        DARK_BG = "\033[48;5;17m"
        
        @staticmethod
        def format(text, color, bold=False):
            bold_code = "\033[1m" if bold else ""
            return f"{bold_code}{color}{text}{Colors.RESET}"

# ASCII art for the cyberpunk interface
CYBER1T4L_LOGO = """
  ██████╗██╗   ██╗██████╗ ███████╗██████╗ ██╗████████╗██╗  ██╗██╗     
 ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║╚══██╔══╝██║  ██║██║     
 ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║   ██║   ███████║██║     
 ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║   ██║   ██╔══██║██║     
 ╚██████╗   ██║   ██████╔╝███████╗██║  ██║██║   ██║   ██║  ██║███████╗
  ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝
                                                                       
 ░█▀█░█▀█░░░█▀▄░█▀█░▀█▀░░░█░█░█▀█░█▀▄░█▀▄░▀█▀░█▀█░█▀▄                  
 ░█▀▀░█▀█░░░█▀▄░█░█░░█░░░░█▀█░█▀█░█▀▄░█▀▄░░█░░█░█░█▀▄                  
 ░▀░░░▀░▀░░░▀▀░░▀▀▀░░▀░░░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀░▀░▀░▀                  
"""

def display_intro():
    """Display the cyberpunk-themed introduction."""
    print(f"\n{Colors.DARK_BG}")
    for line in CYBER1T4L_LOGO.split('\n'):
        colored_line = ""
        for i, char in enumerate(line):
            if char in "█▀▄":
                colors = [Colors.NEON_GREEN, Colors.NEON_BLUE, Colors.NEON_PINK]
                colored_line += f"{colors[i % 3]}{char}{Colors.RESET}"
            elif char == "░":
                colored_line += f"{Colors.CYBER_PURPLE}{char}{Colors.RESET}"
            else:
                colored_line += f"{Colors.CYBER_CYAN}{char}{Colors.RESET}"
        print(colored_line)
        
    print(f"{Colors.RESET}\n")
    print(f"{Colors.format('🔴 🟡 🟢 RASTA HEART ON F1R3 🔴 🟡 🟢', Colors.NEON_ORANGE, True)}")
    print(f"{Colors.format('THE GUARDIAN OF DIVINE FLOW', Colors.NEON_GREEN, True)}")
    print(f"{Colors.format('CyBer1t4L v1.0.0', Colors.NEON_BLUE)} - {Colors.format('QA JEDI Master', Colors.NEON_PINK)}\n")

def run_command(command: List[str], description: str) -> int:
    """
    Run a command with proper formatting and error handling.
    
    Args:
        command: The command to run as a list of strings
        description: A description of what the command does
        
    Returns:
        The return code of the command
    """
    print(f"{Colors.format('EXECUTING', Colors.NEON_YELLOW, True)}: {description}")
    print(f"{Colors.CYBER_CYAN}> {' '.join(command)}{Colors.RESET}\n")
    
    try:
        process = subprocess.run(command, check=False)
        if process.returncode == 0:
            print(f"\n{Colors.format('✅ SUCCESS', Colors.NEON_GREEN, True)}: {description} completed\n")
        else:
            print(f"\n{Colors.format('❌ FAILED', Colors.NEON_RED, True)}: {description} returned code {process.returncode}\n")
        return process.returncode
    except Exception as e:
        print(f"\n{Colors.format('❌ ERROR', Colors.NEON_RED, True)}: {str(e)}\n")
        return 1

def run_coverage_analysis(args):
    """Run test coverage analysis."""
    if DIRECT_IMPORT:
        # Use direct import if available
        monitor = TestCoverageMonitor(Path(args.project_root) if args.project_root else PROJECT_ROOT, 
                                     threshold=args.threshold)
        return monitor.run_coverage_analysis(args.modules) is not None
    else:
        # Build command for subprocess
        cmd = [
            "python", 
            str(PROJECT_ROOT / "src" / "omega_bot_farm" / "qa" / "cyber1t4l_qa_bot.py"),
            "--mode", "coverage",
        ]
        
        if args.project_root:
            cmd.extend(["--project-root", args.project_root])
            
        if args.threshold:
            cmd.extend(["--threshold", str(args.threshold)])
            
        if args.modules:
            cmd.extend(["--modules"] + args.modules)
            
        return run_command(cmd, "Test Coverage Analysis") == 0

def run_test_generation(args):
    """Generate test cases for modules."""
    if DIRECT_IMPORT:
        # Use direct import if available
        generator = TestGenerator(Path(args.project_root) if args.project_root else PROJECT_ROOT)
        success = True
        for module in args.modules:
            result, _ = generator.generate_test_file(module)
            success = success and result
        return success
    else:
        # Build command for subprocess
        cmd = [
            "python", 
            str(PROJECT_ROOT / "src" / "omega_bot_farm" / "qa" / "test_case_generator.py")
        ]
        
        if args.project_root:
            cmd.extend(["--project-root", args.project_root])
            
        if args.modules:
            cmd.extend(args.modules)
            
        return run_command(cmd, "Test Case Generation") == 0

def run_monitoring(args):
    """Run real-time system monitoring."""
    if DIRECT_IMPORT:
        # Use direct import if available
        monitor = RealTimeQAMonitor(Path(args.project_root) if args.project_root else PROJECT_ROOT)
        try:
            monitor.start_monitoring(args.components)
            print(f"{Colors.format('Real-time monitoring active', Colors.NEON_GREEN, True)}")
            print("Press Ctrl+C to stop...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            monitor.stop_monitoring()
            return True
    else:
        # Build command for subprocess
        cmd = [
            "python", 
            str(PROJECT_ROOT / "src" / "omega_bot_farm" / "qa" / "cyber1t4l_qa_bot.py"),
            "--mode", "monitor"
        ]
        
        if args.project_root:
            cmd.extend(["--project-root", args.project_root])
            
        if args.components:
            cmd.extend(["--components"] + args.components)
            
        return run_command(cmd, "Real-time System Monitoring") == 0

def run_full_qa_cycle(args):
    """Run a full QA cycle."""
    if DIRECT_IMPORT:
        # Use direct import if available
        bot = CyBer1t4L(Path(args.project_root) if args.project_root else PROJECT_ROOT)
        bot.run_full_qa_cycle()
        return True
    else:
        # Build command for subprocess
        cmd = [
            "python", 
            str(PROJECT_ROOT / "src" / "omega_bot_farm" / "qa" / "cyber1t4l_qa_bot.py"),
            "--mode", "full"
        ]
        
        if args.project_root:
            cmd.extend(["--project-root", args.project_root])
            
        if args.threshold:
            cmd.extend(["--threshold", str(args.threshold)])
            
        return run_command(cmd, "Full QA Cycle") == 0

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="CyBer1t4L - QA Bot for OMEGA Trading Ecosystem",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full QA cycle
  python run_cyber1t4l.py full

  # Run coverage analysis
  python run_cyber1t4l.py coverage --threshold 85.0

  # Generate tests for specific modules
  python run_cyber1t4l.py generate --modules src/omega_bot_farm/trading/exchanges/ccxt_b0t.py

  # Run real-time monitoring
  python run_cyber1t4l.py monitor
"""
    )
    
    # Mode subparsers
    subparsers = parser.add_subparsers(dest="mode", help="Operation mode")
    
    # Full QA cycle
    full_parser = subparsers.add_parser("full", help="Run full QA cycle")
    full_parser.add_argument("--project-root", help="Project root directory")
    full_parser.add_argument("--threshold", type=float, default=80.0, 
                             help="Coverage threshold percentage (default: 80.0)")
    
    # Coverage analysis
    coverage_parser = subparsers.add_parser("coverage", help="Run coverage analysis")
    coverage_parser.add_argument("--project-root", help="Project root directory")
    coverage_parser.add_argument("--threshold", type=float, default=80.0,
                                help="Coverage threshold percentage (default: 80.0)")
    coverage_parser.add_argument("--modules", nargs="+", help="Specific modules to analyze")
    
    # Test generation
    generate_parser = subparsers.add_parser("generate", help="Generate test cases")
    generate_parser.add_argument("--project-root", help="Project root directory")
    generate_parser.add_argument("--modules", nargs="+", required=True, 
                                help="Modules to generate tests for")
    
    # Real-time monitoring
    monitor_parser = subparsers.add_parser("monitor", help="Run real-time system monitoring")
    monitor_parser.add_argument("--project-root", help="Project root directory")
    monitor_parser.add_argument("--components", nargs="+", 
                               choices=["bitget", "discord", "matrix"],
                               help="Specific components to monitor")
    
    return parser.parse_args()

def main():
    """Main entry point."""
    args = parse_args()
    
    if not args.mode:
        display_intro()
        print(f"{Colors.format('Please specify an operation mode', Colors.NEON_YELLOW)}")
        print("Run with --help to see available options")
        return 1
    
    display_intro()
    
    if args.mode == "full":
        return 0 if run_full_qa_cycle(args) else 1
    elif args.mode == "coverage":
        return 0 if run_coverage_analysis(args) else 1
    elif args.mode == "generate":
        return 0 if run_test_generation(args) else 1
    elif args.mode == "monitor":
        return 0 if run_monitoring(args) else 1
    else:
        print(f"{Colors.format('Unknown mode', Colors.NEON_RED)}: {args.mode}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 