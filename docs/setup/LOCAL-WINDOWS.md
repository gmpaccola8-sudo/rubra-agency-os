# Infraestrutura local (Windows) — plano e procedimento

Decisão da Gabriela (2026-11-26): opção A — Claude Code local + pasta sincronizada do Google Drive.
Fontes: documentação oficial lida em 2026-11-26 (links no fim).

## Arquitetura resultante

```
Servidor na nuvem (render, transcrição, motion)          PC da Gabriela (Windows)
   Claude Code em nuvem  ── Remote Control ──────►  pasta  G:\Meu Drive\RUBRA AGENCY OS\...
                                                         │  (Google Drive para computador)
                                                         ▼
                                                    Google Drive (nuvem) ── sincronização automática
```

- Produção pesada continua na nuvem (o PC tem 7,7 GB e GPU integrada).
- O arquivo final é gravado **na pasta do PC** e o Google Drive para computador sobe sozinho, com
  upload retomável, sem limite de 3 MB e **sem compressão**.
- O Claude Code local (aba Code do app Claude) serve para trabalhar direto nos arquivos e fontes do PC.

## Etapas (uma de cada vez)

| # | Etapa | Status |
|---|---|---|
| 1 | Instalar/confirmar o **Google Drive para computador** e localizar `RUBRA AGENCY OS` no Explorador | ⏳ |
| 2 | Instalar o **app Claude para Windows** e abrir a aba **Code** na pasta `RUBRA AGENCY OS` (modo Manual) | ⏳ |
| 3 | Teste: o Claude local cria um arquivo pequeno na pasta e ele aparece no Drive na web | ⏳ |
| 4 | Ativar **Remote Control** no app e autorizar uma sessão em nuvem a usar a pasta | ⏳ |
| 5 | Teste real: sessão em nuvem renderiza um vídeo e grava o master (sem compressão) na pasta | ⏳ |
| 6 | (Opcional) Git para Windows + login GitHub, para o plugin RUBRA no Claude local | ⏳ |

## Alternativas investigadas para arquivos grandes

| Caminho | Situação |
|---|---|
| Conector Google Drive do claude.ai | ~3,1 MB por chamada. Bom para documentos, não para mídia. **Não é limite do Google Drive**, é do conector. |
| **Google Drive para computador + Remote Control** | Escolhido. Upload retomável feito pelo próprio Drive. |
| API do Drive com upload retomável (OAuth) | Funciona tecnicamente, mas exige projeto no Google Cloud, cliente OAuth e token de atualização guardado; tokens de acesso expiram em 1 h — frágil para uma operação de uma pessoa. Reserva. |
| rclone (sincronização autorizada) | Mesma exigência de OAuth; reserva para lotes grandes. |
| Página privada de revisão (Artifact) | Até 15 MB por arquivo; só para **assistir**, não para entregar ao cliente. Em uso. |

## Pontos não confirmados pela documentação (testar)

- Desempenho do app em 7,7 GB de RAM (sem requisito mínimo publicado).
- Gravação em pasta do Google Drive para computador (bloqueio de arquivo durante sincronização).
- Limite de tamanho de arquivo gravado via Remote Control.
- Se as skills do claude.ai sincronizam para a aba Code do app (documentado para sessões de terminal).

## Fontes

- https://code.claude.com/docs/en/desktop-quickstart.md
- https://code.claude.com/docs/en/desktop.md
- https://code.claude.com/docs/en/remote-control.md
- https://code.claude.com/docs/en/skills.md
- https://code.claude.com/docs/en/plugins/install.md
- https://code.claude.com/docs/en/permission-modes.md
- https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan
