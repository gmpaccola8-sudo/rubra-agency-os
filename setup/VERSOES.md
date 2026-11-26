# Versões registradas — RUBRA AGENCY OS

Registro: 2026-11-26. Python: versões exatas em `requirements.lock`.

## Ferramentas do sistema (imagem da nuvem)

```
ffmpeg: 6.1.1-3ubuntu5
node: v22.23.5
npm: 10.9.9
python: 3.13.18
imagemagick: 6.9.12-98
playwright: 1.63.0
os: Ubuntu 24.04.5 LTS
```

FFmpeg compilado com: libass, libfreetype, libfontconfig, libx264, libvpx, librubberband, libzimg.

## Ambiente de nuvem `rubra-agency-os`

- Rede limitada + gerenciadores de pacote + servidores MCP.
- Hosts: media.canva.com, www.canva.com, export-download.canva.com, drive.usercontent.google.com, huggingface.co, cas-bridge.xethub.hf.co, cdn-lfs.hf.co, cdn-lfs-us-1.hf.co, us.aws.cdn.hf.co, eu.aws.cdn.hf.co
- Variável: HF_HUB_DISABLE_XET=1
- Script: `if [ -d rubra-agency-os ]; then bash rubra-agency-os/setup/nuvem.sh; fi`

## Modelos

| Modelo | Origem | Licença | Uso |
|---|---|---|---|
| Whisper large-v3-turbo (CTranslate2) | Hugging Face | MIT | transcrição padrão |
| Whisper small / medium | Hugging Face | MIT | testados, não padrão |
| Piper pt_BR-faber-medium | rhasspy/piper-voices | dataset CC0 | só mídia de teste |
