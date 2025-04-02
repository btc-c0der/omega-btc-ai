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
import argparse
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from security.metrics_analyzer import SecurityMetricsAnalyzer

class MetricsCLI:
    """Command-line interface for quantum security metrics analysis."""
    
    def __init__(self):
        """Initialize the CLI with argument parser and commands."""
        self.args = None
        self.analyzer = None
        self.metrics = None
        self.parser = self._setup_argument_parser()
        
    def _setup_argument_parser(self) -> argparse.ArgumentParser:
        """Set up the argument parser with all available commands."""
        parser = argparse.ArgumentParser(
            description="Quantum Security Metrics CLI - Security Analysis for qPoW",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Example commands:
  metrics_cli.py run --all
  metrics_cli.py run --hash --auth
  metrics_cli.py report --latest
  metrics_cli.py report --file metrics/qpow_security_metrics_20250401_123045.json
  metrics_cli.py generate --k8s-dashboard
            """
        )
        
        subparsers = parser.add_subparsers(dest="command", help="Command to execute")
        
        # Run command - for running analysis
        run_parser = subparsers.add_parser("run", help="Run security metrics analysis")
        run_parser.add_argument("--all", action="store_true", help="Run all analyses")
        run_parser.add_argument("--hash", action="store_true", help="Analyze hash security")
        run_parser.add_argument("--auth", action="store_true", help="Analyze auth security")
        run_parser.add_argument("--privacy", action="store_true", help="Analyze validator privacy")
        run_parser.add_argument("--test", action="store_true", help="Analyze test coverage")
        run_parser.add_argument("--performance", action="store_true", help="Analyze performance metrics")
        run_parser.add_argument("--kubernetes", action="store_true", help="Analyze Kubernetes deployment")
        run_parser.add_argument("--output", help="Path to save output metrics")
        run_parser.add_argument("--config", help="Path to configuration file")
        
        # Report command - for displaying results
        report_parser = subparsers.add_parser("report", help="Generate report from metrics")
        report_parser.add_argument("--latest", action="store_true", help="Use most recent metrics file")
        report_parser.add_argument("--file", help="Path to metrics file")
        report_parser.add_argument("--format", choices=["text", "json", "markdown"], 
                                 default="text", help="Output format")
        
        # Generate command - for creating visualizations
        generate_parser = subparsers.add_parser("generate", help="Generate visualizations or dashboards")
        generate_parser.add_argument("--k8s-dashboard", action="store_true", help="Generate Kubernetes dashboard")
        generate_parser.add_argument("--security-report", action="store_true", help="Generate security report")
        generate_parser.add_argument("--output-dir", default="quantum_pow/reports", 
                                   help="Directory for generated files")
        generate_parser.add_argument("--template", help="Path to template file")
        
        # Watch command - for continuous monitoring
        watch_parser = subparsers.add_parser("watch", help="Watch for metrics changes")
        watch_parser.add_argument("--interval", type=int, default=60, 
                                help="Interval in seconds between checks")
        watch_parser.add_argument("--metrics", choices=["all", "hash", "auth", "privacy", "test", 
                                                      "performance", "kubernetes"],
                                default="all", help="Metrics to watch")
        watch_parser.add_argument("--alert-threshold", type=float, default=0.8, 
                                help="Alert threshold (0.0-1.0)")
        
        return parser
        
    def parse_args(self, args=None):
        """Parse command-line arguments."""
        self.args = self.parser.parse_args(args)
        
        # Default to 'all' if no specific metrics are selected for 'run'
        if self.args.command == "run" and not any([
            getattr(self.args, metric, False) 
            for metric in ["all", "hash", "auth", "privacy", "test", "performance", "kubernetes"]
        ]):
            self.args.all = True
            
        return self.args
        
    def run_command(self):
        """Execute the command specified by the arguments."""
        if not self.args:
            self.parse_args()
            
        if self.args.command == "run":
            return self._handle_run()
        elif self.args.command == "report":
            return self._handle_report()
        elif self.args.command == "generate":
            return self._handle_generate()
        elif self.args.command == "watch":
            return self._handle_watch()
        else:
            self.parser.print_help()
            return 1
    
    def _handle_run(self) -> int:
        """Handle the 'run' command to analyze security metrics."""
        print("🔒 QUANTUM SECURITY METRICS ANALYSIS 🔒")
        print("=" * 50)
        
        # Initialize the metrics analyzer
        self.analyzer = SecurityMetricsAnalyzer(self.args.config)
        
        # Determine which analyses to run
        if self.args.all:
            self.metrics = self.analyzer.analyze_all_metrics()
        else:
            # Run individual analyses based on flags
            if self.args.hash:
                self.analyzer.analyze_hash_security()
            if self.args.auth:
                self.analyzer.analyze_auth_security()
            if self.args.privacy:
                self.analyzer.analyze_validator_privacy()
            if self.args.test:
                self.analyzer.analyze_test_coverage()
            if self.args.performance:
                self.analyzer.analyze_performance_metrics()
            if self.args.kubernetes:
                self.analyzer.analyze_kubernetes_metrics()
            
            # Calculate score even with partial metrics
            if self.analyzer.metrics:
                self.analyzer.metrics["overall_score"] = self.analyzer._calculate_overall_score()
                self.metrics = self.analyzer.metrics
        
        # Print summary
        if self.metrics:
            self.analyzer.print_summary()
            
            # Save metrics if output is specified
            if self.args.output:
                saved_path = self.analyzer.save_metrics(self.args.output)
                print(f"Metrics saved to: {saved_path}")
            else:
                saved_path = self.analyzer.save_metrics()
                
            return 0
        else:
            print("No metrics were collected!")
            return 1
    
    def _handle_report(self) -> int:
        """Handle the 'report' command to display metrics."""
        print("📊 QUANTUM SECURITY METRICS REPORT 📊")
        print("=" * 50)
        
        # Find metrics file
        metrics_file = self._get_metrics_file()
        if not metrics_file:
            print("No metrics file found!")
            return 1
            
        print(f"Using metrics file: {metrics_file}")
        
        # Load metrics
        try:
            with open(metrics_file, 'r') as f:
                self.metrics = json.load(f)
        except Exception as e:
            print(f"Error loading metrics file: {e}")
            return 1
            
        # Generate report in specified format
        if self.args.format == "text":
            self._generate_text_report()
        elif self.args.format == "json":
            self._generate_json_report()
        elif self.args.format == "markdown":
            self._generate_markdown_report()
            
        return 0
    
    def _get_metrics_file(self) -> Optional[str]:
        """Get the path to the metrics file based on arguments."""
        if self.args.file:
            if os.path.exists(self.args.file):
                return self.args.file
            else:
                print(f"Specified file not found: {self.args.file}")
                return None
        elif self.args.latest:
            # Find the most recent metrics file
            metrics_dir = "quantum_pow/metrics"
            if not os.path.exists(metrics_dir):
                print(f"Metrics directory not found: {metrics_dir}")
                return None
                
            # Get all JSON files
            json_files = [f for f in os.listdir(metrics_dir) if f.endswith('.json')]
            if not json_files:
                print(f"No metrics files found in {metrics_dir}")
                return None
                
            # Sort by modification time and get the latest
            latest_file = max(json_files, key=lambda f: os.path.getmtime(os.path.join(metrics_dir, f)))
            return os.path.join(metrics_dir, latest_file)
        
        return None
    
    def _generate_text_report(self):
        """Generate a text report from the metrics."""
        print("\n🔒 QUANTUM SECURITY METRICS SUMMARY 🔒")
        print("-" * 50)
        
        # Overall score
        score = self.metrics.get("overall_score", 0)
        print(f"Overall Quantum Resistance Score: {score:.4f}")
        
        # Hash metrics
        hash_metrics = self.metrics.get("hash_metrics", {})
        if hash_metrics:
            print("\n📈 HASH SECURITY METRICS:")
            print(f"  Hash Output Size: {hash_metrics.get('output_size_bits', 0)} bits")
            print(f"  Avalanche Effect: {hash_metrics.get('avalanche_effect_percentage', 'unknown')}")
            print(f"  Grover's Resistance Factor: {hash_metrics.get('grovers_resistance_factor', 0):.2e}")
        
        # Auth metrics
        auth_metrics = self.metrics.get("auth_metrics", {})
        if auth_metrics:
            print("\n🔑 AUTHENTICATION METRICS:")
            print(f"  One-shot Signatures: {auth_metrics.get('one_shot_signatures_implemented', False)}")
            print(f"  Supported Schemes: {', '.join(auth_metrics.get('supported_schemes', []))}")
            print(f"  Key Rotation Period: {auth_metrics.get('key_rotation_period_days', 0)} days")
            print(f"  Token Expiration: {auth_metrics.get('token_expiration_minutes', 0)} minutes")
        
        # Privacy metrics
        privacy_metrics = self.metrics.get("privacy_metrics", {})
        if privacy_metrics:
            print("\n🕵️ PRIVACY METRICS:")
            print(f"  Dandelion Routing: {privacy_metrics.get('dandelion_implemented', False)}")
            print(f"  Timing Randomization: {privacy_metrics.get('timing_randomization', False)}")
            print(f"  Peer Rotation: {privacy_metrics.get('peer_rotation_hours', 0)} hours")
            print(f"  Deanonymization Resistance Factor: {privacy_metrics.get('deanonymization_resistance_factor', 0)}x")
        
        # Test metrics
        test_metrics = self.metrics.get("test_metrics", {})
        if test_metrics:
            print("\n🧪 TEST COVERAGE METRICS:")
            categories = test_metrics.get("categories", {})
            for category, data in categories.items():
                print(f"  {category.replace('_', ' ').title()}: {data.get('count', 0)} tests, {data.get('coverage', 0):.1f}% coverage")
            print(f"  Total: {test_metrics.get('overall', {}).get('total_tests', 0)} tests, {test_metrics.get('overall', {}).get('overall_coverage', 0):.1f}% coverage")
        
        # Performance metrics
        perf_metrics = self.metrics.get("performance_metrics", {})
        if perf_metrics:
            print("\n⚡ PERFORMANCE METRICS:")
            hash_comp = perf_metrics.get("hash_computation", {})
            print(f"  Hash Computation: {hash_comp.get('slowdown_factor', 0):.2f}x slower than classical")
            print(f"  System Overhead: {perf_metrics.get('system_overhead', 0)*100:.1f}%")
        
        # K8s metrics
        k8s_metrics = self.metrics.get("kubernetes_metrics", {})
        if k8s_metrics:
            print("\n☸️ KUBERNETES METRICS:")
            deployments = k8s_metrics.get("deployments", {})
            for name, data in deployments.items():
                print(f"  {name.replace('_', '-')}: {data.get('replicas', 0)} replicas, status: {data.get('status', 'unknown')}")
            print(f"  High Availability: {k8s_metrics.get('high_availability', False)}")
            print(f"  Network Policies: {k8s_metrics.get('network_policies', False)}")
            
        print("\n" + "-" * 50)
    
    def _generate_json_report(self):
        """Generate a JSON report from the metrics."""
        print(json.dumps(self.metrics, indent=2))
    
    def _generate_markdown_report(self):
        """Generate a Markdown report from the metrics."""
        # Simplified markdown report
        md_lines = []
        md_lines.append("# Quantum Security Metrics Report")
        md_lines.append("")
        md_lines.append(f"_Generated: {self.metrics.get('timestamp', datetime.datetime.now().isoformat())}_")
        md_lines.append("")
        
        # Overall score
        score = self.metrics.get("overall_score", 0)
        md_lines.append(f"## Overall Quantum Resistance Score: {score:.4f}")
        md_lines.append("")
        
        # Hash metrics
        hash_metrics = self.metrics.get("hash_metrics", {})
        if hash_metrics:
            md_lines.append("## Hash Security Metrics")
            md_lines.append("")
            md_lines.append("| Metric | Value |")
            md_lines.append("|--------|-------|")
            md_lines.append(f"| Hash Output Size | {hash_metrics.get('output_size_bits', 0)} bits |")
            md_lines.append(f"| Avalanche Effect | {hash_metrics.get('avalanche_effect_percentage', 'unknown')} |")
            md_lines.append(f"| Grover's Resistance Factor | {hash_metrics.get('grovers_resistance_factor', 0):.2e} |")
            md_lines.append("")
        
        # Print the markdown report
        print("\n".join(md_lines))
    
    def _handle_generate(self) -> int:
        """Handle the 'generate' command to create visualizations or dashboards."""
        print("🎨 GENERATING QUANTUM SECURITY VISUALIZATIONS 🎨")
        print("=" * 50)
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.args.output_dir):
            os.makedirs(self.args.output_dir)
        
        # Load metrics
        metrics_file = self._get_metrics_file()
        if not metrics_file:
            print("No metrics file found! Running new analysis...")
            self.analyzer = SecurityMetricsAnalyzer()
            self.metrics = self.analyzer.analyze_all_metrics()
        else:
            try:
                with open(metrics_file, 'r') as f:
                    self.metrics = json.load(f)
            except Exception as e:
                print(f"Error loading metrics file: {e}")
                return 1
        
        # Generate requested outputs
        if self.args.k8s_dashboard:
            self._generate_k8s_dashboard()
        
        if self.args.security_report:
            self._generate_security_report()
            
        return 0
    
    def _generate_k8s_dashboard(self):
        """Generate a Kubernetes dashboard configuration."""
        print("Generating Kubernetes dashboard...")
        
        # Simple K8s dashboard manifest
        dashboard = {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {
                "name": "quantum-security-dashboard",
                "namespace": "default",
                "labels": {
                    "app": "quantum-security-dashboard"
                }
            },
            "data": {
                "dashboard.json": json.dumps({
                    "title": "Quantum Security Dashboard",
                    "timestamp": self.metrics.get("timestamp", ""),
                    "score": self.metrics.get("overall_score", 0),
                    "metrics": {
                        "hash": self.metrics.get("hash_metrics", {}),
                        "auth": self.metrics.get("auth_metrics", {}),
                        "privacy": self.metrics.get("privacy_metrics", {})
                    }
                }, indent=2)
            }
        }
        
        # Write dashboard to file
        dashboard_file = os.path.join(self.args.output_dir, "quantum_security_dashboard.yaml")
        with open(dashboard_file, 'w') as f:
            yaml_content = []
            yaml_content.append("apiVersion: " + dashboard["apiVersion"])
            yaml_content.append("kind: " + dashboard["kind"])
            yaml_content.append("metadata:")
            yaml_content.append("  name: " + dashboard["metadata"]["name"])
            yaml_content.append("  namespace: " + dashboard["metadata"]["namespace"])
            yaml_content.append("  labels:")
            for k, v in dashboard["metadata"]["labels"].items():
                yaml_content.append(f"    {k}: {v}")
            yaml_content.append("data:")
            yaml_content.append("  dashboard.json: |")
            # Indent the JSON content
            for line in dashboard["data"]["dashboard.json"].split("\n"):
                yaml_content.append("    " + line)
            
            f.write("\n".join(yaml_content))
            
        print(f"Kubernetes dashboard written to: {dashboard_file}")
    
    def _generate_security_report(self):
        """Generate a detailed security report."""
        print("Generating security report...")
        
        # Generate markdown report
        report_file = os.path.join(self.args.output_dir, "quantum_security_report.md")
        
        with open(report_file, 'w') as f:
            f.write("# 🔒 Quantum Security Analysis Report 🔒\n\n")
            f.write(f"_Generated: {self.metrics.get('timestamp', datetime.datetime.now().isoformat())}_\n\n")
            
            # Overall score
            score = self.metrics.get("overall_score", 0)
            f.write(f"## Overall Quantum Resistance Score: {score:.4f}\n\n")
            
            # Add sections for each metric category
            categories = [
                ("Hash Security", "hash_metrics"),
                ("Authentication Security", "auth_metrics"),
                ("Validator Privacy", "privacy_metrics"),
                ("Test Coverage", "test_metrics"),
                ("Performance", "performance_metrics"),
                ("Kubernetes Deployment", "kubernetes_metrics")
            ]
            
            for title, key in categories:
                if key in self.metrics:
                    f.write(f"## {title}\n\n")
                    f.write("```json\n")
                    f.write(json.dumps(self.metrics[key], indent=2))
                    f.write("\n```\n\n")
            
        print(f"Security report written to: {report_file}")
    
    def _handle_watch(self) -> int:
        """Handle the 'watch' command for continuous monitoring."""
        import time
        
        print("👀 WATCHING QUANTUM SECURITY METRICS 👀")
        print("=" * 50)
        print(f"Interval: {self.args.interval} seconds")
        print(f"Alert threshold: {self.args.alert_threshold}")
        print(f"Metrics: {self.args.metrics}")
        print("Press Ctrl+C to stop watching.")
        print("-" * 50)
        
        try:
            while True:
                # Run analysis
                analyzer = SecurityMetricsAnalyzer()
                
                if self.args.metrics == "all":
                    metrics = analyzer.analyze_all_metrics()
                else:
                    if self.args.metrics == "hash":
                        analyzer.analyze_hash_security()
                    elif self.args.metrics == "auth":
                        analyzer.analyze_auth_security()
                    elif self.args.metrics == "privacy":
                        analyzer.analyze_validator_privacy()
                    elif self.args.metrics == "test":
                        analyzer.analyze_test_coverage()
                    elif self.args.metrics == "performance":
                        analyzer.analyze_performance_metrics()
                    elif self.args.metrics == "kubernetes":
                        analyzer.analyze_kubernetes_metrics()
                    
                    analyzer.metrics["overall_score"] = analyzer._calculate_overall_score()
                    metrics = analyzer.metrics
                
                # Check if we should alert
                score = metrics.get("overall_score", 0)
                if score < self.args.alert_threshold:
                    print(f"⚠️ ALERT: Score {score:.4f} is below threshold {self.args.alert_threshold}!")
                else:
                    print(f"✅ Score: {score:.4f}")
                
                # Wait for next check
                time.sleep(self.args.interval)
                
        except KeyboardInterrupt:
            print("\nStopped watching.")
            
        return 0

def main():
    """Main entry point for the metrics CLI."""
    cli = MetricsCLI()
    return cli.run_command()

if __name__ == "__main__":
    sys.exit(main()) 