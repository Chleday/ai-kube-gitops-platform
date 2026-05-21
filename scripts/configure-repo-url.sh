#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 1 ]]; then
  echo "usage: $0 https://github.com/OWNER/REPO.git"
  exit 1
fi
repo_url="$1"
find bootstrap clusters apps platform -type f \( -name '*.yaml' -o -name '*.yml' \) -print0 \
  | xargs -0 sed -i "s|https://github.com/YOUR_USERNAME/kube-gitops-portfolio.git|${repo_url}|g"
echo "repoURL replaced with: ${repo_url}"
