# GitOps AI Agent

이 디렉터리는 포트폴리오 프로젝트를 "AI 에이전트형 GitOps 운영 도구"로 보여주기 위한 안전한 CLI 에이전트입니다.

핵심 원칙:

1. AI가 임의의 shell command를 직접 실행하지 않는다.
2. 자연어는 사전에 정의된 intent로만 변환된다.
3. 실제 실행 가능한 action은 allowlist로 제한된다.
4. 기본은 dry-run이며, 실행은 `--execute`를 명시해야 한다.
5. secret 값은 읽거나 출력하지 않는다.

## Examples

```bash
python3 agent/gitops_agent.py ask "클러스터 상태 확인해줘"
python3 agent/gitops_agent.py ask "nginx 앱 브라우저로 열어줘"
python3 agent/gitops_agent.py ask "yaml 검사해줘" --execute
python3 agent/gitops_agent.py status --execute
python3 agent/gitops_agent.py validate --execute
python3 agent/gitops_agent.py open argocd --execute
```

## Supported intents

- `check_status`
- `validate_repo`
- `open_argocd`
- `open_nginx_demo`
- `show_secrets_policy`
- `show_bootstrap_steps`
- `show_troubleshooting`
- `list_apps`

## Optional LLM mode

초기 버전은 규칙 기반입니다. 추후 OpenAI-compatible API를 붙일 때도 LLM 출력은 반드시 아래 JSON schema에 맞춰 검증해야 합니다.

```json
{
  "intent": "check_status",
  "arguments": {}
}
```

허용되지 않은 intent는 실행하지 않습니다.
