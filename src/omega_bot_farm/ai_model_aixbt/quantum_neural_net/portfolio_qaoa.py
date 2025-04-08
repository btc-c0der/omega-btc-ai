#!/usr/bin/env python3
"""
Quantum Approximate Optimization Algorithm (QAOA)
================================================

Specialized implementation of QAOA for portfolio optimization problems.
This module provides a quantum-inspired approach to solving portfolio
construction and trade execution challenges.

⚡️ GBU2™ License - Genesis-Bloom-Unfoldment 2.0 ⚡️
"""

import os
import numpy as np
import logging
import time
import math
from typing import Dict, List, Any, Optional, Union, Tuple, Callable
from scipy.optimize import minimize
import random
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("quantum-portfolio-qaoa")

# Constants
LOG_PREFIX = "🧠 vQuB1T-NN QAOA"
PHI = 1.618033988749895  # Golden ratio
DIVINE_PI = 3.1415926535897932384626433832795  # π

class PortfolioQAOA:
    """
    Quantum Approximate Optimization Algorithm for portfolio optimization.
    
    QAOA uses quantum principles to solve combinatorial optimization problems
    like portfolio construction, implementing a quantum-classical hybrid approach.
    """
    
    def __init__(self, 
                p_value: int = 3, 
                iterations: int = 100,
                max_weight: float = 0.25,
                risk_tolerance: float = 0.5):
        """
        Initialize the QAOA solver.
        
        Args:
            p_value: QAOA circuit depth
            iterations: Number of optimization iterations
            max_weight: Maximum asset weight constraint
            risk_tolerance: Risk tolerance parameter (0-1)
        """
        self.p = p_value
        self.iterations = iterations
        self.max_weight = max_weight
        self.risk_tolerance = risk_tolerance
        self.best_solution = None
        self.optimization_results = {}
        self.execution_time = 0
        
        logger.info(f"{LOG_PREFIX} - QAOA initialized with p={p_value}, iterations={iterations}")
    
    def _compute_cost_hamiltonian(self, 
                               expected_returns: np.ndarray, 
                               covariance: np.ndarray,
                               weights: np.ndarray) -> float:
        """
        Compute cost Hamiltonian for portfolio optimization.
        
        In QAOA, this represents the problem Hamiltonian that encodes
        the optimization objective.
        
        Args:
            expected_returns: Expected returns vector
            covariance: Covariance matrix
            weights: Portfolio weights
            
        Returns:
            Energy value of the cost Hamiltonian
        """
        # Calculate return component
        return_term = -np.sum(expected_returns * weights)
        
        # Calculate risk component
        risk_term = self.risk_tolerance * np.dot(weights.T, np.dot(covariance, weights))
        
        # Sum to get energy (negative because we're minimizing)
        energy = return_term + risk_term
        
        return energy
    
    def _mixing_operator(self,
                      weights: np.ndarray,
                      beta: float) -> np.ndarray:
        """
        Apply the mixing operator to weights.
        
        In QAOA, the mixing operator explores the solution space
        by creating superpositions of states.
        
        Args:
            weights: Current weights
            beta: Mixing angle
            
        Returns:
            Mixed weights
        """
        # Create quantum-inspired exploration
        # Instead of quantum rotation, we use a classical approximation
        mixed_weights = weights.copy()
        
        # Apply mixing operation: explore nearby states
        noise = np.random.normal(0, beta, size=weights.shape)
        mixed_weights += noise
        
        # Ensure constraints are satisfied
        mixed_weights = np.maximum(0, np.minimum(self.max_weight, mixed_weights))
        
        # Normalize weights to sum to 1
        if np.sum(mixed_weights) > 0:
            mixed_weights = mixed_weights / np.sum(mixed_weights)
        else:
            # In case all weights become zero, reset to equal weights
            mixed_weights = np.ones_like(weights) / len(weights)
        
        return mixed_weights
    
    def _phase_operator(self,
                     weights: np.ndarray,
                     gamma: float,
                     expected_returns: np.ndarray,
                     covariance: np.ndarray) -> np.ndarray:
        """
        Apply the phase separation operator to weights.
        
        In QAOA, the phase operator encodes the problem structure
        by applying phases based on the cost function.
        
        Args:
            weights: Current weights
            gamma: Phase angle
            expected_returns: Expected returns
            covariance: Covariance matrix
            
        Returns:
            Updated weights after phase separation
        """
        # Calculate gradient approximation
        epsilon = 1e-6
        gradient = np.zeros_like(weights)
        
        for i in range(len(weights)):
            # Perturb weight slightly
            delta = np.zeros_like(weights)
            delta[i] = epsilon
            
            # Calculate numerical gradient
            cost_plus = self._compute_cost_hamiltonian(
                expected_returns, covariance, weights + delta
            )
            cost_minus = self._compute_cost_hamiltonian(
                expected_returns, covariance, weights - delta
            )
            gradient[i] = (cost_plus - cost_minus) / (2 * epsilon)
        
        # Apply phase operation: move in the direction of negative gradient
        # (This is analogous to phase kickback in quantum algorithms)
        updated_weights = weights - gamma * gradient
        
        # Ensure constraints are satisfied
        updated_weights = np.maximum(0, np.minimum(self.max_weight, updated_weights))
        
        # Normalize weights to sum to 1
        if np.sum(updated_weights) > 0:
            updated_weights = updated_weights / np.sum(updated_weights)
        else:
            updated_weights = np.ones_like(weights) / len(weights)
        
        return updated_weights
    
    def optimize(self,
              expected_returns: np.ndarray,
              covariance: np.ndarray,
              initial_weights: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        Run QAOA optimization for portfolio weights.
        
        Args:
            expected_returns: Expected asset returns
            covariance: Covariance matrix of returns
            initial_weights: Initial weight allocation (optional)
            
        Returns:
            Optimization results
        """
        start_time = time.time()
        
        # Ensure inputs are numpy arrays
        expected_returns = np.asarray(expected_returns)
        covariance = np.asarray(covariance)
        
        # Number of assets
        n_assets = len(expected_returns)
        
        # Set initial weights if not provided
        if initial_weights is None:
            initial_weights = np.ones(n_assets) / n_assets
        else:
            # Normalize weights to sum to 1
            initial_weights = np.asarray(initial_weights)
            if np.sum(initial_weights) > 0:
                initial_weights = initial_weights / np.sum(initial_weights)
            else:
                initial_weights = np.ones(n_assets) / n_assets
        
        # Initialize parameters for QAOA
        # Use linearly spaced angles for initial parameters
        betas = np.linspace(0.1, 0.8, self.p)  # Mixing angles
        gammas = np.linspace(0.1, 0.5, self.p)  # Phase separation angles
        
        # Track best solution
        best_weights = initial_weights.copy()
        best_energy = self._compute_cost_hamiltonian(
            expected_returns, covariance, best_weights
        )
        
        # Store all candidate solutions for analysis
        all_candidates = []
        
        # Run QAOA iterations
        for iteration in range(self.iterations):
            # Start with equal weights for each iteration
            weights = initial_weights.copy()
            
            # Apply p layers of QAOA
            for layer in range(self.p):
                # Apply phase separation operator (problem-dependent)
                weights = self._phase_operator(
                    weights, gammas[layer], expected_returns, covariance
                )
                
                # Apply mixing operator (problem-independent)
                weights = self._mixing_operator(weights, betas[layer])
            
            # Evaluate energy of final state
            energy = self._compute_cost_hamiltonian(
                expected_returns, covariance, weights
            )
            
            # Store candidate solution
            all_candidates.append({
                "weights": weights.copy(),
                "energy": energy,
                "iteration": iteration
            })
            
            # Update best solution
            if energy < best_energy:
                best_energy = energy
                best_weights = weights.copy()
                
                logger.info(f"{LOG_PREFIX} - New best solution found at iteration {iteration}, energy: {energy:.6f}")
            
            # Update QAOA parameters based on current performance
            # This mimics the quantum variational approach
            if iteration % 10 == 0 and iteration > 0:
                # Find best angles from recent iterations
                recent_candidates = all_candidates[-10:]
                best_recent = min(recent_candidates, key=lambda x: x["energy"])
                
                # Slightly adjust angles with some randomness for exploration
                betas = betas * (0.95 + 0.1 * np.random.random(self.p))
                gammas = gammas * (0.95 + 0.1 * np.random.random(self.p))
        
        # Calculate portfolio statistics
        portfolio_return = np.sum(expected_returns * best_weights)
        portfolio_variance = np.dot(best_weights.T, np.dot(covariance, best_weights))
        portfolio_volatility = np.sqrt(portfolio_variance)
        sharpe_ratio = portfolio_return / portfolio_volatility if portfolio_volatility > 0 else float('inf')
        
        # Calculate execution time
        execution_time = time.time() - start_time
        self.execution_time = execution_time
        
        # Store results
        self.best_solution = best_weights
        self.optimization_results = {
            "weights": best_weights.tolist(),
            "expected_return": float(portfolio_return),
            "volatility": float(portfolio_volatility),
            "sharpe_ratio": float(sharpe_ratio),
            "energy": float(best_energy),
            "p_value": self.p,
            "iterations": self.iterations,
            "execution_time": execution_time,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"{LOG_PREFIX} - QAOA optimization complete. Execution time: {execution_time:.4f}s, "
                 f"Final energy: {best_energy:.6f}, Sharpe ratio: {sharpe_ratio:.4f}")
        
        return self.optimization_results
    
    def compare_with_classical(self,
                            expected_returns: np.ndarray,
                            covariance: np.ndarray) -> Dict[str, Any]:
        """
        Compare QAOA results with classical optimization.
        
        Args:
            expected_returns: Expected asset returns
            covariance: Covariance matrix
            
        Returns:
            Comparison results
        """
        # Run QAOA if not already done
        if self.best_solution is None:
            self.optimize(expected_returns, covariance)
        
        # Define classical objective function
        def objective(weights):
            weights = np.asarray(weights)
            portfolio_return = np.sum(expected_returns * weights)
            portfolio_variance = np.dot(weights.T, np.dot(covariance, weights))
            
            # Combine return and risk based on risk tolerance
            return -portfolio_return + self.risk_tolerance * portfolio_variance
        
        # Constraints: weights sum to 1
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        
        # Bounds: weight of each asset between 0 and max_weight
        n_assets = len(expected_returns)
        bounds = tuple((0, self.max_weight) for _ in range(n_assets))
        
        # Initial weights (equal weighting)
        initial_weights = np.ones(n_assets) / n_assets
        
        # Run classical optimization
        start_time = time.time()
        result = minimize(
            objective, 
            initial_weights, 
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        classical_time = time.time() - start_time
        
        # Calculate classical portfolio statistics
        classical_weights = result.x
        portfolio_return = np.sum(expected_returns * classical_weights)
        portfolio_variance = np.dot(classical_weights.T, np.dot(covariance, classical_weights))
        portfolio_volatility = np.sqrt(portfolio_variance)
        sharpe_ratio = portfolio_return / portfolio_volatility if portfolio_volatility > 0 else float('inf')
        
        # Comparison results
        comparison = {
            "qaoa": {
                "weights": self.best_solution.tolist(),
                "expected_return": float(np.sum(expected_returns * self.best_solution)),
                "volatility": float(np.sqrt(np.dot(self.best_solution.T, np.dot(covariance, self.best_solution)))),
                "sharpe_ratio": float(self.optimization_results.get("sharpe_ratio", 0)),
                "execution_time": self.execution_time
            },
            "classical": {
                "weights": classical_weights.tolist(),
                "expected_return": float(portfolio_return),
                "volatility": float(portfolio_volatility),
                "sharpe_ratio": float(sharpe_ratio),
                "execution_time": classical_time
            }
        }
        
        # Calculate improvement metrics
        sharpe_improvement = (comparison["qaoa"]["sharpe_ratio"] / comparison["classical"]["sharpe_ratio"] - 1) * 100 if comparison["classical"]["sharpe_ratio"] > 0 else 0
        
        comparison["improvement"] = {
            "sharpe_ratio_pct": float(sharpe_improvement),
            "speed_ratio": float(classical_time / self.execution_time) if self.execution_time > 0 else float('inf')
        }
        
        logger.info(f"{LOG_PREFIX} - QAOA vs Classical: Sharpe improvement: {sharpe_improvement:.2f}%, "
                 f"Speed ratio: {comparison['improvement']['speed_ratio']:.2f}x")
        
        return comparison


# Demo function
def run_demo():
    """Run a simple demo of the Portfolio QAOA."""
    # Generate random test data
    np.random.seed(42)
    n_assets = 5
    
    # Create correlated returns and covariance
    expected_returns = np.random.normal(0.001, 0.0005, n_assets)  # Daily returns
    
    # Create a valid covariance matrix (must be positive semi-definite)
    A = np.random.normal(0, 0.01, (n_assets, n_assets))
    covariance = np.dot(A, A.T) / 100  # Scale down to reasonable values
    
    # Initialize QAOA solver
    qaoa = PortfolioQAOA(p_value=2, iterations=50, risk_tolerance=0.5)
    
    # Run optimization
    results = qaoa.optimize(expected_returns, covariance)
    
    # Compare with classical optimization
    comparison = qaoa.compare_with_classical(expected_returns, covariance)
    
    return comparison


if __name__ == "__main__":
    # Run the demo and print results
    comparison = run_demo()
    
    print("\n===== QAOA Portfolio Optimization Results =====")
    print(f"QAOA Sharpe Ratio: {comparison['qaoa']['sharpe_ratio']:.4f}")
    print(f"QAOA Expected Return: {comparison['qaoa']['expected_return']*252:.4%} (annual)")
    print(f"QAOA Volatility: {comparison['qaoa']['volatility']*math.sqrt(252):.4%} (annual)")
    print(f"QAOA Execution Time: {comparison['qaoa']['execution_time']:.4f}s")
    
    print("\n===== Classical Optimization Results =====")
    print(f"Classical Sharpe Ratio: {comparison['classical']['sharpe_ratio']:.4f}")
    print(f"Classical Expected Return: {comparison['classical']['expected_return']*252:.4%} (annual)")
    print(f"Classical Volatility: {comparison['classical']['volatility']*math.sqrt(252):.4%} (annual)")
    print(f"Classical Execution Time: {comparison['classical']['execution_time']:.4f}s")
    
    print("\n===== Improvement Metrics =====")
    print(f"Sharpe Ratio Improvement: {comparison['improvement']['sharpe_ratio_pct']:.2f}%")
    print(f"Speed Ratio (Classical/QAOA): {comparison['improvement']['speed_ratio']:.2f}x")
    
    print("\n===== Optimal Portfolio Weights =====")
    for i, weight in enumerate(comparison['qaoa']['weights']):
        print(f"Asset {i+1}: {weight:.4f}") 