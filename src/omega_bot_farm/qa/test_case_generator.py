#!/usr/bin/env python3
"""
CyBer1t4L Test Case Generator

Analyzes Python modules using AST to identify functions and classes,
then generates test cases with appropriate mocks and assertions.
"""

import os
import ast
import sys
import argparse
import inspect
import logging
import importlib
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, Set, Union
from datetime import datetime

# ANSI color codes for cyberpunk theming
class Colors:
    RESET = "\033[0m"
    NEON_GREEN = "\033[38;5;82m"
    NEON_BLUE = "\033[38;5;39m"
    NEON_PINK = "\033[38;5;213m"
    NEON_YELLOW = "\033[38;5;226m"
    CYBER_CYAN = "\033[38;5;51m"
    CYBER_PURPLE = "\033[38;5;141m"
    
    @staticmethod
    def format(text, color):
        return f"{color}{text}{Colors.RESET}"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=f"{Colors.CYBER_PURPLE}[%(asctime)s]{Colors.RESET} {Colors.CYBER_CYAN}%(levelname)s{Colors.RESET} %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("CyBer1t4L.TestGen")

class FunctionInfo:
    """Stores information about a function for test generation."""
    def __init__(self, name: str, args: List[str], is_async: bool, 
                 docstring: Optional[str], decorators: List[str],
                 return_type: Optional[str] = None):
        self.name = name
        self.args = args
        self.is_async = is_async
        self.docstring = docstring
        self.decorators = decorators
        self.return_type = return_type
    
    def __repr__(self):
        async_prefix = "async " if self.is_async else ""
        return f"{async_prefix}def {self.name}({', '.join(self.args)})"

class ClassInfo:
    """Stores information about a class for test generation."""
    def __init__(self, name: str, bases: List[str], docstring: Optional[str], 
                 methods: Dict[str, FunctionInfo]):
        self.name = name
        self.bases = bases
        self.docstring = docstring
        self.methods = methods
    
    def __repr__(self):
        return f"class {self.name}({', '.join(self.bases)})"

