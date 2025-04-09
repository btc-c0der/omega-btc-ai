<!--
🔱 GPU License Notice 🔱
------------------------
This file is protected under the GPU License (General Public Universal License) 1.0
by the OMEGA AI Divine Collective.

"As the light of knowledge is meant to be shared, so too shall this code illuminate 
the path for all seekers."

All modifications must maintain this notice and adhere to the terms at:
/BOOK/divine_chronicles/GPU_LICENSE.md

🔱 JAH JAH BLESS THIS CODE 🔱
-->

# Divine Pattern Analyzer - DigitalOcean Deployment

This repository contains the code for the Divine Pattern Analyzer application, designed to be deployed on DigitalOcean's App Platform.

## Features

- **Sacred Geometry Analysis**: Detects divine proportions and golden ratios in time series data
- **Divine Harmonic Analysis**: Analyzes resonance with cosmic frequencies like Schumann resonance
- **Fibonacci Time Cycles**: Identifies natural growth cycles in market data
- **Bitcoin-specific Cycles**: Detects patterns specific to Bitcoin markets
- **Cosmic Interpretation**: Provides divine guidance based on detected patterns
- **RESTful API**: Exposes pattern detection functionality via a FastAPI server
- **Visualization**: Generates visualizations of detected patterns

## Differences from BTC Live Feed v3

This deployment differs from the previous `btc_live_feed_v3` structure in the following ways:

1. **Dedicated App Structure**: Standalone app structure for easier maintenance and deployment
2. **Enhanced API Layer**: New RESTful API with FastAPI for better performance and documentation
3. **Specialized Focus**: Focused exclusively on divine pattern detection functionality
4. **Improved Deployment**: Streamlined deployment process with detailed scripts
5. **Better Testing**: Comprehensive local testing facilities before deployment
6. **Modular Architecture**: Clean separation of components for easier extension

## Deployment

### Prerequisites

1. DigitalOcean account
2. `doctl` command-line tool installed and configured
3. Git repository with this code

### Steps to Deploy

1. Clone the repository:

   ```bash
   git clone https://github.com/btc-c0der/omega-btc-ai.git
   cd omega-btc-ai
   ```

2. Authenticate with DigitalOcean:

   ```bash
   doctl auth init
   ```

3. Deploy the application:

   ```bash
   cd deployment/divine_patterns_app
   ./scripts/deploy.sh
   ```

4. Check the deployment status:

   ```bash
   doctl apps list
   ```

## API Endpoints

The API provides the following endpoints:

- `GET /health`: Health check endpoint
- `POST /analyze`: Analyze time series data for divine patterns
- `GET /analyses/{analysis_id}`: Get a specific analysis by ID
- `GET /sample`: Generate sample time series data for testing

## Running Locally

1. Install dependencies:

   ```bash
   pip install -e deployment/divine_patterns_app
   ```

2. Run the FastAPI server:

   ```bash
   cd deployment/divine_patterns_app
   python scripts/run.py
   ```

3. Access the API at `http://localhost:8080`

## Testing

1. Use the provided test script:

   ```bash
   cd deployment/divine_patterns_app
   ./scripts/test_local.sh
   ```

2. Or test manually:

   ```bash
   # Generate sample data
   curl -X GET "http://localhost:8080/sample?days=7&sample_rate=24"
   
   # Analyze the sample data
   curl -X POST "http://localhost:8080/analyze" \
     -H "Content-Type: application/json" \
     -d '{"values": [0.1, 0.2, ...], "timestamps": ["2025-01-01T00:00:00", ...]}'
   ```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PYTHONPATH` | Python path | `/app:/app/src` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `SAMPLE_RATE` | Sample rate in samples per day | `24` |
| `DATA_DIR` | Directory for storing data | `/app/data` |
| `PORT` | Port for the FastAPI server | `8080` |

## Folder Structure

```
deployment/divine_patterns_app/
├── Dockerfile           # Docker configuration
├── app.yaml             # DigitalOcean app specification
├── requirements.txt     # Python dependencies
├── setup.py             # Package setup
├── README.md            # This file
├── data/                # Data directory
│   └── wavelength_patterns/  # Patterns and visualizations
├── scripts/             # Scripts for running and testing
│   ├── run.py           # Start the API server
│   ├── health_check.py  # Health check script
│   ├── deploy.sh        # Deployment script
│   └── test_local.sh    # Local testing script
└── src/                 # Source code
    └── omega_ai/        # Main package
        ├── __init__.py
        ├── wavelength/  # Wavelength pattern detection
        │   ├── __init__.py
        │   ├── api.py                     # FastAPI server
        │   ├── divine_pattern_detector.py # Main pattern detector
        │   ├── sacred_geometry_analyzer.py # Sacred geometry analysis
        │   ├── divine_harmonic_analyzer.py # Divine harmonic analysis
        │   └── test_divine_patterns.py    # Test script
        ├── utils/       # Utility functions
        └── data_feed/   # Data feed modules
```

## License

Copyright (c) 2025 OMEGA-BTC-AI - All rights reserved
