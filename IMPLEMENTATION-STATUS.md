# RUBRA AGENCY OS — IMPLEMENTATION-STATUS

> Documento de continuidade. Qualquer sessão nova começa lendo este arquivo.
> Cópia mestre: repositório GitHub privado `gmpaccola8-sudo/rubra-agency-os`.
> Espelho: Google Drive → `RUBRA AGENCY OS / DOCUMENTACAO / IMPLEMENTATION-STATUS.md`.
> O histórico completo de versões deste arquivo está no Git (`git log -p IMPLEMENTATION-STATUS.md`).

Última atualização: 2026-11-26 (4ª rodada) · Fase atual: **Entrega da versão 1.0**

---

## Próxima ação

**RUBRA OS 1.0 empacotado.** 8 skills em Drive → `RUBRA AGENCY OS / INSTALAR` (+ guia).
**Gabriela:** (1) subir os 8 ZIPs no claude.ai; (2) aprovar a lista de remoção (32) e desativá-las.
**Depois:** teste de aceitação com uma demanda real; configuração local (Drive para computador + app Claude).

| Etapa 1.0 | Status |
|---|---|
| 1 Aprovar lista de skills | ⏳ Gabriela |
| 2 Escrever as skills (8/8) | ✅ |
| 3 Empacotar + guia no Drive | ✅ ZIPs conferidos byte a byte |
| 4 Agentes no repositório (`.claude/agents`: revisor, pesquisador, analista de mídia) | ✅ |
| 5 Pasta CLIENTES no Drive + modelo de Project (`rubra-os/references/modelo-project.md`) | ✅ |
| 6 Instalar no claude.ai e desativar antigas | ⏳ Gabriela |
| 7 Configuração local (Drive para computador + app Claude) | ⏳ Gabriela (opcional para começar) |
| 8 Teste de aceitação com demanda real | ⏳ juntos |

Benchmark 01 concluído: A, B e C (antes/depois da revisão) na sala de revisão privada
https://claude.ai/artifact/LhHn2aPVQg8WZ3iJtwkPEP — aguarda avaliação da Gabriela.

---

## Mapa de maturidade das capacidades

Estados: `Planejado` → `Instalado` → `Testado (simulado)` → `Testado (material real)` →
`Validado tecnicamente` → `Validado criativamente` → `Aprovado para produção`.
Validação criativa e aprovação para produção dependem da Gabriela.

