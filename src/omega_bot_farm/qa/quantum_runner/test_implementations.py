"""
Test implementation classes for each quantum test dimension.
"""

import os
import sys
import time
import json
import logging
import subprocess
import datetime
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple, Union

from .types import Colors, TestDimension, TestState
from .data_models import TestResult, TestRun

logger = logging.getLogger("0M3G4_B0TS_QA_AUT0_TEST_SUITES_RuNn3R_5D")

class AbstractTestImplementation(ABC):
    """Base abstract class for all test dimension implementations."""
    
    def __init__(self, project_root: str, report_dir: str):
        """Initialize the test implementation."""
        self.project_root = os.path.abspath(project_root)
        self.report_dir = os.path.abspath(report_dir)
        self.dimension = self._get_dimension()
        self.last_run_time = 0
        
    @abstractmethod
    def _get_dimension(self) -> TestDimension:
        """Return the test dimension this implementation handles."""
        pass
        
    @abstractmethod
    def get_test_script(self) -> str:
        """Return the path to the test script for this dimension."""
        pass
        
    @abstractmethod
    def prepare_environment(self) -> None:
        """Prepare the environment for running tests."""
        pass
        
    @abstractmethod
    def get_extra_args(self, files_changed: Optional[List[str]] = None) -> List[str]:
        """Get additional arguments for this test dimension."""
        pass
        
    def run_tests(self, files_changed: Optional[List[str]] = None) -> TestResult:
        """Run tests for this dimension."""
        # Base implementation will be customized by subclasses
        self.prepare_environment()
        
        test_script = self.get_test_script()
        if not os.path.exists(test_script):
            logger.warning(f"{Colors.YELLOW}⚠ Test script not found: {test_script}{Colors.ENDC}")
            return TestResult(
                dimension=self.dimension,
                state=TestState.SKIPPED,
                details={"error": f"Test script not found: {test_script}"}
            )
            
        # Set up result file paths
        run_report_dir = os.path.join(self.report_dir, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
        os.makedirs(run_report_dir, exist_ok=True)
        
        xml_report = os.path.join(run_report_dir, f"{self.dimension.name.lower()}_report.xml")
        html_report = os.path.join(run_report_dir, f"{self.dimension.name.lower()}_report.html")
        json_report = os.path.join(run_report_dir, f"{self.dimension.name.lower()}_report.json")
        
        # Create the base command
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            test_script,
            "-v",
            f"--junit-xml={xml_report}",
            f"--html={html_report}",
            "--self-contained-html"
        ]
        
        # Add dimension-specific args
        extra_args = self.get_extra_args(files_changed)
        if extra_args:
            cmd.extend(extra_args)
            
        cmd_str = " ".join(cmd)
        logger.info(f"{Colors.YELLOW}Command:{Colors.ENDC} {cmd_str}")
        
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
            self.last_run_time = end_time
            
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
            
            return TestResult(
                dimension=self.dimension,
                state=state,
                duration=duration,
                details=details
            )
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            self.last_run_time = end_time
            
            logger.error(f"{Colors.RED}Error running {self.dimension.name} tests: {e}{Colors.ENDC}")
            
            return TestResult(
                dimension=self.dimension,
                state=TestState.FAILED,
                duration=duration,
                details={"error": str(e)}
            )


class UnitTestImplementation(AbstractTestImplementation):
    """Implementation for unit tests."""
    
    def _get_dimension(self) -> TestDimension:
        return TestDimension.UNIT
        
    def get_test_script(self) -> str:
        return os.path.join(self.project_root, "src/omega_bot_farm/qa/tests/unit")
        
    def prepare_environment(self) -> None:
        # Unit tests don't need special environment preparation
        pass
        
    def get_extra_args(self, files_changed: Optional[List[str]] = None) -> List[str]:
        extra_args = []
        
        # If specific files changed, filter tests for those files
        if files_changed:
            # Create appropriate filters for unit tests
            for file_path in files_changed:
                # Extract the base name without extension
                file_name = os.path.basename(file_path)
                name, ext = os.path.splitext(file_name)
                
                # If it's a Python file, add filter
                if ext.lower() == '.py':
                    # If it's a test file itself, run just that test
                    if name.startswith('test_'):
                        extra_args.append(file_path)
                    else:
                        # Otherwise, look for corresponding test file
                        test_filter = f"-k={name}"
                        extra_args.append(test_filter)
        
        # Run tests in parallel if no specific filter
        if not extra_args:
            extra_args.extend(["-xvs", "-n=auto"])
            
        return extra_args


