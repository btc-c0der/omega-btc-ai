#!/usr/bin/env python3
"""
Configuration Module for Core Divergence Predictor
=================================================

Provides configuration handling for the Core Divergence Predictor.
Includes default configurations and utility functions for loading/saving
configurations.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("divergence-predictor-config")

# Constants
CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")
DEFAULT_CONFIG_FILE = os.path.join(CONFIG_DIR, "default_config.json")


class DivergencePredictorConfig:
    """Configuration manager for Core Divergence Predictor."""
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """
        Get default configuration for the predictor.
        
        Returns:
            Dictionary with default configuration
        """
        current_time = datetime.now().isoformat()
        
        # Default configuration dictionary
        default_config = {
            "version": "1.0.0",
            "created_at": current_time,
            "updated_at": current_time,
            "description": "Default configuration for Core Divergence Predictor",
            
            # Data settings
            "data_path": "data/market_data",
            "data_file": "btc_market_data.csv",
            "use_synthetic_data": True,
            "target_column": "future_return",
            
            # Quantum encoding settings
            "quantum_encoding": {
                "encoder_type": "amplitude",
                "n_qubits": 8,
                "feature_subset": ["close", "volume", "rsi", "macd"],
                "normalization": "minmax",
                "use_feature_scaling": True
            },
            
            # Quantum neural network settings
            "quantum_neural_net": {
                "input_dim": 32,
                "output_dim": 1,
                "n_layers": 3,
                "n_filters": 4,
                "use_complex": True,
                "optimizer_params": {
                    "learning_rate": 0.001,
                    "beta_1": 0.9,
                    "beta_2": 0.999
                }
            },
            
            # Training settings
            "training": {
                "batch_size": 32,
                "epochs": 100,
                "validation_split": 0.2,
                "early_stopping": True,
                "patience": 10,
                "min_delta": 0.001
            },
            
            # Quantum RNG settings
            "quantum_rng": {
                "simulator_type": "statevector",
                "num_qubits": 6,
                "shots": 1024,
                "seed": 42
            },
            
            # Stochastic model settings
            "stochastic_model": {
                "model_type": "heston",
                "parameters": {
                    "mu": 0.1,
                    "sigma": 0.2,
                    "kappa": 1.0,
                    "theta": 0.04,
                    "epsilon": 0.3,
                    "rho": -0.7
                }
            },
            
            # Entanglement analysis settings
            "entanglement_analysis": {
                "window_size": 50,
                "overlap": 10,
                "entanglement_threshold": 0.4,
                "warning_threshold": 0.7,
                "critical_threshold": 0.85,
                "measure_type": "entanglement_witness"
            },
            
            # Simulator settings
            "simulator": {
                "simulator_qubits": 8,
                "shots": 1024,
                "noise_model": None
            },
            
            # Feature settings
            "features": {
                "price_features": ["open", "high", "low", "close"],
                "volume_features": ["volume"],
                "technical_features": ["rsi", "macd", "bollinger", "stochastic_k", "stochastic_d"],
                "calculate_missing": True,
                "lookback_window": 14
            },
            
            # Pipeline settings
            "pipeline": {
                "train_on_pipeline_run": True,
                "save_model": True,
                "save_predictions": True,
                "plot_results": False,
                "output_dir": "results"
            },
            
            # Logging settings
            "logging": {
                "level": "INFO",
                "file": "logs/divergence_predictor.log",
                "console": True,
                "log_metrics": True
            }
        }
        
        return default_config
    
    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        """
        Load configuration from file.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Configuration dictionary
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If config file has invalid JSON
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        return config
    
    @staticmethod
    def save_config(config: Dict[str, Any], config_path: str) -> bool:
        """
        Save configuration to file.
        
        Args:
            config: Configuration dictionary
            config_path: Path to save configuration
            
        Returns:
            Success flag
        """
        try:
            # Update the timestamp
            config["updated_at"] = datetime.now().isoformat()
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            # Write config to file
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
            
            logger.info(f"Configuration saved to {config_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False
    
    @staticmethod
    def create_default_config_file() -> bool:
        """
        Create default configuration file if it doesn't exist.
        
        Returns:
            Success flag
        """
        try:
            # Ensure config directory exists
            os.makedirs(CONFIG_DIR, exist_ok=True)
            
            # Check if default config file already exists
            if os.path.exists(DEFAULT_CONFIG_FILE):
                logger.info(f"Default configuration file already exists: {DEFAULT_CONFIG_FILE}")
                return True
            
            # Get default configuration
            default_config = DivergencePredictorConfig.get_default_config()
            
            # Save default configuration
            with open(DEFAULT_CONFIG_FILE, 'w') as f:
                json.dump(default_config, f, indent=4)
            
            logger.info(f"Created default configuration file: {DEFAULT_CONFIG_FILE}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating default configuration file: {e}")
            return False
    
    @staticmethod
    def merge_configs(base_config: Dict[str, Any], 
                     override_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge two configurations, with override_config taking precedence.
        
        Args:
            base_config: Base configuration
            override_config: Configuration to override base values
            
        Returns:
            Merged configuration
        """
        result = base_config.copy()
        
        # Recursively merge dictionaries
        def merge_dicts(d1, d2):
            for k, v in d2.items():
                if k in d1 and isinstance(d1[k], dict) and isinstance(v, dict):
                    merge_dicts(d1[k], v)
                else:
                    d1[k] = v
        
        merge_dicts(result, override_config)
        return result
    
    @staticmethod
    def validate_config(config: Dict[str, Any]) -> bool:
        """
        Validate configuration for required fields and value ranges.
        
        Args:
            config: Configuration to validate
            
        Returns:
            Validation result
        """
        # Check required top-level keys
        required_keys = ["version", "quantum_encoding", "quantum_neural_net", 
                         "quantum_rng", "entanglement_analysis"]
        
        for key in required_keys:
            if key not in config:
                logger.error(f"Missing required configuration key: {key}")
                return False
        
        # Validate n_qubits range (too many qubits would be impractical for simulation)
        if config.get("quantum_encoding", {}).get("n_qubits", 0) > 30:
            logger.error("n_qubits is too large (> 30), would be impractical for simulation")
            return False
        
        # Validate window size for entanglement analysis
        entanglement_config = config.get("entanglement_analysis", {})
        window_size = entanglement_config.get("window_size", 0)
        overlap = entanglement_config.get("overlap", 0)
        
        if window_size <= 0:
            logger.error("window_size must be positive")
            return False
        
        if overlap >= window_size:
            logger.error("overlap must be less than window_size")
            return False
        
        # All checks passed
        return True


# Create default config directory and file if they don't exist
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    logger.info(f"Created configuration directory: {CONFIG_DIR}")

# Create default config file if it doesn't exist
if not os.path.exists(DEFAULT_CONFIG_FILE):
    DivergencePredictorConfig.create_default_config_file() 