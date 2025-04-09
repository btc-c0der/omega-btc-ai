#!/usr/bin/env python3
"""
Core Divergence Predictor
======================

Main module that integrates all quantum components for market divergence prediction.
This is the central hub that coordinates data flow between quantum encoding,
neural networks, optimization, RNG, and entanglement analysis.
"""

import os
import sys
import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Union, Tuple, Callable
from datetime import datetime
import json
import time

# Set up path to import from parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import quantum modules
from quantum_encoding import (
    create_encoder, 
    MarketDataLoader,
    QuantumCircuitSimulator
)

from quantum_encoding.market_analysis import (
    QuantumEntanglementAnalyzer,
    EntanglementMeasure,
    MarketTransitionType
)

from quantum_neural_net import (
    QuantumNeuralNetwork,
    create_quantum_cnn,
    quantum_fidelity,
    entanglement_entropy
)

from quantum_encoding.quantum_rng import (
    QuantumRNG,
    ModelFactory,
    ModelType
)

# Import config (will be implemented)
from .config import DivergencePredictorConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("core-divergence-predictor")

# Constants
LOG_PREFIX = "🔮 CORE DIVERGENCE PREDICTOR"
DEFAULT_CONFIG_PATH = os.path.join(current_dir, "config", "default_config.json")


