# RUBRA AGENCY OS

Infraestrutura operacional da RUBRA: skills, agentes, comandos, scripts e documentação que permitem
ao Claude trabalhar como uma agência multidisciplinar, com produção real e inspeção do resultado.

**Estado atual e próxima ação:** [`IMPLEMENTATION-STATUS.md`](IMPLEMENTATION-STATUS.md)

## O que mora onde

| Onde | O quê |
|---|---|
| Este repositório (privado) | Código, skills, agentes, comandos, scripts, documentação, histórico de versões |
| Google Drive → `RUBRA AGENCY OS` | Backups, documentação espelhada, amostras de calibração |
| Google Drive → pastas de clientes | Logos originais, fontes, fotos, vídeos, entregas |

Nada de clientes, fontes, mídia ou credenciais entra aqui — bloqueado por `.gitignore`
e por verificação automática antes de cada commit.

## Estrutura

```
CLAUDE.md                  instruções carregadas em toda sessão neste repositório
IMPLEMENTATION-STATUS.md   continuidade: o que foi feito, decidido, testado e o que vem a seguir
docs/                      auditorias, decisões, manuais
scripts/                   scripts executáveis do sistema
.githooks/                 verificações automáticas de commit
```

Pastas futuras (criadas quando tiverem conteúdo testado): `skills/`, `agents/`, `commands/`,
`biblioteca/`, `setup/`.

## Ativar a proteção num clone novo

```bash
git config core.hooksPath .githooks
```
