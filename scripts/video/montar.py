"""Monta o vídeo editado a partir de uma proposta de cortes aprovada.

Etapas, em um único render de vídeo (sem perda por recompressão dupla):
  1. Cortes nos tempos exatos, com micro-fades de áudio (evita estalos nos cortes).
  2. Voz: corte de graves (80 Hz), redução de ruído leve, compressão suave.
  3. Loudness em duas passagens (EBU R128): mede primeiro, aplica depois.
  4. Legendas a partir das palavras transcritas, remapeadas para a nova linha do tempo.
  5. Exporta MP4 H.264 + AAC, pronto para redes (faststart).

Uso:
  python montar.py <video_bruto> <proposta.json> <transcricao.json> <saida.mp4> [estilo.json]

estilo.json (opcional — camada do cliente; sem ele, usa um padrão neutro):
  {"fonte": "Inter", "peso_negrito": true, "tamanho": 64, "cor": "#FFFFFF",
   "contorno_cor": "#000000", "contorno": 0, "sombra": 0, "caixa": true, "caixa_cor": "#000000",
   "caixa_opacidade": 0.55, "margem_inferior": 520, "max_caracteres": 28, "caixa_alta": false,
   "loudness_alvo": -14}
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ESTILO_PADRAO = {
    "fonte": "Inter", "peso_negrito": True, "tamanho": 64, "cor": "#FFFFFF",
    "contorno_cor": "#000000", "contorno": 0, "sombra": 0,
    "caixa": True, "caixa_cor": "#000000", "caixa_opacidade": 0.55,
    "margem_inferior": 520,   # 1920px: mantém a legenda acima da interface do Reels/TikTok
    "max_caracteres": 28, "caixa_alta": False, "loudness_alvo": -14,
}
FADE = 0.012  # s


def ass_cor(hex_cor: str, opacidade: float = 1.0) -> str:
    h = hex_cor.lstrip("#")
    alpha = int(round((1 - opacidade) * 255))
    return f"&H{alpha:02X}{h[4:6]}{h[2:4]}{h[0:2]}".upper()


def ass_tempo(t: float) -> str:
    t = max(0.0, t)
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def srt_tempo(t: float) -> str:
    ms = int(round(max(0.0, t) * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def sonda(video: str) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate", "-of", "json", video],
                         capture_output=True, text=True, check=True).stdout
    s = json.loads(out)["streams"][0]
    n, d = s["r_frame_rate"].split("/")
    return {"w": s["width"], "h": s["height"], "fps": float(n) / float(d)}


def remapear_palavras(transcricao: dict, manter: list[dict]) -> list[dict]:
    """Converte o tempo de cada palavra mantida para a nova linha do tempo."""
    offsets, acc = [], 0.0
    for m in manter:
        offsets.append(acc)
        acc += m["fim"] - m["inicio"]
    saida = []
    for seg in transcricao["segmentos"]:
        for w in seg["palavras"]:
            meio = (w["inicio"] + w["fim"]) / 2
            for m, off in zip(manter, offsets):
                if m["inicio"] <= meio <= m["fim"]:
                    saida.append({"p": w["p"],
                                  "inicio": off + max(w["inicio"], m["inicio"]) - m["inicio"],
                                  "fim": off + min(w["fim"], m["fim"]) - m["inicio"]})
                    break
    return saida


PALAVRAS_FRACAS = {
    "o", "a", "os", "as", "um", "uma", "uns", "umas", "de", "do", "da", "dos", "das", "em", "no", "na",
    "nos", "nas", "por", "pelo", "pela", "para", "pra", "com", "sem", "e", "ou", "mas", "que", "se",
    "ao", "à", "aos", "às", "num", "numa", "eu", "me", "te", "lhe", "seu", "sua", "meu", "minha",
}


def _fraca(w: dict) -> bool:
    return re.sub(r"[^\w]", "", w["p"].lower()) in PALAVRAS_FRACAS


def cartelas(palavras: list[dict], max_chars: int) -> list[dict]:
    """Agrupa palavras em cartelas legíveis.

    Regras (aprendidas na inspeção visual do teste 1):
      - Fim de frase (. ! ?) sempre fecha a cartela: uma cartela nunca mistura duas frases.
      - Pausa > 0,3 s fecha a cartela: nunca atravessa um corte ou respiração.
      - Vírgula/;/: fecha a cartela se ela já tiver ~40% do limite.
      - Ao estourar o limite, a cartela não termina em palavra fraca (artigo, preposição,
        conjunção): ela passa para a próxima cartela.
    """
    def tamanho(ws):
        return len(" ".join(x["p"] for x in ws))

    out, atual = [], []
    for w in palavras:
        if atual and w["inicio"] - atual[-1]["fim"] > 0.3:
            out.append(atual)
            atual = []
        if atual and tamanho(atual + [w]) > max_chars:
            levar = []
            while len(atual) > 1 and _fraca(atual[-1]):
                levar.insert(0, atual.pop())
            out.append(atual)
            atual = levar
        atual.append(w)
        if re.search(r"[.!?]$", w["p"]) or (re.search(r"[,;:]$", w["p"]) and tamanho(atual) >= max_chars * 0.4):
            out.append(atual)
            atual = []
    if atual:
        out.append(atual)
    res = []
    for i, c in enumerate(out):
        fim = c[-1]["fim"] + 0.15
        if i + 1 < len(out):
            fim = min(fim, out[i + 1][0]["inicio"])
        res.append({"inicio": c[0]["inicio"], "fim": fim, "texto": " ".join(x["p"] for x in c)})
    return res


def gerar_ass(cards: list[dict], estilo: dict, w: int, h: int) -> str:
    e = {**ESTILO_PADRAO, **estilo}
    borda = 3 if e["caixa"] else 1  # 3 = caixa opaca atrás do texto
    contorno_ou_caixa = ass_cor(e["caixa_cor"], e["caixa_opacidade"]) if e["caixa"] else ass_cor(e["contorno_cor"])
    linhas = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {w}", f"PlayResY: {h}",
        "WrapStyle: 0", "ScaledBorderAndShadow: yes", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, "
        "Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Rubra,{e['fonte']},{e['tamanho']},{ass_cor(e['cor'])},{ass_cor(e['cor'])},"
        f"{contorno_ou_caixa},{contorno_ou_caixa},{-1 if e['peso_negrito'] else 0},0,0,0,100,100,0,0,"
        f"{borda},{e['contorno'] if not e['caixa'] else 18},{e['sombra']},2,90,90,{e['margem_inferior']},1",
        "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for c in cards:
        txt = c["texto"].upper() if e["caixa_alta"] else c["texto"]
        txt = txt.replace("{", "(").replace("}", ")")
        linhas.append(f"Dialogue: 0,{ass_tempo(c['inicio'])},{ass_tempo(c['fim'])},Rubra,,0,0,0,,{txt}")
    return "\n".join(linhas) + "\n"


def filtro_cortes(manter: list[dict], cadeia_voz: str) -> str:
    partes, rot = [], []
    for i, m in enumerate(manter):
        a, b = m["inicio"], m["fim"]
        d = b - a
        partes.append(f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS[v{i}]")
        partes.append(f"[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,"
                      f"afade=t=in:d={FADE},afade=t=out:st={max(0, d - FADE):.3f}:d={FADE}[a{i}]")
        rot.append(f"[v{i}][a{i}]")
    partes.append(f"{''.join(rot)}concat=n={len(manter)}:v=1:a=1[vc][ac]")
    partes.append(f"[ac]{cadeia_voz}[ao]")
    return ";".join(partes)


def montar(bruto: str, proposta: dict, transcricao: dict, saida: str, estilo: dict | None = None) -> dict:
    estilo = {**ESTILO_PADRAO, **(estilo or {})}
    manter = proposta["manter"]
    info = sonda(bruto)
    voz = "highpass=f=80,afftdn=nf=-28:tn=1,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2"
    alvo = estilo["loudness_alvo"]

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        # Passagem 1: medir loudness do áudio já cortado e tratado.
        f1 = filtro_cortes(manter, voz + f",loudnorm=I={alvo}:TP=-1.5:LRA=11:print_format=json")
        r = subprocess.run(["ffmpeg", "-v", "info", "-nostdin", "-i", bruto, "-filter_complex", f1,
                            "-map", "[vc]", "-map", "[ao]", "-f", "null", "-"], capture_output=True, text=True, check=True)
        med = json.loads(re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr)[-1])

        # Legendas.
        palavras = remapear_palavras(transcricao, manter)
        cards = cartelas(palavras, estilo["max_caracteres"])
        ass = tmp / "legendas.ass"
        ass.write_text(gerar_ass(cards, estilo, info["w"], info["h"]), encoding="utf-8")

        # Passagem 2: render final.
        ln = (f"loudnorm=I={alvo}:TP=-1.5:LRA=11:measured_I={med['input_i']}:measured_TP={med['input_tp']}:"
              f"measured_LRA={med['input_lra']}:measured_thresh={med['input_thresh']}:"
              f"offset={med['target_offset']}:linear=true,aresample=48000")
        f2 = filtro_cortes(manter, voz + "," + ln) + f";[vc]subtitles=filename='{ass}'[vo]"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-nostdin", "-i", bruto, "-filter_complex", f2,
                        "-map", "[vo]", "-map", "[ao]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                        "-pix_fmt", "yuv420p", "-r", f"{info['fps']:.3f}", "-c:a", "aac", "-ac", "2", "-b:a", "192k",
                        "-movflags", "+faststart", saida], check=True)
        # Guarda as legendas também em SRT editável, ao lado do vídeo.
        srt = Path(saida).with_suffix(".srt")
        srt.write_text("".join(
            f"{i}\n{srt_tempo(c['inicio'])} --> {srt_tempo(c['fim'])}\n{c['texto']}\n\n"
            for i, c in enumerate(cards, 1)), encoding="utf-8")
    return {"saida": saida, "cartelas": len(cards), "loudness_medida_antes": med["input_i"], "alvo": alvo}


if __name__ == "__main__":
    bruto, prop, trans, saida = sys.argv[1:5]
    est = json.load(open(sys.argv[5], encoding="utf-8")) if len(sys.argv) > 5 else None
    r = montar(bruto, json.load(open(prop, encoding="utf-8")), json.load(open(trans, encoding="utf-8")), saida, est)
    print(json.dumps(r, ensure_ascii=False))
