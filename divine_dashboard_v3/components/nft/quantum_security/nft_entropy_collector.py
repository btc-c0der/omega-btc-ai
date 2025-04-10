
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
NFT Entropy Collector - High-quality randomness for quantum-secure NFTs

This module collects high-quality entropy from multiple sources to provide
truly random values for cryptographic operations in the NFT security system.
"""

import os
import time
import random
import hashlib
import socket
import json
import platform
import uuid
import secrets
import struct
import threading
import subprocess
from typing import List, Dict, Any, Optional, Union, ByteString
from datetime import datetime
from pathlib import Path

# Try importing quantum random number generation if available
try:
    import qrandom
    QRANDOM_AVAILABLE = True
except ImportError:
    QRANDOM_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


class EntropyCollector:
    """
    High-quality entropy collector for NFT security operations.
    
    Collects entropy from multiple sources:
    1. System noise (hardware, OS)
    2. Network timing and data
    3. Temporal information (precise timing)
    4. User activity (if available)
    5. Quantum random numbers (if qrandom library available)
    
    Combines entropy sources with strong mixing to provide high-quality random values.
    """
    
    def __init__(self, sources: Optional[List[str]] = None, cache_file: Optional[str] = None):
        """
        Initialize entropy collector.
        
        Args:
            sources: List of entropy sources to use (default: all available)
            cache_file: Path to entropy cache file (default: no caching)
        """
        # Available entropy sources
        self.available_sources = ["system", "network", "temporal"]
        if QRANDOM_AVAILABLE:
            self.available_sources.append("quantum")
            
        # Use specified sources or all available
        self.sources = sources if sources else self.available_sources
        
        # Entropy cache for improved mixing
        self.entropy_cache = b''
        self.cache_file = cache_file
        
        # Load cache if specified
        if self.cache_file and Path(self.cache_file).exists():
            try:
                with open(self.cache_file, 'rb') as f:
                    self.entropy_cache = f.read()
            except Exception:
                self.entropy_cache = b''
                
        # Initialize random with system entropy
        random.seed(os.urandom(32))
        
        # Entropy collection state
        self.collection_lock = threading.Lock()
        self.last_collection = {}
    
    def collect(self, bits: int = 256) -> bytes:
        """
        Collect entropy from all enabled sources.
        
        Args:
            bits: Number of entropy bits to collect (default: 256)
            
        Returns:
            Collected entropy bytes
        """
        # Determine bytes needed (8 bits per byte)
        bytes_needed = (bits + 7) // 8
        
        # Initialize entropy accumulator
        entropy_pool = bytearray()
        
        # Collect from each source
        with self.collection_lock:
            for source in self.sources:
                try:
                    source_entropy = self.collect_from_source(source, bits)
                    entropy_pool.extend(source_entropy)
                except Exception as e:
                    print(f"Warning: Failed to collect entropy from {source}: {e}")
            
            # Add cache to pool
            if self.entropy_cache:
                entropy_pool.extend(self.entropy_cache)
            
            # Generate hash from all collected entropy
            final_hash = hashlib.sha3_512(entropy_pool).digest()
            
            # Update cache with new entropy (keep at most 1024 bytes)
            self.entropy_cache = (final_hash + self.entropy_cache)[:1024]
            
            # Save to cache file if specified
            if self.cache_file:
                with open(self.cache_file, 'wb') as f:
                    f.write(self.entropy_cache)
            
            # Return the requested amount of entropy
            return final_hash[:bytes_needed]

    def collect_from_source(self, source: str, bits: int = 256) -> bytes:
        """
        Collect entropy from specific source.
        
        Args:
            source: Entropy source name (system, network, temporal, quantum)
            bits: Number of entropy bits to collect
            
        Returns:
            Entropy bytes from the specified source
        """
        bytes_needed = (bits + 7) // 8
        
        # Choose collection method based on source
        if source == "system":
            return self._collect_system_entropy(bytes_needed)
        elif source == "network":
            return self._collect_network_entropy(bytes_needed)
        elif source == "temporal":
            return self._collect_temporal_entropy(bytes_needed)
        elif source == "quantum" and QRANDOM_AVAILABLE:
            return self.collect_quantum_random(bits)
        else:
            raise ValueError(f"Unknown entropy source: {source}")
    
    def _collect_system_entropy(self, bytes_needed: int) -> bytes:
        """
        Collect entropy from system state.
        
        Args:
            bytes_needed: Number of bytes to collect
            
        Returns:
            System entropy bytes
        """
        # Collect system information
        system_info = {
            "platform": platform.platform(),
            "python_build": platform.python_build(),
            "processor": platform.processor(),
            "hostname": platform.node(),
            "machine": platform.machine(),
            "uuid": str(uuid.uuid4()),
            "uuid1": str(uuid.uuid1()),
            "pid": os.getpid(),
            "ppid": os.getppid(),
            "random_value": random.getrandbits(1024),
            "os_urandom": base64.b64encode(os.urandom(64)).decode(),
            "secrets_token": base64.b64encode(secrets.token_bytes(64)).decode(),
        }
        
        # Add environment variables (can be sources of entropy)
        for key, value in os.environ.items():
            if key.lower() not in ["path", "user", "username"]:  # Skip common vars
                system_info[f"env_{key}"] = value
        
        # Try to get system load and memory info
        try:
            import psutil
            system_info["memory"] = psutil.virtual_memory()._asdict()
            system_info["cpu_percent"] = psutil.cpu_percent(interval=0.1)
            system_info["disk_usage"] = psutil.disk_usage('/').percent
        except ImportError:
            # psutil not available, add more random data instead
            system_info["random_extra"] = random.getrandbits(1024)
        
        # Try to get file descriptors
        try:
            system_info["fd_count"] = len(os.listdir('/proc/self/fd'))
        except (FileNotFoundError, PermissionError):
            pass
        
        # Try to get interrupt counts from /proc
        try:
            with open('/proc/interrupts', 'r') as f:
                system_info["interrupts"] = f.read()
        except (FileNotFoundError, PermissionError):
            pass
        
        # Try to get disk stats (I/O) data
        try:
            with open('/proc/diskstats', 'r') as f:
                system_info["diskstats"] = f.read()
        except (FileNotFoundError, PermissionError):
            pass
        
        # Convert to bytes and hash
        system_data = json.dumps(system_info, default=str).encode()
        system_hash = hashlib.sha3_512(system_data).digest()
        
        # If we need more bytes, extend with os.urandom
        if len(system_hash) < bytes_needed:
            return system_hash + os.urandom(bytes_needed - len(system_hash))
        
        return system_hash[:bytes_needed]
    
    def _collect_network_entropy(self, bytes_needed: int) -> bytes:
        """
        Collect entropy from network operations.
        
        Args:
            bytes_needed: Number of bytes to collect
            
        Returns:
            Network entropy bytes
        """
        # Network-based entropy sources
        network_data = bytearray()
        
        # Get local interfaces
        try:
            # Create a temporary socket to get local hostname info
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))  # Google DNS as remote endpoint
            socket_info = {
                "local_ip": s.getsockname()[0],
                "time": time.time()
            }
            s.close()
            network_data.extend(json.dumps(socket_info).encode())
        except (socket.error, OSError):
            pass
        
        # Get network timing entropy
        for host in ["8.8.8.8", "1.1.1.1", "9.9.9.9"]:
            try:
                start_time = time.time_ns()
                # Use socket with timeout
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                try:
                    s.connect((host, 53))
                except (socket.error, OSError):
                    pass
                s.close()
                end_time = time.time_ns()
                
                # Add timing information to entropy
                timing_data = struct.pack("!QQ", start_time, end_time)
                network_data.extend(timing_data)
            except (socket.error, OSError):
                pass
        
        # Try to get network statistics from /proc
        try:
            with open('/proc/net/dev', 'r') as f:
                network_data.extend(f.read().encode())
        except (FileNotFoundError, PermissionError):
            pass
        
        # Try to get network stats using a command
        try:
            result = subprocess.run(
                ["netstat", "-ian"], 
                capture_output=True, 
                timeout=1.0
            )
            if result.stdout:
                network_data.extend(result.stdout)
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        
        # Add random padding if we don't have enough network data
        if len(network_data) < 64:
            network_data.extend(os.urandom(64 - len(network_data)))
        
        # Hash the collected data
        network_hash = hashlib.sha3_512(network_data).digest()
        
        # If we need more bytes, extend with os.urandom
        if len(network_hash) < bytes_needed:
            return network_hash + os.urandom(bytes_needed - len(network_hash))
        
        return network_hash[:bytes_needed]
    
    def _collect_temporal_entropy(self, bytes_needed: int) -> bytes:
        """
        Collect entropy from high-precision timing.
        
        Args:
            bytes_needed: Number of bytes to collect
            
        Returns:
            Temporal entropy bytes
        """
        # Initialize temporal data collection
        temporal_data = bytearray()
        
        # Get high-precision timestamps with interleaved operations
        for _ in range(16):  # Collect multiple timing samples
            # Get timestamp before operation
            start_time = time.time_ns()
            
            # Perform variable-time operations
            x = random.randrange(1000000)
            for i in range(x % 1000):
                _ = i * i * i
                
            # Get timestamp after operation
            end_time = time.time_ns()
            
            # Add timing information to entropy
            temporal_data.extend(struct.pack("!QQ", start_time, end_time))
            
            # Add random delay
            time.sleep(random.random() * 0.001)  # 0-1ms random delay
        
        # Add process time info
        process_times = os.times()
        temporal_data.extend(struct.pack("!ddddd", *process_times))
        
        # Add datetime info
        now = datetime.now()
        temporal_data.extend(now.isoformat().encode())
        
        # Add nanosecond resolution timer if available on this platform
        try:
            for _ in range(32):
                temporal_data.extend(struct.pack("!Q", time.time_ns()))
                # Small random calculation to introduce timing variations
                x = 0
                for i in range(random.randrange(1000)):
                    x += i
        except AttributeError:
            # time_ns() not available, use normal time with more samples
            for _ in range(64):
                temporal_data.extend(struct.pack("!d", time.time()))
                # Small random calculation
                x = 0
                for i in range(random.randrange(1000)):
                    x += i
        
        # Hash the collected data
        temporal_hash = hashlib.sha3_512(temporal_data).digest()
        
        # If we need more bytes, extend with os.urandom
        if len(temporal_hash) < bytes_needed:
            return temporal_hash + os.urandom(bytes_needed - len(temporal_hash))
        
        return temporal_hash[:bytes_needed]
    
    def collect_quantum_random(self, bits: int = 256) -> bytes:
        """
        Collect quantum random numbers if available.
        
        Args:
            bits: Number of random bits to collect
            
        Returns:
            Quantum random bytes
        """
        if not QRANDOM_AVAILABLE:
            raise ImportError("qrandom library not available")
        
        bytes_needed = (bits + 7) // 8
        
        try:
            # Try using ANU Quantum Random Number Generator API
            quantum_bytes = qrandom.binary(bytes_needed)
            return quantum_bytes
        except Exception as e:
            print(f"Warning: Quantum random generation failed: {e}")
            
            # Fallback to local QRNG simulation if numpy available
            if NUMPY_AVAILABLE:
                return self._simulate_qrng(bytes_needed)
            
            # Last resort: use os.urandom
            return os.urandom(bytes_needed)
    
    def _simulate_qrng(self, bytes_needed: int) -> bytes:
        """
        Simulate quantum random number generation using numpy.
        
        This is a fallback when actual quantum sources are not available.
        
        Args:
            bytes_needed: Number of bytes to generate
            
        Returns:
            Simulated quantum random bytes
        """
        if not NUMPY_AVAILABLE:
            raise ImportError("numpy library required for QRNG simulation")
        
        # Seeds from system entropy
        seed = int.from_bytes(os.urandom(8), byteorder='big')
        np.random.seed(seed)
        
        # Generate random values using quantum-inspired algorithms
        # We use Box-Muller transform to get normally distributed values,
        # which better simulate quantum noise
        random_values = np.random.normal(0, 1, bytes_needed * 8)
        
        # Convert to binary bits based on sign
        bits = [1 if val >= 0 else 0 for val in random_values]
        
        # Convert bits to bytes
        result = bytearray()
        for i in range(0, len(bits), 8):
            if i + 8 <= len(bits):
                byte_val = 0
                for j in range(8):
                    byte_val |= (bits[i + j] << (7 - j))
                result.append(byte_val)
        
        return bytes(result) 