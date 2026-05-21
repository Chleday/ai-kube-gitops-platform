#!/usr/bin/env python3
from pathlib import Path
import sys

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

root = Path(__file__).resolve().parents[1]
apps_file = root / "clusters/homelab/apps.yaml"

for doc in yaml.safe_load_all(apps_file.read_text()):
    if not isinstance(doc, dict):
        continue
    if doc.get("kind") != "Application":
        continue
    metadata = doc.get("metadata") or {}
    name = metadata.get("name")
    if name:
        print(name)
