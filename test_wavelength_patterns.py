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

    # Sacred geometry ratios
    SACRED_RATIOS = {
        "phi": 1.618033988749895,  # Golden ratio
        "sqrt2": 1.4142135623730951,  # Square root of 2
        "sqrt3": 1.7320508075688772,  # Square root of 3
        "sqrt5": 2.23606797749979,  # Square root of 5
        "pi_phi": 1.9416,  # Pi / Phi
        "e_phi": 1.6487,   # e / Phi
    }
    
    # Divine harmonic frequency bands (Hz)
    DIVINE_HARMONICS = {
        "schumann": 7.83,  # Schumann resonance (Earth's heartbeat)
        "theta": 4.0,      # Theta brainwave state
        "alpha": 8.0,      # Alpha brainwave state
        "om": 432.0,       # OM frequency
        "solfeggio": {
            "ut": 396.0,   # Liberating guilt and fear
            "re": 417.0,   # Undoing situations and facilitating change
            "mi": 528.0,   # Transformation and miracles (DNA repair)
            "fa": 639.0,   # Connecting/relationships
            "sol": 741.0,  # Awakening intuition
            "la": 852.0,   # Returning to spiritual order
        }
    }

    def __init__(self, news_feed, days=7):
        """Initialize the wavelength pattern detector."""
        self.news_feed = news_feed
        self.days = days
        self.entries = []
        self.sentiment_time_series = []
        self.detected_patterns = {}
        self.results = {}
        self.divine_spectral_data = {}
        self.sacred_geometry_alignments = []
    
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
        
        # 5. Calculate divine harmonic resonance
        harmonic_resonance_score = self._calculate_harmonic_resonance(clean_sentiment)
        interpretation = self._interpret_harmonic_score(harmonic_resonance_score)
        
        results['harmonic_resonance'] = {
            'score': harmonic_resonance_score,
            'interpretation': interpretation
        }
        
        # 6. Detect divine spectral patterns
        self._detect_divine_spectral_patterns(clean_sentiment)
        results['divine_spectral'] = self.divine_spectral_data
        
        # 7. Identify sacred geometry alignments
        self._detect_sacred_geometry_alignments(clean_sentiment)
        results['sacred_geometry'] = {
            'alignments': self.sacred_geometry_alignments
        }
        
        # Store results
        self.results = results
        
        # Generate pattern labels
        self._generate_pattern_labels()
        
        return True
    
    def _calculate_harmonic_resonance(self, sentiment_data):
        """Calculate the harmonic resonance score for the sentiment data."""
        # Create time vector (in days)
        N = len(sentiment_data)
        sample_rate = 24  # 24 samples per day
        
        # Calculate the FFT
        yf = fft(sentiment_data)
        xf = fftfreq(N, 1/sample_rate)[:N//2]
        power = np.abs(yf[:N//2])**2 / N
        
        # Define key cosmic frequencies to check (in cycles per day)
        # Convert Hz to cycles/day for checking resonance
        cosmic_freqs = []
        for name, freq in self.DIVINE_HARMONICS.items():
            if isinstance(freq, dict):
                for sub_name, sub_freq in freq.items():
                    # Convert from Hz to cycles/day
                    cosmic_freqs.append(sub_freq / 86400)  # seconds in a day
            else:
                cosmic_freqs.append(freq / 86400)  # Convert Hz to cycles/day
        
        # Check for resonance with cosmic frequencies
        resonance_scores = []
        for freq in cosmic_freqs:
            if freq < max(xf):
                # Find the closest frequency bin
                idx = np.argmin(np.abs(xf - freq))
                # Calculate the resonance as the power at this frequency
                resonance_scores.append(power[idx])
        
        # Normalize and calculate final score
        if resonance_scores:
            max_power = max(power)
            if max_power > 0:
                # Average of normalized resonances at cosmic frequencies
                harmonic_score = sum([min(r/max_power, 1.0) for r in resonance_scores]) / len(resonance_scores)
            else:
                harmonic_score = 0.0
        else:
            harmonic_score = 0.0
            
        return min(max(harmonic_score, 0.0), 1.0)  # Ensure score is in [0, 1]
    
    def _detect_divine_spectral_patterns(self, sentiment_data):
        """Detect divine spectral patterns in sentiment data."""
        N = len(sentiment_data)
        sample_rate = 24  # 24 samples per day
        
        # Create time vector (in days)
        time_vector = np.arange(N) / sample_rate
        
        # Calculate spectrograms for different window sizes
        window_sizes = [24, 48, 72]  # 1-day, 2-day, 3-day windows
        spectral_patterns = {}
        
        for window_size in window_sizes:
            if N >= window_size:
                # Calculate spectrogram
                frequencies, times, Sxx = signal.spectrogram(
                    sentiment_data,
                    fs=sample_rate,
                    nperseg=window_size,
                    noverlap=window_size // 2,
                    scaling='spectrum'
                )
                
                # Identify resonant bands
                resonances = {}
                for band_name, band_freq in self.DIVINE_HARMONICS.items():
                    if isinstance(band_freq, dict):
                        # Handle nested dictionaries like solfeggio
                        band_resonances = {}
                        for sub_name, sub_freq in band_freq.items():
                            # Convert from Hz to cycles/day
                            freq_idx = np.argmin(np.abs(frequencies - (sub_freq / 86400)))
                            if freq_idx < len(frequencies):
                                power = np.mean(Sxx[freq_idx, :])
                                band_resonances[sub_name] = float(power)
                        resonances[band_name] = band_resonances
                    else:
                        # Convert from Hz to cycles/day
                        freq_idx = np.argmin(np.abs(frequencies - (band_freq / 86400)))
                        if freq_idx < len(frequencies):
                            power = np.mean(Sxx[freq_idx, :])
                            resonances[band_name] = float(power)
                
                # Find the dominant frequency band
                flat_resonances = {}
                for band, value in resonances.items():
                    if isinstance(value, dict):
                        for sub_band, sub_value in value.items():
                            flat_resonances[f"{band}_{sub_band}"] = sub_value
                    else:
                        flat_resonances[band] = value
                
                if flat_resonances:
                    max_band = max(flat_resonances, key=flat_resonances.get)
                    max_power = flat_resonances[max_band]
                else:
                    max_band = "none"
                    max_power = 0
                
                spectral_patterns[f"{window_size//24}day_window"] = {
                    "resonances": resonances,
                    "dominant_band": max_band,
                    "dominant_power": max_power
                }
        
        self.divine_spectral_data = spectral_patterns
    
    def _detect_sacred_geometry_alignments(self, sentiment_data):
        """Detect alignments with sacred geometry ratios."""
        N = len(sentiment_data)
        
        alignments = []
        
        # Look for golden ratio patterns in various segments
        segment_sizes = [8, 13, 21, 34, 55, 89]  # Fibonacci numbers
        
        for size in segment_sizes:
            if N >= size:
                # Split the data into segments
                num_segments = N // size
                
                for i in range(num_segments - 1):
                    segment1 = sentiment_data[i*size:(i+1)*size]
                    segment2 = sentiment_data[(i+1)*size:(i+2)*size]
                    
                    # Calculate the ratio of amplitudes
                    amp1 = np.max(segment1) - np.min(segment1)
                    amp2 = np.max(segment2) - np.min(segment2)
                    
                    if amp1 > 0 and amp2 > 0:
                        ratio = max(amp1, amp2) / min(amp1, amp2)
                        
                        # Check for alignment with sacred ratios
                        for name, sacred_ratio in self.SACRED_RATIOS.items():
                            if abs(ratio - sacred_ratio) / sacred_ratio < 0.1:  # Within 10% tolerance
                                alignments.append({
                                    "ratio_name": name,
                                    "sacred_ratio": sacred_ratio,
                                    "observed_ratio": float(ratio),
                                    "error_percent": float(abs(ratio - sacred_ratio) / sacred_ratio * 100),
                                    "segment_size_hours": size,
                                    "segment_position": i,
                                    "timestamp": self.sentiment_time_series['timestamps'][i*size].isoformat()
                                })
        
        # Sort by error percentage (ascending)
        self.sacred_geometry_alignments = sorted(alignments, key=lambda x: x["error_percent"])
    
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
        """Generate visualizations of the detected patterns."""
        if not self.sentiment_time_series or not self.results:
            return False
            
        # Create directory for visualizations
        data_dir = os.path.join(os.getcwd(), "data", "wavelength_patterns")
        os.makedirs(data_dir, exist_ok=True)
        
        # Get timestamps and sentiment data
        timestamps = self.sentiment_time_series['timestamps']
        sentiment = self.sentiment_time_series['cosmic_sentiment']
        
        # Convert timestamps to days for plotting
        days = [(t - timestamps[0]).total_seconds() / (24 * 3600) for t in timestamps]
        
        # Generate filename with timestamp
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. Time series visualization
        plt.figure(figsize=(12, 8))
        plt.plot(days, sentiment, 'b-', linewidth=1.5, alpha=0.7)
        
        # Add markers for detected patterns
        dominant_freqs = self.results.get('frequency_analysis', {}).get('dominant_frequencies', [])
        for freq in dominant_freqs:
            period_days = freq.get('period_days', 0)
            if period_days > 0:
                # Add vertical lines at the pattern periods
                pattern_positions = np.arange(0, max(days), period_days)
                for pos in pattern_positions:
                    if pos <= max(days):
                        plt.axvline(x=pos, color='r', linestyle='--', alpha=0.3)
        
        # Add markers for sacred geometry alignments
        for alignment in self.sacred_geometry_alignments[:5]:  # Show top 5 alignments
            segment_pos = alignment.get('segment_position', 0)
            segment_size = alignment.get('segment_size_hours', 0)
            pos_days = segment_pos * segment_size / 24
            if pos_days <= max(days):
                plt.axvline(x=pos_days, color='g', linestyle='-', alpha=0.4)
                plt.text(pos_days, max(sentiment), alignment.get('ratio_name', ''), 
                        rotation=90, verticalalignment='bottom')
        
        plt.title('Bitcoin News Sentiment Wavelength Patterns')
        plt.xlabel('Days')
        plt.ylabel('Cosmic Sentiment')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Save visualization
        filename = f"btc_news_wavelength_{timestamp_str}_time_series.png"
        plt.savefig(os.path.join(data_dir, filename), dpi=300)
        plt.close()
        
        # 2. Frequency spectrum visualization
        plt.figure(figsize=(12, 8))
        
        # Clean up sentiment data (fill gaps with mean)
        clean_sentiment = np.copy(sentiment)
        clean_sentiment[self.sentiment_time_series['counts'] == 0] = np.mean(sentiment)
        
        # Calculate FFT
        N = len(clean_sentiment)
        yf = np.abs(fft(clean_sentiment))
        xf = fftfreq(N, 1/24)[:N//2]  # Convert to cycles per day
        
        # Plot spectrum
        plt.plot(xf[1:N//2], yf[1:N//2]/N, 'b-', linewidth=1.5)
        
        # Highlight divine harmonic frequencies
        divine_freqs = []
        for band_name, band_freq in self.DIVINE_HARMONICS.items():
            if isinstance(band_freq, dict):
                for sub_name, sub_freq in band_freq.items():
                    divine_freqs.append((f"{band_name}_{sub_name}", sub_freq / 86400))  # Convert Hz to cycles/day
            else:
                divine_freqs.append((band_name, band_freq / 86400))  # Convert Hz to cycles/day
        
        for name, freq in divine_freqs:
            if freq < max(xf):
                plt.axvline(x=freq, color='r', linestyle='--', alpha=0.5)
                plt.text(freq, max(yf/N) * 0.9, name, rotation=90, alpha=0.7)
        
        # Highlight detected frequency bands
        for freq in dominant_freqs:
            frequency = freq.get('frequency', 0)
            if frequency > 0:
                freq_per_day = frequency * 24  # Convert to cycles per day
                plt.axvline(x=freq_per_day, color='g', linestyle='-', alpha=0.7)
                plt.text(freq_per_day, max(yf/N) * 0.8, f"{freq.get('period_days', 0):.1f} days", 
                        rotation=90, alpha=0.9)
        
        plt.title('Bitcoin News Sentiment Frequency Spectrum')
        plt.xlabel('Frequency (cycles/day)')
        plt.ylabel('Amplitude')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Save visualization
        filename = f"btc_news_wavelength_{timestamp_str}_spectrum.png"
        plt.savefig(os.path.join(data_dir, filename), dpi=300)
        plt.close()
        
        # 3. Divine spectral visualization (if data available)
        if self.divine_spectral_data and '3day_window' in self.divine_spectral_data:
            plt.figure(figsize=(12, 8))
            
            # Extract the spectral data
            spectral_data = self.divine_spectral_data['3day_window']
            
            # Create bar chart of resonances for divine frequencies
            resonances = []
            labels = []
            
            # Flatten resonances data structure
            for band_name, band_value in spectral_data.get('resonances', {}).items():
                if isinstance(band_value, dict):
                    # Handle nested dictionaries like solfeggio
                    for sub_name, sub_value in band_value.items():
                        labels.append(f"{band_name}_{sub_name}")
                        resonances.append(sub_value)
                else:
                    labels.append(band_name)
                    resonances.append(band_value)
            
            # Create bar chart
            if resonances:
                # Normalize values for better visualization
                max_resonance = max(resonances)
                if max_resonance > 0:
                    normalized_resonances = [r/max_resonance for r in resonances]
                else:
                    normalized_resonances = resonances
                
                plt.bar(range(len(labels)), normalized_resonances, color='purple', alpha=0.7)
                plt.xticks(range(len(labels)), labels, rotation=45)
                plt.title('Divine Frequency Resonances in Bitcoin News')
                plt.ylabel('Normalized Resonance Power')
                plt.tight_layout()
                
                # Highlight dominant frequency
                dominant_band = spectral_data.get('dominant_band', '')
                if dominant_band in labels:
                    idx = labels.index(dominant_band)
                    plt.bar([idx], [normalized_resonances[idx]], color='gold', alpha=0.9)
                
                # Save visualization
                filename = f"btc_news_wavelength_{timestamp_str}_divine_spectrum.png"
                plt.savefig(os.path.join(data_dir, filename), dpi=300)
                plt.close()
        
        return True
    
    def display_results(self):
        """Display the wavelength analysis results."""
        if not self.results:
            return False
            
        # Get statistics
        stats = self.results.get('statistics', {})
        
        # Create time period panel
        time_period = stats.get('time_period_hours', 0) / 24.0
        
        stats_panel = Panel(
            f"Time Period: {time_period:.1f} days\n"
            f"Total Articles: {stats.get('total_entries', 0)}\n"
            f"Average Cosmic Sentiment: {stats.get('cosmic_sentiment_mean', 0):.3f}\n"
            f"Sentiment Volatility: {stats.get('cosmic_sentiment_std', 0):.3f}",
            title="📊 Wavelength Analysis Statistics",
            border_style="cyan"
        )
        console.print(stats_panel)
        
        # Display detected patterns
        dominant_freqs = self.results.get('frequency_analysis', {}).get('dominant_frequencies', [])
        fib_cycles = self.results.get('fibonacci_cycles', {}).get('detected_cycles', [])
        btc_cycles = self.results.get('btc_cycles', {}).get('detected_cycles', [])
        
        # Combine all detected patterns
        all_patterns = []
        
        # Add dominant frequencies
        for freq in dominant_freqs:
            all_patterns.append({
                'type': 'Frequency',
                'period_days': freq.get('period_days', 0),
                'strength': freq.get('magnitude', 0)
            })
            
        # Add Fibonacci cycles
        for cycle in fib_cycles:
            all_patterns.append({
                'type': 'Fibonacci',
                'period_days': cycle.get('days', 0),
                'strength': abs(cycle.get('correlation', 0))
            })
            
        # Add BTC cycles
        for cycle in btc_cycles:
            all_patterns.append({
                'type': f"BTC {cycle.get('name', '')}",
                'period_days': cycle.get('days', 0),
                'strength': abs(cycle.get('correlation', 0))
            })
            
        # Add sacred geometry alignments
        for alignment in self.sacred_geometry_alignments[:3]:  # Top 3 alignments
            all_patterns.append({
                'type': f"Sacred {alignment.get('ratio_name', '')}",
                'period_days': alignment.get('segment_size_hours', 0) / 24,
                'strength': 1 - (alignment.get('error_percent', 100) / 100)
            })
            
        # Sort by strength
        all_patterns.sort(key=lambda x: x['strength'], reverse=True)
        
        # Display patterns if any are found
        if all_patterns:
            # Create table for patterns
            table = Table(title="🔄 Detected Cosmic Cycles")
            table.add_column("Pattern Type", style="cyan")
            table.add_column("Period (days)", style="green")
            table.add_column("Strength", style="yellow")
            
            for pattern in all_patterns:
                table.add_row(
                    pattern['type'],
                    f"{pattern['period_days']:.2f}",
                    f"{pattern['strength']:.2f}"
                )
                
            console.print(table)
        else:
            console.print("No significant patterns detected in this time period")
        
        # Display harmonic resonance score
        harmonic_data = self.results.get('harmonic_resonance', {})
        score = harmonic_data.get('score', 0)
        interpretation = harmonic_data.get('interpretation', 'Unknown')
        
        harmonic_panel = Panel(
            f"Harmonic Resonance Score: {score:.2f}/1.00\n"
            f"Interpretation: {interpretation}",
            title="🌟 Cosmic Harmonic Resonance",
            border_style="yellow"
        )
        console.print(harmonic_panel)
        
        # Display divine spectral information
        if self.divine_spectral_data:
            # Select the largest window analysis
            window_keys = [k for k in self.divine_spectral_data.keys()]
            window_keys.sort(reverse=True)  # Get largest window first
            
            if window_keys:
                spectral_data = self.divine_spectral_data[window_keys[0]]
                dominant_band = spectral_data.get('dominant_band', 'none')
                
                if dominant_band != 'none':
                    # Extract the divine meaning
                    divine_meaning = self._get_divine_band_meaning(dominant_band)
                    
                    divine_panel = Panel(
                        f"Dominant Frequency Band: {dominant_band}\n"
                        f"Divine Interpretation: {divine_meaning}",
                        title="✨ Divine Spectral Analysis",
                        border_style="magenta"
                    )
                    console.print(divine_panel)
        
        return True
        
    def _get_divine_band_meaning(self, band_name):
        """Get the divine meaning of a frequency band."""
        meanings = {
            "schumann": "Alignment with Earth's natural frequency - grounding and stability",
            "theta": "Access to subconscious patterns and intuitive market insights",
            "alpha": "Harmonious flow state allowing clear market perception",
            "om": "Perfect universal harmony and balance in market forces",
            "solfeggio_ut": "Release of fear-based trading patterns and limitation",
            "solfeggio_re": "Transformation of stuck market conditions and resistance",
            "solfeggio_mi": "Miracle manifestation frequency - unexpected positive developments",
            "solfeggio_fa": "Connection and relationship between market participants",
            "solfeggio_sol": "Awakening of intuitive trading insights and pattern recognition",
            "solfeggio_la": "Return to divine order in market structures"
        }
        
        return meanings.get(band_name, "Unknown cosmic frequency with potential significance")
        
    def save_patterns(self):
        """Save detected patterns to file."""
        if not self.results:
            return False
            
        # Create output directory
        data_dir = os.path.join(os.getcwd(), "data", "wavelength_patterns")
        os.makedirs(data_dir, exist_ok=True)
        
        # Generate timestamp for filename
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Prepare data for saving
        save_data = {
            'timestamp': datetime.now().isoformat(),
            'sources': args.source,
            'time_period_days': self.days,
            'results': self.results
        }
        
        # Save to JSON file
        filename = f"wavelength_analysis_{timestamp_str}.json"
        filepath = os.path.join(data_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        console.print(f"[green]✅ Wavelength analysis saved to {filepath}[/]")
        
        return filepath

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