
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
Tests for the quantum testing module of the OMEGA GARVEY WISDOM PORTAL.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from omega_ai.garvey_portal.quantum_testing import QuantumMarketAnalyzer

@pytest.fixture
def analyzer():
    """Create a QuantumMarketAnalyzer instance for testing"""
    return QuantumMarketAnalyzer()

@pytest.fixture
def sample_price_data():
    """Create sample price data for testing"""
    dates = pd.date_range(start='2024-01-01', end='2024-01-02', freq='H')
    return pd.DataFrame({
        'timestamp': dates,
        'close': np.random.uniform(40000, 50000, len(dates)),
        'volume': np.random.uniform(100, 1000, len(dates))
    })

@pytest.fixture
def sample_schumann_data():
    """Create sample Schumann resonance data for testing"""
    dates = pd.date_range(start='2024-01-01', end='2024-01-02', freq='H')
    return pd.DataFrame({
        'timestamp': dates,
        'frequency': np.random.normal(7.83, 0.1, len(dates)),
        'amplitude': np.random.uniform(0.5, 1.5, len(dates))
    })

def test_load_schumann_data(analyzer):
    """Test loading Schumann resonance data"""
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 2)
    
    data = analyzer.load_schumann_data(start_date, end_date)
    
    assert isinstance(data, pd.DataFrame)
    assert 'timestamp' in data.columns
    assert 'frequency' in data.columns
    assert 'amplitude' in data.columns
    assert len(data) == 25  # 24 hours + 1 initial hour

def test_calculate_quantum_state(analyzer, sample_price_data, sample_schumann_data):
    """Test quantum state calculation"""
    states = analyzer.calculate_quantum_state(sample_price_data, sample_schumann_data)
    
    assert isinstance(states, dict)
    assert all(state in states for state in ["bullish", "bearish", "neutral", "superposition"])
    assert all(0 <= prob <= 1 for prob in states.values())
    assert abs(sum(states.values()) - 1.0) < 1e-10  # Probabilities should sum to 1

def test_analyze_emotional_entropy(analyzer, sample_price_data):
    """Test emotional entropy analysis"""
    entropy = analyzer.analyze_emotional_entropy(sample_price_data)
    
    assert isinstance(entropy, float)
    assert entropy >= 0  # Entropy should be non-negative

def test_track_quantum_memory(analyzer):
    """Test quantum memory tracking"""
    pattern = {
        'type': 'test_pattern',
        'price_series': [1, 2, 3],
        'volume_series': [100, 200, 300]
    }
    timestamp = datetime.now()
    
    analyzer.track_quantum_memory(pattern, timestamp)
    
    pattern_key = f"{pattern['type']}_{timestamp.strftime('%Y%m%d')}"
    assert pattern_key in analyzer.quantum_memory
    assert analyzer.quantum_memory[pattern_key]['count'] == 1
    assert analyzer.quantum_memory[pattern_key]['confidence'] == 0.1

def test_analyze_pattern_entanglement(analyzer):
    """Test pattern entanglement analysis"""
    pattern1 = {
        'timestamp': datetime.now(),
        'price_series': [1, 2, 3],
        'volume_series': [100, 200, 300]
    }
    pattern2 = {
        'timestamp': datetime.now() + timedelta(hours=1),
        'price_series': [2, 3, 4],
        'volume_series': [200, 300, 400]
    }
    
    entanglement = analyzer.analyze_pattern_entanglement(pattern1, pattern2)
    
    assert isinstance(entanglement, float)
    assert 0 <= entanglement <= 1  # Entanglement should be between 0 and 1

def test_save_and_load_quantum_analysis(analyzer, tmp_path):
    """Test saving and loading quantum analysis results"""
    analysis_data = {
        'timestamp': datetime.now(),
        'quantum_states': {'bullish': 0.7, 'bearish': 0.3},
        'entropy': 0.5
    }
    
    filepath = tmp_path / "quantum_analysis.json"
    
    # Save analysis
    analyzer.save_quantum_analysis(analysis_data, filepath)
    assert filepath.exists()
    
    # Load analysis
    loaded_data = analyzer.load_quantum_analysis(filepath)
    assert loaded_data['quantum_states'] == analysis_data['quantum_states']
    assert loaded_data['entropy'] == analysis_data['entropy'] 