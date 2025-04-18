#!/usr/bin/env python3

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
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
Power Method BTC Eigenwaves
==========================

Implements the power method for finding dominant eigenvalues/eigenvectors in BTC price data.
Uses matrix-based approach to identify key market cycles and oscillation patterns.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple, Any, Union
import os
import json
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle

class PowerMethodBTCEigenwaves:
    """Implements the power method for finding dominant eigenvectors in BTC price waves."""
    
    def __init__(self, n_components=3):
        self.n_components = n_components
        self.eigenvectors = None
        self.eigenvalues = None
        self.model_path = None
        self.price_matrix = None
        self.projections = None
        self.feature_columns = ['close', 'high', 'low']
        self.df_with_eigenwaves = None
        
    def fit(self, df):
        """Fit the eigenwave model to the data."""
        # Create price matrix
        price_matrix = self._create_price_matrix(df)
        
        # Compute correlation matrix
        correlation_matrix = self._compute_correlation_matrix(price_matrix)
        
        # Apply power method
        self.eigenvectors, self.eigenvalues = self._power_method(correlation_matrix)
        
        return self
        
    def _create_price_matrix(self, df):
        """Create price matrix from DataFrame."""
        # Extract price features
        features = df[['close', 'high', 'low']].values
        
        # Normalize features
        features = (features - np.mean(features, axis=0)) / np.std(features, axis=0)
        
        return features
        
    def _compute_correlation_matrix(self, price_matrix):
        """Compute correlation matrix from price matrix."""
        # Ensure price_matrix is a numpy array
        price_matrix = np.array(price_matrix)
        
        # Compute correlation matrix
        correlation_matrix = np.corrcoef(price_matrix.T)
        
        return correlation_matrix
        
    def _power_method(self, matrix, max_iter=1000, tol=1e-6):
        """Apply power method to find eigenvalues and eigenvectors."""
        n = matrix.shape[0]
        eigenvectors = np.zeros((n, self.n_components))
        eigenvalues = np.zeros(self.n_components)
        
        for i in range(self.n_components):
            # Initialize random vector
            v = np.random.randn(n)
            v = v / np.linalg.norm(v)
            
            for _ in range(max_iter):
                v_old = v
                v = matrix @ v
                v = v / np.linalg.norm(v)
                
                if np.abs(np.dot(v, v_old) - 1) < tol:
                    break
                    
            eigenvectors[:, i] = v
            eigenvalues[i] = np.dot(v, matrix @ v)
            
            # Deflate matrix
            matrix = matrix - eigenvalues[i] * np.outer(v, v)
            
        return eigenvectors, eigenvalues
        
    def get_projections(self, df):
        """Get eigenwave projections for input data."""
        if self.eigenvectors is None:
            raise ValueError("Model must be fitted before getting projections")
            
        price_matrix = self._create_price_matrix(df)
        projections = price_matrix @ self.eigenvectors
        
        return pd.DataFrame(projections, columns=[f'eigenwave_{i+1}' for i in range(self.n_components)])
        
    def save_model(self, filepath):
        """Save the model to a file."""
        model_data = {
            'eigenvectors': self.eigenvectors,
            'eigenvalues': self.eigenvalues,
            'n_components': self.n_components
        }
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        self.model_path = filepath
        
    def load_model(self, filepath):
        """Load the model from a file."""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        self.eigenvectors = model_data['eigenvectors']
        self.eigenvalues = model_data['eigenvalues']
        self.n_components = model_data['n_components']
        self.model_path = filepath
        
    def analyze(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze BTC price data with power method to find eigenwaves.
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            DataFrame with eigenwave features added
        """
        # Create price matrix
        price_matrix = self._create_price_matrix(df)
        
        # Compute correlation matrix
        correlation_matrix = self._compute_correlation_matrix(price_matrix)
        
        # Apply power method
        self.eigenvectors, self.eigenvalues = self._power_method(correlation_matrix)
        
        # Project prices onto eigenvectors
        projections = price_matrix @ self.eigenvectors
        self.projections = projections
        
        # Add projections to dataframe
        df_result = df.copy()
        for i in range(self.n_components):
            df_result[f'eigenwave_{i+1}'] = projections[:, i]
            
        # Calculate eigenwave momentum (rate of change)
        for i in range(self.n_components):
            df_result[f'eigenwave_{i+1}_momentum'] = df_result[f'eigenwave_{i+1}'].diff()
            
        # Calculate dominant wave
        wave_columns = [f'eigenwave_{i+1}' for i in range(self.n_components)]
        df_result['dominant_wave'] = df_result[wave_columns].abs().idxmax(axis=1)
        
        # Store processed dataframe
        self.df_with_eigenwaves = df_result
        
        print(f"Power method analysis complete with {self.n_components} eigenwaves")
        
        return df_result
        
    def save_results(self, output_file: str = "results/btc_eigenwaves.csv") -> None:
        """
        Save eigenwave results to CSV file.
        
        Args:
            output_file: Path to save CSV file
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Save eigenvalues and eigenvectors
        eigenwave_data = {
            "eigenvalues": self.eigenvalues.tolist() if self.eigenvalues is not None else None,
            "eigenvectors": self.eigenvectors.tolist() if self.eigenvectors is not None else None,
            "feature_columns": self.feature_columns,
            "n_components": self.n_components
        }
        
        # Save as JSON
        with open("results/eigenwave_data.json", "w") as f:
            json.dump(eigenwave_data, f, indent=2)
            
        print(f"Eigenwave data saved to results/eigenwave_data.json")
        
        # Save projections to CSV if available
        if self.df_with_eigenwaves is not None:
            # Select only necessary columns
            df_to_save = self.df_with_eigenwaves[['date' if 'date' in self.df_with_eigenwaves.columns else 'timestamp'] + 
                                              [f'eigenwave_{i+1}' for i in range(self.n_components)] +
                                              [f'eigenwave_{i+1}_momentum' for i in range(self.n_components)] +
                                              ['dominant_wave']].copy()
            
            # Save to CSV
            df_to_save.to_csv(output_file, index=False)
            print(f"Eigenwave projections saved to {output_file}")
        else:
            print("No eigenwave projections to save")
            
    def visualize_eigenwaves(self, output_file: str = "plots/btc_eigenwaves_projections.html") -> None:
        """
        Create interactive visualization of eigenwaves.
        
        Args:
            output_file: Path to save HTML visualization
        """
        if self.df_with_eigenwaves is None:
            print("No eigenwave data to visualize")
            return
            
        # Create figure with subplots
        fig = make_subplots(rows=self.n_components + 1, cols=1,
                          subplot_titles=['BTC Price'] + 
                                        [f'Eigenwave {i+1} (λ={self.eigenvalues[i]:.4f})' 
                                         for i in range(self.n_components)],
                          vertical_spacing=0.08)
        
        # Add BTC price
        fig.add_trace(
            go.Scatter(x=self.df_with_eigenwaves['date'] if 'date' in self.df_with_eigenwaves.columns else pd.to_datetime(self.df_with_eigenwaves.index),
                     y=self.df_with_eigenwaves['close'],
                     mode='lines',
                     name='BTC Price',
                     line=dict(color='gold', width=1.5)),
            row=1, col=1
        )
        
        # Add eigenwaves
        colors = ['rgba(255,0,0,0.8)', 'rgba(0,128,0,0.8)', 'rgba(0,0,255,0.8)']
        for i in range(min(self.n_components, 3)):
            fig.add_trace(
                go.Scatter(x=self.df_with_eigenwaves['date'] if 'date' in self.df_with_eigenwaves.columns else pd.to_datetime(self.df_with_eigenwaves.index),
                         y=self.df_with_eigenwaves[f'eigenwave_{i+1}'],
                         mode='lines',
                         name=f'Eigenwave {i+1}',
                         line=dict(color=colors[i], width=1.5)),
                row=i+2, col=1
            )
            
            # Add momentum as dotted line
            fig.add_trace(
                go.Scatter(x=self.df_with_eigenwaves['date'] if 'date' in self.df_with_eigenwaves.columns else pd.to_datetime(self.df_with_eigenwaves.index),
                         y=self.df_with_eigenwaves[f'eigenwave_{i+1}_momentum'],
                         mode='lines',
                         name=f'Momentum {i+1}',
                         line=dict(color=colors[i], width=1, dash='dot')),
                row=i+2, col=1
            )
        
        # Update layout
        fig.update_layout(
            title_text="BTC Eigenwave Analysis",
            template="plotly_dark",
            height=200 * (self.n_components + 1),
            width=1000,
            showlegend=True
        )
        
        # Save figure
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        fig.write_html(output_file)
        print(f"Eigenwave visualization saved to {output_file}")
        
        return fig
        
def main():
    """Run power method analysis on BTC data."""
    # Create sample data
    np.random.seed(42)
    dates = pd.date_range(start='2020-01-01', periods=1000, freq='D')
    
    # Generate random walk for close prices
    close = 10000 + np.cumsum(np.random.normal(0, 200, 1000))
    
    # Generate open, high, low based on close
    open_prices = close * (1 + np.random.normal(0, 0.01, 1000))
    high = np.maximum(close, open_prices) * (1 + np.abs(np.random.normal(0, 0.01, 1000)))
    low = np.minimum(close, open_prices) * (1 - np.abs(np.random.normal(0, 0.01, 1000)))
    
    # Generate volume
    volume = np.random.lognormal(10, 1, 1000)
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': dates,
        'open': open_prices,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    })
    
    # Create and run power method
    power_method = PowerMethodBTCEigenwaves()
    df_with_eigenwaves = power_method.analyze(df)
    
    # Save results
    power_method.save_results()
    
    # Visualize
    power_method.visualize_eigenwaves()
    
if __name__ == "__main__":
    main() 