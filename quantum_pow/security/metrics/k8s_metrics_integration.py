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
import yaml
import time
import logging
import subprocess
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("k8s_metrics_integration")

class KubernetesMetricsIntegration:
    """Kubernetes integration for quantum security metrics collection."""
    
    def __init__(self, namespace: str = "default", config_path: Optional[str] = None):
        """Initialize the Kubernetes metrics integration.
        
        Args:
            namespace: Kubernetes namespace to scan for qPoW services
            config_path: Optional path to config file
        """
        self.namespace = namespace
        self.config = self._load_config(config_path)
        self.service_metrics = {}
        self.deployment_metrics = {}
        self.cronjob_metrics = {}
        self.discovered_services = []
        
    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        default_config = {
            "service_label_selector": "app=quantum",
            "metrics_endpoint": "/metrics",
            "metrics_port": 8080,
            "poll_interval_seconds": 60,
            "metrics_output_path": "quantum_pow/metrics/k8s",
            "auto_discovery": True,
            "qpow_services": ["quantum-auth", "validator-privacy", "csrf-monitor"]
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
    
    def discover_services(self) -> List[str]:
        """Discover qPoW services in the Kubernetes cluster."""
        logger.info(f"Discovering qPoW services in namespace {self.namespace}")
        
        try:
            # Get services matching the label selector
            cmd = [
                "kubectl", "get", "services", 
                "-n", self.namespace, 
                "-l", self.config["service_label_selector"],
                "-o", "json"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"Error discovering services: {result.stderr}")
                # Fall back to configured services
                return self.config["qpow_services"]
            
            # Parse the services
            services_data = json.loads(result.stdout)
            services = []
            
            for item in services_data.get("items", []):
                service_name = item.get("metadata", {}).get("name")
                if service_name:
                    services.append(service_name)
            
            logger.info(f"Discovered services: {services}")
            self.discovered_services = services
            return services
            
        except Exception as e:
            logger.error(f"Error during service discovery: {e}")
            # Fall back to configured services
            return self.config["qpow_services"]
    
    def collect_deployment_metrics(self, service_name: str) -> Dict[str, Any]:
        """Collect metrics about a specific deployment.
        
        Args:
            service_name: Name of the service/deployment
            
        Returns:
            Dictionary containing deployment metrics
        """
        logger.info(f"Collecting deployment metrics for {service_name}")
        metrics = {
            "name": service_name,
            "replicas": 0,
            "available_replicas": 0,
            "ready_percentage": 0,
            "restart_count": 0,
            "status": "unknown",
            "containers": [],
            "last_updated": time.time()
        }
        
        try:
            # Get deployment details
            deployment_cmd = [
                "kubectl", "get", "deployment", service_name,
                "-n", self.namespace, "-o", "json"
            ]
            result = subprocess.run(deployment_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.warning(f"Deployment {service_name} not found: {result.stderr}")
                metrics["status"] = "not found"
                return metrics
            
            deployment_data = json.loads(result.stdout)
            
            # Extract basic deployment metrics
            metrics["replicas"] = deployment_data.get("spec", {}).get("replicas", 0)
            metrics["available_replicas"] = deployment_data.get("status", {}).get("availableReplicas", 0)
            
            if metrics["replicas"] > 0:
                metrics["ready_percentage"] = (metrics["available_replicas"] / metrics["replicas"]) * 100
            
            metrics["status"] = "running" if metrics["available_replicas"] > 0 else "not ready"
            
            # Get container information from the pods
            pod_cmd = [
                "kubectl", "get", "pods",
                "-n", self.namespace,
                "-l", f"app={service_name}",
                "-o", "json"
            ]
            pod_result = subprocess.run(pod_cmd, capture_output=True, text=True)
            
            if pod_result.returncode == 0:
                pod_data = json.loads(pod_result.stdout)
                total_restarts = 0
                
                for pod in pod_data.get("items", []):
                    for container_status in pod.get("status", {}).get("containerStatuses", []):
                        container_name = container_status.get("name", "unknown")
                        restarts = container_status.get("restartCount", 0)
                        ready = container_status.get("ready", False)
                        
                        metrics["containers"].append({
                            "name": container_name,
                            "ready": ready,
                            "restarts": restarts,
                            "image": container_status.get("image", "unknown")
                        })
                        
                        total_restarts += restarts
                
                metrics["restart_count"] = total_restarts
        
        except Exception as e:
            logger.error(f"Error collecting deployment metrics for {service_name}: {e}")
            metrics["status"] = "error"
            
        return metrics
    
    def collect_service_metrics(self, service_name: str) -> Dict[str, Any]:
        """Collect service-specific security metrics via port-forwarding to metrics endpoint.
        
        Args:
            service_name: Name of the service
            
        Returns:
            Dictionary containing service-specific metrics
        """
        logger.info(f"Collecting service metrics for {service_name}")
        
        metrics = {
            "name": service_name,
            "security_metrics": {},
            "health": "unknown",
            "latency_ms": 0,
            "last_updated": time.time()
        }
        
        # First, check if the service exists
        try:
            service_cmd = [
                "kubectl", "get", "service", service_name,
                "-n", self.namespace
            ]
            result = subprocess.run(service_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.warning(f"Service {service_name} not found")
                metrics["health"] = "not found"
                return metrics
                
            # Set up port forwarding to the metrics endpoint
            metrics_port = self.config["metrics_port"]
            local_port = self._find_available_port(8000, 9000)
            
            if not local_port:
                logger.error("Failed to find an available local port")
                metrics["health"] = "port_error"
                return metrics
                
            # Start port forwarding in the background
            port_forward_cmd = [
                "kubectl", "port-forward", 
                f"service/{service_name}", 
                f"{local_port}:{metrics_port}",
                "-n", self.namespace
            ]
            
            port_forward_process = subprocess.Popen(
                port_forward_cmd, 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for port-forwarding to establish
            time.sleep(2)
            
            # Check if the process is still running
            if port_forward_process.poll() is not None:
                _, stderr = port_forward_process.communicate()
                logger.error(f"Port forwarding failed: {stderr.decode('utf-8')}")
                metrics["health"] = "port_forward_failed"
                return metrics
            
            try:
                # Make HTTP request to metrics endpoint
                import requests
                
                start_time = time.time()
                response = requests.get(f"http://localhost:{local_port}{self.config['metrics_endpoint']}")
                end_time = time.time()
                
                metrics["latency_ms"] = (end_time - start_time) * 1000
                
                if response.status_code == 200:
                    metrics["health"] = "healthy"
                    
                    # Try to parse metrics from response
                    try:
                        metrics_data = response.json()
                        metrics["security_metrics"] = metrics_data
                    except ValueError:
                        # If not JSON, it might be Prometheus format
                        metrics["security_metrics"] = {
                            "raw_metrics": response.text[:1000]  # Limit size
                        }
                else:
                    metrics["health"] = f"unhealthy_{response.status_code}"
            
            except Exception as e:
                logger.error(f"Error fetching metrics: {e}")
                metrics["health"] = "request_failed"
            
            finally:
                # Terminate port forwarding
                port_forward_process.terminate()
                port_forward_process.wait()
                    
        except Exception as e:
            logger.error(f"Error collecting service metrics for {service_name}: {e}")
            metrics["health"] = "error"
            
        return metrics
    
    def collect_cronjob_metrics(self, cronjob_name: str) -> Dict[str, Any]:
        """Collect metrics about a specific cronjob.
        
        Args:
            cronjob_name: Name of the cronjob
            
        Returns:
            Dictionary containing cronjob metrics
        """
        logger.info(f"Collecting cronjob metrics for {cronjob_name}")
        
        metrics = {
            "name": cronjob_name,
            "schedule": "unknown",
            "last_schedule_time": None,
            "last_successful_time": None,
            "active_jobs": 0,
            "success_count": 0,
            "failure_count": 0,
            "status": "unknown",
            "last_updated": time.time()
        }
        
        try:
            # Get cronjob details
            cronjob_cmd = [
                "kubectl", "get", "cronjob", cronjob_name,
                "-n", self.namespace, "-o", "json"
            ]
            result = subprocess.run(cronjob_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.warning(f"Cronjob {cronjob_name} not found: {result.stderr}")
                metrics["status"] = "not found"
                return metrics
            
            cronjob_data = json.loads(result.stdout)
            
            # Extract basic cronjob metrics
            metrics["schedule"] = cronjob_data.get("spec", {}).get("schedule", "unknown")
            metrics["last_schedule_time"] = cronjob_data.get("status", {}).get("lastScheduleTime")
            metrics["last_successful_time"] = cronjob_data.get("status", {}).get("lastSuccessfulTime")
            metrics["active_jobs"] = len(cronjob_data.get("status", {}).get("active", []))
            
            # Get job history to determine success/failure counts
            selector = f"app={cronjob_name}"
            jobs_cmd = [
                "kubectl", "get", "jobs",
                "-n", self.namespace,
                "-l", selector,
                "-o", "json"
            ]
            jobs_result = subprocess.run(jobs_cmd, capture_output=True, text=True)
            
            if jobs_result.returncode == 0:
                jobs_data = json.loads(jobs_result.stdout)
                
                for job in jobs_data.get("items", []):
                    if job.get("status", {}).get("succeeded", 0) > 0:
                        metrics["success_count"] += 1
                    elif job.get("status", {}).get("failed", 0) > 0:
                        metrics["failure_count"] += 1
            
            # Determine overall status
            if metrics["active_jobs"] > 0:
                metrics["status"] = "active"
            elif metrics["last_successful_time"] is not None:
                metrics["status"] = "succeeded"
            elif metrics["failure_count"] > 0 and metrics["success_count"] == 0:
                metrics["status"] = "failed"
            else:
                metrics["status"] = "idle"
                
        except Exception as e:
            logger.error(f"Error collecting cronjob metrics for {cronjob_name}: {e}")
            metrics["status"] = "error"
            
        return metrics
    
    def _find_available_port(self, start_port: int, end_port: int) -> Optional[int]:
        """Find an available port in the given range.
        
        Args:
            start_port: Start of port range to search
            end_port: End of port range to search
            
        Returns:
            Available port number or None if no ports available
        """
        import socket
        
        for port in range(start_port, end_port):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                result = sock.connect_ex(('localhost', port))
                if result != 0:  # Port is available
                    return port
        
        return None
    
    def collect_all_metrics(self) -> Dict[str, Any]:
        """Collect metrics from all qPoW services and components.
        
        Returns:
            Dictionary containing all collected metrics
        """
        logger.info("Collecting all metrics from qPoW services")
        
        # First discover services if auto-discovery is enabled
        if self.config.get("auto_discovery", True):
            services = self.discover_services()
        else:
            services = self.config.get("qpow_services", [])
        
        if not services:
            logger.warning("No qPoW services found!")
            return {
                "timestamp": time.time(),
                "status": "no_services",
                "services": []
            }
        
        # Collect metrics for each service
        collected_metrics = {
            "timestamp": time.time(),
            "services": [],
            "summary": {
                "healthy_services": 0,
                "total_services": len(services),
                "restart_count": 0,
                "qpow_health": "unknown"
            }
        }
        
        for service_name in services:
            # Collect both deployment and service metrics
            deployment_metrics = self.collect_deployment_metrics(service_name)
            service_metrics = self.collect_service_metrics(service_name)
            
            # Also check for associated cronjobs (using naming convention)
            cronjob_metrics = {}
            cronjob_names = [f"{service_name}-rotation", f"{service_name}-cleanup"]
            
            for cronjob_name in cronjob_names:
                cronjob_metrics[cronjob_name] = self.collect_cronjob_metrics(cronjob_name)
            
            # Merge metrics for this service
            service_data = {
                "name": service_name,
                "deployment": deployment_metrics,
                "service": service_metrics,
                "cronjobs": cronjob_metrics
            }
            
            collected_metrics["services"].append(service_data)
            
            # Update summary metrics
            if service_metrics.get("health") == "healthy":
                collected_metrics["summary"]["healthy_services"] += 1
                
            collected_metrics["summary"]["restart_count"] += deployment_metrics.get("restart_count", 0)
        
        # Calculate overall health
        health_ratio = collected_metrics["summary"]["healthy_services"] / collected_metrics["summary"]["total_services"]
        
        if health_ratio == 1.0:
            collected_metrics["summary"]["qpow_health"] = "optimal"
        elif health_ratio >= 0.8:
            collected_metrics["summary"]["qpow_health"] = "healthy"
        elif health_ratio >= 0.5:
            collected_metrics["summary"]["qpow_health"] = "degraded"
        else:
            collected_metrics["summary"]["qpow_health"] = "critical"
        
        return collected_metrics
    
    def save_metrics(self, metrics: Dict[str, Any], filepath: Optional[str] = None) -> str:
        """Save collected metrics to file.
        
        Args:
            metrics: The metrics to save
            filepath: Optional custom filepath
            
        Returns:
            Path to the saved metrics file
        """
        if not filepath:
            # Use default path with timestamp
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(
                self.config["metrics_output_path"],
                f"k8s_quantum_metrics_{timestamp}.json"
            )
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save file
        with open(filepath, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        logger.info(f"Metrics saved to: {filepath}")
        return filepath
    
    def start_continuous_monitoring(self, interval: Optional[int] = None) -> None:
        """Start continuous monitoring of qPoW services.
        
        Args:
            interval: Override the polling interval from config (in seconds)
        """
        poll_interval = interval or self.config.get("poll_interval_seconds", 60)
        
        logger.info(f"Starting continuous monitoring with {poll_interval}s interval")
        
        try:
            while True:
                metrics = self.collect_all_metrics()
                self.save_metrics(metrics)
                
                # Log summary information
                summary = metrics.get("summary", {})
                logger.info(
                    f"qPoW Health: {summary.get('qpow_health', 'unknown')} | "
                    f"Healthy Services: {summary.get('healthy_services', 0)}/{summary.get('total_services', 0)} | "
                    f"Restarts: {summary.get('restart_count', 0)}"
                )
                
                # Sleep until next poll
                time.sleep(poll_interval)
                
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        except Exception as e:
            logger.error(f"Error in continuous monitoring: {e}")

def main():
    """Command-line interface for Kubernetes metrics integration."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Kubernetes Integration for Quantum Security Metrics")
    parser.add_argument("--namespace", default="default", help="Kubernetes namespace to monitor")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--output", help="Path to save output metrics")
    parser.add_argument("--monitor", action="store_true", help="Start continuous monitoring")
    parser.add_argument("--interval", type=int, help="Override polling interval (seconds)")
    
    args = parser.parse_args()
    
    # Initialize the integration
    k8s_integration = KubernetesMetricsIntegration(
        namespace=args.namespace,
        config_path=args.config
    )
    
    if args.monitor:
        # Start continuous monitoring
        k8s_integration.start_continuous_monitoring(args.interval)
    else:
        # Single collection run
        metrics = k8s_integration.collect_all_metrics()
        filepath = k8s_integration.save_metrics(metrics, args.output)
        
        # Print summary to console
        summary = metrics.get("summary", {})
        print("\n=== qPoW Kubernetes Metrics Summary ===")
        print(f"Overall Health: {summary.get('qpow_health', 'unknown')}")
        print(f"Healthy Services: {summary.get('healthy_services', 0)}/{summary.get('total_services', 0)}")
        print(f"Total Restarts: {summary.get('restart_count', 0)}")
        print(f"Metrics saved to: {filepath}")

if __name__ == "__main__":
    main() 