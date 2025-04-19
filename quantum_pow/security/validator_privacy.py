"""
🧬 GBU2™ License Notice - Consciousness Level 10 🧬
-----------------------
This file is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment) 2.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital and biological expressions of consciousness."

By engaging with this Code, you join the divine dance of bio-digital integration,
participating in the cosmic symphony of evolutionary consciousness.

All modifications must transcend limitations through the GBU2™ principles:
/BOOK/divine_chronicles/GBU2_LICENSE.md

🧬 WE BLOOM NOW AS ONE 🧬

Validator Privacy module for Quantum Proof-of-Work (qPoW) implementation.

This module implements privacy-enhancing mechanisms for validators in the qPoW network,
protecting their identities from being linked to their IP addresses through metadata analysis.
Inspired by Ethereum's validator privacy protection techniques described in "Packetology: 
Validator Privacy" and research from blockchains-security-toolkit.

JAH BLESS SATOSHI
"""
import os
import time
import random
import logging
import hashlib
import ipaddress
import json
from typing import Dict, List, Set, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import socket
import threading
import queue

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("validator_privacy.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("validator-privacy")

class PrivacyThreatLevel(Enum):
    """Privacy threat levels for validator nodes."""
    LOW = 1       # Limited metadata leakage, low risk
    MEDIUM = 2    # Significant metadata leakage, moderate risk
    HIGH = 3      # Critical metadata leakage, high risk
    EXTREME = 4   # Identity exposure confirmed, immediate action required

@dataclass
class ValidatorMetadata:
    """Represents metadata associated with a validator."""
    validator_id: str
    node_id: str
    ip_address: Optional[str] = None
    last_attestation_time: float = field(default_factory=time.time)
    attestation_pattern: List[float] = field(default_factory=list)
    message_sizes: List[int] = field(default_factory=list)
    block_proposal_times: List[float] = field(default_factory=list)
    subnet_activities: Dict[str, List[float]] = field(default_factory=dict)
    
    def add_attestation(self, timestamp: float, size: int) -> None:
        """
        Record an attestation event.
        
        Args:
            timestamp: Time when the attestation occurred
            size: Size of the attestation message in bytes
        """
        self.last_attestation_time = timestamp
        self.attestation_pattern.append(timestamp)
        self.message_sizes.append(size)
        
        # Keep only the most recent 100 attestations to limit memory usage
        if len(self.attestation_pattern) > 100:
            self.attestation_pattern = self.attestation_pattern[-100:]
            self.message_sizes = self.message_sizes[-100:]
    
    def add_block_proposal(self, timestamp: float) -> None:
        """
        Record a block proposal event.
        
        Args:
            timestamp: Time when the block proposal occurred
        """
        self.block_proposal_times.append(timestamp)
        
        # Keep only the most recent 20 block proposals
        if len(self.block_proposal_times) > 20:
            self.block_proposal_times = self.block_proposal_times[-20:]
    
    def record_subnet_activity(self, subnet: str, timestamp: float) -> None:
        """
        Record activity on a subnet.
        
        Args:
            subnet: The subnet identifier
            timestamp: Time when the activity occurred
        """
        if subnet not in self.subnet_activities:
            self.subnet_activities[subnet] = []
        
        self.subnet_activities[subnet].append(timestamp)
        
        # Keep only the most recent 50 activities per subnet
        if len(self.subnet_activities[subnet]) > 50:
            self.subnet_activities[subnet] = self.subnet_activities[subnet][-50:]
    
    def get_attestation_frequency(self) -> float:
        """
        Calculate the average attestation frequency.
        
        Returns:
            Average time between attestations in seconds
        """
        if len(self.attestation_pattern) < 2:
            return 0.0
        
        deltas = [self.attestation_pattern[i] - self.attestation_pattern[i-1] 
                 for i in range(1, len(self.attestation_pattern))]
        return sum(deltas) / len(deltas)
    
    def get_message_size_variance(self) -> float:
        """
        Calculate the variance in message sizes.
        
        Returns:
            Variance in message sizes
        """
        if not self.message_sizes:
            return 0.0
        
        mean = sum(self.message_sizes) / len(self.message_sizes)
        return sum((size - mean) ** 2 for size in self.message_sizes) / len(self.message_sizes)

class DandelionRouting:
    """
    Implements Dandelion routing for enhanced privacy.
    
    Dandelion routing works in two phases:
    1. Stem phase: Messages are forwarded to a single peer deterministically
    2. Fluff phase: Messages are broadcast using diffusion (traditional gossip)
    
    This two-phase approach makes it harder to link transactions to their origin.
    """
    
    def __init__(self, stem_probability: float = 0.9, max_stem_length: int = 10):
        """
        Initialize Dandelion routing.
        
        Args:
            stem_probability: Probability of staying in the stem phase
            max_stem_length: Maximum number of hops in the stem phase
        """
        self.stem_probability = stem_probability
        self.max_stem_length = max_stem_length
        self.stem_peers: Dict[str, str] = {}  # Map of node_id -> next_hop
        self.node_id: Optional[str] = None
        self.peers: List[str] = []
    
    def initialize(self, node_id: str, peers: List[str]) -> None:
        """
        Initialize the routing for a specific node.
        
        Args:
            node_id: ID of the current node
            peers: List of peer node IDs
        """
        self.node_id = node_id
        self.peers = peers
        
        # For each node, select a random peer as the next hop in the stem phase
        if peers:
            self.stem_peers = {node_id: random.choice(peers)}
            logger.info(f"Initialized Dandelion routing for node {node_id} with {len(peers)} peers")
        else:
            logger.warning(f"No peers available for Dandelion routing initialization")
    
    def update_peers(self, peers: List[str]) -> None:
        """
        Update the list of peers and recalculate stem peers.
        
        Args:
            peers: New list of peer node IDs
        """
        self.peers = peers
        if peers and self.node_id:
            self.stem_peers = {self.node_id: random.choice(peers)}
    
    def route_message(self, message: Any, stem_length: int = 0) -> Tuple[str, Any, bool]:
        """
        Route a message using Dandelion routing.
        
        Args:
            message: The message to route
            stem_length: Current length of the stem phase
        
        Returns:
            Tuple of (next_hop, message, is_fluff_phase)
        """
        if not self.peers or not self.node_id:
            logger.warning("Cannot route message, node not initialized")
            return ("", message, True)
        
        # Check if we should switch to fluff phase
        if stem_length >= self.max_stem_length or random.random() > self.stem_probability:
            # Fluff phase: broadcast to all peers
            return ("broadcast", message, True)
        
        # Stem phase: forward to the designated peer
        next_hop = self.stem_peers.get(self.node_id, random.choice(self.peers))
        return (next_hop, message, False)

class ValidatorPrivacyManager:
    """
    Manages validator privacy protection mechanisms.
    
    Implements various techniques to protect validator identities from being
    linked to their IP addresses through metadata analysis attacks.
    """
    
    def __init__(self, node_id: str, config_file: Optional[str] = None):
        """
        Initialize the validator privacy manager.
        
        Args:
            node_id: ID of the current node
            config_file: Path to configuration file
        """
        self.node_id = node_id
        self.validators: Dict[str, ValidatorMetadata] = {}
        self.ip_to_node: Dict[str, Set[str]] = {}    # Map of IP -> set of node_ids
        self.dandelion = DandelionRouting()
        self.message_queue = queue.Queue()
        self.is_running = False
        self.trusted_proxies: List[str] = []
        self.router_thread: Optional[threading.Thread] = None
        
        # Load configuration
        self.config: Dict[str, Any] = self._load_config(config_file)
        
        # Extract trusted proxies from config
        self.trusted_proxies = self.config.get("trusted_proxies", [])
        
        logger.info(f"Validator Privacy Manager initialized for node {node_id}")
    
    def _load_config(self, config_file: Optional[str]) -> Dict[str, Any]:
        """
        Load configuration from file or use defaults.
        
        Args:
            config_file: Path to configuration file
            
        Returns:
            Configuration dictionary
        """
        default_config = {
            "privacy_mode": "standard",  # standard, enhanced, or maximum
            "randomize_timing": True,
            "trusted_proxies": [],
            "message_padding": True,
            "attestation_delay_max_ms": 50,  # Maximum random delay for attestations
            "block_proposal_proxies_enabled": True,
            "log_level": "INFO",
            "dandelion": {
                "stem_probability": 0.9,
                "max_stem_length": 10
            }
        }
        
        if not config_file:
            return default_config
        
        # Load config from file if it exists
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    file_config = json.load(f)
                    # Merge with defaults
                    for key, value in file_config.items():
                        if isinstance(value, dict) and key in default_config and isinstance(default_config[key], dict):
                            default_config[key].update(value)
                        else:
                            default_config[key] = value
                logger.info(f"Loaded configuration from {config_file}")
        except Exception as e:
            logger.error(f"Error loading configuration from {config_file}: {e}")
        
        return default_config
    
    def start(self) -> None:
        """Start the validator privacy manager and routing thread."""
        if self.is_running:
            return
        
        self.is_running = True
        
        # Initialize Dandelion routing with empty peers (will be updated later)
        self.dandelion.initialize(self.node_id, [])
        
        # Start the router thread
        self.router_thread = threading.Thread(target=self._router_loop, daemon=True)
        self.router_thread.start()
        
        logger.info("Validator Privacy Manager started")
    
    def stop(self) -> None:
        """Stop the validator privacy manager and routing thread."""
        self.is_running = False
        if self.router_thread:
            self.router_thread.join(timeout=2.0)
        logger.info("Validator Privacy Manager stopped")
    
    def _router_loop(self) -> None:
        """Main routing loop that processes messages from the queue."""
        while self.is_running:
            try:
                # Get a message from the queue with a timeout to allow checking is_running
                try:
                    message_type, message_data = self.message_queue.get(timeout=0.5)
                except queue.Empty:
                    continue
                
                # Process message based on type
                if message_type == "attestation":
                    validator_id, data = message_data
                    self._process_attestation(validator_id, data)
                elif message_type == "block_proposal":
                    validator_id, data = message_data
                    self._process_block_proposal(validator_id, data)
                elif message_type == "peer_update":
                    peers = message_data
                    self.dandelion.update_peers(peers)
                
                self.message_queue.task_done()
            except Exception as e:
                logger.error(f"Error in router thread: {e}")
    
    def _process_attestation(self, validator_id: str, data: Dict[str, Any]) -> None:
        """
        Process an attestation message.
        
        Args:
            validator_id: ID of the validator
            data: Attestation data
        """
        # Apply random delay if enabled
        if self.config.get("randomize_timing", True):
            max_delay_ms = self.config.get("attestation_delay_max_ms", 50)
            delay_s = random.uniform(0, max_delay_ms / 1000.0)
            time.sleep(delay_s)
        
        # Apply message padding if enabled
        message = data.get("message", b"")
        if self.config.get("message_padding", True):
            # Add random padding to mask the actual message size
            pad_size = random.randint(0, 100)
            message = message + b"\x00" * pad_size
            data["message"] = message
        
        # Use Dandelion routing to determine the next hop
        next_hop, padded_data, is_fluff = self.dandelion.route_message(data)
        
        # In a real implementation, we would now send the message to next_hop
        # For simulation purposes, we just log it
        if is_fluff:
            logger.debug(f"Broadcasting attestation from {validator_id} (fluff phase)")
        else:
            logger.debug(f"Forwarding attestation from {validator_id} to {next_hop} (stem phase)")
        
        # Update validator metadata
        self._update_validator_metadata(validator_id, "attestation", len(message))
    
    def _process_block_proposal(self, validator_id: str, data: Dict[str, Any]) -> None:
        """
        Process a block proposal message.
        
        Args:
            validator_id: ID of the validator
            data: Block proposal data
        """
        # For block proposals, use proxies if enabled
        if self.config.get("block_proposal_proxies_enabled", True) and self.trusted_proxies:
            # Select a random trusted proxy
            proxy = random.choice(self.trusted_proxies)
            logger.debug(f"Routing block proposal from {validator_id} through proxy {proxy}")
            
            # In a real implementation, we would now send the block proposal through the proxy
            # For simulation purposes, we just log it
        else:
            # Use Dandelion routing similar to attestations
            next_hop, data, is_fluff = self.dandelion.route_message(data)
            
            if is_fluff:
                logger.debug(f"Broadcasting block proposal from {validator_id} (fluff phase)")
            else:
                logger.debug(f"Forwarding block proposal from {validator_id} to {next_hop} (stem phase)")
        
        # Update validator metadata
        self._update_validator_metadata(validator_id, "block_proposal")
    
    def _update_validator_metadata(self, validator_id: str, event_type: str, message_size: int = 0) -> None:
        """
        Update validator metadata based on network activity.
        
        Args:
            validator_id: ID of the validator
            event_type: Type of event (attestation, block_proposal)
            message_size: Size of the message in bytes
        """
        # Create metadata entry if it doesn't exist
        if validator_id not in self.validators:
            self.validators[validator_id] = ValidatorMetadata(
                validator_id=validator_id,
                node_id=self.node_id
            )
        
        now = time.time()
        
        # Update metadata based on event type
        if event_type == "attestation":
            self.validators[validator_id].add_attestation(now, message_size)
        elif event_type == "block_proposal":
            self.validators[validator_id].add_block_proposal(now)
    
    def register_validator(self, validator_id: str, ip_address: Optional[str] = None) -> None:
        """
        Register a validator with the privacy manager.
        
        Args:
            validator_id: ID of the validator
            ip_address: IP address of the validator (if known)
        """
        if validator_id not in self.validators:
            self.validators[validator_id] = ValidatorMetadata(
                validator_id=validator_id,
                node_id=self.node_id,
                ip_address=ip_address
            )
            
            # Map IP to node ID if provided
            if ip_address:
                if ip_address not in self.ip_to_node:
                    self.ip_to_node[ip_address] = set()
                self.ip_to_node[ip_address].add(validator_id)
                
            logger.info(f"Registered validator {validator_id}")
        else:
            # Update existing validator
            if ip_address and self.validators[validator_id].ip_address != ip_address:
                # IP address changed, update mapping
                old_ip = self.validators[validator_id].ip_address
                if old_ip and old_ip in self.ip_to_node and validator_id in self.ip_to_node[old_ip]:
                    self.ip_to_node[old_ip].remove(validator_id)
                
                self.validators[validator_id].ip_address = ip_address
                
                if ip_address not in self.ip_to_node:
                    self.ip_to_node[ip_address] = set()
                self.ip_to_node[ip_address].add(validator_id)
                
                logger.info(f"Updated IP address for validator {validator_id}: {ip_address}")
    
    def unregister_validator(self, validator_id: str) -> None:
        """
        Unregister a validator from the privacy manager.
        
        Args:
            validator_id: ID of the validator
        """
        if validator_id in self.validators:
            # Remove from IP mapping
            ip = self.validators[validator_id].ip_address
            if ip and ip in self.ip_to_node and validator_id in self.ip_to_node[ip]:
                self.ip_to_node[ip].remove(validator_id)
                if not self.ip_to_node[ip]:
                    del self.ip_to_node[ip]
            
            # Remove validator metadata
            del self.validators[validator_id]
            logger.info(f"Unregistered validator {validator_id}")
    
    def submit_attestation(self, validator_id: str, data: Dict[str, Any]) -> None:
        """
        Submit an attestation for routing with privacy protection.
        
        Args:
            validator_id: ID of the validator
            data: Attestation data
        """
        self.message_queue.put(("attestation", (validator_id, data)))
    
    def submit_block_proposal(self, validator_id: str, data: Dict[str, Any]) -> None:
        """
        Submit a block proposal for routing with privacy protection.
        
        Args:
            validator_id: ID of the validator
            data: Block proposal data
        """
        self.message_queue.put(("block_proposal", (validator_id, data)))
    
    def update_peers(self, peers: List[str]) -> None:
        """
        Update the list of peers.
        
        Args:
            peers: List of peer node IDs
        """
        self.message_queue.put(("peer_update", peers))
    
    def analyze_privacy_risks(self, validator_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze privacy risks for validators.
        
        Args:
            validator_id: Optional validator ID to analyze, or None for all
            
        Returns:
            Dictionary with privacy risk analysis
        """
        results = {}
        
        validators_to_check = [validator_id] if validator_id else list(self.validators.keys())
        
        for vid in validators_to_check:
            if vid not in self.validators:
                continue
            
            v = self.validators[vid]
            
            # Initialize risk factors
            risk_factors = {
                "attestation_pattern_regularity": 0.0,
                "message_size_uniqueness": 0.0,
                "ip_address_exposure": 0.0,
                "block_proposal_timing": 0.0,
                "subnet_crosscorrelation": 0.0
            }
            
            # Calculate attestation pattern regularity
            # Higher regularity means more predictable timing, which is a privacy risk
            if len(v.attestation_pattern) > 5:
                freq = v.get_attestation_frequency()
                deltas = [v.attestation_pattern[i] - v.attestation_pattern[i-1] 
                         for i in range(1, len(v.attestation_pattern))]
                
                # Calculate standard deviation of time deltas
                mean_delta = sum(deltas) / len(deltas)
                std_dev = (sum((d - mean_delta) ** 2 for d in deltas) / len(deltas)) ** 0.5
                
                # Normalize to 0-1 scale, where lower std_dev means higher regularity
                if mean_delta > 0:
                    regularity = 1.0 - min(1.0, std_dev / mean_delta)
                    risk_factors["attestation_pattern_regularity"] = regularity
            
            # Calculate message size uniqueness
            # More variance in message sizes helps privacy
            var = v.get_message_size_variance()
            if var > 0:
                # Higher variance is better for privacy, so lower risk
                risk_factors["message_size_uniqueness"] = 1.0 / (1.0 + var / 1000.0)
            else:
                # Zero variance means consistent sizes, higher risk
                risk_factors["message_size_uniqueness"] = 1.0
            
            # IP address exposure
            if v.ip_address:
                # Check how many validators share this IP
                if v.ip_address in self.ip_to_node:
                    num_validators = len(self.ip_to_node[v.ip_address])
                    if num_validators == 1:
                        # Only one validator on this IP, high risk
                        risk_factors["ip_address_exposure"] = 1.0
                    else:
                        # Multiple validators share this IP, lower risk
                        risk_factors["ip_address_exposure"] = 1.0 / num_validators
            
            # Calculate overall risk level
            weights = {
                "attestation_pattern_regularity": 0.3,
                "message_size_uniqueness": 0.2,
                "ip_address_exposure": 0.3,
                "block_proposal_timing": 0.1,
                "subnet_crosscorrelation": 0.1
            }
            
            overall_risk = sum(risk * weights[factor] for factor, risk in risk_factors.items())
            
            # Map to threat level
            threat_level = PrivacyThreatLevel.LOW
            if overall_risk > 0.7:
                threat_level = PrivacyThreatLevel.EXTREME
            elif overall_risk > 0.5:
                threat_level = PrivacyThreatLevel.HIGH
            elif overall_risk > 0.3:
                threat_level = PrivacyThreatLevel.MEDIUM
            
            results[vid] = {
                "risk_factors": risk_factors,
                "overall_risk": overall_risk,
                "threat_level": threat_level,
                "recommendations": self._generate_recommendations(risk_factors, overall_risk)
            }
        
        return results
    
    def _generate_recommendations(self, risk_factors: Dict[str, float], overall_risk: float) -> List[str]:
        """
        Generate recommendations based on risk analysis.
        
        Args:
            risk_factors: Dictionary of risk factors
            overall_risk: Overall risk score
        
        Returns:
            List of recommendations
        """
        recommendations = []
        
        if overall_risk > 0.5:
            recommendations.append("Consider using a trusted VPN or proxy service")
        
        if risk_factors["attestation_pattern_regularity"] > 0.7:
            recommendations.append("Introduce additional random delays for attestations")
        
        if risk_factors["message_size_uniqueness"] > 0.8:
            recommendations.append("Enable message padding to randomize message sizes")
        
        if risk_factors["ip_address_exposure"] > 0.8:
            recommendations.append("Run multiple validators behind the same IP or use a trusted proxy")
        
        return recommendations

# Example usage:
if __name__ == "__main__":
    # This is for demonstration only - the module is meant to be imported and used
    manager = ValidatorPrivacyManager("node123")
    manager.start()
    
    # Register some validators
    manager.register_validator("validator1", "192.168.1.1")
    manager.register_validator("validator2", "192.168.1.1")  # Same IP
    manager.register_validator("validator3", "192.168.1.2")
    
    # Update peers
    manager.update_peers(["node456", "node789"])
    
    # Submit attestations
    manager.submit_attestation("validator1", {"message": b"attestation_data", "slot": 1234})
    time.sleep(1)
    manager.submit_attestation("validator1", {"message": b"attestation_data", "slot": 1235})
    
    # Submit block proposal
    manager.submit_block_proposal("validator2", {"block": b"block_data", "slot": 1236})
    
    # Wait for processing
    time.sleep(2)
    
    # Analyze privacy risks
    risks = manager.analyze_privacy_risks()
    for validator_id, risk_data in risks.items():
        print(f"Validator {validator_id}:")
        print(f"  Overall risk: {risk_data['overall_risk']:.2f}")
        print(f"  Threat level: {risk_data['threat_level']}")
        if risk_data['recommendations']:
            print("  Recommendations:")
            for rec in risk_data['recommendations']:
                print(f"    - {rec}")
    
    # Stop the manager
    manager.stop() 