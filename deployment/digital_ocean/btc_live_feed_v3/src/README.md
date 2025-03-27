# OMEGA BTC AI - BTC Live Feed v3 Source Code

This directory contains the source code for the BTC Live Feed v3 component, which provides enhanced reliability through automatic Redis failover capabilities, ensuring 99.99% uptime even during temporary outages of the primary Redis service.

## Directory Structure

```
src/
├── omega_ai/
│   ├── data_feed/
│   │   ├── btc_live_feed_v3.py  # Main BTC Live Feed v3 implementation
│   │   └── health_check.py      # Health check API server
│   └── utils/
│       └── enhanced_redis_manager.py  # Redis manager with failover capability
├── scripts/
│   └── monitor_btc_feed_v3.py   # CLI monitoring dashboard
└── tests/                       # Test suite
    ├── test_btc_live_feed_v3.py
    ├── test_enhanced_redis_manager.py
    └── test_prefix_sampling_v3.py
```

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Start the BTC Live Feed v3 service
python -m omega_ai.data_feed.btc_live_feed_v3

# Start the Health Check API server
python -m omega_ai.data_feed.health_check

# Use the monitoring dashboard
python scripts/monitor_btc_feed_v3.py --host localhost --port 8080
```

## Testing

```bash
# Run the test suite
pytest tests/
```

## License

This code is provided under the GPU (General Public Universal) License.

Copyright (c) 2025 OMEGA BTC AI DIVINE COLLECTIVE
