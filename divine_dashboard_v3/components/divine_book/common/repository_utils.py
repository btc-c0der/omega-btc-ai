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
Repository Utilities

Shared utilities for working with the repository files, especially 
Markdown documents. This module is used by both the Divine Book Dashboard
and Divine Book Browser components.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
import io
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html
from collections import defaultdict

try:
    from rich.tree import Tree
    from rich.console import Console
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Find the repository root directory
def find_repo_root() -> Optional[Path]:
    """Find the repository root directory by looking for .git"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    current_path = Path(current_dir)
    
    # Go up to three parent directories to find repo root
    for _ in range(4):  # Check current dir and up to 3 parents
        if (current_path / ".git").exists():
            return current_path
        
        # Stop if we're at the filesystem root
        if current_path == current_path.parent:
            break
            
        current_path = current_path.parent
    
    # If we can't find .git, use a fallback approach
    current_path = Path(current_dir).parent.parent.parent.parent
    
    return current_path

# Find repo root
REPO_ROOT = find_repo_root()

# Custom Markdown renderer with syntax highlighting
class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, lang=None, info=None):
        """Render a block of code with syntax highlighting.
        
        Args:
            code: The code content to render
            lang: The language of the code (optional)
            info: Additional info for the code block (added in newer mistune versions)
        """
        if lang:
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

# Create Markdown parser
def create_markdown_parser():
    """Create and return a Markdown parser with syntax highlighting"""
    return mistune.create_markdown(
        renderer=HighlightRenderer(),
        plugins=['table', 'url', 'strikethrough', 'footnotes', 'task_lists']
    )

def collect_markdown_files() -> Dict[str, str]:
    """
    Collect all Markdown files from the repository.
    
    Returns:
        Dictionary mapping display names to file paths
    """
    md_files = {}
    ignored_dirs = ["node_modules", ".git", "__pycache__", "venv", "divine_venv"]
    
    # Return empty if repo_root is None
    if REPO_ROOT is None:
        return md_files
    
    # Walk through the repository directory
    for root, dirs, files in os.walk(REPO_ROOT):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                
                # Create a display name from the path
                rel_path = os.path.relpath(file_path, REPO_ROOT)
                display_name = f"{os.path.dirname(rel_path)}/{os.path.basename(rel_path)}"
                
                # Store the file path with its display name
                md_files[display_name] = file_path
    
    return md_files

def build_file_tree(md_files: Dict[str, str]) -> Dict[str, any]:
    """
    Build a hierarchical tree structure of all Markdown files.
    
    Args:
        md_files: Dictionary mapping display names to file paths
        
    Returns:
        Dictionary representing the file tree
    """
    tree = defaultdict(dict)
    
    # Build the tree structure
    for path in md_files.keys():
        parts = path.split('/')
        current = tree
        
        # Navigate through directories
        for i, part in enumerate(parts):
            if i == len(parts) - 1:  # File
                current[part] = path  # Store the display path, not the file path
            else:  # Directory
                if part not in current:
                    current[part] = defaultdict(dict)
                current = current[part]
    
    return tree

def render_file_tree_html(md_files: Dict[str, str]) -> str:
    """
    Render the file tree structure as HTML for display in the UI.
    
    Args:
        md_files: Dictionary mapping display names to file paths
        
    Returns:
        HTML string representation of the file tree
    """
    if not RICH_AVAILABLE:
        return "<div>File tree visualization requires 'rich' package.</div>"
    
    # Build the file tree
    file_tree = build_file_tree(md_files)
    
    # Use rich to create a pretty tree
    console = Console(file=io.StringIO(), highlight=False)
    tree = Tree(f"📚 Repository Markdown Files ({len(md_files)} files)")
    
    # Recursively add branches to the tree
    def add_to_tree(node, data):
        for key, value in sorted(data.items()):
            if isinstance(value, (dict, defaultdict)):
                # This is a directory
                branch = node.add(f"📁 {key}")
                add_to_tree(branch, value)
            else:
                # This is a file - value is the display path
                display_path = value
                node.add(f"📄 {key} [dim]({display_path})[/dim]")
    
    add_to_tree(tree, file_tree)
    
    # Print the tree to the string buffer
    console.print(tree)
    
    # Get the output and convert to HTML
    tree_output = console.file.getvalue()
    
    # Convert to HTML with <pre> and styling
    html_output = f"""
    <style>
        .file-tree {{
            background-color: #1e1e2e;
            color: #cdd6f4;
            padding: 1.2rem;
            border-radius: 8px;
            font-family: 'JetBrains Mono', 'Fira Code', 'Menlo', 'Monaco', 'Courier New', monospace;
            overflow-y: auto;
            height: 480px;  /* Set height explicitly */
            max-height: 600px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
            font-size: 14px;
            line-height: 1.4;
        }}
        
        .file-tree pre {{
            margin: 0;
            padding: 0;
            background: transparent;
            border: none;
            color: inherit;
            font-family: inherit;
        }}
        
        /* Highlight directories with bolder color */
        .file-tree pre span:has(span:contains("📁")) {{
            color: #b4befe;
            font-weight: bold;
        }}
        
        /* Make file names slightly dimmer */
        .file-tree pre span:has(span:contains("📄")) {{
            color: #a6adc8;
        }}
    </style>
    <div class="file-tree">
        <pre>{tree_output}</pre>
    </div>
    """
    
    return html_output

def load_markdown_file(file_path: str, markdown_parser=None) -> tuple[str, str]:
    """
    Load the content of a Markdown file and render it to HTML.
    
    Args:
        file_path: Path to the markdown file
        markdown_parser: Optional parser to use for rendering
        
    Returns:
        Tuple of (raw_markdown, rendered_html)
    """
    if markdown_parser is None:
        markdown_parser = create_markdown_parser()
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Render markdown to HTML
            html_content = markdown_parser(content)
            
            return content, html_content
    except Exception as e:
        error_msg = f"Error loading file: {str(e)}"
        return error_msg, f"<div class='error'>{error_msg}</div>" 