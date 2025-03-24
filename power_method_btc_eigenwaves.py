#!/usr/bin/env python3
"""
OMEGA BTC AI - Power Method BTC Eigenwave Detector
=================================================

Implementation of the Power Method algorithm to detect leading eigenvectors (eigenwaves)
from rolling covariance matrices of BTC price movements.

This divine tool reveals the dominant price movement patterns (eigenwaves) that 
govern Bitcoin's sacred price trajectory, including their stability and cyclical nature.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.io as pio
import os
import warnings
from datetime import datetime, timedelta
from tqdm import tqdm
from sklearn.preprocessing import StandardScaler
import seaborn as sns

# Try to import the HMM BTC State Mapper for data loading
try:
    from hmm_btc_state_mapper import load_btc_data, COLORS
except ImportError:
    # Define our own data loading function if import fails
    def load_btc_data(filepath_or_url=None, start_date=None, end_date=None):
        """Load BTC price data from a file or download it."""
        try:
            import yfinance as yf
            print("Downloading BTC data from yfinance...")
            data = yf.download(
                'BTC-USD',
                start=start_date if start_date else '2020-01-01',
                end=end_date if end_date else datetime.now().strftime('%Y-%m-%d'),
                interval='1d'
            )
            
            if data is None or data.empty:
                print("Failed to download data from yfinance or data is empty")
                return None
                
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
            
            data.columns = [str(c).lower() for c in data.columns]
            data = data.reset_index()
            data = data.rename(columns={'date': 'date', 'open': 'open', 'high': 'high', 
                                       'low': 'low', 'close': 'close', 'volume': 'volume'})
            return data
        except ImportError:
            print("yfinance not installed. Please install it with: pip install yfinance")
            return None
    
    # Define our own colors if import fails
    COLORS = {
        'background': '#0d1117',
        'text': '#c9d1d9',
        'grid': '#21262d',
        'primary': '#58a6ff',
        'secondary': '#bc8cff',
        'accent': '#f0883e',
        'positive': '#3fb950',
        'negative': '#f85149',
        'neutral': '#8b949e',
        'highlight': '#ffffff',
        'state_0': '#e6194B',  # Markdown/Bear
        'state_1': '#3cb44b',  # Markup/Bull
        'state_2': '#ffe119',  # Accumulation
        'state_3': '#4363d8',  # Distribution
        'state_4': '#911eb4',  # Fakeout/Liquidity Grab
        'state_5': '#f58231',  # Consolidation
        # Add eigenwave colors using the same colors as states
        'wave_0': '#e6194B',  # First eigenwave (red)
        'wave_1': '#3cb44b',  # Second eigenwave (green)
        'wave_2': '#ffe119',  # Third eigenwave (yellow)
        'wave_3': '#4363d8',  # Fourth eigenwave (blue)
        'wave_4': '#911eb4',  # Fifth eigenwave (purple)
        'wave_5': '#f58231'   # Sixth eigenwave (orange)
    }

# Set Plotly theme to a divine dark template
pio.templates.default = "plotly_dark"

# Suppress warnings
warnings.filterwarnings("ignore")

class PowerMethodBTCEigenwaves:
    """Power Method implementation for BTC eigenwave detection."""
    
    def __init__(self, window_size=30, n_eigenwaves=3, rolling_step=1, max_iterations=1000, tolerance=1e-6):
        """
        Initialize the Power Method BTC Eigenwave Detector.
        
        Args:
            window_size: Size of rolling window for covariance matrix (days)
            n_eigenwaves: Number of leading eigenwaves to extract
            rolling_step: Step size for rolling windows
            max_iterations: Maximum iterations for Power Method convergence
            tolerance: Convergence tolerance for Power Method
        """
        self.window_size = window_size
        self.n_eigenwaves = n_eigenwaves
        self.rolling_step = rolling_step
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.scaler = StandardScaler()
        self.feature_names = []
        
    def _prepare_features(self, df, return_df=False):
        """
        Prepare and engineer features from price and volume data.
        
        Args:
            df: DataFrame with OHLCV data at minimum
            return_df: If True, return the full DataFrame with all features
            
        Returns:
            Numpy array of features for covariance analysis and optionally the full DataFrame
        """
        # Deep copy to avoid modifying original
        data = df.copy()
        
        # Basic features
        data['returns'] = data['close'].pct_change()
        data['log_returns'] = np.log(data['close'] / data['close'].shift(1))
        data['high_log_returns'] = np.log(data['high'] / data['high'].shift(1))
        data['low_log_returns'] = np.log(data['low'] / data['low'].shift(1))
        data['volatility'] = data['log_returns'].rolling(window=20).std()
        data['volume_change'] = data['volume'].pct_change()
        
        # Price momentum features
        for period in [3, 5, 8, 13, 21, 34]:
            data[f'momentum_{period}d'] = data['close'].pct_change(periods=period)
        
        # Volume momentum features
        for period in [3, 5, 8, 13, 21]:
            data[f'volume_momentum_{period}d'] = data['volume'].pct_change(periods=period)
        
        # Price range features
        data['daily_range'] = (data['high'] - data['low']) / data['low']
        data['range_ma5'] = data['daily_range'].rolling(window=5).mean()
        data['range_ma21'] = data['daily_range'].rolling(window=21).mean()
        
        # Drop NaN values
        data = data.dropna()
        
        # Feature selection for eigenwave analysis
        selected_features = [
            'log_returns', 'high_log_returns', 'low_log_returns', 
            'volume_change', 'daily_range',
            'momentum_3d', 'momentum_5d', 'momentum_8d', 'momentum_13d', 'momentum_21d', 'momentum_34d',
            'volume_momentum_3d', 'volume_momentum_5d', 'volume_momentum_8d', 'volume_momentum_13d', 'volume_momentum_21d'
        ]
        self.feature_names = selected_features
        
        # Scale features
        features = self.scaler.fit_transform(data[selected_features])
        
        if return_df:
            return features, data
        else:
            return features, data.index
    
    def _power_method(self, matrix, n_vectors=1, max_iter=None, tol=None):
        """
        Extract the n leading eigenvectors and eigenvalues using the Power Method.
        
        Args:
            matrix: Covariance matrix
            n_vectors: Number of eigenvectors to extract
            max_iter: Maximum iterations (use instance value if None)
            tol: Convergence tolerance (use instance value if None)
            
        Returns:
            List of eigenvalues and eigenvectors
        """
        max_iter = max_iter if max_iter is not None else self.max_iterations
        tol = tol if tol is not None else self.tolerance
        
        # Get matrix dimensions
        n = matrix.shape[0]
        
        # Initialize storage for eigenvalues and eigenvectors
        eigenvalues = []
        eigenvectors = []
        
        # Make copy of matrix for deflation
        A = matrix.copy()
        
        for i in range(n_vectors):
            # Initialize random vector
            v = np.random.rand(n)
            v = v / np.linalg.norm(v)
            
            # Initialize eigenvalue in case loop exits early
            eigenvalue = 0.0
            
            # Iterate until convergence
            for j in range(max_iter):
                # Power iteration
                v_new = A @ v
                
                # Normalize the vector
                v_new_norm = np.linalg.norm(v_new)
                
                # Check for zero norm (happens with deflated matrices)
                if v_new_norm < tol:
                    # Generate a new random vector orthogonal to previous eigenvectors
                    v_new = np.random.rand(n)
                    for w in eigenvectors:
                        v_new = v_new - np.dot(v_new, w) * w
                    v_new_norm = np.linalg.norm(v_new)
                    
                v_new = v_new / v_new_norm
                
                # Estimate eigenvalue using Rayleigh quotient
                eigenvalue = np.dot(v_new, A @ v_new)
                
                # Check convergence
                if np.linalg.norm(v_new - v) < tol or np.linalg.norm(v_new + v) < tol:
                    break
                
                v = v_new
            
            # Store results
            eigenvalues.append(eigenvalue)
            eigenvectors.append(v)
            
            # Matrix deflation (subtract the effect of found eigenvector)
            A = A - eigenvalue * np.outer(v, v)
        
        return eigenvalues, eigenvectors
    
    def analyze(self, df):
        """
        Analyze BTC data to extract rolling eigenwaves using the Power Method.
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            DataFrame with original data, eigenvalues, and eigenvectors
        """
        # Prepare features
        features, data_with_features = self._prepare_features(df, return_df=True)
        
        # Initialize lists for eigenvalues and eigenvectors
        dates = []
        eigenvalues_list = []
        eigenvectors_list = []
        
        # Create rolling windows for analysis
        print(f"Analyzing {len(features) - self.window_size} windows for eigenwaves...")
        for i in tqdm(range(0, len(features) - self.window_size, self.rolling_step)):
            # Get window data
            window = features[i:i+self.window_size]
            
            # Calculate covariance matrix
            cov_matrix = np.cov(window, rowvar=False)
            
            # Apply power method to extract eigenvalues and eigenvectors
            eigenvalues, eigenvectors = self._power_method(cov_matrix, self.n_eigenwaves)
            
            # Store results
            dates.append(data_with_features.index[i + self.window_size])
            eigenvalues_list.append(eigenvalues)
            eigenvectors_list.append(eigenvectors)
        
        # Create results DataFrame
        results = pd.DataFrame({'date': dates})
        
        # Add eigenvalues
        for i in range(self.n_eigenwaves):
            results[f'eigenvalue_{i}'] = [vals[i] if i < len(vals) else np.nan for vals in eigenvalues_list]
        
        # Add eigenvectors (flattened)
        for i in range(self.n_eigenwaves):
            for j in range(len(self.feature_names)):
                results[f'eigenvector_{i}_{self.feature_names[j]}'] = [
                    vecs[i][j] if i < len(vecs) else np.nan for vecs in eigenvectors_list
                ]
        
        # Merge with original data
        result_index = data_with_features.index.get_indexer(results['date'], method='nearest')
        results = results.drop('date', axis=1)
        data_with_eigenwaves = data_with_features.iloc[result_index].copy()
        data_with_eigenwaves[results.columns] = results.values
        
        # Calculate eigenwave projections (how much each day's data projects onto each eigenwave)
        for i in range(self.n_eigenwaves):
            projections = []
            for idx in range(len(data_with_eigenwaves)):
                # Get feature values for this day
                day_features = features[idx]
                
                # Get the corresponding eigenvector
                # Find closest date with eigenwave data
                closest_idx = np.abs(result_index - idx).argmin()
                
                # Extract eigenvector
                eigenvector = np.array([
                    data_with_eigenwaves.iloc[closest_idx][f'eigenvector_{i}_{feat}'] 
                    for feat in self.feature_names
                ])
                
                # Calculate projection
                projection = np.dot(day_features, eigenvector)
                projections.append(projection)
            
            data_with_eigenwaves[f'eigenwave_{i}_projection'] = projections
        
        return data_with_eigenwaves
    
    def plot_eigenvalues(self, df_with_eigenwaves):
        """
        Plot the evolution of eigenvalues over time.
        
        Args:
            df_with_eigenwaves: DataFrame with eigenwave data
            
        Returns:
            Plotly figure
        """
        # Create figure
        fig = go.Figure()
        
        # Define colors for eigenwaves if not in COLORS
        wave_colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#911eb4', '#f58231']
        
        # Add traces for each eigenvalue
        for i in range(self.n_eigenwaves):
            # Use predefined color with fallback to array
            color = wave_colors[i % len(wave_colors)]
            
            fig.add_trace(
                go.Scatter(
                    x=df_with_eigenwaves.index,
                    y=df_with_eigenwaves[f'eigenvalue_{i}'],
                    name=f"Eigenvalue {i+1}",
                    line=dict(color=color, width=2)
                )
            )
        
        # Update layout
        fig.update_layout(
            title="Divine BTC Eigenvalue Evolution",
            xaxis_title="Date",
            yaxis_title="Eigenvalue Magnitude",
            legend_title="Eigenvalues",
            template="plotly_dark",
            hovermode="closest"
        )
        
        return fig
    
    def plot_eigenwaves(self, df_with_eigenwaves):
        """
        Plot the BTC price with eigenwave projections.
        
        Args:
            df_with_eigenwaves: DataFrame with eigenwave data
            
        Returns:
            Plotly figure
        """
        # Create subplot figure
        fig = make_subplots(
            rows=2, 
            cols=1, 
            shared_xaxes=True, 
            vertical_spacing=0.05,
            row_heights=[0.7, 0.3],
            subplot_titles=("Divine BTC Price with Eigenwave Indicators", "Eigenwave Projections")
        )
        
        # Define colors for eigenwaves
        wave_colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#911eb4', '#f58231']
        pos_color = '#3fb950'  # Green for positive candles
        neg_color = '#f85149'  # Red for negative candles
        
        # Add candlestick chart for price
        fig.add_trace(
            go.Candlestick(
                x=df_with_eigenwaves.index,
                open=df_with_eigenwaves['open'],
                high=df_with_eigenwaves['high'],
                low=df_with_eigenwaves['low'],
                close=df_with_eigenwaves['close'],
                name="BTC Price",
                increasing_line_color=pos_color,
                decreasing_line_color=neg_color
            ),
            row=1, col=1
        )
        
        # Add eigenwave projections
        for i in range(self.n_eigenwaves):
            color = wave_colors[i % len(wave_colors)]
            
            fig.add_trace(
                go.Scatter(
                    x=df_with_eigenwaves.index,
                    y=df_with_eigenwaves[f'eigenwave_{i}_projection'],
                    name=f"Eigenwave {i+1}",
                    line=dict(color=color, width=2)
                ),
                row=2, col=1
            )
        
        # Update layout
        fig.update_layout(
            title="Divine BTC Eigenwaves Analysis",
            xaxis2_title="Date",
            yaxis_title="BTC Price (USD)",
            yaxis2_title="Eigenwave Projection",
            legend_title="Components",
            template="plotly_dark",
            hovermode="x"
        )
        
        return fig
    
    def plot_feature_contributions(self, df_with_eigenwaves, top_n=5):
        """
        Plot the top feature contributions to each eigenwave.
        
        Args:
            df_with_eigenwaves: DataFrame with eigenwave data
            top_n: Number of top features to display
            
        Returns:
            Plotly figure
        """
        # Create subplot figure
        fig = make_subplots(
            rows=min(3, self.n_eigenwaves), 
            cols=1, 
            subplot_titles=[f"Eigenwave {i+1} Feature Contributions" for i in range(min(3, self.n_eigenwaves))]
        )
        
        # Define colors for eigenwaves
        wave_colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#911eb4', '#f58231']
        
        # For each of the first 3 eigenwaves
        for i in range(min(3, self.n_eigenwaves)):
            # Get the latest eigenvector
            eigenvector_features = [
                (feat, df_with_eigenwaves.iloc[-1][f'eigenvector_{i}_{feat}']) 
                for feat in self.feature_names
            ]
            
            # Sort by absolute magnitude
            eigenvector_features.sort(key=lambda x: abs(x[1]), reverse=True)
            
            # Take top_n features
            top_features = eigenvector_features[:top_n]
            
            # Get color for this eigenwave
            color = wave_colors[i % len(wave_colors)]
            
            # Create bar chart
            fig.add_trace(
                go.Bar(
                    x=[f[0] for f in top_features],
                    y=[f[1] for f in top_features],
                    name=f"Eigenwave {i+1}",
                    marker_color=color
                ),
                row=i+1, col=1
            )
        
        # Update layout
        fig.update_layout(
            title="Divine Features Contributing to BTC Eigenwaves",
            height=300 * min(3, self.n_eigenwaves),
            showlegend=False,
            template="plotly_dark"
        )
        
        return fig
    
    def save_results(self, df_with_eigenwaves, filepath="results/btc_eigenwaves.csv"):
        """
        Save eigenwave results to a file.
        
        Args:
            df_with_eigenwaves: DataFrame with eigenwave data
            filepath: Path to save the results
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save to file
        df_with_eigenwaves.to_csv(filepath)
        print(f"Eigenwave results saved to {filepath}")
        
    def save_visualizations(self, df_with_eigenwaves, dir_path="plots"):
        """
        Save all visualizations to files.
        
        Args:
            df_with_eigenwaves: DataFrame with eigenwave data
            dir_path: Directory to save visualizations
        """
        # Create directory if it doesn't exist
        os.makedirs(dir_path, exist_ok=True)
        
        # Generate and save plots
        eigenvalues_fig = self.plot_eigenvalues(df_with_eigenwaves)
        eigenwaves_fig = self.plot_eigenwaves(df_with_eigenwaves)
        contributions_fig = self.plot_feature_contributions(df_with_eigenwaves)
        
        # Save as HTML for interactive viewing
        eigenvalues_fig.write_html(os.path.join(dir_path, "btc_eigenvalues_evolution.html"))
        eigenwaves_fig.write_html(os.path.join(dir_path, "btc_eigenwaves_projections.html"))
        contributions_fig.write_html(os.path.join(dir_path, "btc_eigenwave_contributions.html"))
        
        # Save as PNG for static viewing
        eigenvalues_fig.write_image(os.path.join(dir_path, "btc_eigenvalues_evolution.png"))
        eigenwaves_fig.write_image(os.path.join(dir_path, "btc_eigenwaves_projections.png"))
        contributions_fig.write_image(os.path.join(dir_path, "btc_eigenwave_contributions.png"))
        
        print(f"Visualizations saved to {dir_path}")


