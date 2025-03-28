#!/usr/bin/env python3
"""
OMEGA BTC AI - News Wavelength Pattern Detection
===============================================

This script analyzes Bitcoin news wavelength patterns to detect
cyclical trends, harmonic resonances, and cosmic alignments.

Copyright (c) 2025 OMEGA-BTC-AI - Licensed under the GPU License
"""

import os
import sys
import argparse
import json
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from scipy import signal
from scipy.fft import fft, fftfreq
import pandas as pd

# Ensure the package is in the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'deployment/digitalocean/btc_live_feed_v3/src')
sys.path.insert(0, src_path)

# Parse command line arguments
parser = argparse.ArgumentParser(description="Detect wavelength patterns in Bitcoin news")
parser.add_argument("--nodatabase", action="store_true", help="Run without database connection")
parser.add_argument("--source", type=str, default="all", 
                    help="News source to analyze (default: all sources)")
parser.add_argument("--days", type=int, default=7, help="Number of days to analyze")
parser.add_argument("--save-patterns", action="store_true", help="Save detected patterns to database")
parser.add_argument("--visualize", action="store_true", help="Generate visualization of patterns")
args = parser.parse_args()

console = Console()

class WavelengthPatternDetector:
    """Analyzes news wavelength patterns to detect cyclical trends."""
    
    # Fibonacci time cycles (in hours)
    FIBONACCI_CYCLES = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
    
    # Cosmic alignment frequencies
    COSMIC_FREQUENCIES = {
        "lunar": 29.53,  # lunar cycle in days
        "mercury": 88,   # Mercury orbit in days
        "venus": 224.7,  # Venus orbit in days
        "mars": 687,     # Mars orbit in days
        "jupiter": 4333, # Jupiter orbit in days
        "saturn": 10759, # Saturn orbit in days
    }
    
    # Bitcoin-specific cycle patterns (in days)
    BTC_CYCLES = {
        "halving": 1458,     # ~4 years between halving events
        "accumulation": 63,  # Typical accumulation phase
        "wyckoff": 21,       # Wyckoff distribution pattern
        "fomo": 8,           # Typical FOMO cycle length
        "panic": 3,          # Panic selling cycle
        "weekend": 7,        # Weekly cycle
    }

    def __init__(self, news_feed, days=7):
        """Initialize the wavelength pattern detector."""
        self.news_feed = news_feed
        self.days = days
        self.entries = []
        self.sentiment_time_series = []
        self.detected_patterns = {}
        self.results = {}
    
    def collect_data(self):
        """Collect news data for wavelength analysis."""
        console.print("[bold cyan]Collecting news data for wavelength analysis...[/]")
        
        # Get all relevant news sources
        if args.source == "all":
            sources = list(self.news_feed.DEFAULT_FEEDS.keys())
        else:
            sources = [args.source]
        
        # Collect data from all sources
        total_entries = []
        for source in sources:
            console.print(f"[cyan]Fetching from {source}...[/]")
            entries = self.news_feed.fetch_news(source)
            if entries:
                total_entries.extend(entries)
                console.print(f"[green]Found {len(entries)} entries from {source}[/]")
        
        if not total_entries:
            console.print("[bold red]Error: No news entries found for analysis[/]")
            sys.exit(1)
        
        # Filter by date range
        cutoff_date = datetime.now() - timedelta(days=self.days)
        self.entries = [e for e in total_entries if e['published'] >= cutoff_date]
        
        # Apply cosmic sentiment
        self.entries = self.news_feed.adjust_sentiment_with_cosmic_factors(self.entries)
        
        # Sort by publication date
        self.entries.sort(key=lambda x: x['published'])
        
        console.print(f"[green]✅ Prepared {len(self.entries)} news entries for wavelength analysis[/]")
    
    def create_time_series(self):
        """Create time series data from news sentiments."""
        if not self.entries:
            return False
            
        # Create hourly bins
        start_date = min(e['published'] for e in self.entries)
        end_date = max(e['published'] for e in self.entries)
        
        # Calculate total hours to analyze
        total_hours = int((end_date - start_date).total_seconds() / 3600) + 1
        
        # Initialize time series arrays
        timestamps = [start_date + timedelta(hours=h) for h in range(total_hours)]
        raw_sentiment = np.zeros(total_hours)
        cosmic_sentiment = np.zeros(total_hours)
        counts = np.zeros(total_hours)
        
        # Fill the arrays with sentiment data
        for entry in self.entries:
            hour_index = int((entry['published'] - start_date).total_seconds() / 3600)
            if 0 <= hour_index < total_hours:
                raw_sentiment[hour_index] += entry['sentiment_score']
                cosmic_sentiment[hour_index] += entry.get('cosmic_sentiment', entry['sentiment_score'])
                counts[hour_index] += 1
        
        # Average the sentiments for hours with multiple entries
        for i in range(total_hours):
            if counts[i] > 0:
                raw_sentiment[i] /= counts[i]
                cosmic_sentiment[i] /= counts[i]
        
        # Store as time series
        self.sentiment_time_series = {
            'timestamps': timestamps,
            'raw_sentiment': raw_sentiment,
            'cosmic_sentiment': cosmic_sentiment,
            'counts': counts
        }
        
        return True
    
    def detect_patterns(self):
        """Detect patterns in the news sentiment time series."""
        if not self.sentiment_time_series:
            return False
            
        results = {}
        
        # 1. Basic statistics
        raw_mean = np.mean(self.sentiment_time_series['raw_sentiment'])
        cosmic_mean = np.mean(self.sentiment_time_series['cosmic_sentiment'])
        raw_std = np.std(self.sentiment_time_series['raw_sentiment'])
        cosmic_std = np.std(self.sentiment_time_series['cosmic_sentiment'])
        
        results['statistics'] = {
            'raw_sentiment_mean': raw_mean,
            'cosmic_sentiment_mean': cosmic_mean,
            'raw_sentiment_std': raw_std,
            'cosmic_sentiment_std': cosmic_std,
            'total_entries': len(self.entries),
            'time_period_hours': len(self.sentiment_time_series['timestamps']),
            'start_date': self.sentiment_time_series['timestamps'][0].isoformat(),
            'end_date': self.sentiment_time_series['timestamps'][-1].isoformat()
        }
        
        # 2. Frequency analysis (FFT)
        # Zero-fill sparse data
        clean_sentiment = np.copy(self.sentiment_time_series['cosmic_sentiment'])
        clean_sentiment[self.sentiment_time_series['counts'] == 0] = cosmic_mean
        
        # Perform FFT
        N = len(clean_sentiment)
        yf = fft(clean_sentiment)
        xf = fftfreq(N, 1.0)[:N//2]
        
        # Find dominant frequencies
        dominant_freqs = []
        magnitudes = 2.0/N * np.abs(yf[0:N//2])
        
        # Only consider positive frequencies
        positive_indices = np.where(xf > 0)[0]
        if len(positive_indices) > 0:
            sorted_indices = np.argsort(-magnitudes[positive_indices])
            top_indices = positive_indices[sorted_indices[:5]]  # Top 5 frequencies
            
            for idx in top_indices:
                if magnitudes[idx] > 0.05:  # Threshold for significance
                    period_hours = 1.0 / xf[idx] if xf[idx] > 0 else 0
                    dominant_freqs.append({
                        'frequency': xf[idx],
                        'magnitude': float(magnitudes[idx]),
                        'period_hours': float(period_hours),
                        'period_days': float(period_hours / 24.0)
                    })
            
        results['frequency_analysis'] = {
            'dominant_frequencies': dominant_freqs
        }
        
        # 3. Detect Fibonacci cycles
        fib_cycles = []
        for cycle in self.FIBONACCI_CYCLES:
            # Calculate correlation with sin wave of this cycle length
            if cycle < N:
                cycle_wave = np.sin(np.linspace(0, 2*np.pi*N/cycle, N))
                correlation = np.corrcoef(clean_sentiment, cycle_wave)[0, 1]
                if not np.isnan(correlation) and abs(correlation) > 0.2:  # Correlation threshold
                    fib_cycles.append({
                        'hours': cycle,
                        'days': cycle / 24.0,
                        'correlation': float(correlation)
                    })
                    
        results['fibonacci_cycles'] = {
            'detected_cycles': fib_cycles
        }
        
        # 4. Detect BTC-specific cycles
        btc_cycles = []
        data_days = N / 24.0  # Convert hours to days
        
        for name, cycle_days in self.BTC_CYCLES.items():
            if cycle_days < data_days:
                # Convert days to hours for the analysis
                cycle_hours = cycle_days * 24
                
                # Create sine wave with this cycle length
                cycle_wave = np.sin(np.linspace(0, 2*np.pi*N/cycle_hours, N))
                correlation = np.corrcoef(clean_sentiment, cycle_wave)[0, 1]
                
                if not np.isnan(correlation) and abs(correlation) > 0.18:  # Lower threshold
                    btc_cycles.append({
                        'name': name,
                        'days': cycle_days,
                        'correlation': float(correlation),
                        'phase': 'aligned' if correlation > 0 else 'inverse'
                    })
                    
        results['btc_cycles'] = {
            'detected_cycles': btc_cycles
        }
        
        # 5. Calculate overall harmonic resonance
        harmonic_score = 0.0
        if fib_cycles:
            harmonic_score += sum(abs(cycle['correlation']) for cycle in fib_cycles) / len(fib_cycles)
        if btc_cycles:
            harmonic_score += sum(abs(cycle['correlation']) for cycle in btc_cycles) / len(btc_cycles)
            
        if fib_cycles or btc_cycles:
            harmonic_score /= 2.0 if fib_cycles and btc_cycles else 1.0
            
        # Scale to 0-1 range
        harmonic_score = min(max(harmonic_score, 0.0), 1.0)
        
        results['harmonic_resonance'] = {
            'score': harmonic_score,
            'interpretation': self._interpret_harmonic_score(harmonic_score)
        }
        
        # Store results
        self.results = results
        
        # Generate pattern labels
        self._generate_pattern_labels()
        
        return True
    
    def _interpret_harmonic_score(self, score):
        """Interpret the harmonic resonance score."""
        if score >= 0.8:
            return "Perfect Celestial Alignment - High cosmic resonance detected in news flow"
        elif score >= 0.6:
            return "Strong Harmonic Convergence - News patterns forming coherent waves"
        elif score >= 0.4:
            return "Moderate Harmonic Structure - Some cyclical patterns present"
        elif score >= 0.2:
            return "Weak Harmonic Signal - Minimal pattern resonance"
        else:
            return "Random Noise - No significant harmonic patterns detected"
    
    def _generate_pattern_labels(self):
        """Generate pattern labels for the detected harmonics."""
        if not self.results:
            return
            
        patterns = []
        
        # Generate labels from Fibonacci cycles
        fib_cycles = self.results.get('fibonacci_cycles', {}).get('detected_cycles', [])
        for cycle in fib_cycles:
            if cycle['correlation'] > 0.4:
                patterns.append({
                    'name': f"Fibonacci {cycle['hours']} Hour Cycle",
                    'strength': abs(cycle['correlation']),
                    'description': f"Strong {cycle['hours']} hour Fibonacci time cycle detected",
                    'category': 'fibonacci'
                })
        
        # Generate labels from BTC-specific cycles
        btc_cycles = self.results.get('btc_cycles', {}).get('detected_cycles', [])
        for cycle in btc_cycles:
            patterns.append({
                'name': f"{cycle['name'].title()} Cycle",
                'strength': abs(cycle['correlation']),
                'description': f"Bitcoin {cycle['name']} cycle detected ({cycle['phase']} phase)",
                'category': 'bitcoin'
            })
        
        # Add overall harmonic resonance pattern
        harmonic_score = self.results.get('harmonic_resonance', {}).get('score', 0)
        interpretation = self.results.get('harmonic_resonance', {}).get('interpretation', '')
        
        if harmonic_score > 0.3:
            patterns.append({
                'name': f"Harmonic Resonance Pattern",
                'strength': harmonic_score,
                'description': interpretation,
                'category': 'harmonic'
            })
        
        # Store detected patterns
        self.detected_patterns = patterns
    
    def visualize_patterns(self):
        """Generate visualizations of detected patterns."""
        if not self.sentiment_time_series or not self.results:
            console.print("[yellow]No data available for visualization[/]")
            return
            
        # Create output directory
        output_dir = os.path.join("data", "wavelength_patterns")
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_base = f"btc_news_wavelength_{timestamp}"
        
        # Create time axis in days for plotting
        timestamps = self.sentiment_time_series['timestamps']
        time_days = [(t - timestamps[0]).total_seconds() / (24*3600) for t in timestamps]
        
        # 1. Plot raw time series data
        plt.figure(figsize=(12, 8))
        plt.subplot(211)
        plt.plot(time_days, self.sentiment_time_series['raw_sentiment'], 'b-', label='Raw Sentiment')
        plt.plot(time_days, self.sentiment_time_series['cosmic_sentiment'], 'r-', label='Cosmic Sentiment')
        plt.xlabel('Days')
        plt.ylabel('Sentiment Score')
        plt.title('Bitcoin News Sentiment Wavelength Analysis')
        plt.legend()
        plt.grid(True)
        
        # 2. Plot article frequency 
        plt.subplot(212)
        plt.bar(time_days, self.sentiment_time_series['counts'], alpha=0.5, label='Article Count')
        
        # Add detected cycles as vertical spans
        btc_cycles = self.results.get('btc_cycles', {}).get('detected_cycles', [])
        for i, cycle in enumerate(btc_cycles):
            if i < 5:  # Limit to top 5 cycles
                plt.axvspan(0, cycle['days'], alpha=0.1, color=f'C{i+2}', 
                           label=f"{cycle['name'].title()} Cycle ({cycle['days']} days)")
        
        plt.xlabel('Days')
        plt.ylabel('Number of Articles')
        plt.title('Article Frequency and Detected Cycles')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        
        # Save the figure
        figure_path = os.path.join(output_dir, f"{filename_base}_time_series.png")
        plt.savefig(figure_path)
        plt.close()
        
        # 3. Plot FFT spectrum
        clean_sentiment = np.copy(self.sentiment_time_series['cosmic_sentiment'])
        clean_sentiment[self.sentiment_time_series['counts'] == 0] = np.mean(clean_sentiment)
        
        N = len(clean_sentiment)
        yf = fft(clean_sentiment)
        xf = fftfreq(N, 1.0)[:N//2]
        
        plt.figure(figsize=(12, 6))
        plt.bar(xf[1:], 2.0/N * np.abs(yf[1:N//2]), width=0.01)
        plt.xlabel('Frequency (cycles/hour)')
        plt.ylabel('Amplitude')
        plt.title('Frequency Spectrum of Bitcoin News Sentiment')
        plt.grid(True)
        
        # Add annotations for top frequencies
        dominant_freqs = self.results.get('frequency_analysis', {}).get('dominant_frequencies', [])
        for i, freq in enumerate(dominant_freqs):
            if i < 5:  # Limit to top 5 frequencies
                plt.annotate(f"{freq['period_hours']:.1f} hrs", 
                           xy=(freq['frequency'], freq['magnitude']),
                           xytext=(freq['frequency'], freq['magnitude'] + 0.05),
                           arrowprops=dict(arrowstyle='->'))
        
        # Save the figure
        spectrum_path = os.path.join(output_dir, f"{filename_base}_spectrum.png")
        plt.savefig(spectrum_path)
        plt.close()
        
        console.print(f"[green]✅ Visualizations saved to {output_dir}[/]")
        
        return [figure_path, spectrum_path]
    
    def save_patterns(self):
        """Save detected patterns to file and database."""
        if not self.results:
            return
            
        # Create output directory
        output_dir = os.path.join("data", "wavelength_patterns")
        os.makedirs(output_dir, exist_ok=True)
        
        # Create a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save to JSON file
        results_file = os.path.join(output_dir, f"wavelength_analysis_{timestamp}.json")
        
        with open(results_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'sources': args.source,
                'time_period_days': self.days,
                'results': self.results,
                'detected_patterns': self.detected_patterns
            }, f, indent=2)
        
        console.print(f"[green]✅ Wavelength analysis saved to {results_file}[/]")
        
        # Save to database if enabled and available
        if not args.nodatabase and hasattr(self.news_feed, 'redis_client') and self.news_feed.redis_client:
            try:
                # Prepare data
                key = f"btc:wavelength:patterns:{timestamp}"
                data = json.dumps({
                    'timestamp': datetime.now().isoformat(),
                    'harmonic_score': self.results.get('harmonic_resonance', {}).get('score', 0),
                    'detected_patterns': self.detected_patterns,
                    'period_days': self.days
                })
                
                # Store in Redis
                self.news_feed.redis_client.set(key, data)
                
                # Also store a hash with the pattern strengths for quick access
                pattern_key = f"btc:wavelength:latest"
                pattern_data = {p['name']: p['strength'] for p in self.detected_patterns}
                self.news_feed.redis_client.hset(pattern_key, mapping=pattern_data)
                
                console.print("[green]✅ Patterns saved to database[/]")
            except Exception as e:
                console.print(f"[yellow]Warning: Could not save to database: {e}[/]")
        
        return results_file
    
    def display_results(self):
        """Display wavelength pattern analysis results."""
        if not self.results:
            console.print("[yellow]No results to display[/]")
            return
            
        # 1. Display basic statistics
        stats = self.results.get('statistics', {})
        cosmic_mean = stats.get('cosmic_sentiment_mean', 0)
        time_period = stats.get('time_period_hours', 0) / 24.0  # convert to days
        
        stats_panel = Panel(
            f"[cyan]Time Period:[/] {time_period:.1f} days\n"
            f"[cyan]Total Articles:[/] {stats.get('total_entries', 0)}\n"
            f"[cyan]Average Cosmic Sentiment:[/] {cosmic_mean:.3f}\n"
            f"[cyan]Sentiment Volatility:[/] {stats.get('cosmic_sentiment_std', 0):.3f}",
            title="📊 Wavelength Analysis Statistics",
            border_style="blue"
        )
        console.print(stats_panel)
        
        # 2. Display detected pattern table
        if self.detected_patterns:
            pattern_table = Table(title="🌊 Detected Wavelength Patterns")
            pattern_table.add_column("Pattern", style="cyan")
            pattern_table.add_column("Category", style="green")
            pattern_table.add_column("Strength", style="yellow")
            pattern_table.add_column("Description", style="white")
            
            # Sort patterns by strength
            sorted_patterns = sorted(self.detected_patterns, key=lambda x: x['strength'], reverse=True)
            
            for pattern in sorted_patterns:
                # Format strength as percentage
                strength_pct = f"{pattern['strength']*100:.1f}%"
                
                # Colorize different categories
                category_style = {
                    'fibonacci': "bright_magenta",
                    'bitcoin': "bright_green",
                    'harmonic': "bright_yellow"
                }.get(pattern['category'], "white")
                
                pattern_table.add_row(
                    pattern['name'],
                    pattern['category'].title(),
                    strength_pct,
                    pattern['description']
                )
            
            console.print(pattern_table)
        else:
            console.print("[yellow]No significant patterns detected in this time period[/]")
        
        # 3. Display harmonic resonance score
        harmonic = self.results.get('harmonic_resonance', {})
        harmonic_score = harmonic.get('score', 0)
        
        # Choose color based on score
        if harmonic_score >= 0.8:
            color = "bright_green"
        elif harmonic_score >= 0.6:
            color = "green"
        elif harmonic_score >= 0.4:
            color = "yellow"
        elif harmonic_score >= 0.2:
            color = "red"
        else:
            color = "bright_red"
            
        resonance_panel = Panel(
            f"[cyan]Harmonic Resonance Score:[/] [{color}]{harmonic_score:.2f}/1.00[/]\n"
            f"[cyan]Interpretation:[/] {harmonic.get('interpretation', 'No interpretation available')}",
            title="🌟 Cosmic Harmonic Resonance",
            border_style=color
        )
        console.print(resonance_panel)
        
        # 4. Display recommended actions based on patterns
        if self.detected_patterns:
            actions = []
            
            # Generate recommendations based on detected patterns
            for pattern in sorted_patterns[:3]:  # Top 3 strongest patterns
                if pattern['category'] == 'fibonacci' and pattern['strength'] > 0.5:
                    actions.append(f"[cyan]• Monitor {pattern['name']} wavelength for trend changes[/]")
                
                if pattern['category'] == 'bitcoin':
                    if 'accumulation' in pattern['name'].lower():
                        actions.append("[green]• Potential accumulation phase detected - consider dollar-cost averaging[/]")
                    elif 'fomo' in pattern['name'].lower():
                        actions.append("[yellow]• FOMO cycle detected - exercise caution with new positions[/]")
                    elif 'panic' in pattern['name'].lower():
                        actions.append("[red]• Panic selling pattern detected - potential buying opportunity approaching[/]")
                    elif 'weekend' in pattern['name'].lower():
                        actions.append("[cyan]• Weekend cycle detected - volatility may increase over weekends[/]")
            
            if harmonic_score > 0.6:
                actions.append("[bright_green]• Strong harmonic resonance - markets may experience synchronized movements[/]")
            
            if actions:
                action_panel = Panel(
                    "\n".join(actions),
                    title="⚡ Pattern-Based Insights",
                    border_style="yellow"
                )
                console.print(action_panel)

def run_analysis():
    """Run the wavelength pattern detection analysis."""
    try:
        # Import the module
        from omega_ai.data_feed.newsfeed import BtcNewsFeed, display_rasta_banner
        
        # Display banner
        console.print(Panel(
            "[bold cyan]OMEGA BTC AI - News Wavelength Pattern Detection[/]\n"
            "[yellow]Detecting cyclical patterns, harmonic resonances, and cosmic alignments in Bitcoin news[/]",
            border_style="magenta"
        ))
        
        # Create news feed instance
        news_feed = BtcNewsFeed(data_dir="./data", use_redis=not args.nodatabase)
        
        # Create the wavelength detector
        detector = WavelengthPatternDetector(news_feed, days=args.days)
        
        # Run analysis
        detector.collect_data()
        
        if detector.create_time_series():
            detector.detect_patterns()
            detector.display_results()
            
            # Save the patterns if requested
            if args.save_patterns:
                detector.save_patterns()
            
            # Visualize patterns if requested
            if args.visualize:
                detector.visualize_patterns()
        
    except ImportError as e:
        console.print(f"[bold red]Error importing BtcNewsFeed: {e}[/]")
        console.print("Make sure you've installed the required packages:")
        console.print("  pip install -e ./deployment/digitalocean/btc_live_feed_v3")
        console.print("  pip install feedparser rich numpy scipy pandas matplotlib")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/]")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_analysis() 