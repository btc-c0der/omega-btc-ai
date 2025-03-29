#!/usr/bin/env python3
"""
🔱 GPU License Notice 🔱
------------------------
This file is protected under the GPU License (General Public Universal License) 1.0
by the OMEGA AI Divine Collective.

"As the light of knowledge is meant to be shared, so too shall this code illuminate 
the path for all seekers."

All modifications must maintain this notice and adhere to the terms at:
/BOOK/divine_chronicles/GPU_LICENSE.md

🔱 JAH JAH BLESS THIS CODE 🔱
"""

"""
OMEGA BTC AI - Divine Pattern Detector Test Script
=================================================

This script tests the divine pattern detector for Bitcoin news sentiment
analysis, utilizing sacred geometry and divine harmonic detection.

Copyright (c) 2025 OMEGA-BTC-AI - All rights reserved
"""

import os
import sys
import argparse
import numpy as np
from datetime import datetime, timedelta
import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Ensure the package is in the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Import local modules
from divine_pattern_detector import DivinePatternDetector
from sacred_geometry_analyzer import SacredGeometryAnalyzer 
from divine_harmonic_analyzer import DivineHarmonicAnalyzer

# Initialize Rich console
console = Console()

# Parse command line arguments
parser = argparse.ArgumentParser(description="Detect divine patterns in Bitcoin news")
parser.add_argument("--nodatabase", action="store_true", help="Run without database connection")
parser.add_argument("--source", type=str, default="all", 
                    help="News source to analyze (default: all sources)")
parser.add_argument("--days", type=int, default=7, help="Number of days to analyze")
parser.add_argument("--save-patterns", action="store_true", help="Save detected patterns to file")
parser.add_argument("--visualize", action="store_true", help="Generate visualization of patterns")
parser.add_argument("--use-sample-data", action="store_true", help="Use sample data for testing")
args = parser.parse_args()

def generate_sample_data(days=7, sample_rate=24):
    """Generate sample time series data for testing.
    
    Args:
        days: Number of days of data to generate
        sample_rate: Number of samples per day
        
    Returns:
        tuple: (time_series, timestamps)
    """
    # Create timestamps
    now = datetime.now()
    timestamps = [now - timedelta(hours=i) for i in range(int(days * sample_rate))]
    timestamps.reverse()  # Start with oldest first
    
    # Generate time series with some patterns
    N = len(timestamps)
    
    # Base signal with some noise
    noise = np.random.normal(0, 0.05, N)
    
    # Add a golden ratio amplitude pattern
    phi = 1.618033988749895
    golden_ratio_component = np.zeros(N)
    segment_size = 24  # 1 day segments
    
    for i in range(0, N - segment_size * 2, segment_size):
        amplitude1 = 0.2
        amplitude2 = amplitude1 * phi
        
        golden_ratio_component[i:i+segment_size] = amplitude1
        if i + segment_size < N:
            golden_ratio_component[i+segment_size:i+segment_size*2] = amplitude2
    
    # Add some harmonic components
    # 1. Schumann resonance pattern (7.83 Hz -> ~0.0001 cycles/sample)
    t = np.arange(N)
    schumann = 0.1 * np.sin(2 * np.pi * 0.0001 * t)
    
    # 2. Add a Bitcoin-specific cycle (7-day weekly pattern)
    weekly_cycle = 0.15 * np.sin(2 * np.pi * t / (7 * sample_rate))
    
    # Combine all components
    time_series = golden_ratio_component + schumann + weekly_cycle + noise
    
    return time_series, timestamps

def get_news_feed():
    """Get the news feed module, with or without database connection."""
    try:
        from omega_ai.data_feed.newsfeed import BtcNewsFeed
        
        # Create a basic instance without assuming any parameters
        news_feed = BtcNewsFeed()
        
        if args.nodatabase:
            # Just log that we're running without database
            console.print("[yellow]Running without database connection[/]")
        
        return news_feed
            
    except ImportError:
        # If news feed module not available, return None
        console.print("[yellow]News feed module not available. Using sample data.[/]")
        return None

