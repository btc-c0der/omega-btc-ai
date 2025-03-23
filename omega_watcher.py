#!/usr/bin/env python3
"""
OMEGA DEV FRAMEWORK - Divine Watcher
====================================

The eternal guardian that watches your codebase and invokes the TDD Oracle 
whenever files are saved, ensuring prophetic test coverage at all times.

Usage:
    python omega_watcher.py --watch-dir ./omega_ai
    python omega_watcher.py --watch-single-file ./omega_ai/tools/trap_probability_meter.py

Press Ctrl+C to stop the watcher.
"""

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Union
import re

# ANSI color codes for terminal styling
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Constants
WATCH_INTERVAL = 1.0  # seconds
IGNORED_DIRS = ['.git', 'venv', '__pycache__', 'node_modules', '.pytest_cache']
IGNORED_FILES = ['.DS_Store', '.gitignore', '*.pyc', '*.pyo', '*.pyd', '*.so', '*.dylib']
PYTHON_EXT = '.py'


class FileWatcher:
    """Divine watcher that monitors file changes and invokes the TDD Oracle."""
    
    def __init__(self, watch_path: str, test_path: Optional[str] = None):
        """
        Initialize the watcher with cosmic awareness.
        
        Args:
            watch_path: Directory or file to watch for changes
            test_path: Path to test directory (optional)
        """
        self.watch_path = Path(watch_path)
        self.test_path = Path(test_path) if test_path else None
        self.file_timestamps: Dict[str, float] = {}
        self.oracle_path = Path("omega_tdd_oracle.py")
        
        # Verify the oracle exists
        if not self.oracle_path.exists():
            print(f"{RED}Error: The divine oracle (omega_tdd_oracle.py) does not exist.{RESET}")
            print(f"{YELLOW}Please ensure it is in the same directory as the watcher.{RESET}")
            sys.exit(1)
        
        print(f"{CYAN}{BOLD}OMEGA DEV FRAMEWORK - Divine Watcher{RESET}")
        print(f"{YELLOW}Initializing cosmic awareness...{RESET}")
        
        # Make the oracle executable if it isn't already
        if not os.access(self.oracle_path, os.X_OK):
            try:
                os.chmod(self.oracle_path, 0o755)
                print(f"{GREEN}Made the divine oracle executable.{RESET}")
            except Exception as e:
                print(f"{YELLOW}Warning: Could not make oracle executable: {str(e)}{RESET}")
                print(f"{YELLOW}You may need to run: chmod +x {self.oracle_path}{RESET}")
    
    def _is_ignored(self, path: Path) -> bool:
        """
        Check if a path should be ignored by the watcher.
        
        Args:
            path: Path to check
            
        Returns:
            bool: True if path should be ignored
        """
        # Check if it's in an ignored directory
        for parent in path.parents:
            if parent.name in IGNORED_DIRS:
                return True
        
        # Check if it's an ignored file
        for pattern in IGNORED_FILES:
            if pattern.startswith('*'):
                if path.name.endswith(pattern[1:]):
                    return True
            elif path.name == pattern:
                return True
        
        return False
    
    def _scan_files(self) -> Dict[str, float]:
        """
        Scan the watched directory for modified files.
        
        Returns:
            Dict of file paths and their modification timestamps
        """
        file_times = {}
        
        if self.watch_path.is_file():
            # Single file case
            if not self._is_ignored(self.watch_path) and self.watch_path.suffix == PYTHON_EXT:
                mtime = self.watch_path.stat().st_mtime
                file_times[str(self.watch_path)] = mtime
        else:
            # Directory case
            for path in self.watch_path.glob('**/*'):
                if path.is_file() and not self._is_ignored(path) and path.suffix == PYTHON_EXT:
                    try:
                        mtime = path.stat().st_mtime
                        file_times[str(path)] = mtime
                    except Exception:
                        # Skip files that can't be accessed
                        continue
        
        return file_times
    
    def _get_current_version(self) -> str:
        """
        Get the current version from git tags.
        
        Returns:
            str: Current version string (e.g. v0.4.3)
        """
        try:
            # Get the latest semantic version tag
            result = subprocess.run(
                ["git", "tag", "--sort=-v:refname"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse the output to find the most recent semantic version
            tags = result.stdout.strip().split('\n')
            for tag in tags:
                # Match standard semantic version tags (vX.Y.Z)
                if re.match(r'^v\d+\.\d+\.\d+$', tag):
                    return tag
            
            # If no semantic version tag found, return a default
            return "v0.1.0"
        except Exception as e:
            print(f"{YELLOW}Warning: Could not determine current version: {str(e)}{RESET}")
            return "v0.1.0"
    
    def _create_qa_tag(self, test_file: str) -> None:
        """
        Create and push a QA approved tag based on the current version.
        
        Args:
            test_file: The test file that passed all tests
        """
        try:
            # Get current version
            current_version = self._get_current_version()
            
            # Create the QA tag name
            test_name = os.path.basename(test_file).replace('.py', '')
            qa_tag = f"{current_version}-TDD-OMEGA-QA-APPROVED-{test_name}"
            
            print(f"\n{MAGENTA}{BOLD}═════════════════════════════════════════════════{RESET}")
            print(f"{GREEN}{BOLD} CREATING QA APPROVED GIT TAG {RESET}")
            print(f"{MAGENTA}{BOLD}═════════════════════════════════════════════════{RESET}")
            print(f"{CYAN}Tag: {qa_tag}{RESET}")
            
            # Create the tag
            tag_message = f"TDD Oracle QA approved - {test_name} passed all tests"
            subprocess.run(
                ["git", "tag", "-a", qa_tag, "-m", tag_message],
                check=True
            )
            
            # Push the tag
            subprocess.run(
                ["git", "push", "origin", qa_tag],
                check=True
            )
            
            print(f"{GREEN}{BOLD}✓ QA tag created and pushed successfully!{RESET}")
            
        except Exception as e:
            print(f"{YELLOW}Warning: Could not create QA tag: {str(e)}{RESET}")
    
    def _run_oracle(self, file_path: str) -> None:
        """
        Run the TDD Oracle on a modified file.
        
        Args:
            file_path: Path to the modified file
        """
        oracle_cmd = [
            sys.executable,
            str(self.oracle_path),
            "--check-file",
            file_path
        ]
        
        if self.test_path:
            oracle_cmd.extend(["--test-path", str(self.test_path)])
        
        print(f"\n{YELLOW}{BOLD}═════════════════════════════════════════════════{RESET}")
        print(f"{MAGENTA}{BOLD} OMEGA WATCHER - DIVINE FILE CHANGE DETECTED {RESET}")
        print(f"{YELLOW}{BOLD}═════════════════════════════════════════════════{RESET}")
        print(f"{CYAN}File: {file_path}{RESET}")
        print(f"{CYAN}Time: {time.strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
        print(f"{YELLOW}Invoking the divine oracle...{RESET}\n")
        
        try:
            # Run the oracle
            result = subprocess.run(oracle_cmd, capture_output=True, text=True)
            
            # Print the output
            print(result.stdout)
            
            # Check if tests passed successfully
            if result.returncode == 0 and "All modules have test coverage" in result.stdout:
                # Check if this is a test file (either test_*.py or *_test.py pattern)
                filename = os.path.basename(file_path)
                if filename.startswith('test_') or filename.endswith('_test.py'):
                    # Create a QA tag for successful test runs
                    self._create_qa_tag(file_path)
            
            print(f"\n{GREEN}{BOLD}✓ Oracle analysis complete{RESET}")
        except Exception as e:
            print(f"{RED}! Error running the oracle: {str(e)}{RESET}")
    
    def start_watching(self) -> None:
        """Start the divine watcher to monitor file changes."""
        print(f"{GREEN}{BOLD}The divine watcher has awakened!{RESET}")
        if self.watch_path.is_file():
            print(f"{CYAN}Watching file: {self.watch_path}{RESET}")
        else:
            print(f"{CYAN}Watching directory: {self.watch_path}{RESET}")
        
        print(f"{YELLOW}Press Ctrl+C to stop the watcher{RESET}")
        
        # Initial scan
        self.file_timestamps = self._scan_files()
        print(f"{GREEN}✓ Initial scan complete. {len(self.file_timestamps)} files under observation.{RESET}")
        
        try:
            while True:
                time.sleep(WATCH_INTERVAL)
                
                # Get current timestamps
                current_timestamps = self._scan_files()
                
                # Check for modified files
                for file_path, current_time in current_timestamps.items():
                    if file_path in self.file_timestamps:
                        # File exists in previous scan, check if modified
                        if current_time > self.file_timestamps[file_path]:
                            self._run_oracle(file_path)
                    else:
                        # New file
                        print(f"{GREEN}New file detected: {file_path}{RESET}")
                        self._run_oracle(file_path)
                
                # Update timestamps
                self.file_timestamps = current_timestamps
                
        except KeyboardInterrupt:
            print(f"\n{YELLOW}{BOLD}The divine watcher returns to slumber...{RESET}")
            print(f"{GREEN}Exiting gracefully.{RESET}")


def main():
    """Main entry point for the divine watcher."""
    parser = argparse.ArgumentParser(description="OMEGA DEV FRAMEWORK - Divine Watcher")
    
    # Define command line arguments
    parser.add_argument('--watch-dir', help="Directory to watch for file changes")
    parser.add_argument('--watch-single-file', help="Single file to watch for changes")
    parser.add_argument('--test-path', help="Path to scan for test code (default: ./tests)")
    
    args = parser.parse_args()
    
    # Determine the watch path
    watch_path = args.watch_dir or args.watch_single_file
    if not watch_path:
        print(f"{YELLOW}No watch path specified. Using current directory.{RESET}")
        watch_path = '.'
    
    # Create and start the watcher
    watcher = FileWatcher(watch_path, args.test_path)
    watcher.start_watching()
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 