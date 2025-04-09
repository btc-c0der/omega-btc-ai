# OMEGA Pro Surfer Quickstart Guide

## Environment Setup

1. Ensure your shell is configured with:

   ```bash
   source "~/.omega_quantum_toolkit/quantum_shell_config.sh"
   ```

2. Verify installation with:

   ```bash
   quantum-celebration --cycles 1
   ```

## Core Commands

### Quantum Celebration

Visualize quantum market states:

```bash
quantum-celebration --cycles 5 --interval 0.5
```

### Git Grid

Enhanced git visualization:

```bash
git grid
```

### Quantum Moonet

Advanced neural network visualization:

```bash
quantum-moonet --market BTC/USDT
```

## Trading Strategy Integration

1. Import the OMEGA modules in your strategy:

   ```python
   from omega_bot_farm.ai_model_aixbt.quantum_neural_net import QuantumCelebration
   ```

2. Initialize the quantum predictor:

   ```python
   predictor = QuantumCelebration()
   results = predictor.celebrate(market_data, cycles=3)
   ```

3. Use the quantum insights in your decision logic.

## Getting Help

Run any command with `--help` for detailed usage information:

```bash
quantum-celebration --help
```

Join our community channels for advanced tips and support.
