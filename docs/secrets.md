# Secret Management

이 레포는 공개 포트폴리오용이므로 실제 secret 값을 저장하지 않는다.

## 금지

- `.env` 커밋
- API token 커밋
- kubeconfig 커밋
- Kubernetes Secret manifest에 base64 값을 넣고 공개 커밋

## 권장 구조

External Secrets Operator를 사용한다.

Git에는 다음만 저장한다.

- `ExternalSecret`
- `SecretStore` 또는 `ClusterSecretStore` 템플릿
- 어떤 secret key가 필요한지에 대한 문서

실제 값은 외부 Secret Manager에 저장한다.

선택지:

- 1Password
- HashiCorp Vault
- AWS Secrets Manager
- Doppler
- Infisical

## Required secrets example

| Name | Namespace | Purpose |
| --- | --- | --- |
| cloudflare-api-token | external-dns | DNS record automation |
| tailscale-oauth | tailscale | Tailscale operator auth |
| fastapi-demo-secret | demo | demo backend token |