| Capacidade | Estado atual | Evidência / o que falta |
|---|---|---|
| **Infraestrutura** | | |
| Repositório GitHub + barreira de confidencialidade | Validado tecnicamente | 4/4 bloqueios; revalidado em sessão nova |
| Ambiente de nuvem com reinstalação automática | Validado tecnicamente | Sessão nova independente: 6/6 verificações passaram (2026-11-26) |
| Versões travadas + procedimento de recuperação | Validado tecnicamente | `setup/requirements.lock` instalado do zero em ambiente limpo; `docs/RECUPERACAO.md` |
| Entrega de arquivos pesados ao Drive | Planejado | Solução escolhida: Drive para computador + Remote Control (`docs/setup/LOCAL-WINDOWS.md`) |
| Sala de revisão privada (Artifact) | Validado tecnicamente | Vídeos e peças até 15 MB por arquivo; só para assistir |
| **Edição audiovisual (filmagem real)** — PROTÓTIPO FUNCIONAL | | |
| Transcrição local PT-BR (Faster-Whisper) | Testado (simulado) | Voz sintética; falta voz humana |
| Análise de falas (pausas, take repetido, falso início) | Testado (simulado) | 3 testes de regressão; falta material real |
| Montagem: cortes, voz, loudness, legenda neutra | Validado tecnicamente | -14 LUFS, H.264/AAC estéreo; só simulado |
| Inspeção técnica + folhas de quadros | Validado tecnicamente | Pegou falhas reais de legenda |
| Seleção de melhores trechos / narrativa / retenção | Planejado | Ver "Roteiro da edição profissional" |
| Legendas com direção tipográfica e destaque contextual | Planejado | Estilo por cliente via `estilo.json` |
| B-roll, reenquadramento, cor, trilha, SFX, transições | Planejado | |
| **Motion design** | | |
| Cena 3D determinística independente de motor | Testado (simulado) | "Atrito": luz, material, sombra, faíscas, transição motivada |
| HyperFrames 0.9.98 | Validado tecnicamente — **motor complementar** | Render 2m57s; check sem erros; telemetria desligada |
| Remotion 4.0.547 | Validado tecnicamente — **motor principal (provisório)** | Licença gratuita confirmada: RUBRA é operação individual |
| Sonoplastia sintetizada sincronizada | Validado tecnicamente | 0,0 ms de desvio nos dois motores; **não ouvido** |
| Qualidade criativa do motion | Testado (simulado) — não validado | Abertura ilegível 2,5 s; ver `docs/testes/motion-01-resultado.md` |
| **Design gráfico e direção de arte** | | |
| Peça publicitária autoral | Planejado | |
| Composição tipográfica profissional | Planejado | |
| Carrossel com narrativa visual | Planejado | |
| Manipulação de fotografias (Pillow/OpenCV) | Planejado | |
| Identidade visual (monograma, sistema) | Planejado | Base: skill identidade-visual-monograma |
| Mockups realistas (perspectiva sobre foto real) | Planejado | |
| Vetorização (vtracer, Inkscape) | Planejado | |
| Produção gráfica (PDF/X, CMYK, sangria) | Planejado | Ghostscript |
| Geração de imagens por IA | Planejado | Pesquisa de serviços; PC não suporta local |
| Crítica visual independente (agente revisor) | Planejado | Método já usado: folha de quadros + crítica |
| Impeccable / Taste Skill / Canvas Design / Frontend Design / Algorithmic Art | Investigado (código lido) | Mecanismos incorporados; nenhuma instalada (`docs/testes/ferramentas-graficas-01.md`) |
| Direção criativa (`skills/rubra-direcao` v0.1: mapa do óbvio + 14 mecanismos + análise de referências) | Testado (simulado) | Benchmark 01, condição C |
| Peças gráficas (`skills/rubra-grafico` v0.1 + `render.js`) | Testado (simulado) | render.js achou contraste e margem que o QC antigo não viu |
| Revisor independente (`agents/rubra-revisor`) | Instalado | Rodando no benchmark 01 |
| Geração de imagem — Canva (já pago) | Testado (simulado) | 1 geração; conector só devolve miniatura 160 px |
| Geração de imagem — API externa | Planejado | Aguarda decisão de custo |

---

## Etapas

| Fase | Etapa | Status |
|---|---|---|
| 01 | Inventário do ambiente | ✅ |
| 02 | Backup das 55 skills no Drive | ✅ verificado |
| 02 | Matriz individual das 55 skills (`docs/auditoria/AUDITORIA-SKILLS.md`) | ✅ entregue — aguarda revisão |
| 02 | Teste de recuperação do backup no Windows | ⏳ Gabriela |
| 04 | GitHub privado + app Claude só neste repositório | ✅ |
| 04 | Barreira de confidencialidade | ✅ testada |
| 04 | Ambiente de nuvem `rubra-agency-os` (rede, variável, script) | ✅ |
| 04 | Persistência validada em sessão nova | ✅ 6/6 |
| 04 | Claude Code local no Windows | ⏳ ganhou motivo concreto: P10 |
| 03 | Pipeline de vídeo real (protótipo) | ✅ simulado |
| 03 | Motion: HyperFrames × Remotion | ✅ comparação técnica concluída |
| 03 | Testes gráficos, vetor, pré-impressão, imagem por IA | ⏳ próximos |
| 06–10 | Skills, agentes, comandos | ⏳ |
| 12 | Testes comparativos A/B/C | ⏳ |

---

## Roteiro da edição audiovisual profissional (planejado)

Princípio: nenhum recurso é obrigatório. A edição parte do objetivo, público e identidade do cliente,
e de referências (regra permanente em `CLAUDE.md`). Antes de um estilo novo: pedir/pesquisar referências.

