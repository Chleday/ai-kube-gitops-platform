# Kube GitOps Portfolio

AI vibe coding으로 구축한 GitOps 기반 Kubernetes 플랫폼 포트폴리오입니다.

이 레포는 Kubernetes 클러스터를 수동 `kubectl apply`로 운영하지 않고, Git repository를 단일 진실 공급원(Single Source of Truth)으로 사용하는 구조를 보여줍니다. Argo CD가 이 레포를 감시하고 클러스터 애드온과 데모 백엔드 앱을 자동 동기화합니다.

> 현재 레포는 공개 포트폴리오용 템플릿입니다. 실제 토큰, API key, 비밀번호는 포함하지 않습니다.

## What this demonstrates

- Kubernetes cluster bootstrap with Argo CD
- App of Apps GitOps pattern
- Ingress, TLS, DNS automation 설계
- Secret 값을 Git에 저장하지 않는 External Secrets 구조
- Monitoring with kube-prometheus-stack
- Logging with Loki + Grafana Alloy
- Storage with Longhorn
- Backup with Velero
- Private access with Tailscale Operator
- Policy as Code with Kyverno
- Demo backend app with health/readiness/metrics endpoints
- GitHub Actions based manifest validation

## Architecture

```text
GitHub Repository
  |
  | push / pull request
  v
GitHub Actions
  |  YAML lint / kubeconform / secret scan
  v
Argo CD in Kubernetes
  |
  | sync desired state
  v
Kubernetes Cluster
  ├── ingress-nginx
  ├── cert-manager
  ├── external-dns
  ├── external-secrets
  ├── tailscale-operator
  ├── kube-prometheus-stack
  ├── loki + alloy
  ├── longhorn
  ├── velero
  ├── kyverno
  └── demo apps
```

## Repository structure

```text
bootstrap/          # 최소 수동 bootstrap: Argo CD 설치 + root app 등록
clusters/homelab/  # App of Apps. Argo CD가 여기를 바라봄
apps/              # platform addon과 demo application 정의
platform/          # 공통 namespace, RBAC, NetworkPolicy, 정책
docs/              # 운영/보안/장애대응 문서
.github/workflows/ # manifest validation CI
```

## Bootstrap flow

1. Kubernetes cluster 준비
2. 공개 GitHub 레포 생성
3. repo URL 치환
4. Argo CD 설치
5. root application 등록
6. 이후 모든 변경은 Git push로 반영

```bash
# 1. repo URL 치환
./scripts/configure-repo-url.sh https://github.com/YOUR_USERNAME/kube-gitops-portfolio.git

# 2. Argo CD 설치 및 root app 등록
./bootstrap/install-argocd.sh
```

Argo CD UI 확인:

```bash
kubectl -n argocd port-forward svc/argocd-server 8080:443
```

브라우저:

```text
https://127.0.0.1:8080
```

초기 admin password:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath='{.data.password}' | base64 -d; echo
```

## GitOps rule

Argo CD bootstrap 이후에는 원칙적으로 수동 배포를 하지 않습니다.

Good:

```bash
git add .
git commit -m "feat: add monitoring stack"
git push
```

Avoid:

```bash
kubectl apply -f apps/something.yaml
```

## Secret policy

절대 커밋하지 않는 것:

- `.env`
- API token
- kubeconfig
- TLS private key
- Kubernetes Secret의 실제 base64 값

사용하는 방식:

- External Secrets Operator
- 공개 레포에는 `ExternalSecret`과 `ClusterSecretStore` 템플릿만 저장
- 실제 값은 1Password, Vault, AWS Secrets Manager, Doppler, Infisical 같은 외부 Secret Manager에 저장

자세한 내용:

```text
docs/secrets.md
```

## Demo apps

### whoami

Ingress/DNS/TLS 확인용 간단한 HTTP 앱입니다.

### FastAPI backend

백엔드 포트폴리오를 보여주기 위한 샘플 앱입니다.

엔드포인트:

- `GET /healthz`
- `GET /readyz`
- `GET /version`
- `GET /config`
- `GET /counter`
- `POST /counter`
- `GET /metrics`

Kubernetes 연결 포인트:

- Deployment
- Service
- Ingress
- ConfigMap
- ExternalSecret placeholder
- PVC
- ServiceMonitor
- JSON logging

## Recommended exposure model

- Argo CD: Tailscale private access
- Grafana: Tailscale private access
- Demo app: Public Ingress + TLS

관리 UI를 인터넷에 직접 노출하지 않는 것을 원칙으로 합니다.


## AI Agent CLI

이 프로젝트에는 포트폴리오용 안전한 AI 에이전트 CLI가 포함되어 있습니다.

위치:

```text
agent/gitops_agent.py
```

특징:

- 자연어 요청을 사전 정의된 intent로 분류
- AI가 임의의 shell command를 생성/실행하지 않음
- allowlist에 있는 Kubernetes/GitOps action만 실행
- 기본은 dry-run, 실제 실행은 `--execute` 필요
- secret 값은 읽거나 출력하지 않음

예시:

```bash
python3 agent/gitops_agent.py ask "클러스터 상태 확인해줘"
python3 agent/gitops_agent.py ask "yaml 검사해줘" --execute
python3 agent/gitops_agent.py ask "Argo CD UI 열어줘"
python3 agent/gitops_agent.py open argocd --execute
python3 agent/gitops_agent.py secrets
```

지원 intent:

- `check_status`
- `validate_repo`
- `open_argocd`
- `open_nginx_demo`
- `show_secrets_policy`
- `show_bootstrap_steps`
- `show_troubleshooting`
- `list_apps`

자세한 내용:

```text
agent/README.md
```

## Validation

```bash
# YAML 파싱 검사
python3 scripts/validate-yaml.py

# kubeconform 검사, 설치된 경우
kubeconform -summary -ignore-missing-schemas $(find . -name '*.yaml' -not -path './.git/*')
```

## Sources

- Argo CD Declarative Setup: https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/
- Argo CD Cluster Bootstrapping: https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/
- Flux Concepts: https://fluxcd.io/flux/concepts/
- External Secrets Operator: https://external-secrets.io/latest/
- cert-manager: https://cert-manager.io/docs/
- external-dns: https://kubernetes-sigs.github.io/external-dns/latest/
- Tailscale Kubernetes Operator: https://tailscale.com/kb/1236/kubernetes-operator
- Prometheus Operator: https://prometheus-operator.dev/docs/getting-started/introduction/
- Grafana Loki Helm: https://grafana.com/docs/loki/latest/setup/install/helm/
- Longhorn: https://longhorn.io/docs/
- Velero: https://velero.io/docs/
- Kyverno: https://kyverno.io/docs/
- Renovate: https://docs.renovatebot.com/
