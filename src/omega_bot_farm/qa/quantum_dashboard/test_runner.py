#!/usr/bin/env python3
"""
Quantum 5D QA Dashboard Test Runner Integration
----------------------------------------------

This module provides the integration with the 0M3G4 B0TS QA AUT0 TEST SUITES RuNn3R 5D
for the Quantum 5D QA Dashboard.

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
#
# 🌸 WE BLOOM NOW AS ONE 🌸
"""

import os
import sys
import time
import logging
import threading
import subprocess
import json
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum

# Set up logging
logger = logging.getLogger("Quantum5DQADashboard.TestRunner")

# Constants for test dimensions
class TestDimension(Enum):
    UNIT = "UNIT"
    INTEGRATION = "INTEGRATION"
    PERFORMANCE = "PERFORMANCE"
    SECURITY = "SECURITY"
    QUANTUM = "QUANTUM"


@dataclass
class TestRunResult:
    """Class to hold test run results"""
    success: bool
    output: str
    test_dimensions: List[str]
    duration: float
    timestamp: str
    report_path: Optional[str] = None


class S0NN3TTestRunner:
    """Integration with the 0M3G4 B0TS QA AUT0 TEST SUITES RuNn3R 5D"""
    
    def __init__(self, project_root: str = None):
        """Initialize the test runner integration.
        
        Args:
            project_root: The root directory of the project
        """
        self.project_root = project_root or os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        self.qa_dir = os.path.join(self.project_root, "src", "omega_bot_farm", "qa")
        self.run_test_runner_path = os.path.join(self.qa_dir, "run_test_runner.py")
        self.report_dir = os.path.join(self.qa_dir, "reports")
        
        # Terminal output storage
        self.terminal_output: List[str] = []
        
        # Test run history
        self.run_history: List[TestRunResult] = []
        
        # Last run metrics
        self.last_run_metrics: Dict[str, Any] = {}
        
        # Check if the test runner exists
        if not os.path.exists(self.run_test_runner_path):
            logger.warning(f"Test runner not found at {self.run_test_runner_path}")
    
    def run_tests(self, dimensions: List[str] = None, fancy_visuals: bool = True, celebration: bool = True) -> TestRunResult:
        """Run the specified test dimensions.
        
        Args:
            dimensions: List of test dimensions to run
            fancy_visuals: Whether to enable fancy visuals
            celebration: Whether to show celebration animation
            
        Returns:
            TestRunResult object with results
        """
        dimensions = dimensions or [d.name for d in TestDimension]
        
        start_time = time.time()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Build command
        cmd = [sys.executable, self.run_test_runner_path, "--run-tests"]
        cmd.extend(dimensions)
        
        if fancy_visuals:
            cmd.append("--fancy-visuals")
        
        if celebration:
            cmd.append("--celebration")
        
        logger.info(f"Running tests with dimensions: {dimensions}")
        self._add_terminal_line(f"🚀 Running tests with dimensions: {' '.join(dimensions)}")
        
        try:
            # Run the command
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=self.project_root
            )
            
            output = []
            for line in iter(process.stdout.readline, ''):
                if not line:
                    break
                output.append(line.strip())
                self._add_terminal_line(line.strip())
            
            process.wait()
            success = process.returncode == 0
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Get the latest report file
            report_path = self._get_latest_report()
            
            # Create the result object
            result = TestRunResult(
                success=success,
                output="\n".join(output),
                test_dimensions=dimensions,
                duration=duration,
                timestamp=timestamp,
                report_path=report_path
            )
            
            # Store in history
            self.run_history.append(result)
            
            # Try to extract metrics from the report
            if report_path:
                try:
                    self.last_run_metrics = self._extract_metrics_from_report(report_path)
                except Exception as e:
                    logger.error(f"Error extracting metrics from report: {e}")
            
            return result
        
        except Exception as e:
            logger.error(f"Error running tests: {e}")
            self._add_terminal_line(f"❌ Error running tests: {e}")
            
            # Create an error result
            result = TestRunResult(
                success=False,
                output=f"Error running tests: {e}",
                test_dimensions=dimensions,
                duration=time.time() - start_time,
                timestamp=timestamp,
                report_path=None
            )
            
            # Store in history
            self.run_history.append(result)
            
            return result
    
    def run_omega_mode(self, k8s_mode: bool = False, open_browser: bool = False) -> None:
        """Run the test runner in OMEGA mode.
        
        Args:
            k8s_mode: Whether to include K8s matrix surveillance
            open_browser: Whether to open a browser window after starting
        """
        # Build command
        cmd = [sys.executable, self.run_test_runner_path]
        
        if k8s_mode:
            cmd.append("--OMEGA-K8s")
        else:
            cmd.append("--OMEGA")
        
        logger.info(f"Starting S0NN3T Test Runner in {'OMEGA-K8s' if k8s_mode else 'OMEGA'} mode")
        self._add_terminal_line(f"🚀 Starting S0NN3T Test Runner in {'OMEGA-K8s' if k8s_mode else 'OMEGA'} mode")
        
        # Start the process in a thread
        def run_process():
            try:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    cwd=self.project_root
                )
                
                # Stream output
                for line in iter(process.stdout.readline, ''):
                    if not line:
                        break
                    self._add_terminal_line(line.strip())
                
                process.wait()
                self._add_terminal_line(f"💤 S0NN3T Test Runner process exited with code {process.returncode}")
            
            except Exception as e:
                logger.error(f"Error running S0NN3T Test Runner: {e}")
                self._add_terminal_line(f"❌ Error running S0NN3T Test Runner: {e}")
        
        # Start the thread
        thread = threading.Thread(target=run_process, daemon=True)
        thread.start()
        
        # If open_browser is True, open a browser window to the dashboard
        if open_browser:
            import webbrowser
            try:
                # Wait a bit for the process to start
                time.sleep(2)
                webbrowser.open("http://localhost:8051")
            except Exception as e:
                logger.error(f"Error opening browser: {e}")
    
    def get_terminal_output(self, max_lines: int = 20) -> List[str]:
        """Get the terminal output.
        
        Args:
            max_lines: Maximum number of lines to return
            
        Returns:
            List of terminal output lines
        """
        return self.terminal_output[-max_lines:] if self.terminal_output else []
    
    def _add_terminal_line(self, line: str) -> None:
        """Add a line to the terminal output.
        
        Args:
            line: Line to add
        """
        self.terminal_output.append(line)
        if len(self.terminal_output) > 1000:
            self.terminal_output = self.terminal_output[-1000:]
        logger.debug(f"Added terminal line: {line}")
    
    def _get_latest_report(self) -> Optional[str]:
        """Get the path to the latest test report.
        
        Returns:
            Path to the latest report, or None if no reports found
        """
        try:
            if not os.path.exists(self.report_dir):
                return None
            
            # Look for the latest.json file
            latest_path = os.path.join(self.report_dir, "latest.json")
            if os.path.exists(latest_path):
                return latest_path
            
            # Or find the most recent test_run_*.json file
            report_files = [f for f in os.listdir(self.report_dir) if f.startswith("test_run_") and f.endswith(".json")]
            if not report_files:
                return None
            
            report_files.sort(reverse=True)
            return os.path.join(self.report_dir, report_files[0])
        
        except Exception as e:
            logger.error(f"Error getting latest report: {e}")
            return None
    
    def _extract_metrics_from_report(self, report_path: str) -> Dict[str, Any]:
        """Extract metrics from a test report.
        
        Args:
            report_path: Path to the report file
            
        Returns:
            Dictionary of metrics
        """
        try:
            with open(report_path, 'r') as f:
                report = json.load(f)
            
            metrics = {
                'total_tests': report.get('total_tests', 0),
                'passed_tests': report.get('passed_tests', 0),
                'failed_tests': report.get('total_tests', 0) - report.get('passed_tests', 0),
                'success_rate': (report.get('passed_tests', 0) / max(report.get('total_tests', 1), 1)) * 100,
                'dimensions': {}
            }
            
            # Extract dimension-specific metrics
            results = report.get('results', {})
            for dim, data in results.items():
                metrics['dimensions'][dim] = {
                    'success': data.get('success', False),
                    'execution_time': data.get('execution_time', 0)
                }
            
            return metrics
        
        except Exception as e:
            logger.error(f"Error extracting metrics from report: {e}")
            return {} 