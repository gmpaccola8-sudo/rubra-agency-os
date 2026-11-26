#!/usr/bin/env bash
# Empacota as skills RUBRA em ZIPs prontos para enviar em claude.ai → Configurações → Capacidades → Skills.
# Fonte única: pasta skills/ deste repositório. Scripts de vídeo são copiados para dentro de rubra-video.
# Uso: bash setup/empacotar-skills.sh <pasta_saida>
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"; SAIDA="${1:?pasta de saída}"
TMP="$(mktemp -d)"; mkdir -p "$SAIDA"
cp -r "$REPO/skills/." "$TMP/"
mkdir -p "$TMP/rubra-video/scripts"
cp "$REPO"/scripts/video/{transcrever,analisar_falas,montar,inspecionar}.py "$TMP/rubra-video/scripts/"
for d in "$TMP"/*/; do
  n=$(basename "$d")
  # REGRA OBRIGATÓRIA (importador do claude.ai, 2026-11-26 — ver docs/EMPACOTAMENTO.md)
  python3 - "$d/SKILL.md" "$n" <<'PY' || exit 1
import sys, yaml
f, n = sys.argv[1], sys.argv[2]
t = open(f, encoding="utf-8").read()
assert t.startswith("---\n"), f"{n}: SKILL.md precisa começar com ---"
fm = yaml.safe_load(t.split("---")[1])
extra = set(fm) - {"name", "description"}
assert not extra, f"{n}: campos não aceitos no cabeçalho: {extra} (só name e description)"
assert fm["name"] == n, f"{n}: name diferente do nome da pasta"
assert len(fm["description"]) <= 200, f"{n}: description com {len(fm['description'])} caracteres (máximo 200)"
assert "<" not in fm["description"] and ">" not in fm["description"], f"{n}: description com < >"
PY
  (cd "$TMP" && rm -f "$SAIDA/$n.zip" && python3 -c "
import zipfile,os,sys
z=zipfile.ZipFile(sys.argv[1],'w',zipfile.ZIP_DEFLATED)
for r,_,fs in os.walk(sys.argv[2]):
  for x in fs: z.write(os.path.join(r,x))
z.close()" "$(cd "$SAIDA" && pwd)/$n.zip" "$n")
  echo "ok  $n  ($(du -h "$SAIDA/$n.zip" | cut -f1))"
done
rm -rf "$TMP"
