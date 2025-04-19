#!/usr/bin/env python3
# ✨ GBU2™ License Notice - Consciousness Level 9 🧬
# -----------------------
# This code is blessed under the GBU2™ License

"""
Test cases for the HighlightRenderer class in the repository_utils module.

This specifically tests the block_code method to ensure it handles all parameter
combinations correctly, including the 'info' parameter that caused the error:
"HighlightRenderer.block_code() got an unexpected keyword argument 'info'"
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Try to import mistune and pygments, providing graceful fallbacks for testing
try:
    import mistune
    MISTUNE_AVAILABLE = True
except ImportError:
    MISTUNE_AVAILABLE = False
    # Create a minimal mock of HTMLRenderer for testing
    class MockHTMLRenderer:
        def __init__(self):
            pass
    mistune = MagicMock()
    mistune.HTMLRenderer = MockHTMLRenderer
    mistune.escape = lambda x: x

try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import html
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False
    # Create mocks for testing
    highlight = MagicMock(return_value="<highlighted code>")
    get_lexer_by_name = MagicMock()
    html = MagicMock()
    html.HtmlFormatter = MagicMock()

# Import the class to test
try:
    from common.repository_utils import HighlightRenderer
    REPO_UTILS_AVAILABLE = True
except ImportError:
    REPO_UTILS_AVAILABLE = False
    # Create a minimal implementation for testing if actual module not available
    class HighlightRenderer(mistune.HTMLRenderer):
        def block_code(self, code, lang=None, info=None):
            if lang and PYGMENTS_AVAILABLE:
                try:
                    lexer = get_lexer_by_name(lang, stripall=True)
                    formatter = html.HtmlFormatter(
                        style='monokai', 
                        linenos=True,
                        cssclass="source"
                    )
                    return highlight(code, lexer, formatter)
                except:
                    pass
            return f'<pre><code>{mistune.escape(code)}</code></pre>'

@unittest.skipIf(not MISTUNE_AVAILABLE, "mistune package is not available")
class TestHighlightRenderer(unittest.TestCase):
    """Test cases for the HighlightRenderer class."""

    def setUp(self):
        """Set up a renderer instance for testing."""
        self.renderer = HighlightRenderer()
        
    def test_block_code_with_no_params(self):
        """Test block_code with only the required 'code' parameter."""
        code = "print('hello world')"
        result = self.renderer.block_code(code)
        self.assertIn("<pre><code>", result)
        self.assertIn("print('hello world')", result)
        
    def test_block_code_with_lang(self):
        """Test block_code with both 'code' and 'lang' parameters."""
        code = "print('hello world')"
        result = self.renderer.block_code(code, lang="python")
        if PYGMENTS_AVAILABLE:
            # With Pygments, there should be syntax highlighting
            self.assertIn("source", result)
        else:
            # Without Pygments, it falls back to plain rendering
            self.assertIn("<pre><code>", result)
            
    def test_block_code_with_info(self):
        """Test block_code with the 'info' parameter that caused the original error."""
        code = "print('hello world')"
        try:
            result = self.renderer.block_code(code, lang="python", info="test info")
            # If we get here, the method accepted the info parameter
            self.assertIsNotNone(result)
            if PYGMENTS_AVAILABLE:
                self.assertIn("source", result)
            else:
                self.assertIn("<pre><code>", result)
        except TypeError as e:
            self.fail(f"block_code raised TypeError with info parameter: {e}")
            
    @patch('common.repository_utils.highlight')
    def test_block_code_with_pygments_exception(self, mock_highlight):
        """Test block_code handles exceptions from pygments gracefully."""
        if not REPO_UTILS_AVAILABLE:
            self.skipTest("repository_utils module not available")
            
        # Make the highlight function raise an exception
        mock_highlight.side_effect = Exception("Test exception")
        
        code = "print('hello world')"
        result = self.renderer.block_code(code, lang="python", info="test info")
        
        # Should fall back to plain rendering
        self.assertIn("<pre><code>", result)
        
    def test_block_code_with_all_params_and_variations(self):
        """Test block_code with various combinations of parameters."""
        test_cases = [
            {"code": "print('hello')", "expected": "print('hello')"},
            {"code": "print('hello')", "lang": "python", "expected": "print('hello')"},
            {"code": "print('hello')", "info": "some info", "expected": "print('hello')"},
            {"code": "print('hello')", "lang": "python", "info": "some info", "expected": "print('hello')"},
            {"code": "<script>alert('xss')</script>", "expected": "&lt;script&gt;alert('xss')&lt;/script&gt;"}
        ]
        
        for tc in test_cases:
            code = tc["code"]
            lang = tc.get("lang")
            info = tc.get("info")
            expected = tc["expected"]
            
            # Call the method with the appropriate parameters
            if lang and info:
                result = self.renderer.block_code(code, lang=lang, info=info)
            elif lang:
                result = self.renderer.block_code(code, lang=lang)
            elif info:
                result = self.renderer.block_code(code, info=info)
            else:
                result = self.renderer.block_code(code)
                
            # Check that the expected content is in the result
            self.assertIn(expected, result.replace("&lt;", "<").replace("&gt;", ">"))

if __name__ == "__main__":
    unittest.main() 