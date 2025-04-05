"""
Data models for the Quantum Test Runner.
"""

import datetime
from typing import Dict, List, Set, Any, Optional, Tuple, Union, cast
from dataclasses import dataclass, field

from .types import TestDimension, TestState

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