import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock

from omega_blockchain import (
    OmegaBlockchainStream,
    DivineTransactionAnalyzer,
    NetworkHealthOracle,
    BlockData,
    TransactionData,
    NetworkMetrics
)

@pytest.fixture
def mock_bitcoin_core():
    """Mock Bitcoin Core RPC connection."""
    with patch('omega_blockchain.BitcoinCoreRPC') as mock:
        mock_instance = AsyncMock()
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def blockchain_stream(mock_bitcoin_core):
    """Create a blockchain stream instance with mocked dependencies."""
    return OmegaBlockchainStream(node_connection=mock_bitcoin_core)

@pytest.fixture
def transaction_analyzer():
    """Create a transaction analyzer instance."""
    return DivineTransactionAnalyzer()

@pytest.fixture
def network_health_oracle():
    """Create a network health oracle instance."""
    return NetworkHealthOracle()

class TestOmegaBlockchainStream:
    """Test suite for the OmegaBlockchainStream class."""
    
    @pytest.mark.asyncio
    async def test_connect_to_chain(self, blockchain_stream, mock_bitcoin_core):
        """Test successful connection to Bitcoin Core."""
        await blockchain_stream.connect_to_chain()
        mock_bitcoin_core.connect.assert_called_once()
        
    @pytest.mark.asyncio
    async def test_stream_blocks(self, blockchain_stream, mock_bitcoin_core):
        """Test block streaming functionality."""
        # Mock block data
        mock_block = {
            'hash': '000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f',
            'height': 0,
            'timestamp': 1231006505,
            'tx': ['tx1', 'tx2']
        }
        mock_bitcoin_core.get_block.return_value = mock_block
        
        # Test block streaming
        block = await blockchain_stream.stream_blocks()
        assert isinstance(block, BlockData)
        assert block.hash == mock_block['hash']
        assert block.height == mock_block['height']
        
    @pytest.mark.asyncio
    async def test_error_handling(self, blockchain_stream, mock_bitcoin_core):
        """Test error handling during blockchain operations."""
        mock_bitcoin_core.connect.side_effect = Exception("Connection failed")
        
        with pytest.raises(Exception) as exc_info:
            await blockchain_stream.connect_to_chain()
        assert str(exc_info.value) == "Connection failed"

