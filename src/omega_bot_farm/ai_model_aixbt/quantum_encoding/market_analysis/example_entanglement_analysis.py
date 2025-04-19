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
Quantum Entanglement Analysis Example
==================================

Example script demonstrating how to use the quantum entanglement analyzer
to detect critical market transitions and early warning signals.
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Any
import logging

# Add parent directories to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # quantum_encoding
grand_parent_dir = os.path.dirname(parent_dir)  # ai_model_aixbt
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
if grand_parent_dir not in sys.path:
    sys.path.append(grand_parent_dir)

# Import components
from . import (
    QuantumEntanglementAnalyzer,
    EntanglementMeasure,
    MarketTransitionType
)
from .. import MarketDataLoader, SyntheticDataGenerator

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("entanglement-analysis-example")


def load_market_data() -> Tuple[np.ndarray, List[str]]:
    """
    Load market data for analysis.
    
    Returns:
        Tuple of (data, feature_names)
    """
    # Initialize data loader with fallback to synthetic data
    loader = MarketDataLoader(
        data_dir="data/aixbt_training_data",
        fallback_to_synthetic=True
    )
    
    # Define key features for analysis
    feature_names = [
        'price', 'volume', 'volatility', 'momentum', 
        'rsi', 'macd', 'bollinger', 'fibonacci'
    ]
    
    try:
        # Try to load actual market data
        data = loader.load_data()
        logger.info(f"Loaded real market data with {len(data)} samples")
        
        # Check if all features exist
        missing_features = [f for f in feature_names if f not in data.columns]
        
        if missing_features:
            logger.warning(f"Missing features in real data: {missing_features}")
            logger.info("Generating synthetic data instead")
            raise ValueError("Missing required features")
            
        # Extract feature matrix
        features = loader.get_feature_matrix(feature_names)
        
    except Exception as e:
        logger.warning(f"Failed to load real market data: {e}")
        logger.info("Generating synthetic data with correlations and regime shifts")
        
        # Generate synthetic market dataset with regime shifts
        generator = SyntheticDataGenerator(seed=42)
        
        # Create base features
        n_samples = 500
        features = np.zeros((n_samples, len(feature_names)))
        
        # Generate price with regime shifts
        price = np.zeros(n_samples)
        
        # Normal regime (first 200 samples)
        price[:200] = generator.generate_random_walk(
            n_steps=200, drift=0.01, volatility=0.5, starting_value=100
        )
        
        # Transition period (samples 200-250)
        transition_start = 200
        transition_end = 250
        price[transition_start:transition_end] = generator.generate_random_walk(
            n_steps=transition_end-transition_start, 
            drift=-0.02, 
            volatility=1.0,
            starting_value=price[transition_start-1]
        )
        
        # Crisis regime (samples 250-350)
        crisis_start = 250
        crisis_end = 350
        price[crisis_start:crisis_end] = generator.generate_random_walk(
            n_steps=crisis_end-crisis_start,
            drift=-0.05,
            volatility=2.0,
            starting_value=price[crisis_start-1]
        )
        
        # Recovery regime (samples 350-500)
        recovery_start = 350
        price[recovery_start:] = generator.generate_random_walk(
            n_steps=n_samples-recovery_start,
            drift=0.03,
            volatility=0.7,
            starting_value=price[recovery_start-1]
        )
        
        # Store price in features
        features[:, 0] = price
        
        # Generate volume (correlated with price changes in some regimes)
        volume = np.zeros(n_samples)
        price_changes = np.concatenate([[0], np.diff(price)])
        
        # Normal volume
        volume[:transition_start] = 1000 + 500 * np.random.randn(transition_start)
        
        # Increased volume during transition
        volume[transition_start:transition_end] = 2000 + 1000 * np.random.randn(transition_end-transition_start)
        
        # High volume during crisis, correlated with price changes
        volume[crisis_start:crisis_end] = 3000 + 5000 * np.abs(price_changes[crisis_start:crisis_end]) + 1000 * np.random.randn(crisis_end-crisis_start)
        
        # Decreasing volume during recovery
        volume[recovery_start:] = 2000 + 800 * np.random.randn(n_samples-recovery_start)
        
        # Ensure positive volume
        volume = np.maximum(100, volume)
        features[:, 1] = volume
        
        # Generate volatility
        volatility = np.zeros(n_samples)
        window = 20  # Window for rolling volatility
        
        for i in range(window, n_samples):
            volatility[i] = np.std(price[i-window:i])
        
        # Fill initial values
        volatility[:window] = volatility[window]
        features[:, 2] = volatility
        
        # Generate momentum (price - MA)
        momentum = np.zeros(n_samples)
        window = 14  # Window for momentum
        
        for i in range(window, n_samples):
            momentum[i] = price[i] - np.mean(price[i-window:i])
        
        # Fill initial values
        momentum[:window] = momentum[window]
        features[:, 3] = momentum
        
        # Generate RSI
        rsi = np.zeros(n_samples)
        window = 14
        
        for i in range(window+1, n_samples):
            changes = price[i-window:i] - price[i-window-1:i-1]
            gains = np.sum(np.maximum(0, changes))
            losses = np.sum(np.maximum(0, -changes))
            
            if losses == 0:
                rsi[i] = 100
            else:
                rs = gains / losses
                rsi[i] = 100 - (100 / (1 + rs))
        
        # Fill initial values
        rsi[:window+1] = 50
        features[:, 4] = rsi
        
        # Generate MACD
        macd = np.zeros(n_samples)
        fast = 12
        slow = 26
        
        for i in range(slow, n_samples):
            fast_ema = np.mean(price[i-fast:i])
            slow_ema = np.mean(price[i-slow:i])
            macd[i] = fast_ema - slow_ema
        
        # Fill initial values
        macd[:slow] = macd[slow]
        features[:, 5] = macd
        
        # Generate Bollinger Bands (deviation from middle band)
        bollinger = np.zeros(n_samples)
        window = 20
        
        for i in range(window, n_samples):
            middle = np.mean(price[i-window:i])
            std = np.std(price[i-window:i])
            upper = middle + 2 * std
            lower = middle - 2 * std
            
            # Normalize to [-1, 1] where -1 is at lower band, +1 is at upper band
            if upper > lower:
                bollinger[i] = 2 * (price[i] - lower) / (upper - lower) - 1
        
        # Fill initial values
        bollinger[:window] = bollinger[window]
        features[:, 6] = bollinger
        
        # Generate Fibonacci retracement levels
        fibonacci = np.zeros(n_samples)
        for i in range(100, n_samples):
            # Find recent high and low
            local_high = np.max(price[i-100:i])
            local_low = np.min(price[i-100:i])
            range_price = local_high - local_low
            
            if range_price > 0:
                # Calculate how close price is to a Fibonacci level
                levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
                fib_prices = [local_high - level * range_price for level in levels]
                
                # Find closest level
                distances = [abs(price[i] - fib_price) for fib_price in fib_prices]
                closest_idx = np.argmin(distances)
                fibonacci[i] = levels[closest_idx]
        
        features[:, 7] = fibonacci
    
    return features, feature_names


