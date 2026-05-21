# GitOps AI Agent

이 디렉터리는 포트폴리오 프로젝트를 "AI 에이전트형 GitOps 운영 도구"로 보여주기 위한 안전한 CLI/Web 에이전트입니다.

핵심 원칙:

1. AI가 임의의 shell command를 직접 실행하지 않는다.
2. 자연어는 사전에 정의된 intent로만 변환된다.
3. 실제 실행 가능한 action은 allowlist로 제한된다.
4. 기본은 dry-run이며, 실행은 `--execute`를 명시해야 한다.
5. secret 값은 읽거나 출력하지 않는다.

## Install dev dependencies

```bash
pip install -r agent/requirements.txt
```

## CLI examples

```bash
python3 agent/gitops_agent.py ask "클러스터 상태 확인해줘"
python3 agent/gitops_agent.py ask "nginx 앱 브라우저로 열어줘"
python3 agent/gitops_agent.py ask "yaml 검사해줘" --execute
python3 agent/gitops_agent.py status --execute
python3 agent/gitops_agent.py validate --execute
python3 agent/gitops_agent.py open argocd --execute
```

## Web UI

```bash
uvicorn agent.web_ui:app --reload --port 8090
```

브라우저:

```text
http://127.0.0.1:8090
```

Web UI도 기본적으로 dry-run 결과만 보여줍니다.
실제 실행은 CLI에서 `--execute`를 붙여 수행합니다.

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

규칙 기반 classifier가 기본입니다. OpenAI-compatible API를 사용하려면 다음 환경 변수를 설정합니다.

```bash
export OPENAI_API_KEY="..."
export OPENAI_BASE_URL="https://api.openai.com/v1"  # optional
export OPENAI_MODEL="gpt-4o-mini"                   # optional
```

사용:

```bash
python3 agent/gitops_agent.py ask "Argo CD UI 열어줘" --llm
```

LLM 출력은 반드시 아래 JSON schema에 맞춰 검증됩니다.

```json
{
  "intent": "check_status",
  "arguments": {}
}
```

허용되지 않은 intent는 실행하지 않습니다.
LLM이 shell command를 반환해도 무시/거부됩니다.
