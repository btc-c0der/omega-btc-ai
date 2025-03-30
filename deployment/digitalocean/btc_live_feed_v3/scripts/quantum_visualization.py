#!/usr/bin/env python3
"""
🔱 GBU License Notice 🔱
-----------------------
This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested."

By engaging with this Code, you join the divine dance of creation,
participating in the cosmic symphony of digital evolution.

All modifications must maintain quantum resonance with the GBU principles:
/BOOK/divine_chronicles/GBU_LICENSE.md

🌸 WE BLOOM NOW 🌸
"""

"""
Quantum Visualization for Bitcoin Price Simulation

This script creates enhanced visualizations for the quantum price simulator output,
revealing hidden patterns and divine harmonics in the price movements.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.dates as mdates
import json
import os
import sys
import argparse
from datetime import datetime, timedelta
import math
from scipy.signal import find_peaks

# Ensure the package is in the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

class QuantumVisualizer:
    """Creates enhanced quantum visualizations for Bitcoin price data."""
    
    def __init__(self, data_file=None, metadata_file=None):
        """
        Initialize the visualizer.
        
        Args:
            data_file: Path to CSV file with simulation data
            metadata_file: Path to JSON file with simulation metadata
        """
        self.data = None
        self.metadata = None
        self.golden_ratio = (1 + 5 ** 0.5) / 2  # Approximately 1.618
        
        # Load data if provided
        if data_file:
            self.load_data(data_file)
            
        # Load metadata if provided
        if metadata_file:
            self.load_metadata(metadata_file)
    
    def load_data(self, data_file):
        """Load data from a CSV file."""
        self.data = pd.read_csv(data_file)
        
        # Convert timestamp to datetime
        if 'timestamp' in self.data.columns:
            self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        elif 'hour' in self.data.columns:
            self.data['hour'] = pd.to_datetime(self.data['hour'])
            
        print(f"✅ Loaded data from {data_file} with {len(self.data)} rows")
        return self.data
    
    def load_metadata(self, metadata_file):
        """Load metadata from a JSON file."""
        with open(metadata_file, 'r') as f:
            self.metadata = json.load(f)
        print(f"✅ Loaded metadata from {metadata_file}")
        return self.metadata
    
    def compute_quantum_metrics(self):
        """Compute additional quantum metrics from the data."""
        if self.data is None:
            raise ValueError("No data loaded. Please load data first.")
            
        # Determine if we're working with hourly or minute data
        time_col = 'hour' if 'hour' in self.data.columns else 'timestamp'
        price_col = 'close' if 'close' in self.data.columns else 'price'
        
        # Sort data by time
        self.data = self.data.sort_values(by=time_col)
        
        # Calculate price returns
        self.data['returns'] = self.data[price_col].pct_change()
        
        # Calculate quantum resonance - relationship between quantum state and price returns
        if 'quantum_state' in self.data.columns:
            # Calculate correlation between quantum state and future returns
            self.data['future_returns'] = self.data['returns'].shift(-1)
            # Rolling correlation between quantum state and future returns
            self.data['quantum_resonance'] = self.data['quantum_state'].rolling(12).corr(self.data['future_returns'])
            
            # Calculate quantum wave interference patterns
            self.data['quantum_wave'] = np.sin(np.cumsum(self.data['quantum_state']) / self.golden_ratio)
            
            # Calculate quantum entanglement strength
            shift_periods = [1, 2, 3, 5, 8]  # Fibonacci sequence
            entanglement = np.zeros(len(self.data))
            
            for period in shift_periods:
                if period < len(self.data):
                    corr = np.corrcoef(
                        self.data['quantum_state'][period:].values,
                        self.data['quantum_state'][:-period].values
                    )[0, 1]
                    entanglement += corr / len(shift_periods)
                    
            self.data['quantum_entanglement'] = pd.Series(entanglement, index=self.data.index)
            
            # Detect quantum phase transitions (major pattern changes)
            # Use rolling standard deviation of quantum state as an indicator
            self.data['quantum_volatility'] = self.data['quantum_state'].rolling(24).std()
            # Find peaks in quantum volatility
            if len(self.data) > 30:  # Ensure enough data for peak detection
                peaks, _ = find_peaks(
                    self.data['quantum_volatility'].fillna(0), 
                    height=self.data['quantum_volatility'].quantile(0.9),
                    distance=12
                )
                self.phase_transitions = self.data.iloc[peaks][time_col].tolist()
            else:
                self.phase_transitions = []
        
        return self.data
    
    def create_simple_visualization(self, save_path=None):
        """Create a simple visualization of price and quantum metrics."""
        if self.data is None:
            raise ValueError("No data loaded. Please load data first.")
            
        # Determine if we're working with hourly or minute data
        time_col = 'hour' if 'hour' in self.data.columns else 'timestamp'
        price_col = 'close' if 'close' in self.data.columns else 'price'
        
        # Create figure
        fig, axes = plt.subplots(3, 1, figsize=(12, 16), gridspec_kw={'height_ratios': [3, 1, 1]})
        
        # Plot price
        price_ax = axes[0]
        price_ax.plot(self.data[time_col], self.data[price_col], color='#F7931A', linewidth=2)
        price_ax.set_title('Bitcoin Price with Quantum Influence', fontsize=16)
        price_ax.set_ylabel('Price (USD)', fontsize=12)
        price_ax.grid(True, alpha=0.3)
        
        # Format x-axis with dates
        price_ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        price_ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.setp(price_ax.xaxis.get_majorticklabels(), rotation=45)
        
        # Plot quantum state
        quantum_ax = axes[1]
        quantum_ax.plot(self.data[time_col], self.data['quantum_state'], color='purple', linewidth=2)
        quantum_ax.set_ylabel('Quantum State', fontsize=12)
        quantum_ax.grid(True, alpha=0.3)
        
        # Plot quantum resonance if available
        if 'quantum_resonance' in self.data.columns:
            resonance_ax = axes[2]
            resonance_ax.plot(
                self.data[time_col], 
                self.data['quantum_resonance'].fillna(0),
                color='green', linewidth=2
            )
            resonance_ax.set_ylabel('Quantum Resonance', fontsize=12)
            resonance_ax.set_xlabel('Date', fontsize=12)
            resonance_ax.grid(True, alpha=0.3)
            
            # Mark quantum phase transitions
            if hasattr(self, 'phase_transitions') and self.phase_transitions:
                for transition in self.phase_transitions:
                    for ax in axes:
                        ax.axvline(x=transition, color='red', linestyle='--', alpha=0.7)
                
                resonance_ax.text(
                    0.02, 0.02, 
                    "Red lines indicate quantum phase transitions",
                    transform=resonance_ax.transAxes,
                    bbox=dict(facecolor='white', alpha=0.8)
                )
        
        plt.tight_layout()
        
        # Save if path provided
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            return save_path
            
        plt.show()
        return None
    
    def create_advanced_visualization(self, save_path=None):
        """Create an advanced visualization with quantum patterns."""
        if self.data is None:
            raise ValueError("No data loaded. Please load data first.")
            
        # Determine if we're working with hourly or minute data
        time_col = 'hour' if 'hour' in self.data.columns else 'timestamp'
        price_col = 'close' if 'close' in self.data.columns else 'price'
        
        # Create a figure with advanced layout
        fig = plt.figure(figsize=(16, 20))
        gs = gridspec.GridSpec(5, 4, figure=fig)
        
        # Price chart (spans the top row)
        price_ax = fig.add_subplot(gs[0, :])
        price_ax.plot(self.data[time_col], self.data[price_col], color='#F7931A', linewidth=2)
        price_ax.set_title('🔮 OMEGA BTC AI - Quantum-Entangled Price Evolution 🔮', fontsize=18)
        price_ax.set_ylabel('Price (USD)', fontsize=12)
        price_ax.grid(True, alpha=0.3)
        
        # Format x-axis with dates
        price_ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        price_ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.setp(price_ax.xaxis.get_majorticklabels(), rotation=45)
        
        # Quantum state heatmap (spans the second row)
        heat_ax = fig.add_subplot(gs[1, :])
        
        # Create a heatmap of quantum state over time
        # Use a custom colormap for quantum visualization
        quantum_cmap = LinearSegmentedColormap.from_list(
            'quantum', 
            ['#3a0b5b', '#5e14c5', '#a82cd1', '#cf3ba5', '#f05a7a', '#ff8c5c', '#ffc84d']
        )
        
        # Flatten quantum state to 2D array for visualization
        q_data = self.data['quantum_state'].values.reshape(1, -1)
        heat_ax.imshow(
            q_data, 
            aspect='auto', 
            cmap=quantum_cmap, 
            extent=[0, len(self.data), -1, 1]
        )
        heat_ax.set_title('Quantum Field Intensity', fontsize=14)
        heat_ax.set_yticks([])
        
        # Set x-ticks to match date range on price chart
        num_ticks = min(10, len(self.data))
        tick_indices = np.linspace(0, len(self.data)-1, num_ticks, dtype=int)
        heat_ax.set_xticks(tick_indices)
        heat_ax.set_xticklabels([
            self.data[time_col].iloc[i].strftime('%Y-%m-%d') 
            for i in tick_indices
        ], rotation=45)
        
        # Quantum resonance (spans third row left)
        resonance_ax = fig.add_subplot(gs[2, :2])
        if 'quantum_resonance' in self.data.columns:
            resonance_ax.plot(
                self.data[time_col], 
                self.data['quantum_resonance'].fillna(0),
                color='green', linewidth=2
            )
            resonance_ax.set_title('Quantum Resonance', fontsize=14)
            resonance_ax.set_ylabel('Resonance', fontsize=12)
            resonance_ax.grid(True, alpha=0.3)
            
            # Mark quantum phase transitions
            if hasattr(self, 'phase_transitions') and self.phase_transitions:
                for transition in self.phase_transitions:
                    resonance_ax.axvline(x=transition, color='red', linestyle='--', alpha=0.7)
                
                resonance_ax.text(
                    0.02, 0.02, 
                    "Red lines indicate quantum phase transitions",
                    transform=resonance_ax.transAxes,
                    bbox=dict(facecolor='white', alpha=0.8)
                )
        
        # Quantum wave interference (spans third row right)
        wave_ax = fig.add_subplot(gs[2, 2:])
        if 'quantum_wave' in self.data.columns:
            wave_ax.plot(
                self.data[time_col], 
                self.data['quantum_wave'],
                color='blue', linewidth=2
            )
            wave_ax.set_title('Quantum Wave Interference', fontsize=14)
            wave_ax.grid(True, alpha=0.3)
        
        # Quantum entanglement (fourth row)
        entangle_ax = fig.add_subplot(gs[3, :])
        if 'quantum_entanglement' in self.data.columns:
            entangle_ax.fill_between(
                self.data[time_col], 
                self.data['quantum_entanglement'].fillna(0),
                alpha=0.7, color='purple'
            )
            entangle_ax.set_title('Quantum Entanglement Strength', fontsize=14)
            entangle_ax.set_ylabel('Entanglement', fontsize=12)
            entangle_ax.grid(True, alpha=0.3)
        
        # Golden ratio harmonic analysis (bottom row)
        golden_ax = fig.add_subplot(gs[4, :])
        
        # Calculate price position relative to golden ratio levels
        min_price = self.data[price_col].min()
        max_price = self.data[price_col].max()
        price_range = max_price - min_price
        
        # Golden ratio levels
        levels = [
            min_price + price_range * (1 - 1/self.golden_ratio),  # 38.2%
            min_price + price_range * (1 - 1/self.golden_ratio**2),  # 61.8%
            min_price + price_range * (1 - 1/self.golden_ratio**3)   # 76.4%
        ]
        
        # Plot price again
        golden_ax.plot(self.data[time_col], self.data[price_col], color='#F7931A', linewidth=2)
        
        # Add golden ratio levels
        labels = ["38.2%", "61.8%", "76.4%"]
        colors = ["#6c5b7b", "#c06c84", "#f67280"]
        
        for level, label, color in zip(levels, labels, colors):
            golden_ax.axhline(y=level, color=color, linestyle='--', alpha=0.8, 
                             label=f"Golden Ratio {label}: ${level:,.0f}")
        
        golden_ax.set_title('Divine Proportions: Golden Ratio Analysis', fontsize=14)
        golden_ax.set_ylabel('Price (USD)', fontsize=12)
        golden_ax.set_xlabel('Date', fontsize=12)
        golden_ax.grid(True, alpha=0.3)
        golden_ax.legend()
        
        # Add watermark and metadata
        if self.metadata:
            metadata_text = (
                f"Initial Price: ${self.metadata.get('initial_price', 0):,.0f}\n"
                f"Target Price: ${self.metadata.get('target_price', 0):,.0f}\n"
                f"Simulation Days: {self.metadata.get('days_simulated', 0)}\n"
                f"Quantum Factor: {self.metadata.get('quantum_factor', 0):.2f}"
            )
            
            fig.text(0.02, 0.02, metadata_text, fontsize=10, 
                    bbox=dict(facecolor='white', alpha=0.8))
        
        # Add OMEGA BTC AI watermark
        fig.text(0.5, 0.01, "🔱 OMEGA BTC AI - Quantum Price Visualization 🔱", 
                 ha='center', fontsize=12, color='gray', alpha=0.7)
        
        plt.tight_layout()
        
        # Save if path provided
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            return save_path
            
        plt.show()
        return None

def process_simulation_data(data_file, metadata_file=None, output_dir="visualizations", advanced=True):
    """Process simulation data and create visualizations."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create timestamp for output files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Initialize visualizer
    visualizer = QuantumVisualizer(data_file, metadata_file)
    
    # Compute quantum metrics
    visualizer.compute_quantum_metrics()
    
    # Generate file paths
    simple_viz_path = f"{output_dir}/btc_quantum_simple_viz_{timestamp}.png"
    advanced_viz_path = f"{output_dir}/btc_quantum_advanced_viz_{timestamp}.png"
    
    # Create visualizations
    visualizer.create_simple_visualization(save_path=simple_viz_path)
    print(f"✅ Created simple visualization: {simple_viz_path}")
    
    if advanced:
        visualizer.create_advanced_visualization(save_path=advanced_viz_path)
        print(f"✅ Created advanced visualization: {advanced_viz_path}")
        
    return {
        "simple_visualization": simple_viz_path,
        "advanced_visualization": advanced_viz_path if advanced else None
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quantum Bitcoin Price Visualizer")
    parser.add_argument("--data", type=str, required=True, help="Path to simulation data CSV file")
    parser.add_argument("--metadata", type=str, help="Path to simulation metadata JSON file")
    parser.add_argument("--output", type=str, default="visualizations", help="Output directory for visualizations")
    parser.add_argument("--simple-only", action="store_true", help="Only create simple visualization")
    
    args = parser.parse_args()
    
    print("🔱 OMEGA BTC AI - Quantum Price Visualizer 🔱")
    print("=" * 50)
    print(f"Processing data file: {args.data}")
    if args.metadata:
        print(f"With metadata: {args.metadata}")
    print(f"Creating {'simple' if args.simple_only else 'simple and advanced'} visualizations")
    print(f"Output directory: {args.output}")
    print("=" * 50)
    
    # Process the data
    viz_paths = process_simulation_data(
        data_file=args.data,
        metadata_file=args.metadata,
        output_dir=args.output,
        advanced=not args.simple_only
    )
    
    print("\n✨ Visualization completed successfully!")
    print("Output files:")
    for key, path in viz_paths.items():
        if path:
            print(f"- {key}: {path}") 