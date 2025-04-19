
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

from datetime import datetime, timedelta
from typing import List, Dict
from ..models.transaction import TransactionData

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
        """Check if two transactions are related based on address relationships."""
        # Check if any output address from tx1 is used as an input address in tx2
        tx1_outputs = {output['address'] for output in tx1.outputs}
        tx2_inputs = {input['address'] for input in tx2.inputs}
        return bool(tx1_outputs & tx2_inputs)  # Check for intersection of addresses
        
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