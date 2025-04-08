#!/usr/bin/env python3
"""
Quantum Encoding Data Loaders
===========================

Data loaders for the quantum encoding module.
Provides classes for loading market data and generating 
synthetic data for testing and development.
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Any, Optional, Union, cast
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("quantum-encoding-data")

class MarketDataLoader:
    """
    Loads and preprocesses market data for quantum encoding.
    
    This class handles loading market data from files, preprocessing it,
    and preparing it for quantum encoding.
    """
    
    def __init__(self, data_dir: str = 'data/aixbt_training_data', 
                default_file: str = 'aixbt_training_data.csv',
                fallback_to_synthetic: bool = True):
        """
        Initialize the market data loader.
        
        Args:
            data_dir (str): Directory containing market data files
            default_file (str): Default file to load
            fallback_to_synthetic (bool): Whether to generate synthetic data if file not found
        """
        self.data_dir = data_dir
        self.default_file = default_file
        self.fallback_to_synthetic = fallback_to_synthetic
        self.data: Optional[pd.DataFrame] = None
        self.loaded_file = None
        self.synthetic_generator = SyntheticDataGenerator()
        
        logger.info(f"🔮📊 MARKET DATA LOADER - Initialized with data directory: {data_dir}")
    
    def load_data(self, file_path: Optional[str] = None, 
                 columns: Optional[List[str]] = None,
                 start_date: Optional[str] = None,
                 end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Load market data from a CSV file.
        
        Args:
            file_path (str, optional): Path to the data file
            columns (List[str], optional): List of columns to load
            start_date (str, optional): Start date for filtering (YYYY-MM-DD)
            end_date (str, optional): End date for filtering (YYYY-MM-DD)
            
        Returns:
            pd.DataFrame: Loaded market data
        """
        # Determine file path
        if file_path is None:
            file_path = os.path.join(self.data_dir, self.default_file)
        elif not os.path.isabs(file_path):
            file_path = os.path.join(self.data_dir, file_path)
        
        # Try to load the data
        try:
            logger.info(f"🔮📊 MARKET DATA LOADER - Loading data from {file_path}")
            self.data = pd.read_csv(file_path)
            self.loaded_file = file_path
            
            # Filter columns if specified
            if columns is not None and self.data is not None:
                # Keep only columns that exist in the data
                valid_cols = [col for col in columns if col in self.data.columns]
                if len(valid_cols) < len(columns):
                    missing = set(columns) - set(valid_cols)
                    logger.warning(f"🔮📊 MARKET DATA LOADER - Columns not found: {missing}")
                self.data = self.data[valid_cols]
            
            # Filter by date if both start and end date are provided
            if self.data is not None and start_date is not None and end_date is not None and 'date' in self.data.columns:
                self.data['date'] = pd.to_datetime(self.data['date'])
                self.data = self.data[
                    (self.data['date'] >= start_date) & 
                    (self.data['date'] <= end_date)
                ]
            
            if self.data is not None:
                logger.info(f"🔮📊 MARKET DATA LOADER - Loaded {len(self.data)} rows with {len(self.data.columns)} columns")
            
        except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
            logger.warning(f"🔮📊 MARKET DATA LOADER - Failed to load {file_path}: {str(e)}")
            
            if self.fallback_to_synthetic:
                logger.info(f"🔮📊 MARKET DATA LOADER - Falling back to synthetic data")
                
                # Generate synthetic data with the same columns if available
                synthetic_file = os.path.join(self.data_dir, 'synthetic_data.csv')
                if os.path.exists(synthetic_file):
                    logger.info(f"🔮📊 MARKET DATA LOADER - Loading synthetic data from {synthetic_file}")
                    self.data = pd.read_csv(synthetic_file)
                    self.loaded_file = synthetic_file
                    
                else:
                    # Generate completely synthetic data
                    logger.info(f"🔮📊 MARKET DATA LOADER - Generating synthetic data")
                    rows = 100
                    feature_names = ['price', 'volume', 'volatility', 'momentum']
                    if columns is not None:
                        feature_names = columns
                        
                    features = self.synthetic_generator.generate_feature_matrix(
                        num_samples=rows, 
                        num_features=len(feature_names),
                        feature_correlation=0.3
                    )
                    
                    # Create DataFrame with synthetic data
                    self.data = pd.DataFrame(features, columns=feature_names)
                    
                    # Add date column if filtering by date
                    if self.data is not None and (start_date is not None or 'date' in feature_names):
                        end = datetime.now()
                        start = end - timedelta(days=rows)
                        dates = [start + timedelta(days=i) for i in range(rows)]
                        self.data['date'] = dates
                        
                    # Save synthetic data for future use
                    os.makedirs(self.data_dir, exist_ok=True)
                    if self.data is not None:
                        self.data.to_csv(synthetic_file, index=False)
                        self.loaded_file = synthetic_file
                    
                if self.data is not None:
                    logger.info(f"🔮📊 MARKET DATA LOADER - Generated {len(self.data)} rows of synthetic data")
            else:
                # If not falling back to synthetic data, raise the exception
                raise
        
        # Ensure we always return a DataFrame
        if self.data is None:
            self.data = pd.DataFrame()
            logger.warning("🔮📊 MARKET DATA LOADER - No data was loaded, returning empty DataFrame")
            
        return self.data
    
    def get_feature_vector(self, feature_name: str) -> np.ndarray:
        """
        Get a specific feature vector from the loaded data.
        
        Args:
            feature_name (str): Name of the feature to retrieve
            
        Returns:
            np.ndarray: Feature vector
        """
        if self.data is None:
            self.load_data()
            
        if self.data is None or feature_name not in self.data.columns:
            raise ValueError(f"Feature '{feature_name}' not found in data. Available features: {list(self.data.columns if self.data is not None else [])}")
        
        return self.data[feature_name].to_numpy()
    
    def get_feature_matrix(self, feature_names: List[str]) -> np.ndarray:
        """
        Get multiple feature vectors as a matrix.
        
        Args:
            feature_names (List[str]): Names of features to retrieve
            
        Returns:
            np.ndarray: Feature matrix with shape (samples, features)
        """
        if self.data is None:
            self.load_data()
            
        if self.data is None:
            raise ValueError("No data available")
            
        # Check if all features exist
        missing = [f for f in feature_names if f not in self.data.columns]
        if missing:
            raise ValueError(f"Features not found in data: {missing}. Available features: {list(self.data.columns)}")
        
        return self.data[feature_names].to_numpy()
    
    def split_data(self, feature_names: List[str], test_size: float = 0.2, 
                 random_state: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Split data into training and test sets.
        
        Args:
            feature_names (List[str]): Features to include
            test_size (float): Fraction of data to use for testing
            random_state (int, optional): Random seed for reproducibility
            
        Returns:
            Tuple[np.ndarray, np.ndarray]: (train_data, test_data)
        """
        if self.data is None:
            self.load_data()
            
        data = self.get_feature_matrix(feature_names)
        
        # Determine split index
        n_samples = len(data)
        test_samples = int(n_samples * test_size)
        train_samples = n_samples - test_samples
        
        # Shuffle if random_state is provided
        if random_state is not None:
            np.random.seed(random_state)
            indices = np.random.permutation(n_samples)
            train_indices = indices[:train_samples]
            test_indices = indices[train_samples:]
        else:
            # Simple split without shuffling
            train_indices = np.arange(train_samples)
            test_indices = np.arange(train_samples, n_samples)
        
        train_data = data[train_indices]
        test_data = data[test_indices]
        
        logger.info(f"🔮📊 MARKET DATA LOADER - Split data into {len(train_data)} train and {len(test_data)} test samples")
        
        return train_data, test_data


class SyntheticDataGenerator:
    """
    Generates synthetic market data for testing quantum encoding.
    
    This class provides methods to generate synthetic market data
    with controllable properties like volatility, trends, and correlations.
    """
    
    def __init__(self, seed: Optional[int] = 42):
        """
        Initialize the synthetic data generator.
        
        Args:
            seed (int, optional): Random seed for reproducibility
        """
        self.seed = seed
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
        
        logger.info(f"🔮🧪 SYNTHETIC DATA GENERATOR - Initialized synthetic data generator with seed {seed}")
    
    def generate_random_walk(self, n_steps: int, drift: float = 0.0, 
                            volatility: float = 1.0, 
                            starting_value: float = 100.0) -> np.ndarray:
        """
        Generate a random walk time series.
        
        Args:
            n_steps (int): Number of steps
            drift (float): Drift parameter
            volatility (float): Volatility parameter
            starting_value (float): Starting value
            
        Returns:
            np.ndarray: Random walk time series
        """
        steps = np.random.normal(loc=drift, scale=volatility, size=n_steps)
        return starting_value + np.cumsum(steps)
    
    def generate_sine_wave(self, n_steps: int, frequency: float = 0.1, 
                          amplitude: float = 1.0, phase: float = 0.0,
                          noise_level: float = 0.1) -> np.ndarray:
        """
        Generate a sine wave with optional noise.
        
        Args:
            n_steps (int): Number of points
            frequency (float): Frequency of the sine wave
            amplitude (float): Amplitude of the sine wave
            phase (float): Phase shift
            noise_level (float): Amount of noise to add
            
        Returns:
            np.ndarray: Sine wave time series
        """
        x = np.linspace(0, 2 * np.pi, n_steps)
        y = amplitude * np.sin(frequency * x + phase)
        
        if noise_level > 0:
            noise = np.random.normal(0, noise_level, n_steps)
            y += noise
            
        return y
    
    def generate_feature_matrix(self, num_samples: int = 100, 
                               num_features: int = 4,
                               feature_correlation: float = 0.5) -> np.ndarray:
        """
        Generate a matrix of correlated features.
        
        Args:
            num_samples (int): Number of samples
            num_features (int): Number of features
            feature_correlation (float): Correlation between features
            
        Returns:
            np.ndarray: Feature matrix with shape (num_samples, num_features)
        """
        # Generate correlation matrix with the given correlation
        corr_matrix = np.ones((num_features, num_features))
        for i in range(num_features):
            for j in range(i+1, num_features):
                # Random correlation centered around feature_correlation
                r = feature_correlation + 0.2 * np.random.randn()
                # Ensure correlation is between -1 and 1
                r = max(min(r, 0.99), -0.99)
                corr_matrix[i, j] = r
                corr_matrix[j, i] = r
        
        # Ensure the matrix is positive definite by applying a small regularization
        min_eig = np.min(np.linalg.eigvals(corr_matrix))
        if min_eig < 0:
            # Add a small positive value to the diagonal
            corr_matrix += np.eye(num_features) * (abs(min_eig) + 1e-5)
            
            # Ensure diagonal elements are 1 (proper correlation matrix)
            for i in range(num_features):
                corr_matrix[i, i] = 1.0
            
            # Normalize to ensure valid correlation values
            for i in range(num_features):
                for j in range(i+1, num_features):
                    corr_matrix[i, j] = min(0.99, corr_matrix[i, j] / np.sqrt(corr_matrix[i, i] * corr_matrix[j, j]))
                    corr_matrix[j, i] = corr_matrix[i, j]
        
        try:
            # Generate features using Cholesky decomposition
            L = np.linalg.cholesky(corr_matrix)
            uncorrelated = np.random.randn(num_samples, num_features)
            features = np.dot(uncorrelated, L.T)
        except np.linalg.LinAlgError:
            # Fallback to simpler approach if Cholesky decomposition fails
            logger.warning("🔮🧪 SYNTHETIC DATA GENERATOR - Cholesky decomposition failed, falling back to simple generation")
            features = np.random.randn(num_samples, num_features)
            
            # Add some correlation
            for i in range(1, num_features):
                features[:, i] = feature_correlation * features[:, 0] + np.sqrt(1 - feature_correlation**2) * features[:, i]
        
        logger.info(f"🔮🧪 SYNTHETIC DATA GENERATOR - Generated feature matrix with shape ({num_samples}, {num_features})")
        
        return features
    
    def generate_market_dataset(self, num_samples: int = 100, 
                              include_price: bool = True,
                              include_volume: bool = True,
                              include_volatility: bool = True,
                              include_sentiment: bool = False) -> pd.DataFrame:
        """
        Generate a synthetic market dataset with multiple features.
        
        Args:
            num_samples (int): Number of samples
            include_price (bool): Whether to include price data
            include_volume (bool): Whether to include volume data
            include_volatility (bool): Whether to include volatility
            include_sentiment (bool): Whether to include sentiment scores
            
        Returns:
            pd.DataFrame: Synthetic market dataset
        """
        data: Dict[str, Any] = {}
        
        # Generate dates
        end_date = datetime.now()
        start_date = end_date - timedelta(days=num_samples)
        dates = [start_date + timedelta(days=i) for i in range(num_samples)]
        data['date'] = dates
        
        # Generate price data
        price_data = None
        if include_price:
            price_data = self.generate_random_walk(
                n_steps=num_samples, 
                drift=0.01, 
                volatility=0.5, 
                starting_value=100.0
            )
            data['price'] = price_data
            
            # Add price derivatives
            data['return'] = np.concatenate(([0], np.diff(price_data) / price_data[:-1]))
            data['log_return'] = np.concatenate(([0], np.diff(np.log(price_data))))
        
        # Generate volume data
        if include_volume:
            # Volume often correlates with volatility
            volume_base = np.abs(np.random.normal(loc=1e6, scale=2e5, size=num_samples))
            # Add some spikes
            spikes = np.random.randint(0, num_samples, size=5)
            volume_base[spikes] *= 3
            data['volume'] = volume_base
        
        # Generate volatility
        if include_volatility:
            # Start with base volatility
            vol = np.abs(self.generate_sine_wave(
                n_steps=num_samples,
                frequency=0.02,
                amplitude=0.15,
                noise_level=0.05
            ))
            # Add volatility clustering
            for i in range(1, num_samples):
                vol[i] = 0.8 * vol[i-1] + 0.2 * vol[i]
            data['volatility'] = vol
        
        # Generate sentiment scores
        if include_sentiment:
            # Sentiment often follows price with some lag
            if include_price and price_data is not None:
                # Lagged price influence
                price_norm = (price_data - np.mean(price_data)) / np.std(price_data)
                sentiment = 0.5 * np.roll(price_norm, 5)
                # Fill the rolled values
                sentiment[:5] = sentiment[5]
            else:
                # Independent sentiment
                sentiment = self.generate_sine_wave(
                    n_steps=num_samples,
                    frequency=0.05,
                    amplitude=0.8,
                    noise_level=0.3
                )
            
            # Scale to range [-1, 1]
            sentiment = np.clip(sentiment, -1, 1)
            data['sentiment'] = sentiment
        
        logger.info(f"🔮🧪 SYNTHETIC DATA GENERATOR - Generated synthetic market dataset with {num_samples} samples")
        
        return pd.DataFrame(data) 