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
OMEGA BTC AI - Variational Inference BTC Cycle Approximation
===========================================================

Implementation of variational inference techniques to model and approximate 
Bitcoin market cycles when full probability distributions are too complex.

This sacred tool simplifies the true wave structure of BTC market cycles
while maintaining accuracy, especially when market distortion is present.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Normal, kl_divergence
from scipy.signal import savgol_filter
import warnings
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("VariationalInferenceBTCCycle")

# Try to import the HMM and Power Method modules
try:
    from hmm_btc_state_mapper import load_btc_data, COLORS, MARKET_STATES
    from power_method_btc_eigenwaves import PowerMethodBTCEigenwaves
except ImportError:
    print("Warning: Could not import HMM or Power Method modules. Using standalone implementation.")
    # Define colors if modules not found
    COLORS = {
        'background': '#0d1117',
        'text': '#c9d1d9',
        'grid': '#21262d',
        'positive': '#3fb950',
        'negative': '#f85149',
        'neutral': '#8b949e',
        'state_0': '#e6194B',  # Markdown/Bear
        'state_1': '#3cb44b',  # Markup/Bull
        'state_2': '#ffe119',  # Accumulation
        'state_3': '#4363d8',  # Distribution
        'state_4': '#911eb4',  # Fakeout/Liquidity Grab
        'state_5': '#f58231',  # Consolidation
    }
    
    MARKET_STATES = [
        "Markdown (Bear)",
        "Markup (Bull)",
        "Accumulation",
        "Distribution",
        "Liquidity Grab",
        "Consolidation"
    ]

# Set Plotly theme for divine visuals
pio.templates.default = "plotly_dark"

# Suppress warnings
warnings.filterwarnings("ignore")

# Define the device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_btc_data(start_date: str = "2020-01-01", end_date: str | None = None) -> pd.DataFrame | None:
    """
    Load BTC historical data.
    
    Args:
        start_date: Start date for data in YYYY-MM-DD format
        end_date: End date for data in YYYY-MM-DD format
        
    Returns:
        DataFrame with BTC price data or None if loading fails
    """
    try:
        import yfinance as yf
        
        # Download data
        print("Downloading BTC data from yfinance...")
        btc = yf.download("BTC-USD", start=start_date, end=end_date, auto_adjust=True)
        
        # Check if data is retrieved
        if btc is None or btc.empty:
            print("No data retrieved from yfinance")
            return None
        
        # Extract columns
        print(f"Original columns: {btc.columns}")
        if isinstance(btc.columns, pd.MultiIndex):
            btc.columns = [col[0].lower() for col in btc.columns]
        else:
            btc.columns = [col.lower() for col in btc.columns]
        print(f"Processed columns: {btc.columns}")
        
        # Reset index to have Date as a column
        btc = btc.reset_index()
        print(f"Final columns: {btc.columns}")
        
        return btc
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

