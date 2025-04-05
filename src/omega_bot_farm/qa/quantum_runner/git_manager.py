"""
Git management system for the Quantum Test Runner.
"""

import os
import time
import logging
import subprocess
from typing import Dict, List, Any, Optional, Tuple

from .types import Colors

logger = logging.getLogger("0M3G4_B0TS_QA_AUT0_TEST_SUITES_RuNn3R_5D")

class GitManager:
    """Manages Git operations and provides smart commit suggestions."""
    
    def __init__(self, project_root: str):
        """Initialize the Git manager with project root path."""
        self.project_root = os.path.abspath(project_root)
        self.watched_files = set()
        self.file_contexts = {}  # Store context for each file
        self.change_history = []  # Track changes for better suggestions
        self.last_scan_time = 0
        
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
            logger.error(f"Error running git command: {e}")
            return "", str(e), 1
    
    def get_uncommitted_files(self) -> Dict[str, List[str]]:
        """
        Get list of all uncommitted files categorized by status.
        
        Returns a dictionary with keys:
        - 'modified' - Modified files
        - 'added' - New files staged for commit
        - 'deleted' - Deleted files
        - 'untracked' - New files not staged for commit
        - 'all' - All uncommitted files
        """
        self.last_scan_time = time.time()
        
        # Get status of tracked files
        stdout, stderr, returncode = self._run_git_command(["status", "--porcelain"])
        if returncode != 0:
            logger.error(f"Failed to get git status: {stderr}")
            return {
                'modified': [],
                'added': [],
                'deleted': [],
                'untracked': [],
                'all': []
            }
        
        modified = []
        added = []
        deleted = []
        untracked = []
        
        for line in stdout.strip().split('\n'):
            if not line:
                continue
                
            status = line[:2]
            file_path = line[3:].strip()
            
            # Update watched files set
            self.watched_files.add(file_path)
            
            if status.startswith('M'):  # Modified
                modified.append(file_path)
            elif status.startswith('A'):  # Added
                added.append(file_path)
            elif status.startswith('D'):  # Deleted
                deleted.append(file_path)
            elif status.startswith('??'):  # Untracked
                untracked.append(file_path)
            
        all_files = modified + added + deleted + untracked
        
        # Store results as a dictionary
        result = {
            'modified': modified,
            'added': added,
            'deleted': deleted,
            'untracked': untracked,
            'all': all_files
        }
        
        # Update file contexts
        self._update_file_contexts(all_files)
        
        return result
    
    def _update_file_contexts(self, files: List[str]) -> None:
        """Update context information for files."""
        for file_path in files:
            full_path = os.path.join(self.project_root, file_path)
            
            if file_path not in self.file_contexts:
                self.file_contexts[file_path] = {
                    'first_seen': time.time(),
                    'extension': os.path.splitext(file_path)[1],
                    'directory': os.path.dirname(file_path),
                    'diff_history': [],
                    'content_samples': [],
                    'related_files': []
                }
            
            # Get file diff if it's a modified file
            if os.path.exists(full_path) and os.path.isfile(full_path):
                # Get file diff for modified files
                stdout, stderr, returncode = self._run_git_command(["diff", file_path])
                if returncode == 0 and stdout:
                    self.file_contexts[file_path]['diff_history'].append({
                        'time': time.time(),
                        'diff': stdout
                    })
                    
                # Try to get a sample of the file content
                try:
                    with open(full_path, 'r', errors='ignore') as f:
                        content_sample = f.read(1000)  # Just read the first 1000 characters
                        self.file_contexts[file_path]['content_samples'].append({
                            'time': time.time(),
                            'content': content_sample
                        })
                except Exception as e:
                    logger.warning(f"Could not read content sample from {file_path}: {e}")
    
    def get_uncommitted_report(self) -> Dict[str, Any]:
        """Generate a report of uncommitted files."""
        uncommitted = self.get_uncommitted_files()
        
        # Convert to a format that's easier to process
        report = {
            'total_count': len(uncommitted['all']),
            'categories': {
                'modified': len(uncommitted['modified']),
                'added': len(uncommitted['added']),
                'deleted': len(uncommitted['deleted']),
                'untracked': len(uncommitted['untracked'])
            },
            'files': [],
            'timestamp': time.time()
        }
        
        # Get details for each file
        for file_path in uncommitted['all']:
            file_status = 'modified'
            if file_path in uncommitted['added']:
                file_status = 'added'
            elif file_path in uncommitted['deleted']:
                file_status = 'deleted'
            elif file_path in uncommitted['untracked']:
                file_status = 'untracked'
                
            file_info = {
                'path': file_path,
                'status': file_status,
                'extension': os.path.splitext(file_path)[1],
                'directory': os.path.dirname(file_path)
            }
            report['files'].append(file_info)
        
        # Group by directory
        directories = {}
        for file_info in report['files']:
            directory = file_info['directory']
            if directory not in directories:
                directories[directory] = {
                    'total': 0,
                    'modified': 0,
                    'added': 0,
                    'deleted': 0,
                    'untracked': 0
                }
            
            directories[directory]['total'] += 1
            directories[directory][file_info['status']] += 1
        
        report['directories'] = directories
        
        return report
    
    def suggest_commit_message(self) -> str:
        """Generate a commit message based on changed files."""
        uncommitted = self.get_uncommitted_files()
        
        if not uncommitted['all']:
            return "No uncommitted changes found."
        
        # Get the most common directories
        directories = {}
        for file_path in uncommitted['all']:
            directory = os.path.dirname(file_path)
            top_level = directory.split('/')[0] if '/' in directory else directory
            
            if top_level not in directories:
                directories[top_level] = 0
            directories[top_level] += 1
        
        # Sort directories by count
        sorted_dirs = sorted(directories.items(), key=lambda x: x[1], reverse=True)
        
        # Determine the scope
        scope = sorted_dirs[0][0] if sorted_dirs else "misc"
        
        # Determine the type of change
        change_type = "feat"
        if len(uncommitted['modified']) > len(uncommitted['added']):
            change_type = "fix" if len(uncommitted['modified']) < 5 else "refactor"
        
        # Special case for test files
        test_files = [f for f in uncommitted['all'] if 'test' in f.lower()]
        if len(test_files) > len(uncommitted['all']) / 2:
            change_type = "test"
        
        # Special case for docs
        doc_files = [f for f in uncommitted['all'] if f.endswith('.md') or 'doc' in f.lower()]
        if len(doc_files) > len(uncommitted['all']) / 2:
            change_type = "docs"
        
        # Count the number of files by extension
        extensions = {}
        for file_path in uncommitted['all']:
            ext = os.path.splitext(file_path)[1]
            if ext:
                if ext not in extensions:
                    extensions[ext] = 0
                extensions[ext] += 1
        
        # Get the most common extension
        common_ext = max(extensions.items(), key=lambda x: x[1])[0] if extensions else ""
        
        # Generate a simple message
        if len(uncommitted['all']) == 1:
            # Single file change
            file_path = uncommitted['all'][0]
            file_name = os.path.basename(file_path)
            
            if file_path in uncommitted['added']:
                return f"{change_type}({scope}): Add {file_name}"
            elif file_path in uncommitted['modified']:
                return f"{change_type}({scope}): Update {file_name}"
            elif file_path in uncommitted['deleted']:
                return f"{change_type}({scope}): Remove {file_name}"
            else:
                return f"{change_type}({scope}): Change {file_name}"
        
        # Multiple files
        if common_ext:
            return f"{change_type}({scope}): Update {common_ext[1:]} files"
        else:
            return f"{change_type}({scope}): Multiple changes"
    
    def suggest_git_tag(self) -> str:
        """Suggest a Git tag based on the current state."""
        # Get current commit
        stdout, stderr, returncode = self._run_git_command(["rev-parse", "HEAD"])
        if returncode != 0:
            logger.error(f"Failed to get current commit: {stderr}")
            return ""
        
        commit_hash = stdout.strip()
        
        # Get existing tags
        stdout, stderr, returncode = self._run_git_command(["tag"])
        if returncode != 0:
            logger.error(f"Failed to get tags: {stderr}")
            return ""
        
        tags = stdout.strip().split('\n') if stdout.strip() else []
        
        # Extract version tags
        version_tags = []
        for tag in tags:
            if tag.startswith('v') and '.' in tag:
                try:
                    # Try to parse the version
                    version = tag[1:]
                    parts = version.split('.')
                    if len(parts) >= 2 and all(part.isdigit() for part in parts):
                        version_tags.append(tag)
                except:
                    pass
        
        # Sort version tags
        version_tags.sort(key=lambda x: [int(part) for part in x[1:].split('.')])
        
        # If no version tags, start with v0.1.0
        if not version_tags:
            return "v0.1.0"
        
        # Get the latest version tag
        latest_tag = version_tags[-1]
        
        # Parse the version
        version = latest_tag[1:]
        parts = version.split('.')
        
        # Increment the patch version
        new_patch = int(parts[-1]) + 1
        
        # Create new version
        new_parts = parts[:-1] + [str(new_patch)]
        new_version = '.'.join(new_parts)
        
        return f"v{new_version}"
    
    def print_uncommitted_report(self, report: Dict[str, Any]) -> None:
        """Print a formatted report of uncommitted files."""
        if not report['files']:
            logger.info(f"{Colors.GREEN}No uncommitted changes found.{Colors.ENDC}")
            return
        
        # Show summary
        print(f"\n{Colors.CYAN}╔{'═' * 78}╗{Colors.ENDC}")
        print(f"{Colors.CYAN}║ {Colors.BOLD}UNCOMMITTED CHANGES REPORT{Colors.ENDC}{Colors.CYAN}{' ' * 55}║{Colors.ENDC}")
        print(f"{Colors.CYAN}╠{'═' * 78}╣{Colors.ENDC}")
        
        # Print categories
        print(f"{Colors.CYAN}║ {Colors.BOLD}Total Files:{Colors.ENDC} {report['total_count']}{' ' * (66 - len(str(report['total_count'])))}║{Colors.ENDC}")
        print(f"{Colors.CYAN}║{' ' * 78}║{Colors.ENDC}")
        
        print(f"{Colors.CYAN}║ {Colors.GREEN}Added:{Colors.ENDC} {report['categories']['added']}{' ' * (70 - len(str(report['categories']['added'])))}║{Colors.ENDC}")
        print(f"{Colors.CYAN}║ {Colors.BLUE}Modified:{Colors.ENDC} {report['categories']['modified']}{' ' * (67 - len(str(report['categories']['modified'])))}║{Colors.ENDC}")
        print(f"{Colors.CYAN}║ {Colors.RED}Deleted:{Colors.ENDC} {report['categories']['deleted']}{' ' * (68 - len(str(report['categories']['deleted'])))}║{Colors.ENDC}")
        print(f"{Colors.CYAN}║ {Colors.YELLOW}Untracked:{Colors.ENDC} {report['categories']['untracked']}{' ' * (66 - len(str(report['categories']['untracked'])))}║{Colors.ENDC}")
        
        # Print directories
        if report['directories']:
            # Sort directories by total count
            sorted_dirs = sorted(report['directories'].items(), key=lambda x: x[1]['total'], reverse=True)
            
            print(f"{Colors.CYAN}╠{'═' * 78}╣{Colors.ENDC}")
            print(f"{Colors.CYAN}║ {Colors.BOLD}TOP DIRECTORIES{Colors.ENDC}{Colors.CYAN}{' ' * 64}║{Colors.ENDC}")
            
            # Show top 5 directories
            for i, (directory, counts) in enumerate(sorted_dirs[:5]):
                # Truncate directory name if too long
                dir_display = directory
                if len(directory) > 40:
                    dir_display = "..." + directory[-37:]
                
                print(f"{Colors.CYAN}║ {Colors.PURPLE}{dir_display}:{Colors.ENDC} {counts['total']} files{' ' * (70 - len(dir_display) - len(str(counts['total'])) - 7)}║{Colors.ENDC}")
        
        # Print suggested commit message
        suggested_message = self.suggest_commit_message()
        print(f"{Colors.CYAN}╠{'═' * 78}╣{Colors.ENDC}")
        print(f"{Colors.CYAN}║ {Colors.BOLD}SUGGESTED COMMIT MESSAGE{Colors.ENDC}{Colors.CYAN}{' ' * 56}║{Colors.ENDC}")
        print(f"{Colors.CYAN}║ {Colors.GREEN}{suggested_message}{Colors.ENDC}{' ' * (77 - len(suggested_message))}║{Colors.ENDC}")
        
        # Print footer
        print(f"{Colors.CYAN}╚{'═' * 78}╝{Colors.ENDC}\n") 