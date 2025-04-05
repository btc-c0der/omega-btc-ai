#!/usr/bin/env python3
"""
Discord Integration Test Runner
------------------------------
This script discovers and runs all Discord integration tests
and generates a comprehensive report.
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
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# Add the project root to the path
script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
project_root = Path(os.path.abspath(os.path.join(script_dir, '../../../../')))
sys.path.insert(0, str(project_root))

# Define colors for terminal output
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

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Discord Integration Test Runner")
    
    parser.add_argument(
        "--report-dir",
        default=str(script_dir / "reports"),
        help="Directory to store test reports (default: tests/reports)"
    )
    
    parser.add_argument(
        "--html",
        action="store_true",
        help="Generate HTML report"
    )
    
    parser.add_argument(
        "--xml",
        action="store_true",
        help="Generate XML report for CI/CD"
    )
    
    parser.add_argument(
        "--test-file",
        help="Run a specific test file"
    )
    
    parser.add_argument(
        "--test-class",
        help="Run a specific test class (requires --test-file)"
    )
    
    parser.add_argument(
        "--test-function",
        help="Run a specific test function (requires --test-class)"
    )
    
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="Install required dependencies before running tests"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    parser.add_argument(
        "--live",
        action="store_true",
        help="Run tests against live bot instance"
    )
    
    return parser.parse_args()

def install_dependencies():
    """Install required dependencies for testing."""
    print(f"{Colors.format('Installing test dependencies...', Colors.NEON_BLUE)}")
    
    install_script = script_dir / "install_test_deps.sh"
    
    if install_script.exists():
        # Make the script executable
        os.chmod(install_script, 0o755)
        
        # Run the installation script
        result = subprocess.run([str(install_script)], check=False)
        
        if result.returncode == 0:
            print(f"{Colors.format('✅ Dependencies installed successfully', Colors.NEON_GREEN)}")
            return True
        else:
            print(f"{Colors.format('❌ Failed to install dependencies', Colors.NEON_RED)}")
            return False
    else:
        print(f"{Colors.format('❌ Installation script not found: {install_script}', Colors.NEON_RED)}")
        print(f"{Colors.format('Installing core dependencies manually...', Colors.NEON_YELLOW)}")
        
        # Install core dependencies
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "pytest", "pytest-asyncio", "pytest-cov", "httpx"
        ], check=False)
        
        return True

def discover_test_files():
    """Discover all Discord test files."""
    test_files = list(script_dir.glob("test_discord*.py")) + list(script_dir.glob("test_vcr*.py"))
    return [str(file) for file in test_files]

def run_tests(args):
    """Run the tests with pytest."""
    # Create report directory if it doesn't exist
    report_dir = Path(args.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    
    # Base pytest command
    pytest_args = ["-xvs"] if args.verbose else ["-xs"]
    
    # Add coverage
    pytest_args.extend([
        "--cov=src.omega_bot_farm.qa.cyber1t4l_qa_bot",
        "--cov-report=term",
    ])
    
    # Add HTML report if requested
    if args.html:
        html_dir = report_dir / "html"
        html_dir.mkdir(parents=True, exist_ok=True)
        pytest_args.append(f"--cov-report=html:{html_dir}")
    
    # Add XML report if requested
    if args.xml:
        xml_path = report_dir / "coverage.xml"
        pytest_args.append(f"--cov-report=xml:{xml_path}")
        
        # Also generate JUnit XML for CI systems
        junit_path = report_dir / "junit.xml"
        pytest_args.append(f"--junitxml={junit_path}")
    
    # Determine which tests to run
    if args.test_file:
        test_path = args.test_file
        
        if args.test_class:
            test_path += f"::{args.test_class}"
            
            if args.test_function:
                test_path += f"::{args.test_function}"
                
        test_files = [test_path]
    else:
        test_files = discover_test_files()
    
    # Add test files to pytest arguments
    pytest_args.extend(test_files)
    
    # Add live testing marker if requested
    if args.live:
        print(f"{Colors.format('Enabling live bot testing', Colors.NEON_BLUE)}")
        # Select only TestRunningBotE2E class from test_discord_integration.py
        if not args.test_file:
            # Find test_discord_integration.py in discovered files and add specific class
            for i, file in enumerate(test_files):
                if "test_discord_integration.py" in file:
                    test_files[i] = f"{file}::TestRunningBotE2E"
        
    # Display the command
    command_str = f"pytest {' '.join(pytest_args)}"
    print(f"{Colors.format('Running tests with command:', Colors.NEON_BLUE)}")
    print(f"{Colors.CYBER_CYAN}{command_str}{Colors.RESET}\n")
    
    # Run pytest
    result = subprocess.run(
        [sys.executable, "-m", "pytest"] + pytest_args,
        check=False
    )
    
    return result.returncode

def display_header():
    """Display a header for the test runner."""
    print(f"\n{Colors.DARK_BG}")
    print(f"{Colors.NEON_GREEN}  ██████╗██╗   ██╗██████╗ ███████╗██████╗ ██╗████████╗██╗  ██╗██╗     {Colors.RESET}")
    print(f"{Colors.NEON_BLUE} ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║╚══██╔══╝██║  ██║██║     {Colors.RESET}")
    print(f"{Colors.NEON_PINK} ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║   ██║   ███████║██║     {Colors.RESET}")
    print(f"{Colors.NEON_BLUE} ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║   ██║   ██╔══██║██║     {Colors.RESET}")
    print(f"{Colors.NEON_GREEN} ╚██████╗   ██║   ██████╔╝███████╗██║  ██║██║   ██║   ██║  ██║███████╗{Colors.RESET}")
    print(f"{Colors.NEON_BLUE}  ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝{Colors.RESET}")
    print(f"{Colors.RESET}\n")
    print(f"{Colors.format('DISCORD INTEGRATION TEST RUNNER', Colors.NEON_YELLOW, True)}")
    print(f"{Colors.format('Running tests at: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'), Colors.CYBER_CYAN)}\n")

def main():
    """Main entry point for the test runner."""
    display_header()
    
    args = parse_args()
    
    # Install dependencies if requested
    if args.install_deps:
        success = install_dependencies()
        if not success:
            print(f"{Colors.format('Continuing with tests, but some may fail due to missing dependencies', Colors.NEON_YELLOW)}")
    
    # Run the tests
    exit_code = run_tests(args)
    
    # Report results
    if exit_code == 0:
        print(f"\n{Colors.format('✅ All tests passed!', Colors.NEON_GREEN, True)}")
        
        # Show report locations
        if args.html:
            html_path = Path(args.report_dir) / "html" / "index.html"
            print(f"{Colors.format('HTML Report:', Colors.NEON_BLUE)} {html_path}")
        
        if args.xml:
            xml_path = Path(args.report_dir) / "coverage.xml"
            junit_path = Path(args.report_dir) / "junit.xml"
            print(f"{Colors.format('XML Coverage Report:', Colors.NEON_BLUE)} {xml_path}")
            print(f"{Colors.format('JUnit XML Report:', Colors.NEON_BLUE)} {junit_path}")
    else:
        print(f"\n{Colors.format('❌ Some tests failed', Colors.NEON_RED, True)}")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(main()) 