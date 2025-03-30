"""Branch Analytics Module for Multi-Branch Development Environment.

This module provides analytics and insights for git branch management,
including health monitoring, usage patterns, and performance metrics.
"""

import os
import re
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from subprocess import check_output, CalledProcessError

logger = logging.getLogger(__name__)

@dataclass
class BranchMetrics:
    """Metrics for a single branch."""
    name: str
    last_commit: datetime
    commit_count: int
    contributors: List[str]
    age_days: int
    is_merged: bool
    last_ci_status: str
    lines_changed: Tuple[int, int]  # (additions, deletions)
    review_count: int
    
class BranchAnalytics:
    """Analyzes git branch patterns and health metrics."""
    
    def __init__(self, repo_path: str):
        """Initialize branch analytics.
        
        Args:
            repo_path: Path to git repository
        """
        self.repo_path = os.path.abspath(repo_path)
        if not os.path.exists(os.path.join(repo_path, '.git')):
            raise ValueError(f"Not a git repository: {repo_path}")
            
        self.metrics_cache: Dict[str, BranchMetrics] = {}
        
    def _run_git_command(self, command: List[str]) -> str:
        """Run a git command and return output.
        
        Args:
            command: Git command as list of arguments
            
        Returns:
            Command output as string
        """
        try:
            return check_output(['git'] + command, 
                              cwd=self.repo_path,
                              text=True)
        except CalledProcessError as e:
            logger.error(f"Git command failed: {' '.join(command)}")
            logger.error(f"Error: {str(e)}")
            raise
            
    def get_branch_metrics(self, branch_name: str) -> BranchMetrics:
        """Get comprehensive metrics for a branch.
        
        Args:
            branch_name: Name of the branch
            
        Returns:
            BranchMetrics object with branch statistics
        """
        # Get last commit info
        last_commit_str = self._run_git_command([
            'log', '-1', '--format=%aI', branch_name
        ]).strip()
        last_commit = datetime.fromisoformat(last_commit_str)
        
        # Get commit count
        commit_count = int(self._run_git_command([
            'rev-list', '--count', branch_name
        ]))
        
        # Get contributors
        contributors = self._run_git_command([
            'log', '--format=%aN', branch_name
        ]).splitlines()
        contributors = list(set(contributors))  # Unique contributors
        
        # Calculate age
        first_commit_str = self._run_git_command([
            'log', '--format=%aI', '--reverse', branch_name
        ]).splitlines()[0]
        first_commit = datetime.fromisoformat(first_commit_str)
        age_days = (datetime.now() - first_commit).days
        
        # Check if merged
        is_merged = bool(self._run_git_command([
            'branch', '--merged', 'main'
        ]).find(branch_name) != -1)
        
        # Get CI status (placeholder - implement based on your CI system)
        last_ci_status = "unknown"
        
        # Get lines changed
        diff_stats = self._run_git_command([
            'diff', '--shortstat', f'main...{branch_name}'
        ])
        additions = deletions = 0
        if diff_stats:
            match = re.search(r'(\d+) insertion.+?(\d+) deletion', diff_stats)
            if match:
                additions, deletions = map(int, match.groups())
        
        # Get review count (placeholder - implement based on your review system)
        review_count = 0
        
        return BranchMetrics(
            name=branch_name,
            last_commit=last_commit,
            commit_count=commit_count,
            contributors=contributors,
            age_days=age_days,
            is_merged=is_merged,
            last_ci_status=last_ci_status,
            lines_changed=(additions, deletions),
            review_count=review_count
        )
        
    def analyze_branch_health(self, branch_name: str) -> Dict[str, float]:
        """Analyze branch health and return scores.
        
        Args:
            branch_name: Name of the branch
            
        Returns:
            Dictionary of health metrics (0-1 scale)
        """
        metrics = self.get_branch_metrics(branch_name)
        
        # Age score (penalize old unmerged branches)
        age_score = 1.0
        if not metrics.is_merged and metrics.age_days > 30:
            age_score = max(0.0, 1.0 - (metrics.age_days - 30) / 60)
            
        # Activity score
        now = datetime.now()
        days_since_commit = (now - metrics.last_commit).days
        activity_score = max(0.0, 1.0 - days_since_commit / 30)
        
        # Complexity score (based on changes)
        additions, deletions = metrics.lines_changed
        total_changes = additions + deletions
        complexity_score = 1.0
        if total_changes > 1000:
            complexity_score = max(0.0, 1.0 - (total_changes - 1000) / 4000)
            
        # Collaboration score
        collab_score = min(1.0, len(metrics.contributors) / 3)
        
        # Overall health score
        health_score = (
            age_score * 0.3 +
            activity_score * 0.3 +
            complexity_score * 0.2 +
            collab_score * 0.2
        )
        
        return {
            'health_score': health_score,
            'age_score': age_score,
            'activity_score': activity_score,
            'complexity_score': complexity_score,
            'collaboration_score': collab_score
        }
        
    def get_stale_branches(self, days_threshold: int = 30) -> List[str]:
        """Get list of stale branches.
        
        Args:
            days_threshold: Number of days without commits to consider stale
            
        Returns:
            List of stale branch names
        """
        stale_branches = []
        branches = self._run_git_command(['branch']).splitlines()
        
        for branch in branches:
            branch = branch.strip('* ')
            metrics = self.get_branch_metrics(branch)
            
            if (not metrics.is_merged and 
                (datetime.now() - metrics.last_commit).days > days_threshold):
                stale_branches.append(branch)
                
        return stale_branches
        
    def get_merge_conflicts(self, branch_name: str) -> List[str]:
        """Get list of files with potential merge conflicts.
        
        Args:
            branch_name: Name of the branch
            
        Returns:
            List of files with potential conflicts
        """
        try:
            # Try to merge without committing
            self._run_git_command([
                'merge-tree', 
                self._run_git_command(['merge-base', 'main', branch_name]).strip(),
                'main',
                branch_name
            ])
            return []
        except CalledProcessError as e:
            # Parse output for conflict files
            output = str(e.output)
            conflicts = []
            for line in output.splitlines():
                if line.startswith('CONFLICT'):
                    file_match = re.search(r'in (.+)$', line)
                    if file_match:
                        conflicts.append(file_match.group(1))
            return conflicts
            
    def export_analytics(self, output_file: str):
        """Export branch analytics to JSON file.
        
        Args:
            output_file: Path to output JSON file
        """
        analytics = {
            'timestamp': datetime.now().isoformat(),
            'repository': self.repo_path,
            'branches': {}
        }
        
        branches = self._run_git_command(['branch']).splitlines()
        for branch in branches:
            branch = branch.strip('* ')
            metrics = self.get_branch_metrics(branch)
            health = self.analyze_branch_health(branch)
            
            analytics['branches'][branch] = {
                'metrics': {
                    'last_commit': metrics.last_commit.isoformat(),
                    'commit_count': metrics.commit_count,
                    'contributors': metrics.contributors,
                    'age_days': metrics.age_days,
                    'is_merged': metrics.is_merged,
                    'last_ci_status': metrics.last_ci_status,
                    'lines_changed': {
                        'additions': metrics.lines_changed[0],
                        'deletions': metrics.lines_changed[1]
                    },
                    'review_count': metrics.review_count
                },
                'health': health
            }
            
        with open(output_file, 'w') as f:
            json.dump(analytics, f, indent=2)
            
        logger.info(f"Branch analytics exported to {output_file}") 