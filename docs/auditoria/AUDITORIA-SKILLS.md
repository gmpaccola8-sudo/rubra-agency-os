# RUBRA AGENCY OS — Auditoria das 55 skills

Data: 2026-11-26 · Backup: `RUBRA AGENCY OS / BACKUP / backup-skills-2026-11-26.zip`
Nenhuma skill foi alterada ou excluída. Esta matriz é uma recomendação; cada ação depende de aprovação.

**Base da avaliação:** estrutura de arquivos de todas as 55, leitura integral das que viram núcleo
(gabriela-os, creative-director, quality-control, identidade-visual-monograma, rubra-motion-studio,
editor-de-videos) e verificação automática de referências quebradas. As skills marcadas CONSOLIDAR
serão lidas integralmente no momento da fusão, para extrair o que tiverem de aproveitável.

**Legenda de destino:** `core` (CLAUDE.md / RUBRA CORE) · `direcao` · `marca` · `grafico` · `imagem` ·
`texto` · `video` · `motion` · `producao` · agentes `revisor`, `pesquisador`, `analista-de-midia`.

**Desativar** = remover do claude.ai depois que a substituta estiver testada (fica no backup).
Nada é desativado antes de a nova versão provar que faz melhor.

## A. Skills oficiais da Anthropic (14) — fora da consolidação

| # | Skill | Decisão | Observação |
|---|---|---|---|
| 1 | skill-creator | MANTER | Ferramenta oficial para construir e testar as novas skills (evals). Essencial. |
| 2 | pdf | MANTER | Scripts reais. Base para a pré-impressão. |
| 3 | docx | MANTER | Scripts reais. Manuais e documentos. |
| 4 | pptx | MANTER | Scripts reais. Apresentações editáveis para cliente. |
| 5 | xlsx | MANTER | Scripts reais. Cobre também o papel de analista-de-planilhas. |
| 6 | deep-research | MANTER | Usada pelo agente pesquisador. |
| 7 | google-workspace | MANTER | Necessária para criar/editar arquivos no Drive. |
| 8 | docs | MANTER | Documentos vivos no claude.ai. |
| 9 | computer-use | MANTER | Controle do computador pelo app desktop (CapCut, Canva desktop). |
| 10 | chrome-browser | MANTER | Navegação real, pesquisa de referências logadas. |
| 11 | built-in-browser | MANTER | Navegador interno do app. |
| 12 | setup-writing-style | TESTAR | Sobrepõe email-com-minha-voz. Fica a que soar mais como você. |
| 13 | import-memory | MANTER | Utilitário de plataforma. Sem conflito. |
| 14 | morning | MANTER | Utilitário de plataforma. Sem conflito. |

## B. Skills personalizadas (41)

### Núcleo e direção

| # | Skill | Decisão | Destino | Motivo |
|---|---|---|---|---|
| 15 | gabriela-os | APRIMORAR | core | Seu método. Vira a instrução central, carregada sempre, em vez de skill acionada por sorte. |
| 16 | creative-director | CONSOLIDAR | direcao | Princípios bons (3 territórios, "identidade fixa, layout não"), sem instrumento. |
| 17 | visual-explorer | CONSOLIDAR | direcao | Mesma função da anterior. Duas skills para o mesmo pedido geram acionamento aleatório. |
| 18 | cerebro-do-negocio | SUBSTITUIR | /novo-cliente | Monta "arquivo de contexto" — é exatamente a camada de cliente, agora estruturada. |

### Marca

| # | Skill | Decisão | Destino | Motivo |
|---|---|---|---|---|
| 19 | identidade-visual-monograma | APRIMORAR | marca | A melhor do acervo: tem aprendizado real de aprovações/rejeições. Vira o coração de rubra-marca. |
| 20 | brand-strategist | CONSOLIDAR | marca | Posicionamento entra como primeira etapa de rubra-marca. |
| 21 | kit-de-marca | CONSOLIDAR | marca | O formato design.json é útil — vira o padrão de todo cliente. |
| 22 | marca (/marca) | DESATIVAR | — | Gera identidade completa de uma vez (nome+paleta+tipo). Contraria o método de direções e aprovação. |
| 23 | brand-guardian | CONSOLIDAR | revisor | Verificar fidelidade à marca é critério de controle de qualidade, não etapa de criação. |

### Gráfico, imagem e apresentações

| # | Skill | Decisão | Destino | Motivo |
|---|---|---|---|---|
| 24 | carousel-architect | CONSOLIDAR | grafico | Narrativa de carrossel. Sem quantidade fixa de slides. |
| 25 | carrossel-instagram | DESATIVAR | — | 8 slides fixos e saída "pronta para Canva" — fórmula de volume. |
| 26 | apresentacao-executiva | CONSOLIDAR | grafico | Narrativa útil; render passa a ser verificado. |
| 27 | slides (/slides) | DESATIVAR | — | Duplica a anterior. |
| 28 | editor-de-fotos | CONSOLIDAR | imagem | Tratamento de fotos reais ganha scripts (Pillow/OpenCV). |
| 29 | gerador-de-imagens | CONSOLIDAR | imagem | Prompts de foto viram parte do pipeline de geração. |
| 30 | imagem (/imagem) | DESATIVAR | — | Duplica gerador-de-imagens. |

