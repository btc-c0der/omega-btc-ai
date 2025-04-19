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
"""

import os
import sys
import json
import time
import yaml
import logging
import subprocess
import datetime
from typing import Dict, List, Any, Optional, Union, Tuple
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("qpow_metrics_collector")

class MetricsCollector:
    """Collector for quantum-resistant security metrics from multiple sources."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the metrics collector with optional custom config.
        
        Args:
            config_path: Optional path to configuration file
        """
        self.config = self._load_config(config_path)
        self.metrics = {
            "timestamp": datetime.datetime.now().isoformat(),
            "collector_version": "1.0.0",
            "host_info": self._get_host_info()
        }
        self._prepare_output_dir()
    
    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        default_config = {
            "output_directory": "quantum_pow/metrics",
            "metrics_analyzer_config": None,
            "kubernetes_metrics_config": None,
            "collection_interval_seconds": 300,
            "max_stored_metrics_files": 100,
            "enable_kubernetes_metrics": True,
            "enable_test_metrics": True,
            "enable_performance_metrics": True,
            "enable_analyzer_metrics": True,
            "enable_system_metrics": True,
            "prometheus_integration": False,
            "prometheus_pushgateway": "http://localhost:9091"
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                        return {**default_config, **yaml.safe_load(f)}
                    else:
                        return {**default_config, **json.load(f)}
            except Exception as e:
                logger.error(f"Error loading config: {e}")
                
        return default_config
    
    def _prepare_output_dir(self) -> None:
        """Prepare the output directory for metrics files."""
        output_dir = Path(self.config["output_directory"])
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Clean up old metrics files if we're over the limit
        if self.config["max_stored_metrics_files"] > 0:
            metric_files = sorted(
                [f for f in output_dir.glob("metrics_*.json")],
                key=lambda f: f.stat().st_mtime
            )
            
            # Remove oldest files if we're over the limit
            if len(metric_files) > self.config["max_stored_metrics_files"]:
                files_to_remove = metric_files[:len(metric_files) - self.config["max_stored_metrics_files"]]
                for file in files_to_remove:
                    try:
                        file.unlink()
                        logger.debug(f"Removed old metrics file: {file}")
                    except Exception as e:
                        logger.warning(f"Failed to remove old metrics file {file}: {e}")
    
    def _get_host_info(self) -> Dict[str, Any]:
        """Collect basic information about the host system."""
        host_info = {
            "hostname": "",
            "platform": "",
            "architecture": "",
            "cpu_count": 0,
            "kernel_version": "",
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "kubernetes_node": ""
        }
        
        try:
            import platform
            host_info["hostname"] = platform.node()
            host_info["platform"] = platform.system()
            host_info["architecture"] = platform.machine()
            host_info["cpu_count"] = os.cpu_count() or 0
            host_info["kernel_version"] = platform.release()
            
            # Try to get Kubernetes node name from environment
            if "KUBERNETES_NODE_NAME" in os.environ:
                host_info["kubernetes_node"] = os.environ["KUBERNETES_NODE_NAME"]
            elif self.config["enable_kubernetes_metrics"]:
                # Try to get from kubectl
                try:
                    cmd = ["kubectl", "get", "nodes", "-o", "json"]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        nodes_data = json.loads(result.stdout)
                        if nodes_data.get("items") and len(nodes_data["items"]) > 0:
                            host_info["kubernetes_node"] = nodes_data["items"][0]["metadata"]["name"]
                except Exception:
                    pass
        except Exception as e:
            logger.warning(f"Error collecting host info: {e}")
            
        return host_info
    
    def collect_all_metrics(self) -> Dict[str, Any]:
        """Collect all metrics from available sources.
        
        Returns:
            Dictionary containing all collected metrics
        """
        logger.info("Starting collection of all quantum security metrics")
        collection_start = time.time()
        
        # Update timestamp
        self.metrics["timestamp"] = datetime.datetime.now().isoformat()
        
        # Collect metrics from each source
        if self.config["enable_analyzer_metrics"]:
            self._collect_analyzer_metrics()
            
        if self.config["enable_kubernetes_metrics"]:
            self._collect_kubernetes_metrics()
            
        if self.config["enable_system_metrics"]:
            self._collect_system_metrics()
            
        if self.config["enable_test_metrics"]:
            self._collect_test_metrics()
            
        if self.config["enable_performance_metrics"]:
            self._collect_performance_metrics()
        
        # Add collection metadata
        collection_time = time.time() - collection_start
        self.metrics["collection_info"] = {
            "duration_seconds": round(collection_time, 3),
            "collected_at": datetime.datetime.now().isoformat(),
            "enabled_sources": {
                "analyzer": self.config["enable_analyzer_metrics"],
                "kubernetes": self.config["enable_kubernetes_metrics"],
                "system": self.config["enable_system_metrics"],
                "tests": self.config["enable_test_metrics"],
                "performance": self.config["enable_performance_metrics"]
            }
        }
        
        logger.info(f"Metrics collection completed in {collection_time:.2f} seconds")
        return self.metrics
    
    def _collect_analyzer_metrics(self) -> None:
        """Collect metrics from the SecurityMetricsAnalyzer."""
        logger.info("Collecting metrics from SecurityMetricsAnalyzer")
        
        try:
            # Import the analyzer
            from security.metrics_analyzer import SecurityMetricsAnalyzer
            
            # Initialize with optional config
            analyzer = SecurityMetricsAnalyzer(self.config["metrics_analyzer_config"])
            
            # Run analysis
            analyzer_metrics = analyzer.analyze_all_metrics()
            
            # Merge metrics but don't overwrite our timestamp
            saved_timestamp = self.metrics["timestamp"]
            self.metrics.update(analyzer_metrics)
            self.metrics["timestamp"] = saved_timestamp
            
            logger.info("Successfully collected metrics from analyzer")
        except Exception as e:
            logger.error(f"Error collecting metrics from analyzer: {e}")
            self.metrics["analyzer_error"] = str(e)
    
    def _collect_kubernetes_metrics(self) -> None:
        """Collect metrics from Kubernetes integration."""
        logger.info("Collecting metrics from Kubernetes integration")
        
        try:
            # Import the k8s metrics integration
            from security.metrics.k8s_metrics_integration import KubernetesMetricsIntegration
            
            # Initialize with optional config
            k8s_metrics = KubernetesMetricsIntegration(
                namespace=self.config.get("kubernetes_namespace", "default"),
                config_path=self.config["kubernetes_metrics_config"]
            )
            
            # Collect metrics
            k8s_metrics_data = k8s_metrics.collect_all_metrics()
            
            # Add to our metrics
            self.metrics["kubernetes_metrics"] = k8s_metrics_data
            
            logger.info("Successfully collected metrics from Kubernetes")
        except Exception as e:
            logger.error(f"Error collecting metrics from Kubernetes: {e}")
            self.metrics["kubernetes_error"] = str(e)
    
    def _collect_system_metrics(self) -> None:
        """Collect system-level metrics relevant to quantum security."""
        logger.info("Collecting system metrics")
        
        system_metrics = {
            "timestamp": datetime.datetime.now().isoformat(),
            "cpu_usage": 0.0,
            "memory_usage": 0.0,
            "disk_usage": 0.0,
            "network_connections": 0,
            "entropy_available": 0,
            "processes_running": 0
        }
        
        try:
            # Try to use psutil for detailed system metrics
            import psutil
            
            # CPU metrics
            system_metrics["cpu_usage"] = psutil.cpu_percent(interval=1)
            system_metrics["cpu_count"] = psutil.cpu_count()
            
            # Memory metrics
            memory = psutil.virtual_memory()
            system_metrics["memory_usage"] = memory.percent
            system_metrics["memory_available_gb"] = memory.available / (1024 * 1024 * 1024)
            system_metrics["memory_total_gb"] = memory.total / (1024 * 1024 * 1024)
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            system_metrics["disk_usage"] = disk.percent
            system_metrics["disk_free_gb"] = disk.free / (1024 * 1024 * 1024)
            
            # Network connections
            system_metrics["network_connections"] = len(psutil.net_connections())
            
            # Process count
            system_metrics["processes_running"] = len(psutil.pids())
            
            # Entropy estimation - critical for security
            if os.path.exists('/proc/sys/kernel/random/entropy_avail'):
                with open('/proc/sys/kernel/random/entropy_avail', 'r') as f:
                    system_metrics["entropy_available"] = int(f.read().strip())
        except ImportError:
            logger.warning("psutil module not available, collecting limited system metrics")
            
            # Fallback to basic metrics using os module
            try:
                # Simple load average on Unix systems
                if hasattr(os, 'getloadavg'):
                    load_avg = os.getloadavg()
                    system_metrics["load_average_1min"] = load_avg[0]
                    system_metrics["load_average_5min"] = load_avg[1]
                    system_metrics["load_average_15min"] = load_avg[2]
                
                # Get disk usage for the current directory
                if hasattr(os, 'statvfs'):
                    stat = os.statvfs('.')
                    free = stat.f_bavail * stat.f_frsize
                    total = stat.f_blocks * stat.f_frsize
                    system_metrics["disk_free_gb"] = free / (1024 * 1024 * 1024)
                    system_metrics["disk_total_gb"] = total / (1024 * 1024 * 1024)
                    system_metrics["disk_usage"] = (1 - (free / total)) * 100
            except Exception as e:
                logger.warning(f"Error collecting fallback system metrics: {e}")
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
        
        # Add metrics to our collection
        self.metrics["system_metrics"] = system_metrics
    
    def _collect_test_metrics(self) -> None:
        """Collect metrics from test runs."""
        logger.info("Collecting test metrics")
        
        test_metrics = {
            "timestamp": datetime.datetime.now().isoformat(),
            "test_run_success": False,
            "tests_total": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "tests_skipped": 0,
            "test_coverage": 0.0,
            "categories": {}
        }
        
        try:
            # Run the test suite by importing the run_tests module
            sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
            import run_tests
            
            # Capture stdout to parse results
            import io
            from contextlib import redirect_stdout
            
            f = io.StringIO()
            with redirect_stdout(f):
                try:
                    run_tests.main()
                    test_metrics["test_run_success"] = True
                except SystemExit:
                    pass  # The test runner may exit with SystemExit
            
            output = f.getvalue()
            
            # Parse test output
            if "FAILED" in output:
                test_metrics["test_run_success"] = False
            
            # Extract test counts
            import re
            
            # Parse total tests
            total_match = re.search(r'Ran (\d+) tests? in', output)
            if total_match:
                test_metrics["tests_total"] = int(total_match.group(1))
            
            # Parse failures
            fail_match = re.search(r'FAILED \(failures=(\d+)', output)
            if fail_match:
                test_metrics["tests_failed"] = int(fail_match.group(1))
            
            # Parse skips
            skip_match = re.search(r'skipped=(\d+)', output)
            if skip_match:
                test_metrics["tests_skipped"] = int(skip_match.group(1))
            
            # Calculate passed tests
            test_metrics["tests_passed"] = (
                test_metrics["tests_total"] - 
                test_metrics["tests_failed"] - 
                test_metrics["tests_skipped"]
            )
            
            # Extract test categories
            categories = ["hash_functions", "block_structure", "mining", "quantum_authentication"]
            for category in categories:
                category_matches = re.findall(rf'test_{category}[\w_\.]+', output)
                test_metrics["categories"][category] = {
                    "total": len(category_matches),
                    "name": category
                }
            
            # Try to extract coverage if available
            coverage_match = re.search(r'TOTAL\s+\d+\s+\d+\s+(\d+)%', output)
            if coverage_match:
                test_metrics["test_coverage"] = float(coverage_match.group(1)) / 100
            
        except Exception as e:
            logger.error(f"Error collecting test metrics: {e}")
            test_metrics["test_error"] = str(e)
        
        # Add metrics to our collection
        self.metrics["test_metrics"] = test_metrics
    
    def _collect_performance_metrics(self) -> None:
        """Collect performance metrics for quantum-resistant operations."""
        logger.info("Collecting performance metrics")
        
        performance_metrics = {
            "timestamp": datetime.datetime.now().isoformat(),
            "hash_operations_per_second": 0,
            "signature_operations_per_second": 0,
            "mining_operations_per_second": 0,
            "verification_operations_per_second": 0,
            "relative_classical_performance": 0.0
        }
        
        try:
            # Import required modules
            from hash_functions import QuantumResistantHash
            import hashlib
            import time
            import random
            
            # Prepare test data
            test_data_samples = []
            for _ in range(1000):
                sample_size = random.randint(128, 4096)
                test_data_samples.append(bytes(random.getrandbits(8) for _ in range(sample_size)))
            
            # Measure quantum hash performance
            qr_hash = QuantumResistantHash()
            start_time = time.time()
            operations = 0
            
            # Run for at least 100ms to get a good sample
            while time.time() - start_time < 0.1:
                qr_hash.hash(test_data_samples[operations % len(test_data_samples)])
                operations += 1
            
            elapsed = time.time() - start_time
            performance_metrics["hash_operations_per_second"] = operations / elapsed
            
            # Measure classical hash performance
            start_time = time.time()
            classical_operations = 0
            
            # Run for the same number of operations
            while classical_operations < operations:
                hashlib.sha256(test_data_samples[classical_operations % len(test_data_samples)]).digest()
                classical_operations += 1
            
            classical_elapsed = time.time() - start_time
            classical_ops_per_second = classical_operations / classical_elapsed
            
            # Calculate relative performance (quantum / classical)
            performance_metrics["relative_classical_performance"] = (
                performance_metrics["hash_operations_per_second"] / classical_ops_per_second
            )
            
            # Try to measure mining performance if available
            try:
                import block_structure
                
                # Create a test block
                if hasattr(block_structure, 'QuantumBlock'):
                    # Setup for mining test
                    test_block = block_structure.QuantumBlock(
                        version=1,
                        prev_block_hash="0" * 64,
                        merkle_root="0" * 64,
                        timestamp=int(time.time()),
                        difficulty=1,  # Easy difficulty for testing
                        nonce=0
                    )
                    
                    # Measure mining performance
                    start_time = time.time()
                    mine_operations = 0
                    max_nonce = 10000  # Limit for testing
                    
                    # Try mining for a short time
                    while time.time() - start_time < 0.2 and mine_operations < max_nonce:
                        test_block.nonce = mine_operations
                        test_block.compute_hash()
                        mine_operations += 1
                    
                    mine_elapsed = time.time() - start_time
                    performance_metrics["mining_operations_per_second"] = mine_operations / mine_elapsed
            except Exception as e:
                logger.warning(f"Could not measure mining performance: {e}")
            
        except Exception as e:
            logger.error(f"Error collecting performance metrics: {e}")
            performance_metrics["performance_error"] = str(e)
        
        # Add metrics to our collection
        self.metrics["performance_metrics"] = performance_metrics
    
    def save_metrics(self, filepath: Optional[str] = None) -> str:
        """Save the collected metrics to a file.
        
        Args:
            filepath: Optional specific file path to save to
            
        Returns:
            Path to the saved metrics file
        """
        # If no filepath specified, generate one
        if not filepath:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = Path(self.config["output_directory"])
            filepath = output_dir / f"metrics_{timestamp}.json"
        
        # Save metrics to file
        try:
            with open(filepath, 'w') as f:
                json.dump(self.metrics, f, indent=2)
            logger.info(f"Saved metrics to {filepath}")
            
            # Also save to latest.json for easy access
            latest_path = Path(self.config["output_directory"]) / "metrics_latest.json"
            with open(latest_path, 'w') as f:
                json.dump(self.metrics, f, indent=2)
                
            return str(filepath)
        except Exception as e:
            logger.error(f"Error saving metrics to {filepath}: {e}")
            return ""
    
    def start_continuous_collection(self, interval: Optional[int] = None) -> None:
        """Start continuous collection of metrics at specified interval.
        
        Args:
            interval: Optional interval in seconds (overrides config)
        """
        interval = interval or self.config["collection_interval_seconds"]
        logger.info(f"Starting continuous metrics collection every {interval} seconds")
        
        try:
            while True:
                # Collect and save metrics
                self.collect_all_metrics()
                self.save_metrics()
                
                # Push to Prometheus if enabled
                if self.config["prometheus_integration"]:
                    self._push_to_prometheus()
                
                # Sleep until next collection
                logger.info(f"Sleeping for {interval} seconds until next collection")
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Continuous collection stopped by user")
        except Exception as e:
            logger.error(f"Error in continuous collection: {e}")
    
    def _push_to_prometheus(self) -> None:
        """Push metrics to Prometheus Pushgateway if configured."""
        if not self.config["prometheus_integration"]:
            return
            
        logger.info(f"Pushing metrics to Prometheus at {self.config['prometheus_pushgateway']}")
        
        try:
            from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
            
            registry = CollectorRegistry()
            
            # Create gauges for key metrics
            overall_score = Gauge('qpow_overall_quantum_resistance_score', 
                                'Overall quantum resistance score', 
                                registry=registry)
            
            hash_strength = Gauge('qpow_hash_resistance_score', 
                                 'Quantum resistance score for hash functions',
                                 registry=registry)
                                 
            auth_strength = Gauge('qpow_auth_security_score',
                                 'Security score for quantum authentication',
                                 registry=registry)
                                 
            privacy_score = Gauge('qpow_validator_privacy_score',
                                 'Privacy protection score for validators',
                                 registry=registry)
            
            test_coverage = Gauge('qpow_test_coverage_percentage',
                                 'Test coverage percentage',
                                 registry=registry)
            
            # Set gauge values from metrics
            overall_score.set(self.metrics.get("overall_score", 0))
            
            if "hash_metrics" in self.metrics:
                hash_strength.set(self.metrics["hash_metrics"].get("quantum_resistance_score", 0))
                
            if "auth_metrics" in self.metrics:
                auth_strength.set(self.metrics["auth_metrics"].get("scheme_count", 0) / 5)  # Normalize to 0-1
                
            if "privacy_metrics" in self.metrics:
                privacy_score.set(1 - self.metrics["privacy_metrics"].get("metadata_leakage_reduction", 0))
                
            if "test_metrics" in self.metrics:
                test_coverage.set(self.metrics["test_metrics"].get("test_coverage", 0))
            
            # Push to gateway
            push_to_gateway(
                self.config["prometheus_pushgateway"], 
                job='qpow_metrics', 
                registry=registry
            )
            
            logger.info("Successfully pushed metrics to Prometheus")
        except ImportError:
            logger.warning("prometheus_client module not available, skipping Prometheus integration")
        except Exception as e:
            logger.error(f"Error pushing metrics to Prometheus: {e}")

def main():
    """Main entry point for metrics collection."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Quantum Security Metrics Collector")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--output", help="Output directory for metrics files")
    parser.add_argument("--continuous", action="store_true", 
                       help="Run in continuous collection mode")
    parser.add_argument("--interval", type=int, 
                       help="Collection interval in seconds (for continuous mode)")
    parser.add_argument("--prometheus", action="store_true",
                       help="Enable Prometheus integration")
    parser.add_argument("--k8s-namespace", help="Kubernetes namespace for collection")
    
    args = parser.parse_args()
    
    # Initialize collector
    collector = MetricsCollector(args.config)
    
    # Override config settings from command line
    if args.output:
        collector.config["output_directory"] = args.output
    if args.prometheus:
        collector.config["prometheus_integration"] = True
    if args.k8s_namespace:
        collector.config["kubernetes_namespace"] = args.k8s_namespace
    
    # Run collection
    if args.continuous:
        collector.start_continuous_collection(args.interval)
    else:
        # Single collection run
        collector.collect_all_metrics()
        filepath = collector.save_metrics()
        if filepath:
            print(f"Metrics collected and saved to: {filepath}")

if __name__ == "__main__":
    main() 