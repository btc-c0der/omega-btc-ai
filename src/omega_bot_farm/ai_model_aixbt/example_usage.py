#!/usr/bin/env python3
"""
Example Usage - Mock Quantum Divergence Predictor

This script demonstrates how to use the mock quantum divergence predictor
with sample data and provides a detailed walkthrough of the process.
"""

import os
import sys
import pandas as pd
import numpy as np
import logging
import random
from datetime import datetime, timedelta, timezone
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add the project root to sys.path if needed
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import the predictor directly from file path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mock_quantum_divergence_predictor import MockQuantumDivergencePredictor, run_mock_quantum_predictor

logger = logging.getLogger("quantum-example")

def generate_sample_data(days=30, volatility=0.015, divergence_magnitude=0.008):
    """
    Generate sample price data for BTC and AIXBT with controlled divergence patterns.
    
    Args:
        days: Number of days of data to generate
        volatility: Base volatility for price movements
        divergence_magnitude: Magnitude of divergence events
        
    Returns:
        DataFrame with timestamps, BTC and AIXBT prices
    """
    logger.info(f"Generating {days} days of sample data with volatility={volatility}")
    
    # Generate timestamps
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days)
    timestamps = [start_date + timedelta(hours=i*6) for i in range(days*4)]  # 4 data points per day
    
    # Seed for reproducibility
    random.seed(42)
    np.random.seed(42)
    
    # Generate BTC price (random walk with some trend)
    btc_price = 50000.0
    btc_prices = [btc_price]
    
    # Small upward trend
    trend = 0.0003
    
    for i in range(1, len(timestamps)):
        # Random movement with volatility
        movement = np.random.normal(trend, volatility)
        btc_price = btc_price * (1 + movement)
        btc_prices.append(btc_price)
    
    # Generate AIXBT price (mostly correlated with BTC but with divergence events)
    aixbt_price = 0.00012345
    aixbt_prices = [aixbt_price]
    
    # Create 3 divergence events
    divergence_events = [
        int(len(timestamps) * 0.25),  # First quarter
        int(len(timestamps) * 0.6),   # Middle-end
        int(len(timestamps) * 0.9)    # Near the end
    ]
    
    for i in range(1, len(timestamps)):
        # Base correlation with BTC
        btc_change = btc_prices[i] / btc_prices[i-1] - 1
        
        # Default small random divergence
        divergence = np.random.normal(0, 0.001)
        
        # Amplify divergence during divergence events
        for event_idx in divergence_events:
            # If within 8 data points (2 days) of a divergence event
            if abs(i - event_idx) < 8:
                # Create a pattern that builds up and resolves
                distance = abs(i - event_idx)
                event_impact = (1 - distance/8) * divergence_magnitude
                
                # Direction of divergence
                if i < event_idx:
                    # Building up - positive divergence
                    divergence += event_impact
                else:
                    # Resolving - negative divergence
                    divergence -= event_impact * 0.5
        
        # Apply the combined effect
        aixbt_price *= (1 + btc_change + divergence)
        aixbt_prices.append(aixbt_price)
    
    # Create DataFrame
    df = pd.DataFrame({
        "timestamp": timestamps,
        "btc_price": btc_prices,
        "aixbt_price": aixbt_prices
    })
    
    # Calculate the divergence for reference
    df['actual_divergence'] = (df['aixbt_price'] / df['aixbt_price'].shift(1)) / (df['btc_price'] / df['btc_price'].shift(1)) - 1
    
    logger.info(f"Generated sample data with {len(df)} data points")
    return df

