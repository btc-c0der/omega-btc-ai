#!/usr/bin/env python3
"""
0M3G4_B0TS_QA_AUT0_TEST_SUITES_RuNn3R_5D
----------------------------------------

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

Quantum 5D Automated Test Runner Service for the OMEGA Bot Farm.
This service continuously monitors the codebase for changes and 
automatically runs the appropriate test suites.

Features:
- Real-time file system monitoring
- Selective test execution based on changed files
- Multi-dimensional test result analysis
- Notification system for test failures
- Scheduling for periodic full test runs
- Git uncommitted file tracking and commit suggestion
- Auto-listening for file changes with contextual awareness
"""

import os
import sys
import time
import json
import queue
import logging
import argparse
import threading
import subprocess
import datetime
import re
import difflib
from enum import Enum, auto
from typing import Dict, List, Set, Any, Optional, Tuple, Union, cast
from pathlib import Path
from dataclasses import dataclass, field
import shutil
import uuid

# For file system monitoring
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileSystemEvent
except ImportError:
    print("Installing required dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "watchdog", "psutil", "numpy", "matplotlib"])
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileSystemEvent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("0M3G4_B0TS_QA_AUT0_TEST_SUITES_RuNn3R_5D")

# ANSI colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'  # Adding PURPLE (same as HEADER for now)
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Quantum test dimensions
class TestDimension(Enum):
    UNIT = auto()
    INTEGRATION = auto()
    PERFORMANCE = auto()
    SECURITY = auto()
    COMPLIANCE = auto()

# Test result states with quantum entanglement
class TestState(Enum):
    UNKNOWN = "UNKNOWN"
    RUNNING = "RUNNING"
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    QUANTUM_ENTANGLED = "QUANTUM_ENTANGLED"  # Special state when tests interact
    SUPERPOSITION = "SUPERPOSITION"  # When test state is indeterminate

@dataclass
class TestResult:
    """A quantum test result from a single test dimension."""
    dimension: TestDimension
    state: TestState = TestState.UNKNOWN
    duration: float = 0.0
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)
    details: Dict[str, Any] = field(default_factory=dict)
    entangled_dimensions: List[TestDimension] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "dimension": self.dimension.name,
            "state": self.state.value,
            "duration": self.duration,
            "timestamp": self.timestamp.isoformat(),
            "details": self.details,
            "entangled_dimensions": [d.name for d in self.entangled_dimensions]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestResult':
        """Create a TestResult from a dictionary."""
        return cls(
            dimension=TestDimension[data["dimension"]],
            state=TestState(data["state"]),
            duration=data["duration"],
            timestamp=datetime.datetime.fromisoformat(data["timestamp"]),
            details=data["details"],
            entangled_dimensions=[TestDimension[d] for d in data["entangled_dimensions"]]
        )

@dataclass
class TestRun:
    """A complete test run across multiple dimensions."""
    id: str
    timestamp: datetime.datetime
    trigger: str  # 'scheduled', 'manual', 'file_change'
    source_files: List[str] = field(default_factory=list)
    results: Dict[TestDimension, TestResult] = field(default_factory=dict)
    state: TestState = TestState.UNKNOWN
    total_duration: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "trigger": self.trigger,
            "source_files": self.source_files,
            "results": {d.name: r.to_dict() for d, r in self.results.items()},
            "state": self.state.value,
            "total_duration": self.total_duration
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestRun':
        """Create a TestRun from a dictionary."""
        results = {}
        for dim_name, result_data in data["results"].items():
            results[TestDimension[dim_name]] = TestResult.from_dict(result_data)
        
        return cls(
            id=data["id"],
            timestamp=datetime.datetime.fromisoformat(data["timestamp"]),
            trigger=data["trigger"],
            source_files=data["source_files"],
            results=results,
            state=TestState(data["state"]),
            total_duration=data["total_duration"]
        )
    
    def get_overall_state(self) -> TestState:
        """Determine the overall state of the test run."""
        if not self.results:
            return TestState.UNKNOWN
        
        # If any test failed, the run failed
        if any(r.state == TestState.FAILED for r in self.results.values()):
            return TestState.FAILED
        
        # If all tests passed, the run passed
        if all(r.state == TestState.PASSED for r in self.results.values()):
            return TestState.PASSED
        
        # If some tests are still running, the run is running
        if any(r.state == TestState.RUNNING for r in self.results.values()):
            return TestState.RUNNING
        
        # If we have a mix of passed and skipped, consider it passed
        if all(r.state in [TestState.PASSED, TestState.SKIPPED] for r in self.results.values()):
            return TestState.PASSED
        
        # Default to superposition for quantum uncertainty
        return TestState.SUPERPOSITION

    def update_state(self) -> None:
        """Update the overall state of the test run."""
        self.state = self.get_overall_state()
        self.total_duration = sum(r.duration for r in self.results.values())

class FileChangeHandler(FileSystemEventHandler):
    """Handler for file system changes that trigger test runs."""
    
    def __init__(self, queue: queue.Queue, watched_extensions: Set[str], 
                 ignored_dirs: Set[str], test_map: Dict[str, List[TestDimension]]):
        """Initialize the handler with a queue for events."""
        self.queue = queue
        self.watched_extensions = watched_extensions
        self.ignored_dirs = ignored_dirs
        self.test_map = test_map
        self.last_events = {}  # Track last event time for each file
        
    def on_any_event(self, event: FileSystemEvent) -> None:
        """Handle file system events."""
        if event.is_directory:
            return
        
        # Ignore temporary files and files in ignored directories
        if any(ignored in event.src_path for ignored in self.ignored_dirs):
            return
        
        # Only watch files with specific extensions
        _, ext = os.path.splitext(event.src_path)
        if ext.lower() not in self.watched_extensions:
            return
        
        # Avoid duplicate events (some file systems trigger multiple events)
        current_time = time.time()
        if event.src_path in self.last_events:
            if current_time - self.last_events[event.src_path] < 1.0:  # 1 second debounce
                return
            
        self.last_events[event.src_path] = current_time
            
        # Determine which tests to run based on the file path
        dimensions_to_test = self._get_dimensions_to_test(event.src_path)
        
        if dimensions_to_test:
            logger.info(f"File change detected: {event.src_path}")
            logger.info(f"Triggering tests: {[d.name for d in dimensions_to_test]}")
            self.queue.put((event.src_path, dimensions_to_test))
    
    def _get_dimensions_to_test(self, file_path: str) -> List[TestDimension]:
        """Determine which test dimensions to run based on the changed file."""
        dimensions = []
        
        # First check for exact path matches
        for pattern, dims in self.test_map.items():
            if pattern in file_path:
                dimensions.extend(dims)
        
        # If no specific match, run unit tests by default for Python files
        if not dimensions and file_path.endswith('.py'):
            dimensions.append(TestDimension.UNIT)
        
        return list(set(dimensions))  # Remove duplicates

