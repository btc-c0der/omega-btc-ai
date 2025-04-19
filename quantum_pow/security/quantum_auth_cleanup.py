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

Quantum Authentication Cleanup Script for Quantum Proof-of-Work (qPoW) implementation.

This script is designed to run as a scheduled task in Kubernetes, performing
regular maintenance tasks for the quantum-resistant authentication system:
- Cleaning up expired one-time tokens
- Pruning logs
- Performing basic security checks

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

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("quantum_auth_cleanup.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("quantum-auth-cleanup")

class QuantumAuthCleanup:
    """Performs maintenance tasks for the quantum authentication system."""
    
    def __init__(self, api_url: str, config_file: Optional[str] = None):
        """
        Initialize the cleanup utility.
        
        Args:
            api_url: URL of the quantum authentication API
            config_file: Path to configuration file (optional)
        """
        self.api_url = api_url.rstrip('/')
        self.config = self._load_config(config_file)
        self.log_retention_days = self.config.get("log_retention_days", 7)
        
        logger.info(f"Quantum Authentication Cleanup initialized with API URL: {api_url}")
    
    def _load_config(self, config_file: Optional[str]) -> Dict[str, Any]:
        """
        Load configuration from file or use defaults.
        
        Args:
            config_file: Path to configuration file
            
        Returns:
            Configuration dictionary
        """
        default_config = {
            "log_retention_days": 7,
            "token_cleanup_interval_hours": 1,
            "security_check_interval_hours": 12,
            "api_timeout_seconds": 10,
            "log_directory": "logs"
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
    
    def cleanup_tokens(self) -> bool:
        """
        Clean up expired tokens by calling the API endpoint.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("Starting token cleanup")
            
            # Call the API to clean up tokens
            response = requests.post(
                f"{self.api_url}/cleanup",
                timeout=self.config.get("api_timeout_seconds", 10)
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Cleaned up {result.get('deleted_count', 0)} expired tokens")
                return True
            else:
                logger.error(f"API error during token cleanup: {response.status_code} {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error during token cleanup: {e}")
            return False
    
    def prune_logs(self) -> int:
        """
        Remove log files older than the configured retention period.
        
        Returns:
            Number of log files deleted
        """
        log_dir = self.config.get("log_directory", "logs")
        
        if not os.path.exists(log_dir):
            logger.warning(f"Log directory {log_dir} does not exist")
            return 0
        
        # Calculate cutoff date
        cutoff_date = datetime.now() - timedelta(days=self.log_retention_days)
        deleted_count = 0
        
        try:
            # Iterate through log files
            for filename in os.listdir(log_dir):
                if not filename.endswith(".log"):
                    continue
                
                filepath = os.path.join(log_dir, filename)
                file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                
                # If file is older than retention period, delete it
                if file_modified < cutoff_date:
                    os.remove(filepath)
                    deleted_count += 1
                    logger.debug(f"Deleted old log file: {filepath}")
            
            if deleted_count > 0:
                logger.info(f"Pruned {deleted_count} log files older than {self.log_retention_days} days")
            
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error pruning logs: {e}")
            return 0
    
    def check_server_health(self) -> bool:
        """
        Check if the authentication server is healthy.
        
        Returns:
            True if the server is healthy, False otherwise
        """
        try:
            # Call the health endpoint
            response = requests.get(
                f"{self.api_url}/health",
                timeout=self.config.get("api_timeout_seconds", 10)
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "healthy":
                    logger.info("Authentication server is healthy")
                    return True
                else:
                    logger.warning(f"Authentication server reported unhealthy status: {result}")
                    return False
            else:
                logger.error(f"Health check failed with status code: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error checking server health: {e}")
            return False
    
    def run_full_maintenance(self) -> Dict[str, Any]:
        """
        Run all maintenance tasks.
        
        Returns:
            Dictionary with results of each task
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "token_cleanup": False,
            "log_pruning": 0,
            "server_health": False
        }
        
        # Check server health
        results["server_health"] = self.check_server_health()
        
        # If server is healthy, proceed with other tasks
        if results["server_health"]:
            # Clean up tokens
            results["token_cleanup"] = self.cleanup_tokens()
            
            # Prune logs
            results["log_pruning"] = self.prune_logs()
        
        # Log summary
        logger.info(f"Maintenance run completed: {json.dumps(results)}")
        
        return results

def main():
    """Main entry point for the quantum authentication cleanup script."""
    parser = argparse.ArgumentParser(description="Quantum Authentication Cleanup")
    parser.add_argument("--api-url", default="http://localhost:8083", help="URL of the authentication API")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--token-cleanup", action="store_true", help="Clean up expired tokens")
    parser.add_argument("--prune-logs", action="store_true", help="Prune old log files")
    parser.add_argument("--health-check", action="store_true", help="Check server health")
    parser.add_argument("--full-maintenance", action="store_true", help="Run all maintenance tasks")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    args = parser.parse_args()
    
    # Set log level
    logging.getLogger().setLevel(getattr(logging, args.log_level.upper()))
    
    # Create cleanup utility
    cleanup = QuantumAuthCleanup(args.api_url, args.config)
    
    # Determine which tasks to run
    if args.full_maintenance or (not any([args.token_cleanup, args.prune_logs, args.health_check])):
        # If --full-maintenance is specified or no specific task is requested, run all tasks
        cleanup.run_full_maintenance()
    else:
        # Otherwise, run requested tasks
        if args.health_check:
            cleanup.check_server_health()
        
        if args.token_cleanup:
            cleanup.cleanup_tokens()
        
        if args.prune_logs:
            cleanup.prune_logs()
    
    logger.info("Cleanup tasks completed")

if __name__ == "__main__":
    main() 