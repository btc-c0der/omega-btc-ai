
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
OMEGA BTC AI - Quantum Consensus and Fibonacci Integration Demo

License: GPU (General Public Universal) License v1.0
Copyright (c) 2024-2025 OMEGA BTC AI DIVINE COLLECTIVE

Version: 0.6.1-quantum-consensus

This script demonstrates the integration between the Fibonacci auto-healing
functionality and the quantum-resistant consensus nodes, showcasing how
Fibonacci levels are stored, validated, and protected in the blockchain.
"""

import os
import sys
import json
import time
import asyncio
import logging
import random
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Union

# Set up path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("quantum_fibonacci_integration")

try:
    # Import Fibonacci detector
    from omega_ai.mm_trap_detector.fibonacci_detector import FibonacciDetector, SwingPoint
    # Import quantum consensus
    from omega_ai.blockchain.quantum_consensus import (
        QuantumNetworkManager, 
        ServiceToConsensusConnector
    )
    # Import Redis utilities (optional, only if needed)
    from omega_ai.config import get_redis_client
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error(f"Current directory: {current_dir}")
    logger.error(f"Project root: {project_root}")
    logger.error("Please ensure the project structure is correct")
    sys.exit(1)


class FibonacciConsensusIntegration:
    """Integrates Fibonacci detector with quantum consensus nodes."""
    
    def __init__(self):
        """Initialize the integration."""
        self.redis_client = get_redis_client()
        self.fibonacci_detector = FibonacciDetector(
            price_data_key="BTCUSD_fibonacci_test_data",
            fibonacci_levels_key="BTCUSD_fibonacci_levels",
            swing_points_key="BTCUSD_swing_points"
        )
        self.network_manager = None
        self.service_connector = None
        
    async def initialize_network(self, num_nodes: int = 5, num_shards: int = 2) -> None:
        """
        Initialize the quantum consensus network.
        
        Args:
            num_nodes: Number of nodes in the network
            num_shards: Number of shards to create
        """
        logger.info(f"Initializing quantum network with {num_nodes} nodes in {num_shards} shards")
        
        # Create and start network
        self.network_manager = QuantumNetworkManager()
        await self.network_manager.create_network(num_nodes, num_shards)
        await self.network_manager.start_network()
        
        # Create service connector for Fibonacci
        self.service_connector = ServiceToConsensusConnector(
            "fibonacci_detector", 
            self.network_manager
        )
        
        logger.info("Quantum network initialized successfully")
        
    async def generate_price_data(self, num_points: int = 100) -> None:
        """
        Generate synthetic price data for testing.
        
        Args:
            num_points: Number of price points to generate
        """
        logger.info(f"Generating {num_points} price data points")
        
        # Start with a reasonable BTC price
        price = 35000.0
        timestamp = int(datetime.now(timezone.utc).timestamp()) - (num_points * 60)
        
        price_data = []
        
        # Generate price movement with some volatility
        for i in range(num_points):
            # Random price movement (-2% to +2%)
            change_pct = (random.random() - 0.48) * 0.04  # Slightly bullish bias
            price = price * (1 + change_pct)
            
            # Create candle data
            open_price = price
            close_price = price * (1 + (random.random() - 0.5) * 0.01)
            high_price = max(open_price, close_price) * (1 + random.random() * 0.01)
            low_price = min(open_price, close_price) * (1 - random.random() * 0.01)
            
            # Add to price data
            price_data.append({
                "timestamp": timestamp + (i * 60),
                "open": open_price,
                "high": high_price,
                "low": low_price,
                "close": close_price,
                "volume": random.random() * 100
            })
            
        # Store in Redis
        self.redis_client.set(
            self.fibonacci_detector.price_data_key,
            json.dumps(price_data)
        )
        
        logger.info(f"Generated and stored {len(price_data)} price data points")
        
    async def identify_swing_points(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Identify swing points from price data.
        
        Returns:
            Dict[str, List[Dict[str, Any]]]: Dictionary with high and low swing points
        """
        logger.info("Identifying swing points from price data")
        
        # Get price data
        price_data_json = self.redis_client.get(self.fibonacci_detector.price_data_key)
        if not price_data_json:
            logger.error("No price data found in Redis")
            return {"high": [], "low": []}
            
        price_data = json.loads(price_data_json)
        
        # Identify swing points
        swing_points = self.fibonacci_detector.identify_swing_points(price_data)
        
        # Store in Redis
        self.redis_client.set(
            self.fibonacci_detector.swing_points_key,
            json.dumps({
                "high": [sp.to_dict() for sp in swing_points["high"]],
                "low": [sp.to_dict() for sp in swing_points["low"]]
            })
        )
        
        # Convert to dictionaries for return
        return {
            "high": [sp.to_dict() for sp in swing_points["high"]],
            "low": [sp.to_dict() for sp in swing_points["low"]]
        }
        
    async def calculate_fibonacci_levels(self) -> Dict[str, Any]:
        """
        Calculate Fibonacci levels from swing points.
        
        Returns:
            Dict[str, Any]: Fibonacci levels
        """
        logger.info("Calculating Fibonacci levels")
        
        # Get swing points
        swing_points_json = self.redis_client.get(self.fibonacci_detector.swing_points_key)
        if not swing_points_json:
            logger.error("No swing points found in Redis")
            return {}
            
        swing_points_data = json.loads(swing_points_json)
        
        # Convert dictionary to SwingPoint objects
        swing_points = {
            "high": [SwingPoint(**sp) for sp in swing_points_data["high"]],
            "low": [SwingPoint(**sp) for sp in swing_points_data["low"]]
        }
        
        # Calculate Fibonacci levels
        fibonacci_levels = self.fibonacci_detector.calculate_fibonacci_levels(swing_points)
        
        # Store in Redis
        self.redis_client.set(
            self.fibonacci_detector.fibonacci_levels_key,
            json.dumps(fibonacci_levels)
        )
        
        return fibonacci_levels
        
    async def submit_to_consensus(self, data_type: str) -> str:
        """
        Submit Fibonacci data to the consensus network.
        
        Args:
            data_type: Type of data to submit ("price", "swing_points", or "fibonacci_levels")
            
        Returns:
            str: Transaction ID
        """
        if not self.service_connector:
            logger.error("Service connector not initialized")
            return "ERROR: Service connector not initialized"
            
        logger.info(f"Submitting {data_type} data to consensus network")
        
        data = None
        redis_key = None
        
        # Determine which data to submit
        if data_type == "price":
            redis_key = self.fibonacci_detector.price_data_key
        elif data_type == "swing_points":
            redis_key = self.fibonacci_detector.swing_points_key
        elif data_type == "fibonacci_levels":
            redis_key = self.fibonacci_detector.fibonacci_levels_key
        else:
            logger.error(f"Unknown data type: {data_type}")
            return f"ERROR: Unknown data type: {data_type}"
            
        # Get data from Redis
        data_json = self.redis_client.get(redis_key)
        if not data_json:
            logger.error(f"No {data_type} data found in Redis")
            return f"ERROR: No {data_type} data found in Redis"
            
        try:
            data = json.loads(data_json)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON format for {data_type} data")
            return f"ERROR: Invalid JSON format for {data_type} data"
            
        # Create transaction data
        transaction_data = {
            "type": data_type,
            "timestamp": int(datetime.now(timezone.utc).timestamp()),
            "data": data
        }
        
        # Submit to consensus network
        tx_id = await self.service_connector.submit_data(transaction_data)
        
        logger.info(f"Submitted {data_type} data to consensus network (TX ID: {tx_id})")
        return tx_id
        
    async def corrupt_data_and_test_healing(self) -> None:
        """
        Corrupt Fibonacci data in Redis and test auto-healing.
        """
        logger.info("Testing auto-healing with corrupted data")
        
        # Corrupt Fibonacci levels in Redis
        original_levels = self.redis_client.get(self.fibonacci_detector.fibonacci_levels_key)
        
        # Save original for later restoration
        self.redis_client.set(
            f"{self.fibonacci_detector.fibonacci_levels_key}_backup",
            original_levels
        )
        
        # Corrupt the data
        self.redis_client.set(
            self.fibonacci_detector.fibonacci_levels_key,
            "{{invalid-json-data}}"
        )
        
        logger.info("Corrupted Fibonacci levels in Redis")
        
        # Try to calculate Fibonacci levels again (should trigger auto-healing)
        try:
            time.sleep(1)  # Wait a moment
            fibonacci_levels = self.fibonacci_detector.get_fibonacci_levels()
            logger.info("Auto-healing successful: retrieved Fibonacci levels after corruption")
        except Exception as e:
            logger.error(f"Auto-healing failed: {e}")
            
        # Restore original data
        self.redis_client.set(
            self.fibonacci_detector.fibonacci_levels_key,
            self.redis_client.get(f"{self.fibonacci_detector.fibonacci_levels_key}_backup")
        )
        self.redis_client.delete(f"{self.fibonacci_detector.fibonacci_levels_key}_backup")
        
    async def retrieve_from_consensus(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Retrieve Fibonacci data from the consensus network.
        
        Returns:
            Dict[str, List[Dict[str, Any]]]: Retrieved data by type
        """
        if not self.service_connector:
            logger.error("Service connector not initialized")
            return {}
            
        logger.info("Retrieving Fibonacci data from consensus network")
        
        # Get service data
        service_data = await self.service_connector.retrieve_service_data()
        
        # Organize by type
        organized_data = {
            "price": [],
            "swing_points": [],
            "fibonacci_levels": []
        }
        
        for tx in service_data:
            if "data" in tx and "type" in tx["data"]:
                data_type = tx["data"]["type"]
                if data_type in organized_data:
                    organized_data[data_type].append(tx["data"])
                    
        logger.info(f"Retrieved {len(service_data)} transactions from consensus network")
        
        return organized_data
        
    async def verify_data_integrity(self) -> bool:
        """
        Verify integrity of Fibonacci data in consensus network.
        
        Returns:
            bool: True if integrity is verified, False otherwise
        """
        logger.info("Verifying data integrity in consensus network")
        
        # Get latest data from Redis
        fibonacci_levels_json = self.redis_client.get(self.fibonacci_detector.fibonacci_levels_key)
        if not fibonacci_levels_json:
            logger.error("No Fibonacci levels found in Redis")
            return False
            
        try:
            fibonacci_levels = json.loads(fibonacci_levels_json)
        except json.JSONDecodeError:
            logger.error("Invalid JSON format for Fibonacci levels")
            return False
            
        # Get data from consensus network
        consensus_data = await self.retrieve_from_consensus()
        
        # Check if there are any Fibonacci levels in consensus
        if not consensus_data["fibonacci_levels"]:
            logger.error("No Fibonacci levels found in consensus network")
            return False
            
        # Get the latest Fibonacci level transaction
        latest_fibonacci = max(
            consensus_data["fibonacci_levels"], 
            key=lambda x: x["timestamp"]
        )
        
        # Compare with Redis data
        redis_data_str = json.dumps(fibonacci_levels, sort_keys=True)
        consensus_data_str = json.dumps(latest_fibonacci["data"], sort_keys=True)
        
        integrity_verified = redis_data_str == consensus_data_str
        
        if integrity_verified:
            logger.info("Data integrity verified: Redis and consensus data match")
        else:
            logger.warning("Data integrity issue: Redis and consensus data do not match")
            
        return integrity_verified
        
    async def simulate_network_partition(self) -> None:
        """
        Simulate network partition and subsequent recovery.
        """
        if not self.network_manager:
            logger.error("Network manager not initialized")
            return
            
        logger.info("Simulating network partition")
        
        # Partition network
        await self.network_manager.simulate_network_partition(0.4)
        
        # Submit data during partition
        tx_id = await self.submit_to_consensus("fibonacci_levels")
        logger.info(f"Submitted data during network partition (TX ID: {tx_id})")
        
        # Wait a bit
        await asyncio.sleep(5)
        
        # Heal network
        await self.network_manager.heal_network_partition()
        
        # Wait for consensus
        await asyncio.sleep(10)
        
        # Check consensus
        consensus_reached = await self.network_manager.check_consensus()
        logger.info(f"Consensus after healing: {consensus_reached}")
        
    async def run_demo(self) -> None:
        """
        Run the full demonstration.
        """
        logger.info("Starting Fibonacci and Quantum Consensus integration demo")
        
        # Initialize network
        await self.initialize_network(num_nodes=6, num_shards=2)
        
        # Generate price data
        await self.generate_price_data(num_points=120)
        
        # Identify swing points
        swing_points = await self.identify_swing_points()
        logger.info(f"Identified {len(swing_points['high'])} high swing points and " 
                   f"{len(swing_points['low'])} low swing points")
        
        # Calculate Fibonacci levels
        fibonacci_levels = await self.calculate_fibonacci_levels()
        logger.info(f"Calculated Fibonacci levels with {len(fibonacci_levels.get('levels', []))} points")
        
        # Submit all data to consensus
        await self.submit_to_consensus("price")
        await self.submit_to_consensus("swing_points")
        await self.submit_to_consensus("fibonacci_levels")
        
        # Wait for mining and consensus
        logger.info("Waiting for mining and consensus...")
        await asyncio.sleep(15)
        
        # Test auto-healing with corrupted data
        await self.corrupt_data_and_test_healing()
        
        # Verify data integrity
        await self.verify_data_integrity()
        
        # Simulate network partition
        await self.simulate_network_partition()
        
        # Retrieve final data
        final_data = await self.retrieve_from_consensus()
        logger.info(f"Final data summary:")
        logger.info(f"- Price data entries: {len(final_data['price'])}")
        logger.info(f"- Swing points entries: {len(final_data['swing_points'])}")
        logger.info(f"- Fibonacci levels entries: {len(final_data['fibonacci_levels'])}")
        
        # Stop the network
        await self.network_manager.stop_network()
        
        logger.info("Fibonacci and Quantum Consensus integration demo completed")


async def main():
    """Main entry point for the demo."""
    try:
        integration = FibonacciConsensusIntegration()
        await integration.run_demo()
    except Exception as e:
        logger.error(f"Error running demo: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main()) 