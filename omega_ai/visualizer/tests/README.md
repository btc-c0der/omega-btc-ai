# Big Brother Monitoring Panel Tests

This directory contains tests for the Big Brother monitoring panel implementation in the OMEGA BTC AI trading platform.

## Backend Tests

Backend tests are implemented in `test_big_brother_api.py` and cover the API endpoints and data processing logic.

### Running Backend Tests

To run backend tests:

```bash
# From the project root
pytest omega_ai/visualizer/tests/test_big_brother_api.py -v
```

### What's Covered

- API endpoint `/api/big-brother-data` for fetching all monitoring data
- 3D and 2D flow visualization generation endpoints
- Redis data retrieval with fallback to mock data
- Error handling for missing Redis connection or subprocess failures

## Frontend Tests

Frontend tests are implemented in `omega_ai/visualizer/frontend/reggae-dashboard/tests/big_brother_panel.test.js` and cover the panel UI and interactions.

### Running Frontend Tests

To run frontend tests:

```bash
# From the project root
cd omega_ai/visualizer/frontend/reggae-dashboard
npm test -- tests/big_brother_panel.test.js
```

### What's Covered

- Tab navigation between different monitoring sections
- Position data display and updates
- Flow visualization generation UI
- Panel expansion and fullscreen controls
- Error handling for API failures

## Test Coverage

The tests provide coverage for:

1. **API Endpoints**: All Big Brother monitoring API endpoints
2. **Data Flow**: Retrieval from Redis and fallback mechanisms
3. **Visualization Generation**: Both 3D and 2D flow visualization
4. **UI Components**: Tabs, panels, data displays, and controls
5. **Error Handling**: In both frontend and backend

## Adding More Tests

### For Backend

Add test cases to `test_big_brother_api.py` following the existing pattern. Use the fixture `app_with_redis` to get a server instance with mock Redis.

### For Frontend

Add test cases to `big_brother_panel.test.js`. The DOM setup provides a mock environment to test against.

## Integration Testing

For full end-to-end testing, consider using Cypress or Playwright to test the Big Brother panel in a real browser environment.
