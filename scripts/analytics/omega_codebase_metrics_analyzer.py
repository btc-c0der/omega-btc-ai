#!/usr/bin/env python3

# ✨🔬 GBU2™ License Notice - Consciousness Level 8 🧬🌌
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
🧪⚛️ Omega Codebase Metrics Analyzer ⚛️🧪
-----------------------------------------

This quantum observer collapses the wavefunction of your codebase into measurable metrics including:
- File counts by type (observables)
- Lines of code statistics (discrete quanta)
- Code complexity (wavefunction collapse potential)
- Linux compatibility checks (system entanglement)
- Test coverage status (quantum certainty)
- Technical debt indicators (entropy accumulation)
- Module dependencies (quantum entanglement map)
- Golden ratio compliance (quantum harmonic resonance)

The observer effect: By measuring these properties, we influence the future state of the codebase.

Usage:
    python omega_codebase_metrics_analyzer.py [--path=/path/to/scan] [--output=metrics.json] [--redis-save] [--redis-host=localhost] [--redis-port=6379] [--redis-key=metrics:latest]
"""

import os
import sys
import json
import re
import subprocess
import datetime
import platform
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict
import argparse
import logging

# 🧠 Configure quantum logging channel 🧠
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("OmegaQuantumObserver")

# 🌀 Quantum constants 🌀
GOLDEN_RATIO = 1.618  # Divine proportion - a quantum resonance pattern
CODE_FILE_EXTENSIONS = {
    'python': ['.py'],
    'javascript': ['.js', '.jsx', '.ts', '.tsx'],
    'markup': ['.html', '.xml', '.md', '.svg'],
    'styles': ['.css', '.scss', '.sass'],
    'data': ['.json', '.yaml', '.yml'],
    'config': ['.ini', '.toml', '.env', '.conf'],
    'shell': ['.sh', '.bash'],
    'docker': ['Dockerfile', '.dockerignore', 'docker-compose.yml']
}
IGNORED_DIRS = [
    '.git',
    'node_modules',
    '__pycache__',
    'venv',
    'env',
    'build',
    'dist',
    '.vscode',
    '.idea'
]

# 📏 Quantum thresholds from ZION_TRAIN_V2_ROADMAP 📏
THRESHOLDS = {
    "test_coverage_min": 75.0,  # "Test coverage higher than 75% is superb"
    "class_loc_max": 333,       # "When a class LoC is above 333, we apply a modules refactoring"
    "complexity_warning": 20,   # Reasonable threshold for complexity warnings
    "complexity_critical": 50,  # Critical complexity threshold
    "linux_compatibility_target": 0.5  # Target for Linux compatibility score (0-1)
}

@dataclass
class FileMetrics:
    """🧬 Quantum File Observer - Collapses file wavefunctions into measurable states 🧬"""
    path: str
    size_bytes: int = 0
    lines_total: int = 0
    lines_code: int = 0
    lines_comment: int = 0
    lines_blank: int = 0
    complexity: int = 0
    has_linux_mentions: bool = False
    linux_mentions_count: int = 0
    functions_count: int = 0
    classes_count: int = 0
    todo_count: int = 0
    fixme_count: int = 0
    golden_ratio_score: float = 0.0
    
    def calculate_metrics_from_content(self, content: str) -> None:
        """⚛️ Quantum measurement: Extract observables from file content wavefunction ⚛️"""
        lines = content.splitlines()
        self.lines_total = len(lines)
        
        comment_patterns = {
            'py': r'^\s*#',
            'js': r'^\s*(\/\/|\/\*|\*)',
            'html': r'^\s*<!--'
        }
        
        ext = os.path.splitext(self.path)[1].lower()
        pattern_key = None
        
        if ext in ['.py']:
            pattern_key = 'py'
        elif ext in ['.js', '.jsx', '.ts', '.tsx']:
            pattern_key = 'js'
        elif ext in ['.html', '.xml', '.svg']:
            pattern_key = 'html'
        
        # Count lines
        for line in lines:
            stripped = line.strip()
            if not stripped:
                self.lines_blank += 1
            elif pattern_key and re.match(comment_patterns[pattern_key], stripped):
                self.lines_comment += 1
            else:
                self.lines_code += 1
        
        # Check for Linux mentions
        linux_pattern = re.compile(r'linux', re.IGNORECASE)
        self.linux_mentions_count = len(linux_pattern.findall(content.lower()))
        self.has_linux_mentions = self.linux_mentions_count > 0
        
        # Count TODOs and FIXMEs
        self.todo_count = len(re.findall(r'TODO|FIXME', content))
        self.fixme_count = len(re.findall(r'FIXME', content))
        
        # Count classes and functions (rough estimate for Python)
        if ext in ['.py']:
            self.classes_count = len(re.findall(r'^\s*class\s+\w+', content, re.MULTILINE))
            self.functions_count = len(re.findall(r'^\s*def\s+\w+', content, re.MULTILINE))
        elif ext in ['.js', '.jsx', '.ts', '.tsx']:
            self.classes_count = len(re.findall(r'class\s+\w+|^\s*class\s+\w+', content, re.MULTILINE))
            self.functions_count = len(re.findall(r'function\s+\w+|^\s*\w+\s*=\s*function|^\s*\w+\s*\([^)]*\)\s*{', content, re.MULTILINE))
        
        # Calculate golden ratio score (code:comment ratio compared to phi)
        if self.lines_comment > 0:
            actual_ratio = self.lines_code / self.lines_comment
            self.golden_ratio_score = abs(actual_ratio - GOLDEN_RATIO)
        else:
            self.golden_ratio_score = float('inf')  # No comments = infinite distance from golden ratio
        
        # Estimate complexity (very rough, based on nesting and branching)
        self.complexity = self._estimate_complexity(content)
    
    def _estimate_complexity(self, content: str) -> int:
        """🔮 Quantum complexity estimator: Measures file's probability density function 🔮"""
        complexity = 0
        ext = os.path.splitext(self.path)[1].lower()
        
        if ext in ['.py']:
            # Count if/elif, for, while, try/except
            complexity += len(re.findall(r'\s+if\s+|\s+elif\s+|\s+for\s+|\s+while\s+|\s+try\s*:', content))
            # Count nested structures (indentation level changes)
            indent_changes = re.findall(r'^\s{4,}[^\s]', content, re.MULTILINE)
            complexity += len(indent_changes) // 4  # Rough estimate of nesting levels
        elif ext in ['.js', '.jsx', '.ts', '.tsx']:
            # Count if, for, while, switch, try
            complexity += len(re.findall(r'\s+if\s*\(|\s+for\s*\(|\s+while\s*\(|\s+switch\s*\(|\s+try\s*{', content))
            # Count nested structures (braces)
            open_braces = content.count('{')
            close_braces = content.count('}')
            complexity += min(open_braces, close_braces) // 2  # Rough estimate of nesting
        
        return complexity

