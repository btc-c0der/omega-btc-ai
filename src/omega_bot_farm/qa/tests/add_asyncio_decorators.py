#!/usr/bin/env python3
"""
Add pytest.mark.asyncio Decorator to Async Test Functions

This script automatically adds the pytest.mark.asyncio decorator to all async test functions
in the tests directory to fix the PytestUnhandledCoroutineWarning warnings.
"""
import os
import re
import argparse
from pathlib import Path

IMPORT_PATTERN = r"import\s+pytest"
ASYNCIO_IMPORT_PATTERN = r"from\s+pytest\s+import\s+.*\bmark\b"
ASYNC_TEST_PATTERN = r"async\s+def\s+(test_\w+)"
DECORATOR_PATTERN = r"@pytest\.mark\.asyncio"

def add_asyncio_decorator_to_file(file_path):
    """Add pytest.mark.asyncio decorator to all async test functions in a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file contains async test functions
    if not re.search(ASYNC_TEST_PATTERN, content):
        print(f"No async test functions found in {file_path}")
        return False
    
    # Add pytest import if needed
    has_pytest_import = re.search(IMPORT_PATTERN, content) is not None
    has_mark_import = re.search(ASYNCIO_IMPORT_PATTERN, content) is not None
    
    if not has_pytest_import and not has_mark_import:
        # Add import after other imports
        import_match = re.search(r"(import\s+[^\n]+\n+)", content)
        if import_match:
            last_import = import_match.group(1)
            last_import_pos = content.rfind(last_import) + len(last_import)
            content = content[:last_import_pos] + "import pytest\n" + content[last_import_pos:]
    
    # Add decorator to async test functions
    modified_content = ""
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for async def test_ pattern
        async_match = re.search(ASYNC_TEST_PATTERN, line)
        if async_match:
            # Check if decorator already exists by looking at previous line
            has_decorator = i > 0 and re.search(DECORATOR_PATTERN, lines[i-1])
            
            if not has_decorator:
                # Add decorator before the async def
                modified_content += "@pytest.mark.asyncio\n"
            
        modified_content += line + "\n"
        i += 1
    
    # Write back to file if changes were made
    if content != modified_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content.rstrip())
        print(f"Updated {file_path}")
        return True
    
    print(f"No changes needed for {file_path}")
    return False

def find_test_files(directory):
    """Find all Python test files in the directory."""
    test_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                test_files.append(os.path.join(root, file))
    return test_files

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Add pytest.mark.asyncio decorator to async test functions")
    parser.add_argument("--dir", default=".", help="Directory to search for test files")
    args = parser.parse_args()
    
    directory = Path(args.dir).resolve()
    print(f"Searching for test files in {directory}")
    
    test_files = find_test_files(directory)
    print(f"Found {len(test_files)} test files")
    
    updated_files = 0
    for file in test_files:
        if add_asyncio_decorator_to_file(file):
            updated_files += 1
    
    print(f"Updated {updated_files} files")

if __name__ == "__main__":
    main() 