| Camada | Como será feito | Ferramenta |
|---|---|---|
| Seleção de melhores trechos | Transcrição + marcação editorial (gancho, argumento, prova, fecho) feita pelo Claude sobre o texto; script só executa | Whisper + `analisar_falas.py` estendido |
| Narrativa e retenção | Estrutura proposta antes do corte (gancho nos 3 s, progressão, CTA único); medição de ritmo (duração média de plano, pausas) | Relatório de ritmo |
| Legenda com direção tipográfica | `estilo.json` por cliente (fonte da marca, peso, caixa, posição); destaque de palavra-chave só quando a fala pede | ASS (libass) / Remotion |
| Motion graphics contextual | Cartelas, números, nomes — cenas independentes de motor | Remotion/HyperFrames |
| B-roll | Só material do cliente ou licenciado, com registro de origem | FFmpeg |
| Reenquadramento | 16:9 → 9:16 seguindo o rosto (detecção de rosto) quando a resolução permite | OpenCV |
| Cor | Correção técnica (exposição, balanço) + LUT por cliente, nunca filtro genérico | FFmpeg (lut3d, eq) |
| Áudio | Já existe: limpeza, compressão, loudness. A adicionar: ducking da trilha sob a voz | FFmpeg (sidechaincompress) |
| Trilhas e SFX | Licenciadas pelo cliente, livres com licença registrada, ou sintetizadas | registro de licença |
| Transições | Corte seco como padrão; transição só quando motivada por movimento/forma | — |
| Naturalidade | Pausas de respiração preservadas (0,35 s); sem cortes de sílaba (padding 0,12 s) | já implementado |

---

## Backup (verificado)

| Arquivo | Drive ID | Tamanho | SHA-256 |
|---|---|---|---|
| backup-skills-2026-11-26.zip | 1Fv9K1nHDfxm0qDXOikn-YSdv4p4wYuxw | 906.740 B | bf50bde1…7543cf |
| backup-skills-2026-11-26.tar.gz | 1ZOI80nKNvSIMvAJCaC-qnbtLKlrWK-lQ | 798.556 B | 708eb6d4…bf5370 |

Recuperar: Drive → RUBRA AGENCY OS → BACKUP → baixar .zip → Extrair tudo. Reinstalar uma skill:
compactar a pasta dela em .zip e enviar em claude.ai → Configurações → Capacidades → Skills.

## Estrutura no Drive

```
RUBRA AGENCY OS/                 14v5QbP2iGp1vpYtHi29HKZWdkc5n13nq
├── BACKUP/                      1AJXrnhwT38bm34z-x9UtJhF08XbMA9PF
├── CALIBRACAO/                  1yaQ7LIQop44bwl3N5FUonVFm3VqFtzPs
│   ├── 01-AMADORAS/             1CSSr1-Twz1YkWJP-G6DWamt_izAPfUe9
│   ├── 02-EXCELENTES/           1nthFzyz-HWcFCZcc83mFbGdCefI8Fm-i
│   └── 03-VIDEO-BRUTO-TESTE/    1AmaugfgVGiZhhf5I6iK9f_Anmk9nyrXP
├── DOCUMENTACAO/                1pnhWeWs5up_ZjiwQqBDxfB9MjOvA4aKx
└── TESTES/                      1i2xrlMMN1Z56GqMd90jtH6fLbYL_6fcx
```
A pasta pré-existente "RUBRA" (posts da própria RUBRA) não foi tocada.

---

## Decisões tomadas