@dataclass
class DirectoryMetrics:
    """🌌 Quantum Directory Observer - Maps the spacetime structure of code folders 🌌"""
    path: str
    file_count: int = 0
    files_by_type: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    total_size_bytes: int = 0
    total_lines_code: int = 0
    total_lines_comment: int = 0
    total_lines_blank: int = 0
    linux_compatible_estimate: float = 0.0  # 0-1 score
    average_complexity: float = 0.0
    file_metrics: Dict[str, FileMetrics] = field(default_factory=dict)
    subdirectories: Dict[str, 'DirectoryMetrics'] = field(default_factory=dict)
    technical_debt_score: float = 0.0
    highest_complexity_file: str = ""
    highest_complexity: int = 0
    
    def aggregate_metrics(self) -> None:
        """🔄 Quantum aggregation: Combine wavefunctions into unified quantum state 🔄"""
        # Sum up file metrics
        for file_path, file_metric in self.file_metrics.items():
            self.file_count += 1
            self.total_size_bytes += file_metric.size_bytes
            self.total_lines_code += file_metric.lines_code
            self.total_lines_comment += file_metric.lines_comment
            self.total_lines_blank += file_metric.lines_blank
            
            ext = os.path.splitext(file_path)[1].lower()
            if not ext and 'Dockerfile' in file_path:
                self.files_by_type['docker'] += 1
            else:
                for file_type, extensions in CODE_FILE_EXTENSIONS.items():
                    if ext in extensions:
                        self.files_by_type[file_type] += 1
                        break
                else:
                    self.files_by_type['other'] += 1
            
            # Track highest complexity file
            if file_metric.complexity > self.highest_complexity:
                self.highest_complexity = file_metric.complexity
                self.highest_complexity_file = file_path
        
        # Add subdirectory metrics
        for subdir_name, subdir_metric in self.subdirectories.items():
            subdir_metric.aggregate_metrics()
            self.file_count += subdir_metric.file_count
            self.total_size_bytes += subdir_metric.total_size_bytes
            self.total_lines_code += subdir_metric.total_lines_code
            self.total_lines_comment += subdir_metric.total_lines_comment
            self.total_lines_blank += subdir_metric.total_lines_blank
            
            for file_type, count in subdir_metric.files_by_type.items():
                self.files_by_type[file_type] += count
            
            # Update highest complexity if subdir has higher
            if subdir_metric.highest_complexity > self.highest_complexity:
                self.highest_complexity = subdir_metric.highest_complexity
                self.highest_complexity_file = subdir_metric.highest_complexity_file
        
        # Calculate average complexity
        total_complexity = 0
        file_count = len(self.file_metrics)
        for file_metric in self.file_metrics.values():
            total_complexity += file_metric.complexity
        
        for subdir_metric in self.subdirectories.values():
            # Weighted average based on file count
            if subdir_metric.file_count > 0:
                total_complexity += subdir_metric.average_complexity * subdir_metric.file_count
                file_count += subdir_metric.file_count
        
        self.average_complexity = total_complexity / file_count if file_count > 0 else 0
        
        # Estimate Linux compatibility based on Linux mentions
        linux_mentions_files = sum(1 for m in self.file_metrics.values() if m.has_linux_mentions)
        for subdir_metric in self.subdirectories.values():
            linux_mentions_files += sum(1 for m in subdir_metric.file_metrics.values() if m.has_linux_mentions)
        
        if self.file_count > 0:
            self.linux_compatible_estimate = min(1.0, linux_mentions_files / (self.file_count * 0.1))
        
        # Calculate technical debt score
        self._calculate_technical_debt()
    
    def _calculate_technical_debt(self) -> None:
        """💸 Technical Debt Quantum Analyzer: Measures entropy in the system 💸"""
        # Factors in technical debt:
        # 1. High complexity files
        # 2. TODO/FIXME counts
        # 3. Poor comment ratio
        # 4. Large files
        todo_fixme_count = 0
        high_complexity_files = 0
        poorly_commented_files = 0
        large_files = 0
        
        for file_metric in self.file_metrics.values():
            todo_fixme_count += file_metric.todo_count + file_metric.fixme_count
            
            if file_metric.complexity > 10:
                high_complexity_files += 1
            
            # Low comment ratio (significantly below golden ratio)
            if file_metric.lines_code > 50 and file_metric.lines_comment == 0:
                poorly_commented_files += 1
            
            if file_metric.lines_total > 500:
                large_files += 1
        
        for subdir_metric in self.subdirectories.values():
            for file_metric in subdir_metric.file_metrics.values():
                todo_fixme_count += file_metric.todo_count + file_metric.fixme_count
                
                if file_metric.complexity > 10:
                    high_complexity_files += 1
                
                if file_metric.lines_code > 50 and file_metric.lines_comment == 0:
                    poorly_commented_files += 1
                
                if file_metric.lines_total > 500:
                    large_files += 1
        
        # Calculate the debt score (0-10 scale, higher is worse)
        if self.file_count > 0:
            complexity_factor = min(1.0, high_complexity_files / self.file_count)
            comment_factor = min(1.0, poorly_commented_files / self.file_count)
            size_factor = min(1.0, large_files / self.file_count)
            todo_factor = min(1.0, todo_fixme_count / (self.file_count * 5))  # 5 TODOs per file is max
            
            self.technical_debt_score = (complexity_factor * 3 + comment_factor * 3 + 
                                        size_factor * 2 + todo_factor * 2) * 10 / 10
        else:
            self.technical_debt_score = 0

