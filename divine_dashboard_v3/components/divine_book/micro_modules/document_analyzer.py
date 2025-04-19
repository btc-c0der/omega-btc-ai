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
Document Analyzer Module

This module provides functions for analyzing document content,
extracting statistics, and generating insights.
"""

import re
import math
import html
import statistics
from typing import Dict, Any, List, Tuple, Optional

def analyze_document(content: str) -> Dict[str, Any]:
    """
    Analyze a document's content and structure.
    
    Args:
        content: The document content as a string
        
    Returns:
        Dictionary containing analysis results
    """
    analysis = {
        "structure": analyze_structure(content),
        "sentiment": analyze_sentiment(content),
        "complexity": analyze_complexity(content),
        "keywords": extract_keywords(content),
        "reading_stats": get_reading_stats(content)
    }
    
    return analysis

def get_document_stats(content: str) -> Dict[str, Any]:
    """
    Extract basic statistics from document content.
    
    Args:
        content: The document content as a string
        
    Returns:
        Dictionary containing basic document statistics
    """
    # Split into paragraphs
    paragraphs = re.split(r'\n\s*\n', content)
    paragraphs = [p for p in paragraphs if p.strip()]
    
    # Count words and characters
    words = re.findall(r'\b\w+\b', content)
    sentences = re.split(r'[.!?]+', content)
    sentences = [s for s in sentences if s.strip()]
    
    # Count code blocks
    code_blocks = len(re.findall(r'```[^`]*```', content))
    
    # Count headings
    headings = {
        "h1": len(re.findall(r'^#\s+[^\n]*$', content, re.MULTILINE)),
        "h2": len(re.findall(r'^##\s+[^\n]*$', content, re.MULTILINE)),
        "h3": len(re.findall(r'^###\s+[^\n]*$', content, re.MULTILINE)),
        "total": 0
    }
    headings["total"] = headings["h1"] + headings["h2"] + headings["h3"]
    
    # Calculate stats
    stats = {
        "word_count": len(words),
        "character_count": len(content),
        "sentence_count": len(sentences),
        "paragraph_count": len(paragraphs),
        "code_block_count": code_blocks,
        "headings": headings,
        "avg_words_per_sentence": len(words) / max(1, len(sentences)),
        "avg_characters_per_word": len(content) / max(1, len(words)),
    }
    
    return stats

def analyze_structure(content: str) -> Dict[str, Any]:
    """Analyze the document's structural elements."""
    # Detect sections based on headings
    sections = []
    headings = re.finditer(r'^(#+)\s+(.+)$', content, re.MULTILINE)
    
    for match in headings:
        level = len(match.group(1))
        title = match.group(2).strip()
        position = match.start()
        sections.append({
            "level": level,
            "title": title,
            "position": position
        })
    
    # Detect lists
    unordered_lists = len(re.findall(r'^\s*[-*+]\s+', content, re.MULTILINE))
    ordered_lists = len(re.findall(r'^\s*\d+\.\s+', content, re.MULTILINE))
    
    # Detect tables
    tables = len(re.findall(r'^\|[^|]+\|[^|]+\|', content, re.MULTILINE))
    
    # Detect links and images
    links = len(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content))
    images = len(re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content))
    
    structure = {
        "sections": sections,
        "section_count": len(sections),
        "list_count": {
            "unordered": unordered_lists,
            "ordered": ordered_lists,
            "total": unordered_lists + ordered_lists
        },
        "table_count": tables,
        "link_count": links,
        "image_count": images
    }
    
    return structure

def analyze_sentiment(content: str) -> Dict[str, float]:
    """
    Analyze the sentiment of document content.
    This is a simple placeholder implementation.
    """
    # Simple word-based sentiment analysis
    positive_words = {
        "good", "great", "excellent", "brilliant", "amazing", "wonderful",
        "divine", "sacred", "cosmic", "quantum", "optimal", "efficient",
        "best", "better", "improved", "enhance", "benefit", "advantage",
        "success", "successful", "achieve", "accomplished", "perfect"
    }
    
    negative_words = {
        "bad", "poor", "terrible", "horrible", "awful", "wrong",
        "issue", "problem", "error", "bug", "fail", "failed",
        "worse", "worst", "difficult", "hard", "complex", "complicated",
        "impossible", "negative", "disadvantage", "drawback"
    }
    
    words = re.findall(r'\b\w+\b', content.lower())
    
    positive_count = sum(1 for word in words if word in positive_words)
    negative_count = sum(1 for word in words if word in negative_words)
    total_count = len(words)
    
    positive_score = positive_count / total_count if total_count > 0 else 0
    negative_score = negative_count / total_count if total_count > 0 else 0
    
    sentiment = {
        "positive_score": positive_score,
        "negative_score": negative_score,
        "net_score": positive_score - negative_score,
        "overall": "positive" if positive_score > negative_score else "negative" if negative_score > positive_score else "neutral"
    }
    
    return sentiment

