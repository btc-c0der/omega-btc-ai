
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
MM Trap Detector Package

This package contains components for detecting and analyzing market maker trap patterns
in BTC price movements.

Components:
- High Frequency Detector: Detects rapid price manipulation events
- Fibonacci Detector: Analyzes price movements relative to Fibonacci levels
- MM Trap Consumer: Processes market maker trap events from the queue
- Grafana Reporter: Reports trap events to Grafana dashboards
"""

import logging
import os
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

# Export the high frequency detector singleton
try:
    from omega_ai.mm_trap_detector.high_frequency_detector import HighFrequencyTrapDetector, hf_detector
    from omega_ai.mm_trap_detector.fibonacci_detector import FibonacciDetector, fibonacci_detector
    from omega_ai.mm_trap_detector.fibonacci_detector import (
        check_fibonacci_level,
        update_fibonacci_data,
        detect_fibonacci_confluence,
        get_current_fibonacci_levels
    )
    
    logger.info("MM Trap Detector components loaded successfully")
    __all__ = [
        'HighFrequencyTrapDetector',
        'hf_detector',
        'FibonacciDetector',
        'fibonacci_detector',
        'check_fibonacci_level',
        'update_fibonacci_data',
        'detect_fibonacci_confluence',
        'get_current_fibonacci_levels'
    ]
except ImportError as e:
    logger.warning(f"Could not load all MM Trap Detector components: {e}")
    __all__ = []
except Exception as e:
    logger.error(f"Error initializing MM Trap Detector package: {e}")
    __all__ = []
