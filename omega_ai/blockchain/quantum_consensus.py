"""
OMEGA BTC AI - Quantum Consensus Node Implementation

License: GPU (General Public Universal) License v1.0
Copyright (c) 2024-2025 OMEGA BTC AI DIVINE COLLECTIVE

Version: 0.6.1-quantum-consensus

This module implements quantum-resistant consensus nodes for the OMEGA BTC AI blockchain.
Features include:
- Double-hashing quantum-resistant cryptography
- Byzantine fault tolerance with weighted voting
- Self-healing network partition recovery
- Horizontal scalability through sharding
- Cross-shard validation and transaction processing

All rights granted under the GPU License. See LICENSE file for full terms.
"""

import time
import asyncio
import hashlib
import json
import uuid
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Set, Tuple, Union

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class QuantumNode:
    """Quantum-resistant consensus node implementation."""
    
    def __init__(self, node_id: str, processing_power: float = 1.0, latency: float = 0.01):
        """
        Initialize a quantum-resistant consensus node.
        
        Args:
            node_id: Unique identifier for this node
            processing_power: Relative quantum processing capability (higher = more influence)
            latency: Network latency simulation in seconds
        """
        self.node_id = node_id
        self.processing_power = processing_power
        self.blocks = []  # Local blockchain copy
        self.pending_transactions = []  # Mempool
        self.processed_transactions: Set[str] = set()  # Set of processed transaction IDs
        self.peers = []  # Connected peers
        self.consensus_votes = {}  # Votes for consensus
        self.latency = latency
        self.shard_id: Optional[str] = None  # Shard identifier
        self.is_cross_validator = False  # Whether this node validates across shards
        self.connected_shards: Set[str] = set()  # Shards this node is connected to
        self.last_block_time = 0  # Time of last block creation
        self.mining_interval = 10  # Seconds between blocks
        
    def add_peer(self, peer: 'QuantumNode') -> bool:
        """
        Add a peer node to the network.
        
        Args:
            peer: The peer node to connect with
            
        Returns:
            bool: True if peer was added, False otherwise
        """
        if peer not in self.peers and peer.node_id != self.node_id:
            self.peers.append(peer)
            logger.debug(f"Node {self.node_id} connected to peer {peer.node_id}")
            return True
        return False
            
    async def create_block(self, previous_hash: str) -> Dict[str, Any]:
        """
        Create a new quantum-resistant block.
        
        Args:
            previous_hash: Hash of the previous block in the chain
            
        Returns:
            Dict[str, Any]: The newly created block
        """
        # Take up to 100 transactions that haven't been processed
        transactions = []
        tx_count = 0
        
        for tx in self.pending_transactions:
            if tx_count >= 100:
                break
                
            tx_id = tx.get("id")
            if tx_id and tx_id not in self.processed_transactions:
                transactions.append(tx)
                tx_count += 1
        
        # If no transactions, create at least one dummy transaction
        if not transactions:
            tx_id = str(uuid.uuid4())
            transactions = [{
                "id": tx_id,
                "sender": f"node_{self.node_id}",
                "recipient": f"network",
                "amount": 0.0,
                "timestamp": int(datetime.now(timezone.utc).timestamp()),
                "signature": self._generate_quantum_signature(f"dummy_{tx_id}")
            }]
            
        # Update current timestamp
        current_time = int(datetime.now(timezone.utc).timestamp())
        
        # Create block with metadata
        block = {
            "index": len(self.blocks) + 1,
            "timestamp": current_time,
            "transactions": transactions,
            "previous_hash": previous_hash,
            "merkle_root": self._calculate_merkle_root(transactions),
            "nonce": self._find_nonce(previous_hash, current_time),
            "difficulty": self._calculate_difficulty(),
            "node_id": self.node_id,
            "shard_id": self.shard_id,
            "quantum_signature": self._generate_quantum_signature(f"{previous_hash}_{current_time}")
        }
        
        # Add hash to the block
        block_data = block.copy()
        block["hash"] = await self._generate_quantum_resistant_hash(block_data)
        
        # Mark these transactions as processed
        for tx in transactions:
            if "id" in tx:
                self.processed_transactions.add(tx["id"])
        
        # Update last block time
        self.last_block_time = current_time
        
        logger.info(f"Node {self.node_id} created block {block['index']} with {len(transactions)} transactions")
        return block
    
    async def _generate_quantum_resistant_hash(self, data: Dict[str, Any]) -> str:
        """
        Generate a quantum-resistant hash.
        
        In a production environment, this would use a post-quantum cryptographic algorithm.
        For this implementation, we use a double-hashing approach with SHA-256.
        
        Args:
            data: The data to hash
            
        Returns:
            str: The quantum-resistant hash
        """
        # Remove hash field if present to avoid circular reference
        data_copy = data.copy()
        if "hash" in data_copy:
            del data_copy["hash"]
            
        # Convert to sorted JSON string for consistent hashing
        serialized = json.dumps(data_copy, sort_keys=True, default=str)
        
        # First hash
        first_hash = hashlib.sha256(serialized.encode()).hexdigest()
        
        # Add quantum salt for enhanced security
        quantum_salt = f"quantum_salt_{self.node_id}_{datetime.now().isoformat()}"
        
        # Second hash with quantum salt
        quantum_hash = hashlib.sha256((first_hash + quantum_salt).encode()).hexdigest()
        
        return quantum_hash
    
    def _generate_quantum_signature(self, data: str) -> str:
        """
        Generate a quantum-resistant signature.
        
        In a production environment, this would use a post-quantum signature scheme
        like SPHINCS+ or Falcon. For this implementation, we simulate with a UUID.
        
        Args:
            data: The data to sign
            
        Returns:
            str: The quantum signature
        """
        # In real implementation, would use a post-quantum signature algorithm
        signature_base = hashlib.sha256(data.encode()).hexdigest()
        return f"quantum_signature_{signature_base}_{uuid.uuid4()}"
    
    def _calculate_merkle_root(self, transactions: List[Dict[str, Any]]) -> str:
        """
        Calculate the Merkle root of a list of transactions.
        
        Args:
            transactions: List of transaction dictionaries
            
        Returns:
            str: The Merkle root hash
        """
        if not transactions:
            return hashlib.sha256(b"").hexdigest()
            
        # Get transaction hashes
        tx_hashes = [hashlib.sha256(json.dumps(tx, sort_keys=True).encode()).hexdigest() 
                     for tx in transactions]
        
        # Build Merkle tree
        while len(tx_hashes) > 1:
            if len(tx_hashes) % 2 != 0:
                tx_hashes.append(tx_hashes[-1])  # Duplicate last hash if odd number
                
            tx_hashes = [hashlib.sha256((tx_hashes[i] + tx_hashes[i+1]).encode()).hexdigest() 
                        for i in range(0, len(tx_hashes), 2)]
                
        return tx_hashes[0]
    
    def _find_nonce(self, previous_hash: str, timestamp: int) -> int:
        """
        Find a nonce that satisfies the difficulty requirement.
        
        Args:
            previous_hash: Hash of the previous block
            timestamp: Current timestamp
            
        Returns:
            int: The valid nonce
        """
        nonce = 0
        difficulty = self._calculate_difficulty()
        
        # Simulate proof of work
        # In a production environment, we would do actual mining
        # For this implementation, we use a simplified approach
        nonce = int(hashlib.sha256(f"{previous_hash}_{timestamp}_{self.node_id}".encode()).hexdigest(), 16) % 1000000
        
        return nonce
    
    def _calculate_difficulty(self) -> int:
        """
        Calculate the current mining difficulty.
        
        Returns:
            int: The difficulty value
        """
        # Simple difficulty calculation
        # In a production environment, this would be dynamic based on network hashrate
        base_difficulty = 4
        
        # If part of a shard, adjust difficulty based on shard
        if self.shard_id:
            try:
                shard_number = int(self.shard_id)
                return base_difficulty + (shard_number % 3)  # Slight variation by shard
            except (ValueError, TypeError):
                pass
                
        return base_difficulty
    
    async def validate_block(self, block: Dict[str, Any]) -> bool:
        """
        Validate a block using quantum-resistant verification.
        
        Args:
            block: The block to validate
            
        Returns:
            bool: True if block is valid, False otherwise
        """
        try:
            # Check basic block structure
            required_fields = {"index", "timestamp", "transactions", "previous_hash", 
                              "merkle_root", "nonce", "difficulty", "quantum_signature"}
            if not all(field in block for field in required_fields):
                logger.warning(f"Node {self.node_id} rejected block: missing required fields")
                return False
                
            # Verify quantum signature
            if not self._verify_quantum_signature(block):
                logger.warning(f"Node {self.node_id} rejected block: invalid quantum signature")
                return False
            
            # Verify previous hash if we have blocks
            if self.blocks and block["index"] > 1:
                prev_block = None
                for b in self.blocks:
                    if b["index"] == block["index"] - 1:
                        prev_block = b
                        break
                        
                if prev_block and prev_block["hash"] != block["previous_hash"]:
                    logger.warning(f"Node {self.node_id} rejected block: invalid previous hash")
                    return False
            
            # Verify block hash
            if "hash" in block:
                block_data = block.copy()
                del block_data["hash"]
                calculated_hash = await self._generate_quantum_resistant_hash(block_data)
                if calculated_hash != block["hash"]:
                    logger.warning(f"Node {self.node_id} rejected block: invalid hash")
                    return False
            
            # Verify merkle root
            calculated_merkle = self._calculate_merkle_root(block["transactions"])
            if calculated_merkle != block["merkle_root"]:
                logger.warning(f"Node {self.node_id} rejected block: invalid merkle root")
                return False
            
            # Block passed all validations
            logger.debug(f"Node {self.node_id} validated block {block['index']}")
            return True
            
        except Exception as e:
            logger.error(f"Node {self.node_id} error validating block: {e}")
            return False
    
    def _verify_quantum_signature(self, block: Dict[str, Any]) -> bool:
        """
        Verify the quantum signature of a block.
        
        Args:
            block: The block to verify
            
        Returns:
            bool: True if signature is valid, False otherwise
        """
        # In a production environment, this would use actual signature verification
        # For this implementation, we use a simple prefix check
        return isinstance(block["quantum_signature"], str) and block["quantum_signature"].startswith("quantum_signature_")
    
    async def propagate_block(self, block: Dict[str, Any]) -> None:
        """
        Propagate a block to peers with network latency simulation.
        
        Args:
            block: The block to propagate
        """
        logger.debug(f"Node {self.node_id} propagating block {block['index']} to {len(self.peers)} peers")
        
        # Check if we should propagate across shards
        propagate_across_shards = self.is_cross_validator or not self.shard_id
        
        for peer in self.peers:
            # Check if we should propagate to this peer based on shards
            if not propagate_across_shards and self.shard_id and peer.shard_id != self.shard_id:
                continue
                
            # Simulate network latency based on processing power
            await asyncio.sleep(self.latency * (1 / self.processing_power))
            await peer.receive_block(block)
    
    async def receive_block(self, block: Dict[str, Any]) -> bool:
        """
        Process a received block from the network.
        
        Args:
            block: The received block
            
        Returns:
            bool: True if block was added, False otherwise
        """
        # If we don't have a block index, add it
        if "index" not in block:
            logger.warning(f"Node {self.node_id} received block without index")
            return False
            
        # If we already have this block index, check if it's the same
        existing_blocks = [b for b in self.blocks if b["index"] == block["index"]]
        if existing_blocks and existing_blocks[0].get("hash") == block.get("hash"):
            logger.debug(f"Node {self.node_id} already has block {block['index']}")
            return False
            
        # Validate the block
        if await self.validate_block(block):
            # If we already have a block with this index, only replace if from same shard
            # or if we're a cross-validator
            if existing_blocks:
                if self.is_cross_validator or (
                    block.get("shard_id") == self.shard_id or 
                    not self.shard_id or 
                    not block.get("shard_id")
                ):
                    # Replace the existing block
                    for i, b in enumerate(self.blocks):
                        if b["index"] == block["index"]:
                            self.blocks[i] = block
                            break
                    logger.info(f"Node {self.node_id} replaced block {block['index']}")
                return True
            
            # Add the new block
            self.blocks.append(block)
            logger.info(f"Node {self.node_id} added new block {block['index']}")
            
            # Update processed transactions
            for tx in block["transactions"]:
                if "id" in tx:
                    self.processed_transactions.add(tx["id"])
                    
            # Remove processed transactions from pending
            self.pending_transactions = [tx for tx in self.pending_transactions 
                                       if tx.get("id") not in self.processed_transactions]
            
            return True
        
        return False
    
    async def reach_consensus(self) -> Dict[int, Dict[str, Any]]:
        """
        Reach consensus among nodes using quantum-resistant weighted voting.
        
        Returns:
            Dict[int, Dict[str, Any]]: Consensus blocks indexed by block index
        """
        # For each block index, find the most agreed-upon version
        consensus_blocks = {}
        
        # Reset consensus votes
        self.consensus_votes = {}
        
        # Initialize consensus_votes for each block in our chain
        for block in self.blocks:
            index = block["index"]
            block_hash = block["hash"]
            
            if index not in self.consensus_votes:
                self.consensus_votes[index] = {}
                
            if block_hash not in self.consensus_votes[index]:
                self.consensus_votes[index][block_hash] = 0
                
            # Vote for our own block
            self.consensus_votes[index][block_hash] += 1
            
        # Collect votes from peers (weighted by quantum processing power)
        for peer in self.peers:
            peer_vote_weight = peer.processing_power
            
            # Cross-validators have extra voting power
            if peer.is_cross_validator:
                peer_vote_weight *= 1.5
                
            for block in peer.blocks:
                index = block["index"]
                block_hash = block["hash"]
                
                if index not in self.consensus_votes:
                    self.consensus_votes[index] = {}
                    
                if block_hash not in self.consensus_votes[index]:
                    self.consensus_votes[index][block_hash] = 0
                    
                # Peer's vote weighted by their quantum processing power
                self.consensus_votes[index][block_hash] += peer_vote_weight
        
        # Determine the winning block for each index
        for index, votes in self.consensus_votes.items():
            if votes:
                # Find the hash with the most votes
                winning_hash = max(votes.items(), key=lambda x: x[1])[0]
                
                # Find the block with this hash in our blocks
                winning_blocks = [b for b in self.blocks if b.get("hash") == winning_hash]
                if winning_blocks:
                    consensus_blocks[index] = winning_blocks[0]
                else:
                    # Try to find the block from peers
                    for peer in self.peers:
                        peer_winning_blocks = [b for b in peer.blocks if b.get("hash") == winning_hash]
                        if peer_winning_blocks:
                            # Add winning block to our blocks for future consensus
                            block_to_add = peer_winning_blocks[0]
                            await self.receive_block(block_to_add)
                            consensus_blocks[index] = block_to_add
                            break
        
        logger.debug(f"Node {self.node_id} reached consensus on {len(consensus_blocks)} blocks")
        return consensus_blocks
    
    async def mine(self) -> None:
        """
        Mine new blocks in a loop.
        """
        logger.info(f"Node {self.node_id} started mining")
        
        while True:
            current_time = time.time()
            
            # Only mine if enough time has passed since last block
            if current_time - self.last_block_time >= self.mining_interval:
                # Get previous hash (from our last block or genesis)
                previous_hash = "0" * 64  # Genesis block
                if self.blocks:
                    previous_hash = self.blocks[-1]["hash"]
                
                # Create and add new block
                new_block = await self.create_block(previous_hash)
                self.blocks.append(new_block)
                
                # Propagate to peers
                await self.propagate_block(new_block)
                
                # Update last block time
                self.last_block_time = current_time
                
            # Sleep a bit before next mining attempt
            await asyncio.sleep(1)


