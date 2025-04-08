#!/usr/bin/env python3

"""
DIVINE RASTA TEST DASHBOARD GENERATOR 🌿🔥

Creates a beautiful dashboard showing test metrics, coverage, and performance data
with RASTA divine energy and JAH BLESSING.
"""

import os
import sys
import json
import datetime
import argparse
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from jinja2 import Template
from xml.etree import ElementTree

# Add project root to path for divine imports
project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

# RASTA colors
GREEN = "#52b788"
YELLOW = "#ffb703"
RED = "#e63946"
GOLD = "#ffbd00"
BLACK = "#211a1d"

def parse_coverage_xml(xml_path):
    """Parse coverage XML file with divine wisdom."""
    if not os.path.exists(xml_path):
        print(f"Warning: Coverage file {xml_path} does not exist")
        return {
            "line_rate": 0,
            "branch_rate": 0,
            "complexity": 0,
            "packages": []
        }
    
    tree = ElementTree.parse(xml_path)
    root = tree.getroot()
    
    coverage_data = {
        "line_rate": float(root.attrib.get("line-rate", 0)) * 100,
        "branch_rate": float(root.attrib.get("branch-rate", 0)) * 100,
        "complexity": float(root.attrib.get("complexity", 0)),
        "packages": []
    }
    
    for package in root.findall(".//package"):
        package_data = {
            "name": package.attrib.get("name", ""),
            "line_rate": float(package.attrib.get("line-rate", 0)) * 100,
            "classes": []
        }
        
        for cls in package.findall(".//class"):
            class_name = cls.attrib.get("name", "").split(".")[-1]
            class_data = {
                "name": class_name,
                "line_rate": float(cls.attrib.get("line-rate", 0)) * 100,
                "filename": cls.attrib.get("filename", "")
            }
            package_data["classes"].append(class_data)
            
        coverage_data["packages"].append(package_data)
    
    return coverage_data

def parse_pytest_results(json_path):
    """Parse pytest JSON results with divine insight."""
    if not os.path.exists(json_path):
        print(f"Warning: Pytest results file {json_path} does not exist")
        return {
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "error": 0,
                "pass_percentage": 0
            },
            "tests": []
        }
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Process data into a more usable format
    results = {
        "summary": {
            "total": data.get("summary", {}).get("total", 0),
            "passed": data.get("summary", {}).get("passed", 0),
            "failed": data.get("summary", {}).get("failed", 0),
            "skipped": data.get("summary", {}).get("skipped", 0),
            "error": data.get("summary", {}).get("error", 0),
        },
        "tests": []
    }
    
    if results["summary"]["total"] > 0:
        results["summary"]["pass_percentage"] = (results["summary"]["passed"] / results["summary"]["total"]) * 100
    else:
        results["summary"]["pass_percentage"] = 0
    
    # Extract test details
    for test_id, test_data in data.get("tests", {}).items():
        results["tests"].append({
            "id": test_id,
            "name": test_data.get("name", ""),
            "outcome": test_data.get("outcome", ""),
            "duration": test_data.get("duration", 0),
            "markers": test_data.get("markers", []),
            "file": test_data.get("file", ""),
        })
    
    return results

def create_dashboard(coverage_data, test_results, output_file):
    """Create a divine dashboard with JAH BLESSING."""
    # Create directory for charts if it doesn't exist
    os.makedirs("reports/charts", exist_ok=True)
    
    # Generate coverage chart
    create_coverage_chart(coverage_data)
    
    # Generate test results chart
    create_test_results_chart(test_results)
    
    # Generate package coverage chart
    create_package_coverage_chart(coverage_data)
    
    # Generate test duration chart if tests exist
    if test_results["tests"]:
        create_test_duration_chart(test_results["tests"])
    
    # Generate the HTML dashboard
    with open(output_file, 'w') as f:
        f.write(render_dashboard_html(coverage_data, test_results))
    
    print(f"Divine dashboard generated at {output_file}")

def create_coverage_chart(coverage_data):
    """Create a divine coverage pie chart."""
    plt.figure(figsize=(8, 6))
    
    # Data
    labels = ['Covered', 'Uncovered']
    sizes = [coverage_data["line_rate"], 100 - coverage_data["line_rate"]]
    colors = [GREEN, RED]
    explode = (0.1, 0)
    
    # Create pie chart
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')
    plt.title('Divine Code Coverage', fontsize=16, fontweight='bold')
    
    plt.savefig('reports/charts/coverage_pie.png', bbox_inches='tight')
    plt.close()

