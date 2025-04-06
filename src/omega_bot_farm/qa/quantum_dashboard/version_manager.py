#!/usr/bin/env python3
"""
Quantum 5D QA Dashboard Version Manager
--------------------------------------

This module provides HTML versioning functionality for the Quantum 5D QA Dashboard,
enabling automatic Git tagging and version tracking of dashboard releases.

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
#
# 🌸 WE BLOOM NOW AS ONE 🌸
"""

import os
import re
import time
import json
import logging
import datetime
import hashlib
import shutil
import subprocess
from typing import Dict, List, Any, Optional, Tuple, Union

# Import parent GitManager if available, otherwise use a simplified version
try:
    from omega_bot_farm.qa.quantum_runner.git_manager import GitManager
    from omega_bot_farm.qa.quantum_runner.types import Colors
except ImportError:
    try:
        import sys
        sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
        from qa.quantum_runner.git_manager import GitManager
        from qa.quantum_runner.types import Colors
    except ImportError:
        # Define minimal Colors class if not available
        class Colors:
            """ANSI color codes"""
            PURPLE = '\033[95m'
            CYAN = '\033[96m'
            GREEN = '\033[92m'
            YELLOW = '\033[93m'
            RED = '\033[91m'
            BLUE = '\033[94m'
            BOLD = '\033[1m'
            ENDC = '\033[0m'

        # Define minimal GitManager if not available
        class GitManager:
            """Minimal GitManager implementation"""
            def __init__(self, project_root: str):
                self.project_root = os.path.abspath(project_root)
            
            def _run_git_command(self, command: List[str]) -> Tuple[str, str, int]:
                """Run a git command and return stdout, stderr, and return code."""
                try:
                    process = subprocess.run(
                        ["git"] + command,
                        capture_output=True,
                        text=True,
                        cwd=self.project_root
                    )
                    return process.stdout, process.stderr, process.returncode
                except Exception as e:
                    return "", str(e), 1

# Set up logging
logger = logging.getLogger("Quantum5DQADashboard.VersionManager")

