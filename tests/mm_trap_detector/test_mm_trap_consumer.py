"""
Tests for the Market Maker Trap Consumer component.

This test suite demonstrates TDD best practices including:
1. Complete mocking of external dependencies (Redis, DB, etc.)
2. Standardized test structure following Arrange-Act-Assert pattern
3. Comprehensive error handling tests
4. Clear test organization with fixtures and focused test methods

Each test focuses on a specific aspect of the trap processor's functionality,
from basic initialization to complex batch processing with error handling.
"""

import pytest
import json
import asyncio
import time
from unittest.mock import MagicMock, patch, AsyncMock
from datetime import datetime, timezone

from omega_ai.mm_trap_detector.mm_trap_consumer import TrapProcessor


# ---- Fixtures ----

@pytest.fixture
def mock_redis():
    """
    Mock Redis connection with proper setup for all tests.
    
    This fixture provides a consistent mock Redis object that can be used
    across multiple tests, eliminating the need to recreate the same mock
    in each test method. The mock is configured with default return values
    that represent typical Redis responses for the methods used by the TrapProcessor.
    
    Returns:
        MagicMock: A mock Redis object with pre-configured return values
    """
    mock = MagicMock()
    # Set default return values that all tests can use
    mock.zrange.return_value = []
    mock.zcard.return_value = 0
    mock.zrem.return_value = 1
    return mock


@pytest.fixture
def mock_db():
    """
    Mock database manager.
    
    This fixture provides a mock database interface for testing trap persistence
    operations without requiring an actual database connection.
    
    Returns:
        MagicMock: A mock database manager with pre-configured return values
    """
    mock = MagicMock()
    # Set up default successful return values
    mock.insert_possible_mm_trap.return_value = True
    return mock


@pytest.fixture
def trap_processor():
    """
    Create a trap processor with mocked dependencies for testing.
    
    This fixture creates an isolated TrapProcessor instance with all external
    dependencies (Redis, DB operations, time) mocked out to ensure tests are
    repeatable and don't rely on external services. The processor is configured
    with test-specific settings to facilitate faster testing.
    
    Note that this approach demonstrates proper dependency injection and
    the use of patching for effective isolation in tests.
    
    Returns:
        TrapProcessor: A trap processor instance configured for testing
    """
    # Mock all external dependencies
    with patch('omega_ai.mm_trap_detector.mm_trap_consumer.redis.Redis', return_value=MagicMock()) as mock_redis_cls:
        with patch('omega_ai.mm_trap_detector.mm_trap_consumer.time.sleep') as mock_sleep:
            with patch('omega_ai.mm_trap_detector.mm_trap_consumer.insert_possible_mm_trap') as mock_db_insert:
                # Create the processor with controlled test settings
                processor = TrapProcessor()
                
                # Explicitly override the attributes we want to test with 
                # This avoids linter errors from the constructor parameters
                processor.queue_name = "mm_trap_queue:test"
                processor.batch_size = 2
                processor.processing_interval = 0.01
                
                # Override Redis connection with our test mock
                processor.redis_conn = mock_redis_cls.return_value
                
                return processor


# ---- Test Class ----

