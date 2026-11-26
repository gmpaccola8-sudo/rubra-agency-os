"""Transcrição local com Faster-Whisper (MIT). Nenhum áudio sai da máquina.

Gera JSON com segmentos e palavras com tempo (início/fim), base para cortes,
legendas e edição orientada por texto.

Uso:
  python transcrever.py <arquivo_audio_ou_video> <saida.json> [modelo] [idioma] [glossario.txt]
  modelo padrão: small · idioma padrão: pt
  glossario.txt: um termo por linha (nomes, marca, jargões, anglicismos). Fica na pasta do cliente.
"""
import json
import subprocess
import sys
import time

import numpy as np
from faster_whisper import WhisperModel


def carregar_audio(entrada: str) -> np.ndarray:
    """Decodifica com o FFmpeg do sistema (16 kHz, mono). Evita incompatibilidades do PyAV
    e aceita qualquer formato que o FFmpeg leia (mp4, mov, mkv, wav, m4a...)."""
    bruto = subprocess.run(
        ["ffmpeg", "-v", "error", "-nostdin", "-i", entrada, "-vn", "-ac", "1", "-ar", "16000",
         "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(bruto, dtype=np.float32)


def transcrever(entrada: str, saida: str, modelo: str = "small", idioma: str = "pt",
                glossario: str | None = None) -> dict:
    termos = []
    if glossario:
        termos = [l.strip() for l in open(glossario, encoding="utf-8") if l.strip()]
    t0 = time.time()
    m = WhisperModel(modelo, device="cpu", compute_type="int8")
    t_carga = time.time() - t0

    t1 = time.time()
    segmentos, info = m.transcribe(
        carregar_audio(entrada),
        language=idioma,
        word_timestamps=True,
        vad_filter=False,          # pausas são informação editorial; não descartar
        condition_on_previous_text=False,  # reduz "alucinação" que repete frases
        beam_size=5,
        hotwords=", ".join(termos) or None,
        initial_prompt=("Termos: " + ", ".join(termos) + ".") if termos else None,
    )
    segs = []
    for s in segmentos:
        segs.append({
            "inicio": round(s.start, 3), "fim": round(s.end, 3), "texto": s.text.strip(),
            "palavras": [{"p": w.word.strip(), "inicio": round(w.start, 3), "fim": round(w.end, 3),
                          "conf": round(w.probability, 3)} for w in (s.words or [])],
        })
    t_trans = time.time() - t1

    resultado = {
        "arquivo": entrada, "modelo": modelo, "glossario": termos, "idioma": info.language,
        "duracao_audio": round(info.duration, 2),
        "tempo_carga_s": round(t_carga, 1), "tempo_transcricao_s": round(t_trans, 1),
        "fator_tempo_real": round(t_trans / info.duration, 2),
        "segmentos": segs,
    }
    with open(saida, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    return resultado


if __name__ == "__main__":
    args = sys.argv[1:]
    r = transcrever(*args)
    print(f"{r['modelo']}: {r['duracao_audio']}s de áudio em {r['tempo_transcricao_s']}s "
          f"(fator {r['fator_tempo_real']}x) · {len(r['segmentos'])} segmentos")
