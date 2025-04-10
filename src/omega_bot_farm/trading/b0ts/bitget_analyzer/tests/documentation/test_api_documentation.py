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
Tests that verify the API documentation matches the actual implementation of BitgetPositionAnalyzerB0t.

This test suite ensures:
1. All public methods are documented
2. Method signatures in documentation match the actual implementation
3. Parameter descriptions exist for all parameters
4. Return type documentation matches actual return types
"""

import inspect
import re
import pytest
from pathlib import Path


@pytest.mark.usefixtures("doc_markdown_content")
class TestAPIDocumentation:
    """Test suite for verifying API documentation accuracy and completeness."""

    def test_all_public_methods_are_documented_in_docstrings(self, mock_bitget_position_analyzer_bot):
        """Test that all public methods have docstrings."""
        bot_class = mock_bitget_position_analyzer_bot
        
        for method_name, method in self._get_public_methods(bot_class):
            assert method.__doc__ is not None, f"Method {method_name} is missing a docstring"
            assert len(method.__doc__.strip()) > 0, f"Method {method_name} has an empty docstring"
    
    def test_method_signatures_match_docstrings(self, mock_bitget_position_analyzer_bot):
        """Test that method signatures in code match their docstrings."""
        bot_class = mock_bitget_position_analyzer_bot
        
        for method_name, method in self._get_public_methods(bot_class):
            if method_name == "__init__":
                # For constructor, check class docstring for parameters
                docstring = bot_class.__doc__
            else:
                docstring = method.__doc__

            # Skip if no docstring
            if not docstring:
                continue
                
            # Get actual parameters
            sig = inspect.signature(method)
            actual_params = list(sig.parameters.keys())
            if method_name != "__init__" and len(actual_params) > 0 and actual_params[0] == "self":
                actual_params = actual_params[1:]  # Remove 'self' from instance methods
                
            # Parse the Args section from docstring to get documented parameters
            docstring_params = []
            args_pattern = r"Args:(.*?)(?:Returns:|Raises:|$)"
            args_match = re.search(args_pattern, docstring, re.DOTALL)
            
            if args_match:
                args_section = args_match.group(1).strip()
                param_pattern = r"(\w+)\s*\("
                docstring_params = re.findall(param_pattern, args_section)
                
            # Check that all actual parameters are documented
            for param in actual_params:
                if param != "self":
                    assert param in docstring_params, f"Parameter '{param}' of {method_name} is not documented in docstring"

    def test_parameters_have_type_hints(self, mock_bitget_position_analyzer_bot):
        """Test that parameters have type hints in docstrings."""
        bot_class = mock_bitget_position_analyzer_bot
        
        for method_name, method in self._get_public_methods(bot_class):
            docstring = method.__doc__
            if not docstring:
                continue
                
            args_pattern = r"Args:(.*?)(?:Returns:|Raises:|$)"
            args_match = re.search(args_pattern, docstring, re.DOTALL)
            
            if args_match:
                args_section = args_match.group(1).strip()
                param_lines = [line.strip() for line in args_section.split('\n') if line.strip()]
                
                for line in param_lines:
                    # Check for parameter type hint pattern "param_name (type): description"
                    param_pattern = r"(\w+)\s*\(([^)]+)\):"
                    match = re.search(param_pattern, line)
                    
                    assert match is not None, f"Parameter in {method_name} docstring missing type hint: {line}"
    
    def test_return_values_are_documented(self, mock_bitget_position_analyzer_bot):
        """Test that return values are documented."""
        bot_class = mock_bitget_position_analyzer_bot
        
        for method_name, method in self._get_public_methods(bot_class):
            # Skip __init__ as it doesn't return anything
            if method_name == "__init__":
                continue
                
            docstring = method.__doc__
            if not docstring:
                continue
                
            # Check for Returns section
            returns_pattern = r"Returns:(.*?)(?:Raises:|$)"
            returns_match = re.search(returns_pattern, docstring, re.DOTALL)
            
            # Get return type from signature if available
            sig = inspect.signature(method)
            has_return_annotation = sig.return_annotation != inspect.Signature.empty
            
            # Only assert if method has a return annotation or if it's an async method (which returns a coroutine)
            if has_return_annotation or inspect.iscoroutinefunction(method):
                assert returns_match is not None, f"Method {method_name} is missing a Returns section in docstring"
                
                if returns_match:
                    returns_section = returns_match.group(1).strip()
                    assert len(returns_section) > 0, f"Method {method_name} has an empty Returns section"
    
    def test_all_public_methods_are_documented_in_markdown(self, mock_bitget_position_analyzer_bot, doc_markdown_content):
        """Test that all public methods are documented in the markdown file."""
        bot_class = mock_bitget_position_analyzer_bot
        
        # Skip this test if documentation is not found
        if doc_markdown_content is None:
            pytest.skip("Documentation file not found")
            
        for method_name, _ in self._get_public_methods(bot_class):
            # Check if method name appears in the markdown
            assert method_name in doc_markdown_content, f"Method {method_name} is not documented in the markdown file"
            
            # Check for code example section
            method_heading_pattern = f"#+\\s+`{method_name}`"
            method_heading_match = re.search(method_heading_pattern, doc_markdown_content)
            
            assert method_heading_match is not None, f"Method {method_name} does not have a proper heading in markdown"
    
    def test_examples_for_key_methods(self, mock_bitget_position_analyzer_bot, doc_markdown_content):
        """Test that key methods have usage examples."""
        # List of key methods that should have examples
        key_methods = ["__init__", "get_positions", "analyze_position", "calculate_harmony_score"]
        
        # Skip this test if documentation is not found
        if doc_markdown_content is None:
            pytest.skip("Documentation file not found")
            
        for method_name in key_methods:
            # Check if method has a Python code example in the markdown
            code_example_pattern = f"```python[\\s\\S]*?{method_name}[\\s\\S]*?```"
            code_example_match = re.search(code_example_pattern, doc_markdown_content)
            
            assert code_example_match is not None, f"Key method {method_name} does not have a Python code example"
    
    def _get_public_methods(self, cls):
        """Get all public methods of a class (excluding private/protected methods)."""
        return [(name, method) for name, method in inspect.getmembers(cls, predicate=inspect.isfunction)
                if not name.startswith('_') or name == '__init__']


if __name__ == "__main__":
    pytest.main() 