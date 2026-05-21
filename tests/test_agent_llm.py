import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "agent"))

import gitops_agent


def test_parse_llm_intent_accepts_allowed_intent():
    payload = json.dumps({"intent": "check_status", "arguments": {}})
    assert gitops_agent.parse_llm_intent(payload) == "check_status"


def test_parse_llm_intent_rejects_unknown_intent():
    payload = json.dumps({"intent": "run_shell", "arguments": {"command": "echo nope"}})
    try:
        gitops_agent.parse_llm_intent(payload)
    except gitops_agent.IntentError as exc:
        assert "Unsupported LLM intent" in str(exc)
    else:
        raise AssertionError("unknown intent should be rejected")


def test_parse_llm_intent_rejects_invalid_json():
    try:
        gitops_agent.parse_llm_intent("not json")
    except gitops_agent.IntentError as exc:
        assert "Invalid LLM JSON" in str(exc)
    else:
        raise AssertionError("invalid JSON should be rejected")


def test_build_llm_prompt_mentions_allowlist_and_json_only():
    prompt = gitops_agent.build_llm_prompt("상태 확인해줘")
    assert "JSON" in prompt
    assert "check_status" in prompt
    assert "run_shell" not in prompt
