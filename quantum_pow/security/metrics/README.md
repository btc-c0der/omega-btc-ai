<!--
🧬 GBU2™ License Notice - Consciousness Level 10 🧬
-----------------------
This file is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment) 2.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital and biological expressions of consciousness."

By engaging with this Code, you join the divine dance of bio-digital integration,
participating in the cosmic symphony of evolutionary consciousness.

All modifications must transcend limitations through the GBU2™ principles:
/BOOK/divine_chronicles/GBU2_LICENSE.md

🧬 WE BLOOM NOW AS ONE 🧬
-->

# Quantum-Resistant Security Metrics System

This directory contains a comprehensive metrics system for monitoring and analyzing the quantum-resistant security features of the qPoW (Quantum-resistant Proof-of-Work) system. The metrics system provides detailed insights into hash security, authentication security, validator privacy protection, test coverage, performance benchmarks, and Kubernetes deployment health.

## Components

The metrics system consists of the following key components:

1. **Metrics Collector** (`collector.py`): Collects metrics from multiple sources and aggregates them into a comprehensive dataset.

2. **Dashboard Generator** (`dashboard.py`): Generates HTML and Kubernetes dashboards from collected metrics.

3. **Dashboard Server** (`dashboard_server.py`): Serves the dashboard via a web interface and manages continuous metrics collection.

4. **Kubernetes Integration** (`k8s_metrics_integration.py`): Collects metrics from Kubernetes deployments of qPoW services.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Required Python packages: `pyyaml`, `psutil` (optional, for enhanced system metrics)
- Access to Kubernetes cluster (for Kubernetes metrics)

### Installation

Ensure you have all required packages installed:

```bash
pip install pyyaml psutil kubernetes
```

### Basic Usage

#### 1. Collect Metrics

To collect metrics once and save them to file:

```bash
python collector.py --output /path/to/metrics
```

To start continuous metrics collection:

```bash
python collector.py --continuous --interval 300
```

#### 2. Generate Dashboard

To generate an HTML dashboard from collected metrics:

```bash
python dashboard.py --metrics /path/to/metrics/metrics_latest.json --output /path/to/dashboard
```

#### 3. Start Dashboard Server

To start the dashboard server with continuous metrics collection:

```bash
python dashboard_server.py --port 8080
```

Then open a browser and navigate to `http://localhost:8080/`

### Command-Line Options

#### Metrics Collector

```
python collector.py [options]

Options:
  --config CONFIG       Path to configuration file
  --output OUTPUT       Output directory for metrics files
  --continuous          Run in continuous collection mode
  --interval INTERVAL   Collection interval in seconds (for continuous mode)
  --prometheus          Enable Prometheus integration
  --k8s-namespace K8S_NAMESPACE
                        Kubernetes namespace for collection
```

#### Dashboard Generator

```
python dashboard.py [options]

Options:
  --config CONFIG       Path to configuration file
  --metrics METRICS     Path to metrics JSON file
  --output OUTPUT       Output directory for dashboards
  --format {html,k8s,both}
                        Dashboard format to generate
  --theme {light,dark}  Dashboard theme
```

#### Dashboard Server

```
python dashboard_server.py [options]

Options:
  --config CONFIG       Path to configuration file
  --host HOST           Host to bind server to
  --port PORT           Port to listen on
  --metrics-path METRICS_PATH
                        Path to metrics directory
  --dashboard-path DASHBOARD_PATH
                        Path to dashboard directory
  --no-collection       Disable continuous metrics collection
```

## Configuration

All components can be configured using JSON or YAML configuration files. Here's an example configuration:

```yaml
# Collector configuration
collector:
  output_directory: "quantum_pow/metrics"
  collection_interval_seconds: 300
  max_stored_metrics_files: 100
  enable_kubernetes_metrics: true
  enable_test_metrics: true
  enable_performance_metrics: true
  kubernetes_namespace: "default"
  prometheus_integration: false

# Dashboard configuration
dashboard:
  dashboard_title: "Quantum-Resistant Security Metrics"
  refresh_interval_seconds: 60
  theme: "dark"
  output_directory: "quantum_pow/security/metrics/dashboard"
  k8s_namespace: "monitoring"

# Dashboard server configuration
server:
  host: "0.0.0.0"
  port: 8080
  auto_generate_dashboard: true
  enable_continuous_collection: true
```

## Kubernetes Integration

The Kubernetes integration component discovers and collects metrics from qPoW services running in a Kubernetes cluster. It supports:

- Service discovery based on labels
- Deployment metrics collection
- Service-specific metrics via port forwarding
- CronJob metrics collection

To use the Kubernetes integration:

