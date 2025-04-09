#!/usr/bin/env python3
"""
OMEGA DEV FRAMEWORK - TDD Oracle
================================

The divine prophet that foresees missing tests before Babylon strikes.
This oracle analyzes your codebase, identifies functions and classes without
proper test coverage, and generates prophetic test templates to guide implementation.

Usage:
    python omega_tdd_oracle.py --scan-path ./omega_ai
    python omega_tdd_oracle.py --apply-recommendations
    python omega_tdd_oracle.py --check-file ./omega_ai/tools/trap_probability_meter.py
"""

import argparse
import ast
import importlib.util
import inspect
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any, Union

# ANSI color codes for terminal styling
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Constants
FIBONACCI_RATIO = 1.618033988749895  # Golden ratio
SCHUMANN_RESONANCE = 7.83  # Earth's base frequency (Hz)


class CodeAnalyzer(ast.NodeVisitor):
    """Divine analyzer that extracts functions and classes from Python code."""
    
    def __init__(self, file_path: str):
        """Initialize the analyzer with cosmic awareness."""
        self.file_path = file_path
        self.functions = []
        self.classes = []
        self.current_class = None
        self.imports = []
        
    def visit_FunctionDef(self, node):
        """Visit a function definition node."""
        # Skip special methods
        if node.name.startswith('__') and node.name.endswith('__'):
            self.generic_visit(node)
            return
            
        # Skip test functions
        if node.name.startswith('test_'):
            self.generic_visit(node)
            return
            
        # Record the function details
        function_info = {
            'name': node.name,
            'lineno': node.lineno,
            'args': [arg.arg for arg in node.args.args],
            'decorators': [self._get_decorator_name(dec) for dec in node.decorator_list],
            'class': self.current_class,
            'docstring': ast.get_docstring(node),
            'body': [self._get_source_segment(node)],
            'returns': self._extract_return_type(node),
            'complexity': self._calculate_complexity(node)
        }
        
        self.functions.append(function_info)
        self.generic_visit(node)
        
    def visit_ClassDef(self, node):
        """Visit a class definition node."""
        # Skip test classes
        if node.name.startswith('Test'):
            self.generic_visit(node)
            return
            
        # Record the class details
        class_info = {
            'name': node.name,
            'lineno': node.lineno,
            'bases': [self._get_name(base) for base in node.bases],
            'docstring': ast.get_docstring(node),
            'methods': []
        }
        
        self.classes.append(class_info)
        
        # Set the current class context and visit methods
        prev_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = prev_class
        
    def visit_Import(self, node):
        """Visit an import statement."""
        for name in node.names:
            self.imports.append({
                'name': name.name,
                'alias': name.asname,
                'type': 'import'
            })
        self.generic_visit(node)
        
    def visit_ImportFrom(self, node):
        """Visit a from-import statement."""
        module = node.module
        for name in node.names:
            self.imports.append({
                'name': f"{module}.{name.name}" if module else name.name,
                'alias': name.asname,
                'type': 'from',
                'module': module
            })
        self.generic_visit(node)
        
    def _calculate_complexity(self, node):
        """Calculate the cosmic complexity of a function."""
        # Count branches (if, for, while, etc.)
        complexity_visitor = ComplexityVisitor()
        complexity_visitor.visit(node)
        
        # Calculate a complexity score based on branches and parameters
        base_complexity = complexity_visitor.complexity
        param_complexity = len(node.args.args) * 0.5
        
        # Apply divine mathematics
        return (base_complexity + param_complexity) * (FIBONACCI_RATIO / SCHUMANN_RESONANCE) + 1
        
    def _get_decorator_name(self, node):
        """Extract the name of a decorator."""
        if isinstance(node, ast.Call):
            return self._get_name(node.func)
        return self._get_name(node)
    
    def _get_name(self, node):
        """Extract the name from an AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Call):
            return self._get_name(node.func)
        return str(node)
    
    def _extract_return_type(self, node):
        """Extract the return type from a function definition."""
        if node.returns:
            return self._get_name(node.returns)
        
        # Try to extract from docstring if available
        if node.docstring:
            return_match = re.search(r'[Rr]eturns:.*?(\w+)', node.docstring)
            if return_match:
                return return_match.group(1)
        
        return None
    
    def _get_source_segment(self, node):
        """Get the source code for a node."""
        # This is a simplified version, in reality we'd need the source code
        return f"<code at line {node.lineno}>"
        
    def analyze(self):
        """Analyze the Python file and extract functions and classes."""
        with open(self.file_path, 'r') as file:
            source = file.read()
            
        tree = ast.parse(source, filename=self.file_path)
        self.visit(tree)
        
        # Link methods to their classes
        for func in self.functions:
            if func['class']:
                for cls in self.classes:
                    if cls['name'] == func['class']:
                        cls['methods'].append(func['name'])
                        
        return {
            'functions': self.functions,
            'classes': self.classes,
            'imports': self.imports
        }


class ComplexityVisitor(ast.NodeVisitor):
    """Visitor that calculates the cosmic complexity of a function."""
    
    def __init__(self):
        """Initialize the complexity visitor."""
        self.complexity = 1  # Base complexity
        
    def visit_If(self, node):
        """Count if statements."""
        self.complexity += 1
        self.generic_visit(node)
        
    def visit_For(self, node):
        """Count for loops."""
        self.complexity += 2
        self.generic_visit(node)
        
    def visit_While(self, node):
        """Count while loops."""
        self.complexity += 2
        self.generic_visit(node)
        
    def visit_Try(self, node):
        """Count try-except blocks."""
        self.complexity += 1 + len(node.handlers)
        self.generic_visit(node)
        
    def visit_Assert(self, node):
        """Count assertions."""
        self.complexity += 0.1
        self.generic_visit(node)


class TestCoverageFinder:
    """Divine oracle that identifies untested functions and classes."""
    
    def __init__(self, src_path: str, test_path: Optional[str] = None):
        """
        Initialize the oracle with cosmic awareness.
        
        Args:
            src_path: Path to the source code directory or file
            test_path: Path to the test directory (if different from src_path)
        """
        self.src_path = Path(src_path)
        self.test_path = Path(test_path) if test_path else self.src_path.parent / 'tests'
        
        # Store analysis results
        self.src_modules = {}
        self.test_modules = {}
        self.missing_tests = {}
        
    def scan_directory(self, path: Path, is_test: bool = False) -> Dict[str, Dict]:
        """
        Scan a directory recursively for Python files.
        
        Args:
            path: Directory path to scan
            is_test: Whether these are test files
            
        Returns:
            Dict containing analysis of all Python files
        """
        results = {}
        
        if not path.exists():
            print(f"{YELLOW}Warning: Path {path} does not exist.{RESET}")
            return results
            
        if path.is_file() and path.suffix == '.py':
            # Single file case
            module_name = path.stem
            try:
                analyzer = CodeAnalyzer(str(path))
                results[module_name] = analyzer.analyze()
                results[module_name]['path'] = str(path)
                print(f"{GREEN}✓ Analyzed {path.name}{RESET}")
            except Exception as e:
                print(f"{RED}! Error analyzing {path}: {str(e)}{RESET}")
        else:
            # Directory case - walk recursively
            for item in path.glob('**/*.py'):
                if item.name.startswith('__') or (is_test and not item.name.startswith('test_')):
                    continue
                    
                rel_path = item.relative_to(path)
                module_path = '.'.join(list(rel_path.parent.parts) + [item.stem])
                
                try:
                    analyzer = CodeAnalyzer(str(item))
                    results[module_path] = analyzer.analyze()
                    results[module_path]['path'] = str(item)
                    print(f"{GREEN}✓ Analyzed {module_path}{RESET}")
                except Exception as e:
                    print(f"{RED}! Error analyzing {item}: {str(e)}{RESET}")
        
        return results
        
    def find_test_file(self, src_file: str) -> Optional[str]:
        """
        Find the corresponding test file for a source file.
        
        Args:
            src_file: Path to source file
            
        Returns:
            Path to test file if found, None otherwise
        """
        src_path = Path(src_file)
        src_name = src_path.stem
        
        # Common test file naming patterns
        test_names = [
            f"test_{src_name}.py",
            f"{src_name}_test.py",
            f"test_{src_name}_test.py"
        ]
        
        # Search in the test directory
        for test_name in test_names:
            # Direct match in test dir
            test_file = self.test_path / test_name
            if test_file.exists():
                return str(test_file)
                
            # Match in test/module/ subdirectory
            if src_path.parent.name:
                test_subdir = self.test_path / src_path.parent.name
                test_file = test_subdir / test_name
                if test_file.exists():
                    return str(test_file)
                    
        # Try to find by searching all test files
        for test_file in self.test_path.glob('**/*.py'):
            if test_file.name.startswith(f"test_{src_name}"):
                return str(test_file)
        
        return None
        
    def find_missing_coverage(self) -> Dict[str, Dict]:
        """
        Find functions and classes that lack test coverage.
        
        Returns:
            Dict containing items needing test coverage
        """
        missing = {}
        
        # First, scan source and test directories
        self.src_modules = self.scan_directory(self.src_path)
        self.test_modules = self.scan_directory(self.test_path, is_test=True)
        
        # Check each source module for test coverage
        for module_name, module_info in self.src_modules.items():
            module_missing = {
                'functions': [],
                'classes': [],
                'path': module_info['path'],
                'test_path': self.find_test_file(module_info['path'])
            }
            
            # Extract all tested functions and classes from test modules
            tested_functions = set()
            tested_classes = set()
            
            for test_info in self.test_modules.values():
                for test_func in test_info['functions']:
                    # Function names in test often contain the tested function name
                    func_name = test_func['name']
                    if func_name.startswith('test_'):
                        tested_target = func_name[5:]  # Remove 'test_' prefix
                        tested_functions.add(tested_target)
                        
                for test_class in test_info['classes']:
                    # Test class names often start with 'Test' followed by the class name
                    class_name = test_class['name']
                    if class_name.startswith('Test'):
                        tested_target = class_name[4:]  # Remove 'Test' prefix
                        tested_classes.add(tested_target)
                        
            # Find untested functions
            for func in module_info['functions']:
                func_name = func['name']
                if not any(func_name in tested for tested in tested_functions):
                    module_missing['functions'].append(func)
                    
            # Find untested classes
            for cls in module_info['classes']:
                cls_name = cls['name']
                if not any(cls_name in tested for tested in tested_classes):
                    module_missing['classes'].append(cls)
            
            # Only add if there are missing tests
            if module_missing['functions'] or module_missing['classes']:
                missing[module_name] = module_missing
                
        self.missing_tests = missing
        return missing
        
    def generate_test_template(self, module_name: str) -> str:
        """
        Generate a divine test template for a module with missing coverage.
        
        Args:
            module_name: Name of the module to generate tests for
            
        Returns:
            str: Python test code template
        """
        if module_name not in self.missing_tests:
            return f"# No missing tests found for {module_name}"
            
        missing = self.missing_tests[module_name]
        src_path = missing['path']
        
        # Determine the test file path
        if missing['test_path']:
            test_path = missing['test_path']
            test_exists = True
        else:
            # Create a path for a new test file
            src_file = Path(src_path)
            test_file = self.test_path / f"test_{src_file.stem}.py"
            test_path = str(test_file)
            test_exists = False
            
        # Import the tested module to inspect real signatures
        module_to_import = module_name.replace('/', '.').replace('\\', '.')
        
        # Start building the test template
        template = f"""#!/usr/bin/env python3
