#!/usr/bin/env python3
from pathlib import Path
import sys
try:
    import yaml
except ImportError:
    print('PyYAML is required: pip install pyyaml', file=sys.stderr)
    sys.exit(2)

root = Path(__file__).resolve().parents[1]
errors = 0
for path in sorted(root.rglob('*.yaml')) + sorted(root.rglob('*.yml')):
    if '.git' in path.parts:
        continue
    try:
        with path.open() as f:
            list(yaml.safe_load_all(f))
        print(f'OK {path.relative_to(root)}')
    except Exception as e:
        errors += 1
        print(f'FAIL {path.relative_to(root)}: {e}', file=sys.stderr)
if errors:
    sys.exit(1)
print('All YAML files parsed successfully')
