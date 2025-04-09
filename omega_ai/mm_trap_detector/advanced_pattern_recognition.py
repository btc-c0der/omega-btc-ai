import numpy as np
import torch
import torch.nn as nn
from typing import List, Tuple, Optional, Union, Sequence, Dict
from dataclasses import dataclass
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import plotly.graph_objects as go
from plotly.subplots import make_subplots

@dataclass
class Pattern:
    timestamp: datetime
    confidence: float
    pattern_type: str
    features: Sequence[float]
    metadata: dict

class AdvancedPatternRecognition(nn.Module):
    def __init__(self, input_size: int, hidden_size: int = 64, num_layers: int = 2, num_classes: int = 3, pattern_expiry_hours: int = 24):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_classes = num_classes
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.pattern_expiry_hours = pattern_expiry_hours
        
        # Initialize layers
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True
        )
        
        # Add batch normalization
        self.batch_norm = nn.BatchNorm1d(input_size)
        
        # Fully connected layers
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Linear(hidden_size // 2, num_classes)
        )
        
        # Move model to device
        self.to(self.device)
        
        # Initialize pattern history and confidence threshold
        self.pattern_history: List[Pattern] = []
        self.confidence_threshold: float = 0.75
        
        # Initialize training metrics storage
        self.training_logs: List[dict] = []
        
        # Pattern decay rates (in hours) for different pattern types
        self.decay_rates: Dict[str, float] = {
            'bullish_trap': 6.0,    # Bullish traps decay faster
            'bearish_trap': 12.0,   # Bearish traps decay moderately
            'neutral': 24.0         # Neutral patterns decay slowest
        }
        
        # Pattern persistence tracking
        self.pattern_occurrences: Dict[str, int] = {
            'bullish_trap': 0,
            'bearish_trap': 0,
            'neutral': 0
        }
        
        # Initialize weights using Xavier initialization
        self._init_weights()
        
        # Initialize visualization settings
        self.visualization_settings = {
            'color_scheme': {
                'bullish_trap': '#00ff00',  # Green for bullish traps
                'bearish_trap': '#ff0000',  # Red for bearish traps
                'neutral': '#808080'        # Gray for neutral
            },
            'cluster_colors': ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff'],
            'default_figsize': (15, 10),
            'alpha': 0.7
        }
        
    def _init_weights(self):
        """Initialize model weights using Xavier initialization."""
        for name, param in self.lstm.named_parameters():
            if "weight" in name:
                nn.init.xavier_uniform_(param)
            elif "bias" in name:
                param.data.fill_(0)
        
        # Initialize FC layers with Xavier
        for name, param in self.fc.named_parameters():
            if "weight" in name:
                nn.init.xavier_uniform_(param)
            elif "bias" in name:
                param.data.fill_(0)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass of the model."""
        # LSTM returns (output, (hidden_state, cell_state))
        lstm_out, _ = self.lstm(x)
        # Use the last output from the LSTM
        last_output = lstm_out[:, -1, :]
        return self.fc(last_output)
    
    def preprocess_data(self, data):
        """Preprocess input data for model prediction."""
        # Convert to numpy array for normalization
        if isinstance(data, torch.Tensor):
            data = data.detach().cpu().numpy()
        elif not isinstance(data, np.ndarray):
            data = np.array(data)
        
        # Ensure data is 3D: (batch_size, sequence_length, features)
        if len(data.shape) == 2:
            data = np.expand_dims(data, axis=0)
        
        # Calculate mean and std for each feature
        mean = np.mean(data, axis=(0, 1), keepdims=True)
        std = np.std(data, axis=(0, 1), keepdims=True)
        std[std == 0] = 1.0
        
        # Normalize
        normalized_data = (data - mean) / std
        
        # Convert to torch tensor and move to device
        return torch.FloatTensor(normalized_data).to(self.device)
    
    def detect_pattern(self, data: np.ndarray) -> Optional[Pattern]:
        """Detect patterns in the input data with uncertainty handling."""
        self.eval()  # Set model to evaluation mode
        with torch.no_grad():
            input_tensor = self.preprocess_data(data)
            output = self(input_tensor)
            
            # Get raw logits
            raw_outputs = output.squeeze()
            
            # Calculate confidence using softmax probabilities
            probabilities = torch.softmax(raw_outputs, dim=0)
            predicted = torch.argmax(raw_outputs)
            base_confidence = probabilities[predicted].item()
            
            # Calculate pattern complexity (using standard deviation of returns)
            if len(data.shape) == 3:  # (batch, sequence, features)
                returns = np.diff(data[0], axis=0) / data[0, :-1]
            else:  # (sequence, features)
                returns = np.diff(data, axis=0) / data[:-1]
            complexity = float(np.std(returns))
            
            # Apply complexity penalty
            complexity_penalty = 0.05 * complexity  # 5% penalty
            confidence = max(0.0, min(1.0, base_confidence - complexity_penalty))
            
            # Debug output
            print(f"\nConfidence calculation:")
            print(f"Raw logits: {raw_outputs.tolist()}")
            print(f"Probabilities: {probabilities.tolist()}")
            print(f"Base confidence: {base_confidence:.4f}")
            print(f"Complexity: {complexity:.4f}")
            print(f"Complexity penalty: {complexity_penalty:.4f}")
            print(f"Final confidence: {confidence:.4f}")
            
            # Handle uncertain predictions
            pattern_type = self._get_pattern_type(predicted.item())
            is_uncertain = 0.45 <= confidence <= 0.55
            
            if confidence > self.confidence_threshold:
                pattern = Pattern(
                    timestamp=datetime.now(),
                    confidence=confidence,
                    pattern_type=pattern_type,
                    features=[float(x) for x in data.flatten().tolist()],
                    metadata={
                        'model_version': '1.0',
                        'complexity': complexity,
                        'base_confidence': base_confidence,
                        'complexity_penalty': complexity_penalty,
                        'probabilities': probabilities.tolist(),
                        'is_uncertain': is_uncertain,
                        'requires_review': is_uncertain
                    }
                )
                self.pattern_history.append(pattern)
                return pattern
        return None
    
    def _get_pattern_type(self, class_idx: int) -> str:
        """Map class index to pattern type."""
        pattern_types = ['bullish_trap', 'bearish_trap', 'neutral']
        return pattern_types[class_idx]
    
    def update_confidence_threshold(self, false_positive_rate: float):
        """Dynamically adjust confidence threshold based on false positive rate."""
        if not isinstance(false_positive_rate, (int, float)):
            raise ValueError("false_positive_rate must be a number")
        if false_positive_rate < 0.0 or false_positive_rate > 1.0:
            raise ValueError("false_positive_rate must be between 0.0 and 1.0")
            
        if false_positive_rate > 0.1:  # If too many false positives
            self.confidence_threshold = min(0.95, self.confidence_threshold + 0.05)
        elif false_positive_rate < 0.05:  # If too few detections
            self.confidence_threshold = max(0.5, self.confidence_threshold - 0.05)
    
    def get_pattern_history(self, time_window: Optional[Union[int, timedelta]] = None) -> List[Pattern]:
        """Retrieve pattern history within the specified time window with multi-timescale weighting."""
        # Auto-expire old patterns based on configured expiry time
        cutoff_time = datetime.now() - timedelta(hours=self.pattern_expiry_hours)
        self.pattern_history = [
            p for p in self.pattern_history 
            if p.timestamp > cutoff_time or p.metadata.get("persistent", False)
        ]
        
        if time_window is None:
            return self.pattern_history
        
        # Apply time-based weighting to patterns with pattern-specific decay rates
        current_time = datetime.now()
        weighted_patterns = []
        for pattern in self.pattern_history:
            # Skip weighting for persistent patterns
            if pattern.metadata.get("persistent", False):
                weighted_patterns.append(pattern)
                continue
            
            # Get decay rate for pattern type
            decay_rate = self.decay_rates.get(pattern.pattern_type, 12.0)
            
            # Calculate time weight with pattern-specific decay
            time_since_pattern = (current_time - pattern.timestamp).total_seconds()
            time_weight = np.exp(-time_since_pattern / (60 * 60 * decay_rate))
            
            # Apply time weight to confidence
            weighted_confidence = pattern.confidence * time_weight
            
            # Create weighted pattern
            weighted_pattern = Pattern(
                timestamp=pattern.timestamp,
                confidence=weighted_confidence,
                pattern_type=pattern.pattern_type,
                features=pattern.features,
                metadata={
                    **pattern.metadata,
                    'time_weight': time_weight,
                    'original_confidence': pattern.confidence,
                    'decay_rate': decay_rate
                }
            )
            weighted_patterns.append(weighted_pattern)
        
        # Filter by time window
        cutoff_time = current_time - (time_window if isinstance(time_window, timedelta) else timedelta(seconds=time_window))
        return [p for p in weighted_patterns if p.timestamp > cutoff_time]
    
    def reinforce_training(self, detected_patterns: List[Pattern]):
        """Use detected patterns to refine the model through reinforcement learning."""
        if not detected_patterns:
            return  # No new patterns to learn from
        
        # Extract features and labels from detected patterns
        X_reinforce = np.array([p.features for p in detected_patterns])
        y_reinforce = np.array([self._get_pattern_idx(p.pattern_type) for p in detected_patterns])
        
        # Train further using detected data
        self.train_model(X_reinforce, y_reinforce, epochs=3, batch_size=16)
    
    def cluster_patterns(self, num_clusters: int = 3) -> List[int]:
        """Cluster historical patterns to detect repetitive Market Maker moves."""
        if len(self.pattern_history) < num_clusters:
            return []
        
        # Extract features from pattern history
        features = np.array([p.features for p in self.pattern_history])
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(features)
        
        # Add cluster labels to pattern metadata
        for pattern, label in zip(self.pattern_history, kmeans.labels_):
            pattern.metadata['cluster'] = int(label)
        
        return kmeans.labels_.tolist()
    
    def _get_pattern_idx(self, pattern_type: str) -> int:
        """Map pattern type to class index."""
        pattern_types = ['bullish_trap', 'bearish_trap', 'neutral']
        return pattern_types.index(pattern_type)
    
    def train_model(self, X_train: np.ndarray, y_train: np.ndarray, X_val: Optional[np.ndarray] = None, y_val: Optional[np.ndarray] = None, epochs: int = 10, batch_size: int = 32, patience: int = 3):
        """Train the model on the provided data with early stopping and expanded metrics storage."""
        self.train()  # Set model to training mode
        
        # Convert labels to tensor
        y_train = torch.LongTensor(y_train).to(self.device)
        if X_val is not None and y_val is not None:
            y_val = torch.LongTensor(y_val).to(self.device)
        
        # Create optimizer and loss function
        optimizer = torch.optim.Adam(self.parameters())
        criterion = nn.CrossEntropyLoss()
        
        # Early stopping setup
        best_val_loss = float('inf')
        patience_counter = 0
        
        # Training loop
        for epoch in range(epochs):
            epoch_loss = 0.0
            num_batches = 0
            
            # Process data in batches
            for i in range(0, len(X_train), batch_size):
                batch_X = X_train[i:i + batch_size]
                batch_y = y_train[i:i + batch_size]
                
                # Zero the gradients
                optimizer.zero_grad()
                
                # Forward pass
                batch_X = self.preprocess_data(batch_X)
                outputs = self(batch_X)
                
                # Compute loss
                loss = criterion(outputs, batch_y)
                
                # Backward pass
                loss.backward()
                
                # Clip gradients to prevent exploding gradients
                torch.nn.utils.clip_grad_norm_(self.parameters(), max_norm=1.0)
                
                # Optimize
                optimizer.step()
                
                epoch_loss += loss.item()
                num_batches += 1
            
            # Calculate average training loss
            avg_train_loss = epoch_loss / num_batches
            
            # Calculate validation loss if validation data is provided
            epoch_metrics = {
                'epoch': epoch + 1,
                'train_loss': avg_train_loss,
                'val_loss': None,
                'timestamp': datetime.now(),
                'model_config': {
                    'hidden_size': self.hidden_size,
                    'num_layers': self.num_layers,
                    'confidence_threshold': self.confidence_threshold,
                    'pattern_expiry_hours': self.pattern_expiry_hours
                }
            }
            
            if X_val is not None and y_val is not None:
                self.eval()
                with torch.no_grad():
                    val_X = self.preprocess_data(X_val)
                    val_outputs = self(val_X)
                    val_loss = criterion(val_outputs, y_val).item()
                    epoch_metrics['val_loss'] = val_loss
                    
                    # Early stopping check
                    if val_loss < best_val_loss:
                        best_val_loss = val_loss
                        patience_counter = 0
                        # Save best model state
                        self.best_model_state = self.state_dict()
                    else:
                        patience_counter += 1
                        if patience_counter >= patience:
                            print(f"Early stopping triggered after {epoch + 1} epochs!")
                            # Restore best model state
                            self.load_state_dict(self.best_model_state)
                            break
                    
                    print(f"Epoch {epoch+1}/{epochs}")
                    print(f"Training Loss: {avg_train_loss:.4f}")
                    print(f"Validation Loss: {val_loss:.4f}")
                    print("-" * 50)
            else:
                print(f"Epoch {epoch+1}/{epochs}")
                print(f"Training Loss: {avg_train_loss:.4f}")
                print("-" * 50)
            
            # Store training metrics
            self.training_logs.append(epoch_metrics)
        
        self.eval()  # Set model back to evaluation mode
    
    def visualize_clusters(self, num_clusters: int = 3, save_path: Optional[str] = None):
        """Visualize pattern clusters in 2D space using PCA."""
        if len(self.pattern_history) < num_clusters:
            print("Not enough patterns for clustering.")
            return
        
        # Extract features and perform PCA
        features = np.array([p.features for p in self.pattern_history])
        pca = PCA(n_components=2).fit_transform(features)
        labels = self.cluster_patterns(num_clusters)
        
        # Create visualization
        plt.figure(figsize=(12, 8))
        scatter = plt.scatter(pca[:, 0], pca[:, 1], c=labels, cmap='viridis', alpha=0.7)
        
        # Add pattern type labels
        for i, pattern in enumerate(self.pattern_history):
            plt.annotate(pattern.pattern_type, (pca[i, 0], pca[i, 1]))
        
        plt.colorbar(scatter, label='Cluster')
        plt.title("Market Maker Pattern Clusters")
        plt.xlabel("First Principal Component")
        plt.ylabel("Second Principal Component")
        
        if save_path:
            plt.savefig(save_path)
        plt.show()
    
    def apply_pattern_weighting(self, pattern: Pattern, market_conditions: dict) -> float:
        """Apply sophisticated weighting to pattern confidence based on market conditions."""
        # Volume weighting (log scale to handle large volumes)
        volume_weight = np.log(market_conditions.get("volume", 1) + 1)
        
        # Fibonacci level proximity
        fibo_weight = 1.2 if market_conditions.get("near_fibo", False) else 1.0
        
        # Volatility weighting
        volatility_weight = 1.5 if market_conditions.get("high_volatility", False) else 1.0
        
        # Time decay (patterns become less relevant over time)
        time_since_pattern = (datetime.now() - pattern.timestamp).total_seconds()
        decay_rate = self.decay_rates.get(pattern.pattern_type, 12.0)
        time_weight = np.exp(-time_since_pattern / (60 * 60 * decay_rate))
        
        # Calculate weighted confidence
        weighted_confidence = pattern.confidence * volume_weight * fibo_weight * volatility_weight * time_weight
        
        # Store weights in metadata for analysis
        pattern.metadata.update({
            'volume_weight': volume_weight,
            'fibo_weight': fibo_weight,
            'volatility_weight': volatility_weight,
            'time_weight': time_weight,
            'market_conditions': market_conditions
        })
        
        return min(1.0, weighted_confidence)
    
    def check_persistent_patterns(self, pattern: Pattern, threshold: int = 5):
        """Check if a pattern should be marked as persistent based on frequency."""
        self.pattern_occurrences[pattern.pattern_type] += 1
        occurrences = self.pattern_occurrences[pattern.pattern_type]
        
        if occurrences >= threshold:
            pattern.metadata["persistent"] = True
            pattern.metadata["occurrences"] = occurrences
            pattern.metadata["first_seen"] = pattern.timestamp
            print(f"Pattern {pattern.pattern_type} marked as persistent after {occurrences} occurrences!")
    
    def visualize_patterns_5d(self, save_path: Optional[str] = None):
        """Create a stunning 5D visualization of Market Maker patterns using Plotly."""
        if len(self.pattern_history) < 3:
            print("Not enough patterns for 5D visualization.")
            return
        
        # Extract features and perform PCA for 3D visualization
        features = np.array([p.features for p in self.pattern_history])
        pca = PCA(n_components=3).fit_transform(features)
        
        # Get cluster labels
        labels = self.cluster_patterns(5)  # Use 5 clusters for better visualization
        
        # Create figure with secondary y-axis
        fig = make_subplots(rows=2, cols=2,
                           specs=[[{"type": "scatter3d"}, {"type": "scatter"}],
                                 [{"type": "heatmap"}, {"type": "scatter"}]])
        
        # 3D Scatter Plot (Pattern Clusters)
        fig.add_trace(
            go.Scatter3d(
                x=pca[:, 0],
                y=pca[:, 1],
                z=pca[:, 2],
                mode='markers+text',
                marker=dict(
                    size=8,
                    color=[self.visualization_settings['cluster_colors'][l] for l in labels],
                    opacity=0.8
                ),
                text=[f"{p.pattern_type}<br>Conf: {p.confidence:.2f}" for p in self.pattern_history],
                textposition="top center",
                name="Pattern Clusters"
            ),
            row=1, col=1
        )
        
        # Time Series of Pattern Confidences
        times = [p.timestamp for p in self.pattern_history]
        confidences = [p.confidence for p in self.pattern_history]
        fig.add_trace(
            go.Scatter(
                x=times,
                y=confidences,
                mode='lines+markers',
                name="Confidence Over Time",
                line=dict(color='#00ff00')
            ),
            row=1, col=2
        )
        
        # Pattern Type Distribution Heatmap
        pattern_types = [p.pattern_type for p in self.pattern_history]
        clusters = labels
        heatmap_data = np.zeros((3, 5))  # 3 pattern types, 5 clusters
        for i, (pt, cl) in enumerate(zip(pattern_types, clusters)):
            pt_idx = ['bullish_trap', 'bearish_trap', 'neutral'].index(pt)
            heatmap_data[pt_idx, cl] += 1
        
        fig.add_trace(
            go.Heatmap(
                z=heatmap_data,
                colorscale='Viridis',
                name="Pattern Distribution"
            ),
            row=2, col=1
        )
        
        # Pattern Persistence Timeline
        persistent_patterns = [p for p in self.pattern_history if p.metadata.get("persistent", False)]
        if persistent_patterns:
            fig.add_trace(
                go.Scatter(
                    x=[p.timestamp for p in persistent_patterns],
                    y=[p.metadata.get("occurrences", 0) for p in persistent_patterns],
                    mode='markers',
                    marker=dict(
                        size=10,
                        color='#ff00ff',
                        symbol='star'
                    ),
                    name="Persistent Patterns"
                ),
                row=2, col=2
            )
        
        # Update layout
        fig.update_layout(
            title="Omega AI Market Maker Pattern Analysis",
            showlegend=True,
            height=1000,
            width=1200,
            scene=dict(
                xaxis_title="First Principal Component",
                yaxis_title="Second Principal Component",
                zaxis_title="Third Principal Component"
            )
        )
        
        # Update axes labels
        fig.update_xaxes(title_text="Time", row=1, col=2)
        fig.update_yaxes(title_text="Confidence", row=1, col=2)
        fig.update_xaxes(title_text="Pattern Type", row=2, col=1)
        fig.update_yaxes(title_text="Cluster", row=2, col=1)
        fig.update_xaxes(title_text="Time", row=2, col=2)
        fig.update_yaxes(title_text="Occurrences", row=2, col=2)
        
        if save_path:
            fig.write_html(save_path)
        fig.show()
    
    def visualize_pattern_evolution(self, save_path: Optional[str] = None):
        """Create an animated visualization of pattern evolution over time."""
        if len(self.pattern_history) < 10:
            print("Not enough patterns for evolution visualization.")
            return
        
        # Sort patterns by timestamp
        sorted_patterns = sorted(self.pattern_history, key=lambda x: x.timestamp)
        
        # Create figure
        fig = go.Figure()
        
        # Add initial scatter plot
        fig.add_trace(
            go.Scatter(
                x=[p.timestamp for p in sorted_patterns[:10]],
                y=[p.confidence for p in sorted_patterns[:10]],
                mode='markers+lines',
                marker=dict(
                    size=10,
                    color=[self.visualization_settings['color_scheme'][p.pattern_type] for p in sorted_patterns[:10]]
                ),
                name="Pattern Evolution"
            )
        )
        
        # Create frames for animation
        frames = []
        for i in range(10, len(sorted_patterns) + 1):
            frames.append(
                go.Frame(
                    data=[
                        go.Scatter(
                            x=[p.timestamp for p in sorted_patterns[:i]],
                            y=[p.confidence for p in sorted_patterns[:i]],
                            mode='markers+lines',
                            marker=dict(
                                size=10,
                                color=[self.visualization_settings['color_scheme'][p.pattern_type] for p in sorted_patterns[:i]]
                            )
                        )
                    ]
                )
            )
        
        # Update layout
        fig.update_layout(
            title="Omega AI Pattern Evolution",
            xaxis_title="Time",
            yaxis_title="Confidence",
            showlegend=True,
            updatemenus=[dict(
                type="buttons",
                showactive=False,
                buttons=[dict(
                    label="Play",
                    method="animate",
                    args=[None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}]
                )]
            )]
        )
        
        # Add frames to figure
        fig.frames = frames
        
        if save_path:
            fig.write_html(save_path)
        fig.show()
    
    def visualize_pattern_impact(self, save_path: Optional[str] = None):
        """Create a visualization showing the impact of different market conditions on pattern confidence."""
        if not self.pattern_history:
            print("No patterns to analyze.")
            return
        
        # Create figure with subplots
        fig = make_subplots(rows=2, cols=2,
                           specs=[[{"type": "scatter"}, {"type": "scatter"}],
                                 [{"type": "scatter"}, {"type": "scatter"}]])
        
        # Extract market conditions and weights
        market_conditions = []
        weights = []
        for pattern in self.pattern_history:
            if 'market_conditions' in pattern.metadata:
                market_conditions.append(pattern.metadata['market_conditions'])
                weights.append({
                    'volume': pattern.metadata.get('volume_weight', 1.0),
                    'fibo': pattern.metadata.get('fibo_weight', 1.0),
                    'volatility': pattern.metadata.get('volatility_weight', 1.0),
                    'time': pattern.metadata.get('time_weight', 1.0)
                })
        
        if not market_conditions:
            print("No market conditions data available.")
            return
        
        # Volume Impact
        fig.add_trace(
            go.Scatter(
                x=[mc.get('volume', 0) for mc in market_conditions],
                y=[w['volume'] for w in weights],
                mode='markers',
                marker=dict(
                    size=8,
                    color=[self.visualization_settings['color_scheme'][p.pattern_type] for p in self.pattern_history]
                ),
                name="Volume Impact"
            ),
            row=1, col=1
        )
        
        # Fibonacci Impact
        fig.add_trace(
            go.Scatter(
                x=[1 if mc.get('near_fibo', False) else 0 for mc in market_conditions],
                y=[w['fibo'] for w in weights],
                mode='markers',
                marker=dict(
                    size=8,
                    color=[self.visualization_settings['color_scheme'][p.pattern_type] for p in self.pattern_history]
                ),
                name="Fibonacci Impact"
            ),
            row=1, col=2
        )
        
        # Volatility Impact
        fig.add_trace(
            go.Scatter(
                x=[1 if mc.get('high_volatility', False) else 0 for mc in market_conditions],
                y=[w['volatility'] for w in weights],
                mode='markers',
                marker=dict(
                    size=8,
                    color=[self.visualization_settings['color_scheme'][p.pattern_type] for p in self.pattern_history]
                ),
                name="Volatility Impact"
            ),
            row=2, col=1
        )
        
        # Time Decay
        fig.add_trace(
            go.Scatter(
                x=[(datetime.now() - p.timestamp).total_seconds() / 3600 for p in self.pattern_history],
                y=[w['time'] for w in weights],
                mode='markers',
                marker=dict(
                    size=8,
                    color=[self.visualization_settings['color_scheme'][p.pattern_type] for p in self.pattern_history]
                ),
                name="Time Decay"
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title="Omega AI Pattern Impact Analysis",
            showlegend=True,
            height=800,
            width=1000
        )
        
        # Update axes labels
        fig.update_xaxes(title_text="Volume", row=1, col=1)
        fig.update_yaxes(title_text="Weight", row=1, col=1)
        fig.update_xaxes(title_text="Near Fibonacci", row=1, col=2)
        fig.update_yaxes(title_text="Weight", row=1, col=2)
        fig.update_xaxes(title_text="High Volatility", row=2, col=1)
        fig.update_yaxes(title_text="Weight", row=2, col=1)
        fig.update_xaxes(title_text="Hours Since Pattern", row=2, col=2)
        fig.update_yaxes(title_text="Weight", row=2, col=2)
        
        if save_path:
            fig.write_html(save_path)
        fig.show() 