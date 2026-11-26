# Teste de motion 01 — "Atrito": resultado e comparação de motores

Data: 2026-11-26 · Brief: `motion-01-brief.md` · Código: `motion/cenas/atrito/` (cena.js + som.py)

## Método (comparação justa)

- **Uma única cena** Three.js (`cena.js`), função pura do tempo, e **uma única trilha** (`som.py`,
  sintetizada a partir dos mesmos tempos da cena). Os motores só embrulham, sincronizam e renderizam.
- Mesmo servidor (4 núcleos, GPU por software/SwiftShader), mesmo Chrome headless shell, 4 em paralelo.
- Saída: 1080×1920, 30 fps, 6 s, H.264 + AAC estéreo.

## Resultados medidos

| Critério | HyperFrames 0.9.98 | Remotion 4.0.547 |
|---|---|---|
| Render (6 s, 4 em paralelo) | 2 min 57 s | **2 min 08 s** |
| Render (1 por vez) | 3 min 47 s | — |
| Arquivo | 24 MB (33 Mbps) | 14 MB (18,8 Mbps) |
| Imagem HF × Remotion (SSIM) | 0,974 — praticamente idênticas (diferença = grão e compressão) | |
| Loudness / pico | -17,0 LUFS / -1,6 dB | -17,0 LUFS / -1,5 dB |
| Sincronia de áudio (correlação cruzada) | **0,0 ms** | **0,0 ms** |
| Licença | **Apache 2.0** (livre, qualquer tamanho de empresa) | Grátis p/ pessoa física e empresa com **até 3 funcionários**; acima disso, licença paga |
| Telemetria | **Ligada por padrão** (PostHog). Desligada: `HYPERFRAMES_NO_TELEMETRY=1`, `DO_NOT_TRACK=1`. Skill própria pede para enviar "usage note" — não enviamos | Nenhuma encontrada |
| Autoria | HTML + atributos `data-*`, sem build | React/TypeScript, build com webpack |
| Verificação embutida | `hyperframes check`: lint, layout, contraste, áudio, "craft" (passou sem erros) | Não equivalente |
| Maturidade | jovem (0.9.x), muitas versões | madura (4.0.x), ecossistema grande |
| Dependência de rede por padrão | modelo inicial carrega GSAP de CDN (trocado por cópia local) | nenhuma |
| Integração com Three.js | protocolo `hf-seek` + `buildReady` | `delayRender`/`continueRender` por quadro |

## Conclusões

1. **A qualidade visual não vem do motor.** Com a mesma cena, os dois entregam a mesma imagem.
   A capacidade criativa está na camada de cena (Three.js, luz, material, coreografia) e na direção.
   Decisão estrutural: cenas do RUBRA são **independentes de motor** (`render(t)` puro).
2. Remotion foi ~28% mais rápido e gera arquivos mais enxutos; HyperFrames tem licença mais livre e
   um verificador automático útil para o controle de qualidade.
3. A escolha do motor principal depende de um dado da RUBRA: **número de funcionários** (licença Remotion).

## Avaliação criativa da cena (honesta)

Estado: **Validado tecnicamente · NÃO validado criativamente.**

Funciona: arco de luz como narrativa (escuro → risco incandescente → ignição → caixa revelada com sombra →
chama isolada → brilho vira letras → brasa); transição motivada; som derivado da ação.

Problemas para a próxima iteração:
- Os primeiros 2,5 s são visualmente vazios: gaveta e fósforo se movem no escuro. Retenção ruim.
  Correção: a luz fria deve recortar a gaveta e a cabeça do fósforo (ou abrir mais perto da ação).
- O campo branco em ~5,0–5,2 s fica chapado por um instante.
- Som verificado por medição e forma de onda, **não por audição** (o Claude não ouve).
- GPU por software: sem profundidade de campo real (BokehPass) para manter tempo de render viável.

## Processo de inspeção que funcionou

Quadros-chave renderizados direto da cena (≈0,8 s/quadro) → folha de contato → crítica → correção,
antes de embrulhar nos motores. 4 rodadas corrigiram: trajetória do fósforo invertida, linha do horizonte
da mesa, contraluz virando "spot de palco", chama de vela, assinatura pequena, mixagem desequilibrada
(detectada pela forma de onda).