class TestDivineTransactionAnalyzer:
    """Test suite for the DivineTransactionAnalyzer class."""
    
    @pytest.fixture
    def mock_transactions(self):
        """Create mock transactions for testing."""
        now = datetime.now()
        return [
            TransactionData(
                txid='tx1',
                value=100000000,  # 1 BTC
                timestamp=now,
                inputs=[{'address': 'addr1'}, {'address': 'addr2'}],
                outputs=[{'address': 'addr3'}]
            ),
            TransactionData(
                txid='tx2',
                value=10000000000,  # 100 BTC (whale)
                timestamp=now + timedelta(minutes=30),
                inputs=[{'address': 'addr4'}, {'address': 'addr5'}],
                outputs=[{'address': 'addr6'}, {'address': 'addr7'}]
            ),
            TransactionData(
                txid='tx3',
                value=10500000000,  # 105 BTC (whale)
                timestamp=now + timedelta(minutes=45),
                inputs=[{'address': 'addr8'}, {'address': 'addr9'}],
                outputs=[{'address': 'addr10'}]
            )
        ]
    
    def test_analyze_patterns(self, transaction_analyzer, mock_transactions):
        """Test transaction pattern analysis."""
        patterns = transaction_analyzer.analyze_patterns(mock_transactions)
        
        # Test basic structure
        assert isinstance(patterns, dict)
        assert all(key in patterns for key in [
            'whale_movement',
            'transaction_flow',
            'clusters',
            'cyclic_patterns',
            'temporal_anomalies',
            'fibonacci_clusters'
        ])
        
        # Test whale movements
        assert len(patterns['whale_movement']) == 2
        assert patterns['whale_movement'][0]['transaction'].txid == 'tx2'
        assert patterns['whale_movement'][1]['transaction'].txid == 'tx3'
        
        # Test transaction flow
        assert len(patterns['transaction_flow']) == 3
        
    def test_group_by_time_window(self, transaction_analyzer, mock_transactions):
        """Test transaction grouping by time window."""
        windows = transaction_analyzer._group_by_time_window(mock_transactions)
        assert isinstance(windows, list)
        assert len(windows) == 1  # All transactions within 24h window
        assert len(windows[0]) == 3
        
    def test_detect_whale_movements(self, transaction_analyzer, mock_transactions):
        """Test whale movement detection."""
        whale_movements = transaction_analyzer._detect_whale_movements(mock_transactions)
        assert len(whale_movements) == 2
        
        # Test whale movement analysis
        movement = whale_movements[0]
        assert movement['transaction'].txid == 'tx2'
        assert movement['type'] == 'distribution'
        assert movement['concentration_ratio'] == 1.0
        
        movement = whale_movements[1]
        assert movement['transaction'].txid == 'tx3'
        assert movement['type'] == 'accumulation'
        assert movement['concentration_ratio'] == 0.5
        
    def test_detect_clusters(self, transaction_analyzer, mock_transactions):
        """Test transaction cluster detection."""
        clusters = transaction_analyzer._detect_clusters(mock_transactions)
        assert isinstance(clusters, list)
        
        # Test cluster with whale transactions
        whale_cluster = next((c for c in clusters if len(c['transactions']) >= 2), None)
        if whale_cluster:
            assert whale_cluster['total_value'] > transaction_analyzer.whale_threshold
            
    def test_detect_cyclic_patterns(self, transaction_analyzer, mock_transactions):
        """Test cyclic pattern detection."""
        cycles = transaction_analyzer._detect_cyclic_patterns(mock_transactions)
        assert isinstance(cycles, list)
        
        # Test value range grouping
        if cycles:
            cycle = cycles[0]
            assert 'value_range' in cycle
            assert 'period' in cycle
            assert 'strength' in cycle
            
    def test_detect_temporal_anomalies(self, transaction_analyzer, mock_transactions):
        """Test temporal anomaly detection."""
        anomalies = transaction_analyzer._detect_temporal_anomalies(mock_transactions)
        assert isinstance(anomalies, list)
        
        # Test anomaly structure if any found
        if anomalies:
            anomaly = anomalies[0]
            assert 'transaction' in anomaly
            assert 'time_difference' in anomaly
            assert 'expected_difference' in anomaly
            assert 'deviation' in anomaly
            
    def test_detect_fibonacci_clusters(self, transaction_analyzer, mock_transactions):
        """Test Fibonacci cluster detection."""
        clusters = transaction_analyzer._detect_fibonacci_clusters(mock_transactions)
        assert isinstance(clusters, list)
        
        # Test cluster structure if any found
        if clusters:
            cluster = clusters[0]
            assert 'ratio' in cluster
            assert 'base_value' in cluster
            assert 'target_value' in cluster
            assert 'transactions' in cluster
            assert 'strength' in cluster
            
    def test_track_whales(self, transaction_analyzer, mock_transactions):
        """Test enhanced whale tracking functionality."""
        whale_data = transaction_analyzer.track_whales(mock_transactions)
        assert len(whale_data) == 2
        
        # Test first whale transaction
        whale = whale_data[0]
        assert whale['transaction'].txid == 'tx2'
        assert whale['value_btc'] == 100.0
        assert whale['input_concentration'] == 2
        assert whale['output_distribution'] == 2
        assert not whale['is_consolidation']
        assert not whale['is_distribution']
        
        # Test second whale transaction
        whale = whale_data[1]
        assert whale['transaction'].txid == 'tx3'
        assert whale['value_btc'] == 105.0
        assert whale['input_concentration'] == 2
        assert whale['output_distribution'] == 1
        assert whale['is_consolidation']
        assert not whale['is_distribution']

