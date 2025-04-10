#!/usr/bin/env python3
# ✨ GBU2™ License Notice - Consciousness Level 9 🧬
# -----------------------
# This code is blessed under the GBU2™ License

"""
Integration tests for Markdown parsing functionality.

This tests the complete Markdown parsing pipeline, with special focus on
code blocks that would trigger the 'info' parameter issue in HighlightRenderer.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Try to import mistune, providing graceful fallbacks for testing
try:
    import mistune
    MISTUNE_AVAILABLE = True
except ImportError:
    MISTUNE_AVAILABLE = False
    mistune = MagicMock()

# Try to import the functions to test
try:
    from common.repository_utils import create_markdown_parser, load_markdown_file
    REPO_UTILS_AVAILABLE = True
except ImportError:
    REPO_UTILS_AVAILABLE = False

@unittest.skipIf(not MISTUNE_AVAILABLE or not REPO_UTILS_AVAILABLE, 
                "mistune or repository_utils not available")
class TestMarkdownParsing(unittest.TestCase):
    """Test cases for Markdown parsing functionality."""
    
    def setUp(self):
        """Set up a parser and test data."""
        self.parser = create_markdown_parser()
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Create a temporary test file if it doesn't exist
        self.test_file = os.path.join(self.test_dir, "test_markdown.md")
        if not os.path.exists(self.test_file):
            with open(self.test_file, 'w', encoding='utf-8') as f:
                f.write(self.get_test_markdown())
    
    def tearDown(self):
        """Clean up temporary test files."""
        if os.path.exists(self.test_file):
            try:
                os.remove(self.test_file)
            except:
                pass
    
    def get_test_markdown(self):
        """Generate test markdown content with various code block formats."""
        return """# Test Markdown File

This is a test markdown file with various code block formats.

## Regular Code Block

```
This is a regular code block
with no language specified
```

## Python Code Block

```python
def hello_world():
    print("Hello, world!")
```

## JavaScript Code Block with Info String

```javascript:test.js
function hello() {
    console.log("Hello, world!");
}
```

## Python Code Block with Options

```python {lineNumbers=true}
import os
import sys

def main():
    print("Hello, world!")

if __name__ == "__main__":
    main()
```

## Ruby Code Block with Additional Info

```ruby filename=example.rb
def hello
  puts "Hello, world!"
end
```

## PHP Code Block with Complex Info

```php showLineNumbers title="Example File" {3-5} :test.php
<?php
function hello() {
    echo "Hello, world!";
}
?>
```
"""
    
    def test_parse_markdown_with_code_blocks(self):
        """Test parsing markdown with various code block formats."""
        markdown = self.get_test_markdown()
        html = self.parser(markdown)
        
        # Check that the HTML was generated without errors
        self.assertIsNotNone(html)
        self.assertIn("<h1>", html)
        self.assertIn("<pre><code>", html)
        self.assertIn("Hello, world!", html)
        
        # Count the number of code blocks to make sure all were rendered
        code_block_count = html.count("<pre><code")
        self.assertEqual(code_block_count, 6, f"Expected 6 code blocks, found {code_block_count}")
    
    def test_load_markdown_file(self):
        """Test loading and parsing a markdown file with code blocks."""
        content, html = load_markdown_file(self.test_file, self.parser)
        
        # Check that both content and HTML were returned
        self.assertIsNotNone(content)
        self.assertIsNotNone(html)
        
        # Check that the content matches what we expect
        self.assertIn("# Test Markdown File", content)
        self.assertIn("```python", content)
        
        # Check that the HTML was generated without errors
        self.assertIn("<h1>", html)
        self.assertIn("<pre><code", html)
        
        # Count the number of code blocks to make sure all were rendered
        code_block_count = html.count("<pre><code")
        self.assertEqual(code_block_count, 6, f"Expected 6 code blocks, found {code_block_count}")
    
    def test_different_info_string_formats(self):
        """Test parsing markdown with different code block info string formats."""
        test_cases = [
            "```python\nprint('hello')\n```",
            "```python:test.py\nprint('hello')\n```",
            "```python {lineNumbers=true}\nprint('hello')\n```",
            "```python title='Example'\nprint('hello')\n```",
            "```python showLineNumbers {1-5}\nprint('hello')\n```",
        ]
        
        for tc in test_cases:
            html = self.parser(tc)
            self.assertIsNotNone(html)
            self.assertIn("<pre><code", html)
            self.assertIn("hello", html)
    
    @patch('common.repository_utils.mistune.create_markdown')
    def test_create_markdown_parser_configures_renderer(self, mock_create_markdown):
        """Test that create_markdown_parser correctly configures the renderer."""
        # Reset the mock and call the function
        mock_create_markdown.reset_mock()
        create_markdown_parser()
        
        # Check that create_markdown was called with expected arguments
        mock_create_markdown.assert_called_once()
        
        # Get the renderer argument
        args, kwargs = mock_create_markdown.call_args
        self.assertIn('renderer', kwargs)
        
        # Ensure renderer is an instance of HighlightRenderer
        from common.repository_utils import HighlightRenderer
        self.assertIsInstance(kwargs['renderer'], HighlightRenderer)

if __name__ == "__main__":
    unittest.main() 