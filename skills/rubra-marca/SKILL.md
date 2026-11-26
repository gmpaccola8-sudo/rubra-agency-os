---
name: rubra-marca
description: "Branding da RUBRA: posicionamento, identidade visual, logo, monograma, paleta, tipografia, aplicações, guia de marca e o design.json de cada cliente."
---

# RUBRA · Marca

## 1. Estratégia antes da estética

Antes de qualquer desenho, registre (no `contexto.md` do cliente):
problema → objetivo → percepção atual → percepção desejada → público → concorrentes e como se
apresentam → diferenciação real (compreensível e sustentável) → personalidade → mensagem central.
Não aceite posicionamento genérico ("qualidade", "excelência", "feito com amor"). Não crie slogan só
porque soa bonito.

Num redesenho, liste 3–4 causas **concretas** de por que a marca atual não funciona (cor, letra,
símbolo, sistema). Separe o que é pedido do cliente (CONFIRMADO) do que é proposta sua.

## 2. Referências cedo

Pergunte se existe algum logo ou identidade que a pessoa AMA e o que evitar. Uma referência certeira
economiza rodadas. Use os princípios (traço, construção, respiro), nunca a composição.
Análise: `rubra-direcao/references/referencias.md`.

## 3. Rodadas de conceito

- 3 conceitos realmente diferentes por rodada, numa prancha única comparável, cada um com uma frase de
  intenção. Diga qual você defende e por quê.
- A diferença está no **mecanismo** (onde e como o símbolo encontra as letras; que ideia a marca
  carrega), não em cor ou posição.
- Separe decisões: monograma/símbolo independe da fonte; teste fontes ao lado do símbolo escolhido.
- Desenhe em SVG com cuidado: proporção real do símbolo, peso de traço igual ao da letra, pontas
  coerentes com a fonte. Renderize a prancha e olhe (Claude Code: `rubra-grafico/scripts/render.js`;
  Chat: artifact) — em tamanho grande e em 32 px.
- Não crie significado ou storytelling para um símbolo sem confirmação do cliente.

## 4. Princípios que costumam vencer (aprendidos em projetos da RUBRA)

- A letra é protagonista. O símbolo nasce do traço ou se abriga no espaço vazio da letra.
- Traço fino e uniforme, pontas arredondadas, muito respiro, uma cor.
- Humor discreto: uma brincadeira de forma (o símbolo no lugar do acento ou do pingo), nunca um desenho fofo.

## 5. Costumam ser rejeitados

- Símbolo em silhueta pesada ou com cara de clip-art.
- Formas geométricas em laço ou gota presas num ponto só (hélice).
- Símbolo literal com as letras dentro dele (vira selo).
- Letra cursiva de convite e serifas genéricas.
- Paleta saturada ou degradê.
- Os aglomerados de design gerado por IA: creme + serifa de alto contraste + terracota; preto + um acento
  ácido. Ao **criar** identidade, fuja deles salvo pedido explícito.

## 6. Fechamento de uma opção

Uma prancha por opção, sempre no mesmo formato: monograma, logo (símbolo integrado ao nome, porque são
usados separados), negativo, perfil do Instagram, cartão de visita, tipografia, paleta com proporção de
uso e personalidade. O descritor (ex.: "psicóloga clínica") centralizado sob o nome.
Teste de escala: o logo funciona a 16 px (favicon), 32 px (perfil) e em uma cor.

## 7. design.json (padrão de todo cliente)

Na aprovação final, gere o `design.json` e salve na pasta do cliente:

```json
{
  "marca": "Nome",
  "versao": "1.0 · AAAA-MM-DD",
  "logo": { "arquivos": ["marca/logo.svg", "marca/monograma.svg"], "area_de_respiro": "altura do x",
            "tamanho_minimo_px": 24, "nunca": ["recriar", "distorcer", "mudar cor fora da paleta"] },
  "cores": [
    { "nome": "Base", "hex": "#RRGGBB", "uso": "fundos", "proporcao": "60%" },
    { "nome": "Texto", "hex": "#RRGGBB", "uso": "texto principal", "proporcao": "25%" },
    { "nome": "Acento", "hex": "#RRGGBB", "uso": "um destaque por peça", "proporcao": "≤5%" }
  ],
  "tipografia": {
    "titulos": { "familia": "…", "pesos": [400], "arquivo": "marca/fontes/…", "licenca": "OFL | comprada" },
    "texto": { "familia": "…", "pesos": [400, 500], "arquivo": "…", "licenca": "…" }
  },
  "fotografia": "luz, enquadramento, tratamento, o que nunca",
  "tom_de_voz": "3–5 traços com exemplo de frase certa e errada",
  "fazer": ["específico desta marca"],
  "evitar": ["específico desta marca"],
  "referencias_aprovadas": ["referencias/…"],
  "referencias_rejeitadas": ["referencias/…"]
}
```

Regras: hex reais com contraste legível; fontes com arquivo e licença registrados (fonte licenciada
fica no Drive, nunca no GitHub); "fazer" e "evitar" específicos, nunca genéricos.

## 8. Arquivos de logo

Sempre usar o arquivo original do cliente. Se só existir imagem (PNG/JPG), avise que vetorizar exige
conferência manual; nunca entregue vetor "recriado de memória". Para gráfica, o arquivo final precisa
ser vetor real (sem imagem embutida), conferido em ampliação. Pré-impressão completa está no backlog
(`rubra-producao`, versão futura).
