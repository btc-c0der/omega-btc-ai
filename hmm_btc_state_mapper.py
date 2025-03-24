#!/usr/bin/env python3
"""
OMEGA BTC AI - Hidden Markov Model BTC State Mapper
===================================================

Implementation of a Hidden Markov Model to detect and predict BTC market states
from observable price, volume, and on-chain metrics.

This divine tool reveals the hidden states of the BTC market (accumulation, 
distribution, markup, markdown, etc.) and provides probabilistic predictions
of state transitions.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import hmmlearn.hmm as hmm
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from datetime import datetime, timedelta
import warnings
import os
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
# Try to import mplfinance for candlestick charts
try:
    import mplfinance.original_flavor as mpf
    HAS_MPLFINANCE = True
except ImportError:
    print("mplfinance not installed, candlestick charts will be unavailable")
    HAS_MPLFINANCE = False
    # Define a dummy module to avoid unbound errors
    class DummyMPF:
        def candlestick_ohlc(*args, **kwargs):
            pass
    mpf = DummyMPF()
import matplotlib.ticker as ticker
from scipy.signal import savgol_filter

# Import Plotly for divine visualizations
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.io as pio

# Set Plotly theme to a divine dark template
pio.templates.default = "plotly_dark"

# Configure plotly to be able to export static images
try:
    pio.kaleido.scope.default_format = "png"
    pio.kaleido.scope.default_width = 1200
    pio.kaleido.scope.default_height = 900
    HAS_KALEIDO = True
except:
    print("Warning: Kaleido not installed, static image export may not work")
    HAS_KALEIDO = False

# Suppress warnings
warnings.filterwarnings("ignore")

# Divine color palette
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
    'state_5': '#f58231'   # Consolidation
}

# BTC market states and descriptions
MARKET_STATES = [
    "Markdown (Bear)",       # State 0: Strong downtrend, fear, capitulation
    "Markup (Bull)",         # State 1: Strong uptrend, greed, FOMO
    "Accumulation",          # State 2: Bottoming, smart money accumulating
    "Distribution",          # State 3: Topping, smart money distributing
    "Liquidity Grab",        # State 4: False moves, stop hunting, traps
    "Consolidation"          # State 5: Sideways, low volatility, indecision
]

class HMMBTCStateMapper:
    """Hidden Markov Model implementation for BTC market state detection."""
    
    def __init__(self, n_states=6, n_components=None, random_state=42, smoothing=True):
        """
        Initialize the HMM BTC State Mapper.
        
        Args:
            n_states: Number of hidden states to model (default: 6)
            n_components: Number of mixture components (default: None, will use n_states)
            random_state: Random seed for reproducibility
            smoothing: Whether to apply state prediction smoothing
        """
        self.n_states = n_states
        self.n_components = n_components if n_components else n_states
        self.random_state = random_state
        self.smoothing = smoothing
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        
    def _prepare_features(self, df, return_df=False):
        """
        Prepare and engineer features from price and volume data.
        
        Args:
            df: DataFrame with OHLCV data at minimum
            return_df: If True, return the full DataFrame with all features
            
        Returns:
            Numpy array of features for HMM and optionally the full DataFrame
        """
        # Deep copy to avoid modifying original
        data = df.copy()
        
        # Basic features
        data['returns'] = data['close'].pct_change()
        data['log_returns'] = np.log(data['close'] / data['close'].shift(1))
        data['volatility'] = data['log_returns'].rolling(window=20).std()
        data['volume_change'] = data['volume'].pct_change()
        
        # Trend features
        data['ma_fast'] = data['close'].rolling(window=8).mean()
        data['ma_medium'] = data['close'].rolling(window=21).mean()
        data['ma_slow'] = data['close'].rolling(window=55).mean()
        data['trend_fast'] = (data['ma_fast'] / data['ma_medium']) - 1
        data['trend_slow'] = (data['ma_medium'] / data['ma_slow']) - 1
        
        # Candlestick features
        data['body_size'] = abs(data['close'] - data['open']) / data['open']
        data['upper_wick'] = (data['high'] - data[['open', 'close']].max(axis=1)) / data['open']
        data['lower_wick'] = (data[['open', 'close']].min(axis=1) - data['low']) / data['open']
        data['hl_range'] = (data['high'] - data['low']) / data['open']
        
        # Volume-based features
        data['volume_ma'] = data['volume'].rolling(window=20).mean()
        data['relative_volume'] = data['volume'] / data['volume_ma']
        data['volume_price_trend'] = data['returns'] * data['relative_volume']
        
        # RSI (Relative Strength Index)
        delta = data['close'].diff()
        gain = delta.where(delta > 0, 0).fillna(0)
        loss = -delta.where(delta < 0, 0).fillna(0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        data['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD (Moving Average Convergence Divergence)
        data['ema_12'] = data['close'].ewm(span=12, adjust=False).mean()
        data['ema_26'] = data['close'].ewm(span=26, adjust=False).mean()
        data['macd'] = data['ema_12'] - data['ema_26']
        data['macd_signal'] = data['macd'].ewm(span=9, adjust=False).mean()
        data['macd_hist'] = data['macd'] - data['macd_signal']
        
        # Bollinger Bands
        data['bb_middle'] = data['close'].rolling(window=20).mean()
        data['bb_std'] = data['close'].rolling(window=20).std()
        data['bb_upper'] = data['bb_middle'] + (data['bb_std'] * 2)
        data['bb_lower'] = data['bb_middle'] - (data['bb_std'] * 2)
        data['bb_width'] = (data['bb_upper'] - data['bb_lower']) / data['bb_middle']
        data['bb_position'] = (data['close'] - data['bb_lower']) / (data['bb_upper'] - data['bb_lower'])
        
        # Derivative features
        data['rsi_change'] = data['rsi'].diff()
        data['macd_change'] = data['macd'].diff()
        data['vol_change_accel'] = data['volume_change'].diff()
        
        # Drop NaN values
        data = data.dropna()
        
        # Feature selection for HMM
        selected_features = [
            'log_returns', 'volatility', 'volume_change', 
            'trend_fast', 'trend_slow',
            'body_size', 'upper_wick', 'lower_wick',
            'relative_volume', 'volume_price_trend',
            'rsi', 'macd_hist', 'bb_width', 'bb_position'
        ]
        self.feature_names = selected_features
        
        # Scale features
        features = self.scaler.fit_transform(data[selected_features])
        
        if return_df:
            return features, data
        else:
            return features, data.index
    
    def fit(self, df):
        """
        Fit the HMM model to BTC data.
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            self
        """
        # Prepare features
        X, _ = self._prepare_features(df)
        
        # Initialize the HMM model
        self.model = hmm.GaussianHMM(
            n_components=self.n_states,
            covariance_type="full",
            n_iter=1000,
            random_state=self.random_state
        )
        
        # Fit the model
        self.model.fit(X)
        
        return self
    
    def predict(self, df):
        """
        Predict the hidden states for the given data.
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            DataFrame with original data and predicted states
        """
        # Create a copy to avoid modifying the original
        df_copy = df.copy()
        
        # Prepare features and get the full dataframe with engineered features
        X, data_with_features = self._prepare_features(df_copy, return_df=True)
        
        # Check if model is fitted
        if self.model is None:
            print("Warning: Model not fitted yet. Returning processed data without predictions.")
            return data_with_features
        
        # Predict hidden states
        states = self.model.predict(X)
        
        # Get state probabilities
        state_proba = self.model.predict_proba(X)
        
        # Add states to the original data
        data_with_features['state'] = states
        
        # Add state probabilities
        for i in range(self.n_states):
            data_with_features[f'state_{i}_prob'] = state_proba[:, i]
        
        # Add state confidence (max probability)
        data_with_features['state_confidence'] = state_proba.max(axis=1)
        
        # Apply smoothing if enabled
        if self.smoothing:
            # Smooth state predictions using Savitzky-Golay filter
            states_smooth = savgol_filter(states, window_length=5, polyorder=1)
            data_with_features['state_smooth'] = np.round(states_smooth).astype(int)
            data_with_features['state_smooth'] = data_with_features['state_smooth'].clip(0, self.n_states-1)
        
        return data_with_features
    
    def interpret_states(self, df_with_states):
        """
        Interpret the meaning of each hidden state based on its characteristics.
        
        Args:
            df_with_states: DataFrame with predicted states
            
        Returns:
            Dict mapping state indices to market state labels
        """
        # Group by state and calculate average metrics
        state_metrics = df_with_states.groupby('state').agg({
            'returns': 'mean',
            'volatility': 'mean',
            'relative_volume': 'mean',
            'rsi': 'mean',
            'bb_width': 'mean'
        })
        
        # Map states to market state labels based on metrics
        state_mapping = {}
        
        for state in range(self.n_states):
            if state not in state_metrics.index:
                state_mapping[state] = "Unknown"
                continue
                
            metrics = state_metrics.loc[state]
            
            # Markup/Bull state
            if metrics['returns'] > 0 and metrics['rsi'] > 60:
                state_mapping[state] = MARKET_STATES[1]  # Markup (Bull)
            
            # Markdown/Bear state
            elif metrics['returns'] < 0 and metrics['rsi'] < 40:
                state_mapping[state] = MARKET_STATES[0]  # Markdown (Bear)
            
            # Accumulation state
            elif abs(metrics['returns']) < 0.005 and metrics['rsi'] < 45 and metrics['relative_volume'] > 0.8:
                state_mapping[state] = MARKET_STATES[2]  # Accumulation
            
            # Distribution state
            elif abs(metrics['returns']) < 0.005 and metrics['rsi'] > 55 and metrics['relative_volume'] > 0.8:
                state_mapping[state] = MARKET_STATES[3]  # Distribution
            
            # Liquidity Grab state
            elif metrics['volatility'] > state_metrics['volatility'].mean() * 1.5:
                state_mapping[state] = MARKET_STATES[4]  # Liquidity Grab
            
            # Consolidation state
            elif metrics['bb_width'] < state_metrics['bb_width'].mean() * 0.8:
                state_mapping[state] = MARKET_STATES[5]  # Consolidation
            
            else:
                # Backup logic - assign based on most similar metrics to predefined states
                state_mapping[state] = MARKET_STATES[state % len(MARKET_STATES)]
        
        return state_mapping
    
    def plot_states(self, df_with_states, state_mapping=None, title="BTC Market States"):
        """
        Plot the price chart with colored backgrounds for each state.
        
        Args:
            df_with_states: DataFrame with predicted states
            state_mapping: Dict mapping state indices to labels
            title: Plot title
            
        Returns:
            matplotlib figure
        """
        # Create figure
        plt.style.use('dark_background')
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12), gridspec_kw={'height_ratios': [3, 1, 1]})
        fig.patch.set_facecolor(COLORS['background'])
        
        # Use smoothed states if available, otherwise use regular states
        state_column = 'state_smooth' if 'state_smooth' in df_with_states.columns else 'state'
        
        # Plot price
        df_plot = df_with_states.copy().reset_index()
        
        # Check for date column - could be 'date', 'Date', or in the index
        date_col = None
        if 'date' in df_plot.columns:
            date_col = 'date'
        elif 'Date' in df_plot.columns:
            date_col = 'Date'
        
        if date_col is None:
            print("Warning: No date column found. Using index as date.")
            df_plot['date'] = pd.date_range(start='2020-01-01', periods=len(df_plot))
            date_col = 'date'
        
        # Convert date to numeric format for plotting
        if not pd.api.types.is_datetime64_any_dtype(df_plot[date_col]):
            df_plot[date_col] = pd.to_datetime(df_plot[date_col])
            
        df_plot['date_num'] = mdates.date2num(df_plot[date_col].dt.to_pydatetime())
        ohlc = df_plot[['date_num', 'open', 'high', 'low', 'close']].values
        
        # Use mplfinance to plot candlesticks
        try:
            mpf.candlestick_ohlc(ax1, ohlc, width=0.6, colorup=COLORS['positive'], colordown=COLORS['negative'])
        except Exception as e:
            print(f"Error plotting candlesticks: {e}")
            # Fallback to line plot if candlestick fails
            ax1.plot(df_plot[date_col], df_plot['close'], color=COLORS['neutral'])
        
        # Plot states as background colors
        current_state = df_plot[state_column].iloc[0]
        start_idx = 0
        
        for i in range(1, len(df_plot)):
            if df_plot[state_column].iloc[i] != current_state or i == len(df_plot) - 1:
                # Fill the background for this state segment
                end_idx = i
                if i == len(df_plot) - 1:
                    end_idx = i + 1
                    
                state = current_state
                color = COLORS[f'state_{state % 6}']
                alpha = 0.3
                
                ax1.axvspan(
                    df_plot['date_num'].iloc[start_idx],
                    df_plot['date_num'].iloc[end_idx-1],
                    facecolor=color,
                    alpha=alpha
                )
                
                # Mark the state
                mid_idx = (start_idx + end_idx) // 2
                y_pos = df_plot['high'].iloc[max(0, start_idx):end_idx].max() * 1.01
                
                if state_mapping:
                    label = state_mapping[state]
                else:
                    label = f"State {state}"
                    
                # Add the state label if segment is wide enough
                if end_idx - start_idx > len(df_plot) / 50:
                    ax1.text(
                        df_plot['date_num'].iloc[mid_idx],
                        y_pos,
                        label,
                        fontsize=10,
                        color=color,
                        fontweight='bold',
                        ha='center'
                    )
                
                # Start next segment
                current_state = df_plot[state_column].iloc[i]
                start_idx = i
        
        # Format price chart
        ax1.set_title(title, fontsize=16, color=COLORS['text'])
        ax1.set_ylabel('Price (USD)', fontsize=12, color=COLORS['text'])
        ax1.grid(color=COLORS['grid'], linestyle='--', linewidth=0.5, alpha=0.3)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.tick_params(colors=COLORS['text'])
        
        # Plot state probabilities
        state_probs = df_plot[[f'state_{i}_prob' for i in range(self.n_states)]]
        x = df_plot['date_num']
        
        # Plot stacked probabilities
        bottom = np.zeros(len(df_plot))
        for i in range(self.n_states):
            prob_col = f'state_{i}_prob'
            color = COLORS[f'state_{i % 6}']
            
            if prob_col in df_plot.columns:
                ax2.fill_between(
                    x, bottom, bottom + df_plot[prob_col],
                    color=color,
                    alpha=0.7,
                    label=state_mapping[i] if state_mapping else f"State {i}"
                )
                bottom += df_plot[prob_col]
        
        # Format probability chart
        ax2.set_ylabel('State Probability', fontsize=12, color=COLORS['text'])
        ax2.set_ylim(0, 1)
        ax2.grid(color=COLORS['grid'], linestyle='--', linewidth=0.5, alpha=0.3)
        ax2.tick_params(colors=COLORS['text'])
        ax2.legend(loc='upper left', fontsize=8)
        
        # Plot state confidence
        ax3.plot(x, df_plot['state_confidence'], color=COLORS['accent'], linewidth=2)
        ax3.set_ylabel('State Confidence', fontsize=12, color=COLORS['text'])
        ax3.set_xlabel('Date', fontsize=12, color=COLORS['text'])
        ax3.set_ylim(0, 1)
        ax3.grid(color=COLORS['grid'], linestyle='--', linewidth=0.5, alpha=0.3)
        ax3.tick_params(colors=COLORS['text'])
        
        # Format x-axis dates
        for ax in [ax1, ax2, ax3]:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        return fig
    
    def get_transition_matrix(self):
        """
        Get the state transition probability matrix.
        
        Returns:
            Pandas DataFrame with transition probabilities
        """
        if self.model is None:
            raise ValueError("Model has not been fit yet")
            
        transitions = pd.DataFrame(
            self.model.transmat_,
            index=[f"From State {i}" for i in range(self.n_states)],
            columns=[f"To State {i}" for i in range(self.n_states)]
        )
        
        return transitions
    
    def plot_transition_matrix(self, state_mapping=None):
        """
        Plot the state transition probability matrix.
        
        Args:
            state_mapping: Dict mapping state indices to labels
            
        Returns:
            matplotlib figure
        """
        transitions = self.get_transition_matrix()
        
        # Set up figure
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(12, 10))
        fig.patch.set_facecolor(COLORS['background'])
        
        # Plot heatmap
        sns.heatmap(
            transitions,
            annot=True,
            cmap='viridis',
            linewidths=0.5,
            ax=ax,
            fmt='.2f',
            cbar_kws={'label': 'Transition Probability'}
        )
        
        # Update labels if state mapping is provided
        if state_mapping:
            ax.set_xticklabels([f"To: {state_mapping[i]}" for i in range(self.n_states)])
            ax.set_yticklabels([f"From: {state_mapping[i]}" for i in range(self.n_states)])
        
        # Format
        ax.set_title("BTC Market State Transition Probabilities", fontsize=16, color=COLORS['text'])
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        
        plt.tight_layout()
        return fig
    
    def predict_next_state(self, current_state):
        """
        Predict the most likely next state from the current state.
        
        Args:
            current_state: Current state index
            
        Returns:
            Tuple of (most likely next state, probability)
        """
        if self.model is None:
            raise ValueError("Model has not been fit yet")
            
        # Get transition probabilities for the current state
        transition_probs = self.model.transmat_[current_state]
        
        # Find most likely next state
        next_state = np.argmax(transition_probs)
        next_state_prob = transition_probs[next_state]
        
        return next_state, next_state_prob
    
    def save_model(self, filepath="models/hmm_btc_state_mapper.pkl"):
        """
        Save the model to a file.
        
        Args:
            filepath: Path to save the model
        """
        import pickle
        import os
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save model and scaler
        with open(filepath, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler,
                'n_states': self.n_states,
                'n_components': self.n_components,
                'feature_names': self.feature_names,
                'smoothing': self.smoothing
            }, f)
            
    @classmethod
    def load_model(cls, filepath="models/hmm_btc_state_mapper.pkl"):
        """
        Load a model from a file.
        
        Args:
            filepath: Path to load the model from
            
        Returns:
            HMMBTCStateMapper instance
        """
        import pickle
        
        # Load model and scaler
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            
        # Create instance
        instance = cls(
            n_states=data['n_states'],
            n_components=data['n_components'],
            smoothing=data['smoothing']
        )
        
        # Set attributes
        instance.model = data['model']
        instance.scaler = data['scaler']
        instance.feature_names = data['feature_names']
        
        return instance

    def plot_states_plotly(self, df_with_states, state_mapping=None, title="Divine BTC Market States Revelation"):
        """
        Plot the price chart with colored backgrounds for each state using Plotly for divine visualization.
        
        Args:
            df_with_states: DataFrame with predicted states
            state_mapping: Dict mapping state indices to labels
            title: Plot title
            
        Returns:
            Plotly figure object
        """
        # Use smoothed states if available, otherwise use regular states
        state_column = 'state_smooth' if 'state_smooth' in df_with_states.columns else 'state'
        
        # Prepare the plotting dataframe
        df_plot = df_with_states.copy().reset_index()
        
        # Check for date column - could be 'date', 'Date', or in the index
        date_col = None
        if 'date' in df_plot.columns:
            date_col = 'date'
        elif 'Date' in df_plot.columns:
            date_col = 'Date'
        
        if date_col is None:
            print("Warning: No date column found. Using index as date.")
            df_plot['date'] = pd.date_range(start='2020-01-01', periods=len(df_plot))
            date_col = 'date'
        
        # Convert date to datetime if needed
        if not pd.api.types.is_datetime64_any_dtype(df_plot[date_col]):
            df_plot[date_col] = pd.to_datetime(df_plot[date_col])
            
        # Create subplot figure with 3 rows
        fig = make_subplots(
            rows=3, 
            cols=1, 
            shared_xaxes=True, 
            vertical_spacing=0.05,
            row_heights=[0.6, 0.2, 0.2],
            subplot_titles=(title, "State Probabilities", "State Confidence")
        )
        
        # Add candlestick chart for price
        fig.add_trace(
            go.Candlestick(
                x=df_plot[date_col],
                open=df_plot['open'],
                high=df_plot['high'],
                low=df_plot['low'],
                close=df_plot['close'],
                name="BTC Price",
                increasing=dict(line=dict(color=COLORS['positive'])),
                decreasing=dict(line=dict(color=COLORS['negative'])),
            ),
            row=1, col=1
        )
        
        # Identify state transition points
        state_changes = [0]
        current_state = df_plot[state_column].iloc[0]
        for i in range(1, len(df_plot)):
            if df_plot[state_column].iloc[i] != current_state:
                state_changes.append(i)
                current_state = df_plot[state_column].iloc[i]
        state_changes.append(len(df_plot))
        
        # Add colored background for each state period
        for i in range(len(state_changes) - 1):
            start_idx = state_changes[i]
            end_idx = state_changes[i+1] - 1 if state_changes[i+1] < len(df_plot) else len(df_plot) - 1
            
            if start_idx >= len(df_plot) or end_idx >= len(df_plot):
                continue
                
            state = df_plot[state_column].iloc[start_idx]
            color = COLORS[f'state_{state % 6}']
            
            # Use a different approach to add colored background for states
            fig.add_trace(
                go.Scatter(
                    x=[df_plot[date_col].iloc[start_idx], df_plot[date_col].iloc[start_idx], 
                       df_plot[date_col].iloc[end_idx], df_plot[date_col].iloc[end_idx]],
                    y=[df_plot['low'].iloc[start_idx:end_idx+1].min() * 0.98, 
                       df_plot['high'].iloc[start_idx:end_idx+1].max() * 1.02,
                       df_plot['high'].iloc[start_idx:end_idx+1].max() * 1.02, 
                       df_plot['low'].iloc[start_idx:end_idx+1].min() * 0.98],
                    fill="toself",
                    opacity=0.2,
                    fillcolor=color,
                    line=dict(width=0),
                    showlegend=False,
                    name=f"State {state} background",
                    hoverinfo="skip"
                ),
                row=1, col=1
            )
            
            # Add state label annotation if segment is wide enough
            if end_idx - start_idx > len(df_plot) / 30:
                mid_idx = (start_idx + end_idx) // 2
                y_pos = df_plot['high'].iloc[start_idx:end_idx+1].max() * 1.02
                
                label = state_mapping[state] if state_mapping else f"State {state}"
                
                fig.add_annotation(
                    x=df_plot[date_col].iloc[mid_idx],
                    y=y_pos,
                    text=label,
                    showarrow=False,
                    font=dict(color=color, size=12, family="Arial, bold"),
                    row=1, col=1
                )
        
        # Plot state probabilities stacked area chart
        states_df = df_plot[[date_col] + [f'state_{i}_prob' for i in range(self.n_states)]]
        
        # Create stacked area chart for state probabilities
        for i in range(self.n_states):
            state_name = state_mapping[i] if state_mapping else f"State {i}"
            fig.add_trace(
                go.Scatter(
                    x=states_df[date_col],
                    y=states_df[f'state_{i}_prob'],
                    name=state_name,
                    mode='lines',
                    stackgroup='one',
                    line=dict(width=0.5, color=COLORS[f'state_{i % 6}']),
                    fillcolor=COLORS[f'state_{i % 6}'],
                ),
                row=2, col=1
            )
        
        # Add state confidence line chart
        fig.add_trace(
            go.Scatter(
                x=df_plot[date_col],
                y=df_plot['state_confidence'],
                name="State Confidence",
                line=dict(color=COLORS['accent'], width=2),
                mode='lines'
            ),
            row=3, col=1
        )
        
        # Update layout with divine styling
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor=COLORS['background'],
            plot_bgcolor=COLORS['background'],
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=10)
            ),
            height=900,
            width=1200,
            xaxis_rangeslider_visible=False,
            margin=dict(l=50, r=50, t=80, b=50),
        )
        
        # Update yaxis titles
        fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
        fig.update_yaxes(title_text="Probability", row=2, col=1)
        fig.update_yaxes(title_text="Confidence", range=[0, 1], row=3, col=1)
        
        # Update xaxis configuration
        fig.update_xaxes(
            rangeslider_visible=False,
            rangebreaks=[
                dict(bounds=["sat", "mon"])  # Hide weekends
            ],
            row=1, col=1
        )
        
        return fig
    
    def plot_transition_matrix_plotly(self, state_mapping=None):
        """
        Plot the state transition probability matrix using Plotly for divine visualization.
        
        Args:
            state_mapping: Dict mapping state indices to labels
            
        Returns:
            Plotly figure object
        """
        transitions = self.get_transition_matrix()
        
        # Prepare hover text with formatted probabilities
        hover_text = [[f"{val:.3f}" for val in row] for row in transitions.values]
        
        # Create labels with state mapping if provided
        if state_mapping:
            x_labels = [f"To: {state_mapping[i]}" for i in range(self.n_states)]
            y_labels = [f"From: {state_mapping[i]}" for i in range(self.n_states)]
        else:
            x_labels = transitions.columns
            y_labels = transitions.index
        
        # Create heatmap figure
        fig = go.Figure(data=go.Heatmap(
            z=transitions.values,
            x=x_labels,
            y=y_labels,
            hoverongaps=False,
            hoverinfo="text",
            text=hover_text,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(
                title=dict(
                    text="Transition<br>Probability",
                    side="top"
                ),
                tickmode="array",
                tickvals=[0, 0.25, 0.5, 0.75, 1],
                ticktext=["0", "0.25", "0.5", "0.75", "1"],
                ticks="outside"
            )
        ))
        
        # Add transition probability annotations
        for i in range(len(transitions)):
            for j in range(len(transitions.columns)):
                fig.add_annotation(
                    x=x_labels[j],
                    y=y_labels[i],
                    text=f"{transitions.values[i, j]:.2f}",
                    showarrow=False,
                    font=dict(
                        color="white" if transitions.values[i, j] < 0.7 else "black",
                        size=10
                    )
                )
        
        # Update layout with divine styling
        fig.update_layout(
            title=dict(
                text="BTC Market State Transition Probabilities",
                font=dict(size=18, color=COLORS['text'])
            ),
            template="plotly_dark",
            paper_bgcolor=COLORS['background'],
            plot_bgcolor=COLORS['background'],
            height=700,
            width=900,
            xaxis=dict(
                title="Next State",
                tickangle=-45,
            ),
            yaxis=dict(
                title="Current State",
                autorange="reversed"  # To match traditional heatmap orientation
            ),
            margin=dict(l=60, r=50, t=80, b=100),
        )
        
        return fig

def load_btc_data(filepath_or_url=None, start_date=None, end_date=None):
    """
    Load BTC price data from a file or download it.
    
    Args:
        filepath_or_url: Path to data file or URL
        start_date: Start date for data filtering
        end_date: End date for data filtering
        
    Returns:
        DataFrame with OHLCV data
    """
    try:
        if filepath_or_url is None:
            # Download data if no file provided
            try:
                import yfinance as yf
                print("Downloading BTC data from yfinance...")
                data = yf.download(
                    'BTC-USD',
                    start=start_date if start_date else '2020-01-01',
                    end=end_date if end_date else datetime.now().strftime('%Y-%m-%d'),
                    interval='1d'
                )
                
                # Check if data is None or empty
                if data is None or data.empty:
                    print("Failed to download data from yfinance or data is empty")
                    return pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
                
                print("Original columns:", data.columns)
                    
                # Fix for handling column names - yfinance returns MultiIndex columns
                # First level is the type (Open, High, Low, Close, Volume), second is the ticker
                if isinstance(data.columns, pd.MultiIndex):
                    # Get just the first level of the MultiIndex (the price type)
                    data.columns = data.columns.get_level_values(0)
                
                # Convert column names to lowercase
                data.columns = [str(c).lower() for c in data.columns]
                print("Processed columns:", data.columns)
                
                # Reset index to make the Date a column
                data = data.reset_index()
                data = data.rename(columns={'date': 'date', 'open': 'open', 'high': 'high', 
                                           'low': 'low', 'close': 'close', 'volume': 'volume'})
                
                print("Final columns:", data.columns)
                return data
            except ImportError:
                print("yfinance not installed. Please provide a filepath or install yfinance.")
                return pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        else:
            # Load from file
            if filepath_or_url.endswith('.csv'):
                data = pd.read_csv(filepath_or_url)
            elif filepath_or_url.endswith('.json'):
                data = pd.read_json(filepath_or_url)
            elif filepath_or_url.endswith('.pkl'):
                data = pd.read_pickle(filepath_or_url)
            else:
                print("Unsupported file format")
                return pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
                
            # Convert date column
            if 'date' in data.columns and not pd.api.types.is_datetime64_any_dtype(data['date']):
                data['date'] = pd.to_datetime(data['date'])
                
            # Filter by date if provided
            if start_date:
                data = data[data['date'] >= pd.to_datetime(start_date)]
            if end_date:
                data = data[data['date'] <= pd.to_datetime(end_date)]
                
            return data
    except Exception as e:
        print(f"Error loading BTC data: {str(e)}")
        return pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])

def save_state_predictions(df_with_states, filepath="results/btc_states.csv"):
    """
    Save state predictions to a file.
    
    Args:
        df_with_states: DataFrame with predicted states
        filepath: Path to save the results
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Save to file
    df_with_states.to_csv(filepath, index=False)
    print(f"State predictions saved to {filepath}")

