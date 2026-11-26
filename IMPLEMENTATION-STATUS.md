# RUBRA AGENCY OS — IMPLEMENTATION-STATUS

> Documento de continuidade. Qualquer sessão nova começa lendo este arquivo.
> Cópia mestre: Google Drive → `RUBRA AGENCY OS / DOCUMENTACAO / IMPLEMENTATION-STATUS.md`
> Cópia mestre: repositório GitHub privado `gmpaccola8-sudo/rubra-agency-os`. O Drive guarda um espelho.

Última atualização: 2026-11-26 · Fase atual: **03 — Pesquisa técnica e testes** · pipeline de vídeo real ✅ validado com mídia sintética

---

## Próxima ação

**Claude:** continuar a Fase 03 — motion (HyperFrames × Remotion, teste com cena real de 3–5 s),
depois Impeccable × Taste Skill, vetor/pré-impressão (Inkscape, vtracer, Ghostscript) e pesquisa
de geração de imagem e vídeo por IA (custos, licença, qualidade).
**Gabriela (sem urgência):** vídeo bruto real em `CALIBRACAO/03-VIDEO-BRUTO-TESTE` (para validar o
pipeline com voz humana) e as demais amostras; teste de abertura do .zip do backup.

---

## Etapas

| Fase | Etapa | Status |
|---|---|---|
| 01 | Inventário do ambiente (skills, conectores, ferramentas) | ✅ concluído |
| 02 | Backup das 55 skills no Drive | ✅ concluído e verificado (ver abaixo) |
| 02 | Matriz individual das 55 skills | ✅ entregue — aguarda aprovação |
| 02 | Teste de recuperação do backup no Windows | ⏳ Gabriela |
| 04 | Conta GitHub + repositório privado | ✅ `gmpaccola8-sudo/rubra-agency-os` (privado) |
| 04 | Conexão GitHub ↔ claude.ai (app Claude, só este repositório) | ✅ |
| 04 | Estrutura do repositório + commit inicial | ✅ |
| 04 | Barreira contra material confidencial (.gitignore + hook) | ✅ testada |
| 04 | Ambiente de nuvem `rubra-agency-os` (rede: Canva, Drive, Hugging Face) | ✅ criado com aprovação |
| 04 | Script de ambiente da nuvem (`setup/nuvem.sh`) | ✅ testado (11 s); salvo no ambiente |
| 03 | Pipeline de edição de vídeo real (transcrever → analisar → montar → inspecionar) | ✅ validado com bruto sintético; falta voz humana |
| 04 | Claude Code local no Windows | ⏳ depois da nuvem (só se os testes provarem necessidade) |
| — | Amostras de calibração no Drive | ⏳ Gabriela (pastas já criadas) |
| 03 | Pesquisa técnica: ferramentas, geração de imagem e vídeo por IA | ⏳ pendente |
| 03 | Testes reais das ferramentas | ⏳ pendente |
| 06–10 | Construção das skills, agentes, scripts | ⏳ pendente |
| 12 | Testes comparativos A/B/C | ⏳ pendente |

---

## Backup (verificado)

| Arquivo | Drive ID | Tamanho | SHA-256 |
|---|---|---|---|
| backup-skills-2026-11-26.zip | 1Fv9K1nHDfxm0qDXOikn-YSdv4p4wYuxw | 906.740 B | bf50bde1…7543cf |
| backup-skills-2026-11-26.tar.gz | 1ZOI80nKNvSIMvAJCaC-qnbtLKlrWK-lQ | 798.556 B | 708eb6d4…bf5370 |

Verificações feitas: zip testado (sem erros), 55 SKILL.md contados dentro do arquivo, upload por
referência sha256 ao arquivo local, tamanho no Drive idêntico ao original, visibilidade PRIVADA.
Falta: abrir o .zip no Windows (teste de recuperação real).

