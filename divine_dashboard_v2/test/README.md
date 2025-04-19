# OMEGA Divine Book Browser v2.0 Test Suite

This directory contains a comprehensive test suite for the OMEGA Divine Book Browser v2.0, designed to achieve a minimum of 80% code coverage across the entire codebase.

## Test Suite Features

- **Unit Tests**: Testing individual functions and components in isolation
- **Integration Tests**: Testing interaction between components
- **Accessibility Tests**: Ensuring WCAG 2.1 AA compliance
- **Performance Tests**: Measuring and ensuring acceptable rendering times
- **Visual Regression Tests**: Using snapshots to detect unintended UI changes
- **Browser Compatibility Tests**: Ensuring cross-browser functionality

## Running the Tests

To run the test suite:

```bash
# Install dependencies
npm install

# Run tests with coverage report
npm test

# Run tests in watch mode during development
npm run test:watch

# Run tests with enforced 80% coverage threshold
npm run coverage
```

## Coverage Requirements

This test suite is configured to ensure a minimum of 80% code coverage across:

- Statements
- Branches
- Functions
- Lines

The coverage thresholds are configured in the `package.json` file:

```json
"coverageThreshold": {
  "global": {
    "statements": 80,
    "branches": 80,
    "functions": 80,
    "lines": 80
  }
}
```

## Coverage Report

After running the tests, a coverage report will be generated in multiple formats:

- **Text**: Displayed in the terminal
- **HTML**: Available in the `/coverage/lcov-report/index.html` file for detailed browsing
- **LCOV**: For integration with CI/CD systems

## Test Structure

- `test-suite.js`: Main test suite with all test cases
- `jest.setup.js`: Setup file for Jest configuration and global mocks
- `__mocks__/`: Directory containing mock files for non-JavaScript assets

## Continuous Integration

The test suite is integrated with our CI pipeline and will automatically run on pull requests and commits to the main branch. Tests must pass with the required coverage before merging is allowed.

## Contributing New Tests

When adding new features to the OMEGA Divine Book Browser, please also add appropriate tests to maintain our 80% coverage threshold. Follow these guidelines:

1. Write tests before implementing features (TDD approach)
2. Ensure all code paths are tested, including error conditions
3. Use the existing patterns and utilities in the test suite
4. Run `npm run test:watch` during development to get immediate feedback

## Troubleshooting

If tests are failing, check the following:

1. Ensure all dependencies are installed (`npm install`)
2. Verify that your DOM queries match the actual structure
3. Check that mocks are properly set up for external dependencies
4. Verify that event handlers are correctly attached

## Accessibility Testing

The test suite includes accessibility testing using axe-core. When adding new UI elements, ensure they meet WCAG 2.1 AA standards and include appropriate tests.

---

OMEGA Divine Book Browser v2.0  
© 2025 OMEGA BTC AI Divine Collective. Licensed under GBU2™ License.
