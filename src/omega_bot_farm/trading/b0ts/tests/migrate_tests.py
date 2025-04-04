#!/usr/bin/env python3
"""
Test Migration Script for Omega Bot Farm

This script helps migrate test files from the old test directories to the new unified
test directory structure. It copies files to their appropriate locations and adjusts
import paths as needed.
"""

import os
import sys
import shutil
import re
import argparse
from pathlib import Path

# Source directories
SOURCE_DIRS = [
    "/Users/fsiqueira/Desktop/GitHub/omega-btc-ai/src/omega_bot_farm/trading/b0ts/tests",
    "/Users/fsiqueira/Desktop/GitHub/omega-btc-ai/src/omega_bot_farm/trading/b0ts/bitget_analyzer/tests"
]

# Destination directory
DEST_DIR = "/Users/fsiqueira/Desktop/GitHub/omega-btc-ai/src/omega_bot_farm/trading/b0ts/tests_merged"

# Mapping of source directories to target directories
FILE_MAPPING = {
    # BitgetPositionAnalyzerB0t unit tests
    "bitget_analyzer/tests/unit/": "unit/bitget_analyzer/",
    "tests/unit/": "unit/",
    
    # Component tests
    "bitget_analyzer/tests/component/": "component/bitget_analyzer/",
    
    # BDD tests
    "bitget_analyzer/tests/BDD/": "BDD/",
    
    # Integration tests
    "bitget_analyzer/tests/integration/": "integration/",
    "tests/integration/": "integration/",
    
    # Performance tests
    "tests/performance/": "performance/",
    
    # End-to-end tests
    "bitget_analyzer/tests/end_to_end/": "end_to_end/",
    
    # Specialized tests
    "bitget_analyzer/tests/i18n/": "specialized/i18n/",
    "bitget_analyzer/tests/security/": "specialized/security/",
    "bitget_analyzer/tests/quantum/": "specialized/quantum/",
    "bitget_analyzer/tests/usability/": "specialized/usability/",
    
    # Handle specific test files in the root directories
    "tests/test_bitget_position_analyzer.py": "unit/bitget_analyzer/",
    "tests/test_cosmic_factor_service.py": "unit/cosmic/",
    "tests/test_strategic_bot_cosmic.py": "unit/cosmic/",
    "tests/test_ccxt_strategic_cosmic.py": "unit/cosmic/",
}

# Import path adjustments
IMPORT_ADJUSTMENTS = [
    (r'from\s+src\.omega_bot_farm\.trading\.b0ts\.bitget_analyzer',
     'from src.omega_bot_farm.trading.b0ts.bitget_analyzer'),
]

def adjust_imports(file_path):
    """Adjust import statements in the file if needed."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for pattern, replacement in IMPORT_ADJUSTMENTS:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            modified = True
    
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Adjusted imports in {file_path}")

def should_copy_file(src_path):
    """Determine if a file should be copied."""
    # Skip __pycache__ and other temporary files
    if '__pycache__' in src_path or '.pyc' in src_path or '.DS_Store' in src_path:
        return False
    
    return True

def get_destination_path(src_path):
    """Determine the destination path for a file based on mapping rules."""
    for src_pattern, dest_subdir in FILE_MAPPING.items():
        if src_pattern in src_path:
            # Handle specific files
            if os.path.isfile(src_path) and src_pattern == src_path:
                dest_file = os.path.join(DEST_DIR, dest_subdir, os.path.basename(src_path))
                return dest_file
            
            # Handle directories
            rel_path = src_path.split(src_pattern)[1]
            dest_path = os.path.join(DEST_DIR, dest_subdir, rel_path)
            return dest_path
    
    # Default: preserve the path relative to the source directory
    for source_dir in SOURCE_DIRS:
        if source_dir in src_path:
            rel_path = src_path.replace(source_dir, "").lstrip("/")
            return os.path.join(DEST_DIR, rel_path)
    
    return None

def copy_files(dry_run=False):
    """Copy files from source directories to destination directory."""
    file_count = 0
    
    for source_dir in SOURCE_DIRS:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                src_path = os.path.join(root, file)
                
                if not should_copy_file(src_path):
                    continue
                
                dest_path = get_destination_path(src_path)
                if not dest_path:
                    print(f"Skipping {src_path} - No mapping rule found")
                    continue
                
                # Create destination directory if it doesn't exist
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                if dry_run:
                    print(f"Would copy {src_path} -> {dest_path}")
                else:
                    # Copy the file
                    shutil.copy2(src_path, dest_path)
                    print(f"Copied {src_path} -> {dest_path}")
                    
                    # Adjust imports if needed
                    if dest_path.endswith('.py'):
                        adjust_imports(dest_path)
                
                file_count += 1
    
    return file_count

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description='Migrate test files to new structure')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    args = parser.parse_args()
    
    if args.dry_run:
        print("*** DRY RUN - No changes will be made ***")
    
    file_count = copy_files(dry_run=args.dry_run)
    
    if args.dry_run:
        print(f"\nWould migrate {file_count} files to the new test structure")
    else:
        print(f"\nSuccessfully migrated {file_count} files to the new test structure")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 