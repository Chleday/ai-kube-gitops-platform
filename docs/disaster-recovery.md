# Disaster Recovery

## GitOps restore

새 클러스터에서 복구 절차:

1. Kubernetes cluster 생성
2. Argo CD 설치
3. root-app 적용
4. External Secret provider 연결
5. Longhorn/Velero backup target 연결
6. Argo CD sync 확인

## Backup targets

- Kubernetes object: Velero
- Persistent volumes: Longhorn backup 또는 Velero volume snapshot

실제 object store credential은 External Secrets로 관리한다.