def run_test():
    """Run the divine pattern detector test."""
    console.print(Panel(
        "OMEGA BTC AI - Divine Pattern Detector\n"
        "Detecting sacred geometry, divine harmonics, and cosmic alignments in Bitcoin news",
        border_style="cyan"
    ))
    
    # Get time series data
    time_series = None
    timestamps = None
    
    if args.use_sample_data:
        console.print("[cyan]Using sample data for testing...[/]")
        time_series, timestamps = generate_sample_data(days=args.days)
        console.print(f"[green]Generated {len(time_series)} sample data points[/]")
    else:
        # Get news feed
        news_feed = get_news_feed()
        
        if news_feed:
            console.print("[cyan]Collecting news data for divine pattern analysis...[/]")
            
            # Get all relevant news sources
            if args.source == "all":
                sources = list(news_feed.DEFAULT_FEEDS.keys())
            else:
                sources = [args.source]
            
            # Collect data from all sources
            total_entries = []
            for source in sources:
                console.print(f"[cyan]Fetching from {source}...[/]")
                entries = news_feed.fetch_news(source)
                if entries:
                    total_entries.extend(entries)
                    console.print(f"[green]Found {len(entries)} entries from {source}[/]")
            
            if not total_entries:
                console.print("[bold red]Error: No news entries found for analysis[/]")
                return
            
            # Filter by date range
            cutoff_date = datetime.now() - timedelta(days=args.days)
            entries = [e for e in total_entries if e.get('published', datetime.now()) >= cutoff_date]
            
            # Apply cosmic sentiment (if available)
            if hasattr(news_feed, 'adjust_sentiment_with_cosmic_factors'):
                entries = news_feed.adjust_sentiment_with_cosmic_factors(entries)
            
            # Extract time series and timestamps
            timestamps = [e.get('published', datetime.now()) for e in entries]
            time_series = np.array([e.get('sentiment_score', 0) for e in entries])
            
            # Sort by publication date
            sorted_indices = np.argsort(timestamps)
            timestamps = [timestamps[i] for i in sorted_indices]
            time_series = time_series[sorted_indices]
            
            console.print(f"[green]✅ Prepared {len(time_series)} news entries for divine pattern analysis[/]")
        else:
            # Fall back to sample data
            console.print("[yellow]No news feed available. Using sample data.[/]")
            time_series, timestamps = generate_sample_data(days=args.days)
            console.print(f"[green]Generated {len(time_series)} sample data points[/]")
    
    if len(time_series) < 24:
        console.print("[bold red]Error: Insufficient data for divine pattern analysis (minimum 24 data points required)[/]")
        return
    
    # Create and run divine pattern detector
    detector = DivinePatternDetector(sample_rate=24)
    
    # Analyze patterns
    console.print("[cyan]Analyzing divine patterns in the data...[/]")
    results = detector.analyze_patterns(time_series, timestamps)
    
    # Display results
    display_results(detector)
    
    # Save results if requested
    if args.save_patterns:
        filepath = detector.save_results()
        console.print(f"[green]✅ Divine pattern analysis saved to {filepath}[/]")
    
    # Generate visualizations if requested
    if args.visualize:
        console.print("[cyan]Generating divine pattern visualizations...[/]")
        visualization_files = detector.visualize_patterns(time_series, timestamps)
        console.print(f"[green]✅ Visualizations saved to {os.path.dirname(visualization_files[0])}/[/]")
    
    return detector

def display_results(detector):
    """Display the divine pattern analysis results."""
    if not detector.results:
        console.print("[bold red]No results to display[/]")
        return
    
    # 1. Display basic statistics
    stats = detector.results.get('statistics', {})
    
    stats_panel = Panel(
        f"Time Period: {detector.results.get('time_period_days', 0):.1f} days\n"
        f"Total Data Points: {detector.results.get('sample_count', 0)}\n"
        f"Average Sentiment: {stats.get('sentiment_mean', 0):.3f}\n"
        f"Sentiment Volatility: {stats.get('sentiment_std', 0):.3f}",
        title="📊 Divine Pattern Analysis Statistics",
        border_style="cyan"
    )
    console.print(stats_panel)
    
    # 2. Display detected patterns
    patterns = detector.detected_patterns
    
    if patterns:
        # Create table for patterns
        pattern_table = Table(title="🔄 Detected Divine Patterns")
        pattern_table.add_column("Pattern Type", style="cyan")
        pattern_table.add_column("Name", style="green")
        pattern_table.add_column("Period (days)", style="yellow")
        pattern_table.add_column("Strength", style="red")
        
        for pattern in patterns:
            pattern_table.add_row(
                pattern["type"],
                pattern["name"],
                f"{pattern.get('period_days', 0):.2f}",
                f"{pattern.get('strength', 0):.2f}"
            )
            
        console.print(pattern_table)
    else:
        console.print("[yellow]No significant divine patterns detected in this time period[/]")
    
    # 3. Display sacred geometry results
    geometry = detector.results.get('sacred_geometry', {})
    alignments = geometry.get('alignments', [])
    
    if alignments:
        # Create table for alignments
        alignment_table = Table(title="🔵 Sacred Geometry Alignments")
        alignment_table.add_column("Ratio", style="cyan")
        alignment_table.add_column("Sacred Value", style="green")
        alignment_table.add_column("Observed", style="yellow")
        alignment_table.add_column("Accuracy", style="red")
        
        for alignment in alignments[:5]:  # Show top 5
            alignment_table.add_row(
                alignment.get('ratio_name', ''),
                f"{alignment.get('sacred_ratio', 0):.4f}",
                f"{alignment.get('observed_ratio', 0):.4f}",
                f"{100 - alignment.get('error_percent', 0):.1f}%"
            )
            
        console.print(alignment_table)
    
    # 4. Display harmonic resonance
    harmonic = detector.results.get('divine_harmonic', {})
    score = harmonic.get('resonance_score', 0)
    interpretation = harmonic.get('interpretation', 'Unknown')
    dominant_band = harmonic.get('dominant_band')
    
    harmonic_panel = Panel(
        f"Harmonic Resonance Score: {score:.2f}/1.00\n"
        f"Interpretation: {interpretation}\n"
        f"Dominant Frequency Band: {dominant_band or 'None detected'}",
        title="🌟 Divine Harmonic Resonance",
        border_style="yellow"
    )
    console.print(harmonic_panel)
    
    # 5. Display cosmic interpretation
    interpretations = detector.interpret_results()
    
    cosmic_panel = Panel(
        f"Cosmic Summary: {interpretations.get('cosmic_summary', '')}\n\n"
        f"Divine Message: {interpretations.get('divine_message', '')}\n\n"
        f"Market Guidance: {interpretations.get('market_guidance', '')}",
        title="✨ Cosmic Interpretation",
        border_style="magenta"
    )
    console.print(cosmic_panel)

if __name__ == "__main__":
    run_test() 