### Conteúdo e texto

| # | Skill | Decisão | Destino | Motivo |
|---|---|---|---|---|
| 31 | content-strategist | CONSOLIDAR | texto | Pilares e planejamento. |
| 32 | copywriter | CONSOLIDAR | texto | Voz humana, CTA único. |
| 33 | conteudo (/conteudo) | DESATIVAR | — | 30 dias de posts de uma vez — calendário para preencher calendário. |
| 34 | copy-ads (/copy-ads) | CONSOLIDAR | texto | Mantém o mecanismo de variações para teste; elimina o número fixo de 15. |
| 35 | roteiro (/roteiro) | CONSOLIDAR | texto | Roteiro falado; motion recebe roteiro visual. |
| 36 | bio (/bio) | CONSOLIDAR | texto | Vira uma referência dentro de rubra-texto. |
| 37 | social-media (/social-media) | CONSOLIDAR | pesquisador | Diagnóstico de perfil é pesquisa. |
| 38 | dossie-de-concorrente | CONSOLIDAR | pesquisador | Mesma natureza: pesquisa com fontes. |

### Audiovisual

| # | Skill | Decisão | Destino | Motivo |
|---|---|---|---|---|
| 39 | rubra-motion-studio | SUBSTITUIR | motion + video | 8 arquivos ausentes (lista abaixo). Princípios aproveitados; estrutura reconstruída. |
| 40 | editor-de-videos | APRIMORAR | video | Única skill criativa com scripts reais (FFmpeg/Node). Falta transcrição — entra Faster-Whisper. |
| 41 | reels-director | CONSOLIDAR | motion | Conceito de Reels. |
| 42 | criador-de-videos | CONSOLIDAR | motion | Usa HyperFrames — vira um dos motores de rubra-motion. |

### Qualidade

| # | Skill | Decisão | Destino | Motivo |
|---|---|---|---|---|
| 43 | quality-control | SUBSTITUIR | revisor | Nota 0–10 sobre texto. Passa a ser agente independente que inspeciona o arquivo renderizado. |

### Comercial e operação (fora dos departamentos criativos)

| # | Skill | Decisão | Destino | Motivo |
|---|---|---|---|---|
| 44 | proposta-comercial | TESTAR | comercial | Duplica /proposta. Teste com o mesmo briefing; fica a melhor. |
| 45 | proposta (/proposta) | TESTAR | comercial | Idem. |
| 46 | captar | MANTER | — | Prospecção. Gatilho próprio, sem conflito. |
| 47 | follow-up-de-clientes | MANTER | — | Operação comercial. Sem conflito. |
| 48 | revisor-de-contratos | MANTER | — | Útil para contratos com clientes. Sem conflito. |
| 49 | email-com-minha-voz | TESTAR | — | Sobrepõe setup-writing-style (oficial). |
| 50 | trafego (/trafego) | MANTER | — | Análise de mídia paga. Domínio próprio. |
| 51 | auditor-de-skills | MANTER | — | Será usado agora: verifica skills externas (Impeccable, Taste) antes de instalar. |
| 52 | analista-de-planilhas | DESATIVAR | — | xlsx oficial cobre. |
| 53 | escritor-de-prd | DESATIVAR | — | Fora do escopo da agência. |
| 54 | diagnostico-de-automacao | DESATIVAR | — | Uso único; cumprido por este projeto. |
| 55 | meu-primeiro-agente | DESATIVAR | — | Uso único; substituído por este projeto. |

## Resumo

| Decisão | Qtd |
|---|---|
| MANTER | 18 |
| APRIMORAR | 3 |
| CONSOLIDAR | 18 |
| SUBSTITUIR | 3 |
| TESTAR | 4 |
| DESATIVAR | 9 |
| EXCLUIR | 0 (nada é excluído; desativadas ficam no backup) |

Resultado: das 41 personalizadas, a operação criativa passa a depender de **9 skills RUBRA** + 3 agentes,
mais 7 utilitárias comerciais/operacionais com gatilho próprio.

## Referências ausentes em rubra-motion-studio (verificado)

- references/direcao.md
- references/direcao_arte_movimento.md  ← marcada como "prioridade máxima"
- references/producao.md
- references/qualidade.md
- references/som.md
- scripts/inspect_media.py
- templates/briefing.md
- templates/timeline.csv

Se você tiver esses arquivos em algum lugar (computador, conversa antiga), envie — aproveitamos o conteúdo.
