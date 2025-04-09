#!/usr/bin/env python3
"""
Quantum Entanglement Analyzer
===========================

Implementation of quantum entanglement analysis methods for market data.
This module provides tools to analyze and detect critical market transitions
using quantum entanglement principles and correlation structures.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from enum import Enum
import logging
from typing import Dict, List, Tuple, Optional, Union, Any
from scipy.stats import entropy
from scipy.linalg import eigh
import networkx as nx
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("quantum-entanglement-analyzer")


class EntanglementMeasure(Enum):
    """Types of quantum entanglement measures."""
    VON_NEUMANN_ENTROPY = "von_neumann_entropy"
    MUTUAL_INFORMATION = "mutual_information"
    CONCURRENCE = "concurrence"
    NEGATIVITY = "negativity"
    SCHMIDT_NUMBER = "schmidt_number"
    QUANTUM_DISCORD = "quantum_discord"
    ENTANGLEMENT_WITNESS = "entanglement_witness"


class MarketTransitionType(Enum):
    """Types of market transitions that can be detected."""
    NORMAL = "normal"
    CRITICAL = "critical"
    REGIME_SHIFT = "regime_shift"
    VOLATILITY_BURST = "volatility_burst"
    CORRELATION_BREAKDOWN = "correlation_breakdown"
    EARLY_WARNING = "early_warning"
    UNSTABLE = "unstable"


class QuantumEntanglementAnalyzer:
    """
    Analyzes market data using quantum entanglement measures.
    
    This class implements methods to compute entanglement measures between
    market variables and detect critical market transitions based on
    changes in the entanglement structure.
    """
    
    def __init__(self, window_size: int = 30, overlap: int = 5, 
                entanglement_threshold: float = 0.6,
                warning_threshold: float = 0.75,
                critical_threshold: float = 0.9):
        """
        Initialize the quantum entanglement analyzer.
        
        Args:
            window_size: Size of the rolling window for analysis
            overlap: Overlap between consecutive windows
            entanglement_threshold: Threshold for significant entanglement
            warning_threshold: Threshold for early warning signals
            critical_threshold: Threshold for critical transitions
        """
        self.window_size = window_size
        self.overlap = overlap
        self.entanglement_threshold = entanglement_threshold
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
        
        # Storage for analysis results
        self.density_matrices = {}
        self.entanglement_measures = {}
        self.transition_signals = {}
        self.feature_names = []
        
        logger.info(f"Initialized Quantum Entanglement Analyzer with window_size={window_size}, "
                   f"entanglement_threshold={entanglement_threshold}")
    
    def prepare_data(self, data: Union[np.ndarray, pd.DataFrame], 
                    feature_names: Optional[List[str]] = None) -> np.ndarray:
        """
        Prepare market data for quantum entanglement analysis.
        
        Args:
            data: Input market data (samples x features)
            feature_names: Optional list of feature names
            
        Returns:
            Prepared data as numpy array
        """
        # Convert to numpy array if pandas DataFrame
        if isinstance(data, pd.DataFrame):
            if feature_names is None:
                feature_names = data.columns.tolist()
            data = data.values
        
        # Store feature names
        self.feature_names = feature_names if feature_names is not None else [f"F{i}" for i in range(data.shape[1])]
        
        # Ensure 2D data
        if len(data.shape) == 1:
            data = data.reshape(-1, 1)
        
        # Normalize data
        normalized_data = np.zeros_like(data, dtype=float)
        for i in range(data.shape[1]):
            column = data[:, i]
            min_val = np.min(column)
            max_val = np.max(column)
            # Handle constant values
            if max_val == min_val:
                normalized_data[:, i] = 0.5  # Set to middle value
            else:
                normalized_data[:, i] = (column - min_val) / (max_val - min_val)
        
        logger.info(f"Prepared data with shape {data.shape}, features: {self.feature_names}")
        return normalized_data
    
    def compute_density_matrix(self, data: np.ndarray, start_idx: int, 
                              end_idx: int) -> np.ndarray:
        """
        Compute density matrix for a window of data.
        
        Args:
            data: Normalized market data
            start_idx: Start index of window
            end_idx: End index of window
            
        Returns:
            Density matrix representing quantum state
        """
        # Extract window data
        window_data = data[start_idx:end_idx, :]
        
        # Compute correlation matrix
        corr_matrix = np.corrcoef(window_data, rowvar=False)
        
        # Handle NaN values that might arise from constant features
        corr_matrix = np.nan_to_num(corr_matrix, nan=0.0)
        
        # Transform correlation to density matrix
        # Ensure positive semi-definiteness
        eigvals, eigvecs = eigh(corr_matrix)
        eigvals = np.maximum(eigvals, 0)  # Make sure eigenvalues are non-negative
        
        # Normalize to have trace = 1
        trace = np.sum(eigvals)
        if trace > 0:
            eigvals = eigvals / trace
        else:
            # If all eigenvalues are 0 (unlikely), create identity/maximally mixed state
            n_features = corr_matrix.shape[0]
            return np.eye(n_features) / n_features
        
        # Reconstruct density matrix
        density_matrix = eigvecs @ np.diag(eigvals) @ eigvecs.T
        
        return density_matrix
    
    def compute_entanglement_measure(self, density_matrix: np.ndarray, 
                                   measure: EntanglementMeasure,
                                   subsystems: Optional[List[List[int]]] = None) -> float:
        """
        Compute specified entanglement measure for a density matrix.
        
        Args:
            density_matrix: Quantum density matrix
            measure: Type of entanglement measure to compute
            subsystems: Optional list of subsystems for bipartite measures
            
        Returns:
            Computed entanglement measure
        """
        # Define subsystems if not provided
        if subsystems is None:
            n = density_matrix.shape[0]
            # Default: split features in half for bipartite entanglement
            mid = n // 2
            subsystems = [[i for i in range(mid)], [i for i in range(mid, n)]]
        
        if measure == EntanglementMeasure.VON_NEUMANN_ENTROPY:
            # Compute von Neumann entropy: S(ρ) = -Tr(ρ log ρ)
            eigvals = np.linalg.eigvalsh(density_matrix)
            eigvals = eigvals[eigvals > 0]  # Remove zeros (log(0) undefined)
            return -np.sum(eigvals * np.log2(eigvals))
            
        elif measure == EntanglementMeasure.MUTUAL_INFORMATION:
            # Compute quantum mutual information between subsystems
            # I(A:B) = S(ρA) + S(ρB) - S(ρAB)
            if len(subsystems) != 2:
                raise ValueError("Mutual information requires exactly 2 subsystems")
                
            subsystem_A = subsystems[0]
            subsystem_B = subsystems[1]
            
            # Reduced density matrices
            rho_A = self._partial_trace(density_matrix, keep=subsystem_A)
            rho_B = self._partial_trace(density_matrix, keep=subsystem_B)
            
            # Compute entropies
            S_A = self.compute_entanglement_measure(rho_A, EntanglementMeasure.VON_NEUMANN_ENTROPY)
            S_B = self.compute_entanglement_measure(rho_B, EntanglementMeasure.VON_NEUMANN_ENTROPY)
            S_AB = self.compute_entanglement_measure(density_matrix, EntanglementMeasure.VON_NEUMANN_ENTROPY)
            
            return S_A + S_B - S_AB
            
        elif measure == EntanglementMeasure.NEGATIVITY:
            # Simplified negativity - measure of entanglement based on negative eigenvalues
            # after partial transpose
            eigvals = np.linalg.eigvalsh(density_matrix)
            return np.sum(np.abs(eigvals[eigvals < 0]))
            
        elif measure == EntanglementMeasure.ENTANGLEMENT_WITNESS:
            # Simple entanglement witness based on correlation structure
            # Higher absolute correlations indicate more entanglement
            n = density_matrix.shape[0]
            witness_value = 0.0
            
            for i in range(n):
                for j in range(i+1, n):
                    # Use off-diagonal elements as indicator of correlations
                    witness_value += abs(density_matrix[i, j])
            
            # Normalize by number of pairs
            n_pairs = (n * (n - 1)) / 2
            if n_pairs > 0:
                witness_value /= n_pairs
                
            return witness_value
            
        else:
            logger.warning(f"Entanglement measure {measure} not implemented, using witness")
            return self.compute_entanglement_measure(density_matrix, EntanglementMeasure.ENTANGLEMENT_WITNESS)
    
    def _partial_trace(self, density_matrix: np.ndarray, keep: List[int]) -> np.ndarray:
        """
        Compute partial trace of density matrix, keeping specified subsystems.
        
        Args:
            density_matrix: Full system density matrix
            keep: Indices of subsystems to keep
            
        Returns:
            Reduced density matrix
        """
        n = density_matrix.shape[0]
        
        # For simplicity, we'll implement a basic version that works with correlation matrices
        # This is an approximation of the actual quantum partial trace
        
        # Extract submatrix of kept systems
        reduced = density_matrix[np.ix_(keep, keep)]
        
        # Renormalize to trace = 1
        trace = np.trace(reduced)
        if trace > 0:
            reduced = reduced / trace
            
        return reduced
    
    def analyze_entanglement(self, data: Union[np.ndarray, pd.DataFrame], 
                           feature_names: Optional[List[str]] = None, 
                           measure: EntanglementMeasure = EntanglementMeasure.ENTANGLEMENT_WITNESS) -> Dict[str, Any]:
        """
        Analyze quantum entanglement in market data.
        
        Args:
            data: Market data to analyze
            feature_names: Optional feature names
            measure: Entanglement measure to use
            
        Returns:
            Dictionary with analysis results
        """
        # Prepare data
        prepared_data = self.prepare_data(data, feature_names)
        n_samples, n_features = prepared_data.shape
        
        # Determine windows
        step_size = self.window_size - self.overlap
        n_windows = max(1, (n_samples - self.window_size) // step_size + 1)
        
        # Initialize results storage
        self.density_matrices = {}
        self.entanglement_measures = {measure.value: []}
        
        logger.info(f"Analyzing {n_samples} samples with {n_windows} windows")
        
        # Analyze each window
        for window in range(n_windows):
            start_idx = window * step_size
            end_idx = start_idx + self.window_size
            
            if end_idx > n_samples:
                end_idx = n_samples
            
            # Compute density matrix
            window_key = f"window_{window}"
            self.density_matrices[window_key] = self.compute_density_matrix(
                prepared_data, start_idx, end_idx
            )
            
            # Compute entanglement measure
            entanglement_value = self.compute_entanglement_measure(
                self.density_matrices[window_key], measure
            )
            self.entanglement_measures[measure.value].append(entanglement_value)
            
            logger.debug(f"Window {window}: {start_idx}-{end_idx}, entanglement={entanglement_value:.4f}")
        
        # Detect transitions
        self.detect_transitions(measure)
        
        # Return results
        result = {
            "entanglement_measures": self.entanglement_measures,
            "transition_signals": self.transition_signals,
            "feature_names": self.feature_names,
            "window_size": self.window_size,
            "measure": measure.value,
            "n_windows": n_windows
        }
        
        logger.info(f"Completed entanglement analysis using {measure.value}")
        
        return result
    
    def detect_transitions(self, measure: EntanglementMeasure) -> Dict[str, List[Tuple[int, MarketTransitionType, float]]]:
        """
        Detect critical transitions based on entanglement measures.
        
        Args:
            measure: Entanglement measure used in analysis
            
        Returns:
            Dictionary with detected transitions
        """
        measure_values = self.entanglement_measures.get(measure.value, [])
        if not measure_values:
            logger.warning(f"No entanglement measures available for {measure.value}")
            return {}
        
        # Initialize transitions dictionary
        self.transition_signals = {}
        
        # Compute difference between consecutive measures
        diffs = np.diff(measure_values)
        mean_diff = np.mean(np.abs(diffs))
        std_diff = np.std(diffs)
        
        # Detect significant changes
        transitions = []
        for i in range(len(diffs)):
            window_idx = i + 1  # +1 because diffs is one shorter than measure_values
            current_value = measure_values[window_idx]
            change = diffs[i]
            
            # Determine transition type based on magnitude and direction of change
            if abs(change) > self.critical_threshold * std_diff:
                # Critical transition
                if change > 0:
                    # Sudden increase in entanglement
                    transition_type = MarketTransitionType.CRITICAL
                else:
                    # Sudden decrease in entanglement
                    transition_type = MarketTransitionType.CORRELATION_BREAKDOWN
                    
                transitions.append((window_idx, transition_type, current_value))
                
            elif abs(change) > self.warning_threshold * std_diff:
                # Warning signal
                if change > 0:
                    transition_type = MarketTransitionType.EARLY_WARNING
                else:
                    transition_type = MarketTransitionType.UNSTABLE
                    
                transitions.append((window_idx, transition_type, current_value))
                
            elif current_value > self.entanglement_threshold:
                # High but stable entanglement - potential regime shift
                if i > 0 and all(v > self.entanglement_threshold for v in measure_values[max(0, window_idx-3):window_idx+1]):
                    transition_type = MarketTransitionType.REGIME_SHIFT
                    transitions.append((window_idx, transition_type, current_value))
            
            # Volatility burst detection
            if i >= 2:
                recent_volatility = np.std(measure_values[max(0, window_idx-5):window_idx+1])
                overall_volatility = np.std(measure_values[:window_idx+1])
                
                if recent_volatility > 2 * overall_volatility:
                    transition_type = MarketTransitionType.VOLATILITY_BURST
                    transitions.append((window_idx, transition_type, current_value))
        
        # Store transitions
        self.transition_signals[measure.value] = transitions
        
        # Log results
        n_transitions = len(transitions)
        logger.info(f"Detected {n_transitions} transitions using {measure.value}")
        for window_idx, transition_type, value in transitions:
            logger.info(f"  Window {window_idx}: {transition_type.value} (value={value:.4f})")
        
        return self.transition_signals
    
    def visualize_entanglement(self, figsize: Tuple[int, int] = (12, 8)) -> plt.Figure:
        """
        Visualize entanglement measures and detected transitions.
        
        Args:
            figsize: Figure size (width, height)
            
        Returns:
            Matplotlib figure
        """
        # Create figure
        fig, axes = plt.subplots(2, 1, figsize=figsize)
        
        # Plot entanglement measures
        ax1 = axes[0]
        for measure_name, values in self.entanglement_measures.items():
            windows = range(len(values))
            ax1.plot(windows, values, label=measure_name, marker='o', markersize=4)
        
        # Add threshold lines
        ax1.axhline(y=self.entanglement_threshold, color='gray', linestyle='--', alpha=0.5, label='Entanglement Threshold')
        
        ax1.set_title('Quantum Entanglement Analysis')
        ax1.set_xlabel('Window Index')
        ax1.set_ylabel('Entanglement Measure')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Plot transitions
        ax2 = axes[1]
        colors = {
            MarketTransitionType.CRITICAL: 'red',
            MarketTransitionType.CORRELATION_BREAKDOWN: 'blue',
            MarketTransitionType.EARLY_WARNING: 'orange',
            MarketTransitionType.REGIME_SHIFT: 'purple',
            MarketTransitionType.VOLATILITY_BURST: 'green',
            MarketTransitionType.UNSTABLE: 'darkred',
            MarketTransitionType.NORMAL: 'gray'
        }
        
        # Plot each transition type
        for measure_name, transitions in self.transition_signals.items():
            for window_idx, transition_type, value in transitions:
                color = colors.get(transition_type, 'black')
                ax2.scatter(window_idx, value, color=color, s=100, label=transition_type.value)
                
                # Add vertical line to top plot
                ax1.axvline(x=window_idx, color=color, alpha=0.3)
        
        # Add entanglement measure line to transition plot
        for measure_name, values in self.entanglement_measures.items():
            windows = range(len(values))
            ax2.plot(windows, values, color='gray', alpha=0.5)
        
        ax2.set_title('Detected Market Transitions')
        ax2.set_xlabel('Window Index')
        ax2.set_ylabel('Transition Signal Strength')
        ax2.grid(True, alpha=0.3)
        
        # Create custom legend for transition types
        handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=ttype.value)
                  for ttype, color in colors.items()]
        ax2.legend(handles=handles, title="Transition Types", loc='best')
        
        plt.tight_layout()
        return fig
    
    def compute_entanglement_graph(self, density_matrix: np.ndarray, 
                                  threshold: float = 0.3) -> nx.Graph:
        """
        Create a graph representing entanglement structure.
        
        Args:
            density_matrix: Quantum density matrix
            threshold: Minimum entanglement for edge creation
            
        Returns:
            NetworkX graph of entanglement
        """
        n_features = density_matrix.shape[0]
        G = nx.Graph()
        
        # Add nodes
        for i in range(n_features):
            feature_name = self.feature_names[i] if i < len(self.feature_names) else f"F{i}"
            G.add_node(i, name=feature_name)
        
        # Add edges based on entanglement
        for i in range(n_features):
            for j in range(i+1, n_features):
                # Use absolute value of density matrix element as entanglement measure
                entanglement = abs(density_matrix[i, j])
                if entanglement > threshold:
                    G.add_edge(i, j, weight=entanglement)
        
        return G
    
    def visualize_entanglement_network(self, window_index: int = -1, figsize: Tuple[int, int] = (10, 8)) -> plt.Figure:
        """
        Visualize the entanglement network between market variables.
        
        Args:
            window_index: Window index to visualize (-1 for last window)
            figsize: Figure size
            
        Returns:
            Matplotlib figure
        """
        if not self.density_matrices:
            raise ValueError("No density matrices available. Run analyze_entanglement first.")
        
        # Get density matrix for specified window
        window_keys = list(self.density_matrices.keys())
        if window_index < 0:
            window_index = len(window_keys) + window_index
        
        if window_index < 0 or window_index >= len(window_keys):
            raise ValueError(f"Window index {window_index} out of bounds (0 to {len(window_keys)-1})")
        
        window_key = window_keys[window_index]
        density_matrix = self.density_matrices[window_key]
        
        # Create graph
        G = self.compute_entanglement_graph(density_matrix)
        
        # Create figure
        fig, ax = plt.subplots(figsize=figsize)
        
        # Define positions - circular layout
        pos = nx.circular_layout(G)
        
        # Get edge weights for line thickness
        edge_weights = [G[u][v]['weight'] * 3 for u, v in G.edges()]
        
        # Node colors based on degree centrality
        centrality = nx.degree_centrality(G)
        node_colors = [centrality[n] for n in G.nodes()]
        
        # Draw graph
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=700, alpha=0.8, cmap=plt.cm.viridis, ax=ax)
        nx.draw_networkx_edges(G, pos, width=edge_weights, alpha=0.5, edge_color='gray', ax=ax)
        
        # Add labels
        labels = {n: G.nodes[n]['name'] for n in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, ax=ax)
        
        ax.set_title(f"Quantum Entanglement Network (Window {window_index})")
        ax.axis('off')
        
        return fig

    def get_early_warning_signals(self, lookback: int = 5) -> List[Tuple[int, str, float]]:
        """
        Get early warning signals for potential market transitions.
        
        Args:
            lookback: Number of recent windows to analyze
            
        Returns:
            List of (window_index, signal_type, strength) tuples
        """
        # Collect all early warning signals
        warnings = []
        
        for measure_name, transitions in self.transition_signals.items():
            for window_idx, transition_type, value in transitions:
                if transition_type == MarketTransitionType.EARLY_WARNING:
                    warnings.append((window_idx, f"{measure_name}_{transition_type.value}", value))
        
        # Sort by window index
        warnings.sort(key=lambda x: x[0])
        
        # Filter to get only recent warnings if requested
        if lookback > 0 and warnings:
            max_window = max(w[0] for w in warnings)
            warnings = [w for w in warnings if w[0] > max_window - lookback]
        
        return warnings
    
    def get_instability_index(self, recent_windows: int = 10) -> float:
        """
        Calculate market instability index based on entanglement analysis.
        
        Args:
            recent_windows: Number of recent windows to consider
            
        Returns:
            Instability index (0-1)
        """
        # Need entanglement measures
        if not self.entanglement_measures:
            return 0.0
        
        # Get most recent entanglement values
        measure_values = next(iter(self.entanglement_measures.values()))
        if not measure_values:
            return 0.0
            
        # Consider only recent windows
        recent_values = measure_values[-min(recent_windows, len(measure_values)):]
        
        # Calculate metrics for instability:
        # 1. Volatility of entanglement measures
        volatility = np.std(recent_values) if len(recent_values) > 1 else 0
        
        # 2. Trend - increasing entanglement can indicate approaching transition
        trend = 0
        if len(recent_values) > 1:
            trend = np.mean(np.diff(recent_values))
        
        # 3. Level - high absolute entanglement
        level = np.mean(recent_values) / self.entanglement_threshold if self.entanglement_threshold > 0 else 0
        
        # 4. Count warning signals
        warnings = self.get_early_warning_signals(recent_windows)
        warning_factor = len(warnings) / recent_windows if recent_windows > 0 else 0
        
        # Combine factors with weights
        weights = [0.3, 0.2, 0.3, 0.2]  # Volatility, Trend, Level, Warnings
        factors = [min(1.0, volatility * 5), min(1.0, abs(trend) * 10), min(1.0, level), warning_factor]
        
        instability = sum(w * f for w, f in zip(weights, factors))
        
        # Ensure in [0, 1] range
        instability = max(0.0, min(1.0, instability))
        
        return instability 