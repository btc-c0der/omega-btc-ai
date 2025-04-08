#!/usr/bin/env python3

"""
Test runner script for StrategicTraderB0t.

This script runs tests and generates coverage reports for the StrategicTraderB0t.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_tests_with_coverage(test_path=None, show_report=True):
    """
    Run tests and generate coverage report.
    
    Args:
        test_path: Path to specific test file or directory (optional)
        show_report: Whether to display the coverage report
    
    Returns:
        tuple: (success, coverage_percentage)
    """
    # Get the directory of this script
    script_dir = Path(__file__).parent.absolute()
    
    # Get project root
    project_root = script_dir.parent.parent.parent.parent.parent.parent
    
    # Target module path
    target_module = "src.omega_bot_farm.trading.b0ts.strategic_fibo.strategic_b0t"
    
    # Default test path is the directory containing this script
    if test_path is None:
        test_path = script_dir
    
    # Build command
    cmd = [
        "pytest",
        str(test_path),
        "-v",
        f"--cov={target_module}",
        "--cov-report=term-missing"
    ]
    
    if not show_report:
        cmd.append("--cov-report=none")
    
    # Run tests
    os.chdir(project_root)
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Print output
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    # Extract coverage percentage
    coverage_percentage = 0
    for line in result.stdout.splitlines():
        if "TOTAL" in line and "%" in line:
            # Parse coverage percentage
            parts = line.split("%")
            coverage_parts = parts[0].split()
            if coverage_parts:
                try:
                    coverage_percentage = float(coverage_parts[-1])
                except ValueError:
                    pass
    
    success = result.returncode == 0
    return success, coverage_percentage

def assess_coverage_gaps():
    """Analyze coverage report to identify gaps."""
    print("\n========== Coverage Analysis ==========")
    print("Potential coverage gaps to address:")
    print("1. Error handling paths")
    print("2. Edge cases in computation")
    print("3. Cosmic factor integration edge cases")
    print("4. Market regime transitions")
    print("5. Extreme market conditions")
    print("=======================================\n")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run tests for StrategicTraderB0t")
    parser.add_argument("--test-path", help="Specific test file or directory to run")
    parser.add_argument("--no-report", action="store_true", help="Don't display coverage report")
    parser.add_argument("--analyze-gaps", action="store_true", help="Analyze coverage gaps")
    args = parser.parse_args()
    
    success, coverage = run_tests_with_coverage(args.test_path, not args.no_report)
    
    print(f"\nCoverage: {coverage:.2f}%")
    if coverage < 80:
        print(f"WARNING: Coverage below target of 80% (Currently: {coverage:.2f}%)")
    else:
        print(f"SUCCESS: Coverage meets or exceeds target of 80% (Currently: {coverage:.2f}%)")
    
    if args.analyze_gaps:
        assess_coverage_gaps()
    
    return 0 if success and coverage >= 80 else 1

if __name__ == "__main__":
    sys.exit(main()) 