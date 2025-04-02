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
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("qpow_metrics")

# Add parent directories to path if needed
qpow_dir = Path(__file__).resolve().parent.parent.parent
if str(qpow_dir) not in sys.path:
    sys.path.insert(0, str(qpow_dir))

# Import key components to make them accessible through the package
try:
    from .collector import MetricsCollector
    from .dashboard import DashboardGenerator
    from .dashboard_server import DashboardServer
    from .k8s_metrics_integration import KubernetesMetricsIntegration
except ImportError as e:
    logger.warning(f"Not all metrics components could be imported: {e}")

# Package information
__version__ = "1.0.0"
__author__ = "OMEGA Divine Collective"
__description__ = "Quantum-Resistant Security Metrics System"

# Convenience functions

def collect_metrics(config_path=None, output_dir=None, save=True):
    """Collect metrics and optionally save them.
    
    Args:
        config_path: Optional path to configuration file
        output_dir: Optional directory to save metrics to
        save: Whether to save metrics to file
        
    Returns:
        Dictionary containing collected metrics
    """
    try:
        collector = MetricsCollector(config_path)
        
        if output_dir:
            collector.config["output_directory"] = output_dir
            
        # Collect metrics
        metrics = collector.collect_all_metrics()
        
        # Save if requested
        if save:
            collector.save_metrics()
            
        return metrics
    except Exception as e:
        logger.error(f"Error collecting metrics: {e}")
        return None

def generate_dashboard(metrics_path=None, output_dir=None, theme="dark", format="html"):
    """Generate a dashboard from metrics.
    
    Args:
        metrics_path: Optional path to metrics file
        output_dir: Optional directory to save dashboard to
        theme: Dashboard theme ("dark" or "light")
        format: Dashboard format ("html", "k8s", or "both")
        
    Returns:
        Path to the generated dashboard file
    """
    try:
        dashboard_gen = DashboardGenerator()
        
        # Override configuration
        if output_dir:
            dashboard_gen.config["output_directory"] = output_dir
        dashboard_gen.config["theme"] = theme
        
        # Load metrics if specified
        if metrics_path:
            dashboard_gen.load_metrics(metrics_path)
        else:
            dashboard_gen.load_metrics()
            
        # Generate dashboard
        if format == "html" or format == "both":
            html_path = dashboard_gen.generate_html_dashboard()
            if format == "html":
                return html_path
                
        if format == "k8s" or format == "both":
            k8s_path = dashboard_gen.generate_k8s_dashboard()
            if format == "k8s":
                return k8s_path
                
        return html_path
    except Exception as e:
        logger.error(f"Error generating dashboard: {e}")
        return None

def start_dashboard_server(host="0.0.0.0", port=8080, metrics_path=None, dashboard_path=None):
    """Start a dashboard server.
    
    Args:
        host: Host to bind to
        port: Port to listen on
        metrics_path: Optional path to metrics directory
        dashboard_path: Optional path to dashboard directory
        
    Returns:
        The DashboardServer instance
    """
    try:
        server = DashboardServer()
        
        # Override configuration
        server.config["host"] = host
        server.config["port"] = port
        
        if metrics_path:
            server.config["metrics_path"] = metrics_path
        if dashboard_path:
            server.config["dashboard_path"] = dashboard_path
            
        # Start in a separate thread so it doesn't block
        import threading
        server_thread = threading.Thread(
            target=server.start_server,
            daemon=True
        )
        server_thread.start()
        
        logger.info(f"Dashboard server started on http://{host}:{port}/")
        return server
    except Exception as e:
        logger.error(f"Error starting dashboard server: {e}")
        return None

def collect_kubernetes_metrics(namespace="default", config_path=None):
    """Collect metrics from Kubernetes.
    
    Args:
        namespace: Kubernetes namespace
        config_path: Optional path to configuration file
        
    Returns:
        Dictionary containing Kubernetes metrics
    """
    try:
        k8s_metrics = KubernetesMetricsIntegration(namespace, config_path)
        return k8s_metrics.collect_all_metrics()
    except Exception as e:
        logger.error(f"Error collecting Kubernetes metrics: {e}")
        return None

# Expose key classes and functions
__all__ = [
    'MetricsCollector',
    'DashboardGenerator',
    'DashboardServer',
    'KubernetesMetricsIntegration',
    'collect_metrics',
    'generate_dashboard',
    'start_dashboard_server',
    'collect_kubernetes_metrics'
] 