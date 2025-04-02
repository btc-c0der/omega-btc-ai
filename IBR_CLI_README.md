# Kubernetes Commands

## Kubernetes Integration

The CLI integrates with Kubernetes to manage IBR España's cloud infrastructure. It provides:

- Monitoring of deployments, pods, and services
- Deployment management (restart, scaling)
- Log viewing
- Manifest application
- Deployment creation with a single command

The `k8s start` command lets you quickly create new deployments without writing YAML:

```bash
# Basic nginx deployment with 2 replicas
ibr k8s start ibr-web --image nginx:latest --port 80 --replicas 2

# Set environment variables
ibr k8s start ibr-api --image ibr-spain/api:latest --env DEBUG=true API_KEY=secret
```

It uses the official Kubernetes Python client and requires proper kubeconfig setup to connect to the cluster. Make sure to install the dependencies with:

```bash
pip install -r scripts/requirements-ibr-cli.txt
```

```bash
# Show the status of IBR España's Kubernetes resources
ibr k8s status

# Restart a deployment
ibr k8s restart instagram-connector

# View logs from a pod
ibr k8s logs ibr-api-pod-name

# Apply a Kubernetes manifest
ibr k8s apply kubernetes/ibr-spain/base/instagram-connector.yaml

# Start a new deployment
ibr k8s start ibr-api --image ibr-spain/api:latest --port 3000 --replicas 2 --env NODE_ENV=production DB_HOST=mongodb
```
