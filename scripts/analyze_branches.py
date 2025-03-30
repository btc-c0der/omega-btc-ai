#!/usr/bin/env python3
"""Script to analyze git branch health and metrics."""

import os
import sys
import json
import argparse
from datetime import datetime
from tabulate import tabulate

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from omega_ai.mde.branch_analytics import BranchAnalytics

def format_score(score: float) -> str:
    """Format a score as a colored string."""
    score_int = int(score * 100)
    if score_int >= 80:
        return f"\033[92m{score_int}%\033[0m"  # Green
    elif score_int >= 60:
        return f"\033[93m{score_int}%\033[0m"  # Yellow
    else:
        return f"\033[91m{score_int}%\033[0m"  # Red

def main(repo_path: str, export_path: str = None):
    """Run branch analysis and display results.
    
    Args:
        repo_path: Path to git repository
        export_path: Optional path to export JSON results
    """
    analytics = BranchAnalytics(repo_path)
    
    # Get all branches
    branches = [b.strip('* ') for b in analytics.
        _run_git_command(['branch']).splitlines()]
    
    # Collect metrics and health scores
    results = []
    for branch in branches:
        metrics = analytics.get_branch_metrics(branch)
        health = analytics.analyze_branch_health(branch)
        
        results.append([
            branch,
            metrics.age_days,
            len(metrics.contributors),
            sum(metrics.lines_changed),
            format_score(health['health_score']),
            format_score(health['age_score']),
            format_score(health['activity_score']),
            format_score(health['complexity_score']),
            format_score(health['collaboration_score'])
        ])
    
    # Display results
    headers = [
        'Branch',
        'Age (days)',
        'Contributors',
        'Changes',
        'Health',
        'Age Score',
        'Activity',
        'Complexity',
        'Collab'
    ]
    
    print("\nBranch Analytics Report")
    print("=" * 80)
    print(f"Repository: {repo_path}")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(tabulate(results, headers=headers, tablefmt='grid'))
    print()
    
    # Show stale branches
    stale = analytics.get_stale_branches()
    if stale:
        print("\nStale Branches (inactive > 30 days):")
        for branch in stale:
            print(f"  - {branch}")
    
    # Export if requested
    if export_path:
        analytics.export_analytics(export_path)
        print(f"\nDetailed analytics exported to: {export_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze git branch health")
    parser.add_argument("--repo", default=".", help="Path to git repository")
    parser.add_argument("--export", help="Export JSON results to file")
    args = parser.parse_args()
    
    main(args.repo, args.export) 