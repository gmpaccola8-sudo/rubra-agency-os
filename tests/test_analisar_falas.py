"""Testes de regressão da análise de falas. Rodam sem mídia e sem modelos.

python3 -I tests/test_analisar_falas.py   (sai com código 1 se algum caso falhar)

Cada caso reproduz uma forma REAL como o Whisper transcreveu o mesmo áudio em execuções
diferentes — a análise precisa chegar ao mesmo corte independentemente da pontuação.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "video"))
from analisar_falas import analisar  # noqa: E402


def transcricao(frases_com_tempo: list[tuple[str, float, float]], duracao: float) -> dict:
    segs = []
    for texto, ini, fim in frases_com_tempo:
        ws = texto.split()
        passo = (fim - ini) / len(ws)
        segs.append({"inicio": ini, "fim": fim, "texto": texto, "palavras": [
            {"p": w, "inicio": round(ini + i * passo, 3), "fim": round(ini + (i + 1) * passo, 3), "conf": 0.9}
            for i, w in enumerate(ws)]})
    return {"arquivo": "teste", "duracao_audio": duracao, "segmentos": segs}


CERTA = ("Oi, eu sou a Gabriela, diretora criativa da Rubra.", 4.6, 7.5)
RESTO = [
    ("Hoje eu quero falar sobre por que tantas marcas parecem iguais.", 8.3, 11.5),
    ("A maioria das marcas começa pelo visual.", 14.8, 17.3),
    ("A maioria das marcas começa pelo visual, antes de saber o que quer dizer.", 18.3, 22.2),
]

CASOS = {
    # forma vista com o modelo small
    "marca explícita": [("Oi, eu sou A, não, espera.", 0.0, 1.7), CERTA, *RESTO],
    # forma vista com large-v3-turbo: abandono vira palavras sem sentido + correção separada
    "abandono com correção separada": [("Oi, eu sou o Anão.", 0.0, 1.2), ("Espera.", 1.4, 1.9), CERTA, *RESTO],
    # forma da sessão nova: tudo colado numa frase só
    "falso início colado na frase": [("Oi, eu sou o Anão Espera, Oi, eu sou a Gabriela, diretora criativa da Rubra.", 0.0, 7.5), *RESTO],
}


def main() -> int:
    falhas = 0
    for nome, frases in CASOS.items():
        r = analisar(transcricao(frases, 33.0))
        mantidos = " ".join(m["texto"] for m in r["manter"])
        ok = (mantidos.startswith("Oi, eu sou a Gabriela")
              and "Anão" not in mantidos and "espera" not in mantidos.lower()
              and mantidos.count("A maioria das marcas") == 1
              and "antes de saber" in mantidos)
        print(f"{'OK   ' if ok else 'FALHA'} {nome}")
        if not ok:
            print("      manteve:", mantidos)
            falhas += 1
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
