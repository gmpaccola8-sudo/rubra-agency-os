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
