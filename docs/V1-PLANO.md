# RUBRA AGENCY OS 1.0 — plano de entrega

Redefinição da Gabriela (2026-11-26): entregar uma versão operacional, utilizável no dia a dia.
Pesquisa e testes avançados vão para o backlog.

## O que o 1.0 entrega

**8 skills RUBRA** (instaladas no claude.ai → funcionam no Chat, Cowork e Claude Code):

| Skill | Faz | Substitui |
|---|---|---|
| `rubra-os` | Núcleo: identifica a especialidade, consulta o cliente, aplica o método, regra de referências, registra aprovações/rejeições | gabriela-os, cerebro-do-negocio |
| `rubra-direcao` | Conceitos fora do óbvio (mapa do óbvio + 14 mecanismos + análise de referências) | creative-director, visual-explorer |
| `rubra-marca` | Estratégia de marca, identidade, logo/monograma, design.json, guia | identidade-visual-monograma, brand-strategist, kit-de-marca, marca, brand-guardian |
| `rubra-grafico` | Peças, carrosséis, materiais comerciais, apresentações; render + inspeção | carousel-architect, carrossel-instagram, apresentacao-executiva, slides |
| `rubra-texto` | Estratégia de conteúdo, copy, roteiros, bio, anúncios, diagnóstico de perfil | copywriter, content-strategist, conteudo, copy-ads, roteiro, bio, social-media |
| `rubra-video` | Edição de filmagem real (transcrição local, cortes, legendas, áudio) | editor-de-videos |
| `rubra-motion` | Motion e vídeo autoral (Remotion principal, HyperFrames complementar) | rubra-motion-studio, reels-director, criador-de-videos |
| `rubra-revisao` | Crítica em três níveis com evidência, antes de toda entrega | quality-control |

**Agentes** (só no Claude Code): `rubra-revisor`, `rubra-pesquisador`, `rubra-analista-de-midia`.

**Camada de cliente** no Drive: `RUBRA AGENCY OS / CLIENTES / <cliente> /` com `contexto.md`,
`design.json`, `decisoes.md`, `referencias/`, `entregas/` + um modelo de Project do claude.ai por cliente.

## Etapas restantes

| # | Etapa | Quem |
|---|---|---|
| 1 | Aprovar a lista de skills a remover/manter | Gabriela |
| 2 | Escrever as 6 skills que faltam, aproveitando o melhor das antigas | Claude |
| 3 | Empacotar 8 ZIPs + guia de instalação e uso, publicar no Drive | Claude |
| 4 | Agentes no repositório + plugin para o Claude Code local; instalar Remotion no script de ambiente | Claude |
| 5 | Estrutura de clientes no Drive + modelo de Project | Claude |
| 6 | Subir os 8 ZIPs no claude.ai e desativar as skills antigas | Gabriela |
| 7 | Google Drive para computador + app Claude (aba Code) | Gabriela |
| 8 | Teste de aceitação com uma demanda real de cliente, ponta a ponta | juntos |

## Backlog (versões 1.x, conforme demanda real)

- Geração de imagem por API (pesquisa feita; aguarda decisão de custo) → skill `rubra-imagem`
- Pré-impressão e vetor (`rubra-producao`: Ghostscript, Inkscape/vtracer, PDF/X, CMYK)
- Edição de vídeo: testar com filmagem real; b-roll, reenquadramento, cor, trilha com ducking
- Motion: iteração 2 da cena teste; explorar recursos nativos do Remotion e do HyperFrames
- Benchmark gráfico rodada 2 (com imagens) e rodada de identidade visual
- Remote Control: produção na nuvem gravando direto na pasta do Drive
- Rota de resolução cheia do Canva
- Impeccable completo quando houver demanda de site/landing page
