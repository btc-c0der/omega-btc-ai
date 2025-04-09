#!/usr/bin/env python3

import numpy as np
import pandas as pd
import tensorflow as tf
import logging
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path

from ..quantum_encoding.quantum_features import QuantumFeatureExtractor
from .market_data_utils import (
    load_market_data,
    calculate_technical_indicators,
    normalize_features,
    split_train_test
)

logger = logging.getLogger(__name__)

class DivergencePredictor:
    """Core module for predicting market divergences using ML and quantum techniques.
    
    This predictor identifies divergences between price action and technical indicators,
    leveraging both classical ML and quantum feature extraction for enhanced prediction.
    """
    
    def __init__(
        self,
        model_path: Optional[str] = None,
        use_quantum_features: bool = True,
        quantum_depth: int = 3,
        confidence_threshold: float = 0.75
    ):
        """Initialize the divergence predictor.
        
        Args:
            model_path: Optional path to load a pre-trained model
            use_quantum_features: Whether to use quantum feature extraction
            quantum_depth: Depth of quantum circuits for feature extraction
            confidence_threshold: Minimum confidence to report a divergence
        """
        self.model = None
        self.model_path = model_path
        self.use_quantum_features = use_quantum_features
        self.confidence_threshold = confidence_threshold
        self.feature_columns = [
            'close', 'volume', 'rsi', 'macd', 'macd_signal', 
            'bb_upper', 'bb_lower', 'bb_width'
        ]
        
        if use_quantum_features:
            self.quantum_extractor = QuantumFeatureExtractor(
                circuit_depth=quantum_depth,
                n_qubits=8
            )
        
        if model_path and Path(model_path).exists():
            self._load_model(model_path)
        else:
            self._build_model()
            
        logger.info(f"Divergence Predictor initialized with quantum features: {use_quantum_features}")
    
    def _build_model(self):
        """Build the neural network model for divergence prediction."""
        input_dim = len(self.feature_columns) * 2 if self.use_quantum_features else len(self.feature_columns)
        
        inputs = tf.keras.Input(shape=(input_dim,))
        x = tf.keras.layers.Dense(64, activation='relu')(inputs)
        x = tf.keras.layers.Dropout(0.2)(x)
        x = tf.keras.layers.Dense(32, activation='relu')(x)
        x = tf.keras.layers.Dropout(0.1)(x)
        outputs = tf.keras.layers.Dense(3, activation='softmax')(x)  # [No Divergence, Bullish, Bearish]
        
        self.model = tf.keras.Model(inputs=inputs, outputs=outputs)
        self.model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        logger.info("Built new divergence prediction model")
    
    def _load_model(self, model_path: str):
        """Load a pre-trained model from disk.
        
        Args:
            model_path: Path to the saved model
        """
        try:
            self.model = tf.keras.models.load_model(model_path)
            logger.info(f"Loaded model from {model_path}")
        except Exception as e:
            logger.error(f"Failed to load model from {model_path}: {e}")
            self._build_model()
    
    def save_model(self, save_path: str):
        """Save the current model to disk.
        
        Args:
            save_path: Path to save the model
        """
        if self.model is not None:
            try:
                self.model.save(save_path)
                logger.info(f"Model saved to {save_path}")
            except Exception as e:
                logger.error(f"Failed to save model to {save_path}: {e}")
    
    def _extract_quantum_features(self, features: np.ndarray) -> np.ndarray:
        """Extract quantum features from classical data.
        
        Args:
            features: Classical feature array
            
        Returns:
            Enhanced feature array with quantum features
        """
        if not self.use_quantum_features:
            return features
            
        quantum_features = self.quantum_extractor.extract_features(features)
        # Concatenate classical and quantum features
        enhanced_features = np.hstack((features, quantum_features))
        return enhanced_features
    
    def train(
        self, 
        data_path: str,
        filename: str,
        epochs: int = 50,
        batch_size: int = 32,
        validation_split: float = 0.2,
        save_path: Optional[str] = None
    ) -> Dict[str, float]:
        """Train the divergence prediction model on historical data.
        
        Args:
            data_path: Path to the directory containing market data
            filename: Name of the market data file
            epochs: Number of training epochs
            batch_size: Training batch size
            validation_split: Fraction of data to use for validation
            save_path: Optional path to save the trained model
            
        Returns:
            Dictionary containing training metrics
        """
        # Load and prepare data
        df = load_market_data(data_path, filename)
        df = calculate_technical_indicators(df)
        df = normalize_features(df)
        
        # Create target: 0 = no divergence, 1 = bullish divergence, 2 = bearish divergence
        # This is a simplified approach - in production, use more sophisticated divergence detection
        df['target'] = 0
        df.loc[(df['close'].pct_change(5) < 0) & (df['rsi'].pct_change(5) > 0), 'target'] = 1  # Bullish
        df.loc[(df['close'].pct_change(5) > 0) & (df['rsi'].pct_change(5) < 0), 'target'] = 2  # Bearish
        
        # Remove NaN values
        df = df.dropna()
        
        # Prepare features and targets
        features = df[self.feature_columns].values
        targets = tf.keras.utils.to_categorical(df['target'].values, num_classes=3)
        
        # Apply quantum feature extraction if enabled
        if self.use_quantum_features:
            features = self._extract_quantum_features(features)
        
        # Split data
        data_splits = split_train_test(
            features, 
            targets, 
            test_size=0.2, 
            validation_size=validation_split
        )
        
        # Train the model
        history = self.model.fit(
            data_splits['X_train'], 
            data_splits['y_train'],
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(data_splits['X_val'], data_splits['y_val']),
            callbacks=[
                tf.keras.callbacks.EarlyStopping(
                    monitor='val_loss',
                    patience=10,
                    restore_best_weights=True
                )
            ]
        )
        
        # Evaluate the model
        test_results = self.model.evaluate(data_splits['X_test'], data_splits['y_test'])
        metrics = {
            'test_loss': test_results[0],
            'test_accuracy': test_results[1]
        }
        
        logger.info(f"Model training completed with test accuracy: {metrics['test_accuracy']:.4f}")
        
        # Save the model if requested
        if save_path:
            self.save_model(save_path)
            
        return metrics
    
    def predict_divergence(self, market_data: pd.DataFrame) -> Dict[str, Union[str, float]]:
        """Predict divergences from current market data.
        
        Args:
            market_data: DataFrame containing recent market data
            
        Returns:
            Dictionary with prediction results
        """
        if self.model is None:
            logger.error("Model not loaded or trained")
            return {"error": "Model not ready"}
            
        # Prepare data
        df = calculate_technical_indicators(market_data.copy())
        df = normalize_features(df)
        
        # Handle NaN values that might have been introduced
        df = df.fillna(method='ffill').fillna(method='bfill')
        
        # Extract features
        features = df[self.feature_columns].values[-1:] # Get latest data point
        
        # Apply quantum feature extraction if enabled
        if self.use_quantum_features:
            features = self._extract_quantum_features(features)
            
        # Make prediction
        prediction = self.model.predict(features)[0]
        
        # Interpret results
        divergence_type = np.argmax(prediction)
        confidence = prediction[divergence_type]
        
        if confidence < self.confidence_threshold:
            result = "No significant divergence detected"
            div_type = "none"
        elif divergence_type == 0:
            result = "No divergence detected"
            div_type = "none"
        elif divergence_type == 1:
            result = "Bullish divergence detected"
            div_type = "bullish"
        else:
            result = "Bearish divergence detected"
            div_type = "bearish"
            
        return {
            "divergence_type": div_type,
            "confidence": float(confidence),
            "raw_predictions": prediction.tolist(),
            "result": result
        }
    
    def analyze_timeframes(
        self, 
        data_path: str, 
        filename: str,
        timeframes: List[int] = [1, 4, 24]
    ) -> Dict[str, Dict]:
        """Analyze divergences across multiple timeframes.
        
        Args:
            data_path: Path to the directory containing market data
            filename: Name of the market data file
            timeframes: List of timeframes to analyze (in hours)
            
        Returns:
            Dictionary with predictions for each timeframe
        """
        # Load data
        df = load_market_data(data_path, filename)
        
        results = {}
        
        for tf in timeframes:
            # Resample data to the specified timeframe
            tf_df = df.copy()
            if tf > 1:
                # Resample to specified timeframe
                tf_df = df.resample(f'{tf}H').agg({
                    'open': 'first',
                    'high': 'max',
                    'low': 'min',
                    'close': 'last',
                    'volume': 'sum'
                })
            
            # Make prediction for this timeframe
            prediction = self.predict_divergence(tf_df)
            results[f"{tf}h"] = prediction
            
        return results
    
    def backtest(
        self, 
        data_path: str,
        filename: str,
        window_size: int = 30
    ) -> Dict[str, float]:
        """Backtest the divergence predictor on historical data.
        
        Args:
            data_path: Path to the directory containing market data
            filename: Name of the market data file
            window_size: Size of the rolling window for backtesting
            
        Returns:
            Dictionary with backtesting performance metrics
        """
        # Load data
        df = load_market_data(data_path, filename)
        df = calculate_technical_indicators(df)
        
        # Prepare results tracking
        correct_predictions = 0
        total_predictions = 0
        
        # Create a copy to avoid SettingWithCopyWarning
        backtest_df = df.copy()
        backtest_df['predicted'] = None
        backtest_df['actual'] = None
        
        # Define actual divergences (simplified approach)
        backtest_df.loc[(backtest_df['close'].pct_change(5) < 0) & 
                        (backtest_df['rsi'].pct_change(5) > 0), 'actual'] = 'bullish'
        backtest_df.loc[(backtest_df['close'].pct_change(5) > 0) & 
                        (backtest_df['rsi'].pct_change(5) < 0), 'actual'] = 'bearish'
        backtest_df['actual'] = backtest_df['actual'].fillna('none')
        
        # Rolling window backtest
        for i in range(window_size, len(df)):
            window = df.iloc[i-window_size:i]
            prediction = self.predict_divergence(window)
            div_type = prediction['divergence_type']
            
            # Store prediction
            backtest_df.iloc[i, backtest_df.columns.get_loc('predicted')] = div_type
            
            # Compare with actual divergence
            actual = backtest_df.iloc[i]['actual']
            if div_type == actual:
                correct_predictions += 1
            
            total_predictions += 1
        
        # Calculate metrics
        accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
        
        # Calculate precision, recall, and F1 for each class
        metrics = {
            'accuracy': accuracy,
            'bullish_precision': 0,
            'bullish_recall': 0,
            'bearish_precision': 0,
            'bearish_recall': 0,
            'f1_score': 0
        }
        
        # Only use rows where we made predictions
        results_df = backtest_df.dropna(subset=['predicted'])
        
        # Calculate precision and recall for bullish divergences
        bullish_predicted = (results_df['predicted'] == 'bullish').sum()
        bullish_actual = (results_df['actual'] == 'bullish').sum()
        bullish_true_pos = ((results_df['predicted'] == 'bullish') & 
                            (results_df['actual'] == 'bullish')).sum()
        
        metrics['bullish_precision'] = bullish_true_pos / bullish_predicted if bullish_predicted > 0 else 0
        metrics['bullish_recall'] = bullish_true_pos / bullish_actual if bullish_actual > 0 else 0
        
        # Calculate precision and recall for bearish divergences
        bearish_predicted = (results_df['predicted'] == 'bearish').sum()
        bearish_actual = (results_df['actual'] == 'bearish').sum()
        bearish_true_pos = ((results_df['predicted'] == 'bearish') & 
                           (results_df['actual'] == 'bearish')).sum()
        
        metrics['bearish_precision'] = bearish_true_pos / bearish_predicted if bearish_predicted > 0 else 0
        metrics['bearish_recall'] = bearish_true_pos / bearish_actual if bearish_actual > 0 else 0
        
        # Calculate F1 score (harmonic mean of precision and recall)
        bullish_f1 = 0
        if metrics['bullish_precision'] > 0 and metrics['bullish_recall'] > 0:
            bullish_f1 = 2 * (metrics['bullish_precision'] * metrics['bullish_recall']) / \
                         (metrics['bullish_precision'] + metrics['bullish_recall'])
                         
        bearish_f1 = 0
        if metrics['bearish_precision'] > 0 and metrics['bearish_recall'] > 0:
            bearish_f1 = 2 * (metrics['bearish_precision'] * metrics['bearish_recall']) / \
                         (metrics['bearish_precision'] + metrics['bearish_recall'])
        
        # Average F1 score
        metrics['f1_score'] = (bullish_f1 + bearish_f1) / 2
        
        logger.info(f"Backtest completed with accuracy: {metrics['accuracy']:.4f}, F1: {metrics['f1_score']:.4f}")
        
        return metrics


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Example usage
    predictor = DivergencePredictor(use_quantum_features=True)
    
    # You would typically load your own data
    # For testing, can use:
    # metrics = predictor.train(
    #     data_path="path/to/data",
    #     filename="btc_data.csv", 
    #     epochs=50,
    #     save_path="models/divergence_model.h5"
    # ) 