@dataclass
class CodebaseMetrics:
    """🌠 Quantum Codebase Observer - Measures the unified field theory of your code 🌠"""
    root_path: str
    scan_timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    system_info: Dict[str, str] = field(default_factory=dict)
    root_directory: DirectoryMetrics = None
    test_coverage: float = 0.0
    linux_compatibility_score: float = 0.0
    overall_golden_ratio_score: float = 0.0
    recommendations: List[Dict[str, Any]] = field(default_factory=list)
    
    def __post_init__(self):
        """🚀 Initialize quantum observer state 🚀"""
        self.system_info = {
            "os": platform.platform(),
            "python": platform.python_version(),
            "processor": platform.processor(),
            "machine": platform.machine(),
            "is_linux": platform.system().lower() == "linux",
            "quantum_timestamp": str(datetime.datetime.now().timestamp())  # Quantum timestamp
        }
        self.root_directory = DirectoryMetrics(path=self.root_path)
    
    def scan_codebase(self) -> None:
        """🔭 Quantum Scan: Observe and collapse the codebase superposition 🔭"""
        logger.info(f"🧬 Initiating quantum observation at {self.root_path}...")
        self._scan_directory(self.root_path, self.root_directory)
        self.root_directory.aggregate_metrics()
        
        # Calculate overall golden ratio score
        self._calculate_golden_ratio_score()
        
        # Get test coverage if available
        self._get_test_coverage()
        
        # Set Linux compatibility score from root directory
        self.linux_compatibility_score = self.root_directory.linux_compatible_estimate
        
        # Generate recommendations based on metrics
        self._generate_recommendations()
        
        logger.info("✨ Quantum observation complete. Wavefunction collapsed.")
    
    def _scan_directory(self, path: str, dir_metrics: DirectoryMetrics) -> None:
        """🔍 Quantum Directory Scanner: Observes folder probability distributions 🔍"""
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                
                # Skip ignored directories
                if os.path.isdir(item_path) and item in IGNORED_DIRS:
                    continue
                
                if os.path.isfile(item_path):
                    file_metrics = self._scan_file(item_path)
                    if file_metrics:
                        dir_metrics.file_metrics[item_path] = file_metrics
                
                elif os.path.isdir(item_path):
                    subdir_metrics = DirectoryMetrics(path=item_path)
                    dir_metrics.subdirectories[item] = subdir_metrics
                    self._scan_directory(item_path, subdir_metrics)
        
        except PermissionError:
            logger.warning(f"Permission denied for directory: {path}")
        except Exception as e:
            logger.error(f"Error scanning directory {path}: {str(e)}")
    
    def _scan_file(self, file_path: str) -> Optional[FileMetrics]:
        """📝 Quantum File Scanner: Measures individual file states 📝"""
        try:
            # Check if it's a text file we can analyze
            if _is_binary_file(file_path):
                return None
            
            # Get basic file info
            file_size = os.path.getsize(file_path)
            metrics = FileMetrics(path=file_path, size_bytes=file_size)
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Calculate metrics from content
            metrics.calculate_metrics_from_content(content)
            
            return metrics
            
        except UnicodeDecodeError:
            # Binary file or non-utf8 encoding
            return None
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            return None
    
    def _calculate_golden_ratio_score(self) -> None:
        """📐 Golden Ratio Quantum Harmonic: Calculates resonance with divine proportion 📐"""
        total_code_lines = self.root_directory.total_lines_code
        total_comment_lines = self.root_directory.total_lines_comment
        
        if total_comment_lines > 0:
            actual_ratio = total_code_lines / total_comment_lines
            # Calculate distance from golden ratio (closer to 0 is better)
            self.overall_golden_ratio_score = abs(actual_ratio - GOLDEN_RATIO)
        else:
            # No comments at all is bad
            self.overall_golden_ratio_score = float('inf')
    
    def _get_test_coverage(self) -> None:
        """🧪 Test Coverage Quantum Analyzer: Measures test certainty principle 🧪"""
        coverage_paths = [
            os.path.join(self.root_path, 'coverage.json'),
            os.path.join(self.root_path, '.coverage'),
            os.path.join(self.root_path, 'coverage/coverage-final.json')
        ]
        
        for path in coverage_paths:
            if os.path.exists(path):
                if path.endswith('.json'):
                    try:
                        with open(path, 'r') as f:
                            coverage_data = json.load(f)
                            if 'total_coverage' in coverage_data:
                                self.test_coverage = coverage_data['total_coverage']
                                break
                            elif 'totals' in coverage_data:
                                self.test_coverage = coverage_data['totals'].get('percent_covered', 0)
                                break
                    except Exception:
                        pass
                else:
                    # Try to use coverage report command if it's a .coverage file
                    try:
                        result = subprocess.run(
                            ["coverage", "report"],
                            capture_output=True, text=True, check=False
                        )
                        output = result.stdout
                        if "TOTAL" in output:
                            total_line = output.strip().split("\n")[-1]
                            coverage_value = re.search(r'(\d+)%', total_line)
                            if coverage_value:
                                self.test_coverage = float(coverage_value.group(1))
                                break
                    except Exception:
                        pass
        
        # If we couldn't find coverage data, check if pytest-cov is available
        if self.test_coverage == 0 and _command_exists("pytest"):
            try:
                logger.info("No coverage data found. Trying to run pytest with coverage...")
                result = subprocess.run(
                    ["pytest", "--cov=.", "--cov-report=term-missing"],
                    cwd=self.root_path,
                    capture_output=True, text=True, check=False
                )
                output = result.stdout
                if "TOTAL" in output:
                    total_line = output.strip().split("\n")[-1]
                    coverage_value = re.search(r'(\d+)%', total_line)
                    if coverage_value:
                        self.test_coverage = float(coverage_value.group(1))
            except Exception:
                pass
    
    def _generate_recommendations(self) -> None:
        """💡 Quantum Recommendation Generator: Creates superpositions of potential improvements 💡"""
        self.recommendations = []
        
        # Test coverage recommendations
        if self.test_coverage < THRESHOLDS["test_coverage_min"]:
            self.recommendations.append({
                "category": "test_coverage",
                "severity": "high" if self.test_coverage < 50 else "medium",
                "title": f"⚛️ Improve test coverage from {self.test_coverage:.2f}% to {THRESHOLDS['test_coverage_min']}%",
                "description": "According to the ZION_TRAIN_V2_ROADMAP, test coverage should exceed 75% to achieve quantum certainty.",
                "suggested_actions": [
                    "Focus on writing tests for core trading logic first",
                    "Implement test-driven development for new features",
                    "Add integration tests for critical system flows",
                    "Apply quantum superposition testing for edge cases"
                ]
            })
        
        # Complex file recommendations
        top_complex_files = sorted(
            [(file.path, file.complexity) for directory in [self.root_directory] 
             for file in directory.file_metrics.values()], 
            key=lambda x: x[1], reverse=True
        )[:10]
        
        if top_complex_files and top_complex_files[0][1] > THRESHOLDS["complexity_critical"]:
            self.recommendations.append({
                "category": "code_complexity",
                "severity": "high",
                "title": f"🌀 Reduce quantum complexity in high-entropy files",
                "description": f"Several files exceed the complexity threshold recommended for quantum coherence and maintainability.",
                "suggested_actions": [
                    f"Refactor {os.path.basename(top_complex_files[0][0])} (complexity: {top_complex_files[0][1]}) to reduce entropy",
                    f"Apply modular architecture to break down complex classes into quantum modules",
                    f"Follow the 333 LoC rule from ZION_TRAIN_V2_ROADMAP to maintain quantum harmony",
                    f"Implement quantum factoring of large components"
                ],
                "affected_files": [{"path": path, "complexity": compl} for path, compl in top_complex_files[:5]]
            })
        
        # Linux compatibility recommendations
        if self.linux_compatibility_score < THRESHOLDS["linux_compatibility_target"]:
            self.recommendations.append({
                "category": "linux_compatibility",
                "severity": "high",
                "title": "🐧 Enhance quantum Linux compatibility",
                "description": "The codebase has limited Linux-specific handling which may affect deployment stability across the quantum field.",
                "suggested_actions": [
                    "Add platform detection and specific handling for Linux environments",
                    "Create Linux-specific quantum deployment and management scripts",
                    "Test core functionality on Linux distributions (Ubuntu, Debian, CentOS)",
                    "Implement proper file path handling compatible with Linux (use os.path or pathlib)",
                    "Ensure process management is Linux-compatible with proper signal handling",
                    "Create quantum entanglement between OS-specific code paths"
                ]
            })
        
        # Golden ratio recommendations
        if self.overall_golden_ratio_score > 5.0:
            self.recommendations.append({
                "category": "documentation",
                "severity": "medium",
                "title": "📜 Achieve quantum documentation harmony",
                "description": "Code-to-comment ratio deviates significantly from the golden ratio (1.618), affecting quantum resonance.",
                "suggested_actions": [
                    "Add inline quantum documentation to complex algorithms",
                    "Document public API interfaces with quantum-aware docstrings",
                    "Create architecture documentation for core quantum components",
                    "Follow the 'Divine Flow Principles' from ZION_TRAIN_V2_ROADMAP",
                    "Balance code and comments according to phi (1.618) for maximum quantum coherence"
                ]
            })
        
        # TODO/FIXME recommendations
        todo_count = sum(file.todo_count + file.fixme_count 
                        for directory in [self.root_directory] 
                        for file in directory.file_metrics.values())
        
        if todo_count > 50:
            self.recommendations.append({
                "category": "technical_debt",
                "severity": "medium",
                "title": f"💫 Resolve {todo_count} quantum TODOs and FIXMEs in codebase",
                "description": "Numerous TODO/FIXME comments indicate quantum uncertainty that should be resolved.",
                "suggested_actions": [
                    "Create tickets for critical TODOs and FIXMEs",
                    "Implement missing functionality marked by TODOs",
                    "Plan dedicated quantum debt reduction sprints",
                    "Prioritize TODOs affecting system coherence"
                ]
            })
            
        # Nix/Linux integration recommendations
        if self.system_info.get("is_linux", False):
            self.recommendations.append({
                "category": "linux_integration",
                "severity": "high",
                "title": "🌟 Achieve quantum Linux/Nix integration",
                "description": "Improve system compatibility and deployment on Linux/Nix quantum environments.",
                "suggested_actions": [
                    "Create Nix package definitions for consistent quantum development environments",
                    "Add systemd service files for reliable quantum daemon management",
                    "Implement proper syslog integration for quantum production logging",
                    "Create Linux-specific quantum installation scripts with dependency handling",
                    "Set up automatic quantum service recovery using systemd features",
                    "Use Linux cgroups for quantum resource limitation and management",
                    "Ensure file permissions follow Linux security best practices for quantum systems"
                ]
            })
    
    def generate_report(self) -> Dict[str, Any]:
        """📊 Quantum Report Generator: Materializes metrics into observable data structures 📊"""
        report = {
            "scan_timestamp": self.scan_timestamp,
            "quantum_signature": f"QS-{hash(self.scan_timestamp) % 10000:04d}",
            "system_info": self.system_info,
            "summary": {
                "total_files": self.root_directory.file_count,
                "total_size_mb": round(self.root_directory.total_size_bytes / (1024 * 1024), 2),
                "total_lines_code": self.root_directory.total_lines_code,
                "total_lines_comment": self.root_directory.total_lines_comment,
                "total_lines_blank": self.root_directory.total_lines_blank,
                "files_by_type": dict(self.root_directory.files_by_type),
                "test_coverage": f"{self.test_coverage:.2f}%",
                "linux_compatibility_score": f"{self.linux_compatibility_score:.2f}",
                "overall_golden_ratio_score": f"{self.overall_golden_ratio_score:.4f}",
                "technical_debt_score": f"{self.root_directory.technical_debt_score:.2f}/10",
                "average_complexity": round(self.root_directory.average_complexity, 2),
                "highest_complexity_file": self.root_directory.highest_complexity_file,
                "highest_complexity_score": self.root_directory.highest_complexity,
                "quantum_coherence_score": round((100 - self.root_directory.technical_debt_score * 10) / 100, 2)
            },
            "directory_metrics": self._generate_directory_report(self.root_directory),
            "notable_files": self._get_notable_files(self.root_directory),
            "linux_compatibility": self._generate_linux_compatibility_report(),
            "recommendations": self.recommendations
        }
        return report
    
    def _generate_directory_report(self, dir_metrics: DirectoryMetrics, depth: int = 0, max_depth: int = 2) -> Dict[str, Any]:
        """📂 Directory Report: Maps the quantum topology of the directory structure 📂"""
        if depth > max_depth:
            return {
                "file_count": dir_metrics.file_count,
                "size_kb": round(dir_metrics.total_size_bytes / 1024, 2),
                "lines_of_code": dir_metrics.total_lines_code
            }
        
        result = {
            "path": dir_metrics.path,
            "file_count": dir_metrics.file_count,
            "size_kb": round(dir_metrics.total_size_bytes / 1024, 2),
            "lines_of_code": dir_metrics.total_lines_code,
            "lines_of_comment": dir_metrics.total_lines_comment,
            "technical_debt_score": f"{dir_metrics.technical_debt_score:.2f}/10",
            "average_complexity": round(dir_metrics.average_complexity, 2)
        }
        
        if depth < max_depth and dir_metrics.subdirectories:
            result["subdirectories"] = {}
            for subdir_name, subdir_metric in dir_metrics.subdirectories.items():
                # Only include non-empty directories
                if subdir_metric.file_count > 0:
                    result["subdirectories"][subdir_name] = self._generate_directory_report(
                        subdir_metric, depth + 1, max_depth
                    )
        
        return result
    
    def _get_notable_files(self, dir_metrics: DirectoryMetrics, limit: int = 10) -> Dict[str, List[Dict[str, Any]]]:
        """🌟 Notable Files Quantum Analysis: Identifies files with exceptional properties 🌟"""
        all_files = []
        
        def collect_files(directory):
            for file_path, file_metric in directory.file_metrics.items():
                all_files.append(file_metric)
            
            for subdir in directory.subdirectories.values():
                collect_files(subdir)
        
        collect_files(dir_metrics)
        
        notable = {
            "highest_complexity": sorted(all_files, key=lambda x: x.complexity, reverse=True)[:limit],
            "largest_files": sorted(all_files, key=lambda x: x.size_bytes, reverse=True)[:limit],
            "most_linux_mentions": sorted(all_files, key=lambda x: x.linux_mentions_count, reverse=True)[:limit],
            "most_todo_fixme": sorted(all_files, key=lambda x: x.todo_count + x.fixme_count, reverse=True)[:limit],
            "best_golden_ratio": sorted(all_files, key=lambda x: x.golden_ratio_score)[:limit],
        }
        
        # Convert to serializable format
        for category, files in notable.items():
            notable[category] = [
                {
                    "path": file.path,
                    "size_kb": round(file.size_bytes / 1024, 2),
                    "lines_code": file.lines_code,
                    "lines_comment": file.lines_comment,
                    "complexity": file.complexity,
                    "linux_mentions": file.linux_mentions_count,
                    "todos": file.todo_count,
                    "fixmes": file.fixme_count
                }
                for file in files
            ]
        
        return notable
    
    def _generate_linux_compatibility_report(self) -> Dict[str, Any]:
        """🐧 Linux Quantum Compatibility Report: Measures system entanglement 🐧"""
        linux_files = []
        
        def collect_linux_files(directory):
            for file_path, file_metric in directory.file_metrics.items():
                if file_metric.has_linux_mentions:
                    linux_files.append({
                        "path": file_path,
                        "mentions_count": file_metric.linux_mentions_count
                    })
            
            for subdir in directory.subdirectories.values():
                collect_linux_files(subdir)
        
        collect_linux_files(self.root_directory)
        
        return {
            "compatibility_score": f"{self.linux_compatibility_score:.2f}",
            "files_with_linux_mentions": len(linux_files),
            "total_linux_mentions": sum(f["mentions_count"] for f in linux_files),
            "top_linux_files": sorted(linux_files, key=lambda x: x["mentions_count"], reverse=True)[:10]
        }
    
    def save_to_file(self, filepath: str) -> None:
        """💾 Quantum State Persistence: Save metrics to a classical storage medium 💾"""
        report = self.generate_report()
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        logger.info(f"🔄 Quantum metrics solidified to {filepath}")
    
    def save_to_redis(self, host: str = 'localhost', port: int = 6379, key: str = 'metrics:latest') -> bool:
        """⚡ Quantum Redis Integration: Stream metrics to the quantum memory field ⚡"""
        try:
            import redis
            client = redis.Redis(host=host, port=port)
            report = self.generate_report()
            
            # Convert to JSON string
            report_json = json.dumps(report)
            
            # Save to Redis
            client.set(key, report_json)
            
            # Save a timestamped version too
            quantum_key = f"metrics:quantum:{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            client.set(quantum_key, report_json)
            
            # Add to metrics history list
            client.lpush('metrics:quantum:history', quantum_key)
            client.ltrim('metrics:quantum:history', 0, 99)  # Keep last 100 quantum records
            
            logger.info(f"⚛️ Quantum metrics entangled with Redis at {host}:{port} with key '{key}'")
            return True
            
        except ImportError:
            logger.error("🔍 Redis quantum entanglement package not installed. Run 'pip install redis' to enable Redis integration.")
            return False
        except Exception as e:
            logger.error(f"❌ Failed to save quantum metrics to Redis: {str(e)}")
            return False
    
    def print_summary(self) -> None:
        """📋 Quantum Summary Printer: Materializes metrics into visual patterns 📋"""
        report = self.generate_report()
        summary = report["summary"]
        
        print("\n" + "=" * 80)
        print(f"⚛️ OMEGA QUANTUM CODEBASE METRICS ⚛️ - {self.scan_timestamp}")
        print("=" * 80)
        
        print(f"\n🔭 QUANTUM CODEBASE STATISTICS:")
        print(f"  🧮 Total Files: {summary['total_files']}")
        print(f"  📦 Total Size: {summary['total_size_mb']} MB")
        print(f"  📝 Lines of Code: {summary['total_lines_code']}")
        print(f"  💬 Lines of Comments: {summary['total_lines_comment']}")
        
        print(f"\n📋 QUANTUM FILE TYPES:")
        for file_type, count in summary['files_by_type'].items():
            print(f"  {_get_filetype_emoji(file_type)} {file_type}: {count}")
        
        print(f"\n🧪 QUANTUM QUALITY METRICS:")
        print(f"  🎯 Test Coverage: {summary['test_coverage']}")
        print(f"  💸 Technical Debt Score: {summary['technical_debt_score']}")
        print(f"  🌀 Average Complexity: {summary['average_complexity']}")
        print(f"  📏 Golden Ratio Score: {summary['overall_golden_ratio_score']} (closer to 0 is better)")
        print(f"  ✨ Quantum Coherence: {summary.get('quantum_coherence_score', 0)}")
        
        print(f"\n🐧 LINUX QUANTUM COMPATIBILITY:")
        print(f"  🧩 Compatibility Score: {summary['linux_compatibility_score']}")
        print(f"  📄 Top Linux Related Files:")
        for file_info in report["linux_compatibility"]["top_linux_files"][:5]:
            print(f"    📌 {file_info['path']} ({file_info['mentions_count']} mentions)")
        
        print(f"\n🌟 NOTABLE QUANTUM FILES:")
        print("  🔮 Highest Complexity:")
        for file_info in report["notable_files"]["highest_complexity"][:5]:
            print(f"    ⚠️ {file_info['path']} (complexity: {file_info['complexity']})")
        
        print("\n  📝 Most TODOs/FIXMEs:")
        for file_info in report["notable_files"]["most_todo_fixme"][:5]:
            print(f"    ⏳ {file_info['path']} (todos: {file_info['todos']}, fixmes: {file_info['fixmes']})")
        
        print("\n💡 QUANTUM RECOMMENDATIONS:")
        for i, rec in enumerate(report["recommendations"], 1):
            severity_emoji = "🔴" if rec['severity'] == "high" else "🟠" if rec['severity'] == "medium" else "🟡"
            print(f"  {i}. {severity_emoji} {rec['title']}")
            print(f"     {rec['description']}")
            for j, action in enumerate(rec['suggested_actions'][:3], 1):
                print(f"     ✅ {action}")
            if len(rec['suggested_actions']) > 3:
                print(f"     ✨ ... and {len(rec['suggested_actions']) - 3} more quantum actions")
        
        print("\n" + "=" * 80)
        print("🚀 Run with --output=file.json to save detailed quantum report")
        print("⚡ Run with --redis-save to entangle metrics in Redis quantum memory")
        print("=" * 80 + "\n")

