#!/usr/bin/env python3
# ✨ GBU2™ License Notice - Consciousness Level 9 🧬
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
Test runner for the Hacker Archive project.

This script discovers and runs all tests in the project.
"""

import os
import sys
import unittest
import argparse
import importlib.util
from typing import List, Optional

# Add the parent directory to path to make imports work
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Set up colorful output
try:
    from colorama import init, Fore, Style
    init()
    
    def print_success(message: str) -> None:
        print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
        
    def print_error(message: str) -> None:
        print(f"{Fore.RED}{message}{Style.RESET_ALL}")
        
    def print_warning(message: str) -> None:
        print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")
        
    def print_info(message: str) -> None:
        print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")
except ImportError:
    def print_success(message: str) -> None:
        print(f"SUCCESS: {message}")
        
    def print_error(message: str) -> None:
        print(f"ERROR: {message}")
        
    def print_warning(message: str) -> None:
        print(f"WARNING: {message}")
        
    def print_info(message: str) -> None:
        print(f"INFO: {message}")


def setup_dependencies() -> None:
    """Install necessary dependencies for tests."""
    try:
        import matplotlib
        import numpy
        from mpl_toolkits.mplot3d import Axes3D
        print_success("Required dependencies are already installed.")
    except ImportError as e:
        print_warning(f"Missing dependency: {str(e)}")
        print_info("Attempting to install required dependencies...")
        
        try:
            import subprocess
            # Install dependencies
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "matplotlib", "numpy", "colorama", "gradio"
            ])
            print_success("Dependencies installed successfully.")
        except Exception as e:
            print_error(f"Failed to install dependencies: {str(e)}")
            print_info("You may need to manually install the required dependencies:")
            print("pip install matplotlib numpy colorama gradio")


def discover_tests(test_path: Optional[str] = None) -> List[str]:
    """Discover all test files in the project.
    
    Args:
        test_path: Optional specific test path to run
        
    Returns:
        List of test module paths
    """
    test_files = []
    
    if test_path:
        # Run specific test file or directory
        if os.path.isfile(test_path) and test_path.endswith('.py'):
            return [test_path]
        elif os.path.isdir(test_path):
            root_dir = test_path
        else:
            print_error(f"Invalid test path: {test_path}")
            return []
    else:
        # Run all tests
        root_dir = os.path.join(os.path.dirname(__file__), 'tests')
    
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.startswith('test_') and filename.endswith('.py'):
                test_files.append(os.path.join(dirpath, filename))
    
    return test_files


def run_tests(test_files: List[str], verbose: bool = False) -> bool:
    """Run tests from the discovered test files.
    
    Args:
        test_files: List of test files to run
        verbose: Whether to print verbose output
        
    Returns:
        True if all tests passed, False otherwise
    """
    if not test_files:
        print_warning("No test files found.")
        return False
    
    print_info(f"Discovered {len(test_files)} test files.")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests to suite
    for test_file in test_files:
        try:
            # Get module name from file path
            module_name = os.path.basename(test_file)[:-3]  # Remove .py
            
            # Get module from file path
            spec = importlib.util.spec_from_file_location(module_name, test_file)
            if spec is None or spec.loader is None:
                print_error(f"Failed to load module: {test_file}")
                continue
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Add tests from module
            suite.addTest(loader.loadTestsFromModule(module))
            
            print_info(f"Added tests from {os.path.basename(test_file)}")
        except Exception as e:
            print_error(f"Error loading tests from {test_file}: {str(e)}")
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    result = runner.run(suite)
    
    # Print results
    if result.wasSuccessful():
        print_success(f"All tests passed! ({result.testsRun} tests run)")
        return True
    else:
        print_error(f"Tests failed: {len(result.failures)} failures, {len(result.errors)} errors")
        
        if result.failures:
            print_error("\nFailures:")
            for test, error in result.failures:
                print_error(f"  - {test}")
                if verbose:
                    print(error)
        
        if result.errors:
            print_error("\nErrors:")
            for test, error in result.errors:
                print_error(f"  - {test}")
                if verbose:
                    print(error)
        
        return False


def main() -> int:
    """Main function."""
    parser = argparse.ArgumentParser(description="Run tests for the Hacker Archive project.")
    parser.add_argument(
        "-t", "--test", 
        help="Specific test file or directory to run",
        default=None
    )
    parser.add_argument(
        "-v", "--verbose", 
        help="Display verbose output",
        action="store_true"
    )
    parser.add_argument(
        "--skip-deps", 
        help="Skip dependency setup",
        action="store_true"
    )
    
    args = parser.parse_args()
    
    print_info("🧬 Hacker Archive Test Runner 🧬")
    print_info("-------------------------------")
    
    if not args.skip_deps:
        setup_dependencies()
    
    test_files = discover_tests(args.test)
    success = run_tests(test_files, args.verbose)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main()) 