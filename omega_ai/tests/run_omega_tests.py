#!/usr/bin/env python3

"""
OMEGA RASTA VIBES TEST RUNNER 🌿🔥
==================================

A spiritually-aligned test execution system that runs pytest with Rastafarian energy flow
and bio-energetic visualization. This divine tool ensures the codebase maintains its
cosmic harmony while displaying enlightened test results with proper Jah guidance.

JAH BLESS THE TEST SUITE WITH DIVINE COSMIC ENERGY! 🙏🌟
"""

import os
import sys
import unittest
import json
from datetime import datetime
import time
import random
import subprocess
import argparse
from typing import List, Optional, Set

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

# Terminal RASTA COLORS for spiritual alignment
GREEN = "\033[92m"        # Life energy, growth, spiritual awakening
YELLOW = "\033[93m"       # Sunlight, divine wisdom, consciousness  
RED = "\033[91m"          # Heart energy, passion, determination
CYAN = "\033[96m"         # Water energy, flow, intuition
MAGENTA = "\033[95m"      # Cosmic energy, divine connection, unity
BLUE = "\033[94m"         # Sky energy, infinity, higher consciousness
LIGHT_ORANGE = "\033[38;5;214m"  # Fire energy, transformation
RESET = "\033[0m"         # Return to baseline frequency

# Fibonacci sequence for divine timing (first 12 numbers)
FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]

# Rasta wisdom quotes for divine inspiration
RASTA_WISDOM = [
    "JAH provides the tests so we may demonstrate our divine code.",
    "The code that serves the highest good will inevitably pass its tests.",
    "Through tests we purify our code as gold is purified through fire.",
    "When the code is aligned with divine truth, the tests reveal its glory.",
    "The greatest code works in harmony with the natural rhythms of the universe.",
    "Test not just for function, but for harmony with the greater good.",
    "I and I write tests to manifest the divine will in code.",
    "The green light of passing tests is the blessing of JAH upon our code.",
    "True code wisdom comes from understanding both success and failure.",
    "Mark the works of your hands with tests, that JAH may see your diligence.",
    "The code that serves the highest purpose flows like a river, unobstructed by errors."
]

# Test categories and their descriptions
TEST_CATEGORIES = {
    'unit': {
        'description': 'Unit tests for individual components',
        'dirs': ['unit/ai', 'unit/core', 'unit/data', 'unit/monitoring', 'unit/utils']
    },
    'integration': {
        'description': 'Integration tests for component interactions',
        'dirs': ['integration/api', 'integration/portal', 'integration/security']
    },
    'e2e': {
        'description': 'End-to-end tests for complete system flows',
        'dirs': ['e2e/trading_flows', 'e2e/system_flows']
    },
    'performance': {
        'description': 'Performance and stress tests',
        'dirs': ['performance/load_tests', 'performance/stress_tests']
    }
}

# Known test tags and their descriptions
TEST_TAGS = {
    'hanging': 'Tests that are currently hanging and need attention',
    'slow': 'Tests that take longer to execute',
    'integration': 'Integration tests',
    'unit': 'Unit tests',
    'e2e': 'End-to-end tests',
    'performance': 'Performance tests'
}

