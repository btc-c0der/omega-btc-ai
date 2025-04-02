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
import threading
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver
import datetime

# Add parent directories to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import our modules
from security.metrics.collector import MetricsCollector
from security.metrics.dashboard import DashboardGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("qpow_dashboard_server")

class DashboardRequestHandler(SimpleHTTPRequestHandler):
    """Custom request handler for serving dashboard files."""
    
    # Class variable to store server configuration
    server_config = {}
    metrics_path = ""
    dashboard_path = ""
    
    def __init__(self, *args, **kwargs):
        # Set the directory to serve files from
        if self.dashboard_path:
            self.directory = self.dashboard_path
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests for the dashboard."""
        # Serve dashboard.html as root
        if self.path == "/" or self.path == "":
            self.path = "/dashboard.html"
            
        # Handle API requests for metrics data
        if self.path.startswith("/api/metrics"):
            self.send_metrics_data()
            return
        
        # Handle requests for latest dashboard
        if self.path == "/dashboard.html" or self.path == "/index.html":
            self.send_latest_dashboard()
            return
            
        # Let the parent class handle static files
        return super().do_GET()
    
    def send_metrics_data(self):
        """Send metrics data as JSON response."""
        try:
            # Default to the latest metrics file
            metrics_dir = Path(self.metrics_path)
            if not metrics_dir.exists():
                self.send_error(404, "Metrics directory not found")
                return
                
            # Find the latest metrics file
            metrics_file = metrics_dir / "metrics_latest.json"
            if not metrics_file.exists():
                # Try to find any metrics file
                metrics_files = sorted(
                    [f for f in metrics_dir.glob("metrics_*.json")],
                    key=lambda f: f.stat().st_mtime,
                    reverse=True
                )
                
                if not metrics_files:
                    self.send_error(404, "No metrics files found")
                    return
                    
                metrics_file = metrics_files[0]
            
            # Read metrics data
            with open(metrics_file, 'r') as f:
                metrics_data = json.load(f)
            
            # Send response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            # Send JSON data
            self.wfile.write(json.dumps(metrics_data).encode())
            
        except Exception as e:
            logger.error(f"Error sending metrics data: {e}")
            self.send_error(500, f"Internal server error: {e}")
    
    def send_latest_dashboard(self):
        """Generate and send the latest dashboard HTML."""
        try:
            # Create dashboard generator
            dashboard_gen = DashboardGenerator()
            
            # Generate dashboard HTML
            html_content = dashboard_gen._generate_dashboard_html()
            
            # Send response
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            
            # Send HTML content
            self.wfile.write(html_content.encode())
            
        except Exception as e:
            logger.error(f"Error generating dashboard: {e}")
            self.send_error(500, f"Internal server error: {e}")
    
    def log_message(self, format, *args):
        """Override to use our logger instead of stderr."""
        logger.info(format % args)

class DashboardServer:
    """Server for hosting the quantum security metrics dashboard."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the dashboard server.
        
        Args:
            config_path: Optional path to configuration file
        """
        self.config = self._load_config(config_path)
        self.collector = None
        self.dashboard_generator = None
        self.server = None
        self.collector_thread = None
        
        # Configure the request handler with our settings
        DashboardRequestHandler.server_config = self.config
        DashboardRequestHandler.metrics_path = self.config["metrics_path"]
        DashboardRequestHandler.dashboard_path = self.config["dashboard_path"]
    
    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        default_config = {
            "host": "0.0.0.0",
            "port": 8080,
            "metrics_path": "quantum_pow/metrics",
            "dashboard_path": "quantum_pow/security/metrics/dashboard",
            "collection_interval_seconds": 300,
            "dashboard_update_interval_seconds": 60,
            "collector_config": None,
            "dashboard_config": None,
            "auto_generate_dashboard": True,
            "enable_continuous_collection": True
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
    
    def _prepare_paths(self):
        """Prepare directories for metrics and dashboard files."""
        # Create metrics directory if it doesn't exist
        metrics_path = Path(self.config["metrics_path"])
        metrics_path.mkdir(parents=True, exist_ok=True)
        
        # Create dashboard directory if it doesn't exist
        dashboard_path = Path(self.config["dashboard_path"])
        dashboard_path.mkdir(parents=True, exist_ok=True)
    
    def start_metrics_collection(self):
        """Start the metrics collector in a background thread."""
        if not self.config["enable_continuous_collection"]:
            logger.info("Continuous metrics collection disabled")
            return
            
        # Initialize collector
        self.collector = MetricsCollector(self.config["collector_config"])
        
        # Start collection in a separate thread
        def collection_thread():
            try:
                logger.info("Starting metrics collection thread")
                interval = self.config["collection_interval_seconds"]
                
                while True:
                    start_time = time.time()
                    
                    # Collect metrics
                    self.collector.collect_all_metrics()
                    filepath = self.collector.save_metrics()
                    
                    if filepath:
                        logger.info(f"Collected metrics and saved to {filepath}")
                        
                    # Generate dashboard if auto-generate is enabled
                    if self.config["auto_generate_dashboard"]:
                        self.generate_dashboard()
                    
                    # Calculate sleep time
                    elapsed = time.time() - start_time
                    sleep_time = max(1, interval - elapsed)
                    
                    logger.info(f"Sleeping for {sleep_time:.1f} seconds until next collection")
                    time.sleep(sleep_time)
            except Exception as e:
                logger.error(f"Error in metrics collection thread: {e}")
        
        # Start the thread
        self.collector_thread = threading.Thread(
            target=collection_thread,
            daemon=True
        )
        self.collector_thread.start()
        logger.info("Metrics collection thread started")
    
    def generate_dashboard(self):
        """Generate dashboard files from the latest metrics."""
        try:
            logger.info("Generating dashboard from latest metrics")
            
            # Initialize dashboard generator
            self.dashboard_generator = DashboardGenerator(self.config["dashboard_config"])
            
            # Generate HTML dashboard
            html_path = self.dashboard_generator.generate_html_dashboard(
                os.path.join(self.config["dashboard_path"], "dashboard.html")
            )
            
            if html_path:
                logger.info(f"Generated dashboard at {html_path}")
            else:
                logger.warning("Failed to generate dashboard")
                
        except Exception as e:
            logger.error(f"Error generating dashboard: {e}")
    
    def start_server(self):
        """Start the HTTP server to serve the dashboard."""
        # Prepare directories
        self._prepare_paths()
        
        # Start metrics collection
        self.start_metrics_collection()
        
        # Generate initial dashboard if it doesn't exist
        dashboard_file = os.path.join(self.config["dashboard_path"], "dashboard.html")
        if not os.path.exists(dashboard_file) and self.config["auto_generate_dashboard"]:
            self.generate_dashboard()
        
        # Create and start the HTTP server
        host = self.config["host"]
        port = self.config["port"]
        
        # Try to start the server
        for attempt in range(3):
            try:
                self.server = HTTPServer((host, port), DashboardRequestHandler)
                logger.info(f"Starting dashboard server on http://{host}:{port}/")
                
                # Start serving
                self.server.serve_forever()
                
            except OSError as e:
                if attempt < 2:
                    logger.warning(f"Port {port} is in use, trying port {port + 1}")
                    port += 1
                    self.config["port"] = port
                else:
                    logger.error(f"Failed to start server: {e}")
                    raise
            except KeyboardInterrupt:
                logger.info("Server stopped by user")
                break
            except Exception as e:
                logger.error(f"Server error: {e}")
                break
        
        # Shutdown server if it's running
        if self.server:
            self.server.shutdown()
    
    def stop(self):
        """Stop the server and collection thread."""
        logger.info("Stopping dashboard server")
        
        # Stop the server
        if self.server:
            self.server.shutdown()
            
        # Thread will stop automatically since it's a daemon

def main():
    """Main entry point for the dashboard server."""
    parser = argparse.ArgumentParser(description="Quantum Security Metrics Dashboard Server")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--host", help="Host to bind server to")
    parser.add_argument("--port", type=int, help="Port to listen on")
    parser.add_argument("--metrics-path", help="Path to metrics directory")
    parser.add_argument("--dashboard-path", help="Path to dashboard directory")
    parser.add_argument("--no-collection", action="store_true", 
                       help="Disable continuous metrics collection")
    
    args = parser.parse_args()
    
    # Initialize server
    server = DashboardServer(args.config)
    
    # Override config from command line
    if args.host:
        server.config["host"] = args.host
    if args.port:
        server.config["port"] = args.port
    if args.metrics_path:
        server.config["metrics_path"] = args.metrics_path
    if args.dashboard_path:
        server.config["dashboard_path"] = args.dashboard_path
    if args.no_collection:
        server.config["enable_continuous_collection"] = False
    
    try:
        # Start server
        server.start_server()
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
    finally:
        # Ensure clean shutdown
        server.stop()

if __name__ == "__main__":
    main() 