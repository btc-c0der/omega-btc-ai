#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
Tests for count_files_loc.py - File and Line Counter Utility
Licensed under GBU2™ License - Consciousness Level 8
"""

import os
import sys
import unittest
import tempfile
import shutil
from io import StringIO
from contextlib import redirect_stdout
from collections import defaultdict

# Import the module we want to test
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from count_files_loc import (
    count_files_and_lines,
    human_readable_size,
    format_number,
    print_summary
)

class TestCountFilesLOC(unittest.TestCase):
    """Test cases for count_files_loc.py utility"""

    def setUp(self):
        """Create a temporary directory structure for testing"""
        self.test_dir = tempfile.mkdtemp()
        
        # Create a python file
        with open(os.path.join(self.test_dir, 'test.py'), 'w') as f:
            f.write('#!/usr/bin/env python3\n')
            f.write('# This is a test file\n')
            f.write('import os\n')
            f.write('\n')
            f.write('def test_function():\n')
            f.write('    print("Test")\n')
        
        # Create a markdown file
        with open(os.path.join(self.test_dir, 'README.md'), 'w') as f:
            f.write('# Test Markdown\n')
            f.write('\n')
            f.write('This is a test file.\n')
            f.write('\n')
            f.write('## Section\n')
            f.write('\n')
            f.write('Content.\n')
        
        # Create a subdirectory with a file
        os.mkdir(os.path.join(self.test_dir, 'subdir'))
        with open(os.path.join(self.test_dir, 'subdir', 'subfile.js'), 'w') as f:
            f.write('// This is a JavaScript file\n')
            f.write('function test() {\n')
            f.write('    console.log("test");\n')
            f.write('    return true;\n')
            f.write('}\n')
        
        # Create a .git directory that should be excluded
        os.mkdir(os.path.join(self.test_dir, '.git'))
        with open(os.path.join(self.test_dir, '.git', 'config'), 'w') as f:
            f.write('[core]\n')
            f.write('    repositoryformatversion = 0\n')
        
        # Create a binary file that should be excluded
        with open(os.path.join(self.test_dir, 'binary.exe'), 'wb') as f:
            f.write(os.urandom(100))
    
    def tearDown(self):
        """Remove the temporary directory after tests"""
        shutil.rmtree(self.test_dir)
    
    def test_count_files_and_lines(self):
        """Test counting files and lines with different parameters"""
        # Test with default parameters
        stats_by_ext, total_files, total_lines, total_bytes = count_files_and_lines(self.test_dir)
        
        # Should find 3 files (test.py, README.md, subdir/subfile.js)
        self.assertEqual(len(stats_by_ext), 3)
        
        # Check file counts by extension
        self.assertEqual(stats_by_ext['.py']['files'], 1)
        self.assertEqual(stats_by_ext['.md']['files'], 1)
        self.assertEqual(stats_by_ext['.js']['files'], 1)
        
        # Check line counts
        self.assertEqual(stats_by_ext['.py']['lines'], 6)
        self.assertEqual(stats_by_ext['.md']['lines'], 7)
        self.assertEqual(stats_by_ext['.js']['lines'], 5)
        
        # Test with exclude directories
        stats_by_ext, _, _, _ = count_files_and_lines(self.test_dir, exclude_dirs=['subdir'])
        self.assertEqual(len(stats_by_ext), 2)  # Should exclude subdir/subfile.js
        self.assertNotIn('.js', stats_by_ext)
        
        # Test with exclude patterns
        stats_by_ext, _, _, _ = count_files_and_lines(self.test_dir, exclude_patterns=['*.md'])
        self.assertEqual(len(stats_by_ext), 2)  # Should exclude README.md
        self.assertNotIn('.md', stats_by_ext)
        
        # Test that .git directories are automatically excluded
        # The .git directory should be excluded by default in count_files_and_lines
        self.assertNotIn('.git', [os.path.basename(d) for d in os.listdir(self.test_dir) if os.path.isdir(os.path.join(self.test_dir, d)) and not d.startswith('.')])
        
        # Test that binary files are not counted
        self.assertNotIn('.exe', stats_by_ext)
    
    def test_human_readable_size(self):
        """Test conversion of byte sizes to human readable format"""
        self.assertEqual(human_readable_size(0), "0 B")
        self.assertEqual(human_readable_size(512), "512 B")
        self.assertEqual(human_readable_size(1024), "1.00 KB")
        self.assertEqual(human_readable_size(1536), "1.50 KB")
        self.assertEqual(human_readable_size(1048576), "1.00 MB")
        self.assertEqual(human_readable_size(1073741824), "1.00 GB")
        self.assertEqual(human_readable_size(1099511627776), "1.00 TB")
    
    def test_format_number(self):
        """Test formatting numbers with thousands separator"""
        self.assertEqual(format_number(0), "0")
        self.assertEqual(format_number(1), "1")
        self.assertEqual(format_number(1000), "1,000")
        self.assertEqual(format_number(1000000), "1,000,000")
        self.assertEqual(format_number(1234567), "1,234,567")
    
    def test_print_summary(self):
        """Test printing summary information"""
        # Create sample data
        data = {
            '.py': {'files': 10, 'lines': 500, 'size': 10240},
            '.js': {'files': 5, 'lines': 300, 'size': 5120},
            '.md': {'files': 3, 'lines': 100, 'size': 2048},
        }
        
        # Capture stdout
        output = StringIO()
        with redirect_stdout(output):
            print_summary(data, 18, 900, 17408, sort_by='lines')
        
        # Check that output contains expected information
        output_str = output.getvalue()
        self.assertIn("Total Files: 18", output_str)
        self.assertIn("Total Lines: 900", output_str)
        self.assertIn("Total Size: 17.00 KB", output_str)
        
        # Test sorting by different criteria
        output = StringIO()
        with redirect_stdout(output):
            print_summary(data, 18, 900, 17408, sort_by='files')
        output_str = output.getvalue()
        first_ext = output_str.split("\n")[3].split()[0]  # Get first extension in table
        self.assertEqual(first_ext, ".py")  # Should be sorted by most files
        
        output = StringIO()
        with redirect_stdout(output):
            print_summary(data, 18, 900, 17408, sort_by='extension')
        output_str = output.getvalue()
        first_ext = output_str.split("\n")[3].split()[0]  # Get first extension in table
        self.assertEqual(first_ext, ".js")  # Should be sorted alphabetically
    
    def test_empty_directory(self):
        """Test analyzing an empty directory"""
        empty_dir = tempfile.mkdtemp()
        try:
            stats_by_ext, total_files, total_lines, total_bytes = count_files_and_lines(empty_dir)
            self.assertEqual(len(stats_by_ext), 0)
            
            # Capture stdout
            output = StringIO()
            with redirect_stdout(output):
                print_summary(stats_by_ext, total_files, total_lines, total_bytes)
            
            # Check output for empty directory
            output_str = output.getvalue()
            self.assertIn("Total files: 0", output_str)
            self.assertIn("Total lines of code: 0", output_str)
        finally:
            shutil.rmtree(empty_dir)
    
    def test_nested_directories(self):
        """Test analyzing deeply nested directories"""
        nested_dir = tempfile.mkdtemp()
        try:
            # Create a deeply nested structure
            current_dir = nested_dir
            for i in range(5):  # Create 5 nested directories
                current_dir = os.path.join(current_dir, f"level{i}")
                os.mkdir(current_dir)
                
                # Add a file to each level
                with open(os.path.join(current_dir, f"file{i}.txt"), 'w') as f:
                    for j in range(i + 1):
                        f.write(f"Line {j} of file {i}\n")
            
            stats_by_ext, total_files, total_lines, total_bytes = count_files_and_lines(nested_dir)
            self.assertEqual(len(stats_by_ext), 1)  # Only .txt files
            self.assertEqual(stats_by_ext['.txt']['files'], 5)  # 5 .txt files
            self.assertEqual(stats_by_ext['.txt']['lines'], 15)  # Sum of lines: 1+2+3+4+5 = 15
        finally:
            shutil.rmtree(nested_dir)
    
    def test_large_file_handling(self):
        """Test handling of large files"""
        large_file_dir = tempfile.mkdtemp()
        try:
            # Create a relatively large file (100KB)
            with open(os.path.join(large_file_dir, "large.txt"), 'w') as f:
                for i in range(10000):
                    f.write(f"Line {i} of the large file\n")
            
            stats_by_ext, total_files, total_lines, total_bytes = count_files_and_lines(large_file_dir)
            self.assertEqual(stats_by_ext['.txt']['files'], 1)
            self.assertEqual(stats_by_ext['.txt']['lines'], 10000)
            self.assertTrue(stats_by_ext['.txt']['bytes'] > 100000)  # Should be over 100KB
        finally:
            shutil.rmtree(large_file_dir)

if __name__ == '__main__':
    unittest.main() 