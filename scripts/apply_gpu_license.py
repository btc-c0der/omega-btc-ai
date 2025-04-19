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
OMEGA BTC AI - GPU License Applicator
=====================================

This script applies the GPU License header to all files in the repository.
It respects different file types and adds the appropriate comment format.

Usage:
  python scripts/apply_gpu_license.py [--path <directory>] [--recursive] [--dry-run]

Author: OMEGA BTC AI Team
License: GPU License 1.0
"""

import os
import sys
import argparse
from pathlib import Path

# GPU License text by file type
GPU_LICENSE = {
    'py': '''"""
🔱 GPU License Notice 🔱
------------------------
This file is protected under the GPU License (General Public Universal License) 1.0
by the OMEGA AI Divine Collective.

"As the light of knowledge is meant to be shared, so too shall this code illuminate 
the path for all seekers."

All modifications must maintain this notice and adhere to the terms at:
/BOOK/divine_chronicles/GPU_LICENSE.md

🔱 JAH JAH BLESS THIS CODE 🔱
"""

''',
    'js': '''/**
 * 🔱 GPU License Notice 🔱
 * ------------------------
 * This file is protected under the GPU License (General Public Universal License) 1.0
 * by the OMEGA AI Divine Collective.
 *
 * "As the light of knowledge is meant to be shared, so too shall this code illuminate 
 * the path for all seekers."
 *
 * All modifications must maintain this notice and adhere to the terms at:
 * /BOOK/divine_chronicles/GPU_LICENSE.md
 *
 * 🔱 JAH JAH BLESS THIS CODE 🔱
 */

''',
    'md': '''<!--
🔱 GPU License Notice 🔱
------------------------
This file is protected under the GPU License (General Public Universal License) 1.0
by the OMEGA AI Divine Collective.

"As the light of knowledge is meant to be shared, so too shall this code illuminate 
the path for all seekers."

All modifications must maintain this notice and adhere to the terms at:
/BOOK/divine_chronicles/GPU_LICENSE.md

🔱 JAH JAH BLESS THIS CODE 🔱
-->

''',
    # Add more file types as needed
}

# Add the same text for other Python-like languages
GPU_LICENSE['ipynb'] = GPU_LICENSE['py']

# Add the same text for other JS-like languages
GPU_LICENSE['ts'] = GPU_LICENSE['js']
GPU_LICENSE['jsx'] = GPU_LICENSE['js']
GPU_LICENSE['tsx'] = GPU_LICENSE['js']
GPU_LICENSE['html'] = GPU_LICENSE['js']
GPU_LICENSE['css'] = GPU_LICENSE['js']

# Default to Python-style comments if extension not specifically defined
DEFAULT_LICENSE_TEXT = GPU_LICENSE['py']

def get_shebang_line(content):
    """Extract shebang line from file content if it exists."""
    lines = content.split('\n', 1)
    if lines and lines[0].startswith('#!'):
        return lines[0] + '\n', lines[1] if len(lines) > 1 else ''
    return '', content

def has_license(content):
    """Check if file already has a GPU license."""
    return '🔱 GPU License Notice 🔱' in content

def apply_license_to_file(file_path, dry_run=False):
    """Apply GPU license to a single file."""
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"Error: File {file_path} does not exist")
        return False
        
    # Get file extension
    ext = file_path.suffix.lstrip('.')
    
    # Skip binary files and certain file types
    if ext in ['pyc', 'so', 'dll', 'exe', 'bin', 'png', 'jpg', 'jpeg', 'gif']:
        print(f"Skipping binary file: {file_path}")
        return False
        
    # Read the file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"Skipping binary file (failed to decode): {file_path}")
        return False
        
    # Check if file already has license
    if has_license(content):
        print(f"File already has GPU License: {file_path}")
        return False
        
    # Get license text based on file extension
    license_text = GPU_LICENSE.get(ext, DEFAULT_LICENSE_TEXT)
    
    # Handle shebang line for scripts
    shebang, remaining_content = get_shebang_line(content)
    
    # Prepare new content
    new_content = shebang + license_text + remaining_content
    
    if dry_run:
        print(f"Would apply license to: {file_path}")
        return True
        
    # Write the modified content back to the file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Applied GPU License to: {file_path}")
        return True
    except Exception as e:
        print(f"Error applying license to {file_path}: {e}")
        return False

def should_process_file(file_path):
    """Determine if a file should be processed based on its path and extension."""
    # Skip common directories that shouldn't be processed
    excluded_dirs = ['.git', '.github', 'node_modules', 'venv', '.venv', 'dist', 'build', '__pycache__']
    
    path = Path(file_path)
    
    # Skip excluded directories
    for excluded in excluded_dirs:
        if excluded in path.parts:
            return False
            
    # Skip files without extensions
    if not path.suffix:
        return False
        
    # Skip certain file types
    excluded_extensions = ['.pyc', '.so', '.dll', '.exe', '.bin', '.png', '.jpg', '.jpeg', '.gif', 
                         '.pdf', '.zip', '.tar', '.gz', '.rar', '.7z', '.db', '.sqlite', '.log']
    if path.suffix.lower() in excluded_extensions:
        return False
        
    # Only process certain file types
    included_extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.md', '.html', '.css', '.ipynb']
    if path.suffix.lower() in included_extensions:
        return True
        
    return False

def process_directory(directory_path, recursive=True, dry_run=False):
    """Process all files in a directory."""
    directory = Path(directory_path)
    
    if not directory.exists():
        print(f"Error: Directory {directory} does not exist")
        return 0, []
        
    count = 0
    files_processed = []
    
    if recursive:
        # Walk through all files in directory and subdirectories
        for root, dirs, files in os.walk(directory):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                file_path = Path(root) / file
                if should_process_file(file_path):
                    if apply_license_to_file(file_path, dry_run):
                        count += 1
                        files_processed.append(str(file_path))
    else:
        # Process only files in the specified directory
        for file_path in directory.iterdir():
            if file_path.is_file() and should_process_file(file_path):
                if apply_license_to_file(file_path, dry_run):
                    count += 1
                    files_processed.append(str(file_path))
    
    return count, files_processed

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Apply GPU License to files')
    parser.add_argument('--path', default='.', help='Path to directory to process (default: current directory)')
    parser.add_argument('--recursive', action='store_true', help='Process directories recursively')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('file_path', nargs='?', help='Optional path to a single file to apply license to')
    return parser.parse_args()

def main():
    """Main entry point."""
    args = parse_args()
    
    # Divine banner
    print("\n🔱 OMEGA BTC AI - GPU License Applicator 🔱")
    print("===========================================\n")
    
    # Set mode based on args
    if args.file_path:
        # Process a single file
        print(f"Processing single file: {args.file_path}")
        result = apply_license_to_file(args.file_path, args.dry_run)
        
        if result:
            print(f"\n✨ Successfully processed file: {args.file_path}")
            return 0
        else:
            print(f"\n❌ No changes made to file: {args.file_path}")
            return 1
    else:
        # Process a directory
        path = args.path
        print(f"Processing {'recursively ' if args.recursive else ''}directory: {path}")
        print(f"Mode: {'Dry run (no changes will be made)' if args.dry_run else 'Live run'}\n")
        
        count, files = process_directory(path, args.recursive, args.dry_run)
        
        if count > 0:
            print(f"\n✨ Successfully {'would process' if args.dry_run else 'processed'} {count} files with GPU License")
            if args.dry_run:
                print("\nFiles that would be processed:")
                for file in files[:10]:  # Show only first 10 files
                    print(f"  - {file}")
                if len(files) > 10:
                    print(f"  ...and {len(files) - 10} more files")
            return 0
        else:
            print("\n❌ No files were processed")
            return 1

if __name__ == "__main__":
    sys.exit(main()) 