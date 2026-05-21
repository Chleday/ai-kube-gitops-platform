import json
import os
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, generate_latest

APP_NAME = os.getenv("APP_NAME", "kube-gitops-fastapi-demo")
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
DATA_DIR = Path(os.getenv("DATA_DIR", "/data"))
COUNTER_FILE = DATA_DIR / "counter.txt"

REQUESTS = Counter("fastapi_demo_requests_total", "Total demo requests", ["endpoint"])
COUNTER_VALUE = Gauge("fastapi_demo_counter_value", "Current persisted counter value")

app = FastAPI(title=APP_NAME, version="0.1.0")


def log(event: str, **fields):
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "app": APP_NAME,
        **fields,
    }
    print(json.dumps(record, ensure_ascii=False), flush=True)


def read_counter() -> int:
    try:
        return int(COUNTER_FILE.read_text().strip())
    except Exception:
        return 0


def write_counter(value: int) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    COUNTER_FILE.write_text(str(value))
    COUNTER_VALUE.set(value)


@app.on_event("startup")
def startup():
    value = read_counter()
    COUNTER_VALUE.set(value)
    log("startup", counter=value, log_level=LOG_LEVEL)


@app.get("/healthz")
def healthz():
    REQUESTS.labels("healthz").inc()
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    REQUESTS.labels("readyz").inc()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return {"status": "ready"}


@app.get("/version")
def version():
    REQUESTS.labels("version").inc()
    return {"app": APP_NAME, "version": "0.1.0"}


@app.get("/config")
def config():
    REQUESTS.labels("config").inc()
    token_present = bool(os.getenv("API_TOKEN"))
    return {"app_name": APP_NAME, "log_level": LOG_LEVEL, "api_token_present": token_present}


@app.get("/counter")
def get_counter():
    REQUESTS.labels("get_counter").inc()
    value = read_counter()
    COUNTER_VALUE.set(value)
    log("counter_read", value=value)
    return {"counter": value}


@app.post("/counter")
def increment_counter():
    REQUESTS.labels("increment_counter").inc()
    value = read_counter() + 1
    write_counter(value)
    log("counter_incremented", value=value)
    return {"counter": value}


@app.get("/metrics")
def metrics():
    REQUESTS.labels("metrics").inc()
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
