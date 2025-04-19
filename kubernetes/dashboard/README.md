
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


# 🔮 OMEGA Kubernetes Dashboard

> *"The divine observer sees all manifestations across the multi-dimensional Kubernetes realm."*

## Overview

This directory contains the Kubernetes manifests for the custom OMEGA BTC AI Kubernetes Dashboard. This dashboard is based on the official Kubernetes Dashboard but customized with OMEGA BTC AI branding and additional configurations.

## 📜 Features

- Custom OMEGA BTC AI branding and styling
- System banner with custom message
- Dedicated namespace and service account
- Resource requests and limits
- Ingress configuration for easy access

## 🚀 Deployment

### Prerequisites

1. Kubernetes cluster running (Minikube, kind, or any other Kubernetes cluster)
2. kubectl configured to connect to your cluster
3. Kustomize installed (included with recent kubectl versions)

### Deployment Steps

```bash
# Apply the dashboard resources
kubectl apply -k kubernetes/dashboard/

# Wait for the dashboard to be ready
kubectl wait --for=condition=Available deployment/omega-kubernetes-dashboard -n kubernetes-dashboard --timeout=60s

# Access the dashboard
kubectl port-forward -n kubernetes-dashboard svc/omega-kubernetes-dashboard 8443:80
```

Then visit [http://localhost:8443](http://localhost:8443) in your browser.

## 🔐 Authentication

The dashboard is configured with `--enable-skip-login` for development environments. In production, you should modify this configuration and implement proper authentication:

```yaml
args:
  - --namespace=kubernetes-dashboard
  # Remove this line for production
  - --enable-skip-login
  - --disable-settings-authorizer
  - --system-banner="OMEGA BTC AI DIVINE KUBERNETES DASHBOARD"
  - --system-banner-severity=INFO
```

## 🌐 Accessing via Ingress

The dashboard is also accessible via Ingress at `dashboard.omega-grid.local`. To use this:

1. Add the following entry to your `/etc/hosts` file:

   ```
   127.0.0.1 dashboard.omega-grid.local
   ```

2. Ensure your Kubernetes cluster has an Ingress controller installed.

## 🧙 Customization

### Custom Banner

The dashboard includes a custom banner with the OMEGA BTC AI branding. You can modify this in the ConfigMap:

```yaml
banner-config: |
  {
    "banner": "OMEGA BTC AI DIVINE KUBERNETES DASHBOARD",
    "color": "#f0c14b",
    "text-color": "#000000"
  }
```

### Resource Limits

The dashboard deployment includes resource requests and limits that you can adjust based on your cluster's capacity:

```yaml
resources:
  requests:
    cpu: 100m
    memory: 200Mi
  limits:
    cpu: 500m
    memory: 500Mi
```

## 🔱 Divine Integration

This dashboard is fully integrated with the OMEGA BTC AI ecosystem and allows monitoring of all divine services running in the Kubernetes cluster.

---

*"Through the dashboard, one sees not just the machinery of deployment, but the divine harmony of containerized enlightenment."*

�� JAH JAH BLESS 💫