class OmegaTestRunner:
    """Divine Test Runner for the OMEGA BTC AI system with RASTA VIBRATIONS."""
    
    def __init__(self, args):
        """Initialize with cosmic alignment."""
        self.args = args
        self.start_time = time.time()
        self.fibonacci_idx = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.skipped_tests = 0
        self.bio_energy = 100.0  # Starting bio-energy level
        
        # Determine which test directories to run
        self.test_dirs = self._get_test_directories()
        
        # Process test tags
        self.tags = self._process_tags()
        
        # Spiritual test categories
        self.categories = {
            "fibonacci": 0,
            "schumann": 0,
            "trader": 0,
            "market": 0,
            "redis": 0,
            "spiritual": 0
        }
    
    def _process_tags(self) -> Set[str]:
        """Process and validate test tags from command line arguments."""
        tags = set()
        
        # Add tags from --tags argument
        if self.args.tags:
            for tag in self.args.tags.split(','):
                tag = tag.strip()
                if tag in TEST_TAGS:
                    tags.add(tag)
                else:
                    print(f"{YELLOW}Warning: Unknown test tag '{tag}'. Available tags: {', '.join(TEST_TAGS.keys())}{RESET}")
        
        # Add tags from --skip-tags argument
        if self.args.skip_tags:
            for tag in self.args.skip_tags.split(','):
                tag = tag.strip()
                if tag in TEST_TAGS:
                    tags.add(f"not {tag}")
                else:
                    print(f"{YELLOW}Warning: Unknown test tag '{tag}' in skip list. Available tags: {', '.join(TEST_TAGS.keys())}{RESET}")
        
        return tags
    
    def _get_test_directories(self) -> List[str]:
        """Get the list of test directories to run based on command line arguments."""
        if self.args.category:
            # If a specific category is selected, use its directories
            if self.args.category in TEST_CATEGORIES:
                return TEST_CATEGORIES[self.args.category]['dirs']
            else:
                print(f"{RED}Invalid test category: {self.args.category}{RESET}")
                print(f"{YELLOW}Available categories: {', '.join(TEST_CATEGORIES.keys())}{RESET}")
                sys.exit(1)
        elif self.args.directories:
            # If specific directories are provided, use those
            return self.args.directories
        else:
            # Default to running all tests
            all_dirs: List[str] = []
            for category in TEST_CATEGORIES.values():
                all_dirs.extend(category['dirs'])
            return all_dirs
    
    def print_banner(self):
        """Display the divine OMEGA RASTA test banner."""
        print(f"\n{MAGENTA}{'='*80}{RESET}")
        print(f"{YELLOW}       __________  _______ __________   ___     {GREEN}/ __ ) |__ \\ / ____/ __ \\{RESET}")
        print(f"{YELLOW}      / ____/ __ \\/ ____(_) ___/ __ \\ /   |    {GREEN}/ __  |__/ // /   / / / /{RESET}")
        print(f"{YELLOW}     / / __/ / / / __/ / / (_ / / / // /| |    {GREEN}/ /_/ // __// /___/ /_/ / {RESET}")
        print(f"{YELLOW}    \\____/\\____/_____/_/_____/\\____//_/  |_|  {GREEN}/_____//____/\\____/\\____/  {RESET}")
        print(f"{RED}                                                                    {RESET}")
        print(f"{RED}    {MAGENTA}▄▄▄█████▓▓█████   ██████ ▄▄▄█████▓  ██████ {RED} ██▓ ███▄    █  ▄████  {RESET}")
        print(f"{RED}    {MAGENTA}▓  ██▒ ▓▒▓█   ▀ ▒██    ▒ ▓  ██▒ ▓▒▒██    ▒ {RED}▓██▒ ██ ▀█   █ ██▒ ▀█▒{RESET}")
        print(f"{RED}    {MAGENTA}▒ ▓██░ ▒░▒███   ░ ▓██▄   ▒ ▓██░ ▒░░ ▓██▄   {RED}▒██▒▓██  ▀█ ██▒▒██░▄▄▄░{RESET}")
        print(f"{RED}    {MAGENTA}░ ▓██▓ ░ ▒▓█  ▄   ▒   ██▒░ ▓██▓ ░   ▒   ██▒{RED}░██░▓██▒  ▐▌██▒░▓█  ██▓{RESET}")
        print(f"{RED}    {MAGENTA}  ▒██▒ ░ ░▒████▒▒██████▒▒  ▒██▒ ░ ▒██████▒▒{RED}░██░▒██░   ▓██░░▒▓███▀▒{RESET}")
        print(f"{RED}    {MAGENTA}  ▒ ░░   ░░ ▒░ ░▒ ▒▓▒ ▒ ░  ▒ ░░   ▒ ▒▓▒ ▒ ░{RED}░▓  ░ ▒░   ▒ ▒  ░▒   ▒ {RESET}")
        print(f"{CYAN}                            WITH DIVINE UBUNTU ENERGY")
        print(f"{YELLOW}                       {GREEN}JAH BLESS THE CODE{YELLOW} | RASTAFARI VIBRATION{RESET}")
        
        print(f"\n{CYAN}{'='*34} OMEGA TEST RUNNER {'='*33}{RESET}")
        print(f"{GREEN}🌿 Test Categories: {', '.join(self.test_dirs)}{RESET}")
        print(f"{CYAN}🕒 Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
        if self.args.pattern:
            print(f"{MAGENTA}🔍 Test Pattern: {self.args.pattern}{RESET}")
        if self.tags:
            print(f"{YELLOW}🏷️  Test Tags: {', '.join(self.tags)}{RESET}")
        print(f"{YELLOW}🧪 Test Verbose Level: {self.args.verbose}{RESET}")
        
        # Display a random spiritual quote
        quote = random.choice(RASTA_WISDOM)
        print(f"\n{GREEN}RASTA WISDOM:{RESET} {LIGHT_ORANGE}{quote}{RESET}")
        print(f"\n{MAGENTA}{'='*80}{RESET}\n")
    
    def fibonacci_pause(self):
        """Create divine pauses using the Fibonacci sequence."""
        if self.args.rapid:
            return
        
        pause = FIBONACCI[self.fibonacci_idx % len(FIBONACCI)] / 20
        self.fibonacci_idx += 1
        time.sleep(pause)
    
    def display_spinning_meditation(self, cycles=3):
        """Display a spiritual spinning meditation to align energy."""
        if self.args.rapid:
            return
            
        spinner = ["⚡", "🔥", "🌿", "💧", "🌍", "🌟", "🙏"]
        
        # Start with a deep breath moment
        print(f"{CYAN}Aligning test energy", end="", flush=True)
        
        for _ in range(cycles):
            for symbol in spinner:
                time.sleep(0.1)
                print(f"{MAGENTA}{symbol}{RESET}", end="", flush=True)
        
        print(f" {GREEN}ALIGNED!{RESET}")
    
    def run_tests(self):
        """Execute tests with divine guidance and proper energy flow."""
        self.print_banner()
        self.display_spinning_meditation()
        
        # Build pytest command
        cmd = ["pytest"]
        
        # Add verbosity
        if self.args.verbose > 0:
            cmd.append(f"-{'v' * self.args.verbose}")
            
        # Add test pattern if specified
        if self.args.pattern:
            cmd.append(f"-k {self.args.pattern}")
        
        # Add test tags
        if self.tags:
            cmd.append(f"-m {' and '.join(self.tags)}")
        
        # Make sure we're using absolute paths for test directories
        absolute_test_dirs = [os.path.join(project_root, 'omega_ai', 'tests', d) for d in self.test_dirs]
        cmd.extend(absolute_test_dirs)
        
        # Add --color=yes to ensure colored output
        cmd.append("--color=yes")
        
        if self.args.xvs:
            print(f"{GREEN}Running tests with xvs (Extra Verbose Spiritual){RESET}")
            cmd.append("-vv")
            cmd.append("--durations=0")
        
        print(f"{CYAN}Invoking divine test command:{RESET} {' '.join(cmd)}\n")
        
        try:
            # Execute the tests with spiritual energy
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            if process.stdout is None:
                print(f"{RED}Error: Failed to create subprocess output stream{RESET}")
                return 1
            
            # Process the output with Rasta energy visualization
            test_count = 0
            energy_factor = 1.0
            
            for line in process.stdout:
                test_count += self.process_test_line(line)
                
                # Modulate the energy flow
                if "PASSED" in line:
                    self.passed_tests += 1
                    self.bio_energy = min(100, self.bio_energy + 2.0 * energy_factor)
                    print(f"{GREEN}{line.rstrip()}{RESET}")
                    
                elif "FAILED" in line:
                    self.failed_tests += 1
                    self.bio_energy = max(10, self.bio_energy - 5.0 * energy_factor)
                    print(f"{RED}{line.rstrip()}{RESET}")
                    
                elif "SKIPPED" in line:
                    self.skipped_tests += 1
                    print(f"{YELLOW}{line.rstrip()}{RESET}")
                    
                elif "ERROR" in line:
                    self.bio_energy = max(10, self.bio_energy - 8.0 * energy_factor) 
                    print(f"{MAGENTA}{line.rstrip()}{RESET}")
                    
                else:
                    sys_line = self.colorize_output(line)
                    print(sys_line, end="")
                
                # Create divine Fibonacci timing between test outputs
                if test_count > 0 and test_count % 5 == 0:
                    self.fibonacci_pause()
            
            # Wait for process to complete
            return_code = process.wait()
            
            # Display test summary with divine energy
            self.display_test_summary(return_code)
            
            return return_code
            
        except subprocess.SubprocessError as e:
            print(f"{RED}Error running tests: {str(e)}{RESET}")
            return 1
        except Exception as e:
            print(f"{RED}Unexpected error: {str(e)}{RESET}")
            return 1
    
    def process_test_line(self, line: str) -> int:
        """Process a line of test output and update test counts."""
        test_count = 0
        
        if "collected" in line and "items" in line:
            try:
                test_count = int(line.split()[0])
                print(f"{CYAN}{line.rstrip()}{RESET}")
            except ValueError:
                print(f"{YELLOW}{line.rstrip()}{RESET}")
        
        return test_count
    
    def colorize_output(self, line: str) -> str:
        """Add divine colors to test output lines."""
        if "warning" in line.lower():
            return f"{YELLOW}{line}{RESET}"
        elif "error" in line.lower():
            return f"{RED}{line}{RESET}"
        elif "info" in line.lower():
            return f"{CYAN}{line}{RESET}"
        elif "debug" in line.lower():
            return f"{BLUE}{line}{RESET}"
        else:
            return line
    
    def display_test_summary(self, return_code: int):
        """Display a divine summary of test results."""
        duration = time.time() - self.start_time
        print(f"\n{MAGENTA}{'='*80}{RESET}")
        print(f"{CYAN}📊 Test Summary:{RESET}")
        print(f"{GREEN}✅ Passed: {self.passed_tests}{RESET}")
        print(f"{RED}❌ Failed: {self.failed_tests}{RESET}")
        print(f"{YELLOW}⏭️  Skipped: {self.skipped_tests}{RESET}")
        print(f"{BLUE}⏱️  Duration: {duration:.2f}s{RESET}")
        print(f"{MAGENTA}💫 Bio-Energy: {self.bio_energy:.1f}%{RESET}")
        
        if return_code == 0:
            print(f"\n{GREEN}✨ All tests passed with divine harmony! ✨{RESET}")
        else:
            print(f"\n{RED}🔥 Some tests failed - may JAH guide us to fix them! 🔥{RESET}")
        
        print(f"{MAGENTA}{'='*80}{RESET}\n")
    
    def execute(self):
        """Execute the test suite with divine guidance."""
        return_code = self.run_tests()
        self.display_test_summary(return_code)
        return return_code

def main():
    """Main entry point for the divine test runner."""
    parser = argparse.ArgumentParser(description="OMEGA RASTA VIBES TEST RUNNER 🌿🔥")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity level")
    parser.add_argument("-k", "--pattern", help="Run tests matching the given pattern")
    parser.add_argument("-c", "--category", help="Run tests from a specific category")
    parser.add_argument("-d", "--directories", nargs="+", help="Run tests from specific directories")
    parser.add_argument("--rapid", action="store_true", help="Run tests without divine pauses")
    parser.add_argument("--xvs", action="store_true", help="Extra Verbose Spiritual mode")
    parser.add_argument("--tags", help="Comma-separated list of test tags to include")
    parser.add_argument("--skip-tags", help="Comma-separated list of test tags to exclude")
    
    args = parser.parse_args()
    
    runner = OmegaTestRunner(args)
    return runner.run_tests()

if __name__ == "__main__":
    sys.exit(main())