#!/usr/bin/env python3

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
Quantum Encoder Factory
=====================

Factory module for creating quantum encoders.
This module provides a unified interface for initializing
different types of quantum encoders.
"""

import os
import logging
from typing import Dict, Any, List, Optional, Union

# Import encoders - using relative imports for better module structure
from .amplitude_encoder import AmplitudeEncoder
from .angle_encoder import AngleEncoder
from .basis_encoder import BasisEncoder
from .entanglement_encoder import EntanglementEncoder

# Set up logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Registry of available encoders
ENCODER_REGISTRY = {
    'amplitude': AmplitudeEncoder,
    'angle': AngleEncoder,
    'basis': BasisEncoder,
    'entanglement': EntanglementEncoder,
}

def get_available_encoders() -> List[str]:
    """
    Returns a list of available quantum encoder types.
    
    Returns:
        List[str]: Names of available encoders
    """
    return list(ENCODER_REGISTRY.keys())

def create_encoder(encoder_type: str, **kwargs) -> Any:
    """
    Factory function to create a quantum encoder of the specified type.
    
    Args:
        encoder_type (str): Type of encoder to create ('amplitude', 'angle', 'basis', 'entanglement')
        **kwargs: Additional parameters to pass to the encoder constructor
            - n_qubits: Number of qubits to use
            - name: Name identifier for the encoder
            - Additional encoder-specific parameters
    
    Returns:
        An instance of the specified encoder type
        
    Raises:
        ValueError: If the specified encoder type is not available
    """
    encoder_type = encoder_type.lower()
    
    if encoder_type not in ENCODER_REGISTRY:
        available = ", ".join(get_available_encoders())
        raise ValueError(f"Encoder type '{encoder_type}' not available. Choose from: {available}")
    
    logger.info(f"Creating {encoder_type} encoder with parameters: {kwargs}")
    
    # Create and return the encoder instance
    return ENCODER_REGISTRY[encoder_type](**kwargs)

def register_encoder(name: str, encoder_class: Any) -> None:
    """
    Register a new encoder type in the factory.
    
    Args:
        name (str): Name for the encoder type
        encoder_class (Any): The encoder class to register
    """
    if name in ENCODER_REGISTRY:
        logger.warning(f"Overwriting existing encoder type: {name}")
    
    ENCODER_REGISTRY[name] = encoder_class
    logger.info(f"Registered new encoder type: {name}")

def create_encoder_from_config(config: Dict[str, Any]) -> Any:
    """
    Create an encoder from a configuration dictionary.
    
    Args:
        config: Dictionary with encoder configuration
        
    Returns:
        Configured encoder instance
        
    Raises:
        ValueError: If required configuration is missing or invalid
    """
    # Extract encoder type from config
    encoder_type = config.get('type')
    if not encoder_type:
        raise ValueError("Encoder type must be specified in configuration")
    
    # Remove 'type' key and pass remaining config as kwargs
    encoder_config = {k: v for k, v in config.items() if k != 'type'}
    
    return create_encoder(encoder_type, **encoder_config)

def get_encoder_info(encoder_type: str) -> Dict[str, Any]:
    """
    Get information about an encoder type.
    
    Args:
        encoder_type: Type of encoder to get info for
        
    Returns:
        Dictionary with encoder information
        
    Raises:
        ValueError: If encoder_type is not recognized
    """
    encoder_type = encoder_type.lower()
    
    if encoder_type not in ENCODER_REGISTRY:
        available_encoders = ', '.join(ENCODER_REGISTRY.keys())
        raise ValueError(f"Unknown encoder type '{encoder_type}'. Available types: {available_encoders}")
    
    # Get encoder class from registry
    encoder_class = ENCODER_REGISTRY[encoder_type]
    
    # Get docstring and other information
    info = {
        'name': encoder_type,
        'description': encoder_class.__doc__.strip().split('\n')[0] if encoder_class.__doc__ else '',
        'class': encoder_class.__name__,
        'parameters': {
            'n_qubits': 'Number of qubits to use for encoding'
        }
    }
    
    # Add encoder-specific parameters
    if encoder_type == 'amplitude':
        info['parameters']['padding_value'] = 'Value to use for padding'
    elif encoder_type == 'angle':
        info['parameters']['rotation_axis'] = 'Rotation axis (x, y, z, or all)'
        info['parameters']['repetitions'] = 'Number of repetition layers'
    
    return info 