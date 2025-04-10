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
Tests that verify code examples in the documentation for BitgetPositionAnalyzerB0t.

This test suite ensures:
1. Code examples in the documentation actually run
2. Examples produce the expected outputs
3. API usage examples match the current API
4. Advanced usage examples are valid
"""

import ast
import re
import pytest
import tempfile
import textwrap
import asyncio
import sys
import io
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch, MagicMock


@pytest.mark.usefixtures("doc_markdown_content")
class TestExampleValidation:
    """Test suite for verifying examples in the documentation."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.examples = []

    def test_example_syntax(self, doc_markdown_content, temp_py_file):
        """Test that code examples have valid Python syntax."""
        if doc_markdown_content is None:
            pytest.skip("Documentation file not found")
            
        # Extract examples from documentation
        examples = self._extract_python_examples(doc_markdown_content)
        
        for i, example in enumerate(examples):
            # Write example to temporary file for syntax checking
            with open(temp_py_file, 'w') as f:
                f.write(example)
                
            try:
                # Try to parse the example as Python code
                with open(temp_py_file, 'r') as f:
                    ast.parse(f.read())
            except SyntaxError as e:
                pytest.fail(f"Example {i+1} has invalid syntax: {str(e)}\nCode:\n{example}")
    
    def test_basic_examples_run(self, doc_markdown_content, mock_bitget_position_analyzer_bot, temp_py_file):
        """Test that basic examples run without errors."""
        if doc_markdown_content is None:
            pytest.skip("Documentation file not found")
            
        # Extract examples from documentation
        examples = self._extract_python_examples(doc_markdown_content)
        basic_examples = [ex for ex in examples if "import" in ex and len(ex.strip().split('\n')) < 10]
        
        MockBot = mock_bitget_position_analyzer_bot
        
        for i, example in enumerate(basic_examples):
            # Skip examples that require external services
            if "redis" in example.lower() or "discord" in example.lower():
                continue
                
            # Modify example to use our mock class
            modified_example = self._prepare_example_for_execution(example, MockBot)
            
            with open(temp_py_file, 'w') as f:
                f.write(modified_example)
                
            # Create a namespace for executing the example
            namespace = {
                'BitgetPositionAnalyzerB0t': MockBot,
                'asyncio': asyncio,
                'print': print
            }
            
            try:
                # Execute the example
                with open(temp_py_file, 'r') as f:
                    exec(f.read(), namespace)
            except Exception as e:
                pytest.fail(f"Basic example {i+1} failed to run: {str(e)}\nCode:\n{modified_example}")
    
    def test_initialization_examples(self, doc_markdown_content, mock_bitget_position_analyzer_bot):
        """Test that initialization examples are correct."""
        if doc_markdown_content is None:
            pytest.skip("Documentation file not found")
            
        # Find initialization examples
        init_pattern = r"```python\s*(?:.*?\n)?.*?BitgetPositionAnalyzerB0t\s*\(.*?\).*?```"
        init_examples = re.findall(init_pattern, doc_markdown_content, re.DOTALL)
        
        if not init_examples:
            pytest.skip("No initialization examples found in documentation")
            
        MockBot = mock_bitget_position_analyzer_bot
        
        for i, example in enumerate(init_examples):
            # Extract the actual initialization code
            code_lines = example.replace("```python", "").replace("```", "").strip().split("\n")
            init_line = next((line for line in code_lines if "BitgetPositionAnalyzerB0t(" in line), None)
            
            if not init_line:
                continue
                
            # Extract the parameters
            init_params = {}
            if "=" in init_line:
                # Handle the case with named parameters
                params_match = re.search(r"BitgetPositionAnalyzerB0t\((.*?)\)", init_line)
                if params_match and params_match.group(1).strip():
                    params_text = params_match.group(1)
                    for param in params_text.split(","):
                        if "=" in param:
                            key, value = param.split("=", 1)
                            init_params[key.strip()] = eval(value.strip())
            
            # Check if the parameters are valid
            try:
                bot = MockBot(**init_params)
                assert isinstance(bot, MockBot), "Failed to create bot instance"
                
                # Verify that all parameters were set correctly
                for param, value in init_params.items():
                    assert hasattr(bot, param), f"Parameter '{param}' not set in bot instance"
                    assert getattr(bot, param) == value, f"Parameter '{param}' has incorrect value"
                    
            except Exception as e:
                pytest.fail(f"Initialization example {i+1} is invalid: {str(e)}\nCode:\n{init_line}")
    
    async def _run_async_example(self, code, namespace):
        """Helper to run async code examples."""
        exec(code, namespace)
        if 'main' in namespace and asyncio.iscoroutinefunction(namespace['main']):
            await namespace['main']()
    
    def test_analysis_examples(self, doc_markdown_content, mock_bitget_position_analyzer_bot, temp_py_file):
        """Test that position analysis examples are correct."""
        if doc_markdown_content is None:
            pytest.skip("Documentation file not found")
            
        # Find analysis examples
        analysis_pattern = r"```python\s*(?:.*?\n)?.*?analyze_position\s*\(.*?\).*?```"
        analysis_examples = re.findall(analysis_pattern, doc_markdown_content, re.DOTALL)
        
        if not analysis_examples:
            pytest.skip("No position analysis examples found in documentation")
            
        MockBot = mock_bitget_position_analyzer_bot
        
        for i, example in enumerate(analysis_examples):
            # Skip examples that require external services
            if "redis" in example.lower() or "discord" in example.lower():
                continue
                
            # Extract the code within the python block
            code = example.replace("```python", "").replace("```", "").strip()
            
            # Modify example to use our mock class
            modified_code = self._prepare_example_for_execution(code, MockBot)
            
            with open(temp_py_file, 'w') as f:
                f.write(modified_code)
                
            # Create a namespace for executing the example
            namespace = {
                'BitgetPositionAnalyzerB0t': MockBot,
                'asyncio': asyncio,
                'print': print
            }
            
            try:
                # Capture the output
                captured_output = io.StringIO()
                with redirect_stdout(captured_output):
                    # If the example contains async code, run it accordingly
                    if "async " in modified_code or "await " in modified_code:
                        asyncio.run(self._run_async_example(modified_code, namespace))
                    else:
                        exec(modified_code, namespace)
                        
                # Verify that the example produced some output
                output = captured_output.getvalue()
                if "print" in modified_code:
                    assert output.strip(), "Analysis example didn't produce expected output"
                    
            except Exception as e:
                pytest.fail(f"Analysis example {i+1} failed to run: {str(e)}\nCode:\n{modified_code}")
    
    def test_harmony_score_examples(self, doc_markdown_content, mock_bitget_position_analyzer_bot, temp_py_file):
        """Test that harmony score examples are correct."""
        if doc_markdown_content is None:
            pytest.skip("Documentation file not found")
            
        # Find harmony score examples
        harmony_pattern = r"```python\s*(?:.*?\n)?.*?calculate_harmony_score\s*\(.*?\).*?```"
        harmony_examples = re.findall(harmony_pattern, doc_markdown_content, re.DOTALL)
        
        if not harmony_examples:
            pytest.skip("No harmony score examples found in documentation")
            
        MockBot = mock_bitget_position_analyzer_bot
        
        for i, example in enumerate(harmony_examples):
            # Extract the code within the python block
            code = example.replace("```python", "").replace("```", "").strip()
            
            # Modify example to use our mock class
            modified_code = self._prepare_example_for_execution(code, MockBot)
            
            with open(temp_py_file, 'w') as f:
                f.write(modified_code)
                
            # Create a namespace for executing the example
            namespace = {
                'BitgetPositionAnalyzerB0t': MockBot,
                'asyncio': asyncio,
                'print': print
            }
            
            try:
                # Capture the output
                captured_output = io.StringIO()
                with redirect_stdout(captured_output):
                    # Execute the example
                    exec(modified_code, namespace)
                    
                # If the example calculates a harmony score, make sure it's in the expected range
                if "harmony_score" in modified_code and "print" in modified_code:
                    output = captured_output.getvalue()
                    if output.strip():
                        try:
                            # Try to extract numeric values from the output
                            numbers = re.findall(r"\d+\.\d+|\d+", output)
                            for num_str in numbers:
                                num = float(num_str)
                                # Harmony scores should typically be between 0 and 100
                                if 0 <= num <= 100:
                                    break
                            else:
                                pytest.fail(f"Harmony score example {i+1} didn't produce a value in the expected range (0-100)")
                        except ValueError:
                            pass  # Not all numbers in output may be harmony scores
                
            except Exception as e:
                pytest.fail(f"Harmony score example {i+1} failed to run: {str(e)}\nCode:\n{modified_code}")
    
    def _extract_python_examples(self, content):
        """Extract Python code examples from markdown content."""
        # Find all Python code blocks
        pattern = r"```python\s*(.*?)\s*```"
        examples = re.findall(pattern, content, re.DOTALL)
        
        # Clean up the examples (remove comments, fix indentation)
        cleaned_examples = []
        for example in examples:
            # Skip empty examples
            if not example.strip():
                continue
                
            # Skip examples that are just import statements
            if example.strip().startswith("import ") and "\n" not in example.strip():
                continue
                
            # Dedent the example to fix indentation
            example = textwrap.dedent(example)
            
            cleaned_examples.append(example)
            
        return cleaned_examples
    
    def _prepare_example_for_execution(self, example, mock_class):
        """Prepare an example for execution with mock class."""
        # Replace imports with mock class and ensure asyncio is imported
        modified_lines = []
        
        # Add imports if needed
        if "import asyncio" not in example:
            modified_lines.append("import asyncio")
            
        # Process each line
        for line in example.split('\n'):
            # Skip original import of BitgetPositionAnalyzerB0t
            if "import" in line and "BitgetPositionAnalyzerB0t" in line:
                continue
                
            # Add the line to our modified example
            modified_lines.append(line)
            
        # Create an async main function for examples with await
        if "await" in example and "async def main" not in example:
            # Indent all lines
            for i in range(len(modified_lines)):
                if modified_lines[i].strip():
                    modified_lines[i] = "    " + modified_lines[i]
            
            # Wrap in async main function
            modified_lines.insert(0, "async def main():")
            modified_lines.append("")
            modified_lines.append("if __name__ == '__main__':")
            modified_lines.append("    asyncio.run(main())")
            
        return "\n".join(modified_lines)


if __name__ == "__main__":
    pytest.main() 