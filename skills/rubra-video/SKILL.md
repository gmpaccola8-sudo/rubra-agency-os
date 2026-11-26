---
name: rubra-video
description: "Edita filmagens reais da RUBRA: cortes por narrativa, transcrição, legendas revisadas, tratamento de áudio e exportação MP4. Para animações do zero, use rubra-motion."
---

# RUBRA · Edição de vídeo (filmagem real)

Estado: **protótipo funcional** — validado com gravação simulada; ainda sem filmagem real de cliente.

## Onde roda

- **Claude Code em nuvem** (repositório `rubra-agency-os`, ambiente `rubra-agency-os`): edição completa.
- **Chat / Cowork:** não renderiza vídeo. Entregue o plano de edição (estrutura, cortes por timecode se
  houver transcrição, legendas, trilha) e diga que a execução é no Claude Code.

Nunca altere o arquivo original. Trabalhe numa pasta da demanda.

## Fluxo

1. **Diagnóstico:** duração, resolução, fps, áudio (`ffprobe`). Assista amostras; não diga que viu se só
   leu metadados.
2. **Transcrição local** (nenhum áudio sai do servidor):
   `/opt/rubra-venv/bin/python <skill>/scripts/transcrever.py bruto.mp4 trans.json large-v3-turbo pt glossario.txt`
   O `glossario.txt` do cliente (nomes, marca, termos) fica na pasta dele. Sem glossário, nomes saem errados.
3. **Narrativa antes do corte:** com a transcrição, escreva a estrutura: gancho (primeiros 3 s), o que
   fica, a ordem, o fecho e o CTA. Selecione os melhores trechos por sentido e energia, não só por
   remoção de pausa. Preserve pausas naturais e a expressividade da pessoa.
4. **Proposta automática de cortes** (pausas longas, takes repetidos, falsos inícios):
   `python3 <skill>/scripts/analisar_falas.py trans.json proposta.json` → **revise e ajuste** a proposta
   segundo a estrutura do passo 3. O script propõe; a decisão editorial é sua.
5. **Legendas:** revise a grafia na transcrição antes de montar (D10: legenda nunca é queimada sem
   revisão). Estilo do cliente em `estilo.json` (fonte, cor, posição, caixa). Destaque de palavra só
   quando a fala pedir.
6. **Montagem:** `python3 <skill>/scripts/montar.py bruto.mp4 proposta.json trans.json final.mp4 estilo.json`
   (cortes com micro-fades, limpeza de voz, loudness -14 LUFS, legendas, H.264/AAC estéreo, .srt ao lado).
7. **Inspeção:** `python3 <skill>/scripts/inspecionar.py final.mp4 inspecao/ proposta.json` e **olhe** as
   folhas de quadros; depois `rubra-revisao`.
8. **Entrega:** master sem compressão extra na pasta do cliente no Drive (via Drive para computador /
   Remote Control quando configurado; o conector do Drive só aceita ~3 MB) + `.srt` + plano de edição.

## Princípios

- Corte serve à narrativa e à retenção; nada de zoom aleatório ou efeito para "parecer dinâmico".
- Nenhum recurso é obrigatório (legenda animada, b-roll, zoom, transição): cada um precisa servir à
  identidade e ao público do cliente. Novo estilo de vídeo → referências antes (regra permanente).
- Trilha e efeitos só com licença comprovada (do cliente, livre com registro, ou sintetizados).
- Não ainda no sistema (backlog): b-roll automático, reenquadramento por rosto, correção de cor por LUT,
  ducking de trilha. Faça manualmente com FFmpeg se necessário e registre.
