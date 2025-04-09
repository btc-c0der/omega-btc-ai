#!/usr/bin/env python3
"""
Market Data Utilities
====================

Helper functions for loading, preprocessing, and analyzing market data
for the Core Divergence Predictor.
"""

import os
import numpy as np
import pandas as pd
import logging
from typing import Dict, List, Tuple, Optional, Union, Any
from datetime import datetime, timedelta
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import talib
from talib import abstract

# Configure logging
logger = logging.getLogger("market-data-utils")

def load_market_data(data_path: str, filename: str) -> pd.DataFrame:
    """
    Load market data from CSV file.
    
    Args:
        data_path: Directory containing market data
        filename: CSV filename
        
    Returns:
        DataFrame with market data
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    file_path = Path(data_path) / filename
    
    if not file_path.exists():
        raise FileNotFoundError(f"Market data file not found at {file_path}")
    
    logger.info(f"Loading market data from {file_path}")
    df = pd.read_csv(file_path)
    
    # Convert timestamp to datetime if present
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
    elif 'date' in df.columns:
        df['timestamp'] = pd.to_datetime(df['date'])
        df = df.drop('date', axis=1)
    
    # Make sure all required columns exist
    required_columns = ['open', 'high', 'low', 'close', 'volume']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Missing required columns in data: {missing_columns}")
    
    logger.info(f"Loaded {len(df)} rows of market data")
    return df

def generate_synthetic_data(days: int = 365, 
                           volatility: float = 0.02,
                           trend: float = 0.0001,
                           start_price: float = 45000.0,
                           volume_scale: float = 1000000.0) -> pd.DataFrame:
    """
    Generate synthetic BTC market data for testing.
    
    Args:
        days: Number of days of data
        volatility: Daily price volatility
        trend: Daily price trend
        start_price: Starting price
        volume_scale: Volume scaling factor
        
    Returns:
        DataFrame with synthetic market data
    """
    np.random.seed(42)  # For reproducibility
    
    # Generate timestamps
    end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = end_date - timedelta(days=days)
    timestamps = pd.date_range(start=start_date, end=end_date, freq='1H')
    
    # Generate price data with random walk
    n = len(timestamps)
    price_changes = np.random.normal(trend, volatility, n)
    
    # Calculate prices
    close_prices = start_price * np.cumprod(1 + price_changes)
    
    # Generate open, high, low prices
    open_prices = np.roll(close_prices, 1)
    open_prices[0] = start_price
    
    # Daily volatility for high-low range
    high_prices = close_prices * (1 + np.abs(np.random.normal(0, volatility * 0.5, n)))
    low_prices = close_prices * (1 - np.abs(np.random.normal(0, volatility * 0.5, n)))
    
    # Ensure high is always the highest and low is always the lowest
    for i in range(n):
        prices = [open_prices[i], close_prices[i], high_prices[i], low_prices[i]]
        high_prices[i] = max(prices)
        low_prices[i] = min(prices)
    
    # Generate volume data (higher during price movements)
    volume = volume_scale * (1 + np.abs(price_changes) * 10) * np.random.lognormal(0, 0.5, n)
    
    # Create DataFrame
    data = {
        'timestamp': timestamps,
        'open': open_prices,
        'high': high_prices,
        'low': low_prices,
        'close': close_prices,
        'volume': volume
    }
    
    df = pd.DataFrame(data)
    logger.info(f"Generated {len(df)} rows of synthetic market data")
    
    return df

def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate technical indicators for market data.
    
    Args:
        df: DataFrame with OHLCV data
        
    Returns:
        DataFrame with added technical indicators
    """
    # Create a copy to avoid modifying the original
    df_with_indicators = df.copy()
    
    # Ensure df has the necessary columns
    required_cols = ['open', 'high', 'low', 'close', 'volume']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"DataFrame is missing required columns. Needed: {required_cols}")
    
    # Calculate RSI (Relative Strength Index)
    df_with_indicators['rsi'] = talib.RSI(df['close'].values, timeperiod=14)
    
    # Calculate MACD (Moving Average Convergence Divergence)
    macd, macd_signal, macd_hist = talib.MACD(
        df['close'].values, 
        fastperiod=12, 
        slowperiod=26, 
        signalperiod=9
    )
    df_with_indicators['macd'] = macd
    df_with_indicators['macd_signal'] = macd_signal
    df_with_indicators['macd_hist'] = macd_hist
    
    # Calculate Bollinger Bands
    upper, middle, lower = talib.BBANDS(
        df['close'].values, 
        timeperiod=20, 
        nbdevup=2, 
        nbdevdn=2, 
        matype=0
    )
    df_with_indicators['bb_upper'] = upper
    df_with_indicators['bb_middle'] = middle
    df_with_indicators['bb_lower'] = lower
    
    # Calculate ADX (Average Directional Index)
    df_with_indicators['adx'] = talib.ADX(
        df['high'].values, 
        df['low'].values, 
        df['close'].values, 
        timeperiod=14
    )
    
    # Calculate ATR (Average True Range)
    df_with_indicators['atr'] = talib.ATR(
        df['high'].values, 
        df['low'].values, 
        df['close'].values, 
        timeperiod=14
    )
    
    # Calculate moving averages
    df_with_indicators['sma_20'] = talib.SMA(df['close'].values, timeperiod=20)
    df_with_indicators['sma_50'] = talib.SMA(df['close'].values, timeperiod=50)
    df_with_indicators['sma_200'] = talib.SMA(df['close'].values, timeperiod=200)
    df_with_indicators['ema_20'] = talib.EMA(df['close'].values, timeperiod=20)
    
    # Calculate OBV (On-Balance Volume)
    df_with_indicators['obv'] = talib.OBV(df['close'].values, df['volume'].values)
    
    # Calculate MFI (Money Flow Index)
    df_with_indicators['mfi'] = talib.MFI(
        df['high'].values,
        df['low'].values,
        df['close'].values,
        df['volume'].values,
        timeperiod=14
    )
    
    # Calculate Stochastic Oscillator
    slowk, slowd = talib.STOCH(
        df['high'].values,
        df['low'].values,
        df['close'].values,
        fastk_period=5,
        slowk_period=3,
        slowk_matype=0,
        slowd_period=3,
        slowd_matype=0
    )
    df_with_indicators['stoch_k'] = slowk
    df_with_indicators['stoch_d'] = slowd
    
    # Calculate rate of change
    df_with_indicators['roc'] = talib.ROC(df['close'].values, timeperiod=10)
    
    # Calculate volatility
    df_with_indicators['volatility'] = df['close'].pct_change().rolling(window=20).std() * np.sqrt(252)
    
    logger.info("Calculated technical indicators for market data")
    
    return df_with_indicators

