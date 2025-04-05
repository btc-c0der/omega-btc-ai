"""
Core type definitions for the Quantum Test Runner.
"""

import os
import sys
import enum
from enum import Enum, auto

# ANSI colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'  # Same as HEADER for now
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