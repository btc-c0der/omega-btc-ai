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
from .test_implementations import get_test_implementation, AbstractTestImplementation

logger = logging.getLogger("0M3G4_B0TS_QA_AUT0_TEST_SUITES_RuNn3R_5D")

class TestRunner:
    """Runs tests in multiple dimensions."""
    
    def __init__(self, project_root: str, report_dir: str):
        """Initialize the test runner."""
        self.project_root = os.path.abspath(project_root)
        self.report_dir = os.path.abspath(report_dir)
        
        # Create directory for reports
        os.makedirs(self.report_dir, exist_ok=True)
        
        # Cache for test implementations
        self._test_implementations = {}
        
    def _get_test_implementation(self, dimension: TestDimension) -> AbstractTestImplementation:
        """Get the test implementation for a dimension, with caching."""
        if dimension not in self._test_implementations:
            self._test_implementations[dimension] = get_test_implementation(
                dimension, 
                self.project_root, 
                self.report_dir
            )
        return self._test_implementations[dimension]
    
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
        
        # Run tests for each dimension
        for dimension in dimensions:
            try:
                # Get the implementation for this dimension
                implementation = self._get_test_implementation(dimension)
                
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
                
                # Mark this dimension as running
                test_run.results[dimension] = TestResult(
                    dimension=dimension,
                    state=TestState.RUNNING
                )
                test_run.update_state()
                
                # Run the tests for this dimension
                result = implementation.run_tests(source_files)
                
                # Update the test run with the result
                test_run.results[dimension] = result
                
                # Print results with improved formatting
                status_symbol = "✓" if result.state == TestState.PASSED else "✗"
                status_color = Colors.GREEN if result.state == TestState.PASSED else Colors.RED
                
                # Result box
                logger.info(f"\n{status_color}┌{'─' * 78}┐{Colors.ENDC}")
                logger.info(f"{status_color}│ {Colors.BOLD}{status_symbol} {dimension.name} tests {result.state.value}{Colors.ENDC}{status_color}{' ' * (66 - len(dimension.name) - len(result.state.value))}│{Colors.ENDC}")
                logger.info(f"{status_color}│ {Colors.BOLD}Duration:{Colors.ENDC} {result.duration:.2f}s{' ' * (68 - len(str(round(result.duration, 2))))}│{Colors.ENDC}")
                logger.info(f"{status_color}└{'─' * 78}┘{Colors.ENDC}\n")
                
                # Print error details for failed tests
                if result.state == TestState.FAILED and 'output' in result.details:
                    logger.info(f"{Colors.RED}Failed Test Details:{Colors.ENDC}")
                    for line in result.details['output'].split("\n"):
                        if "FAILED" in line:
                            logger.error(f"{Colors.RED}  {line}{Colors.ENDC}")
                    logger.info("")
            
            except Exception as e:
                logger.error(f"{Colors.RED}Error running {dimension.name} tests: {e}{Colors.ENDC}")
                test_run.results[dimension] = TestResult(
                    dimension=dimension,
                    state=TestState.FAILED,
                    duration=0.0,
                    details={"error": str(e)}
                )
        
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