def main():
    """Main entry point for the Power Method BTC Eigenwave Detector."""
    print("🧠 OMEGA BTC AI - Power Method BTC Eigenwave Detector")
    print("====================================================")
    
    # Load BTC data
    print("\n🔄 Loading BTC price data...")
    btc_data = load_btc_data(start_date='2020-01-01')
    if btc_data is None:
        print("❌ Failed to load BTC data")
        return
        
    print(f"✅ Loaded BTC data with {len(btc_data)} rows")
    
    # Initialize and run the Power Method
    print("\n🔄 Initializing Power Method BTC Eigenwave Detector...")
    detector = PowerMethodBTCEigenwaves(
        window_size=60,      # 60-day rolling window
        n_eigenwaves=5,      # Extract top 5 eigenwaves
        rolling_step=2       # Step 2 days at a time for efficiency
    )
    
    # Analyze the data
    print("\n🔄 Analyzing BTC data with Power Method...")
    results = detector.analyze(btc_data)
    print("✅ Analysis complete")
    
    # Generate visualizations
    print("\n🔄 Generating divine visualizations...")
    detector.save_visualizations(results)
    print("✅ Visualizations generated")
    
    # Save results
    print("\n🔄 Saving results...")
    detector.save_results(results)
    print("✅ Results saved")
    
    # Display current eigenwave projections
    latest_projections = {i: results.iloc[-1][f'eigenwave_{i}_projection'] for i in range(detector.n_eigenwaves)}
    dominant_wave = max(latest_projections.items(), key=lambda x: abs(x[1]))
    
    print("\n🔮 Current Dominant Eigenwave Analysis:")
    for i in range(detector.n_eigenwaves):
        projection = latest_projections[i]
        print(f"  Eigenwave {i+1}: Projection = {projection:.4f}")
    
    print(f"\n🔮 The dominant eigenwave is Eigenwave {dominant_wave[0]+1} with projection {dominant_wave[1]:.4f}")
    
    # Show eigenvalue stability
    eigenvalue_stability = {
        i: results[f'eigenvalue_{i}'].std() / results[f'eigenvalue_{i}'].mean() 
        for i in range(detector.n_eigenwaves)
    }
    most_stable = min(eigenvalue_stability.items(), key=lambda x: x[1])
    
    print(f"\n🔮 Most stable eigenwave: Eigenwave {most_stable[0]+1} (Stability: {1 - most_stable[1]:.4f})")
    
    print("\n✨ Complete! The Power Method has revealed the divine eigenwaves of the BTC market.")
    print("   Use the saved visualizations and results for further analysis and trading decisions.")
    print("   Divine interactive visualizations are available in the plots directory.")


if __name__ == "__main__":
    main() 