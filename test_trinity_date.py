#!/usr/bin/env python3
"""
Test script to verify date column handling in GAMONTrinityMatrix
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys

# Import GAMON Trinity Matrix
from gamon_trinity_matrix import GAMONTrinityMatrix

def create_test_data():
    """Create test data with different date column formats"""
    # Create dates
    base_date = datetime(2023, 1, 1)
    dates = [base_date + timedelta(days=i) for i in range(100)]
    timestamps = [d.timestamp() for d in dates]
    date_strings = [d.isoformat() for d in dates]
    
    # Create HMM data with both 'timestamp' and 'date' columns
    hmm_data = {
        'timestamp': timestamps,
        'date': date_strings,  # Add a date column to ensure matching
        'state': np.random.randint(0, 6, 100),
        'state_smooth': np.random.randint(0, 6, 100),
        'close': np.random.uniform(30000, 60000, 100),
        'open': np.random.uniform(30000, 60000, 100),
        'high': np.random.uniform(30000, 60000, 100),
        'low': np.random.uniform(30000, 60000, 100),
        'volume': np.random.uniform(1000, 10000, 100)
    }
    
    # Create eigenwave data with both 'datetime' and 'date' columns
    eigenwave_data = {
        'datetime': date_strings,
        'date': date_strings,  # Add a date column to ensure matching
        'eigenwave_0_projection': np.random.uniform(-1, 1, 100),
        'eigenwave_1_projection': np.random.uniform(-1, 1, 100),
        'eigenwave_2_projection': np.random.uniform(-1, 1, 100),
        'eigenwave_3_projection': np.random.uniform(-1, 1, 100),
        'eigenwave_4_projection': np.random.uniform(-1, 1, 100)
    }
    
    # Convert to DataFrames
    hmm_df = pd.DataFrame(hmm_data)
    eigenwave_df = pd.DataFrame(eigenwave_data)
    
    return hmm_df, eigenwave_df

def test_date_handling():
    """Test date handling in GAMONTrinityMatrix"""
    print("Creating test data...")
    hmm_df, eigenwave_df = create_test_data()
    
    # Save test data to results directory
    os.makedirs("results", exist_ok=True)
    hmm_df.to_csv("results/btc_states.csv", index=False)
    eigenwave_df.to_csv("results/btc_eigenwaves.csv", index=False)
    
    print("\nHMM Data Columns:")
    print(hmm_df.columns.tolist())
    print("\nEigenwave Data Columns:")
    print(eigenwave_df.columns.tolist())
    
    # Initialize GAMONTrinityMatrix
    print("\nInitializing GAMONTrinityMatrix...")
    trinity = GAMONTrinityMatrix()
    
    # Initialize vi_model to None
    trinity.vi_model = None
    trinity.merged_data = None
    
    # Load results
    print("\nLoading results...")
    trinity.hmm_results = hmm_df.copy()
    trinity.eigenwave_results = eigenwave_df.copy()
    
    # Print the first few rows of each DataFrame's date column
    print("\nHMM Data 'date' column (first 5 rows):")
    if 'date' in hmm_df.columns:
        for i, date in enumerate(hmm_df['date'].head()):
            print(f"  {i}: {date} (type: {type(date)})")
    
    print("\nEigenwave Data 'date' column (first 5 rows):")
    if 'date' in eigenwave_df.columns:
        for i, date in enumerate(eigenwave_df['date'].head()):
            print(f"  {i}: {date} (type: {type(date)})")
    
    # Test merge_datasets
    print("\nMerging datasets...")
    merged_df = trinity.merge_datasets()
    
    # Check if merge was successful
    if merged_df is not None:
        print("\nMerge successful!")
        print("Merged DataFrame Shape:", merged_df.shape)
        print("\nMerged Data Columns:")
        print(merged_df.columns.tolist())
        
        if 'date' in merged_df.columns and len(merged_df) > 0:
            print("\nDate Column exists and DataFrame is not empty")
            print("Date Column Type:", type(merged_df['date'].iloc[0]))
            print("First 5 dates:")
            for i, date in enumerate(merged_df['date'].head()):
                print(f"  {i}: {date}")
            
            # Test computing metrics
            print("\nComputing Trinity metrics...")
            metrics = trinity.compute_trinity_metrics()
            
            if metrics is not None:
                print("\nMetrics computed successfully!")
                print("Number of metrics:", len(metrics))
                print("Sample metrics:", list(metrics.keys())[:5] if len(metrics) > 5 else list(metrics.keys()))
            else:
                print("\nError computing metrics!")
        else:
            print("\nEither Date Column is missing or DataFrame is empty")
            if 'date' not in merged_df.columns:
                print("Date Column is missing!")
            if len(merged_df) == 0:
                print("DataFrame is empty!")
                
        # Print detailed info about both input dataframes
        print("\nHMM DataFrame Head:")
        print(hmm_df.head())
        print("\nEigenwave DataFrame Head:")
        print(eigenwave_df.head())
    else:
        print("\nError merging datasets!")

if __name__ == "__main__":
    print("=== Testing GAMONTrinityMatrix Date Handling ===\n")
    test_date_handling()
    print("\n=== Test Complete ===") 