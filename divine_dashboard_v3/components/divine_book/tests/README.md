# Divine Book Tests

This directory contains tests for the Divine Book components, with special focus on testing the fix for the `HighlightRenderer.block_code()` error.

## Overview

The tests cover:

1. **Unit Tests for HighlightRenderer** - Testing the `block_code()` method with different parameter combinations including the `info` parameter that caused the original error.

2. **Integration Tests for Markdown Parsing** - Testing the full markdown parsing pipeline with various code block formats that would trigger the `info` parameter.

## Running the Tests

To run all tests, use the provided test runner script:

```bash
python run_tests.py
```

To run individual test files:

```bash
python test_highlight_renderer.py
python test_markdown_parsing.py
```

## Test Cases for the `info` Parameter Error

The test cases specifically verify that the `block_code()` method properly handles:

1. Code blocks without language specification
2. Code blocks with language but no info
3. Code blocks with both language and info
4. Code blocks with complex info strings containing multiple parameters
5. Code blocks with various separator formats (colons, braces, etc.)

Each of these cases tests a different scenario that could potentially trigger the error: "HighlightRenderer.block_code() got an unexpected keyword argument 'info'".

## Dependencies

The tests require:

- mistune
- pygments
- rich (for some tests)

However, the test runner is designed to gracefully handle missing dependencies and will skip relevant tests if needed.

## Troubleshooting

If you encounter issues:

1. Make sure all dependencies are installed:

   ```bash
   pip install -r ../requirements.txt
   ```

2. Check that the HighlightRenderer class in `common/repository_utils.py` has the following method signature:

   ```python
   def block_code(self, code, lang=None, info=None):
   ```

3. Verify that the test directory is in the Python path:

   ```python
   import sys
   sys.path.insert(0, '../')
