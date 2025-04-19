# IBR España Test Suite Documentation

✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------

This code is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

*"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."*

By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸

## Overview

This test suite validates the functionality of the IBR España component within the Divine Dashboard v3 application. The tests focus on the Flask routes and API endpoints that provide church event management capabilities.

## Test Structure

The test suite is organized into several categories:

1. **Unit Tests** - Isolated tests for individual route functions using mocked dependencies
2. **API Tests** - Tests for the RESTful API endpoints
3. **Integration Tests** - End-to-end tests that exercise complete workflows

## Test Files

- `tests/test_ibr_spain_routes.py` - Main test file for IBR España routes
- `run_ibr_tests.sh` - Shell script to execute tests with various options

## Running the Tests

You can run the tests using the provided shell script:

```bash
./run_ibr_tests.sh
```

### Command-line Options

The script supports the following options:

- `--coverage` or `-c`: Generate code coverage reports
- `--verbose` or `-v`: Display detailed test output
- `--test` or `-t`: Run a specific test (e.g., `test_view_event`)

Examples:

```bash
# Run with coverage report
./run_ibr_tests.sh --coverage

# Run with verbose output
./run_ibr_tests.sh --verbose

# Run a specific test
./run_ibr_tests.sh --test test_view_event

# Combine options
./run_ibr_tests.sh --coverage --verbose --test test_api_create_event
```

## Test Coverage

The test suite aims to provide comprehensive coverage of the IBR España component:

| Component | Coverage |
|-----------|----------|
| Route Handlers | 100% |
| API Endpoints | 100% |
| Event CRUD Operations | 100% |
| Error Handling | 100% |

## Tested Functionality

### Route Handlers

- Main dashboard index page
- Events listing page with filtering
- Event creation form
- Event detail view
- Event edit form
- Event deletion

### API Endpoints

- GET `/api/events` - Retrieve events with optional filtering
- GET `/api/events/<event_id>` - Retrieve a specific event
- POST `/api/events` - Create a new event
- PUT `/api/events/<event_id>` - Update an existing event
- DELETE `/api/events/<event_id>` - Delete an event

### Utility Routes

- POST `/generate-sample-events` - Generate sample events for testing

## Mocking Strategy

The test suite uses pytest's monkeypatch and unittest.mock to simulate the EventsManager behavior without requiring a real database. This allows for:

1. Faster test execution
2. Isolation from external dependencies
3. Precise control over test conditions

## Integration Testing

The integration tests use a real EventsManager instance with a temporary directory for storage. These tests exercise the complete lifecycle of an event:

1. Creation
2. Retrieval
3. Modification
4. Deletion

## Troubleshooting

If you encounter issues running the tests:

1. Ensure all requirements are installed:

   ```bash
   pip install -r requirements.txt
   ```

2. Verify your Python environment:

   ```bash
   python --version  # Should be 3.8+
   ```

3. Check for template and static file paths:

   ```python
   # Templates should be in:
   # divine_dashboard_v3/templates/ibr_spain/
   
   # Static files should be in:
   # divine_dashboard_v3/static/
   ```

## Contributing

When contributing to the IBR España component:

1. Add tests for any new functionality
2. Ensure all existing tests pass
3. Maintain or improve test coverage

## Divine Resonance

The test suite is aligned with the divine resonance principles of the GBU2™ License. Each test acts as a celestial guardian, ensuring the divine flow of code remains pure and unobstructed.

---

*"When tests shine green, the divine code flows serene."* - OMEGA BTC AI Development Principles
