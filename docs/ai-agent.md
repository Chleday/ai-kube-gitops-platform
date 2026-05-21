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
  -> Rule-based classifier or LLM JSON classifier
  -> JSON validation
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

## LLM mode

기본은 규칙 기반 classifier다.
`--llm` 옵션을 붙이면 OpenAI-compatible Chat Completions API로 intent 분류를 시도한다.

환경 변수:

```bash
export OPENAI_API_KEY="..."
export OPENAI_BASE_URL="https://api.openai.com/v1"
export OPENAI_MODEL="gpt-4o-mini"
```

사용:

```bash
python3 agent/gitops_agent.py ask "Argo CD UI 열어줘" --llm
```

LLM 출력은 다음 JSON만 허용한다.

```json
{"intent":"check_status","arguments":{}}
```

허용되지 않는 intent 또는 invalid JSON은 거부된다.
실패 시 rule-based classifier로 fallback한다.

## Web UI

간단한 FastAPI Web UI를 제공한다.

```bash
pip install -r agent/requirements.txt
uvicorn agent.web_ui:app --reload --port 8090
```

접속:

```text
http://127.0.0.1:8090
```

Web UI는 의도적으로 dry-run 결과만 보여준다.
실제 실행은 CLI에서 `--execute`로 수행한다.

## 왜 이렇게 설계했나

- 공개 포트폴리오에서 보안적으로 설명하기 좋다.
- secret 노출 가능성을 줄인다.
- LLM hallucination으로 잘못된 명령이 실행되는 것을 막는다.
- 실제 운영 자동화 도구의 기본 설계와 비슷하다.
- CLI와 Web UI 양쪽에서 같은 안전한 intent/action 계층을 재사용한다.

## 향후 개선

- JSON schema library 기반 엄격 검증
- 승인 플로우 추가
- 실행 로그를 Markdown report로 저장
- Argo CD API 연동
- Slack/Discord 알림 연동
- Tailscale auth key 없이 OAuth 기반 bootstrap 자동화