\"\"\"
OMEGA DEV FRAMEWORK - Divine Test Template
==========================================

This is a divine test template for {module_name}
Generated by the OMEGA TDD ORACLE.

Path: {test_path}
\"\"\"

import unittest
import pytest
from unittest.mock import patch, MagicMock

# Import the module to test
"""
        
        # Add imports
        if module_to_import.startswith('.'):
            template += f"from {module_to_import} import *  # Relative import\n"
        else:
            template += f"import {module_to_import}  # Adjust if needed\n"
            
        # Add mock data generator
        template += """
def generate_mock_data(data_type):
    \"\"\"Generate divine mock data for testing.\"\"\"
    if data_type == 'str':
        return "cosmic_string"
    elif data_type == 'int':
        return 42
    elif data_type == 'float':
        return 1.618
    elif data_type == 'list':
        return ["alpha", "omega", "divine"]
    elif data_type == 'dict':
        return {"key": "value", "divine": True}
    elif data_type == 'bool':
        return True
    else:
        return None

"""
        
        # Add test class
        template += f"""
class Test{Path(src_path).stem.capitalize()}(unittest.TestCase):
    \"\"\"Divine tests for {module_name}.\"\"\"
    
    def setUp(self):
        \"\"\"Set up the divine test environment.\"\"\"
        # TODO: Set up any necessary test fixtures
        pass
        
    def tearDown(self):
        \"\"\"Clean up after the divine tests.\"\"\"
        # TODO: Clean up any resources
        pass