| # | Data | Decisão | Por quê |
|---|---|---|---|
| D1 | 11-26 | GitHub privado = código, skills, agentes, docs. Drive = materiais de clientes. | Versionamento sem expor material confidencial. |
| D2 | 11-26 | Nada de clientes, fontes licenciadas, fotos, credenciais ou chaves no GitHub. | Exigência da Gabriela; `.gitignore` + hook. |
| D3 | 11-26 | Pasta "RUBRA AGENCY OS" separada da pasta "RUBRA". | Não misturar sistema com conteúdo. |
| D4 | 11-26 | Backup em .zip + .tar.gz. | .zip abre nativamente no Windows. |
| D5 | 11-26 | 9 skills + 3 agentes + comandos + scripts. | Especialização sem redundância. |
| D6 | 11-26 | Skills desativadas só depois de a substituta provar resultado melhor. | Não perder capacidade na transição. |
| D7 | 11-26 | Nuvem primeiro; local só onde os testes provarem necessidade. | Nuvem já tem as ferramentas. |
| D8 | 11-26 | Nuvem = estúdio de produção. PC = acesso a arquivos. Imagem por IA = serviço externo. | PC: 7,7 GB RAM, GPU integrada. |
| D9 | 11-26 | Transcrição padrão: `large-v3-turbo` + glossário do cliente. | 2,7% de erro vs 8,2% do `small`. |
| D10 | 11-26 | Legenda nunca é queimada sem revisão de grafia. | Até o melhor modelo erra nomes. |
| D11 | 11-26 | Falso início detectado por estrutura, inclusive dentro da mesma frase. | Whisper varia a pontuação entre execuções. |
| D12 | 11-26 | Cortes são PROPOSTA do script; decisão editorial é de quem dirige. | Edição é narrativa. |
| D13 | 11-26 | Regra permanente: referências e contexto do cliente antes de criar (em `CLAUDE.md`). | Pedido da Gabriela. |
| D14 | 11-26 | Autonomia em testes internos; consulta só para criação, custo, permissão, confidencial, arquitetura. | Pedido da Gabriela. |
| D15 | 11-26 | Estados de maturidade obrigatórios; edição de vídeo = protótipo funcional. | Pedido da Gabriela. |
| D16 | 11-26 | Cenas de motion independentes de motor (`render(t)` puro). | Teste mostrou: qualidade vem da cena, não do motor. |
| D17 | 11-26 | HyperFrames sempre com telemetria desligada; não enviar "usage note". | Envia uso ao PostHog por padrão. |
| D19 | 11-26 | Remotion = motor principal provisório; HyperFrames complementar; testar recursos nativos de cada um. | Licença ok para operação individual; nenhum descartado por velocidade. |
| D20 | 11-26 | Arquivos pesados: Drive para computador + Remote Control. Sem compressão para caber em limite de transferência. | Decisão da Gabriela (opção A). |
| D21 | 11-26 | Três níveis de validação criativa: técnico, estético, publicitário. | Pedido da Gabriela. |
| D22 | 11-26 | Não instalar Impeccable/Taste como skills; incorporar mecanismos. | Focados em web; hooks/binários geram ruído. |
| D23 | 11-26 | Skills do sistema nunca citam cliente ou briefing específico. | Universalidade e benchmark justo. |
| D18 | 11-26 | Dependências de motion locais (sem CDN). | CDN bloqueado e frágil; reprodutibilidade. |

## Arquitetura de funções (aprovada em princípio)

| Função | Forma | Justificativa técnica |
|---|---|---|
| Orquestração (RUBRA CORE) | CLAUDE.md + instrução de Projeto | Precisa estar sempre ativa. |
| Direção criativa + publicidade | skill `rubra-direcao` | Conhecimento sob demanda no contexto principal. |
| Branding | skill `rubra-marca` | Inclui o padrão design.json. |
| Design gráfico | skill `rubra-grafico` + scripts de render | HTML/SVG → PNG/PDF. |
| Imagem | skill `rubra-imagem` + scripts | Depende da pesquisa da Fase 03. |
| Conteúdo + copy | skill `rubra-texto` | |
| Edição audiovisual | skill `rubra-video` + scripts | Pipeline existente. |
| Motion design | skill `rubra-motion` + cenas + motores | |
| Produção técnica | skill `rubra-producao` + scripts | Script mede, não opina. |
| Controle de qualidade | **agente** `rubra-revisor` | Julgamento independente sobre o arquivo renderizado. |
| Pesquisa | **agente** `rubra-pesquisador` | Isola volume de leitura. |
| Análise de mídia bruta | **agente** `rubra-analista-de-midia` | Isola volume de transcrição/quadros. |
| Gestão de projetos | comandos + pastas + scripts | |

## Distribuição entre ambientes

Fonte única: GitHub. Gera: (1) ZIP por skill → claude.ai (alcança Chat, Cowork, Code nuvem);
(2) plugin do Claude Code (agentes, comandos, scripts); (3) instrução curta por Project de cliente.
Regra: `version` em cada skill; nunca o mesmo recurso por dois canais no mesmo ambiente.

| Capacidade | Chat | Cowork | Code nuvem | Code local |
|---|---|---|---|---|
| Skills RUBRA | ✅ | ✅ | ✅ | a testar |
| Conectores (Drive, Canva) | ✅ | ✅ | ✅ | ✅ |
| Agentes / comandos RUBRA | ❌ | a testar | ✅ | ✅ |
| Render + inspeção | limitado | limitado | ✅ | ✅ após instalar |
| Arquivos pesados / fontes do PC | ❌ | parcial | ❌ (P10) | ✅ |

