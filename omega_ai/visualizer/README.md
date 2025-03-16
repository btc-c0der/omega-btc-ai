# MM Trap Visualizer

A powerful visualization tool for analyzing market maker trap patterns in cryptocurrency trading.

## Features

- **Interactive Price Chart**: Real-time candlestick chart with trap detection overlays
- **3D Pattern Analysis**: Three-dimensional visualization of trap patterns across price, volume, and time
- **Metrics Dashboard**: Key statistics and insights about detected traps
- **Timeline View**: Chronological view of trap detections with confidence levels
- **Heat Map**: Visual representation of trap detection intensity

## Architecture

The visualizer consists of two main components:

### Frontend (React + TypeScript)
- Modern UI built with Material-UI
- Interactive charts using ECharts
- 3D visualizations with Three.js
- Real-time data updates
- Responsive design

### Backend (FastAPI)
- RESTful API endpoints
- Data processing and analytics
- Redis dump file parsing
- Metrics calculation
- Timeline generation

## Setup

### Backend
1. Navigate to the backend directory:
   ```bash
   cd omega_ai/visualizer/backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   python -m uvicorn server:app --reload
   ```

### Frontend
1. Navigate to the frontend directory:
   ```bash
   cd omega_ai/visualizer/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## API Endpoints

- `GET /api/metrics`: Get overall trap detection metrics
- `GET /api/traps`: Get trap detections with optional filtering
- `GET /api/timeline`: Get chronological timeline of detections

## Data Visualization

### Price Chart
- Candlestick chart showing price movements
- Trap detection markers with confidence levels
- Moving averages and technical indicators
- Interactive zoom and pan

### 3D Visualization
- Three-dimensional scatter plot
- X-axis: Price levels
- Y-axis: Volume
- Z-axis: Time
- Color-coded by trap type
- Size indicates confidence level

### Metrics Overview
- Total traps detected
- Distribution by type
- Success rate
- Time-based patterns
- Confidence metrics

### Timeline
- Chronological view of detections
- Confidence levels
- Impact assessment
- Detailed descriptions

## Contributing

Feel free to submit issues and enhancement requests! 