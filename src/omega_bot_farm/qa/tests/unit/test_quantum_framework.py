"""
Unit test for the quantum framework components.

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
import datetime
from typing import Dict, List, Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the quantum runner components
try:
    from quantum_runner.types import TestDimension, TestState
    from quantum_runner.data_models import TestResult, TestRun
except ImportError:
    # Fallback to direct imports if not installed as a package
    from test_implementations import TestDimension, TestState
    from test_implementations import TestResult, TestRun

class QuantumTestFrameworkTests(unittest.TestCase):
    """Unit tests for the quantum test framework components."""
    
    def test_test_dimensions(self):
        """Test that all test dimensions can be created."""
        dimensions = [
            TestDimension.UNIT,
            TestDimension.INTEGRATION,
            TestDimension.PERFORMANCE,
            TestDimension.SECURITY,
            TestDimension.COMPLIANCE
        ]
        
        # Verify each dimension is unique
        self.assertEqual(len(dimensions), len(set(dimensions)))
        
        # Verify dimension names
        expected_names = ["UNIT", "INTEGRATION", "PERFORMANCE", "SECURITY", "COMPLIANCE"]
        actual_names = [dim.name for dim in dimensions]
        self.assertEqual(expected_names, actual_names)
    
    def test_test_states(self):
        """Test that all test states work correctly."""
        states = [
            TestState.UNKNOWN,
            TestState.RUNNING,
            TestState.PASSED,
            TestState.FAILED,
            TestState.SKIPPED,
            TestState.QUANTUM_ENTANGLED,
            TestState.SUPERPOSITION
        ]
        
        # Verify each state is unique
        self.assertEqual(len(states), len(set(states)))
        
        # Verify state values
        expected_values = ["UNKNOWN", "RUNNING", "PASSED", "FAILED", "SKIPPED", 
                          "QUANTUM_ENTANGLED", "SUPERPOSITION"]
        actual_values = [state.value for state in states]
        self.assertEqual(expected_values, actual_values)
    
    def test_test_result(self):
        """Test creating and manipulating TestResult objects."""
        # Create a test result
        result = TestResult(
            dimension=TestDimension.UNIT,
            state=TestState.PASSED,
            duration=1.23,
            details={"test_count": 42}
        )
        
        # Verify properties
        self.assertEqual(TestDimension.UNIT, result.dimension)
        self.assertEqual(TestState.PASSED, result.state)
        self.assertEqual(1.23, result.duration)
        self.assertEqual({"test_count": 42}, result.details)
        
        # Test conversion to dict
        result_dict = result.to_dict()
        self.assertEqual("UNIT", result_dict["dimension"])
        self.assertEqual("PASSED", result_dict["state"])
        self.assertEqual(1.23, result_dict["duration"])
        self.assertEqual({"test_count": 42}, result_dict["details"])
        
        # Test conversion from dict
        new_result = TestResult.from_dict(result_dict)
        self.assertEqual(result.dimension, new_result.dimension)
        self.assertEqual(result.state, new_result.state)
        self.assertEqual(result.duration, new_result.duration)
        self.assertEqual(result.details, new_result.details)
    
    def test_test_run(self):
        """Test creating and manipulating TestRun objects."""
        # Create a test run
        timestamp = datetime.datetime.now()
        run = TestRun(
            id="test_123",
            timestamp=timestamp,
            trigger="manual",
            source_files=["test_file.py"]
        )
        
        # Add results
        run.results[TestDimension.UNIT] = TestResult(
            dimension=TestDimension.UNIT,
            state=TestState.PASSED,
            duration=1.0
        )
        
        run.results[TestDimension.INTEGRATION] = TestResult(
            dimension=TestDimension.INTEGRATION,
            state=TestState.FAILED,
            duration=2.0
        )
        
        # Update state
        run.update_state()
        
        # Verify properties
        self.assertEqual("test_123", run.id)
        self.assertEqual(timestamp, run.timestamp)
        self.assertEqual("manual", run.trigger)
        self.assertEqual(["test_file.py"], run.source_files)
        self.assertEqual(2, len(run.results))
        self.assertEqual(3.0, run.total_duration)
        self.assertEqual(TestState.FAILED, run.state)
        
        # Test conversion to dict
        run_dict = run.to_dict()
        self.assertEqual("test_123", run_dict["id"])
        self.assertEqual(timestamp.isoformat(), run_dict["timestamp"])
        self.assertEqual("manual", run_dict["trigger"])
        self.assertEqual(["test_file.py"], run_dict["source_files"])
        self.assertEqual("FAILED", run_dict["state"])
        
        # Test conversion from dict
        new_run = TestRun.from_dict(run_dict)
        self.assertEqual(run.id, new_run.id)
        self.assertEqual(run.trigger, new_run.trigger)
        self.assertEqual(run.source_files, new_run.source_files)
        self.assertEqual(run.state, new_run.state)
    
    def test_get_overall_state(self):
        """Test the logic for determining overall state."""
        # Create a test run
        run = TestRun(
            id="test_123",
            timestamp=datetime.datetime.now(),
            trigger="manual"
        )
        
        # Empty run should be UNKNOWN
        self.assertEqual(TestState.UNKNOWN, run.get_overall_state())
        
        # All passed should be PASSED
        run.results[TestDimension.UNIT] = TestResult(
            dimension=TestDimension.UNIT,
            state=TestState.PASSED
        )
        
        run.results[TestDimension.INTEGRATION] = TestResult(
            dimension=TestDimension.INTEGRATION,
            state=TestState.PASSED
        )
        
        self.assertEqual(TestState.PASSED, run.get_overall_state())
        
        # Any failed should be FAILED
        run.results[TestDimension.SECURITY] = TestResult(
            dimension=TestDimension.SECURITY,
            state=TestState.FAILED
        )
        
        self.assertEqual(TestState.FAILED, run.get_overall_state())
        
        # Any running should be RUNNING
        run.results = {}
        run.results[TestDimension.UNIT] = TestResult(
            dimension=TestDimension.UNIT,
            state=TestState.RUNNING
        )
        
        self.assertEqual(TestState.RUNNING, run.get_overall_state())
        
        # Mix of passed and skipped should be PASSED
        run.results = {}
        run.results[TestDimension.UNIT] = TestResult(
            dimension=TestDimension.UNIT,
            state=TestState.PASSED
        )
        
        run.results[TestDimension.INTEGRATION] = TestResult(
            dimension=TestDimension.INTEGRATION,
            state=TestState.SKIPPED
        )
        
        self.assertEqual(TestState.PASSED, run.get_overall_state())
        
        # Quantum states should be SUPERPOSITION
        run.results = {}
        run.results[TestDimension.UNIT] = TestResult(
            dimension=TestDimension.UNIT,
            state=TestState.QUANTUM_ENTANGLED
        )
        
        self.assertEqual(TestState.SUPERPOSITION, run.get_overall_state())


if __name__ == "__main__":
    unittest.main() 