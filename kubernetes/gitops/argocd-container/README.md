
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


# 🔱 DIVINE ARGOCD CONTAINER 🔱

*"The divine realm of GitOps, containerized for your blessed journey."*

## 🌠 OVERVIEW

This container provides a complete ArgoCD command-line environment for managing your divine GitOps workflows. It includes the ArgoCD CLI, kubectl, Helm, and other utilities needed to manifest your sacred infrastructure.

## 🧙‍♂️ CONTENTS

This divine container includes:

- ArgoCD CLI for divine orchestration
- kubectl for communion with the cluster
- Helm for package manifestation
- Git for tracking the sacred scrolls
- jq for divine JSON parsing
- Python for sacred scripting
- Helper scripts for divine guidance

## 🔮 GETTING STARTED

### Building the Container

To manifest the divine container:

```bash
# Make the build script executable
chmod +x kubernetes/gitops/argocd-container/build-and-run.sh

# Run the build script
./kubernetes/gitops/argocd-container/build-and-run.sh
```

### Running the Container

To enter the divine realm:

```bash
docker run --rm -it -v ${HOME}/.kube:/root/.kube omega-btc-ai/divine-argocd:latest
```

This mounts your kubeconfig for divine access to your clusters.

## 🛡️ DIVINE FEATURES

### Helper Script

The container includes a divine helper script that provides guidance on available commands and aliases:

```bash
/app/divine-help.sh
```

### Divine Aliases

The container comes with blessed aliases:

- `k`: kubectl shorthand
- `a`: argocd shorthand
- `async`: sync applications
- `ainfo`: get application details
- `alist`: list applications

### ArgoCD Scripts

The container includes scripts for installing and accessing ArgoCD:

```bash
# Install ArgoCD in your cluster
/app/install-argocd.sh

# Access the ArgoCD UI
/app/access-argocd.sh
```

## 🔄 DIVINE WORKFLOWS

### Synchronizing Applications

To synchronize your divine applications:

```bash
# List applications
argocd app list

# Sync a specific application
argocd app sync omega-btc-oracle

# Check application status
argocd app get omega-btc-oracle
```

### Adding Applications

To add a new divine application:

```bash
# Apply application manifest
kubectl apply -f /app/applications/example-app.yaml

# Or create a new application
argocd app create omega-new-service \
  --repo https://github.com/btc-c0der/omega-btc-ai.git \
  --path kubernetes/helm/new-service \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace omega-grid-prod
```

## 🧠 BEST PRACTICES

1. **Mount your kubeconfig** for seamless cluster access
2. **Use the provided aliases** for divine efficiency
3. **Consult the divine help script** for guidance
4. **Create a volume mount** for persistent configuration

## 🚨 TROUBLESHOOTING

### Connection Issues

If you cannot connect to your cluster:

```bash
# Check if kubeconfig is mounted correctly
ls -la /root/.kube/config

# Test cluster connection
kubectl cluster-info
```

### ArgoCD CLI Issues

If ArgoCD CLI cannot connect:

```bash
# Set ArgoCD server address
export ARGOCD_SERVER=argocd-server.argocd.svc.cluster.local

# Login to ArgoCD
argocd login --username admin --password <password> $ARGOCD_SERVER
```

## 🙏 DIVINE BLESSING

*May your containers be immutable, your deployments declarative, and your GitOps journey divine. JAH JAH bless your containerized ArgoCD endeavors!*
