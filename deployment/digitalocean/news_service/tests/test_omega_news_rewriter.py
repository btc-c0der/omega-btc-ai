#!/usr/bin/env python3
"""
OMEGA BTC AI - News Divine Rewriter
==================================

This script transforms news narratives according to Omega divine principles,
promoting harmony, unity, and global well-being through resonant reframing.

Copyright (c) 2025 OMEGA-BTC-AI - Licensed under the GPU License
"""

import os
import sys
import argparse
import json
import re
import random
from datetime import datetime
import numpy as np
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

# Ensure the package is in the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
src_path = os.path.join(project_root, 'deployment/digitalocean/news_service/src')
sys.path.insert(0, src_path)

# Parse command line arguments
parser = argparse.ArgumentParser(description="Omega News Divine Rewriter")
parser.add_argument("--nodatabase", action="store_true", help="Run without database connection")
parser.add_argument("--source", type=str, default="coindesk", help="News source to rewrite")
parser.add_argument("--limit", type=int, default=5, help="Number of news items to rewrite")
parser.add_argument("--rewrite-mode", type=str, default="divine", 
                    choices=["divine", "harmony", "prosperity", "unity", "transcendent", "coyote", "whale"],
                    help="Rewriting modality to apply")
parser.add_argument("--output", type=str, default="terminal", 
                    choices=["terminal", "json", "markdown"],
                    help="Output format for rewritten news")
parser.add_argument("--save", action="store_true", help="Save rewritten news to file")
args = parser.parse_args()

console = Console()

# Import the OmegaNewsRewriter class
try:
    from omega_ai.news_rewriter import OmegaNewsRewriter
    news_rewriter_imported = True
except ImportError as e:
    console.print(f"[yellow]⚠️ Could not import OmegaNewsRewriter: {e}. Using sample news instead.[/]")
    news_rewriter_imported = False

def run_divine_rewriter():
    """Run the divine news rewriter."""
    console.print(Panel(
        "OMEGA BTC AI - News Divine Rewriter\nTransforming news narratives through Omega divine principles",
        border_style="cyan"
    ))
    
    # Display transformation paradigm
    console.print(Panel(
        f"Active Divine Principle: {args.rewrite_mode.title()}\n"
        f"Principle Essence: {OmegaNewsRewriter.DIVINE_PRINCIPLES.get(args.rewrite_mode, 'Divine transformation')}",
        title="✨ Transformation Paradigm",
        border_style="magenta"
    ))
    
    # Create divine rewriter
    rewriter = OmegaNewsRewriter(data_dir="./data", rewrite_mode=args.rewrite_mode)
    
    # Set output format
    rewriter.set_output_format(args.output)
    
    # Fetch news
    news_entries = rewriter.fetch_news(source=args.source, limit=args.limit)
    
    # Apply divine transformations
    rewriter.process_all_news()
    
    # Display transformations
    if args.output == "terminal":
        if not rewriter.rewritten_entries:
            console.print("[yellow]No rewritten entries to display[/]")
            return
        
        # Display each transformation
        for original, transformed in zip(rewriter.news_entries, rewriter.rewritten_entries):
            # Original news panel
            console.print(Panel(
                f"Title: {original.get('title', 'No title')}\n\n"
                f"Content: {original.get('content', original.get('description', 'No content'))}\n\n"
                f"Sentiment: {original.get('sentiment_score', 0):.2f}",
                title=f"📰 Original News from {original.get('source', 'Unknown')}",
                border_style="blue"
            ))
            
            # Transformed news panel
            console.print(Panel(
                f"Title: {transformed.get('transformed_title', 'No title')}\n\n"
                f"Content: {transformed.get('transformed_content', 'No content')}\n\n"
                f"Divine Principle: {transformed.get('divine_principle', 'Unknown').title()}\n"
                f"Sentiment: {transformed.get('new_sentiment', 0):.2f} (Shift: {transformed.get('sentiment_shift', 0):+.2f})",
                title=f"✨ Divine Transformation ({args.rewrite_mode.title()} Mode)",
                border_style="green"
            ))
            
            # Add space between entries
            console.print()
    
    elif args.output == "json":
        # Display as JSON
        json_output = rewriter.display_transformations(format="json")
        if json_output:
            console.print_json(json_output)
    
    elif args.output == "markdown":
        # Display as Markdown
        markdown_output = rewriter.display_transformations(format="markdown")
        if markdown_output:
            console.print(Markdown(markdown_output))
    
    # Save if requested
    if args.save:
        filepath = rewriter.save_transformations()
        if filepath:
            console.print(f"[green]✅ Divine transformations saved to {filepath}[/]")

if __name__ == "__main__":
    run_divine_rewriter() 