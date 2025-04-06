#!/usr/bin/env python3
"""
Code Metrics Service Micromodule
--------------------------------

This microservice handles code quality metrics:
- Lines of code tracking
- Code complexity analysis
- Refactoring suggestions based on refactoring.guru principles
- Code smell detection
"""

import os
import re
import time
import logging
import json
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime

# Configure logging
logger = logging.getLogger("code_metrics_service")

# Constants
MAX_RECOMMENDED_LOC = 420  # Maximum recommended lines of code per file
MAX_RECOMMENDED_METHOD_LOC = 60  # Maximum recommended lines per method
MAX_RECOMMENDED_CLASS_LOC = 300  # Maximum recommended lines per class


class RefactoringGuru:
    """
    Refactoring recommendations based on refactoring.guru principles.
    """
    
    @staticmethod
    def get_code_smell(file_size: int, method_sizes: Dict[str, int], class_sizes: Dict[str, int]) -> List[Dict[str, Any]]:
        """
        Detect code smells based on size metrics.
        
        Args:
            file_size: Size of the file in lines
            method_sizes: Dictionary of method names and their sizes in lines
            class_sizes: Dictionary of class names and their sizes in lines
            
        Returns:
            List of code smell descriptions
        """
        smells = []
        
        # Check for "Large Class" smell
        for class_name, size in class_sizes.items():
            if size > MAX_RECOMMENDED_CLASS_LOC:
                smells.append({
                    "type": "Large Class",
                    "element": class_name,
                    "description": f"Class '{class_name}' has {size} lines of code (recommended max: {MAX_RECOMMENDED_CLASS_LOC})",
                    "refactoring": "Extract Class, Extract Interface, or Move Method",
                    "details": "https://refactoring.guru/smells/large-class",
                    "severity": min(10, max(1, int(size / MAX_RECOMMENDED_CLASS_LOC)))
                })
        
        # Check for "Long Method" smell
        for method_name, size in method_sizes.items():
            if size > MAX_RECOMMENDED_METHOD_LOC:
                smells.append({
                    "type": "Long Method",
                    "element": method_name,
                    "description": f"Method '{method_name}' has {size} lines of code (recommended max: {MAX_RECOMMENDED_METHOD_LOC})",
                    "refactoring": "Extract Method or Replace Temp with Query",
                    "details": "https://refactoring.guru/smells/long-method",
                    "severity": min(10, max(1, int(size / MAX_RECOMMENDED_METHOD_LOC)))
                })
        
        # Check for "Large File" smell (not a standard smell but practical)
        if file_size > MAX_RECOMMENDED_LOC:
            smells.append({
                "type": "Large File",
                "element": "File",
                "description": f"File has {file_size} lines of code (recommended max: {MAX_RECOMMENDED_LOC})",
                "refactoring": "Extract Class, Move Method, or Split into Modules",
                "details": "https://refactoring.guru/refactoring/techniques/moving-features-between-objects",
                "severity": min(10, max(1, int(file_size / MAX_RECOMMENDED_LOC)))
            })
        
        return smells
    
    @staticmethod
    def suggest_refactoring(smell_type: str) -> Dict[str, Any]:
        """
        Get specific refactoring suggestions for a code smell.
        
        Args:
            smell_type: Type of code smell
            
        Returns:
            Dictionary with refactoring suggestions
        """
        suggestions = {
            "Large Class": {
                "techniques": [
                    "Extract Class: Move some related fields and methods to a new class",
                    "Extract Subclass: Move specialized behavior to a subclass",
                    "Extract Interface: Extract common behavior into an interface"
                ],
                "benefits": [
                    "Improves readability and maintainability",
                    "Makes the code more modular",
                    "Follows the Single Responsibility Principle"
                ],
                "link": "https://refactoring.guru/extract-class"
            },
            "Long Method": {
                "techniques": [
                    "Extract Method: Move code fragment to a separate method",
                    "Replace Temp with Query: Replace temporary variable with a query method",
                    "Introduce Parameter Object: Replace a long list of parameters with an object",
                    "Decompose Conditional: Extract complex conditional logic into separate methods"
                ],
                "benefits": [
                    "Improves readability and understanding",
                    "Makes code more reusable",
                    "Reduces cognitive load when reading the code"
                ],
                "link": "https://refactoring.guru/extract-method"
            },
            "Large File": {
                "techniques": [
                    "Split into Modules: Divide the file into multiple smaller modules",
                    "Extract Class: Move related functionality to new classes",
                    "Apply Microservices Architecture: Split functionality into separate services"
                ],
                "benefits": [
                    "Improves maintainability",
                    "Makes the codebase more navigable",
                    "Enables better team collaboration"
                ],
                "link": "https://refactoring.guru/decompose-conditional"
            }
        }
        
        return suggestions.get(smell_type, {
            "techniques": ["Consider refactoring to reduce complexity"],
            "benefits": ["Will improve maintainability and readability"],
            "link": "https://refactoring.guru/"
        })


