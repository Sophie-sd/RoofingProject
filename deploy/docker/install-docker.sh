#!/usr/bin/env bash
set -euo pipefail

if command -v docker >/dev/null 2>&1; then
  echo "==> Docker already installed: $(docker --version)"
  exit 0
fi

echo "==> Installing Docker..."
curl -fsSL https://get.docker.com | sh
systemctl enable --now docker

echo "==> Docker installed: $(docker --version)"
