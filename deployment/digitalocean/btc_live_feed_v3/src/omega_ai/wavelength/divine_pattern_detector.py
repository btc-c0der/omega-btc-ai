#!/usr/bin/env python3
"""
OMEGA BTC AI - Divine Pattern Detector
======================================

This module provides tools for detecting divine patterns in time series data
using sacred geometry and harmonic analysis.

Copyright (c) 2025 OMEGA-BTC-AI - All rights reserved
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import json
from typing import List, Dict, Tuple, Union, Optional, Any

# Direct imports instead of relative imports
from sacred_geometry_analyzer import SacredGeometryAnalyzer
from divine_harmonic_analyzer import DivineHarmonicAnalyzer


class DivinePatternDetector:
    """Detects cosmic patterns in time series data using sacred geometry and divine harmonics."""
    
    # Bitcoin-specific cycle patterns (in days)
    BTC_CYCLES = {
        "halving": 1458,     # ~4 years between halving events
        "accumulation": 63,  # Typical accumulation phase
        "wyckoff": 21,       # Wyckoff distribution pattern
        "fomo": 8,           # Typical FOMO cycle length
        "panic": 3,          # Panic selling cycle
        "weekend": 7,        # Weekly cycle
    }
    
    def __init__(self, sample_rate=24):
        """Initialize the divine pattern detector.
        
        Args:
            sample_rate: The sample rate of the time series data in samples per day
        """
        self.sample_rate = sample_rate
        self.sacred_geometry = SacredGeometryAnalyzer()
        self.divine_harmonic = DivineHarmonicAnalyzer(sample_rate=sample_rate)
        self.results = {}
        self.detected_patterns = []
    
    def analyze_patterns(self, time_series, timestamps=None):
        """Analyze the time series data for divine patterns.
        
        Args:
            time_series: A numpy array of sentiment or price values
            timestamps: Optional list of datetime objects
            
        Returns:
            dict: Analysis results including divine patterns, harmonics, and geometry
        """
        # Initialize results
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "sample_count": len(time_series),
            "time_period_days": len(time_series) / self.sample_rate if len(time_series) > 0 else 0
        }
        
        # Skip analysis if not enough data
        if len(time_series) < 24:  # At least one day of data
            self.results["error"] = "Insufficient data for divine pattern analysis"
            return self.results
        
        # Clean the data
        clean_data = np.copy(time_series)
        clean_data[~np.isfinite(clean_data)] = 0
        
        # Calculate basic statistics
        self.results["statistics"] = {
            "sentiment_mean": float(np.mean(clean_data)),
            "sentiment_std": float(np.std(clean_data)),
            "sentiment_min": float(np.min(clean_data)),
            "sentiment_max": float(np.max(clean_data)),
        }
        
        # 1. Sacred Geometry Analysis
        geometry_results = self.sacred_geometry.analyze_geometry(clean_data, timestamps)
        self.results["sacred_geometry"] = geometry_results
        
        # 2. Divine Harmonic Analysis
        harmonic_results = self.divine_harmonic.analyze_harmonics(clean_data)
        self.results["divine_harmonic"] = harmonic_results
        
        # 3. Fibonacci Time Cycles
        fibonacci_cycles = self.sacred_geometry.detect_fibonacci_time_cycles(clean_data, timestamps)
        self.results["fibonacci_cycles"] = {
            "detected_cycles": fibonacci_cycles
        }
        
        # 4. Bitcoin-specific cycle detection
        btc_cycles = self._detect_btc_cycles(clean_data)
        self.results["btc_cycles"] = {
            "detected_cycles": btc_cycles
        }
        
        # 5. Integrate detected patterns
        self._integrate_patterns()
        
        return self.results
    
    def _detect_btc_cycles(self, time_series):
        """Detect Bitcoin-specific cycles in the data.
        
        Args:
            time_series: A numpy array of sentiment or price values
            
        Returns:
            list: Detected Bitcoin cycles
        """
        N = len(time_series)
        
        # Convert days to hours
        cycles = []
        data_days = N / self.sample_rate
        
        for name, cycle_days in self.BTC_CYCLES.items():
            if cycle_days < data_days:
                # Convert days to samples
                cycle_samples = cycle_days * self.sample_rate
                
                # Create sine wave with this cycle length
                cycle_wave = np.sin(np.linspace(0, 2*np.pi*N/cycle_samples, N))
                correlation = np.corrcoef(time_series, cycle_wave)[0, 1]
                
                if not np.isnan(correlation) and abs(correlation) > 0.18:  # Threshold
                    cycles.append({
                        "name": name,
                        "days": cycle_days,
                        "correlation": float(correlation),
                        "phase": "aligned" if correlation > 0 else "inverse"
                    })
        
        return sorted(cycles, key=lambda x: abs(x["correlation"]), reverse=True)
    
    def _integrate_patterns(self):
        """Integrate detected patterns from various analyzers."""
        all_patterns = []
        
        # Add sacred geometry alignments
        for alignment in self.results.get("sacred_geometry", {}).get("alignments", [])[:3]:
            all_patterns.append({
                "type": "Sacred Geometry",
                "name": f"Sacred {alignment.get('ratio_name', '')}",
                "period_days": alignment.get('segment_size', 0) / 24.0,
                "strength": 1.0 - (alignment.get('error_percent', 100.0) / 100.0),
                "insight": self.sacred_geometry.get_divine_insights(
                    alignment.get('ratio_name', ''),
                    1.0 - (alignment.get('error_percent', 100.0) / 100.0)
                )
            })
        
        # Add divine harmonic resonances
        harmonic_data = self.results.get("divine_harmonic", {})
        dominant_band = harmonic_data.get("dominant_band")
        
        if dominant_band:
            all_patterns.append({
                "type": "Divine Harmonic",
                "name": f"Harmonic {dominant_band}",
                "period_days": 1.0,  # Default for harmonics
                "strength": harmonic_data.get("resonance_score", 0.0),
                "insight": self.divine_harmonic.get_divine_meaning(dominant_band)
            })
        
        # Add Fibonacci cycles
        for cycle in self.results.get("fibonacci_cycles", {}).get("detected_cycles", [])[:2]:
            all_patterns.append({
                "type": "Fibonacci Cycle",
                "name": f"Fibonacci {cycle.get('days', 0)}-Day Cycle",
                "period_days": cycle.get('days', 0),
                "strength": abs(cycle.get('correlation', 0.0)),
                "insight": "Divine Fibonacci time cycle revealing cosmic temporal harmonics"
            })
        
        # Add BTC cycles
        for cycle in self.results.get("btc_cycles", {}).get("detected_cycles", [])[:2]:
            all_patterns.append({
                "type": "Bitcoin Cycle",
                "name": f"BTC {cycle.get('name', '').title()}",
                "period_days": cycle.get('days', 0),
                "strength": abs(cycle.get('correlation', 0.0)),
                "insight": f"Market {cycle.get('name', '')} cycle aligned with cosmic flow"
            })
        
        # Sort by strength
        self.detected_patterns = sorted(all_patterns, key=lambda x: x["strength"], reverse=True)
        self.results["detected_patterns"] = self.detected_patterns
    
    def visualize_patterns(self, time_series, timestamps=None, output_dir=None):
        """Generate visualizations of the detected patterns.
        
        Args:
            time_series: A numpy array of sentiment or price values
            timestamps: Optional list of datetime objects
            output_dir: Directory to save visualizations
            
        Returns:
            list: Paths to generated visualization files
        """
        if not self.results:
            raise ValueError("Must run analyze_patterns before visualization")
            
        # Create directory for visualizations
        if output_dir is None:
            output_dir = os.path.join(os.getcwd(), "data", "wavelength_patterns")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate timestamp for filenames
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create time vector in days if timestamps not provided
        if timestamps is None:
            days = np.arange(len(time_series)) / self.sample_rate
        else:
            # Convert timestamps to days from start
            start_time = timestamps[0]
            days = [(t - start_time).total_seconds() / (24 * 3600) for t in timestamps]
        
        visualization_files = []
        
        # 1. Time series visualization with pattern markers
        plt.figure(figsize=(12, 8))
        plt.plot(days, time_series, 'b-', linewidth=1.5, alpha=0.7)
        
        # Add sacred geometry alignment markers
        alignments = self.results.get("sacred_geometry", {}).get("alignments", [])
        for alignment in alignments[:5]:  # Show top 5 alignments
            segment_pos = alignment.get('segment_position', 0)
            segment_size = alignment.get('segment_size', 0)
            pos_days = segment_pos * segment_size / self.sample_rate
            
            if pos_days <= max(days):
                plt.axvline(x=pos_days, color='g', linestyle='-', alpha=0.4)
                plt.text(pos_days, max(time_series), alignment.get('ratio_name', ''),
                        rotation=90, verticalalignment='bottom')
        
        # Add markers for dominant harmonics
        harmonic_data = self.results.get("divine_harmonic", {})
        dominant_band = harmonic_data.get("dominant_band")
        if dominant_band:
            plt.text(min(days) + 0.5, max(time_series) * 0.9, 
                   f"Dominant Harmonic: {dominant_band}", 
                   backgroundcolor='yellow', alpha=0.5)
        
        plt.title('Divine Pattern Analysis of Bitcoin News Sentiment')
        plt.xlabel('Days')
        plt.ylabel('Sentiment')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Save visualization
        time_series_file = os.path.join(output_dir, f"divine_patterns_{timestamp_str}_time_series.png")
        plt.savefig(time_series_file, dpi=300)
        plt.close()
        visualization_files.append(time_series_file)
        
        # 2. Cosmic wheel of patterns - polar visualization
        if self.detected_patterns:
            plt.figure(figsize=(10, 10))
            ax = plt.subplot(111, polar=True)
            
            # Convert patterns to polar coordinates
            max_patterns = min(len(self.detected_patterns), 8)  # Limit to 8 patterns
            theta = np.linspace(0, 2*np.pi, max_patterns, endpoint=False)  # Angles
            radii = [p["strength"] for p in self.detected_patterns[:max_patterns]]  # Strengths
            width = 2*np.pi / max_patterns * 0.8  # Bar width
            
            # Create bars
            bars = ax.bar(theta, radii, width=width, bottom=0.0, alpha=0.5)
            
            # Color bars by pattern type
            colors = {
                "Sacred Geometry": "green",
                "Divine Harmonic": "purple",
                "Fibonacci Cycle": "blue",
                "Bitcoin Cycle": "red"
            }
            
            for i, pattern in enumerate(self.detected_patterns[:max_patterns]):
                bars[i].set_color(colors.get(pattern["type"], "gray"))
                bars[i].set_alpha(0.7)
            
            # Add pattern names
            for i, pattern in enumerate(self.detected_patterns[:max_patterns]):
                angle = theta[i]
                ax.text(angle, 1.1, pattern["name"], 
                       rotation=angle*180/np.pi - 90,
                       ha='center', va='center',
                       fontsize=8)
            
            # Add strength scale
            ax.set_rlabel_position(0)
            ax.set_rticks([0.25, 0.5, 0.75, 1.0])
            ax.set_yticklabels(["0.25", "0.5", "0.75", "1.0"])
            
            plt.title('Cosmic Wheel of Divine Patterns')
            
            # Save visualization
            cosmic_wheel_file = os.path.join(output_dir, f"divine_patterns_{timestamp_str}_cosmic_wheel.png")
            plt.savefig(cosmic_wheel_file, dpi=300)
            plt.close()
            visualization_files.append(cosmic_wheel_file)
        
        return visualization_files
    
    def save_results(self, output_dir=None):
        """Save the analysis results to a JSON file.
        
        Args:
            output_dir: Directory to save results
            
        Returns:
            str: Path to the saved JSON file
        """
        if not self.results:
            raise ValueError("No results to save. Run analyze_patterns first.")
            
        # Create directory if needed
        if output_dir is None:
            output_dir = os.path.join(os.getcwd(), "data", "wavelength_patterns")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate timestamp for filename
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"divine_pattern_analysis_{timestamp_str}.json"
        filepath = os.path.join(output_dir, filename)
        
        # Ensure results are JSON serializable
        results_copy = {}
        for key, value in self.results.items():
            if isinstance(value, np.ndarray):
                results_copy[key] = value.tolist()
            else:
                results_copy[key] = value
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump(results_copy, f, indent=2)
        
        return filepath
        
    def interpret_results(self):
        """Generate cosmic interpretations of the detected patterns.
        
        Returns:
            dict: Cosmic interpretations and recommendations
        """
        interpretations = {
            "cosmic_summary": "",
            "divine_message": "",
            "market_guidance": "",
            "strongest_pattern": None
        }
        
        # Check if we have enough patterns to interpret
        if not self.detected_patterns:
            interpretations["cosmic_summary"] = "Insufficient cosmic patterns detected for divine interpretation"
            return interpretations
        
        # Get the strongest pattern
        strongest = self.detected_patterns[0]
        interpretations["strongest_pattern"] = strongest["name"]
        
        # Generate cosmic summary based on pattern types
        pattern_types = [p["type"] for p in self.detected_patterns[:3]]
        
        if "Sacred Geometry" in pattern_types and "Divine Harmonic" in pattern_types:
            interpretations["cosmic_summary"] = "Perfect union of form and vibration in the market consciousness"
        elif "Sacred Geometry" in pattern_types:
            interpretations["cosmic_summary"] = "Divine proportions revealing the structural patterns of market order"
        elif "Divine Harmonic" in pattern_types:
            interpretations["cosmic_summary"] = "Resonant frequencies aligning market energetics with cosmic vibrations"
        elif "Fibonacci Cycle" in pattern_types:
            interpretations["cosmic_summary"] = "Natural growth and spiraling evolution of market consciousness"
        else:
            interpretations["cosmic_summary"] = "Subtle patterns of divine significance emerging in the data field"
        
        # Generate divine message based on pattern strengths
        top_strength = strongest["strength"]
        if top_strength > 0.9:
            interpretations["divine_message"] = "Clear cosmic signals manifesting through market patterns"
        elif top_strength > 0.7:
            interpretations["divine_message"] = "Strong divine guidance flowing through data fluctuations"
        elif top_strength > 0.5:
            interpretations["divine_message"] = "Moderate cosmic alignment suggesting attentive awareness"
        else:
            interpretations["divine_message"] = "Subtle whispers from the universe indicating potential significance"
        
        # Add specific insight from the strongest pattern
        interpretations["divine_message"] += f". {strongest.get('insight', '')}"
        
        # Generate market guidance
        if "Bitcoin Cycle" in pattern_types:
            btc_cycle = next((p for p in self.detected_patterns if p["type"] == "Bitcoin Cycle"), None)
            if btc_cycle:
                cycle_name = btc_cycle["name"].split()[-1].lower()
                
                if cycle_name == "halving":
                    interpretations["market_guidance"] = "Prepare for transition between market epochs"
                elif cycle_name == "accumulation":
                    interpretations["market_guidance"] = "Period of quiet gathering before expansion phase"
                elif cycle_name == "wyckoff":
                    interpretations["market_guidance"] = "Smart money movements determining next market direction"
                elif cycle_name == "fomo":
                    interpretations["market_guidance"] = "Emotional market dynamics creating velocity"
                elif cycle_name == "panic":
                    interpretations["market_guidance"] = "Fear-based clearance creating opportunity"
                else:
                    interpretations["market_guidance"] = "Align with natural market rhythms for harmonious flow"
                    
        else:
            # Default guidance based on strongest pattern type
            if strongest["type"] == "Sacred Geometry":
                interpretations["market_guidance"] = "Seek divine proportion in your market approach"
            elif strongest["type"] == "Divine Harmonic":
                interpretations["market_guidance"] = "Attune to the resonant frequency of market consciousness"
            elif strongest["type"] == "Fibonacci Cycle":
                interpretations["market_guidance"] = "Honor the natural growth cycles in market evolution"
            else:
                interpretations["market_guidance"] = "Listen to subtle cosmic whispers guiding market movements"
        
        return interpretations

    def _create_sacred_geometry_radar(self, time_series: np.ndarray, timestamps) -> str:
        """Create a sacred geometry radar visualization.
        
        Args:
            time_series: The time series data to visualize
            timestamps: The corresponding timestamps
            
        Returns:
            str: Path to the saved visualization file
        """
        # Get sacred geometry alignments
        sacred_geometry = self.results.get('sacred_geometry', {})
        alignments = sacred_geometry.get('alignments', [])
        
        if not alignments:
            return None
        
        # Create radar plot
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, polar=True)
        
        # Categories and values
        categories = [a.get('ratio_name', 'Unknown') for a in alignments[:8]]
        values = [100 - a.get('error_percent', 0) for a in alignments[:8]]
        
        # Number of categories
        N = len(categories)
        
        # Compute angles for each category
        angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
        
        # Make the plot circular by repeating the first value
        values.append(values[0])
        angles.append(angles[0])
        categories.append(categories[0])
        
        # Plot data
        ax.plot(angles, values, 'o-', linewidth=2)
        ax.fill(angles, values, alpha=0.25)
        
        # Set category labels
        ax.set_thetagrids(np.degrees(angles[:-1]), categories[:-1])
        
        # Configure polar plot properly using appropriate matplotlib methods
        # These methods are available for polar plots in matplotlib
        ax.grid(True)
        ax.set_ylim(0, 100)
        
        # Set position of y-labels (use appropriate method if available)
        try:
            # For matplotlib versions that support this
            ax.set_rlabel_position(45)
            ax.set_rticks([20, 40, 60, 80, 100])
        except AttributeError:
            # Alternative for versions that don't have these methods
            plt.yticks([20, 40, 60, 80, 100])
        
        # Set title and labels
        plt.title('Sacred Geometry Alignment', size=16)
        
        # Save the figure
        filename = f"sacred_geometry_radar_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath 