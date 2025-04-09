#!/usr/bin/env python3
"""
Stochastic Models using Quantum RNG
=================================

This module implements stochastic models for financial time series
that leverage quantum random number generation for improved accuracy.
"""

import numpy as np
import pandas as pd
import logging
from typing import List, Dict, Union, Optional, Any, Tuple, Callable
from dataclasses import dataclass
from enum import Enum
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from .quantum_rng import QuantumRNG

logger = logging.getLogger("quantum-rng")

class ModelType(Enum):
    """Enum representing different stochastic model types."""
    
    GEOMETRIC_BROWNIAN_MOTION = "gbm"
    HESTON = "heston"
    JUMP_DIFFUSION = "jump_diffusion"
    ORNSTEIN_UHLENBECK = "ornstein_uhlenbeck"
    REGIME_SWITCHING = "regime_switching"


@dataclass
class ModelParameters:
    """Base class for stochastic model parameters."""
    
    def __init__(
        self,
        initial_price: float = 100.0,
        mu: float = 0.05,
        sigma: float = 0.2,
        dt: float = 1/252,
        num_steps: int = 252,
        num_paths: int = 100
    ):
        """
        Initialize base model parameters.
        
        Args:
            initial_price: Initial price
            mu: Drift term
            sigma: Volatility
            dt: Time step size
            num_steps: Number of time steps
            num_paths: Number of simulation paths
        """
        self.initial_price = initial_price
        self.mu = mu
        self.sigma = sigma
        self.dt = dt
        self.num_steps = num_steps
        self.num_paths = num_paths


@dataclass
class GBMParameters(ModelParameters):
    """Parameters for Geometric Brownian Motion model."""
    
    mu: float = 0.05  # Drift (annualized)
    sigma: float = 0.20  # Volatility (annualized)
    initial_price: float = 100.0  # Initial price


@dataclass
class HestonModelParameters(ModelParameters):
    """Parameters for the Heston stochastic volatility model."""
    
    def __init__(
        self,
        initial_price: float = 100.0,
        mu: float = 0.05,
        sigma: float = 0.2,
        dt: float = 1/252,
        num_steps: int = 252,
        num_paths: int = 100,
        initial_variance: float = 0.04,
        kappa: float = 2.0,
        theta: float = 0.04,
        rho: float = -0.7
    ):
        """
        Initialize Heston model parameters.
        
        Args:
            initial_price: Initial price
            mu: Drift term
            sigma: Vol of vol parameter
            dt: Time step size
            num_steps: Number of time steps
            num_paths: Number of simulation paths
            initial_variance: Initial variance
            kappa: Mean reversion speed
            theta: Long-term variance
            rho: Correlation between price and variance
        """
        super().__init__(initial_price, mu, sigma, dt, num_steps, num_paths)
        self.initial_variance = initial_variance
        self.kappa = kappa
        self.theta = theta
        self.rho = rho


@dataclass
class JumpDiffusionParameters(ModelParameters):
    """Parameters for Merton Jump Diffusion model."""
    
    mu: float = 0.05  # Drift (annualized)
    sigma: float = 0.20  # Volatility (annualized)
    lambda_jump: float = 5.0  # Jump intensity (average number of jumps per year)
    mu_jump: float = -0.01  # Average jump size
    sigma_jump: float = 0.03  # Jump size volatility
    initial_price: float = 100.0  # Initial price


@dataclass
class OUModelParameters(ModelParameters):
    """Parameters for the Ornstein-Uhlenbeck mean-reverting model."""
    
    def __init__(
        self,
        initial_value: float = 0.0,
        mu: float = 0.0,
        sigma: float = 0.1,
        dt: float = 1/252,
        num_steps: int = 252,
        num_paths: int = 100,
        kappa: float = 1.0,
        theta: float = 0.0
    ):
        """
        Initialize Ornstein-Uhlenbeck model parameters.
        
        Args:
            initial_value: Initial value
            mu: Not used in this model
            sigma: Volatility
            dt: Time step size
            num_steps: Number of time steps
            num_paths: Number of simulation paths
            kappa: Mean reversion speed
            theta: Long-term mean level
        """
        super().__init__(initial_value, mu, sigma, dt, num_steps, num_paths)
        self.initial_value = initial_value  # Override initial_price
        self.kappa = kappa
        self.theta = theta


