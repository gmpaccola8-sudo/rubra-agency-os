# Ferramentas gráficas — investigação 01

Data: 2026-11-26. Fontes primárias lidas: código e SKILL.md de cada ferramenta (clonados em pasta
isolada, nada instalado no ambiente). Estado de todas: **Planejado → leitura/auditoria concluída;
nenhuma instalada.**

## O que cada uma é de verdade

| Ferramenta | Origem / licença | Foco real | Executa algo? | Risco / atenção |
|---|---|---|---|---|
| **Impeccable** 4.11.1 | pbakaus · Apache 2.0 | Interfaces (sites, apps, design system) | Sim: binário próprio (`impeccable shot`, `context`, `font-fetch`), baixado do GitHub Releases no 1º uso, com checksums | Binário externo baixado em tempo de execução (verificar checksum antes de usar); sem telemetria encontrada |
| **Taste Skill** 2.5.1 | Leonxlnx · MIT | Sites institucionais ("nível figma.com / x.ai") | Sim: `gate.mjs` (verificador em navegador), `copy-lint.mjs` | Instala **hook Stop** que roda Node a cada parada do agente; regras rígidas de site (uma seção por tela, micro-hover); scripts consultam jsDelivr e Wikimedia |
| **Canvas Design** | Anthropic (oficial) | Pôsteres / arte estática PNG/PDF via "filosofia visual" | Não (instrução) + **~40 famílias de fonte OFL** embutidas | Arte 90% imagem / 10% texto: conflita com peça publicitária (mensagem, marca, CTA) |
| **Frontend Design** | Anthropic (oficial) | Direção visual de UI | Não (instrução, 71 linhas) | Nenhum |
| **Algorithmic Art** | Anthropic (oficial) | Arte generativa p5.js com semente | Não (instrução + template) | Nenhum |

## O que é aproveitável para publicidade, branding e peças gráficas

Nenhuma delas foi feita para peça publicitária impressa ou de rede social. O valor está em
**mecanismos** que funcionam independentemente da mídia:

1. **Lista nominal de reflexos genéricos** (Frontend Design §calibração; Impeccable "Refuse").
   Nomeia os padrões em que o design gerado por IA se aglomera:
   creme + serifa de alto contraste + terracota; preto + um acento ácido; layout de jornal com filetes;
   kit de cards SaaS; rótulo em caixa alta acima de todo título; separadores "A · B · C";
   "PALAVRA — fragmento"; seta "→" em todo link; uma palavra do título em itálico/cor;
   numeração 01/02/03 sem sequência real; texto em gradiente; máscara geométrica fingindo recorte de foto;
   fonte do sistema como display; emoji no lugar de ícone.
   → **Adotar** como verificação do revisor, em versão RUBRA para peças (não só web).
2. **Teste de divergência** (Frontend Design): antes de executar, verificar se um briefing parecido
   levaria ao mesmo plano; se sim, a escolha é default, não decisão. → **Adotar** no método de criação.
3. **"Gaste a ousadia em um lugar só"** + "tire um acessório antes de sair" (Frontend Design).
   → Princípio de composição para peças.
4. **Proibir sempre com um movimento positivo ao lado** (Taste Skill, copy-tells): regra que só proíbe
   faz o modelo trocar pelo substituto mais próximo; o específico vem do insumo (briefing, palavras do
   cliente), nunca de regra de estilo. → **Adotar** na escrita das skills RUBRA.
5. **Tells de texto escrito por IA** (Taste Skill copy-tells, nov/2026): palavras e estruturas
   denunciadoras com a correção de cada uma. → **Adaptar para PT-BR** em `rubra-texto` + linter.
6. **Filosofia antes da execução** (Canvas Design). → Útil para peças autorais/pôsteres, não para
   anúncio com CTA.
7. **Arte generativa com semente** (Algorithmic Art). → Elementos gráficos autorais (texturas, padrões,
   ilustrações abstratas) derivados do conceito, reproduzíveis.
8. **Biblioteca de fontes OFL** (Canvas Design). → Repertório tipográfico livre para uso comercial,
   sempre subordinado à identidade do cliente.
9. **Verificar olhando o render** (todas): coincide com o método já adotado no RUBRA.

## Decisão provisória

- Não instalar Impeccable nem Taste Skill como skills ativas: o foco em web e os hooks/binários
  trariam ruído e conflito de acionamento para pedidos de peça gráfica.
- Incorporar os mecanismos 1–5 e 7 nas skills RUBRA (com crédito e licença registrados), escritos
  para peça publicitária e identidade, não para site.
- Reavaliar o Impeccable inteiro quando houver demanda de site/landing page de cliente.
- A prova de que isso melhora o resultado vem do benchmark A/B/C — não desta leitura.

## Achado sobre o próprio briefing do benchmark

A identidade fictícia "Miolo" (creme #F2EBDD + Instrument Serif + terracota #C4572B) cai exatamente no
primeiro aglomerado listado pela Anthropic. Foi mantida de propósito: simula uma identidade **fixada pelo
cliente** que tende ao genérico — teste mais difícil e realista. Lição para o RUBRA: ao **criar**
identidades, checar a paleta e a tipografia contra os aglomerados conhecidos.