def create_test_results_chart(test_results):
    """Create a divine test results chart."""
    plt.figure(figsize=(10, 6))
    
    # Data
    categories = ['Passed', 'Failed', 'Skipped', 'Error']
    values = [
        test_results["summary"]["passed"],
        test_results["summary"]["failed"],
        test_results["summary"]["skipped"],
        test_results["summary"]["error"]
    ]
    colors = [GREEN, RED, YELLOW, BLACK]
    
    # Create bar chart
    plt.bar(categories, values, color=colors)
    plt.title('Divine Test Results', fontsize=16, fontweight='bold')
    plt.ylabel('Number of Tests')
    
    # Add values on top of bars
    for i, v in enumerate(values):
        plt.text(i, v + 0.5, str(v), ha='center')
    
    plt.savefig('reports/charts/test_results.png', bbox_inches='tight')
    plt.close()

def create_package_coverage_chart(coverage_data):
    """Create a divine package coverage chart."""
    packages = coverage_data["packages"]
    
    if not packages:
        return
    
    # Sort packages by coverage rate (ascending)
    packages.sort(key=lambda x: x["line_rate"])
    
    plt.figure(figsize=(12, 8))
    
    # Data
    names = [p["name"] for p in packages]
    rates = [p["line_rate"] for p in packages]
    
    # Define colors based on coverage thresholds
    colors = []
    for rate in rates:
        if rate >= 80:
            colors.append(GREEN)
        elif rate >= 60:
            colors.append(YELLOW)
        else:
            colors.append(RED)
    
    # Create horizontal bar chart
    y_pos = range(len(names))
    plt.barh(y_pos, rates, color=colors)
    plt.yticks(y_pos, names)
    plt.xlabel('Coverage (%)')
    plt.title('Divine Package Coverage', fontsize=16, fontweight='bold')
    
    # Add values at end of bars
    for i, v in enumerate(rates):
        plt.text(v + 1, i, f"{v:.1f}%", va='center')
    
    plt.savefig('reports/charts/package_coverage.png', bbox_inches='tight')
    plt.close()

def create_test_duration_chart(tests):
    """Create a chart showing test durations."""
    # Get top 10 longest tests
    sorted_tests = sorted(tests, key=lambda x: x["duration"], reverse=True)[:10]
    
    plt.figure(figsize=(12, 8))
    
    # Data
    names = [t["name"].split("::")[-1][:20] + "..." if len(t["name"].split("::")[-1]) > 20 
             else t["name"].split("::")[-1] for t in sorted_tests]
    durations = [t["duration"] for t in sorted_tests]
    colors = [GREEN if t["outcome"] == "passed" else RED for t in sorted_tests]
    
    # Create horizontal bar chart
    y_pos = range(len(names))
    plt.barh(y_pos, durations, color=colors)
    plt.yticks(y_pos, names)
    plt.xlabel('Duration (seconds)')
    plt.title('Divine Test Durations (Top 10)', fontsize=16, fontweight='bold')
    
    # Add values at end of bars
    for i, v in enumerate(durations):
        plt.text(v + 0.05, i, f"{v:.2f}s", va='center')
    
    plt.savefig('reports/charts/test_duration.png', bbox_inches='tight')
    plt.close()

