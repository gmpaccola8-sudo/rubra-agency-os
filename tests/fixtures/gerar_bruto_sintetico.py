"""Gera um "vídeo bruto" sintético em português para testar o pipeline de edição.

Simula problemas reais de gravação: falso início, frase repetida (dois takes),
pausas longas e ruído de fundo. Nenhuma mídia é versionada — só este gerador.

Uso:
  python gerar_bruto_sintetico.py <modelo_piper.onnx> <pasta_saida>
Saída: <pasta_saida>/bruto.mp4 e <pasta_saida>/roteiro_esperado.json
"""
import json
import subprocess
import sys
import wave
from pathlib import Path

from piper import PiperVoice

ROTEIRO = [
    ("fala", "Oi, eu sou a... não, espera.", "falso_inicio"),
    ("pausa", 2.5, "pausa_longa"),
    ("fala", "Oi, eu sou a Gabriela, diretora criativa da Rubra.", "manter"),
    ("pausa", 0.4, "pausa_natural"),
    ("fala", "Hoje eu quero falar sobre por que tantas marcas parecem iguais.", "manter"),
    ("pausa", 3.0, "pausa_longa"),
    ("fala", "A maioria das marcas começa pelo visual.", "take_repetido"),
    ("pausa", 0.5, "pausa_natural"),
    ("fala", "A maioria das marcas começa pelo visual, antes de saber o que quer dizer.", "manter"),
    ("pausa", 0.6, "pausa_natural"),
    ("fala", "Quando a estratégia vem primeiro, o design deixa de ser decoração e passa a ser argumento.", "manter"),
    ("pausa", 2.0, "pausa_longa"),
    ("fala", "Se isso faz sentido pra você, me chama no direct.", "manter"),
]


def main(modelo: str, saida: str) -> None:
    out = Path(saida)
    out.mkdir(parents=True, exist_ok=True)
    voz = PiperVoice.load(modelo)
    taxa = voz.config.sample_rate

    pecas, esperado, t = [], [], 0.0
    for i, (tipo, valor, rotulo) in enumerate(ROTEIRO):
        arq = out / f"_parte{i:02d}.wav"
        if tipo == "fala":
            with wave.open(str(arq), "wb") as w:
                voz.synthesize_wav(valor, w)
        else:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                            f"anullsrc=r={taxa}:cl=mono", "-t", str(valor), str(arq)], check=True)
        with wave.open(str(arq)) as w:
            dur = w.getnframes() / w.getframerate()
        esperado.append({"tipo": tipo, "texto": valor if tipo == "fala" else None,
                         "rotulo": rotulo, "inicio": round(t, 3), "fim": round(t + dur, 3)})
        t += dur
        pecas.append(arq)

    lista = out / "_lista.txt"
    lista.write_text("".join(f"file '{p.name}'\n" for p in pecas))
    voz_wav = out / "_voz.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lista),
                    "-c", "copy", str(voz_wav)], check=True)

    # Vídeo 1080x1920 30fps com ruído de sala (-42 dB) e um "enquadramento" simples
    # com relógio, para que cortes errados fiquem visíveis na inspeção de quadros.
    subprocess.run([
        "ffmpeg", "-v", "error", "-y",
        "-f", "lavfi", "-i", f"color=c=0x2b2b2b:s=1080x1920:r=30:d={t:.3f}",
        "-i", str(voz_wav),
        "-f", "lavfi", "-i", f"anoisesrc=c=pink:a=0.008:d={t:.3f}:r=48000",
        "-filter_complex",
        "[0:v]drawbox=x=240:y=560:w=600:h=800:color=0x8a6f5a:t=fill,"
        "drawtext=text='BRUTO %{pts\\:hms}':x=60:y=120:fontsize=56:fontcolor=white[v];"
        "[1:a]aresample=48000,volume=0.9[a1];[a1][2:a]amix=inputs=2:duration=first:normalize=0[a]",
        "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
        "-b:a", "160k", str(out / "bruto.mp4")], check=True)

    (out / "roteiro_esperado.json").write_text(json.dumps(esperado, ensure_ascii=False, indent=2))
    for p in [*pecas, lista, voz_wav]:
        p.unlink()
    print(f"bruto.mp4 gerado: {t:.2f}s")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