class IntegrationTestImplementation(AbstractTestImplementation):
    """Implementation for integration tests."""
    
    def _get_dimension(self) -> TestDimension:
        return TestDimension.INTEGRATION
        
    def get_test_script(self) -> str:
        return os.path.join(self.project_root, "src/omega_bot_farm/qa/tests/integration")
        
    def prepare_environment(self) -> None:
        # Ensure any test databases or services are set up
        os.environ["INTEGRATION_TEST_MODE"] = "1"
        
    def get_extra_args(self, files_changed: Optional[List[str]] = None) -> List[str]:
        extra_args = []
        
        # Add appropriate filters based on changed files
        if files_changed:
            for file_path in files_changed:
                # For integration tests, look for integration related components
                if 'api' in file_path or 'service' in file_path or 'integration' in file_path:
                    # Extract component name
                    base_name = os.path.basename(file_path)
                    component = os.path.splitext(base_name)[0]
                    test_filter = f"-k={component}"
                    if test_filter not in extra_args:
                        extra_args.append(test_filter)
        
        # Always run integration tests sequentially
        extra_args.append("-v")
        
        return extra_args


class PerformanceTestImplementation(AbstractTestImplementation):
    """Implementation for performance tests."""
    
    def _get_dimension(self) -> TestDimension:
        return TestDimension.PERFORMANCE
        
    def get_test_script(self) -> str:
        return os.path.join(self.project_root, "src/omega_bot_farm/qa/tests/performance")
        
    def prepare_environment(self) -> None:
        # Set up performance test environment
        os.environ["PERFORMANCE_TEST_MODE"] = "1"
        
        # Could add more setup like:
        # - Ensuring certain system resources are available
        # - Setting performance thresholds
        
    def get_extra_args(self, files_changed: Optional[List[str]] = None) -> List[str]:
        extra_args = []
        
        # Performance tests usually run all tests unless specifically targeting
        # components that were changed
        if files_changed:
            performance_related = any('performance' in f.lower() for f in files_changed)
            
            if performance_related:
                for file_path in files_changed:
                    base_name = os.path.basename(file_path)
                    component = os.path.splitext(base_name)[0]
                    test_filter = f"-k={component}"
                    if test_filter not in extra_args:
                        extra_args.append(test_filter)
        
        # Add performance-specific arguments
        extra_args.extend(["--benchmark-enable", "--benchmark-json", 
                           os.path.join(self.report_dir, "performance_benchmark.json")])
        
        return extra_args


class SecurityTestImplementation(AbstractTestImplementation):
    """Implementation for security tests."""
    
    def _get_dimension(self) -> TestDimension:
        return TestDimension.SECURITY
        
    def get_test_script(self) -> str:
        return os.path.join(self.project_root, "src/omega_bot_farm/qa/tests/security")
        
    def prepare_environment(self) -> None:
        # Set up security test environment
        os.environ["SECURITY_TEST_MODE"] = "1"
        
    def get_extra_args(self, files_changed: Optional[List[str]] = None) -> List[str]:
        extra_args = []
        
        # Security tests may focus on specific components based on changes
        if files_changed:
            security_keywords = ['auth', 'password', 'token', 'crypt', 'security', 'permission']
            
            security_related = any(any(keyword in f.lower() for keyword in security_keywords) 
                                   for f in files_changed)
            
            if security_related:
                for file_path in files_changed:
                    base_name = os.path.basename(file_path)
                    component = os.path.splitext(base_name)[0]
                    test_filter = f"-k={component}"
                    if test_filter not in extra_args:
                        extra_args.append(test_filter)
        
        # Add security-specific arguments
        extra_args.append("--security-audit")
        
        return extra_args


class ComplianceTestImplementation(AbstractTestImplementation):
    """Implementation for compliance tests."""
    
    def _get_dimension(self) -> TestDimension:
        return TestDimension.COMPLIANCE
        
    def get_test_script(self) -> str:
        return os.path.join(self.project_root, "src/omega_bot_farm/qa/tests/compliance")
        
    def prepare_environment(self) -> None:
        # Set up compliance test environment
        os.environ["COMPLIANCE_TEST_MODE"] = "1"
        
    def get_extra_args(self, files_changed: Optional[List[str]] = None) -> List[str]:
        extra_args = []
        
        # Compliance tests typically run a standard set of checks
        # but can be filtered for specific areas
        if files_changed:
            compliance_areas = ['gdpr', 'hipaa', 'api', 'standard', 'regulation']
            
            for area in compliance_areas:
                if any(area in f.lower() for f in files_changed):
                    test_filter = f"-k={area}"
                    if test_filter not in extra_args:
                        extra_args.append(test_filter)
        
        # Add compliance-specific arguments
        extra_args.append("--compliance-report")
        
        return extra_args


# Factory function to get the appropriate test implementation
def get_test_implementation(dimension: TestDimension, project_root: str, report_dir: str) -> AbstractTestImplementation:
    """Factory function to get the appropriate test implementation for a dimension."""
    implementations = {
        TestDimension.UNIT: UnitTestImplementation,
        TestDimension.INTEGRATION: IntegrationTestImplementation,
        TestDimension.PERFORMANCE: PerformanceTestImplementation,
        TestDimension.SECURITY: SecurityTestImplementation,
        TestDimension.COMPLIANCE: ComplianceTestImplementation
    }
    
    implementation_class = implementations.get(dimension)
    if implementation_class:
        return implementation_class(project_root, report_dir)
    else:
        raise ValueError(f"No implementation available for test dimension: {dimension}") 