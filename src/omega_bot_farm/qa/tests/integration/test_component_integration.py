"""
Integration test for different framework components.

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
"""

import os
import sys
import unittest
import tempfile
import datetime
from typing import Dict, List, Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the quantum runner components
try:
    from quantum_runner.types import TestDimension, TestState
    from quantum_runner.data_models import TestResult, TestRun
    from quantum_runner.test_runner import TestRunner
    from quantum_runner.gbu2_license import GBU2LicenseChecker
except ImportError:
    # Fallback import mechanism
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../quantum_runner')))
    from types import TestDimension, TestState
    from data_models import TestResult, TestRun
    from test_runner import TestRunner
    from gbu2_license import GBU2LicenseChecker

class ComponentIntegrationTests(unittest.TestCase):
    """Tests that verify the integration between different components."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary directory for test reports
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        
    def tearDown(self):
        """Clean up test environment."""
        self.temp_dir.cleanup()
    
    def test_runner_and_license_checker_integration(self):
        """Test integration between TestRunner and GBU2LicenseChecker."""
        # Create test runner and license checker
        runner = TestRunner(self.project_root, self.temp_dir.name)
        license_checker = GBU2LicenseChecker(self.project_root)
        
        # Get a list of test files
        current_file = os.path.abspath(__file__)
        test_files = [current_file]
        
        # Check if this file has license
        has_license, level = license_checker.check_file(current_file)
        
        # Verify this file has GBU2 license
        self.assertTrue(has_license, "Test file should have GBU2 license")
        self.assertIsNotNone(level, "License should have a consciousness level")
        
        # Use the license checker to verify this test file
        report = license_checker.check_directory(os.path.dirname(current_file), recursive=False)
        
        # There should be at least one file with license
        self.assertGreater(report["files_with_license"], 0, 
                          "Directory should have at least one file with license")
        
        # Create a test run with results
        test_run = TestRun(
            id="integration_test",
            timestamp=datetime.datetime.now(),
            trigger="test",
            source_files=test_files
        )
        
        # Add a test result
        test_run.results[TestDimension.INTEGRATION] = TestResult(
            dimension=TestDimension.INTEGRATION,
            state=TestState.PASSED,
            duration=0.1,
            details={"license_report": report}
        )
        
        # Update state
        test_run.update_state()
        
        # Save the test run using the runner
        runner.save_test_run(test_run)
        
        # Verify the test run was saved
        run_file = os.path.join(self.temp_dir.name, f"test_run_{test_run.id}.json")
        self.assertTrue(os.path.exists(run_file), "Test run file should exist")
        
        # Verify the latest.json file was also created
        latest_file = os.path.join(self.temp_dir.name, "latest.json")
        self.assertTrue(os.path.exists(latest_file), "Latest test run file should exist")
    
    def test_dimensions_compatibility(self):
        """Test that all dimensions are compatible with test runner."""
        # Create test runner
        runner = TestRunner(self.project_root, self.temp_dir.name)
        
        # Verify we can create test runs for all dimensions
        all_dimensions = list(TestDimension)
        
        # This is a partial test since we're not actually running the implementations
        # But we're verifying that we can create a test run with all dimensions
        test_run = TestRun(
            id="all_dimensions",
            timestamp=datetime.datetime.now(),
            trigger="test"
        )
        
        # Add a result for each dimension
        for dimension in all_dimensions:
            test_run.results[dimension] = TestResult(
                dimension=dimension,
                state=TestState.PASSED,
                duration=0.1
            )
        
        # Update state and save
        test_run.update_state()
        runner.save_test_run(test_run)
        
        # Verify the file was saved
        run_file = os.path.join(self.temp_dir.name, f"test_run_{test_run.id}.json")
        self.assertTrue(os.path.exists(run_file), "Test run file should exist")


if __name__ == "__main__":
    unittest.main() 