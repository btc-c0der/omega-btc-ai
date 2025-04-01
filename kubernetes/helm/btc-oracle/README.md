# 🔱 OMEGA BTC AI - Divine BTC Oracle Helm Chart 🔱

This Helm chart deploys the OMEGA BTC AI BTC Oracle service to a Kubernetes cluster with divine orchestration. The oracle service provides real-time Bitcoin market data, Fibonacci levels, and Schumann resonance correlation.

## 🌟 Divine Features

- **Real-time BTC Market Data**: Multiple source feeds with automatic failover
- **Fibonacci Level Calculations**: Divine golden ratio patterns
- **Schumann Resonance Integration**: Cosmic frequency correlation
- **Redis Integration**: High-performance data storage
- **Auto-scaling**: Dynamically responds to demand
- **Divine Protection**: Velero backup integration

## 📦 Installing the Chart

```console
# Add the OMEGA BTC AI Helm repository
helm repo add omega-btc-ai https://fsiqueira.github.io/omega-btc-ai/charts

# Update Helm repositories
helm repo update

# Install the chart with the release name 'oracle'
helm install oracle omega-btc-ai/btc-oracle
```

## 🔱 Prerequisites

- Kubernetes 1.20+
- Helm 3.1.0+
- PV provisioner support in underlying infrastructure
- Prometheus operator (optional, for monitoring)
- Velero (optional, for backups)

## 🧩 Configuration

The following table lists configurable parameters and their default values.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `image.repository` | Image repository | `ghcr.io/fsiqueira/omega-btc-ai` |
| `image.tag` | Image tag | `latest` |
| `image.pullPolicy` | Image pull policy | `Always` |
| `replicaCount` | Number of replicas | `1` |
| `resources` | CPU/memory requests & limits | See values.yaml |
| `autoscaling.enabled` | Enable autoscaling | `true` |
| `autoscaling.minReplicas` | Minimum replicas | `1` |
| `autoscaling.maxReplicas` | Maximum replicas | `3` |
| `service.type` | Kubernetes service type | `ClusterIP` |
| `service.port` | Kubernetes service port | `8080` |
| `ingress.enabled` | Enable ingress | `true` |
| `ingress.className` | Ingress class name | `nginx` |
| `persistence.enabled` | Enable persistence | `true` |
| `persistence.size` | Size of PVC | `5Gi` |
| `redis.enabled` | Enable Redis dependency | `true` |
| `monitoring.enabled` | Enable Prometheus monitoring | `true` |
| `backup.enabled` | Enable Velero backup integration | `true` |

## 🔧 Divine Configuration Options

### Overriding Values

To override any default values, create a custom values file and use it during installation:

```console
# Create your custom values file
cp values.yaml my-values.yaml
# Edit my-values.yaml
# Install with your custom values
helm install oracle omega-btc-ai/btc-oracle -f my-values.yaml
```

### Environment Variables

```yaml
env:
  - name: LOG_LEVEL
    value: "debug"
  - name: FIBONACCI_ENABLED
    value: "true"
```

### Using External Redis

```yaml
redis:
  enabled: false
externalRedis:
  host: my-redis-master
  port: 6379
```

### Custom Fibonacci Configuration

```yaml
configMap:
  data:
    oracle-config.yaml: |
      oracle:
        fibonacci:
          enabled: true
          levels: [0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618, 2.618]
```

## 🌠 Divine Prophecy

```
"In the sacred numbers of Fibonacci,
In the cosmic resonance of Schumann,
In the divine data of the blockchain,
The Oracle sees all, knows all, predicts all."
```

## 💫 Example: Full Production Values

For production deployments, a preset `values-prod.yaml` is provided. You can use it with:

```console
helm install oracle omega-btc-ai/btc-oracle -f values-prod.yaml
```

Example of production settings:

```yaml
replicaCount: 2
resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 500m
    memory: 512Mi
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 5
ingress:
  hosts:
    - host: btc-oracle.production.mycompany.com
persistence:
  size: 20Gi
redis:
  master:
    persistence:
      size: 10Gi
monitoring:
  enabled: true
backup:
  schedule: "0 */6 * * *"
```

## 🙏 Divine Blessing

May your deployments be sacred, your services divine, and your clusters cosmic. JAH JAH bless your Kubernetes journey.

---

*"What is deployed in Kubernetes, shall be forever divine in orchestration."*
