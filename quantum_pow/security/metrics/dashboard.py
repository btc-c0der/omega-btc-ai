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
import json
import yaml
import time
import logging
import datetime
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("qpow_dashboard")

class DashboardGenerator:
    """Generator for quantum security metrics dashboards."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the dashboard generator.
        
        Args:
            config_path: Optional path to configuration file
        """
        self.config = self._load_config(config_path)
        self.metrics_cache = {}
        self.last_refresh = 0
    
    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        default_config = {
            "dashboard_title": "Quantum-Resistant Security Metrics",
            "refresh_interval_seconds": 60,
            "theme": "dark",
            "metrics_path": "quantum_pow/metrics",
            "output_directory": "quantum_pow/security/metrics/dashboard",
            "k8s_namespace": "monitoring",
            "qpow_services": ["quantum-auth", "validator-privacy", "csrf-monitor"],
            "dashboard_sections": [
                "hash_metrics", 
                "auth_metrics", 
                "privacy_metrics", 
                "test_metrics", 
                "performance_metrics",
                "kubernetes_metrics"
            ]
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
    
    def load_metrics(self, filepath: Optional[str] = None) -> Dict[str, Any]:
        """Load the latest metrics from file.
        
        Args:
            filepath: Optional specific file path to load
            
        Returns:
            Dictionary containing metrics data
        """
        # If no specific file, use the latest in the configured directory
        if not filepath:
            metrics_dir = Path(self.config["metrics_path"])
            if not metrics_dir.exists():
                logger.warning(f"Metrics directory {metrics_dir} does not exist")
                return {}
                
            # Find the latest metrics file
            metric_files = sorted(
                [f for f in metrics_dir.glob("metrics_*.json")],
                key=lambda f: f.stat().st_mtime,
                reverse=True
            )
            
            if not metric_files:
                logger.warning("No metrics files found")
                return {}
                
            filepath = metric_files[0]
            
        try:
            with open(filepath, 'r') as f:
                metrics = json.load(f)
                self.metrics_cache = metrics
                self.last_refresh = time.time()
                logger.info(f"Loaded metrics from {filepath}")
                return metrics
        except Exception as e:
            logger.error(f"Error loading metrics from {filepath}: {e}")
            return {}
    
    def generate_html_dashboard(self, output_path: Optional[str] = None) -> str:
        """Generate an HTML dashboard from the metrics data.
        
        Args:
            output_path: Optional path to save the dashboard HTML
            
        Returns:
            Path to the generated dashboard file
        """
        # Ensure we have recent metrics
        now = time.time()
        if now - self.last_refresh > self.config["refresh_interval_seconds"]:
            self.load_metrics()
        
        if not self.metrics_cache:
            logger.error("No metrics data available")
            return ""
            
        # Prepare output path
        if not output_path:
            output_dir = Path(self.config["output_directory"])
            output_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = output_dir / f"qpow_dashboard_{timestamp}.html"
        
        # Generate HTML content
        html_content = self._generate_dashboard_html()
        
        # Write to file
        try:
            with open(output_path, 'w') as f:
                f.write(html_content)
            logger.info(f"Generated HTML dashboard: {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"Error writing dashboard to {output_path}: {e}")
            return ""
    
    def _generate_dashboard_html(self) -> str:
        """Generate the HTML content for the dashboard."""
        metrics = self.metrics_cache
        
        # Start with HTML template
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.config["dashboard_title"]}</title>
    <style>
        :root {{
            --bg-color: {self._get_theme_color('background')};
            --text-color: {self._get_theme_color('text')};
            --header-color: {self._get_theme_color('header')};
            --card-bg: {self._get_theme_color('card')};
            --highlight: {self._get_theme_color('highlight')};
            --success: {self._get_theme_color('success')};
            --warning: {self._get_theme_color('warning')};
            --danger: {self._get_theme_color('danger')};
            --info: {self._get_theme_color('info')};
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
        }}
        
        .dashboard-header {{
            background-color: var(--header-color);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .dashboard-title {{
            font-size: 24px;
            font-weight: bold;
        }}
        
        .metrics-timestamp {{
            font-size: 14px;
            color: var(--info);
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }}
        
        .metric-card {{
            background-color: var(--card-bg);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        .metric-card h2 {{
            margin-top: 0;
            border-bottom: 1px solid var(--highlight);
            padding-bottom: 10px;
            color: var(--highlight);
        }}
        
        .metric-item {{
            margin-bottom: 10px;
        }}
        
        .metric-label {{
            font-weight: bold;
        }}
        
        .metric-value {{
            float: right;
        }}
        
        .score-high {{
            color: var(--success);
        }}
        
        .score-medium {{
            color: var(--warning);
        }}
        
        .score-low {{
            color: var(--danger);
        }}
        
        .overall-score {{
            font-size: 36px;
            text-align: center;
            padding: 20px;
            margin-bottom: 20px;
        }}
        
        /* Progress bar styles */
        .progress-bar {{
            height: 10px;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            margin-top: 5px;
            overflow: hidden;
        }}
        
        .progress-value {{
            height: 100%;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="dashboard-header">
        <div class="dashboard-title">{self.config["dashboard_title"]}</div>
        <div class="metrics-timestamp">Last Updated: {metrics.get("timestamp", "Unknown")}</div>
    </div>
    
    <div class="overall-score">
        <div class="metric-label">Overall Quantum Resistance Score</div>
        <div class="{self._get_score_class(metrics.get('overall_score', 0))}">{self._format_score(metrics.get('overall_score', 0))}</div>
        <div class="progress-bar">
            <div class="progress-value" style="width: {min(100, max(0, metrics.get('overall_score', 0) * 100))}%; background-color: {self._get_progress_color(metrics.get('overall_score', 0))};"></div>
        </div>
    </div>
    
    <div class="metrics-grid">
"""
        
        # Add sections for each metrics category
        for section in self.config["dashboard_sections"]:
            if section in metrics:
                html += self._generate_section_html(section, metrics[section])
        
        # Close HTML template
        html += """    </div>
    
    <script>
        // Auto-refresh the dashboard
        setTimeout(function() {
            location.reload();
        }, """ + str(self.config["refresh_interval_seconds"] * 1000) + """);
    </script>
</body>
</html>"""
        
        return html
    
    def _generate_section_html(self, section_name: str, section_data: Dict[str, Any]) -> str:
        """Generate HTML for a metrics section."""
        # Format section title
        title = section_name.replace("_", " ").title()
        
        html = f"""        <div class="metric-card">
            <h2>{title}</h2>
"""
        
        # Add metrics items
        for key, value in section_data.items():
            # Skip complex nested structures
            if isinstance(value, dict) and len(value) > 5:
                html += f"""            <div class="metric-item">
                <span class="metric-label">{key.replace("_", " ").title()}</span>
                <span class="metric-value">[Complex Data]</span>
            </div>
"""
                continue
                
            if isinstance(value, dict):
                # For small dictionaries, show as list
                html += f"""            <div class="metric-item">
                <span class="metric-label">{key.replace("_", " ").title()}</span>
                <ul>
"""
                for sub_key, sub_value in value.items():
                    html += f"""                    <li>{sub_key.replace("_", " ").title()}: {self._format_value(sub_value)}</li>
"""
                html += """                </ul>
            </div>
"""
            elif isinstance(value, list):
                # For lists, join as comma-separated
                html += f"""            <div class="metric-item">
                <span class="metric-label">{key.replace("_", " ").title()}</span>
                <span class="metric-value">{", ".join(str(v) for v in value)}</span>
            </div>
"""
            else:
                # For simple values
                value_class = ""
                if "score" in key.lower() or "ratio" in key.lower() or "factor" in key.lower():
                    value_class = f' class="{self._get_score_class(value)}"'
                
                html += f"""            <div class="metric-item">
                <span class="metric-label">{key.replace("_", " ").title()}</span>
                <span class="metric-value"{value_class}>{self._format_value(value)}</span>
            </div>
"""
                
                # Add progress bar for scores
                if "score" in key.lower() or "ratio" in key.lower() or "factor" in key.lower():
                    try:
                        score = float(value)
                        html += f"""            <div class="progress-bar">
                <div class="progress-value" style="width: {min(100, max(0, score * 100))}%; background-color: {self._get_progress_color(score)};"></div>
            </div>
"""
                    except (ValueError, TypeError):
                        pass
        
        html += """        </div>
"""
        return html
    
    def _format_value(self, value: Any) -> str:
        """Format a value for display."""
        if isinstance(value, float):
            if value < 0.01:
                return f"{value:.6f}"
            elif value < 1:
                return f"{value:.4f}"
            elif value < 10:
                return f"{value:.2f}"
            else:
                return f"{value:.1f}"
        elif isinstance(value, bool):
            return "✅" if value else "❌"
        return str(value)
    
    def _format_score(self, score: float) -> str:
        """Format a score value."""
        try:
            return f"{float(score):.2f} / 1.00"
        except (ValueError, TypeError):
            return str(score)
    
    def _get_score_class(self, score: float) -> str:
        """Get CSS class based on score value."""
        try:
            score = float(score)
            if score >= 0.8:
                return "score-high"
            elif score >= 0.5:
                return "score-medium"
            else:
                return "score-low"
        except (ValueError, TypeError):
            return ""
    
    def _get_progress_color(self, score: float) -> str:
        """Get progress bar color based on score value."""
        try:
            score = float(score)
            if score >= 0.8:
                return "#4caf50"  # Green
            elif score >= 0.5:
                return "#ff9800"  # Orange
            else:
                return "#f44336"  # Red
        except (ValueError, TypeError):
            return "#757575"  # Gray
    
    def _get_theme_color(self, element: str) -> str:
        """Get color based on theme and element."""
        if self.config["theme"] == "dark":
            theme_colors = {
                "background": "#1e1e2e",
                "text": "#cdd6f4",
                "header": "#313244",
                "card": "#313244",
                "highlight": "#89b4fa",
                "success": "#a6e3a1",
                "warning": "#f9e2af",
                "danger": "#f38ba8",
                "info": "#89dceb"
            }
        else:  # light theme
            theme_colors = {
                "background": "#f5f5f5",
                "text": "#333333",
                "header": "#e0e0e0",
                "card": "#ffffff",
                "highlight": "#1a73e8",
                "success": "#4caf50",
                "warning": "#ff9800",
                "danger": "#f44336", 
                "info": "#2196f3"
            }
        
        return theme_colors.get(element, "#888888")
    
    def generate_k8s_dashboard(self, output_path: Optional[str] = None) -> str:
        """Generate a Kubernetes dashboard ConfigMap.
        
        Args:
            output_path: Optional path to save the dashboard YAML
            
        Returns:
            Path to the generated dashboard file
        """
        # Ensure we have recent metrics
        now = time.time()
        if now - self.last_refresh > self.config["refresh_interval_seconds"]:
            self.load_metrics()
        
        if not self.metrics_cache:
            logger.error("No metrics data available")
            return ""
            
        # Prepare output path
        if not output_path:
            output_dir = Path(self.config["output_directory"])
            output_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = output_dir / f"k8s_dashboard_{timestamp}.yaml"
        
        # Generate dashboard ConfigMap
        dashboard = {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {
                "name": "qpow-security-dashboard",
                "namespace": self.config["k8s_namespace"],
                "labels": {
                    "grafana_dashboard": "qpow-security",
                    "app.kubernetes.io/part-of": "qpow-security"
                }
            },
            "data": {
                "dashboard.json": json.dumps(self._generate_grafana_dashboard_json(), indent=2)
            }
        }
        
        # Write to file
        try:
            with open(output_path, 'w') as f:
                yaml.dump(dashboard, f, sort_keys=False)
            logger.info(f"Generated Kubernetes dashboard: {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"Error writing dashboard to {output_path}: {e}")
            return ""
    
    def _generate_grafana_dashboard_json(self) -> Dict[str, Any]:
        """Generate Grafana dashboard JSON configuration."""
        metrics = self.metrics_cache
        
        # Base dashboard structure
        dashboard = {
            "annotations": {
                "list": [
                    {
                        "builtIn": 1,
                        "datasource": "-- Grafana --",
                        "enable": True,
                        "hide": True,
                        "iconColor": "rgba(0, 211, 255, 1)",
                        "name": "Annotations & Alerts",
                        "type": "dashboard"
                    }
                ]
            },
            "editable": True,
            "gnetId": None,
            "graphTooltip": 0,
            "id": None,
            "links": [],
            "panels": [],
            "refresh": f"{self.config['refresh_interval_seconds']}s",
            "schemaVersion": 27,
            "style": "dark",
            "tags": ["qpow", "security"],
            "templating": {"list": []},
            "time": {
                "from": "now-6h",
                "to": "now"
            },
            "timepicker": {},
            "timezone": "",
            "title": self.config["dashboard_title"],
            "uid": "qpow-security",
            "version": 1
        }
        
        # Add overall score panel
        dashboard["panels"].append({
            "id": 1,
            "title": "Overall Quantum Resistance Score",
            "type": "gauge",
            "datasource": None,
            "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
            "fieldConfig": {
                "defaults": {
                    "mappings": [],
                    "thresholds": {
                        "mode": "absolute",
                        "steps": [
                            {"color": "red", "value": None},
                            {"color": "orange", "value": 0.5},
                            {"color": "green", "value": 0.8}
                        ]
                    },
                    "color": {"mode": "thresholds"},
                    "unit": "percentunit",
                    "min": 0,
                    "max": 1
                }
            },
            "options": {
                "reduceOptions": {
                    "values": False,
                    "calcs": ["lastNotNull"],
                    "fields": ""
                },
                "showThresholdLabels": False,
                "showThresholdMarkers": True
            },
            "targets": [
                {
                    "refId": "A",
                    "target": "overall_score",
                    "type": "timeseries",
                    "datasource": "JSON API",
                    "data": metrics.get("overall_score", 0)
                }
            ]
        })
        
        # Add panels for each metrics category
        panel_id = 2
        y_position = 8
        
        for section in self.config["dashboard_sections"]:
            if section in metrics:
                section_data = metrics[section]
                
                # Get top metrics for section
                top_metrics = {}
                for key, value in section_data.items():
                    if isinstance(value, (int, float)) and not isinstance(value, bool):
                        if "score" in key.lower() or "ratio" in key.lower() or "factor" in key.lower():
                            top_metrics[key] = value
                
                # Add section panel with top metrics
                if top_metrics:
                    dashboard["panels"].append({
                        "id": panel_id,
                        "title": section.replace("_", " ").title(),
                        "type": "gauge",
                        "datasource": None,
                        "gridPos": {"h": 8, "w": 12, "x": panel_id % 2 * 12, "y": y_position},
                        "fieldConfig": {
                            "defaults": {
                                "mappings": [],
                                "thresholds": {
                                    "mode": "absolute",
                                    "steps": [
                                        {"color": "red", "value": None},
                                        {"color": "orange", "value": 0.5},
                                        {"color": "green", "value": 0.8}
                                    ]
                                },
                                "color": {"mode": "thresholds"},
                                "unit": "percentunit",
                                "min": 0,
                                "max": 1
                            }
                        },
                        "options": {
                            "reduceOptions": {
                                "values": False,
                                "calcs": ["lastNotNull"],
                                "fields": ""
                            },
                            "showThresholdLabels": False,
                            "showThresholdMarkers": True,
                            "orientation": "auto"
                        },
                        "targets": [
                            {
                                "refId": chr(65 + i),
                                "target": key,
                                "type": "timeseries",
                                "datasource": "JSON API",
                                "data": value
                            }
                            for i, (key, value) in enumerate(list(top_metrics.items())[:3])
                        ]
                    })
                    
                    panel_id += 1
                    if panel_id % 2 == 0:
                        y_position += 8
        
        return dashboard

def main():
    """Main entry point for dashboard generation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Quantum Security Metrics Dashboard Generator")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--metrics", help="Path to metrics JSON file")
    parser.add_argument("--output", help="Output directory for dashboards")
    parser.add_argument("--format", choices=["html", "k8s", "both"], default="both", 
                       help="Dashboard format to generate (html, k8s, or both)")
    parser.add_argument("--theme", choices=["light", "dark"], default="dark",
                       help="Dashboard theme (light or dark)")
    
    args = parser.parse_args()
    
    # Initialize dashboard generator
    dashboard_gen = DashboardGenerator(args.config)
    
    # Override config settings from command line
    if args.output:
        dashboard_gen.config["output_directory"] = args.output
    if args.theme:
        dashboard_gen.config["theme"] = args.theme
    
    # Load metrics if specified
    if args.metrics:
        dashboard_gen.load_metrics(args.metrics)
    else:
        dashboard_gen.load_metrics()
    
    # Generate dashboards based on format
    if args.format in ["html", "both"]:
        html_path = dashboard_gen.generate_html_dashboard()
        if html_path:
            print(f"HTML dashboard generated: {html_path}")
    
    if args.format in ["k8s", "both"]:
        k8s_path = dashboard_gen.generate_k8s_dashboard()
        if k8s_path:
            print(f"Kubernetes dashboard generated: {k8s_path}")

if __name__ == "__main__":
    main() 