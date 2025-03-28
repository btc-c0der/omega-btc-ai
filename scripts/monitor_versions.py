#!/usr/bin/env python3
"""
🔱 OMEGA BTC AI - Version Monitoring Script
📜 GPU²: General Public Universal + Graphics Processing Unison
🔐 Divine Copyright (c) 2025 - OMEGA Collective

This script monitors both BTC Live Feed v2 and v3 during the transition period,
ensuring data consistency and service health.
"""

import os
import sys
import time
import json
import requests
from datetime import datetime
from typing import Dict, Any
import logging
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Colors for divine output
class Colors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class VersionMonitor:
    def __init__(self, v2_url: str, v3_url: str, refresh_interval: int = 5):
        self.v2_url = v2_url
        self.v3_url = v3_url
        self.refresh_interval = refresh_interval
        self.console = Console()
        
    def get_health(self, url: str) -> Dict[str, Any]:
        """Get health status from a service endpoint."""
        try:
            response = requests.get(f"{url}/health", timeout=5)
            return response.json()
        except Exception as e:
            logger.error(f"Error getting health from {url}: {e}")
            return {"status": "error", "error": str(e)}
    
    def get_redis_status(self, url: str) -> Dict[str, Any]:
        """Get Redis status from a service endpoint."""
        try:
            response = requests.get(f"{url}/redis/status", timeout=5)
            return response.json()
        except Exception as e:
            logger.error(f"Error getting Redis status from {url}: {e}")
            return {"status": "error", "error": str(e)}
    
    def get_latest_price(self, url: str) -> Dict[str, Any]:
        """Get latest price from a service endpoint."""
        try:
            response = requests.get(f"{url}/price/latest", timeout=5)
            return response.json()
        except Exception as e:
            logger.error(f"Error getting latest price from {url}: {e}")
            return {"status": "error", "error": str(e)}
    
    def create_status_table(self, v2_data: Dict[str, Any], v3_data: Dict[str, Any]) -> Table:
        """Create a rich table with status information."""
        table = Table(title="BTC Live Feed Version Comparison")
        table.add_column("Metric", style="cyan")
        table.add_column("v2", style="blue")
        table.add_column("v3", style="green")
        
        # Health Status
        table.add_row(
            "Health",
            v2_data.get("health", {}).get("status", "unknown"),
            v3_data.get("health", {}).get("status", "unknown")
        )
        
        # Redis Status
        table.add_row(
            "Redis",
            v2_data.get("redis", {}).get("status", "unknown"),
            v3_data.get("redis", {}).get("status", "unknown")
        )
        
        # Latest Price
        v2_price = v2_data.get("price", {}).get("price", "unknown")
        v3_price = v3_data.get("price", {}).get("price", "unknown")
        table.add_row(
            "Latest Price",
            str(v2_price),
            str(v3_price)
        )
        
        # Price Difference
        if v2_price != "unknown" and v3_price != "unknown":
            diff = abs(float(v2_price) - float(v3_price))
            table.add_row(
                "Price Difference",
                f"{diff:.2f}",
                f"{diff:.2f}"
            )
        
        # Last Update
        table.add_row(
            "Last Update",
            v2_data.get("price", {}).get("timestamp", "unknown"),
            v3_data.get("price", {}).get("timestamp", "unknown")
        )
        
        return table
    
    def monitor(self):
        """Main monitoring loop."""
        self.console.print(Panel.fit(
            "[bold purple]🔱 OMEGA BTC AI - Version Monitoring[/bold purple]\n"
            "[blue]Monitoring BTC Live Feed v2 and v3 during transition[/blue]",
            title="Divine Monitor"
        ))
        
        with Live(self.create_status_table({}, {}), refresh_per_second=1) as live:
            while True:
                try:
                    # Get data from both versions
                    v2_data = {
                        "health": self.get_health(self.v2_url),
                        "redis": self.get_redis_status(self.v2_url),
                        "price": self.get_latest_price(self.v2_url)
                    }
                    
                    v3_data = {
                        "health": self.get_health(self.v3_url),
                        "redis": self.get_redis_status(self.v3_url),
                        "price": self.get_latest_price(self.v3_url)
                    }
                    
                    # Update the table
                    live.update(self.create_status_table(v2_data, v3_data))
                    
                    # Check for significant differences
                    if v2_data["price"].get("price") and v3_data["price"].get("price"):
                        diff = abs(float(v2_data["price"]["price"]) - float(v3_data["price"]["price"]))
                        if diff > 100:  # Alert if price difference is significant
                            logger.warning(f"Significant price difference detected: {diff}")
                    
                    time.sleep(self.refresh_interval)
                    
                except KeyboardInterrupt:
                    self.console.print("\n[yellow]Monitoring stopped by user[/yellow]")
                    break
                except Exception as e:
                    logger.error(f"Error in monitoring loop: {e}")
                    time.sleep(self.refresh_interval)

def main():
    """Main entry point."""
    # Get URLs from environment or use defaults
    v2_url = os.getenv("V2_URL", "https://btc-live-feed-v2.ondigitalocean.app")
    v3_url = os.getenv("V3_URL", "https://btc-live-feed-v3.ondigitalocean.app")
    refresh_interval = int(os.getenv("REFRESH_INTERVAL", "5"))
    
    monitor = VersionMonitor(v2_url, v3_url, refresh_interval)
    monitor.monitor()

if __name__ == "__main__":
    main() 