#!/usr/bin/env bash
# Reconstrói o laboratório de motion (fora do repositório) e renderiza o teste "Atrito" nos dois motores.
# Uso: bash motion/montar-laboratorio.sh <pasta_lab>
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"; LAB="${1:?pasta do laboratório}"
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1   # regra RUBRA: telemetria desligada
mkdir -p "$LAB" && cd "$LAB"
[ -f package.json ] || npm init -y >/dev/null
npm install --no-fund --no-audit hyperframes@0.9.98 remotion@4.0.547 @remotion/cli@4.0.547 \
  @remotion/renderer@4.0.547 react@19 react-dom@19 three@0.187.0 gsap@3.13.0 >/dev/null
mkdir -p compartilhado
# Fonte Fraunces 900 (OFL) — baixada, nunca versionada
curl -sf -o compartilhado/fraunces-900.woff2 \
  "https://fonts.gstatic.com/s/fraunces/v38/6NUh8FyLNQOQZAnv9bYEvDiIdE9Ea92uemAk_WBq8U_9v0c2Wa0K7iN7hzFUPJH58njr1a03gg7S2nfgRYIcHhyTB_7TtUs.woff2"
/opt/rubra-venv/bin/python -I "$REPO/motion/cenas/atrito/som.py" "$REPO/motion/cenas/atrito/cena.js" compartilhado/som_bruto.wav >/dev/null
ffmpeg -v error -y -i compartilhado/som_bruto.wav -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 compartilhado/som.wav
# HyperFrames
mkdir -p hf/assets/fonts hf/lib/addons
cp "$REPO/motion/motores/hyperframes/index.html" hf/
cp compartilhado/som.wav hf/assets/; cp compartilhado/fraunces-900.woff2 hf/assets/fonts/
cp node_modules/three/build/three.module.js node_modules/three/build/three.core.js node_modules/gsap/dist/gsap.min.js hf/lib/
cp -r node_modules/three/examples/jsm/postprocessing node_modules/three/examples/jsm/shaders hf/lib/addons/
cp "$REPO/motion/cenas/atrito/cena.js" hf/lib/
# Remotion
mkdir -p rm/src rm/public; ln -sfn ../node_modules rm/node_modules
cp "$REPO"/motion/motores/remotion/src/* rm/src/; cp "$REPO/motion/cenas/atrito/cena.js" rm/src/
cp compartilhado/som.wav compartilhado/fraunces-900.woff2 rm/public/
CHROME=$(ls -d /opt/pw-browsers/chromium_headless_shell-*/*/chrome-headless-shell | head -1)
(cd hf && HYPERFRAMES_BROWSER_PATH="$CHROME" npx hyperframes render --output ../hf-atrito.mp4 --workers 4)
(cd rm && npx remotion render src/index.ts Atrito ../rm-atrito.mp4 --public-dir="$(pwd)/public" \
  --browser-executable="$CHROME" --gl=swangle --concurrency=4)
echo "Pronto: $LAB/hf-atrito.mp4 e $LAB/rm-atrito.mp4"
