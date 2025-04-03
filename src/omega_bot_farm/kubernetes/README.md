# Kubernetes Configuration

## Overview

The Kubernetes configuration for Omega Bot Farm provides scalable, resilient deployment of the trading bot ecosystem. This directory contains manifests for deploying all system components to a Kubernetes cluster, with appropriate resource allocation, scaling policies, and service discovery.

## Directory Structure

```
kubernetes/
├── deployments/        # Deployment configurations for system components
├── configmaps/         # Configuration data
├── secrets/            # Templates for secret management
└── services/           # Service definitions for networking
```

## Core Deployments

### BitGet Position Analyzer (deployments/bitget-position-analyzer.yaml)

Deployment configuration for the BitGet position analysis bot:

- CPU/memory resource requirements
- Scaling policies
- Environment variable configuration
- Volume mounts

### CCXT Strategic Trader (deployments/ccxt-strategic-trader.yaml)

Deployment for the CCXT-based trading bot:

- Multi-exchange support
- Trading strategy configuration
- Persistent volume claims for strategy data
- Resource limits

### Discord Bot (deployments/discord-bot.yaml)

Deployment for the Waze Bot Discord interface:

- Discord API integration
- User interaction service
- Notification system
- Authentication handlers

### Strategic Trader (deployments/strategic-trader.yaml)

Deployment for the Fibonacci-based strategic trading bot:

- Golden ratio trading algorithms
- Position sizing logic
- Market analysis components
- Risk management settings

## Configuration Management

### ConfigMaps

ConfigMaps store non-sensitive configuration data:

- Trading parameters
- Service endpoints
- Feature toggles
- Logging configuration

### Secrets

Secret templates for managing sensitive information:

- API keys
- Exchange credentials
- Authentication tokens
- Encryption keys

## Service Discovery

Service definitions enable component communication:

- Redis service for shared state
- Internal API endpoints
- External-facing services
- Headless services for stateful workloads

## Deployment Guide

### Prerequisites

- Kubernetes cluster (v1.19+)
- kubectl configured with cluster access
- Container registry with bot images
- Persistent storage provisioner

### Deployment Steps

1. Create namespace:

   ```bash
   kubectl create namespace omega-bot-farm
   ```

2. Apply ConfigMaps:

   ```bash
   kubectl apply -f kubernetes/configmaps/
   ```

3. Create Secrets:

   ```bash
   # Edit secret templates first with actual values
   kubectl apply -f kubernetes/secrets/
   ```

4. Deploy core infrastructure:

   ```bash
   kubectl apply -f kubernetes/services/redis.yaml
   ```

5. Deploy bots:

   ```bash
   kubectl apply -f kubernetes/deployments/
   ```

## Scaling

The Kubernetes deployment supports both horizontal and vertical scaling:

### Horizontal Pod Autoscaling

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: bitget-position-analyzer
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: bitget-position-analyzer
  minReplicas: 1
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 80
```

### Manual Scaling

```bash
# Scale Discord bot to 3 replicas
kubectl scale deployment discord-bot -n omega-bot-farm --replicas=3
```

## Observability

Kubernetes manifests include configurations for:

- Prometheus metrics endpoints
- Liveness and readiness probes
- Resource monitoring
- Logging integration

## Production Considerations

For production environments:

- Use node selectors or affinities for optimal placement
- Configure Pod Disruption Budgets for availability
- Implement network policies for security
- Use StatefulSets for components requiring stable identities