**Como recuperar:** Drive → RUBRA AGENCY OS → BACKUP → baixar o .zip → clique direito → Extrair tudo.
Cada pasta é uma skill; para reinstalar, compactar a pasta da skill em .zip e enviar em
claude.ai → Configurações → Capacidades → Skills.

## Estrutura no Drive

```
RUBRA AGENCY OS/                 14v5QbP2iGp1vpYtHi29HKZWdkc5n13nq
├── BACKUP/                      1AJXrnhwT38bm34z-x9UtJhF08XbMA9PF
├── CALIBRACAO/                  1yaQ7LIQop44bwl3N5FUonVFm3VqFtzPs
│   ├── 01-AMADORAS/             1CSSr1-Twz1YkWJP-G6DWamt_izAPfUe9
│   ├── 02-EXCELENTES/           1nthFzyz-HWcFCZcc83mFbGdCefI8Fm-i
│   └── 03-VIDEO-BRUTO-TESTE/    1AmaugfgVGiZhhf5I6iK9f_Anmk9nyrXP
└── DOCUMENTACAO/                1pnhWeWs5up_ZjiwQqBDxfB9MjOvA4aKx
```
A pasta pré-existente "RUBRA" (posts da própria RUBRA) não foi tocada.

---

## Decisões tomadas

| # | Data | Decisão | Por quê |
|---|---|---|---|
| D1 | 11-26 | GitHub privado = código, skills, agentes, docs. Drive = materiais de clientes. | Versionamento sem expor material confidencial. |
| D2 | 11-26 | Nada de clientes, fontes licenciadas, fotos, credenciais ou chaves no GitHub. | Exigência da Gabriela. Reforçado por `.gitignore` e verificação antes de cada commit. |
| D3 | 11-26 | Nova pasta "RUBRA AGENCY OS" separada da pasta "RUBRA" existente. | Não misturar sistema com conteúdo. |
| D4 | 11-26 | Backup em .zip (Windows) + .tar.gz. | .zip abre nativamente no Windows. |
| D5 | 11-26 | 9 skills + 3 agentes + comandos + scripts (ver arquitetura). | Especialização sem redundância. |
| D6 | 11-26 | Skills desativadas só depois de a substituta provar resultado melhor. | Não perder capacidade durante a transição. |
| D7 | 11-26 | Nuvem primeiro; local só onde os testes provarem necessidade. | A nuvem já tem FFmpeg, Node, Python, Chromium. Local exige instalação no Windows. |
| D9 | 11-26 | Transcrição padrão: Faster-Whisper `large-v3-turbo` + glossário do cliente. | Teste: 2,7% de erro e nomes corretos vs 8,2% do `small`. |
| D10 | 11-26 | Legenda nunca é queimada sem revisão de grafia. | Até o melhor modelo erra nomes sem glossário. |
| D11 | 11-26 | Detecção de falso início por estrutura (frase recomeçada), não por palavra-chave. | O modelo transcreveu "a... não, espera" como "o Anão. Espera." |
| D12 | 11-26 | Cortes são PROPOSTA do script; decisão editorial é de quem dirige. | Edição é narrativa, não só remoção de pausa. |
| D8 | 11-26 | Nuvem = estúdio de produção (render, transcrição, motion). PC = acesso a arquivos. Imagem por IA = serviço externo. | PC com 7,7 GB RAM e GPU integrada; o servidor da nuvem é mais potente. |

## Arquitetura de funções (aprovada em princípio)

