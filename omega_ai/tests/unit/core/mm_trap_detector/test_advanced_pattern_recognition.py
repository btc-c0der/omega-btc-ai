import unittest
import numpy as np
from datetime import datetime, timedelta
from omega_ai.mm_trap_detector.advanced_pattern_recognition import AdvancedPatternRecognition, Pattern
import torch
import torch.nn as nn

class TestAdvancedPatternRecognition(unittest.TestCase):
    def setUp(self):
        self.input_size = 10
        self.sequence_length = 5
        self.model = AdvancedPatternRecognition(
            input_size=self.input_size,
            hidden_size=64,
            num_layers=2,
            num_classes=3
        )
        
    def test_model_initialization(self):
        """Test that the model is initialized correctly."""
        self.assertIsNotNone(self.model)
        self.assertIsNotNone(self.model.lstm)
        self.assertIsNotNone(self.model.fc)
        self.assertEqual(self.model.confidence_threshold, 0.75)
        self.assertEqual(len(self.model.pattern_history), 0)
        
        # Verify LSTM layer configuration
        self.assertEqual(self.model.lstm.input_size, self.input_size)
        self.assertEqual(self.model.lstm.hidden_size, 64)
        self.assertEqual(self.model.lstm.num_layers, 2)
        self.assertTrue(self.model.lstm.batch_first)
        
        # Verify fully connected layers
        fc_layers = list(self.model.fc)
        self.assertEqual(len(fc_layers), 3)  # Linear, ReLU, Linear
        self.assertEqual(fc_layers[0].in_features, 64)
        self.assertEqual(fc_layers[0].out_features, 32)
        self.assertEqual(fc_layers[2].in_features, 32)
        self.assertEqual(fc_layers[2].out_features, 3)
        
        # Test input-output compatibility
        test_input = torch.randn(1, self.sequence_length, self.input_size)
        output = self.model(test_input)
        self.assertEqual(output.shape, (1, 3))  # (batch_size, num_classes)
        
    def test_data_preprocessing(self):
        """Test data normalization and preprocessing."""
        # Create sample data with shape (batch_size, sequence_length, features)
        data = np.random.randn(1, self.sequence_length, self.input_size)
        processed_data = self.model.preprocess_data(data)
        
        # Check if the data is normalized
        processed_numpy = processed_data.cpu().numpy()
        mean_values = np.mean(processed_numpy, axis=(0, 1))
        std_values = np.std(processed_numpy, axis=(0, 1))
        print(f"\nMean values: {mean_values}")
        print(f"Std values: {std_values}")
        
        # Use a more reasonable tolerance for floating-point arithmetic
        self.assertTrue(np.allclose(mean_values, 0, atol=1e-7))
        self.assertTrue(np.allclose(std_values, 1, atol=1e-7))
        
    def test_pattern_detection(self):
        """Test pattern detection with synthetic data."""
        # Test with untrained model
        data = np.random.randn(1, self.sequence_length, self.input_size)
        pattern = self.model.detect_pattern(data)
        self.assertIsNone(pattern)
        
        # Mock a trained model by setting weights
        with torch.no_grad():
            # Set LSTM weights to create a simple pattern detector
            for name, param in self.model.lstm.named_parameters():
                if 'weight' in name:
                    param.fill_(0.5)  # Increased weights
                elif 'bias' in name:
                    param.fill_(0.2)  # Positive bias
            
            # Set FC layer weights to favor one class
            self.model.fc[0].weight.fill_(0.5)  # First FC layer
            self.model.fc[0].bias.fill_(0.2)
            self.model.fc[2].weight.fill_(0.6)  # Output layer
            self.model.fc[2].bias.data[0] = 2.0  # Strong bias for first class
        
        # Test with trained model
        pattern = self.model.detect_pattern(data)
        self.assertIsNotNone(pattern)
        self.assertEqual(pattern.pattern_type, 'bullish_trap')
        self.assertGreater(pattern.confidence, self.model.confidence_threshold)
        
    def test_pattern_history(self):
        """Test pattern history tracking and retrieval."""
        # Create multiple patterns with different timestamps
        now = datetime.now()
        test_features = [1.0] * (self.input_size * self.sequence_length)
        test_metadata = {'test': True}
        
        patterns = [
            Pattern(
                pattern_type='bullish_trap',
                confidence=0.85,
                timestamp=now - timedelta(hours=2),
                features=test_features,
                metadata=test_metadata
            ),
            Pattern(
                pattern_type='bearish_trap',
                confidence=0.92,
                timestamp=now - timedelta(minutes=45),  # Within 1 hour window
                features=test_features,
                metadata=test_metadata
            ),
            Pattern(
                pattern_type='neutral',
                confidence=0.78,
                timestamp=now - timedelta(minutes=15),  # Within 30 min window
                features=test_features,
                metadata=test_metadata
            )
        ]
        
        # Add patterns to history
        for pattern in patterns:
            self.model.pattern_history.append(pattern)
        
        # Test full history retrieval
        full_history = self.model.get_pattern_history()
        self.assertEqual(len(full_history), 3)
        self.assertEqual(full_history[0].pattern_type, 'bullish_trap')
        self.assertEqual(full_history[1].pattern_type, 'bearish_trap')
        self.assertEqual(full_history[2].pattern_type, 'neutral')
        
        # Test time-windowed history
        one_hour_history = self.model.get_pattern_history(time_window=timedelta(hours=1))
        self.assertEqual(len(one_hour_history), 2)  # Last 2 patterns
        
        thirty_min_history = self.model.get_pattern_history(time_window=timedelta(minutes=30))
        self.assertEqual(len(thirty_min_history), 1)  # Only the most recent pattern
        
    def test_confidence_threshold_adjustment(self):
        """Test dynamic confidence threshold adjustment."""
        initial_threshold = self.model.confidence_threshold
        
        # Test increasing threshold
        self.model.update_confidence_threshold(false_positive_rate=0.15)
        self.assertGreater(self.model.confidence_threshold, initial_threshold)
        
        # Test decreasing threshold
        self.model.update_confidence_threshold(false_positive_rate=0.03)
        self.assertLess(self.model.confidence_threshold, 0.95)
        
    def test_confidence_threshold_edge_cases(self):
        """Test confidence threshold adjustment with edge cases."""
        initial_threshold = self.model.confidence_threshold
        
        # Test extreme false positive rates
        # Case 1: 100% false positives
        self.model.update_confidence_threshold(false_positive_rate=1.0)
        self.assertEqual(self.model.confidence_threshold, min(0.95, initial_threshold + 0.05))
        
        # Reset threshold
        self.model.confidence_threshold = initial_threshold
        
        # Case 2: 0% false positives
        self.model.update_confidence_threshold(false_positive_rate=0.0)
        self.assertEqual(self.model.confidence_threshold, max(0.5, initial_threshold - 0.05))
        
        # Test multiple consecutive adjustments
        # Should not exceed bounds even with repeated calls
        self.model.confidence_threshold = 0.75  # Reset to initial
        for _ in range(10):
            self.model.update_confidence_threshold(false_positive_rate=1.0)
        self.assertLessEqual(self.model.confidence_threshold, 0.95)
        
        self.model.confidence_threshold = 0.75  # Reset to initial
        for _ in range(10):
            self.model.update_confidence_threshold(false_positive_rate=0.0)
        self.assertGreaterEqual(self.model.confidence_threshold, 0.5)
        
        # Test boundary values
        self.model.confidence_threshold = 0.94  # Just below upper bound
        self.model.update_confidence_threshold(false_positive_rate=0.15)
        self.assertEqual(self.model.confidence_threshold, 0.95)
        
        self.model.confidence_threshold = 0.51  # Just above lower bound
        self.model.update_confidence_threshold(false_positive_rate=0.03)
        self.assertEqual(self.model.confidence_threshold, 0.5)
        
        # Test invalid inputs (should handle gracefully)
        with self.assertRaises(ValueError):
            self.model.update_confidence_threshold(false_positive_rate=-0.1)
        
        with self.assertRaises(ValueError):
            self.model.update_confidence_threshold(false_positive_rate=1.1)
        
    def test_model_training(self):
        """Test model training with synthetic data."""
        # Create synthetic training data with clear patterns
        X_train = np.random.randn(100, self.sequence_length, self.input_size)
        y_train = np.zeros(100, dtype=np.int64)  # All samples belong to class 0
        
        # Store initial model state
        initial_state = {
            name: param.clone().detach()
            for name, param in self.model.named_parameters()
        }
        
        # Train the model with more epochs to ensure learning
        self.model.train_model(
            X_train, 
            y_train, 
            epochs=10,  # Increase epochs
            batch_size=32
        )
        
        # Verify model parameters have changed
        params_changed = False
        for name, param in self.model.named_parameters():
            if 'bias' in name or 'weight' in name:
                if not torch.allclose(param, initial_state[name], rtol=1e-3):
                    params_changed = True
                    break
        self.assertTrue(params_changed, "Model parameters did not change during training")
        
        # Test model performance on a small validation set
        X_val = np.random.randn(10, self.sequence_length, self.input_size)
        y_val = np.zeros(10, dtype=np.int64)  # All validation samples belong to class 0
        
        self.model.eval()
        with torch.no_grad():
            X_val_tensor = self.model.preprocess_data(X_val)
            outputs = self.model(X_val_tensor)
            loss = nn.CrossEntropyLoss()(outputs, torch.LongTensor(y_val).to(self.model.device))
            
            # Verify loss is reasonable
            self.assertLess(loss.item(), 2.0)  # Cross-entropy loss should be less than 2 for 3 classes
            
            # Check prediction shapes
            predictions = torch.argmax(outputs, dim=1)
            self.assertEqual(predictions.shape, (10,))

    def test_pattern_confidence_distribution(self):
        """Test that pattern confidence scores follow expected distribution."""
        sequence_length = self.sequence_length
        input_size = self.input_size
        
        # Print model's confidence threshold
        print(f"\nModel confidence threshold: {self.model.confidence_threshold}")
        
        # Mock a trained model by setting weights
        with torch.no_grad():
            # Set LSTM weights to create a pattern detector
            lstm_ih = torch.zeros(4 * self.model.hidden_size, input_size)
            lstm_ih[:self.model.hidden_size] = 0.6  # Input gate - moderate response to input
            lstm_ih[self.model.hidden_size:2*self.model.hidden_size] = -0.3  # Forget gate - moderate forgetting
            lstm_ih[2*self.model.hidden_size:3*self.model.hidden_size] = 0.5  # Cell gate - moderate memory
            lstm_ih[3*self.model.hidden_size:] = 0.2  # Output gate - weak output
            self.model.lstm.weight_ih_l0.copy_(lstm_ih)
            
            lstm_hh = torch.zeros(4 * self.model.hidden_size, self.model.hidden_size)
            lstm_hh[:self.model.hidden_size] = 0.3  # Input gate - moderate self connection
            lstm_hh[self.model.hidden_size:2*self.model.hidden_size] = 0.4  # Forget gate - moderate memory
            lstm_hh[2*self.model.hidden_size:3*self.model.hidden_size] = 0.2  # Cell gate - weak memory
            lstm_hh[3*self.model.hidden_size:] = 0.1  # Output gate - very weak output
            self.model.lstm.weight_hh_l0.copy_(lstm_hh)
            
            # Set biases to small positive values for better activation
            self.model.lstm.bias_ih_l0.fill_(0.1)
            self.model.lstm.bias_hh_l0.fill_(0.1)
            
            # Set FC layer weights for moderate pattern recognition
            fc1_weight = torch.zeros(self.model.fc[0].weight.shape)
            fc1_weight[0] = 0.7  # Moderate-strong weights for first output
            self.model.fc[0].weight.copy_(fc1_weight)
            self.model.fc[0].bias.fill_(0.1)
            
            fc2_weight = torch.zeros(self.model.fc[2].weight.shape)
            fc2_weight[0] = 0.8  # Strong weights for first class
            self.model.fc[2].weight.copy_(fc2_weight)
            self.model.fc[2].bias.data[0] = 1.2  # Moderate bias for first class
        
        # Create a clear pattern with price-like characteristics
        clear_pattern = np.zeros((1, sequence_length, input_size))
        base_price = 100.0
        for i in range(sequence_length):
            # Create a clear uptrend with very small random variations
            trend = 0.2 * i / sequence_length  # Stronger linear uptrend
            if i < sequence_length // 2:
                # First half: steady uptrend
                noise = np.random.randn() * 0.002  # Very small random variations
            else:
                # Second half: accelerating uptrend
                trend *= 1.5
                noise = np.random.randn() * 0.001  # Even smaller random variations
            clear_pattern[0, i] = base_price * (1 + trend + noise)
        
        # Create a noisy pattern with random price movements
        noisy_pattern = np.zeros((1, sequence_length, input_size))
        for i in range(sequence_length):
            # Random walk with high volatility and mean reversion
            if i > 0:
                mean_reversion = 0.3 * (base_price - noisy_pattern[0, i-1]) / base_price
                noise = np.random.randn() * 0.15  # Very large random variations
                noisy_pattern[0, i] = noisy_pattern[0, i-1] * (1 + noise + mean_reversion)
            else:
                noise = np.random.randn() * 0.1
                noisy_pattern[0, i] = base_price * (1 + noise)
        
        # Print raw pattern statistics
        print(f"\nRaw clear pattern statistics:")
        print(f"Mean: {clear_pattern.mean():.4f}")
        print(f"Std: {clear_pattern.std():.4f}")
        print(f"Min: {clear_pattern.min():.4f}")
        print(f"Max: {clear_pattern.max():.4f}")
        
        print(f"\nRaw noisy pattern statistics:")
        print(f"Mean: {noisy_pattern.mean():.4f}")
        print(f"Std: {noisy_pattern.std():.4f}")
        print(f"Min: {noisy_pattern.min():.4f}")
        print(f"Max: {noisy_pattern.max():.4f}")
        
        # Calculate returns instead of using raw prices
        clear_returns = np.zeros_like(clear_pattern)
        clear_returns[0, 1:] = np.diff(clear_pattern[0], axis=0) / clear_pattern[0, :-1]
        
        noisy_returns = np.zeros_like(noisy_pattern)
        noisy_returns[0, 1:] = np.diff(noisy_pattern[0], axis=0) / noisy_pattern[0, :-1]
        
        # Normalize returns using their own statistics
        clear_returns = (clear_returns - clear_returns.mean()) / (clear_returns.std() + 1e-8)
        noisy_returns = (noisy_returns - noisy_returns.mean()) / (noisy_returns.std() + 1e-8)
        
        # Print normalized return statistics
        print(f"\nNormalized clear returns statistics:")
        print(f"Mean: {clear_returns.mean():.4f}")
        print(f"Std: {clear_returns.std():.4f}")
        print(f"Min: {clear_returns.min():.4f}")
        print(f"Max: {clear_returns.max():.4f}")
        
        print(f"\nNormalized noisy returns statistics:")
        print(f"Mean: {noisy_returns.mean():.4f}")
        print(f"Std: {noisy_returns.std():.4f}")
        print(f"Min: {noisy_returns.min():.4f}")
        print(f"Max: {noisy_returns.max():.4f}")
        
        # Detect patterns using returns
        clear_result = self.model.detect_pattern(clear_returns)
        noisy_result = self.model.detect_pattern(noisy_returns)
        
        # Print detection results
        print(f"\nDetection results:")
        print(f"Clear pattern detected: {clear_result is not None}")
        if clear_result is not None:
            print(f"Clear pattern confidence: {clear_result.confidence:.4f}")
        print(f"Noisy pattern detected: {noisy_result is not None}")
        if noisy_result is not None:
            print(f"Noisy pattern confidence: {noisy_result.confidence:.4f}")
        
        # Clear pattern should have high confidence
        self.assertIsNotNone(clear_result)
        self.assertGreater(clear_result.confidence, 0.75)
        
        # Noisy pattern should either have low confidence or not be detected
        if noisy_result is not None:
            self.assertLess(noisy_result.confidence, clear_result.confidence)
        
        # Generate multiple patterns and check confidence distribution
        num_samples = 100
        confidences = []
        
        for i in range(num_samples):
            # Create a pattern with varying levels of noise
            noise_level = i / num_samples  # Gradually increase noise
            
            # Start with a clear trend
            base_pattern = np.zeros((sequence_length, input_size))
            for j in range(sequence_length):
                trend = 0.1 * j / sequence_length  # Linear trend
                noise = np.random.randn() * 0.01 * (1 + noise_level)  # Increasing noise
                base_pattern[j] = base_price * (1 + trend + noise)
            
            # Add random walk component
            random_walk = np.zeros((sequence_length, input_size))
            for j in range(sequence_length):
                noise = np.random.randn() * 0.05 * noise_level
                if j > 0:
                    random_walk[j] = random_walk[j-1] * (1 + noise)
                else:
                    random_walk[j] = base_price * noise
            
            # Combine trend and random walk
            mixed_pattern = base_pattern + random_walk
            
            # Normalize the pattern
            mixed_pattern = (mixed_pattern - mixed_pattern.mean()) / (mixed_pattern.std() + 1e-8)
            mixed_pattern = mixed_pattern.reshape(1, sequence_length, input_size)
            
            result = self.model.detect_pattern(mixed_pattern)
            if result is not None:
                confidences.append(result.confidence)
        
        if confidences:
            confidences = np.array(confidences)
            
            # Print confidence distribution statistics
            print(f"\nConfidence distribution statistics:")
            print(f"Number of detections: {len(confidences)}")
            print(f"Mean confidence: {confidences.mean():.4f}")
            print(f"Std confidence: {confidences.std():.4f}")
            print(f"Min confidence: {confidences.min():.4f}")
            print(f"Max confidence: {confidences.max():.4f}")
            
            # Check confidence distribution properties
            self.assertGreater(len(confidences), 0)
            self.assertTrue(np.all(confidences >= self.model.confidence_threshold))
            self.assertTrue(np.all(confidences <= 1.0))
            
            # Check for reasonable spread in confidences
            confidence_std = np.std(confidences)
            self.assertGreater(confidence_std, 0.001)
            self.assertLess(confidence_std, 0.1)

    def test_overfitting_protection(self):
        """Test that the model doesn't overfit during training."""
        # Generate synthetic training and validation data
        X_train = np.random.randn(200, self.sequence_length, self.input_size)
        y_train = np.random.randint(0, self.model.num_classes, 200)
        
        X_val = np.random.randn(50, self.sequence_length, self.input_size)
        y_val = np.random.randint(0, self.model.num_classes, 50)
        
        # Convert validation data to tensors
        X_val_tensor = self.model.preprocess_data(X_val)
        y_val_tensor = torch.LongTensor(y_val).to(self.model.device)
        
        # Track losses across epochs
        train_losses = []
        val_losses = []
        criterion = nn.CrossEntropyLoss()
        
        # Train for multiple epochs
        num_epochs = 5
        batch_size = 32
        
        for epoch in range(num_epochs):
            # Train for one epoch
            self.model.train_model(X_train, y_train, epochs=1, batch_size=batch_size)
            
            # Calculate training loss
            self.model.eval()
            with torch.no_grad():
                X_train_tensor = self.model.preprocess_data(X_train)
                y_train_tensor = torch.LongTensor(y_train).to(self.model.device)
                train_outputs = self.model(X_train_tensor)
                train_loss = criterion(train_outputs, y_train_tensor).item()
                train_losses.append(train_loss)
                
                # Calculate validation loss
                val_outputs = self.model(X_val_tensor)
                val_loss = criterion(val_outputs, y_val_tensor).item()
                val_losses.append(val_loss)
        
        # Check for signs of overfitting
        for train_loss, val_loss in zip(train_losses, val_losses):
            # Training loss shouldn't be too close to zero
            self.assertGreater(train_loss, 0.1)
            
            # Validation loss shouldn't be much larger than training loss
            loss_ratio = val_loss / train_loss if train_loss > 0 else float('inf')
            self.assertLess(loss_ratio, 3.0)
            
        # Check that loss decreases over time (but not too quickly)
        for i in range(1, len(train_losses)):
            # Loss should decrease
            self.assertLess(train_losses[i], train_losses[i-1])
            
            # But not too dramatically (indicating potential overfitting)
            loss_reduction = train_losses[i-1] - train_losses[i]
            self.assertLess(loss_reduction, train_losses[i-1] * 0.5)

if __name__ == '__main__':
    unittest.main() 