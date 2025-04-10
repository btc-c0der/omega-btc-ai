
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

import os
import sys
import json
import argparse
import subprocess
import logging
import datetime
import tempfile
import shutil
import yaml
import socket
from datetime import datetime
from colorama import Fore, Style

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ibr_cli.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ibr-cli")

# Default configuration
DEFAULT_NAMESPACE = "ibr-spain"

class IBRConfig:
    """Configuration manager for IBR CLI"""
    
    def __init__(self, config_path=None):
        self.config_path = config_path or os.path.expanduser("~/.ibr-cli.json")
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from file or create default if it doesn't exist"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                logger.info(f"Loaded configuration from {self.config_path}")
                return config
            except Exception as e:
                logger.error(f"Error loading configuration: {e}")
        
        # Create default config if it doesn't exist
        return self._create_default_config()
    
    def _create_default_config(self):
        """Create and save a default configuration"""
        default_config = {
            "kubernetes": {
                "context": None,
                "namespace": DEFAULT_NAMESPACE
            },
            "instagram": {
                "username": None,
                "password": None,
                "templates_dir": os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
            }
        }
        
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
            logger.info(f"Created default configuration at {self.config_path}")
        except Exception as e:
            logger.error(f"Error creating default configuration: {e}")
        
        return default_config
    
    def get(self, section, key=None):
        """Get a configuration value"""
        if section not in self.config:
            return None
        
        if key is None:
            return self.config[section]
        
        return self.config[section].get(key)
    
    def set(self, section, key, value):
        """Set a configuration value"""
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section][key] = value
        
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False