## Ferramentas testadas

| Ferramenta | Estado | Resultado |
|---|---|---|
| Google Drive (conector) | Validado tecnicamente (com limite) | Upload ok até ~3,1 MB por chamada |
| FFmpeg 6.1.1 | Validado tecnicamente | Cortes, voz, loudness, legendas, comparação SSIM, correlação de áudio |
| Faster-Whisper 1.2.1 | Testado (simulado) | small 8,2% · medium 5,5% · turbo 2,7% |
| Piper TTS 1.8 | Validado tecnicamente | Só mídia de teste |
| Playwright + Chromium (SwiftShader) | Validado tecnicamente | Quadros de cena 3D ≈0,8 s cada |
| Three.js 0.187 (MIT) | Validado tecnicamente | PCFSoftShadowMap removido → PCFShadowMap |
| HyperFrames 0.9.98 (Apache 2.0) | Validado tecnicamente | ver `docs/testes/motion-01-resultado.md` |
| Remotion 4.0.547 (licença própria) | Validado tecnicamente | idem |
| GSAP 3.13 | Instalado | Usado só como linha do tempo vazia no HyperFrames |
| Canva (conector) | Instalado | Não testado |

Aprovadas e ainda não testadas: Impeccable, Taste Skill, Whisper (original), Video-Use, Inkscape,
vtracer, OpenCV, Ghostscript, Skill Creator.

## Dados do ambiente da Gabriela

Windows · Plano Pro · Chat, Cowork, Code · Drive + PC · Canva Pro, CapCut Pro ·
GitHub `gmpaccola8-sudo`. Hardware (print): **7,7 GB RAM** utilizáveis (91% em uso),
**GPU integrada Intel UHD**, SSD NVMe. Sem geração de imagem local; render pesado na nuvem.

## Problemas encontrados

| # | Problema | Situação |
|---|---|---|
| P1 | rubra-motion-studio referencia 8 arquivos inexistentes | Reconstrução aprovada |
| P2 | Drive não informa checksum via conector | Tamanho + upload por hash |
| P3 | Sessão na nuvem é temporária | ✅ Resolvido: GitHub + script de ambiente, validado em sessão nova |
| P4 | App Claude no GitHub não achava o repositório | ✅ Repositório criado |
| P5 | Hugging Face bloqueado / host Xet | ✅ Hosts liberados; `HF_HUB_DISABLE_XET=1` |
| P6 | faster-whisper × PyAV recente | ✅ Áudio decodificado pelo FFmpeg |
| P7 | Legendas atravessando frase/corte, terminando em artigo | ✅ Regras de cartela |
| P8 | Áudio mono | ✅ Estéreo |
| P9 | Sessão nova: Whisper juntou falso início e frase certa → falso início não removido | ✅ Detecção dentro da frase + 3 testes de regressão |
| P10 | **Conector do Drive: ~3,1 MB por chamada.** Vídeos finais não chegam ao Drive | ⏳ Decisão da Gabriela (opções no relatório) |
| P11 | HyperFrames: telemetria ligada por padrão; modelo inicial usa CDN | ✅ Desligada; dependências locais |
| P13 | Fontes do benchmark com nomes trocados (erro do Claude) | ✅ Corrigido; registrado no protocolo |
| P14 | Canva: resolução cheia só via novo design gerado (gasta cota) | ⏳ Pendente; perde relevância se API for aprovada |
| P12 | Primeiros 2,5 s da cena "Atrito" ilegíveis | ⏳ Iteração 2 |

## Pipeline de vídeo — como usar (protótipo)

```
/opt/rubra-venv/bin/python scripts/video/transcrever.py bruto.mp4 trans.json large-v3-turbo pt glossario.txt
python3 scripts/video/analisar_falas.py trans.json proposta.json        # revisar a proposta!
python3 scripts/video/montar.py bruto.mp4 proposta.json trans.json final.mp4 [estilo.json]
python3 scripts/video/inspecionar.py final.mp4 inspecao/ proposta.json   # e OLHAR as folhas .png
python3 -I tests/test_analisar_falas.py                                  # regressão
```

## Motion — como reproduzir

`bash motion/montar-laboratorio.sh <pasta_lab>` reconstrói o laboratório (dependências locais, fonte,
som) e renderiza a cena "Atrito" nos dois motores.
