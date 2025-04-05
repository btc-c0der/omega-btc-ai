"""
Kubernetes Matrix surveillance system for the Quantum Test Runner.
"""

import os
import time
import logging
import threading
import datetime
from typing import Dict, List, Set, Any, Optional, Tuple, Union, cast

from .types import Colors

logger = logging.getLogger("0M3G4_B0TS_QA_AUT0_TEST_SUITES_RuNn3R_5D")

# For Kubernetes surveillance support
KUBERNETES_AVAILABLE = False
try:
    from kubernetes import client, config, watch
    KUBERNETES_AVAILABLE = True
except ImportError:
    logger.warning("Kubernetes client not available. Install with: pip install kubernetes")
    # Create placeholder objects for type checking
    class PlaceholderConfig:
        @staticmethod
        def load_kube_config(*args, **kwargs): pass
        
        @staticmethod
        def load_incluster_config(*args, **kwargs): pass
    
    class PlaceholderClient:
        class CoreV1Api: pass
        class AppsV1Api: pass
    
    # Use placeholder objects if kubernetes not available
    client = cast(Any, PlaceholderClient)
    config = cast(Any, PlaceholderConfig)
    watch = cast(Any, object())

class K8sMatrixSurveillance:
    """Monitor Kubernetes resources and provide matrix-style insights."""
    
    def __init__(self, namespace: Optional[str] = None):
        """Initialize the Kubernetes surveillance system."""
        self.namespace = namespace
        self.available = KUBERNETES_AVAILABLE
        self.running = False
        self.thread = None
        self.last_scan_time = 0
        self.k8s_resources = {}
        self.scan_interval = 30  # seconds
        
        # Try to load Kubernetes config
        if self.available:
            try:
                config.load_kube_config()
                # Fallback to in-cluster config if running inside a pod
                if not os.path.exists(os.path.expanduser('~/.kube/config')):
                    config.load_incluster_config()
                self.v1 = client.CoreV1Api()
                self.apps_v1 = client.AppsV1Api()
                logger.info(f"{Colors.CYAN}🔷 Kubernetes surveillance system initialized{Colors.ENDC}")
            except Exception as e:
                logger.error(f"{Colors.RED}Failed to initialize Kubernetes client: {e}{Colors.ENDC}")
                self.available = False
        else:
            # Initialize placeholders for type checking
            self.v1 = client.CoreV1Api()
            self.apps_v1 = client.AppsV1Api()
            
    def start(self) -> bool:
        """Start the Kubernetes surveillance thread."""
        if not self.available:
            logger.warning(f"{Colors.YELLOW}⚠ Kubernetes client not available. Surveillance disabled.{Colors.ENDC}")
            return False
            
        if self.running:
            logger.info("K8s surveillance is already running")
            return True
            
        self.running = True
        self.thread = threading.Thread(target=self._surveillance_loop, daemon=True)
        self.thread.start()
        logger.info(f"{Colors.BLUE}🔶 Entered the Matrix: K8s surveillance activated{Colors.ENDC}")
        return True
    
    def stop(self) -> None:
        """Stop the Kubernetes surveillance thread."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        logger.info(f"{Colors.YELLOW}Exited the Matrix: K8s surveillance deactivated{Colors.ENDC}")
    
    def _surveillance_loop(self) -> None:
        """Main surveillance loop for monitoring Kubernetes resources."""
        while self.running:
            try:
                self._scan_resources()
                self.last_scan_time = time.time()
                
                # Scan at regular intervals
                time.sleep(self.scan_interval)
            except Exception as e:
                logger.error(f"{Colors.RED}Error in K8s surveillance loop: {e}{Colors.ENDC}")
                time.sleep(60)  # Wait longer after error
    
    def _scan_resources(self) -> None:
        """Scan Kubernetes resources and store the results."""
        if not self.available:
            return
            
        try:
            # Get pods
            if self.namespace:
                pods = self.v1.list_namespaced_pod(self.namespace)
            else:
                pods = self.v1.list_pod_for_all_namespaces()
                
            # Get deployments
            if self.namespace:
                deployments = self.apps_v1.list_namespaced_deployment(self.namespace)
            else:
                deployments = self.apps_v1.list_deployment_for_all_namespaces()
                
            # Get services
            if self.namespace:
                services = self.v1.list_namespaced_service(self.namespace)
            else:
                services = self.v1.list_service_for_all_namespaces()
                
            # Store results
            self.k8s_resources = {
                'pods': pods.items,
                'deployments': deployments.items,
                'services': services.items,
                'last_updated': time.time()
            }
            
            # Log summary
            logger.info(f"{Colors.CYAN}Matrix Surveillance: {len(pods.items)} pods, "
                       f"{len(deployments.items)} deployments, "
                       f"{len(services.items)} services{Colors.ENDC}")
                       
            # Check for problematic pods
            self._check_pod_health()
            
        except Exception as e:
            logger.error(f"{Colors.RED}Error scanning K8s resources: {e}{Colors.ENDC}")
    
    def _check_pod_health(self) -> None:
        """Check for pods with issues and log warnings."""
        if 'pods' not in self.k8s_resources:
            return
            
        problem_pods = []
        
        for pod in self.k8s_resources['pods']:
            pod_name = pod.metadata.name
            pod_namespace = pod.metadata.namespace
            pod_status = pod.status.phase
            
            # Check for problematic statuses
            if pod_status != 'Running' and pod_status != 'Succeeded':
                problem_pods.append({
                    'name': pod_name,
                    'namespace': pod_namespace,
                    'status': pod_status,
                    'container_statuses': [
                        {
                            'name': container.name,
                            'ready': container.ready,
                            'restarts': container.restart_count
                        }
                        for container in (pod.status.container_statuses or [])
                    ]
                })
        
        if problem_pods:
            logger.warning(f"{Colors.YELLOW}⚠ Matrix Anomalies Detected: {len(problem_pods)} problematic pods{Colors.ENDC}")
            for pod in problem_pods:
                logger.warning(f"{Colors.RED}Pod {pod['name']} in namespace {pod['namespace']} has status {pod['status']}{Colors.ENDC}")
                
                for container in pod['container_statuses']:
                    if not container['ready']:
                        logger.warning(f"{Colors.RED}  Container {container['name']} not ready (restarts: {container['restarts']}){Colors.ENDC}")
    
    def get_resource_report(self) -> Dict[str, Any]:
        """Generate a comprehensive report of Kubernetes resources."""
        if not self.available or not self.k8s_resources:
            return {'error': 'No Kubernetes data available'}
            
        report = {
            'timestamp': time.time(),
            'summary': {
                'pods': len(self.k8s_resources['pods']),
                'deployments': len(self.k8s_resources['deployments']),
                'services': len(self.k8s_resources['services'])
            },
            'namespaces': {},
            'health': {
                'healthy_pods': 0,
                'problematic_pods': 0,
                'total_restarts': 0
            }
        }
        
        # Analyze pods by namespace
        for pod in self.k8s_resources['pods']:
            namespace = pod.metadata.namespace
            
            if namespace not in report['namespaces']:
                report['namespaces'][namespace] = {
                    'pods': 0,
                    'deployments': 0,
                    'services': 0
                }
                
            report['namespaces'][namespace]['pods'] += 1
            
            # Track health statistics
            if pod.status.phase == 'Running':
                report['health']['healthy_pods'] += 1
            else:
                report['health']['problematic_pods'] += 1
                
            # Count restarts
            if pod.status.container_statuses:
                for container in pod.status.container_statuses:
                    report['health']['total_restarts'] += container.restart_count
        
        # Analyze deployments by namespace
        for deployment in self.k8s_resources['deployments']:
            namespace = deployment.metadata.namespace
            
            if namespace not in report['namespaces']:
                report['namespaces'][namespace] = {
                    'pods': 0,
                    'deployments': 0,
                    'services': 0
                }
                
            report['namespaces'][namespace]['deployments'] += 1
            
        # Analyze services by namespace
        for service in self.k8s_resources['services']:
            namespace = service.metadata.namespace
            
            if namespace not in report['namespaces']:
                report['namespaces'][namespace] = {
                    'pods': 0,
                    'deployments': 0,
                    'services': 0
                }
                
            report['namespaces'][namespace]['services'] += 1
            
        return report
    
    def print_matrix_report(self, detailed: bool = False) -> None:
        """Print a Matrix-style report of Kubernetes resources."""
        if not self.available:
            print(f"\n{Colors.RED}⚠️ THE MATRIX IS UNAVAILABLE ⚠️{Colors.ENDC}")
            print(f"{Colors.YELLOW}Kubernetes client not installed or configured{Colors.ENDC}")
            print(f"{Colors.CYAN}Install with: pip install kubernetes{Colors.ENDC}\n")
            return
            
        if not self.k8s_resources:
            print(f"\n{Colors.YELLOW}⚠️ NO DATA FROM THE MATRIX YET ⚠️{Colors.ENDC}")
            print(f"{Colors.CYAN}Waiting for first scan to complete...{Colors.ENDC}\n")
            return
            
        report = self.get_resource_report()
        
        # Matrix-style header
        matrix_header = f"""
{Colors.GREEN}╔═════════════════════════════════════════════════════════════╗
║                                                             ║
║  𝕋𝕙𝕖 𝕄𝕒𝕥𝕣𝕚𝕩 𝕂𝟠𝕤 𝔾𝕣𝕚𝕕: 𝕊𝕠𝕟𝕟𝕖𝕥 𝔹𝕝𝕦𝕖 ℙ𝕚𝕝𝕝 𝔼𝕕𝕚𝕥𝕚𝕠𝕟            ║
║                                                             ║
╚═════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
        print(matrix_header)
        
        # Matrix time
        matrix_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"{Colors.CYAN}Time in the Matrix: {matrix_time}{Colors.ENDC}")
        
        # Summary section
        print(f"\n{Colors.BOLD}{Colors.GREEN}🧬 MATRIX RESOURCE SUMMARY{Colors.ENDC}")
        print(f"{Colors.GREEN}───────────────────────────{Colors.ENDC}")
        print(f"  📦 Pods:        {report['summary']['pods']}")
        print(f"  🚀 Deployments:  {report['summary']['deployments']}")
        print(f"  🔌 Services:     {report['summary']['services']}")
        
        # Health section
        health_color = Colors.GREEN if report['health']['problematic_pods'] == 0 else Colors.RED
        print(f"\n{Colors.BOLD}{health_color}🔋 MATRIX HEALTH STATUS{Colors.ENDC}")
        print(f"{health_color}───────────────────────────{Colors.ENDC}")
        print(f"  ✅ Healthy Pods:     {report['health']['healthy_pods']}")
        print(f"  ⚠️ Problematic Pods:  {report['health']['problematic_pods']}")
        print(f"  🔄 Total Restarts:    {report['health']['total_restarts']}")
        
        # Namespace section
        if detailed:
            print(f"\n{Colors.BOLD}{Colors.BLUE}🌐 MATRIX NAMESPACE BREAKDOWN{Colors.ENDC}")
            print(f"{Colors.BLUE}───────────────────────────{Colors.ENDC}")
            for namespace, resources in report['namespaces'].items():
                print(f"  {Colors.CYAN}{namespace}:{Colors.ENDC}")
                print(f"    📦 Pods:        {resources['pods']}")
                print(f"    🚀 Deployments:  {resources['deployments']}")
                print(f"    🔌 Services:     {resources['services']}")
        
        # Footer
        print(f"\n{Colors.GREEN}═════════════════════════════════════════════════════════════{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.GREEN}                  FOLLOW THE WHITE RABBIT                  {Colors.ENDC}")
        print(f"{Colors.GREEN}═════════════════════════════════════════════════════════════{Colors.ENDC}\n") 