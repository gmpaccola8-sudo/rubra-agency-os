---
name: rubra-grafico
description: Execução de peças gráficas estáticas da RUBRA — anúncios, posts, carrosséis, stories, materiais comerciais, cartazes — renderizadas em PNG/PDF e inspecionadas antes da entrega. Use depois que a direção estiver definida (rubra-direcao) ou para desdobrar uma direção aprovada. Não use para sites/interfaces nem para vídeo.
version: 1.0.0
---

# RUBRA · Peças gráficas

Executa uma direção já escolhida (`direcao.md`). Se não houver direção para uma peça nova e
relevante, pare e rode `rubra-direcao` primeiro.

## 1. Antes de compor

- Carregue a identidade do cliente (`marca/design.json`): fontes, cores e proporções de uso, logo.
  Use só os arquivos oficiais. Nunca redesenhe um logo.
- Releia em `direcao.md`: o elemento único da ousadia, a hierarquia de leitura e as 3 proibições.
- Abra `references/tiques.md` e mantenha à vista durante a composição.

## 2. Compor

- **Formato e zonas seguras** (`references/formatos.md`): respeite as áreas cobertas pela interface
  da plataforma.
- **Uma ousadia só.** O resto fica quieto: alinhado, com respiro, sem elementos de apoio que não
  carreguem informação.
- **Hierarquia por escala e posição**, não por quantidade de estilos. Até 3 níveis de texto por peça.
  Razão título/texto de pelo menos 3:1 quando o título é o protagonista.
- **Texto é material.** Corte palavras até o mínimo que ainda diz a mensagem. Texto do cliente
  e fatos do briefing; nunca invente dado, prova, número ou depoimento.
- **Carrossel:** a capa promete, cada slide entrega uma coisa, o último pede uma ação. A ligação
  entre slides vem da ideia (e do deslizar, se for o mecanismo), não de numeração decorativa.

## 3. Renderizar e inspecionar (obrigatório)

Escreva cada peça como HTML/CSS (ou SVG) e renderize com o script — nunca entregue sem o render:

```bash
node <skill>/scripts/render.js <pasta_html> <pasta_saida> --largura 1080 --altura 1350
```

O script gera, por peça: `nome.png` (final), `nome@miniatura.png` (como aparece no feed do celular),
`nome@desfoque.png` (teste de hierarquia: o que ainda se lê desfocado é o que domina) e
`relatorio.json` com **falhas objetivas**: fonte que não carregou (fallback), texto transbordando ou
cortado, elementos fora da área segura, contraste de texto abaixo do mínimo.

Corrija toda falha objetiva e renderize de novo. Depois **olhe** as três imagens de cada peça:
- Na miniatura, a mensagem principal ainda se lê?
- No desfoque, o que domina é o que a direção definiu como 1º nível?
- Algum item de `tiques.md` apareceu?

## 4. Revisão independente

A revisão crítica é feita pelo agente `rubra-revisor`, que vê só as imagens renderizadas, o
briefing e a direção — não o código nem o raciocínio de quem produziu. Aplique as correções e
renderize de novo. Limite: 2 ciclos de revisão por peça; o que restar vai para a Gabriela como
ponto em aberto, com a explicação.

## 5. Entrega

PNG final + fonte editável (HTML/SVG) + `direcao.md` + o relatório do revisor. Para impressão,
seguir `rubra-producao` (PDF, CMYK, sangria) antes de declarar pronto para gráfica.

## Recursos

- `references/tiques.md` — reflexos de peça genérica, cada um com a alternativa positiva.
- `references/formatos.md` — dimensões e zonas seguras.
- `scripts/render.js` — render + inspeção objetiva (Playwright).