class ModuleAnalyzer(ast.NodeVisitor):
    """Analyzes a Python module using AST to extract information for test generation."""
    def __init__(self):
        self.functions: Dict[str, FunctionInfo] = {}
        self.classes: Dict[str, ClassInfo] = {}
        self.imports: Set[str] = set()
        self.current_class = None
    
    def visit_Import(self, node):
        """Record import statements."""
        for name in node.names:
            self.imports.add(name.name)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """Record from import statements."""
        if node.module:
            for name in node.names:
                self.imports.add(f"{node.module}.{name.name}")
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        """Extract class information."""
        bases = [self._get_name(base) for base in node.bases]
        docstring = ast.get_docstring(node)
        
        # Store previous class context if we're nested
        prev_class = self.current_class
        self.current_class = node.name
        
        # First pass to collect methods
        methods = {}
        self.classes[node.name] = ClassInfo(node.name, bases, docstring, methods)
        
        # Visit the class body
        self.generic_visit(node)
        
        # Restore previous context
        self.current_class = prev_class
    
    def visit_FunctionDef(self, node):
        """Extract function information."""
        self._process_function(node, is_async=False)
    
    def visit_AsyncFunctionDef(self, node):
        """Extract async function information."""
        self._process_function(node, is_async=True)
    
    def _process_function(self, node, is_async: bool):
        """Process a function or method definition."""
        # Get args without self/cls for methods
        args = []
        for arg in node.args.args:
            # Skip 'self' and 'cls' when in a class context
            if self.current_class and arg.arg in ('self', 'cls'):
                continue
            args.append(arg.arg)
        
        # Extract docstring
        docstring = ast.get_docstring(node)
        
        # Extract return type annotation if present
        return_type = None
        if node.returns:
            return_type = self._get_name(node.returns)
        
        # Extract decorators
        decorators = []
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name):
                decorators.append(decorator.id)
            elif isinstance(decorator, ast.Attribute):
                decorators.append(self._get_name(decorator))
        
        # Create function info
        func_info = FunctionInfo(
            name=node.name,
            args=args,
            is_async=is_async,
            docstring=docstring,
            decorators=decorators,
            return_type=return_type
        )
        
        # Store in appropriate place
        if self.current_class:
            self.classes[self.current_class].methods[node.name] = func_info
        else:
            self.functions[node.name] = func_info
    
    def _get_name(self, node):
        """Extract a name from various node types."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Subscript):
            return f"{self._get_name(node.value)}[{self._get_name(node.slice)}]"
        elif isinstance(node, ast.Index):
            # For Python < 3.9
            return self._get_name(node.value)
        elif isinstance(node, ast.Str):
            return node.s
        else:
            return str(node)

class TestGenerator:
    """Generates test cases based on analyzed module information."""
    def __init__(self, project_root: Path):
        self.project_root = project_root
    
    def generate_test_file(self, module_path: str) -> Tuple[bool, str]:
        """
        Generate test file for a module.
        
        Args:
            module_path: Path to the module file
            
        Returns:
            Tuple of (success, output_path)
        """
        try:
            # Parse the module path
            module_file = Path(module_path)
            if not module_file.exists():
                logger.error(f"Module file not found: {module_path}")
                return False, ""
            
            # Generate test file path
            module_name = module_file.stem
            test_file_path = self.project_root / "tests" / f"test_{module_name}.py"
            
            # Analyze the module
            with open(module_file, 'r') as f:
                module_content = f.read()
                
            # Parse the AST
            tree = ast.parse(module_content)
            analyzer = ModuleAnalyzer()
            analyzer.visit(tree)
            
            # Generate test content
            test_content = self._generate_test_content(
                module_path=module_path,
                module_name=module_name,
                functions=analyzer.functions,
                classes=analyzer.classes,
                imports=analyzer.imports
            )
            
            # Create the output directory if it doesn't exist
            test_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write the test file
            with open(test_file_path, 'w') as f:
                f.write(test_content)
                
            logger.info(f"{Colors.format('Test file generated:', Colors.NEON_GREEN)} {test_file_path}")
            return True, str(test_file_path)
            
        except Exception as e:
            logger.error(f"Error generating test file: {str(e)}")
            return False, ""
    
    def _generate_test_content(self, module_path: str, module_name: str,
                              functions: Dict[str, FunctionInfo],
                              classes: Dict[str, ClassInfo],
                              imports: Set[str]) -> str:
        """Generate the content for the test file."""
        # Format the import path
        rel_path = Path(module_path).relative_to(self.project_root) if self.project_root in Path(module_path).parents else Path(module_path)
        import_path = str(rel_path).replace("/", ".").replace(".py", "")
        
        # Create the test file header
        lines = [
            "#!/usr/bin/env python3",
            f'"""',
            f"Tests for {module_name}",
            "",
            f"Auto-generated by CyBer1t4L Test Generator",
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f'"""',
            "",
            "import os",
            "import sys",
            "import pytest",
            "import unittest.mock as mock",
            "from unittest.mock import patch, MagicMock, AsyncMock",
            "",
            "# Add the project root to the path for imports",
            "sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))",
            "",
        ]
        
        # Add module import
        import_names = []
        for cls_name in classes.keys():
            import_names.append(cls_name)
        for func_name in functions.keys():
            import_names.append(func_name)
            
        if import_names:
            lines.append(f"# Import the module elements to test")
            lines.append(f"from {import_path} import {', '.join(import_names)}")
            lines.append("")
        
        # Generate test classes for each class in the module
        for cls_name, cls_info in classes.items():
            lines.extend(self._generate_class_test(cls_name, cls_info))
            lines.append("")
        
        # Generate test functions for each standalone function
        if functions:
            lines.append(f"class Test{module_name.capitalize()}Functions:")
            lines.append(f'    """Tests for standalone functions in the {module_name} module."""')
            lines.append("")
            
            for func_name, func_info in functions.items():
                lines.extend(self._generate_function_test(func_name, func_info, indent=4))
            
            lines.append("")
        
        return "\n".join(lines)
    
    def _generate_class_test(self, cls_name: str, cls_info: ClassInfo) -> List[str]:
        """Generate test class for a class."""
        lines = [
            f"class Test{cls_name}:",
            f'    """Tests for the {cls_name} class."""',
            "",
            "    @pytest.fixture",
            "    def instance(self):",
            f'        """Create a {cls_name} instance for testing."""',
            "        # TODO: Add appropriate constructor arguments",
            f"        return {cls_name}()",
            ""
        ]
        
        # Add a test method for each method in the class
        for method_name, method_info in cls_info.methods.items():
            # Skip private methods
            if method_name.startswith('_') and not method_name.startswith('__') and not method_name.endswith('__'):
                continue
                
            # Skip dunder methods except for common ones we might want to test
            if method_name.startswith('__') and method_name.endswith('__') and method_name not in ('__init__', '__call__', '__str__', '__repr__'):
                continue
                
            lines.extend(self._generate_method_test(method_name, method_info))
        
        return lines
    
    def _generate_method_test(self, method_name: str, method_info: FunctionInfo) -> List[str]:
        """Generate test for a class method."""
        # Skip initialization method since it's tested through the fixture
        if method_name == '__init__':
            return []
            
        is_property = 'property' in method_info.decorators
        
        if is_property:
            lines = [
                f"    def test_{method_name}_property(self, instance):",
                f'        """Test the {method_name} property."""',
                "        # TODO: Implement property test",
                f"        result = instance.{method_name}",
                "        assert result is not None  # Replace with appropriate assertion",
                ""
            ]
        else:
            test_name = f"test_{method_name}"
            
            # Create test parameters
            args = []
            for arg in method_info.args:
                args.append(f"{arg}=mock.MagicMock()")
            
            async_prefix = "async " if method_info.is_async else ""
            test_decorator = "@pytest.mark.asyncio\n    " if method_info.is_async else ""
            await_prefix = "await " if method_info.is_async else ""
            
            lines = [
                f"    {test_decorator}def {test_name}(self, instance):",
                f'        """Test the {method_name} method."""',
                "        # TODO: Implement method test",
            ]
            
            if method_info.args:
                lines.append(f"        # Method signature: {method_info}")
                
            if method_info.return_type:
                lines.append(f"        # Expected return type: {method_info.return_type}")
                
            lines.extend([
                f"        result = {await_prefix}instance.{method_name}({', '.join(repr(mock.MagicMock()) for _ in method_info.args)})",
                "        assert result is not None  # Replace with appropriate assertion",
                ""
            ])
            
        return lines
    
    def _generate_function_test(self, func_name: str, func_info: FunctionInfo, indent: int = 0) -> List[str]:
        """Generate test for a standalone function."""
        indentation = " " * indent
        test_name = f"test_{func_name}"
        
        async_prefix = "async " if func_info.is_async else ""
        test_decorator = f"{indentation}@pytest.mark.asyncio\n{indentation}" if func_info.is_async else ""
        await_prefix = "await " if func_info.is_async else ""
        
        lines = [
            f"{indentation}{test_decorator}def {test_name}(self):",
            f'{indentation}    """Test the {func_name} function."""',
            f"{indentation}    # TODO: Implement function test",
        ]
        
        if func_info.args:
            lines.append(f"{indentation}    # Function signature: {func_info}")
            
        if func_info.return_type:
            lines.append(f"{indentation}    # Expected return type: {func_info.return_type}")
            
        args = []
        for arg in func_info.args:
            args.append(f"{arg}=mock.MagicMock()")
            
        lines.extend([
            f"{indentation}    result = {await_prefix}{func_name}({', '.join(repr(mock.MagicMock()) for _ in func_info.args)})",
            f"{indentation}    assert result is not None  # Replace with appropriate assertion",
            ""
        ])
        
        return lines

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="CyBer1t4L Test Case Generator")
    
    parser.add_argument("modules", nargs="+", help="Modules to generate tests for")
    
    parser.add_argument("--project-root", "-r", type=str, help="Project root directory")
    
    parser.add_argument("--output-dir", "-o", type=str, help="Output directory for test files")
    
    return parser.parse_args()

def main():
    """Main entry point."""
    args = parse_args()
    
    # Determine project root
    if args.project_root:
        project_root = Path(args.project_root)
    else:
        project_root = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
    
    logger.info(f"{Colors.format('CyBer1t4L Test Generator', Colors.NEON_BLUE)}")
    logger.info(f"Project root: {project_root}")
    
    # Create test generator
    generator = TestGenerator(project_root)
    
    # Process each module
    for module_path in args.modules:
        logger.info(f"Generating tests for {Colors.format(module_path, Colors.CYBER_CYAN)}")
        success, output_path = generator.generate_test_file(module_path)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 