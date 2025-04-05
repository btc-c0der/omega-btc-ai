"""
Test runner for executing tests across multiple dimensions.
"""

import os
import sys
import time
import json
import logging
import subprocess
import datetime
import uuid
from typing import Dict, List, Set, Any, Optional, Tuple, Union

from .types import Colors, TestDimension, TestState
from .data_models import TestResult, TestRun
from .utils import log_with_formatting, print_section_header, print_test_result, print_file_action

logger = logging.getLogger("0M3G4_B0TS_QA_AUT0_TEST_SUITES_RuNn3R_5D")

class TestRunner:
    """Runs tests in multiple dimensions."""
    
    def __init__(self, project_root: str, report_dir: str):
        """Initialize the test runner."""
        self.project_root = os.path.abspath(project_root)
        self.report_dir = os.path.abspath(report_dir)
        
        # Create directory for reports
        os.makedirs(self.report_dir, exist_ok=True)
        
        # Determine Python executable to use
        if os.path.exists(os.path.join(self.project_root, ".venv/bin/python")):
            self.python_path = os.path.join(self.project_root, ".venv/bin/python")
        elif os.path.exists(os.path.join(self.project_root, "venv/bin/python")):
            self.python_path = os.path.join(self.project_root, "venv/bin/python")
        else:
            self.python_path = sys.executable
            
        # Map test dimensions to test scripts
        self.test_scripts = self._discover_test_scripts()
        
    def _discover_test_scripts(self) -> Dict[TestDimension, str]:
        """Discover test scripts in the project."""
        # Define paths for test scripts
        unit_script = os.path.join(self.project_root, "src/omega_bot_farm/qa/tests/test_quantum_ai_integration.py")
        integration_script = os.path.join(self.project_root, "src/omega_bot_farm/qa/tests/test_quantum_ai_integration.py")
        performance_script = os.path.join(self.project_root, "src/omega_bot_farm/qa/tests/test_quantum_ai_performance.py")
        
        # Return mapping
        return {
            TestDimension.UNIT: unit_script,
            TestDimension.INTEGRATION: integration_script,
            TestDimension.PERFORMANCE: performance_script
        }
    
    def _get_test_script_for_dimension(self, dimension: TestDimension) -> Optional[str]:
        """Get the test script for a dimension."""
        return self.test_scripts.get(dimension)
        
    def _create_test_filter_args(self, files_changed: List[str]) -> List[str]:
        """Create pytest filter arguments based on changed files."""
        return []  # Placeholder for more sophisticated filtering
    
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