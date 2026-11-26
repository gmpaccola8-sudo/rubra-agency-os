"""Inspeção técnica de um vídeo renderizado. Produz evidências, não opinião.

Verifica: codec, resolução, fps, duração, loudness integrado e pico real (EBU R128),
quadros pretos, silêncios longos, e gera uma folha de contato com os quadros
de cada ponto de corte (para inspeção visual por quem revisa).

Uso:
  python inspecionar.py <video.mp4> <pasta_relatorio> [proposta.json]
Saída: relatorio.json + folha_cortes.png + folha_geral.png
"""
import json
import re
import subprocess
import sys
from pathlib import Path

LIMITES = {"loudness_min": -16.0, "loudness_max": -12.0, "pico_max_dbtp": -1.0,
           "silencio_max_s": 1.2, "preto_max_s": 0.1}


def rodar(cmd: list[str]) -> str:
    return subprocess.run(cmd, capture_output=True, text=True).stderr


def inspecionar(video: str, pasta: str, proposta: dict | None = None) -> dict:
    out = Path(pasta)
    out.mkdir(parents=True, exist_ok=True)
    probe = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration,bit_rate:stream=codec_type,codec_name,width,height,r_frame_rate,pix_fmt,sample_rate,channels",
         "-of", "json", video], capture_output=True, text=True, check=True).stdout)
    v = next(s for s in probe["streams"] if s["codec_type"] == "video")
    a = next((s for s in probe["streams"] if s["codec_type"] == "audio"), None)
    dur = float(probe["format"]["duration"])

    eb = rodar(["ffmpeg", "-nostdin", "-i", video, "-af", "ebur128=peak=true", "-f", "null", "-"])
    integ = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", eb)[-1])
    pico = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", eb)[-1])

    sil = rodar(["ffmpeg", "-nostdin", "-i", video, "-af", "silencedetect=n=-45dB:d=0.8", "-f", "null", "-"])
    silencios = [float(x) for x in re.findall(r"silence_duration: ([\d.]+)", sil)]

    bl = rodar(["ffmpeg", "-nostdin", "-i", video, "-vf", "blackdetect=d=0.05:pix_th=0.05", "-an", "-f", "null", "-"])
    pretos = [float(x) for x in re.findall(r"black_duration:([\d.]+)", bl)]

    # Folha geral: 12 quadros distribuídos ao longo do vídeo.
    n = 12
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-nostdin", "-i", video, "-vf",
                    f"fps={n}/{dur:.3f},scale=270:-1,tile=6x2:padding=6:color=white",
                    "-frames:v", "1", str(out / "folha_geral.png")], check=True)

    # Folha de cortes: quadro antes e depois de cada ponto de corte.
    cortes = []
    if proposta:
        acc = 0.0
        for m in proposta["manter"][:-1]:
            acc += m["fim"] - m["inicio"]
            cortes.append(round(acc, 3))
    if cortes:
        tempos = [t for c in cortes for t in (max(0, c - 0.1), c + 0.1)]
        sel = "+".join(f"between(t,{t:.3f},{t + 1 / 30:.3f})" for t in tempos)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-nostdin", "-i", video, "-vf",
                        f"select='{sel}',scale=270:-1,tile=2x{len(cortes)}:padding=6:color=white",
                        "-vsync", "vfr", "-frames:v", "1", str(out / "folha_cortes.png")], check=True)

    falhas = []
    if not (LIMITES["loudness_min"] <= integ <= LIMITES["loudness_max"]):
        falhas.append(f"loudness {integ} LUFS fora de {LIMITES['loudness_min']}..{LIMITES['loudness_max']}")
    if pico > LIMITES["pico_max_dbtp"]:
        falhas.append(f"pico {pico} dB acima de {LIMITES['pico_max_dbtp']}")
    if any(s > LIMITES["silencio_max_s"] for s in silencios):
        falhas.append(f"silêncio longo: {max(silencios):.2f}s")
    if any(p > LIMITES["preto_max_s"] for p in pretos):
        falhas.append(f"quadro preto: {max(pretos):.2f}s")
    if v["codec_name"] != "h264" or v.get("pix_fmt") != "yuv420p":
        falhas.append(f"vídeo {v['codec_name']}/{v.get('pix_fmt')} (esperado h264/yuv420p)")
    if not a or a["codec_name"] != "aac":
        falhas.append("áudio ausente ou não-AAC")

    rel = {
        "arquivo": video, "duracao_s": round(dur, 2),
        "video": f"{v['codec_name']} {v['width']}x{v['height']} {v['r_frame_rate']} {v.get('pix_fmt')}",
        "audio": f"{a['codec_name']} {a['sample_rate']}Hz {a['channels']}ch" if a else None,
        "loudness_lufs": integ, "pico_dbfs": pico,
        "silencios_s": silencios, "quadros_pretos_s": pretos, "pontos_de_corte_s": cortes,
        "falhas_tecnicas": falhas, "aprovado_tecnicamente": not falhas,
        "aviso": "Aprovação técnica não é aprovação criativa: as folhas de quadros precisam ser olhadas.",
    }
    (out / "relatorio.json").write_text(json.dumps(rel, ensure_ascii=False, indent=2), encoding="utf-8")
    return rel


if __name__ == "__main__":
    prop = json.load(open(sys.argv[3], encoding="utf-8")) if len(sys.argv) > 3 else None
    print(json.dumps(inspecionar(sys.argv[1], sys.argv[2], prop), ensure_ascii=False, indent=2))
