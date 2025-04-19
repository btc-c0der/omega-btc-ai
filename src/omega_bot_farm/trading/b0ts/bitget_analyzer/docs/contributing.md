
✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This code is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."

By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸


# Contributing to BitGet Position Analyzer Bot

Thank you for your interest in contributing to the BitGet Position Analyzer Bot! This document provides guidelines and instructions for contributors.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Code Standards](#code-standards)
5. [Testing Guidelines](#testing-guidelines)
6. [Documentation](#documentation)
7. [Pull Request Process](#pull-request-process)
8. [Feature Requests](#feature-requests)
9. [Bug Reports](#bug-reports)
10. [Community](#community)

## Code of Conduct

Our community is dedicated to providing a harassment-free experience for everyone. We do not tolerate harassment of participants in any form. Please be respectful of others and follow these guidelines:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A BitGet account (for testing, though mock options are available)
- Redis (optional, for advanced features)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

   ```bash
   git clone https://github.com/YOUR-USERNAME/omega-btc-ai.git
   cd omega-btc-ai
   ```

3. Add the upstream repository as a remote:

   ```bash
   git remote add upstream https://github.com/ORIGINAL-OWNER/omega-btc-ai.git
   ```

4. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

### Project Structure

Here's an overview of the project structure:

```
src/omega_bot_farm/trading/b0ts/bitget_analyzer/
├── __init__.py
├── analyzer.py            # Main analyzer class
├── config/                # Configuration files
├── docs/                  # Documentation
├── core/
│   ├── __init__.py
│   ├── fibonacci.py       # Fibonacci analysis implementation
│   ├── harmony.py         # Harmony calculation implementation
│   └── position.py        # Position data structures
├── services/
│   ├── __init__.py
│   ├── api_client.py      # BitGet API client
│   └── redis_service.py   # Redis integration
├── utils/
│   ├── __init__.py
│   ├── logging.py         # Logging utilities
│   └── helpers.py         # Helper functions
└── tests/                 # Test suite
    ├── __init__.py
    ├── unit/
    ├── integration/
    └── performance/
```

## Development Workflow

### Branching Strategy

We use a simplified Git flow approach:

- `main` - Stable production code
- `develop` - Integration branch for new features
- Feature branches - Named as `feature/short-description`
- Bug fix branches - Named as `fix/issue-description`

### Creating a Branch

Create a branch from `develop` for your work:

```bash
git checkout develop
git pull upstream develop
git checkout -b feature/your-feature-name
```

### Keeping Your Branch Updated

Regularly update your branch with changes from `develop`:

```bash
git checkout develop
git pull upstream develop
git checkout feature/your-feature-name
git merge develop
```

## Code Standards

### Python Style Guide

We follow PEP 8 with some project-specific guidelines:

- Line length: 100 characters maximum
- Use 4 spaces for indentation
- Use docstrings for all public classes and functions
- Import order: standard library, third-party, local application

### Type Annotations

Use type annotations for all function parameters and return values:

```python
def calculate_fibonacci_ratio(high_price: float, low_price: float) -> dict[str, float]:
    """
    Calculate Fibonacci ratios based on price range.
    
    Args:
        high_price: The highest price in the range
        low_price: The lowest price in the range
        
    Returns:
        Dictionary of Fibonacci levels and their corresponding prices
    """
    # Implementation
```

### Linting and Formatting

We use the following tools:

- `flake8` for linting
- `black` for code formatting
- `isort` for sorting imports
- `mypy` for type checking

Run the checks before submitting a PR:

```bash
# Format code
black src/omega_bot_farm/trading/b0ts/bitget_analyzer
isort src/omega_bot_farm/trading/b0ts/bitget_analyzer

# Lint
flake8 src/omega_bot_farm/trading/b0ts/bitget_analyzer

# Type check
mypy src/omega_bot_farm/trading/b0ts/bitget_analyzer
```

## Testing Guidelines

### Test Coverage

We aim for high test coverage. All new code should include appropriate tests:

- Unit tests for individual functions and classes
- Integration tests for API endpoints and service interactions
- Performance tests for measuring efficiency and responsiveness

### Test Structure

Follow these principles for tests:

- Use descriptive test names that explain the behavior being tested
- Organize tests by module and functionality
- Use parameterized tests for testing multiple cases
- Mock external dependencies (API calls, Redis, etc.)

### Running Tests

```bash
# Run all tests
pytest src/omega_bot_farm/trading/b0ts/bitget_analyzer/tests/

# Run specific test modules
pytest src/omega_bot_farm/trading/b0ts/bitget_analyzer/tests/unit/test_fibonacci.py

# Run with coverage report
pytest --cov=src/omega_bot_farm/trading/b0ts/bitget_analyzer tests/
```

### Test Environment

Set up a test environment in `.env.test` with mock credentials:

```
BITGET_API_KEY=test_key
BITGET_SECRET_KEY=test_secret
BITGET_PASSPHRASE=test_passphrase
USE_TESTNET=True
```

## Documentation

### Code Documentation

- All public classes, methods, and functions should have docstrings
- Follow Google-style docstring format
- Include examples where appropriate

### Project Documentation

When adding new features, update the relevant documentation:

- `README.md` for overall project description
- API reference for new methods
- Configuration guide for new configuration options
- User guides for new functionality

### Documentation Generation

We use Sphinx to generate documentation from docstrings:

```bash
cd docs
make html
```

## Pull Request Process

1. **Prepare Your Changes**
   - Make sure tests pass
   - Update documentation as needed
   - Add yourself to CONTRIBUTORS.md if not already there

2. **Create a Pull Request**
   - Submit a PR from your feature branch to the `develop` branch
   - Fill out the PR template completely
   - Link any related issues

3. **Code Review**
   - Maintainers will review your code
   - Address all comments and requested changes
   - Maintain a polite and collaborative attitude

4. **Merge**
   - Once approved, a maintainer will merge your PR
   - PRs are squashed and merged to keep a clean history

## Feature Requests

To request a new feature:

1. Check existing issues and discussions to avoid duplicates
2. Open a new issue using the Feature Request template
3. Clearly describe the feature and the problem it solves
4. Provide examples of how the feature would be used

## Bug Reports

When reporting bugs:

1. Check existing issues to avoid duplicates
2. Use the Bug Report template
3. Include detailed steps to reproduce
4. Provide environment information:
   - Python version
   - OS
   - Package versions
5. Include logs, screenshots, or error messages

## Community

### Communication Channels

- GitHub Discussions: For questions, ideas, and community discussion
- Issue Tracker: For bugs and feature requests
- Development Chat: Join our Discord server for real-time discussion

### Mentoring

New contributors can request mentoring by:

1. Commenting on issues tagged with "good first issue"
2. Asking questions in the discussion forums
3. Reaching out to project maintainers directly

### Recognition

We recognize contributions in several ways:

- Adding you to CONTRIBUTORS.md
- Acknowledging contributions in release notes
- Promoting regular contributors to maintainers

## Development Best Practices

### Asyncio Guidelines

Since the bot uses asyncio for concurrency:

- Never use blocking calls in async functions
- Use `asyncio.gather` for parallel execution
- Always provide timeout parameters for API calls
- Handle cancellation properly

Example:

```python
async def get_multiple_positions(symbols: list[str]) -> dict:
    """Get positions for multiple symbols concurrently."""
    tasks = [self.get_position(symbol) for symbol in symbols]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results, handling any exceptions
    processed_results = {}
    for symbol, result in zip(symbols, results):
        if isinstance(result, Exception):
            logger.error(f"Error getting position for {symbol}: {result}")
            continue
        processed_results[symbol] = result
    
    return processed_results
```

### Error Handling

Follow these practices for error handling:

- Use specific exception types rather than catching all exceptions
- Log errors with appropriate context
- Provide meaningful error messages
- Handle API errors gracefully

### Resource Management

For proper resource management:

- Use context managers (`async with`) for resources
- Close connections properly in cleanup code
- Implement proper timeouts for external service calls
- Use connection pooling where appropriate

## Adding New Analysis Methods

When adding new technical analysis methods:

1. Create a new module in the `core` package
2. Implement the analysis logic with proper documentation
3. Add unit tests that verify the calculations
4. Update the main analyzer class to expose the new functionality
5. Update API documentation and user guides

Example structure for a new analysis method:

```
core/
└── rsi_analysis.py      # New module for RSI analysis

tests/unit/
└── test_rsi_analysis.py # Tests for the new module

docs/
└── rsi_analysis.md      # Documentation for RSI analysis
```

## Versioning and Releases

We follow semantic versioning:

- **Major** version for incompatible API changes
- **Minor** version for new functionality in a backward-compatible manner
- **Patch** version for backward-compatible bug fixes

Contributors should note in PR descriptions if their changes are:

- Breaking changes (major)
- New features (minor)
- Bug fixes (patch)

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.
