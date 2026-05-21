# Bootstrap

## Prerequisites

- Kubernetes cluster
- kubectl configured
- GitHub repository pushed

## Steps

```bash
./scripts/configure-repo-url.sh https://github.com/YOUR_USERNAME/kube-gitops-portfolio.git
git add .
git commit -m "chore: configure repository url"
git push
./bootstrap/install-argocd.sh
```

## After bootstrap

```bash
kubectl -n argocd get applications
kubectl get pods -A
```
