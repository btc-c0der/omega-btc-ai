# Divine Book Components Test Suite

This directory contains test cases for the Divine Book components, including quantum-enhanced text analysis, resonance detection, and the web dashboard interfaces.

## Overview

The test suite covers the following modules:

1. **Quantum Indexer**: Tests for document indexing and quantum-enhanced search functionality
2. **Divine Book Dashboard**: Tests for the dashboard interface and text analysis visualization
3. **Divine Book Browser**: Tests for the browser interface and sacred text exploration

## Running Tests

### Setting Up the Environment

Before running the tests, you need to set up a virtual environment and install the required dependencies:

```bash
# Create a virtual environment
python3 -m venv divine_venv

# Activate the virtual environment
source divine_venv/bin/activate  # On Unix/MacOS
# or
divine_venv\Scripts\activate      # On Windows

# Install dependencies
pip install -r requirements-test.txt
```

### Running All Tests

To run all test cases at once:

```bash
python run_tests.py
```

### Running Specific Tests

To run a specific test file:

```bash
python run_tests.py test_divine_book_browser.py
```

Or run a test file directly:

```bash
python micro_modules/test_quantum_indexer.py
```

## Test Structure

### Quantum Indexer Tests

The quantum indexer tests verify the following functionality:

- Adding documents to the index
- Text tokenization and processing
- Exact match search functionality
- Quantum entanglement effects in search
- Result ranking by relevance

### Divine Book Dashboard Tests

These tests verify the functionality of the dashboard interface:

- Loading of sample sacred texts
- Text analysis with various parameters
- Interpretation of resonance scores
- Generation of visualization charts

### Divine Book Browser Tests

These tests check the browser interface functionality:

- Sample text availability
- Dashboard creation
- Text analysis with quantum parameters
- Resonance interpretation
- Chart creation

## Test Mocking Strategy

The tests use a mocking strategy to avoid actually creating and displaying the Gradio UI components during testing:

1. Dashboard components are mocked using `unittest.mock`
2. Chart visualization using matplotlib is configured to not display during tests
3. Functions with side effects are properly isolated

## Adding New Tests

When adding new tests, follow these guidelines:

1. Place test files in the same directory as the module they test
2. Use the naming convention `test_*.py` for all test files
3. Use the `unittest` framework for consistency
4. Mock external dependencies as needed