def _get_filetype_emoji(file_type: str) -> str:
    """Return an appropriate quantum emoji for each file type"""
    emoji_map = {
        'python': '🐍',
        'javascript': '⚡',
        'markup': '📄',
        'styles': '🎨',
        'data': '📊',
        'config': '⚙️',
        'shell': '💻',
        'docker': '🐳',
        'other': '📁'
    }
    return emoji_map.get(file_type, '📁')

def _is_binary_file(file_path: str) -> bool:
    """🔍 Quantum Binary Detector: Determines if a file exists in binary superposition 🔍"""
    # Check file extension first
    extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg',
                 '.pdf', '.zip', '.gz', '.tar', '.tgz', '.rar', '.7z',
                 '.exe', '.dll', '.so', '.dylib', '.pyc', '.pyd',
                 '.mp3', '.mp4', '.wav', '.avi', '.mov', '.mkv',
                 '.db', '.sqlite', '.ttf', '.woff']
    
    if any(file_path.lower().endswith(ext) for ext in extensions):
        return True
    
    # Check file content
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if b'\0' in chunk:  # Null bytes indicate binary file
                return True
            
            # Check if it's mostly non-printable characters
            text_chars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7F})
            return bool(chunk.translate(None, text_chars))
    except Exception:
        # If we can't read it, assume it's binary
        return True
    
    return False