class CoreDivergencePredictor:
    """
    Core Divergence Predictor integrating all quantum modules.
    
    This class serves as the central integration point for:
    1. Quantum Data Encoding
    2. Quantum Neural Networks
    3. Quantum Optimization
    4. Quantum Random Number Generation
    5. Quantum Entanglement Analysis
    
    It provides a unified interface for market divergence prediction.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the core divergence predictor.
        
        Args:
            config_path: Path to configuration file (optional)
        """
        # Load configuration
        self.config_path = config_path or DEFAULT_CONFIG_PATH
        self.config = self._load_config()
        
        # Initialize components
        self._init_components()
        
        # Set up data storage
        self.market_data = None
        self.encoded_data = None
        self.prediction_results = {}
        self.entanglement_analysis = {}
        self.evaluation_metrics = {}
        
        # Performance tracking
        self.last_run_time = None
        self.initialization_time = datetime.now()
        
        logger.info(f"{LOG_PREFIX} - Initialized with configuration from {self.config_path}")
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file or use default.
        
        Returns:
            Configuration dictionary
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                logger.info(f"{LOG_PREFIX} - Loaded configuration from {self.config_path}")
                return config
            else:
                logger.warning(f"{LOG_PREFIX} - Config file not found: {self.config_path}")
                logger.info(f"{LOG_PREFIX} - Using default configuration")
                return DivergencePredictorConfig.get_default_config()
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error loading config: {e}")
            logger.info(f"{LOG_PREFIX} - Using default configuration")
            return DivergencePredictorConfig.get_default_config()
    
    def _init_components(self) -> None:
        """Initialize all quantum components based on configuration."""
        # 1. Initialize Quantum Data Encoder
        encoder_config = self.config.get("quantum_encoding", {})
        encoder_type = encoder_config.get("encoder_type", "amplitude")
        n_qubits = encoder_config.get("n_qubits", 8)
        
        self.data_encoder = create_encoder(
            encoder_type=encoder_type,
            n_qubits=n_qubits,
            name="market_encoder"
        )
        
        # 2. Initialize Quantum Neural Network
        qnn_config = self.config.get("quantum_neural_net", {})
        input_dim = qnn_config.get("input_dim", 32)
        output_dim = qnn_config.get("output_dim", 1)
        
        self.quantum_nn = create_quantum_cnn(
            input_shape=input_dim,
            output_dim=output_dim,
            n_filters=qnn_config.get("n_filters", 4),
            use_complex=qnn_config.get("use_complex", True)
        )
        
        # Compile the neural network
        self.quantum_nn.compile(
            optimizer="quantum_adam",
            loss="quantum_mse",
            metrics=["quantum_fidelity", "entanglement_entropy"]
        )
        
        # 3. Initialize Quantum RNG
        rng_config = self.config.get("quantum_rng", {})
        self.quantum_rng = QuantumRNG(
            simulator_type=rng_config.get("simulator_type", "statevector"),
            num_qubits=rng_config.get("num_qubits", 6)
        )
        
        # 4. Initialize Stochastic Model Factory
        self.model_factory = ModelFactory()
        
        # 5. Initialize Quantum Entanglement Analyzer
        entanglement_config = self.config.get("entanglement_analysis", {})
        self.entanglement_analyzer = QuantumEntanglementAnalyzer(
            window_size=entanglement_config.get("window_size", 50),
            overlap=entanglement_config.get("overlap", 10),
            entanglement_threshold=entanglement_config.get("entanglement_threshold", 0.4),
            warning_threshold=entanglement_config.get("warning_threshold", 0.7),
            critical_threshold=entanglement_config.get("critical_threshold", 0.85)
        )
        
        # 6. Initialize Quantum Circuit Simulator (for general quantum operations)
        self.circuit_simulator = QuantumCircuitSimulator(
            n_qubits=self.config.get("simulator_qubits", 8)
        )
        
        logger.info(f"{LOG_PREFIX} - Initialized all quantum components")
    
    def load_market_data(self, data_path: Optional[str] = None, 
                      file_name: Optional[str] = None,
                      start_date: Optional[str] = None,
                      end_date: Optional[str] = None) -> bool:
        """
        Load market data for analysis and prediction.
        
        Args:
            data_path: Path to data directory (optional)
            file_name: Name of data file (optional)
            start_date: Start date for filtering (YYYY-MM-DD format)
            end_date: End date for filtering (YYYY-MM-DD format)
            
        Returns:
            Success flag
        """
        try:
            # Use configuration if parameters not provided
            data_path = data_path or self.config.get("data_path", "data/market_data")
            file_name = file_name or self.config.get("data_file", "market_data.csv")
            
            # Initialize data loader
            loader = MarketDataLoader(
                data_dir=data_path,
                default_file=file_name,
                fallback_to_synthetic=True
            )
            
            # Load data
            data = loader.load_data(
                start_date=start_date,
                end_date=end_date
            )
            
            if data.empty:
                logger.error(f"{LOG_PREFIX} - Failed to load market data")
                return False
            
            # Store the data
            self.market_data = data
            logger.info(f"{LOG_PREFIX} - Loaded {len(data)} records from {os.path.join(data_path, file_name)}")
            
            # Process features
            self._extract_features()
            
            return True
            
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error loading market data: {e}")
            return False
    
    def _extract_features(self) -> None:
        """Extract and prepare features from market data."""
        if self.market_data is None or self.market_data.empty:
            logger.warning(f"{LOG_PREFIX} - No market data available for feature extraction")
            return
        
        try:
            # Get feature configuration
            feature_config = self.config.get("features", {})
            price_features = feature_config.get("price_features", ["open", "high", "low", "close"])
            volume_features = feature_config.get("volume_features", ["volume"])
            technical_features = feature_config.get("technical_features", ["rsi", "macd", "bollinger"])
            
            # Identify available features in the data
            available_features = []
            
            for feature_list in [price_features, volume_features, technical_features]:
                for feature in feature_list:
                    if feature in self.market_data.columns:
                        available_features.append(feature)
            
            if not available_features:
                logger.warning(f"{LOG_PREFIX} - No valid features found in market data")
            else:
                logger.info(f"{LOG_PREFIX} - Extracted features: {available_features}")
                
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error extracting features: {e}")
    
    def encode_market_data(self) -> np.ndarray:
        """
        Encode market data using quantum data encoding.
        
        Returns:
            Encoded data as numpy array
        """
        if self.market_data is None or self.market_data.empty:
            logger.error(f"{LOG_PREFIX} - No market data available for encoding")
            return np.array([])
        
        try:
            # Get encoding configuration
            encoding_config = self.config.get("quantum_encoding", {})
            feature_subset = encoding_config.get("feature_subset", [])
            
            # Select features for encoding
            features = self.market_data.select_dtypes(include=['number'])
            
            if feature_subset:
                # Use only specified features if they exist
                valid_features = [f for f in feature_subset if f in features.columns]
                if valid_features:
                    features = features[valid_features]
            
            # Convert to numpy array
            feature_array = features.values
            
            # Encode data using quantum encoder
            start_time = time.time()
            encoded_data = self.data_encoder.encode(feature_array)
            encoding_time = time.time() - start_time
            
            # Store encoded data
            self.encoded_data = encoded_data
            
            logger.info(f"{LOG_PREFIX} - Encoded {feature_array.shape} market data in {encoding_time:.2f}s")
            logger.info(f"{LOG_PREFIX} - Encoded data shape: {encoded_data.shape}")
            
            return encoded_data
            
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error encoding market data: {e}")
            return np.array([])
    
    def analyze_entanglement(self) -> Dict[str, Any]:
        """
        Analyze quantum entanglement in market data.
        
        Returns:
            Dictionary with entanglement analysis results
        """
        if self.market_data is None or self.market_data.empty:
            logger.error(f"{LOG_PREFIX} - No market data available for entanglement analysis")
            return {}
        
        try:
            # Get entanglement configuration
            entanglement_config = self.config.get("entanglement_analysis", {})
            measure = EntanglementMeasure.ENTANGLEMENT_WITNESS  # Default
            
            # Get features for analysis
            features = self.market_data.select_dtypes(include=['number'])
            feature_names = features.columns.tolist()
            
            # Run entanglement analysis
            start_time = time.time()
            results = self.entanglement_analyzer.analyze_entanglement(
                data=features.values,
                feature_names=feature_names,
                measure=measure
            )
            analysis_time = time.time() - start_time
            
            # Store results
            self.entanglement_analysis = results
            
            # Get early warning signals
            warnings = self.entanglement_analyzer.get_early_warning_signals(lookback=10)
            
            # Calculate instability index
            instability = self.entanglement_analyzer.get_instability_index(recent_windows=10)
            
            logger.info(f"{LOG_PREFIX} - Completed entanglement analysis in {analysis_time:.2f}s")
            logger.info(f"{LOG_PREFIX} - Market instability index: {instability:.4f}")
            logger.info(f"{LOG_PREFIX} - Detected {len(warnings)} early warning signals")
            
            return results
            
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error in entanglement analysis: {e}")
            return {}
    
    def train_prediction_model(self, target_column: str = "future_return", 
                            test_size: float = 0.2,
                            epochs: int = 100,
                            batch_size: int = 32) -> Dict[str, Any]:
        """
        Train quantum neural network for divergence prediction.
        
        Args:
            target_column: Column to predict
            test_size: Fraction of data to use for testing
            epochs: Number of training epochs
            batch_size: Training batch size
            
        Returns:
            Dictionary with training results
        """
        if self.encoded_data is None or len(self.encoded_data) == 0:
            logger.error(f"{LOG_PREFIX} - No encoded data available for training")
            return {}
        
        if self.market_data is None or self.market_data.empty:
            logger.error(f"{LOG_PREFIX} - No market data available for training")
            return {}
        
        try:
            # Check if target column exists
            if target_column not in self.market_data.columns:
                logger.error(f"{LOG_PREFIX} - Target column '{target_column}' not found in market data")
                return {}
            
            # Get the target values
            y = self.market_data[target_column].values
            
            # Ensure encoded data and target have the same length
            if len(self.encoded_data) != len(y):
                logger.error(f"{LOG_PREFIX} - Length mismatch between encoded data ({len(self.encoded_data)}) and target ({len(y)})")
                return {}
            
            # Split data into training and test sets
            split_idx = int(len(self.encoded_data) * (1 - test_size))
            
            X_train = self.encoded_data[:split_idx]
            X_test = self.encoded_data[split_idx:]
            y_train = y[:split_idx]
            y_test = y[split_idx:]
            
            # Reshape data if needed
            if len(X_train.shape) == 1:
                X_train = X_train.reshape(-1, 1)
                X_test = X_test.reshape(-1, 1)
            
            # Train the quantum neural network
            start_time = time.time()
            history = self.quantum_nn.fit(
                X_train, y_train,
                epochs=epochs,
                batch_size=batch_size,
                validation_data=(X_test, y_test),
                verbose=1
            )
            training_time = time.time() - start_time
            
            # Evaluate on test set
            eval_results = self.quantum_nn.evaluate(X_test, y_test)
            
            # Store evaluation metrics
            self.evaluation_metrics = eval_results
            
            logger.info(f"{LOG_PREFIX} - Completed model training in {training_time:.2f}s")
            logger.info(f"{LOG_PREFIX} - Test loss: {eval_results.get('loss', 'N/A')}")
            logger.info(f"{LOG_PREFIX} - Test metrics: {', '.join([f'{k}: {v:.4f}' for k, v in eval_results.items() if k != 'loss'])}")
            
            return {
                "history": history,
                "evaluation": eval_results,
                "training_time": training_time
            }
            
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error training prediction model: {e}")
            return {}
    
    def predict_divergence(self, input_data: Optional[Union[pd.DataFrame, np.ndarray]] = None,
                         prediction_horizon: int = 1) -> Dict[str, Any]:
        """
        Predict market divergence using the trained model.
        
        Args:
            input_data: Input data for prediction (uses latest available data if None)
            prediction_horizon: Number of steps ahead to predict
            
        Returns:
            Dictionary with prediction results
        """
        try:
            # Use provided data or latest available
            if input_data is None:
                if self.encoded_data is None or len(self.encoded_data) == 0:
                    logger.error(f"{LOG_PREFIX} - No encoded data available for prediction")
                    return {}
                
                # Use the last data point
                prediction_input = self.encoded_data[-1].reshape(1, -1)
            else:
                # Encode provided data
                if isinstance(input_data, pd.DataFrame):
                    # Keep only numeric columns
                    input_data = input_data.select_dtypes(include=['number'])
                    
                    # Convert to numpy array
                    input_array = input_data.values
                else:
                    input_array = input_data
                
                # Encode the data
                prediction_input = self.data_encoder.encode(input_array)
                
                # Reshape if needed
                if len(prediction_input.shape) == 1:
                    prediction_input = prediction_input.reshape(1, -1)
            
            # Get the instability index from entanglement analysis
            instability_index = 0.0
            if self.entanglement_analysis:
                # Use the stored instability index if available
                try:
                    instability_index = self.entanglement_analyzer.get_instability_index()
                except:
                    pass
            
            # Make prediction
            start_time = time.time()
            raw_prediction = self.quantum_nn.predict(prediction_input)
            prediction_time = time.time() - start_time
            
            # Generate prediction confidence using quantum RNG
            confidence_seed = int(np.sum(raw_prediction) * 1000)
            self.quantum_rng.seed(confidence_seed)
            confidence_factor = min(0.95, 0.5 + instability_index)
            confidence = self.quantum_rng.generate_random_float() * confidence_factor + (1 - confidence_factor)
            
            # Prepare prediction results
            predicted_value = float(raw_prediction[0][0]) if raw_prediction.ndim > 1 else float(raw_prediction[0])
            prediction_result = {
                "predicted_value": predicted_value,
                "confidence": float(confidence),
                "instability_index": float(instability_index),
                "prediction_time": prediction_time,
                "timestamp": datetime.now().isoformat(),
                "prediction_horizon": prediction_horizon
            }
            
            # Store the prediction result
            self.prediction_results = prediction_result
            
            logger.info(f"{LOG_PREFIX} - Completed divergence prediction in {prediction_time:.4f}s")
            logger.info(f"{LOG_PREFIX} - Predicted value: {predicted_value:.4f}, Confidence: {confidence:.4f}")
            
            return prediction_result
            
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error predicting divergence: {e}")
            return {}
    
    def run_full_prediction_pipeline(self, data_path: Optional[str] = None,
                                  file_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Run the complete prediction pipeline from data loading to prediction.
        
        Args:
            data_path: Path to data directory (optional)
            file_name: Name of data file (optional)
            
        Returns:
            Dictionary with complete results
        """
        try:
            start_time = time.time()
            
            # 1. Load market data
            load_success = self.load_market_data(data_path, file_name)
            if not load_success:
                logger.error(f"{LOG_PREFIX} - Failed to load market data, aborting pipeline")
                return {"success": False, "error": "Failed to load market data"}
            
            # 2. Encode market data
            encoded_data = self.encode_market_data()
            if len(encoded_data) == 0:
                logger.error(f"{LOG_PREFIX} - Failed to encode market data, aborting pipeline")
                return {"success": False, "error": "Failed to encode market data"}
            
            # 3. Analyze entanglement
            entanglement_results = self.analyze_entanglement()
            
            # 4. Train prediction model (if required by config)
            if self.config.get("train_on_pipeline_run", True):
                training_results = self.train_prediction_model(
                    target_column=self.config.get("target_column", "future_return"),
                    epochs=self.config.get("training_epochs", 100),
                    batch_size=self.config.get("batch_size", 32)
                )
            
            # 5. Make prediction
            prediction_result = self.predict_divergence()
            
            # Calculate total runtime
            total_time = time.time() - start_time
            self.last_run_time = datetime.now()
            
            # Prepare pipeline results
            pipeline_results = {
                "success": True,
                "prediction": prediction_result,
                "entanglement_analysis": {
                    "instability_index": self.entanglement_analyzer.get_instability_index(),
                    "warnings": len(self.entanglement_analyzer.get_early_warning_signals())
                },
                "metrics": self.evaluation_metrics,
                "runtime": total_time,
                "timestamp": self.last_run_time.isoformat()
            }
            
            logger.info(f"{LOG_PREFIX} - Completed full prediction pipeline in {total_time:.2f}s")
            
            return pipeline_results
            
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error in prediction pipeline: {e}")
            return {"success": False, "error": str(e)}
    
    def get_api_data(self) -> Dict[str, Any]:
        """
        Get formatted data for API responses.
        
        Returns:
            Dictionary with formatted prediction data for API
        """
        # Prepare API response data
        api_data = {
            "prediction": self.prediction_results,
            "entanglement": {
                "instability_index": self.entanglement_analyzer.get_instability_index() 
                  if hasattr(self, 'entanglement_analyzer') else 0.0,
                "early_warnings": len(self.entanglement_analyzer.get_early_warning_signals())
                  if hasattr(self, 'entanglement_analyzer') else 0
            },
            "model_metrics": self.evaluation_metrics,
            "status": {
                "last_run": self.last_run_time.isoformat() if self.last_run_time else None,
                "initialization_time": self.initialization_time.isoformat()
            }
        }
        
        return api_data 