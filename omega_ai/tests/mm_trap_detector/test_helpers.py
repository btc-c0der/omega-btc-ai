import time
from omega_ai.mm_trap_detector.mm_trap_processor import process_mm_trap

def _run_detector_once(mock_sleep):
    """Run one iteration of the trap detector process."""
    # Save original sleep function
    original_sleep = time.sleep
    
    # Replace sleep with mock during execution
    time.sleep = mock_sleep
    
    # Set flag to exit after one iteration
    process_mm_trap._test_single_run = True
    
    try:
        # Call the main processor function once
        process_mm_trap()
    finally:
        # Restore original sleep function
        time.sleep = original_sleep
        # Reset the test flag
        process_mm_trap._test_single_run = False
    
    # Assert that sleep was called (to prevent infinite loop in tests)
    mock_sleep.assert_called_once()
    # Reset mock for next call
    mock_sleep.reset_mock()