def plot_data_and_predictions(df, predictions):
    """
    Plot the price data and predictions.
    
    Args:
        df: DataFrame with BTC and AIXBT prices
        predictions: List of prediction dictionaries
    """
    plt.figure(figsize=(14, 10))
    
    # Plot 1: Price movements
    plt.subplot(3, 1, 1)
    plt.title('BTC and AIXBT Price Movements (Normalized)')
    
    # Normalize prices to start at 1.0 for comparison
    btc_norm = df['btc_price'] / df['btc_price'].iloc[0]
    aixbt_norm = df['aixbt_price'] / df['aixbt_price'].iloc[0]
    
    plt.plot(df['timestamp'], btc_norm, label='BTC (normalized)', color='orange')
    plt.plot(df['timestamp'], aixbt_norm, label='AIXBT (normalized)', color='blue')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Actual divergence
    plt.subplot(3, 1, 2)
    plt.title('Actual Divergence Between AIXBT and BTC')
    plt.plot(df['timestamp'][1:], df['actual_divergence'][1:], color='red')
    plt.axhline(y=0, color='black', linestyle='--', alpha=0.3)
    plt.grid(True, alpha=0.3)
    
    # Plot 3: Predictions vs Actual
    plt.subplot(3, 1, 3)
    plt.title('Predicted vs Actual Divergence')
    
    # Plot actual divergence
    actual_dates = df['timestamp'][1:].tolist()
    actual_divergence = df['actual_divergence'][1:].tolist()
    plt.plot(actual_dates, actual_divergence, label='Actual', color='red', alpha=0.5)
    
    # Plot predictions
    if predictions:
        prediction_dates = []
        prediction_values = []
        confidence_values = []
        
        for pred in predictions:
            try:
                date = datetime.fromisoformat(pred['timestamp'].replace('Z', '+00:00'))
                prediction_dates.append(date)
                prediction_values.append(float(pred['predicted_divergence']))
                confidence_values.append(float(pred['confidence']))
            except (ValueError, KeyError) as e:
                logger.warning(f"Could not parse prediction: {e}")
        
        scatter = plt.scatter(prediction_dates, prediction_values, 
                             label='Predictions', 
                             c=confidence_values, 
                             cmap='viridis',
                             s=80,
                             zorder=5)
        plt.colorbar(scatter, label='Confidence')
    
    plt.axhline(y=0, color='black', linestyle='--', alpha=0.3)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Create the directory if it doesn't exist
    os.makedirs("outputs", exist_ok=True)
    
    # Save the plot
    plt.savefig("outputs/quantum_divergence_predictions.png")
    logger.info("Plot saved to outputs/quantum_divergence_predictions.png")
    
    # Display the plot
    plt.show()

def main():
    """Main function to demonstrate the quantum divergence predictor."""
    logger.info("Starting quantum divergence predictor example")
    
    # Generate sample data
    sample_data = generate_sample_data(days=30)
    
    # Save the sample data
    os.makedirs("data/aixbt_training_data", exist_ok=True)
    sample_data.to_csv("data/aixbt_training_data/example_data.csv", index=False)
    logger.info("Saved sample data to data/aixbt_training_data/example_data.csv")
    
    # Initialize the predictor
    predictor = MockQuantumDivergencePredictor()
    
    # Load the sample data
    predictor.load_data("example_data.csv")
    
    # Initialize lists to store predictions
    predictions = []
    
    # Make predictions for the last several days
    start_idx = max(20, len(sample_data) - 10)
    end_idx = len(sample_data)
    
    for i in range(start_idx, end_idx):
        # Extract a subset of data leading up to this point
        subset_data = sample_data.iloc[:i].copy()
        
        # Re-initialize predictor with this subset
        test_predictor = MockQuantumDivergencePredictor()
        
        # Save a temporary file with the subset data
        temp_file = "data/aixbt_training_data/temp_subset.csv"
        subset_data.to_csv(temp_file, index=False)
        
        # Load the data into the predictor
        test_predictor.load_data("temp_subset.csv")
        
        # Encode data and train the model
        test_predictor.simulate_quantum_data_encoding()
        X, y = test_predictor.prepare_divergence_prediction_data()
        test_predictor.train_mock_quantum_neural_network(X, y)
        
        # Make prediction
        prediction = test_predictor.predict_divergence()
        predictions.append(prediction)
        
        logger.info(f"Prediction for {subset_data['timestamp'].iloc[-1]}: "
                   f"Divergence: {float(prediction['predicted_divergence']):.6f}, "
                   f"Confidence: {float(prediction['confidence']):.4f}")
    
    # Plot the results
    plot_data_and_predictions(sample_data, predictions)
    
    logger.info("Example complete!")
    logger.info(f"Generated {len(predictions)} predictions")
    
    # Print summary statistics
    actual_values = sample_data['actual_divergence'].iloc[start_idx:end_idx].values
    actual_recent = np.nanmean(actual_values)
    predicted_values = [float(p['predicted_divergence']) for p in predictions]
    predicted_mean = sum(predicted_values) / len(predicted_values) if predicted_values else 0
    
    print("\n" + "=" * 70)
    print("MOCK QUANTUM DIVERGENCE PREDICTOR - EXAMPLE RESULTS")
    print("=" * 70)
    print(f"Data Period: {sample_data['timestamp'].iloc[0]} to {sample_data['timestamp'].iloc[-1]}")
    print(f"Number of Data Points: {len(sample_data)}")
    print(f"Number of Predictions: {len(predictions)}")
    print(f"Average Recent Actual Divergence: {actual_recent:.6f}")
    print(f"Average Predicted Divergence: {predicted_mean:.6f}")
    print("=" * 70)
    print("Note: For visualization, check the generated plot at:")
    print("outputs/quantum_divergence_predictions.png")
    print("=" * 70)

if __name__ == "__main__":
    main() 