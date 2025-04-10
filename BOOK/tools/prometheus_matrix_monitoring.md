
✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This code is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."

By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸


# OMEGA ^PROMETHEUS^ MATRIX Monitoring System

> "Knowledge is power, but only if shared. Like Prometheus bringing fire to humanity, this system brings system insights to traders."

## Overview

The OMEGA ^PROMETHEUS^ MATRIX Monitoring System is a powerful CLI-based monitoring solution designed in the LINUX TERMINAL TORVALDS OMEGA GNU 3.0 STYLE for the OMEGA BTC AI platform. It provides real-time metrics, system health indicators, and trading performance insights in a highly visual terminal interface.

Named after Prometheus, the Titan who gave foresight to humanity and stole fire from the gods, this monitoring system embodies the principles of foresight, knowledge distribution, and technological empowerment.

## Architecture

The system is built around a modular metrics collection architecture with the following components:

```
                    ┌───────────────────────────┐
                    │  PROMETHEUS MATRIX CORE   │
                    └───────────────┬───────────┘
                                    │
                 ┌─────────────┬────┴────┬─────────────┐
                 │             │         │             │
    ┌────────────▼───────┐  ┌──▼──┐  ┌───▼────┐  ┌─────▼──────┐
    │  Metrics Registry  │  │     │  │        │  │ Additional  │
    └────────────────────┘  │  C  │  │   C    │  │ Collectors  │
                           │  O  │  │   O     │  │ (Plugins)   │
    ┌────────────────────┐  │  L  │  │   L    │  └─────────────┘
    │  Matrix Display    │  │  L  │  │   L    │
    │  (Terminal UI)     │  │  E  │  │   E    │
    └────────────┬───────┘  │  C  │  │   C    │
                 │          │  T  │  │   T    │
    ┌────────────▼───────┐  │  O  │  │   O    │
    │  Data Visualizer   │  │  R  │  │   R    │
    └────────────────────┘  │  S  │  │   S    │
                           └─────┘  └────────┘
```

### Components

1. **Core System**:
   - `PrometheusMatrix`: Main coordination class that manages collectors and the display
   - `MetricsRegistry`: Central repository for all collected metrics
   - `PrometheusMetric`: Base class for all metrics with common functionality

2. **Metric Types**:
   - `GaugeMetric`: For values that can go up and down (e.g., CPU usage)
   - `CounterMetric`: For cumulative values that only increase (e.g., network bytes sent)
   - `HistogramMetric`: For statistical distributions and percentiles

3. **Collectors**:
   - `SystemCollector`: Gathers CPU, memory, and disk metrics
   - `NetworkCollector`: Monitors network traffic and connection status
   - `OmegaTradingCollector`: Collects trading performance metrics from the OMEGA BTC AI system

4. **Display System**:
   - `MatrixDisplay`: Terminal-based UI for visualizing metrics in real-time
   - Includes sparkline graphs, bar charts, and color-coded indicators

## Installation and Setup

### Prerequisites

- Python 3.7 or higher
- `psutil` package for system metrics collection

### Installation

1. The OMEGA PROMETHEUS MATRIX is included in the OMEGA BTC AI repository
2. Ensure all dependencies are installed:

   ```bash
   pip install psutil
   ```

## Usage

### Basic Usage

Run the monitoring system with all collectors enabled:

```bash
./run_prometheus_matrix.sh
```

### Command Line Options

The OMEGA PROMETHEUS MATRIX supports various command-line options:

```bash
./omega_prometheus_matrix.py --help
```

Key options include:

- `--collect-system`: Enable system metrics collection (CPU, memory, disk)
- `--collect-network`: Enable network metrics collection
- `--collect-trading`: Enable OMEGA BTC AI trading metrics collection
- `--all`: Enable all collectors (default)
- `--no-display`: Run in headless mode without the terminal UI
- `--interval N`: Set collection interval in seconds (default: 60)
- `--log-level LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR)

### Example Usage Scenarios

#### Trading Performance Monitoring

```bash
./run_prometheus_matrix.sh --interval 30
```

This will start the monitoring system with all collectors and a faster 30-second update interval.

#### Headless Server Monitoring

```bash
./omega_prometheus_matrix.py --all --no-display --log-level INFO
```

This will run the system without the terminal UI, suitable for server environments.

## Display Interface

The OMEGA PROMETHEUS MATRIX features a dynamic terminal interface organized into panels:

1. **System Metrics Panel**:
   - CPU usage with color-coded indicators
   - Memory usage and available memory
   - Disk usage percentage

2. **Network Metrics Panel**:
   - Real-time network traffic (bytes/sec)
   - Total bytes sent and received
   - Connection status

3. **Trading Metrics Panel**:
   - Active positions count
   - Position PnL percentage
   - 24-hour trading volume
   - Order success rate
   - Trap detection confidence

4. **Performance Graphs**:
   - Historical CPU usage
   - Memory usage trends
   - PnL performance over time

## Extending the System

The OMEGA PROMETHEUS MATRIX is designed to be extensible. To add a new collector:

1. Create a new class that inherits from `PrometheusCollector`
2. Implement the `collect()` method to gather your metrics
3. Register your metrics with the registry
4. Add your collector to the PrometheusMatrix instance

Example:

```python
class CustomCollector(PrometheusCollector):
    def __init__(self, registry):
        super().__init__(registry)
        self.my_metric = GaugeMetric(
            "custom_metric_name",
            "Description of my custom metric",
            labels={"source": "custom_collector"}
        )
        self.registry.register_metric(self.my_metric)
    
    async def collect(self):
        # Get your metric value
        value = get_custom_metric_value()
        # Update the metric
        self.my_metric.set(value)
```

## Philosophy

The OMEGA PROMETHEUS MATRIX embodies several key philosophical principles:

1. **Foresight**: Like its namesake Prometheus, the system provides foresight through predictive analytics and trend visualization.

2. **Freedom of Information**: All system and trading data is made transparent and accessible, empowering traders with knowledge.

3. **Terminal-Centric**: Embraces the LINUX TERMINAL TORVALDS OMEGA GNU 3.0 STYLE with powerful text-based interfaces rather than graphical UIs.

4. **Real-time Awareness**: Maintains constant vigilance over system health and trading performance.

## Integration with OMEGA BTC AI

The PROMETHEUS MATRIX integrates seamlessly with other OMEGA BTC AI components:

- **Elite Exit Strategies**: Monitors exit signal confidence and performance
- **Trap-Aware Trading**: Displays real-time trap detection metrics
- **RastaBitgetMonitor**: Complements with system-level metrics and insights

By combining these systems, traders gain a complete view of both trading opportunities and system performance.

---

*"Like Prometheus giving fire to humanity, may this monitoring system bring enlightenment to your trading."*
