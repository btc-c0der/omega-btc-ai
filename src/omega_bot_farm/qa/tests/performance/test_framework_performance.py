"""
Performance test for the quantum framework.

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
import time
import unittest
import tempfile
import datetime
import json
import random
from typing import Dict, List, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the quantum runner components
try:
    from quantum_runner.types import TestDimension, TestState
    from quantum_runner.data_models import TestResult, TestRun
except ImportError:
    # Fallback import mechanism
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../quantum_runner')))
    from types import TestDimension, TestState
    from data_models import TestResult, TestRun

# Check if pytest-benchmark is available
try:
    import pytest
    from pytest import approx
    BENCHMARK_AVAILABLE = hasattr(pytest, 'mark') and hasattr(pytest.mark, 'benchmark')
except ImportError:
    BENCHMARK_AVAILABLE = False
    print("Note: pytest-benchmark not available. Some tests will be skipped.")

# Define benchmark decorator for when pytest-benchmark is not available
def simple_benchmark(func):
    """Simple benchmark decorator for when pytest-benchmark is not available."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time:.6f} seconds")
        return result
    return wrapper

class TestResultPerformance:
    """Performance benchmarks for TestResult operations."""
    
    @pytest.mark.benchmark(
        group="test_result",
        min_time=0.1,
        max_time=0.5,
        min_rounds=5,
        timer=time.time,
        disable_gc=True,
        warmup=False
    )
    def test_create_test_result(self, benchmark):
        """Benchmark creating TestResult objects."""
        def create_result():
            return TestResult(
                dimension=TestDimension.UNIT,
                state=TestState.PASSED,
                duration=0.123,
                timestamp=datetime.datetime.now(),
                details={"test_count": 42},
                entangled_dimensions=[TestDimension.INTEGRATION]
            )
        
        # Run the benchmark
        result = benchmark(create_result)
        
        # Verify the result
        assert result.dimension == TestDimension.UNIT
        assert result.state == TestState.PASSED
    
    @pytest.mark.benchmark(
        group="test_result",
        min_time=0.1,
        max_time=0.5,
        min_rounds=5,
        timer=time.time,
        disable_gc=True,
        warmup=False
    )
    def test_test_result_to_dict(self, benchmark):
        """Benchmark converting TestResult to dictionary."""
        # Create a test result
        result = TestResult(
            dimension=TestDimension.UNIT,
            state=TestState.PASSED,
            duration=0.123,
            timestamp=datetime.datetime.now(),
            details={"test_count": 42},
            entangled_dimensions=[TestDimension.INTEGRATION]
        )
        
        # Run the benchmark
        result_dict = benchmark(result.to_dict)
        
        # Verify the result
        assert result_dict["dimension"] == "UNIT"
        assert result_dict["state"] == "PASSED"
    
    @pytest.mark.benchmark(
        group="test_result",
        min_time=0.1,
        max_time=0.5,
        min_rounds=5,
        timer=time.time,
        disable_gc=True,
        warmup=False
    )
    def test_test_result_from_dict(self, benchmark):
        """Benchmark creating TestResult from dictionary."""
        # Create a dictionary
        result_dict = {
            "dimension": "UNIT",
            "state": "PASSED",
            "duration": 0.123,
            "timestamp": datetime.datetime.now().isoformat(),
            "details": {"test_count": 42},
            "entangled_dimensions": ["INTEGRATION"]
        }
        
        # Run the benchmark
        result = benchmark(TestResult.from_dict, result_dict)
        
        # Verify the result
        assert result.dimension == TestDimension.UNIT
        assert result.state == TestState.PASSED