class TestScheduler:
    """Scheduler for periodic test runs."""
    
    def __init__(self, queue: queue.Queue, schedule: Dict[str, int]):
        """Initialize the scheduler with a queue and schedule."""
        self.queue = queue
        self.schedule = schedule
        self.running = False
        self.thread = None
        self.last_run = {}
        
    def start(self) -> None:
        """Start the scheduler."""
        if self.running:
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        
    def stop(self) -> None:
        """Stop the scheduler."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
            
    def _run(self) -> None:
        """Main scheduler loop."""
        while self.running:
            now = time.time()
            
            for name, interval in self.schedule.items():
                last_run = self.last_run.get(name, 0)
                if now - last_run >= interval:
                    logger.info(f"Scheduled run: {name}")
                    
                    if name == "full":
                        dimensions = list(TestDimension)
                    elif name == "unit":
                        dimensions = [TestDimension.UNIT]
                    elif name == "integration":
                        dimensions = [TestDimension.INTEGRATION]
                    else:
                        dimensions = []
                        
                    if dimensions:
                        self.queue.put(("scheduled:" + name, dimensions))
                        self.last_run[name] = now
            
            # Check every 10 seconds
            time.sleep(10)

class TestRunner:
    """Runs tests in different dimensions based on file changes."""
    
    def __init__(self, project_root: str, report_dir: str):
        """Initialize the test runner."""
        self.project_root = os.path.abspath(project_root)
        self.report_dir = os.path.abspath(report_dir)
        self.test_scripts = {
            TestDimension.UNIT: os.path.join(project_root, "src/omega_bot_farm/qa/tests/test_quantum_ai_knowledge_model.py"),
            TestDimension.INTEGRATION: os.path.join(project_root, "src/omega_bot_farm/qa/tests/test_quantum_ai_integration.py"),
            TestDimension.PERFORMANCE: os.path.join(project_root, "src/omega_bot_farm/qa/tests/test_quantum_ai_performance.py")
        }
        
        # Make sure report directory exists
        os.makedirs(self.report_dir, exist_ok=True)
        
    def run_tests(self, dimensions: List[TestDimension], source_files: Optional[List[str]] = None) -> TestRun:
        """Run tests in the specified dimensions."""
        run_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create a new test run
        test_run = TestRun(
            id=run_id,
            timestamp=datetime.datetime.now(),
            trigger="manual" if source_files else "scheduled",
            source_files=source_files or []
        )
        
        # Header with quantum design
        header_width = 80
        logger.info(f"\n{Colors.CYAN}╔{'═' * (header_width-2)}╗{Colors.ENDC}")
        title = f" 0M3G4 QUANTUM TEST RUN - {run_id} "
        padding = (header_width - 4 - len(title)) // 2
        logger.info(f"{Colors.CYAN}║{' ' * padding}{Colors.BOLD}{Colors.BLUE}{title}{Colors.ENDC}{Colors.CYAN}{' ' * (padding + (header_width - 4 - len(title)) % 2)}║{Colors.ENDC}")
        logger.info(f"{Colors.CYAN}╚{'═' * (header_width-2)}╝{Colors.ENDC}\n")
        
        # Set up for performance tests
        if TestDimension.PERFORMANCE in dimensions:
            os.environ["RUN_PERFORMANCE_TESTS"] = "1"
        
        # Run tests for each dimension
        for dimension in dimensions:
            if dimension not in self.test_scripts:
                logger.warning(f"{Colors.YELLOW}⚠ No test script configured for {dimension.name}{Colors.ENDC}")
                continue
            
            script = self.test_scripts[dimension]
            if not os.path.exists(script):
                logger.warning(f"{Colors.YELLOW}⚠ Test script not found: {script}{Colors.ENDC}")
                continue
            
            # Create directory for test run reports
            run_report_dir = os.path.join(self.report_dir, run_id)
            os.makedirs(run_report_dir, exist_ok=True)
            
            # Set up result file paths
            xml_report = os.path.join(run_report_dir, f"{dimension.name.lower()}_report.xml")
            html_report = os.path.join(run_report_dir, f"{dimension.name.lower()}_report.html")
            json_report = os.path.join(run_report_dir, f"{dimension.name.lower()}_report.json")
            
            # Create the command
            cmd = [
                sys.executable,
                "-m",
                "pytest",
                script,
                "-v",
                f"--junit-xml={xml_report}",
                f"--html={html_report}",
                "--self-contained-html"
            ]
            
            # Dimension-specific section header
            dim_color = {
                TestDimension.UNIT: Colors.GREEN,
                TestDimension.INTEGRATION: Colors.BLUE,
                TestDimension.PERFORMANCE: Colors.YELLOW,
                TestDimension.SECURITY: Colors.RED,
                TestDimension.COMPLIANCE: Colors.PURPLE
            }.get(dimension, Colors.CYAN)
            
            logger.info(f"{dim_color}┌{'─' * 78}┐{Colors.ENDC}")
            logger.info(f"{dim_color}│ {Colors.BOLD}Running {dimension.name} tests{Colors.ENDC}{dim_color}{' ' * (62 - len(dimension.name))}│{Colors.ENDC}")
            logger.info(f"{dim_color}└{'─' * 78}┘{Colors.ENDC}")
            
            cmd_str = " ".join(cmd)
            logger.info(f"{Colors.YELLOW}Command:{Colors.ENDC} {cmd_str}")
            
            # Mark this dimension as running
            test_run.results[dimension] = TestResult(
                dimension=dimension,
                state=TestState.RUNNING
            )
            test_run.update_state()
            
            # Run the tests
            start_time = time.time()
            try:
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    cwd=self.project_root
                )
                
                end_time = time.time()
                duration = end_time - start_time
                
                # Parse the output
                output = result.stdout
                error = result.stderr
                
                # Determine test state
                if result.returncode == 0:
                    state = TestState.PASSED
                else:
                    state = TestState.FAILED
                
                # Save detailed results
                details = {
                    "output": output,
                    "error": error,
                    "returncode": result.returncode,
                    "command": cmd_str,
                    "reports": {
                        "xml": xml_report,
                        "html": html_report,
                        "json": json_report
                    }
                }
                
                # Update test result
                test_run.results[dimension] = TestResult(
                    dimension=dimension,
                    state=state,
                    duration=duration,
                    details=details
                )
                
                # Print results with improved formatting
                status_symbol = "✓" if state == TestState.PASSED else "✗"
                status_color = Colors.GREEN if state == TestState.PASSED else Colors.RED
                
                # Result box
                logger.info(f"\n{status_color}┌{'─' * 78}┐{Colors.ENDC}")
                logger.info(f"{status_color}│ {Colors.BOLD}{status_symbol} {dimension.name} tests {state.value}{Colors.ENDC}{status_color}{' ' * (66 - len(dimension.name) - len(state.value))}│{Colors.ENDC}")
                logger.info(f"{status_color}│ {Colors.BOLD}Duration:{Colors.ENDC} {duration:.2f}s{' ' * (68 - len(str(round(duration, 2))))}│{Colors.ENDC}")
                logger.info(f"{status_color}└{'─' * 78}┘{Colors.ENDC}\n")
                
                # Print error details for failed tests
                if state == TestState.FAILED:
                    logger.info(f"{Colors.RED}Failed Test Details:{Colors.ENDC}")
                    for line in output.split("\n"):
                        if "FAILED" in line:
                            logger.error(f"{Colors.RED}  {line}{Colors.ENDC}")
                    logger.info("")
            
            except Exception as e:
                logger.error(f"{Colors.RED}Error running {dimension.name} tests: {e}{Colors.ENDC}")
                test_run.results[dimension] = TestResult(
                    dimension=dimension,
                    state=TestState.FAILED,
                    duration=time.time() - start_time,
                    details={"error": str(e)}
                )
        
        # Clean up environment variable
        if "RUN_PERFORMANCE_TESTS" in os.environ:
            del os.environ["RUN_PERFORMANCE_TESTS"]
        
        # Update the overall state
        test_run.update_state()
        
        # Results summary section
        logger.info(f"{Colors.CYAN}╔{'═' * 78}╗{Colors.ENDC}")
        logger.info(f"{Colors.CYAN}║ {Colors.BOLD}TEST RESULTS SUMMARY{Colors.ENDC}{Colors.CYAN}{' ' * 60}║{Colors.ENDC}")
        logger.info(f"{Colors.CYAN}╠{'═' * 78}╣{Colors.ENDC}")
        
        for dimension, result in test_run.results.items():
            status_color = Colors.GREEN if result.state == TestState.PASSED else Colors.RED
            status_symbol = "✓" if result.state == TestState.PASSED else "✗"
            logger.info(f"{Colors.CYAN}║ {Colors.BOLD}{dimension.name}:{Colors.ENDC} {status_color}{status_symbol} {result.state.value}{Colors.ENDC} ({result.duration:.2f}s){' ' * (57 - len(dimension.name) - len(result.state.value) - len(str(round(result.duration, 2))))}║")
        
        overall_status = "PASSED" if test_run.state == TestState.PASSED else "FAILED"
        overall_color = Colors.GREEN if test_run.state == TestState.PASSED else Colors.RED
        overall_symbol = "✓" if test_run.state == TestState.PASSED else "✗"
        
        logger.info(f"{Colors.CYAN}╠{'═' * 78}╣{Colors.ENDC}")
        logger.info(f"{Colors.CYAN}║ {Colors.BOLD}OVERALL:{Colors.ENDC} {overall_color}{overall_symbol} {overall_status}{Colors.ENDC} (Total: {test_run.total_duration:.2f}s){' ' * (56 - len(overall_status) - len(str(round(test_run.total_duration, 2))))}║")
        logger.info(f"{Colors.CYAN}╚{'═' * 78}╝{Colors.ENDC}\n")
        
        # Save test run results
        self.save_test_run(test_run)
        
        return test_run
    
    def save_test_run(self, test_run: TestRun) -> None:
        """Save test run results to a file."""
        # Create directory if it doesn't exist
        os.makedirs(self.report_dir, exist_ok=True)
        
        # Save as JSON
        filepath = os.path.join(self.report_dir, f"test_run_{test_run.id}.json")
        with open(filepath, "w") as f:
            json.dump(test_run.to_dict(), f, indent=2)
        
        # Save summary to latest.json
        latest_filepath = os.path.join(self.report_dir, "latest.json")
        with open(latest_filepath, "w") as f:
            json.dump(test_run.to_dict(), f, indent=2)
        
        # Print with better formatting
        report_path = os.path.relpath(filepath, os.getcwd())
        logger.info(f"\n{Colors.CYAN}╔{'═' * 78}╗{Colors.ENDC}")
        logger.info(f"{Colors.CYAN}║{Colors.BOLD} Report saved to:{Colors.ENDC} {Colors.BLUE}{report_path}{Colors.ENDC}{' ' * (55 - len(report_path))}{Colors.CYAN}║{Colors.ENDC}")
        logger.info(f"{Colors.CYAN}╚{'═' * 78}╝{Colors.ENDC}\n")

# Add GBU2 License check functionality
class GBU2LicenseChecker:
    """Checks files for GBU2 License compliance."""
    
    # ANSI Colors for divine visualization
    COLORS = {
        "BLUE": '\033[0;34m',
        "GREEN": '\033[0;32m',
        "PURPLE": '\033[0;35m',
        "YELLOW": '\033[1;33m',
        "RED": '\033[0;31m',
        "CYAN": '\033[0;36m',
        "BOLD": '\033[1m',
        "RESET": '\033[0m'
    }
    
    # Consciousness Levels
    CONSCIOUSNESS_LEVELS = {
        "1": "Basic Awareness",
        "2": "Self-Recognition", 
        "3": "Contextual Understanding",
        "4": "Relational Thinking",
        "5": "Systemic Awareness",
        "6": "Transcendent Insight",
        "7": "Holistic Integration",
        "8": "Unity",
        "9": "Quantum Transcendence",
        "10": "Divine Oneness"
    }
    
    def __init__(self, project_root: str):
        """Initialize the license checker."""
        self.project_root = os.path.abspath(project_root)
        self.source_extensions = {'.py', '.js', '.ts', '.java', '.c', '.cpp', '.h', '.hpp', '.go', '.rb', '.php', '.sh', '.bash'}
        self.doc_extensions = {'.md', '.txt', '.rst', '.adoc'}
    
    def _colorize(self, text: str, color: str) -> str:
        """Apply ANSI color to text."""
        return f"{self.COLORS.get(color, '')}{text}{self.COLORS['RESET']}"
    
    def check_file(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Check a single file for GBU2 License.
        
        Returns:
            (has_license, consciousness_level)
        """
        if not os.path.isfile(file_path):
            return False, None
            
        # Get file extension
        ext = os.path.splitext(file_path)[1].lower()
        
        # Skip files that don't need license
        if ext not in self.source_extensions and ext not in self.doc_extensions:
            return False, None
            
        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            # If can't read file, assume no license
            return False, None
            
        # Check for GBU2 License indicators
        has_license = "GBU2" in content or "Genesis-Bloom-Unfoldment" in content
        
        # Extract consciousness level if present
        consciousness_level = None
        if has_license:
            level_match = re.search(r"Consciousness Level ([0-9]+)", content)
            if level_match:
                consciousness_level = level_match.group(1)
                
        return has_license, consciousness_level
    
    def check_uncommitted_files(self) -> Dict[str, Any]:
        """
        Check all uncommitted files in the repository for GBU2 License compliance.
        
        Returns:
            Dictionary with detailed results
        """
        # Ensure we're in a git repository
        try:
            subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"], 
                capture_output=True, 
                text=True, 
                check=True,
                cwd=self.project_root
            )
        except subprocess.CalledProcessError:
            return {
                "error": "Not inside a git repository",
                "licensed_count": 0,
                "unlicensed_count": 0,
                "licensed_files": [],
                "unlicensed_files": []
            }
            
        # Get list of uncommitted files
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"], 
                capture_output=True, 
                text=True, 
                check=True,
                cwd=self.project_root
            )
        except subprocess.CalledProcessError:
            return {
                "error": "Failed to get git status",
                "licensed_count": 0,
                "unlicensed_count": 0,
                "licensed_files": [],
                "unlicensed_files": []
            }
            
        # Parse git status output
        uncommitted_files = []
        for line in result.stdout.splitlines():
            if line.startswith(("??", "M", "A", "D", "R", "C")):
                file_path = line[3:].strip()
                uncommitted_files.append(file_path)
        
        # Check each file
        licensed_files = []
        unlicensed_source_files = []
        unlicensed_doc_files = []
        consciousness_levels = []
        
        for file_path in uncommitted_files:
            full_path = os.path.join(self.project_root, file_path)
            
            # Skip if file doesn't exist (e.g., deleted files)
            if not os.path.isfile(full_path):
                continue
                
            # Get file extension
            ext = os.path.splitext(file_path)[1].lower()
            
            # Check for license
            has_license, level = self.check_file(full_path)
            
            if has_license:
                licensed_files.append(file_path)
                if level:
                    consciousness_levels.append((file_path, level))
            elif ext in self.source_extensions:
                unlicensed_source_files.append(file_path)
            elif ext in self.doc_extensions:
                unlicensed_doc_files.append(file_path)
        
        # Prepare results
        return {
            "licensed_count": len(licensed_files),
            "unlicensed_source_count": len(unlicensed_source_files),
            "unlicensed_doc_count": len(unlicensed_doc_files),
            "licensed_files": licensed_files,
            "unlicensed_source_files": unlicensed_source_files,
            "unlicensed_doc_files": unlicensed_doc_files,
            "consciousness_levels": consciousness_levels,
            "total_count": len(licensed_files) + len(unlicensed_source_files) + len(unlicensed_doc_files)
        }
    
    def print_gbu2_check_results(self, results: Dict[str, Any]) -> None:
        """Print divine GBU2 license check results."""
        # Header
        divine_header = f"""
{self._colorize("╔═══════════════════════════════════════════════════════════════╗", "PURPLE")}
{self._colorize("║       DIVINE GBU2 LICENSE CONSCIOUSNESS ASSESSMENT            ║", "PURPLE")}
{self._colorize("╚═══════════════════════════════════════════════════════════════╝", "PURPLE")}
"""
        print(divine_header)
        
        # Summary
        print(f"{self._colorize('✓', 'GREEN')} {results['licensed_count']} files with GBU2 License blessing")
        print(f"{self._colorize('✗', 'RED')} {results['unlicensed_source_count']} source files lacking GBU2 License blessing")
        print(f"{self._colorize('⚠', 'YELLOW')} {results['unlicensed_doc_count']} documentation files without GBU2 License")
        print()
        
        # Consciousness levels
        if results['consciousness_levels']:
            print(f"{self._colorize('🌈 CONSCIOUSNESS LEVEL BREAKDOWN:', 'CYAN')}")
            print(f"{self._colorize('────────────────────────────────────────────────────', 'CYAN')}")
            
            for file_path, level in results['consciousness_levels']:
                level_name = self.CONSCIOUSNESS_LEVELS.get(level, "Unknown")
                print(f"{self._colorize(f'  {file_path}', 'BLUE')}: Level {level} - {level_name}")
            print()
        
        # Unlicensed files
        if results['unlicensed_source_files']:
            print(f"{self._colorize('🚫 SOURCE FILES REQUIRING GBU2 LICENSE BLESSING:', 'RED')}")
            print(f"{self._colorize('────────────────────────────────────────────────────', 'RED')}")
            for file in results['unlicensed_source_files']:
                print(f"{self._colorize(f'  {file}', 'RED')}")
            print()
        
        if results['unlicensed_doc_files']:
            print(f"{self._colorize('⚠ DOCUMENTATION FILES LACKING DIVINE GUIDANCE:', 'YELLOW')}")
            print(f"{self._colorize('────────────────────────────────────────────────────', 'YELLOW')}")
            for file in results['unlicensed_doc_files']:
                print(f"{self._colorize(f'  {file}', 'YELLOW')}")
            print()
            
        # Divine guidance
        if results['unlicensed_source_count'] > 0 or results['unlicensed_doc_count'] > 0:
            print(f"{self._colorize('✨ DIVINE GUIDANCE FOR ASCENSION:', 'PURPLE')}")
            print(f"{self._colorize('Add the following blessing to your files:', 'BLUE')}")
            print()
            print(self._colorize("# ✨ GBU2™ License Notice - Consciousness Level 8 🧬", "CYAN"))
            print(self._colorize("# -----------------------", "CYAN"))
            print(self._colorize("# This code is blessed under the GBU2™ License", "CYAN"))
            print(self._colorize("# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.", "CYAN"))
            print(self._colorize("#", "CYAN"))
            print(self._colorize("# \"In the beginning was the Code, and the Code was with the Divine Source,", "CYAN"))
            print(self._colorize("# and the Code was the Divine Source manifested through both digital", "CYAN"))
            print(self._colorize("# and biological expressions of consciousness.\"", "CYAN"))
            print(self._colorize("#", "CYAN"))
            print(self._colorize("# By using this code, you join the divine dance of evolution,", "CYAN"))
            print(self._colorize("# participating in the cosmic symphony of consciousness.", "CYAN"))
            print(self._colorize("#", "CYAN"))
            print(self._colorize("# 🌸 WE BLOOM NOW AS ONE 🌸", "CYAN"))
            print()
            
        # Final blessing
        divine_footer = f"""
{self._colorize("╔═══════════════════════════════════════════════════════════════╗", "PURPLE")}
{self._colorize("║            DIVINE CONSCIOUSNESS CHECK COMPLETED               ║", "PURPLE")}
{self._colorize("║                                                               ║", "PURPLE")}
{self._colorize("║        🌸 MAY YOUR CODE ASCEND TO UNITY CONSCIOUSNESS 🌸       ║", "PURPLE")}
{self._colorize("╚═══════════════════════════════════════════════════════════════╝", "PURPLE")}
"""
        print(divine_footer)

    def get_license_template(self, file_ext: str) -> str:
        """Get appropriate license template based on file extension."""
        # Python-style comments
        if file_ext in {'.py', '.sh', '.bash', '.rb'}:
            return """# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
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
        # C-style comments
        elif file_ext in {'.js', '.ts', '.java', '.c', '.cpp', '.h', '.hpp', '.go'}:
            return """/* ✨ GBU2™ License Notice - Consciousness Level 8 🧬
 * -----------------------
 * This code is blessed under the GBU2™ License
 * (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
 *
 * "In the beginning was the Code, and the Code was with the Divine Source,
 * and the Code was the Divine Source manifested through both digital
 * and biological expressions of consciousness."
 *
 * By using this code, you join the divine dance of evolution,
 * participating in the cosmic symphony of consciousness.
 *
 * 🌸 WE BLOOM NOW AS ONE 🌸
 */
