#!/usr/bin/env python3
"""
IBR España Divine CLI Tool

A comprehensive command-line interface for managing IBR España's digital presence,
Kubernetes infrastructure, and content management.

JAH JAH BLESS THE DIVINE FLOW OF IBR ESPAÑA!
"""

import os
import sys
import json
import argparse
import subprocess
import logging
from datetime import datetime
import tempfile
import shutil
import yaml
from pathlib import Path

# Try to import required packages
try:
    import kubernetes as k8s
    import requests
    from PIL import Image, ImageDraw, ImageFont
    from tabulate import tabulate
    from colorama import init, Fore, Style
except ImportError:
    print("Required packages not found. Install with:")
    print("pip install kubernetes requests pillow tabulate colorama")
    sys.exit(1)

# Initialize colorama
init()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ibr_cli.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ibr_cli")

# Constants
DEFAULT_CONFIG_PATH = os.path.expanduser("~/.ibr/config.json")
DEFAULT_NAMESPACE = "ibr-spain"
IBR_BLUE = (30, 80, 162)

def print_banner():
    """Print the divine IBR CLI banner"""
    banner = f"""
{Fore.YELLOW}🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱{Style.RESET_ALL}
                                                           
{Fore.YELLOW}  𝕴𝕭𝕽 𝕰𝕾𝕻𝕬Ñ𝕬 𝕯𝕴𝖁𝕴𝕹𝕰 𝕮𝕷𝕴 𝕿𝕺𝕺𝕷 {Style.RESET_ALL}
                                                           
{Fore.YELLOW}🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱{Style.RESET_ALL}
"""
    print(banner)

class IBRConfig:
    """Configuration manager for IBR CLI"""
    
    def __init__(self, config_path=None):
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from file or create default"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON in config file {self.config_path}")
                return self._create_default_config()
        else:
            return self._create_default_config()
    
    def _create_default_config(self):
        """Create a default configuration"""
        config = {
            "instagram": {
                "username": "",
                "password": ""
            },
            "kubernetes": {
                "context": "default",
                "namespace": DEFAULT_NAMESPACE
            },
            "church": {
                "name": "IBR España",
                "website": "https://ibr-espana.org"
            }
        }
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        # Save config
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        return config
    
    def get(self, section, key=None):
        """Get configuration value"""
        if section not in self.config:
            return None
        
        if key is None:
            return self.config[section]
        
        return self.config[section].get(key)
    
    def set(self, section, key, value):
        """Set configuration value"""
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section][key] = value
        
        # Save updated config
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
        
        return True

class KubernetesManager:
    """Manager for Kubernetes operations"""
    
    def __init__(self, context=None, namespace=None):
        self.context = context
        self.namespace = namespace or DEFAULT_NAMESPACE
        self._init_kubernetes()
    
    def _init_kubernetes(self):
        """Initialize Kubernetes client"""
        try:
            k8s.config.load_kube_config(context=self.context)
            self.core_api = k8s.client.CoreV1Api()
            self.apps_api = k8s.client.AppsV1Api()
            self.batch_api = k8s.client.BatchV1Api()
            self.networking_api = k8s.client.NetworkingV1Api()
            logger.info(f"Kubernetes client initialized with namespace: {self.namespace}")
        except Exception as e:
            logger.error(f"Failed to initialize Kubernetes client: {e}")
            raise
    
    def get_pods(self):
        """Get all pods in the namespace"""
        return self.core_api.list_namespaced_pod(self.namespace)
    
    def get_services(self):
        """Get all services in the namespace"""
        return self.core_api.list_namespaced_service(self.namespace)
    
    def get_deployments(self):
        """Get all deployments in the namespace"""
        return self.apps_api.list_namespaced_deployment(self.namespace)
    
    def restart_deployment(self, deployment_name):
        """Restart a deployment by patching it"""
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
        return self.core_api.read_namespaced_pod_log(
            name=pod_name,
            namespace=self.namespace,
            container=container,
            tail_lines=tail_lines
        )

    def start_deployment(self, deployment_name, image=None, replicas=1, port=None, env_vars=None):
        """Start a new Kubernetes deployment"""
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
        if port:
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

