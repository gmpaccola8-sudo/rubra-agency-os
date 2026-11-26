# Formatos e zonas seguras

Medidas em px. Zonas seguras são aproximadas e mudam com as atualizações das plataformas:
conferir quando houver mudança visível de interface.

| Formato | Tamanho | Área segura para texto e logo |
|---|---|---|
| Feed Instagram (retrato) | 1080×1350 | margem mínima de 60 px; a grade do perfil corta para 3:4 central (1012×1350) — o essencial fica dentro |
| Feed quadrado | 1080×1080 | margem mínima de 60 px |
| Carrossel | 1080×1350 por slide | igual ao feed; ponto de continuidade entre slides: borda lateral |
| Story / Reels (capa) | 1080×1920 | topo: 250 px livres; base: 340 px livres (interface de resposta) |
| Capa de Reels no grid | 1080×1920, exibida 1080×1440 | essencial entre y=240 e y=1680 |
| LinkedIn (retrato) | 1080×1350 | margem 60 px |
| A4 impresso | 210×297 mm | sangria 3 mm; margem de segurança 5 mm (ver rubra-producao) |

`scripts/render.js` usa `--seguranca <px>` (padrão 60) e reprova texto fora da área segura.