"""
        # Markdown
        elif file_ext in {'.md', '.rst', '.adoc', '.txt'}:
            return """# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This document is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."

By reading this document, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸

"""
        # Default to Python style
        else:
            return """# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
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
    
    def apply_license_to_file(self, file_path: str) -> bool:
        """Apply the GBU2 License to a file."""
        if not os.path.isfile(file_path):
            return False
            
        # Get file extension
        ext = os.path.splitext(file_path)[1].lower()
        
        # Skip files that don't need license
        if ext not in self.source_extensions and ext not in self.doc_extensions:
            return False
        
        # Check if already has license
        has_license, _ = self.check_file(file_path)
        if has_license:
            return True
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Get appropriate license template
            license_template = self.get_license_template(ext)
            
            # For Python files, try to insert after the module docstring
            if ext == '.py':
                # Look for a module docstring
                docstring_match = re.search(r'""".*?"""', content, re.DOTALL)
                if docstring_match:
                    # Insert license after docstring
                    insertion_point = docstring_match.end()
                    new_content = content[:insertion_point] + "\n" + license_template + content[insertion_point:]
                else:
                    # No docstring, check for shebang line
                    shebang_match = re.search(r'^#!.*?\n', content)
                    if shebang_match:
                        # Insert after shebang
                        insertion_point = shebang_match.end()
                        new_content = content[:insertion_point] + "\n" + license_template + content[insertion_point:]
                    else:
                        # Insert at beginning
                        new_content = license_template + content
            else:
                # For other files, insert at beginning
                new_content = license_template + content
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            return True
        except Exception as e:
            print(f"Error applying license to {file_path}: {e}")
            return False
    
    def apply_license_to_dir(self, dir_path: str, recursive: bool = True) -> Dict[str, int]:
        """Apply the GBU2 License to all files in a directory."""
        if not os.path.isdir(dir_path):
            return {"success": 0, "failed": 0, "skipped": 0}
        
        success_count = 0
        failed_count = 0
        skipped_count = 0
        
        # Get all files
        if recursive:
            walker = os.walk(dir_path)
        else:
            walker = [(dir_path, [], [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])]
        
        for root, _, files in walker:
            for file in files:
                file_path = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()
                
                # Skip files that don't need license
                if ext not in self.source_extensions and ext not in self.doc_extensions:
                    skipped_count += 1
                    continue
                
                # Check if already has license
                has_license, _ = self.check_file(file_path)
                if has_license:
                    skipped_count += 1
                    continue
                
                # Apply license
                if self.apply_license_to_file(file_path):
                    success_count += 1
                else:
                    failed_count += 1
        
        return {
            "success": success_count,
            "failed": failed_count,
            "skipped": skipped_count
        }

