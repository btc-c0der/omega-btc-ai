#!/usr/bin/env python3

"""
Divine Environment Loader

This module loads environment variables from .env files for the Omega Bots Bundle.
It supports multiple .env file locations and provides validation for required credentials.
"""

import os
import sys
import logging
from typing import Dict, List, Optional, Any, Set
from pathlib import Path
import re

# Check if dotenv is installed
try:
    from dotenv import load_dotenv
    HAVE_DOTENV = True
except ImportError:
    HAVE_DOTENV = False

logger = logging.getLogger("omega_bots_bundle.utils.env_loader")

class DivineEnvLoader:
    """Divine loader for environment variables from .env files."""
    
    def __init__(self, load_immediately: bool = True, verbose: bool = False):
        """Initialize the divine environment loader.
        
        Args:
            load_immediately: Whether to load environment variables immediately
            verbose: Whether to log detailed information
        """
        self.verbose = verbose
        self._loaded = False
        self._env_paths = []
        
        # Check for dotenv
        if not HAVE_DOTENV:
            logger.warning(
                "The python-dotenv package is not installed. "
                "Automatic .env loading will not be available. "
                "Install with: pip install python-dotenv"
            )
        
        if load_immediately and HAVE_DOTENV:
            self.load_environment()

    def load_environment(self) -> bool:
        """Load environment variables from various divine locations.
        
        Returns:
            bool: True if environment was loaded successfully
        """
        if not HAVE_DOTENV:
            logger.warning("Cannot load .env files without python-dotenv")
            return False
            
        # Store original environment state for validation later
        original_env_keys = set(os.environ.keys())
        
        # Look for .env files in divine locations
        env_paths = self._find_env_files()
        
        # Load each .env file in order
        loaded_any = False
        for env_path in env_paths:
            success = load_dotenv(env_path)
            if success:
                loaded_any = True
                if self.verbose:
                    logger.info(f"Loaded divine environment from {env_path}")
                self._env_paths.append(env_path)
        
        # Determine which keys were added
        new_env_keys = set(os.environ.keys()) - original_env_keys
        if self.verbose and new_env_keys:
            logger.info(f"Added {len(new_env_keys)} environment variables")
            
        self._loaded = loaded_any
        return loaded_any

    def _find_env_files(self) -> List[Path]:
        """Find .env files in various divine locations.
        
        Returns:
            List of paths to .env files, in order of precedence
        """
        env_paths = []
        
        # Current directory .env
        cwd_env = Path.cwd() / ".env"
        if cwd_env.exists():
            env_paths.append(cwd_env)
            
        # Project root .env (look for git root)
        try:
            project_root = self._find_project_root()
            if project_root and project_root != Path.cwd():
                project_env = project_root / ".env"
                if project_env.exists() and project_env not in env_paths:
                    env_paths.append(project_env)
        except Exception as e:
            if self.verbose:
                logger.warning(f"Error finding project root: {e}")
                
        # User home directory .env
        home_env = Path.home() / ".env"
        if home_env.exists() and home_env not in env_paths:
            env_paths.append(home_env)
            
        # Specific omega_bots paths
        module_dir = Path(__file__).parent.parent  # omega_bots_bundle dir
        omega_env = module_dir / ".env"
        if omega_env.exists() and omega_env not in env_paths:
            env_paths.append(omega_env)
            
        # omega_bot_farm .env
        farm_dir = module_dir.parent.parent / "omega_bot_farm"
        if farm_dir.exists():
            farm_env = farm_dir / ".env"
            if farm_env.exists() and farm_env not in env_paths:
                env_paths.append(farm_env)
        
        if self.verbose:
            logger.info(f"Found {len(env_paths)} divine .env files to load")
            
        return env_paths

    def _find_project_root(self) -> Optional[Path]:
        """Find the project root by looking for .git directory or other indicators.
        
        Returns:
            Path to project root, or None if not found
        """
        current = Path.cwd()
        
        # Look up to 10 levels for git directory
        for _ in range(10):
            # Check for .git directory (most common)
            if (current / ".git").exists():
                return current
                
            # Check for other common project indicators
            if (current / "pyproject.toml").exists() or (current / "setup.py").exists():
                return current
                
            # Move up one directory
            parent = current.parent
            if parent == current:  # Reached root
                break
            current = parent
            
        return None

    def validate_credentials(self, required_keys: Set[str]) -> bool:
        """Validate that required credentials are loaded in environment.
        
        Args:
            required_keys: Set of required environment variable names
            
        Returns:
            bool: True if all required credentials are present
        """
        missing_keys = required_keys - set(os.environ.keys())
        
        if missing_keys:
            logger.warning(
                f"Missing required credentials: {', '.join(sorted(missing_keys))}"
            )
            return False
            
        return True

    def validate_exchange_credentials(self, exchange: str = None) -> bool:
        """Validate that credentials for a specific exchange are loaded.
        
        Args:
            exchange: Exchange name (e.g., 'bitget', 'binance')
            
        Returns:
            bool: True if exchange credentials are present
        """
        if not exchange:
            # Check for any exchange credentials
            has_generic = self.validate_credentials({
                "EXCHANGE_API_KEY", "EXCHANGE_API_SECRET"
            })
            
            # Check for specific exchange credentials
            has_specific = any(
                all(f"{exch.upper()}_API_KEY" in os.environ and 
                    f"{exch.upper()}_SECRET_KEY" in os.environ)
                for exch in ["bitget", "binance", "bybit", "kucoin"]
            )
            
            return has_generic or has_specific
            
        # Check for specific exchange
        exchange = exchange.upper()
        if exchange == "BITGET":
            return self.validate_credentials({
                "BITGET_API_KEY", "BITGET_SECRET_KEY", "BITGET_PASSPHRASE"
            })
        elif exchange in ["BINANCE", "BYBIT", "KUCOIN"]:
            return self.validate_credentials({
                f"{exchange}_API_KEY", f"{exchange}_SECRET_KEY"
            })
        else:
            # For other exchanges, check generic credentials
            return self.validate_credentials({
                "EXCHANGE_API_KEY", "EXCHANGE_API_SECRET"
            })

    def generate_env_template(self, exchange: str = None) -> str:
        """Generate a template .env file with required credentials.
        
        Args:
            exchange: Exchange name to generate credentials for
            
        Returns:
            str: Template .env file content
        """
        template = [
            "# Divine Omega Bots Bundle - Environment Configuration",
            "# Generated by DivineEnvLoader",
            "",
            "# === Exchange Credentials ===",
        ]
        
        if not exchange or exchange.lower() == "bitget":
            template.extend([
                "",
                "# Bitget Exchange",
                "BITGET_API_KEY=your_api_key_here",
                "BITGET_SECRET_KEY=your_secret_key_here",
                "BITGET_PASSPHRASE=your_passphrase_here",
                "# BITGET_API_URL=https://api.bitget.com  # Optional custom API URL"
            ])
            
        if not exchange or exchange.lower() == "binance":
            template.extend([
                "",
                "# Binance Exchange",
                "BINANCE_API_KEY=your_api_key_here",
                "BINANCE_SECRET_KEY=your_secret_key_here",
            ])
            
        template.extend([
            "",
            "# Generic Exchange (for others)",
            "EXCHANGE_API_KEY=your_api_key_here",
            "EXCHANGE_API_SECRET=your_secret_key_here",
            "EXCHANGE_API_PASSPHRASE=your_passphrase_here  # If required",
            "",
            "# === Trading Parameters ===",
            "",
            "# Symbol to trade",
            "SYMBOL=BTCUSDT",
            "TRADING_SYMBOL=BTCUSDT_UMCBL  # Exchange-specific format (e.g., Bitget)",
            "",
            "# Initial capital and position sizing",
            "INITIAL_CAPITAL=24.0",
            "POSITION_SIZE_PERCENT=1.0",
            "",
            "# Risk management",
            "MAX_LEVERAGE=20",
            "STOP_LOSS_PERCENT=1.0",
            "TAKE_PROFIT_MULTIPLIER=2.0",
            "",
            "# === Environment Settings ===",
            "",
            "# Use testnet/sandbox mode (true/false)",
            "USE_TESTNET=true",
            "",
            "# === Logging & Monitoring ===",
            "",
            "LOG_LEVEL=INFO",
            "",
            "# === Divine Configuration ===",
            "",
            "# GBU2 Consciousness Level (8-10)",
            "CONSCIOUSNESS_LEVEL=8"
        ])
        
        return "\n".join(template)

    def save_env_template(self, path: str = ".env.example", exchange: str = None) -> bool:
        """Save a template .env file.
        
        Args:
            path: Path to save the template file
            exchange: Exchange name to generate credentials for
            
        Returns:
            bool: True if template was saved successfully
        """
        try:
            template = self.generate_env_template(exchange)
            with open(path, "w") as f:
                f.write(template)
            
            if self.verbose:
                logger.info(f"Saved divine environment template to {path}")
            return True
        except Exception as e:
            logger.error(f"Error saving environment template: {e}")
            return False


