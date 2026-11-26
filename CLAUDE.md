# RUBRA AGENCY OS — instruções de sessão

Repositório do sistema operacional da RUBRA (estúdio de branding, design, conteúdo e audiovisual).
Diretora geral, comercial e criativa: Gabriela. Ela não é programadora.

## Ao iniciar qualquer sessão

1. Leia `IMPLEMENTATION-STATUS.md`. A seção "Próxima ação" diz onde paramos.
2. Não refaça diagnóstico já registrado. Continue a partir do status.
3. Ao terminar uma etapa, atualize o status (etapas, decisões, testes, problemas, próxima ação),
   faça commit e push. Se o status mudar, envie também a cópia para o Drive
   (`RUBRA AGENCY OS / DOCUMENTACAO`).

## Regras invioláveis

- **Nunca versionar:** materiais de clientes, fontes licenciadas, fotografias, vídeos, áudios,
  credenciais, chaves de API. Eles ficam no Google Drive. O `.gitignore` e o hook
  `scripts/verificar-confidencial.sh` bloqueiam; não contorne (`--no-verify` é proibido).
- Ative o hook em cada clone novo: `git config core.hooksPath .githooks`.
- Não alterar nem excluir as skills originais da Gabriela no claude.ai sem aprovação explícita.
  Backup: Drive → `RUBRA AGENCY OS / BACKUP`.
- Não contratar nem usar serviço pago sem apresentar custo e obter aprovação.
- Não instalar ferramenta externa sem verificar origem, licença, dependências, scripts de instalação,
  telemetria e envio de dados. Skills de terceiros passam pela skill `auditor-de-skills`.
- Ferramenta instalada ≠ ferramenta funcional. Só registre como funcional após uma tarefa real
  com resultado inspecionável.

## Regra permanente: referências antes de criar

Nenhuma produção criativa relevante (campanha, identidade, peça autoral, novo estilo de vídeo,
motion) começa sem:
1. consultar o contexto do cliente (pasta do cliente, decisões, aprovações e rejeições anteriores);
2. verificar arquivos e referências existentes;
3. identificar informações indispensáveis ausentes;
4. pedir referências à Gabriela quando faltarem — ou, se ela não tiver, pesquisar referências
   profissionais e apresentá-las;
5. extrair das referências **mecanismos** (por que funciona: composição, ritmo, tipografia, luz,
   narrativa), nunca layouts para reproduzir;
6. apresentar direções genuinamente distintas e validar antes da produção final.

Exceção: desdobramentos de direção já aprovada e demandas simples (modo PRODUÇÃO) seguem com autonomia.
Nenhuma técnica (zoom, legenda animada, b-roll, transição) é obrigatória: cada uma precisa servir
à identidade, ao público e ao objetivo daquele cliente.

## Autonomia operacional (autorizada pela Gabriela em 2026-11-26)

Avance sem pedir aprovação em testes técnicos e etapas internas já autorizadas.
Peça participação apenas para: decisões criativas relevantes, instalações não autorizadas, custos,
novas permissões, acesso a informação confidencial, arquivos/referências, e escolhas que mudem a
arquitetura de forma significativa.

## Estados de maturidade (usar sempre no status)

`Planejado` → `Instalado` → `Testado (simulado)` → `Testado (material real)` →
`Validado tecnicamente` → `Validado criativamente` → `Aprovado para produção`

Um teste técnico nunca promove uma capacidade a "pronta". Validação criativa e aprovação para
produção dependem da Gabriela.

Toda avaliação criativa separa três níveis (nenhum substitui o outro):
- **Técnico:** o arquivo funciona (formato, fontes, nada cortado, áudio, codec).
- **Estético:** composição, tipografia, hierarquia, acabamento.
- **Publicitário:** conceito original, direção estratégica, narrativa visual, capacidade de despertar interesse.
Uma ferramenta que só atinge o nível técnico não está aprovada para produção.

## Universalidade

Skills, scripts, motores e o revisor são universais: nunca citam um cliente, briefing ou estética
específica. Identidade, referências, preferências e decisões de cada cliente ficam na pasta do cliente.

## Comunicação com a Gabriela

- Português, direto, humano, sem jargão desnecessário.
- Quando depender dela: **uma etapa por vez**, com onde estar, onde clicar, o que aparece na tela,
  como confirmar e o que responder.
- Execute você mesmo tudo o que estiver autorizado e ao seu alcance.

## Ambiente

- PC da Gabriela: Windows, 7,7 GB RAM utilizáveis, GPU integrada Intel UHD. Não rodar render pesado lá.
- Produção pesada (render, transcrição, motion) roda no Claude Code em nuvem.
- Sessões em nuvem são temporárias: tudo que importa vai para este repositório (código/docs)
  ou para o Drive (materiais).
