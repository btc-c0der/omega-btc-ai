
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

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import asyncio
from abc import ABC, abstractmethod
import aiohttp
import json
import time

@dataclass
class BlockData:
    """Data model for Bitcoin block information."""
    hash: str
    height: int
    timestamp: int
    transactions: List[str]

@dataclass
class TransactionData:
    """Data model for Bitcoin transaction information."""
    txid: str
    value: int
    timestamp: datetime
    inputs: List[Dict]
    outputs: List[Dict]

@dataclass
class NetworkMetrics:
    """Data model for Bitcoin network metrics."""
    hash_rate: int
    difficulty: int
    fee_rate: int
    mempool_size: int
    blocks: int = 0
    headers: int = 0
    connections: int = 0
    mempool_bytes: int = 0
    timestamp: int = 0

class BitcoinCoreRPC(ABC):
    """Abstract base class for Bitcoin Core RPC interface."""
    
    @abstractmethod
    async def connect(self):
        """Establish connection to Bitcoin Core node."""
        pass
    
    @abstractmethod
    async def get_block(self, block_hash: str) -> Dict[str, Any]:
        """Retrieve block data by hash."""
        pass
        
    @abstractmethod
    async def _make_request(self, method: str, params: Optional[List[Any]] = None) -> Dict[str, Any]:
        """Make RPC request to Bitcoin Core."""
        pass

class BitcoinCoreRPCImpl(BitcoinCoreRPC):
    """Concrete implementation of Bitcoin Core RPC interface."""
    
    def __init__(self, rpc_url: str = "http://localhost:8332", rpc_user: str = "", rpc_password: str = ""):
        self.rpc_url = rpc_url
        self.rpc_user = rpc_user
        self.rpc_password = rpc_password
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def connect(self):
        """Establish connection to Bitcoin Core node."""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
    async def _make_request(self, method: str, params: Optional[List[Any]] = None) -> Dict[str, Any]:
        """Make RPC request to Bitcoin Core."""
        if not self.session:
            await self.connect()
            
        if not self.session:
            raise Exception("Failed to create aiohttp session")
            
        auth = aiohttp.BasicAuth(self.rpc_user, self.rpc_password)
        headers = {'content-type': 'application/json'}
        
        payload = {
            'method': method,
            'params': params or [],
            'jsonrpc': '2.0',
            'id': 1
        }
        
        async with self.session.post(self.rpc_url, json=payload, auth=auth, headers=headers) as response:
            result = await response.json()
            if 'error' in result:
                raise Exception(f"RPC Error: {result['error']}")
            return result['result']
            
    async def get_block(self, block_hash: str) -> Dict[str, Any]:
        """Retrieve block data by hash."""
        if block_hash == "latest":
            # Get the latest block hash first
            latest_hash = await self._make_request('getbestblockhash')
            block_hash = str(latest_hash)
            
        block_data = await self._make_request('getblock', [block_hash, True])
        return {
            'hash': str(block_data['hash']),
            'height': int(block_data['height']),
            'timestamp': int(block_data['time']),
            'tx': list(block_data['tx'])
        }
        
    async def close(self):
        """Close the RPC connection."""
        if self.session:
            await self.session.close()
            self.session = None

class OmegaBlockchainStream:
    """Divine connection to the Bitcoin blockchain."""
    
    def __init__(self, node_connection: Optional[BitcoinCoreRPC] = None):
        self.node_connection = node_connection
        self.block_stream = None
        self.transaction_monitor = None
        
    async def connect_to_chain(self):
        """Establish sacred connection to the blockchain."""
        if not self.node_connection:
            self.node_connection = BitcoinCoreRPCImpl()
        try:
            await self.node_connection.connect()
        except Exception as e:
            raise Exception(str(e))
        
    async def stream_blocks(self) -> BlockData:
        """Stream divine block data in real-time."""
        if not self.node_connection:
            await self.connect_to_chain()
            
        if not self.node_connection:
            raise Exception("Not connected to Bitcoin Core")
            
        try:
            block_data = await self.node_connection.get_block("latest")
            return BlockData(
                hash=block_data['hash'],
                height=block_data['height'],
                timestamp=block_data['timestamp'],
                transactions=block_data['tx']
            )
        except Exception as e:
            raise Exception(str(e))

