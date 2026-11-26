# Regra obrigatória de empacotamento de skills (claude.ai)

Origem: em 2026-11-26 os 8 ZIPs da versão 1.0 foram rejeitados pelo importador do claude.ai.

1. Cabeçalho do `SKILL.md` só com `name` e `description`. Nada de `version` ou outros campos
   (versão vai no corpo do texto ou no histórico do Git).
2. `description` com **no máximo 200 caracteres**, entre aspas duplas (dois-pontos sem aspas quebram o YAML).
3. `name` igual ao nome da pasta, minúsculas e hífen.
4. ZIP com a pasta da skill na raiz (`rubra-x.zip` → `rubra-x/SKILL.md`), sem níveis extras.
5. Validar com o Skill Creator oficial (`quick_validate.py`) antes de publicar.

`setup/empacotar-skills.sh` aplica as regras 1–4 e se recusa a gerar o pacote se alguma falhar.
Fonte da verdade: as versões instaladas no claude.ai (sincronizadas em `~/.claude/skills/synced/`
nas sessões do Claude Code) — conferir com `diff` antes de reempacotar.
