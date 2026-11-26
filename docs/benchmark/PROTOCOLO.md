# Protocolo do benchmark gráfico A/B/C

| Condição | Como roda |
|---|---|
| A | Agente novo, sem nenhuma skill (ferramenta Skill proibida) |
| B | Agente novo, com as skills criativas anteriores da RUBRA (gabriela-os, creative-director, visual-explorer, copywriter, carousel-architect, brand-guardian, quality-control) |
| C | Agente novo, seguindo os arquivos do novo sistema (`skills/rubra-direcao`, `skills/rubra-grafico`) + revisão independente (`agents/rubra-revisor`) e um ciclo de correção |

Controles: mesmo briefing (`briefing-XX-*.md`), mesmas fontes, mesmo método de saída (PNG 1080×1350
via Playwright), agentes sem acesso ao trabalho das outras condições nem a estes documentos.
Os arquivos das skills do novo sistema não podem citar o briefing do benchmark (verificado por busca
antes da rodada 01: referências específicas foram removidas).

Avaliação: as peças renderizadas lado a lado vão para a Gabriela, que avalia nos três níveis
(técnico, estético, publicitário). Medidas objetivas (render.js) e a crítica do revisor são
evidência de apoio, não nota final. Nenhuma pontuação atribuída pelo próprio sistema decide o resultado.

## Rodada 01 — Miolo (2026-11-26)

Diferenças de condição registradas:
- A e B receberam os arquivos Instrument Serif com nomes trocados (erro nosso). Ambos perceberam e
  corrigiram o mapeamento. C recebeu os arquivos já corrigidos.
- A e B: ~8 min e ~2 min. C: ver resultado.
