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

"""
Quantum Neural Network Metrics
============================

Specialized metrics for evaluating quantum neural network models,
including quantum-inspired fidelity and entanglement measures.
"""

import numpy as np
import logging
from typing import Dict, Any, Optional, Union
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score

# Set up logging
logger = logging.getLogger("quantum-neural-net")

# Constants
LOG_PREFIX = "🧠 vQuB1T-NN"
PI = np.pi

def quantum_fidelity(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Compute quantum fidelity between true and predicted values.
    
    In quantum computing, fidelity measures how close two quantum
    states are to each other. This is a classical approximation.
    
    Args:
        y_true: True values
        y_pred: Predicted values
        
    Returns:
        Fidelity value (0 to 1, higher is better)
    """
    # Normalize the vectors to unit length (quantum state-like)
    if np.iscomplexobj(y_true) or np.iscomplexobj(y_pred):
        # For complex values, normalization uses the complex modulus
        y_true_norm = np.abs(y_true)**2
        y_pred_norm = np.abs(y_pred)**2
        
        # Ensure proper normalization (sum to 1)
        y_true_norm = y_true_norm / np.sum(y_true_norm, axis=-1, keepdims=True)
        y_pred_norm = y_pred_norm / np.sum(y_pred_norm, axis=-1, keepdims=True)
        
        # Calculate fidelity using Bhattacharyya coefficient for probability distributions
        fidelity = np.sum(np.sqrt(y_true_norm * y_pred_norm), axis=-1)
        
        # If multi-dimensional, average across all dimensions
        if fidelity.ndim > 0:
            fidelity = np.mean(fidelity)
    else:
        # For real values, normalize vectors
        y_true_norm = y_true / (np.linalg.norm(y_true) + 1e-10)
        y_pred_norm = y_pred / (np.linalg.norm(y_pred) + 1e-10)
        
        # Calculate classical fidelity (cosine similarity)
        fidelity = np.abs(np.dot(y_true_norm, y_pred_norm))
    
    return float(fidelity)

def entanglement_entropy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Compute entanglement entropy of the prediction errors.
    
    Higher entropy indicates more complex error patterns that could 
    benefit from quantum entanglement modeling.
    
    Args:
        y_true: True values
        y_pred: Predicted values
        
    Returns:
        Entropy value (0 to log2(n), higher indicates more complex errors)
    """
    # Compute errors
    errors = y_true - y_pred
    
    # Create correlation matrix from errors
    if errors.ndim == 1:
        # For univariate predictions, reshape to matrix form
        errors = errors.reshape(-1, 1)
    
    # Center the errors
    centered_errors = errors - np.mean(errors, axis=0, keepdims=True)
    
    # Compute error covariance matrix
    n_samples = errors.shape[0]
    cov_matrix = np.dot(centered_errors.T, centered_errors) / n_samples
    
    # Ensure matrix is valid for eigenvalue calculation
    cov_matrix = (cov_matrix + cov_matrix.T) / 2  # Make symmetric
    
    # Add small diagonal term for numerical stability
    cov_matrix = cov_matrix + np.eye(cov_matrix.shape[0]) * 1e-10
    
    # Compute eigenvalues
    eigenvalues = np.linalg.eigvalsh(cov_matrix)
    
    # Ensure eigenvalues are positive and sum to 1 (like probabilities)
    eigenvalues = np.maximum(eigenvalues, 0)
    eigenvalues = eigenvalues / (np.sum(eigenvalues) + 1e-10)
    
    # Von Neumann entropy formula (quantum-inspired)
    entropy = -np.sum(eigenvalues * np.log2(eigenvalues + 1e-10))
    
    return float(entropy)

def prediction_accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calculate accuracy of predictions for classification or regression.
    
    Automatically handles both classification and regression tasks.
    
    Args:
        y_true: True values
        y_pred: Predicted values
        
    Returns:
        Accuracy value (0 to 1, higher is better)
    """
    # Check if this is a classification problem
    if np.all(np.mod(y_true, 1) == 0) and np.all((y_true == 0) | (y_true == 1)):
        # For binary classification
        y_pred_binary = (y_pred > 0.5).astype(int)
        return float(accuracy_score(y_true, y_pred_binary))
    else:
        # For regression, use R^2 score
        r2 = r2_score(y_true, y_pred)
        
        # Convert to 0-1 range (R^2 can be negative for poor models)
        accuracy = max(0, r2)
        accuracy = min(1, accuracy)  # Cap at 1
        
        return float(accuracy)

def quantum_advantage_factor(y_true: np.ndarray, y_pred: np.ndarray, 
                           classical_pred: Optional[np.ndarray] = None,
                           alpha: float = 0.5) -> float:
    """
    Calculate the quantum advantage factor over classical methods.
    
    This metric compares quantum-inspired predictions with classical baselines,
    and also considers the quantum coherence in the predictions.
    
    Args:
        y_true: True values
        y_pred: Quantum model predictions
        classical_pred: Classical model predictions (if available)
        alpha: Weighting factor for combining metrics (0 to 1)
        
    Returns:
        Advantage factor (above 1 indicates quantum advantage)
    """
    # Quantum fidelity of the predictions
    q_fidelity = quantum_fidelity(y_true, y_pred)
    
    if classical_pred is not None:
        # Compare with classical predictions
        classical_mse = mean_squared_error(y_true, classical_pred)
        quantum_mse = mean_squared_error(y_true, y_pred)
        
        # Compute improvement ratio (> 1 means quantum is better)
        # Avoid division by zero
        if quantum_mse == 0:
            improvement_ratio = 2.0  # Cap at 2x improvement
        elif classical_mse == 0:
            improvement_ratio = 0.5  # Worse than perfect classical
        else:
            improvement_ratio = min(classical_mse / quantum_mse, 2.0)  # Cap at 2x improvement
    else:
        # No classical baseline, use a default value
        improvement_ratio = 1.0
    
    # Compute coherence in predictions
    if np.iscomplexobj(y_pred):
        # For complex predictions, use phase coherence
        phases = np.angle(y_pred)
        phase_diff = np.diff(phases, axis=0)
        coherence = np.abs(np.mean(np.exp(1j * phase_diff)))
    else:
        # For real predictions, use correlation between adjacent predictions
        if y_pred.ndim == 1 and len(y_pred) > 1:
            coherence = np.abs(np.corrcoef(y_pred[:-1], y_pred[1:])[0, 1])
        else:
            coherence = 0.5  # Default value
    
    # Combine metrics into advantage factor
    advantage = alpha * improvement_ratio + (1 - alpha) * (q_fidelity + coherence) / 2
    
    return float(advantage)

def divergence_prediction_score(y_true: np.ndarray, y_pred: np.ndarray, 
                              threshold: float = 0.05) -> Dict[str, float]:
    """
    Specialized score for market divergence prediction.
    
    This metric evaluates how well the model predicts significant divergences
    between AIXBT and BTC price movements.
    
    Args:
        y_true: True divergence values
        y_pred: Predicted divergence values
        threshold: Threshold for significant divergence (e.g., 5%)
        
    Returns:
        Dictionary with multiple divergence prediction metrics
    """
    # Identify significant divergences in true data
    significant_true = np.abs(y_true) > threshold
    
    # Identify predicted significant divergences
    significant_pred = np.abs(y_pred) > threshold
    
    # Calculate directional accuracy
    correct_direction = np.sign(y_true) == np.sign(y_pred)
    
    # Calculate metrics
    total_samples = len(y_true)
    true_positives = np.sum(significant_true & significant_pred & correct_direction)
    true_negatives = np.sum(~significant_true & ~significant_pred)
    false_positives = np.sum(~significant_true & significant_pred)
    false_negatives = np.sum(significant_true & ~significant_pred)
    
    # Avoid division by zero
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    specificity = true_negatives / (true_negatives + false_positives) if (true_negatives + false_positives) > 0 else 0
    
    # Calculate F1 score
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    # Calculate directional accuracy for significant divergences
    dir_accuracy = np.sum(correct_direction & significant_true) / np.sum(significant_true) if np.sum(significant_true) > 0 else 0
    
    # Calculate overall accuracy
    accuracy = (true_positives + true_negatives) / total_samples
    
    return {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "specificity": float(specificity),
        "f1_score": float(f1),
        "directional_accuracy": float(dir_accuracy)
    }

def quantum_ensemble_confidence(ensemble_preds: np.ndarray) -> Dict[str, float]:
    """
    Calculate confidence metrics for quantum ensemble predictions.
    
    Quantum ensembles can represent uncertainty through interference patterns.
    This metric evaluates the confidence of ensemble predictions.
    
    Args:
        ensemble_preds: Array of predictions from ensemble members (shape: n_members, n_samples, ...)
        
    Returns:
        Dictionary with confidence metrics
    """
    # Calculate mean and standard deviation across ensemble
    mean_pred = np.mean(ensemble_preds, axis=0)
    std_pred = np.std(ensemble_preds, axis=0)
    
    # Calculate coefficient of variation (normalized uncertainty)
    # Avoid division by zero
    cv = np.mean(std_pred / (np.abs(mean_pred) + 1e-10))
    
    # Calculate ensemble coherence (agreement between members)
    # Higher is better
    coherence = 1.0 / (1.0 + cv)
    
    # Calculate phase agreement for complex predictions
    if np.iscomplexobj(ensemble_preds):
        # Extract phases
        phases = np.angle(ensemble_preds)
        
        # Calculate circular standard deviation of phases
        # Lower means more agreement
        phase_diff = np.std(np.exp(1j * phases), axis=0)
        phase_agreement = 1.0 - np.mean(np.abs(phase_diff))
    else:
        phase_agreement = 1.0
    
    return {
        "ensemble_coherence": float(coherence),
        "coefficient_of_variation": float(cv),
        "phase_agreement": float(phase_agreement),
        "confidence_score": float((coherence + phase_agreement) / 2)
    } 