| Função | Forma | Justificativa técnica |
|---|---|---|
| Orquestração (RUBRA CORE) | CLAUDE.md + instrução de Projeto | Precisa estar sempre ativa; skill depende de acionamento. |
| Direção criativa + publicidade | skill `rubra-direcao` | Conhecimento carregado sob demanda no contexto principal, onde a conversa com você acontece. |
| Branding | skill `rubra-marca` | Idem; inclui o padrão design.json. |
| Design gráfico | skill `rubra-grafico` + scripts de render | Precisa de scripts (HTML/SVG → PNG/PDF). |
| Imagem (geração, tratamento, mockup) | skill `rubra-imagem` + scripts | Nova; depende da pesquisa da Fase 03. |
| Estratégia de conteúdo + copy | skill `rubra-texto` | Texto não exige isolamento. |
| Edição audiovisual | skill `rubra-video` + scripts | Pipeline FFmpeg/Whisper. |
| Motion design | skill `rubra-motion` + scripts | HyperFrames/Remotion. |
| Produção técnica | skill `rubra-producao` + scripts de verificação | Determinística: script mede, não opina. |
| Controle de qualidade | **agente** `rubra-revisor` | Contexto separado = não defende o próprio trabalho; vê só o arquivo renderizado. |
| Pesquisa | **agente** `rubra-pesquisador` | Lê dezenas de páginas; devolve só a síntese, sem poluir o contexto da criação. |
| Análise de mídia bruta | **agente** `rubra-analista-de-midia` | Transcrição e quadros de horas de filmagem são volumosos; devolve log de takes. |
| Gestão de projetos | comandos + estrutura de pastas + scripts | Gestão é registro e rotina, não "personalidade". |

Por que não mais agentes: um agente só se justifica por (1) julgamento independente, (2) isolamento
de grande volume de contexto ou (3) paralelismo. Especialização de conhecimento é papel de skill.
Agentes funcionam com segurança apenas no Claude Code; no Chat/Cowork as skills continuam funcionando.

## Distribuição entre ambientes (estratégia)

Fonte única: repositório GitHub. Um script de empacotamento gera, a partir dele:
1. **ZIP de cada skill** → enviado em claude.ai → Skills. Observado nesta sessão: skills do claude.ai
   sincronizam para o Claude Code na nuvem. Alcança Chat, Cowork e Code em nuvem.
2. **Plugin do Claude Code** (agentes, comandos, hooks, scripts) → instalado do próprio repositório.
3. **Instrução de Projeto** curta por cliente → cola no Project do claude.ai.

Regra anti-conflito: cada skill tem `version` no cabeçalho; o mesmo número aparece aqui e no
registro de alterações. Uma skill nunca é instalada por dois canais no mesmo ambiente.
A testar: se o Claude Code local também recebe as skills do claude.ai (decide se o plugin leva skills).

| Capacidade | Chat | Cowork | Code nuvem | Code local |
|---|---|---|---|---|
| Skills RUBRA (conhecimento) | ✅ | ✅ | ✅ | a testar |
| Conectores (Drive, Canva) | ✅ | ✅ | ✅ | ✅ |
| Agentes RUBRA | ❌ | a testar | ✅ | ✅ |
| Comandos /novo-cliente etc. | ❌ | a testar | ✅ | ✅ |
| Render + inspeção (FFmpeg, Chromium) | limitado | limitado | ✅ | ✅ após instalar |
| Fontes instaladas no seu PC, arquivos pesados, CapCut | ❌ | parcial | ❌ | ✅ |

## Ferramentas testadas

| Ferramenta | Instalada | Testada com tarefa real | Resultado |
|---|---|---|---|
| Node 22 / Python 3.13 / Pillow 13 (nuvem) | ✅ | ❌ | — |
| ImageMagick 6.9 (nuvem) | ✅ | ❌ | — |
| Playwright + Chromium (nuvem) | ✅ | ❌ | — |
| Canva (conector) | ✅ conectado | ❌ | — |
| Google Drive (conector) | ✅ | ✅ upload, pastas, metadados | funcionando |
| FFmpeg 6.1.1 (libass, loudnorm, arnndn, x264) | ✅ | ✅ cortes, tratamento de voz, loudness 2 passagens, legendas, MP4 | -14,0 LUFS, pico -1,4 dB, H.264/AAC estéreo |
| Faster-Whisper 1.2.1 (MIT) | ✅ | ✅ PT-BR, palavras com tempo | small 8,2% erro · medium 5,5% · large-v3-turbo 2,7%; turbo ≈0,3–0,6× tempo real em 4 núcleos |
| Piper TTS 1.8 (GPL-3) + voz pt_BR-faber (dataset CC0) | ✅ | ✅ gerou bruto de teste | uso apenas para mídia de teste |
| Barreira de confidencialidade | ✅ | ✅ commit com fonte, imagem, chave falsa e pasta de cliente | 4/4 bloqueados; .gitignore oculta sem -f |

