# RUBRA AGENCY OS 1.0 — guia de instalação e uso

## O que é cada coisa

| Peça | Onde mora | Para quê |
|---|---|---|
| **8 skills RUBRA** | sua conta claude.ai (instaladas uma vez) | aparecem sozinhas no Chat, no Cowork e no Claude Code |
| **Pasta de cada cliente** | Google Drive → `RUBRA AGENCY OS / CLIENTES` | identidade, contexto, decisões, referências, entregas |
| **Project por cliente** | claude.ai → Projects | conversa já sabe qual é o cliente |
| **Agentes e ferramentas** (revisor, pesquisador, render, vídeo, motion) | repositório GitHub, usado pelo Claude Code | produção e inspeção de verdade |

Instala **uma vez** (global): as 8 skills. Configura **por cliente**: uma pasta + um Project.
Nada mais se repete.

## Instalação (uma vez, ~15 min)

### 1. Subir as 8 skills
1. Abra o Google Drive → `RUBRA AGENCY OS` → `INSTALAR` e baixe os 8 arquivos `.zip`
   (não abra os zips; o claude.ai recebe o zip fechado).
2. No navegador, abra **claude.ai** → clique no seu nome/ícone (canto inferior esquerdo) →
   **Configurações** → **Capacidades** (ou "Capabilities").
3. Na área **Skills**, clique em **Enviar skill** / **Upload skill** e escolha `rubra-os.zip`.
4. Repita para os outros 7.
5. **Confirma:** a lista de skills mostra as 8 com nome `rubra-…` e o botão ativado.

### 2. Desativar as antigas (depois do passo 1)
Na mesma lista, **desligue** (não exclua) as 32 skills aprovadas para remoção. É reversível.
Excluir só depois de 2–3 semanas de uso sem sentir falta. Todas estão no backup do Drive.

## Para cada cliente (~5 min)

1. Peça no Chat: **"novo cliente: <nome>"**. O sistema faz as perguntas que faltarem e devolve
   `contexto.md` (e `design.json` se já houver identidade).
2. No Drive, em `CLIENTES`, crie a pasta do cliente com as subpastas
   `marca`, `referencias`, `fotos`, `entregas` e salve ali os arquivos gerados + logo original e fontes.
3. No claude.ai, crie um **Project** chamado `RUBRA · <cliente>`, cole as instruções que o sistema
   entregou e suba `contexto.md`, `design.json` e `decisoes.md` em **Conhecimento**.

## Uso no dia a dia

Abra o Project do cliente e peça naturalmente:
- "Crie uma campanha de lançamento para…", "Desenvolva três direções de identidade."
- "Faça um carrossel sobre…", "Crie uma peça para…", "Analise este material."
- "Escreva a legenda", "Planeje o conteúdo de dezembro."
- "Aprovado" / "Não gostei porque…" → o sistema registra em `decisoes.md`.

O sistema escolhe a especialidade, consulta o cliente, pede referências quando a criação é nova
e relevante, cria, revisa e entrega.

## O que cada ambiente faz

| Quero… | Use |
|---|---|
| Estratégia, conceitos, textos, direção, crítica, peças simples | **Chat** (no Project do cliente) |
| Peças renderizadas e inspecionadas, editar vídeo, motion | **Claude Code** em claude.ai/code, com o repositório `rubra-agency-os` e o ambiente `rubra-agency-os` |
| Trabalhar com arquivos e fontes do seu PC | **App Claude → aba Code** (configuração local, em andamento) |

## Limites desta versão (estão no backlog)

- Imagens fotográficas por IA: ainda não (sem API contratada). Use fotos reais; sem foto, solução gráfica.
- Pré-impressão (PDF para gráfica, CMYK, sangria): ainda não automatizada.
- Edição de vídeo: protótipo; o primeiro vídeo real será o teste de validação.
- Arquivos de vídeo grandes chegam ao Drive quando a configuração local estiver pronta.
