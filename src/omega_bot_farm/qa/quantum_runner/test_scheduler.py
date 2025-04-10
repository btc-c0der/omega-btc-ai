
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
Test scheduling system for the Quantum Test Runner.
"""

import time
import threading
import queue
import logging
from typing import Dict, List, Optional, Any

from .types import TestDimension

logger = logging.getLogger("0M3G4_B0TS_QA_AUT0_TEST_SUITES_RuNn3R_5D")

class TestScheduler:
    """Schedules tests to run at specific intervals."""
    
    def __init__(self, event_queue: queue.Queue, schedule: Dict[str, int]):
        """
        Initialize the test scheduler.
        
        Args:
            event_queue: Queue to put scheduled test events
            schedule: Dictionary mapping test types to intervals in seconds
        """
        self.event_queue = event_queue
        self.schedule = schedule
        self.running = False
        self.thread = None
        self.last_run = {
            'full': 0,
            'unit': 0,
            'integration': 0,
            'performance': 0,
            'security': 0
        }
    
    def start(self) -> None:
        """Start the scheduler thread."""
        if self.running:
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.thread.start()
        logger.info("Test scheduler started")
    
    def stop(self) -> None:
        """Stop the scheduler thread."""
        if not self.running:
            return
            
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        logger.info("Test scheduler stopped")
    
    def _scheduler_loop(self) -> None:
        """Main loop for the scheduler thread."""
        while self.running:
            try:
                self._check_schedules()
                time.sleep(60)  # Check once per minute
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                time.sleep(60)  # Wait a bit after an error
    
    def _check_schedules(self) -> None:
        """Check if any tests need to be run based on schedules."""
        now = time.time()
        
        # Check each scheduled test type
        for test_type, interval in self.schedule.items():
            if now - self.last_run.get(test_type, 0) >= interval:
                self._schedule_test(test_type)
                self.last_run[test_type] = now
    
    def _schedule_test(self, test_type: str) -> None:
        """Schedule a test of the specified type."""
        logger.info(f"Scheduling test: {test_type}")
        
        try:
            if test_type == 'full':
                # Run all test dimensions
                self.event_queue.put((None, list(TestDimension)))
            elif test_type == 'unit':
                self.event_queue.put((None, [TestDimension.UNIT]))
            elif test_type == 'integration':
                self.event_queue.put((None, [TestDimension.INTEGRATION]))
            elif test_type == 'performance':
                self.event_queue.put((None, [TestDimension.PERFORMANCE]))
            elif test_type == 'security':
                self.event_queue.put((None, [TestDimension.SECURITY]))
        except Exception as e:
            logger.error(f"Error scheduling test {test_type}: {e}") 