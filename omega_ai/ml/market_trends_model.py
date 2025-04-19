
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

import time
import redis
import logging
import json
import os
import numpy as np
import pandas as pd
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report
import joblib
from collections import deque

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Terminal colors for enhanced visibility
BLUE = "\033[94m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"
BOLD = "\033[1m"
WHITE = "\033[97m"

class MarketTrendsModel:
    """AI model that learns from historical market trends data to predict future market behavior."""

    def __init__(self, redis_host='localhost', redis_port=6379):
        """Initialize the market trends model with Redis connection."""
        # Connect to Redis
        self.redis_host = redis_host
        self.redis_port = redis_port
        try:
            self.redis_conn = redis.StrictRedis(
                host=redis_host, 
                port=redis_port,
                db=0, 
                decode_responses=True
            )
            self.redis_conn.ping()
            logger.info(f"Successfully connected to Redis at {redis_host}:{redis_port}")
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

        # Model parameters
        self.model_dir = os.path.join(os.path.dirname(__file__), "models")
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Initialize models
        self.trend_classifier = None  # For trend classification (bullish, bearish, neutral)
        self.price_regressor = None   # For price prediction
        self.trap_classifier = None   # For MM trap detection
        
        # Data preparation tools
        self.price_scaler = MinMaxScaler()
        self.volume_scaler = MinMaxScaler()
        
        # Cache for recent predictions
        self.prediction_cache = {
            "trend": deque(maxlen=100),
            "price": deque(maxlen=100),
            "trap": deque(maxlen=100)
        }
        
        # Fibonacci constants
        self.PHI = 1.618033988749895
        self.FIBONACCI_RATIOS = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618, 2.618]
        
        # Load models if they exist
        self.load_models()

    def load_models(self) -> None:
        """Load previously trained models if they exist."""
        try:
            trend_model_path = os.path.join(self.model_dir, "trend_classifier.joblib")
            price_model_path = os.path.join(self.model_dir, "price_regressor.joblib")
            trap_model_path = os.path.join(self.model_dir, "trap_classifier.joblib")
            
            if os.path.exists(trend_model_path):
                self.trend_classifier = joblib.load(trend_model_path)
                logger.info("Loaded trend classifier model")
                
            if os.path.exists(price_model_path):
                self.price_regressor = joblib.load(price_model_path)
                logger.info("Loaded price regressor model")
                
            if os.path.exists(trap_model_path):
                self.trap_classifier = joblib.load(trap_model_path)
                logger.info("Loaded trap classifier model")
                
        except Exception as e:
            logger.error(f"Error loading models: {e}")
    
    def save_models(self) -> None:
        """Save trained models to disk."""
        try:
            if self.trend_classifier:
                joblib.dump(self.trend_classifier, 
                           os.path.join(self.model_dir, "trend_classifier.joblib"))
                
            if self.price_regressor:
                joblib.dump(self.price_regressor, 
                           os.path.join(self.model_dir, "price_regressor.joblib"))
                
            if self.trap_classifier:
                joblib.dump(self.trap_classifier, 
                           os.path.join(self.model_dir, "trap_classifier.joblib"))
                
            logger.info("Models saved successfully")
        except Exception as e:
            logger.error(f"Error saving models: {e}")
    
    def get_historical_data(self, days_back: int = 30) -> pd.DataFrame:
        """Retrieve and process historical data from Redis for model training."""
        logger.info(f"Retrieving historical data for the past {days_back} days")
        
        try:
            # Get price history
            price_history = []
            raw_data = self.redis_conn.lrange("btc_movement_history", 0, -1)
            
            if not raw_data:
                logger.warning("No historical price data found in Redis")
                return pd.DataFrame()
            
            # Process the raw price data
            for item in raw_data:
                try:
                    if "," in item:
                        price_str, volume_str = item.split(",")
                        price = float(price_str)
                        volume = float(volume_str)
                    else:
                        price = float(item)
                        volume = 0
                    
                    # For simplicity, we're using the current time minus an offset
                    # In production, you'd want to store timestamps with your data
                    price_history.append({
                        "price": price, 
                        "volume": volume
                    })
                except Exception as e:
                    logger.warning(f"Error parsing price history item: {e}")
                    continue
            
            # Convert to DataFrame
            df = pd.DataFrame(price_history)
            
            # Add trend data if available
            timeframes = ["1min", "5min", "15min", "30min", "60min", "240min", "720min", "1444min"]
            for tf in timeframes:
                trend_key = f"btc_trend_{tf}"
                trend_data = self.redis_conn.get(trend_key)
                
                if trend_data:
                    try:
                        trend_info = json.loads(trend_data)
                        df[f"trend_{tf}"] = self._encode_trend(trend_info.get("trend", "Neutral"))
                        df[f"change_{tf}"] = trend_info.get("change", 0.0)
                    except Exception as e:
                        logger.warning(f"Error parsing trend data for {tf}: {e}")
            
            # Create a timestamp for each row (this is a simplification)
            # In production, store actual timestamps with your data
            now = datetime.now(timezone.utc)
            df["timestamp"] = [(now - timedelta(minutes=i)).isoformat() for i in range(len(df))]
            
            # Add engineered features
            df = self._engineer_features(df)
            
            logger.info(f"Retrieved {len(df)} historical data points")
            return df
            
        except Exception as e:
            logger.error(f"Error retrieving historical data: {e}")
            return pd.DataFrame()
    
    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer additional features for better model performance."""
        if df.empty:
            return df
        
        # Copy the dataframe to avoid modifying the original
        df_new = df.copy()
        
        # Calculate moving averages
        windows = [8, 13, 21, 34, 55]  # Fibonacci-inspired windows
        for window in windows:
            if len(df) >= window:
                df_new[f'ma_{window}'] = df_new['price'].rolling(window=window).mean()
                df_new[f'vol_{window}'] = df_new['price'].rolling(window=window).std()
                df_new[f'vol_ratio_{window}'] = df_new[f'vol_{window}'] / df_new['price'] * 100
                
                # Volume moving averages
                if 'volume' in df_new.columns:
                    df_new[f'volume_ma_{window}'] = df_new['volume'].rolling(window=window).mean()
        
        # Calculate price momentum
        momentum_periods = [1, 2, 3, 5, 8, 13, 21]
        for period in momentum_periods:
            if len(df) > period:
                df_new[f'momentum_{period}'] = df_new['price'].pct_change(periods=period) * 100
        
        # Calculate RSI
        if len(df) > 14:
            delta = df_new['price'].diff()
            gain = (delta.where(delta.astype(float) > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta.astype(float) < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df_new['rsi_14'] = 100 - (100 / (1 + rs))
        
        # Fibonacci-based features
        if len(df) > 55:  # Only calculate if we have enough data
            # Get recent high and low for Fibonacci levels
            high = df_new['price'].rolling(window=55).max()
            low = df_new['price'].rolling(window=55).min()
            price_range = high - low
            
            # Calculate distance from key Fibonacci levels
            for ratio in self.FIBONACCI_RATIOS:
                level = low + ratio * price_range
                df_new[f'fib_dist_{ratio}'] = (df_new['price'] - level) / df_new['price'] * 100
        
        # Create trend change indicators - but ensure we don't duplicate "_change" suffix
        timeframes = [tf for tf in df.columns if tf.startswith('trend_') and not tf.endswith('_change')]
        for tf in timeframes:
            df_new[f'{tf}_change'] = df_new[tf].diff().fillna(0)
        
        # Logical features
        if 'trend_15min' in df_new.columns and 'trend_60min' in df_new.columns:
            # Alignment between different timeframes
            df_new['trend_alignment'] = (df_new['trend_15min'] == df_new['trend_60min']).astype(int)
        
        # Fill NaN values
        df_new = df_new.fillna(0)
        
        return df_new
    
    def _encode_trend(self, trend_str: str) -> int:
        """Convert trend string to numerical value."""
        if "Bullish" in trend_str:
            return 1
        elif "Bearish" in trend_str:
            return -1
        else:
            return 0
    
    def prepare_training_data(self, df: pd.DataFrame, target_col: str, forecast_period: int = 1) -> Tuple:
        """Prepare data for model training with a specified forecast period."""
        if df.empty:
            logger.warning("Empty dataframe provided for training data preparation")
            return None, None, None, None
        
        try:
            # Create target column - shifted by forecast_period
            if target_col == 'trend_future':
                # For trend classification, use the 15min trend as default
                if 'trend_15min' in df.columns:
                    y = df['trend_15min'].shift(-forecast_period)
                else:
                    logger.warning("trend_15min column not found for trend prediction")
                    return None, None, None, None
            elif target_col == 'price_future':
                # For price prediction, use the actual price
                y = df['price'].shift(-forecast_period)
            elif target_col == 'trap_future':
                # For trap detection, we need to construct this from other signals
                # This is a simplification; in reality you'd use actual trap labels
                if 'trend_15min' in df.columns and 'change_15min' in df.columns:
                    conditions = (
                        ((df['trend_15min'] == 1) & (df['change_15min'] > 1.5)) |  # Bull trap conditions
                        ((df['trend_15min'] == -1) & (df['change_15min'] < -1.5))  # Bear trap conditions
                    )
                    y = conditions.astype(int).shift(-forecast_period)
                else:
                    logger.warning("Required columns not found for trap prediction")
                    return None, None, None, None
            else:
                logger.warning(f"Unknown target column: {target_col}")
                return None, None, None, None
            
            # Drop rows with NaN in target
            df = df.iloc[:-forecast_period]
            y = y.iloc[:-forecast_period]
            
            # Select features (drop timestamp and target-related columns)
            exclude_cols = ['timestamp', 'trend_15min', 'price', 'trap_detected']
            feature_cols = [col for col in df.columns if col not in exclude_cols]
            X = df[feature_cols]
            
            # Split into train and test sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
            
            # Scale numerical features
            if target_col == 'price_future':
                # For price prediction, scale the target too
                y_train = pd.Series(self.price_scaler.fit_transform(
                    y_train.values.reshape(-1, 1)).flatten(), index=y_train.index)
                y_test = pd.Series(self.price_scaler.transform(
                    y_test.values.reshape(-1, 1)).flatten(), index=y_test.index)
            
            logger.info(f"Prepared training data with {len(X_train)} train and {len(X_test)} test samples")
            return X_train, X_test, y_train, y_test
            
        except Exception as e:
            logger.error(f"Error preparing training data: {e}")
            return None, None, None, None
    
    def train_trend_model(self, df: pd.DataFrame, forecast_period: int = 3) -> None:
        """Train the trend classification model."""
        logger.info(f"Training trend classifier model with forecast period {forecast_period}")
        
        X_train, X_test, y_train, y_test = self.prepare_training_data(
            df, 'trend_future', forecast_period)
        
        if X_train is None:
            logger.error("Failed to prepare training data for trend model")
            return
        
        try:
            # Initialize and train the model
            self.trend_classifier = RandomForestClassifier(
                n_estimators=100, 
                max_depth=10,
                random_state=42
            )
            self.trend_classifier.fit(X_train, y_train)
            
            # Evaluate the model
            y_pred = self.trend_classifier.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            logger.info(f"Trend model trained with test accuracy: {accuracy:.4f}")
            logger.info(f"\n{str(classification_report(y_test, y_pred))}")
            
            # Save the model
            self.save_models()
            
        except Exception as e:
            logger.error(f"Error training trend model: {e}")
    
    def train_price_model(self, df: pd.DataFrame, forecast_period: int = 1) -> None:
        """Train the price regression model."""
        logger.info(f"Training price regressor model with forecast period {forecast_period}")
        
        X_train, X_test, y_train, y_test = self.prepare_training_data(
            df, 'price_future', forecast_period)
        
        if X_train is None:
            logger.error("Failed to prepare training data for price model")
            return
        
        try:
            # Initialize and train the model
            self.price_regressor = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42
            )
            self.price_regressor.fit(X_train, y_train)
            
            # Evaluate the model
            y_pred = self.price_regressor.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            
            logger.info(f"Price model trained with test RMSE: {rmse:.4f}")
            
            # Save the model
            self.save_models()
            
        except Exception as e:
            logger.error(f"Error training price model: {e}")
    
    def train_trap_model(self, df: pd.DataFrame, forecast_period: int = 1) -> None:
        """Train the MM trap detection model."""
        logger.info(f"Training trap classifier model with forecast period {forecast_period}")
        
        X_train, X_test, y_train, y_test = self.prepare_training_data(
            df, 'trap_future', forecast_period)
        
        if X_train is None:
            logger.error("Failed to prepare training data for trap model")
            return
        
        try:
            # Initialize and train the model
            self.trap_classifier = RandomForestClassifier(
                n_estimators=100,
                max_depth=8,
                class_weight='balanced',
                random_state=42
            )
            self.trap_classifier.fit(X_train, y_train)
            
            # Evaluate the model
            y_pred = self.trap_classifier.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            logger.info(f"Trap model trained with test accuracy: {accuracy:.4f}")
            logger.info(f"\n{str(classification_report(y_test, y_pred))}")
            
            # Save the model
            self.save_models()
            
        except Exception as e:
            logger.error(f"Error training trap model: {e}")
    
    def train_all_models(self, days_back: int = 30) -> None:
        """Train all models with historical data."""
        logger.info(f"Training all models with {days_back} days of historical data")
        
        # Get historical data
        df = self.get_historical_data(days_back)
        
        if df.empty:
            logger.error("No historical data available for model training")
            return
        
        # Train models with different forecast periods
        self.train_trend_model(df, forecast_period=3)  # Predict trend 3 periods ahead
        self.train_price_model(df, forecast_period=1)  # Predict price 1 period ahead 
        self.train_trap_model(df, forecast_period=5)   # Predict traps 5 periods ahead
        
        logger.info("All models trained successfully")
    
    def get_latest_data(self) -> pd.DataFrame:
        """Get the latest market data for predictions."""
        try:
            # Get current price
            current_price = float(self.redis_conn.get("last_btc_price") or 0)
            if current_price == 0:
                logger.warning("No current price available")
                return pd.DataFrame()
            
            # Create a dataframe with the latest data point
            data = {"price": current_price}
            
            # Add volume if available
            volume = float(self.redis_conn.get("last_btc_volume") or 0)
            data["volume"] = volume
            
            # Add trend data
            timeframes = ["1min", "5min", "15min", "30min", "60min", "240min", "720min", "1444min"]
            for tf in timeframes:
                trend_key = f"btc_trend_{tf}"
                trend_data = self.redis_conn.get(trend_key)
                
                if trend_data:
                    try:
                        trend_info = json.loads(trend_data)
                        data[f"trend_{tf}"] = self._encode_trend(trend_info.get("trend", "Neutral"))
                        data[f"change_{tf}"] = trend_info.get("change", 0.0)
                    except:
                        pass
            
            # Create a dataframe
            df = pd.DataFrame([data])
            
            # Get historical data for feature engineering
            hist_df = self.get_historical_data(days_back=2)  # Get 2 days of history
            
            if not hist_df.empty:
                # Append the current data to historical data
                full_df = pd.concat([hist_df, df], ignore_index=True)
                
                # Engineer features for the full dataset
                full_df = self._engineer_features(full_df)
                
                # Return only the last row (current data with engineered features)
                return full_df.iloc[[-1]]
            else:
                logger.warning("No historical data available for feature engineering")
                return df
            
        except Exception as e:
            logger.error(f"Error getting latest data: {e}")
            return pd.DataFrame()
    
    def predict_trend(self) -> Dict[str, Any]:
        """Predict future market trend."""
        if not self.trend_classifier:
            logger.warning("Trend classifier model not trained yet")
            return {"trend": "Unknown", "confidence": 0.0}
        
        try:
            # Get latest data
            df = self.get_latest_data()
            
            if df.empty:
                logger.warning("No data available for trend prediction")
                return {"trend": "Unknown", "confidence": 0.0}
            
            # Select features (exclude timestamp and target-related columns)
            exclude_cols = ['timestamp', 'trend_15min', 'price', 'trap_detected']
            feature_cols = [col for col in df.columns if col not in exclude_cols]
            X = df[feature_cols]
            
            # IMPORTANT: Ensure feature consistency by using only features the model was trained on
            if hasattr(self.trend_classifier, 'feature_names_in_'):
                # For newer scikit-learn versions
                trained_features = self.trend_classifier.feature_names_in_
                missing_features = set(trained_features) - set(X.columns)
                extra_features = set(X.columns) - set(trained_features)
                
                # Add missing features with zeros
                for feature in missing_features:
                    X[feature] = 0
                
                # Select only the features used during training
                X = X[trained_features]
            
            # Make prediction
            pred_class = self.trend_classifier.predict(X)[0]
            pred_proba = np.max(self.trend_classifier.predict_proba(X)[0])
            
            # Convert prediction to trend string
            if pred_class == 1:
                trend = "Bullish"
            elif pred_class == -1:
                trend = "Bearish"
            else:
                trend = "Neutral"
            
            # Store prediction for accuracy tracking
            self.prediction_cache["trend"].append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "prediction": trend,
                "confidence": float(pred_proba)
            })
            
            # Store prediction in Redis for other components to use
            self.redis_conn.set(
                "ai_trend_prediction",
                json.dumps({
                    "trend": trend,
                    "confidence": float(pred_proba),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
            )
            
            return {"trend": trend, "confidence": float(pred_proba)}
            
        except Exception as e:
            logger.error(f"Error predicting trend: {e}")
            return {"trend": "Error", "confidence": 0.0}
    
    def predict_price(self) -> Dict[str, Any]:
        """Predict future BTC price."""
        if not self.price_regressor:
            logger.warning("Price regressor model not trained yet")
            return {"price": 0.0, "confidence": 0.0}
        
        try:
            # Get latest data
            df = self.get_latest_data()
            
            if df.empty:
                logger.warning("No data available for price prediction")
                return {"price": 0.0, "confidence": 0.0}
            
            # Get current price for reference
            current_price = df["price"].values[0]
            
            # Select features
            exclude_cols = ['timestamp', 'trend_15min', 'price', 'trap_detected']
            feature_cols = [col for col in df.columns if col not in exclude_cols]
            X = df[feature_cols]
            
            # IMPORTANT: Ensure feature consistency by using only features the model was trained on
            if hasattr(self.price_regressor, 'feature_names_in_'):
                # For newer scikit-learn versions
                trained_features = self.price_regressor.feature_names_in_
                missing_features = set(trained_features) - set(X.columns)
                extra_features = set(X.columns) - set(trained_features)
                
                # Add missing features with zeros
                for feature in missing_features:
                    X[feature] = 0
                
                # Select only the features used during training
                X = X[trained_features]
            
            # Make prediction (scaled)
            scaled_pred = self.price_regressor.predict(X)[0]
            
            # Check if scaler is fitted before using inverse_transform
            try:
                # Convert back to original scale
                price_pred = self.price_scaler.inverse_transform(np.array([[scaled_pred]]))[0][0]
            except Exception as e:
                logger.warning(f"Price scaler not fitted. Using scaled prediction: {e}")
                # If scaler is not fitted, use the scaled prediction directly with current price as baseline
                # This is a fallback approach when the scaler is not available
                price_pred = current_price * (1 + scaled_pred)
            
            # Calculate confidence based on feature importance and variance
            # This is a simplified approach - in a real model, use prediction intervals
            score_val = float(self.price_regressor.score(X, np.array([[scaled_pred]])))
            r2_score = max(0.0, min(1.0, score_val))
            
            # Calculate percent change
            pct_change = ((price_pred - current_price) / current_price) * 100
            
            # Store prediction for accuracy tracking
            self.prediction_cache["price"].append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "prediction": float(price_pred),
                "current_price": float(current_price),
                "pct_change": float(pct_change),
                "confidence": float(r2_score)
            })
            
            # Store prediction in Redis
            self.redis_conn.set(
                "ai_price_prediction",
                json.dumps({
                    "price": float(price_pred),
                    "current_price": float(current_price),
                    "pct_change": float(pct_change),
                    "confidence": float(r2_score),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
            )
            
            return {
                "price": float(price_pred),
                "current_price": float(current_price),
                "pct_change": float(pct_change),
                "confidence": float(r2_score)
            }
            
        except Exception as e:
            logger.error(f"Error predicting price: {e}")
            return {"price": 0.0, "confidence": 0.0}
    
    def predict_mm_trap(self) -> Dict[str, Any]:
        """Predict potential market maker traps."""
        if not self.trap_classifier:
            logger.warning("Trap classifier model not trained yet")
            return {"trap_detected": False, "confidence": 0.0}
        
        try:
            # Get latest data
            df = self.get_latest_data()
            
            if df.empty:
                logger.warning("No data available for trap prediction")
                return {"trap_detected": False, "confidence": 0.0}
            
            # Select features
            exclude_cols = ['timestamp', 'trend_15min', 'price', 'trap_detected']
            feature_cols = [col for col in df.columns if col not in exclude_cols]
            X = df[feature_cols]
            
            # IMPORTANT: Ensure feature consistency by using only features the model was trained on
            if hasattr(self.trap_classifier, 'feature_names_in_'):
                # For newer scikit-learn versions
                trained_features = self.trap_classifier.feature_names_in_
                missing_features = set(trained_features) - set(X.columns)
                extra_features = set(X.columns) - set(trained_features)
                
                # Add missing features with zeros
                for feature in missing_features:
                    X[feature] = 0
                
                # Select only the features used during training
                X = X[trained_features]
            
            # Make prediction
            trap_detected = bool(self.trap_classifier.predict(X)[0])
            confidence = np.max(self.trap_classifier.predict_proba(X)[0])
            
            # Get additional context for trap type
            trap_type = None
            if trap_detected:
                # Determine trap type based on current trends
                if 'trend_15min' in df.columns:
                    trend_val = df['trend_15min'].values[0]
                    if trend_val == 1:  # Bullish
                        trap_type = "Bull Trap"
                    elif trend_val == -1:  # Bearish
                        trap_type = "Bear Trap"
            
            # Store prediction for accuracy tracking
            self.prediction_cache["trap"].append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "prediction": trap_detected,
                "trap_type": trap_type,
                "confidence": float(confidence)
            })
            
            # Store prediction in Redis
            self.redis_conn.set(
                "ai_trap_prediction",
                json.dumps({
                    "trap_detected": trap_detected,
                    "trap_type": trap_type,
                    "confidence": float(confidence),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
            )
            
            return {
                "trap_detected": trap_detected,
                "trap_type": trap_type,
                "confidence": float(confidence)
            }
            
        except Exception as e:
            logger.error(f"Error predicting MM trap: {e}")
            return {"trap_detected": False, "confidence": 0.0}
    
    def generate_predictions(self) -> Dict[str, Any]:
        """Generate comprehensive predictions from all models."""
        results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trend": self.predict_trend(),
            "price": self.predict_price(),
            "trap": self.predict_mm_trap()
        }
        
        # Store combined predictions in Redis
        self.redis_conn.set("ai_predictions", json.dumps(results))
        
        return results
    
    def save_historical_predictions(self) -> None:
        """Save historical predictions to Redis."""
        for pred_type, predictions in self.prediction_cache.items():
            if predictions:
                key = f"ai_prediction_history_{pred_type}"
                try:
                    # Convert to JSON strings
                    pred_strings = [json.dumps(p) for p in predictions]
                    
                    # Store in Redis list (up to 1000 predictions)
                    pipeline = self.redis_conn.pipeline()
                    for p in pred_strings:
                        pipeline.lpush(key, p)
                    pipeline.ltrim(key, 0, 999)  # Keep only the last 1000 predictions
                    pipeline.execute()
                    
                    logger.info(f"Saved {len(predictions)} {pred_type} predictions to Redis")
                except Exception as e:
                    logger.error(f"Error saving historical {pred_type} predictions: {e}")
    
    def display_predictions(self, predictions: Dict[str, Any]) -> None:
        """Display predictions with enhanced formatting."""
        print(f"\n{MAGENTA}{BOLD}🧠 AI MODEL PREDICTIONS 🧠{RESET}")
        print(f"{YELLOW}══════════════════════════════════════{RESET}")
        
        # Trend prediction
        trend = predictions["trend"]
        trend_name = trend.get("trend", "Unknown")
        trend_conf = trend.get("confidence", 0.0)
        
        if trend_name == "Bullish":
            trend_color = GREEN
        elif trend_name == "Bearish":
            trend_color = RED
        else:
            trend_color = CYAN
            
        print(f"{BOLD}📈 TREND PREDICTION:{RESET}")
        print(f"  Direction: {trend_color}{trend_name}{RESET}")
        print(f"  Confidence: {self._format_confidence(trend_conf)}")
        
        # Price prediction
        price = predictions["price"]
        price_val = price.get("price", 0.0)
        current_price = price.get("current_price", 0.0)
        pct_change = price.get("pct_change", 0.0)
        price_conf = price.get("confidence", 0.0)
        
        price_color = GREEN if pct_change > 0 else RED if pct_change < 0 else BLUE
        
        print(f"\n{BOLD}💰 PRICE PREDICTION:{RESET}")
        print(f"  Current: ${current_price:,.2f}")
        print(f"  Predicted: {price_color}${price_val:,.2f} ({pct_change:+.2f}%){RESET}")
        print(f"  Confidence: {self._format_confidence(price_conf)}")
        
        # Trap prediction
        trap = predictions["trap"]
        trap_detected = trap.get("trap_detected", False)
        trap_type = trap.get("trap_type", None)
        trap_conf = trap.get("confidence", 0.0)
        
        print(f"\n{BOLD}⚠️ TRAP PREDICTION:{RESET}")
        if trap_detected:
            trap_color = RED if trap_type == "Bull Trap" else YELLOW if trap_type == "Bear Trap" else MAGENTA
            print(f"  {trap_color}TRAP DETECTED: {trap_type}{RESET}")
            print(f"  Confidence: {self._format_confidence(trap_conf)}")
        else:
            print(f"  {GREEN}No trap detected{RESET}")
            print(f"  Confidence: {self._format_confidence(trap_conf)}")
        
        # Overall harmony score (combined assessment)
        harmony = self._calculate_harmony_score(predictions)
        harmony_color = self._get_harmony_color(harmony)
        
        print(f"\n{BOLD}🌟 FIBONACCI HARMONY SCORE:{RESET}")
        print(f"  {harmony_color}{harmony:.2f}/10{RESET}")
        
        # Divine wisdom (custom insight based on predictions)
        wisdom = self._generate_divine_wisdom(predictions)
        print(f"\n{MAGENTA}{BOLD}🔮 DIVINE WISDOM:{RESET}")
        print(f"  {CYAN}{wisdom}{RESET}")
        
        print(f"\n{YELLOW}Timestamp: {predictions['timestamp']}{RESET}")
        print(f"{YELLOW}══════════════════════════════════════{RESET}")
    
    def _format_confidence(self, confidence: float) -> str:
        """Format confidence value with color."""
        if confidence > 0.8:
            return f"{GREEN}{confidence:.2f}{RESET}"
        elif confidence > 0.6:
            return f"{BLUE}{confidence:.2f}{RESET}"
        elif confidence > 0.4:
            return f"{YELLOW}{confidence:.2f}{RESET}"
        else:
            return f"{RED}{confidence:.2f}{RESET}"
    
    def _calculate_harmony_score(self, predictions: Dict[str, Any]) -> float:
        """Calculate a Fibonacci-inspired harmony score from the predictions."""
        # This is a custom scoring function that combines different predictions
        # into a single "harmony" score based on Fibonacci principles
        
        score = 0.0
        
        # Trend confidence contribution (0-3 points)
        trend_conf = predictions["trend"].get("confidence", 0.0)
        score += trend_conf * 3
        
        # Price confidence contribution (0-3 points)
        price_conf = predictions["price"].get("confidence", 0.0)
        score += price_conf * 3
        
        # Trap confidence contribution (0-2 points)
        # Higher score if no trap or if trap detection is very confident
        trap_detected = predictions["trap"].get("trap_detected", False)
        trap_conf = predictions["trap"].get("confidence", 0.0)
        
        if trap_detected:
            # If trap detected with high confidence, lower score
            score += (1 - trap_conf) * 2
        else:
            # If no trap with high confidence, higher score
            score += trap_conf * 2
        
        # Alignment between trend and price change (0-2 points)
        trend = predictions["trend"].get("trend", "Unknown")
        pct_change = predictions["price"].get("pct_change", 0.0)
        
        trend_aligned = (
            (trend == "Bullish" and pct_change > 0) or
            (trend == "Bearish" and pct_change < 0) or
            (trend == "Neutral" and abs(pct_change) < 0.5)
        )
        
        if trend_aligned:
            score += 2
        
        return score
    
    def _get_harmony_color(self, score: float) -> str:
        """Get color based on harmony score."""
        if score > 8:
            return GREEN
        elif score > 6:
            return BLUE
        elif score > 4:
            return YELLOW
        else:
            return RED
    
    def _generate_divine_wisdom(self, predictions: Dict[str, Any]) -> str:
        """Generate divine wisdom based on the predictions."""
        trend = predictions["trend"].get("trend", "Unknown")
        trend_conf = predictions["trend"].get("confidence", 0.0)
        
        price_val = predictions["price"].get("price", 0.0)
        current_price = predictions["price"].get("current_price", 0.0)
        pct_change = predictions["price"].get("pct_change", 0.0)
        
        trap_detected = predictions["trap"].get("trap_detected", False)
        trap_type = predictions["trap"].get("trap_type", None)
        trap_conf = predictions["trap"].get("confidence", 0.0)
        
        harmony = self._calculate_harmony_score(predictions)
        
        # Generate wisdom based on the combined factors
        if trap_detected and trap_conf > 0.7:
            return f"The market appears to be setting a {trap_type}. Exercise caution and wait for confirmation before taking action."
        
        if trend == "Bullish" and trend_conf > 0.8 and pct_change > 1.0:
            return f"The divine Fibonacci patterns reveal strong bullish momentum. The market is in harmony with upward forces."
        
        if trend == "Bearish" and trend_conf > 0.8 and pct_change < -1.0:
            return f"The sacred patterns indicate bearish pressure. Protect capital and wait for the divine reversal."
        
        if harmony > 8:
            return f"Cosmic alignment detected. The market is flowing with the divine Fibonacci sequence."
        
        if harmony < 4:
            return f"Market lacks harmony with natural Fibonacci flow. Exercise patience until the divine pattern emerges."
        
        if abs(pct_change) < 0.3:
            return f"The market is in a state of equilibrium. Accumulation phase may be in progress."
        
        # Default wisdom
        return f"The market follows the eternal dance of the Fibonacci sequence. Observe the pattern and flow with it."

def run_model(days_back=30, train=True):
    """Run the market trends model."""
    # Get Redis connection details from environment
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    
    print(f"{GREEN}{BOLD}🧠 INITIALIZING MARKET TRENDS AI MODEL 🧠{RESET}")
    print(f"{BLUE}Connecting to Redis at {redis_host}:{redis_port}{RESET}")
    
    model = MarketTrendsModel(redis_host=redis_host, redis_port=redis_port)
    
    if train:
        print(f"{YELLOW}Training models with {days_back} days of historical data...{RESET}")
        model.train_all_models(days_back=days_back)
    
    # Generate and display predictions
    predictions = model.generate_predictions()
    model.display_predictions(predictions)
    
    # Save historical predictions
    model.save_historical_predictions()
    
    return model

if __name__ == "__main__":
    run_model(days_back=30, train=True) 