class CodeMetricsCollector:
    """Collects metrics about code files."""
    
    def __init__(self, project_root: str, metrics_dir: str = None):
        """
        Initialize the code metrics collector.
        
        Args:
            project_root: Path to the project root
            metrics_dir: Directory to store metrics (default: <project_root>/.quantum/metrics)
        """
        self.project_root = Path(project_root).resolve()
        
        if metrics_dir:
            self.metrics_dir = Path(metrics_dir).resolve()
        else:
            self.metrics_dir = self.project_root / ".quantum" / "metrics"
            
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        self.watched_dirs: Set[Path] = set()
        self.scanned_files: Dict[str, Dict[str, Any]] = {}
        self.running = False
        self._scanner_thread = None
        self._lock = threading.Lock()
        self.metrics_file = self.metrics_dir / "code_metrics.json"
        self._load_metrics()
    
    def _load_metrics(self):
        """Load metrics from disk if they exist."""
        self.metrics = {
            "last_scan": None,
            "file_metrics": {},
            "project_metrics": {
                "total_files": 0,
                "total_lines": 0,
                "total_code_lines": 0,
                "avg_file_size": 0,
                "large_files": []
            }
        }
        
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, "r") as f:
                    self.metrics = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"Error loading code metrics: {e}")
    
    def _save_metrics(self):
        """Save metrics to disk."""
        try:
            with open(self.metrics_file, "w") as f:
                json.dump(self.metrics, f, indent=2)
        except IOError as e:
            logger.error(f"Error saving code metrics: {e}")
    
    def watch_directory(self, dir_path: str, extensions: List[str] = None):
        """
        Add a directory to watch for code metrics collection.
        
        Args:
            dir_path: Path to the directory
            extensions: Optional list of file extensions to include
        """
        if extensions is None:
            extensions = [".py", ".js", ".java", ".cpp", ".c", ".go", ".rb", ".php"]
            
        path = Path(dir_path)
        if not path.is_absolute():
            path = self.project_root / path
        
        if not path.exists() or not path.is_dir():
            logger.warning(f"Directory does not exist: {path}")
            return
        
        with self._lock:
            self.watched_dirs.add((path, tuple(extensions)))
    
    def analyze_python_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Analyze a Python file to extract code metrics.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            Dictionary with code metrics
        """
        metrics = {
            "path": str(file_path),
            "relative_path": str(file_path.relative_to(self.project_root)) if self.project_root in file_path.parents else str(file_path),
            "size": 0,
            "code_lines": 0,
            "comment_lines": 0,
            "blank_lines": 0,
            "classes": {},
            "methods": {},
            "updated": datetime.now().isoformat()
        }
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                
            metrics["size"] = len(lines)
            
            in_multiline_comment = False
            current_class = None
            current_method = None
            class_start_line = 0
            method_start_line = 0
            line_num = 0
            
            for line in lines:
                line_num += 1
                stripped = line.strip()
                
                # Skip blank lines
                if not stripped:
                    metrics["blank_lines"] += 1
                    continue
                
                # Handle multi-line comments/strings
                if in_multiline_comment:
                    metrics["comment_lines"] += 1
                    if '"""' in stripped or "'''" in stripped:
                        in_multiline_comment = False
                    continue
                
                # Check for multi-line comment/string start
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    metrics["comment_lines"] += 1
                    if not (stripped.endswith('"""') and len(stripped) > 3) and not (stripped.endswith("'''") and len(stripped) > 3):
                        in_multiline_comment = True
                    continue
                
                # Single line comments
                if stripped.startswith("#"):
                    metrics["comment_lines"] += 1
                    continue
                
                # Count as code line
                metrics["code_lines"] += 1
                
                # Class definition
                class_match = re.match(r"^class\s+(\w+)\s*(\(.*\))?:", stripped)
                if class_match:
                    current_class = class_match.group(1)
                    class_start_line = line_num
                    metrics["classes"][current_class] = {"start": line_num, "end": line_num, "size": 0}
                    continue
                
                # Method definition
                method_match = re.match(r"^(?:async\s+)?def\s+(\w+)\s*\(", stripped)
                if method_match:
                    current_method = method_match.group(1)
                    if current_class:
                        current_method = f"{current_class}.{current_method}"
                    method_start_line = line_num
                    metrics["methods"][current_method] = {"start": line_num, "end": line_num, "size": 0}
                    continue
            
            # Process classes and methods
            current_class = None
            current_method = None
            line_num = 0
            method_indent = 0
            class_indent = 0
            
            for line in lines:
                line_num += 1
                if not line.strip():
                    continue
                
                # Calculate indentation level
                indent_level = len(line) - len(line.lstrip())
                
                # Check for class end
                if current_class and indent_level <= class_indent:
                    metrics["classes"][current_class]["end"] = line_num - 1
                    metrics["classes"][current_class]["size"] = (
                        metrics["classes"][current_class]["end"] - metrics["classes"][current_class]["start"] + 1
                    )
                    current_class = None
                
                # Check for method end
                if current_method and indent_level <= method_indent:
                    metrics["methods"][current_method]["end"] = line_num - 1
                    metrics["methods"][current_method]["size"] = (
                        metrics["methods"][current_method]["end"] - metrics["methods"][current_method]["start"] + 1
                    )
                    current_method = None
                
                # Class definition
                class_match = re.match(r"^class\s+(\w+)\s*(\(.*\))?:", line.strip())
                if class_match:
                    current_class = class_match.group(1)
                    class_indent = indent_level
                    metrics["classes"][current_class] = {"start": line_num, "end": line_num, "size": 1}
                    continue
                
                # Method definition
                method_match = re.match(r"^(?:async\s+)?def\s+(\w+)\s*\(", line.strip())
                if method_match:
                    method_name = method_match.group(1)
                    if current_class:
                        method_name = f"{current_class}.{method_name}"
                    current_method = method_name
                    method_indent = indent_level
                    metrics["methods"][current_method] = {"start": line_num, "end": line_num, "size": 1}
                    continue
                
                # Count lines in current class/method
                if current_class:
                    metrics["classes"][current_class]["size"] += 1
                if current_method:
                    metrics["methods"][current_method]["size"] += 1
            
            # Analyze code smells
            method_sizes = {name: data["size"] for name, data in metrics["methods"].items()}
            class_sizes = {name: data["size"] for name, data in metrics["classes"].items()}
            
            metrics["code_smells"] = RefactoringGuru.get_code_smell(
                metrics["size"], method_sizes, class_sizes
            )
            
            # Add refactoring suggestions if there are smells
            metrics["refactoring_suggestions"] = []
            for smell in metrics["code_smells"]:
                suggestions = RefactoringGuru.suggest_refactoring(smell["type"])
                metrics["refactoring_suggestions"].append({
                    "smell": smell["type"],
                    "element": smell["element"],
                    "suggestions": suggestions
                })
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {e}")
            return metrics
    
    def scan_files(self):
        """Scan all watched directories for code metrics."""
        all_files = []
        
        with self._lock:
            for dir_path, extensions in self.watched_dirs:
                for ext in extensions:
                    all_files.extend(dir_path.glob(f"**/*{ext}"))
        
        logger.info(f"Found {len(all_files)} files to analyze")
        
        total_lines = 0
        total_code_lines = 0
        large_files = []
        
        for file_path in all_files:
            if file_path.suffix == ".py":
                metrics = self.analyze_python_file(file_path)
                with self._lock:
                    rel_path = str(file_path.relative_to(self.project_root)) if self.project_root in file_path.parents else str(file_path)
                    self.metrics["file_metrics"][rel_path] = metrics
                    
                total_lines += metrics["size"]
                total_code_lines += metrics["code_lines"]
                
                if metrics["size"] > MAX_RECOMMENDED_LOC:
                    large_files.append({
                        "path": rel_path,
                        "size": metrics["size"],
                        "smells": len(metrics["code_smells"])
                    })
        
        # Update project metrics
        with self._lock:
            self.metrics["project_metrics"]["total_files"] = len(all_files)
            self.metrics["project_metrics"]["total_lines"] = total_lines
            self.metrics["project_metrics"]["total_code_lines"] = total_code_lines
            self.metrics["project_metrics"]["avg_file_size"] = total_lines / len(all_files) if all_files else 0
            self.metrics["project_metrics"]["large_files"] = large_files
            self.metrics["last_scan"] = datetime.now().isoformat()
            
            self._save_metrics()
        
        logger.info(f"Completed code metrics scan: {len(all_files)} files, {total_lines} lines")
        
        # Print refactoring alerts
        for file_info in large_files:
            logger.warning(
                f"⚠️ REFACTORING ALERT: {file_info['path']} has {file_info['size']} lines "
                f"(exceeds recommended {MAX_RECOMMENDED_LOC}) - Consult refactoring.guru for strategies"
            )
    
    def scanner_loop(self):
        """Run the continuous file scanning loop."""
        logger.info("Starting code metrics scanner")
        self.running = True
        
        while self.running:
            try:
                self.scan_files()
            except Exception as e:
                logger.error(f"Error in code metrics scanner: {e}")
            
            # Sleep for a while before next scan
            for _ in range(600):  # Sleep for 10 minutes
                if not self.running:
                    break
                time.sleep(1)
    
    def start(self):
        """Start the code metrics collector in a background thread."""
        if self._scanner_thread and self._scanner_thread.is_alive():
            logger.warning("Code metrics collector is already running")
            return
        
        self._scanner_thread = threading.Thread(target=self.scanner_loop, daemon=True)
        self._scanner_thread.start()
    
    def stop(self):
        """Stop the code metrics collector."""
        logger.info("Stopping code metrics collector")
        self.running = False
        if self._scanner_thread:
            self._scanner_thread.join(timeout=5.0)
    
    def get_file_metrics(self, file_path: str) -> Dict[str, Any]:
        """
        Get metrics for a specific file.
        
        Args:
            file_path: Path to the file (relative to project root)
            
        Returns:
            Dictionary with file metrics
        """
        with self._lock:
            return self.metrics["file_metrics"].get(file_path, {})
    
    def get_project_metrics(self) -> Dict[str, Any]:
        """
        Get overall project metrics.
        
        Returns:
            Dictionary with project metrics
        """
        with self._lock:
            return self.metrics["project_metrics"]

# Example usage when module is run directly
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    collector = CodeMetricsCollector(".")
    
    # Watch Python files in the current directory
    collector.watch_directory(".", extensions=[".py"])
    
    # Run a one-time scan
    collector.scan_files()
    
    # Print large files
    for file_info in collector.metrics["project_metrics"]["large_files"]:
        print(f"Large file: {file_info['path']} ({file_info['size']} lines)")
        
        # Get detailed metrics
        metrics = collector.get_file_metrics(file_info["path"])
        if metrics:
            for smell in metrics.get("code_smells", []):
                print(f"  - {smell['type']}: {smell['description']}")
                print(f"    Suggested refactoring: {smell['refactoring']}")
                print(f"    Details: {smell['details']}") 