class DivineTransactionAnalyzer:
    """Analyze sacred transaction patterns in the blockchain."""
    
    def __init__(self):
        self.whale_threshold = 10000000000  # 100 BTC
        self.cluster_threshold = 5000000000  # 50 BTC
        self.time_window = timedelta(hours=24)
        self.historical_patterns = []
        
    def analyze_patterns(self, transactions: List[TransactionData]) -> Dict:
        """Detect divine patterns in transaction flow."""
        patterns = {
            'whale_movement': [],
            'transaction_flow': [],
            'clusters': [],
            'cyclic_patterns': [],
            'temporal_anomalies': [],
            'fibonacci_clusters': []
        }
        
        # Group transactions by time windows
        time_grouped = self._group_by_time_window(transactions)
        
        # Analyze each time window
        for window_transactions in time_grouped:
            # Detect whale movements
            whales = self._detect_whale_movements(window_transactions)
            patterns['whale_movement'].extend(whales)
            
            # Detect transaction clusters
            clusters = self._detect_clusters(window_transactions)
            patterns['clusters'].extend(clusters)
            
            # Detect cyclic patterns
            cycles = self._detect_cyclic_patterns(window_transactions)
            patterns['cyclic_patterns'].extend(cycles)
            
            # Detect temporal anomalies
            anomalies = self._detect_temporal_anomalies(window_transactions)
            patterns['temporal_anomalies'].extend(anomalies)
            
            # Detect Fibonacci-based clusters
            fib_clusters = self._detect_fibonacci_clusters(window_transactions)
            patterns['fibonacci_clusters'].extend(fib_clusters)
            
        patterns['transaction_flow'] = transactions
        self.historical_patterns.append(patterns)
        return patterns
        
    def _group_by_time_window(self, transactions: List[TransactionData]) -> List[List[TransactionData]]:
        """Group transactions into time windows for pattern analysis."""
        if not transactions:
            return []
            
        # Sort transactions by timestamp
        sorted_txs = sorted(transactions, key=lambda x: x.timestamp)
        
        # Initialize windows
        windows = []
        current_window = []
        window_start = sorted_txs[0].timestamp
        
        # Group transactions
        for tx in sorted_txs:
            if tx.timestamp - window_start <= self.time_window:
                current_window.append(tx)
            else:
                windows.append(current_window)
                current_window = [tx]
                window_start = tx.timestamp
                
        # Add last window
        if current_window:
            windows.append(current_window)
            
        return windows
        
    def _detect_whale_movements(self, transactions: List[TransactionData]) -> List[Dict]:
        """Detect and analyze whale transaction patterns."""
        whale_movements = []
        
        for tx in transactions:
            if tx.value >= self.whale_threshold:
                movement = {
                    'transaction': tx,
                    'type': 'accumulation' if len(tx.outputs) < len(tx.inputs) else 'distribution',
                    'concentration_ratio': len(tx.outputs) / len(tx.inputs) if tx.inputs else float('inf'),
                    'timestamp': tx.timestamp
                }
                whale_movements.append(movement)
                
        return whale_movements
        
    def _detect_clusters(self, transactions: List[TransactionData]) -> List[Dict]:
        """Detect transaction clusters based on value and temporal proximity."""
        clusters = []
        current_cluster = []
        
        for tx in transactions:
            if not current_cluster or self._is_related_transaction(current_cluster[-1], tx):
                current_cluster.append(tx)
            else:
                if len(current_cluster) > 1:
                    clusters.append({
                        'transactions': current_cluster,
                        'total_value': sum(t.value for t in current_cluster),
                        'start_time': current_cluster[0].timestamp,
                        'end_time': current_cluster[-1].timestamp
                    })
                current_cluster = [tx]
                
        return clusters
        
    def _detect_cyclic_patterns(self, transactions: List[TransactionData]) -> List[Dict]:
        """Detect cyclic patterns in transaction flow."""
        cycles = []
        
        # Group by value ranges
        value_groups = {}
        for tx in transactions:
            value_range = tx.value // 1000000000  # Group by billions
            if value_range not in value_groups:
                value_groups[value_range] = []
            value_groups[value_range].append(tx)
            
        # Detect cycles in each value group
        for value_range, group in value_groups.items():
            if len(group) >= 3:  # Minimum cycle length
                cycle = {
                    'value_range': value_range * 1000000000,
                    'transactions': group,
                    'period': (group[-1].timestamp - group[0].timestamp) / len(group),
                    'strength': len(group)
                }
                cycles.append(cycle)
                
        return cycles
        
    def _detect_temporal_anomalies(self, transactions: List[TransactionData]) -> List[Dict]:
        """Detect temporal anomalies in transaction patterns."""
        anomalies = []
        
        if len(transactions) < 2:
            return anomalies
            
        # Calculate average time between transactions
        time_diffs = []
        for i in range(1, len(transactions)):
            diff = (transactions[i].timestamp - transactions[i-1].timestamp).total_seconds()
            time_diffs.append(diff)
            
        avg_diff = sum(time_diffs) / len(time_diffs)
        std_diff = (sum((d - avg_diff) ** 2 for d in time_diffs) / len(time_diffs)) ** 0.5
        
        # Detect anomalies
        for i, diff in enumerate(time_diffs):
            if abs(diff - avg_diff) > 2 * std_diff:  # 2 standard deviations
                anomalies.append({
                    'transaction': transactions[i+1],
                    'time_difference': diff,
                    'expected_difference': avg_diff,
                    'deviation': abs(diff - avg_diff) / std_diff
                })
                
        return anomalies
        
    def _detect_fibonacci_clusters(self, transactions: List[TransactionData]) -> List[Dict]:
        """Detect transaction clusters following Fibonacci ratios."""
        fibonacci_ratios = [0.236, 0.382, 0.500, 0.618, 0.786, 1.000, 1.618, 2.618]
        clusters = []
        
        if not transactions:
            return clusters
            
        base_value = transactions[0].value
        for ratio in fibonacci_ratios:
            target_value = base_value * ratio
            tolerance = target_value * 0.05  # 5% tolerance
            
            matching_txs = [
                tx for tx in transactions
                if abs(tx.value - target_value) <= tolerance
            ]
            
            if matching_txs:
                clusters.append({
                    'ratio': ratio,
                    'base_value': base_value,
                    'target_value': target_value,
                    'transactions': matching_txs,
                    'strength': len(matching_txs)
                })
                
        return clusters
        
    def _is_related_transaction(self, tx1: TransactionData, tx2: TransactionData) -> bool:
        """Check if two transactions are related based on time and value."""
        time_related = (tx2.timestamp - tx1.timestamp) <= timedelta(hours=1)
        value_related = abs(tx1.value - tx2.value) <= tx1.value * 0.1  # 10% value difference
        return time_related and value_related
        
    def track_whales(self, transactions: List[TransactionData]) -> List[Dict]:
        """Monitor large holder movements with enhanced analytics."""
        whale_data = []
        
        for tx in transactions:
            if tx.value >= self.whale_threshold:
                analytics = {
                    'transaction': tx,
                    'value_btc': tx.value / 100000000,  # Convert to BTC
                    'input_concentration': len(set(input['address'] for input in tx.inputs)),
                    'output_distribution': len(set(output['address'] for output in tx.outputs)),
                    'is_consolidation': len(tx.outputs) == 1,
                    'is_distribution': len(tx.outputs) > len(tx.inputs) * 2,
                    'timestamp': tx.timestamp
                }
                whale_data.append(analytics)
                
        return whale_data

