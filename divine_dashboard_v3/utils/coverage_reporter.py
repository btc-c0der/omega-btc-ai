#!/usr/bin/env python3

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

# -*- coding: utf-8 -*-
"""
Coverage Reporter Utility
------------------------
Generates coverage reports in multiple formats from test coverage data.
"""

import json
import os
import datetime
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple

class CoverageReporter:
    """Utility for generating coverage reports in multiple formats."""
    
    def __init__(self, 
                 project_name: str = "Divine Dashboard",
                 target_coverage: float = 90.0,
                 report_format: str = "markdown"):
        """
        Initialize the coverage reporter.
        
        Args:
            project_name: Name of the project
            target_coverage: Target coverage percentage (0-100)
            report_format: Format for the report (markdown, html, json)
        """
        self.project_name = project_name
        self.target_coverage = target_coverage
        self.report_format = report_format.lower()
        self.coverage_data = {}
        self.metrics = {
            "total_lines": 0,
            "covered_lines": 0,
            "coverage_percent": 0.0,
            "components": {}
        }
        self.output_dir = Path("coverage_reports")
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    def load_data_from_file(self, filepath: str) -> bool:
        """
        Load coverage data from a JSON file.
        
        Args:
            filepath: Path to the JSON coverage data file
            
        Returns:
            bool: True if loading was successful
        """
        try:
            with open(filepath, 'r') as f:
                self.coverage_data = json.load(f)
            self._calculate_metrics()
            return True
        except Exception as e:
            print(f"Error loading coverage data: {str(e)}")
            return False
    
    def load_data(self, coverage_data: Dict[str, Any]) -> None:
        """
        Load coverage data directly.
        
        Args:
            coverage_data: Dictionary containing coverage data
        """
        self.coverage_data = coverage_data
        self._calculate_metrics()
    
    def _calculate_metrics(self) -> None:
        """Calculate coverage metrics from the loaded data."""
        total_lines = 0
        covered_lines = 0
        components = {}
        
        for component, data in self.coverage_data.items():
            if isinstance(data, dict) and "lines" in data and "covered" in data:
                comp_total = data["lines"]
                comp_covered = data["covered"]
                comp_percent = (comp_covered / comp_total * 100) if comp_total > 0 else 0
                
                components[component] = {
                    "total_lines": comp_total,
                    "covered_lines": comp_covered,
                    "coverage_percent": comp_percent,
                    "status": "good" if comp_percent >= self.target_coverage else "needs_improvement"
                }
                
                total_lines += comp_total
                covered_lines += comp_covered
        
        self.metrics = {
            "total_lines": total_lines,
            "covered_lines": covered_lines,
            "coverage_percent": (covered_lines / total_lines * 100) if total_lines > 0 else 0,
            "components": components
        }
    
    def set_target_coverage(self, target: float) -> None:
        """
        Set the target coverage percentage.
        
        Args:
            target: Target coverage percentage (0-100)
        """
        self.target_coverage = max(0.0, min(100.0, target))
        # Recalculate component status based on new target
        if self.metrics["components"]:
            for comp in self.metrics["components"].values():
                comp["status"] = "good" if comp["coverage_percent"] >= self.target_coverage else "needs_improvement"
    
    def set_report_format(self, format_type: str) -> None:
        """
        Set the report format.
        
        Args:
            format_type: Format for the report (markdown, html, json)
        """
        self.report_format = format_type.lower()
    
    def set_output_dir(self, directory: str) -> None:
        """
        Set the output directory for reports.
        
        Args:
            directory: Directory path for saving reports
        """
        self.output_dir = Path(directory)
    
    def generate_report(self) -> str:
        """
        Generate a report in the specified format.
        
        Returns:
            str: Generated report content
        """
        if self.report_format == "markdown":
            return self._generate_markdown_report()
        elif self.report_format == "html":
            return self._generate_html_report()
        elif self.report_format == "json":
            return self._generate_json_report()
        else:
            return self._generate_markdown_report()  # Default to markdown
    
    def _generate_markdown_report(self) -> str:
        """
        Generate a markdown format report.
        
        Returns:
            str: Markdown report content
        """
        report = [
            f"# {self.project_name} Coverage Report",
            f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Summary",
            f"- Total Lines: {self.metrics['total_lines']}",
            f"- Covered Lines: {self.metrics['covered_lines']}",
            f"- Overall Coverage: {self.metrics['coverage_percent']:.2f}%",
            f"- Target Coverage: {self.target_coverage:.2f}%",
            f"- Status: {'✅ Target Met' if self.metrics['coverage_percent'] >= self.target_coverage else '⚠️ Below Target'}",
            "",
            "## Component Coverage",
            "",
            "| Component | Lines | Covered | Coverage % | Status |",
            "|-----------|-------|---------|------------|--------|"
        ]
        
        # Sort components by coverage percentage (ascending)
        sorted_components = sorted(
            self.metrics["components"].items(),
            key=lambda x: x[1]["coverage_percent"]
        )
        
        for component, data in sorted_components:
            status_icon = "✅" if data["status"] == "good" else "⚠️"
            report.append(
                f"| {component} | {data['total_lines']} | {data['covered_lines']} | "
                f"{data['coverage_percent']:.2f}% | {status_icon} |"
            )
        
        report.append("")
        report.append("## Recommendations")
        report.append("")
        
        below_target = [c for c, d in sorted_components if d["status"] == "needs_improvement"]
        if below_target:
            report.append("The following components need improvement to reach the target coverage:")
            for component in below_target:
                report.append(f"- {component}")
        else:
            report.append("All components have met or exceeded the target coverage. Great job!")
        
        report.append("")
        report.append("---")
        report.append(f"*Generated automatically by Coverage Reporter v1.0*")
        
        return "\n".join(report)
    
    def _generate_html_report(self) -> str:
        """
        Generate an HTML format report.
        
        Returns:
            str: HTML report content
        """
        overall_status_class = "success" if self.metrics["coverage_percent"] >= self.target_coverage else "warning"
        
        sorted_components = sorted(
            self.metrics["components"].items(),
            key=lambda x: x[1]["coverage_percent"]
        )
        
        component_rows = []
        for component, data in sorted_components:
            status_class = "success" if data["status"] == "good" else "warning"
            component_rows.append(f"""
            <tr>
                <td>{component}</td>
                <td>{data['total_lines']}</td>
                <td>{data['covered_lines']}</td>
                <td>
                    <div class="progress">
                        <div class="progress-bar bg-{status_class}" 
                             role="progressbar" 
                             style="width: {data['coverage_percent']}%"
                             aria-valuenow="{data['coverage_percent']}" 
                             aria-valuemin="0" 
                             aria-valuemax="100">
                            {data['coverage_percent']:.2f}%
                        </div>
                    </div>
                </td>
                <td><span class="badge bg-{status_class}">{data['status'].replace('_', ' ').title()}</span></td>
            </tr>
            """)
        
        below_target = [c for c, d in sorted_components if d["status"] == "needs_improvement"]
        recommendations = ""
        if below_target:
            recommendations += "<p>The following components need improvement to reach the target coverage:</p>"
            recommendations += "<ul>"
            for component in below_target:
                recommendations += f"<li>{component}</li>"
            recommendations += "</ul>"
        else:
            recommendations += "<p>All components have met or exceeded the target coverage. Great job!</p>"
        
        html = f"""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{self.project_name} Coverage Report</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{ padding: 20px; }}
                .header {{ margin-bottom: 30px; }}
                .summary-card {{ margin-bottom: 20px; }}
                .table-responsive {{ margin-bottom: 30px; }}
                .footer {{ margin-top: 50px; color: #6c757d; font-size: 0.9rem; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{self.project_name} Coverage Report</h1>
                    <p class="text-muted">Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <div class="card summary-card">
                    <div class="card-header bg-{overall_status_class} text-white">
                        <h5 class="card-title mb-0">Coverage Summary</h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <p><strong>Total Lines:</strong> {self.metrics['total_lines']}</p>
                                <p><strong>Covered Lines:</strong> {self.metrics['covered_lines']}</p>
                            </div>
                            <div class="col-md-6">
                                <p><strong>Overall Coverage:</strong> {self.metrics['coverage_percent']:.2f}%</p>
                                <p><strong>Target Coverage:</strong> {self.target_coverage:.2f}%</p>
                                <p><strong>Status:</strong> 
                                    <span class="badge bg-{overall_status_class}">
                                        {'Target Met' if self.metrics['coverage_percent'] >= self.target_coverage else 'Below Target'}
                                    </span>
                                </p>
                            </div>
                        </div>
                        <div class="progress mt-3">
                            <div class="progress-bar bg-{overall_status_class}" 
                                 role="progressbar" 
                                 style="width: {self.metrics['coverage_percent']}%"
                                 aria-valuenow="{self.metrics['coverage_percent']}" 
                                 aria-valuemin="0" 
                                 aria-valuemax="100">
                                {self.metrics['coverage_percent']:.2f}%
                            </div>
                        </div>
                    </div>
                </div>
                
                <h2>Component Coverage</h2>
                <div class="table-responsive">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                <th>Component</th>
                                <th>Lines</th>
                                <th>Covered</th>
                                <th>Coverage %</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {"".join(component_rows)}
                        </tbody>
                    </table>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <h5 class="card-title mb-0">Recommendations</h5>
                    </div>
                    <div class="card-body">
                        {recommendations}
                    </div>
                </div>
                
                <div class="footer">
                    <hr>
                    <p>Generated automatically by Coverage Reporter v1.0</p>
                </div>
            </div>
            
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        """
        
        return html
    
    def _generate_json_report(self) -> str:
        """
        Generate a JSON format report.
        
        Returns:
            str: JSON report content
        """
        report = {
            "metadata": {
                "project": self.project_name,
                "generated_at": datetime.datetime.now().isoformat(),
                "target_coverage": self.target_coverage
            },
            "summary": {
                "total_lines": self.metrics["total_lines"],
                "covered_lines": self.metrics["covered_lines"],
                "coverage_percent": self.metrics["coverage_percent"],
                "status": "target_met" if self.metrics["coverage_percent"] >= self.target_coverage else "below_target"
            },
            "components": self.metrics["components"],
            "recommendations": {
                "needs_improvement": [
                    comp for comp, data in self.metrics["components"].items() 
                    if data["status"] == "needs_improvement"
                ]
            }
        }
        
        return json.dumps(report, indent=2)
    
    def save_report(self, filename: Optional[str] = None) -> Tuple[bool, str]:
        """
        Save the report to a file.
        
        Args:
            filename: Optional filename for the report
            
        Returns:
            Tuple[bool, str]: Success status and path to the saved file
        """
        if not filename:
            extension = {
                "markdown": "md",
                "html": "html",
                "json": "json"
            }.get(self.report_format, "txt")
            
            filename = f"{self.project_name.lower().replace(' ', '_')}_coverage_{self.timestamp}.{extension}"
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w') as f:
                f.write(self.generate_report())
            return True, str(filepath)
        except Exception as e:
            print(f"Error saving report: {str(e)}")
            return False, ""

    def print_report(self) -> None:
        """Print the report to stdout."""
        print(self.generate_report())


if __name__ == "__main__":
    # Example usage
    reporter = CoverageReporter(
        project_name="Divine Dashboard",
        target_coverage=90.0,
        report_format="markdown"
    )
    
    # Example data - in real usage, this would come from a coverage tool
    example_data = {
        "NFTDashboard": {"lines": 150, "covered": 135},
        "QuantumSecurity": {"lines": 200, "covered": 170},
        "UIComponents": {"lines": 300, "covered": 250},
        "BlockchainIntegration": {"lines": 250, "covered": 210}
    }
    
    reporter.load_data(example_data)
    
    # Command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--json":
            reporter.set_report_format("json")
        elif sys.argv[1] == "--html":
            reporter.set_report_format("html")
    
    if len(sys.argv) > 2:
        try:
            target = float(sys.argv[2])
            reporter.set_target_coverage(target)
        except ValueError:
            pass
    
    # Print to console and save to file
    reporter.print_report()
    success, filepath = reporter.save_report()
    
    if success:
        print(f"\nReport saved to: {filepath}") 