class QuantumNetworkManager:
    """Manages a network of quantum-resistant consensus nodes."""
    
    def __init__(self):
        """Initialize the quantum network manager."""
        self.nodes: List[QuantumNode] = []
        self.shards: Dict[str, List[QuantumNode]] = {}
        self.cross_validators: List[QuantumNode] = []
        self.is_running = False
        self.tasks = []
    
    async def create_network(self, num_nodes: int = 5, num_shards: int = 1) -> None:
        """
        Create a network of quantum-resistant nodes.
        
        Args:
            num_nodes: Total number of nodes to create
            num_shards: Number of shards to create
        """
        self.nodes = []
        self.shards = {}
        self.cross_validators = []
        
        # Ensure we have at least one node per shard
        if num_nodes < num_shards:
            num_nodes = num_shards
            
        # Create nodes with varying processing power
        for i in range(num_nodes):
            # Processing power between 0.5 and 2.0
            processing_power = 0.5 + (i / max(1, num_nodes - 1)) * 1.5
            
            # Create node
            node = QuantumNode(f"node_{i}", processing_power)
            self.nodes.append(node)
            
            # Assign to shard
            if num_shards > 1:
                shard_id = str(i % num_shards)
                node.shard_id = shard_id
                
                if shard_id not in self.shards:
                    self.shards[shard_id] = []
                    
                self.shards[shard_id].append(node)
        
        # Create cross-shard validators - one per shard
        if num_shards > 1:
            for shard_id, shard_nodes in self.shards.items():
                if shard_nodes:
                    # Select node with highest processing power as validator
                    validator = max(shard_nodes, key=lambda n: n.processing_power)
                    validator.is_cross_validator = True
                    validator.connected_shards = set(self.shards.keys())
                    self.cross_validators.append(validator)
        
        # Connect nodes in a mesh network within shards
        if num_shards > 1:
            # Connect nodes within each shard
            for shard_id, shard_nodes in self.shards.items():
                for node in shard_nodes:
                    for peer in shard_nodes:
                        if node.node_id != peer.node_id:
                            node.add_peer(peer)
            
            # Connect cross-validators to all nodes
            for validator in self.cross_validators:
                for node in self.nodes:
                    if validator.node_id != node.node_id:
                        validator.add_peer(node)
                        node.add_peer(validator)
        else:
            # Simple mesh network if no sharding
            for node in self.nodes:
                for peer in self.nodes:
                    if node.node_id != peer.node_id:
                        node.add_peer(peer)
                        
        logger.info(f"Created quantum network with {num_nodes} nodes in {num_shards} shards")
    
    async def start_network(self) -> None:
        """
        Start the quantum network.
        """
        if self.is_running:
            logger.warning("Network is already running")
            return
            
        self.is_running = True
        self.tasks = []
        
        # Start mining on all nodes
        for node in self.nodes:
            task = asyncio.create_task(node.mine())
            self.tasks.append(task)
            
        logger.info(f"Started quantum network with {len(self.nodes)} nodes")
    
    async def stop_network(self) -> None:
        """
        Stop the quantum network.
        """
        if not self.is_running:
            logger.warning("Network is not running")
            return
            
        self.is_running = False
        
        # Cancel all tasks
        for task in self.tasks:
            task.cancel()
            
        # Wait for tasks to complete
        await asyncio.gather(*self.tasks, return_exceptions=True)
        self.tasks = []
        
        logger.info("Stopped quantum network")
    
    async def add_transaction(self, transaction: Dict[str, Any]) -> str:
        """
        Add a transaction to the network.
        
        Args:
            transaction: The transaction to add
            
        Returns:
            str: The transaction ID
        """
        # Ensure transaction has ID
        if "id" not in transaction:
            transaction["id"] = str(uuid.uuid4())
            
        # Ensure timestamp
        if "timestamp" not in transaction:
            transaction["timestamp"] = int(datetime.now(timezone.utc).timestamp())
            
        # Add to nodes based on sharding
        if "shard_id" in transaction and transaction["shard_id"] in self.shards:
            # Add to specific shard
            shard_id = transaction["shard_id"]
            for node in self.shards[shard_id]:
                node.pending_transactions.append(transaction)
        else:
            # Add to all nodes if no shard specified
            for node in self.nodes:
                node.pending_transactions.append(transaction)
                
        logger.info(f"Added transaction {transaction['id']} to the network")
        return transaction["id"]
    
    async def check_consensus(self) -> bool:
        """
        Check if all nodes have reached consensus on the blockchain.
        
        Returns:
            bool: True if consensus reached, False otherwise
        """
        if not self.nodes:
            return False
            
        # Get the consensus blocks from the first node
        reference_node = self.nodes[0]
        reference_blocks = await reference_node.reach_consensus()
        
        # Check if all nodes agree
        for node in self.nodes[1:]:
            node_blocks = await node.reach_consensus()
            
            # Compare the two consensus views
            if len(reference_blocks) != len(node_blocks):
                return False
                
            for index, block in reference_blocks.items():
                if index not in node_blocks:
                    return False
                    
                if block["hash"] != node_blocks[index]["hash"]:
                    return False
        
        return True
    
    async def simulate_network_partition(self, partition_percentage: float = 0.3) -> None:
        """
        Simulate a network partition where some nodes are disconnected.
        
        Args:
            partition_percentage: Percentage of nodes to partition (0.0-1.0)
        """
        partition_count = max(1, int(len(self.nodes) * partition_percentage))
        partitioned_nodes = self.nodes[:partition_count]
        
        logger.info(f"Simulating network partition with {partition_count} nodes")
        
        # Disconnect partitioned nodes from the rest
        for node in partitioned_nodes:
            node.peers = [peer for peer in node.peers 
                         if any(peer.node_id == n.node_id for n in partitioned_nodes)]
                         
        # Wait a bit for the partition to take effect
        await asyncio.sleep(1)
    
    async def heal_network_partition(self) -> None:
        """
        Heal a network partition by reconnecting all nodes.
        """
        logger.info("Healing network partition")
        
        # Reconnect all nodes in a mesh network
        for node in self.nodes:
            node.peers = []
            for peer in self.nodes:
                if node.node_id != peer.node_id:
                    node.add_peer(peer)
                    
        # Wait a bit for healing to take effect
        await asyncio.sleep(1)
    
    async def get_blockchain(self, node_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get the blockchain from a specific node or the first node.
        
        Args:
            node_id: ID of the node to get the blockchain from, or None for first node
            
        Returns:
            List[Dict[str, Any]]: The blockchain as a list of blocks
        """
        target_node = None
        
        if node_id:
            # Find node by ID
            for node in self.nodes:
                if node.node_id == node_id:
                    target_node = node
                    break
        else:
            # Use first node
            if self.nodes:
                target_node = self.nodes[0]
                
        if not target_node:
            return []
            
        # Use the node's consensus view
        consensus_blocks = await target_node.reach_consensus()
        
        # Convert to sorted list
        sorted_blocks = [consensus_blocks[idx] for idx in sorted(consensus_blocks.keys())]
        
        return sorted_blocks


class ServiceToConsensusConnector:
    """Connector for services to interact with the quantum consensus network."""
    
    def __init__(self, service_id: str, network_manager: QuantumNetworkManager):
        """
        Initialize the service connector.
        
        Args:
            service_id: Unique identifier for the service
            network_manager: The quantum network manager
        """
        self.service_id = service_id
        self.network_manager = network_manager
        
    async def submit_data(self, data: Any, signature: Optional[str] = None) -> str:
        """
        Submit data to the consensus network.
        
        Args:
            data: The data to submit
            signature: Optional signature for the data
            
        Returns:
            str: The transaction ID
        """
        # Create transaction
        transaction = {
            "id": str(uuid.uuid4()),
            "service_id": self.service_id,
            "data": data,
            "timestamp": int(datetime.now(timezone.utc).timestamp()),
            "signature": signature or f"service_signature_{uuid.uuid4()}"
        }
        
        # Submit to network
        tx_id = await self.network_manager.add_transaction(transaction)
        
        return tx_id
        
    async def retrieve_service_data(self) -> List[Dict[str, Any]]:
        """
        Retrieve all data for this service from the blockchain.
        
        Returns:
            List[Dict[str, Any]]: List of transactions for this service
        """
        # Get the blockchain
        blockchain = await self.network_manager.get_blockchain()
        
        # Extract service data
        service_data = []
        for block in blockchain:
            for tx in block["transactions"]:
                if tx.get("service_id") == self.service_id:
                    service_data.append(tx)
                    
        return service_data


async def run_demo():
    """Run a demonstration of the quantum consensus network."""
    logger.info("Starting quantum consensus network demonstration")
    
    # Create network manager
    network = QuantumNetworkManager()
    
    # Create network with 9 nodes in 3 shards
    await network.create_network(num_nodes=9, num_shards=3)
    
    # Start the network
    await network.start_network()
    
    # Create a service connector
    market_trends_service = ServiceToConsensusConnector("market_trends_monitor", network)
    
    # Submit some market trend predictions
    for i in range(5):
        trend = "Bullish" if i % 2 == 0 else "Bearish"
        confidence = 0.5 + (i * 0.1)
        
        data = {
            "prediction": trend,
            "confidence": confidence,
            "price": 35000 + (i * 100)
        }
        
        tx_id = await market_trends_service.submit_data(data)
        logger.info(f"Submitted market trend prediction: {trend} (ID: {tx_id})")
        
        # Wait a bit between transactions
        await asyncio.sleep(2)
    
    # Wait for mining and consensus
    logger.info("Waiting for mining and consensus...")
    await asyncio.sleep(15)
    
    # Check consensus
    consensus_reached = await network.check_consensus()
    logger.info(f"Consensus reached: {consensus_reached}")
    
    # Retrieve market trend data
    market_data = await market_trends_service.retrieve_service_data()
    logger.info(f"Retrieved {len(market_data)} market trend predictions")
    
    # Simulate network partition
    await network.simulate_network_partition(0.3)
    
    # Submit data during partition
    partition_data = {
        "prediction": "Strongly Bullish",
        "confidence": 0.95,
        "price": 36000
    }
    tx_id = await market_trends_service.submit_data(partition_data)
    logger.info(f"Submitted prediction during partition (ID: {tx_id})")
    
    # Wait for mining during partition
    await asyncio.sleep(10)
    
    # Heal network
    await network.heal_network_partition()
    
    # Wait for consensus after healing
    logger.info("Waiting for consensus after healing...")
    await asyncio.sleep(15)
    
    # Check consensus again
    consensus_reached = await network.check_consensus()
    logger.info(f"Consensus after healing: {consensus_reached}")
    
    # Retrieve final data
    final_data = await market_trends_service.retrieve_service_data()
    logger.info(f"Final data count: {len(final_data)}")
    
    # Stop the network
    await network.stop_network()
    
    logger.info("Quantum consensus demonstration completed")


if __name__ == "__main__":
    # Run the demo
    asyncio.run(run_demo()) 