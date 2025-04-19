
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
from datetime import datetime, timedelta
from omega_blockchain.analyzers.transaction import DivineTransactionAnalyzer
from omega_blockchain.models.transaction import TransactionData

@pytest.fixture
def transaction_analyzer():
    return DivineTransactionAnalyzer()

@pytest.fixture
def sample_transactions():
    """Create sample transactions for testing."""
    base_time = datetime.now()
    return [
        TransactionData(
            txid="tx1",
            value=15000000000,  # 150 BTC
            timestamp=base_time,
            inputs=[{"address": "addr1", "value": 10000000000}],
            outputs=[{"address": "addr2", "value": 5000000000}]
        ),
        TransactionData(
            txid="tx2",
            value=20000000000,  # 200 BTC
            timestamp=base_time + timedelta(minutes=5),
            inputs=[{"address": "addr2", "value": 20000000000}],
            outputs=[{"address": "addr3", "value": 20000000000}]
        ),
        TransactionData(
            txid="tx3",
            value=5000000000,  # 50 BTC
            timestamp=base_time + timedelta(minutes=10),
            inputs=[{"address": "addr3", "value": 5000000000}],
            outputs=[{"address": "addr4", "value": 5000000000}]
        )
    ]

def test_analyze_patterns(transaction_analyzer, sample_transactions):
    """Test pattern analysis on sample transactions."""
    patterns = transaction_analyzer.analyze_patterns(sample_transactions)
    
    assert isinstance(patterns, dict)
    assert "whale_movement" in patterns
    assert "transaction_flow" in patterns
    assert "clusters" in patterns
    assert "cyclic_patterns" in patterns
    assert "temporal_anomalies" in patterns
    assert "fibonacci_clusters" in patterns

def test_detect_whale_movements(transaction_analyzer, sample_transactions):
    """Test whale movement detection."""
    whale_movements = transaction_analyzer._detect_whale_movements(sample_transactions)
    
    assert len(whale_movements) > 0
    for movement in whale_movements:
        assert "transaction" in movement
        assert "type" in movement
        assert "concentration_ratio" in movement
        assert "timestamp" in movement

def test_detect_clusters(transaction_analyzer, sample_transactions):
    """Test transaction cluster detection."""
    clusters = transaction_analyzer._detect_clusters(sample_transactions)
    
    assert isinstance(clusters, list)
    for cluster in clusters:
        assert "transactions" in cluster
        assert "total_value" in cluster
        assert "start_time" in cluster
        assert "end_time" in cluster

def test_detect_cyclic_patterns(transaction_analyzer, sample_transactions):
    """Test cyclic pattern detection."""
    cycles = transaction_analyzer._detect_cyclic_patterns(sample_transactions)
    
    assert isinstance(cycles, list)
    for cycle in cycles:
        assert "value_range" in cycle
        assert "transactions" in cycle
        assert "period" in cycle
        assert "strength" in cycle

def test_detect_temporal_anomalies(transaction_analyzer, sample_transactions):
    """Test temporal anomaly detection."""
    anomalies = transaction_analyzer._detect_temporal_anomalies(sample_transactions)
    
    assert isinstance(anomalies, list)
    for anomaly in anomalies:
        assert "transaction" in anomaly
        assert "time_difference" in anomaly
        assert "expected_difference" in anomaly
        assert "deviation" in anomaly

def test_detect_fibonacci_clusters(transaction_analyzer, sample_transactions):
    """Test Fibonacci-based cluster detection."""
    clusters = transaction_analyzer._detect_fibonacci_clusters(sample_transactions)
    
    assert isinstance(clusters, list)
    for cluster in clusters:
        assert "ratio" in cluster
        assert "base_value" in cluster
        assert "target_value" in cluster
        assert "transactions" in cluster
        assert "strength" in cluster

def test_track_whales(transaction_analyzer, sample_transactions):
    """Test whale tracking functionality."""
    whale_data = transaction_analyzer.track_whales(sample_transactions)
    
    assert isinstance(whale_data, list)
    for whale in whale_data:
        assert "transaction" in whale
        assert "value_btc" in whale
        assert "input_concentration" in whale
        assert "output_distribution" in whale
        assert "is_consolidation" in whale
        assert "is_distribution" in whale
        assert "timestamp" in whale

def test_group_by_time_window(transaction_analyzer, sample_transactions):
    """Test time window grouping functionality."""
    windows = transaction_analyzer._group_by_time_window(sample_transactions)
    
    assert isinstance(windows, list)
    assert len(windows) > 0
    for window in windows:
        assert isinstance(window, list)
        assert len(window) > 0
        assert all(isinstance(tx, TransactionData) for tx in window)

def test_is_related_transaction(transaction_analyzer, sample_transactions):
    """Test transaction relationship detection."""
    # Test related transactions
    assert transaction_analyzer._is_related_transaction(
        sample_transactions[0],
        sample_transactions[1]
    )
    
    # Test unrelated transactions
    assert not transaction_analyzer._is_related_transaction(
        sample_transactions[0],
        sample_transactions[2]
    ) 