def _command_exists(cmd: str) -> bool:
    """🔧 Quantum Command Detector: Checks if a command exists in the system 🔧"""
    try:
        subprocess.run(['which', cmd], capture_output=True, check=False)
        return True
    except Exception:
        return False

def main():
    """🚀 Main Quantum Entry Point: Initiates the codebase observation process 🚀"""
    parser = argparse.ArgumentParser(description='⚛️ Analyze codebase with quantum metrics ⚛️')
    parser.add_argument('--path', default='.', help='Path to the codebase quantum field')
    parser.add_argument('--output', help='Path to save quantum JSON report')
    parser.add_argument('--max-depth', type=int, default=2, help='Maximum quantum directory depth for detailed analysis')
    parser.add_argument('--redis-save', action='store_true', help='Save metrics to Redis quantum store')
    parser.add_argument('--redis-host', default='localhost', help='Redis quantum host')
    parser.add_argument('--redis-port', type=int, default=6379, help='Redis quantum port')
    parser.add_argument('--redis-key', default='metrics:quantum:latest', help='Redis quantum key')
    parser.add_argument('--recommendations-only', action='store_true', help='Show only quantum recommendations')
    args = parser.parse_args()
    
    # Resolve path to absolute
    root_path = os.path.abspath(args.path)
    if not os.path.exists(root_path):
        logger.error(f"❌ Quantum path not found: {root_path}")
        return 1
    
    # Create and run analyzer
    metrics = CodebaseMetrics(root_path=root_path)
    metrics.scan_codebase()
    
    # Save report if requested
    if args.output:
        metrics.save_to_file(args.output)
    
    # Save to Redis if requested
    if args.redis_save:
        if not metrics.save_to_redis(args.redis_host, args.redis_port, args.redis_key):
            logger.warning("⚠️ Failed to entangle quantum metrics with Redis. See log for details.")
    
    # Print summary to stdout
    if args.recommendations_only:
        report = metrics.generate_report()
        print("\n⚛️ QUANTUM RECOMMENDATIONS:")
        for i, rec in enumerate(report["recommendations"], 1):
            severity_emoji = "🔴" if rec['severity'] == "high" else "🟠" if rec['severity'] == "medium" else "🟡"
            print(f"{i}. {severity_emoji} {rec['title']}")
            print(f"   {rec['description']}")
            for action in rec['suggested_actions']:
                print(f"   ✅ {action}")
            print("")
    else:
        metrics.print_summary()
    
    return 0

if __name__ == "__main__":
    print("⚛️✨ OMEGA QUANTUM METRICS ANALYZER INITIALIZING ✨⚛️")
    sys.exit(main())