class ContentManager:
    """Manager for church content"""
    
    @staticmethod
    def create_scripture_image(text, reference, output_path, template='default'):
        """Create a beautiful scripture image with the given text and reference"""
        # Import the dedicated script for scripture image creation
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        try:
            from create_ibr_scripture_image import create_scripture_image
            return create_scripture_image(text, reference, output_path, template)
        except ImportError:
            logger.error("Could not import create_ibr_scripture_image module")
            # Fallback to a basic implementation
            # Image dimensions
            width, height = 1080, 1080
            
            # Create a new image with white background
            image = Image.new('RGB', (width, height), color=(255, 255, 255))
            draw = ImageDraw.Draw(image)
            
            try:
                # Try to load fonts (adjust paths for your system)
                title_font = ImageFont.truetype("Arial.ttf", 60)
                text_font = ImageFont.truetype("Arial.ttf", 50)
                reference_font = ImageFont.truetype("Arial.ttf", 40)
            except OSError:
                # Use default font if custom font not available
                title_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
                reference_font = ImageFont.load_default()
            
            # Add a decorative border
            border_width = 30
            draw.rectangle(
                [(border_width, border_width), (width - border_width, height - border_width)],
                outline=IBR_BLUE,
                width=5
            )
            
            # Draw the title
            title = "Versículo del Día"
            title_width = draw.textlength(title, font=title_font)
            draw.text(
                ((width - title_width) / 2, 120),
                title,
                font=title_font,
                fill=IBR_BLUE
            )
            
            # Simple text rendering (without proper word wrapping)
            draw.text(
                (width // 2, height // 2),
                text,
                font=text_font,
                fill=(0, 0, 0),
                anchor="mm"
            )
            
            # Draw the reference
            ref_width = draw.textlength(reference, font=reference_font)
            draw.text(
                ((width - ref_width) / 2, height - 180),
                reference,
                font=reference_font,
                fill=IBR_BLUE
            )
            
            # Save the image
            image.save(output_path)
            logger.info(f"Created scripture image: {output_path}")
            return output_path
    
    @staticmethod
    def post_to_instagram(content_type, content_path, caption=None):
        """Post content to Instagram"""
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        try:
            # Try to use the dedicated script if available
            subprocess.run(
                [
                    "python", "ibr_instagram_post.py",
                    "--type", content_type,
                    "--content", content_path,
                ],
                check=True
            )
            return True
        except (ImportError, subprocess.CalledProcessError) as e:
            logger.error(f"Failed to post to Instagram: {e}")
            return False

# Command handlers
def handle_k8s_status(args, config):
    """Handle kubernetes status command"""
    print(f"{Fore.CYAN}Fetching IBR España Kubernetes status...{Style.RESET_ALL}")
    
    try:
        k8s_manager = KubernetesManager(
            context=config.get("kubernetes", "context"),
            namespace=args.namespace or config.get("kubernetes", "namespace")
        )
        
        # Get pods
        pods = k8s_manager.get_pods()
        
        # Get deployments
        deployments = k8s_manager.get_deployments()
        
        # Get services
        services = k8s_manager.get_services()
        
        # Format and display status
        pod_data = []
        for pod in pods.items:
            status = "Ready"
            if pod.status.container_statuses:
                for container in pod.status.container_statuses:
                    if not container.ready:
                        status = "Not Ready"
                        break
            else:
                status = "Unknown"
            
            pod_data.append([
                pod.metadata.name,
                status,
                pod.status.phase,
                pod.status.pod_ip or "N/A"
            ])
        
        deployment_data = []
        for deploy in deployments.items:
            deployment_data.append([
                deploy.metadata.name,
                f"{deploy.status.ready_replicas or 0}/{deploy.spec.replicas}",
                deploy.metadata.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            ])
        
        service_data = []
        for svc in services.items:
            ports = ", ".join([f"{port.port}:{port.target_port}" for port in svc.spec.ports])
            service_data.append([
                svc.metadata.name,
                svc.spec.type,
                ports,
                svc.spec.cluster_ip
            ])
        
        # Print tables
        print(f"\n{Fore.YELLOW}🔱 IBR España Kubernetes Status 🔱{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Pods:{Style.RESET_ALL}")
        print(tabulate(pod_data, headers=["Name", "Status", "Phase", "IP"], tablefmt="grid"))
        
        print(f"\n{Fore.CYAN}Deployments:{Style.RESET_ALL}")
        print(tabulate(deployment_data, headers=["Name", "Ready", "Created"], tablefmt="grid"))
        
        print(f"\n{Fore.CYAN}Services:{Style.RESET_ALL}")
        print(tabulate(service_data, headers=["Name", "Type", "Ports", "Cluster IP"], tablefmt="grid"))
        
    except Exception as e:
        print(f"{Fore.RED}Error fetching Kubernetes status: {e}{Style.RESET_ALL}")
        return 1
    
    return 0

def handle_k8s_restart(args, config):
    """Handle kubernetes restart command"""
    print(f"{Fore.CYAN}Restarting IBR España Kubernetes deployment: {args.deployment}{Style.RESET_ALL}")
    
    try:
        k8s_manager = KubernetesManager(
            context=config.get("kubernetes", "context"),
            namespace=args.namespace or config.get("kubernetes", "namespace")
        )
        
        result = k8s_manager.restart_deployment(args.deployment)
        print(f"{Fore.GREEN}Successfully restarted deployment: {result.metadata.name}{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}Error restarting deployment: {e}{Style.RESET_ALL}")
        return 1
    
    return 0

def handle_k8s_logs(args, config):
    """Handle kubernetes logs command"""
    print(f"{Fore.CYAN}Fetching logs for pod: {args.pod}{Style.RESET_ALL}")
    
    try:
        k8s_manager = KubernetesManager(
            context=config.get("kubernetes", "context"),
            namespace=args.namespace or config.get("kubernetes", "namespace")
        )
        
        logs = k8s_manager.get_logs(args.pod, args.container, args.tail)
        print(f"\n{Fore.YELLOW}Logs for {args.pod}:{Style.RESET_ALL}")
        print(logs)
        
    except Exception as e:
        print(f"{Fore.RED}Error fetching logs: {e}{Style.RESET_ALL}")
        return 1
    
    return 0

def handle_k8s_apply(args, config):
    """Handle kubernetes apply command"""
    print(f"{Fore.CYAN}Applying Kubernetes manifest: {args.manifest}{Style.RESET_ALL}")
    
    try:
        k8s_manager = KubernetesManager(
            context=config.get("kubernetes", "context"),
            namespace=args.namespace or config.get("kubernetes", "namespace")
        )
        
        output = k8s_manager.apply_manifest(args.manifest)
        print(f"{Fore.GREEN}Successfully applied manifest:{Style.RESET_ALL}")
        print(output)
        
    except Exception as e:
        print(f"{Fore.RED}Error applying manifest: {e}{Style.RESET_ALL}")
        return 1
    
    return 0

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
            env_vars=env_vars
        )
        
        print(f"{Fore.GREEN}Successfully started deployment: {args.deployment}{Style.RESET_ALL}")
        
        if results.get('service'):
            print(f"{Fore.GREEN}Successfully created service for: {args.deployment}{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}Error starting deployment: {e}{Style.RESET_ALL}")
        return 1
    
    return 0

