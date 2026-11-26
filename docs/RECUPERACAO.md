# Recuperação do ambiente — RUBRA AGENCY OS

Como o sistema se reconstrói, e o que fazer quando algo falha.

## Onde cada coisa vive

| Camada | Onde | Recupera como |
|---|---|---|
| Código, skills, agentes, scripts, docs | GitHub `gmpaccola8-sudo/rubra-agency-os` (privado) | Clonado automaticamente em cada sessão |
| Dependências Python | `setup/requirements.lock` (versões exatas) | Script de ambiente → `/opt/rubra-venv` |
| Ferramentas do sistema (FFmpeg, Node, Chromium) | Imagem do servidor da nuvem | Já vêm instaladas — versões em `setup/VERSOES.md` |
| Modelos de IA (Whisper, voz de teste) | Hugging Face | Baixados no primeiro uso (cache da sessão) |
| Rede permitida, variáveis, script de ambiente | Ambiente de nuvem `rubra-agency-os` (claude.ai) | Persistente na conta |
| Skills originais da Gabriela | claude.ai + backup no Drive | `RUBRA AGENCY OS / BACKUP` |
| Materiais de clientes, calibração, testes | Google Drive | Não dependem do servidor |

## Sequência automática numa sessão nova

1. O servidor é criado com o ambiente `rubra-agency-os` (rede + variável `HF_HUB_DISABLE_XET=1`).
2. O repositório é clonado.
3. O script de ambiente roda `setup/nuvem.sh`, que:
   - ativa a barreira de confidencialidade (`core.hooksPath`);
   - cria `/opt/rubra-venv` e instala as versões exatas de `setup/requirements.lock`.
4. O Claude lê `CLAUDE.md` e `IMPLEMENTATION-STATUS.md` e continua de onde parou.

## Diagnóstico rápido

```bash
ls /opt/rubra-venv/bin/python && /opt/rubra-venv/bin/python -c "import faster_whisper; print(faster_whisper.__version__)"
git config core.hooksPath          # esperado: .githooks
echo $HF_HUB_DISABLE_XET           # esperado: 1
```

## Falhas conhecidas e correção

| Sintoma | Causa provável | Correção |
|---|---|---|
| `/opt/rubra-venv` não existe | Sessão iniciada em outro ambiente (ex.: Default) | Iniciar a sessão no ambiente `rubra-agency-os`, ou rodar `bash setup/nuvem.sh` a partir da pasta-mãe do repositório |
| Sessão não inicia (erro no script de ambiente) | Falha de rede no `pip install` | claude.ai → menu do ambiente → Editar → Script de configuração; ou iniciar sessão no Default e rodar o script manualmente |
| `403 ... no rule allows host` ao baixar modelo | Host novo do Hugging Face | Adicionar o host ao ambiente (o Claude propõe; Gabriela aprova) |
| `CAS Client Error ... xethub` | Variável `HF_HUB_DISABLE_XET` ausente | `export HF_HUB_DISABLE_XET=1` |
| `open() got an unexpected keyword argument 'metadata_errors'` | PyAV recente × faster-whisper | Já contornado: `transcrever.py` decodifica com FFmpeg |
| Commit bloqueado | Barreira de confidencialidade funcionando | Mover o arquivo para o Drive. Nunca usar `--no-verify` |

## Recuperação total (pior caso)

Se o ambiente de nuvem for apagado:
1. claude.ai/code → novo ambiente chamado `rubra-agency-os`, rede limitada, com os hosts listados em
   `setup/VERSOES.md`, variável `HF_HUB_DISABLE_XET=1` e o script:
   `if [ -d rubra-agency-os ]; then bash rubra-agency-os/setup/nuvem.sh; fi`
2. Iniciar sessão com o repositório selecionado. Tudo o mais se reconstrói.

## Atualizar uma dependência

1. Testar a nova versão numa sessão (tarefa real, resultado inspecionado).
2. `/opt/rubra-venv/bin/pip freeze > setup/requirements.lock`.
3. Registrar em `IMPLEMENTATION-STATUS.md` (o que mudou, por quê, resultado do teste).
4. Commit. A próxima sessão nova usa a versão nova.