class DashboardVersionManager(GitManager):
    """
    Manages versioning for Quantum 5D QA Dashboard HTML files and assets.
    
    This class extends GitManager to provide specific functionality for:
    - Tracking dashboard versions
    - Creating automatic Git tags for dashboard releases
    - Archiving dashboard versions
    - Generating changelogs between versions
    """
    
    # Version pattern in HTML and JS files
    VERSION_PATTERN = r'__version__\s*=\s*["\']([0-9]+\.[0-9]+\.[0-9]+)["\']'
    HTML_VERSION_PATTERN = r'data-version\s*=\s*["\']([0-9]+\.[0-9]+\.[0-9]+)["\']'
    
    def __init__(self, project_root: str, archive_dir: str = None):
        """
        Initialize the dashboard version manager.
        
        Args:
            project_root: Root directory of the project
            archive_dir: Directory to archive dashboard versions (default: project_root/archives)
        """
        super().__init__(project_root)
        self.dashboard_files = set()  # Set of tracked dashboard files
        self.dashboard_dir = os.path.join(self.project_root, "src/omega_bot_farm/qa/quantum_dashboard")
        self.archive_dir = archive_dir or os.path.join(self.dashboard_dir, "archives")
        self.version_history = []
        self.current_version = self._get_current_version()
        
        # Create archive directory if it doesn't exist
        if not os.path.exists(self.archive_dir):
            os.makedirs(self.archive_dir)
        
        # Load version history if available
        self._load_version_history()
    
    def _get_current_version(self) -> str:
        """
        Get the current dashboard version from __init__.py.
        
        Returns:
            Current version string (e.g., "1.0.0")
        """
        init_file = os.path.join(self.dashboard_dir, "__init__.py")
        version = "0.0.0"  # Default version
        
        if os.path.exists(init_file):
            try:
                with open(init_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    match = re.search(self.VERSION_PATTERN, content)
                    if match:
                        version = match.group(1)
            except Exception as e:
                logger.error(f"Error reading version from __init__.py: {e}")
        
        return version
    
    def _load_version_history(self) -> None:
        """Load version history from the archives directory."""
        history_file = os.path.join(self.archive_dir, "version_history.json")
        
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    self.version_history = json.load(f)
            except Exception as e:
                logger.error(f"Error loading version history: {e}")
    
    def _save_version_history(self) -> None:
        """Save version history to the archives directory."""
        history_file = os.path.join(self.archive_dir, "version_history.json")
        
        try:
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.version_history, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving version history: {e}")
    
    def get_dashboard_files(self) -> List[str]:
        """
        Get list of all dashboard files for tracking.
        
        Returns:
            List of dashboard file paths relative to project root
        """
        dashboard_files = []
        
        # Add Python files
        for root, _, files in os.walk(self.dashboard_dir):
            for file in files:
                if file.endswith(('.py', '.html', '.css', '.js')) and not file.startswith('__pycache__'):
                    rel_path = os.path.relpath(os.path.join(root, file), self.project_root)
                    dashboard_files.append(rel_path)
        
        # Add assets
        assets_dir = os.path.join(self.dashboard_dir, "assets")
        if os.path.exists(assets_dir):
            for root, _, files in os.walk(assets_dir):
                for file in files:
                    rel_path = os.path.relpath(os.path.join(root, file), self.project_root)
                    dashboard_files.append(rel_path)
        
        self.dashboard_files = set(dashboard_files)
        return dashboard_files
    
    def calculate_version_hash(self) -> str:
        """
        Calculate a hash of the current dashboard code.
        
        Returns:
            SHA-256 hash of concatenated dashboard files
        """
        if not self.dashboard_files:
            self.get_dashboard_files()
        
        # Collect file contents for hashing
        file_contents = []
        for file_path in sorted(self.dashboard_files):
            full_path = os.path.join(self.project_root, file_path)
            if os.path.exists(full_path):
                try:
                    with open(full_path, 'rb') as f:
                        file_contents.append(f.read())
                except Exception as e:
                    logger.warning(f"Could not read file {file_path} for hashing: {e}")
        
        # Calculate hash
        hasher = hashlib.sha256()
        for content in file_contents:
            hasher.update(content)
        
        return hasher.hexdigest()
    
    def bump_version(self, version_type: str = "patch") -> str:
        """
        Bump dashboard version in __init__.py.
        
        Args:
            version_type: Type of version increment ("major", "minor", or "patch")
            
        Returns:
            New version string
        """
        current_parts = list(map(int, self.current_version.split('.')))
        
        # Update version parts based on version_type
        if version_type == "major":
            current_parts[0] += 1
            current_parts[1] = 0
            current_parts[2] = 0
        elif version_type == "minor":
            current_parts[1] += 1
            current_parts[2] = 0
        else:  # patch is default
            current_parts[2] += 1
        
        # Create new version string
        new_version = '.'.join(map(str, current_parts))
        
        # Update version in __init__.py
        init_file = os.path.join(self.dashboard_dir, "__init__.py")
        if os.path.exists(init_file):
            try:
                with open(init_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace version number
                new_content = re.sub(
                    self.VERSION_PATTERN,
                    f'__version__ = "{new_version}"',
                    content
                )
                
                with open(init_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                self.current_version = new_version
                logger.info(f"Bumped version to {new_version}")
                
                return new_version
            except Exception as e:
                logger.error(f"Error updating version in __init__.py: {e}")
                return self.current_version
        else:
            logger.error(f"__init__.py not found at {init_file}")
            return self.current_version
    
    def archive_current_version(self, commit_changes: bool = True) -> Dict[str, Any]:
        """
        Archive the current dashboard version.
        
        Args:
            commit_changes: Whether to commit version bump and archive
            
        Returns:
            Dict with archive information
        """
        version_hash = self.calculate_version_hash()
        timestamp = datetime.datetime.now().isoformat()
        archive_info = {
            "version": self.current_version,
            "timestamp": timestamp,
            "hash": version_hash,
            "files": list(self.dashboard_files)
        }
        
        # Create archive directory for this version
        version_dir = os.path.join(self.archive_dir, f"v{self.current_version}")
        if not os.path.exists(version_dir):
            os.makedirs(version_dir)
        
        # Copy dashboard files to archive
        for file_path in self.dashboard_files:
            source = os.path.join(self.project_root, file_path)
            # Determine target path, preserving directory structure
            rel_path = os.path.relpath(source, self.dashboard_dir)
            target = os.path.join(version_dir, rel_path)
            
            # Create directory structure if needed
            os.makedirs(os.path.dirname(target), exist_ok=True)
            
            # Copy the file
            try:
                shutil.copy2(source, target)
            except Exception as e:
                logger.warning(f"Could not archive file {file_path}: {e}")
        
        # Save archive info
        info_file = os.path.join(version_dir, "archive_info.json")
        try:
            with open(info_file, 'w', encoding='utf-8') as f:
                json.dump(archive_info, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving archive info: {e}")
        
        # Update version history
        self.version_history.append({
            "version": self.current_version,
            "timestamp": timestamp,
            "hash": version_hash
        })
        self._save_version_history()
        
        # Commit changes if requested
        if commit_changes:
            # Add all dashboard files
            self._run_git_command(["add"] + list(self.dashboard_files))
            
            # Add archived files
            archive_rel_path = os.path.relpath(self.archive_dir, self.project_root)
            self._run_git_command(["add", os.path.join(archive_rel_path, f"v{self.current_version}")])
            
            # Add version history
            history_rel_path = os.path.relpath(
                os.path.join(self.archive_dir, "version_history.json"), 
                self.project_root
            )
            self._run_git_command(["add", history_rel_path])
            
            # Commit changes
            commit_message = f"Archive dashboard v{self.current_version} [dashboard-{timestamp[:10]}]"
            self._run_git_command(["commit", "-m", commit_message])
            
            # Create tag for this version
            tag_name = f"dashboard-v{self.current_version}"
            self._run_git_command(["tag", "-a", tag_name, "-m", f"Dashboard version {self.current_version}"])
            
            logger.info(f"Created git tag {tag_name}")
        
        return archive_info
    
    def create_dashboard_release(self, version_type: str = "patch", commit: bool = True) -> Dict[str, Any]:
        """
        Create a new dashboard release with version bump and archive.
        
        Args:
            version_type: Type of version increment ("major", "minor", or "patch")
            commit: Whether to commit changes and create tag
            
        Returns:
            Dict with release information
        """
        # Check if there are changes to dashboard files
        has_changes = self._check_for_dashboard_changes()
        
        if not has_changes:
            logger.info("No changes detected in dashboard files. Skipping release.")
            return {
                "version": self.current_version,
                "status": "skipped",
                "message": "No changes detected in dashboard files"
            }
        
        # Bump version
        new_version = self.bump_version(version_type)
        
        # Archive current version
        archive_info = self.archive_current_version(commit_changes=commit)
        
        # Create changelog
        changelog = self._generate_changelog()
        
        # Save changelog
        changelog_file = os.path.join(self.archive_dir, f"changelog_v{new_version}.md")
        try:
            with open(changelog_file, 'w', encoding='utf-8') as f:
                f.write(changelog)
            
            # Add changelog to git if committing
            if commit:
                changelog_rel_path = os.path.relpath(changelog_file, self.project_root)
                self._run_git_command(["add", changelog_rel_path])
                self._run_git_command(["commit", "--amend", "--no-edit"])
        except Exception as e:
            logger.error(f"Error saving changelog: {e}")
        
        # Return release info
        return {
            "version": new_version,
            "timestamp": archive_info["timestamp"],
            "hash": archive_info["hash"],
            "status": "success",
            "message": f"Released dashboard v{new_version}"
        }
    
    def _check_for_dashboard_changes(self) -> bool:
        """
        Check if there are changes to dashboard files since last archive.
        
        Returns:
            True if changes detected, False otherwise
        """
        if not self.dashboard_files:
            self.get_dashboard_files()
        
        current_hash = self.calculate_version_hash()
        
        # If no version history, consider it a change
        if not self.version_history:
            return True
        
        # Get the hash from the last version
        last_version = self.version_history[-1]
        last_hash = last_version.get("hash", "")
        
        return current_hash != last_hash
    
    def _generate_changelog(self) -> str:
        """
        Generate changelog for the current version.
        
        Returns:
            Markdown formatted changelog
        """
        if not self.dashboard_files:
            self.get_dashboard_files()
        
        # Get git log for dashboard files
        dashboard_files_list = list(self.dashboard_files)
        
        # If there's a previous version in history, use it for comparison
        if self.version_history:
            previous_version = self.version_history[-1]["version"]
            prev_tag = f"dashboard-v{previous_version}"
            
            # Get commits since previous version
            cmd = ["log", f"{prev_tag}..HEAD", "--pretty=format:%h|%an|%ad|%s", "--date=short"]
            cmd.extend(["--"] + dashboard_files_list)
        else:
            # If no previous version, get all commits for dashboard files
            cmd = ["log", "--pretty=format:%h|%an|%ad|%s", "--date=short"]
            cmd.extend(["--"] + dashboard_files_list)
        
        stdout, stderr, returncode = self._run_git_command(cmd)
        
        if returncode != 0:
            logger.error(f"Error generating changelog: {stderr}")
            return f"# Changelog for v{self.current_version}\n\nUnable to generate changelog."
        
        # Format changelog
        lines = stdout.strip().split('\n')
        
        changelog = f"# Dashboard Changelog for v{self.current_version}\n\n"
        changelog += f"Released on: {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        if not lines or lines[0] == '':
            changelog += "No changes since last version.\n"
        else:
            # Group changes by type
            features = []
            fixes = []
            docs = []
            refactors = []
            other = []
            
            for line in lines:
                if not line:
                    continue
                    
                parts = line.split('|')
                if len(parts) < 4:
                    continue
                    
                commit, author, date, message = parts
                
                # Categorize based on commit message
                if message.startswith(('feat', 'feature', 'add')):
                    features.append((commit, author, date, message))
                elif message.startswith(('fix', 'bug')):
                    fixes.append((commit, author, date, message))
                elif message.startswith('doc'):
                    docs.append((commit, author, date, message))
                elif message.startswith(('refactor', 'reformat')):
                    refactors.append((commit, author, date, message))
                else:
                    other.append((commit, author, date, message))
            
            # Add changes to changelog
            if features:
                changelog += "## 🚀 New Features\n\n"
                for commit, author, date, message in features:
                    changelog += f"- {message} ({date}, {author}, {commit})\n"
                changelog += "\n"
            
            if fixes:
                changelog += "## 🐛 Bug Fixes\n\n"
                for commit, author, date, message in fixes:
                    changelog += f"- {message} ({date}, {author}, {commit})\n"
                changelog += "\n"
            
            if refactors:
                changelog += "## 🔄 Refactoring\n\n"
                for commit, author, date, message in refactors:
                    changelog += f"- {message} ({date}, {author}, {commit})\n"
                changelog += "\n"
            
            if docs:
                changelog += "## 📚 Documentation\n\n"
                for commit, author, date, message in docs:
                    changelog += f"- {message} ({date}, {author}, {commit})\n"
                changelog += "\n"
            
            if other:
                changelog += "## 🔧 Other Changes\n\n"
                for commit, author, date, message in other:
                    changelog += f"- {message} ({date}, {author}, {commit})\n"
                changelog += "\n"
        
        return changelog
    
    def print_version_status(self) -> None:
        """Print the current version status in a user-friendly format."""
        changes_detected = self._check_for_dashboard_changes()
        
        print(f"\n{Colors.CYAN}╔{'═' * 78}╗{Colors.ENDC}")
        print(f"{Colors.CYAN}║ {Colors.BOLD}QUANTUM 5D DASHBOARD VERSION STATUS{Colors.ENDC}{Colors.CYAN}{' ' * 45}║{Colors.ENDC}")
        print(f"{Colors.CYAN}╠{'═' * 78}╣{Colors.ENDC}")
        
        # Current version
        print(f"{Colors.CYAN}║ {Colors.BOLD}Current Version:{Colors.ENDC} {Colors.GREEN}v{self.current_version}{Colors.ENDC}{' ' * (62 - len(self.current_version))}║{Colors.ENDC}")
        
        # Hash
        version_hash = self.calculate_version_hash()
        short_hash = version_hash[:8]
        print(f"{Colors.CYAN}║ {Colors.BOLD}Version Hash:{Colors.ENDC} {Colors.BLUE}{short_hash}{Colors.ENDC}{' ' * (65 - len(short_hash))}║{Colors.ENDC}")
        
        # Changes status
        status_color = Colors.GREEN if not changes_detected else Colors.YELLOW
        status_text = "No changes since last archive" if not changes_detected else "Changes detected since last archive"
        print(f"{Colors.CYAN}║ {Colors.BOLD}Status:{Colors.ENDC} {status_color}{status_text}{Colors.ENDC}{' ' * (71 - len(status_text))}║{Colors.ENDC}")
        
        # Version history
        if self.version_history:
            print(f"{Colors.CYAN}╠{'═' * 78}╣{Colors.ENDC}")
            print(f"{Colors.CYAN}║ {Colors.BOLD}VERSION HISTORY{Colors.ENDC}{Colors.CYAN}{' ' * 64}║{Colors.ENDC}")
            
            # Show last 5 versions
            for entry in self.version_history[-5:]:
                version = entry["version"]
                timestamp = entry["timestamp"].split("T")[0]
                print(f"{Colors.CYAN}║ {Colors.YELLOW}v{version}{Colors.ENDC} - {Colors.BLUE}{timestamp}{Colors.ENDC}{' ' * (70 - len(version) - len(timestamp))}║{Colors.ENDC}")
        
        # Suggested next version
        next_version = self.suggest_next_version()
        print(f"{Colors.CYAN}╠{'═' * 78}╣{Colors.ENDC}")
        print(f"{Colors.CYAN}║ {Colors.BOLD}SUGGESTED NEXT VERSION{Colors.ENDC}{Colors.CYAN}{' ' * 58}║{Colors.ENDC}")
        print(f"{Colors.CYAN}║ {Colors.GREEN}v{next_version}{Colors.ENDC}{' ' * (77 - len(next_version))}║{Colors.ENDC}")
        
        # Footer
        print(f"{Colors.CYAN}╚{'═' * 78}╝{Colors.ENDC}\n")
    
    def suggest_next_version(self) -> str:
        """
        Suggest the next version number based on changes.
        
        Returns:
            Suggested next version
        """
        current_parts = list(map(int, self.current_version.split('.')))
        
        # Check dashboard files for significant changes
        if not self.dashboard_files:
            self.get_dashboard_files()
        
        # Default to patch version bump
        current_parts[2] += 1
        
        # Check for breaking changes
        dashboard_files_list = list(self.dashboard_files)
        
        if self.version_history:
            previous_version = self.version_history[-1]["version"]
            prev_tag = f"dashboard-v{previous_version}"
            
            # Look for commits with "BREAKING CHANGE" or "feat!" prefix
            cmd = ["log", f"{prev_tag}..HEAD", "--pretty=format:%s", "--grep=BREAKING CHANGE", "--grep=feat!"]
            cmd.extend(["--"] + dashboard_files_list)
            
            stdout, stderr, returncode = self._run_git_command(cmd)
            
            if returncode == 0 and stdout.strip():
                # Major version bump for breaking changes
                current_parts[0] += 1
                current_parts[1] = 0
                current_parts[2] = 0
            else:
                # Check for feature additions
                cmd = ["log", f"{prev_tag}..HEAD", "--pretty=format:%s", "--grep=feat"]
                cmd.extend(["--"] + dashboard_files_list)
                
                stdout, stderr, returncode = self._run_git_command(cmd)
                
                if returncode == 0 and stdout.strip():
                    # Minor version bump for features
                    current_parts[1] += 1
                    current_parts[2] = 0
        
        return '.'.join(map(str, current_parts))


# Helper functions

def get_dashboard_version_manager(project_root: str = None, archive_dir: str = None) -> DashboardVersionManager:
    """
    Create and return a dashboard version manager.
    
    Args:
        project_root: Root directory of the project
        archive_dir: Directory to archive dashboard versions
        
    Returns:
        Configured DashboardVersionManager instance
    """
    if project_root is None:
        # Try to determine project root
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)  # qa directory
        project_root = os.path.dirname(os.path.dirname(parent_dir))  # project root
    
    return DashboardVersionManager(project_root, archive_dir)


if __name__ == "__main__":
    # This script can be run directly to manage dashboard versions
    import argparse
    
    parser = argparse.ArgumentParser(description="Quantum 5D QA Dashboard Version Manager")
    parser.add_argument("--status", action="store_true", help="Show current version status")
    parser.add_argument("--bump", choices=["major", "minor", "patch"], 
                        help="Bump version (major, minor, or patch)")
    parser.add_argument("--archive", action="store_true", 
                        help="Archive current version without version bump")
    parser.add_argument("--release", choices=["major", "minor", "patch"], 
                        help="Create a new release with version bump")
    parser.add_argument("--no-commit", action="store_true", 
                        help="Do not commit changes to git")
    
    args = parser.parse_args()
    
    # Create version manager
    manager = get_dashboard_version_manager()
    
    if args.status or (not args.bump and not args.archive and not args.release):
        # Show status by default
        manager.print_version_status()
    
    if args.bump:
        new_version = manager.bump_version(args.bump)
        print(f"{Colors.GREEN}Bumped version to v{new_version}{Colors.ENDC}")
    
    if args.archive:
        archive_info = manager.archive_current_version(commit_changes=not args.no_commit)
        print(f"{Colors.GREEN}Archived version v{archive_info['version']}{Colors.ENDC}")
    
    if args.release:
        release_info = manager.create_dashboard_release(
            version_type=args.release,
            commit=not args.no_commit
        )
        if release_info["status"] == "success":
            print(f"{Colors.GREEN}Released dashboard v{release_info['version']}{Colors.ENDC}")
        else:
            print(f"{Colors.YELLOW}{release_info['message']}{Colors.ENDC}") 