def normalize_features(
    df: pd.DataFrame, 
    feature_columns: List[str], 
    window: int = 20
) -> pd.DataFrame:
    """Normalize features using rolling Z-score normalization.
    
    Args:
        df: DataFrame with features
        feature_columns: List of columns to normalize
        window: Rolling window size for normalization
        
    Returns:
        DataFrame with normalized features
    """
    df_normalized = df.copy()
    
    for column in feature_columns:
        if column in df.columns:
            # Calculate rolling mean and standard deviation
            rolling_mean = df[column].rolling(window=window).mean()
            rolling_std = df[column].rolling(window=window).std()
            
            # Replace zero standard deviation with 1 to avoid division by zero
            rolling_std = rolling_std.replace(0, 1)
            
            # Calculate Z-score
            df_normalized[f'{column}_norm'] = (df[column] - rolling_mean) / rolling_std
    
    return df_normalized

def create_features_target(df: pd.DataFrame, 
                         feature_cols: List[str],
                         target_col: str = 'future_return',
                         horizon: int = 24,
                         sequence_length: int = 50) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create feature and target arrays for model training.
    
    Args:
        df: DataFrame with market data
        feature_cols: List of feature column names
        target_col: Target column name (usually 'future_return')
        horizon: Prediction horizon in hours
        sequence_length: Length of input sequences
        
    Returns:
        Tuple of (features, targets) as numpy arrays
    """
    # Calculate future returns if not already present
    if target_col not in df.columns:
        df[target_col] = df['close'].pct_change(periods=horizon).shift(-horizon)
    
    # Create feature array
    data = df[feature_cols].values
    features = []
    
    for i in range(len(data) - sequence_length + 1):
        features.append(data[i:i+sequence_length])
    
    features = np.array(features)
    
    # Create target array (corresponding to the last element of each sequence)
    targets = df[target_col].values[sequence_length-1:len(data)]
    
    # Remove NaN values
    mask = ~np.isnan(targets)
    features = features[mask]
    targets = targets[mask]
    
    logger.info(f"Created {len(features)} feature sequences with shape {features.shape}")
    
    return features, targets

def detect_anomalies(df: pd.DataFrame, 
                   window_size: int = 50,
                   threshold: float = 3.0) -> pd.DataFrame:
    """
    Detect anomalies in market data using Z-score.
    
    Args:
        df: DataFrame with market data
        window_size: Rolling window size
        threshold: Z-score threshold for anomaly detection
        
    Returns:
        DataFrame with anomaly flags
    """
    # Make a copy to avoid modifying the original
    result = df.copy()
    
    # Detect price anomalies
    rolling_mean = result['close'].rolling(window=window_size).mean()
    rolling_std = result['close'].rolling(window=window_size).std()
    z_score = (result['close'] - rolling_mean) / rolling_std
    
    result['price_anomaly'] = abs(z_score) > threshold
    
    # Detect volume anomalies
    rolling_vol_mean = result['volume'].rolling(window=window_size).mean()
    rolling_vol_std = result['volume'].rolling(window=window_size).std()
    vol_z_score = (result['volume'] - rolling_vol_mean) / rolling_vol_std
    
    result['volume_anomaly'] = abs(vol_z_score) > threshold
    
    # Combined anomaly flag
    result['is_anomaly'] = result['price_anomaly'] | result['volume_anomaly']
    
    # Count anomalies
    anomaly_count = result['is_anomaly'].sum()
    logger.info(f"Detected {anomaly_count} anomalies in {len(result)} data points")
    
    return result

def calculate_volatility(df: pd.DataFrame, 
                       window_size: int = 30) -> pd.DataFrame:
    """
    Calculate rolling volatility of market data.
    
    Args:
        df: DataFrame with market data
        window_size: Rolling window size
        
    Returns:
        DataFrame with volatility metrics
    """
    # Make a copy to avoid modifying the original
    result = df.copy()
    
    # Calculate returns
    result['return'] = result['close'].pct_change()
    
    # Calculate rolling volatility (annualized)
    # Assuming 365 trading days and hourly data
    trading_hours_per_year = 365 * 24
    result['volatility'] = result['return'].rolling(window=window_size).std() * np.sqrt(trading_hours_per_year)
    
    # Calculate Parkinson volatility (using high-low range)
    hl_ratio = np.log(result['high'] / result['low'])
    result['parkinson_volatility'] = np.sqrt((1/(4 * np.log(2))) * hl_ratio**2)
    
    # Calculate GARCH-type volatility (simplified)
    # Using exponentially weighted moving average
    result['garch_volatility'] = result['return'].ewm(span=window_size).std() * np.sqrt(trading_hours_per_year)
    
    return result

def split_train_test(
    X: np.ndarray,
    y: np.ndarray,
    test_size: float = 0.2,
    validation_size: float = 0.1,
    random_state: int = 42
) -> Dict[str, np.ndarray]:
    """Split data into training, validation, and test sets.
    
    Args:
        X: Feature matrix
        y: Target values
        test_size: Fraction of data to use for testing
        validation_size: Fraction of training data to use for validation
        random_state: Random seed for reproducibility
        
    Returns:
        Dictionary containing the split datasets
    """
    # First split into train+val and test
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # Then split train+val into train and val
    # Adjust validation_size to be relative to the train+val set
    val_ratio = validation_size / (1 - test_size)
    
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=val_ratio, random_state=random_state
    )
    
    return {
        'X_train': X_train,
        'X_val': X_val,
        'X_test': X_test,
        'y_train': y_train,
        'y_val': y_val,
        'y_test': y_test
    }

def create_sequences(
    df: pd.DataFrame,
    features: List[str],
    target: str,
    sequence_length: int = 30,
    prediction_horizon: int = 5
) -> Tuple[np.ndarray, np.ndarray]:
    """Create sequence data for time series forecasting.
    
    Args:
        df: DataFrame containing the data
        features: List of feature column names
        target: Target column name
        sequence_length: Length of input sequences
        prediction_horizon: How far ahead to predict
        
    Returns:
        Tuple of (X, y) containing input sequences and target values
    """
    X, y = [], []
    
    for i in range(len(df) - sequence_length - prediction_horizon + 1):
        X.append(df[features].iloc[i:i+sequence_length].values)
        y.append(df[target].iloc[i+sequence_length+prediction_horizon-1])
    
    return np.array(X), np.array(y)

def detect_regime_change(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """Detect market regime changes based on volatility and trend.
    
    Args:
        df: DataFrame with market data
        window: Window size for regime detection
        
    Returns:
        DataFrame with regime indicator column
    """
    df_regime = df.copy()
    
    # Calculate volatility change using ATR
    atr = calculate_atr(df_regime)
    atr_ratio = atr / atr.rolling(window=window).mean()
    
    # Calculate trend direction and strength
    price_trend = df_regime['close'].pct_change(window).fillna(0)
    
    # Define regime types:
    # 0: Low volatility, ranging market
    # 1: Medium volatility, trending market
    # 2: High volatility, potential regime change
    df_regime['regime'] = 0
    
    # Medium volatility, trending
    df_regime.loc[(atr_ratio > 0.8) & (atr_ratio < 1.2) & (abs(price_trend) > 0.02), 'regime'] = 1
    
    # High volatility, potential regime change
    df_regime.loc[atr_ratio > 1.5, 'regime'] = 2
    
    return df_regime

def identify_divergences(df: pd.DataFrame) -> pd.DataFrame:
    """Identify potential divergences between price and oscillators.
    
    Args:
        df: DataFrame with price and indicator data
        
    Returns:
        DataFrame with additional divergence columns
    """
    df_div = df.copy()
    
    # Regular bullish divergence: Price makes lower low but RSI makes higher low
    # Look back period for local extrema
    window = 5
    
    # Initialize divergence columns
    df_div['rsi_bullish_div'] = False
    df_div['rsi_bearish_div'] = False
    df_div['macd_bullish_div'] = False
    df_div['macd_bearish_div'] = False
    
    # Find local minima/maxima
    for i in range(window, len(df_div) - window):
        # Check if we have a local price minimum
        if (df_div['close'].iloc[i-window:i].min() > df_div['close'].iloc[i] and 
            df_div['close'].iloc[i+1:i+window+1].min() > df_div['close'].iloc[i]):
            
            # Check if RSI made a higher low compared to previous low
            rsi_min_idx = df_div['rsi'].iloc[max(0, i-15):i+1].idxmin()
            prev_rsi_window = df_div.loc[:rsi_min_idx-1]
            
            if len(prev_rsi_window) > 0:
                prev_rsi_min_idx = prev_rsi_window['rsi'].idxmin()
                
                if (df_div.loc[rsi_min_idx, 'close'] < df_div.loc[prev_rsi_min_idx, 'close'] and 
                    df_div.loc[rsi_min_idx, 'rsi'] > df_div.loc[prev_rsi_min_idx, 'rsi']):
                    df_div.loc[i, 'rsi_bullish_div'] = True
        
        # Check if we have a local price maximum
        if (df_div['close'].iloc[i-window:i].max() < df_div['close'].iloc[i] and 
            df_div['close'].iloc[i+1:i+window+1].max() < df_div['close'].iloc[i]):
            
            # Check if RSI made a lower high compared to previous high
            rsi_max_idx = df_div['rsi'].iloc[max(0, i-15):i+1].idxmax()
            prev_rsi_window = df_div.loc[:rsi_max_idx-1]
            
            if len(prev_rsi_window) > 0:
                prev_rsi_max_idx = prev_rsi_window['rsi'].idxmax()
                
                if (df_div.loc[rsi_max_idx, 'close'] > df_div.loc[prev_rsi_max_idx, 'close'] and 
                    df_div.loc[rsi_max_idx, 'rsi'] < df_div.loc[prev_rsi_max_idx, 'rsi']):
                    df_div.loc[i, 'rsi_bearish_div'] = True
    
    return df_div

def export_data_for_visualization(df: pd.DataFrame, 
                                output_path: str) -> None:
    """
    Export market data for visualization tools.
    
    Args:
        df: DataFrame with market data
        output_path: Path to save output file
        
    Returns:
        None
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Select relevant columns for visualization
    vis_cols = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    
    # Add technical indicators if available
    for col in ['rsi', 'macd', 'bollinger', 'volatility', 'is_anomaly']:
        if col in df.columns:
            vis_cols.append(col)
    
    # Extract data to export
    export_df = df[vis_cols].copy()
    
    # Convert timestamp to string if needed
    if pd.api.types.is_datetime64_any_dtype(export_df['timestamp']):
        export_df['timestamp'] = export_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Export to CSV
    export_df.to_csv(output_path, index=False)
    logger.info(f"Exported visualization data to {output_path}")
    
    return 