class KubernetesManager:
    """Manager for Kubernetes operations"""
    
    def __init__(self, context=None, namespace=None):
        self.context = context
        self.namespace = namespace or DEFAULT_NAMESPACE
        self.core_api = None
        self.apps_api = None
        self.batch_api = None
        self.networking_api = None
        try:
            self._init_kubernetes()
        except Exception as e:
            logger.error(f"Failed to initialize Kubernetes client: {e}")
            # Continue without failing - CLI can still be used for non-k8s operations
    
    def _init_kubernetes(self):
        """Initialize Kubernetes client"""
        try:
            import kubernetes as k8s
            k8s.config.load_kube_config(context=self.context)
            self.core_api = k8s.client.CoreV1Api()
            self.apps_api = k8s.client.AppsV1Api()
            self.batch_api = k8s.client.BatchV1Api()
            self.networking_api = k8s.client.NetworkingV1Api()
            logger.info(f"Kubernetes client initialized with namespace: {self.namespace}")
        except (ImportError, AttributeError) as e:
            logger.error(f"Kubernetes client initialization failed: {e}")
            raise
    
    def get_pods(self):
        """Get all pods in the namespace"""
        if not self.core_api:
            raise RuntimeError("Kubernetes client not initialized")
        return self.core_api.list_namespaced_pod(self.namespace)
    
    def get_services(self):
        """Get all services in the namespace"""
        if not self.core_api:
            raise RuntimeError("Kubernetes client not initialized")
        return self.core_api.list_namespaced_service(self.namespace)
    
    def get_deployments(self):
        """Get all deployments in the namespace"""
        if not self.apps_api:
            raise RuntimeError("Kubernetes client not initialized")
        return self.apps_api.list_namespaced_deployment(self.namespace)
    
    def restart_deployment(self, deployment_name):
        """Restart a deployment by patching it"""
        if not self.apps_api:
            raise RuntimeError("Kubernetes client not initialized")
        
        # To restart, we patch the template spec with a new annotation
        patch = {
            "spec": {
                "template": {
                    "metadata": {
                        "annotations": {
                            "ibr-cli/restartedAt": datetime.now().isoformat()
                        }
                    }
                }
            }
        }
        
        return self.apps_api.patch_namespaced_deployment(
            name=deployment_name,
            namespace=self.namespace,
            body=patch
        )
    
    def apply_manifest(self, manifest_path):
        """Apply a Kubernetes manifest file"""
        try:
            result = subprocess.run(
                ["kubectl", "apply", "-f", manifest_path, "-n", self.namespace],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to apply manifest {manifest_path}: {e.stderr}")
            raise
    
    def get_logs(self, pod_name, container=None, tail_lines=100):
        """Get logs from a pod"""
        if not self.core_api:
            raise RuntimeError("Kubernetes client not initialized")
        return self.core_api.read_namespaced_pod_log(
            name=pod_name,
            namespace=self.namespace,
            container=container,
            tail_lines=tail_lines
        )
    
    def find_available_port(self, start_port=8000, max_port=9000):
        """Find an available port in the Kubernetes cluster
        
        Checks for any existing services using the port and returns the first available one.
        """
        if not self.core_api:
            raise RuntimeError("Kubernetes client not initialized")
        
        # Get all services in the namespace
        try:
            services = self.core_api.list_namespaced_service(self.namespace)
            used_ports = set()
            
            # Collect all ports used by existing services
            for service in services.items:
                for port in service.spec.ports:
                    used_ports.add(port.port)
            
            # Find the first available port in the range that is not used by k8s services
            # and is also available on the local machine
            for port in range(start_port, max_port + 1):
                if port not in used_ports and self._is_port_available_locally(port):
                    logger.info(f"Found available port: {port}")
                    return port
                    
            # If we get here, no ports were available
            raise RuntimeError(f"No available ports found between {start_port} and {max_port}")
            
        except Exception as e:
            logger.error(f"Error finding available port: {e}")
            raise
    
    def _is_port_available_locally(self, port):
        """Check if a port is available on the local machine."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Try to bind to the port
                sock.bind(('127.0.0.1', port))
                # If we get here, the port is available
                return True
        except socket.error:
            # Port is in use
            return False
        except Exception as e:
            logger.warning(f"Error checking port {port} availability: {e}")
            # Be conservative and assume the port is in use
            return False
    
    def start_deployment(self, deployment_name, image=None, replicas=1, port=None, env_vars=None, auto_port=False):
        """Start a new Kubernetes deployment"""
        # If auto_port is True and port is None, automatically find an available port
        if auto_port and port is None:
            port = self.find_available_port()
            logger.info(f"Auto-selected port {port} for deployment {deployment_name}")
        elif auto_port and port is not None:
            # If port is specified but we want to check availability
            # Check if the specified port is available
            try:
                services = self.core_api.list_namespaced_service(self.namespace)
                for service in services.items:
                    for service_port in service.spec.ports:
                        if service_port.port == port:
                            # Port is in use, find a new one
                            logger.warning(f"Port {port} is already in use, finding an alternative")
                            port = self.find_available_port(start_port=port+1)
                            break
            except Exception as e:
                logger.error(f"Error checking port availability: {e}")
                # Continue with the specified port as a fallback
        
        # Create a basic deployment manifest
        deployment = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": deployment_name,
                "namespace": self.namespace,
                "labels": {
                    "app": deployment_name,
                    "created-by": "ibr-cli"
                }
            },
            "spec": {
                "replicas": replicas,
                "selector": {
                    "matchLabels": {
                        "app": deployment_name
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": deployment_name
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "name": deployment_name,
                                "image": image or f"ibr-spain/{deployment_name}:latest",
                                "imagePullPolicy": "IfNotPresent"
                            }
                        ]
                    }
                }
            }
        }
        
        # Add ports if specified
        service = None
        if port:
            deployment["spec"]["template"]["spec"]["containers"][0]["ports"] = [
                {"containerPort": port}
            ]
            
            # Also create a service for this deployment
            service = {
                "apiVersion": "v1",
                "kind": "Service",
                "metadata": {
                    "name": deployment_name,
                    "namespace": self.namespace
                },
                "spec": {
                    "selector": {
                        "app": deployment_name
                    },
                    "ports": [
                        {
                            "port": port,
                            "targetPort": port
                        }
                    ]
                }
            }

        # Add environment variables if specified
        if env_vars:
            env_list = []
            for key, value in env_vars.items():
                env_list.append({
                    "name": key,
                    "value": value
                })
            deployment["spec"]["template"]["spec"]["containers"][0]["env"] = env_list
        
        # Write deployment to a temporary file
        with tempfile.NamedTemporaryFile(suffix='.yaml', mode='w', delete=False) as temp_file:
            yaml.dump(deployment, temp_file)
            deployment_file = temp_file.name
        
        # Create service if port was specified
        service_file = None
        if service:
            with tempfile.NamedTemporaryFile(suffix='.yaml', mode='w', delete=False) as temp_file:
                yaml.dump(service, temp_file)
                service_file = temp_file.name
        
        try:
            # Apply the deployment
            deployment_result = self.apply_manifest(deployment_file)
            service_result = None
            
            # Apply the service if it was created
            if service_file:
                service_result = self.apply_manifest(service_file)
            
            # Return the results
            return {
                "deployment": deployment_result,
                "service": service_result
            }
        finally:
            # Clean up temporary files
            os.unlink(deployment_file)
            if service_file:
                os.unlink(service_file)

def handle_k8s_start(args, config):
    """Handle kubernetes start deployment command"""
    print(f"{Fore.CYAN}Starting IBR España Kubernetes deployment: {args.deployment}{Style.RESET_ALL}")
    
    # Parse environment variables if provided
    env_vars = {}
    if args.env:
        for env_var in args.env:
            if '=' in env_var:
                key, value = env_var.split('=', 1)
                env_vars[key] = value
            else:
                print(f"{Fore.YELLOW}Warning: Skipping invalid environment variable format: {env_var}{Style.RESET_ALL}")
    
    try:
        k8s_manager = KubernetesManager(
            context=config.get("kubernetes", "context"),
            namespace=args.namespace or config.get("kubernetes", "namespace")
        )
        
        results = k8s_manager.start_deployment(
            args.deployment,
            image=args.image,
            replicas=args.replicas,
            port=args.port,
            env_vars=env_vars,
            auto_port=args.auto_port
        )
        
        print(f"{Fore.GREEN}Successfully started deployment: {args.deployment}{Style.RESET_ALL}")
        
        if results.get('service'):
            print(f"{Fore.GREEN}Successfully created service for: {args.deployment}{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}Error starting deployment: {e}{Style.RESET_ALL}")
        return 1
    
    return 0

def main():
    """Main entry point for IBR CLI"""
    # Create the argument parser
    parser = argparse.ArgumentParser(
        description="IBR España Divine CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Global arguments
    parser.add_argument('--config', help='Path to config file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    
    # Create subparsers for different command groups
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Kubernetes commands
    k8s_parser = subparsers.add_parser('k8s', help='Kubernetes commands')
    k8s_subparsers = k8s_parser.add_subparsers(dest='subcommand')
    
    # k8s start command
    k8s_start_parser = k8s_subparsers.add_parser('start', help='Start a new deployment')
    k8s_start_parser.add_argument('deployment', help='Deployment name')
    k8s_start_parser.add_argument('--image', help='Container image to use')
    k8s_start_parser.add_argument('--replicas', type=int, default=1, help='Number of replicas')
    k8s_start_parser.add_argument('--port', type=int, help='Container port to expose')
    k8s_start_parser.add_argument('--auto-port', action='store_true', help='Automatically find an available port if the specified one is in use')
    k8s_start_parser.add_argument('--env', action='append', help='Environment variables (format: KEY=VALUE)')
    k8s_start_parser.add_argument('--namespace', '-n', help='Kubernetes namespace')
    k8s_start_parser.set_defaults(func=handle_k8s_start)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Load configuration
    config = IBRConfig(args.config)
    
    # Set log level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # If no command specified, show help
    if not hasattr(args, 'func'):
        parser.print_help()
        return 0
    
    # Call the appropriate handler function
    return args.func(args, config)

if __name__ == "__main__":
    sys.exit(main()) 