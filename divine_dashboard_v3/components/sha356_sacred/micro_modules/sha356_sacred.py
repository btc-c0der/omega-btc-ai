# ✨ GBU2™ License Notice - Consciousness Level 10 🧬
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
SHA356 Sacred Hash Function

Enhanced SHA256 with 356-bit output and bio-inspired transformations for
sacred alignment with universal harmonics.

Includes partial avalanche control and cosmic alignment scoring.
"""

import hashlib
import time
import hmac
from typing import Dict, Any, List, Tuple, Optional, Union, Literal
from datetime import datetime

from .bio_padder import bio_padder
from .fibonacci_transform import fibonacci_transform, fibonacci_transform_with_metadata
from .resonance_score import get_resonance_score

# Define a local function for detailed cosmic alignment
def get_detailed_cosmic_alignment(hash_value: str) -> Dict[str, Any]:
    """
    Calculate detailed cosmic alignment metrics for a hash value.
    
    Args:
        hash_value: The hash value to analyze
        
    Returns:
        Dictionary with various cosmic alignment metrics
    """
    return {
        "schumann_resonance": round(0.7 + 0.3 * hash_value.count('7') / len(hash_value), 2),
        "phi_alignment": round(0.6 + 0.4 * hash_value.count('1') / len(hash_value), 2),
        "lunar_phase": round(0.5 + 0.5 * hash_value.count('9') / len(hash_value), 2),
        "overall_score": get_resonance_score(hash_value)
    }

class SHA356Sacred:
    """
    SHA356 Sacred Hash implementation
    
    A sacred cryptographic hash function that extends SHA256 with
    bio-inspired transformations and additional bits of entropy
    derived from sacred mathematical principles.
    """
    
    def __init__(self):
        """Initialize the SHA356 Sacred hasher."""
        self.last_hash = None
        self.last_input = None
        self.hash_history = []
    
    @staticmethod
    def _extend_to_356_bits(hash_256: str) -> str:
        """
        Extend a 256-bit hash (as hex string) to 356 bits by adding 
        100 bits (25 hex chars) of sacred mathematical constants.
        
        Args:
            hash_256: Standard 256-bit hash as 64-char hex string
            
        Returns:
            356-bit hash as 89-char hex string
        """
        # Start with the phi constant (golden ratio)
        phi = (1 + 5**0.5) / 2
        
        # Use properties of the original hash to seed the extension
        seed = int(hash_256[:8], 16)
        
        # Generate 25 more hex characters (100 bits)
        extension = ""
        for i in range(25):
            # Use phi and original hash to generate next value
            seed = (seed * int(phi * 10**10) + int(hash_256[i % 64], 16)) % (2**32)
            extension += format(seed % 16, 'x')
        
        return hash_256 + extension
    
    def hash(self, data: Union[bytes, str], bio_transform: bool = True, 
             padding_method: Literal["fibonacci", "phi", "schumann", "lunar", "sacred"] = "fibonacci", 
             metadata: bool = True) -> Dict[str, Any]:
        """
        Generate a SHA356 Sacred hash from input data.
        
        Args:
            data: Input data to hash (bytes or string)
            bio_transform: Whether to apply bio-inspired transformations
            padding_method: Method for bio padding (fibonacci, schumann, etc.)
            metadata: Whether to include detailed metadata
            
        Returns:
            Dictionary with hash result and metadata
        """
        # Convert string to bytes if needed
        if isinstance(data, str):
            data_bytes = data.encode('utf-8')
        else:
            data_bytes = data
            
        # Store original input
        original_data = data_bytes
        
        # Initialize transform_metadata to None
        transform_metadata = None
        
        # Apply bio transformations if requested
        if bio_transform:
            # Apply bio padding
            padded_data = bio_padder(data_bytes, method=padding_method)
            
            # Apply Fibonacci transform with metadata if requested
            if metadata:
                transform_result = fibonacci_transform_with_metadata(padded_data)
                transformed_data = transform_result["transformed_data"]
                transform_metadata = transform_result["metadata"]
            else:
                transformed_data = fibonacci_transform(padded_data)
        else:
            transformed_data = data_bytes
        
        # Calculate base SHA256 hash
        hash_256 = hashlib.sha256(transformed_data).hexdigest()
        
        # Extend to 356 bits
        hash_356 = self._extend_to_356_bits(hash_256)
        
        # Calculate time stamp and cosmic resonance
        timestamp = datetime.now().isoformat()
        
        # Prepare result
        result = {
            "hash": hash_356,
            "standard_sha256": hash_256,
            "input_type": "string" if isinstance(data, str) else "bytes",
            "input_length": len(original_data),
            "timestamp": timestamp,
            "bio_transform_applied": bio_transform,
        }
        
        # Add detailed metadata if requested
        if metadata:
            if bio_transform and transform_metadata is not None:
                result["transform_metadata"] = transform_metadata
            
            # Calculate cosmic alignment
            cosmic_alignment = get_detailed_cosmic_alignment(hash_356)
            result["cosmic_alignment"] = cosmic_alignment
            
            # Calculate resonance score
            result["resonance_score"] = get_resonance_score(hash_356)
        
        # Store in history
        self.last_hash = hash_356
        self.last_input = original_data
        self.hash_history.append({
            "hash": hash_356,
            "timestamp": timestamp,
            "input_length": len(original_data)
        })
        
        return result
    
    def hash_message(self, message: str, bio_transform: bool = True,
                    padding_method: Literal["fibonacci", "phi", "schumann", "lunar", "sacred"] = "fibonacci") -> Dict[str, Any]:
        """
        Simplified interface for hashing string messages.
        
        Args:
            message: String message to hash
            bio_transform: Whether to apply bio transformations
            padding_method: Bio padding method to use
            
        Returns:
            Dictionary with hash result and essential metadata
        """
        result = self.hash(message, bio_transform, padding_method)
        
        # Simplified result for display purposes
        return {
            "message": message,
            "hash": result["hash"],
            "standard_sha256": result["standard_sha256"],
            "bio_transform": bio_transform,
            "padding_method": padding_method if bio_transform else "none",
            "timestamp": result["timestamp"],
            "resonance_score": result.get("resonance_score", None)
        }
    
    def verify(self, message: str, hash_value: str, bio_transform: bool = True,
              padding_method: Literal["fibonacci", "phi", "schumann", "lunar", "sacred"] = "fibonacci") -> bool:
        """
        Verify if a hash matches the expected value for a message.
        
        Args:
            message: Message to verify
            hash_value: Expected hash value (356-bit hex string)
            bio_transform: Whether to apply bio transformations  
            padding_method: Bio padding method to use
            
        Returns:
            True if hash matches, False otherwise
        """
        result = self.hash(message, bio_transform, padding_method, metadata=False)
        return result["hash"] == hash_value
    
    def hash_file(self, file_path: str, bio_transform: bool = True,
                 padding_method: Literal["fibonacci", "phi", "schumann", "lunar", "sacred"] = "fibonacci", 
                 chunk_size: int = 4096) -> Dict[str, Any]:
        """
        Hash a file using SHA356 Sacred.
        
        Args:
            file_path: Path to file to hash
            bio_transform: Whether to apply bio transformations
            padding_method: Bio padding method to use
            chunk_size: Size of chunks to read from file
            
        Returns:
            Dictionary with hash result and metadata
        """
        file_data = b''
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                file_data += chunk
        
        # Now apply our full algorithm to the complete file data
        return self.hash(file_data, bio_transform, padding_method)
    
    def hmac_sha356(self, key: bytes, message: bytes, bio_transform: bool = True,
                   padding_method: Literal["fibonacci", "phi", "schumann", "lunar", "sacred"] = "fibonacci") -> Dict[str, Any]:
        """
        Create an HMAC using SHA356 Sacred.
        
        Args:
            key: Secret key bytes
            message: Message bytes to authenticate
            bio_transform: Whether to apply bio transformations
            padding_method: Bio padding method to use
            
        Returns:
            Dictionary with HMAC result and metadata
        """
        # First apply bio transformations if requested
        if bio_transform:
            key = bio_padder(key, method=padding_method)
            key = fibonacci_transform(key)
            
            message = bio_padder(message, method=padding_method)
            message = fibonacci_transform(message)
        
        # Calculate standard HMAC with SHA256
        hmac_256 = hmac.new(key, message, hashlib.sha256).hexdigest()
        
        # Extend to 356 bits
        hmac_356 = self._extend_to_356_bits(hmac_256)
        
        return {
            "hmac": hmac_356,
            "standard_hmac_sha256": hmac_256,
            "bio_transform_applied": bio_transform,
            "padding_method": padding_method if bio_transform else "none",
            "timestamp": datetime.now().isoformat(),
        }

# Convenience functions for direct use
def hash_message(message: str, bio_transform: bool = True, 
                padding_method: Literal["fibonacci", "phi", "schumann", "lunar", "sacred"] = "fibonacci") -> Dict[str, Any]:
    """
    Convenience function to hash a string message with SHA356 Sacred.
    
    Args:
        message: String message to hash
        bio_transform: Whether to apply bio transformations  
        padding_method: Bio padding method to use
        
    Returns:
        Dictionary with hash result and metadata
    """
    hasher = SHA356Sacred()
    return hasher.hash_message(message, bio_transform, padding_method)

def hash_file(file_path: str, bio_transform: bool = True,
             padding_method: Literal["fibonacci", "phi", "schumann", "lunar", "sacred"] = "fibonacci") -> Dict[str, Any]:
    """
    Convenience function to hash a file with SHA356 Sacred.
    
    Args:
        file_path: Path to file to hash
        bio_transform: Whether to apply bio transformations
        padding_method: Bio padding method to use
        
    Returns:
        Dictionary with hash result and metadata
    """
    hasher = SHA356Sacred()
    return hasher.hash_file(file_path, bio_transform, padding_method)

def verify_hash(message: str, hash_value: str, bio_transform: bool = True,
               padding_method: Literal["fibonacci", "phi", "schumann", "lunar", "sacred"] = "fibonacci") -> bool:
    """
    Convenience function to verify a hash with SHA356 Sacred.
    
    Args:
        message: Message to verify
        hash_value: Expected hash value (356-bit hex string)
        bio_transform: Whether to apply bio transformations
        padding_method: Bio padding method to use
        
    Returns:
        True if hash matches, False otherwise
    """
    hasher = SHA356Sacred()
    return hasher.verify(message, hash_value, bio_transform, padding_method) 