class TestRunPerformance:
    """Performance benchmarks for TestRun operations."""
    
    @pytest.mark.benchmark(
        group="test_run",
        min_time=0.1,
        max_time=0.5,
        min_rounds=5,
        timer=time.time,
        disable_gc=True,
        warmup=False
    )
    def test_create_test_run(self, benchmark):
        """Benchmark creating TestRun objects."""
        def create_run():
            return TestRun(
                id="test_run_123",
                timestamp=datetime.datetime.now(),
                trigger="manual",
                source_files=["file1.py", "file2.py"]
            )
        
        # Run the benchmark
        run = benchmark(create_run)
        
        # Verify the result
        assert run.id == "test_run_123"
        assert run.trigger == "manual"
    
    @pytest.mark.benchmark(
        group="test_run",
        min_time=0.1,
        max_time=0.5,
        min_rounds=5,
        timer=time.time,
        disable_gc=True,
        warmup=False
    )
    def test_test_run_with_results(self, benchmark):
        """Benchmark creating TestRun with multiple results."""
        def create_run_with_results():
            run = TestRun(
                id="test_run_123",
                timestamp=datetime.datetime.now(),
                trigger="manual",
                source_files=["file1.py", "file2.py"]
            )
            
            # Add results for all dimensions
            for dimension in TestDimension:
                run.results[dimension] = TestResult(
                    dimension=dimension,
                    state=random.choice([TestState.PASSED, TestState.FAILED]),
                    duration=random.random() * 5
                )
            
            # Update state
            run.update_state()
            return run
        
        # Run the benchmark
        run = benchmark(create_run_with_results)
        
        # Verify the result
        assert len(run.results) == len(list(TestDimension))
    
    @pytest.mark.benchmark(
        group="test_run",
        min_time=0.1,
        max_time=0.5,
        min_rounds=5,
        timer=time.time,
        disable_gc=True,
        warmup=False
    )
    def test_test_run_to_dict(self, benchmark):
        """Benchmark converting TestRun to dictionary."""
        # Create a test run with results
        run = TestRun(
            id="test_run_123",
            timestamp=datetime.datetime.now(),
            trigger="manual",
            source_files=["file1.py", "file2.py"]
        )
        
        # Add results for all dimensions
        for dimension in TestDimension:
            run.results[dimension] = TestResult(
                dimension=dimension,
                state=random.choice([TestState.PASSED, TestState.FAILED]),
                duration=random.random() * 5
            )
        
        # Update state
        run.update_state()
        
        # Run the benchmark
        run_dict = benchmark(run.to_dict)
        
        # Verify the result
        assert run_dict["id"] == "test_run_123"
        assert run_dict["trigger"] == "manual"
    
    @pytest.mark.benchmark(
        group="test_run",
        min_time=0.1,
        max_time=0.5,
        min_rounds=5,
        timer=time.time,
        disable_gc=True,
        warmup=False
    )
    def test_large_test_run_serialization(self, benchmark):
        """Benchmark serializing a large TestRun to JSON."""
        # Create a test run with many detailed results
        run = TestRun(
            id="large_test_run",
            timestamp=datetime.datetime.now(),
            trigger="manual",
            source_files=["file1.py", "file2.py"]
        )
        
        # Add results for all dimensions with detailed output
        for dimension in TestDimension:
            # Create a large details dictionary with test output
            details = {
                "output": "".join(f"Test {i}: {'PASS' if i % 3 != 0 else 'FAIL'}\n" for i in range(500)),
                "error": "".join(f"Error in test {i}\n" for i in range(50) if i % 10 == 0),
                "returncode": 1 if dimension == TestDimension.SECURITY else 0,
                "command": f"pytest -xvs tests/{dimension.name.lower()}",
                "reports": {
                    "xml": f"reports/{dimension.name.lower()}_report.xml",
                    "html": f"reports/{dimension.name.lower()}_report.html",
                    "json": f"reports/{dimension.name.lower()}_report.json"
                }
            }
            
            run.results[dimension] = TestResult(
                dimension=dimension,
                state=TestState.PASSED if dimension != TestDimension.SECURITY else TestState.FAILED,
                duration=random.random() * 10,
                details=details
            )
        
        # Update state
        run.update_state()
        
        # Convert to dict first
        run_dict = run.to_dict()
        
        # Benchmark JSON serialization
        def serialize_to_json():
            return json.dumps(run_dict, indent=2)
        
        # Run the benchmark
        json_str = benchmark(serialize_to_json)
        
        # Verify the result
        assert len(json_str) > 1000  # Should be a large JSON string


# Create a fallback test class for when pytest-benchmark is not available
class FallbackPerformanceTests(unittest.TestCase):
    """Fallback tests that run when pytest-benchmark is not available."""
    
    @unittest.skipIf(BENCHMARK_AVAILABLE, "Using pytest-benchmark instead")
    def test_create_test_result_performance(self):
        """Test performance of creating TestResult objects."""
        @simple_benchmark
        def create_results(count):
            results = []
            for i in range(count):
                results.append(TestResult(
                    dimension=TestDimension.UNIT,
                    state=TestState.PASSED,
                    duration=0.123,
                    timestamp=datetime.datetime.now(),
                    details={"test_count": 42},
                    entangled_dimensions=[TestDimension.INTEGRATION]
                ))
            return results
        
        # Create 1000 test results
        results = create_results(1000)
        self.assertEqual(1000, len(results))
    
    @unittest.skipIf(BENCHMARK_AVAILABLE, "Using pytest-benchmark instead")
    def test_test_run_serialization_performance(self):
        """Test performance of serializing TestRun objects."""
        # Create a test run with results
        run = TestRun(
            id="test_run_123",
            timestamp=datetime.datetime.now(),
            trigger="manual",
            source_files=["file1.py", "file2.py"]
        )
        
        # Add results for all dimensions
        for dimension in TestDimension:
            run.results[dimension] = TestResult(
                dimension=dimension,
                state=random.choice([TestState.PASSED, TestState.FAILED]),
                duration=random.random() * 5
            )
        
        # Update state
        run.update_state()
        
        @simple_benchmark
        def serialize_run(run_obj):
            # Convert to dict
            run_dict = run_obj.to_dict()
            # Serialize to JSON
            return json.dumps(run_dict, indent=2)
        
        # Serialize the test run
        json_str = serialize_run(run)
        self.assertIsInstance(json_str, str)


if __name__ == "__main__":
    if BENCHMARK_AVAILABLE:
        # Run with pytest if benchmark is available
        import sys
        sys.exit(pytest.main(["-xvs", __file__]))
    else:
        # Otherwise run with unittest
        unittest.main() 