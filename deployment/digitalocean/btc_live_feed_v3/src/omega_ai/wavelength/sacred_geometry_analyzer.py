#!/usr/bin/env python3
"""
OMEGA BTC AI - Sacred Geometry Analyzer
=======================================

This module analyzes time series data for alignment with sacred geometry
ratios like the golden ratio (phi), square roots, and other divine
proportions.

Copyright (c) 2025 OMEGA-BTC-AI - All rights reserved
"""

import numpy as np
from datetime import datetime


class SacredGeometryAnalyzer:
    """Analyzes time series data for sacred geometry patterns and divine proportions."""
    
    # Sacred geometry ratios
    SACRED_RATIOS = {
        "phi": 1.618033988749895,  # Golden ratio
        "sqrt2": 1.4142135623730951,  # Square root of 2
        "sqrt3": 1.7320508075688772,  # Square root of 3
        "sqrt5": 2.23606797749979,  # Square root of 5
        "pi_phi": 1.9416,  # Pi / Phi
        "e_phi": 1.6487,   # e / Phi
    }
    
    # Fibonacci numbers
    FIBONACCI_NUMBERS = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
    
    def __init__(self, tolerance=0.1):
        """Initialize the sacred geometry analyzer.
        
        Args:
            tolerance: The tolerance for ratio matching (default: 0.1 or 10%)
        """
        self.tolerance = tolerance
        self.alignments = []
    
    def analyze_geometry(self, time_series, timestamps=None):
        """Analyze the time series data for sacred geometry patterns.
        
        Args:
            time_series: A numpy array of sentiment or price values
            timestamps: Optional list of datetime objects corresponding to the time series
            
        Returns:
            dict: Analysis results including sacred geometry alignments and scores
        """
        if len(time_series) < 8:  # Minimum length for meaningful analysis
            return {
                "alignments": [],
                "has_alignments": False,
                "strongest_ratio": None,
                "strongest_accuracy": 0.0
            }
        
        # Detect sacred geometry alignments
        self.alignments = self._detect_alignments(time_series, timestamps)
        
        # Find strongest alignment
        strongest = None
        strongest_accuracy = 0.0
        
        if self.alignments:
            # Sort by error percentage (ascending)
            sorted_alignments = sorted(self.alignments, key=lambda x: x["error_percent"])
            strongest = sorted_alignments[0]["ratio_name"]
            strongest_accuracy = 1.0 - (sorted_alignments[0]["error_percent"] / 100.0)
        
        return {
            "alignments": self.alignments,
            "has_alignments": len(self.alignments) > 0,
            "strongest_ratio": strongest,
            "strongest_accuracy": strongest_accuracy
        }
    
    def _detect_alignments(self, time_series, timestamps=None):
        """Detect alignments with sacred geometry ratios.
        
        Args:
            time_series: A numpy array of sentiment or price values
            timestamps: Optional list of datetime objects corresponding to the time series
            
        Returns:
            list: Detected alignments with sacred geometry ratios
        """
        alignments = []
        
        # Look for golden ratio patterns in various segments
        segment_sizes = [s for s in self.FIBONACCI_NUMBERS if s < len(time_series) // 2]
        
        for size in segment_sizes:
            # Split the data into segments
            num_segments = len(time_series) // size
            
            for i in range(num_segments - 1):
                segment1 = time_series[i*size:(i+1)*size]
                segment2 = time_series[(i+1)*size:(i+2)*size]
                
                # Calculate metrics for comparison
                alignments.extend(self._compare_segments(segment1, segment2, size, i, timestamps))
        
        return alignments
    
    def _compare_segments(self, segment1, segment2, segment_size, segment_position, timestamps=None):
        """Compare two segments for sacred geometry alignments.
        
        Args:
            segment1: First segment of time series
            segment2: Second segment of time series
            segment_size: Size of each segment
            segment_position: Position of the first segment
            timestamps: Optional list of datetime objects
            
        Returns:
            list: Alignments found between the segments
        """
        alignments = []
        
        # Different metrics to compare
        metrics = [
            ("amplitude", np.max(segment1) - np.min(segment1), np.max(segment2) - np.min(segment2)),
            ("volatility", np.std(segment1), np.std(segment2)),
            ("mean", np.mean(np.abs(segment1)), np.mean(np.abs(segment2))),
            ("energy", np.sum(segment1**2), np.sum(segment2**2))
        ]
        
        for metric_name, value1, value2 in metrics:
            if value1 > 0 and value2 > 0:
                ratio = max(value1, value2) / min(value1, value2)
                
                # Check for alignment with sacred ratios
                for name, sacred_ratio in self.SACRED_RATIOS.items():
                    error_pct = abs(ratio - sacred_ratio) / sacred_ratio * 100
                    
                    if error_pct < self.tolerance * 100:  # Within tolerance
                        # Get timestamp if available
                        timestamp = None
                        if timestamps and len(timestamps) > segment_position * segment_size:
                            timestamp = timestamps[segment_position * segment_size].isoformat()
                        
                        alignments.append({
                            "ratio_name": name,
                            "sacred_ratio": sacred_ratio,
                            "observed_ratio": float(ratio),
                            "error_percent": float(error_pct),
                            "segment_size": segment_size,
                            "segment_position": segment_position,
                            "metric": metric_name,
                            "timestamp": timestamp
                        })
        
        return alignments
    
    def detect_fibonacci_time_cycles(self, time_series, timestamps=None, min_correlation=0.2):
        """Detect Fibonacci time cycles in the data.
        
        Args:
            time_series: A numpy array of sentiment or price values
            timestamps: Optional list of datetime objects
            min_correlation: Minimum correlation coefficient to consider (default: 0.2)
            
        Returns:
            list: Detected Fibonacci cycles
        """
        if len(time_series) < 10:
            return []
            
        cycles = []
        N = len(time_series)
        
        # Clean the data
        clean_data = np.copy(time_series)
        clean_data[~np.isfinite(clean_data)] = 0
        
        # Check various Fibonacci cycle lengths
        for cycle in self.FIBONACCI_NUMBERS:
            if cycle < N // 2:  # Need at least 2 cycles to detect pattern
                # Create sine wave with this cycle length
                cycle_wave = np.sin(np.linspace(0, 2*np.pi*N/cycle, N))
                
                # Calculate correlation
                correlation = np.corrcoef(clean_data, cycle_wave)[0, 1]
                
                if not np.isnan(correlation) and abs(correlation) > min_correlation:
                    cycles.append({
                        "hours": cycle,
                        "days": cycle / 24.0,
                        "correlation": float(correlation),
                        "phase": "aligned" if correlation > 0 else "inverse"
                    })
        
        # Sort by correlation strength
        return sorted(cycles, key=lambda x: abs(x["correlation"]), reverse=True)
    
    def get_divine_insights(self, ratio_name, strength):
        """Get divine insights about a sacred geometry ratio.
        
        Args:
            ratio_name: The name of the sacred ratio
            strength: The strength of the alignment (0.0 to 1.0)
            
        Returns:
            str: Divine insights about the sacred ratio
        """
        insights = {
            "phi": [
                "The Golden Ratio reveals divine proportion in market cycles",
                "Perfect balance between growth and contraction phases",
                "Natural harmony aligning with cosmic expansion patterns"
            ],
            "sqrt2": [
                "The Diagonal of Unity showing balance of opposing market forces",
                "Transformation from one state of market to another",
                "The measure of harmonic progression in price movements"
            ],
            "sqrt3": [
                "The Divine Vesica Piscis ratio revealing union of buy/sell energies",
                "Trinity forces creating stability in apparent chaos",
                "The measure of perfect triangular balance in market forces"
            ],
            "sqrt5": [
                "The Pentagonal Star alignment showing hidden order",
                "Connection between microcosmic trades and macrocosmic cycles",
                "The divine proportion of regenerative market cycles"
            ],
            "pi_phi": [
                "The Cosmic Reconciliation of circular and spiral forces",
                "Transcendental alignment of cyclical and progressive energies",
                "Divine union of revolutionary and evolutionary market forces"
            ],
            "e_phi": [
                "The Growth Constant revealing natural market expansion patterns",
                "Organic unfolding of market potential according to divine law",
                "The mathematical constant of continuous compounding growth"
            ]
        }
        
        if ratio_name in insights:
            # Select insight based on strength
            index = min(int(strength * len(insights[ratio_name])), len(insights[ratio_name]) - 1)
            return insights[ratio_name][index]
        
        return "Mysterious cosmic pattern of unknown divine significance" 