def handle_instagram_post(args, config):
    """Handle Instagram post command"""
    print(f"{Fore.CYAN}Posting to Instagram: {args.type}{Style.RESET_ALL}")
    
    try:
        # Handle scripture post with image generation
        if args.type == 'scripture':
            if args.text and args.reference:
                # Generate a temp file for the image
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_img:
                    temp_img_path = temp_img.name
                
                # Create the scripture image
                ContentManager.create_scripture_image(
                    args.text, 
                    args.reference, 
                    temp_img_path, 
                    args.template
                )
                
                # Create a temp JSON file for content
                with tempfile.NamedTemporaryFile(suffix='.json', mode='w', delete=False) as temp_json:
                    json.dump({
                        'text': args.text,
                        'reference': args.reference
                    }, temp_json)
                    temp_json_path = temp_json.name
                
                # Post to Instagram
                success = ContentManager.post_to_instagram('scripture', temp_json_path)
                
                # Clean up temp files
                os.unlink(temp_img_path)
                os.unlink(temp_json_path)
                
                if success:
                    print(f"{Fore.GREEN}Successfully posted scripture to Instagram{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Failed to post to Instagram{Style.RESET_ALL}")
                    return 1
            else:
                print(f"{Fore.RED}Error: For scripture posts, both --text and --reference are required{Style.RESET_ALL}")
                return 1
        else:
            print(f"{Fore.RED}Error: Instagram post type '{args.type}' not implemented yet{Style.RESET_ALL}")
            return 1
        
    except Exception as e:
        print(f"{Fore.RED}Error posting to Instagram: {e}{Style.RESET_ALL}")
        return 1
    
    return 0

def handle_config(args, config):
    """Handle configuration commands"""
    if args.get:
        section, key = args.get.split('.') if '.' in args.get else (args.get, None)
        value = config.get(section, key)
        if value is not None:
            print(f"{Fore.GREEN}{args.get} = {json.dumps(value, indent=2)}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Config value not found: {args.get}{Style.RESET_ALL}")
            return 1
    elif args.set:
        section_key, value = args.set
        section, key = section_key.split('.') if '.' in section_key else (section_key, None)
        
        if key is None:
            print(f"{Fore.RED}Invalid format. Use 'section.key value'{Style.RESET_ALL}")
            return 1
        
        try:
            # Try to parse value as JSON
            value = json.loads(value)
        except json.JSONDecodeError:
            # If not valid JSON, treat as string
            pass
        
        if config.set(section, key, value):
            print(f"{Fore.GREEN}Set {section_key} = {value}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Failed to set config value{Style.RESET_ALL}")
            return 1
    
    return 0

def main():
    """Main entry point for IBR CLI"""
    print_banner()
    
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
    
    # k8s status command
    k8s_status_parser = k8s_subparsers.add_parser('status', help='Show Kubernetes status')
    k8s_status_parser.add_argument('--namespace', '-n', help='Kubernetes namespace')
    k8s_status_parser.set_defaults(func=handle_k8s_status)
    
    # k8s restart command
    k8s_restart_parser = k8s_subparsers.add_parser('restart', help='Restart a deployment')
    k8s_restart_parser.add_argument('deployment', help='Deployment to restart')
    k8s_restart_parser.add_argument('--namespace', '-n', help='Kubernetes namespace')
    k8s_restart_parser.set_defaults(func=handle_k8s_restart)
    
    # k8s logs command
    k8s_logs_parser = k8s_subparsers.add_parser('logs', help='Get logs from a pod')
    k8s_logs_parser.add_argument('pod', help='Pod name')
    k8s_logs_parser.add_argument('--container', '-c', help='Container name')
    k8s_logs_parser.add_argument('--tail', '-t', type=int, default=100, help='Number of lines to show')
    k8s_logs_parser.add_argument('--namespace', '-n', help='Kubernetes namespace')
    k8s_logs_parser.set_defaults(func=handle_k8s_logs)
    
    # k8s apply command
    k8s_apply_parser = k8s_subparsers.add_parser('apply', help='Apply a Kubernetes manifest')
    k8s_apply_parser.add_argument('manifest', help='Path to manifest file')
    k8s_apply_parser.add_argument('--namespace', '-n', help='Kubernetes namespace')
    k8s_apply_parser.set_defaults(func=handle_k8s_apply)
    
    # k8s start command
    k8s_start_parser = k8s_subparsers.add_parser('start', help='Start a Kubernetes deployment')
    k8s_start_parser.add_argument('deployment', help='Deployment name')
    k8s_start_parser.add_argument('--image', help='Image for the deployment')
    k8s_start_parser.add_argument('--replicas', type=int, help='Number of replicas')
    k8s_start_parser.add_argument('--port', type=int, help='Port for the deployment')
    k8s_start_parser.add_argument('--env', nargs='+', help='Environment variables for the deployment')
    k8s_start_parser.add_argument('--namespace', '-n', help='Kubernetes namespace')
    k8s_start_parser.set_defaults(func=handle_k8s_start)
    
    # Instagram commands
    instagram_parser = subparsers.add_parser('instagram', help='Instagram commands')
    instagram_subparsers = instagram_parser.add_subparsers(dest='subcommand')
    
    # instagram post command
    instagram_post_parser = instagram_subparsers.add_parser('post', help='Post to Instagram')
    instagram_post_parser.add_argument('type', choices=['scripture', 'sermon', 'event'], help='Type of post')
    instagram_post_parser.add_argument('--text', help='Text for scripture posts')
    instagram_post_parser.add_argument('--reference', help='Reference for scripture posts')
    instagram_post_parser.add_argument('--template', choices=['default', 'light', 'dark'], default='default', help='Template for scripture images')
    instagram_post_parser.set_defaults(func=handle_instagram_post)
    
    # Config commands
    config_parser = subparsers.add_parser('config', help='Configuration commands')
    config_parser.add_argument('--get', metavar='KEY', help='Get a configuration value')
    config_parser.add_argument('--set', nargs=2, metavar=('KEY', 'VALUE'), help='Set a configuration value')
    config_parser.set_defaults(func=handle_config)
    
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
