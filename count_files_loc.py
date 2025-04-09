#!/usr/bin/env python3
"""
File and Line Counter - Summarizes files and lines of code by extension
"""

import os
import sys
from collections import defaultdict
import argparse
from datetime import datetime
from pathlib import Path

def format_number(num):
    """Format number with thousands separator"""
    return f"{num:,}"

def count_files_and_lines(root_dir, exclude_dirs=None, exclude_patterns=None):
    """
    Count files and lines by extension in the given directory
    
    Args:
        root_dir (str): Root directory to start search
        exclude_dirs (list): List of directory names to exclude
        exclude_patterns (list): List of file patterns to exclude
    
    Returns:
        tuple: (stats_by_ext, total_files, total_lines)
    """
    if exclude_dirs is None:
        exclude_dirs = ['.git', 'node_modules', '__pycache__', 'venv', '.venv', '.idea', '.vscode']
    
    if exclude_patterns is None:
        exclude_patterns = ['.DS_Store', '.gitignore', '*.pyc', '*.pyo', '*.pyd', '*.so', '*.dll', 
                           '*.exe', '*.obj', '*.o', '*.a', '*.lib', '*.egg', '*.egg-info']
    
    stats_by_ext = defaultdict(lambda: {'files': 0, 'lines': 0, 'bytes': 0})
    total_files = 0
    total_lines = 0
    total_bytes = 0
    
    print(f"Scanning directory: {root_dir}")
    print("This may take a moment for large repositories...\n")
    
    # Convert root_dir to absolute path
    root_dir = os.path.abspath(root_dir)
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip excluded directories
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        
        for filename in filenames:
            # Skip excluded patterns
            if any(Path(filename).match(pattern) for pattern in exclude_patterns):
                continue
            
            filepath = os.path.join(dirpath, filename)
            
            # Get file extension (default to "no_ext" if no extension)
            _, ext = os.path.splitext(filename)
            ext = ext.lower() if ext else "no_ext"
            
            # Skip binary files except common text-based formats
            if ext not in ['.py', '.sh', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.scss', 
                          '.md', '.txt', '.json', '.yml', '.yaml', '.toml', '.ini', '.cfg', 
                          '.c', '.cpp', '.h', '.hpp', '.java', '.go', '.rs', '.rb', '.php',
                          '.ipynb', '.svg', '.xml', '.csv', '.r', '.sql', '.m', '.swift',
                          '.dart', '.vue', '.gradle', '.tf', '.groovy', '.lua', '.pl', '.ps1',
                          '.bat', '.cmd', '.asm', '.s', '.kt', '.kts', '.clj', '.scala']:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        f.read(1024)  # Try to read a bit to see if it's text
                except UnicodeDecodeError:
                    # Skip binary files
                    continue
                except Exception:
                    # Skip files that can't be read
                    continue
            
            try:
                # Count lines and file size
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = sum(1 for _ in f)
                    
                file_size = os.path.getsize(filepath)
                
                # Update statistics
                stats_by_ext[ext]['files'] += 1
                stats_by_ext[ext]['lines'] += lines
                stats_by_ext[ext]['bytes'] += file_size
                
                total_files += 1
                total_lines += lines
                total_bytes += file_size
                
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
    
    return stats_by_ext, total_files, total_lines, total_bytes

def human_readable_size(size_bytes):
    """Convert size in bytes to human readable format"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    
    units = ['KB', 'MB', 'GB', 'TB']
    size = size_bytes / 1024
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    return f"{size:.2f} {units[unit_index]}"

def print_summary(stats_by_ext, total_files, total_lines, total_bytes, sort_by='lines'):
    """Print summary of files and lines by extension"""
    print(f"\n{'=' * 80}")
    print(f"CODE REPOSITORY ANALYSIS")
    print(f"{'=' * 80}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total files: {format_number(total_files)}")
    print(f"Total lines of code: {format_number(total_lines)}")
    print(f"Total size: {human_readable_size(total_bytes)}")
    print(f"{'=' * 80}")
    
    # Sort extensions by the specified criteria
    if sort_by == 'lines':
        sorted_exts = sorted(stats_by_ext.items(), key=lambda x: x[1]['lines'], reverse=True)
    elif sort_by == 'files':
        sorted_exts = sorted(stats_by_ext.items(), key=lambda x: x[1]['files'], reverse=True)
    elif sort_by == 'extension':
        sorted_exts = sorted(stats_by_ext.items(), key=lambda x: x[0])
    else:  # Default to lines
        sorted_exts = sorted(stats_by_ext.items(), key=lambda x: x[1]['lines'], reverse=True)
    
    # Print table header
    print(f"{'Extension':<15} {'Files':<10} {'Lines':<12} {'Size':<10} {'Avg Lines/File':<15}")
    print(f"{'-' * 15} {'-' * 10} {'-' * 12} {'-' * 10} {'-' * 15}")
    
    # Print statistics for each extension
    for ext, stats in sorted_exts:
        avg_lines = stats['lines'] / stats['files'] if stats['files'] > 0 else 0
        print(f"{ext:<15} {format_number(stats['files']):<10} {format_number(stats['lines']):<12} {human_readable_size(stats['bytes']):<10} {avg_lines:.1f}")
    
    print(f"{'=' * 80}")
    print("\nNOTE: Binary files and certain file types may be excluded from line counting")
    print(f"{'=' * 80}")

def main():
    parser = argparse.ArgumentParser(description='Count files and lines of code in a repository')
    parser.add_argument('--dir', type=str, default='.', help='Root directory to analyze')
    parser.add_argument('--sort', type=str, default='lines', choices=['lines', 'files', 'extension'], 
                        help='Sort results by lines, files, or extension')
    
    args = parser.parse_args()
    
    # Get absolute path of the directory
    root_dir = os.path.abspath(args.dir)
    
    # Count files and lines
    stats_by_ext, total_files, total_lines, total_bytes = count_files_and_lines(root_dir)
    
    # Print summary
    print_summary(stats_by_ext, total_files, total_lines, total_bytes, sort_by=args.sort)

if __name__ == '__main__':
    main() 