class TestNetworkHealthOracle:
    """Test suite for the NetworkHealthOracle class."""
    
    @pytest.fixture
    def mock_bitcoin_core(self):
        """Create a mock Bitcoin Core RPC connection."""
        with patch('omega_blockchain.BitcoinCoreRPC') as mock:
            mock_instance = AsyncMock()
            mock.return_value = mock_instance
            yield mock_instance
            
    @pytest.fixture
    def network_oracle(self, mock_bitcoin_core):
        """Create a network health oracle instance with mocked dependencies."""
        oracle = NetworkHealthOracle(node_connection=mock_bitcoin_core)
        return oracle
    
    @pytest.mark.asyncio
    async def test_check_network_health(self, network_oracle, mock_bitcoin_core):
        """Test comprehensive network health checking."""
        # Mock network data
        mock_bitcoin_core._make_request.side_effect = [
            {'chain': 'main', 'blocks': 800000, 'headers': 800000, 'difficulty': 50000000000000},  # getblockchaininfo
            400000000000000,  # getnetworkhashps (returns number directly)
            {'size': 15000, 'bytes': 3000000},  # getmempoolinfo
            {'paytxfee': 0.00001000}  # getwalletinfo
        ]
        
        metrics = await network_oracle.check_network_health()
        assert isinstance(metrics, NetworkMetrics)
        
        # Verify network metrics
        assert metrics.hash_rate > 0
        assert metrics.difficulty > 0
        assert metrics.fee_rate > 0
        assert metrics.mempool_size > 0
        
        # Verify specific metric ranges
        assert 100_000_000_000_000 <= metrics.hash_rate <= 1_000_000_000_000_000  # 100-1000 TH/s
        assert metrics.fee_rate >= 1  # Minimum 1 sat/vB
        assert 0 <= metrics.mempool_size <= 10_000_000  # 0-10MB mempool size
        
    @pytest.mark.asyncio
    async def test_predict_congestion(self, network_oracle, mock_bitcoin_core):
        """Test network congestion prediction with historical data."""
        # Mock historical mempool data
        mock_bitcoin_core._make_request.side_effect = [
            {'size': 5000, 'bytes': 1000000},  # t-6h
            {'size': 8000, 'bytes': 1600000},  # t-3h
            {'size': 15000, 'bytes': 3000000},  # current
        ]
        
        prediction = await network_oracle.predict_congestion()
        assert isinstance(prediction, dict)
        
        # Verify prediction structure
        assert 'congestion_level' in prediction
        assert 'estimated_fee_rate' in prediction
        assert 'confidence' in prediction
        assert 'trend' in prediction
        assert 'next_block_eta' in prediction
        
        # Verify prediction values
        assert prediction['congestion_level'] in ['low', 'medium', 'high']
        assert isinstance(prediction['estimated_fee_rate'], (int, float))
        assert 0 <= prediction['confidence'] <= 1
        assert prediction['trend'] in ['increasing', 'decreasing', 'stable']
        assert isinstance(prediction['next_block_eta'], (int, float))
        
    @pytest.mark.asyncio
    async def test_network_health_error_handling(self, network_oracle, mock_bitcoin_core):
        """Test error handling in network health monitoring."""
        # Simulate RPC errors
        mock_bitcoin_core._make_request.side_effect = Exception("RPC Error")
        
        with pytest.raises(Exception) as exc_info:
            await network_oracle.check_network_health()
        assert "Failed to retrieve network metrics" in str(exc_info.value)
        
    @pytest.mark.asyncio
    async def test_mempool_analysis(self, network_oracle, mock_bitcoin_core):
        """Test detailed mempool analysis."""
        # Mock mempool transaction data
        mock_bitcoin_core._make_request.return_value = {
            'size': 15000,
            'bytes': 3000000,
            'usage': 2000000,
            'maxmempool': 300000000,
            'mempoolminfee': 0.00001000,
            'minrelaytxfee': 0.00001000
        }
        
        analysis = await network_oracle.analyze_mempool()
        assert isinstance(analysis, dict)
        
        # Verify analysis metrics
        assert 'utilization' in analysis
        assert 'fee_histogram' in analysis
        assert 'size_histogram' in analysis
        assert 'transaction_types' in analysis
        
        # Verify metric ranges
        assert 0 <= analysis['utilization'] <= 100  # percentage
        assert isinstance(analysis['fee_histogram'], list)
        assert isinstance(analysis['size_histogram'], list)
        assert isinstance(analysis['transaction_types'], dict)
        
    @pytest.mark.asyncio
    async def test_network_synchronization(self, network_oracle, mock_bitcoin_core):
        """Test network synchronization status checking."""
        # Mock blockchain info
        mock_bitcoin_core._make_request.return_value = {
            'chain': 'main',
            'blocks': 800000,
            'headers': 800000,
            'verificationprogress': 0.9999,
            'initialblockdownload': False
        }
        
        sync_status = await network_oracle.check_synchronization()
        assert isinstance(sync_status, dict)
        
        # Verify sync status
        assert 'is_synced' in sync_status
        assert 'progress' in sync_status
        assert 'blocks_behind' in sync_status
        assert 'estimated_time_remaining' in sync_status
        
        # Verify status values
        assert isinstance(sync_status['is_synced'], bool)
        assert 0 <= sync_status['progress'] <= 1
        assert sync_status['blocks_behind'] >= 0
        assert sync_status['estimated_time_remaining'] >= 0

    @pytest.mark.asyncio
    async def test_ddos_protection_rate_limiting(self, network_oracle, mock_bitcoin_core):
        """Test rate limiting under high request frequency."""
        # Simulate rapid RPC requests
        mock_bitcoin_core._make_request.side_effect = [
            {'chain': 'main', 'blocks': 800000, 'headers': 800000, 'difficulty': 50000000000000},
            400000000000000,
            {'size': 15000, 'bytes': 3000000},
            {'paytxfee': 0.00001000}
        ] * 100  # 100 rapid requests
        
        # Make multiple rapid requests
        tasks = []
        for _ in range(10):
            tasks.append(network_oracle.check_network_health())
            
        # Execute requests concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Verify rate limiting behavior
        assert len([r for r in results if isinstance(r, Exception)]) > 0
        assert mock_bitcoin_core._make_request.call_count <= 50  # Should be rate limited
        
    @pytest.mark.asyncio
    async def test_ddos_connection_resilience(self, network_oracle, mock_bitcoin_core):
        """Test connection resilience under connection failures."""
        # Simulate intermittent connection failures
        mock_bitcoin_core._make_request.side_effect = [
            Exception("Connection timeout"),
            Exception("Connection refused"),
            {'chain': 'main', 'blocks': 800000, 'headers': 800000, 'difficulty': 50000000000000},
            400000000000000,
            {'size': 15000, 'bytes': 3000000},
            {'paytxfee': 0.00001000}
        ]
        
        # Attempt to get network health
        with pytest.raises(Exception) as exc_info:
            await network_oracle.check_network_health()
        assert "Failed to retrieve network metrics" in str(exc_info.value)
        
        # Verify connection retry behavior
        assert mock_bitcoin_core._make_request.call_count >= 2
        
    @pytest.mark.asyncio
    async def test_ddos_memory_management(self, network_oracle, mock_bitcoin_core):
        """Test memory management under sustained load."""
        # Disable rate limiting for this test
        network_oracle.disable_rate_limit()
        
        # Generate large amounts of historical data
        mock_bitcoin_core._make_request.side_effect = [
            {'chain': 'main', 'blocks': 800000, 'headers': 800000, 'difficulty': 50000000000000},
            400000000000000,
            {'size': 15000, 'bytes': 3000000},
            {'paytxfee': 0.00001000}
        ] * 1000  # 1000 requests
        
        # Simulate 24 hours of data collection
        for _ in range(1000):
            await network_oracle.check_network_health()
            
        # Verify historical data cleanup
        cutoff = datetime.now() - timedelta(hours=24)
        assert all(m.timestamp > int(cutoff.timestamp()) for m in network_oracle.historical_metrics)
        assert len(network_oracle.historical_metrics) <= 144  # Max 144 entries (6 per hour)
        
        # Re-enable rate limiting
        network_oracle.enable_rate_limit()
        
    @pytest.mark.asyncio
    async def test_ddos_resource_exhaustion(self, network_oracle, mock_bitcoin_core):
        """Test behavior under resource exhaustion conditions."""
        # Simulate resource exhaustion
        mock_bitcoin_core._make_request.side_effect = [
            {'chain': 'main', 'blocks': 800000, 'headers': 800000, 'difficulty': 50000000000000},
            400000000000000,
            {'size': 15000, 'bytes': 3000000},
            {'paytxfee': 0.00001000}
        ] * 10000  # 10000 requests
        
        # Attempt to exhaust resources
        tasks = []
        for _ in range(100):
            tasks.append(network_oracle.check_network_health())
            
        # Execute requests concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Verify resource protection
        assert len([r for r in results if isinstance(r, Exception)]) > 0
        assert mock_bitcoin_core._make_request.call_count <= 1000  # Should be limited
        
    @pytest.mark.asyncio
    async def test_ddos_system_stability(self, network_oracle, mock_bitcoin_core):
        """Test system stability under sustained attack conditions."""
        # Simulate sustained attack conditions
        mock_bitcoin_core._make_request.side_effect = [
            Exception("Connection timeout"),
            Exception("Connection refused"),
            Exception("Rate limit exceeded"),
            {'chain': 'main', 'blocks': 800000, 'headers': 800000, 'difficulty': 50000000000000},
            400000000000000,
            {'size': 15000, 'bytes': 3000000},
            {'paytxfee': 0.00001000}
        ] * 100
        
        # Attempt multiple operations under attack conditions
        tasks = []
        for _ in range(10):
            tasks.extend([
                network_oracle.check_network_health(),
                network_oracle.predict_congestion(),
                network_oracle.analyze_mempool(),
                network_oracle.check_synchronization()
            ])
            
        # Execute operations concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Verify system stability
        assert len([r for r in results if isinstance(r, Exception)]) > 0
        assert mock_bitcoin_core._make_request.call_count <= 50  # Should be limited
        assert len(network_oracle.historical_metrics) <= 144  # Should maintain data limits

