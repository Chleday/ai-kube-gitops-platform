# Troubleshooting

## WSL에서 NodePort가 Windows 브라우저로 열리지 않음

증상:

- WSL 내부 `curl http://127.0.0.1:NODEPORT`는 성공
- Windows 브라우저 `http://127.0.0.1:NODEPORT`는 실패

원인:

- Kubernetes NodePort는 일반 프로세스가 포트를 listen하는 방식이 아니라 kube-proxy/iptables 라우팅이다.
- WSL localhost forwarding이 이 트래픽을 항상 처리하지 못할 수 있다.

해결:

```bash
kubectl port-forward --address 0.0.0.0 service/nginx-test 8080:80
```

브라우저:

```text
http://127.0.0.1:8080
```

## Argo CD app이 OutOfSync

```bash
kubectl -n argocd get applications
kubectl -n argocd describe application <name>
```

일반 원인:

- repoURL 미치환
- Helm chart version 오류
- CRD 설치 전 custom resource 적용
- namespace 누락
- secret 미생성
