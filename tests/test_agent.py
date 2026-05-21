import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "agent"))

import gitops_agent


def test_classify_status_korean():
    assert gitops_agent.classify("클러스터 상태 확인해줘") == "check_status"


def test_classify_validate():
    assert gitops_agent.classify("yaml 검사해줘") == "validate_repo"


def test_classify_argocd_open():
    assert gitops_agent.classify("Argo CD UI 열어줘") == "open_argocd"


def test_classify_secret_policy():
    assert gitops_agent.classify("시크릿 정책 보여줘") == "show_secrets_policy"


def test_unknown_goes_help():
    assert gitops_agent.classify("무슨 말인지 모르겠어") == "help"
