#!/usr/bin/env python3

"""
OMEGA BTC AI - README Scanner

This script scans the repository for README files and displays information about each one.
"""

import os
import re
import datetime
from pathlib import Path

EXCLUDE_DIRS = [
    "node_modules",
    "venv",
    "__pycache__",
    ".git",
    ".pytest_cache",
    "omega_ai.egg-info"
]

def get_readme_files(base_path="."):
    """Find all README files in the repository."""
    readme_files = []
    
    for root, dirs, files in os.walk(base_path):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            if re.match(r"README.*\.md", file, re.IGNORECASE):
                readme_path = os.path.join(root, file)
                # Get relative path for cleaner output
                rel_path = os.path.relpath(readme_path, base_path)
                readme_files.append(rel_path)
    
    return sorted(readme_files)

def count_lines(file_path):
    """Count the number of lines in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except Exception as e:
        return f"Error: {str(e)}"

def get_title(file_path):
    """Extract the title (first heading) from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Look for markdown headings (# Title)
                match = re.match(r'^#+\s+(.+)$', line.strip())
                if match:
                    return match.group(1)
    except Exception:
        pass
    
    # If no title found, use the filename
    return os.path.basename(file_path)

def get_summary(file_path, max_lines=10):
    """Get a summary of the file content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            # Skip empty lines at the beginning
            start_idx = 0
            while start_idx < len(lines) and not lines[start_idx].strip():
                start_idx += 1
            
            # Get the first few non-empty lines
            summary_lines = []
            line_count = 0
            
            for i in range(start_idx, len(lines)):
                if lines[i].strip() and not lines[i].startswith('#'):
                    summary_lines.append(lines[i].strip())
                    line_count += 1
                    if line_count >= max_lines:
                        break
            
            summary = ' '.join(summary_lines)
            # Truncate if too long
            if len(summary) > 200:
                summary = summary[:197] + '...'
            
            return summary
    except Exception as e:
        return f"Error: {str(e)}"

def export_to_markdown(readme_files, output_file="README_SUMMARY.md"):
    """Export README summaries to a markdown file."""
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# OMEGA BTC AI - README Summaries\n\n")
        f.write(f"Generated on: {date_str}\n\n")
        f.write(f"This document provides a summary of all README files in the OMEGA BTC AI project.\n\n")
        
        f.write("## Table of Contents\n\n")
        for i, readme in enumerate(readme_files):
            title = get_title(readme)
            f.write(f"{i+1}. [{title}](#{readme.replace('/', '-').replace('.', '-').replace(' ', '-').lower()})\n")
        
        f.write("\n## Summaries\n\n")
        
        for readme in readme_files:
            anchor = readme.replace('/', '-').replace('.', '-').replace(' ', '-').lower()
            title = get_title(readme)
            lines = count_lines(readme)
            summary = get_summary(readme)
            
            f.write(f"### {title}\n\n")
            f.write(f"**File:** `{readme}`  \n")
            f.write(f"**Lines:** {lines}  \n\n")
            f.write(f"**Summary:**  \n{summary}\n\n")
            f.write("---\n\n")
            
    print(f"\nSummary exported to {output_file}")
    return output_file

def main():
    """Main function to scan and display README files."""
    print("\nOMEGA BTC AI - README Scanner\n")
    
    # Get all README files
    readme_files = get_readme_files()
    
    if not readme_files:
        print("No README files found!")
        return
    
    print(f"Found {len(readme_files)} README files:\n")
    
    # Print a summary table
    print(f"{'Path':<50} {'Lines':<10} {'Title':<30}")
    print(f"{'-' * 50} {'-' * 10} {'-' * 30}")
    
    for readme in readme_files:
        lines = count_lines(readme)
        title = get_title(readme)
        print(f"{readme:<50} {lines:<10} {title[:30]}")
    
    # Export summaries to markdown file
    output_file = export_to_markdown(readme_files)
    
    print("\nREADME Summaries:")
    print(f"{'-' * 80}")
    
    # Print a summary of each README
    for readme in readme_files:
        print(f"\nFILE: {readme}")
        print(f"TITLE: {get_title(readme)}")
        print(f"LINES: {count_lines(readme)}")
        print(f"SUMMARY: {get_summary(readme)}")
        print(f"{'-' * 80}")

if __name__ == "__main__":
    main() 