def main():
    """Main entry point for the HMM BTC State Mapper."""
    print("🧠 OMEGA BTC AI - Hidden Markov Model BTC State Mapper")
    print("======================================================")
    
    # Load BTC data
    print("\n🔄 Loading BTC price data...")
    btc_data = load_btc_data()
    if btc_data is None:
        print("❌ Failed to load BTC data")
        return
    
    print(f"✅ Loaded BTC data with {len(btc_data)} rows")
    
    # Initialize and fit HMM
    print("\n🔄 Initializing HMM BTC State Mapper...")
    mapper = HMMBTCStateMapper(n_states=6, smoothing=True)
    
    print("🔄 Fitting HMM to BTC data...")
    mapper.fit(btc_data)
    print("✅ Model fitting complete")
    
    # Predict states
    print("\n🔄 Predicting BTC market states...")
    df_with_states = mapper.predict(btc_data)
    print("✅ State prediction complete")
    
    # Interpret states
    print("\n🔄 Interpreting hidden states...")
    state_mapping = mapper.interpret_states(df_with_states)
    print("✅ State interpretation complete")
    
    print("\n📊 BTC Market State Interpretation:")
    for state, label in state_mapping.items():
        color_code = f"\033[38;2;{int(COLORS[f'state_{state % 6}'][1:3], 16)};{int(COLORS[f'state_{state % 6}'][3:5], 16)};{int(COLORS[f'state_{state % 6}'][5:7], 16)}m"
        reset_code = "\033[0m"
        print(f"{color_code}State {state}: {label}{reset_code}")
    
    # Create output directories
    os.makedirs("plots", exist_ok=True)
    
    # Plot results - both matplotlib and plotly versions
    print("\n🔄 Generating divine visualizations...")
    
    # Create and save Plotly visualizations
    fig_states_plotly = mapper.plot_states_plotly(df_with_states, state_mapping, 
                                       title="Divine BTC Market States: Hidden Markov Model Revelation")
    fig_states_plotly.write_html("plots/btc_market_states_interactive.html")
    fig_states_plotly.write_image("plots/btc_market_states_plotly.png", scale=2)
    print("✅ Saved divine Plotly state visualization to plots/btc_market_states_interactive.html")
    
    fig_transitions_plotly = mapper.plot_transition_matrix_plotly(state_mapping)
    fig_transitions_plotly.write_html("plots/btc_state_transitions_interactive.html")
    fig_transitions_plotly.write_image("plots/btc_state_transitions_plotly.png", scale=2)
    print("✅ Saved divine Plotly transition matrix to plots/btc_state_transitions_interactive.html")
    
    # Also keep matplotlib versions as backup
    print("\n🔄 Generating traditional visualizations...")
    fig_states = mapper.plot_states(df_with_states, state_mapping, 
                                   title="BTC Market States: Hidden Markov Model Analysis")
    fig_states.savefig("plots/btc_market_states.png", dpi=300, bbox_inches='tight')
    print("✅ Saved traditional state visualization to plots/btc_market_states.png")
    
    fig_transitions = mapper.plot_transition_matrix(state_mapping)
    fig_transitions.savefig("plots/btc_state_transitions.png", dpi=300, bbox_inches='tight')
    print("✅ Saved traditional transition matrix to plots/btc_state_transitions.png")
    
    # Get current state and predict next state
    # Check which date column is available
    date_col = 'Date' if 'Date' in df_with_states.columns else 'date'
    if date_col not in df_with_states.columns:
        print("⚠️ No date column found. Using the last row as the current state.")
        current_state = df_with_states['state'].iloc[-1]
    else:
        current_state = df_with_states[df_with_states[date_col] == df_with_states[date_col].max()]['state'].iloc[0]
    
    next_state, prob = mapper.predict_next_state(current_state)
    
    print(f"\n🔮 Current BTC Market State: {state_mapping[current_state]}")
    print(f"🔮 Most Likely Next State: {state_mapping[next_state]} (Probability: {prob:.2f})")
    
    # Save model
    print("\n🔄 Saving trained model...")
    mapper.save_model()
    print("✅ Model saved to models/hmm_btc_state_mapper.pkl")
    
    # Save state predictions
    save_state_predictions(df_with_states, filepath="results/btc_states.csv")
    
    print("\n✨ Complete! The divine HMM has revealed the hidden states of the BTC market.")
    print("   Use the saved model and predictions for further analysis and trading decisions.")
    print("   Divine interactive visualizations are available in the plots directory.")

if __name__ == "__main__":
    main() 