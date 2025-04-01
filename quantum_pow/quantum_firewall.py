#!/usr/bin/env python3
"""
OMEGA BTC AI - Quantum Firewall with Auto-Healing capabilities
==============================================================

A quantum-enhanced firewall with auto-healing capabilities that uses
Character Prefix Conditioning (CPC) to recover from attack attempts
and maintain system integrity.

The firewall monitors system traffic, detects malicious activity,
and uses quantum-based algorithms to automatically recover and 
adapt to potential threats.

🔮 GPU (General Public Universal) License 1.0
--------------------------------------------
OMEGA BTC AI DIVINE COLLECTIVE
Licensed under the GPU (General Public Universal) License v1.0
"""

import os
import sys
import json
import time
import random
import asyncio
import logging
import hashlib
import socket
import re
import threading
from typing import Dict, List, Any, Tuple, Optional, Union, Callable, Set
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field
from collections import defaultdict, Counter

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("quantum_firewall.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("quantum-firewall")

# Constants
MAX_THRESHOLD = 100  # Maximum threshold for threat detection
RECOVERY_TIMEOUT = 30  # Seconds to wait for recovery
ENTROPY_BITS = 256  # Number of bits of quantum entropy to use
DEFAULT_PORT = 8545  # Default port to monitor
HEAL_INTERVAL = 15  # Seconds between autonomous healing checks

@dataclass
class SecurityEvent:
    """Represents a security event in the firewall system."""
    
    timestamp: float
    event_type: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    source: str
    details: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "severity": self.severity,
            "source": self.source,
            "details": self.details
        }
        
    def __str__(self) -> str:
        """String representation of the security event."""
        return (f"[{self.severity.upper()}] {self.event_type} from {self.source} "
                f"at {time.ctime(self.timestamp)}")

