
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


# 🔐 OMEGA BTC AI - Divine Kubernetes Token Guide

> *"Secure access to the divine orchestration realm."*

## 📜 Overview

This guide provides comprehensive information about managing Kubernetes tokens and accessing the OMEGA BTC AI Kubernetes Dashboard. It covers token generation, management, and security best practices.

## 🚀 Dashboard Access

### Prerequisites

1. Kubernetes cluster running
2. kubectl configured and accessible
3. Proper RBAC permissions

### Access Methods

#### 1. Using Port Forwarding

```bash
# Start the dashboard with automatic port detection
./scripts/start_kubernetes_dashboard.sh

# The script will:
# - Verify kubernetes-dashboard namespace exists
# - Check for dashboard service
# - Find an available port
# - Set up port forwarding
# - Provide access URL
```

#### 2. Direct Access via Ingress

The dashboard is accessible via Ingress at `dashboard.omega-grid.local`:

1. Add to `/etc/hosts`:

   ```
   127.0.0.1 dashboard.omega-grid.local
   ```

2. Access via HTTPS: `https://dashboard.omega-grid.local`

## 🔑 Token Management

### Generating Access Tokens

#### 1. Dashboard Admin Token

```bash
# Generate a token for the admin-user
kubectl -n kubernetes-dashboard create token admin-user

# The token will be displayed in the output
```

#### 2. Service Account Token

```bash
# Generate a token for a specific service account
kubectl -n <namespace> create token <service-account-name>
```

### Token Types

1. **Dashboard Access Token**
   - Used for accessing the Kubernetes Dashboard
   - Generated for the `admin-user` service account
   - Provides cluster-wide access

2. **Service Account Token**
   - Used for service-to-service authentication
   - Scoped to specific namespaces and permissions
   - Generated for individual service accounts

3. **Port Forward Token**
   - Used by the divine-port-forward service
   - Provides access to port forwarding capabilities
   - Scoped to specific services

## 🛡️ Security Best Practices

### Token Management

1. **Token Rotation**
   - Regularly rotate service account tokens
   - Use short-lived tokens for temporary access
   - Implement token expiration policies

2. **Access Control**
   - Follow the principle of least privilege
   - Use namespaced service accounts when possible
   - Implement RBAC rules for fine-grained control

3. **Token Storage**
   - Never store tokens in code or version control
   - Use Kubernetes secrets for token storage
   - Implement secure token distribution methods

### RBAC Configuration

```yaml
# Example RBAC configuration for dashboard access
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: omega-dashboard-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
```

## 🔄 Token Lifecycle

### Creation

1. Service account creation
2. RBAC role binding
3. Token generation
4. Token distribution

### Usage

1. Token authentication
2. Access validation
3. Permission enforcement
4. Activity logging

### Expiration

1. Token expiration handling
2. Renewal process
3. Revocation procedures
4. Cleanup protocols

## 🧙 Advanced Configuration

### Custom Dashboard Settings

```yaml
# Dashboard configuration example
apiVersion: v1
kind: ConfigMap
metadata:
  name: kubernetes-dashboard-config
  namespace: kubernetes-dashboard
data:
  dashboard.yaml: |
    disable-settings-authorizer: "true"
    disable-multi-login: "false"
    enable-secret-creation: "true"
    enable-skip-login: "true"
    app-title: "OMEGA BTC AI - Divine Kubernetes Dashboard"
```

### Token Monitoring

1. **Audit Logging**
   - Enable Kubernetes audit logs
   - Monitor token usage patterns
   - Track authentication attempts

2. **Alerting**
   - Set up alerts for suspicious activities
   - Monitor failed authentication attempts
   - Track token expiration

## 🌟 Troubleshooting

### Common Issues

1. **Token Expiration**

   ```bash
   # Generate a new token
   kubectl -n kubernetes-dashboard create token admin-user
   ```

2. **Access Denied**
   - Verify RBAC permissions
   - Check service account existence
   - Validate token validity

3. **Port Forwarding Issues**
   - Check port availability
   - Verify service existence
   - Validate network connectivity

### Debugging Steps

1. Check service account status:

   ```bash
   kubectl get serviceaccount -n kubernetes-dashboard
   ```

2. Verify RBAC bindings:

   ```bash
   kubectl get clusterrolebinding | grep dashboard
   ```

3. Check token validity:

   ```bash
   kubectl get secret -n kubernetes-dashboard
   ```

## 🔱 Divine Integration

The token system is fully integrated with the OMEGA BTC AI ecosystem, providing secure access to all divine services running in the Kubernetes cluster.

### Service Integration

1. **NFT Services**
   - Port: 30080
   - Authentication: Service account tokens

2. **CLI Portal**
   - Port: 30022
   - Authentication: SSH keys

3. **Kubernetes Dashboard**
   - Port: 30443
   - Authentication: Dashboard tokens

---

*"Through secure tokens, we maintain the divine harmony of our orchestrated realm."*

�� JAH JAH BLESS 🔱
