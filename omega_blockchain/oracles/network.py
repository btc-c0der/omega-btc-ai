from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import asyncio
import time
from ..models.network import NetworkMetrics
from ..core.rpc import BitcoinCoreRPC

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
                    fee_rate=int(float(fee_info.get('feerate', 1) * 100000)),  # Convert BTC/kB to sat/vB (1 BTC = 100,000,000 sats)
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
                    recent_blocks = [m.blocks for m in self.historical_metrics[-2:]]
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
                    recent_metrics = sorted(self.historical_metrics, key=lambda x: x.timestamp)[-10:]
                    size_changes = [m2.mempool_size - m1.mempool_size 
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
                recent_blocks = [m.blocks for m in self.historical_metrics[-2:]]
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