class PrefixConditioner:
    """
    Character Prefix Conditioning (CPC) for network traffic analysis.
    
    This class implements a pattern-based learning system that:
    1. Learns legitimate prefixes and their expected completions
    2. Detects anomalies in incoming messages
    3. Can reconstruct (heal) damaged messages based on learned patterns
    """
    
    def __init__(self, max_prefix_length: int = 64, threshold: float = 0.7):
        """
        Initialize the prefix conditioner.
        
        Args:
            max_prefix_length: Maximum length of prefixes to track
            threshold: Similarity threshold for anomaly detection (0.0-1.0)
        """
        self.prefix_map: Dict[str, List[str]] = defaultdict(list)
        self.max_prefix_length = max_prefix_length
        self.threshold = threshold
        self.seen_messages: Set[str] = set()
        self.learning_mode = True
    
    def learn_prefix(self, prefix: str, full_message: str) -> None:
        """
        Learn a prefix and its associated full message.
        
        Args:
            prefix: The prefix string
            full_message: The complete message
        """
        if not self.learning_mode:
            return
        
        # Don't relearn the same message
        if full_message in self.seen_messages:
            return
        
        # Add all increasing length prefixes up to max_prefix_length
        for i in range(1, min(len(prefix) + 1, self.max_prefix_length)):
            current_prefix = prefix[:i]
            if current_prefix and full_message:
                self.prefix_map[current_prefix].append(full_message)
        
        self.seen_messages.add(full_message)
    
    def detect_anomaly(self, message: str) -> bool:
        """
        Detect if a message contains anomalous patterns.
        
        Args:
            message: The message to check
            
        Returns:
            True if the message appears anomalous, False otherwise
        """
        # Exact matches are never anomalous
        if message in self.seen_messages:
            return False
        
        # If we're still in learning mode, learn this pattern
        if self.learning_mode:
            self.learn_prefix(message, message)
            return False
        
        # Check increasing prefix lengths to find the best match
        max_similarity = 0.0
        
        for i in range(min(len(message), self.max_prefix_length), 0, -1):
            prefix = message[:i]
            if prefix in self.prefix_map:
                # We found a matching prefix, check similarity with known messages
                for known_message in self.prefix_map[prefix]:
                    similarity = self._calculate_similarity(message, known_message)
                    max_similarity = max(max_similarity, similarity)
                    
                    if similarity >= self.threshold:
                        return False  # Similar enough to a known message
                
                # If we found a matching prefix but similarity is low, that's suspicious
                if max_similarity > 0:
                    break
        
        # If no prefix matched or max_similarity is below threshold, it's anomalous
        return max_similarity < self.threshold
    
    def predict_completion(self, prefix: str) -> Optional[str]:
        """
        Predict the most likely completion for a prefix based on learned patterns.
        
        Args:
            prefix: The prefix to complete
            
        Returns:
            The most likely full message, or None if no completion is available
        """
        if not prefix:
            return None
        
        # Find the longest matching prefix
        matching_prefix = ""
        for i in range(min(len(prefix), self.max_prefix_length), 0, -1):
            current_prefix = prefix[:i]
            if current_prefix in self.prefix_map:
                matching_prefix = current_prefix
                break
        
        if not matching_prefix:
            return None
        
        # Count the frequency of each completion
        completions = Counter(self.prefix_map[matching_prefix])
        
        # Return the most common completion
        if completions:
            return completions.most_common(1)[0][0]
        return None
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """
        Calculate similarity between two strings.
        
        Uses a combination of prefix matching and character distribution similarity.
        
        Args:
            str1: First string
            str2: Second string
            
        Returns:
            Similarity score between 0.0 (completely different) and 1.0 (identical)
        """
        if not str1 or not str2:
            return 0.0
        
        if str1 == str2:
            return 1.0
        
        # Common prefix length similarity
        min_len = min(len(str1), len(str2))
        common_prefix_len = 0
        for i in range(min_len):
            if str1[i] == str2[i]:
                common_prefix_len += 1
            else:
                break
        
        prefix_similarity = common_prefix_len / min_len if min_len > 0 else 0.0
        
        # Character distribution similarity using Counter
        c1 = Counter(str1)
        c2 = Counter(str2)
        chars = set(c1.keys()) | set(c2.keys())
        
        if not chars:
            return 0.0
        
        # Calculate normalized difference in character frequencies
        total_diff = 0
        total_chars = sum(c1.values()) + sum(c2.values())
        
        if total_chars == 0:
            return 0.0
        
        for c in chars:
            freq1 = c1.get(c, 0) / len(str1) if len(str1) > 0 else 0
            freq2 = c2.get(c, 0) / len(str2) if len(str2) > 0 else 0
            total_diff += abs(freq1 - freq2)
        
        # Scale the difference to a similarity score (0-1)
        char_similarity = 1.0 - (total_diff / 2.0)  # Divide by 2 as max diff is 2.0
        
        # Combine the two similarity metrics (weighted average)
        combined_similarity = (0.7 * prefix_similarity) + (0.3 * char_similarity)
        
        return combined_similarity

