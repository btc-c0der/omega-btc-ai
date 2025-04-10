
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

import time
from omega_ai.mm_trap_detector.mm_trap_detector import MMTrapDetector

def _run_detector_once(mock_sleep):
    """Run one iteration of the trap detector process."""
    # Save original sleep function
    original_sleep = time.sleep
    
    # Replace sleep with mock during execution
    time.sleep = mock_sleep
    
    # Create detector instance
    detector = MMTrapDetector()
    
    try:
        # Call the main processor function once
        detector.process_price_update(detector.current_btc_price)
    finally:
        # Restore original sleep function
        time.sleep = original_sleep
    
    # Assert that sleep was called (to prevent infinite loop in tests)
    mock_sleep.assert_called_once()
    # Reset mock for next call
    mock_sleep.reset_mock()