class TestDataModels:
    """Test suite for data models."""
    
    def test_block_data(self):
        """Test BlockData model."""
        block = BlockData(
            hash='000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f',
            height=0,
            timestamp=1231006505,
            transactions=['tx1', 'tx2']
        )
        assert block.hash == '000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f'
        assert block.height == 0
        assert isinstance(block.timestamp, int)
        assert len(block.transactions) == 2
        
    def test_transaction_data(self):
        """Test TransactionData model."""
        tx = TransactionData(
            txid='tx1',
            value=100000000,
            timestamp=datetime.now(),
            inputs=[],
            outputs=[]
        )
        assert tx.txid == 'tx1'
        assert tx.value == 100000000
        assert isinstance(tx.timestamp, datetime)
        assert isinstance(tx.inputs, list)
        assert isinstance(tx.outputs, list)
        
    def test_network_metrics(self):
        """Test NetworkMetrics model."""
        metrics = NetworkMetrics(
            hash_rate=100000000000,  # 100 TH/s
            difficulty=1000000000000,
            fee_rate=10,  # 10 sat/vB
            mempool_size=1000000
        )
        assert metrics.hash_rate == 100000000000
        assert metrics.difficulty == 1000000000000
        assert metrics.fee_rate == 10
        assert metrics.mempool_size == 1000000 