# ✨ GBU2™ License Notice - Consciousness Level 9 🧬
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
SHA256 Crypto Analyzer

Provides analysis tools for cryptographic hashes, blockchain proof generation,
and visualization of hash properties.
"""

import hashlib
import base64
import time
import os
import json
import random
import math
from typing import Dict, List, Tuple, Union, Optional, Any, BinaryIO, cast, TypeVar
from datetime import datetime
import re

# Flag to check if visualization libraries are available
VISUALIZATION_AVAILABLE = False

# Type for numpy array-like objects
T = TypeVar('T')
ArrayLike = List[T]

# Try to import visualization dependencies - use try/except for each import
try:
    # Import numpy functions individually with error handling
    try:
        from numpy import ndarray  # type: ignore
        from numpy import mean as np_mean  # type: ignore
        from numpy import median as np_median  # type: ignore
        from numpy import std as np_std  # type: ignore
        from numpy import array as np_array  # type: ignore
        from numpy import log2 as np_log2  # type: ignore
    except ImportError:
        # These will be defined in the fallback section
        pass
        
    import matplotlib  # type: ignore
    import matplotlib.pyplot as plt  # type: ignore
    from io import BytesIO
    from matplotlib.figure import Figure  # type: ignore
    VISUALIZATION_AVAILABLE = True
except ImportError:
    # Will use fallback implementations
    pass

# Define fallback functions/classes for visualization if not available
if not VISUALIZATION_AVAILABLE:
    class MockBytesIO:
        def __init__(self):
            self.buffer = b""
            
        def getvalue(self) -> bytes:
            return self.buffer
            
        def seek(self, pos: int) -> None:
            pass
    
    # Simple numpy-like functions for fallback
    class MockNumpy:
        @staticmethod
        def mean(values: List[int]) -> float:
            return sum(values) / len(values) if values else 0
        
        @staticmethod
        def median(values: List[int]) -> float:
            sorted_values = sorted(values)
            n = len(sorted_values)
            if n == 0:
                return 0
            if n % 2 == 1:
                return sorted_values[n // 2]
            else:
                return (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
        
        @staticmethod
        def std(values: List[int]) -> float:
            if not values:
                return 0
            mean = sum(values) / len(values)
            return math.sqrt(sum((x - mean) ** 2 for x in values) / len(values))
            
        @staticmethod
        def array(values: ArrayLike[T]) -> ArrayLike[T]:
            return values
            
        class MockArray(List[Any]):
            def __init__(self, data: List[Any]):
                super().__init__(data)
                
            def reshape(self, shape: Tuple[int, int]) -> List[List[Any]]:
                """Implementation of reshape for 2D arrays"""
                result = []
                rows, cols = shape
                for i in range(rows):
                    row = []
                    for j in range(cols):
                        if i * cols + j < len(self):
                            row.append(self[i * cols + j])
                        else:
                            row.append(0)
                    result.append(row)
                return result
            
        @staticmethod
        def reshape(array: List[Any], shape: Tuple[int, int]) -> List[List[Any]]:
            """Mock implementation of reshape for 2D arrays"""
            mock_array = MockNumpy.MockArray(array)
            return mock_array.reshape(shape)
            
        @staticmethod
        def log2(value: float) -> float:
            return math.log2(value)
    
    # Mock empty module for matplotlib
    class MockFig:
        def savefig(self, buffer: Any, format: str = 'png', dpi: int = 100) -> None:
            pass
            
        def colorbar(self, im: Any, ax: Any = None, label: str = '') -> Any:
            class MockColorbar:
                pass
            return MockColorbar()
    
    class MockIm:
        pass
            
    class MockAx:
        def bar(self, *args: Any, **kwargs: Any) -> None:
            pass
            
        def set_title(self, title: str) -> None:
            pass
            
        def set_xlabel(self, label: str) -> None:
            pass
            
        def set_ylabel(self, label: str) -> None:
            pass
            
        def grid(self, enabled: bool = True, alpha: float = 0.3) -> None:
            pass
            
        def imshow(self, *args: Any, **kwargs: Any) -> MockIm:
            return MockIm()
    
    class MockPlt:
        @staticmethod
        def subplots(*args: Any, **kwargs: Any) -> Tuple[MockFig, Tuple[MockAx, MockAx]]:
            return MockFig(), (MockAx(), MockAx())
        
        @staticmethod
        def tight_layout() -> None:
            pass
            
        @staticmethod
        def close(fig: Any = None) -> None:
            pass
    
    # Create mock objects
    np_mean = MockNumpy.mean
    np_median = MockNumpy.median
    np_std = MockNumpy.std
    np_array = MockNumpy.array
    np_log2 = MockNumpy.log2
    MockArray = MockNumpy.MockArray
    plt = MockPlt()
    BytesIO = MockBytesIO

class CryptoAnalyzer:
    """
    Analyzer for SHA256 cryptographic operations with blockchain proof capabilities.
    """
    
    def __init__(self, redis_client=None):
        """
        Initialize the crypto analyzer.
        
        Args:
            redis_client: Optional Redis client for metrics tracking
        """
        self.redis_client = redis_client
        self.hash_history = []
        self.last_analysis = None
        
    def compute_sha256(self, data: Union[str, bytes]) -> str:
        """
        Compute SHA256 hash of input data.
        
        Args:
            data: Input data as string or bytes
            
        Returns:
            Hexadecimal representation of SHA256 hash
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
            
        hash_obj = hashlib.sha256(data)
        hash_hex = hash_obj.hexdigest()
        
        # Track metrics if Redis is available
        if self.redis_client:
            try:
                self.redis_client.hincrby('crypto_analyzer:metrics', 'total_hashes', 1)
                self.redis_client.lpush('crypto_analyzer:recent_hashes', hash_hex)
                self.redis_client.ltrim('crypto_analyzer:recent_hashes', 0, 99)  # Keep last 100
            except Exception as e:
                print(f"Redis error: {e}")
                
        self.hash_history.append({
            'hash': hash_hex,
            'timestamp': datetime.now().isoformat(),
            'data_length': len(data)
        })
        
        return hash_hex
    
    def analyze_hash(self, hash_str: str) -> Dict[str, Any]:
        """
        Analyze properties of a SHA256 hash.
        
        Args:
            hash_str: Hexadecimal hash string to analyze
            
        Returns:
            Dictionary of hash properties and analysis
        """
        if not re.match(r'^[0-9a-f]{64}$', hash_str, re.IGNORECASE):
            return {'error': 'Invalid SHA256 hash format'}
            
        # Normalize to lowercase
        hash_str = hash_str.lower()
        
        # Calculate bit distribution
        binary_repr = ''.join(format(int(c, 16), '04b') for c in hash_str)
        ones_count = binary_repr.count('1')
        zeros_count = binary_repr.count('0')
        
        # Calculate hex character distribution
        char_counts = {hex_char: hash_str.count(hex_char) for hex_char in '0123456789abcdef'}
        
        # Entropy calculation (Shannon entropy)
        entropy = 0
        for count in char_counts.values():
            if count > 0:
                probability = count / len(hash_str)
                entropy -= probability * np_log2(probability)
                
        # Check for leading zeros (mining difficulty)
        leading_zeros = len(hash_str) - len(hash_str.lstrip('0'))
        
        # Generate analysis result
        analysis = {
            'hash': hash_str,
            'bit_distribution': {
                'ones': ones_count,
                'zeros': zeros_count,
                'ones_percentage': round(ones_count / (ones_count + zeros_count) * 100, 2)
            },
            'character_distribution': char_counts,
            'entropy': round(entropy, 6),
            'mining_difficulty': {
                'leading_zeros': leading_zeros,
                'difficulty_score': 16 ** leading_zeros if leading_zeros > 0 else 1
            },
            'visualization_data': {
                'binary_chunks': [binary_repr[i:i+8] for i in range(0, len(binary_repr), 8)],
                'hex_chunks': [hash_str[i:i+8] for i in range(0, len(hash_str), 8)]
            }
        }
        
        self.last_analysis = analysis
        return analysis
    
    def generate_blockchain_proof(self, data: Union[str, bytes], 
                                 difficulty: int = 1) -> Dict[str, Any]:
        """
        Generate a blockchain-style proof of work for given data.
        
        Args:
            data: Input data to create proof for
            difficulty: Number of leading zeros required (mining difficulty)
            
        Returns:
            Dictionary containing the proof details
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
            
        nonce = 0
        start_time = time.time()
        target_prefix = '0' * difficulty
        
        while True:
            nonce_bytes = str(nonce).encode('utf-8')
            # Fix bytes concatenation by using a new bytes object
            combined_data = bytearray(data)
            combined_data.extend(nonce_bytes)
            hash_hex = hashlib.sha256(combined_data).hexdigest()
            
            if hash_hex.startswith(target_prefix):
                break
                
            nonce += 1
            
            # Safety check to prevent infinite loops
            if nonce > 10000000:  # 10M attempts max
                return {
                    'error': 'Proof generation timeout - difficulty too high',
                    'recommendation': 'Try a lower difficulty level'
                }
                
        end_time = time.time()
        
        proof = {
            'original_data': data.decode('utf-8') if isinstance(data, bytes) else data,
            'nonce': nonce,
            'hash': hash_hex,
            'difficulty': difficulty,
            'attempts': nonce + 1,
            'time_seconds': round(end_time - start_time, 3),
            'hash_rate': round((nonce + 1) / (end_time - start_time), 2),
            'timestamp': datetime.now().isoformat()
        }
        
        # Track proof generation if Redis is available
        if self.redis_client:
            try:
                self.redis_client.hincrby('crypto_analyzer:metrics', 'proofs_generated', 1)
                # Convert to integer explicitly for Redis
                total_operations = int(nonce + 1)
                self.redis_client.hincrby('crypto_analyzer:metrics', 'total_hash_operations', total_operations)
            except Exception as e:
                print(f"Redis error: {e}")
                
        return proof
    
    def visualize_hash_distribution(self, hash_str: str) -> Tuple[bytes, Dict[str, Any]]:
        """
        Create visualization of hash byte distribution.
        
        Args:
            hash_str: SHA256 hash to visualize
            
        Returns:
            Tuple of (png_bytes, metadata)
        """
        if not VISUALIZATION_AVAILABLE:
            return b"", {"error": "Visualization libraries not available"}
            
        # Parse hash to bytes
        hash_bytes = bytes.fromhex(hash_str)
        
        # Create figure and axes
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plot 1: Byte distribution as bar chart
        byte_values = list(hash_bytes)
        ax1.bar(range(len(byte_values)), byte_values, color='darkblue', alpha=0.7)
        ax1.set_title('SHA256 Byte Distribution')
        ax1.set_xlabel('Byte Position')
        ax1.set_ylabel('Byte Value')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: 2D visualization (8x8 heatmap of the 64 hex chars)
        hex_values = [int(hash_str[i:i+2], 16) for i in range(0, 64, 2)]
        
        if VISUALIZATION_AVAILABLE:
            # Create a properly typed grid with actual numpy if available
            try:
                # We use explicit imports with type ignore to avoid linter errors
                from numpy import array, reshape  # type: ignore
                grid = array(hex_values).reshape((8, 8))
            except (ImportError, AttributeError):
                # Fallback to basic list operations if reshape fails
                grid = [hex_values[i:i+8] for i in range(0, len(hex_values), 8)]
        else:
            # Use our mock implementation with proper array type
            array_obj = MockArray(hex_values)
            grid = array_obj.reshape((8, 8))
            
        im = ax2.imshow(grid, cmap='viridis')
        fig.colorbar(im, ax=ax2, label='Byte Value')
        
        # Save figure to bytes
        buffer = BytesIO()
        plt.tight_layout()
        
        if VISUALIZATION_AVAILABLE:
            # Only save the figure if matplotlib is available
            try:
                from matplotlib.figure import Figure  # type: ignore
                from io import BytesIO as RealBytesIO
                # Cast fig to Figure to help type checker
                typed_fig = cast(Figure, fig)
                # Create a real BytesIO object if needed
                real_buffer = buffer if isinstance(buffer, RealBytesIO) else RealBytesIO()
                typed_fig.savefig(real_buffer, format='png', dpi=100)
                plt.close(typed_fig)
                real_buffer.seek(0)
                image_bytes = real_buffer.getvalue()
            except Exception as e:
                print(f"Error saving figure: {e}")
                image_bytes = b""
        else:
            image_bytes = b""
        
        # Calculate metadata about the distribution
        if byte_values:
            mean_val = float(np_mean(byte_values))
            median_val = float(np_median(byte_values))
            std_dev = float(np_std(byte_values))
            min_val = float(min(byte_values))
            max_val = float(max(byte_values))
        else:
            mean_val = 0.0
            median_val = 0.0
            std_dev = 0.0
            min_val = 0.0
            max_val = 0.0
            
        metadata = {
            'mean': mean_val,
            'median': median_val,
            'std_dev': std_dev,
            'min': min_val,
            'max': max_val,
            'entropy': self.last_analysis['entropy'] if self.last_analysis else None
        }
        
        return image_bytes, metadata
    
    def extract_hashes(self, text: str) -> List[str]:
        """
        Extract SHA256 hashes from text content.
        
        Args:
            text: Input text to scan for hashes
            
        Returns:
            List of found SHA256 hashes
        """
        # Match SHA256 pattern (64 hex characters)
        pattern = r'\b[0-9a-fA-F]{64}\b'
        return re.findall(pattern, text)
    
    def verify_hash(self, data: Union[str, bytes], expected_hash: str) -> Dict[str, Any]:
        """
        Verify if data matches expected hash.
        
        Args:
            data: Data to verify
            expected_hash: Expected SHA256 hash
            
        Returns:
            Verification result details
        """
        actual_hash = self.compute_sha256(data)
        matches = actual_hash.lower() == expected_hash.lower()
        
        return {
            'valid': matches,
            'expected_hash': expected_hash,
            'actual_hash': actual_hash,
            'timestamp': datetime.now().isoformat()
        }
    
    def hash_file(self, file_path: str) -> Dict[str, Any]:
        """
        Compute SHA256 hash of a file.
        
        Args:
            file_path: Path to file to hash
            
        Returns:
            Hash and file metadata
        """
        if not os.path.exists(file_path):
            return {'error': f'File not found: {file_path}'}
            
        try:
            file_size = os.path.getsize(file_path)
            
            # Read file and compute hash
            sha256_hash = hashlib.sha256()
            md5_hash = hashlib.md5()
            
            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(65536)  # Read in 64k chunks
                    if not data:
                        break
                    sha256_hash.update(data)
                    md5_hash.update(data)
            
            result = {
                'filename': os.path.basename(file_path),
                'file_size': file_size,
                'file_size_human': self._format_size(file_size),
                'sha256': sha256_hash.hexdigest(),
                'md5': md5_hash.hexdigest(),
                'timestamp': datetime.now().isoformat()
            }
            
            # Track hash in history
            self.hash_history.append({
                'hash': result['sha256'],
                'filename': result['filename'],
                'timestamp': result['timestamp'],
                'file_size': file_size
            })
            
            return result
            
        except Exception as e:
            return {'error': f'Failed to hash file: {str(e)}'}
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB" 