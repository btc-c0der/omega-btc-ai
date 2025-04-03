#!/usr/bin/env python3

"""
Tests that verify the quality of markdown documentation for BitgetPositionAnalyzerB0t.

This test suite ensures:
1. Documentation follows markdown best practices
2. Required sections are present
3. Code examples are properly formatted
4. Headers follow a logical structure
"""

import re
import pytest
from pathlib import Path
from bs4 import BeautifulSoup

try:
    import markdown
    MARKDOWN_PARSER_AVAILABLE = True
except ImportError:
    MARKDOWN_PARSER_AVAILABLE = False


@pytest.mark.usefixtures("doc_markdown_content")
class TestMarkdownQuality:
    """Test suite for verifying documentation quality."""
    
    @pytest.fixture(autouse=True)
    def setup_markdown_parser(self, doc_markdown_content):
        """Setup the markdown parser for each test."""
        self.skip_if_no_doc_content(doc_markdown_content)
        
        if not MARKDOWN_PARSER_AVAILABLE:
            pytest.skip("Markdown parser not available. Install with: pip install markdown")
            
        # Parse the markdown to HTML
        self.html = markdown.markdown(doc_markdown_content, extensions=['tables', 'fenced_code'])
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.markdown_content = doc_markdown_content
    
    def skip_if_no_doc_content(self, doc_markdown_content):
        """Skip the test if documentation content is not available."""
        if doc_markdown_content is None:
            pytest.skip("Documentation file not found")
    
    def test_required_sections_present(self):
        """Test that all required sections are present in the documentation."""
        # Define required sections and patterns to identify them
        required_sections = {
            'Title': r'^#\s+.*?BitgetPositionAnalyzerB0t',
            'Overview': r'##\s+Overview|Introduction',
            'Installation': r'##\s+Installation|Setup',
            'Usage': r'##\s+Usage|Getting Started',
            'API': r'##\s+API|Methods',
            'Configuration': r'##\s+Configuration'
        }
        
        # Check each required section
        for section, pattern in required_sections.items():
            match = re.search(pattern, self.markdown_content, re.MULTILINE)
            assert match is not None, f"Documentation is missing required '{section}' section"
    
    def test_header_structure(self):
        """Test that headers follow a logical structure."""
        # Get all headers
        headers = self.soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        # Check that there is at most one h1 header
        h1_headers = self.soup.find_all('h1')
        assert len(h1_headers) <= 1, "Documentation should have at most one H1 header"
        
        # Check header nesting - headers should not skip levels (e.g., h2 -> h4)
        current_level = 1
        for i, header in enumerate(headers):
            level = int(header.name[1])
            
            # Allow h1 -> h2, but not larger jumps
            if i > 0:
                prev_level = int(headers[i-1].name[1])
                assert level <= prev_level + 1, f"Header '{header.get_text()}' jumps more than one level from previous header"
            
            current_level = level
    
    def test_code_blocks(self):
        """Test that code blocks are properly formatted."""
        # Find all code blocks in the markdown
        code_blocks = re.findall(r'```(\w*)\n(.*?)```', self.markdown_content, re.DOTALL)
        
        for lang, code in code_blocks:
            # Check that code blocks specify a language
            assert lang.strip() != "", "Code blocks should specify a language (e.g., ```python instead of ```)"
            
            # For Python code blocks, perform additional checks
            if lang.lower() == 'python':
                # Check that Python code blocks are not empty
                assert code.strip() != "", "Python code blocks should not be empty"
                
                # Check that Python code blocks don't have excessive blank lines
                lines = code.split('\n')
                blank_line_count = sum(1 for line in lines if line.strip() == '')
                code_line_count = len(lines) - blank_line_count
                
                # Allow at most 30% blank lines in code blocks with >5 lines
                if code_line_count > 5:
                    assert blank_line_count / len(lines) <= 0.3, "Python code blocks contain too many blank lines"
    
    def test_links(self):
        """Test that links in the documentation are valid."""
        # Find all links in the markdown
        links = re.findall(r'\[([^\]]*)\]\(([^)]*)\)', self.markdown_content)
        
        for text, url in links:
            # Check that link text is not empty
            assert text.strip() != "", "Links should have descriptive text"
            
            # Check that URL is not empty and not just a #
            assert url.strip() != "", "Links should have a URL"
            assert url.strip() != "#", "Links should not be empty anchors (#)"
            
            # For relative links (not starting with http), check for spaces
            if not url.startswith('http'):
                assert ' ' not in url, f"Relative link '{url}' contains spaces, which may cause issues"
    
    def test_images(self):
        """Test that images in the documentation have alt text."""
        # Find all images in the markdown
        images = re.findall(r'!\[([^\]]*)\]\(([^)]*)\)', self.markdown_content)
        
        for alt_text, url in images:
            # Check that image has alt text
            assert alt_text.strip() != "", f"Image {url} should have alt text for accessibility"
            
            # Check that image URL is not empty
            assert url.strip() != "", "Image reference should have a URL"
    
    def test_tables(self):
        """Test that tables in the documentation are well-formatted."""
        # Find all tables in the HTML
        tables = self.soup.find_all('table')
        
        for table in tables:
            # Check that tables have headers
            headers = table.find_all('th')
            assert len(headers) > 0, "Tables should have header cells"
            
            # Check that header cells are not empty
            for header in headers:
                header_text = header.get_text().strip() if header.get_text() else ""
                assert header_text != "", "Table header cells should not be empty"
            
            # Check that tables have at least two columns
            header_count = len(headers)
            assert header_count >= 2, "Tables should have at least two columns for better readability"
    
    def test_spelling_grammar(self):
        """Test for common spelling and grammar issues in the documentation."""
        # List of common spelling/grammar issues to check for
        common_issues = [
            (r'\b(its)\s+(\w+ing)', "Check use of 'its' with a gerund"),
            (r'\b(their)\s+(\w+ing)', "Check use of 'their' with a gerund"),
            (r'\b(thier)\b', "Misspelling of 'their'"),
            (r'\b(recieve)\b', "Misspelling of 'receive'"),
            (r'\b(seperate)\b', "Misspelling of 'separate'"),
            (r'\b(then)\s+(a|an)\b', "Possible confusion of 'then' vs 'than'"),
            (r'\ba\s+([aeiou]\w+)', "Use 'an' instead of 'a' before vowels")
        ]
        
        for pattern, message in common_issues:
            matches = re.findall(pattern, self.markdown_content, re.IGNORECASE)
            assert len(matches) == 0, f"Possible grammar/spelling issue: {message}"
    
    def test_api_method_documentation(self, mock_bitget_position_analyzer_bot):
        """Test for proper documentation of API methods."""
        bot_class = mock_bitget_position_analyzer_bot
        
        # Get public methods of the bot class
        methods = [(name, method) for name, method in self._get_public_methods(bot_class)
                   if not name.startswith('_') or name == '__init__']
        
        # Define key methods that should be well-documented
        key_methods = ['__init__', 'get_positions', 'analyze_position', 'calculate_harmony_score']
        
        for method_name in key_methods:
            # Check if method has a section in the documentation
            section_pattern = rf'##\s+.*?{method_name}.*?\n'
            section_match = re.search(section_pattern, self.markdown_content, re.MULTILINE)
            
            assert section_match is not None, f"Key method '{method_name}' should have a dedicated section"
            
            # Find the section content (text until the next heading)
            section_start = section_match.end()
            next_heading = re.search(r'\n##\s+', self.markdown_content[section_start:])
            
            if next_heading:
                section_content = self.markdown_content[section_start:section_start + next_heading.start()]
            else:
                section_content = self.markdown_content[section_start:]
            
            # Check for parameter descriptions
            param_pattern = r'- `([^`]+)`\s*:\s*'
            param_matches = re.findall(param_pattern, section_content)
            
            # For key methods (except __init__), check for return value description
            if method_name != '__init__':
                assert 'Returns' in section_content, f"Method '{method_name}' should document its return value"
            
            # Check for example code
            assert '```python' in section_content, f"Method '{method_name}' should include example code"
    
    def _get_public_methods(self, cls):
        """Get all public methods of a class."""
        import inspect
        return inspect.getmembers(cls, predicate=inspect.isfunction)


if __name__ == "__main__":
    pytest.main() 