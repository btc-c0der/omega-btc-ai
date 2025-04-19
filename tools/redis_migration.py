
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
Redis Migration Helper
====================

This script helps track and manage the migration from direct Redis usage and RedisConnectionManager
to the enhanced RedisManager implementation.
"""

import os
import sys
from typing import List, Dict, Set, Optional
import ast
import logging
from dataclasses import dataclass
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class RedisUsage:
    file_path: str
    import_type: str  # 'direct', 'connection_manager', 'redis_manager'
    line_numbers: List[int]
    uses_async: bool = False

class RedisMigrationHelper:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.redis_files: Dict[str, RedisUsage] = {}
        self.migrated_files: Set[str] = set()
        
    def scan_codebase(self) -> None:
        """Scan the codebase for Redis usage patterns."""
        for root, _, files in os.walk(self.project_root):
            if any(exclude in root for exclude in ['.git', '__pycache__', 'venv', 'env']):
                continue
                
            for file in files:
                if not file.endswith('.py'):
                    continue
                    
                file_path = os.path.join(root, file)
                self._analyze_file(file_path)
    
    def _analyze_file(self, file_path: str) -> None:
        """Analyze a single file for Redis usage."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
            tree = ast.parse(content)
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    imports.append(node.lineno)
                    
                    # Check import type
                    if isinstance(node, ast.Import):
                        for name in node.names:
                            if name.name == 'redis':
                                self._record_usage(file_path, 'direct', node.lineno)
                    elif isinstance(node, ast.ImportFrom):
                        module = node.module if node.module else ''
                        if 'redis_connection' in module:
                            self._record_usage(file_path, 'connection_manager', node.lineno)
                        elif 'redis_manager' in module:
                            self._record_usage(file_path, 'redis_manager', node.lineno)
                        elif module == 'redis.asyncio':
                            self._record_usage(file_path, 'direct', node.lineno, uses_async=True)
                            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
    
    def _record_usage(self, file_path: str, import_type: str, line_number: int, uses_async: bool = False) -> None:
        """Record Redis usage in a file."""
        rel_path = os.path.relpath(file_path, self.project_root)
        
        if rel_path not in self.redis_files:
            self.redis_files[rel_path] = RedisUsage(
                file_path=rel_path,
                import_type=import_type,
                line_numbers=[line_number],
                uses_async=uses_async
            )
        else:
            self.redis_files[rel_path].line_numbers.append(line_number)
            if uses_async:
                self.redis_files[rel_path].uses_async = True
    
    def generate_migration_report(self) -> str:
        """Generate a detailed migration report."""
        report = ["Redis Migration Report", "===================\n"]
        
        # Group by import type
        direct_redis = []
        connection_manager = []
        redis_manager = []
        async_redis = []
        
        for file_info in self.redis_files.values():
            if file_info.uses_async:
                async_redis.append(file_info)
            elif file_info.import_type == 'direct':
                direct_redis.append(file_info)
            elif file_info.import_type == 'connection_manager':
                connection_manager.append(file_info)
            else:
                redis_manager.append(file_info)
        
        report.extend([
            "Files using direct Redis imports:",
            "-----------------------------",
            *[f"- {f.file_path} (lines: {', '.join(map(str, f.line_numbers))})" for f in direct_redis],
            "\nFiles using RedisConnectionManager:",
            "--------------------------------",
            *[f"- {f.file_path} (lines: {', '.join(map(str, f.line_numbers))})" for f in connection_manager],
            "\nFiles using RedisManager:",
            "----------------------",
            *[f"- {f.file_path} (lines: {', '.join(map(str, f.line_numbers))})" for f in redis_manager],
            "\nFiles using Async Redis:",
            "---------------------",
            *[f"- {f.file_path} (lines: {', '.join(map(str, f.line_numbers))})" for f in async_redis],
            "\nMigration Progress:",
            "-----------------",
            f"Total files to migrate: {len(direct_redis) + len(connection_manager)}",
            f"Files already using RedisManager: {len(redis_manager)}",
            f"Files requiring async support: {len(async_redis)}",
            f"Files migrated: {len(self.migrated_files)}",
            f"Remaining: {len(direct_redis) + len(connection_manager) - len(self.migrated_files)}"
        ])
        
        return "\n".join(report)
    
    def mark_as_migrated(self, file_path: str) -> None:
        """Mark a file as successfully migrated."""
        self.migrated_files.add(file_path)
    
    def suggest_next_file(self) -> str:
        """Suggest the next file to migrate based on complexity and dependencies."""
        # Prioritize files with fewer Redis usages first
        candidates = [
            f for f in self.redis_files.values()
            if f.file_path not in self.migrated_files
            and not f.uses_async  # Skip async files for now
            and f.import_type != 'redis_manager'  # Skip already migrated
        ]
        
        if not candidates:
            return "No more files to migrate!"
            
        # Sort by number of Redis usages (fewer first)
        candidates.sort(key=lambda x: len(x.line_numbers))
        return candidates[0].file_path

if __name__ == "__main__":
    # Get project root from command line or use current directory
    project_root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    
    helper = RedisMigrationHelper(project_root)
    helper.scan_codebase()
    print(helper.generate_migration_report()) 