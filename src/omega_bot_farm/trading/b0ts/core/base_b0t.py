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
Base B0t for Omega Bot Farm

This module provides the foundation for all bots in the Omega Bot Farm ecosystem.
It handles common functionality such as initialization, logging, state management, 
and environment loading.
"""

import os
import sys
import json
import logging
import random
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any, Union
from pathlib import Path

# Constants for terminal colors (for visual output)
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
BLUE = "\033[94m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RED_BG = "\033[41m"

# Divine constants for mathematical harmony
PHI = 1.618033988749895  # Golden Ratio - Divine Proportion
INVERSE_PHI = 0.618033988749895  # Inverse Golden Ratio
SCHUMANN_BASE = 7.83  # Earth's base frequency (Hz)
FIBONACCI_SEQUENCE = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]

class BaseB0t:
    """
    Base class for all bots in the Omega Bot Farm ecosystem.
    
    This class provides common functionality for all bots, including:
    - Initialization and configuration
    - Logging setup with different levels
    - State management (persistence, loading, updates)
    - Environment variable loading
    - Base randomization with seedable RNG
    """
    
    def __init__(self, 
                 name: Optional[str] = None,
                 log_level: str = "INFO",
                 seed: Optional[int] = None,
                 state_dir: Optional[str] = None):
        """
        Initialize the base bot with common functionality.
        
        Args:
            name: Bot name (defaults to class name if None)
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            seed: Random seed for reproducibility
            state_dir: Directory to store bot state files
        """
        # Basic bot identity
        self.name = name or self.__class__.__name__
        self.version = getattr(self, 'VERSION', '1.0.0')
        self.created_at = datetime.now()
        self.seed = seed
        
        # Setup logging
        self.logger = self._setup_logger(log_level)
        
        # State management
        self.state_dir = state_dir or os.path.join(os.getcwd(), 'states')
        self.state = {
            "created_at": self.created_at.isoformat(),
            "version": self.version,
            "name": self.name,
            "seed": self.seed,
            "last_updated": self.created_at.isoformat()
        }
        
        # Setup deterministic random
        self.random = random.Random(seed)
        
        # Load environment variables
        self._load_environment()
        
        # Mark as initialized
        self.initialized = True
        self.logger.info(f"{self.name} v{self.version} initialized at {self.created_at}")
    
    def _setup_logger(self, log_level: str) -> logging.Logger:
        """
        Set up logger for the bot.
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            
        Returns:
            Configured logger instance
        """
        logger_name = f"omega_bot_farm.{self.name}"
        logger = logging.getLogger(logger_name)
        
        # Only add handler if it doesn't already have one
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        # Set log level
        level = getattr(logging, log_level.upper(), logging.INFO)
        logger.setLevel(level)
        
        return logger
    
    def _load_environment(self) -> bool:
        """
        Load environment variables using env_loader if available.
        
        Returns:
            True if environment was loaded successfully, False otherwise
        """
        try:
            # Try import with full path to avoid relative import issues
            from src.omega_bot_farm.utils.env_loader import load_environment
            loaded = load_environment()
            if loaded:
                self.logger.info("Environment loaded successfully")
            else:
                self.logger.warning("No environment files found")
            return loaded
        except ImportError:
            self.logger.warning("Environment loader not available. Using default environment.")
            return False
    
    def update_state(self, updates: Dict[str, Any]) -> None:
        """
        Update bot state with new values.
        
        Args:
            updates: Dictionary of state updates to apply
        """
        self.state.update(updates)
        self.state["last_updated"] = datetime.now().isoformat()
    
    def get_state(self, key: str, default: Any = None) -> Any:
        """
        Get value from bot state.
        
        Args:
            key: State key to retrieve
            default: Default value if key doesn't exist
            
        Returns:
            The value for the specified key, or default if not found
        """
        return self.state.get(key, default)
    
    def get_full_state(self) -> Dict[str, Any]:
        """
        Get complete bot state.
        
        Returns:
            Dictionary containing full bot state
        """
        # Add runtime information
        uptime_seconds = (datetime.now() - self.created_at).total_seconds()
        
        return {
            **self.state,
            "uptime_seconds": uptime_seconds,
            "snapshot_time": datetime.now().isoformat()
        }
    
    def save_state(self, filename: Optional[str] = None) -> bool:
        """
        Save bot state to file.
        
        Args:
            filename: Custom filename (default: <botname>_state.json)
            
        Returns:
            True if successful, False otherwise
        """
        if not filename:
            filename = f"{self.name.lower()}_state.json"
            
        # Ensure state directory exists
        os.makedirs(self.state_dir, exist_ok=True)
        filepath = os.path.join(self.state_dir, filename)
            
        try:
            with open(filepath, 'w') as f:
                json.dump(self.get_full_state(), f, indent=2)
            self.logger.info(f"State saved to {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save state: {e}")
            return False
    
    def load_state(self, filename: Optional[str] = None) -> bool:
        """
        Load bot state from file.
        
        Args:
            filename: Custom filename (default: <botname>_state.json)
            
        Returns:
            True if successful, False otherwise
        """
        if not filename:
            filename = f"{self.name.lower()}_state.json"
            
        filepath = os.path.join(self.state_dir, filename)
            
        if not os.path.exists(filepath):
            self.logger.warning(f"State file {filepath} does not exist")
            return False
            
        try:
            with open(filepath, 'r') as f:
                loaded_state = json.load(f)
                # Only update the state dict, not the runtime attributes
                # that were set in __init__
                for key, value in loaded_state.items():
                    if key not in ["name", "version", "created_at"]:
                        self.state[key] = value
                        
            self.logger.info(f"State loaded from {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to load state: {e}")
            return False
    
    def get_version(self) -> str:
        """
        Get bot version.
        
        Returns:
            Bot version string
        """
        return self.version
    
    def get_name(self) -> str:
        """
        Get bot name.
        
        Returns:
            Bot name
        """
        return self.name
    
    def calculate_divine_proportion(self, value: float) -> Dict[str, float]:
        """
        Calculate golden ratio-based values from a base value.
        
        Args:
            value: Base value for calculations
            
        Returns:
            Dictionary with golden ratio-based values
        """
        return {
            "phi": value * PHI,
            "inverse_phi": value * INVERSE_PHI,
            "phi_squared": value * PHI * PHI,
            "phi_cubed": value * PHI * PHI * PHI,
            "phi_inverse_squared": value * INVERSE_PHI * INVERSE_PHI
        }
    
    def format_with_color(self, value: Union[float, str], is_positive_good: bool = True) -> str:
        """
        Format a value with color based on positivity.
        
        Args:
            value: Numeric value or string to format
            is_positive_good: Whether positive values should be green (True) or red (False)
            
        Returns:
            Color-formatted string
        """
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                return value
        
        if value > 0:
            color = GREEN if is_positive_good else RED
            return f"{color}{value:.2f}{RESET}"
        elif value < 0:
            color = RED if is_positive_good else GREEN
            return f"{color}{value:.2f}{RESET}"
        else:
            return f"{YELLOW}{value:.2f}{RESET}"

    def __str__(self) -> str:
        """
        String representation of the bot.
        
        Returns:
            String describing the bot
        """
        return f"{self.name} v{self.version}"
        
    def __repr__(self) -> str:
        """
        Detailed representation of the bot.
        
        Returns:
            Detailed string representation
        """
        return f"{self.__class__.__name__}(name='{self.name}', version='{self.version}')" 