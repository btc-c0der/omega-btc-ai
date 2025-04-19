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

Quantum Authentication Key Rotation Script for Quantum Proof-of-Work (qPoW) implementation.

This script is designed to run as a scheduled task in Kubernetes, performing
regular key rotation for the quantum-resistant authentication system to ensure
ongoing security against quantum computing attacks. It manages both scheduled
rotations and can be triggered for emergency rotations as well.

JAH BLESS SATOSHI
"""
import os
import sys
import json
import time
import logging
import argparse
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
import random

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("quantum_auth_rotation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("quantum-auth-rotation")

class QuantumAuthRotation:
    """Performs key rotation for the quantum authentication system."""
    
    def __init__(self, api_url: str, config_file: Optional[str] = None):
        """
        Initialize the key rotation utility.
        
        Args:
            api_url: URL of the quantum authentication API
            config_file: Path to configuration file (optional)
        """
        self.api_url = api_url.rstrip('/')
        self.config = self._load_config(config_file)
        self.rotation_interval_days = self.config.get("rotation_interval_days", 7)
        self.rotation_file = self.config.get("rotation_record_file", "rotation_history.json")
        
        logger.info(f"Quantum Authentication Key Rotation initialized with API URL: {api_url}")
    
    def _load_config(self, config_file: Optional[str]) -> Dict[str, Any]:
        """
        Load configuration from file or use defaults.
        
        Args:
            config_file: Path to configuration file
            
        Returns:
            Configuration dictionary
        """
        default_config = {
            "rotation_interval_days": 7,
            "rotation_jitter_hours": 6,     # Add randomness to rotation time
            "rotation_record_file": "rotation_history.json",
            "api_timeout_seconds": 10,
            "validator_batch_size": 10,     # Number of validators to rotate in one batch
            "emergency_cooldown_hours": 24  # Cooldown period after emergency rotation
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
                        default_config[key] = value
                logger.info(f"Loaded configuration from {config_file}")
        except Exception as e:
            logger.error(f"Error loading configuration from {config_file}: {e}")
        
        return default_config
    
    def _load_rotation_history(self) -> Dict[str, Any]:
        """
        Load rotation history from file.
        
        Returns:
            Dictionary with rotation history
        """
        default_history = {
            "last_rotation": 0,           # Timestamp of last rotation
            "emergency_rotations": [],    # List of emergency rotation timestamps
            "scheduled_rotations": [],    # List of scheduled rotation timestamps
            "validator_last_rotation": {}  # Dict of validator_id -> last rotation timestamp
        }
        
        if not os.path.exists(self.rotation_file):
            return default_history
        
        try:
            with open(self.rotation_file, 'r') as f:
                history = json.load(f)
                return history
        except Exception as e:
            logger.error(f"Error loading rotation history: {e}")
            return default_history
    
    def _save_rotation_history(self, history: Dict[str, Any]) -> bool:
        """
        Save rotation history to file.
        
        Args:
            history: Rotation history dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.rotation_file, 'w') as f:
                json.dump(history, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving rotation history: {e}")
            return False
    
    def get_server_stats(self) -> Dict[str, Any]:
        """
        Get server statistics to determine which validators need rotation.
        
        Returns:
            Server statistics dictionary or empty dict if failed
        """
        try:
            # Call the stats endpoint
            response = requests.get(
                f"{self.api_url}/stats",
                timeout=self.config.get("api_timeout_seconds", 10)
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error getting server stats: {response.status_code} {response.text}")
                return {}
                
        except Exception as e:
            logger.error(f"Error getting server stats: {e}")
            return {}
    
    def rotate_keys(self, reason: str = "scheduled", validator_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Rotate keys by calling the API endpoint.
        
        Args:
            reason: Reason for key rotation (scheduled, emergency, or manual)
            validator_id: Optional validator ID to rotate keys for (if None, rotate all)
            
        Returns:
            Dictionary with rotation results
        """
        try:
            logger.info(f"Starting key rotation: reason={reason}, validator={validator_id or 'all'}")
            
            # Prepare request data
            data = {
                "reason": reason
            }
            if validator_id:
                data["validator_id"] = validator_id
            
            # Call the API to rotate keys
            response = requests.post(
                f"{self.api_url}/keys/rotate",
                json=data,
                timeout=self.config.get("api_timeout_seconds", 10)
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Update rotation history
                history = self._load_rotation_history()
                history["last_rotation"] = time.time()
                
                # Add to appropriate history list
                if reason == "emergency":
                    history["emergency_rotations"].append(time.time())
                    # Keep only the last 10 emergency rotations
                    history["emergency_rotations"] = history["emergency_rotations"][-10:]
                elif reason == "scheduled":
                    history["scheduled_rotations"].append(time.time())
                    # Keep only the last 50 scheduled rotations
                    history["scheduled_rotations"] = history["scheduled_rotations"][-50:]
                
                # Update validator-specific rotation time
                if validator_id:
                    history["validator_last_rotation"][validator_id] = time.time()
                
                # Save updated history
                self._save_rotation_history(history)
                
                # Log rotation results
                rotated_count = sum(result.get("rotated_keys", {}).values())
                logger.info(f"Rotated {rotated_count} keys: {result.get('rotated_keys', {})}")
                
                return result
            else:
                logger.error(f"API error during key rotation: {response.status_code} {response.text}")
                return {"error": f"API error: {response.status_code}", "rotated_keys": {}}
                
        except Exception as e:
            logger.error(f"Error during key rotation: {e}")
            return {"error": str(e), "rotated_keys": {}}
    
    def should_rotate(self) -> bool:
        """
        Determine if keys need rotation based on rotation history.
        
        Returns:
            True if keys should be rotated, False otherwise
        """
        history = self._load_rotation_history()
        last_rotation = history["last_rotation"]
        
        # If no rotation has ever been performed, do it now
        if last_rotation == 0:
            return True
        
        # Calculate the rotation interval with jitter
        jitter_hours = self.config.get("rotation_jitter_hours", 6)
        jitter_seconds = random.uniform(-jitter_hours * 3600, jitter_hours * 3600)
        rotation_seconds = self.rotation_interval_days * 24 * 3600 + jitter_seconds
        
        # Check if it's time for rotation
        time_since_last = time.time() - last_rotation
        should_rotate = time_since_last >= rotation_seconds
        
        if should_rotate:
            logger.info(f"Time for scheduled rotation (last was {time_since_last/3600:.1f} hours ago)")
        else:
            logger.info(f"No rotation needed yet (last was {time_since_last/3600:.1f} hours ago)")
        
        return should_rotate
    
    def can_emergency_rotate(self) -> bool:
        """
        Check if emergency rotation is allowed based on cooldown period.
        
        Returns:
            True if emergency rotation is allowed, False otherwise
        """
        history = self._load_rotation_history()
        
        # If no emergency rotations have been performed, allow it
        if not history["emergency_rotations"]:
            return True
        
        # Get last emergency rotation time
        last_emergency = max(history["emergency_rotations"])
        
        # Check if cooldown period has elapsed
        cooldown_seconds = self.config.get("emergency_cooldown_hours", 24) * 3600
        time_since_last = time.time() - last_emergency
        
        can_rotate = time_since_last >= cooldown_seconds
        
        if not can_rotate:
            logger.warning(f"Emergency rotation not allowed yet (cooldown: {time_since_last/3600:.1f}/{cooldown_seconds/3600:.1f} hours)")
        
        return can_rotate
    
    def find_validators_for_rotation(self) -> List[str]:
        """
        Find validators that need key rotation based on last rotation time.
        
        Returns:
            List of validator IDs that need rotation
        """
        # Get the list of validators from server stats or API
        # For now, we'll just use the history to determine which validators to rotate
        
        history = self._load_rotation_history()
        validator_rotations = history.get("validator_last_rotation", {})
        
        # Calculate the rotation interval
        rotation_seconds = self.rotation_interval_days * 24 * 3600
        current_time = time.time()
        
        # Find validators that need rotation
        validators_to_rotate = []
        for validator_id, last_rotation in validator_rotations.items():
            if current_time - last_rotation >= rotation_seconds:
                validators_to_rotate.append(validator_id)
        
        # Limit to batch size
        batch_size = self.config.get("validator_batch_size", 10)
        return validators_to_rotate[:batch_size]
    
    def run_scheduled_rotation(self) -> Dict[str, Any]:
        """
        Run scheduled key rotation if needed.
        
        Returns:
            Dictionary with rotation results
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "rotation_needed": False,
            "rotation_performed": False,
            "rotation_results": {}
        }
        
        # Check if rotation is needed
        if not self.should_rotate():
            return results
        
        results["rotation_needed"] = True
        
        # Find validators to rotate
        validators = self.find_validators_for_rotation()
        
        # If specific validators need rotation, rotate them one by one
        if validators:
            combined_results = {"rotated_keys": {}}
            for validator_id in validators:
                validator_result = self.rotate_keys("scheduled", validator_id)
                # Merge the results
                if "rotated_keys" in validator_result:
                    for scheme, count in validator_result["rotated_keys"].items():
                        if scheme in combined_results["rotated_keys"]:
                            combined_results["rotated_keys"][scheme] += count
                        else:
                            combined_results["rotated_keys"][scheme] = count
            
            results["rotation_results"] = combined_results
        else:
            # Otherwise, rotate all keys
            results["rotation_results"] = self.rotate_keys("scheduled")
        
        results["rotation_performed"] = True
        
        # Log summary
        logger.info(f"Scheduled rotation completed: {json.dumps(results)}")
        
        return results
    
    def run_emergency_rotation(self) -> Dict[str, Any]:
        """
        Run emergency key rotation.
        
        Returns:
            Dictionary with rotation results
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "allowed": False,
            "rotation_performed": False,
            "rotation_results": {}
        }
        
        # Check if emergency rotation is allowed
        if not self.can_emergency_rotate():
            return results
        
        results["allowed"] = True
        
        # Perform emergency rotation
        results["rotation_results"] = self.rotate_keys("emergency")
        results["rotation_performed"] = True
        
        # Log summary
        logger.warning(f"Emergency rotation completed: {json.dumps(results)}")
        
        return results

def main():
    """Main entry point for the quantum authentication key rotation script."""
    parser = argparse.ArgumentParser(description="Quantum Authentication Key Rotation")
    parser.add_argument("--api-url", default="http://localhost:8083", help="URL of the authentication API")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--scheduled-rotation", action="store_true", help="Run scheduled key rotation")
    parser.add_argument("--emergency-rotation", action="store_true", help="Run emergency key rotation")
    parser.add_argument("--validator", help="Rotate keys for a specific validator")
    parser.add_argument("--reason", default="manual", help="Reason for key rotation")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    args = parser.parse_args()
    
    # Set log level
    logging.getLogger().setLevel(getattr(logging, args.log_level.upper()))
    
    # Create rotation utility
    rotation = QuantumAuthRotation(args.api_url, args.config)
    
    # Determine which operation to run
    if args.emergency_rotation:
        rotation.run_emergency_rotation()
    elif args.scheduled_rotation:
        rotation.run_scheduled_rotation()
    elif args.validator:
        # Rotate keys for a specific validator
        rotation.rotate_keys(args.reason, args.validator)
    else:
        # Default behavior: check if rotation is needed and perform if necessary
        rotation.run_scheduled_rotation()
    
    logger.info("Key rotation tasks completed")

if __name__ == "__main__":
    main() 