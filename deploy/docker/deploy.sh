#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -f .env ]]; then
  echo "FATAL: .env not found. Copy .env.docker.example → .env and fill secrets."
  exit 1
fi

# shellcheck disable=SC1091
set -a
# Load USE_HTTPS / HTTP_PORT without exporting unrelated secrets into the shell noise
USE_HTTPS="$(grep -E '^USE_HTTPS=' .env | tail -1 | cut -d= -f2- | tr -d '\r' || true)"
set +a

USE_HTTPS="${USE_HTTPS:-false}"

if [[ "${USE_HTTPS}" =~ ^(true|True|1|yes|YES)$ ]]; then
  COMPOSE=(docker compose -f docker-compose.yml -f docker-compose.prod.yml)
  echo "==> Mode: HTTPS (docker-compose.prod.yml)"
else
  COMPOSE=(docker compose -f docker-compose.yml)
  echo "==> Mode: HTTP (docker-compose.yml) — set USE_HTTPS=true after certbot"
fi

free_host_ports() {
  echo "==> Freeing host ports 80/443 (host nginx/gunicorn if any)..."
  systemctl stop nginx 2>/dev/null || true
  systemctl disable nginx 2>/dev/null || true
  systemctl stop 'gunicorn-*' 2>/dev/null || true
  systemctl disable 'gunicorn-*' 2>/dev/null || true
}

free_host_ports

echo "==> Build + up"
"${COMPOSE[@]}" build
"${COMPOSE[@]}" up -d

echo "==> Waiting for healthz..."
SITE_HOST=""
if grep -qE '^SITE_URL=' .env; then
  SITE_HOST="$(grep -E '^SITE_URL=' .env | tail -1 | sed -E 's#^SITE_URL=https?://([^/:]+).*#\1#' | tr -d '\r')"
fi

for _ in $(seq 1 30); do
  if [[ "${USE_HTTPS}" =~ ^(true|True|1|yes|YES)$ ]]; then
    if [[ -n "${SITE_HOST}" ]] && curl -sfk "https://127.0.0.1/healthz/" -H "Host: ${SITE_HOST}" >/dev/null 2>&1; then
      echo "==> HTTPS healthz OK (${SITE_HOST})"
      exit 0
    fi
  elif curl -sf "http://127.0.0.1/healthz/" >/dev/null 2>&1; then
    echo "==> HTTP healthz OK"
    exit 0
  fi
  sleep 2
done

echo "WARN: /healthz/ did not respond in time. Check logs:"
echo "  ${COMPOSE[*]} logs --tail=50"
"${COMPOSE[@]}" ps
exit 1
