
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
    MAGENTA = '\033[35m'  # Darker magenta
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