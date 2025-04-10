#!/usr/bin/env python3
# ✨ GBU2™ License Notice - Consciousness Level 9 🧬
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
Markdown Renderer Module

Provides functions for rendering markdown content and extracting metadata
with support for special divine extensions and syntax highlighting.
"""

import re
import yaml
import html
from typing import Dict, Any, List, Optional, Tuple

# Try to import markdown/highlighting packages
try:
    import markdown
    import pygments
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

def render_markdown(content: str) -> str:
    """
    Render markdown content to HTML with divine extensions.
    
    Args:
        content: Markdown content to render
        
    Returns:
        HTML rendered content
    """
    # If markdown package is available, use it
    if MARKDOWN_AVAILABLE:
        # Apply divine extensions
        content = apply_divine_extensions(content)
        
        # Custom code block handling for syntax highlighting
        content = process_code_blocks(content)
        
        # Render with Python Markdown
        html_content = markdown.markdown(
            content,
            extensions=[
                'extra',               # Tables, footnotes, etc.
                'codehilite',          # Syntax highlighting
                'nl2br',               # Convert newlines to <br>
                'sane_lists',          # Better list handling
                'smarty',              # Smart quotes
                'toc'                  # Table of contents
            ]
        )
        
        return html_content
    else:
        # Fallback to basic markdown conversion
        return basic_markdown_to_html(content)

def extract_metadata(content: str) -> Dict[str, Any]:
    """
    Extract YAML metadata from the beginning of markdown content.
    
    Args:
        content: Markdown content with optional YAML frontmatter
        
    Returns:
        Dictionary of metadata values
    """
    metadata = {}
    
    # Check for YAML frontmatter
    yaml_match = re.match(r'---\s+(.*?)\s+---', content, re.DOTALL)
    if yaml_match:
        yaml_content = yaml_match.group(1)
        try:
            metadata = yaml.safe_load(yaml_content)
        except Exception:
            pass
    
    # Try to extract metadata from markdown headers
    if not metadata:
        # Try to get title from first heading
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            metadata['title'] = title_match.group(1).strip()
        
        # Try to extract category from tags
        tags_match = re.search(r'(?:tags|categories):\s*\[([^\]]+)\]', content, re.IGNORECASE)
        if tags_match:
            tag_list = [tag.strip() for tag in tags_match.group(1).split(',')]
            if tag_list:
                metadata['category'] = tag_list[0].upper()
        
        # Try to extract description from first paragraph
        desc_match = re.search(r'^(?!#)(.+?)(?:\n\n|\n*$)', content.split('---\n')[-1].strip(), re.DOTALL)
        if desc_match:
            desc = desc_match.group(1).strip()
            # Limit description length
            if len(desc) > 150:
                desc = desc[:147] + '...'
            metadata['description'] = desc
    
    # Ensure category is always present
    if 'category' not in metadata:
        # Try to infer category from content
        categories = [
            ("QUANTUM", ["quantum", "qubits", "superposition", "entanglement"]),
            ("DIVINE", ["divine", "sacred", "spiritual", "consciousness"]),
            ("COSMIC", ["cosmic", "universe", "galaxies", "celestial"]),
            ("TECHNICAL", ["technical", "code", "algorithm", "function"]),
            ("TRADING", ["trading", "market", "crypto", "bitcoin"]),
            ("DOCUMENTATION", ["documentation", "guide", "manual", "reference"]),
            ("SOURCE", ["source code", "implementation", "class", "method"]),
            ("TESTING", ["test", "testing", "validation", "verification"])
        ]
        
        content_lower = content.lower()
        for cat_name, keywords in categories:
            if any(keyword in content_lower for keyword in keywords):
                metadata['category'] = cat_name
                break
        
        # Default category if still not found
        if 'category' not in metadata:
            metadata['category'] = "UNCATEGORIZED"
    
    return metadata

def apply_divine_extensions(content: str) -> str:
    """Apply divine markdown extensions to content."""
    # Extension 1: Divine blockquotes with cosmic symbols
    content = re.sub(
        r'(?m)^>\s*\*\*DIVINE\*\*:\s*(.+)$',
        r'<div class="divine-quote">🔮 \1</div>',
        content
    )
    
    # Extension 2: Quantum highlighted text
    content = re.sub(
        r'==([^=]+)==',
        r'<mark class="quantum-highlight">\1</mark>',
        content
    )
    
    # Extension 3: Sacred tags
    content = re.sub(
        r'#\[([\w\s]+)\]',
        r'<span class="sacred-tag">#\1</span>',
        content
    )
    
    # Extension 4: Energy indicators
    content = re.sub(
        r'~{([1-5])}\s*(.+?)~',
        lambda m: f'<span class="energy-level energy-level-{m.group(1)}">{m.group(2)}</span>',
        content
    )
    
    return content

def process_code_blocks(content: str) -> str:
    """Process code blocks for syntax highlighting."""
    if not MARKDOWN_AVAILABLE:
        return content
    
    def replace_code_block(match):
        language = match.group(1) or 'text'
        code = match.group(2)
        
        try:
            lexer = get_lexer_by_name(language, stripall=True)
            formatter = HtmlFormatter(linenos=False, cssclass="highlight")
            highlighted = pygments.highlight(code, lexer, formatter)
            return highlighted
        except Exception:
            # Fallback if lexer not found
            return f'<pre><code class="language-{language}">{html.escape(code)}</code></pre>'
    
    # Replace code blocks with syntax highlighted versions
    content = re.sub(
        r'```(\w+)?\n(.*?)```',
        replace_code_block,
        content,
        flags=re.DOTALL
    )
    
    return content

def basic_markdown_to_html(content: str) -> str:
    """
    Basic markdown to HTML conversion for when the markdown package is not available.
    This is a simplified implementation supporting only basic markdown features.
    """
    # Escape HTML
    content = html.escape(content)
    
    # Headers
    content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', content, flags=re.MULTILINE)
    content = re.sub(r'^##### (.+)$', r'<h5>\1</h5>', content, flags=re.MULTILINE)
    
    # Bold and Italic
    content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
    content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)
    
    # Lists
    content = re.sub(r'(?m)^- (.+)$', r'<ul><li>\1</li></ul>', content)
    
    # Fix adjacent list items
    content = re.sub(r'</ul>\s*<ul>', '', content)
    
    # Links
    content = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', content)
    
    # Code blocks
    content = re.sub(r'```(.+?)```', r'<pre><code>\1</code></pre>', content, flags=re.DOTALL)
    content = re.sub(r'`(.+?)`', r'<code>\1</code>', content)
    
    # Paragraphs
    content = re.sub(r'(?<!\n)\n(?!\n)(?!<\/?\w+>)', '<br>', content)
    content = re.sub(r'\n\s*\n', '</p><p>', content)
    content = f'<p>{content}</p>'
    
    # Fix extra paragraph tags
    content = re.sub(r'<p>(<h[1-6]>)', r'\1', content)
    content = re.sub(r'(</h[1-6]>)</p>', r'\1', content)
    
    return content 