# Global instance for easy access
divine_env = DivineEnvLoader(verbose=False)


def load_environment(verbose: bool = False) -> bool:
    """Load environment variables from .env files.
    
    This is a convenience function to load environment variables.
    
    Args:
        verbose: Whether to log detailed information
        
    Returns:
        bool: True if environment was loaded successfully
    """
    global divine_env
    divine_env.verbose = verbose
    return divine_env.load_environment()


def validate_exchange_credentials(exchange: str = None, verbose: bool = False) -> bool:
    """Validate that credentials for a specific exchange are loaded.
    
    Args:
        exchange: Exchange name (e.g., 'bitget', 'binance') 
        verbose: Whether to log detailed information
        
    Returns:
        bool: True if exchange credentials are present
    """
    global divine_env
    divine_env.verbose = verbose
    return divine_env.validate_exchange_credentials(exchange)


def generate_env_template(exchange: str = None) -> str:
    """Generate a template .env file with required credentials.
    
    Args:
        exchange: Exchange name to generate credentials for
        
    Returns:
        str: Template .env file content
    """
    global divine_env
    return divine_env.generate_env_template(exchange)


if __name__ == "__main__":
    # When run as script, generate template .env file
    logging.basicConfig(level=logging.INFO)
    loader = DivineEnvLoader(verbose=True)
    
    if len(sys.argv) > 1:
        exchange = sys.argv[1]
        output_file = f".env.{exchange.lower()}.example"
    else:
        exchange = None
        output_file = ".env.example"
        
    loader.save_env_template(output_file, exchange)
    print(f"Generated divine .env template at {output_file}")
    
    # Check if environment is loaded
    loader.load_environment()
    
    if exchange:
        has_creds = loader.validate_exchange_credentials(exchange)
        if has_creds:
            print(f"✅ Divine credentials for {exchange.upper()} are configured!")
        else:
            print(f"❌ Divine credentials for {exchange.upper()} are missing.")
    else:
        has_any_creds = loader.validate_exchange_credentials()
        if has_any_creds:
            print("✅ Divine exchange credentials are configured!")
        else:
            print("❌ No divine exchange credentials found.")
            print(f"Please edit {output_file} and rename to .env to configure credentials.") 