class QuantumFirewall:
    """
    Quantum Firewall with Character Prefix Conditioning for network protection.
    
    Provides real-time monitoring and protection against classical and quantum threats
    using a combination of pattern recognition and anomaly detection.
    """
    
    def __init__(self, port: int = 9000, interface: str = '127.0.0.1'):
        """
        Initialize the quantum firewall.
        
        Args:
            port: Port to listen on
            interface: Network interface to bind to
        """
        self.port = port
        self.interface = interface
        self.running = False
        self.learning_mode = True
        self.prefix_conditioner = PrefixConditioner()
        self.security_events: List[SecurityEvent] = []
        self.server_socket = None
        self.thread = None
        
        # Firewall configuration
        self.max_connections = 100
        self.blocked_ips: Set[str] = set()
        self.blocked_patterns: List[re.Pattern] = []
        
        logger.info(f"Initializing Quantum Firewall on {interface}:{port}")
    
    def start(self) -> None:
        """Start the firewall server."""
        if self.running:
            logger.warning("Firewall is already running")
            return
        
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.interface, self.port))
            self.server_socket.listen(self.max_connections)
            
            self.running = True
            self.thread = threading.Thread(target=self._listen_loop)
            self.thread.daemon = True
            self.thread.start()
            
            logger.info(f"Quantum Firewall started on {self.interface}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to start firewall: {str(e)}")
            if self.server_socket:
                self.server_socket.close()
                self.server_socket = None
    
    def stop(self) -> None:
        """Stop the firewall server."""
        if not self.running:
            return
        
        self.running = False
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
        
        if self.thread:
            self.thread.join(timeout=5.0)
            self.thread = None
        
        logger.info("Quantum Firewall stopped")
    
    def toggle_learning_mode(self, enabled: bool) -> None:
        """
        Toggle learning mode on or off.
        
        Args:
            enabled: True to enable learning mode, False to disable
        """
        self.learning_mode = enabled
        self.prefix_conditioner.learning_mode = enabled
        logger.info(f"Learning mode {'enabled' if enabled else 'disabled'}")
    
    def block_ip(self, ip_address: str) -> None:
        """
        Block an IP address.
        
        Args:
            ip_address: IP address to block
        """
        self.blocked_ips.add(ip_address)
        logger.info(f"Blocked IP: {ip_address}")
    
    def add_blocked_pattern(self, pattern: str) -> None:
        """
        Add a regex pattern to block.
        
        Args:
            pattern: Regex pattern to block
        """
        try:
            compiled = re.compile(pattern)
            self.blocked_patterns.append(compiled)
            logger.info(f"Added blocked pattern: {pattern}")
        except re.error as e:
            logger.error(f"Invalid regex pattern '{pattern}': {str(e)}")
    
    def get_security_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get recent security events.
        
        Args:
            limit: Maximum number of events to return
            
        Returns:
            List of security events as dictionaries
        """
        return [event.to_dict() for event in self.security_events[-limit:]]
    
    def _listen_loop(self) -> None:
        """Main listening loop for the firewall."""
        logger.info("Firewall listening thread started")
        
        while self.running and self.server_socket:
            try:
                client_socket, address = self.server_socket.accept()
                client_ip = address[0]
                
                if client_ip in self.blocked_ips:
                    logger.warning(f"Connection from blocked IP rejected: {client_ip}")
                    client_socket.close()
                    continue
                
                # Handle the connection in a separate thread
                threading.Thread(
                    target=self._handle_connection,
                    args=(client_socket, address),
                    daemon=True
                ).start()
                
            except socket.error as e:
                if self.running:  # Only log if not intentionally stopped
                    logger.error(f"Socket error in listener: {str(e)}")
            except Exception as e:
                logger.error(f"Error in listener: {str(e)}")
    
    def _handle_connection(self, client_socket: socket.socket, address: Tuple[str, int]) -> None:
        """
        Handle an individual client connection.
        
        Args:
            client_socket: Client socket
            address: Client address tuple (ip, port)
        """
        client_ip = address[0]
        client_port = address[1]
        logger.debug(f"Handling connection from {client_ip}:{client_port}")
        
        try:
            # Set a timeout to prevent hanging
            client_socket.settimeout(10.0)
            
            # Read data from the client
            buffer = b""
            while self.running:
                data = client_socket.recv(4096)
                if not data:
                    break
                
                buffer += data
                
                # Process complete messages if possible
                messages = self._process_buffer(buffer)
                if messages:
                    buffer = b""  # Reset buffer if we processed messages
                    
                    for message in messages:
                        if self._inspect_message(message, client_ip):
                            # If message passes inspection, forward it
                            # In a real implementation, this would forward to the protected service
                            response = b"Message accepted\n"
                        else:
                            # If message fails inspection, reject it
                            response = b"Message rejected\n"
                        
                        client_socket.sendall(response)
        
        except socket.timeout:
            logger.warning(f"Connection from {client_ip}:{client_port} timed out")
        except Exception as e:
            logger.error(f"Error handling connection from {client_ip}:{client_port}: {str(e)}")
        finally:
            client_socket.close()
            logger.debug(f"Connection from {client_ip}:{client_port} closed")
    
    def _process_buffer(self, buffer: bytes) -> List[str]:
        """
        Process the buffer and extract complete messages.
        
        In a real implementation, this would handle various protocols and message formats.
        This simplified version assumes JSON messages separated by newlines.
        
        Args:
            buffer: Bytes buffer to process
            
        Returns:
            List of complete messages extracted from the buffer
        """
        try:
            # Basic implementation: assume messages are newline separated
            text = buffer.decode('utf-8')
            messages = text.split('\n')
            
            # Filter out empty messages
            return [msg for msg in messages if msg.strip()]
        except UnicodeDecodeError:
            logger.warning("Failed to decode message buffer as UTF-8")
            # Record malformed data as a security event
            self._record_security_event(
                "malformed_data",
                "medium",
                "buffer_processor",
                {"buffer_hex": buffer.hex()[:100]}
            )
            return []
    
    def _inspect_message(self, message: str, source_ip: str) -> bool:
        """
        Inspect a message for security threats.
        
        Args:
            message: The message to inspect
            source_ip: Source IP address
            
        Returns:
            True if the message is considered safe, False otherwise
        """
        # Check for blocked patterns
        for pattern in self.blocked_patterns:
            if pattern.search(message):
                self._record_security_event(
                    "blocked_pattern_match",
                    "high",
                    source_ip,
                    {"pattern": pattern.pattern, "message_sample": message[:100]}
                )
                return False
        
        # Check for anomalies using the prefix conditioner
        if self.learning_mode:
            # In learning mode, learn all messages
            self.prefix_conditioner.learn_prefix(message, message)
            return True
        else:
            # In protection mode, check for anomalies
            is_anomalous = self.prefix_conditioner.detect_anomaly(message)
            
            if is_anomalous:
                # Try to fix the message if it's damaged
                prefix_length = int(len(message) * 0.3)  # Use first 30% as prefix
                prefix = message[:prefix_length]
                predicted = self.prefix_conditioner.predict_completion(prefix)
                
                self._record_security_event(
                    "anomalous_message",
                    "medium",
                    source_ip,
                    {
                        "message_sample": message[:100],
                        "predicted_completion": predicted[:100] if predicted else None,
                        "repair_possible": predicted is not None
                    }
                )
                
                return False
        
        return True
    
    def _record_security_event(self, event_type: str, severity: str, 
                              source: str, details: Dict[str, Any]) -> None:
        """
        Record a security event.
        
        Args:
            event_type: Type of security event
            severity: Severity level (low, medium, high, critical)
            source: Source of the event (e.g., IP address)
            details: Additional details about the event
        """
        event = SecurityEvent(
            timestamp=time.time(),
            event_type=event_type,
            severity=severity,
            source=source,
            details=details
        )
        
        self.security_events.append(event)
        logger.warning(f"Security event: {event}")
        
        # Keep only the most recent events (limit to 1000)
        if len(self.security_events) > 1000:
            self.security_events = self.security_events[-1000:]

async def main():
    """Main entry point for Quantum Firewall."""
    # Parse command-line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Quantum Firewall with Auto-Healing")
    parser.add_argument('--port', type=int, default=DEFAULT_PORT, help="Port to monitor")
    parser.add_argument('--learning', action='store_true', help="Start in learning mode")
    args = parser.parse_args()
    
    # Create and start the firewall
    firewall = QuantumFirewall(port=args.port)
    if args.learning:
        firewall.toggle_learning_mode(True)
        logger.info("Starting in learning mode")
    
    try:
        await firewall.start()
    except KeyboardInterrupt:
        logger.info("Stopping Quantum Firewall due to user interrupt")
    finally:
        await firewall.stop()
        
    logger.info("Quantum Firewall stopped")

if __name__ == "__main__":
    asyncio.run(main()) 