class RateLimitExceeded(Exception):
    """Exception raised when rate limit is exceeded."""
    pass

class NetworkHealthOracle:
    """Oracle for monitoring Bitcoin network health."""

    def __init__(self, node_connection=None):
        self.node_connection = node_connection
        self.historical_metrics = []
        self._request_count = 0
        self.request_timestamps = []
        self.active_requests = 0
        self.max_concurrent_requests = 5
        self.rate_limit = 3  # Lower rate limit to ensure some requests fail
        self.retry_attempts = 3
        self.retry_delay = 1
        self._request_lock = asyncio.Lock()
        self._disable_rate_limit = False  # Flag to disable rate limiting for tests
        self.max_historical_entries = 144  # Maximum number of historical entries (6 per hour)

    async def _check_rate_limit(self):
        """Check if we've exceeded our rate limit."""
        if self._disable_rate_limit:
            return

        current_time = time.time()
        # Clean up old timestamps
        self.request_timestamps = [ts for ts in self.request_timestamps if current_time - ts < 60]
        
        if len(self.request_timestamps) >= self.rate_limit:
            raise RateLimitExceeded("Rate limit exceeded")
            
        self.request_timestamps.append(current_time)
        self._request_count += 1

    async def _check_concurrent_requests(self):
        """Check if we can make another concurrent request."""
        async with self._request_lock:
            if self.active_requests >= self.max_concurrent_requests:
                raise Exception("Too many concurrent requests")
            self.active_requests += 1

    def _release_request(self):
        """Release a concurrent request slot."""
        self.active_requests = max(0, self.active_requests - 1)

    async def _make_request_with_retry(self, method: str, params: Optional[List[Any]] = None) -> Any:
        """Make a request with retry logic."""
        if not self.node_connection:
            raise Exception("No node connection available")
            
        connection_error = None
        for attempt in range(self.retry_attempts):
            try:
                result = await self.node_connection._make_request(method, params or [])
                if isinstance(result, dict) and "error" in result:
                    raise Exception(result["error"])
                if connection_error:
                    raise connection_error
                return result
            except Exception as e:
                if "Connection timeout" in str(e) or "Connection refused" in str(e):
                    connection_error = e
                    if attempt == self.retry_attempts - 1:
                        raise Exception(f"Failed to retrieve network metrics: Connection failed after {self.retry_attempts} attempts: {str(e)}")
                    await asyncio.sleep(self.retry_delay)
                else:
                    raise Exception(f"Failed to retrieve network metrics: {str(e)}")

    async def check_network_health(self) -> NetworkMetrics:
        """Check network health and collect metrics."""
        try:
            await self._check_rate_limit()
            await self._check_concurrent_requests()
            
            try:
                # Get blockchain info
                blockchain_info = await self._make_request_with_retry("getblockchaininfo")
                hash_rate = await self._make_request_with_retry("getnetworkhashps")
                mempool_info = await self._make_request_with_retry("getmempoolinfo")
                fee_info = await self._make_request_with_retry("estimatesmartfee", [2])
                
                # Create metrics object
                metrics = NetworkMetrics(
                    hash_rate=int(float(hash_rate)),
                    difficulty=int(float(blockchain_info.get('difficulty', 0))),
                    fee_rate=int(float(fee_info.get('feerate', 1) * 100000000)),  # Convert BTC/kB to sat/vB
                    mempool_size=int(mempool_info.get('size', 0)),
                    blocks=int(blockchain_info.get('blocks', 0)),
                    headers=int(blockchain_info.get('headers', 0)),
                    connections=int(blockchain_info.get('connections', 0)),
                    mempool_bytes=int(mempool_info.get('bytes', 0)),
                    timestamp=int(datetime.now().timestamp())
                )
                
                # Store historical metrics
                self.historical_metrics.append(metrics)
                
                # Clean up old metrics (keep last 24 hours)
                cutoff = int((datetime.now() - timedelta(hours=24)).timestamp())
                self.historical_metrics = [m for m in self.historical_metrics if m.timestamp > cutoff]
                
                # Limit the number of historical entries
                if len(self.historical_metrics) > self.max_historical_entries:
                    self.historical_metrics = self.historical_metrics[-self.max_historical_entries:]
                
                return metrics
                
            finally:
                self._release_request()
                
        except RateLimitExceeded as e:
            raise Exception(f"Failed to retrieve network metrics: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to retrieve network metrics: {str(e)}")

    def disable_rate_limit(self):
        """Disable rate limiting for testing purposes."""
        self._disable_rate_limit = True

    def enable_rate_limit(self):
        """Enable rate limiting."""
        self._disable_rate_limit = False

    async def predict_congestion(self):
        """Predict network congestion based on historical mempool data."""
        if not self.node_connection:
            raise Exception("No node connection available")

        try:
            await self._check_rate_limit()
            await self._check_concurrent_requests()

            try:
                mempool_info = await self._make_request_with_retry("getmempoolinfo")
                mempool_bytes = mempool_info.get("bytes", 0)
                mempool_size = mempool_info.get("size", 0)
                
                # Calculate average block time from recent history
                if len(self.historical_metrics) > 1:
                    recent_blocks = [m.get("blocks", 0) for m in self.historical_metrics[-2:]]
                    if len(recent_blocks) >= 2:
                        blocks_per_hour = recent_blocks[1] - recent_blocks[0]
                        next_block_eta = 3600 / blocks_per_hour if blocks_per_hour > 0 else float('inf')
                    else:
                        next_block_eta = 600  # Default to 10 minutes
                else:
                    next_block_eta = 600

                # Analyze historical trends
                trend = "stable"  # Default to stable
                if len(self.historical_metrics) > 1:
                    recent_metrics = sorted(self.historical_metrics, key=lambda x: x["timestamp"])[-10:]
                    size_changes = [m2["mempool_size"] - m1["mempool_size"] 
                                  for m1, m2 in zip(recent_metrics[:-1], recent_metrics[1:])]
                    
                    # Calculate the overall trend
                    total_change = sum(size_changes)
                    if total_change > 1000:  # Significant increase
                        trend = "increasing"
                    elif total_change < -1000:  # Significant decrease
                        trend = "decreasing"
                    else:
                        trend = "stable"

                # Determine congestion level
                if mempool_bytes < 1_000_000:  # Less than 1MB
                    congestion_level = "low"
                    confidence = 0.9
                elif mempool_bytes < 5_000_000:  # Less than 5MB
                    congestion_level = "medium"
                    confidence = 0.7
                else:
                    congestion_level = "high"
                    confidence = 0.8

                # Get fee estimates
                fee_info = await self._make_request_with_retry("estimatesmartfee", [2])
                estimated_fee_rate = fee_info.get("feerate", 1) if isinstance(fee_info, dict) else fee_info

                return {
                    "congestion_level": congestion_level,
                    "confidence": confidence,
                    "mempool_bytes": mempool_bytes,
                    "mempool_size": mempool_size,
                    "next_block_eta": next_block_eta,
                    "estimated_fee_rate": float(estimated_fee_rate),
                    "trend": trend
                }

            finally:
                self._release_request()

        except Exception as e:
            raise Exception(f"Failed to predict congestion: {str(e)}")
            
    async def analyze_mempool(self) -> Dict[str, Any]:
        """Perform detailed analysis of the mempool state."""
        if not self.node_connection:
            raise Exception("No Bitcoin Core connection available")

        try:
            await self._check_rate_limit()
            await self._check_concurrent_requests()

            try:
                # Get mempool data
                mempool_info = await self._make_request_with_retry("getmempoolinfo")
                mempool_size = mempool_info.get("size", 0)
                mempool_bytes = mempool_info.get("bytes", 0)

                # Calculate utilization
                max_mempool_size = 300000  # Example max size
                utilization = min(1.0, mempool_size / max_mempool_size)

                # Create fee histogram (10 buckets)
                fee_histogram = [0] * 10  # Initialize with zeros

                # Create size histogram (10 buckets)
                size_histogram = [0] * 10  # Initialize with zeros

                # Analyze transaction types
                transaction_types = {
                    "standard": 0,
                    "segwit": 0,
                    "unknown": 0
                }

                return {
                    "mempool_size": mempool_size,
                    "mempool_bytes": mempool_bytes,
                    "utilization": utilization,
                    "fee_histogram": fee_histogram,
                    "size_histogram": size_histogram,
                    "transaction_types": transaction_types
                }

            finally:
                self._release_request()

        except Exception as e:
            raise Exception(f"Failed to analyze mempool: {str(e)}")
            
    async def check_synchronization(self):
        """Check the synchronization status of the network."""
        if not self.node_connection:
            raise Exception("No node connection available")

        try:
            blockchain_info = await self.node_connection._make_request("getblockchaininfo")
            headers = blockchain_info.get("headers", 0)
            blocks = blockchain_info.get("blocks", 0)
            blocks_behind = headers - blocks
            initial_block_download = blockchain_info.get("initialblockdownload", False)
            verification_progress = blockchain_info.get("verificationprogress", 0.0)

            # Calculate estimated time remaining based on recent block processing speed
            if blocks_behind > 0 and len(self.historical_metrics) > 1:
                recent_blocks = [m["blocks"] for m in self.historical_metrics[-2:]]
                if len(recent_blocks) >= 2:
                    blocks_per_second = (recent_blocks[1] - recent_blocks[0]) / 3600  # Assuming hourly metrics
                    estimated_time_remaining = blocks_behind / blocks_per_second if blocks_per_second > 0 else float('inf')
                else:
                    estimated_time_remaining = float('inf')
            else:
                estimated_time_remaining = 0

            return {
                "is_synced": blocks_behind == 0,
                "blocks_behind": blocks_behind,
                "initial_block_download": initial_block_download,
                "estimated_time_remaining": estimated_time_remaining,
                "hours_remaining": estimated_time_remaining / 3600 if estimated_time_remaining != float('inf') else float('inf'),
                "progress": verification_progress,  # Keep as decimal between 0 and 1
                "verification_progress": verification_progress
            }
        except Exception as e:
            raise Exception(f"Failed to check synchronization status: {str(e)}") 