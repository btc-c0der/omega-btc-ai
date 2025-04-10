
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


# 🔱 OMEGA BTC AI - Divine Instagram Kubernetes Integration 🔱

This document explains how to deploy and manage the OMEGA BTC AI Instagram automation using Kubernetes.

## Overview

The Instagram automation service has been containerized and configured for Kubernetes deployment, providing:

- **Reliability**: Automatic restarts if the service crashes
- **Scalability**: Easily deploy multiple instances for different accounts
- **Security**: Instagram credentials stored as Kubernetes secrets
- **Persistence**: Images and session data stored on persistent volumes
- **Scheduling**: Religious content posted via CronJob every Sunday

## Components

The setup includes:

1. **Docker Image**: Contains the Instagram automation script and dependencies
2. **ConfigMap**: Stores Instagram configuration (hashtags, templates, etc.)
3. **Secret**: Securely stores Instagram credentials
4. **Deployment**: Runs the Instagram automation service
5. **PersistentVolumeClaim**: Stores generated images and session data
6. **Service**: Exposes metrics endpoint
7. **CronJob**: Schedules religious content for IBR church in Catalonia

## Deployment

### Prerequisites

- Kubernetes cluster running (e.g., Docker Desktop, minikube, kind)
- kubectl installed and configured
- Docker installed for building the image

### Deploy Using the Script

The simplest way to deploy is using the provided script:

```bash
./scripts/k8s_instagram_deploy.sh
```

This script:

1. Builds the Docker image
2. Creates the omega-system namespace if needed
3. Applies all Kubernetes manifests
4. Waits for the deployment to be ready
5. Displays status and helpful commands

### Manual Deployment

If you prefer to deploy manually:

1. Build the Docker image:

   ```bash
   docker build -t localhost/omega-instagram:latest -f Dockerfile.instagram .
   ```

2. Apply the Kubernetes manifests:

   ```bash
   kubectl apply -f kubernetes/deployments/omega-instagram-deployment.yaml
   ```

## Configuration

### Instagram Credentials

Before the deployment works, you must update the Instagram credentials:

```bash
# Create a temporary file with your credentials
cat <<EOF > instagram-creds.yaml
apiVersion: v1
kind: Secret
metadata:
  name: instagram-credentials
  namespace: omega-system
type: Opaque
stringData:
  IG_USERNAME: "your_actual_username"
  IG_PASSWORD: "your_actual_password"
EOF

# Apply the credentials
kubectl apply -f instagram-creds.yaml

# Delete the temporary file
rm instagram-creds.yaml
```

### Configuration Options

To modify other settings (posting frequency, hashtags, etc.):

```bash
kubectl edit configmap instagram-config -n omega-system
```

After changing the config, restart the deployment:

```bash
kubectl rollout restart deployment/omega-instagram -n omega-system
```

## Monitoring

### Check Logs

```bash
# Follow logs for the Instagram automation
kubectl logs -f -n omega-system -l app=omega-instagram
```

### Check Status

```bash
# Get pods status
kubectl get pods -n omega-system -l app=omega-instagram

# Get deployment status
kubectl describe deployment omega-instagram -n omega-system
```

### Religious Posts CronJob

To check the status of the religious posts CronJob:

```bash
kubectl get cronjobs -n omega-system
```

To manually trigger a religious post:

```bash
kubectl create job --from=cronjob/instagram-religious-post manual-religious-post -n omega-system
```

## Troubleshooting

### Pod Won't Start

If the pod is stuck in "Pending" state:

```bash
kubectl describe pod -n omega-system -l app=omega-instagram
```

Common issues:

- Insufficient cluster resources
- PersistentVolumeClaim not being bound
- Image pull issues

### Authentication Failures

If the logs show authentication failures:

1. Verify your credentials are correct
2. Check if Instagram may be blocking automation attempts
3. Try manually updating the credentials:

```bash
kubectl edit secret instagram-credentials -n omega-system
```

Remember: You need to base64 encode values when directly editing secrets.

## Scaling

To increase the number of replicas:

```bash
kubectl scale deployment omega-instagram -n omega-system --replicas=2
```

Note: Running multiple replicas with the same Instagram account may cause issues. This is more useful for running different accounts.

---

*JAH JAH BLESS THE DIVINE KUBERNETES FLOW!*