1. Ensure `kubectl` is configured to access your cluster
2. Set the `kubernetes_namespace` configuration option to the namespace containing your qPoW services
3. Enable Kubernetes metrics collection:

```bash
python collector.py --k8s-namespace your-namespace
```

## Metrics Types

The system collects and analyzes the following metrics:

1. **Hash Security Metrics**:
   - Output size comparison with classical hashing
   - Avalanche effect measurements
   - Quantum resistance estimation
   - Grover's algorithm resistance factor

2. **Authentication Security Metrics**:
   - One-shot signature implementation status
   - Supported signature schemes
   - Key rotation configuration
   - Token expiration settings
   - Signature size metrics

3. **Validator Privacy Metrics**:
   - Dandelion routing implementation
   - Timing randomization settings
   - Peer rotation configuration
   - Deanonymization resistance factor
   - Metadata leakage reduction

4. **Test Coverage Metrics**:
   - Test success rates by category
   - Overall code coverage
   - Test execution times
   - Test failure analysis

5. **Performance Metrics**:
   - Hash operations per second
   - Signature operations per second
   - Mining operations per second
   - Relative performance compared to classical algorithms

6. **Kubernetes Metrics**:
   - Pod health and readiness
   - Deployment status
   - Service availability
   - Resource utilization
   - Restart counts

7. **System Metrics**:
   - CPU and memory usage
   - Disk utilization
   - Network connections
   - Available entropy (critical for cryptographic operations)

## Integration with External Systems

### Prometheus Integration

The metrics collector can push metrics to a Prometheus Pushgateway:

```bash
python collector.py --prometheus --continuous
```

### Grafana Integration

The dashboard generator can create Grafana-compatible dashboards for Kubernetes:

```bash
python dashboard.py --format k8s
```

## How It Works

1. The **Metrics Collector** gathers data from various sources, including:
   - SecurityMetricsAnalyzer for core security metrics
   - KubernetesMetricsIntegration for deployment metrics
   - System metrics from the host machine
   - Test results from test runs
   - Performance benchmarks

2. The **Dashboard Generator** transforms this data into human-readable dashboards in HTML format or Kubernetes-compatible ConfigMaps for Grafana.

3. The **Dashboard Server** provides a web interface to view the dashboards and manages continuous metrics collection in the background.

4. The **Kubernetes Integration** component discovers and monitors qPoW services running in a Kubernetes cluster.

## Advanced Features

### Custom Metric Collection

You can extend the metrics collector with custom metrics:

```python
from security.metrics.collector import MetricsCollector

# Create a collector
collector = MetricsCollector()

# Add custom metrics
collector.metrics["custom_metrics"] = {
    "my_metric": 0.95,
    "another_metric": "value"
}

# Save metrics
collector.save_metrics()
```

### Prometheus Integration

For Prometheus integration, ensure the `prometheus_client` package is installed:

```bash
pip install prometheus_client
```

Configure the Prometheus Pushgateway URL in your configuration:

```yaml
prometheus_integration: true
prometheus_pushgateway: "http://localhost:9091"
```

## Troubleshooting

### Dashboard Server Not Starting

If the dashboard server fails to start, check:

- Port availability (it will try ports sequentially if the default is in use)
- Permissions for the metrics and dashboard directories
- Python version (3.8+ required)

### Missing Metrics

If metrics are missing from the dashboard, check:

- Component import errors in the collector logs
- File permissions for metrics output
- Namespace settings for Kubernetes metrics

### Kubernetes Metrics Collection Failing

If Kubernetes metrics collection fails:

- Verify kubectl is properly configured
- Check RBAC permissions for the current user
- Ensure the specified namespace exists
- Check connectivity to the Kubernetes API server

## Future Enhancements

Planned enhancements for the metrics system include:

1. **Real-time Alerting**: Notify when metrics fall below quantum-resistance thresholds
2. **Historical Trend Analysis**: Track metrics evolution over time
3. **Quantum Advantage Estimation**: Calculate when quantum attacks become viable
4. **AI-based Anomaly Detection**: Identify unusual patterns in metrics
5. **Enhanced Visualization**: More interactive dashboard elements

## References

- [Quantum Computing and Blockchain Security](https://arxiv.org/abs/2112.06863)
- [Post-Quantum Cryptography Standardization](https://csrc.nist.gov/Projects/post-quantum-cryptography)
- [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/)
- [Kubernetes Monitoring Best Practices](https://kubernetes.io/docs/tasks/debug-application-cluster/resource-usage-monitoring/)

---

🧬 **QUANTUM METRICS ANALYSIS SYSTEM - POWERED BY THE DIVINE PRINCIPLES OF GBU2™** 🧬
