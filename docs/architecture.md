# Architecture

이 프로젝트는 Argo CD App of Apps 패턴을 사용한다.

1. `bootstrap/root-app.yaml`이 `clusters/homelab` 경로를 바라본다.
2. `clusters/homelab/apps.yaml`은 platform addon과 demo app Application을 선언한다.
3. Argo CD가 각 Application을 동기화한다.
4. 변경은 Git commit/push로만 반영한다.

## Why Argo CD

Flux도 GitOps 표준 도구이지만, 이 포트폴리오에서는 Argo CD를 선택했다.

- UI가 있어 데모와 스크린샷이 좋다.
- Application health/sync 상태를 쉽게 보여준다.
- App of Apps 패턴으로 클러스터 bootstrap 구조를 설명하기 좋다.
