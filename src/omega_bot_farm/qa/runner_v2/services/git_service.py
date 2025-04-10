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
Git Service Micromodule
-----------------------

This microservice handles all git-related operations:
- Repository status monitoring
- Uncommitted file tracking
- Commit suggestions
- Change history analysis
"""

import os
import time
import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
import subprocess
import json
from datetime import datetime
from pathlib import Path
import threading

# Configure logging
logger = logging.getLogger("git_service")

class GitStatusMonitor:
    """Git repository status monitoring service."""
    
    def __init__(self, project_root: str, refresh_interval: int = 180):
        """
        Initialize the git status monitor.
        
        Args:
            project_root: Path to the project root directory
            refresh_interval: How often to refresh git status (in seconds), default 3 minutes
        """
        self.project_root = Path(project_root).resolve()
        self.refresh_interval = refresh_interval
        self.last_status: Dict[str, Any] = {}
        self.running = False
        self.status_callback = None
        self._monitor_thread = None
        self._lock = threading.Lock()
        
    def _run_git_command(self, command: List[str]) -> Tuple[str, str, int]:
        """
        Run a git command and return its output.
        
        Args:
            command: List of command arguments to pass to git
            
        Returns:
            Tuple of (stdout, stderr, return_code)
        """
        process = subprocess.Popen(
            ["git"] + command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.project_root,
            text=True
        )
        
        stdout, stderr = process.communicate()
        return stdout.strip(), stderr.strip(), process.returncode
    
    def get_current_status(self) -> Dict[str, Any]:
        """
        Get the current git status.
        
        Returns:
            Dictionary with git status information
        """
        status = {
            "timestamp": datetime.now().isoformat(),
            "branch": "",
            "modified_files": [],
            "untracked_files": [],
            "staged_files": []
        }
        
        # Get current branch
        stdout, stderr, return_code = self._run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])
        if return_code == 0:
            status["branch"] = stdout
        
        # Get status
        stdout, stderr, return_code = self._run_git_command(["status", "--porcelain"])
        if return_code == 0:
            for line in stdout.splitlines():
                if line:
                    state = line[:2]
                    file_path = line[3:]
                    
                    if state.startswith("??"):
                        status["untracked_files"].append(file_path)
                    elif state.startswith(" M"):
                        status["modified_files"].append(file_path)
                    elif state.startswith("M"):
                        status["staged_files"].append(file_path)
        
        # Get commit count
        stdout, stderr, return_code = self._run_git_command(["rev-list", "--count", "HEAD"])
        if return_code == 0:
            status["commit_count"] = int(stdout)
        
        # Get last commit info
        stdout, stderr, return_code = self._run_git_command(
            ["log", "-1", "--pretty=format:%h|%an|%ad|%s", "--date=iso"]
        )
        if return_code == 0 and stdout:
            parts = stdout.split("|", 3)
            if len(parts) == 4:
                status["last_commit"] = {
                    "hash": parts[0],
                    "author": parts[1],
                    "date": parts[2],
                    "message": parts[3]
                }
        
        return status
    
    def monitor_loop(self):
        """Run the continuous monitoring loop in a separate thread."""
        logger.info(f"Starting git status monitor with {self.refresh_interval}s refresh interval")
        self.running = True
        
        while self.running:
            try:
                with self._lock:
                    status = self.get_current_status()
                    
                # Check if status changed
                status_changed = (not self.last_status or 
                                 status["modified_files"] != self.last_status.get("modified_files", []) or
                                 status["untracked_files"] != self.last_status.get("untracked_files", []) or
                                 status["staged_files"] != self.last_status.get("staged_files", []))
                
                if status_changed:
                    if self.status_callback:
                        self.status_callback(status)
                    
                    # Store summary statistics in a file for other services
                    stats = {
                        "timestamp": status["timestamp"],
                        "branch": status["branch"],
                        "modified_count": len(status["modified_files"]),
                        "untracked_count": len(status["untracked_files"]),
                        "staged_count": len(status["staged_files"]),
                    }
                    
                    stats_path = self.project_root / ".quantum" / "git_stats.json"
                    os.makedirs(os.path.dirname(stats_path), exist_ok=True)
                    
                    with open(stats_path, "w") as f:
                        json.dump(stats, f)
                
                self.last_status = status
                
            except Exception as e:
                logger.error(f"Error in git status monitor: {e}")
            
            # Sleep until next refresh
            for _ in range(self.refresh_interval):
                if not self.running:
                    break
                time.sleep(1)
    
    def start(self, callback=None):
        """
        Start the git status monitor in a background thread.
        
        Args:
            callback: Optional function to call when git status changes
        """
        if self._monitor_thread and self._monitor_thread.is_alive():
            logger.warning("Git status monitor is already running")
            return
        
        self.status_callback = callback
        self._monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self._monitor_thread.start()
    
    def stop(self):
        """Stop the git status monitor."""
        logger.info("Stopping git status monitor")
        self.running = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5.0)

class GitCommitSuggester:
    """Suggests meaningful commit messages based on changes."""
    
    def __init__(self, project_root: str):
        """
        Initialize the commit suggester.
        
        Args:
            project_root: Path to the project root directory
        """
        self.project_root = Path(project_root).resolve()
        self.git_monitor = GitStatusMonitor(project_root)
    
    def get_diff_summary(self) -> str:
        """
        Get a summary of changes since last commit.
        
        Returns:
            A string describing the changes
        """
        stdout, stderr, return_code = self.git_monitor._run_git_command(
            ["diff", "--stat"]
        )
        if return_code == 0:
            return stdout
        return ""
    
    def suggest_commit_message(self) -> str:
        """
        Generate a suggested commit message based on changes.
        
        Returns:
            A suggested commit message
        """
        status = self.git_monitor.get_current_status()
        
        if not status["modified_files"] and not status["staged_files"]:
            return "No changes to commit"
        
        # Analyze the types of files changed
        file_types = {}
        all_files = status["modified_files"] + status["staged_files"]
        
        for file_path in all_files:
            file_ext = Path(file_path).suffix.lower()
            if file_ext in file_types:
                file_types[file_ext] += 1
            else:
                file_types[file_ext] = 1
        
        # Categorize the change
        message_parts = []
        
        if any(f.endswith("test.py") or "/tests/" in f for f in all_files):
            message_parts.append("Update tests")
        
        if any(f.endswith(".md") for f in all_files):
            message_parts.append("Update documentation")
        
        if any(f.endswith(".py") and not f.endswith("test.py") and "/tests/" not in f for f in all_files):
            message_parts.append("Update code")
        
        if any("/qa/" in f for f in all_files):
            message_parts.append("Update QA systems")
        
        if any("requirements.txt" in f or "setup.py" in f for f in all_files):
            message_parts.append("Update dependencies")
        
        # If we couldn't categorize, use a generic message
        if not message_parts:
            message_parts = ["Update project files"]
        
        # Combine categories
        commit_message = " and ".join(message_parts)
        
        # Add statistics
        file_count = len(all_files)
        if file_count == 1:
            commit_message += f" ({all_files[0]})"
        else:
            commit_message += f" ({file_count} files)"
        
        return commit_message


# Example usage when module is run directly
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    monitor = GitStatusMonitor(".")
    
    def status_changed(status):
        print(f"Git status changed: {status['branch']}")
        print(f"Modified files: {len(status['modified_files'])}")
        print(f"Untracked files: {len(status['untracked_files'])}")
    
    monitor.start(callback=status_changed)
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop() 