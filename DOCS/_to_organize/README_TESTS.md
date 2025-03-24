# OMEGA BTC AI - Reggae Dashboard Testing Guide

This document explains how to run tests for the Reggae Dashboard components.

## Backend Testing

The backend tests are implemented using `pytest` and test the FastAPI server endpoints and other functionality.

### Prerequisites

1. Install test dependencies:

```
pip install -r tests/requirements-test.txt
```

2. Make sure Redis is running locally or configure the tests to use a remote Redis instance.

### Running Backend Tests

To run all tests:

```
pytest tests/
```

To run only unit tests:

```
pytest tests/unit/
```

To run specific tests for the Reggae Dashboard server:

```
pytest tests/unit/visualizer/test_reggae_dashboard_server.py
```

### Generating Test Data

You can generate test data in Redis using the provided script:

```
python tests/fixtures/create_test_trap_data.py --interval 2
```

Options:

- `--host`: Redis host (default: localhost)
- `--port`: Redis port (default: 6379)
- `--password`: Redis password (if required)
- `--cycles`: Number of update cycles (default: infinite)
- `--interval`: Update interval in seconds (default: 1.0)

Press Ctrl+C to stop the data generator.

## Frontend Testing

The frontend tests are implemented using Vitest and React Testing Library.

### Prerequisites

1. Install dependencies:

```
cd omega_ai/visualizer/frontend/reggae-dashboard
npm install
```

### Running Frontend Tests

To run all frontend tests:

```
cd omega_ai/visualizer/frontend/reggae-dashboard
npm test
```

To run tests in watch mode:

```
npm run test:watch
```

To run tests with coverage:

```
npm run test:coverage
```

## Running the Dashboard for Testing

To test the full application:

1. Start the backend server:

```
cd omega_ai/visualizer/backend
python reggae_dashboard_server.py
```

2. In another terminal, start generating test data:

```
python tests/fixtures/create_test_trap_data.py
```

3. In a third terminal, start the frontend development server:

```
cd omega_ai/visualizer/frontend/reggae-dashboard
npm run dev
```

4. Open a browser and navigate to `http://localhost:5173` (or the URL displayed in the terminal).

## Troubleshooting

### Common Issues

1. **Redis Connection Error**: Make sure Redis is running and accessible. Check the connection parameters.

2. **Missing Dependencies**: Run the appropriate install commands shown in the prerequisites section.

3. **Port Already in Use**: If port 8000 is already in use, modify the server port in the server code.

4. **WebSocket Connection Issues**: Check that the WebSocket URL in the frontend matches the backend server.
