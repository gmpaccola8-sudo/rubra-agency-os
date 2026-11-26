#!/usr/bin/env bash
# Script de ambiente da nuvem: roda a cada sessão nova, antes do Claude começar.
# Reinstala as dependências testadas para que nada se perca entre sessões.
set -euo pipefail
if [ -d rubra-agency-os ]; then
  git -C rubra-agency-os config core.hooksPath .githooks
  python3 -m venv /opt/rubra-venv
  /opt/rubra-venv/bin/pip install -q --disable-pip-version-check -r rubra-agency-os/setup/requirements.lock
fi