class TestTrapProcessor:
    """
    Comprehensive tests for the Market Maker Trap Processor component.
    
    These tests verify the trap processor's ability to:
    1. Process individual traps with proper confidence classification
    2. Handle batches of traps from the queue
    3. Manage errors gracefully (invalid JSON, missing fields, DB failures)
    4. Provide accurate status information
    
    The test organization follows the standard lifecycle of the processor:
    - Initialization
    - Individual trap processing
    - Batch processing
    - Error handling
    - Run loop
    - Status reporting
    """
    
    def test_init(self, trap_processor):
        """
        Test initialization with proper parameters.
        
        Verifies that the trap processor initializes with the correct
        default values and configuration.
        """
        assert trap_processor.queue_name == "mm_trap_queue:test"
        assert trap_processor.batch_size == 2
        assert trap_processor.processing_interval == 0.01
        assert trap_processor.processed_count == 0
        assert trap_processor.high_confidence_count == 0
        assert trap_processor.low_confidence_count == 0
        
    @patch('omega_ai.mm_trap_detector.mm_trap_consumer.insert_possible_mm_trap')
    def test_process_trap_high_confidence(self, mock_db_insert, trap_processor):
        """
        Test processing a high-confidence trap.
        
        Verifies that high-confidence traps (>= 0.7) are correctly:
        1. Identified as high confidence
        2. Counted in the high confidence counter
        3. Stored in the database
        4. Included in the total processed count
        """
        # Arrange
        trap_data = {
            "type": "Fake Pump",
            "confidence": 0.85,
            "price": 81000,
            "price_change": 1.2,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Act
        result = trap_processor.process_trap(json.dumps(trap_data))
        
        # Assert
        assert result is True
        assert trap_processor.processed_count == 1
        assert trap_processor.high_confidence_count == 1
        assert trap_processor.low_confidence_count == 0
        mock_db_insert.assert_called_once()
        
    @patch('omega_ai.mm_trap_detector.mm_trap_consumer.insert_possible_mm_trap')
    def test_process_trap_low_confidence(self, mock_db_insert, trap_processor):
        """
        Test processing a low-confidence trap.
        
        Verifies that low-confidence traps (< 0.7) are correctly:
        1. Identified as low confidence
        2. Counted in the low confidence counter
        3. Still stored in the database (for later analysis)
        4. Included in the total processed count
        """
        # Arrange
        trap_data = {
            "type": "Potential Bear Trap",
            "confidence": 0.4,
            "price": 80000,
            "price_change": -0.8,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Act
        result = trap_processor.process_trap(json.dumps(trap_data))
        
        # Assert
        assert result is True
        assert trap_processor.processed_count == 1
        assert trap_processor.high_confidence_count == 0
        assert trap_processor.low_confidence_count == 1
        mock_db_insert.assert_called_once()
    
    def test_process_trap_invalid_json(self, trap_processor):
        """
        Test error handling for invalid JSON.
        
        Verifies that the processor gracefully handles malformed JSON
        without crashing, and properly increments the error counter.
        This is a critical error handling test to ensure robustness.
        """
        # Arrange
        invalid_data = "{invalid json"
        
        # Act
        result = trap_processor.process_trap(invalid_data)
        
        # Assert
        assert result is False
        assert trap_processor.processed_count == 0
        assert trap_processor.error_count == 1
    
    def test_process_trap_missing_fields(self, trap_processor):
        """
        Test error handling for missing required fields.
        
        Verifies that the processor gracefully handles valid JSON that is
        missing required fields, and properly increments the error counter.
        This tests input validation capabilities.
        """
        # Arrange
        incomplete_data = json.dumps({"type": "Fake Pump"})  # Missing confidence and other fields
        
        # Act
        result = trap_processor.process_trap(incomplete_data)
        
        # Assert
        assert result is False
        assert trap_processor.processed_count == 0
        assert trap_processor.error_count == 1
    
    @patch('omega_ai.mm_trap_detector.mm_trap_consumer.insert_possible_mm_trap')
    def test_database_failure(self, mock_db_insert, trap_processor):
        """
        Test handling database insertion failure.
        
        Verifies that the processor handles database failures gracefully
        by returning appropriate error status and incrementing the error count
        without raising exceptions. This is critical for maintaining system
        stability during infrastructure issues.
        """
        # Arrange
        mock_db_insert.return_value = False  # Simulate DB failure
        trap_data = {
            "type": "Fake Pump",
            "confidence": 0.85,
            "price": 81000,
            "price_change": 1.2,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Act
        result = trap_processor.process_trap(json.dumps(trap_data))
        
        # Assert - we should handle the error gracefully
        assert result is False
        assert trap_processor.processed_count == 0
        assert trap_processor.error_count == 1
    
    def test_process_batch_empty_queue(self, trap_processor):
        """
        Test processing a batch when queue is empty.
        
        Verifies that the batch processing function handles an empty queue
        gracefully, returning 0 processed items and not advancing the queue position.
        """
        # Arrange
        trap_processor.redis_conn.zrange.return_value = []
        
        # Act
        processed = trap_processor.process_batch()
        
        # Assert
        assert processed == 0
        assert trap_processor.queue_position == 0
    
    def test_process_batch_with_traps(self, trap_processor):
        """
        Test processing a batch of traps from the queue.
        
        Verifies that multiple traps can be processed in a batch,
        with each trap being properly processed and removed from the queue.
        """
        # Arrange
        mock_traps = [
            json.dumps({"type": "Fake Pump", "confidence": 0.85, "price": 81000, "price_change": 1.2}),
            json.dumps({"type": "Liquidity Grab", "confidence": 0.7, "price": 80500, "price_change": -0.6})
        ]
        trap_processor.redis_conn.zrange.return_value = mock_traps
        
        # Mock successful processing
        trap_processor.process_trap = MagicMock(return_value=True)
        
        # Act
        processed = trap_processor.process_batch()
        
        # Assert
        assert processed == 2
        assert trap_processor.process_trap.call_count == 2
        # Verify we removed processed items from the queue
        trap_processor.redis_conn.zrem.assert_called()
    
    def test_process_batch_with_partial_failures(self, trap_processor):
        """
        Test batch processing with some traps failing.
        
        Verifies that batch processing can continue even when some individual
        trap items fail validation or processing. This ensures resilience where
        one bad trap doesn't block processing of other valid traps.
        """
        # Arrange
        mock_traps = [
            json.dumps({"type": "Fake Pump", "confidence": 0.85, "price": 81000, "price_change": 1.2}),
            json.dumps({"type": "Invalid", "confidence": 0.7}),  # This one will fail due to missing fields
            json.dumps({"type": "Liquidity Grab", "confidence": 0.7, "price": 80500, "price_change": -0.6})
        ]
        trap_processor.redis_conn.zrange.return_value = mock_traps
        
        # Mock process_trap to succeed for valid traps and fail for invalid ones
        def side_effect(trap_json):
            trap = json.loads(trap_json)
            return "price" in trap
            
        trap_processor.process_trap = MagicMock(side_effect=side_effect)
        
        # Act
        processed = trap_processor.process_batch()
        
        # Assert
        assert processed == 2  # Only 2 of 3 succeed
        assert trap_processor.process_trap.call_count == 3
        trap_processor.redis_conn.zrem.assert_called()
    
    @patch('omega_ai.mm_trap_detector.mm_trap_consumer.time.sleep')
    def test_run_with_stop_event(self, mock_sleep, trap_processor):
        """
        Test run loop with stop event.
        
        Verifies that the main run loop:
        1. Processes batches continuously
        2. Respects the stop event to terminate gracefully
        3. Waits the appropriate interval between batches
        
        This test simulates a run that processes two batches and then terminates,
        verifying the full execution lifecycle.
        """
        # Arrange
        stop_event = MagicMock()
        stop_event.is_set.side_effect = [False, False, True]  # Run twice then stop
        
        trap_processor.process_batch = MagicMock(return_value=2)  # Process 2 items each time
        
        # Act
        trap_processor.run(stop_event)
        
        # Assert
        assert trap_processor.process_batch.call_count == 2
        assert mock_sleep.call_count == 2
    
    @patch('omega_ai.mm_trap_detector.mm_trap_consumer.redis.Redis')
    def test_redis_connection_error(self, mock_redis_cls):
        """
        Test handling Redis connection errors.
        
        Verifies that Redis connection errors during initialization are
        properly surfaced and not silently ignored. This ensures that
        the application doesn't start with a broken Redis connection.
        """
        # Arrange - simulate Redis connection failure
        mock_redis_cls.side_effect = Exception("Connection failed")
        
        # Act & Assert - we should handle this gracefully
        with pytest.raises(Exception) as excinfo:
            processor = TrapProcessor()
            
        assert "Connection failed" in str(excinfo.value)
        
    def test_get_queue_status(self, trap_processor):
        """
        Test getting queue status information.
        
        Verifies that the status reporting functionality correctly aggregates:
        1. Queue size from Redis
        2. Processing statistics (counts by confidence level)
        3. Error counts
        4. Processing rate information
        
        This is important for monitoring and operational visibility.
        """
        # Arrange
        trap_processor.redis_conn.zcard.return_value = 150
        trap_processor.processed_count = 75
        trap_processor.high_confidence_count = 40
        trap_processor.low_confidence_count = 35
        trap_processor.error_count = 10
        
        # Act
        status = trap_processor.get_queue_status()
        
        # Assert
        assert status["queue_size"] == 150
        assert status["processed_total"] == 75
        assert status["high_confidence"] == 40
        assert status["low_confidence"] == 35
        assert status["error_count"] == 10
        assert "processing_rate" in status