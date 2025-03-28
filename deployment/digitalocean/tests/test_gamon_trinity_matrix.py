import unittest
import tempfile
import shutil
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
from pathlib import Path
import json
from typing import Dict, List, Optional

from ..quantum.gamon_trinity_matrix import GAMONTrinityMatrix
from .test_omega_logger import DivineRankingTestCase

class TestGAMONTrinityMatrix(DivineRankingTestCase):
    """Test suite for GAMON Trinity Matrix Analysis System"""
    
    def setUp(self):
        """Set up test environment with temporary directory."""
        super().setUp()
        self.temp_dir = tempfile.mkdtemp()
        self.trinity = GAMONTrinityMatrix()
        
        # Create test data directories
        os.makedirs(os.path.join(self.temp_dir, "results"), exist_ok=True)
        
        # Create sample test data
        self.create_test_data()
        
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
        super().tearDown()
        
    def create_test_data(self):
        """Create sample test data for HMM and Eigenwave results."""
        # Create sample HMM results
        hmm_data = {
            'date': pd.date_range(start='2024-01-01', periods=100),
            'state': np.random.randint(0, 6, 100),
            'confidence': np.random.uniform(0.6, 0.9, 100),
            'price': np.random.uniform(40000, 50000, 100)
        }
        hmm_df = pd.DataFrame(hmm_data)
        hmm_df.to_csv(os.path.join(self.temp_dir, "results/btc_states.csv"), index=False)
        
        # Create sample Eigenwave results
        eigenwave_data = {
            'date': pd.date_range(start='2024-01-01', periods=100),
            'eigenwave_0_projection': np.random.normal(0, 1, 100),
            'eigenwave_1_projection': np.random.normal(0, 1, 100),
            'eigenwave_2_projection': np.random.normal(0, 1, 100),
            'price': np.random.uniform(40000, 50000, 100)
        }
        eigenwave_df = pd.DataFrame(eigenwave_data)
        eigenwave_df.to_csv(os.path.join(self.temp_dir, "results/btc_eigenwaves.csv"), index=False)
    
    def test_initialization(self):
        """Test GAMONTrinityMatrix initialization."""
        self.assertIsNotNone(self.trinity)
        self.assertIsNone(self.trinity.hmm_results)
        self.assertIsNone(self.trinity.eigenwave_results)
        self.assertIsNone(self.trinity.merged_data)
        self.assertIsNone(self.trinity.trinity_metrics)
    
    def test_load_results(self):
        """Test loading analysis results."""
        # Load results from temp directory
        self.trinity.load_results(
            hmm_file=os.path.join(self.temp_dir, "results/btc_states.csv"),
            eigenwave_file=os.path.join(self.temp_dir, "results/btc_eigenwaves.csv")
        )
        
        # Verify results are loaded
        self.assertIsNotNone(self.trinity.hmm_results)
        self.assertIsNotNone(self.trinity.eigenwave_results)
        
        # Check data structure
        self.assertTrue('date' in self.trinity.hmm_results.columns)
        self.assertTrue('state' in self.trinity.hmm_results.columns)
        self.assertTrue('eigenwave_0_projection' in self.trinity.eigenwave_results.columns)
    
    def test_merge_datasets(self):
        """Test merging of HMM and Eigenwave datasets."""
        # Load and merge results
        self.trinity.load_results(
            hmm_file=os.path.join(self.temp_dir, "results/btc_states.csv"),
            eigenwave_file=os.path.join(self.temp_dir, "results/btc_eigenwaves.csv")
        )
        merged_data = self.trinity.merge_datasets()
        
        # Verify merged data
        self.assertIsNotNone(merged_data)
        self.assertEqual(len(merged_data), 100)  # Should match our test data length
        
        # Check for required columns
        required_columns = ['date', 'state', 'eigenwave_0_projection']
        for col in required_columns:
            self.assertTrue(col in merged_data.columns)
    
    def test_compute_trinity_metrics(self):
        """Test computation of trinity metrics."""
        # Load and process data
        self.trinity.load_results(
            hmm_file=os.path.join(self.temp_dir, "results/btc_states.csv"),
            eigenwave_file=os.path.join(self.temp_dir, "results/btc_eigenwaves.csv")
        )
        self.trinity.merge_datasets()
        metrics = self.trinity.compute_trinity_metrics()
        
        # Verify metrics
        self.assertIsNotNone(metrics)
        
        # Check for key metric types
        for state in range(6):
            for wave in range(5):
                key = f'state_{state}_wave_{wave}_avg'
                if key in metrics:
                    self.assertIsInstance(metrics[key], float)
    
    def test_render_trinity_matrix(self):
        """Test rendering of trinity matrix visualization."""
        # Load and process data
        self.trinity.load_results(
            hmm_file=os.path.join(self.temp_dir, "results/btc_states.csv"),
            eigenwave_file=os.path.join(self.temp_dir, "results/btc_eigenwaves.csv")
        )
        self.trinity.merge_datasets()
        self.trinity.compute_trinity_metrics()
        
        # Create visualization
        output_file = os.path.join(self.temp_dir, "gamon_trinity_matrix.html")
        fig = self.trinity.render_trinity_matrix(output_file=output_file)
        
        # Verify visualization
        self.assertTrue(os.path.exists(output_file))
        self.assertGreater(os.path.getsize(output_file), 0)
        self.assertIsNotNone(fig)
    
    def test_error_handling(self):
        """Test error handling for missing or invalid data."""
        # Test loading non-existent files
        with self.assertRaises(FileNotFoundError):
            self.trinity.load_results(
                hmm_file="nonexistent.csv",
                eigenwave_file="nonexistent.csv"
            )
        
        # Test merging without loading
        merged_data = self.trinity.merge_datasets()
        self.assertIsNone(merged_data)
        
        # Test computing metrics without data
        metrics = self.trinity.compute_trinity_metrics()
        self.assertIsNone(metrics)
    
    def test_data_validation(self):
        """Test data validation and handling of edge cases."""
        # Create invalid test data
        invalid_hmm_data = pd.DataFrame({
            'date': pd.date_range(start='2024-01-01', periods=5),
            'invalid_column': np.random.rand(5)
        })
        invalid_hmm_file = os.path.join(self.temp_dir, "results/invalid_states.csv")
        invalid_hmm_data.to_csv(invalid_hmm_file, index=False)
        
        # Test loading invalid data
        self.trinity.load_results(
            hmm_file=invalid_hmm_file,
            eigenwave_file=os.path.join(self.temp_dir, "results/btc_eigenwaves.csv")
        )
        
        # Verify handling of invalid data
        merged_data = self.trinity.merge_datasets()
        self.assertIsNotNone(merged_data)  # Should handle missing columns gracefully 