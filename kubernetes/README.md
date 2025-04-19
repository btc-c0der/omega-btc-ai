
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


# 🔱 OMEGA BTC AI - KUBERNETES DEPLOYMENT 🔱

> *"Divine orchestration through cosmic containers."*

## Overview

This directory contains Kubernetes manifests for deploying the OMEGA BTC AI system in a Kubernetes cluster. The deployment follows the principles of GitOps and Infrastructure as Code, with a base configuration and environment-specific overlays.

## Structure

- `base/`: Contains the base Kubernetes manifests
- `overlays/`: Contains environment-specific customizations
  - `dev/`: Development environment
  - `staging/`: Staging environment
  - `prod/`: Production environment

## Components

The OMEGA BTC AI system consists of the following components:

- **Matrix News Service**: Provides divine news and information
- **BTC Live Feed**: Streams real-time Bitcoin data
- **Prophecy Core**: Contains the central wisdom engine
- **Redis**: Sacred data store for all components
- **Monitoring Stack**: Prometheus, Grafana, and AlertManager

## Prerequisites

- Kubernetes 1.19+
- kubectl 1.19+
- kustomize 3.8+
- Ingress controller (nginx-ingress recommended)

## Deployment

### Development Environment

```bash
# Apply the dev overlay
kubectl apply -k kubernetes/overlays/dev
```

### Production Environment

```bash
# Apply the prod overlay
kubectl apply -k kubernetes/overlays/prod
```

## Configuration

### Environment Variables

Environment-specific variables are managed through Kustomize patches. For sensitive data like passwords and API keys, Kubernetes Secrets are used.

### Secrets

Production secrets should be managed using a secure method such as:

- Sealed Secrets
- HashiCorp Vault
- AWS Secrets Manager
- Azure Key Vault

### Resource Management

Resource requests and limits are defined in the base configuration and adjusted in environment-specific overlays:

- Development: Minimal resources
- Production: Sufficient resources for high availability and performance

## Scaling

The OMEGA BTC AI system can scale horizontally by increasing the number of replicas:

```bash
kubectl scale deployment matrix-news --replicas=5 -n omega-btc-ai-prod
```

## Monitoring

The deployment includes a full monitoring stack:

- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboards
- **AlertManager**: Alert routing and notifications

Access Grafana at: `https://omega.example.com/grafana`

## Backup and Recovery

For data persistence and backup, consider:

1. Using persistent volumes for Redis and other stateful components
2. Setting up regular backups of Redis data
3. Implementing point-in-time recovery mechanisms

## Divine Maintenance

Regular maintenance keeps the cosmic harmony:

```bash
# Check the status of all pods
kubectl get pods -n omega-btc-ai-prod

# View logs of a specific component
kubectl logs deployment/matrix-news -n omega-btc-ai-prod

# Execute commands in a pod
kubectl exec -it deployment/redis -n omega-btc-ai-prod -- redis-cli
```

---

*This sacred Kubernetes deployment was channeled during the alignment of cosmic forces and container orchestration wisdom. May your deployments be blessed with stability and divine performance.*