"""
        
        # Add test methods for functions
        for func in missing['functions']:
            func_name = func['name']
            template += f"""
    def test_{func_name}(self):
        \"\"\"Test the divine functionality of {func_name}.\"\"\"
        # Arrange - Set up the test environment
"""
            
            # Add parameter setup
            for arg in func['args']:
                if arg == 'self' or arg == 'cls':
                    continue
                template += f"        {arg} = generate_mock_data('str')  # TODO: Use appropriate mock data\n"
                
            # Add function call
            if func['class']:
                # Method call
                template += f"\n        # Act - Call the function\n"
                template += f"        instance = {func['class']}()  # TODO: Initialize properly\n"
                
                args_str = ', '.join(arg for arg in func['args'] if arg != 'self')
                template += f"        result = instance.{func_name}({args_str})\n"
            else:
                # Function call
                template += f"\n        # Act - Call the function\n"
                args_str = ', '.join(arg for arg in func['args'] if arg != 'cls')
                
                if module_to_import.startswith('.'):
                    template += f"        result = {func_name}({args_str})\n"
                else:
                    template += f"        result = {module_to_import}.{func_name}({args_str})\n"
                    
            # Add assertions
            template += f"""
        # Assert - Verify the results
        # TODO: Replace with actual assertions
        self.assertIsNotNone(result)
