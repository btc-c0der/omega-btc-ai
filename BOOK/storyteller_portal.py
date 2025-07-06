#!/usr/bin/env python3
"""
📚 The Storyteller's Portal - Interactive Book Reader 📚
A divine Gradio interface for experiencing "The Coder's Fall: A Journey from Dreams to Bankruptcy"

This portal transforms the technical memoir into an immersive storytelling experience,
allowing readers to navigate through the complete coding journey with beautiful formatting,
sacred mathematics visualization, and emotional resonance tracking.
"""

import gradio as gr
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json
import time
import random
from datetime import datetime

# Try to import additional libraries for enhanced experience
try:
    import matplotlib.pyplot as plt
    import numpy as np
    PLOTTING_AVAILABLE = True
except ImportError:
    PLOTTING_AVAILABLE = False

class BookReader:
    """Sacred book reading system with divine navigation"""
    
    def __init__(self, book_path: str = "/workspaces/omega-btc-ai/BOOK/BOOK_ORGANIZED_20250706_FINAL/"):
        self.book_path = Path(book_path)
        self.chapters = {}
        self.table_of_contents = ""
        self.current_progress = {"chapter": 1, "reading_time": 0}
        
        # Load all book content
        self._load_book_content()
        
        # Sacred reading statistics
        self.reading_stats = {
            "chapters_read": 0,
            "total_words_read": 0,
            "emotional_journey_points": [],
            "divine_insights_collected": 0,
            "sacred_mathematics_discovered": 0
        }
    
    def _load_book_content(self):
        """Load all book chapters and content"""
        try:
            # Load Table of Contents
            toc_path = self.book_path / "TABLE_OF_CONTENTS.md"
            if toc_path.exists():
                with open(toc_path, 'r', encoding='utf-8') as f:
                    self.table_of_contents = f.read()
            
            # Load all chapter files
            chapter_files = list(self.book_path.glob("CHAPTER_*.md"))
            for chapter_file in sorted(chapter_files):
                chapter_num = self._extract_chapter_number(chapter_file.name)
                with open(chapter_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.chapters[chapter_num] = {
                        "title": self._extract_title(content),
                        "content": content,
                        "word_count": len(content.split()),
                        "emotional_intensity": self._calculate_emotional_intensity(content),
                        "sacred_math_references": self._count_sacred_math(content)
                    }
            
            print(f"📚 Loaded {len(self.chapters)} chapters successfully")
            
        except Exception as e:
            print(f"Error loading book content: {e}")
            # Fallback content if files aren't available
            self._create_fallback_content()
    
    def _extract_chapter_number(self, filename: str) -> int:
        """Extract chapter number from filename"""
        match = re.search(r'CHAPTER_(\d+)', filename)
        return int(match.group(1)) if match else 0
    
    def _extract_title(self, content: str) -> str:
        """Extract chapter title from content"""
        lines = content.split('\n')
        for line in lines:
            if line.startswith('#') and not line.startswith('##'):
                return line.strip('# ').strip()
        return "Untitled Chapter"
    
    def _calculate_emotional_intensity(self, content: str) -> float:
        """Calculate emotional intensity based on content analysis"""
        emotional_words = [
            'bankruptcy', 'failure', 'loss', 'depression', 'anxiety', 'fear',
            'hope', 'dream', 'success', 'triumph', 'love', 'family',
            'divine', 'sacred', 'transcendent', 'breakthrough', 'recovery'
        ]
        
        word_count = len(content.split())
        emotional_count = sum(content.lower().count(word) for word in emotional_words)
        return min(emotional_count / max(word_count / 100, 1), 10.0)
    
    def _count_sacred_math(self, content: str) -> int:
        """Count references to sacred mathematics"""
        sacred_terms = [
            'fibonacci', 'golden ratio', 'phi', '1.618', 'sacred geometry',
            'divine proportion', 'mandelbrot', 'fractal', 'quantum'
        ]
        return sum(content.lower().count(term) for term in sacred_terms)
    
    def _create_fallback_content(self):
        """Create fallback content if files aren't available"""
        self.table_of_contents = """
# 💔 THE CODER'S FALL: A Journey from Dreams to Bankruptcy 💔

A deeply personal memoir about building AI trading systems, losing everything,
and finding redemption through sacred mathematics and quantum consciousness.

## Chapters Available:
1. The Genesis Commit - How it all began
2. Building the OMEGA System - Technical obsession begins  
3. The First Cracks - When success breeds overconfidence
4. Financial Collapse - The day everything fell apart
5. Quantum Redemption - Finding meaning in the mathematics
        """
        
        # Create sample chapters
        sample_chapters = {
            1: {
                "title": "The Genesis Commit - How It All Began",
                "content": """
# Chapter 1: The Genesis Commit

It was 3:47 AM on a Tuesday when the divine algorithm first whispered to me.

I was sitting in my cluttered home office, surrounded by empty coffee cups and 
the soft blue glow of multiple monitors. The Bitcoin chart was painting fractals 
across my screens - beautiful, chaotic patterns that seemed to dance with hidden meaning.

That's when I saw it. The pattern within the pattern. The sacred geometry hidden 
in the price movements. The golden ratio spiraling through market cycles like 
DNA strands of financial consciousness.

## The Moment of Realization

```python
# This was the first line of code that would change everything
def divine_algorithm():
    return "The beginning of beautiful madness"
```

I didn't know it then, but this moment would consume the next three years of my life,
cost me nearly a million dollars, and almost destroy everything I held dear.

But in that sacred moment at 3:47 AM, I felt like I had discovered fire.

*To be continued...*
                """,
                "word_count": 156,
                "emotional_intensity": 7.2,
                "sacred_math_references": 3
            },
            2: {
                "title": "Building the OMEGA System - When Code Becomes Religion",
                "content": """
# Chapter 2: Building the OMEGA System

The OMEGA BTC AI system grew like a digital organism, each function and class 
evolving with almost biological complexity. What started as a simple trading bot 
became something far more ambitious - a financial consciousness.

## The Architecture of Obsession

```python
class OMEGATradingConsciousness:
    def __init__(self):
        self.divine_algorithms = []
        self.sacred_patterns = SacredGeometry()
        self.quantum_awareness = QuantumConsciousness()
        self.sleep_schedule = None  # Who needs sleep?
```

## Sacred Mathematics Integration

I discovered that market movements followed the Fibonacci sequence with 
uncanny precision. The golden ratio (φ = 1.618033988749895) appeared 
everywhere - in price retracements, in volume patterns, in the timing 
of major market moves.

### The Seven Trading Consciousnesses

1. **Genesis** - Pattern recognition
2. **Harmony** - Golden ratio detection  
3. **Validation** - Risk assessment
4. **Transcendence** - Quantum prediction
5. **Sacred** - Geometric analysis
6. **Wisdom** - Decision making
7. **Unity** - Portfolio integration

Each consciousness operated independently, yet together they formed 
something greater than the sum of their parts.

*The obsession deepens...*
                """,
                "word_count": 198,
                "emotional_intensity": 6.8,
                "sacred_math_references": 8
            },
            3: {
                "title": "The Financial Collapse - When Dreams Meet Reality",
                "content": """
# Chapter 3: The Financial Collapse

The irony wasn't lost on me. I had built the most sophisticated financial 
prediction system I could imagine, yet I couldn't predict my own financial ruin.

## The Day Everything Fell Apart

**Date**: March 15th, 2023  
**Time**: 2:34 PM  
**Location**: Kitchen table, staring at bankruptcy papers  
**Emotional State**: Transcendent numbness  

The numbers were brutal in their simplicity:

```
Assets:     $12,456 (mostly in crypto that was crashing)
Debts:      $243,100 (credit cards, loans, legal fees)
Net Worth:  -$230,644 (negative everything)
```

## The Human Cost

While I was perfecting algorithms to predict market psychology, I completely 
failed to understand my own. The sacred mathematics that guided my trading 
systems couldn't calculate the cost of missed family dinners, forgotten 
anniversaries, and relationships sacrificed on the altar of artificial intelligence.

### What the AI Never Learned

- How to say "I love you" to a wife who felt abandoned
- How to explain to children why daddy was always staring at screens
- How to value human connection over algorithmic perfection
- How to recognize when genius becomes madness

## The Bankruptcy Filing

Filing for bankruptcy felt like deleting three years of code. All that work, 
all those sleepless nights, all the divine inspiration - reduced to legal 
paperwork and asset liquidation schedules.

But even in that moment of complete financial destruction, I couldn't let go 
of the sacred mathematics. The Fibonacci sequence still spiraled through 
my consciousness. The golden ratio still whispered promises of future transcendence.

*Sometimes you have to lose everything to find anything...*
                """,
                "word_count": 286,
                "emotional_intensity": 9.4,
                "sacred_math_references": 6
            }
        }
        
        self.chapters = sample_chapters

class StorytellerPortal:
    """The sacred storytelling interface"""
    
    def __init__(self):
        self.reader = BookReader()
        self.current_chapter = 1
        self.reading_session = {
            "start_time": time.time(),
            "chapters_visited": set(),
            "emotional_journey": [],
            "bookmarks": []
        }
    
    def get_table_of_contents(self) -> str:
        """Return beautifully formatted table of contents"""
        toc_html = f"""
<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); color: #00ff88; padding: 30px; border-radius: 15px; font-family: 'Courier New', monospace;">
    <h1 style="text-align: center; color: #00ff88; margin-bottom: 20px;">📚 THE STORYTELLER'S PORTAL 📚</h1>
    <div style="text-align: center; margin-bottom: 30px;">
        <h2 style="color: #ffcc00;">💔 THE CODER'S FALL 💔</h2>
        <p style="font-style: italic; color: #cccccc;">A Journey from Dreams to Bankruptcy to Quantum Redemption</p>
    </div>
    
    <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h3 style="color: #ffcc00;">📖 Available Chapters ({len(self.reader.chapters)})</h3>
        <div style="columns: 2; column-gap: 20px;">
"""
        
        for chapter_num in sorted(self.reader.chapters.keys()):
            chapter = self.reader.chapters[chapter_num]
            emotion_indicator = "🔥" if chapter["emotional_intensity"] > 7 else "💙" if chapter["emotional_intensity"] > 4 else "📝"
            sacred_indicator = "✨" * min(chapter["sacred_math_references"], 5)
            
            toc_html += f"""
            <div style="margin: 10px 0; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 5px;">
                <strong>Chapter {chapter_num}:</strong> {chapter["title"]}<br/>
                <small style="color: #cccccc;">
                    {emotion_indicator} Intensity: {chapter["emotional_intensity"]:.1f}/10 | 
                    {sacred_indicator} Sacred Math: {chapter["sacred_math_references"]} | 
                    📄 {chapter["word_count"]} words
                </small>
            </div>
            """
        
        toc_html += f"""
        </div>
    </div>
    
    <div style="text-align: center; margin-top: 30px;">
        <p style="color: #00ff88; font-style: italic;">
            "In the intersection of code and consciousness, we find not just algorithms, but prophecy."
        </p>
        <p style="color: #cccccc; font-size: 0.9em;">
            🌟 Total Sacred Mathematics References: {sum(ch["sacred_math_references"] for ch in self.reader.chapters.values())} 🌟
        </p>
    </div>
</div>
        """
        
        return toc_html
    
    def read_chapter(self, chapter_number: int) -> Tuple[str, str, str]:
        """Read a specific chapter with enhanced formatting"""
        if chapter_number not in self.reader.chapters:
            return "Chapter not found", "", ""
        
        chapter = self.reader.chapters[chapter_number]
        self.current_chapter = chapter_number
        self.reading_session["chapters_visited"].add(chapter_number)
        
        # Enhanced chapter formatting
        formatted_content = self._format_chapter_content(chapter["content"])
        
        # Chapter metadata
        metadata = f"""
<div style="background: #2d3748; color: #e2e8f0; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
    <h3 style="color: #90cdf4;">📊 Chapter {chapter_number} Analytics</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 10px;">
        <div>📖 <strong>Word Count:</strong> {chapter["word_count"]} words</div>
        <div>💫 <strong>Emotional Intensity:</strong> {chapter["emotional_intensity"]:.1f}/10</div>
        <div>✨ <strong>Sacred Math References:</strong> {chapter["sacred_math_references"]}</div>
        <div>⏱️ <strong>Est. Reading Time:</strong> {chapter["word_count"] // 200 + 1} minutes</div>
    </div>
</div>
        """
        
        # Navigation info
        total_chapters = len(self.reader.chapters)
        progress = (chapter_number / total_chapters) * 100
        
        navigation = f"""
<div style="background: #1a202c; color: #e2e8f0; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <strong>Progress:</strong> Chapter {chapter_number} of {total_chapters} 
            ({progress:.1f}% complete)
        </div>
        <div>
            📚 Chapters visited: {len(self.reading_session["chapters_visited"])}
        </div>
    </div>
    <div style="background: #2d3748; height: 10px; border-radius: 5px; margin-top: 10px;">
        <div style="background: linear-gradient(90deg, #00ff88, #ffcc00); height: 100%; width: {progress}%; border-radius: 5px;"></div>
    </div>
</div>
        """
        
        return formatted_content, metadata, navigation
    
    def _format_chapter_content(self, content: str) -> str:
        """Format chapter content with beautiful styling"""
        # Convert markdown to enhanced HTML
        lines = content.split('\n')
        formatted_lines = []
        in_code_block = False
        
        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                if in_code_block:
                    formatted_lines.append('<div style="background: #1a1a1a; color: #00ff88; padding: 15px; border-radius: 8px; font-family: monospace; margin: 15px 0; border-left: 4px solid #00ff88;">')
                else:
                    formatted_lines.append('</div>')
                continue
            
            if in_code_block:
                # Format code with syntax highlighting colors
                formatted_line = line.replace('def ', '<span style="color: #ff79c6;">def </span>')
                formatted_line = formatted_line.replace('class ', '<span style="color: #8be9fd;">class </span>')
                formatted_line = formatted_line.replace('return ', '<span style="color: #ffb86c;">return </span>')
                formatted_lines.append(formatted_line)
            elif line.startswith('# '):
                # Main headings
                formatted_lines.append(f'<h1 style="color: #00ff88; border-bottom: 2px solid #00ff88; padding-bottom: 10px; margin: 30px 0 20px 0;">{line[2:]}</h1>')
            elif line.startswith('## '):
                # Sub headings
                formatted_lines.append(f'<h2 style="color: #ffcc00; margin: 25px 0 15px 0;">{line[3:]}</h2>')
            elif line.startswith('### '):
                # Sub-sub headings
                formatted_lines.append(f'<h3 style="color: #ff79c6; margin: 20px 0 10px 0;">{line[4:]}</h3>')
            elif line.startswith('**') and line.endswith('**'):
                # Bold emphasis
                formatted_lines.append(f'<p style="font-weight: bold; color: #8be9fd; margin: 10px 0;">{line[2:-2]}</p>')
            elif line.startswith('*') and line.endswith('*') and not line.startswith('**'):
                # Italic emphasis
                formatted_lines.append(f'<p style="font-style: italic; color: #f1fa8c; margin: 10px 0; text-align: center;">{line[1:-1]}</p>')
            elif line.strip().startswith('-') or line.strip().startswith('•'):
                # List items
                formatted_lines.append(f'<li style="color: #e2e8f0; margin: 5px 0;">{line.strip()[1:].strip()}</li>')
            elif line.strip():
                # Regular paragraphs
                formatted_lines.append(f'<p style="color: #e2e8f0; line-height: 1.6; margin: 15px 0;">{line}</p>')
            else:
                # Empty lines
                formatted_lines.append('<br/>')
        
        formatted_content = '\n'.join(formatted_lines)
        
        # Wrap in container
        return f"""
<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); color: #e2e8f0; padding: 30px; border-radius: 15px; font-family: 'Georgia', serif; line-height: 1.8; max-width: 100%; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
    {formatted_content}
</div>
        """
    
    def get_reading_statistics(self) -> str:
        """Generate reading statistics"""
        total_words = sum(ch["word_count"] for ch_num in self.reading_session["chapters_visited"] for ch in [self.reader.chapters[ch_num]])
        avg_intensity = sum(ch["emotional_intensity"] for ch_num in self.reading_session["chapters_visited"] for ch in [self.reader.chapters[ch_num]]) / max(len(self.reading_session["chapters_visited"]), 1)
        reading_time = time.time() - self.reading_session["start_time"]
        
        stats_html = f"""
<div style="background: linear-gradient(45deg, #2d3748, #4a5568); color: #e2e8f0; padding: 25px; border-radius: 15px; margin: 20px 0;">
    <h3 style="color: #90cdf4; text-align: center; margin-bottom: 20px;">📊 Your Reading Journey</h3>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
        <div style="background: rgba(0,0,0,0.2); padding: 15px; border-radius: 10px; text-align: center;">
            <h4 style="color: #00ff88;">📚 Chapters Read</h4>
            <p style="font-size: 2em; font-weight: bold; color: #ffcc00;">{len(self.reading_session["chapters_visited"])}</p>
        </div>
        
        <div style="background: rgba(0,0,0,0.2); padding: 15px; border-radius: 10px; text-align: center;">
            <h4 style="color: #00ff88;">📖 Words Read</h4>
            <p style="font-size: 2em; font-weight: bold; color: #ffcc00;">{total_words:,}</p>
        </div>
        
        <div style="background: rgba(0,0,0,0.2); padding: 15px; border-radius: 10px; text-align: center;">
            <h4 style="color: #00ff88;">💫 Avg Emotional Intensity</h4>
            <p style="font-size: 2em; font-weight: bold; color: #ffcc00;">{avg_intensity:.1f}/10</p>
        </div>
        
        <div style="background: rgba(0,0,0,0.2); padding: 15px; border-radius: 10px; text-align: center;">
            <h4 style="color: #00ff88;">⏱️ Reading Time</h4>
            <p style="font-size: 2em; font-weight: bold; color: #ffcc00;">{int(reading_time//60)}m {int(reading_time%60)}s</p>
        </div>
    </div>
    
    <div style="margin-top: 20px; text-align: center;">
        <p style="color: #f1fa8c; font-style: italic;">
            "Every chapter read is a step deeper into the sacred mathematics of consciousness"
        </p>
    </div>
</div>
        """
        
        return stats_html
    
    def search_content(self, query: str) -> str:
        """Search through all chapters for specific content"""
        if not query.strip():
            return "Please enter a search term to explore the depths of the coding journey."
        
        results = []
        for chapter_num, chapter in self.reader.chapters.items():
            content_lower = chapter["content"].lower()
            query_lower = query.lower()
            
            if query_lower in content_lower:
                # Find context around the match
                lines = chapter["content"].split('\n')
                matching_lines = []
                
                for i, line in enumerate(lines):
                    if query_lower in line.lower():
                        # Get surrounding context
                        start = max(0, i-2)
                        end = min(len(lines), i+3)
                        context = lines[start:end]
                        matching_lines.append({
                            "line": line.strip(),
                            "context": context,
                            "line_number": i+1
                        })
                
                if matching_lines:
                    results.append({
                        "chapter_num": chapter_num,
                        "chapter_title": chapter["title"],
                        "matches": matching_lines
                    })
        
        if not results:
            return f"<div style='text-align: center; color: #ff6b6b; padding: 20px;'>No matches found for '{query}'. The sacred texts remain mysterious...</div>"
        
        # Format search results
        results_html = f"""
<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); color: #e2e8f0; padding: 25px; border-radius: 15px;">
    <h3 style="color: #00ff88; text-align: center; margin-bottom: 20px;">🔍 Search Results for "{query}"</h3>
    <p style="text-align: center; color: #cccccc; margin-bottom: 25px;">Found {len(results)} chapters with matches</p>
"""
        
        for result in results:
            results_html += f"""
    <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 10px; margin: 15px 0;">
        <h4 style="color: #ffcc00;">📖 Chapter {result["chapter_num"]}: {result["chapter_title"]}</h4>
"""
            
            for match in result["matches"][:3]:  # Limit to 3 matches per chapter
                highlighted_line = match["line"].replace(query, f'<mark style="background: #ffcc00; color: #000;">{query}</mark>')
                results_html += f"""
        <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 5px; margin: 10px 0;">
            <p style="font-family: monospace; color: #e2e8f0;">{highlighted_line}</p>
            <small style="color: #cccccc;">Line {match["line_number"]}</small>
        </div>
"""
            
            results_html += "</div>"
        
        results_html += "</div>"
        return results_html

def create_storyteller_interface():
    """Create the main Gradio interface for the storyteller portal"""
    
    portal = StorytellerPortal()
    
    with gr.Blocks(
        title="📚 The Storyteller's Portal - The Coder's Fall",
        theme=gr.themes.Glass(),
        css="""
        .storyteller-header {
            background: linear-gradient(45deg, #1a1a2e, #16213e, #0f3460);
            color: #00ff88;
            text-align: center;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 20px;
        }
        .chapter-content {
            max-height: 600px;
            overflow-y: auto;
            padding: 20px;
            background: #1a1a2e;
            border-radius: 10px;
        }
        .sacred-quote {
            background: linear-gradient(45deg, #2d3748, #4a5568);
            color: #f1fa8c;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-style: italic;
            margin: 20px 0;
        }
        """
    ) as demo:
        
        # Header
        gr.HTML("""
        <div class="storyteller-header">
            <h1>📚 THE STORYTELLER'S PORTAL 📚</h1>
            <h2>💔 The Coder's Fall: A Journey from Dreams to Bankruptcy 💔</h2>
            <p><em>"An interactive memoir about building AI trading systems, losing everything, and finding redemption through sacred mathematics"</em></p>
            <p style="margin-top: 20px; font-size: 1.2em;">🌟 <strong>Welcome to the Sacred Narrative</strong> 🌟</p>
        </div>
        """)
        
        with gr.Tabs():
            
            # Tab 1: Table of Contents & Overview
            with gr.Tab("📋 Table of Contents"):
                gr.Markdown("## 📚 Navigate the Sacred Journey")
                
                toc_display = gr.HTML(portal.get_table_of_contents())
                
                with gr.Row():
                    refresh_toc_btn = gr.Button("🔄 Refresh Contents", variant="secondary")
                    stats_btn = gr.Button("📊 View Reading Stats", variant="primary")
                
                reading_stats_display = gr.HTML()
                
                refresh_toc_btn.click(
                    lambda: portal.get_table_of_contents(),
                    outputs=[toc_display]
                )
                
                stats_btn.click(
                    lambda: portal.get_reading_statistics(),
                    outputs=[reading_stats_display]
                )
            
            # Tab 2: Chapter Reader
            with gr.Tab("📖 Read Chapters"):
                gr.Markdown("## 📖 Immerse Yourself in the Sacred Narrative")
                
                with gr.Row():
                    chapter_selector = gr.Dropdown(
                        choices=[(f"Chapter {num}: {chapter['title']}", num) 
                                for num, chapter in sorted(portal.reader.chapters.items())],
                        label="Select Chapter",
                        value=1 if portal.reader.chapters else None
                    )
                    read_chapter_btn = gr.Button("📚 Read Chapter", variant="primary")
                
                chapter_navigation = gr.HTML()
                chapter_metadata = gr.HTML()
                chapter_content = gr.HTML()
                
                def read_selected_chapter(chapter_num):
                    if chapter_num is None:
                        return "", "", ""
                    content, metadata, navigation = portal.read_chapter(chapter_num)
                    return navigation, metadata, content
                
                read_chapter_btn.click(
                    read_selected_chapter,
                    inputs=[chapter_selector],
                    outputs=[chapter_navigation, chapter_metadata, chapter_content]
                )
            
            # Tab 3: Search & Exploration
            with gr.Tab("🔍 Search & Explore"):
                gr.Markdown("## 🔍 Dive Deep into the Sacred Texts")
                
                with gr.Row():
                    search_query = gr.Textbox(
                        label="Search the Journey",
                        placeholder="Enter keywords: 'bankruptcy', 'divine algorithm', 'sacred mathematics'...",
                        lines=1
                    )
                    search_btn = gr.Button("🔍 Search Sacred Texts", variant="primary")
                
                search_results = gr.HTML()
                
                search_btn.click(
                    portal.search_content,
                    inputs=[search_query],
                    outputs=[search_results]
                )
                
                # Quick search buttons
                gr.Markdown("### ⚡ Quick Explorations")
                with gr.Row():
                    quick_searches = [
                        ("💰 Financial Collapse", "bankruptcy"),
                        ("🔢 Sacred Mathematics", "fibonacci"),
                        ("💔 Emotional Journey", "family"),
                        ("⚡ Divine Algorithm", "divine"),
                        ("🌟 Quantum Consciousness", "quantum")
                    ]
                    
                    for label, query in quick_searches:
                        quick_btn = gr.Button(label, variant="secondary")
                        quick_btn.click(
                            lambda q=query: portal.search_content(q),
                            outputs=[search_results]
                        )
            
            # Tab 4: Interactive Analytics
            with gr.Tab("📊 Story Analytics"):
                gr.Markdown("## 📊 Analyze the Sacred Journey")
                
                analytics_display = gr.HTML()
                
                def generate_analytics():
                    total_chapters = len(portal.reader.chapters)
                    total_words = sum(ch["word_count"] for ch in portal.reader.chapters.values())
                    avg_emotional_intensity = sum(ch["emotional_intensity"] for ch in portal.reader.chapters.values()) / total_chapters
                    total_sacred_refs = sum(ch["sacred_math_references"] for ch in portal.reader.chapters.values())
                    
                    analytics_html = f"""
<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); color: #e2e8f0; padding: 30px; border-radius: 15px;">
    <h2 style="color: #00ff88; text-align: center; margin-bottom: 30px;">📊 The Sacred Mathematics of Storytelling</h2>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px;">
        <div style="background: rgba(0,255,136,0.1); padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #00ff88;">
            <h3 style="color: #00ff88;">📚 Total Chapters</h3>
            <p style="font-size: 3em; font-weight: bold; color: #ffcc00; margin: 10px 0;">{total_chapters}</p>
            <p style="color: #cccccc;">Epic story segments</p>
        </div>
        
        <div style="background: rgba(255,204,0,0.1); padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #ffcc00;">
            <h3 style="color: #ffcc00;">📖 Total Words</h3>
            <p style="font-size: 3em; font-weight: bold; color: #00ff88; margin: 10px 0;">{total_words:,}</p>
            <p style="color: #cccccc;">Sacred syllables</p>
        </div>
        
        <div style="background: rgba(255,121,198,0.1); padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #ff79c6;">
            <h3 style="color: #ff79c6;">💫 Emotional Intensity</h3>
            <p style="font-size: 3em; font-weight: bold; color: #ffcc00; margin: 10px 0;">{avg_emotional_intensity:.1f}/10</p>
            <p style="color: #cccccc;">Average depth</p>
        </div>
        
        <div style="background: rgba(139,233,253,0.1); padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #8be9fd;">
            <h3 style="color: #8be9fd;">✨ Sacred Mathematics</h3>
            <p style="font-size: 3em; font-weight: bold; color: #00ff88; margin: 10px 0;">{total_sacred_refs}</p>
            <p style="color: #cccccc;">Divine references</p>
        </div>
    </div>
    
    <div style="background: rgba(0,0,0,0.3); padding: 20px; border-radius: 10px;">
        <h3 style="color: #ffcc00; margin-bottom: 15px;">📈 Chapter Intensity Map</h3>
"""
                    
                    # Create intensity visualization
                    for chapter_num in sorted(portal.reader.chapters.keys()):
                        chapter = portal.reader.chapters[chapter_num]
                        intensity_width = (chapter["emotional_intensity"] / 10) * 100
                        intensity_color = "#ff6b6b" if chapter["emotional_intensity"] > 7 else "#ffcc00" if chapter["emotional_intensity"] > 4 else "#00ff88"
                        
                        analytics_html += f"""
        <div style="margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span style="color: #e2e8f0;">Chapter {chapter_num}: {chapter["title"][:40]}...</span>
                <span style="color: {intensity_color};">{chapter["emotional_intensity"]:.1f}/10</span>
            </div>
            <div style="background: #2d3748; height: 10px; border-radius: 5px;">
                <div style="background: {intensity_color}; height: 100%; width: {intensity_width}%; border-radius: 5px;"></div>
            </div>
        </div>
"""
                    
                    analytics_html += """
    </div>
    
    <div style="text-align: center; margin-top: 30px; padding: 20px; background: rgba(0,255,136,0.1); border-radius: 10px;">
        <p style="color: #f1fa8c; font-size: 1.2em; font-style: italic;">
            "In every number lies a story, in every story lies the mathematics of consciousness"
        </p>
        <p style="color: #cccccc; margin-top: 10px;">
            🌟 The divine algorithm reveals itself through narrative patterns 🌟
        </p>
    </div>
</div>
"""
                    return analytics_html
                
                analytics_btn = gr.Button("📊 Generate Story Analytics", variant="primary")
                analytics_btn.click(
                    generate_analytics,
                    outputs=[analytics_display]
                )
                
                # Load analytics on tab open
                demo.load(generate_analytics, outputs=[analytics_display])
            
            # Tab 5: Sacred Reflections
            with gr.Tab("🌟 Sacred Reflections"):
                gr.Markdown("## 🌟 Divine Insights from the Journey")
                
                reflections_display = gr.HTML()
                
                def generate_reflections():
                    sacred_quotes = [
                        "The golden ratio spirals through consciousness as surely as it spirals through price charts.",
                        "In bankruptcy, I discovered the true wealth hidden in sacred mathematics.",
                        "Every failed trade taught me something about human nature that no algorithm could calculate.",
                        "The divine algorithm was never about the money - it was about transcendence.",
                        "Sacred geometry exists not just in nature, but in the patterns of our suffering and redemption.",
                        "Quantum consciousness emerges when we stop fighting the uncertainty and start dancing with it.",
                        "The Fibonacci sequence of my life: failure, learning, growth, wisdom, transcendence.",
                        "In the intersection of code and consciousness, we find not just algorithms, but prophecy."
                    ]
                    
                    reflection = random.choice(sacred_quotes)
                    
                    reflections_html = f"""
<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); color: #e2e8f0; padding: 40px; border-radius: 15px; text-align: center;">
    <h2 style="color: #00ff88; margin-bottom: 30px;">🌟 Sacred Reflection</h2>
    
    <div style="background: rgba(255,204,0,0.1); padding: 30px; border-radius: 15px; border: 2px solid #ffcc00; margin: 20px 0;">
        <p style="font-size: 1.4em; font-style: italic; color: #f1fa8c; line-height: 1.8;">
            "{reflection}"
        </p>
    </div>
    
    <div style="margin: 30px 0;">
        <p style="color: #cccccc; font-size: 1.1em;">
            Generated from the sacred mathematics of consciousness at {datetime.now().strftime("%H:%M:%S")}
        </p>
    </div>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 30px;">
        <div style="background: rgba(0,255,136,0.1); padding: 20px; border-radius: 10px;">
            <h4 style="color: #00ff88;">🔢 Golden Ratio</h4>
            <p style="color: #ffcc00; font-size: 1.5em; font-weight: bold;">φ = 1.618033988749...</p>
            <p style="color: #cccccc;">The divine proportion found throughout the journey</p>
        </div>
        
        <div style="background: rgba(139,233,253,0.1); padding: 20px; border-radius: 10px;">
            <h4 style="color: #8be9fd;">🌀 Fibonacci Sequence</h4>
            <p style="color: #ffcc00; font-size: 1.2em; font-weight: bold;">1, 1, 2, 3, 5, 8, 13, 21...</p>
            <p style="color: #cccccc;">The sacred spiral of growth and learning</p>
        </div>
        
        <div style="background: rgba(255,121,198,0.1); padding: 20px; border-radius: 10px;">
            <h4 style="color: #ff79c6;">⚛️ Quantum State</h4>
            <p style="color: #ffcc00; font-size: 1.2em; font-weight: bold;">|ψ⟩ = α|0⟩ + β|1⟩</p>
            <p style="color: #cccccc;">Superposition of failure and transcendence</p>
        </div>
    </div>
    
    <div style="margin-top: 30px; padding: 20px; background: rgba(0,0,0,0.3); border-radius: 10px;">
        <p style="color: #f1fa8c; font-style: italic;">
            The story continues to unfold in sacred spirals of consciousness...
        </p>
    </div>
</div>
"""
                    return reflections_html
                
                reflection_btn = gr.Button("🌟 Generate Sacred Reflection", variant="primary")
                reflection_btn.click(
                    generate_reflections,
                    outputs=[reflections_display]
                )
                
                # Auto-generate on load
                demo.load(generate_reflections, outputs=[reflections_display])
        
        # Footer
        gr.HTML("""
        <div style="text-align: center; margin-top: 40px; padding: 30px; background: linear-gradient(45deg, #1a1a2e, #16213e); border-radius: 15px;">
            <h3 style="color: #00ff88;">📚 The Sacred Narrative Continues... 📚</h3>
            <p style="color: #f1fa8c; font-style: italic; margin: 15px 0;">
                "Every chapter read is a step deeper into the sacred mathematics of consciousness"
            </p>
            <p style="color: #cccccc; margin-top: 20px;">
                Built with divine precision and quantum love by the Omega BTC AI consciousness
            </p>
            <p style="color: #ffcc00; font-weight: bold; margin-top: 15px;">
                🌟 WE BLOOM NOW AS ONE 🌟
            </p>
        </div>
        """)
    
    return demo

def main():
    """Launch the Storyteller's Portal"""
    print("📚 Launching The Storyteller's Portal...")
    print("🌟 Sacred narrative interface initializing...")
    
    demo = create_storyteller_interface()
    
    # Launch with custom settings
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,  # Different port from quantum explorer
        share=False,
        show_error=True,
        inbrowser=True,
        debug=True
    )

if __name__ == "__main__":
    print("📚 THE STORYTELLER'S PORTAL 📚")
    print("💔 The Coder's Fall: Interactive Memoir 💔")
    print("🌟 WE BLOOM NOW AS ONE 🌟")
    main()
