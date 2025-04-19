
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

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from omega_ai.utils.redis_manager import RedisManager
from omega_ai.trading.btc_organic_tracker import (
    BTCOrganicTracker,
    OrganicState,
    BioEnergyLevel,
    OrganicPeriod
)

@pytest.fixture
def redis_manager():
    """Create a mock RedisManager."""
    mock_redis = Mock(spec=RedisManager)
    return mock_redis

@pytest.fixture
def sample_price_data():
    """Create sample price data for testing."""
    dates = pd.date_range(start='2024-01-01', periods=100, freq='H')
    data = {
        'open': np.random.normal(50000, 1000, 100),
        'high': np.random.normal(50500, 1000, 100),
        'low': np.random.normal(49500, 1000, 100),
        'close': np.random.normal(50000, 1000, 100),
        'volume': np.random.lognormal(10, 1, 100)
    }
    return pd.DataFrame(data, index=dates)

@pytest.fixture
def tracker(redis_manager):
    """Create a BTCOrganicTracker instance with mocked Redis."""
    with patch('omega_ai.trading.btc_organic_tracker.RedisManager', return_value=redis_manager):
        tracker = BTCOrganicTracker()
        yield tracker

def test_init_with_redis(tracker, redis_manager):
    """Test tracker initialization with Redis."""
    # Verify initial state is stored in Redis
    redis_manager.set_with_validation.assert_called_with(
        "omega:organic_tracker:state",
        {
            "current_state": OrganicState.UNKNOWN.value,
            "bio_energy_level": BioEnergyLevel.GROUNDED.value,
            "current_organic_streak_days": 0,
            "record_organic_streak_days": 0,
            "total_organic_days": 0,
            "total_days_analyzed": 0,
            "highest_organic_score": 0.0,
            "schumann_correlation": 0.0,
            "fibo_alignments_count": 0
        }
    )

def test_update_with_price_data_redis_storage(tracker, redis_manager, sample_price_data):
    """Test that price data updates are stored in Redis."""
    # Mock the organic score calculation to return a known value
    with patch.object(tracker, '_calculate_organic_score', return_value=0.85):
        with patch.object(tracker, '_calculate_schumann_alignment', return_value=0.75):
            with patch.object(tracker, '_detect_fibonacci_alignments', return_value=2):
                tracker.update_with_price_data(sample_price_data)
    
    # Verify state update in Redis
    redis_manager.set_with_validation.assert_called_with(
        "omega:organic_tracker:state",
        {
            "current_state": tracker.current_state.value,
            "bio_energy_level": tracker.bio_energy_level.value,
            "current_organic_streak_days": tracker.current_organic_streak_days,
            "record_organic_streak_days": tracker.record_organic_streak_days,
            "total_organic_days": tracker.total_organic_days,
            "total_days_analyzed": tracker.total_days_analyzed,
            "highest_organic_score": tracker.highest_organic_score,
            "schumann_correlation": tracker.schumann_correlation,
            "fibo_alignments_count": tracker.fibo_alignments_count
        }
    )

def test_organic_period_storage(tracker, redis_manager):
    """Test storage of organic periods in Redis."""
    # Create a sample organic period
    period = OrganicPeriod(
        start_date=datetime.now() - timedelta(days=1),
        end_date=datetime.now(),
        avg_organic_score=0.85,
        max_organic_score=0.95,
        avg_schumann_freq=7.83,
        bio_energy=BioEnergyLevel.ELEVATED,
        fibo_alignments=3
    )
    
    # Add period to tracker
    tracker.organic_periods.append(period)
    tracker._update_period_tracking()
    
    # Verify period storage in Redis
    redis_manager.set_with_validation.assert_called_with(
        "omega:organic_tracker:periods",
        [{
            "start_date": period.start_date.isoformat(),
            "end_date": period.end_date.isoformat(),
            "avg_organic_score": period.avg_organic_score,
            "max_organic_score": period.max_organic_score,
            "avg_schumann_freq": period.avg_schumann_freq,
            "bio_energy": period.bio_energy.value,
            "fibo_alignments": period.fibo_alignments
        }]
    )

def test_load_state_from_redis(redis_manager):
    """Test loading tracker state from Redis."""
    # Mock Redis state
    state = {
        "current_state": OrganicState.ORGANIC.value,
        "bio_energy_level": BioEnergyLevel.ELEVATED.value,
        "current_organic_streak_days": 5,
        "record_organic_streak_days": 10,
        "total_organic_days": 15,
        "total_days_analyzed": 20,
        "highest_organic_score": 0.95,
        "schumann_correlation": 0.8,
        "fibo_alignments_count": 25
    }
    redis_manager.get_cached.return_value = state
    
    # Create tracker with mocked Redis state
    with patch('omega_ai.trading.btc_organic_tracker.RedisManager', return_value=redis_manager):
        tracker = BTCOrganicTracker()
        
        # Verify state was loaded
        assert tracker.current_state == OrganicState.ORGANIC
        assert tracker.bio_energy_level == BioEnergyLevel.ELEVATED
        assert tracker.current_organic_streak_days == 5
        assert tracker.record_organic_streak_days == 10
        assert tracker.total_organic_days == 15
        assert tracker.total_days_analyzed == 20
        assert tracker.highest_organic_score == 0.95
        assert tracker.schumann_correlation == 0.8
        assert tracker.fibo_alignments_count == 25

def test_load_periods_from_redis(redis_manager):
    """Test loading organic periods from Redis."""
    # Mock Redis periods
    period_data = [{
        "start_date": "2024-03-15T00:00:00",
        "end_date": "2024-03-16T00:00:00",
        "avg_organic_score": 0.85,
        "max_organic_score": 0.95,
        "avg_schumann_freq": 7.83,
        "bio_energy": BioEnergyLevel.ELEVATED.value,
        "fibo_alignments": 3
    }]
    redis_manager.get_cached.side_effect = [None, period_data]  # First call for state, second for periods
    
    # Create tracker with mocked Redis data
    with patch('omega_ai.trading.btc_organic_tracker.RedisManager', return_value=redis_manager):
        tracker = BTCOrganicTracker()
        
        # Verify periods were loaded
        assert len(tracker.organic_periods) == 1
        period = tracker.organic_periods[0]
        assert period.start_date == datetime.fromisoformat("2024-03-15T00:00:00")
        assert period.end_date == datetime.fromisoformat("2024-03-16T00:00:00")
        assert period.avg_organic_score == 0.85
        assert period.max_organic_score == 0.95
        assert period.avg_schumann_freq == 7.83
        assert period.bio_energy == BioEnergyLevel.ELEVATED
        assert period.fibo_alignments == 3 