@dataclass
class RegimeSwitchingParameters(ModelParameters):
    """Parameters for Regime Switching model."""
    
    mu1: float = 0.10  # Drift in regime 1 (bull market)
    sigma1: float = 0.15  # Volatility in regime 1
    mu2: float = -0.05  # Drift in regime 2 (bear market)
    sigma2: float = 0.25  # Volatility in regime 2
    p12: float = 0.05  # Probability of switching from regime 1 to 2
    p21: float = 0.10  # Probability of switching from regime 2 to 1
    initial_price: float = 100.0  # Initial price
    initial_regime: int = 1  # Initial regime (1 or 2)


class StochasticModel:
    """Base class for stochastic models using quantum RNG."""
    
    def __init__(
        self,
        quantum_rng: Optional[QuantumRNG] = None,
        parameters: Optional[ModelParameters] = None
    ):
        """
        Initialize the stochastic model.
        
        Args:
            quantum_rng: Quantum random number generator
            parameters: Model parameters
        """
        self.quantum_rng = quantum_rng or QuantumRNG()
        self.parameters = parameters or ModelParameters()
        
        logger.info(f"Initialized {self.__class__.__name__} with quantum RNG")
    
    def simulate(self) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        """
        Simulate the stochastic process.
        
        Returns:
            Array of simulated paths or tuple of arrays
        """
        raise NotImplementedError("Subclasses must implement simulate()")
    
    def plot_paths(self, paths: Optional[Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]] = None, title: str = "", ax: Optional[Axes] = None) -> Axes:
        """
        Plot the simulated paths.
        
        Args:
            paths: Simulated paths (if None, will call simulate())
            title: Plot title
            ax: Matplotlib axes to plot on
            
        Returns:
            Matplotlib axes with plot
        """
        if paths is None:
            paths = self.simulate()
        
        if ax is None:
            _, ax = plt.subplots(figsize=(10, 6))
            
        # Check if paths is a tuple (for models that return multiple arrays)
        if isinstance(paths, tuple) and len(paths) > 0:
            # Just plot the first element (usually price paths)
            price_paths = paths[0]
            if price_paths is not None and price_paths.ndim == 2:
                time_steps = np.arange(price_paths.shape[1])
                for i in range(min(price_paths.shape[0], 10)):  # Plot up to 10 paths
                    ax.plot(time_steps, price_paths[i, :])
        else:
            # For single array output
            if paths is not None and paths.ndim == 2:
                time_steps = np.arange(paths.shape[1])
                for i in range(min(paths.shape[0], 10)):  # Plot up to 10 paths
                    ax.plot(time_steps, paths[i, :])
        
        ax.set_title(title or f"{self.__class__.__name__} Simulation")
        ax.set_xlabel("Time Steps")
        ax.set_ylabel("Price")
        ax.grid(True)
        
        return ax


class GeometricBrownianMotion(StochasticModel):
    """Geometric Brownian Motion model using quantum RNG."""
    
    def __init__(
        self,
        quantum_rng: Optional[QuantumRNG] = None,
        parameters: Optional[GBMParameters] = None
    ):
        """
        Initialize the GBM model.
        
        Args:
            quantum_rng: Quantum random number generator
            parameters: GBM parameters
        """
        super().__init__(quantum_rng, parameters or GBMParameters())
        
        # Ensure parameters have the right type
        if not isinstance(self.parameters, GBMParameters):
            raise TypeError("Parameters must be of type GBMParameters")
    
    def simulate(self) -> np.ndarray:
        """
        Simulate GBM paths.
        
        Returns:
            Array of shape (num_paths, num_steps+1) with simulated price paths
        """
        p = self.parameters
        
        # Initialize paths
        paths = np.zeros((p.num_paths, p.num_steps + 1))
        paths[:, 0] = p.initial_price
        
        # Generate random normal increments using quantum RNG
        for path_idx in range(p.num_paths):
            for step in range(p.num_steps):
                # Generate random normal increment
                z = self.quantum_rng.generate_random_normal()
                
                # Update price using GBM formula
                paths[path_idx, step + 1] = paths[path_idx, step] * np.exp(
                    (p.mu - 0.5 * p.sigma**2) * p.dt + p.sigma * np.sqrt(p.dt) * z
                )
        
        return paths


