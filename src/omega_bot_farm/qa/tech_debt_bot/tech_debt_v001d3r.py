#!/usr/bin/env python3
"""
T3CH D3BT V001D3R - CYBERITAL™ Edition - 0m3g4_k1ng
-----------------------------------------------------------------------
The Matrix-Reggae Quantum Watcher: Monitors codebase for tech debt,
eliminates wasteful patterns, and maintains the divine flow of the code.

Created under GBU2™ License with RASTA HEART ON F1R3
"""

import os
import sys
import time
import json
import glob
import re
import logging
import argparse
import asyncio
import threading
import subprocess
import difflib
import math
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple, Set
from pathlib import Path
import tempfile
import hashlib
import random

# Import for watching files
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add dotenv import for loading environment variables
from dotenv import load_dotenv

# For file matching
import fnmatch

# For accessing git information
try:
    import git
    HAVE_GIT = True
except ImportError:
    HAVE_GIT = False

# Import Discord for bot integration
try:
    import discord
    from discord import app_commands
    from discord.ext import commands, tasks
    HAVE_DISCORD = True
    print("✅ Discord.py successfully imported!")
except ImportError:
    print("❌ Discord.py not found. Discord integration will be disabled.")
    HAVE_DISCORD = False
    # Create placeholder discord module to avoid NameError
    class PlaceholderDiscord:
        class Intents:
            @staticmethod
            def default():
                return PlaceholderDiscord.IntentsObject()
                
        class IntentsObject:
            def __init__(self):
                self.message_content = False
                
        class Activity:
            def __init__(self, **kwargs):
                pass
                
        class ActivityType:
            watching = None
            
        class Embed:
            def __init__(self, **kwargs):
                pass
                
            def add_field(self, **kwargs):
                pass
                
            def set_footer(self, **kwargs):
                pass
                
            def timestamp(self, value):
                pass
                
    discord = PlaceholderDiscord()
    
    class PlaceholderCommands:
        class Bot:
            def __init__(self, **kwargs):
                self.user = None
                self.tree = PlaceholderTree()
                
            def event(self, func):
                return func
                
            def change_presence(self, **kwargs):
                pass
                
            def run(self, *args, **kwargs):
                pass
                
            def get_channel(self, channel_id):
                return None
                
        class Context:
            async def send(self, *args, **kwargs):
                pass
                
    class PlaceholderTree:
        def command(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator
            
        async def sync(self):
            pass
    
    commands = PlaceholderCommands()
    
    class PlaceholderAppCommands:
        def describe(**kwargs):
            def decorator(func):
                return func
            return decorator
            
    app_commands = PlaceholderAppCommands
    
    class PlaceholderTasks:
        def loop(**kwargs):
            def decorator(func):
                return func
            return decorator
    
    tasks = PlaceholderTasks()

# ASCII Art for TECH DEBT V001D3R
VOIDER_LOGO = """
████████╗███████╗ ██████╗██╗  ██╗    ██████╗ ███████╗██████╗ ████████╗
╚══██╔══╝██╔════╝██╔════╝██║  ██║    ██╔══██╗██╔════╝██╔══██╗╚══██╔══╝
   ██║   █████╗  ██║     ███████║    ██║  ██║█████╗  ██████╔╝   ██║   
   ██║   ██╔══╝  ██║     ██╔══██║    ██║  ██║██╔══╝  ██╔══██╗   ██║   
   ██║   ███████╗╚██████╗██║  ██║    ██████╔╝███████╗██████╔╝   ██║   
   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝    ╚═════╝ ╚══════╝╚═════╝    ╚═╝   
                                                                       
██╗   ██╗ ██████╗  ██████╗ ███╗   ███╗██████╗ ██████╗ ██████╗ ██╗     
██║   ██║██╔═████╗██╔═████╗████╗ ████║╚════██╗╚════██╗██╔══██╗██║     
██║   ██║██║██╔██║██║██╔██║██╔████╔██║ █████╔╝ █████╔╝██████╔╝██║     
╚██╗ ██╔╝████╔╝██║████╔╝██║██║╚██╔╝██║ ╚═══██╗ ╚═══██╗██╔══██╗██║     
 ╚████╔╝ ╚██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝██████╔╝██║  ██║███████╗
  ╚═══╝   ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
                                                                       
  ╔═══════════════════════════════════════════════════════════════╗
  ║  CYBERITAL™ - When MATRIX meets REGGAE to vanquish TECH DEBT  ║
  ╚═══════════════════════════════════════════════════════════════╝
"""

REGGAE_INTRO = """
🌈 DIVINE FLOW ACTIVATED - JAH BLESS THE CODEBASE 🌈
✨ GBU2™ CONSCIOUSNESS LEVEL 9: TRANSCENDENCE ✨
"""

# ANSI color codes for matrix/reggae theming
class Colors:
    RESET = "\033[0m"
    MATRIX_GREEN = "\033[38;5;46m"
    MATRIX_DARK_GREEN = "\033[38;5;22m"
    MATRIX_BRIGHT_GREEN = "\033[38;5;118m"
    MATRIX_CODE_GREEN = "\033[38;5;41m"
    RASTA_RED = "\033[38;5;196m"
    RASTA_YELLOW = "\033[38;5;226m"
    RASTA_GREEN = "\033[38;5;40m"
    CYBER_BLUE = "\033[38;5;39m"
    CYBER_PINK = "\033[38;5;213m"
    CYBER_PURPLE = "\033[38;5;141m"
    NEON_GREEN = "\033[38;5;82m"
    NEON_CYAN = "\033[38;5;51m"
    DARK_BG = "\033[48;5;17m"
    ERROR_RED = "\033[38;5;160m"
    WARNING_YELLOW = "\033[38;5;214m"
    SUCCESS_GREEN = "\033[38;5;76m"
    
    @staticmethod
    def format(text, color, bold=False):
        bold_code = "\033[1m" if bold else ""
        return f"{bold_code}{color}{text}{Colors.RESET}"
    
    @staticmethod
    def matrix_print(text, delay=0.01):
        """Print text with a matrix-like effect"""
        for char in text:
            color = random.choice([
                Colors.MATRIX_GREEN, 
                Colors.MATRIX_BRIGHT_GREEN, 
                Colors.MATRIX_CODE_GREEN
            ])
            sys.stdout.write(f"{color}{char}{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write("\n")

# Tech Debt patterns to detect
TECH_DEBT_PATTERNS = {
    "TODO comments": (r'#\s*TODO', 5),
    "FIXME comments": (r'#\s*FIXME', 8),
    "HACK comments": (r'#\s*HACK', 7),
    "Magic numbers": (r'=[^=]\s*[0-9]{4,}', 4),
    "Nested if statements": (r'if.*:\s*\n\s+if.*:\s*\n\s+if.*:', 6),
    "Long functions": (r'def\s+\w+\s*\([^)]*\).*\n(?:\s+[^\n]*\n){30,}', 7),
    "Commented code blocks": (r'(?:#[^\n]*\n){5,}', 4),
    "Hardcoded credentials": (r'password|secret|key|token\s*=\s*[\'"]\w+[\'"]', 9),
    "Print debugging": (r'print\s*\([\'"]DEBUG', 3),
    "Bare except clauses": (r'except\s*:', 6),
    "Redundant code": (r'(?:\s*\w+\s*=\s*\w+\s*\n){3,}', 5),
    "Deep nesting": (r'\n\s{24,}\w+', 6)
}

# Configure Discord embed colors
EMBED_COLORS = {
    "info": 0x00FF00,      # Green
    "warning": 0xFFFF00,    # Yellow
    "error": 0xFF0000,      # Red
    "matrix": 0x00FF41,     # Matrix green
    "reggae": 0xFFD700,     # Gold
    "tech_debt": 0xFF6B00,  # Orange
    "success": 0x00FFFF     # Cyan
}

# Configure logging with cyberpunk styling
def setup_logging(log_level=logging.INFO):
    log_format = f"{Colors.CYBER_PURPLE}[%(asctime)s]{Colors.RESET} {Colors.CYBER_PINK}|{Colors.RESET} {Colors.NEON_CYAN}%(levelname)s{Colors.RESET} {Colors.CYBER_PINK}|{Colors.RESET} {Colors.MATRIX_GREEN}%(message)s{Colors.RESET}"
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger("T3CH-D3BT-V001D3R")

class TechDebtDetector:
    """
    Detects technical debt in code and provides suggestions for improvement.
    """
    def __init__(self, 
                 project_root: Path,
                 ignore_patterns: Optional[List[str]] = None,
                 include_patterns: Optional[List[str]] = None):
        self.project_root = project_root
        self.ignore_patterns = ignore_patterns or [
            "*/venv/*", 
            "*/.git/*", 
            "*/node_modules/*", 
            "*/__pycache__/*",
            "*/build/*",
            "*/dist/*"
        ]
        self.include_patterns = include_patterns or [
            "*.py", "*.js", "*.ts", "*.tsx", "*.jsx", 
            "*.java", "*.kt", "*.c", "*.cpp", "*.h", 
            "*.cs", "*.go", "*.rb", "*.php"
        ]
        self.logger = logging.getLogger("T3CH-D3BT-V001D3R.Detector")
        self.debt_database = {}  # Path -> List of issues
        self.debt_history = {}   # Track debt over time
        self.matrix_activation_level = 0  # Increases with each detection
        self.reggae_harmony_level = 100   # Decreases with tech debt
        
    def scan_codebase(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Perform a complete scan of the codebase for technical debt
        """
        self.logger.info(f"{Colors.format('Initiating quantum scan of the codebase', Colors.CYBER_BLUE, True)}")
        self.debt_database = {}
        total_files = 0
        total_issues = 0
        
        # Get all matching files
        for include_pattern in self.include_patterns:
            pattern = os.path.join(self.project_root, "**", include_pattern)
            files = glob.glob(pattern, recursive=True)
            
            for file_path in files:
                if self._should_ignore(file_path):
                    continue
                    
                total_files += 1
                relative_path = os.path.relpath(file_path, self.project_root)
                
                # Print matrix-style scanning animation
                if total_files % 10 == 0:
                    scan_msg = f"[SCAN] {relative_path}"
                    Colors.matrix_print(scan_msg, delay=0.001)
                
                issues = self.analyze_file(file_path)
                if issues:
                    self.debt_database[relative_path] = issues
                    total_issues += len(issues)
        
        # Update history
        timestamp = datetime.now().isoformat()
        self.debt_history[timestamp] = {
            "total_files": total_files,
            "total_issues": total_issues,
            "debt_score": self._calculate_debt_score()
        }
        
        self.logger.info(f"{Colors.format('Matrix scan complete', Colors.MATRIX_GREEN, True)} - " +
                        f"Analyzed {Colors.format(total_files, Colors.RASTA_YELLOW)} files, " +
                        f"Found {Colors.format(total_issues, Colors.RASTA_RED)} tech debt issues")
        
        # Update Matrix activation level based on debt found
        self.matrix_activation_level = min(100, self.matrix_activation_level + (total_issues // 5))
        
        # Update Reggae harmony level
        self.reggae_harmony_level = max(0, 100 - (total_issues // 2))
        
        return self.debt_database
    
    def analyze_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Analyze a single file for technical debt
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            issues = []
            for name, (pattern, severity) in TECH_DEBT_PATTERNS.items():
                matches = re.finditer(pattern, content)
                for match in matches:
                    line_number = content.count('\n', 0, match.start()) + 1
                    code_snippet = self._get_code_snippet(content, line_number)
                    issues.append({
                        'name': name,
                        'severity': severity,
                        'line_number': line_number,
                        'match': match.group(0),
                        'snippet': code_snippet,
                        'suggestion': self._generate_suggestion(name, match.group(0))
                    })
            
            return issues
            
        except Exception as e:
            self.logger.error(f"Error analyzing file {file_path}: {str(e)}")
            return []
    
    def analyze_changes(self, file_path: str, old_content: str, new_content: str) -> List[Dict[str, Any]]:
        """
        Analyze changes in a file for new technical debt
        """
        issues = []
        
        # Get diff between old and new content
        diff = list(difflib.unified_diff(
            old_content.splitlines(True),
            new_content.splitlines(True),
            n=0
        ))
        
        # Extract added lines (starting with '+')
        added_lines = [line[1:] for line in diff if line.startswith('+') and not line.startswith('+++')]
        added_content = ''.join(added_lines)
        
        # Check added content for tech debt patterns
        for name, (pattern, severity) in TECH_DEBT_PATTERNS.items():
            matches = re.finditer(pattern, added_content)
            for match in matches:
                # Approximate line number in the new content
                line_number = added_content.count('\n', 0, match.start()) + 1
                
                # Get actual line number in the full new content
                actual_line_number = self._map_to_full_line_number(new_content, added_content, line_number)
                
                issues.append({
                    'name': name,
                    'severity': severity,
                    'line_number': actual_line_number,
                    'match': match.group(0),
                    'snippet': self._get_code_snippet(new_content, actual_line_number),
                    'suggestion': self._generate_suggestion(name, match.group(0)),
                    'is_new': True
                })
        
        return issues
    
    def _map_to_full_line_number(self, full_content: str, added_content: str, added_line_number: int) -> int:
        """Map a line number in added content to its position in the full content"""
        # This is a simplified approach - for a real implementation, you'd need a more
        # sophisticated algorithm to accurately map lines
        added_lines = added_content.splitlines()
        if added_line_number > len(added_lines):
            return 1  # Default to first line if out of range
            
        target_line = added_lines[added_line_number - 1]
        full_lines = full_content.splitlines()
        
        for i, line in enumerate(full_lines):
            if line.strip() == target_line.strip():
                return i + 1
                
        return 1  # Default to first line if not found
    
    def _should_ignore(self, file_path: str) -> bool:
        """Check if a file should be ignored"""
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(file_path, pattern):
                return True
        return False
    
    def _get_code_snippet(self, content: str, line_number: int, context: int = 2) -> str:
        """Get code snippet around the specified line number"""
        lines = content.splitlines()
        start = max(0, line_number - context - 1)
        end = min(len(lines), line_number + context)
        
        result = []
        for i in range(start, end):
            line_prefix = f"{i+1:4d} | " 
            if i == line_number - 1:
                result.append(f"{line_prefix}{Colors.format(lines[i], Colors.RASTA_RED)}")
            else:
                result.append(f"{line_prefix}{lines[i]}")
                
        return "\n".join(result)
    
    def _generate_suggestion(self, issue_type: str, matched_text: str) -> str:
        """Generate a suggestion for fixing the technical debt"""
        suggestions = {
            "TODO comments": "Replace TODO with a GitHub issue or implement the missing functionality",
            "FIXME comments": "Address the issue before it becomes legacy debt",
            "HACK comments": "Refactor this hack into a proper implementation",
            "Magic numbers": f"Replace {matched_text} with a named constant",
            "Nested if statements": "Refactor nested conditions with early returns or a state machine",
            "Long functions": "Break down this function into smaller, reusable components",
            "Commented code blocks": "Remove dead code or document why it's being kept",
            "Hardcoded credentials": "Move credentials to environment variables or secrets manager",
            "Print debugging": "Replace with proper logging",
            "Bare except clauses": "Specify exact exceptions to catch",
            "Redundant code": "Extract repeated patterns into reusable functions",
            "Deep nesting": "Reduce nesting by extracting methods or using guard clauses"
        }
        
        if issue_type in suggestions:
            return suggestions[issue_type]
        
        return "Consider refactoring this code"
    
    def _calculate_debt_score(self) -> float:
        """Calculate an overall technical debt score for the codebase"""
        if not self.debt_database:
            return 0.0
            
        total_severity = 0
        issue_count = 0
        
        for file_path, issues in self.debt_database.items():
            for issue in issues:
                total_severity += issue['severity']
                issue_count += 1
                
        if issue_count == 0:
            return 0.0
            
        # Normalized score from 0-100, where higher is worse
        return min(100, (total_severity * issue_count) / 10)
    
    def get_debt_trends(self) -> Dict[str, Any]:
        """Get trends of technical debt over time"""
        if len(self.debt_history) < 2:
            return {
                "trend": "unknown",
                "data": list(self.debt_history.values()),
                "change_percent": 0.0
            }
            
        # Get the two most recent entries
        timestamps = sorted(self.debt_history.keys())
        current = self.debt_history[timestamps[-1]]
        previous = self.debt_history[timestamps[-2]]
        
        current_score = current["debt_score"]
        previous_score = previous["debt_score"]
        
        if previous_score == 0:
            change_percent = 100 if current_score > 0 else 0
        else:
            change_percent = ((current_score - previous_score) / previous_score) * 100
            
        trend = "improving" if change_percent < 0 else "worsening" if change_percent > 0 else "stable"
        
        return {
            "trend": trend,
            "data": [self.debt_history[t] for t in timestamps],
            "change_percent": change_percent
        }
    
    def generate_tech_debt_report(self) -> Dict[str, Any]:
        """Generate a comprehensive technical debt report"""
        issues_by_severity = {}
        files_by_issues = {}
        total_issues = 0
        
        for file_path, issues in self.debt_database.items():
            total_issues += len(issues)
            files_by_issues[file_path] = len(issues)
            
            for issue in issues:
                severity = issue['severity']
                if severity not in issues_by_severity:
                    issues_by_severity[severity] = []
                issues_by_severity[severity].append({
                    'file': file_path,
                    'line': issue['line_number'],
                    'issue': issue['name'],
                    'snippet': issue['snippet']
                })
        
        # Sort files by number of issues
        top_files = sorted(files_by_issues.items(), key=lambda x: x[1], reverse=True)[:10]
        
        debt_score = self._calculate_debt_score()
        trends = self.get_debt_trends()
        
        # Calculate "vibes" based on debt score
        if debt_score < 20:
            vibe = "DIVINE FLOW"
        elif debt_score < 40:
            vibe = "RASTAFARIAN RHYTHM"
        elif debt_score < 60:
            vibe = "MATRIX RIPPLES"
        elif debt_score < 80:
            vibe = "DIGITAL TURBULENCE"
        else:
            vibe = "CYBER CHAOS"
        
        report = {
            "total_issues": total_issues,
            "debt_score": debt_score,
            "vibe": vibe,
            "matrix_level": self.matrix_activation_level,
            "reggae_level": self.reggae_harmony_level,
            "trends": trends,
            "top_files": top_files,
            "issues_by_severity": issues_by_severity,
            "timestamp": datetime.now().isoformat(),
            "suggestions": self._generate_top_suggestions()
        }
        
        return report
    
    def _generate_top_suggestions(self) -> List[str]:
        """Generate top suggestions for improving the codebase"""
        if not self.debt_database:
            return ["Codebase is in divine harmony. Jah bless!"]
            
        issue_types = {}
        for file_path, issues in self.debt_database.items():
            for issue in issues:
                issue_type = issue['name']
                if issue_type not in issue_types:
                    issue_types[issue_type] = 0
                issue_types[issue_type] += 1
                
        # Sort by frequency
        sorted_issues = sorted(issue_types.items(), key=lambda x: x[1], reverse=True)
        
        suggestions = []
        for issue_type, count in sorted_issues[:5]:
            for pattern, (_, severity) in TECH_DEBT_PATTERNS.items():
                if pattern == issue_type:
                    suggestions.append(f"Fix {count} instances of {issue_type} (Severity: {severity}/10)")
                    break
        
        return suggestions

class CodebaseWatcher:
    """
    Watches the codebase for changes and detects technical debt in real-time.
    """
    def __init__(self, 
                 project_root: Path,
                 tech_debt_detector: TechDebtDetector,
                 discord_connector: Optional[Any] = None):
        self.project_root = project_root
        self.tech_debt_detector = tech_debt_detector
        self.discord_connector = discord_connector
        self.logger = logging.getLogger("T3CH-D3BT-V001D3R.Watcher")
        self.observer = Observer()
        self.file_cache = {}  # Stores the previous content of files
        self.is_running = False
        self.watch_paths = []
        
    def watch(self, paths: Optional[List[str]] = None, exclude_dirs: Optional[List[str]] = None):
        """Start watching the specified paths"""
        if paths is None:
            paths = [str(self.project_root)]
            
        if exclude_dirs is None:
            exclude_dirs = ["venv", ".git", "node_modules", "__pycache__", "build", "dist"]
            
        self.watch_paths = paths
        self.logger.info(f"{Colors.format('Initializing Matrix vision...', Colors.MATRIX_GREEN, True)}")
        
        # Create event handler
        event_handler = TechDebtEventHandler(
            self.tech_debt_detector, 
            self.discord_connector,
            self._on_file_change,
            exclude_dirs
        )
        
        # Schedule watching
        for path in paths:
            self.logger.info(f"Watching path: {path}")
            self.observer.schedule(event_handler, path, recursive=True)
            
        # Start the observer
        self.observer.start()
        self.is_running = True
        Colors.matrix_print("MATRIX VISION ACTIVATED - ALL FILES UNDER SURVEILLANCE", delay=0.01)
        
        self._build_initial_cache()
        
    def stop(self):
        """Stop watching the codebase"""
        if self.is_running:
            self.logger.info(f"{Colors.format('Deactivating Matrix vision...', Colors.CYBER_BLUE)}")
            self.observer.stop()
            self.observer.join()
            self.is_running = False
            self.logger.info("File watching stopped")
    
    def _build_initial_cache(self):
        """Build the initial cache of file contents"""
        self.logger.info("Building initial file cache...")
        
        include_patterns = self.tech_debt_detector.include_patterns
        
        for pattern in include_patterns:
            for watch_path in self.watch_paths:
                full_pattern = os.path.join(watch_path, "**", pattern)
                files = glob.glob(full_pattern, recursive=True)
                
                for file_path in files:
                    if not self.tech_debt_detector._should_ignore(file_path):
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                self.file_cache[file_path] = content
                        except Exception as e:
                            self.logger.warning(f"Could not cache file {file_path}: {str(e)}")
        
        self.logger.info(f"Cached {len(self.file_cache)} files for change detection")
        
    def _on_file_change(self, file_path: str, event_type: str):
        """
        Handle file change events by analyzing for tech debt
        """
        if event_type not in ["modified", "created"]:
            return
            
        if not os.path.exists(file_path):
            return
            
        try:
            # Read new content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                new_content = f.read()
                
            old_content = self.file_cache.get(file_path, "")
            
            # Update cache
            self.file_cache[file_path] = new_content
            
            # Skip if no old content (new file)
            if not old_content and event_type == "modified":
                return
                
            # Analyze changes
            relative_path = os.path.relpath(file_path, self.project_root)
            
            if event_type == "created":
                self.logger.info(f"{Colors.format('NEW FILE DETECTED', Colors.RASTA_GREEN)}: {relative_path}")
                issues = self.tech_debt_detector.analyze_file(file_path)
            else:
                self.logger.info(f"{Colors.format('FILE MODIFIED', Colors.MATRIX_CODE_GREEN)}: {relative_path}")
                issues = self.tech_debt_detector.analyze_changes(file_path, old_content, new_content)
            
            # If we found issues, report them
            if issues:
                self.logger.warning(f"Found {len(issues)} potential tech debt issues in {relative_path}")
                
                # Send to Discord if available
                if self.discord_connector and hasattr(self.discord_connector, 'send_tech_debt_alert'):
                    self.discord_connector.send_tech_debt_alert(relative_path, issues, event_type)
            else:
                green_msg = "DIVINE FLOW MAINTAINED"
                Colors.matrix_print(green_msg, delay=0.005)
                
        except Exception as e:
            self.logger.error(f"Error processing file change for {file_path}: {str(e)}")


class TechDebtEventHandler(FileSystemEventHandler):
    """
    Event handler for file system events
    """
    def __init__(self, 
                 tech_debt_detector: TechDebtDetector,
                 discord_connector: Optional[Any],
                 callback: callable,
                 exclude_dirs: List[str]):
        self.tech_debt_detector = tech_debt_detector
        self.discord_connector = discord_connector
        self.callback = callback
        self.exclude_dirs = exclude_dirs
        self.logger = logging.getLogger("T3CH-D3BT-V001D3R.EventHandler")
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        file_path = event.src_path
        if self._should_process(file_path):
            self.callback(file_path, "modified")
            
    def on_created(self, event):
        if event.is_directory:
            return
            
        file_path = event.src_path
        if self._should_process(file_path):
            self.callback(file_path, "created")
    
    def _should_process(self, file_path: str) -> bool:
        """Determine if we should process this file"""
        # Check excluded directories
        for exclude_dir in self.exclude_dirs:
            if f"/{exclude_dir}/" in file_path or file_path.endswith(f"/{exclude_dir}"):
                return False
                
        # Check if it matches any include pattern
        include_patterns = self.tech_debt_detector.include_patterns
        for pattern in include_patterns:
            # Convert glob pattern to regex for matching
            pattern_regex = pattern.replace(".", "\\.").replace("*", ".*")
            if re.search(pattern_regex, file_path):
                return True
                
        return False

class DiscordBot:
    """
    Discord bot implementation for tech debt reporting.
    """
    def __init__(self, 
                 token: Optional[str] = None, 
                 app_id: Optional[str] = None,
                 tech_debt_detector: Optional[TechDebtDetector] = None,
                 logger=None):
        # Get credentials from parameters or environment
        self.token = token or os.environ.get('TECH_DEBT_BOT_TOKEN')
        self.app_id = app_id or os.environ.get('TECH_DEBT_APP_ID')
        self.tech_debt_detector = tech_debt_detector
        self.logger = logger or logging.getLogger("T3CH-D3BT-V001D3R.Discord")
        
        # Debug output for Discord connection
        self.logger.info(f"DiscordBot initialization with token: {'SET' if self.token else 'NOT SET'}, app_id: {'SET' if self.app_id else 'NOT SET'}")
        if not self.token:
            self.logger.error(f"Discord bot token is missing! Check your .env file.")
        if not self.app_id:
            self.logger.error(f"Discord app ID is missing! Check your .env file.")
        
        # Initialize bot intents
        intents = discord.Intents.default()
        intents.message_content = True
        
        # Create bot instance
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        self.report_channel_id = None
        self._initialize_commands()
        
    def _initialize_commands(self):
        """Initialize bot commands and events"""
        
        @self.bot.event
        async def on_ready():
            self.logger.info(f"{Colors.format('Discord bot is connected!', Colors.SUCCESS_GREEN, True)}")
            self.logger.info(f"Bot name: {self.bot.user.name}")
            self.logger.info(f"Bot ID: {self.bot.user.id}")
            self.logger.info(f"Bot discriminator: {self.bot.user.discriminator}")
            self.logger.info(f"Connected to {len(self.bot.guilds)} guild(s)")
            
            await self.bot.tree.sync()
            self.logger.info(f"{Colors.format('Discord slash commands are synced!', Colors.MATRIX_BRIGHT_GREEN, True)}")
            
            Colors.matrix_print(f"DISCORD NEURAL LINK ESTABLISHED AS {self.bot.user}", delay=0.003)
            
            # Set bot activity
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name="for TECH DEBT in the MATRIX"
                )
            )
            
            self._setup_report_channel()
            
        @self.bot.event
        async def on_connect():
            self.logger.info(f"{Colors.format('Discord bot has connected to gateway!', Colors.RASTA_GREEN, True)}")
            
        @self.bot.event
        async def on_disconnect():
            self.logger.error(f"{Colors.format('Discord bot has disconnected from gateway!', Colors.RASTA_RED, True)}")
            
        @self.bot.event
        async def on_error(event, *args, **kwargs):
            self.logger.error(f"Discord event error in {event}: {sys.exc_info()[1]}")
            
        @self.bot.event
        async def on_guild_join(guild):
            self.logger.info(f"Bot joined new guild: {guild.name}")
            # Try to find a suitable channel to send welcome message
            general_channel = discord.utils.get(guild.text_channels, name="general")
            target_channel = general_channel or guild.text_channels[0] if guild.text_channels else None
            
            if target_channel:
                embed = discord.Embed(
                    title="🧩 TECH DEBT V001D3R has entered the MATRIX 🧩",
                    description=(
                        "Greetings, programs! I am here to hunt down tech debt "
                        "and bring divine reggae harmony to your code.\n\n"
                        "Use `/v001d3r_help` to see available commands."
                    ),
                    color=EMBED_COLORS["matrix"]
                )
                embed.set_footer(text="Created with RASTA HEART ON F1R3 🔥")
                
                await target_channel.send(embed=embed)
        
        # Command error handler
        @self.bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandNotFound):
                return
                
            self.logger.error(f"Command error: {str(error)}")
            await ctx.send(f"⚠️ Error: {str(error)}")
            
        # Help command
        @self.bot.tree.command(name="v001d3r_help", description="Show help for the TECH DEBT V001D3R")
        async def slash_help(interaction: discord.Interaction):
            embed = discord.Embed(
                title="🧩 TECH DEBT V001D3R Commands 🧩",
                description="Here are the commands you can use:",
                color=EMBED_COLORS["matrix"]
            )
            
            embed.add_field(
                name="`/scan`", 
                value="Scan the entire codebase for tech debt", 
                inline=False
            )
            embed.add_field(
                name="`/report`", 
                value="Generate a tech debt report", 
                inline=False
            )
            embed.add_field(
                name="`/set_report_channel`", 
                value="Set the channel for tech debt reports", 
                inline=False
            )
            embed.add_field(
                name="`/scan_file [file_path]`", 
                value="Scan a specific file for tech debt",
                inline=False
            )
            embed.add_field(
                name="`/top_issues`", 
                value="Show the top tech debt issues", 
                inline=False
            )
            
            embed.set_footer(text="CYBERITAL™ - When MATRIX meets REGGAE")
            
            await interaction.response.send_message(embed=embed)
            
        # Scan command
        @self.bot.tree.command(name="scan", description="Scan the codebase for tech debt")
        async def slash_scan(interaction: discord.Interaction):
            if not self.tech_debt_detector:
                await interaction.response.send_message("⚠️ Tech debt detector not initialized!")
                return
                
            await interaction.response.defer(thinking=True)
            
            # Matrix-style loading message
            await interaction.followup.send("```\nINITIATING QUANTUM SCAN...\n[####################] 100%\nMATRIX VISION ACTIVATED```")
            
            # Run the scan
            debt_database = self.tech_debt_detector.scan_codebase()
            total_issues = sum(len(issues) for issues in debt_database.values())
            
            # Create embed report
            embed = discord.Embed(
                title="🧬 TECH DEBT MATRIX SCAN COMPLETE 🧬",
                description=f"Found **{total_issues}** tech debt issues across the codebase.",
                color=EMBED_COLORS["tech_debt"]
            )
            
            # Add top issues if there are any
            if total_issues > 0:
                top_files = sorted(
                    [(path, len(issues)) for path, issues in debt_database.items()],
                    key=lambda x: x[1],
                    reverse=True
                )[:5]
                
                files_list = "\n".join([f"`{path}`: **{count}** issues" for path, count in top_files])
                embed.add_field(
                    name="🔍 Top Files with Tech Debt",
                    value=files_list or "No issues found",
                    inline=False
                )
                
                # Add suggestions
                suggestions = self.tech_debt_detector._generate_top_suggestions()
                suggestions_list = "\n".join([f"• {suggestion}" for suggestion in suggestions])
                embed.add_field(
                    name="💡 Suggestions",
                    value=suggestions_list,
                    inline=False
                )
                
                # Add debt score
                debt_score = self.tech_debt_detector._calculate_debt_score()
                embed.add_field(
                    name="🧮 Tech Debt Score",
                    value=f"**{debt_score:.1f}/100**",
                    inline=True
                )
                
                # Add matrix level
                matrix_level = self.tech_debt_detector.matrix_activation_level
                embed.add_field(
                    name="🖥️ Matrix Activation",
                    value=f"**{matrix_level}/100**",
                    inline=True
                )
                
                # Add reggae harmony level
                reggae_level = self.tech_debt_detector.reggae_harmony_level
                embed.add_field(
                    name="🎵 Reggae Harmony",
                    value=f"**{reggae_level}/100**",
                    inline=True
                )
            else:
                embed.description += "\n\n✨ **DIVINE FLOW DETECTED!** ✨\nYour codebase is in perfect harmony."
                embed.color = EMBED_COLORS["success"]
                
            embed.set_footer(text=f"CYBERITAL™ - Scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            await interaction.followup.send(embed=embed)
            
        # Report command
        @self.bot.tree.command(name="report", description="Generate a comprehensive tech debt report")
        async def slash_report(interaction: discord.Interaction):
            if not self.tech_debt_detector:
                await interaction.response.send_message("⚠️ Tech debt detector not initialized!")
                return
                
            await interaction.response.defer(thinking=True)
            
            # Generate the report
            report = self.tech_debt_detector.generate_tech_debt_report()
            
            # Create main embed
            embed = discord.Embed(
                title=f"🧩 TECH DEBT REPORT - {report['vibe']} 🧩",
                description=(
                    f"**Tech Debt Score:** {report['debt_score']:.1f}/100\n"
                    f"**Total Issues:** {report['total_issues']}\n"
                    f"**Matrix Level:** {report['matrix_level']}/100\n"
                    f"**Reggae Harmony:** {report['reggae_level']}/100\n\n"
                ),
                color=self._get_color_for_debt_score(report['debt_score'])
            )
            
            # Add trends
            trend_text = report['trends']['trend']
            change_percent = report['trends']['change_percent']
            trend_emoji = "📈" if trend_text == "worsening" else "📉" if trend_text == "improving" else "📊"
            
            embed.add_field(
                name=f"{trend_emoji} Trend",
                value=f"Tech debt is **{trend_text}** ({change_percent:.1f}% change)",
                inline=False
            )
            
            # Add top file list if there are issues
            if report['top_files']:
                top_files_text = "\n".join([f"`{path}`: **{count}** issues" for path, count in report['top_files'][:5]])
                embed.add_field(
                    name="🔍 Top Tech Debt Files",
                    value=top_files_text,
                    inline=False
                )
            
            # Add suggestions
            suggestions_text = "\n".join([f"• {s}" for s in report['suggestions'][:5]])
            embed.add_field(
                name="💡 Suggestions",
                value=suggestions_text or "No suggestions needed",
                inline=False
            )
            
            # Set timestamp and footer
            embed.timestamp = datetime.now()
            embed.set_footer(text="CYBERITAL™ - When MATRIX meets REGGAE to vanquish TECH DEBT")
            
            # Send the report
            await interaction.followup.send(embed=embed)
            
            # Send additional embeds for high severity issues if there are any
            high_severity_issues = report['issues_by_severity'].get(8, []) + report['issues_by_severity'].get(9, []) + report['issues_by_severity'].get(10, [])
            
            if high_severity_issues:
                high_sev_embed = discord.Embed(
                    title="⚠️ HIGH SEVERITY TECH DEBT ISSUES ⚠️",
                    description="These issues should be addressed immediately:",
                    color=EMBED_COLORS["error"]
                )
                
                for idx, issue in enumerate(high_severity_issues[:5]):
                    high_sev_embed.add_field(
                        name=f"{idx+1}. {issue['issue']} in {issue['file']}",
                        value=f"Line {issue['line']}\n```{issue['snippet']}```",
                        inline=False
                    )
                
                await interaction.followup.send(embed=high_sev_embed)
                
        # Set report channel command
        @self.bot.tree.command(name="set_report_channel", description="Set the channel for tech debt reports")
        async def slash_set_report_channel(interaction: discord.Interaction):
            # Check if the user has admin permissions
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("⚠️ You need administrator permissions to use this command!", ephemeral=True)
                return
                
            # Use the current channel
            self.report_channel_id = interaction.channel_id
            self.logger.info(f"Set report channel to {interaction.channel.name} ({self.report_channel_id})")
            
            await interaction.response.send_message(f"✅ Set this channel as the tech debt report channel!")
            
        # Scan specific file command
        @self.bot.tree.command(name="scan_file", description="Scan a specific file for tech debt")
        @app_commands.describe(file_path="Path to the file to scan, relative to the project root")
        async def slash_scan_file(interaction: discord.Interaction, file_path: str):
            if not self.tech_debt_detector:
                await interaction.response.send_message("⚠️ Tech debt detector not initialized!")
                return
                
            await interaction.response.defer(thinking=True)
            
            # Build the full path
            full_path = os.path.join(self.tech_debt_detector.project_root, file_path)
            
            # Check if the file exists
            if not os.path.exists(full_path):
                await interaction.followup.send(f"⚠️ File not found: `{file_path}`")
                return
                
            # Scan the file
            issues = self.tech_debt_detector.analyze_file(full_path)
            
            # Create embed
            embed = discord.Embed(
                title=f"🧬 Tech Debt Scan: {file_path} 🧬",
                description=f"Found **{len(issues)}** tech debt issues.",
                color=EMBED_COLORS["matrix"] if issues else EMBED_COLORS["success"]
            )
            
            # Add issues
            if issues:
                for i, issue in enumerate(issues[:10]):  # Limit to 10 issues to avoid too long messages
                    embed.add_field(
                        name=f"{i+1}. {issue['name']} (Severity: {issue['severity']}/10)",
                        value=(
                            f"Line {issue['line_number']}\n"
                            f"```{issue['snippet']}```\n"
                            f"**Suggestion**: {issue['suggestion']}"
                        ),
                        inline=False
                    )
                    
                if len(issues) > 10:
                    embed.add_field(
                        name="...",
                        value=f"And {len(issues) - 10} more issues. Run a full report for details.",
                        inline=False
                    )
            else:
                embed.description += "\n\n✨ **DIVINE FLOW DETECTED!** ✨\nThis file is in perfect harmony."
                
            embed.set_footer(text=f"CYBERITAL™ - Scan completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            await interaction.followup.send(embed=embed)
            
        # Top issues command
        @self.bot.tree.command(name="top_issues", description="Show the top tech debt issues")
        @app_commands.describe(count="Number of issues to show (default: 5)")
        async def slash_top_issues(interaction: discord.Interaction, count: int = 5):
            if not self.tech_debt_detector:
                await interaction.response.send_message("⚠️ Tech debt detector not initialized!")
                return
                
            await interaction.response.defer(thinking=True)
            
            # Get all issues sorted by severity
            all_issues = []
            for file_path, issues in self.tech_debt_detector.debt_database.items():
                for issue in issues:
                    all_issues.append({
                        'file': file_path,
                        'issue': issue
                    })
                    
            # Sort by severity
            sorted_issues = sorted(all_issues, key=lambda x: x['issue']['severity'], reverse=True)
            
            # Create embed
            embed = discord.Embed(
                title="🔍 Top Tech Debt Issues",
                description=f"Showing the top {min(count, len(sorted_issues))} tech debt issues by severity:",
                color=EMBED_COLORS["tech_debt"]
            )
            
            # Add issues
            if sorted_issues:
                for i, issue_data in enumerate(sorted_issues[:count]):
                    issue = issue_data['issue']
                    file_path = issue_data['file']
                    
                    embed.add_field(
                        name=f"{i+1}. {issue['name']} (Severity: {issue['severity']}/10)",
                        value=(
                            f"File: `{file_path}`\n"
                            f"Line {issue['line_number']}\n"
                            f"```{issue['snippet']}```\n"
                            f"**Suggestion**: {issue['suggestion']}"
                        ),
                        inline=False
                    )
            else:
                embed.description = "✨ **DIVINE FLOW DETECTED!** ✨\nNo tech debt issues found."
                embed.color = EMBED_COLORS["success"]
                
            embed.set_footer(text=f"CYBERITAL™ - When MATRIX meets REGGAE to vanquish TECH DEBT")
            
            await interaction.followup.send(embed=embed)
        
    def _setup_report_channel(self):
        """Setup the report channel if configured"""
        if not self.report_channel_id:
            return
            
        # Verify that the channel exists
        channel = self.bot.get_channel(int(self.report_channel_id))
        if not channel:
            self.logger.warning(f"Could not find report channel with ID {self.report_channel_id}")
            return
            
        self.logger.info(f"Tech debt reports will be sent to #{channel.name}")
    
    def send_tech_debt_alert(self, file_path: str, issues: List[Dict[str, Any]], event_type: str):
        """Send a tech debt alert to the report channel"""
        if not self.report_channel_id or not self.bot.is_ready():
            return
            
        # Queue the alert to be sent in the Discord event loop
        asyncio.run_coroutine_threadsafe(
            self._send_tech_debt_alert_async(file_path, issues, event_type),
            self.bot.loop
        )
    
    async def _send_tech_debt_alert_async(self, file_path: str, issues: List[Dict[str, Any]], event_type: str):
        """Send a tech debt alert to the report channel (async version)"""
        if not self.report_channel_id:
            return
            
        channel = self.bot.get_channel(int(self.report_channel_id))
        if not channel:
            self.logger.warning(f"Could not find report channel with ID {self.report_channel_id}")
            return
            
        # Create embed
        embed = discord.Embed(
            title=f"⚠️ TECH DEBT DETECTED IN {'NEW' if event_type == 'created' else 'MODIFIED'} FILE ⚠️",
            description=f"File: `{file_path}`\nFound **{len(issues)}** tech debt issues.",
            color=EMBED_COLORS["warning"]
        )
        
        # Add highest severity issues
        sorted_issues = sorted(issues, key=lambda x: x['severity'], reverse=True)
        for i, issue in enumerate(sorted_issues[:3]):  # Show top 3 issues
            embed.add_field(
                name=f"{i+1}. {issue['name']} (Severity: {issue['severity']}/10)",
                value=(
                    f"Line {issue['line_number']}\n"
                    f"```{issue['snippet']}```\n"
                    f"**Suggestion**: {issue['suggestion']}"
                ),
                inline=False
            )
            
        if len(issues) > 3:
            embed.add_field(
                name="...",
                value=f"And {len(issues) - 3} more issues. Use `/scan_file {file_path}` for details.",
                inline=False
            )
            
        embed.set_footer(text=f"CYBERITAL™ - Alert triggered at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        await channel.send(embed=embed)
    
    def _get_color_for_debt_score(self, score: float) -> int:
        """Get color based on debt score"""
        if score < 20:
            return EMBED_COLORS["success"]
        elif score < 40:
            return EMBED_COLORS["reggae"]
        elif score < 60:
            return EMBED_COLORS["matrix"]
        elif score < 80:
            return EMBED_COLORS["warning"]
        else:
            return EMBED_COLORS["error"]
                
    def is_configured(self) -> bool:
        """Check if the bot is configured with token and app ID"""
        return bool(self.token and self.app_id)
        
    def start(self) -> bool:
        """Start the Discord bot in a separate thread"""
        if not self.is_configured():
            self.logger.error("Discord bot is not configured properly. Check token and app ID.")
            return False
            
        try:
            self.logger.info(f"{Colors.format('Starting Discord bot thread...', Colors.CYBER_BLUE)}")
            
            # Run the bot in a separate thread to avoid blocking the main thread
            thread = threading.Thread(
                target=self._run_discord_bot,
                daemon=True
            )
            thread.start()
            
            self.logger.info(f"{Colors.format('Discord bot thread started!', Colors.SUCCESS_GREEN)}")
            return True
        except Exception as e:
            self.logger.error(f"Error starting Discord bot thread: {str(e)}")
            import traceback
            self.logger.error(f"Exception details: {traceback.format_exc()}")
            return False
    
    def _run_discord_bot(self):
        """Run the Discord bot (in a thread)"""
        self.logger.info(f"{Colors.format('Discord bot thread running', Colors.MATRIX_GREEN)}")
        
        # Verify token
        if not self.token:
            self.logger.error("Discord bot token is missing!")
            return
            
        self.logger.info(f"Bot token length: {len(self.token)}")
        self.logger.info(f"Bot token starts with: {self.token[:5]}...")
        self.logger.info(f"Using App ID: {self.app_id}")
            
        try:
            # Use run_forever to handle reconnection
            self.bot.run(self.token, reconnect=True, log_handler=None)
        except discord.errors.LoginFailure as e:
            self.logger.error(f"Discord login failed. Invalid token: {str(e)}")
            self.logger.error("Please check that your TECH_DEBT_BOT_TOKEN is correct in the .env file")
        except discord.errors.PrivilegedIntentsRequired as e:
            self.logger.error(f"Privileged intents not enabled for this bot: {str(e)}")
            self.logger.error("Please enable the Message Content intent in the Discord Developer Portal")
        except discord.errors.HTTPException as e:
            self.logger.error(f"HTTP error connecting to Discord: {str(e)}")
            self.logger.error("This could be a network issue or Discord service outage")
        except Exception as e:
            self.logger.error(f"Error running Discord bot: {str(e)}")
            # Print detailed exception info
            import traceback
            self.logger.error(f"Exception details: {traceback.format_exc()}")

class TechDebtV001d3r:
    """
    Main class for the Tech Debt V001d3r application.
    Coordinates between the tech debt detector, codebase watcher, and Discord bot.
    """
    def __init__(self, project_root: Optional[Path] = None):
        # Load environment variables
        load_dotenv()
        
        # Set up project root
        self.project_root = project_root or Path(os.getcwd())
        
        # Set up logging
        self.logger = setup_logging()
        
        # Set up tech debt detector
        self.tech_debt_detector = TechDebtDetector(self.project_root)
        
        # Set up Discord bot only if Discord is available
        token = os.environ.get('TECH_DEBT_BOT_TOKEN')
        app_id = os.environ.get('TECH_DEBT_APP_ID')
        if HAVE_DISCORD:
            self.discord_bot = DiscordBot(token, app_id, self.tech_debt_detector, self.logger)
        else:
            self.discord_bot = None
        
        # Set up codebase watcher
        self.codebase_watcher = CodebaseWatcher(
            self.project_root,
            self.tech_debt_detector,
            self.discord_bot if HAVE_DISCORD else None
        )
        
        self.matrix_mode = False
    
    def display_intro(self):
        """Display the intro banner"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Colors.DARK_BG}{Colors.MATRIX_GREEN}{VOIDER_LOGO}{Colors.RESET}")
        print(f"{Colors.RASTA_RED}{REGGAE_INTRO}{Colors.RESET}")
        print(f"\n{Colors.MATRIX_GREEN}Initializing T3CH D3BT V001D3R...{Colors.RESET}")
        time.sleep(1)
        print(f"{Colors.CYBER_BLUE}Project root: {self.project_root}{Colors.RESET}")
        
        # Matrix effect for initializing
        effects = [
            "Loading quantum computing matrices...",
            "Calibrating reggae harmonics...",
            "Initializing tech debt patterns...",
            "Connecting to the divine flow...",
            "Activating matrix vision...",
            "Establishing neural links...",
            "Unfolding cosmic consciousness..."
        ]
        
        for effect in effects:
            Colors.matrix_print(effect, delay=0.005)
            time.sleep(0.2)
            
        print(f"\n{Colors.RASTA_GREEN}🌈 INITIALIZATION COMPLETE - JAH BLESS 🌈{Colors.RESET}\n")
    
    def run(self, discord_mode: bool = False, watch_mode: bool = True):
        """Run the tech debt voider"""
        self.display_intro()
        
        # Do an initial scan
        self.logger.info("Running initial tech debt scan...")
        self.tech_debt_detector.scan_codebase()
        report = self.tech_debt_detector.generate_tech_debt_report()
        
        # Print report summary
        print(f"\n{Colors.CYBER_PURPLE}========================{Colors.RESET}")
        print(f"{Colors.MATRIX_GREEN}TECH DEBT REPORT{Colors.RESET}")
        print(f"{Colors.CYBER_PURPLE}========================{Colors.RESET}")
        print(f"{Colors.RASTA_YELLOW}Tech Debt Score: {report['debt_score']:.1f}/100{Colors.RESET}")
        print(f"{Colors.RASTA_GREEN}Total Issues: {report['total_issues']}{Colors.RESET}")
        print(f"{Colors.MATRIX_CODE_GREEN}Matrix Level: {report['matrix_level']}/100{Colors.RESET}")
        print(f"{Colors.RASTA_RED}Reggae Harmony: {report['reggae_level']}/100{Colors.RESET}")
        print(f"{Colors.CYBER_BLUE}Vibe: {report['vibe']}{Colors.RESET}")
        print(f"{Colors.CYBER_PURPLE}========================{Colors.RESET}")
        
        # Start Discord bot if requested
        if discord_mode and HAVE_DISCORD:
            if self.discord_bot.is_configured():
                self.logger.info("Starting Discord bot...")
                discord_thread = threading.Thread(target=self.discord_bot.start, daemon=True)
                discord_thread.start()
                self.logger.info(f"{Colors.format('Discord bot thread started!', Colors.NEON_GREEN)}")
            else:
                self.logger.warning("Discord bot not configured properly. Set TECH_DEBT_BOT_TOKEN and TECH_DEBT_APP_ID environment variables.")
        
        # Start watching if requested
        if watch_mode:
            self.logger.info("Starting codebase watcher...")
            self.codebase_watcher.watch()
            
        # Enter the main loop if in watch mode
        if watch_mode:
            try:
                while True:
                    cmd = input(f"{Colors.MATRIX_GREEN}> {Colors.RESET}").strip().lower()
                    
                    if cmd in ['exit', 'quit', 'q']:
                        self.logger.info("Exiting...")
                        break
                    elif cmd == 'scan':
                        self.tech_debt_detector.scan_codebase()
                        report = self.tech_debt_detector.generate_tech_debt_report()
                        print(f"{Colors.MATRIX_GREEN}Tech Debt Score: {report['debt_score']:.1f}/100{Colors.RESET}")
                    elif cmd == 'report':
                        report = self.tech_debt_detector.generate_tech_debt_report()
                        print(f"\n{Colors.CYBER_PURPLE}========================{Colors.RESET}")
                        print(f"{Colors.MATRIX_GREEN}TECH DEBT REPORT{Colors.RESET}")
                        print(f"{Colors.CYBER_PURPLE}========================{Colors.RESET}")
                        print(f"{Colors.RASTA_YELLOW}Tech Debt Score: {report['debt_score']:.1f}/100{Colors.RESET}")
                        print(f"{Colors.RASTA_GREEN}Total Issues: {report['total_issues']}{Colors.RESET}")
                        print(f"{Colors.MATRIX_CODE_GREEN}Matrix Level: {report['matrix_level']}/100{Colors.RESET}")
                        print(f"{Colors.RASTA_RED}Reggae Harmony: {report['reggae_level']}/100{Colors.RESET}")
                        print(f"{Colors.CYBER_BLUE}Vibe: {report['vibe']}{Colors.RESET}")
                        print(f"{Colors.CYBER_PURPLE}========================{Colors.RESET}")
                    elif cmd == 'matrix':
                        self.matrix_mode = not self.matrix_mode
                        print(f"{Colors.MATRIX_GREEN}Matrix mode: {'ON' if self.matrix_mode else 'OFF'}{Colors.RESET}")
                        if self.matrix_mode:
                            Colors.matrix_print("THE MATRIX HAS YOU...", delay=0.05)
                    elif cmd == 'help':
                        print(f"{Colors.CYBER_BLUE}Available commands:{Colors.RESET}")
                        print(f"{Colors.RASTA_GREEN}scan{Colors.RESET} - Run a tech debt scan")
                        print(f"{Colors.RASTA_GREEN}report{Colors.RESET} - Generate a tech debt report")
                        print(f"{Colors.RASTA_GREEN}matrix{Colors.RESET} - Toggle matrix mode")
                        print(f"{Colors.RASTA_GREEN}exit/quit/q{Colors.RESET} - Exit the program")
                    elif cmd:
                        print(f"{Colors.MATRIX_RED}Unknown command. Type 'help' for available commands.{Colors.RESET}")
                        
            except KeyboardInterrupt:
                print(f"\n{Colors.RASTA_RED}Keyboard interrupt received. Exiting...{Colors.RESET}")
            finally:
                if watch_mode:
                    self.codebase_watcher.stop()
    
    def stop(self):
        """Stop all components"""
        self.codebase_watcher.stop()

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="T3CH D3BT V001D3R - CYBERITAL™ Edition")
    parser.add_argument("-p", "--path", help="Path to the project root", type=str)
    parser.add_argument("-d", "--discord", help="Run with Discord bot integration", action="store_true")
    parser.add_argument("-w", "--watch", help="Watch the codebase for changes", action="store_true", default=True)
    parser.add_argument("-s", "--scan-only", help="Scan the codebase once and exit", action="store_true")
    parser.add_argument("-v", "--verbose", help="Enable verbose logging", action="store_true")
    
    return parser.parse_args()

def main():
    """Main entry point"""
    args = parse_args()
    
    # Set up logging level
    log_level = logging.DEBUG if args.verbose else logging.INFO
    
    # Set project root
    project_root = Path(args.path) if args.path else Path.cwd()
    
    # Create the voider with Discord support
    voider = TechDebtV001d3r(project_root)
    
    # Run in appropriate mode
    if args.scan_only:
        voider.run(discord_mode=False, watch_mode=False)
    else:
        voider.run(discord_mode=args.discord, watch_mode=args.watch)

if __name__ == "__main__":
    main() 