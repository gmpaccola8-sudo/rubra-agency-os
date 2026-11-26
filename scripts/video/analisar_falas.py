"""Analisa uma transcrição (saída de transcrever.py) e PROPÕE uma lista de cortes.

Detecta: pausas longas, takes repetidos (frase regravada logo depois) e falsos inícios
(frase abandonada). É uma proposta editorial — a decisão final é de quem dirige a edição.

Uso:
  python analisar_falas.py <transcricao.json> <proposta.json> [pausa_max_s=0.8]

Saída (proposta.json):
  manter: trechos a manter [{inicio, fim, texto}]
  removidos: o que saiu e por quê
  resumo: duração original x proposta
"""
import json
import re
import sys
from difflib import SequenceMatcher

PADDING = 0.12          # respiro antes/depois de cada fala (s): evita cortar sílabas
PAUSA_NATURAL = 0.35    # pausa mantida entre frases depois de encurtar pausa longa
MARCAS_ABANDONO = re.compile(r"(\.\.\.|…|\bn[ãa]o,?\s*espera\b|\bdesculp|\bde novo\b|\brecome)", re.I)


def normalizar(t: str) -> str:
    return re.sub(r"[^\w\s]", "", t.lower()).strip()


def frases(transcricao: dict) -> list[dict]:
    """Reagrupa palavras em frases pela pontuação final — segmentos do Whisper
    nem sempre coincidem com frases."""
    saida, atual = [], []
    for seg in transcricao["segmentos"]:
        for w in seg["palavras"]:
            atual.append(w)
            if re.search(r"[.!?]$", w["p"]):
                saida.append(atual)
                atual = []
    if atual:
        saida.append(atual)
    return [{"inicio": f[0]["inicio"], "fim": f[-1]["fim"],
             "texto": " ".join(w["p"] for w in f),
             "conf_media": round(sum(w["conf"] for w in f) / len(f), 3)} for f in saida]


def analisar(transcricao: dict, pausa_max: float = 0.8) -> dict:
    fs = frases(transcricao)
    removidos, candidatos = [], []

    def inicio(t, n=3):
        return normalizar(t).split()[:n]

    descartar_ate = -1
    for i, f in enumerate(fs):
        if i <= descartar_ate:
            removidos.append({**f, "motivo": "parte de falso início (correção falada)"})
            continue
        # Falso início estrutural: uma das 2 frases seguintes recomeça com as mesmas 3 palavras
        # e é mais longa. Independe do que foi dito no abandono (o Whisper pode transcrever
        # "a... não, espera" de formas diferentes). Frases curtas no meio (≤ 3 palavras,
        # ex.: "Espera.") são a correção falada e saem junto.
        recomeco = next((j for j in (i + 1, i + 2) if j < len(fs)
                         and len(inicio(f["texto"])) == 3 and inicio(fs[j]["texto"]) == inicio(f["texto"])
                         and len(fs[j]["texto"]) > len(f["texto"])
                         and all(len(normalizar(fs[k]["texto"]).split()) <= 3 for k in range(i + 1, j))), None)
        if recomeco is not None and not normalizar(fs[recomeco]["texto"]).startswith(normalizar(f["texto"])):
            removidos.append({**f, "motivo": "falso início (frase recomeçada logo depois)"})
            descartar_ate = recomeco - 1
            continue
        # Falso início por marca explícita de abandono.
        if MARCAS_ABANDONO.search(f["texto"]):
            removidos.append({**f, "motivo": "falso início (frase abandonada)"})
            continue
        # Take repetido: a frase seguinte começa igual a esta (regravação).
        if i + 1 < len(fs):
            a, b = normalizar(f["texto"]), normalizar(fs[i + 1]["texto"])
            prefixo = b[: len(a)]
            if len(a) > 10 and SequenceMatcher(None, a, prefixo).ratio() > 0.85:
                removidos.append({**f, "motivo": "take repetido (mantido o seguinte, mais completo)"})
                continue
        candidatos.append(f)

    # Pausas: encurta as longas, preserva as naturais.
    manter = []
    for i, f in enumerate(candidatos):
        ini = max(0.0, f["inicio"] - PADDING)
        fim = f["fim"] + PADDING
        if manter:
            gap = ini - manter[-1]["fim"]
            if gap <= 0:
                ini = manter[-1]["fim"]
            elif gap > pausa_max:
                removidos.append({"inicio": round(manter[-1]["fim"], 3), "fim": round(ini, 3),
                                  "texto": None, "motivo": f"pausa longa ({gap:.1f}s → {PAUSA_NATURAL}s)"})
                manter[-1]["fim"] += PAUSA_NATURAL / 2
                ini -= PAUSA_NATURAL / 2
        manter.append({"inicio": round(ini, 3), "fim": round(fim, 3), "texto": f["texto"]})

    dur_orig = transcricao["duracao_audio"]
    dur_nova = sum(m["fim"] - m["inicio"] for m in manter)
    return {
        "fonte": transcricao["arquivo"],
        "manter": manter,
        "removidos": sorted(removidos, key=lambda r: r["inicio"]),
        "resumo": {"duracao_original_s": dur_orig, "duracao_proposta_s": round(dur_nova, 2),
                   "reducao_pct": round(100 * (1 - dur_nova / dur_orig), 1)},
    }


if __name__ == "__main__":
    t = json.load(open(sys.argv[1], encoding="utf-8"))
    pausa = float(sys.argv[3]) if len(sys.argv) > 3 else 0.8
    r = analisar(t, pausa)
    json.dump(r, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(json.dumps(r["resumo"], ensure_ascii=False))
    for x in r["removidos"]:
        print(f"  − {x['inicio']:6.2f}–{x['fim']:6.2f}  {x['motivo']}  {x['texto'] or ''}")