class Encoder(nn.Module):
    """Encoder network for the variational autoencoder."""
    def __init__(self, input_dim, hidden_dim, latent_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc_mu = nn.Linear(hidden_dim, latent_dim)
        self.fc_logvar = nn.Linear(hidden_dim, latent_dim)
        
    def forward(self, x):
        h = F.relu(self.fc1(x))
        mu = self.fc_mu(h)
        logvar = self.fc_logvar(h)
        return mu, logvar

class Decoder(nn.Module):
    """Decoder network for the variational autoencoder."""
    def __init__(self, latent_dim, hidden_dim, output_dim):
        super().__init__()
        self.fc1 = nn.Linear(latent_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x):
        h = F.relu(self.fc1(x))
        return self.fc2(h)

class VariationalInferenceBTCCycle(nn.Module):
    """Variational inference model for BTC market cycles."""
    
    def __init__(self, input_dim: int = 5, hidden_dim: int = 64, latent_dim: int = 32, 
                 sequence_length: int = 100, learning_rate: float = 1e-3, beta: float = 1.0):
        """
        Initialize the variational inference model.
        
        Args:
            input_dim: Dimension of input features
            hidden_dim: Dimension of hidden layers
            latent_dim: Dimension of latent space
            sequence_length: Length of input sequences
            learning_rate: Learning rate for optimizer
            beta: Weight of KL divergence term
        """
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.latent_dim = latent_dim
        self.sequence_length = sequence_length
        self.learning_rate = learning_rate
        self.beta = beta
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Initialize encoder and decoder
        self.encoder = Encoder(input_dim, hidden_dim, latent_dim)
        self.decoder = Decoder(latent_dim, hidden_dim, input_dim)
        
        # Move to device
        self.encoder = self.encoder.to(self.device)
        self.decoder = self.decoder.to(self.device)
        self.model_path = None
        
    def reparameterize(self, mu, logvar):
        """Reparameterization trick for sampling from latent space."""
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std
        
    def predict(self, df: pd.DataFrame) -> int:
        """
        Predict the current market cycle phase.
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            int: Predicted cycle phase (0-3)
        """
        try:
            if self.encoder is None or self.decoder is None:
                logger.warning("Model not fitted. Using simple cycle detection.")
                return self._simple_cycle_detection(df)
            
            # Prepare input features
            features = self._prepare_features(df)
            features_tensor = torch.FloatTensor(features)
            
            # Encode to latent space
            mu, logvar = self.encoder(features_tensor)
            z = self.reparameterize(mu, logvar)
            
            # Decode to reconstruct input
            reconstructed = self.decoder(z)
            
            # Determine cycle phase based on reconstruction error
            return self._determine_cycle_phase(features_tensor, reconstructed)
            
        except Exception as e:
            logger.error(f"Error in prediction: {e}")
            return self._simple_cycle_detection(df)
            
    def _simple_cycle_detection(self, df: pd.DataFrame) -> int:
        """
        Simple cycle detection based on price and volume patterns.
        
        Args:
            df: DataFrame with OHLCV data
            
        Returns:
            int: Detected cycle phase (0-3)
        """
        try:
            # Calculate basic indicators
            returns = df['close'].pct_change()
            volume_change = df['volume'].pct_change()
            
            # Calculate moving averages
            ma_short = df['close'].rolling(window=20).mean()
            ma_long = df['close'].rolling(window=50).mean()
            
            # Get latest values
            latest_returns = returns.iloc[-1]
            latest_volume = volume_change.iloc[-1]
            latest_ma_ratio = ma_short.iloc[-1] / ma_long.iloc[-1]
            
            # Determine cycle phase
            if latest_returns > 0 and latest_ma_ratio > 1:
                return 1  # Markup phase
            elif latest_returns < 0 and latest_ma_ratio < 1:
                return 0  # Markdown phase
            elif abs(latest_returns) < 0.01 and latest_volume > 0:
                return 2  # Accumulation phase
            else:
                return 3  # Distribution phase
                
        except Exception as e:
            logger.error(f"Error in simple cycle detection: {e}")
            return 0  # Default to markdown phase
            
    def _prepare_features(self, df: pd.DataFrame) -> np.ndarray:
        """Prepare input features from DataFrame."""
        features = pd.DataFrame()
        
        # Price changes
        features['price_change'] = df['close'].pct_change()
        features['volume_change'] = df['volume'].pct_change()
        
        # High-Low range
        features['high_low_range'] = (df['high'] - df['low']) / df['close']
        
        # Open-Close range
        features['open_close_range'] = (df['close'] - df['open']) / df['open']
        
        # Volume/Price ratio
        features['volume_price_ratio'] = df['volume'] / df['close']
        
        # Fill NaN values
        features = features.fillna(0)
        
        # Normalize features
        features = (features - features.mean()) / features.std()
        
        return features.values
        
    def _determine_cycle_phase(self, input_tensor, reconstructed_tensor):
        """Determine cycle phase based on reconstruction error."""
        # Calculate reconstruction error
        error = torch.mean((input_tensor - reconstructed_tensor) ** 2, dim=1)
        
        # Map error to cycle phase
        if error.mean() < 0.1:
            return 2  # Accumulation
        elif error.mean() < 0.3:
            return 1  # Markup
        elif error.mean() < 0.5:
            return 3  # Distribution
        else:
            return 0  # Markdown
    
    def forward(self, x):
        """
        Forward pass through the model.
        
        Args:
            x: Input tensor
            
        Returns:
            Reconstructed input, mean, log variance
        """
        # Encode
        mu, logvar = self.encoder(x)
        
        # Sample from latent distribution
        z = self.reparameterize(mu, logvar)
        
        # Decode
        x_recon = self.decoder(z)
        
        return x_recon, mu, logvar
    
    def _calculate_loss(self, x, x_recon, mu, logvar):
        """
        Calculate the ELBO loss: reconstruction + KL divergence.
        
        Args:
            x: Original input
            x_recon: Reconstructed input
            mu: Mean of latent Gaussian
            logvar: Log variance of latent Gaussian
            
        Returns:
            Total loss, reconstruction loss, KL divergence
        """
        # Reconstruction loss - Mean Squared Error
        recon_loss = F.mse_loss(x_recon, x, reduction='sum')
        
        # KL divergence
        kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
        
        # Total loss
        total_loss = recon_loss + self.beta * kl_loss
        
        return total_loss, recon_loss, kl_loss
    
    def train_model(self, dataloader, num_epochs=100, learning_rate=1e-3):
        """
        Train the variational autoencoder.
        
        Args:
            dataloader: DataLoader with training data
            num_epochs: Number of training epochs
            learning_rate: Learning rate for optimizer
            
        Returns:
            Dictionary of training history
        """
        optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate)
        history = {
            'loss': [],
            'recon_loss': [],
            'kl_loss': []
        }
        
        for epoch in range(num_epochs):
            epoch_loss = 0
            epoch_recon_loss = 0
            epoch_kl_loss = 0
            
            for batch in dataloader:
                # DataLoader returns a tuple of tensors when using TensorDataset
                # Extract the actual data tensor from the batch
                if isinstance(batch, tuple):
                    data = batch[0]
                else:
                    data = batch
                
                # Move data to device
                data = data.to(self.device)
                
                # Forward pass
                optimizer.zero_grad()
                recon_batch, mu, logvar = self(data)
                
                # Compute loss
                recon_loss = F.mse_loss(recon_batch, data)
                kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
                
                # Total loss
                loss = recon_loss + self.beta * kl_loss
                
                # Backward pass and optimize
                loss.backward()
                optimizer.step()
                
                # Update metrics
                epoch_loss += loss.item()
                epoch_recon_loss += recon_loss.item()
                epoch_kl_loss += kl_loss.item()
            
            # Epoch metrics
            avg_loss = epoch_loss / len(dataloader)
            avg_recon_loss = epoch_recon_loss / len(dataloader)
            avg_kl_loss = epoch_kl_loss / len(dataloader)
            
            # Update history
            history['loss'].append(avg_loss)
            history['recon_loss'].append(avg_recon_loss)
            history['kl_loss'].append(avg_kl_loss)
            
            # Print progress every 10 epochs
            if (epoch + 1) % 10 == 0:
                print(f"Epoch {epoch+1}/{num_epochs}, Loss: {avg_loss:.4f}, Recon: {avg_recon_loss:.4f}, KL: {avg_kl_loss:.4f}")
        
        return history
    
    def encode(self, x):
        """
        Encode input data to the latent space.
        
        Args:
            x: Input tensor
            
        Returns:
            Mean and log variance of latent Gaussian
        """
        self.encoder.eval()
        with torch.no_grad():
            x = torch.tensor(x, dtype=torch.float32).to(self.device)
            mu, logvar = self.encoder(x)
        
        return mu, logvar
    
    def decode(self, z):
        """
        Decode latent vectors to the original space.
        
        Args:
            z: Latent vectors
            
        Returns:
            Reconstructed data
        """
        self.decoder.eval()
        with torch.no_grad():
            z = torch.tensor(z, dtype=torch.float32).to(self.device)
            x_recon = self.decoder(z)
        
        return x_recon.cpu().numpy()
    
    def generate_cycles(self, num_samples=10):
        """
        Generate BTC market cycles from the latent space.
        
        Args:
            num_samples: Number of cycles to generate
            
        Returns:
            Generated market cycles
        """
        # Sample from the latent space
        z = torch.randn(num_samples, self.latent_dim).to(self.device)
        
        # Decode samples
        cycles = self.decode(z)
        
        return cycles
    
    def prepare_data(self, df, feature_col='close', window_size=None):
        """
        Prepare data sequences for the model.
        
        Args:
            df: DataFrame with BTC price data
            feature_col: Column to use for sequences (default: 'close')
            window_size: Size of the sliding window (default: self.sequence_length)
            
        Returns:
            Preprocessed sequences as a PyTorch DataLoader
        """
        from torch.utils.data import DataLoader, TensorDataset
        
        window_size = window_size or self.sequence_length
        
        # Extract the feature column
        series = df[feature_col].values
        
        # Normalize the data
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        scaled = scaler.fit_transform(series.reshape(-1, 1)).flatten()
        
        # Create sequences
        sequences = []
        for i in range(len(scaled) - window_size + 1):
            sequences.append(scaled[i:i+window_size])
        
        # Convert to tensor
        sequences_tensor = torch.tensor(sequences, dtype=torch.float32)
        
        # Create DataLoader
        dataset = TensorDataset(sequences_tensor)
        dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
        
        return dataloader, scaler
    
    def plot_latent_space(self, dataloader):
        """
        Visualize the latent space.
        
        Args:
            dataloader: DataLoader with data to encode
            
        Returns:
            Plotly figure
        """
        # Encode all data points
        all_mu = []
        all_logvar = []
        
        self.encoder.eval()
        with torch.no_grad():
            for batch_idx, (data,) in enumerate(dataloader):
                data = data.to(self.device)
                mu, logvar = self.encoder(data)
                
                all_mu.append(mu.cpu().numpy())
                all_logvar.append(logvar.cpu().numpy())
        
        all_mu = np.vstack(all_mu)
        all_logvar = np.vstack(all_logvar)
        
        # Create figure
        fig = go.Figure()
        
        # Add scatter plot of latent space
        if self.latent_dim >= 2:
            fig.add_trace(go.Scatter(
                x=all_mu[:, 0],
                y=all_mu[:, 1],
                mode='markers',
                marker=dict(
                    size=8,
                    color=all_mu[:, 0],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title='Latent Dimension 1')
                ),
                name='Latent Space'
            ))
        else:
            # For 1D latent space
            fig.add_trace(go.Scatter(
                x=all_mu[:, 0],
                y=np.zeros_like(all_mu[:, 0]),
                mode='markers',
                marker=dict(
                    size=8,
                    color=all_mu[:, 0],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title='Latent Dimension')
                ),
                name='Latent Space'
            ))
        
        # Update layout
        fig.update_layout(
            title='BTC Market Cycle Latent Space',
            xaxis_title='Latent Dimension 1',
            yaxis_title='Latent Dimension 2' if self.latent_dim >= 2 else '',
            template='plotly_dark',
            width=900,
            height=700
        )
        
        return fig
    
    def fit(self, df, epochs=100, batch_size=32, learning_rate=1e-3):
        """Train the variational autoencoder on market data."""
        try:
            # Prepare input features
            features = self._prepare_features(df)
            features_tensor = torch.FloatTensor(features)
            
            # Initialize encoder and decoder if not already done
            if self.encoder is None:
                self.encoder = Encoder(self.input_dim, self.hidden_dim, self.latent_dim)
                
            if self.decoder is None:
                self.decoder = Decoder(self.latent_dim, self.hidden_dim, self.input_dim)
                
            # Initialize optimizer
            optimizer = torch.optim.Adam(
                list(self.encoder.parameters()) + list(self.decoder.parameters()),
                lr=learning_rate
            )
            
            # Training loop
            for epoch in range(epochs):
                # Forward pass
                mu, logvar = self.encoder(features_tensor)
                z = self.reparameterize(mu, logvar)
                reconstructed = self.decoder(z)
                
                # Compute loss
                recon_loss = F.mse_loss(reconstructed, features_tensor)
                kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
                loss = recon_loss + 0.1 * kl_loss
                
                # Backward pass and optimization
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                
                if (epoch + 1) % 10 == 0:
                    logger.info(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")
                
            return self
            
        except Exception as e:
            logger.error(f"Error in training: {e}")
            raise
        
    def save_model(self, filepath):
        """Save the trained model to a file."""
        try:
            model_data = {
                'encoder_state_dict': self.encoder.state_dict() if self.encoder else None,
                'decoder_state_dict': self.decoder.state_dict() if self.decoder else None,
                'input_dim': self.input_dim,
                'hidden_dim': self.hidden_dim,
                'latent_dim': self.latent_dim
            }
            torch.save(model_data, filepath)
            self.model_path = filepath
            logger.info(f"Model saved to {filepath}")
            
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            raise
        
    def load_model(self, filepath):
        """Load a trained model from a file."""
        try:
            model_data = torch.load(filepath)
            
            # Initialize model architecture
            self.input_dim = model_data['input_dim']
            self.hidden_dim = model_data['hidden_dim']
            self.latent_dim = model_data['latent_dim']
            
            # Initialize encoder and decoder
            self.encoder = Encoder(self.input_dim, self.hidden_dim, self.latent_dim)
            self.decoder = Decoder(self.latent_dim, self.hidden_dim, self.input_dim)
            
            # Load state dictionaries
            if model_data['encoder_state_dict']:
                self.encoder.load_state_dict(model_data['encoder_state_dict'])
            if model_data['decoder_state_dict']:
                self.decoder.load_state_dict(model_data['decoder_state_dict'])
                
            self.model_path = filepath
            logger.info(f"Model loaded from {filepath}")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise


def main():
    """Main function to train and save the model."""
    # Load data
    df = load_btc_data()
    if df is None:
        print("Failed to load data")
        return
    
    # Initialize model
    model = VariationalInferenceBTCCycle()
    
    # Prepare data
    dataloader, scaler = model.prepare_data(df)
    
    # Train model
    history = model.train_model(dataloader, num_epochs=100)
    
    # Save model
    model_path = os.path.join('models', 'variational_inference_btc_cycle.pkl')
    os.makedirs('models', exist_ok=True)
    model.save_model(model_path)
    
    print("✨ Training complete! Model saved to:", model_path)


if __name__ == "__main__":
    main() 