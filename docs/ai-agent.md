# AI Agent Design

## 목적

이 프로젝트의 AI 에이전트는 Kubernetes GitOps 플랫폼을 자연어로 운영하는 경험을 보여주기 위한 포트폴리오 기능이다.

예:

```text
"클러스터 상태 확인해줘"
"Argo CD UI 열어줘"
"시크릿 정책 보여줘"
"yaml 검사해줘"
```

## 안전 설계

LLM이나 자연어 입력이 직접 shell command로 변환되면 위험하다.
따라서 이 프로젝트는 다음 구조를 사용한다.

```text
Natural Language
  -> Intent Classifier
  -> Allowed Intent
  -> Fixed Action Template
  -> Dry-run or Execute
```

## 지원 intent

| Intent | Action |
| --- | --- |
| check_status | kubectl get nodes/applications/pods/services |
| validate_repo | YAML/Python 문법 검증 |
| open_argocd | Argo CD port-forward |
| open_nginx_demo | whoami demo port-forward |
| show_secrets_policy | docs/secrets.md 출력 |
| show_bootstrap_steps | docs/bootstrap.md 출력 |
| show_troubleshooting | docs/troubleshooting.md 출력 |
| list_apps | Argo CD Application 목록 출력 |

## 왜 이렇게 설계했나

- 공개 포트폴리오에서 보안적으로 설명하기 좋다.
- secret 노출 가능성을 줄인다.
- LLM hallucination으로 잘못된 명령이 실행되는 것을 막는다.
- 실제 운영 자동화 도구의 기본 설계와 비슷하다.

## 향후 개선

- OpenAI-compatible API를 붙여 intent JSON 생성
- JSON schema validation 추가
- 승인 플로우 추가
- 실행 로그를 Markdown report로 저장
- Argo CD API 연동
- Slack/Discord 알림 연동
