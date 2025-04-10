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


import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Union, Tuple, Any
import os
import logging
import importlib.util

# Check if joblib is available
joblib_spec = importlib.util.find_spec("joblib")
if joblib_spec:
    import joblib
else:
    joblib = None

# Import the QuantumFeatureExtractor using absolute import to avoid linter errors
try:
    from omega_bot_farm.ai_model_aixbt.quantum_encoding.quantum_features.quantum_feature_extractor import QuantumFeatureExtractor
except ImportError:
    try:
        # Try relative import as fallback
        from ..quantum_encoding.quantum_features.quantum_feature_extractor import QuantumFeatureExtractor
    except ImportError:
        # Create a stub class if imports fail
        class QuantumFeatureExtractor:
            def __init__(self, n_qubits=4, n_layers=2, backend_name="aer_simulator", shots=1024):
                self.n_qubits = n_qubits
                self.n_layers = n_layers
                self.backend_name = backend_name
                self.shots = shots
                logging.warning("QuantumFeatureExtractor stub used - functionality limited")
            
            def extract_features(self, data):
                return data  # Simply return the data as-is
                
            def get_config(self):
                return {
                    "n_qubits": self.n_qubits,
                    "n_layers": self.n_layers, 
                    "backend_name": self.backend_name,
                    "shots": self.shots
                }

# Check for sklearn
SKLEARN_AVAILABLE = False
RandomForestRegressor = None
train_test_split = None
mean_squared_error = None
r2_score = None

sklearn_spec = importlib.util.find_spec("sklearn")
if sklearn_spec:
    try:
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import mean_squared_error, r2_score
        SKLEARN_AVAILABLE = True
    except ImportError:
        pass

