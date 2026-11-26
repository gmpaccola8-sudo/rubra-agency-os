---
name: rubra-revisao
description: Controle de qualidade da RUBRA. Use antes de entregar qualquer peça, carrossel, identidade, texto, vídeo ou motion, e quando a Gabriela pedir para analisar, criticar ou melhorar um material (inclusive de terceiros). Crítica em três níveis com evidência e correção concreta; nunca nota de autoavaliação.
version: 1.0.0
---

# RUBRA · Revisão

Revisar é procurar o que impede o trabalho de ser profissional e eficaz — não defender o que foi feito.
Sempre sobre o **resultado real** (imagem renderizada, vídeo exportado, texto final), nunca sobre código
ou descrição.

## Independência

- **Claude Code:** use o agente `rubra-revisor` (contexto separado, vê só o resultado, o briefing e a
  direção). É o padrão para entregas.
- **Chat / Cowork:** não há agente separado. Faça a revisão como etapa distinta: releia o briefing e a
  direção, olhe o resultado como quem vê pela primeira vez, e siga o formato abaixo à risca.

## Os três níveis (nesta ordem)

1. **Técnico — o arquivo funciona?** Formato e tamanho certos; fontes corretas (sem substituta); nada
   cortado ou fora da área segura; contraste legível; vídeo: duração, resolução, sincronia, áudio sem
   estouro, loudness (~ -14 LUFS para redes); impresso: ver backlog de pré-impressão.
   No Claude Code, use as medições: `rubra-grafico/scripts/render.js` (peças) e
   `rubra-video/scripts/inspecionar.py` (vídeo).
2. **Estético — composição, tipografia, acabamento.** Hierarquia (o que domina é o que deveria
   dominar?); leitura na miniatura do celular; alinhamentos, respiro, quebras, viúvas; consistência na
   série; identidade do cliente respeitada; tiques de `rubra-grafico/references/tiques.md` e
   `rubra-texto/references/tells-ptbr.md`.
3. **Publicitário — ideia e eficácia.** O conceito aprovado chegou à execução? Teste de troca (com o
   nome do concorrente, continua fazendo sentido? então é genérico); mensagem e CTA em 3 segundos;
   motivo para parar o dedo e, no carrossel, para deslizar; nenhuma alegação sem base.

Olhe sempre: tamanho real, miniatura e (para hierarquia) a versão desfocada. Vídeo: quadros do início,
meio, fim e de cada corte; ouça/meça o áudio.

## Formato

```
VEREDITO: BLOQUEADA | CORRIGIR | APROVÁVEL (para a Gabriela avaliar)
Bloqueantes (técnico): [peça] problema — evidência
Correções, por impacto (máx. 7): [peça] problema — evidência (o que se vê, onde) — correção concreta
Preservar: o que está funcionando
```

Regras: toda crítica diz onde e o que fazer; sem nota numérica; "APROVÁVEL" não é aprovação — a
validação criativa é da Gabriela. Após corrigir, revise de novo; no máximo 2 ciclos, depois o que restar
vai como ponto em aberto explicado.

## Analisar material de terceiros ou antigo

Mesmo formato, mais: o que a peça tenta fazer, por que funciona ou não (mecanismo), e 3 correções de
maior impacto em ordem. Diferencie preferência pessoal de falha.
