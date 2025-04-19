#!/usr/bin/env python3
"""
Quantum AI Test Runner
---------------------

This script runs all tests for the Quantum AI Knowledge Model and generates
a comprehensive test report.
"""
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


import os
import sys
import time
import argparse
import subprocess
import pytest
import datetime
import json
from typing import Dict, List, Any, Union, Optional

# Set up path to project root
PROJECT_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 
    "..", "..", "..", ".."
))
sys.path.insert(0, PROJECT_ROOT)

# ANSI colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text: str) -> None:
    """Print a formatted header."""
    border = "=" * (len(text) + 4)
    print(f"\n{Colors.HEADER}{Colors.BOLD}{border}")
    print(f"  {text}  ")
    print(f"{border}{Colors.ENDC}\n")

def print_section(text: str) -> None:
    """Print a formatted section title."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}=== {text} ==={Colors.ENDC}\n")

def print_result(text: str, success: bool) -> None:
    """Print a test result with appropriate coloring."""
    if success:
        print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")
    else:
        print(f"{Colors.RED}✗ {text}{Colors.ENDC}")

def run_tests(test_files: List[str], options: Optional[List[str]] = None) -> Dict[str, Any]:
    """Run pytest on the specified test files with options."""
    if options is None:
        options = ["-v"]
    
    # Build the command
    command = ["pytest"] + options + test_files
    print(f"{Colors.BLUE}Running: {' '.join(command)}{Colors.ENDC}")
    
    # Run the tests
    start_time = time.time()
    result = subprocess.run(command, capture_output=True, text=True)
    end_time = time.time()
    
    # Parse the output
    output = result.stdout
    error_output = result.stderr
    success = result.returncode == 0
    
    # Format test results
    if success:
        status = f"{Colors.GREEN}PASSED{Colors.ENDC}"
    else:
        status = f"{Colors.RED}FAILED{Colors.ENDC}"
    
    # Print output
    print(f"\n{output}")
    if error_output:
        print(f"{Colors.RED}Errors:{Colors.ENDC}\n{error_output}")
    
    print(f"Test run {status} in {end_time - start_time:.2f} seconds")
    
    return {
        "success": success,
        "output": output,
        "error_output": error_output,
        "execution_time": end_time - start_time,
        "returncode": result.returncode
    }

def generate_test_report(results: Dict[str, Dict[str, Any]], 
                         output_file: Optional[str] = None) -> None:
    """Generate a test report from the results."""
    now = datetime.datetime.now()
    report = {
        "timestamp": now.isoformat(),
        "total_tests": len(results),
        "passed_tests": sum(1 for r in results.values() if r["success"]),
        "failed_tests": sum(1 for r in results.values() if not r["success"]),
        "total_execution_time": sum(r["execution_time"] for r in results.values()),
        "results": results
    }
    
    # Save to file if specified
    if output_file:
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)
            print(f"\nTest report saved to {output_file}")
    
    # Print summary
    print_section("Test Summary")
    print(f"Date: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Tests: {report['total_tests']}")
    print(f"Passed: {report['passed_tests']}")
    print(f"Failed: {report['failed_tests']}")
    print(f"Total Execution Time: {report['total_execution_time']:.2f} seconds")
    
    # Print details
    print_section("Test Details")
    for test_type, result in results.items():
        if result["success"]:
            status = f"{Colors.GREEN}PASSED{Colors.ENDC}"
        else:
            status = f"{Colors.RED}FAILED{Colors.ENDC}"
        print(f"{test_type}: {status} in {result['execution_time']:.2f} seconds")

def main() -> None:
    """Run all tests for the Quantum AI Knowledge Model."""
    parser = argparse.ArgumentParser(description="Run Quantum AI Knowledge Model tests")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--performance", action="store_true", help="Run performance tests only")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--report", type=str, help="Save test report to file")
    parser.add_argument("--xml", type=str, help="Generate JUnit XML report")
    parser.add_argument("--html", type=str, help="Generate HTML report")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    
    args = parser.parse_args()
    
    # Default to running all tests if no specific test is specified
    if not (args.unit or args.integration or args.performance):
        args.all = True
    
    print_header("Quantum AI Knowledge Model Test Runner")
    
    # Get the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define test files
    test_files = {
        "unit": os.path.join(script_dir, "test_quantum_ai_knowledge_model.py"),
        "integration": os.path.join(script_dir, "test_quantum_ai_integration.py"),
        "performance": os.path.join(script_dir, "test_quantum_ai_performance.py")
    }
    
    # Prepare results
    results = {}
    
    # Run unit tests
    if args.unit or args.all:
        print_section("Running Unit Tests")
        options = ["-v"]
        if args.xml:
            options.extend(["--junit-xml", f"{args.xml}_unit.xml"])
        if args.html:
            options.extend(["--html", f"{args.html}_unit.html", "--self-contained-html"])
        if args.coverage:
            options.extend(["--cov=src.omega_bot_farm.qa.quantum_ai_knowledge_model", "--cov-report=term"])
        
        results["unit"] = run_tests([test_files["unit"]], options)
    
    # Run integration tests
    if args.integration or args.all:
        print_section("Running Integration Tests")
        options = ["-v"]
        if args.xml:
            options.extend(["--junit-xml", f"{args.xml}_integration.xml"])
        if args.html:
            options.extend(["--html", f"{args.html}_integration.html", "--self-contained-html"])
        
        results["integration"] = run_tests([test_files["integration"]], options)
    
    # Run performance tests
    if args.performance or args.all:
        print_section("Running Performance Tests")
        options = ["-v"]
        if args.xml:
            options.extend(["--junit-xml", f"{args.xml}_performance.xml"])
        if args.html:
            options.extend(["--html", f"{args.html}_performance.html", "--self-contained-html"])
        
        # Set environment variable to run performance tests
        os.environ["RUN_PERFORMANCE_TESTS"] = "1"
        results["performance"] = run_tests([test_files["performance"]], options)
        
        # Clean up environment variable
        del os.environ["RUN_PERFORMANCE_TESTS"]
    
    # Generate test report
    if results:
        report_file = args.report or os.path.join(
            script_dir, "reports", f"quantum_test_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        # Ensure reports directory exists
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        generate_test_report(results, report_file)
    
    # Exit with appropriate code
    all_success = all(r["success"] for r in results.values())
    sys.exit(0 if all_success else 1)

if __name__ == "__main__":
    main() 