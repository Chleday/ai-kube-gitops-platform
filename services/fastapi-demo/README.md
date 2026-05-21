# FastAPI demo backend

백엔드 + Kubernetes 운영 역량을 보여주기 위한 샘플 앱입니다.

## Features

- Health endpoint: `/healthz`
- Readiness endpoint: `/readyz`
- Version endpoint: `/version`
- Config endpoint: `/config`
- Persistent counter: `GET /counter`, `POST /counter`
- Prometheus metrics: `/metrics`
- JSON structured logs
- PVC-backed state at `/data/counter.txt`

## Local run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Container build

```bash
docker build -t ghcr.io/chleday/kube-gitops-fastapi-demo:0.1.0 .
```
