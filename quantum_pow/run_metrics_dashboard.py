#!/usr/bin/env python3
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
import argparse
import time
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def main():
    """Run the quantum security metrics dashboard system."""
    parser = argparse.ArgumentParser(
        description="Quantum-Resistant Security Metrics Dashboard",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Main command groups
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Collect command
    collect_parser = subparsers.add_parser("collect", help="Collect metrics")
    collect_parser.add_argument("--config", help="Path to configuration file")
    collect_parser.add_argument("--output", default="quantum_pow/metrics", help="Output directory")
    collect_parser.add_argument("--continuous", action="store_true", help="Run in continuous mode")
    collect_parser.add_argument("--interval", type=int, default=300, help="Collection interval in seconds")
    
    # Dashboard command
    dashboard_parser = subparsers.add_parser("dashboard", help="Generate dashboard")
    dashboard_parser.add_argument("--config", help="Path to configuration file")
    dashboard_parser.add_argument("--metrics", help="Path to metrics file")
    dashboard_parser.add_argument("--output", default="quantum_pow/security/metrics/dashboard", help="Output directory")
    dashboard_parser.add_argument("--theme", choices=["dark", "light"], default="dark", help="Dashboard theme")
    dashboard_parser.add_argument("--format", choices=["html", "k8s", "both"], default="html", help="Dashboard format")
    
    # Server command
    server_parser = subparsers.add_parser("server", help="Run dashboard server")
    server_parser.add_argument("--config", help="Path to configuration file")
    server_parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    server_parser.add_argument("--port", type=int, default=8080, help="Port to listen on")
    server_parser.add_argument("--metrics-path", default="quantum_pow/metrics", help="Path to metrics directory")
    server_parser.add_argument("--dashboard-path", default="quantum_pow/security/metrics/dashboard", help="Path to dashboard directory")
    server_parser.add_argument("--no-collection", action="store_true", help="Disable continuous collection")
    
    # K8s command
    k8s_parser = subparsers.add_parser("k8s", help="Kubernetes operations")
    k8s_parser.add_argument("--namespace", default="default", help="Kubernetes namespace")
    k8s_parser.add_argument("--config", help="Path to configuration file")
    k8s_parser.add_argument("--output", help="Path to save metrics")
    
    # Demo command
    demo_parser = subparsers.add_parser("demo", help="Run metrics dashboard demo")
    demo_parser.add_argument("--port", type=int, default=8080, help="Port to run server on")
    demo_parser.add_argument("--metrics-dir", default="quantum_pow/metrics", help="Path to metrics directory")
    demo_parser.add_argument("--dashboard-dir", default="quantum_pow/security/metrics/dashboard", help="Path to dashboard directory")
    demo_parser.add_argument("--interval", type=int, default=60, help="Update interval in seconds")
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no command specified, show help
    if not args.command:
        parser.print_help()
        return
    
    # Import necessary modules based on command
    if args.command == "collect":
        from security.metrics.collector import MetricsCollector
        
        collector = MetricsCollector(args.config)
        if args.output:
            collector.config["output_directory"] = args.output
            
        if args.continuous:
            print(f"Starting continuous metrics collection every {args.interval} seconds")
            print("Press Ctrl+C to stop")
            
            try:
                collector.start_continuous_collection(args.interval)
            except KeyboardInterrupt:
                print("\nMetrics collection stopped by user")
        else:
            print("Collecting metrics...")
            metrics = collector.collect_all_metrics()
            filepath = collector.save_metrics()
            print(f"Metrics saved to {filepath}")
    
    elif args.command == "dashboard":
        from security.metrics.dashboard import DashboardGenerator
        
        print("Generating dashboard...")
        dashboard_gen = DashboardGenerator(args.config)
        
        if args.output:
            dashboard_gen.config["output_directory"] = args.output
        dashboard_gen.config["theme"] = args.theme
        
        if args.metrics:
            dashboard_gen.load_metrics(args.metrics)
        else:
            dashboard_gen.load_metrics()
            
        if args.format in ["html", "both"]:
            html_path = dashboard_gen.generate_html_dashboard()
            if html_path:
                print(f"HTML dashboard generated: {html_path}")
        
        if args.format in ["k8s", "both"]:
            k8s_path = dashboard_gen.generate_k8s_dashboard()
            if k8s_path:
                print(f"Kubernetes dashboard generated: {k8s_path}")
    
    elif args.command == "server":
        from security.metrics.dashboard_server import DashboardServer
        
        print(f"Starting dashboard server on http://{args.host}:{args.port}/")
        print("Press Ctrl+C to stop")
        
        server = DashboardServer(args.config)
        
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
            server.start_server()
        except KeyboardInterrupt:
            print("\nServer stopped by user")
        finally:
            server.stop()
    
    elif args.command == "k8s":
        from security.metrics.k8s_metrics_integration import KubernetesMetricsIntegration
        
        print(f"Collecting Kubernetes metrics from namespace: {args.namespace}")
        k8s_metrics = KubernetesMetricsIntegration(args.namespace, args.config)
        
        metrics = k8s_metrics.collect_all_metrics()
        
        if args.output:
            filepath = k8s_metrics.save_metrics(metrics, args.output)
            print(f"Kubernetes metrics saved to {filepath}")
        else:
            print("Kubernetes metrics collected (not saved to file):")
            import json
            print(json.dumps(metrics, indent=2))
    
    elif args.command == "demo":
        print("Starting metrics dashboard demo...")
        
        try:
            from security.metrics.run_dashboard_demo import main as run_demo
            
            # Override sys.argv to pass args to the demo
            sys.argv = [
                sys.argv[0],
                "--port", str(args.port),
                "--metrics-dir", args.metrics_dir,
                "--dashboard-dir", args.dashboard_dir,
                "--update-interval", str(args.interval)
            ]
            
            run_demo()
        except ImportError:
            print("Error: Could not import demo module.")
            print("Make sure you're running from the project root directory.")

if __name__ == "__main__":
    main() 