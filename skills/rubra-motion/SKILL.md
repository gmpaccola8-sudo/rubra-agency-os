---
name: rubra-motion
description: "Motion design da RUBRA: teasers, Reels do zero, vídeos publicitários, animação, cenas 3D e sonoplastia com render MP4. Use quando não houver filmagem para editar."
---

# RUBRA · Motion

Estado: motores **validados tecnicamente**; qualidade criativa ainda em calibração.

## Onde roda

- **Claude Code em nuvem:** produção e render. Monte o laboratório com
  `bash motion/montar-laboratorio.sh <pasta>` (instala Remotion, HyperFrames, Three.js localmente).
- **Chat / Cowork:** conceito, roteiro visual, storyboard, styleframes como imagem/HTML; render no Claude Code.

## Antes de animar

1. Contexto e referências do cliente (regra permanente). Sem referência para um estilo novo: peça ou
   pesquise e analise (`rubra-direcao/references/referencias.md`, item 7 — ritmo e transições).
2. Conceito com `rubra-direcao`: uma metáfora visual central e uma narrativa (gancho, progressão,
   clímax, fecho). **Slide animado não é motion**: texto entrando e saindo não é ideia.
3. Roteiro por cena: o que se vê, câmera, o que se transforma, que movimento leva à próxima cena,
   som de cada ação, duração.

## Construir

- **Cena independente de motor:** escreva a cena como função pura do tempo (`render(t)`), sem relógio
  nem aleatório sem semente. Assim qualquer motor a renderiza e o resultado é reprodutível.
  Exemplo completo: `motion/cenas/atrito/` (Three.js: material procedural, luz motivada, sombras,
  partículas, câmera, transição por luz).
- **Teste a cena mais difícil primeiro** (3–5 s) com quadros-chave renderizados e olhados antes do vídeo inteiro.
- **Luz, material e profundidade** vêm da cena; transições são motivadas por movimento ou forma
  (match cut, movimento contínuo), corte seco como padrão.
- **Som junto com a imagem:** derive o som dos mesmos tempos da cena (`motion/cenas/atrito/som.py`):
  cada ação visível tem seu som; amplitude acompanha a velocidade do objeto. Trilhas e efeitos de
  terceiros só com licença comprovada.

## Motores

| Motor | Quando | Atenção |
|---|---|---|
| **Remotion** (principal) | composições React, cenas 3D (`delayRender`/`continueRender`), legendas, projetos com componentes reutilizáveis | licença gratuita para operação individual / até 3 pessoas |
| **HyperFrames** (complementar) | composição em HTML puro, sobreposições, peças com checagem automática (`hyperframes check`) | sempre `HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1`; dependências locais, sem CDN; não enviar "usage note" |

Render no servidor usa GPU por software: ~20–30 s por segundo de vídeo em 1080×1920. Planeje.

## Inspecionar e entregar

Quadros-chave em folha de contato, sincronia de áudio (correlação), loudness, duração e codec
(`rubra-video/scripts/inspecionar.py`); depois `rubra-revisao`. Entregue MP4 H.264/AAC + código-fonte da cena
+ roteiro. Para revisão rápida, página privada (até 15 MB); master sem compressão vai para a pasta do
cliente no Drive.