def analyze_complexity(content: str) -> Dict[str, float]:
    """Analyze the document's complexity."""
    sentences = re.split(r'[.!?]+', content)
    sentences = [s for s in sentences if s.strip()]
    
    words = re.findall(r'\b\w+\b', content)
    word_lengths = [len(word) for word in words]
    
    # Calculate average word length
    avg_word_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0
    
    # Calculate sentence length stats
    sentence_lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences]
    avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
    
    # Basic Flesch-Kincaid readability
    syllables = estimate_syllables(content)
    if len(words) > 0 and len(sentences) > 0:
        flesch_reading_ease = 206.835 - 1.015 * (len(words) / len(sentences)) - 84.6 * (syllables / len(words))
    else:
        flesch_reading_ease = 0
    
    # Word variety (unique words ratio)
    unique_words = len(set(word.lower() for word in words))
    word_variety = unique_words / len(words) if words else 0
    
    complexity = {
        "avg_word_length": avg_word_length,
        "avg_sentence_length": avg_sentence_length,
        "flesch_reading_ease": max(0, min(100, flesch_reading_ease)),
        "word_variety": word_variety,
        "estimated_syllables": syllables
    }
    
    return complexity

def extract_keywords(content: str, top_n: int = 10) -> List[Dict[str, Any]]:
    """Extract top keywords from document content."""
    # Remove code blocks and other non-content elements
    cleaned_content = re.sub(r'```[^`]*```', '', content)
    cleaned_content = re.sub(r'`[^`]*`', '', cleaned_content)
    
    # List of common English stopwords
    stopwords = {
        "a", "an", "the", "and", "or", "but", "if", "then", "else", "when",
        "at", "by", "for", "with", "about", "against", "between", "into",
        "through", "during", "before", "after", "above", "below", "to", "from",
        "up", "down", "in", "out", "on", "off", "over", "under", "again",
        "further", "then", "once", "here", "there", "when", "where", "why",
        "how", "all", "any", "both", "each", "few", "more", "most", "other",
        "some", "such", "no", "nor", "not", "only", "own", "same", "so",
        "than", "too", "very", "can", "will", "just", "should", "now"
    }
    
    # Count word frequencies
    words = re.findall(r'\b\w+\b', cleaned_content.lower())
    word_freq = {}
    
    for word in words:
        if word not in stopwords and len(word) > 2:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency
    keywords = [{"word": word, "frequency": freq} for word, freq in word_freq.items()]
    keywords.sort(key=lambda x: x["frequency"], reverse=True)
    
    return keywords[:top_n]

def get_reading_stats(content: str) -> Dict[str, Any]:
    """Get reading time and other reading-related statistics."""
    words = re.findall(r'\b\w+\b', content)
    
    # Average reading speed is around 200-250 words per minute
    reading_speed_wpm = 225
    reading_time_minutes = len(words) / reading_speed_wpm
    
    stats = {
        "reading_time_minutes": reading_time_minutes,
        "reading_time_formatted": format_reading_time(reading_time_minutes)
    }
    
    return stats

def estimate_syllables(text: str) -> int:
    """Estimate the number of syllables in text (English)."""
    text = text.lower()
    text = re.sub(r'[^a-z]', ' ', text)
    words = re.findall(r'\b\w+\b', text)
    
    syllable_count = 0
    
    for word in words:
        word = word.lower()
        
        # Count vowel groups
        vowels = "aeiouy"
        count = 0
        prev_is_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_is_vowel:
                count += 1
            prev_is_vowel = is_vowel
        
        # Adjust for special cases
        if word.endswith('e'):
            count -= 1
        if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
            count += 1
        if count == 0:
            count = 1
        
        syllable_count += count
    
    return syllable_count

def format_reading_time(minutes: float) -> str:
    """Format reading time in minutes to a human-readable string."""
    if minutes < 1:
        return "less than a minute"
    elif minutes < 60:
        min_int = int(minutes)
        return f"{min_int} minute{'s' if min_int != 1 else ''}"
    else:
        hours = int(minutes / 60)
        mins = int(minutes % 60)
        if mins == 0:
            return f"{hours} hour{'s' if hours != 1 else ''}"
        else:
            return f"{hours} hour{'s' if hours != 1 else ''} {mins} minute{'s' if mins != 1 else ''}" 