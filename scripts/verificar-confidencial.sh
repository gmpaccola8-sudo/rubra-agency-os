#!/usr/bin/env bash
# Barreira de segurança: bloqueia commits com material confidencial.
# Roda automaticamente antes de cada commit (via .githooks/pre-commit).
# Também pode ser executado manualmente: bash scripts/verificar-confidencial.sh
set -uo pipefail

LIMITE_KB=2048
falhas=0

arquivos=$(git diff --cached --name-only --diff-filter=ACMR)
[ -z "$arquivos" ] && exit 0

while IFS= read -r f; do
  [ -f "$f" ] || continue
  baixo=$(printf '%s' "$f" | tr '[:upper:]' '[:lower:]')

  case "$baixo" in
    clientes/*|*/clientes/*|calibracao/*|entregas/*|demandas/*)
      echo "BLOQUEADO (pasta de cliente/produção): $f"; falhas=1; continue ;;
    *.ttf|*.otf|*.woff|*.woff2|*.eot)
      echo "BLOQUEADO (fonte): $f"; falhas=1; continue ;;
    *.jpg|*.jpeg|*.png|*.webp|*.heic|*.tif|*.tiff|*.psd|*.ai|*.indd|*.mp4|*.mov|*.avi|*.mkv|*.webm|*.mp3|*.wav|*.m4a|*.aac|*.flac|*.zip|*.rar|*.tar.gz)
      echo "BLOQUEADO (mídia ou pacote): $f"; falhas=1; continue ;;
    .env|.env.*|*.key|*.pem|*credentials*.json)
      echo "BLOQUEADO (credencial): $f"; falhas=1; continue ;;
  esac

  kb=$(( $(wc -c < "$f") / 1024 ))
  if [ "$kb" -gt "$LIMITE_KB" ]; then
    echo "BLOQUEADO (arquivo grande, ${kb} KB): $f"; falhas=1; continue
  fi

  # Padrões de chaves e tokens conhecidos
  if git show ":$f" 2>/dev/null | grep -Eq \
     'sk-ant-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{32,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{50,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|xox[baprs]-[A-Za-z0-9-]{10,}'; then
    echo "BLOQUEADO (parece conter chave/token): $f"; falhas=1
  fi
done <<< "$arquivos"

if [ "$falhas" -ne 0 ]; then
  echo
  echo "Commit cancelado. Materiais de clientes, fontes, mídia e credenciais ficam no Google Drive."
  exit 1
fi
exit 0
