#!/usr/bin/env python3
"""Tiny web UI for the safe GitOps AI agent.

Run:
  uvicorn agent.web_ui:app --reload --port 8090
"""
from __future__ import annotations

import html
import io
from contextlib import redirect_stdout

try:
    from fastapi import FastAPI, Form
    from fastapi.responses import HTMLResponse
except ModuleNotFoundError:  # Allows render_* unit tests without optional web deps installed.
    FastAPI = None
    Form = None
    HTMLResponse = str

import gitops_agent

app = FastAPI(title="GitOps AI Agent UI") if FastAPI else None


def page(body: str) -> str:
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>GitOps AI Agent</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 960px; margin: 40px auto; padding: 0 16px; }}
    textarea {{ width: 100%; min-height: 100px; font-size: 16px; }}
    pre {{ background: #111827; color: #e5e7eb; padding: 16px; border-radius: 8px; overflow-x: auto; }}
    button {{ padding: 10px 14px; font-weight: 700; }}
    .hint {{ color: #555; }}
  </style>
</head>
<body>
{body}
</body>
</html>"""


def render_home() -> str:
    return page(
        """
<h1>GitOps AI Agent</h1>
<p>자연어를 안전한 Kubernetes/GitOps intent로 변환합니다.</p>
<p class="hint">기본은 Dry-run입니다. 실제 실행은 CLI에서 <code>--execute</code>로 수행하세요.</p>
<form method="post" action="/ask">
  <textarea name="question" placeholder="예: 클러스터 상태 확인해줘"></textarea>
  <p><button type="submit">Ask Agent</button></p>
</form>
<h2>Examples</h2>
<ul>
  <li>클러스터 상태 확인해줘</li>
  <li>yaml 검사해줘</li>
  <li>Argo CD UI 열어줘</li>
  <li>시크릿 정책 보여줘</li>
</ul>
"""
    )


def render_answer(question: str, execute: bool = False) -> str:
    safe_question = html.escape(question)
    args = type("Args", (), {"text": question, "execute": execute, "llm": False})()
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        gitops_agent.ask(args)
    output = html.escape(buffer.getvalue())
    return page(
        f"""
<h1>GitOps AI Agent</h1>
<p><a href="/">Back</a></p>
<h2>Question</h2>
<pre>{safe_question}</pre>
<h2>Answer</h2>
<pre>{output}</pre>
"""
    )


if app is not None:
    @app.get("/", response_class=HTMLResponse)
    def home():
        return render_home()

    @app.post("/ask", response_class=HTMLResponse)
    def ask(question: str = Form(...)):
        return render_answer(question, execute=False)
