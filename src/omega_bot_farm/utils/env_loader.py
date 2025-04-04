#!/usr/bin/env python3

"""
Environment variable loader for Omega Bot Farm.

This module handles loading environment variables from both the root project .env file
and the bot farm's own .env file, with the bot farm's values taking precedence.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Optional, Any

# Set up logging
logger = logging.getLogger(__name__)

# Try to import dotenv
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    logger.warning("python-dotenv not installed. Will only use OS environment variables.")
    
    # Create a no-op load_dotenv function to avoid errors
    def load_dotenv(*args, **kwargs):
        return False


def get_project_root() -> Path:
    """Get the project root directory path.
    
    Returns:
        Path to the project root directory
    """
    # Assuming this file is in src/omega_bot_farm/utils/
    return Path(__file__).parent.parent.parent.parent


def load_bot_farm_env(override_existing: bool = True) -> Dict[str, str]:
    """Load environment variables for the bot farm.
    
    First loads from the root project .env, then from the bot farm's own .env,
    with the bot farm's variables taking precedence if override_existing is True.
    
    Args:
        override_existing: If True, bot farm's .env values override existing values
                          If False, existing values are kept
    
    Returns:
        Dictionary of loaded environment variables
    """
    loaded_vars = {}
    
    if not DOTENV_AVAILABLE:
        logger.warning("python-dotenv not available. Only using existing environment variables.")
        return loaded_vars
    
    # First load the root project .env
    root_env_path = get_project_root() / ".env"
    if root_env_path.exists():
        logger.info(f"Loading environment from root: {root_env_path}")
        load_dotenv(dotenv_path=root_env_path, override=override_existing)
        loaded_vars["root_env"] = str(root_env_path)
    
    # Then load the bot farm's .env
    bot_farm_env_path = get_project_root() / "src" / "omega_bot_farm" / ".env"
    if bot_farm_env_path.exists():
        logger.info(f"Loading environment from bot farm: {bot_farm_env_path}")
        load_dotenv(dotenv_path=bot_farm_env_path, override=override_existing)
        loaded_vars["bot_farm_env"] = str(bot_farm_env_path)
    
    return loaded_vars


def get_env_var(key: str, default: Optional[Any] = None) -> Any:
    """Get an environment variable with a default value.
    
    Args:
        key: The environment variable key
        default: Default value if key not found
    
    Returns:
        The environment variable value or default
    """
    return os.environ.get(key, default)


def get_bool_env_var(key: str, default: bool = False) -> bool:
    """Get a boolean environment variable.
    
    Args:
        key: The environment variable key
        default: Default value if key not found
    
    Returns:
        The environment variable as a boolean
    """
    value = os.environ.get(key, str(default)).lower()
    return value in ("true", "1", "t", "yes", "y")


def get_int_env_var(key: str, default: int = 0) -> int:
    """Get an integer environment variable.
    
    Args:
        key: The environment variable key
        default: Default value if key not found
    
    Returns:
        The environment variable as an integer
    """
    try:
        return int(os.environ.get(key, default))
    except (ValueError, TypeError):
        return default


def get_float_env_var(key: str, default: float = 0.0) -> float:
    """Get a float environment variable.
    
    Args:
        key: The environment variable key
        default: Default value if key not found
    
    Returns:
        The environment variable as a float
    """
    try:
        return float(os.environ.get(key, default))
    except (ValueError, TypeError):
        return default


# Automatically load environment when imported
loaded_env_files = load_bot_farm_env(override_existing=True)
if loaded_env_files:
    logger.info(f"Loaded environment variables from: {', '.join(loaded_env_files.values())}") 