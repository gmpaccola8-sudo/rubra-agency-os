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
  n=$(basename "$d"); f="$d/SKILL.md"
  head -1 "$f" | grep -q '^---$' || { echo "ERRO $n: SKILL.md sem cabeçalho"; exit 1; }
  grep -q "^name: $n$" "$f" || { echo "ERRO $n: name diferente da pasta"; exit 1; }
  grep -q '^description: ' "$f" || { echo "ERRO $n: sem description"; exit 1; }
  v=$(grep -m1 '^version:' "$f" | cut -d' ' -f2)
  (cd "$TMP" && rm -f "$SAIDA/$n.zip" && python3 -c "
import zipfile,os,sys
z=zipfile.ZipFile(sys.argv[1],'w',zipfile.ZIP_DEFLATED)
for r,_,fs in os.walk(sys.argv[2]):
  for x in fs: z.write(os.path.join(r,x))
z.close()" "$(cd "$SAIDA" && pwd)/$n.zip" "$n")
  echo "ok  $n $v  ($(du -h "$SAIDA/$n.zip" | cut -f1))"
done
rm -rf "$TMP"
