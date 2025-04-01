#!/usr/bin/env python3
"""
OMEGA BTC AI - Initialize GAMON Trinity Models
============================================

This script initializes and saves the models used by the GAMON Trinity Matrix:
1. HMM BTC State Mapper
2. Power Method BTC Eigenwaves
3. Variational Inference BTC Cycle
"""

import os
import logging
import yfinance as yf
import pandas as pd
from hmm_btc_state_mapper import HMMBTCStateMapper
from power_method_btc_eigenwaves import PowerMethodBTCEigenwaves
from variational_inference_btc_cycle import VariationalInferenceBTCCycle

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("GAMON-Trinity-Initializer")

def load_btc_data(start_date="2020-01-01"):
    """Load BTC price data from Yahoo Finance."""
    logger.info(f"Loading BTC data from {start_date}...")
    btc = yf.download("BTC-USD", start=start_date)
    
    # Handle multi-level columns from yfinance
    if isinstance(btc.columns, pd.MultiIndex):
        btc.columns = btc.columns.get_level_values(0)
    
    # Rename columns to lowercase
    btc.columns = [col.lower() for col in btc.columns]
    
    # Reset index to make date a column
    btc = btc.reset_index()
    
    return btc

def initialize_models(df):
    """Initialize and save all models."""
    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)
    
    # Initialize HMM model
    logger.info("Initializing HMM model...")
    hmm_model = HMMBTCStateMapper()
    hmm_model.fit(df)
    hmm_model.save_model("models/hmm_btc_state_mapper.pkl")
    logger.info("✅ HMM model saved")
    
    # Initialize Eigenwave model
    logger.info("Initializing Eigenwave model...")
    eigenwave_model = PowerMethodBTCEigenwaves(n_components=3)
    eigenwave_model.fit(df)
    eigenwave_model.save_model("models/power_method_btc_eigenwaves.pkl")
    logger.info("✅ Eigenwave model saved")
    
    # Initialize Cycle model
    logger.info("Initializing Cycle model...")
    cycle_model = VariationalInferenceBTCCycle()
    cycle_model.fit(df)
    cycle_model.save_model("models/variational_inference_btc_cycle.pkl")
    logger.info("✅ Cycle model saved")

def main():
    """Main function to initialize all models."""
    logger.info("🔱 GAMON Trinity Model Initialization")
    logger.info("====================================")
    
    try:
        # Load BTC data
        df = load_btc_data()
        
        # Initialize and save models
        initialize_models(df)
        
        logger.info("✨ All models initialized successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error initializing models: {e}")
        raise

if __name__ == "__main__":
    main() 