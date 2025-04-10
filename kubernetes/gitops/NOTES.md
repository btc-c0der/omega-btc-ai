
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


# 🔱 DIVINE GITOPS QUICK REFERENCE 🔱

This document provides quick reference information for divine operators working with the OMEGA BTC AI GitOps system.

## 🌟 ArgoCD Access

- **ArgoCD UI**: <http://localhost:8080> (after running `./access-argocd.sh`)
- **Default User**: admin
- **Default Password**: Retrieved via script or command below

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

## 🚀 Initial Setup Steps

1. **Bootstrap ArgoCD**:

```bash
./kubernetes/gitops/install-argocd.sh
```

2. **Apply App of Apps**:

```bash
kubectl apply -f kubernetes/gitops/applications/omega-app-of-apps.yaml
```

3. **Verify Sync Status**:

```bash
kubectl get applications -n argocd
```

## 🔮 Divine GitOps Workflow

1. Create branch for changes
2. Modify application manifests or Helm values
3. Submit Pull Request for divine review
4. Upon merge to main, ArgoCD will automatically detect and sync changes

## 🧙‍♂️ Key ArgoCD Commands

```bash
# Port-forward to ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# View application status
kubectl get applications -n argocd

# View detailed app info
kubectl describe application omega-btc-oracle -n argocd

# Trigger manual sync for an app
kubectl patch application omega-btc-oracle -n argocd -p '{"spec":{"syncPolicy":{"automated":{"prune":true,"selfHeal":true}}}}' --type=merge

# View ArgoCD logs
kubectl logs deployment/argocd-application-controller -n argocd
```

## 💫 Application Troubleshooting

- Check application status on ArgoCD UI
- Verify that Git repo is accessible from ArgoCD
- Check for sync errors in Application resources
- Ensure correct values files are referenced in Helm applications

## 🌈 Divine Resource Hierachy

```
omega-divine-grid (App of Apps)
├── omega-btc-oracle
└── omega-matrix-news
```

## 🙏 Blessing of Access

"What is granted in RBAC, shall be forever divine in permission."
