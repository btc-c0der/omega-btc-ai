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

Privacy Analysis Script for Quantum Proof-of-Work (qPoW) implementation.

This script analyzes validator privacy risks by querying the validator privacy service,
generating detailed privacy reports and recommendations. It can be run as a standalone
tool or as part of a scheduled job in Kubernetes.

JAH BLESS SATOSHI
"""
import os
import sys
import json
import time
import argparse
import logging
import datetime
from typing import Dict, List, Any, Optional
import requests

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("privacy_analysis.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("privacy-analysis")

class PrivacyAnalyzer:
    """Analyzes validator privacy risks and generates reports."""
    
    def __init__(self, api_url: str, config_file: Optional[str] = None):
        """
        Initialize the privacy analyzer.
        
        Args:
            api_url: URL of the validator privacy service API
            config_file: Path to configuration file (optional)
        """
        self.api_url = api_url.rstrip('/')
        self.config = self._load_config(config_file)
        self.notification_endpoints = self.config.get("notification_endpoints", [])
        self.alert_threshold = self.config.get("alert_threshold", "MEDIUM")
        
        logger.info(f"Privacy Analyzer initialized with API URL: {api_url}")
    
    def _load_config(self, config_file: Optional[str]) -> Dict[str, Any]:
        """
        Load configuration from file or use defaults.
        
        Args:
            config_file: Path to configuration file
            
        Returns:
            Configuration dictionary
        """
        default_config = {
            "notification_endpoints": [],
            "alert_threshold": "MEDIUM",  # LOW, MEDIUM, HIGH, EXTREME
            "output_format": "json",
            "report_dir": "privacy_reports",
            "include_recommendations": True,
            "max_report_age_days": 30
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
    
    def fetch_validator_risks(self) -> List[Dict[str, Any]]:
        """
        Fetch privacy risk data from the validator privacy service.
        
        Returns:
            List of validator risk data
        """
        try:
            response = requests.get(f"{self.api_url}/privacy-risks")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching validator risks: {e}")
            return []
    
    def get_config_info(self) -> Dict[str, Any]:
        """
        Fetch configuration information from the validator privacy service.
        
        Returns:
            Configuration data
        """
        try:
            response = requests.get(f"{self.api_url}/config")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching configuration: {e}")
            return {}
    
    def get_server_stats(self) -> Dict[str, Any]:
        """
        Fetch server statistics from the validator privacy service.
        
        Returns:
            Server statistics
        """
        try:
            response = requests.get(f"{self.api_url}/stats")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching server stats: {e}")
            return {}
    
    def analyze(self) -> Dict[str, Any]:
        """
        Perform a complete privacy risk analysis.
        
        Returns:
            Analysis report
        """
        # Get current timestamp
        timestamp = datetime.datetime.now().isoformat()
        
        # Fetch data from the service
        risks = self.fetch_validator_risks()
        config = self.get_config_info()
        stats = self.get_server_stats()
        
        # Calculate summary statistics
        risk_levels = {
            "LOW": 0,
            "MEDIUM": 0,
            "HIGH": 0,
            "EXTREME": 0
        }
        
        high_risk_validators = []
        
        for validator in risks:
            threat_level = validator.get("threat_level", "LOW")
            risk_levels[threat_level] = risk_levels.get(threat_level, 0) + 1
            
            # Track high-risk validators for alerting
            if threat_level in ["HIGH", "EXTREME"]:
                high_risk_validators.append(validator)
        
        # Check if alerts should be sent
        send_alerts = False
        alert_levels = ["EXTREME", "HIGH", "MEDIUM", "LOW"]
        alert_index = alert_levels.index(self.alert_threshold)
        
        for level in alert_levels[:alert_index + 1]:
            if risk_levels.get(level, 0) > 0:
                send_alerts = True
                break
        
        # Compile full report
        report = {
            "timestamp": timestamp,
            "summary": {
                "total_validators": len(risks),
                "risk_levels": risk_levels,
                "privacy_mode": config.get("privacy_mode", "unknown"),
                "highest_risk": max(risk_levels.keys(), key=lambda k: risk_levels[k]) if risk_levels else "NONE"
            },
            "validators": risks,
            "config": config,
            "stats": stats
        }
        
        # Send alerts if needed
        if send_alerts and high_risk_validators and self.notification_endpoints:
            self.send_alerts(high_risk_validators)
        
        return report
    
    def send_alerts(self, high_risk_validators: List[Dict[str, Any]]) -> None:
        """
        Send alerts for high-risk validators.
        
        Args:
            high_risk_validators: List of high-risk validator data
        """
        if not self.notification_endpoints:
            logger.info("No notification endpoints configured, skipping alerts")
            return
        
        for endpoint in self.notification_endpoints:
            try:
                alert_data = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "alert_type": "validator_privacy_risk",
                    "severity": "high",
                    "details": f"High privacy risk detected for {len(high_risk_validators)} validators",
                    "validators": high_risk_validators
                }
                
                logger.info(f"Sending alert to {endpoint}")
                response = requests.post(
                    endpoint,
                    json=alert_data,
                    timeout=5
                )
                
                if response.status_code != 200:
                    logger.warning(f"Failed to send alert to {endpoint}: {response.status_code} {response.text}")
            except Exception as e:
                logger.error(f"Error sending alert to {endpoint}: {e}")
    
    def save_report(self, report: Dict[str, Any], output_file: Optional[str] = None) -> None:
        """
        Save the analysis report to a file.
        
        Args:
            report: The report to save
            output_file: Path to output file
        """
        if not output_file:
            # Generate a filename based on timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            report_dir = self.config.get("report_dir", "privacy_reports")
            
            # Create report directory if it doesn't exist
            os.makedirs(report_dir, exist_ok=True)
            
            output_file = os.path.join(report_dir, f"privacy_analysis_{timestamp}.json")
        
        try:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            logger.info(f"Saved privacy analysis report to {output_file}")
            
            # Clean up old reports
            self.cleanup_old_reports()
        except Exception as e:
            logger.error(f"Error saving report to {output_file}: {e}")
    
    def cleanup_old_reports(self) -> None:
        """Clean up old reports based on max_report_age_days configuration."""
        report_dir = self.config.get("report_dir", "privacy_reports")
        max_age_days = self.config.get("max_report_age_days", 30)
        
        if not os.path.exists(report_dir):
            return
        
        # Calculate cutoff time
        cutoff_time = time.time() - (max_age_days * 24 * 60 * 60)
        
        try:
            # Iterate over files in the report directory
            for filename in os.listdir(report_dir):
                if not filename.startswith("privacy_analysis_") or not filename.endswith(".json"):
                    continue
                
                filepath = os.path.join(report_dir, filename)
                file_time = os.path.getmtime(filepath)
                
                # Delete files older than cutoff_time
                if file_time < cutoff_time:
                    os.remove(filepath)
                    logger.info(f"Deleted old report: {filepath}")
        except Exception as e:
            logger.error(f"Error cleaning up old reports: {e}")
    
    def rotate_peers(self) -> bool:
        """
        Request peer rotation from the validator privacy service.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("Requesting peer rotation")
            response = requests.post(
                f"{self.api_url}/api/rotate-peers",
                json={"rotation_reason": "scheduled_analysis"}
            )
            response.raise_for_status()
            logger.info("Peer rotation successful")
            return True
        except Exception as e:
            logger.error(f"Error requesting peer rotation: {e}")
            return False

def main():
    """Main entry point for the privacy analysis script."""
    parser = argparse.ArgumentParser(description="Validator Privacy Analysis")
    parser.add_argument("--api-url", default="http://localhost:8082", help="URL of the validator privacy service API")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--output", help="Path to output file")
    parser.add_argument("--rotate-peers", action="store_true", help="Request peer rotation after analysis")
    args = parser.parse_args()
    
    # If OUTPUT_FILE env var is set (e.g., from Kubernetes), use it
    output_file = args.output
    if not output_file and "OUTPUT_FILE" in os.environ:
        output_file = os.environ["OUTPUT_FILE"]
    
    # Initialize analyzer
    analyzer = PrivacyAnalyzer(args.api_url, args.config)
    
    # Perform analysis
    report = analyzer.analyze()
    
    # Save report
    analyzer.save_report(report, output_file)
    
    # Rotate peers if requested
    if args.rotate_peers:
        analyzer.rotate_peers()

if __name__ == "__main__":
    main() 