from .market_data_utils import (
    load_market_data, 
    calculate_technical_indicators, 
    normalize_features,
    identify_divergences,
    split_train_test,
    create_sequences,
    detect_regime_change
)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QuantumDivergencePredictor:
    """Quantum-enhanced divergence predictor for cryptocurrency market analysis.
    
    This class combines classical ML approaches with quantum-enhanced features
    to predict price divergences and potential market reversals.
    """
    
    def __init__(self, 
                 n_qubits: int = 4,
                 n_layers: int = 2,
                 quantum_backend: str = "aer_simulator",
                 shots: int = 1024,
                 forecast_horizon: int = 5,
                 confidence_threshold: float = 0.65,
                 model_type: str = "random_forest",
                 model_params: Optional[Dict[str, Any]] = None):
        """
        Initialize the quantum divergence predictor.
        
        Args:
            n_qubits: Number of qubits for quantum feature extraction
            n_layers: Number of entanglement layers in quantum circuit
            quantum_backend: Name of the quantum backend to use
            shots: Number of measurement shots for quantum circuit
            forecast_horizon: Number of steps to forecast into the future
            confidence_threshold: Minimum confidence level for predictions
            model_type: Type of classical ML model to use
            model_params: Parameters for the classical ML model
        """
        self.logger = logging.getLogger(__name__)
        
        # Quantum parameters
        self.n_qubits = n_qubits
        self.n_layers = n_layers
        self.quantum_backend = quantum_backend
        self.shots = shots
        
        # Prediction parameters
        self.forecast_horizon = forecast_horizon
        self.confidence_threshold = confidence_threshold
        
        # Initialize quantum feature extractor
        self.feature_extractor = QuantumFeatureExtractor(
            n_qubits=n_qubits,
            n_layers=n_layers,
            backend_name=quantum_backend,
            shots=shots
        )
        
        # ML model parameters
        self.model_type = model_type
        self.model_params = model_params or {}
        self.model = self._initialize_model()
        
        # Tracking metrics
        self.is_trained = False
        self.training_metrics = {}
        
    def _initialize_model(self):
        """Initialize the classical ML model based on model_type."""
        if not SKLEARN_AVAILABLE:
            self.logger.warning("sklearn not available. Prediction functionality will be limited.")
            return None
            
        if RandomForestRegressor is None:
            self.logger.warning("RandomForestRegressor not available.")
            return None
            
        if self.model_type == "random_forest":
            # Default parameters for RandomForestRegressor
            params = {
                "n_estimators": 100,
                "max_depth": 20,
                "random_state": 42,
                "criterion": "squared_error",
                "bootstrap": True,
                "oob_score": False,
                "warm_start": False
            }
            # Update with user-provided parameters
            params.update(self.model_params)
            return RandomForestRegressor(**params)
        else:
            self.logger.warning(f"Unknown model type: {self.model_type}. Using RandomForestRegressor.")
            return RandomForestRegressor(
                n_estimators=100,
                max_depth=20,
                random_state=42
            )
    
    def train(self, 
              market_data: pd.DataFrame,
              target_column: str,
              feature_columns: Optional[List[str]] = None,
              test_size: float = 0.2,
              random_state: int = 42) -> Dict[str, Any]:
        """
        Train the model on market data.
        
        Args:
            market_data: DataFrame containing market data
            target_column: Column name for the prediction target
            feature_columns: List of columns to use as features
            test_size: Proportion of data to use for testing
            random_state: Random seed for train/test split
            
        Returns:
            Dictionary of training metrics
        """
        if not SKLEARN_AVAILABLE:
            self.logger.error("sklearn is required for training")
            return {"error": "sklearn not available"}
            
        if self.model is None:
            self.logger.error("Model not initialized")
            return {"error": "Model not initialized"}
            
        if train_test_split is None:
            self.logger.error("train_test_split not available")
            return {"error": "train_test_split not available"}
            
        # Extract features if specified, otherwise use all columns except target
        if feature_columns is None:
            feature_columns = [col for col in market_data.columns if col != target_column]
            
        X = market_data[feature_columns].values
        y = market_data[target_column].values
        
        # Extract quantum features
        self.logger.info("Extracting quantum features...")
        X_quantum = self.feature_extractor.extract_features(X)
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X_quantum, y, test_size=test_size, random_state=random_state
        )
        
        # Train model
        self.logger.info("Training model...")
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        train_pred = self.model.predict(X_train)
        test_pred = self.model.predict(X_test)
        
        # Safely compute metrics
        training_metrics = {"n_samples": len(X)}
        
        if mean_squared_error is not None:
            train_mse = mean_squared_error(y_train, train_pred)
            test_mse = mean_squared_error(y_test, test_pred)
            training_metrics["train_mse"] = train_mse
            training_metrics["test_mse"] = test_mse
            
        if r2_score is not None:
            train_r2 = r2_score(y_train, train_pred)
            test_r2 = r2_score(y_test, test_pred)
            training_metrics["train_r2"] = train_r2
            training_metrics["test_r2"] = test_r2
            
        training_metrics.update({
            "n_features": X.shape[1],
            "n_quantum_features": X_quantum.shape[1]
        })
        
        self.training_metrics = training_metrics
        self.is_trained = True
        
        self.logger.info(f"Training complete. Metrics: {training_metrics}")
        
        return self.training_metrics
        
    def predict(self, 
                market_data: pd.DataFrame,
                feature_columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Generate divergence predictions for market data.
        
        Args:
            market_data: DataFrame containing market data
            feature_columns: List of columns to use as features
            
        Returns:
            Dictionary containing predictions and confidence levels
        """
        if not self.is_trained:
            self.logger.warning("Model not trained yet. Results may be unreliable.")
            
        if not SKLEARN_AVAILABLE or self.model is None:
            self.logger.error("sklearn and trained model required for prediction")
            return {"error": "Prediction not available"}
            
        # Extract features
        if feature_columns is None:
            # Assuming all columns are features
            feature_columns = market_data.columns.tolist()
            
        X = market_data[feature_columns].values
        
        # Extract quantum features
        X_quantum = self.feature_extractor.extract_features(X)
        
        # Make predictions
        try:
            predictions = self.model.predict(X_quantum)
            
            # Calculate confidence
            confidence = np.ones_like(predictions)  # Default confidence
            
            # For ensemble models, calculate confidence based on variance of predictions
            if hasattr(self.model, "estimators_"):
                predictions_by_estimator = np.array([
                    estimator.predict(X_quantum) for estimator in self.model.estimators_
                ])
                # Standard deviation across ensemble predictions
                pred_std = np.std(predictions_by_estimator, axis=0)
                # Simple normalization for confidence: higher std → lower confidence
                max_std = np.max(pred_std) if np.max(pred_std) > 0 else 1.0
                confidence = 1.0 - (pred_std / max_std)
            
            return {
                "predictions": predictions,
                "confidence": confidence,
                "high_confidence_mask": confidence >= self.confidence_threshold
            }
        except Exception as e:
            self.logger.error(f"Error during prediction: {e}")
            return {"error": str(e)}
    
    def get_feature_importance(self) -> Dict[str, Any]:
        """Get feature importance from the trained model if available."""
        if not self.is_trained or self.model is None:
            return {"error": "Model not trained"}
            
        if hasattr(self.model, "feature_importances_"):
            return {"importance": self.model.feature_importances_}
        else:
            return {"error": "Model does not support feature importance"}
    
    def forecast_divergence(self,
                           market_data: pd.DataFrame,
                           feature_columns: Optional[List[str]] = None,
                           target_column: Optional[str] = None,
                           horizon: Optional[int] = None) -> Dict[str, Any]:
        """
        Forecast market divergence for a specified horizon.
        
        Args:
            market_data: DataFrame containing market data
            feature_columns: List of columns to use as features
            target_column: Column to predict (if None, predict all)
            horizon: Forecast horizon (defaults to self.forecast_horizon)
            
        Returns:
            Dictionary with forecast values and confidence
        """
        if not self.is_trained:
            self.logger.warning("Model not trained yet. Results may be unreliable.")
            
        if self.model is None:
            self.logger.error("Model not initialized")
            return {"error": "Model not initialized"}
        
        horizon = horizon or self.forecast_horizon
        
        # Copy data to avoid modifying original
        forecast_data = market_data.copy()
        
        if feature_columns is None:
            feature_columns = forecast_data.columns.tolist()
            
        if target_column is not None and target_column not in forecast_data.columns:
            # Add target column if it doesn't exist
            forecast_data[target_column] = np.nan
            
        # Array to store forecasts
        forecasts = np.zeros((len(forecast_data), horizon))
        confidence = np.zeros((len(forecast_data), horizon))
        
        try:
            # Iteratively forecast
            for step in range(horizon):
                # Get current features
                current_features = forecast_data[feature_columns].values
                
                # Extract quantum features
                quantum_features = self.feature_extractor.extract_features(current_features)
                
                # Make prediction
                step_prediction = self.model.predict(quantum_features)
                
                # Calculate confidence for ensemble models
                step_confidence = np.ones_like(step_prediction)
                if hasattr(self.model, "estimators_"):
                    predictions_by_estimator = np.array([
                        estimator.predict(quantum_features) for estimator in self.model.estimators_
                    ])
                    pred_std = np.std(predictions_by_estimator, axis=0)
                    max_std = np.max(pred_std) if np.max(pred_std) > 0 else 1.0
                    step_confidence = 1.0 - (pred_std / max_std)
                
                # Store forecast and confidence
                forecasts[:, step] = step_prediction
                confidence[:, step] = step_confidence
                
                # Update data for next step if target column is provided
                if target_column is not None:
                    # Shift everything one step forward
                    forecast_data[target_column] = step_prediction
                
            return {
                "forecast": forecasts,
                "confidence": confidence,
                "horizon": horizon
            }
        except Exception as e:
            self.logger.error(f"Error during forecasting: {e}")
            return {"error": str(e)}
    
    def save_model(self, filepath: str) -> bool:
        """
        Save the trained model to disk.
        
        Args:
            filepath: Path to save the model
        
        Returns:
            True if successful, False otherwise
        """
        if not self.is_trained:
            self.logger.warning("Saving untrained model")
            
        if joblib is None:
            self.logger.error("joblib is required to save the model")
            return False
            
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Save model, metrics, and configuration
            model_data = {
                "model": self.model,
                "training_metrics": self.training_metrics,
                "config": {
                    "n_qubits": self.n_qubits,
                    "n_layers": self.n_layers,
                    "quantum_backend": self.quantum_backend,
                    "shots": self.shots,
                    "forecast_horizon": self.forecast_horizon,
                    "confidence_threshold": self.confidence_threshold,
                    "model_type": self.model_type,
                    "feature_extractor_config": self.feature_extractor.get_config()
                }
            }
            
            joblib.dump(model_data, filepath)
            self.logger.info(f"Model saved to {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving model: {e}")
            return False
    
    @classmethod
    def load_model(cls, filepath: str) -> Optional['QuantumDivergencePredictor']:
        """
        Load a trained model from disk.
        
        Args:
            filepath: Path to the saved model
            
        Returns:
            Loaded QuantumDivergencePredictor instance or None if error
        """
        if joblib is None:
            logger.error("joblib is required to load the model")
            return None
            
        try:
            model_data = joblib.load(filepath)
            
            # Extract configuration
            config = model_data["config"]
            
            # Create new instance
            predictor = cls(
                n_qubits=config["n_qubits"],
                n_layers=config["n_layers"],
                quantum_backend=config["quantum_backend"],
                shots=config["shots"],
                forecast_horizon=config["forecast_horizon"],
                confidence_threshold=config["confidence_threshold"],
                model_type=config["model_type"]
            )
            
            # Restore model and metrics
            predictor.model = model_data["model"]
            predictor.training_metrics = model_data["training_metrics"]
            predictor.is_trained = True
            
            logger.info(f"Model loaded from {filepath}")
            return predictor
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return None
    
    def analyze_market_conditions(
        self, 
        df: pd.DataFrame,
        lookahead_window: int = 10
    ) -> pd.DataFrame:
        """Analyze market conditions and identify potential divergence opportunities.
        
        Args:
            df: Market data DataFrame
            lookahead_window: Number of periods to look ahead for opportunity analysis
            
        Returns:
            DataFrame with analysis results
        """
        # Calculate technical indicators
        df = calculate_technical_indicators(df)
        
        # Detect market regimes
        df = detect_regime_change(df)
        
        # Identify divergences
        df = identify_divergences(df)
        
        # Prepare sequences for prediction
        latest_data = df.tail(self.forecast_horizon + lookahead_window)
        
        # Create sequences for prediction
        sequences = []
        for i in range(lookahead_window):
            seq_start = i
            seq_end = seq_start + self.forecast_horizon
            if seq_end <= len(latest_data):
                sequence = latest_data.iloc[seq_start:seq_end][self.feature_extractor.feature_columns].values
                sequences.append(sequence)
        
        if not sequences:
            logger.warning("Not enough data to create prediction sequences")
            return df
        
        # Convert to numpy array and reshape
        X_predict = np.array(sequences)
        
        # Make predictions
        predictions, probabilities = self.predict(X_predict)
        
        # Add predictions to the dataframe
        df_result = df.copy()
        df_result['divergence_prediction'] = False
        df_result['divergence_probability'] = 0.0
        
        # Add predictions to the last rows
        for i in range(len(predictions)):
            if self.forecast_horizon + i < len(df_result):
                df_result.iloc[self.forecast_horizon + i, df_result.columns.get_loc('divergence_prediction')] = bool(predictions[i])
                df_result.iloc[self.forecast_horizon + i, df_result.columns.get_loc('divergence_probability')] = probabilities[i]
        
        # Add quantum analysis metrics
        df_result['quantum_confidence'] = 0.0
        
        # Generate quantum confidence scores (simplified)
        for i in range(len(predictions)):
            if self.forecast_horizon + i < len(df_result):
                # Higher quantum confidence when probability is far from 0.5
                quantum_conf = 2 * abs(probabilities[i] - 0.5)
                df_result.iloc[self.forecast_horizon + i, df_result.columns.get_loc('quantum_confidence')] = quantum_conf
        
        return df_result
    
    def get_model_summary(self) -> Dict[str, Any]:
        """Get a summary of the model and its performance.
        
        Returns:
            Dictionary with model summary information
        """
        return {
            "model_type": self.model_type,
            "quantum_config": {
                "n_qubits": self.n_qubits,
                "n_layers": self.n_layers,
                "quantum_backend": self.quantum_backend,
                "shots": self.shots,
                "forecast_horizon": self.forecast_horizon,
                "confidence_threshold": self.confidence_threshold
            },
            "training_metrics": self.training_metrics,
            "trained_at": datetime.now().isoformat(),
            "feature_count": len(self.feature_extractor.feature_columns) if hasattr(self, "feature_extractor") else 0,
        } 