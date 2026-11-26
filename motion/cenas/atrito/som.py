"""Sonoplastia sintetizada do teste "Atrito" — 100% original (sem licença de terceiros).

Cada som é derivado dos MESMOS tempos da cena (lidos de cena.js), então a sincronia é
estrutural, não ajustada no olho. A amplitude dos sons de atrito segue a VELOCIDADE do objeto
(a gaveta soa mais quando corre mais rápido; o risco acelera junto com a cabeça do fósforo).

Uso: python som.py <cena.js> <saida.wav>
"""
import json
import re
import sys
import wave

import numpy as np

SR = 48000
rng = np.random.default_rng(1977)


def tempos(cena_js: str) -> dict:
    bloco = re.search(r"export const TEMPOS = \{(.*?)\};", open(cena_js, encoding="utf-8").read(), re.S).group(1)
    return {k: float(v) for k, v in re.findall(r"(\w+):\s*([\d.]+)", bloco)}


def banda(x, lo, hi):
    """Filtro passa-faixa por FFT com bordas suaves."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    m = 1 / (1 + (lo / np.maximum(f, 1)) ** 4) * 1 / (1 + (f / hi) ** 4)
    return np.fft.irfft(X * m, len(x))


def env(n, a, d):
    """Envelope ataque/decaimento exponencial (segundos)."""
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) / max(d, 1e-4))


def norm(x):
    """Pico em 1. Cada elemento é normalizado antes do ganho de mixagem (como numa mesa)."""
    return x / max(1e-9, np.abs(x).max())


def prog(t, a, b):
    return np.clip((t - a) / (b - a), 0, 1)


def gerar(T: dict) -> np.ndarray:
    n = int(T["duracao"] * SR)
    t = np.arange(n) / SR
    L, R = np.zeros(n), np.zeros(n)

    def soma(sinal, inicio, pan=0.0, ganho=1.0):  # pan -1 (esq) .. 1 (dir)
        i = int(inicio * SR)
        s = sinal[: max(0, n - i)] * ganho
        L[i:i + len(s)] += s * np.sqrt((1 - pan) / 2)
        R[i:i + len(s)] += s * np.sqrt((1 + pan) / 2)

    # Ambiente: sala silenciosa (ruído marrom grave), some no cartão final
    marrom = np.cumsum(rng.standard_normal(n)); marrom -= np.convolve(marrom, np.ones(4800) / 4800, "same")
    amb = banda(marrom, 30, 400); amb = norm(amb)
    amb *= 0.05 * (1 - 0.6 * prog(t, T["cartaoInicio"], T["duracao"]))
    soma(amb, 0)

    # Gaveta: papel deslizando; amplitude = velocidade da gaveta (derivada do easeInOut)
    g0, g1 = T["gavetaInicio"], T["gavetaFim"]
    k = prog(t, g0, g1)
    vel = np.where((t > g0) & (t < g1), np.where(k < 0.5, 12 * k * k, 12 * (1 - k) ** 2), 0)
    papel = banda(rng.standard_normal(n), 900, 5200) * (0.6 + 0.4 * banda(rng.standard_normal(n), 10, 60) * 8)
    soma(norm(papel * vel) * 0.38, 0, pan=0.35)

    # Fósforo tirado da gaveta: pequeno toque de madeira
    tique = banda(rng.standard_normal(int(0.04 * SR)), 1500, 6000) * env(int(0.04 * SR), 0.001, 0.008)
    soma(norm(tique) * 0.3, T["fosforoSobeInicio"], pan=0.3)

    # Risco: raspar áspero que acelera (easeIn) e corre da esquerda para a direita
    r0, rc, r1 = T["riscoContato"], T["riscoContato"], T["ignicao"]
    nr = int((r1 - r0) * SR)
    kr = np.arange(nr) / nr
    raspa = banda(rng.standard_normal(nr), 1800, 9000)
    graos = (rng.random(nr) > 0.9965) * rng.standard_normal(nr) * 6       # grãos da lixa
    raspa = raspa + banda(graos, 2000, 12000)
    raspa = norm(raspa * (0.25 + 0.75 * kr ** 2) * np.minimum(1, kr * 40))  # entra seco, cresce
    for i, pan in enumerate(np.linspace(-0.7, 0.6, 8)):                      # acompanha a cabeça
        a, b = i * nr // 8, (i + 1) * nr // 8
        seg = np.zeros(nr); seg[a:b] = raspa[a:b]
        soma(seg * 0.85, rc, pan=pan)

    # Ignição: estalo + sopro (fwoomp) com varredura de brilho, e um peso grave curto
    ni = int(0.6 * SR)
    estalo = banda(rng.standard_normal(int(0.02 * SR)), 2500, 14000) * env(int(0.02 * SR), 0.0005, 0.004)
    ruido_ign = rng.standard_normal(ni)
    abre = np.minimum(1, np.arange(ni) / (0.12 * SR))                       # o brilho do sopro abre
    sopro = norm(banda(ruido_ign, 120, 900) * (1 - abre) + banda(ruido_ign, 120, 3800) * abre)
    sopro *= env(ni, 0.025, 0.2)
    peso = np.sin(2 * np.pi * 70 * np.arange(ni) / SR) * env(ni, 0.005, 0.09)
    soma(norm(estalo) * 0.6, T["ignicao"], pan=0.5)
    soma(sopro * 0.75 + norm(peso) * 0.45, T["ignicao"], pan=0.3)

    # Chama acesa: rugido suave + crepitar esparso
    c0, c1 = T["ignicao"] + 0.1, T["cartaoFim"]
    nc = int((c1 - c0) * SR)
    rugido = norm(banda(rng.standard_normal(nc), 60, 700)) * 0.12
    crep = (rng.random(nc) > 0.9993) * rng.standard_normal(nc) * 3
    crep = norm(banda(crep, 1500, 9000)) * 0.28
    fade = np.minimum(1, np.arange(nc) / (0.2 * SR)) * np.minimum(1, (nc - np.arange(nc)) / (0.25 * SR))
    soma((rugido + crep) * fade, c0, pan=0.15)

    # Mergulho: sopro crescente que sobe de brilho (movimento motivado → transição)
    m0, m1 = T["mergulhoInicio"], T["cartaoInicio"] + 0.25
    nm = int((m1 - m0) * SR)
    km = np.arange(nm) / nm
    ar = banda(rng.standard_normal(nm), 200, 2500) * km ** 2.2
    ar *= np.minimum(1, (nm - np.arange(nm)) / (0.08 * SR))
    soma(norm(ar) * 0.5, m0)

    # Assinatura: uma única nota grave e quente (sem "whoosh" de logo genérico)
    na = int((T["duracao"] - T["cartaoInicio"]) * SR)
    ta = np.arange(na) / SR
    nota = (np.sin(2 * np.pi * 55 * ta) + 0.5 * np.sin(2 * np.pi * 110 * ta + 0.3) + 0.18 * np.sin(2 * np.pi * 165 * ta))
    nota = norm(nota * env(na, 0.12, 0.9)) * 0.2
    soma(nota, T["cartaoInicio"] + 0.1)

    est = np.stack([L, R], 1)
    est /= max(1e-9, np.abs(est).max()) / 0.89   # pico em -1 dBFS; loudness final ajustado no render
    fim = int(0.15 * SR)
    est[-fim:] *= np.linspace(1, 0, fim)[:, None]
    return est


def salvar(est: np.ndarray, caminho: str) -> None:
    pcm = (np.clip(est, -1, 1) * 32767).astype("<i2")
    with wave.open(caminho, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


if __name__ == "__main__":
    T = tempos(sys.argv[1])
    salvar(gerar(T), sys.argv[2])
    print(json.dumps(T))
