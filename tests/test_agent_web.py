import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "agent"))

import web_ui


def test_render_home_contains_form_and_dry_run_hint():
    html = web_ui.render_home()
    assert "GitOps AI Agent" in html
    assert "textarea" in html
    assert "Dry-run" in html


def test_render_answer_escapes_user_input():
    html = web_ui.render_answer('<script>alert(1)</script>', execute=False)
    assert "<script>" not in html
    assert "&lt;script&gt;" in html