def render_dashboard_html(coverage_data, test_results):
    """Render the divine dashboard HTML with JAH BLESSING."""
    template = Template("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OMEGA BTC AI - Divine Test Dashboard</title>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Montserrat', sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f8f9fa;
                color: #333;
            }
            header {
                background: linear-gradient(135deg, #52b788, #2d6a4f);
                color: white;
                padding: 20px;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .rasta-stripe {
                display: flex;
                height: 10px;
            }
            .rasta-green { background-color: #52b788; flex: 1; }
            .rasta-yellow { background-color: #ffbd00; flex: 1; }
            .rasta-red { background-color: #e63946; flex: 1; }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            .dashboard-section {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 30px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            h1, h2, h3 {
                margin-top: 0;
                color: #2d6a4f;
            }
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 20px;
            }
            .metric-card {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
                text-align: center;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
                border-left: 5px solid #52b788;
            }
            .metric-value {
                font-size: 2em;
                font-weight: bold;
                margin: 10px 0;
            }
            .good { color: #52b788; }
            .warning { color: #ffbd00; }
            .bad { color: #e63946; }
            .charts-row {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 20px;
            }
            .chart {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            }
            .chart img {
                width: 100%;
                height: auto;
            }
            .test-table {
                width: 100%;
                border-collapse: collapse;
            }
            .test-table th, .test-table td {
                padding: 12px 15px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            .test-table th {
                background-color: #f8f9fa;
                font-weight: bold;
            }
            .test-table tr:hover {
                background-color: #f1f1f1;
            }
            .passed { background-color: rgba(82, 183, 136, 0.1); }
            .failed { background-color: rgba(230, 57, 70, 0.1); }
            .skipped { background-color: rgba(255, 189, 0, 0.1); }
            footer {
                text-align: center;
                margin-top: 50px;
                padding: 20px;
                font-style: italic;
                color: #666;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>OMEGA BTC AI - DIVINE TEST DASHBOARD</h1>
            <p>Generated on {{ generation_time }}</p>
        </header>
        <div class="rasta-stripe">
            <div class="rasta-green"></div>
            <div class="rasta-yellow"></div>
            <div class="rasta-red"></div>
        </div>
        
        <div class="container">
            <div class="dashboard-section">
                <h2>🔥 Divine Coverage Summary</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <h3>Overall Line Coverage</h3>
                        <div class="metric-value {{ 'good' if coverage.line_rate >= 80 else 'warning' if coverage.line_rate >= 60 else 'bad' }}">
                            {{ "%.1f"|format(coverage.line_rate) }}%
                        </div>
                    </div>
                    <div class="metric-card">
                        <h3>Branch Coverage</h3>
                        <div class="metric-value {{ 'good' if coverage.branch_rate >= 80 else 'warning' if coverage.branch_rate >= 60 else 'bad' }}">
                            {{ "%.1f"|format(coverage.branch_rate) }}%
                        </div>
                    </div>
                    <div class="metric-card">
                        <h3>Code Complexity</h3>
                        <div class="metric-value {{ 'good' if coverage.complexity < 5 else 'warning' if coverage.complexity < 10 else 'bad' }}">
                            {{ "%.1f"|format(coverage.complexity) }}
                        </div>
                    </div>
                </div>
                
                <div class="charts-row">
                    <div class="chart">
                        <h3>Line Coverage</h3>
                        <img src="charts/coverage_pie.png" alt="Coverage Pie Chart">
                    </div>
                    <div class="chart">
                        <h3>Package Coverage</h3>
                        <img src="charts/package_coverage.png" alt="Package Coverage Chart">
                    </div>
                </div>
            </div>
            
            <div class="dashboard-section">
                <h2>🌿 Divine Test Results</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <h3>Total Tests</h3>
                        <div class="metric-value">{{ tests.summary.total }}</div>
                    </div>
                    <div class="metric-card">
                        <h3>Passing Rate</h3>
                        <div class="metric-value {{ 'good' if tests.summary.pass_percentage >= 90 else 'warning' if tests.summary.pass_percentage >= 70 else 'bad' }}">
                            {{ "%.1f"|format(tests.summary.pass_percentage) }}%
                        </div>
                    </div>
                    <div class="metric-card">
                        <h3>Passed Tests</h3>
                        <div class="metric-value good">{{ tests.summary.passed }}</div>
                    </div>
                    <div class="metric-card">
                        <h3>Failed Tests</h3>
                        <div class="metric-value {{ 'good' if tests.summary.failed == 0 else 'bad' }}">{{ tests.summary.failed }}</div>
                    </div>
                </div>
                
                <div class="charts-row">
                    <div class="chart">
                        <h3>Test Results</h3>
                        <img src="charts/test_results.png" alt="Test Results Chart">
                    </div>
                    <div class="chart">
                        <h3>Test Durations</h3>
                        <img src="charts/test_duration.png" alt="Test Duration Chart">
                    </div>
                </div>
                
                <h3>Recent Test Details</h3>
                <table class="test-table">
                    <thead>
                        <tr>
                            <th>Test Name</th>
                            <th>Result</th>
                            <th>Duration (s)</th>
                            <th>Markers</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for test in tests.tests[:15] %}
                        <tr class="{{ test.outcome }}">
                            <td>{{ test.name }}</td>
                            <td>{{ test.outcome.upper() }}</td>
                            <td>{{ "%.3f"|format(test.duration) }}</td>
                            <td>{{ ", ".join(test.markers) if test.markers else "-" }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        
        <footer>
            <div class="rasta-stripe" style="margin-bottom: 15px">
                <div class="rasta-green"></div>
                <div class="rasta-yellow"></div>
                <div class="rasta-red"></div>
            </div>
            <p>JAH BLESS THIS CODE WITH DIVINE QUALITY! 🙏</p>
            <p>ONE LOVE, ONE HEART, ONE CODE</p>
        </footer>
    </body>
    </html>
    """)
    
    return template.render(
        coverage=coverage_data,
        tests=test_results,
        generation_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

def main():
    parser = argparse.ArgumentParser(description="Generate divine test dashboard")
    parser.add_argument("--coverage", default="coverage.xml", help="Path to coverage XML file")
    parser.add_argument("--test-results", default="reports/pytest.json", help="Path to pytest JSON results")
    parser.add_argument("--output", default="reports/divine_dashboard.html", help="Output dashboard HTML file")
    
    args = parser.parse_args()
    
    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)
    
    coverage_data = parse_coverage_xml(args.coverage)
    test_results = parse_pytest_results(args.test_results)
    create_dashboard(coverage_data, test_results, args.output)

if __name__ == "__main__":
    main()