#!/usr/bin/env python3
"""Script to analyze git branch health and metrics."""

import os
import sys
import json
import argparse
from datetime import datetime
from tabulate import tabulate

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from omega_ai.mde.branch_analytics import BranchAnalytics, BranchMetrics

def format_score(score: float) -> str:
    """Format a health score with color."""
    score_int = int(score * 100)
    if score >= 0.8:
        return f"\033[92m{score_int}%\033[0m"  # Green
    elif score >= 0.6:
        return f"\033[93m{score_int}%\033[0m"  # Yellow
    else:
        return f"\033[91m{score_int}%\033[0m"  # Red

def format_score_html(score: float) -> str:
    """Format a health score with HTML color."""
    score_int = int(score * 100)
    if score >= 0.8:
        color = "green"
    elif score >= 0.6:
        color = "orange"
    else:
        color = "red"
    return f'<span style="color: {color}">{score_int}%</span>'

def export_to_html(rows: list, headers: list, analytics: BranchAnalytics, output_file: str):
    """Export branch analytics to HTML file."""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Branch Analytics Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            .stale { color: red; }
            .genesis { font-style: italic; color: #666; }
            h1 { color: #333; }
            h2 { color: #666; }
        </style>
    </head>
    <body>
        <h1>Branch Analytics Report</h1>
        <p>Generated on: {timestamp}</p>
        <h2>Branch Metrics</h2>
        <table>
            <tr>{header_row}</tr>
            {table_rows}
        </table>
        
        <h2>Branch Details</h2>
        {branch_details}
        
        <h2>Stale Branches</h2>
        {stale_branches}
    </body>
    </html>
    """
    
    # Format headers
    header_row = "".join(f"<th>{h}</th>" for h in headers)
    
    # Format table rows
    table_rows = ""
    for row in rows:
        # Convert terminal color codes to HTML for health score
        row_copy = list(row)
        if isinstance(row[-1], str) and "\033[" in row[-1]:
            score = float(row[-1].split("%")[0].split("m")[1]) / 100
            row_copy[-1] = format_score_html(score)
        table_rows += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row_copy) + "</tr>"
    
    # Get branch details
    branch_details = ""
    for branch in [r[0] for r in rows]:
        metrics = analytics.get_branch_metrics(branch)
        branch_details += f"""
        <div>
            <h3>{branch}</h3>
            <p class="genesis">Genesis: {metrics.genesis_message}</p>
            <ul>
                <li>Total Lines of Code: {metrics.total_lines:,}</li>
                <li>Contributors: {', '.join(metrics.contributors)}</li>
                <li>Lines Changed: +{metrics.lines_changed[0]}, -{metrics.lines_changed[1]}</li>
            </ul>
        </div>
        """
    
    # Get stale branches
    stale = analytics.get_stale_branches()
    if stale:
        stale_branches = "<ul>" + "".join(f'<li class="stale">{b}</li>' for b in stale) + "</ul>"
    else:
        stale_branches = "<p>No stale branches found.</p>"
    
    # Generate HTML
    html_content = html_template.format(
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        header_row=header_row,
        table_rows=table_rows,
        branch_details=branch_details,
        stale_branches=stale_branches
    )
    
    # Write HTML file
    with open(output_file, 'w') as f:
        f.write(html_content)

def main(repo_path: str, export_path: str = "", html_path: str = "") -> None:
    """
    Main function to analyze git branch health and metrics.
    
    Args:
        repo_path (str): Path to the git repository
        export_path (str, optional): Path to export analytics JSON
        html_path (str, optional): Path to export HTML report
    """
    analytics = BranchAnalytics(repo_path)
    
    # Get all branches
    branches = [b.strip('* ') for b in analytics._run_git_command(['branch']).splitlines()]
    
    # Collect metrics and health scores
    rows = []
    for branch in branches:
        metrics = analytics.get_branch_metrics(branch)
        health = analytics.analyze_branch_health(branch)
        
        rows.append([
            branch,
            metrics.last_commit.strftime('%Y-%m-%d %H:%M'),
            metrics.commit_count,
            len(metrics.contributors),
            metrics.age_days,
            'Yes' if metrics.is_merged else 'No',
            metrics.total_lines,
            format_score(health['health_score'])
        ])
    
    # Display results
    headers = ['Branch', 'Last Commit', 'Commits', 'Contributors', 'Age (days)', 'Merged', 'Lines of Code', 'Health']
    print("\nBranch Analytics Report")
    print("=====================")
    print(tabulate(rows, headers=headers, tablefmt='grid'))
    
    # Show genesis messages
    print("\nGenesis Messages:")
    for branch in branches:
        metrics = analytics.get_branch_metrics(branch)
        print(f"\n{branch}:")
        print(f"  {metrics.genesis_message}")
    
    # Show stale branches
    stale = analytics.get_stale_branches()
    if stale:
        print("\nStale Branches (inactive > 30 days):")
        for branch in stale:
            print(f"- {branch}")
    
    # Export if requested
    if export_path:
        analytics.export_analytics(export_path)
        print(f"\nAnalytics exported to: {export_path}")
    
    # Export HTML if requested
    if html_path:
        export_to_html(rows, headers, analytics, html_path)
        print(f"\nHTML report exported to: {html_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze git branch health and metrics')
    parser.add_argument('repo_path', help='Path to git repository')
    parser.add_argument('--export', help='Export analytics to JSON file', default="")
    parser.add_argument('--html', help='Export report to HTML file', default="branch_analytics.html")
    args = parser.parse_args()
    
    main(args.repo_path, args.export, args.html) 