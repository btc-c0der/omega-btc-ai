# Big Brother Monitoring Panel Tests

This directory contains tests for the Big Brother monitoring panel components of the OMEGA BTC AI trading platform.

## Overview

The test suite covers both backend API endpoints and frontend functionality:

1. **Backend Tests** - Verify the API endpoints that provide data and visualization functionality
2. **Frontend Tests** - Verify the panel's UI interactions and data display

## Test Files

- `test_big_brother_api.py` - Tests for the backend API endpoints
- `../frontend/reggae-dashboard/tests/big_brother_panel.test.js` - Tests for the frontend components

## Running Backend Tests

To run the backend tests, use:

```bash
cd omega-btc-ai
python -m pytest omega_ai/visualizer/tests/test_big_brother_api.py -v
```

## Running Frontend Tests

To run the frontend tests, use:

```bash
cd omega-btc-ai/omega_ai/visualizer/frontend/reggae-dashboard
npm test
```

Make sure you have the required testing dependencies installed:

```bash
npm install --save-dev jsdom sinon assert mocha
```

## Test Coverage

The tests cover:

### Backend Tests

- Big Brother data endpoint
- 3D flow visualization endpoint
- 2D flow visualization endpoint
- Redis data retrieval
- Error handling

### Frontend Tests

- Tab navigation functionality
- Data loading and display
- Flow visualization generation
- Panel controls (expand/collapse, fullscreen)

## Adding New Tests

When adding new features to the Big Brother panel:

1. Add corresponding backend tests in `test_big_brother_api.py`
2. Add corresponding frontend tests in `big_brother_panel.test.js`
3. Run the entire test suite to ensure no regressions

## Mock Data

The tests use mock data to simulate Redis data and API responses. If you change the data structure:

1. Update the mock data in `test_big_brother_api.py`
2. Update the mock API responses in `big_brother_panel.test.js`

## CI/CD Integration

These tests are designed to be integrated with CI/CD pipelines. The backend tests use pytest, which can generate JUnit XML reports. The frontend tests can be run with the Mocha test runner with the appropriate reporters.