def run_entanglement_analysis(data: np.ndarray, feature_names: List[str]) -> Dict[str, Any]:
    """
    Run quantum entanglement analysis on market data.
    
    Args:
        data: Market data
        feature_names: Feature names
        
    Returns:
        Analysis results
    """
    # Initialize the analyzer
    analyzer = QuantumEntanglementAnalyzer(
        window_size=50,
        overlap=10,
        entanglement_threshold=0.4,
        warning_threshold=0.7,
        critical_threshold=0.85
    )
    
    # Run analysis using entanglement witness measure
    results = analyzer.analyze_entanglement(
        data=data,
        feature_names=feature_names,
        measure=EntanglementMeasure.ENTANGLEMENT_WITNESS
    )
    
    # Get early warning signals
    warnings = analyzer.get_early_warning_signals(lookback=10)
    logger.info(f"Detected {len(warnings)} early warning signals")
    
    # Calculate instability index
    instability = analyzer.get_instability_index(recent_windows=10)
    logger.info(f"Market instability index: {instability:.4f}")
    
    # Create visualizations
    entanglement_fig = analyzer.visualize_entanglement()
    network_fig = analyzer.visualize_entanglement_network(window_index=-1)
    
    # Save figures
    output_dir = os.path.join(current_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    entanglement_fig.savefig(os.path.join(output_dir, "quantum_entanglement_analysis.png"))
    network_fig.savefig(os.path.join(output_dir, "entanglement_network.png"))
    
    logger.info(f"Saved visualizations to {output_dir}")
    
    # Add figures to results
    results["figures"] = {
        "entanglement": entanglement_fig,
        "network": network_fig
    }
    
    return results


def main():
    """Main function."""
    logger.info("Starting Quantum Entanglement Analysis Example")
    
    # Load market data
    data, feature_names = load_market_data()
    logger.info(f"Loaded data with shape {data.shape}")
    
    # Run entanglement analysis
    results = run_entanglement_analysis(data, feature_names)
    
    # Extract key results
    transitions = results["transition_signals"]
    total_transitions = sum(len(t) for t in transitions.values())
    
    # Summary
    logger.info("=" * 80)
    logger.info("QUANTUM ENTANGLEMENT ANALYSIS SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Data: {data.shape[0]} samples, {data.shape[1]} features")
    logger.info(f"Features: {', '.join(feature_names)}")
    logger.info(f"Detected {total_transitions} market transitions")
    logger.info(f"Visualizations saved to {os.path.join(current_dir, 'output')}")
    logger.info("=" * 80)
    
    logger.info("Example completed successfully")
    

if __name__ == "__main__":
    main() 