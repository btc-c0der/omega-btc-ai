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
🔱 OMEGA BTC AI - Redis Sync Verification Script
📜 GPU²: General Public Universal + Graphics Processing Unison
🔐 Divine Copyright (c) 2025 - OMEGA Collective

This script verifies data synchronization between BTC Live Feed v2 and v3 Redis instances,
ensuring data consistency during the transition period.
"""

import os
import sys
import time
import json
import redis
from datetime import datetime
from typing import Dict, Any, List, Union, Optional
import logging
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RedisSyncVerifier:
    def __init__(self, v2_redis: Dict[str, Union[str, int, bool]], v3_redis: Dict[str, Union[str, int, bool]]):
        self.v2_redis = redis.Redis(
            host=str(v2_redis["host"]),
            port=int(v2_redis["port"]),
            username=Optional[str](v2_redis.get("username")),
            password=Optional[str](v2_redis.get("password")),
            ssl=bool(v2_redis.get("ssl", False)),
            decode_responses=True
        )
        
        self.v3_redis = redis.Redis(
            host=str(v3_redis["host"]),
            port=int(v3_redis["port"]),
            username=Optional[str](v3_redis.get("username")),
            password=Optional[str](v3_redis.get("password")),
            ssl=bool(v3_redis.get("ssl", False)),
            decode_responses=True
        )
        
        self.console = Console()
        
    def verify_connection(self) -> bool:
        """Verify Redis connections."""
        try:
            self.v2_redis.ping()
            self.v3_redis.ping()
            return True
        except Exception as e:
            logger.error(f"Redis connection error: {e}")
            return False
    
    def get_key_types(self) -> Dict[str, Dict[str, str]]:
        """Get all key types from both Redis instances."""
        v2_keys: Dict[str, str] = {}
        v3_keys: Dict[str, str] = {}
        
        for key in self.v2_redis.keys("*"):
            v2_keys[key] = self.v2_redis.type(key).decode()
            
        for key in self.v3_redis.keys("*"):
            v3_keys[key] = self.v3_redis.type(key).decode()
            
        return {
            "v2": v2_keys,
            "v3": v3_keys
        }
    
    def compare_values(self, key: str, v2_type: str, v3_type: str) -> Dict[str, Any]:
        """Compare values for a specific key between v2 and v3."""
        result = {
            "key": key,
            "v2_type": v2_type,
            "v3_type": v3_type,
            "v2_exists": True,
            "v3_exists": True,
            "match": False,
            "details": {}
        }
        
        if v2_type != v3_type:
            result["match"] = False
            result["details"]["error"] = "Type mismatch"
            return result
            
        try:
            if v2_type == "string":
                v2_value = self.v2_redis.get(key)
                v3_value = self.v3_redis.get(key)
                result["match"] = v2_value == v3_value
                result["details"] = {
                    "v2_value": v2_value,
                    "v3_value": v3_value
                }
                
            elif v2_type == "hash":
                v2_value = self.v2_redis.hgetall(key)
                v3_value = self.v3_redis.hgetall(key)
                result["match"] = v2_value == v3_value
                result["details"] = {
                    "v2_value": v2_value,
                    "v3_value": v3_value
                }
                
            elif v2_type == "list":
                v2_value = self.v2_redis.lrange(key, 0, -1)
                v3_value = self.v3_redis.lrange(key, 0, -1)
                result["match"] = v2_value == v3_value
                result["details"] = {
                    "v2_value": v2_value,
                    "v3_value": v3_value
                }
                
            elif v2_type == "set":
                v2_value = self.v2_redis.smembers(key)
                v3_value = self.v3_redis.smembers(key)
                result["match"] = v2_value == v3_value
                result["details"] = {
                    "v2_value": v2_value,
                    "v3_value": v3_value
                }
                
            elif v2_type == "zset":
                v2_value = self.v2_redis.zrange(key, 0, -1, withscores=True)
                v3_value = self.v3_redis.zrange(key, 0, -1, withscores=True)
                result["match"] = v2_value == v3_value
                result["details"] = {
                    "v2_value": v2_value,
                    "v3_value": v3_value
                }
                
        except Exception as e:
            result["match"] = False
            result["details"]["error"] = str(e)
            
        return result
    
    def create_sync_table(self, results: List[Dict[str, Any]]) -> Table:
        """Create a rich table with sync verification results."""
        table = Table(title="Redis Sync Verification")
        table.add_column("Key", style="cyan")
        table.add_column("v2 Type", style="blue")
        table.add_column("v3 Type", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Details", style="white")
        
        for result in results:
            status_style = "green" if result["match"] else "red"
            table.add_row(
                result["key"],
                result["v2_type"],
                result["v3_type"],
                f"[{status_style}]{'✓' if result['match'] else '✗'}[/{status_style}]",
                str(result["details"])
            )
            
        return table
    
    def verify_sync(self):
        """Main verification process."""
        self.console.print(Panel.fit(
            "[bold purple]🔱 OMEGA BTC AI - Redis Sync Verification[/bold purple]\n"
            "[blue]Verifying data synchronization between v2 and v3[/blue]",
            title="Divine Verifier"
        ))
        
        if not self.verify_connection():
            self.console.print("[red]Failed to connect to Redis instances[/red]")
            return
            
        key_types = self.get_key_types()
        results = []
        
        # Compare all keys
        all_keys = set(key_types["v2"].keys()) | set(key_types["v3"].keys())
        
        for key in all_keys:
            v2_type = key_types["v2"].get(key, "none")
            v3_type = key_types["v3"].get(key, "none")
            
            result = self.compare_values(key, v2_type, v3_type)
            results.append(result)
            
        # Display results
        self.console.print(self.create_sync_table(results))
        
        # Summary
        total = len(results)
        matches = sum(1 for r in results if r["match"])
        self.console.print(f"\n[bold]Summary:[/bold] {matches}/{total} keys synchronized")

def main():
    """Main entry point."""
    # Get Redis configurations from environment
    v2_redis = {
        "host": os.getenv("V2_REDIS_HOST", "redis-19332.fcrce173.eu-west-1-1.ec2.redns.redis-cloud.com"),
        "port": int(os.getenv("V2_REDIS_PORT", "19332")),
        "username": os.getenv("V2_REDIS_USERNAME", "omega"),
        "password": os.getenv("V2_REDIS_PASSWORD", "VuKJU8Z.Z2V8Qn_"),
        "ssl": os.getenv("V2_REDIS_SSL", "true").lower() == "true"
    }
    
    v3_redis = {
        "host": os.getenv("V3_REDIS_HOST", "redis-19332.fcrce173.eu-west-1-1.ec2.redns.redis-cloud.com"),
        "port": int(os.getenv("V3_REDIS_PORT", "19332")),
        "username": os.getenv("V3_REDIS_USERNAME", "omega"),
        "password": os.getenv("V3_REDIS_PASSWORD", "VuKJU8Z.Z2V8Qn_"),
        "ssl": os.getenv("V3_REDIS_SSL", "true").lower() == "true"
    }
    
    verifier = RedisSyncVerifier(v2_redis, v3_redis)
    verifier.verify_sync()

if __name__ == "__main__":
    main() 