"""
            
        # Add test methods for classes
        for cls in missing['classes']:
            cls_name = cls['name']
            template += f"""
    def test_{cls_name}_initialization(self):
        \"\"\"Test the divine initialization of {cls_name}.\"\"\"
        # Arrange - Set up the test environment
        # TODO: Set up any required parameters
        
        # Act - Initialize the class
        instance = {cls_name}()  # TODO: Add required constructor args
        
        # Assert - Verify initialization
        self.assertIsNotNone(instance)
"""
            
            # Add tests for class methods
            for method in cls.get('methods', []):
                template += f"""
    def test_{cls_name}_{method}(self):
        \"\"\"Test the divine method {method} of {cls_name}.\"\"\"
        # Arrange - Set up the test environment
        instance = {cls_name}()  # TODO: Add required constructor args
        
        # Act - Call the method
        # TODO: Add required method args
        result = instance.{method}()
        
        # Assert - Verify the results
        self.assertIsNotNone(result)
"""
                
        # Add main section
        template += """

if __name__ == '__main__':
    unittest.main()
"""
            
        return template
        
    def save_test_template(self, module_name: str) -> str:
        """
        Save a divine test template to file.
        
        Args:
            module_name: Name of the module to generate tests for
            
        Returns:
            str: Path to the saved test file
        """
        if module_name not in self.missing_tests:
            print(f"{YELLOW}No missing tests found for {module_name}{RESET}")
            return ""
            
        missing = self.missing_tests[module_name]
        
        # Determine the test file path
        if missing['test_path']:
            test_path = Path(missing['test_path'])
            test_exists = True
        else:
            # Create a path for a new test file
            src_file = Path(missing['path'])
            
            # Ensure the test directory exists
            test_dir = self.test_path
            if not test_dir.exists():
                test_dir.mkdir(parents=True)
                
            test_file = test_dir / f"test_{src_file.stem}.py"
            test_path = test_file
            test_exists = False
            
        # Generate the template
        template = self.generate_test_template(module_name)
        
        # Only write if the file doesn't exist or is empty
        if not test_exists or (test_path.exists() and test_path.stat().st_size == 0):
            test_path.parent.mkdir(parents=True, exist_ok=True)
            with open(test_path, 'w') as f:
                f.write(template)
            print(f"{GREEN}✓ Divine test template saved to {test_path}{RESET}")
        else:
            print(f"{YELLOW}! Test file already exists at {test_path}. Not overwriting.{RESET}")
            
            # Create a new file with a timestamp
            import time
            timestamp = int(time.time())
            new_path = test_path.parent / f"test_{test_path.stem}_{timestamp}.py"
            with open(new_path, 'w') as f:
                f.write(template)
            print(f"{GREEN}✓ Divine test template saved to {new_path} instead{RESET}")
            test_path = new_path
            
        return str(test_path)
        
    def print_missing_coverage_report(self) -> None:
        """Print a divine report of missing test coverage."""
        missing = self.missing_tests
        
        if not missing:
            print(f"{GREEN}{BOLD}✓ Divine blessing! All modules have test coverage.{RESET}")
            return
            
        total_missing_funcs = sum(len(info['functions']) for info in missing.values())
        total_missing_classes = sum(len(info['classes']) for info in missing.values())
        
        print(f"{YELLOW}{BOLD}═════════════════════════════════════════════════{RESET}")
        print(f"{MAGENTA}{BOLD} OMEGA TDD ORACLE - DIVINE COVERAGE PROPHECY {RESET}")
        print(f"{YELLOW}{BOLD}═════════════════════════════════════════════════{RESET}")
        print(f"{CYAN}Modules lacking complete test coverage: {len(missing)}{RESET}")
        print(f"{CYAN}Total functions needing tests: {total_missing_funcs}{RESET}")
        print(f"{CYAN}Total classes needing tests: {total_missing_classes}{RESET}")
        print()
        
        # Display detailed information for each module
        for module_name, info in missing.items():
            module_path = info['path']
            print(f"{BOLD}{YELLOW}Module: {module_name}{RESET}")
            print(f"{CYAN}Path: {module_path}{RESET}")
            
            if info['test_path']:
                print(f"{GREEN}Test file exists: {info['test_path']}{RESET}")
            else:
                print(f"{RED}No test file found{RESET}")
                
            # Print missing function coverage
            if info['functions']:
                print(f"\n{BOLD}Functions needing divine tests:{RESET}")
                for func in info['functions']:
                    complexity = func.get('complexity', 1.0)
                    priority = "HIGH" if complexity > 5 else "MEDIUM" if complexity > 2 else "LOW"
                    color = RED if priority == "HIGH" else YELLOW if priority == "MEDIUM" else GREEN
                    
                    print(f"  {color}• {func['name']} (line {func['lineno']}) - Complexity: {complexity:.1f} - Priority: {priority}{RESET}")
            
            # Print missing class coverage
            if info['classes']:
                print(f"\n{BOLD}Classes needing divine tests:{RESET}")
                for cls in info['classes']:
                    print(f"  {YELLOW}• {cls['name']} (line {cls['lineno']}) - Methods: {len(cls.get('methods', []))}{RESET}")
                    
            print(f"{YELLOW}{BOLD}─────────────────────────────────────────────────{RESET}\n")


def main():
    """Main entry point for the divine TDD Oracle."""
    parser = argparse.ArgumentParser(description="OMEGA DEV FRAMEWORK - Divine TDD Oracle")
    
    # Define command line arguments
    parser.add_argument('--scan-path', help="Path to scan for source code")
    parser.add_argument('--test-path', help="Path to scan for test code (default: ./tests)")
    parser.add_argument('--check-file', help="Check coverage for a specific file")
    parser.add_argument('--apply-recommendations', action='store_true', 
                        help="Generate test templates for all uncovered code")
    parser.add_argument('--generate-test', help="Generate test template for a specific module")
    
    args = parser.parse_args()
    
    # Determine the scan path
    scan_path = args.scan_path
    if args.check_file:
        scan_path = args.check_file
    if not scan_path:
        scan_path = '.'
        
    # Create the oracle
    oracle = TestCoverageFinder(scan_path, args.test_path)
    
    # Execute the divine command
    if args.check_file:
        print(f"{CYAN}Checking divine test coverage for single file: {args.check_file}{RESET}")
        oracle.find_missing_coverage()
        oracle.print_missing_coverage_report()
    elif args.generate_test:
        print(f"{CYAN}Generating divine test template for module: {args.generate_test}{RESET}")
        oracle.find_missing_coverage()
        oracle.save_test_template(args.generate_test)
    elif args.apply_recommendations:
        print(f"{CYAN}Applying divine test recommendations to all modules...{RESET}")
        oracle.find_missing_coverage()
        oracle.print_missing_coverage_report()
        
        # Generate and save test templates for all missing modules
        for module_name in oracle.missing_tests:
            oracle.save_test_template(module_name)
    else:
        print(f"{CYAN}Performing divine test coverage analysis...{RESET}")
        oracle.find_missing_coverage()
        oracle.print_missing_coverage_report()
        
        # Suggest next steps
        if oracle.missing_tests:
            print(f"{YELLOW}Divine guidance:{RESET}")
            print(f"{YELLOW}Run with --apply-recommendations to generate test templates{RESET}")
            print(f"{YELLOW}Or use --generate-test MODULE to create tests for a specific module{RESET}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 