class HestonModel(StochasticModel):
    """Heston stochastic volatility model."""
    
    def __init__(
        self,
        quantum_rng: Optional[QuantumRNG] = None,
        parameters: Optional[HestonModelParameters] = None
    ):
        """
        Initialize the Heston model.
        
        Args:
            quantum_rng: Quantum random number generator
            parameters: Model parameters
        """
        if parameters is None:
            parameters = HestonModelParameters()
        self.quantum_rng = quantum_rng or QuantumRNG()
        self.parameters = parameters
        
        logger.info(f"Initialized {self.__class__.__name__} with quantum RNG")
        
        # Ensure parameters have the right type
        if not isinstance(self.parameters, HestonModelParameters):
            raise TypeError("Parameters must be of type HestonModelParameters")
    
    def simulate(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Simulate the Heston model.
        
        Returns:
            Tuple of (price_paths, variance_paths)
        """
        params = self.parameters
        S0 = params.initial_price
        v0 = params.initial_variance
        mu = params.mu
        kappa = params.kappa
        theta = params.theta
        sigma = params.sigma  # Vol of vol in this context
        rho = params.rho
        dt = params.dt
        num_steps = params.num_steps
        num_paths = params.num_paths
        
        # Initialize paths
        price_paths = np.zeros((num_paths, num_steps + 1))
        variance_paths = np.zeros((num_paths, num_steps + 1))
        
        price_paths[:, 0] = S0
        variance_paths[:, 0] = v0
        
        # Generate correlated random normal increments using quantum RNG
        for path_idx in range(num_paths):
            for step in range(num_steps):
                # Generate two uncorrelated random normal increments
                z1 = self.quantum_rng.generate_random_normal()
                z2 = self.quantum_rng.generate_random_normal()
                
                # Create correlated increments
                dw1 = z1
                dw2 = rho * z1 + np.sqrt(1 - rho**2) * z2
                
                # Current values
                S = price_paths[path_idx, step]
                v = max(0, variance_paths[path_idx, step])  # Ensure positive variance
                
                # Update variance (using full truncation scheme to handle potential negativity)
                v_new = v + kappa * (theta - v) * dt + sigma * np.sqrt(v * dt) * dw2
                variance_paths[path_idx, step + 1] = max(0, v_new)
                
                # Update price
                price_paths[path_idx, step + 1] = S * np.exp(
                    (mu - 0.5 * v) * dt + np.sqrt(v * dt) * dw1
                )
        
        return price_paths, variance_paths


class JumpDiffusionModel(StochasticModel):
    """Jump Diffusion model using quantum RNG."""
    
    def __init__(
        self,
        quantum_rng: Optional[QuantumRNG] = None,
        parameters: Optional[JumpDiffusionParameters] = None
    ):
        """
        Initialize the Jump Diffusion model.
        
        Args:
            quantum_rng: Quantum random number generator
            parameters: Jump Diffusion parameters
        """
        super().__init__(quantum_rng, parameters or JumpDiffusionParameters())
        
        # Ensure parameters have the right type
        if not isinstance(self.parameters, JumpDiffusionParameters):
            raise TypeError("Parameters must be of type JumpDiffusionParameters")
    
    def simulate(self) -> np.ndarray:
        """
        Simulate Jump Diffusion paths.
        
        Returns:
            Array of shape (num_paths, num_steps+1) with simulated price paths
        """
        # Use explicit cast to access specific parameters
        params = self.parameters
        if not isinstance(params, JumpDiffusionParameters):
            raise TypeError("Parameters must be of type JumpDiffusionParameters")
        
        # Initialize paths
        paths = np.zeros((params.num_paths, params.num_steps + 1))
        paths[:, 0] = params.initial_price
        
        # Generate random normal increments and jump events using quantum RNG
        for path_idx in range(params.num_paths):
            for step in range(params.num_steps):
                # Generate diffusion component (normal increment)
                z_diff = self.quantum_rng.generate_random_normal()
                
                # Generate jump component (Poisson process)
                lambda_dt = params.lambda_jump * params.dt
                jump_count = np.random.poisson(lambda_dt)
                
                # Generate jump sizes (if any)
                jump_size = 0.0
                if jump_count > 0:
                    for _ in range(jump_count):
                        z_jump = self.quantum_rng.generate_random_normal()
                        jump_size += params.mu_jump + params.sigma_jump * z_jump
                
                # Update price using Jump Diffusion formula
                paths[path_idx, step + 1] = paths[path_idx, step] * np.exp(
                    (params.mu - 0.5 * params.sigma**2) * params.dt + params.sigma * np.sqrt(params.dt) * z_diff + jump_size
                )
        
        return paths


class RegimeSwitchingModel(StochasticModel):
    """Regime Switching model using quantum RNG."""
    
    def __init__(
        self,
        quantum_rng: Optional[QuantumRNG] = None,
        parameters: Optional[RegimeSwitchingParameters] = None
    ):
        """
        Initialize the Regime Switching model.
        
        Args:
            quantum_rng: Quantum random number generator
            parameters: Regime Switching parameters
        """
        super().__init__(quantum_rng, parameters or RegimeSwitchingParameters())
        
        # Ensure parameters have the right type
        if not isinstance(self.parameters, RegimeSwitchingParameters):
            raise TypeError("Parameters must be of type RegimeSwitchingParameters")
    
    def simulate(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Simulate Regime Switching paths.
        
        Returns:
            Tuple of (price_paths, regime_paths) arrays
        """
        # Use explicit cast to access specific parameters
        params = self.parameters
        if not isinstance(params, RegimeSwitchingParameters):
            raise TypeError("Parameters must be of type RegimeSwitchingParameters")
        
        # Initialize paths
        price_paths = np.zeros((params.num_paths, params.num_steps + 1))
        regime_paths = np.zeros((params.num_paths, params.num_steps + 1), dtype=int)
        
        price_paths[:, 0] = params.initial_price
        regime_paths[:, 0] = params.initial_regime
        
        # Generate random increments using quantum RNG
        for path_idx in range(params.num_paths):
            for step in range(params.num_steps):
                # Current regime
                current_regime = regime_paths[path_idx, step]
                
                # Determine if regime switches
                switch_probability = params.p12 if current_regime == 1 else params.p21
                regime_switches = self.quantum_rng.generate_random_float() < switch_probability
                
                # Update regime
                if regime_switches:
                    new_regime = 2 if current_regime == 1 else 1
                else:
                    new_regime = current_regime
                
                regime_paths[path_idx, step + 1] = new_regime
                
                # Select parameters based on regime
                mu = params.mu1 if new_regime == 1 else params.mu2
                sigma = params.sigma1 if new_regime == 1 else params.sigma2
                
                # Generate random normal increment
                z = self.quantum_rng.generate_random_normal()
                
                # Update price using GBM with regime-specific parameters
                price_paths[path_idx, step + 1] = price_paths[path_idx, step] * np.exp(
                    (mu - 0.5 * sigma**2) * params.dt + sigma * np.sqrt(params.dt) * z
                )
        
        return price_paths, regime_paths


class OrnsteinUhlenbeckModel(StochasticModel):
    """Ornstein-Uhlenbeck mean-reverting model."""
    
    def __init__(
        self,
        quantum_rng: Optional[QuantumRNG] = None,
        parameters: Optional[OUModelParameters] = None
    ):
        """
        Initialize the Ornstein-Uhlenbeck model.
        
        Args:
            quantum_rng: Quantum random number generator
            parameters: Model parameters
        """
        if parameters is None:
            parameters = OUModelParameters()
        self.quantum_rng = quantum_rng or QuantumRNG()
        self.parameters = parameters
        
        logger.info(f"Initialized {self.__class__.__name__} with quantum RNG")
        
        # Ensure parameters have the right type
        if not isinstance(self.parameters, OUModelParameters):
            raise TypeError("Parameters must be of type OUModelParameters")
    
    def simulate(self) -> np.ndarray:
        """
        Simulate the Ornstein-Uhlenbeck process.
        
        Returns:
            Array of simulated paths
        """
        params = self.parameters
        X0 = params.initial_value
        kappa = params.kappa
        theta = params.theta
        sigma = params.sigma
        dt = params.dt
        num_steps = params.num_steps
        num_paths = params.num_paths
        
        # Initialize paths
        paths = np.zeros((num_paths, num_steps + 1))
        paths[:, 0] = X0
        
        # Generate random increments using quantum RNG
        for path_idx in range(num_paths):
            for step in range(num_steps):
                # Generate random normal increment
                z = self.quantum_rng.generate_random_normal()
                
                # Update value using OU formula
                paths[path_idx, step + 1] = paths[path_idx, step] + kappa * (theta - paths[path_idx, step]) * dt + sigma * np.sqrt(dt) * z
        
        return paths


class ModelFactory:
    """Factory for creating stochastic models."""
    
    @staticmethod
    def create(model_type: ModelType, parameters: ModelParameters, quantum_rng: Optional[QuantumRNG] = None) -> StochasticModel:
        """
        Factory method to create a stochastic model based on model type.

        Args:
            model_type: Type of model to create
            parameters: Model parameters appropriate for the selected model type
            quantum_rng: Optional quantum random number generator

        Returns:
            StochasticModel: The created stochastic model instance

        Raises:
            TypeError: If the parameters are not of the correct type for the model
            ValueError: If the model type is unknown
        """
        
        if model_type == ModelType.GEOMETRIC_BROWNIAN_MOTION:
            if not isinstance(parameters, GBMParameters):
                raise TypeError("Parameters must be of type GBMParameters for GBM model")
            return GeometricBrownianMotion(quantum_rng=quantum_rng, parameters=parameters)

        elif model_type == ModelType.HESTON:
            if not isinstance(parameters, HestonModelParameters):
                raise TypeError("Parameters must be of type HestonModelParameters for Heston model")
            return HestonModel(quantum_rng=quantum_rng, parameters=parameters)

        elif model_type == ModelType.JUMP_DIFFUSION:
            if not isinstance(parameters, JumpDiffusionParameters):
                raise TypeError("Parameters must be of type JumpDiffusionParameters for Jump Diffusion model")
            return JumpDiffusionModel(quantum_rng=quantum_rng, parameters=parameters)

        elif model_type == ModelType.ORNSTEIN_UHLENBECK:
            if not isinstance(parameters, OUModelParameters):
                raise TypeError("Parameters must be of type OUModelParameters for Ornstein-Uhlenbeck model")
            return OrnsteinUhlenbeckModel(quantum_rng=quantum_rng, parameters=parameters)

        elif model_type == ModelType.REGIME_SWITCHING:
            if not isinstance(parameters, RegimeSwitchingParameters):
                raise TypeError("Parameters must be of type RegimeSwitchingParameters for Regime Switching model")
            return RegimeSwitchingModel(quantum_rng=quantum_rng, parameters=parameters)

        else:
            raise ValueError(f"Unknown model type: {model_type}")


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Create quantum RNG
    qrng = QuantumRNG()
    
    # Create and simulate GBM
    gbm = GeometricBrownianMotion(qrng)
    gbm_paths = gbm.simulate()
    
    # Create and simulate Jump Diffusion
    jd = JumpDiffusionModel(qrng)
    jd_paths = jd.simulate()
    
    # Plot some paths
    gbm.plot_paths(gbm_paths)
    jd.plot_paths(jd_paths)