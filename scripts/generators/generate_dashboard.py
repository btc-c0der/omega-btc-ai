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


"""
DIVINE RASTA TEST DASHBOARD GENERATOR 🌿🔥📊
Creates a blessed HTML dashboard with divine test metrics.
"""

import os
import json
import datetime
import argparse
import matplotlib.pyplot as plt
import numpy as np
from jinja2 import Template

# Terminal colors for spiritual output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def generate_dashboard(coverage_file, metrics_file, complexity_file, output_file="dashboard.html"):
    """Generate a divine dashboard with JAH BLESSING."""
    print(f"{GREEN}🌿 Generating divine test metrics dashboard with JAH BLESSING 🌿{RESET}")
    
    # Load the reports
    coverage_data = json.load(open(coverage_file)) if os.path.exists(coverage_file) else {}
    metrics_data = json.load(open(metrics_file)) if os.path.exists(metrics_file) else {}
    
    # Read complexity data
    complexity_text = open(complexity_file).read() if os.path.exists(complexity_file) else ""
    
    # Extract metrics
    total_coverage = coverage_data.get("totals", {}).get("percent_covered", 0)
    total_tests = metrics_data.get("total", 0)
    passed_tests = metrics_data.get("passed", 0)
    failed_tests = metrics_data.get("failed", 0)
    skipped_tests = metrics_data.get("skipped", 0)
    
    # Calculate test pass rate
    pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    # Create charts
    create_coverage_chart(total_coverage)
    create_test_results_chart(passed_tests, failed_tests, skipped_tests)
    
    # Generate HTML dashboard
    template = get_dashboard_template()
    html = template.render(
        total_coverage=total_coverage,
        total_tests=total_tests,
        passed_tests=passed_tests,
        failed_tests=failed_tests,
        skipped_tests=skipped_tests,
        pass_rate=pass_rate,
        complexity_report=complexity_text,
        generated_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        version="1.0.0"
    )
    
    # Write the dashboard
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"{YELLOW}Divine dashboard generated: {output_file}{RESET}")

def create_coverage_chart(coverage):
    """Create a divine coverage chart with JAH BLESSING."""
    plt.figure(figsize=(6, 6))
    sizes = [coverage, 100-coverage]
    labels = ['Covered', 'Uncovered']
    colors = ['#52b788', '#e63946']
    explode = (0.1, 0)
    
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')
    plt.title('Divine Code Coverage')
    plt.savefig('reports/coverage_chart.png')
    plt.close()

def create_test_results_chart(passed, failed, skipped):
    """Create a divine test results chart with JAH BLESSING."""
    plt.figure(figsize=(8, 6))
    
    labels = ['Passed', 'Failed', 'Skipped']
    values = [passed, failed, skipped]
    colors = ['#52b788', '#e63946', '#ffb703']
    
    plt.bar(labels, values, color=colors)
    plt.title('Divine Test Results')
    plt.ylabel('Number of Tests')
    plt.savefig('reports/test_results_chart.png')
    plt.close()

def get_dashboard_template():
    """Get the divine HTML template for the dashboard."""
    return Template('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OMEGA BTC AI - Divine Test Dashboard</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #f5f5f5;
                color: #333;
                line-height: 1.6;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                padding: 20px;
            }
            header {
                text-align: center;
                padding: 20px;
                background: linear-gradient(135deg, #52b788, #2d6a4f);
                color: white;
                border-radius: 10px 10px 0 0;
                margin: -20px -20px 20px;
            }
            h1 {
                margin: 0;
                font-size: 2.5em;
            }
            .dashboard-date {
                margin-top: 5px;
                font-style: italic;
            }
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .metric-card {
                background: white;
                border-radius: 8px;
                box-shadow: 0 1px 5px rgba(0,0,0,0.1);
                padding: 20px;
                text-align: center;
            }
            .metric-value {
                font-size: 2.5em;
                font-weight: bold;
                margin: 10px 0;
                color: #2d6a4f;
            }
            .charts {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 30px;
            }
            .chart {
                background: white;
                border-radius: 8px;
                box-shadow: 0 1px 5px rgba(0,0,0,0.1);
                padding: 20px;
            }
            .chart img {
                width: 100%;
                height: auto;
            }
            .complexity-report {
                background: white;
                border-radius: 8px;
                box-shadow: 0 1px 5px rgba(0,0,0,0.1);
                padding: 20px;
            }
            .divine-blessing {
                text-align: center;
                margin-top: 30px;
                font-style: italic;
                color: #666;
            }
            .good {
                color: #52b788;
            }
            .medium {
                color: #ffb703;
            }
            .bad {
                color: #e63946;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>OMEGA BTC AI - DIVINE TEST DASHBOARD</h1>
                <p class="dashboard-date">Generated on {{ generated_date }} | Version {{ version }}</p>
            </header>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <h2>Total Code Coverage</h2>
                    <div class="metric-value {% if total_coverage > 80 %}good{% elif total_coverage > 60 %}medium{% else %}bad{% endif %}">{{ "%.1f"|format(total_coverage) }}%</div>
                </div>
                <div class="metric-card">
                    <h2>Total Tests</h2>
                    <div class="metric-value">{{ total_tests }}</div>
                </div>
                <div class="metric-card">
                    <h2>Tests Passed</h2>
                    <div class="metric-value good">{{ passed_tests }}</div>
                </div>
                <div class="metric-card">
                    <h2>Pass Rate</h2>
                    <div class="metric-value {% if pass_rate > 90 %}good{% elif pass_rate > 75 %}medium{% else %}bad{% endif %}">{{ "%.1f"|format(pass_rate) }}%</div>
                </div>
            </div>
            
            <div class="charts">
                <div class="chart">
                    <h2>Divine Code Coverage</h2>
                    <img src="coverage_chart.png" alt="Code Coverage Chart">
                </div>
                <div class="chart">
                    <h2>Divine Test Results</h2>
                    <img src="test_results_chart.png" alt="Test Results Chart">
                </div>
            </div>
            
            <div class="complexity-report">
                <h2>Divine Code Complexity</h2>
                <pre>{{ complexity_report }}</pre>
            </div>
            
            <div class="divine-blessing">
                <p>JAH BLESS THIS CODE WITH DIVINE QUALITY AND HARMONY!</p>
                <p>ONE LOVE, ONE HEART, ONE CODE!</p>
            </div>
        </div>
    </body>
    </html>
    ''')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate divine test dashboard")
    parser.add_argument("--coverage", default="reports/coverage.json", help="Path to coverage JSON file")
    parser.add_argument("--metrics", default="reports/metrics.json", help="Path to test metrics JSON file")
    parser.add_argument("--complexity", default="reports/complexity.md", help="Path to complexity report file")
    parser.add_argument("--output", default="reports/dashboard.html", help="Output HTML file path")
    
    args = parser.parse_args()
    generate_dashboard(args.coverage, args.metrics, args.complexity, args.output)