Aprovadas para teste: HyperFrames, Remotion, Impeccable, Taste Skill, Whisper, Faster-Whisper,
Video-Use, Inkscape, vtracer, OpenCV, Ghostscript, GSAP, Skill Creator.

## Dados do ambiente da Gabriela

Windows · Plano Pro · usa Chat, Cowork, Code · arquivos no Drive e no PC ·
licenças: Canva Pro, CapCut Pro · GitHub: sem conta confirmada.

**Hardware verificado por print do Gerenciador de Tarefas (2026-11-26):**
- RAM utilizável: **7,7 GB** (não 16 GB), com 91% em uso no momento do print.
- GPU: **Intel UHD Graphics integrada**, 3,8 GB de memória compartilhada (sem GPU dedicada).
- Disco: SSD NVMe.

**Consequências (decisão D8):**
- Geração de imagem local (Stable Diffusion/Flux): **inviável**. Geração de imagem será por serviço externo.
- Transcrição, render de vídeo e motion: **na nuvem** (4 núcleos, 15 GB RAM), não no PC.
- Claude Code local: continua possível (é leve), mas só para acessar arquivos/fontes do PC, não para render.

## Problemas encontrados

| # | Problema | Situação |
|---|---|---|
| P1 | rubra-motion-studio referencia 8 arquivos inexistentes | Reconstrução aprovada |
| P2 | Drive não informa checksum via conector | Verificação feita por tamanho + upload por hash; falta teste de abertura |
| P3 | Sessão na nuvem é temporária | Resolvido em parte: GitHub ativo. Falta script de ambiente. |
| P5 | Hugging Face bloqueado pela rede / protocolo Xet usa host extra | Hosts liberados; `HF_HUB_DISABLE_XET=1` evita o host Xet |
| P6 | faster-whisper 1.2.1 incompatível com PyAV recente (`metadata_errors`) | Áudio decodificado pelo FFmpeg do sistema |
| P7 | Inspeção visual achou legendas atravessando frase/corte e terminando em artigo | Regras novas de cartela; reinspecionado ✅ |
| P8 | Saída de áudio mono | Forçado estéreo; reinspecionado ✅ |
| P4 | 1ª tentativa de instalar o app Claude no GitHub não achou o repositório | Repositório não havia sido criado; criado e resolvido. |

## Pipeline de vídeo — como usar (validado)

```
/opt/rubra-venv/bin/python scripts/video/transcrever.py bruto.mp4 trans.json large-v3-turbo pt glossario.txt
python3 scripts/video/analisar_falas.py trans.json proposta.json        # revisar a proposta!
python3 scripts/video/montar.py bruto.mp4 proposta.json trans.json final.mp4 [estilo.json]
python3 scripts/video/inspecionar.py final.mp4 inspecao/ proposta.json   # e OLHAR as folhas .png
```
Teste reproduzível: `tests/fixtures/gerar_bruto_sintetico.py` (bruto de 33 s com falso início,
take repetido, pausas longas e ruído). Resultado: 33,3 s → 19,9 s, todos os 4 problemas detectados.

Limites atuais (honestos): testado só com voz sintética; estilo de legenda é neutro (o estilo
autoral por cliente e destaque animado por palavra entram na Fase 09); sem b-roll, trilha, zoom
ou correção de cor ainda; a seleção de "melhores trechos" por narrativa é decisão do Claude/da
Gabriela sobre a transcrição, não do script.