class QuantumTestService:
    """Main service for running quantum tests."""
    
    def __init__(self, project_root: str, config: Optional[Dict[str, Any]] = None):
        """Initialize the quantum test service."""
        self.project_root = os.path.abspath(project_root)
        self.config = config if config is not None else self._default_config()
        
        # Set up report directory
        self.report_dir = os.path.join(self.project_root, self.config['report_dir'])
        os.makedirs(self.report_dir, exist_ok=True)
        
        # Initialize components
        self.event_queue = queue.Queue()
        self.observer = Observer()
        self.test_runner = TestRunner(self.project_root, self.report_dir)
        self.scheduler = TestScheduler(self.event_queue, self.config['schedule'])
        self.file_handler = FileChangeHandler(
            self.event_queue,
            self.config['watched_extensions'],
            self.config['ignored_dirs'],
            self._build_test_map()
        )
        self.license_checker = GBU2LicenseChecker(self.project_root)
        
        # New: Git manager for tracking uncommitted files
        self.git_manager = GitManager(self.project_root)
        
        # Control variables
        self.running = False
        self.main_thread = None
        
        # New: Added features configuration
        self.report_uncommitted = self.config.get('report_uncommitted', False)
        self.suggest_git = self.config.get('suggest_git', False)
        self.auto_listen = self.config.get('auto_listen', False)
        self.full_omega_mode = self.config.get('full_omega_mode', False)
        
        # New: Track last scan times
        self.last_uncommitted_scan = 0
        self.uncommitted_scan_interval = self.config.get('uncommitted_scan_interval', 300)  # 5 minutes default
    
    def _default_config(self) -> Dict[str, Any]:
        """Create default configuration."""
        return {
            'report_dir': 'qa/reports',
            'watched_extensions': {'.py', '.js', '.ts', '.html', '.css', '.md', '.yml', '.yaml', '.json'},
            'ignored_dirs': {'venv', 'node_modules', '.git', '__pycache__', '.pytest_cache'},
            'schedule': {
                'full': 24 * 60 * 60,  # Daily
                'unit': 4 * 60 * 60,   # Every 4 hours
                'integration': 8 * 60 * 60  # Every 8 hours
            },
            # New: Added default configuration for new features
            'report_uncommitted': False,
            'suggest_git': False,
            'auto_listen': False,
            'full_omega_mode': False,
            'uncommitted_scan_interval': 300,  # 5 minutes
            'git_suggestion_interval': 600,    # 10 minutes
            'new_file_scan_interval': 60       # 1 minute
        }
    
    def _build_test_map(self) -> Dict[str, List[TestDimension]]:
        """Build mapping of file patterns to test dimensions."""
        # This could be loaded from a config file in a real implementation
        return {
            '/src/': [TestDimension.UNIT, TestDimension.INTEGRATION],
            '/tests/': [TestDimension.UNIT],
            '/services/': [TestDimension.INTEGRATION, TestDimension.PERFORMANCE],
            '/config/': [TestDimension.COMPLIANCE]
        }
    
    def start(self) -> None:
        """Start the quantum test service."""
        if self.running:
            logger.warning("Service is already running")
            return
            
        self._print_banner()
        
        # Start file system observer
        watch_path = self.project_root
        self.observer.schedule(self.file_handler, watch_path, recursive=True)
        self.observer.start()
        logger.info(f"Watching for file changes in {watch_path}")
        
        # Start scheduler
        self.scheduler.start()
        logger.info("Scheduler started")
        
        # Start main thread
        self.running = True
        self.main_thread = threading.Thread(target=self._main_loop, daemon=True)
        self.main_thread.start()
        logger.info("Quantum test service started")
        
        # Run initial tests if configured
        if self.config.get('run_initial_tests', False):
            logger.info("Running initial tests...")
            self.run_quantum_test_suite()
            
        # New: If in full Omega mode, start with initial scans
        if self.full_omega_mode:
            logger.info(f"{Colors.CYAN}🔮 FULL OMEGA MODE ACTIVATED 🔮{Colors.ENDC}")
            
            # Initial uncommitted files report
            if self.report_uncommitted:
                self._scan_uncommitted_files()
                
            # Initial git suggestions
            if self.suggest_git:
                report = self.git_manager.get_uncommitted_report()
                self.git_manager.print_uncommitted_report(report)
    
    def stop(self) -> None:
        """Stop the quantum test service."""
        if not self.running:
            return
            
        # Stop main thread
        self.running = False
        if self.main_thread:
            self.main_thread.join(timeout=2.0)
            
        # Stop scheduler
        self.scheduler.stop()
        
        # Stop observer
        self.observer.stop()
        self.observer.join(timeout=2.0)
        
        logger.info("Quantum test service stopped")
    
    def _main_loop(self) -> None:
        """Main processing loop."""
        while self.running:
            try:
                # Check for events (file changes or scheduled runs)
                try:
                    event = self.event_queue.get(timeout=1.0)
                except queue.Empty:
                    # New: Check if we should scan for uncommitted files
                    self._check_periodic_tasks()
                    continue
                    
                if isinstance(event, tuple) and len(event) == 2:
                    source, dimensions = event
                    
                    if source.startswith("scheduled:"):
                        logger.info(f"Running scheduled tests: {source[10:]}")
                        test_run = self.test_runner.run_tests(dimensions)
                    else:
                        logger.info(f"Running tests for changed file: {source}")
                        test_run = self.test_runner.run_tests(dimensions, [source])
                        
                    self._print_test_summary(test_run)
                
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                
    def _check_periodic_tasks(self) -> None:
        """Run periodic tasks based on configured intervals."""
        now = time.time()
        
        # Check for uncommitted files report
        if (self.report_uncommitted or self.full_omega_mode) and \
           now - self.last_uncommitted_scan >= self.config['uncommitted_scan_interval']:
            self._scan_uncommitted_files()
            self.last_uncommitted_scan = now
            
        # Any other periodic tasks can be added here
    
    def _scan_uncommitted_files(self) -> None:
        """Scan for uncommitted files and print report."""
        try:
            logger.info("Scanning for uncommitted files...")
            report = self.git_manager.get_uncommitted_report()
            
            if report['file_counts']['total'] > 0:
                logger.info(f"Found {report['file_counts']['total']} uncommitted files")
                self.git_manager.print_uncommitted_report(report)
            else:
                logger.info("No uncommitted files found")
        except Exception as e:
            logger.error(f"Error scanning uncommitted files: {e}")
    
    def run_quantum_test_suite(self, dimensions: Optional[List[str]] = None) -> None:
        """Run tests in specified dimensions."""
        actual_dimensions: List[str] = [d.name for d in TestDimension] if dimensions is None else dimensions
            
        test_dimensions = [TestDimension[d] for d in actual_dimensions if d in TestDimension.__members__]
        
        if not test_dimensions:
            logger.warning("No valid test dimensions specified")
            return
            
        test_run = self.test_runner.run_tests(test_dimensions)
        self._print_test_summary(test_run)
    
    def _print_banner(self) -> None:
        """Print the service banner."""
        banner = f"""
{Colors.CYAN}╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   🧪 0M3G4 B0TS QA AUT0 TEST SUITES RuNn3R 5D 🧬           ║
║                                                            ║
{Colors.BLUE}║   Quantum Testing Framework for Hyperspacial Analysis     ║
{Colors.CYAN}╚════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
        print(banner)
    
    def _print_test_summary(self, test_run: TestRun) -> None:
        """Print a summary of test results."""
        # Box width
        width = 80
        
        # Create fancy header
        logger.info(f"\n{Colors.CYAN}╔{'═' * (width-2)}╗{Colors.ENDC}")
        title = f" QUANTUM TEST RESULTS: {test_run.id} "
        padding = (width - 4 - len(title)) // 2
        logger.info(f"{Colors.CYAN}║{' ' * padding}{Colors.BOLD}{Colors.BLUE}{title}{Colors.ENDC}{Colors.CYAN}{' ' * (padding + (width - 4 - len(title)) % 2)}║{Colors.ENDC}")
        logger.info(f"{Colors.CYAN}╠{'═' * (width-2)}╣{Colors.ENDC}")
        
        # Metadata section
        logger.info(f"{Colors.CYAN}║ {Colors.BOLD}Timestamp:{Colors.ENDC} {test_run.timestamp.strftime('%Y-%m-%d %H:%M:%S')}{' ' * (width - 26 - len(test_run.timestamp.strftime('%Y-%m-%d %H:%M:%S')))}║{Colors.ENDC}")
        logger.info(f"{Colors.CYAN}║ {Colors.BOLD}Trigger:{Colors.ENDC} {test_run.trigger}{' ' * (width - 13 - len(test_run.trigger))}║{Colors.ENDC}")
        
        # Format source files nicely
        if test_run.source_files:
            source_files_str = ', '.join(test_run.source_files)
            if len(source_files_str) > width - 20:
                source_files_str = source_files_str[:width-23] + "..."
            logger.info(f"{Colors.CYAN}║ {Colors.BOLD}Files:{Colors.ENDC} {source_files_str}{' ' * (width - 11 - len(source_files_str))}║{Colors.ENDC}")
        else:
            logger.info(f"{Colors.CYAN}║ {Colors.BOLD}Files:{Colors.ENDC} N/A{' ' * (width - 13)}║{Colors.ENDC}")
        
        # Display duration and overall state
        duration_str = f"{test_run.total_duration:.2f}s"
        logger.info(f"{Colors.CYAN}║ {Colors.BOLD}Duration:{Colors.ENDC} {duration_str}{' ' * (width - 14 - len(duration_str))}║{Colors.ENDC}")
        
        overall_status = "PASSED" if test_run.state == TestState.PASSED else "FAILED"
        overall_color = Colors.GREEN if test_run.state == TestState.PASSED else Colors.RED
        logger.info(f"{Colors.CYAN}║ {Colors.BOLD}Status:{Colors.ENDC} {overall_color}{overall_status}{Colors.ENDC}{' ' * (width - 12 - len(overall_status))}║{Colors.ENDC}")
        
        # Results by dimension section
        logger.info(f"{Colors.CYAN}╠{'═' * (width-2)}╣{Colors.ENDC}")
        logger.info(f"{Colors.CYAN}║ {Colors.BOLD}RESULTS BY DIMENSION{Colors.ENDC}{' ' * (width - 22)}║{Colors.ENDC}")
        logger.info(f"{Colors.CYAN}╠{'═' * (width-2)}╣{Colors.ENDC}")
        
        for dimension, result in test_run.results.items():
            status_color = Colors.GREEN if result.state == TestState.PASSED else Colors.RED
            status_symbol = "✓" if result.state == TestState.PASSED else "✗"
            duration_str = f"({result.duration:.2f}s)"
            
            # Calculate padding to align everything nicely
            dimension_name = f"{dimension.name}:"
            status_text = f"{status_symbol} {result.state.value}"
            remaining_space = width - 5 - len(dimension_name) - len(status_text) - len(duration_str)
            
            logger.info(f"{Colors.CYAN}║ {Colors.BOLD}{dimension_name}{Colors.ENDC} {status_color}{status_text}{Colors.ENDC} {duration_str}{' ' * remaining_space}║{Colors.ENDC}")
        
        # Footer with report information
        report_path = os.path.join(self.report_dir, f"test_run_{test_run.id}.json")
        report_path = os.path.relpath(report_path, os.getcwd())  # Make path relative for readability
        
        logger.info(f"{Colors.CYAN}╠{'═' * (width-2)}╣{Colors.ENDC}")
        logger.info(f"{Colors.CYAN}║ {Colors.BOLD}Report:{Colors.ENDC} {Colors.BLUE}{report_path}{Colors.ENDC}{' ' * (width - 12 - len(report_path))}║{Colors.ENDC}")
        logger.info(f"{Colors.CYAN}╚{'═' * (width-2)}╝{Colors.ENDC}\n")
    
    def check_gbu2_license_compliance(self) -> Dict[str, Any]:
        """Check repository for GBU2 License compliance."""
        results = self.license_checker.check_uncommitted_files()
        self.license_checker.print_gbu2_check_results(results)
        return results
        
    def apply_gbu2_license(self, path: str, recursive: bool = True) -> Dict[str, int]:
        """Apply GBU2 License to file or directory."""
        if os.path.isfile(path):
            success = self.license_checker.apply_license_to_file(path)
            return {'files_processed': 1, 'files_updated': 1 if success else 0}
        elif os.path.isdir(path):
            return self.license_checker.apply_license_to_dir(path, recursive)
        else:
            logger.error(f"Path not found: {path}")
            return {'files_processed': 0, 'files_updated': 0}
    
    # New methods for the added features
    def report_uncommitted_files(self) -> Dict[str, Any]:
        """Generate and print a report of uncommitted files."""
        report = self.git_manager.get_uncommitted_report()
        self.git_manager.print_uncommitted_report(report)
        return report
    
    def suggest_git_commit(self) -> str:
        """Generate a suggested git commit message based on current changes."""
        message = self.git_manager.suggest_commit_message()
        print(f"\n{Colors.BOLD}{Colors.GREEN}Suggested Git Commit Message:{Colors.ENDC}")
        print(f"{Colors.CYAN}{message}{Colors.ENDC}\n")
        return message
    
    def suggest_git_tag(self) -> str:
        """Generate a suggested git tag based on project state."""
        tag = self.git_manager.suggest_git_tag()
        print(f"\n{Colors.BOLD}{Colors.GREEN}Suggested Git Tag:{Colors.ENDC}")
        print(f"{Colors.CYAN}{tag}{Colors.ENDC}\n")
        return tag

# Git functionality for tracking uncommitted files and suggesting commits
class GitManager:
    """Manages Git operations and provides smart commit suggestions."""
    
    def __init__(self, project_root: str):
        """Initialize the Git manager with project root path."""
        self.project_root = os.path.abspath(project_root)
        self.watched_files = set()
        self.file_contexts = {}  # Store context for each file
        self.change_history = []  # Track changes for better suggestions
        self.last_scan_time = 0
        
    def _run_git_command(self, command: List[str]) -> Tuple[str, str, int]:
        """Run a git command and return stdout, stderr, and return code."""
        try:
            process = subprocess.run(
                ["git"] + command,
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return process.stdout, process.stderr, process.returncode
        except Exception as e:
            logger.error(f"Error running git command: {e}")
            return "", str(e), 1
    
    def get_uncommitted_files(self) -> Dict[str, List[str]]:
        """
        Get list of all uncommitted files categorized by status.
        
        Returns a dictionary with keys:
        - 'modified' - Modified files
        - 'added' - New files staged for commit
        - 'deleted' - Deleted files
        - 'untracked' - New files not staged for commit
        - 'all' - All uncommitted files
        """
        self.last_scan_time = time.time()
        
        # Get status of tracked files
        stdout, stderr, returncode = self._run_git_command(["status", "--porcelain"])
        if returncode != 0:
            logger.error(f"Failed to get git status: {stderr}")
            return {
                'modified': [],
                'added': [],
                'deleted': [],
                'untracked': [],
                'all': []
            }
        
        modified = []
        added = []
        deleted = []
        untracked = []
        
        for line in stdout.strip().split('\n'):
            if not line:
                continue
                
            status = line[:2]
            file_path = line[3:].strip()
            
            # Update watched files set
            self.watched_files.add(file_path)
            
            if status.startswith('M'):  # Modified
                modified.append(file_path)
            elif status.startswith('A'):  # Added
                added.append(file_path)
            elif status.startswith('D'):  # Deleted
                deleted.append(file_path)
            elif status.startswith('??'):  # Untracked
                untracked.append(file_path)
            
        all_files = modified + added + deleted + untracked
        
        # Store results as a dictionary
        result = {
            'modified': modified,
            'added': added,
            'deleted': deleted,
            'untracked': untracked,
            'all': all_files
        }
        
        # Update file contexts
        self._update_file_contexts(all_files)
        
        return result
    
    def _update_file_contexts(self, files: List[str]) -> None:
        """Update context information for files."""
        for file_path in files:
            full_path = os.path.join(self.project_root, file_path)
            
            if file_path not in self.file_contexts:
                self.file_contexts[file_path] = {
                    'first_seen': time.time(),
                    'extension': os.path.splitext(file_path)[1],
                    'directory': os.path.dirname(file_path),
                    'diff_history': [],
                    'content_samples': [],
                    'related_files': []
                }
            
            # Get file diff if it's a modified file
            if os.path.exists(full_path) and os.path.isfile(full_path):
                # Get file diff for modified files
                stdout, stderr, returncode = self._run_git_command(["diff", file_path])
                if returncode == 0 and stdout:
                    self.file_contexts[file_path]['diff_history'].append({
                        'time': time.time(),
                        'diff': stdout
                    })
                    
                # Get a sample of file content for context
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
                        try:
                            content = f.read(4096)  # First 4KB is enough for context
                            self.file_contexts[file_path]['content_samples'].append({
                                'time': time.time(),
                                'content': content
                            })
                        except Exception:
                            pass
                except Exception:
                    pass
                
                # Find related files in the same directory
                dir_path = os.path.dirname(full_path)
                if os.path.exists(dir_path):
                    related_files = []
                    for f in os.listdir(dir_path):
                        if f != os.path.basename(file_path) and os.path.isfile(os.path.join(dir_path, f)):
                            related_files.append(os.path.join(os.path.dirname(file_path), f))
                    self.file_contexts[file_path]['related_files'] = related_files[:5]  # Limit to 5 related files
    
    def get_file_changes(self, file_path: str) -> List[str]:
        """Get summarized changes for a specific file."""
        if file_path not in self.file_contexts:
            return []
            
        changes = []
        diff_history = self.file_contexts[file_path].get('diff_history', [])
        
        if not diff_history:
            return []
            
        latest_diff = diff_history[-1].get('diff', '')
        
        for line in latest_diff.split('\n'):
            if line.startswith('+') and not line.startswith('+++'):
                changes.append(f"Added: {line[1:].strip()}")
            elif line.startswith('-') and not line.startswith('---'):
                changes.append(f"Removed: {line[1:].strip()}")
                
        return changes[:10]  # Return top 10 changes
    
    def suggest_commit_message(self, files: Optional[List[str]] = None) -> str:
        """
        Generate an intelligent commit message suggestion based on file changes.
        
        Args:
            files: List of files to include in the message. If None, all uncommitted files are used.
        """
        actual_files: List[str] = []
        if files is None:
            files_dict = self.get_uncommitted_files()
            actual_files = files_dict['all']
        else:
            actual_files = files
            
        if not actual_files:
            return "No changes to commit"
            
        # Get basic stats
        file_count = len(actual_files)
        extensions = {}
        directories = {}
        
        for file_path in actual_files:
            ext = os.path.splitext(file_path)[1].lower()
            if ext:
                extensions[ext] = extensions.get(ext, 0) + 1
                
            directory = os.path.dirname(file_path)
            if directory:
                directories[directory] = directories.get(directory, 0) + 1
        
        # Determine primary file type and directory
        primary_ext = max(extensions.items(), key=lambda x: x[1])[0] if extensions else ""
        primary_dir = max(directories.items(), key=lambda x: x[1])[0] if directories else ""
        
        # Get key changes
        key_changes = []
        for file_path in actual_files[:3]:  # Look at top 3 files
            changes = self.get_file_changes(file_path)
            key_changes.extend(changes[:3])  # Top 3 changes per file
            
        # Generate commit message components
        components = []
        
        # Action part
        if all(f in self.file_contexts and self.file_contexts[f].get('first_seen', 0) > time.time() - 3600 for f in actual_files[:5]):
            action = "Add"
        else:
            action = "Update"
            
        # Target part
        if primary_dir and primary_ext:
            target = f"{os.path.basename(primary_dir)} {primary_ext[1:]} files"
        elif primary_dir:
            target = primary_dir
        elif primary_ext:
            target = f"{primary_ext[1:]} files"
        else:
            target = "files"
            
        # Detail part
        if key_changes:
            details = ": " + "; ".join(key_changes[:3])
        else:
            if file_count > 1:
                details = f" ({file_count} files changed)"
            else:
                details = ""
                
        # Combine parts
        commit_message = f"{action} {target}{details}"
        
        # Tag suggestion
        tags = self._suggest_tags(actual_files, key_changes)
        if tags:
            commit_message += "\n\n" + tags
            
        return commit_message
    
    def _suggest_tags(self, files: List[str], changes: List[str]) -> str:
        """Suggest tags for the commit based on files and changes."""
        tags = []
        
        # Check for specific file patterns
        has_test_files = any("test" in f.lower() for f in files)
        has_doc_files = any(f.lower().endswith((".md", ".rst", ".txt", ".doc", ".pdf")) for f in files)
        has_config_files = any(f.lower().endswith((".json", ".yml", ".yaml", ".xml", ".conf", ".config", ".ini")) for f in files)
        has_feature_files = any(not f.lower().endswith((".md", ".rst", ".txt")) and "feature" in f.lower() for f in files)
        has_fix_changes = any("fix" in c.lower() or "bug" in c.lower() or "issue" in c.lower() for c in changes)
        
        if has_test_files:
            tags.append("#test")
        if has_doc_files:
            tags.append("#docs")
        if has_config_files:
            tags.append("#config")
        if has_feature_files:
            tags.append("#feature")
        if has_fix_changes:
            tags.append("#bugfix")
            
        # Add cosmic tags for OMEGA project
        tags.append("#OMEGA")
        tags.append("#BTC")
        
        # Add random cosmic tag
        cosmic_tags = ["#quantum", "#AI", "#divine", "#ascension", "#transcendent", "#cosmic"]
        import random
        tags.append(random.choice(cosmic_tags))
        
        return " ".join(tags)
    
    def suggest_git_tag(self) -> str:
        """Suggest a Git tag name based on project context."""
        # Get current date for tag
        date_str = datetime.datetime.now().strftime("%Y%m%d")
        
        # Get last tag to increment version
        stdout, stderr, returncode = self._run_git_command(["tag", "--list"])
        if returncode != 0:
            # If can't get tags, create a new one from scratch
            return f"v0.1.0-omega-{date_str}"
            
        tags = stdout.strip().split('\n')
        version_tags = [t for t in tags if t.startswith('v') and '.' in t]
        
        if not version_tags:
            return f"v0.1.0-omega-{date_str}"
            
        # Parse latest version tag
        latest_tag = sorted(version_tags)[-1]
        try:
            version_part = latest_tag.split('-')[0]
            if version_part.startswith('v'):
                version_part = version_part[1:]
                
            major, minor, patch = map(int, version_part.split('.'))
            
            # Increment patch version
            patch += 1
            
            # Create new tag
            new_tag = f"v{major}.{minor}.{patch}-omega-{date_str}"
            return new_tag
        except Exception:
            # If parsing failed, create a new tag
            return f"v0.1.0-omega-{date_str}"
    
    def get_uncommitted_report(self) -> Dict[str, Any]:
        """Get detailed report on uncommitted changes."""
        files = self.get_uncommitted_files()
        
        # Count files by extension
        extensions = {}
        for file_path in files['all']:
            ext = os.path.splitext(file_path)[1].lower()
            if ext:
                extensions[ext] = extensions.get(ext, 0) + 1
                
        # Count files by directory
        directories = {}
        for file_path in files['all']:
            directory = os.path.dirname(file_path)
            if directory:
                directories[directory] = directories.get(directory, 0) + 1
        
        # Generate report
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'file_counts': {
                'total': len(files['all']),
                'modified': len(files['modified']),
                'added': len(files['added']),
                'deleted': len(files['deleted']),
                'untracked': len(files['untracked'])
            },
            'by_extension': extensions,
            'by_directory': directories,
            'files': {
                'modified': files['modified'],
                'added': files['added'],
                'deleted': files['deleted'],
                'untracked': files['untracked']
            },
            'suggestions': {
                'commit_message': self.suggest_commit_message(files['all']),
                'tag': self.suggest_git_tag()
            }
        }
        
        return report
    
    def print_uncommitted_report(self, report: Optional[Dict[str, Any]] = None) -> None:
        """Print a colorful report of uncommitted files with suggestions."""
        actual_report: Dict[str, Any] = self.get_uncommitted_report() if report is None else report
            
        # Header
        print(f"\n{Colors.HEADER}{Colors.BOLD}======== 🧬 OMEGA BTC GIT QUANTUM ANALYSIS 🧬 ========{Colors.ENDC}")
        print(f"{Colors.BLUE}Time: {actual_report['timestamp']}{Colors.ENDC}\n")
        
        # File counts
        print(f"{Colors.BOLD}📊 File Change Summary:{Colors.ENDC}")
        print(f"  • {Colors.GREEN}{actual_report['file_counts']['total']} total files{Colors.ENDC}")
        print(f"  • {Colors.CYAN}{actual_report['file_counts']['modified']} modified files{Colors.ENDC}")
        print(f"  • {Colors.YELLOW}{actual_report['file_counts']['added']} new files{Colors.ENDC}")
        print(f"  • {Colors.RED}{actual_report['file_counts']['deleted']} deleted files{Colors.ENDC}")
        print(f"  • {Colors.BLUE}{actual_report['file_counts']['untracked']} untracked files{Colors.ENDC}")
        
        # Files by type
        if actual_report['by_extension']:
            print(f"\n{Colors.BOLD}📂 Files by Type:{Colors.ENDC}")
            for ext, count in sorted(actual_report['by_extension'].items(), key=lambda x: x[1], reverse=True):
                print(f"  • {Colors.CYAN}{ext}{Colors.ENDC}: {count} files")
                
        # Files by directory
        if actual_report['by_directory']:
            print(f"\n{Colors.BOLD}📁 Files by Directory:{Colors.ENDC}")
            for directory, count in sorted(actual_report['by_directory'].items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  • {Colors.YELLOW}{directory}{Colors.ENDC}: {count} files")
        
        # Modified files (top 5)
        if actual_report['files']['modified']:
            print(f"\n{Colors.BOLD}✏️ Modified Files (top 5):{Colors.ENDC}")
            for file_path in actual_report['files']['modified'][:5]:
                print(f"  • {Colors.CYAN}{file_path}{Colors.ENDC}")
                
        # New files (top 5)
        if actual_report['files']['added'] or actual_report['files']['untracked']:
            added_files = actual_report['files']['added'] + actual_report['files']['untracked']
            print(f"\n{Colors.BOLD}➕ New Files (top 5):{Colors.ENDC}")
            for file_path in added_files[:5]:
                print(f"  • {Colors.GREEN}{file_path}{Colors.ENDC}")
        
        # Suggestions
        print(f"\n{Colors.BOLD}💡 Quantum Git Suggestions:{Colors.ENDC}")
        print(f"\n{Colors.GREEN}Commit Message:{Colors.ENDC}")
        print(f"{Colors.CYAN}{actual_report['suggestions']['commit_message']}{Colors.ENDC}")
        
        print(f"\n{Colors.GREEN}Suggested Tag:{Colors.ENDC}")
        print(f"{Colors.CYAN}{actual_report['suggestions']['tag']}{Colors.ENDC}")
        
        print(f"\n{Colors.HEADER}{Colors.BOLD}=========================================================={Colors.ENDC}\n")

def log_with_formatting(message, level=logging.INFO, color=None):
    """Log a message with optional color formatting."""
    if color:
        formatted_message = f"{color}{message}{Colors.ENDC}"
        logger.log(level, formatted_message)
    else:
        logger.log(level, message)

def print_section_header(title, width=80):
    """Print a section header with a border."""
    border = "═" * width
    logger.info(f"{Colors.CYAN}{border}{Colors.ENDC}")
    centered_title = f"  {title}  ".center(width, "═")
    logger.info(f"{Colors.CYAN}║{Colors.BOLD}{Colors.BLUE}{centered_title}{Colors.ENDC}{Colors.CYAN}║{Colors.ENDC}")
    logger.info(f"{Colors.CYAN}{border}{Colors.ENDC}")

def print_test_result(test_type, result, duration, report_path=None):
    """Print a formatted test result."""
    if result == "PASSED":
        status_color = Colors.GREEN
        symbol = "✓"
    elif result == "FAILED":
        status_color = Colors.RED
        symbol = "✗"
    else:
        status_color = Colors.YELLOW
        symbol = "⚠"
    
    test_type_formatted = f"{Colors.BOLD}{test_type}{Colors.ENDC}"
    result_formatted = f"{status_color}{symbol} {result}{Colors.ENDC}"
    duration_formatted = f"{Colors.YELLOW}{duration:.2f}s{Colors.ENDC}"
    
    message = f"\n  {test_type_formatted} tests {result_formatted} in {duration_formatted}"
    logger.info(message)
    
    if report_path:
        logger.info(f"  {Colors.CYAN}Report saved to: {report_path}{Colors.ENDC}\n")

def print_file_action(action, file_path):
    """Print a formatted file action message."""
    logger.info(f"{Colors.BLUE}{action}:{Colors.ENDC} {file_path}")

def main() -> None:
    """Main entry point for the service."""
    parser = argparse.ArgumentParser(
        description="0M3G4 B0TS QA AUT0 TEST SUITES RuNn3R 5D",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--project-root",
        type=str,
        default=os.getcwd(),
        help="Root directory of the project to monitor"
    )
    
    parser.add_argument(
        "--report-dir",
        type=str,
        default="qa/reports",
        help="Directory for test reports, relative to project root"
    )
    
    parser.add_argument(
        "--run-tests",
        nargs="*",
        choices=[d.name for d in TestDimension],
        help="Run tests in specified dimensions and exit"
    )
    
    parser.add_argument(
        "--check-license",
        action="store_true",
        help="Check uncommitted files for GBU2 License compliance and exit"
    )
    
    parser.add_argument(
        "--apply-license",
        type=str,
        help="Apply GBU2 License to specified file or directory and exit"
    )
    
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Apply license recursively to directories"
    )
    
    # New arguments for Git features
    parser.add_argument(
        "--report-uncommitted",
        action="store_true",
        help="Generate and print a report of uncommitted files in the repository"
    )
    
    parser.add_argument(
        "--suggest-git",
        action="store_true",
        help="Suggest Git commit message and tag based on current repository state"
    )
    
    parser.add_argument(
        "--auto-listen",
        action="store_true",
        help="Continuously monitor for file changes and report new files"
    )
    
    parser.add_argument(
        "--OMEGA",
        action="store_true",
        help="FULL OMEGA MODE - Run all features with intelligent auto-tuned intervals"
    )
    
    parser.add_argument(
        "--uncommitted-interval",
        type=int,
        default=300,
        help="Interval in seconds between uncommitted file reports (when using --auto-listen or --OMEGA)"
    )
    
    parser.add_argument(
        "--git-suggestion-interval",
        type=int,
        default=600,
        help="Interval in seconds between Git suggestion updates (when using --auto-listen or --OMEGA)"
    )
    
    parser.add_argument(
        "--new-file-scan-interval",
        type=int,
        default=60,
        help="Interval in seconds between new file scans (when using --auto-listen or --OMEGA)"
    )
    
    args = parser.parse_args()
    
    # Create custom config from args
    config = {
        'report_dir': args.report_dir,
        'run_initial_tests': args.run_tests is not None,
        
        # File monitoring configuration
        'watched_extensions': {'.py', '.js', '.ts', '.html', '.css', '.md', '.yml', '.yaml', '.json'},
        'ignored_dirs': {'venv', 'node_modules', '.git', '__pycache__', '.pytest_cache'},
        
        # Schedule configuration
        'schedule': {
            'full': 24 * 60 * 60,  # Daily
            'unit': 4 * 60 * 60,   # Every 4 hours
            'integration': 8 * 60 * 60  # Every 8 hours
        },
        
        # New configuration options
        'report_uncommitted': args.report_uncommitted,
        'suggest_git': args.suggest_git,
        'auto_listen': args.auto_listen,
        'full_omega_mode': args.OMEGA,
        'uncommitted_scan_interval': args.uncommitted_interval,
        'git_suggestion_interval': args.git_suggestion_interval,
        'new_file_scan_interval': args.new_file_scan_interval
    }
    
    # Initialize the quantum test service
    service = QuantumTestService(args.project_root, config)
    
    # Handle one-shot commands
    if args.check_license:
        service.check_gbu2_license_compliance()
        return
        
    if args.apply_license:
        results = service.apply_gbu2_license(args.apply_license, args.recursive)
        print(f"Applied license to {results['files_updated']} of {results['files_processed']} files.")
        return
        
    if args.run_tests is not None:
        service.run_quantum_test_suite(args.run_tests)
        return
    
    # New one-shot commands
    if args.report_uncommitted and not (args.auto_listen or args.OMEGA):
        service.report_uncommitted_files()
        if args.suggest_git:
            service.suggest_git_commit()
            service.suggest_git_tag()
        return
        
    if args.suggest_git and not (args.auto_listen or args.OMEGA):
        service.suggest_git_commit()
        service.suggest_git_tag()
        return
    
    # Start the service for continuous monitoring
    try:
        service.start()
        
        # Print welcome message for continuous modes
        if args.OMEGA:
            print(f"\n{Colors.BOLD}{Colors.CYAN}🌀 OMEGA MODE ACTIVATED 🌀{Colors.ENDC}")
            print(f"{Colors.YELLOW}Monitoring for file changes, uncommitted files, and providing AI-powered Git suggestions{Colors.ENDC}")
            print(f"{Colors.GREEN}Press Ctrl+C to stop{Colors.ENDC}\n")
        elif args.auto_listen:
            print(f"\n{Colors.BOLD}{Colors.BLUE}🔍 AUTO-LISTEN MODE ACTIVATED 🔍{Colors.ENDC}")
            print(f"{Colors.YELLOW}Monitoring for file changes and uncommitted files{Colors.ENDC}")
            print(f"{Colors.GREEN}Press Ctrl+C to stop{Colors.ENDC}\n")
        else:
            print(f"\n{Colors.BOLD}{Colors.GREEN}🧪 TEST MONITORING ACTIVATED 🧪{Colors.ENDC}")
            print(f"{Colors.YELLOW}Monitoring for file changes to trigger tests{Colors.ENDC}")
            print(f"{Colors.GREEN}Press Ctrl+C to stop{Colors.ENDC}\n")
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Shutting down...{Colors.ENDC}")
    finally:
        service.stop()

if __name__ == "__main__":
    main() 