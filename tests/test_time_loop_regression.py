#!/usr/bin/env python3

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
OMEGA BTC AI - Time Loop Regression Tests
=======================================

Tests for time-loop invariance of the Cosmic Price Oracle predictions.
Validates that cosmic alignment predictions remain consistent across different
calendar alignments while respecting natural cycles.

🔮 GPU (General Public Universal) License 1.0
--------------------------------------------
OMEGA BTC AI DIVINE COLLECTIVE
Licensed under the GPU (General Public Universal) License v1.0
"""

import os
import json
import pytest
import asyncio
import numpy as np
import datetime
from typing import List, Dict, Any, Optional
from unittest.mock import patch, MagicMock, AsyncMock

# Import the Cosmic Price Oracle
from omega_ai.oracle.cosmic_price_oracle import (
    CosmicPriceOracle,
    FibonacciPriceAnalyzer,
    GoldenRatioPatternMatcher,
    SchumannResonanceDetector,
    BTCDNASequencer
)

# Test constants
BASE_TIMESTAMP = 1609459200  # 2021-01-01 00:00:00 UTC
ONE_DAY_SECONDS = 86400
LUNAR_CYCLE_DAYS = 29.53  # Average lunar cycle in days
SOLAR_CYCLE_DAYS = 365.25  # Solar year in days
PHI = 1.618033988749895  # Golden Ratio
SCHUMANN_BASE_FREQUENCY = 7.83  # Hz

# Sample BTC price data - same pattern but will be tested with different timestamps
SAMPLE_PRICE_PATTERN = [
    29000.00, 29500.00, 30000.00, 32000.00, 34000.00, 
    36000.00, 38000.00, 40000.00, 41000.00, 42000.00
]

# ===================================
# Test Fixtures
# ===================================

@pytest.fixture
def base_price_history():
    """Fixture for base BTC price history data with original timestamps."""
    return [
        {"timestamp": BASE_TIMESTAMP + (i * ONE_DAY_SECONDS), "price": price}
        for i, price in enumerate(SAMPLE_PRICE_PATTERN)
    ]

@pytest.fixture
def lunar_aligned_price_history():
    """Fixture for BTC price history aligned with lunar cycle."""
    # Shift timestamps to align with lunar cycle but keep price pattern identical
    return [
        {"timestamp": BASE_TIMESTAMP + int(i * LUNAR_CYCLE_DAYS * ONE_DAY_SECONDS / 10), "price": price}
        for i, price in enumerate(SAMPLE_PRICE_PATTERN)
    ]

@pytest.fixture
def solar_aligned_price_history():
    """Fixture for BTC price history aligned with solar cycle."""
    # Shift timestamps to align with solar cycle but keep price pattern identical
    return [
        {"timestamp": BASE_TIMESTAMP + int(i * SOLAR_CYCLE_DAYS * ONE_DAY_SECONDS / 10), "price": price}
        for i, price in enumerate(SAMPLE_PRICE_PATTERN)
    ]

@pytest.fixture
def phi_aligned_price_history():
    """Fixture for BTC price history with golden ratio time intervals."""
    # Intervals follow Fibonacci/golden ratio progression
    intervals = [0]
    for i in range(1, len(SAMPLE_PRICE_PATTERN)):
        # Each interval grows by PHI compared to previous
        intervals.append(intervals[-1] + max(1, int(intervals[-1] * PHI)) if intervals[-1] > 0 else 1)
    
    return [
        {"timestamp": BASE_TIMESTAMP + (interval * ONE_DAY_SECONDS), "price": price}
        for interval, price in zip(intervals, SAMPLE_PRICE_PATTERN)
    ]

@pytest.fixture
def mock_redis_manager():
    """Fixture for mock Redis manager."""
    manager = MagicMock()
    manager.get_cached = AsyncMock(return_value=None)
    manager.set_cached = AsyncMock(return_value=True)
    manager.connect = AsyncMock(return_value=True)
    manager.ping = AsyncMock(return_value=True)
    return manager

@pytest.fixture
def mock_cosmic_oracle():
    """Fixture for mocked Cosmic Price Oracle with controlled components."""
    with patch('omega_ai.oracle.cosmic_price_oracle.EnhancedRedisManager') as mock_redis_cls:
        mock_redis_instance = MagicMock()
        mock_redis_instance.connect = AsyncMock(return_value=True)
        mock_redis_instance.get_cached = AsyncMock(return_value=None)
        mock_redis_instance.set_cached = AsyncMock(return_value=True)
        mock_redis_cls.return_value = mock_redis_instance
        
        # Create real analyzers but with deterministic behavior
        oracle = CosmicPriceOracle(redis_host="localhost", redis_port=6379)
        
        # Replace certain methods with mocks for controlled testing
        oracle.get_price_history = AsyncMock()
        oracle.get_schumann_data = AsyncMock()
        
        yield oracle

# ===================================
# Test Cases
# ===================================

@pytest.mark.asyncio
async def test_fibonacci_time_invariance(mock_cosmic_oracle, base_price_history, lunar_aligned_price_history):
    """Test that Fibonacci price levels are invariant to timestamp alignment."""
    # Extract price series only (timestamps should not affect Fibonacci levels)
    base_prices = [entry["price"] for entry in base_price_history]
    lunar_prices = [entry["price"] for entry in lunar_aligned_price_history]
    
    # Verify prices are the same despite different timestamp patterns
    assert base_prices == lunar_prices
    
    # Analyze with Fibonacci analyzer
    fib_analyzer = FibonacciPriceAnalyzer()
    base_levels = fib_analyzer.find_fibonacci_levels(base_prices)
    lunar_levels = fib_analyzer.find_fibonacci_levels(lunar_prices)
    
    # Levels should be identical since only prices matter, not timestamps
    assert base_levels["support_levels"] == lunar_levels["support_levels"]
    assert base_levels["resistance_levels"] == lunar_levels["resistance_levels"]
    assert base_levels["extension_levels"] == lunar_levels["extension_levels"]

@pytest.mark.asyncio
async def test_golden_ratio_time_invariance(mock_cosmic_oracle, base_price_history, phi_aligned_price_history):
    """Test that golden ratio pattern detection works regardless of time intervals."""
    # Extract price series only
    base_prices = [entry["price"] for entry in base_price_history]
    phi_prices = [entry["price"] for entry in phi_aligned_price_history]
    
    # Verify prices are the same despite different timestamp patterns
    assert base_prices == phi_prices
    
    # Analyze with Golden Ratio matcher
    golden_matcher = GoldenRatioPatternMatcher()
    base_patterns = golden_matcher.find_golden_patterns(base_prices)
    phi_patterns = golden_matcher.find_golden_patterns(phi_prices)
    
    # Pattern detection should yield very similar results
    # (small differences might occur due to floating point)
    assert abs(base_patterns["confidence"] - phi_patterns["confidence"]) < 0.01
    assert base_patterns["dominant_pattern"] == phi_patterns["dominant_pattern"]
    assert len(base_patterns["price_targets"]) == len(phi_patterns["price_targets"])

@pytest.mark.asyncio
async def test_schumann_resonance_cycle_detection(mock_cosmic_oracle):
    """Test that Schumann resonance cycle detection respects natural cycles."""
    # Create two sets of resonance data with the same pattern but different base frequencies
    base_resonance_data = [
        {"timestamp": BASE_TIMESTAMP + (i * ONE_DAY_SECONDS), 
         "frequency": SCHUMANN_BASE_FREQUENCY + (0.1 * np.sin(i/3)), 
         "amplitude": 0.1 + (0.05 * np.sin(i/5))}
        for i in range(30)
    ]
    
    # Shifted resonance data - same pattern but base frequency shifted
    shifted_resonance_data = [
        {"timestamp": BASE_TIMESTAMP + (i * ONE_DAY_SECONDS), 
         "frequency": (SCHUMANN_BASE_FREQUENCY + 0.5) + (0.1 * np.sin(i/3)), 
         "amplitude": 0.1 + (0.05 * np.sin(i/5))}
        for i in range(30)
    ]
    
    # Analyze with Schumann detector
    detector = SchumannResonanceDetector()
    base_cycles = detector.detect_resonance_cycles(base_resonance_data)
    shifted_cycles = detector.detect_resonance_cycles(shifted_resonance_data)
    
    # The cycle days should be the same since the pattern is the same
    assert base_cycles["amplitude_cycle_days"] == shifted_cycles["amplitude_cycle_days"]
    
    # The frequency shift should be different
    assert abs(base_cycles["frequency_shift"] - shifted_cycles["frequency_shift"]) > 0.4

@pytest.mark.asyncio
async def test_dna_sequencing_time_invariance(mock_cosmic_oracle, base_price_history, solar_aligned_price_history):
    """Test that DNA sequencing is invariant to absolute timestamps."""
    # Analyze with DNA sequencer
    dna_sequencer = BTCDNASequencer()
    base_dna = dna_sequencer.generate_dna_sequence(base_price_history)
    solar_dna = dna_sequencer.generate_dna_sequence(solar_aligned_price_history)
    
    # DNA sequence should be identical since only price changes matter, not timestamps
    assert base_dna["sequence"] == solar_dna["sequence"]
    assert base_dna["pattern_strength"] == solar_dna["pattern_strength"]
    assert base_dna["bullish_probability"] == solar_dna["bullish_probability"]

@pytest.mark.asyncio
async def test_prediction_seasonal_variance(mock_cosmic_oracle):
    """Test that predictions account for seasonal variance when provided with seasonal markers."""
    # Create price histories for different seasons with identical price patterns
    winter_start = 1609459200  # January 1st
    summer_start = 1625097600  # July 1st
    
    winter_price_history = [
        {"timestamp": winter_start + (i * ONE_DAY_SECONDS), "price": price}
        for i, price in enumerate(SAMPLE_PRICE_PATTERN)
    ]
    
    summer_price_history = [
        {"timestamp": summer_start + (i * ONE_DAY_SECONDS), "price": price}
        for i, price in enumerate(SAMPLE_PRICE_PATTERN)
    ]
    
    # Setup mock for Schumann data with seasonal variations
    winter_schumann = [
        {"timestamp": winter_start + (i * ONE_DAY_SECONDS), 
         "frequency": SCHUMANN_BASE_FREQUENCY - 0.15, 
         "amplitude": 0.08 + (0.03 * np.sin(i/4))}
        for i in range(len(SAMPLE_PRICE_PATTERN))
    ]
    
    summer_schumann = [
        {"timestamp": summer_start + (i * ONE_DAY_SECONDS), 
         "frequency": SCHUMANN_BASE_FREQUENCY + 0.25, 
         "amplitude": 0.12 + (0.05 * np.sin(i/4))}
        for i in range(len(SAMPLE_PRICE_PATTERN))
    ]
    
    # Mock the get_schumann_data to return seasonal data
    mock_cosmic_oracle.get_schumann_data = AsyncMock(side_effect=[winter_schumann, summer_schumann])
    
    # Generate predictions for winter and summer
    mock_cosmic_oracle.predict_price_movement = MagicMock(wraps=mock_cosmic_oracle.predict_price_movement)
    
    # Setup SchmannResonanceDetector with visible seasonal variations
    original_analyzer = mock_cosmic_oracle.schumann_detector.analyze_correlation
    mock_cosmic_oracle.schumann_detector.analyze_correlation = MagicMock(side_effect=[
        {"correlation_coefficient": 0.65, "resonance_shift": -0.15, "market_impact_score": 0.55},  # Winter
        {"correlation_coefficient": 0.85, "resonance_shift": 0.25, "market_impact_score": 0.75}   # Summer
    ])
    
    # Generate predictions
    winter_prediction = mock_cosmic_oracle.predict_price_movement(winter_price_history)
    summer_prediction = mock_cosmic_oracle.predict_price_movement(summer_price_history)
    
    # Restore original method
    mock_cosmic_oracle.schumann_detector.analyze_correlation = original_analyzer
    
    # Supporting patterns should potentially differ due to seasonal factors
    # but fundamental patterns should be consistent
    assert set(winter_prediction["supporting_patterns"]) != set(summer_prediction["supporting_patterns"])
    
    # However, the fundamental direction should be consistent
    winter_direction = winter_prediction["predicted_prices"][0] > winter_prediction["current_price"]
    summer_direction = summer_prediction["predicted_prices"][0] > summer_prediction["current_price"]
    assert winter_direction == summer_direction

@pytest.mark.asyncio
async def test_cosmic_alignment_cycle_consistency(mock_cosmic_oracle, base_price_history):
    """Test that cosmic alignment scores follow natural cycles across time."""
    # Create a year of timestamps to test alignment over time
    timestamps = [BASE_TIMESTAMP + (i * 14 * ONE_DAY_SECONDS) for i in range(26)]  # ~364 days
    
    # Create price histories for each timestamp, keeping the pattern identical
    yearly_histories = []
    for base_ts in timestamps:
        history = [
            {"timestamp": base_ts + (i * ONE_DAY_SECONDS), "price": price}
            for i, price in enumerate(SAMPLE_PRICE_PATTERN)
        ]
        yearly_histories.append(history)
    
    # Generate predictions for each time period
    alignment_scores = []
    
    for history in yearly_histories:
        # Generate a prediction
        prediction = mock_cosmic_oracle.predict_price_movement(history)
        alignment_scores.append(prediction["cosmic_alignment_score"])
    
    # Analysis of cycle patterns in alignment scores
    # Convert to numpy array for easier analysis
    scores_array = np.array(alignment_scores)
    
    # Calculate autocorrelation to detect cycles
    autocorr = np.correlate(scores_array - np.mean(scores_array), 
                           scores_array - np.mean(scores_array), 
                           mode='full')
    autocorr = autocorr[len(autocorr)//2:]
    autocorr = autocorr / autocorr[0]
    
    # Detect peaks in autocorrelation
    peaks = []
    for i in range(1, len(autocorr)-1):
        if autocorr[i] > autocorr[i-1] and autocorr[i] > autocorr[i+1] and autocorr[i] > 0.5:
            peaks.append(i)
    
    if len(peaks) >= 2:
        # Calculate average cycle length in terms of our 14-day periods
        cycle_length = np.mean(np.diff(peaks))
        
        # Expected cycles: quarterly (6-7 periods) or seasonal (8-9 periods) or lunar (~2 periods)
        expected_cycles = [2, 6.5, 8.5, 26]  # lunar, quarterly, seasonal, annual in 14-day periods
        
        # Check if detected cycle is close to any expected cycle
        is_natural_cycle = any(abs(cycle_length - expected) < 1.0 for expected in expected_cycles)
        assert is_natural_cycle, f"Cycle length {cycle_length} periods is not close to natural cycles"
    else:
        # If we can't detect multiple peaks, the variation should at least show some pattern
        # rather than pure randomness
        trend_diff = np.diff(scores_array)
        sign_changes = np.sum(np.diff(np.signbit(trend_diff)))
        
        # In 26 periods, we should see 4-8 sign changes for natural cycles, not constant or random
        assert 4 <= sign_changes <= 8, f"Found {sign_changes} trend reversals, expected 4-8 for natural cycles"

@pytest.mark.asyncio
async def test_full_oracle_time_loop_invariance(mock_cosmic_oracle):
    """Test that the complete oracle maintains appropriate invariance across time loops."""
    # Setup time loop test - same price pattern at different points in time
    time_points = [
        BASE_TIMESTAMP,                    # Jan 1, 2021
        BASE_TIMESTAMP + (180 * ONE_DAY_SECONDS),  # ~6 months later
        BASE_TIMESTAMP + (365 * ONE_DAY_SECONDS)   # ~1 year later
    ]
    
    histories = []
    for start_time in time_points:
        history = [
            {"timestamp": start_time + (i * ONE_DAY_SECONDS), "price": price}
            for i, price in enumerate(SAMPLE_PRICE_PATTERN)
        ]
        histories.append(history)
    
    # Generate predictions for each time point
    predictions = []
    for history in histories:
        prediction = mock_cosmic_oracle.predict_price_movement(history)
        predictions.append(prediction)
    
    # Verify key invariants
    for i in range(1, len(predictions)):
        # Current price should be the same since it's based on the last price in our pattern
        assert predictions[0]["current_price"] == predictions[i]["current_price"]
        
        # The absolute predicted prices should be similar (not necessarily identical due to
        # potential seasonal adjustments)
        first_day_price_diff = abs(predictions[0]["predicted_prices"][0] - predictions[i]["predicted_prices"][0])
        first_day_price_pct_diff = first_day_price_diff / predictions[0]["current_price"]
        assert first_day_price_pct_diff < 0.05, f"Price prediction varies by {first_day_price_pct_diff:.2%} across time loops"
        
        # The confidence scores should be reasonably similar
        confidence_diff = abs(predictions[0]["confidence_scores"][0] - predictions[i]["confidence_scores"][0])
        assert confidence_diff < 0.1, f"Confidence varies by {confidence_diff:.2f} across time loops"
        
        # Direction should be consistent
        first_direction = predictions[0]["predicted_prices"][0] > predictions[0]["current_price"]
        current_direction = predictions[i]["predicted_prices"][0] > predictions[i]["current_price"]
        assert first_direction == current_direction, "Price direction changed across time loops"

if __name__ == "__main__":
    pytest.main(["-xvs", __file__]) 