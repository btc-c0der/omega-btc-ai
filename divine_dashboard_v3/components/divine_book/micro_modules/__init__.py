"""
Divine Book Browser Micro Modules

This package contains the micro modules used by the Divine Book Browser component.
These modules provide document analysis, quantum indexing, markdown rendering,
and sacred pattern detection capabilities.

Modules:
- document_analyzer: Analyzes document structure and content
- quantum_indexer: Provides quantum-enhanced document indexing and search
- markdown_renderer: Renders markdown content with advanced formatting
- resonance_detector: Detects sacred patterns and calculates quantum resonance
"""

from .document_analyzer import analyze_document, get_document_stats
from .quantum_indexer import index_documents, search_documents
from .markdown_renderer import render_markdown, extract_metadata
from .resonance_detector import calculate_resonance, find_sacred_patterns

__all__ = [
    'analyze_document',
    'get_document_stats',
    'index_documents',
    'search_documents',
    'render_markdown',
    'extract_metadata',
    'calculate_resonance',
    'find_sacred_patterns'
] 