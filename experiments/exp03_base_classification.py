#!/usr/bin/env python3
"""
Test 3 extendido:
  (A) k = 2..11 para opción 1 (PL) — oscilación con la factorización de k.
  (B) k = 2..8 para opciones 2, 3, 4 — universalidad del patrón.
  (C) comparación de celdas no vacías entre opciones.

Usa generate_poda (canonical augmentation) para generar canónicas sin
enumerar todos los candidatos crudos, lo cual es prohibitivo para k ≥ 7.
"""

import os
import sys
from itertools import permutations
from collections import Counter, defaultdict
from time import perf_counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CAUGJAM_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, CAUGJAM_DIR)

from caugjam import generate_poda


# ──────────────────────────────────────────────────────────────────────
# Clasificación combinatoria (idéntica a Test 3 original)
# ──────────────────────────────────────────────────────────────────────

S3 = list(permutations("ABC"))

def apply_perm(w, perm):
    mp = dict(zip("ABC", perm))
    return "".join(mp[c] for c in w)

def is_s3_palindromic(w):
    rw = w[::-1]
    return any(apply_perm(w, p) == rw for p in S3)

def is_periodic(w):
    n = len(w)
    for d in range(1, n):
        if n % d == 0 and w[:d] * (n // d) == w:
            return True
    return False

def classify(w):
    p, q = is_s3_palindromic(w), is_periodic(w)
    if p and q: return "PP"   # periódica palindrómica
    if q:       return "Pp"   # periódica pura
    if p:       return "pP"   # palindrómica pura
    return              "Ap"   # aperiódica


def chain_to_word(chain):
    """
    Proyecta una cadena canónica de opciones 1-4 a su palabra ABC.
    La letra es la posición del +0 en cada fila.
    """
    blocks = chain.split("/")
    cols = []
    for blk in blocks:
        toks, i = [], 0
        while i < len(blk):
            if blk[i] == "(":
                toks.append(blk[i:i+6]); i += 6
            else:
                toks.append(blk[i:i+2]); i += 2
        cols.append(toks)
    k = len(cols[0])
    word = []
    for i in range(k):
        row = [cols[c][i] for c in range(3)]
        letter = None
        for pos, tok in enumerate(row):
            if tok == "+0":
                letter = "ABC"[pos]
                break
        if letter is None:
            raise ValueError(f"fila sin +0: {row} en {chain}")
        word.append(letter)
    return "".join(word)


# ──────────────────────────────────────────────────────────────────────
# Cómputo
# ──────────────────────────────────────────────────────────────────────

def tabla_para_opcion(option, ks, verbose=True):
    n_max = max(ks)
    t0 = perf_counter()
    classes = generate_poda(n_max, option)
    t_gen = perf_counter() - t0

    if verbose:
        print(f"  [opción {option}] generación hasta k={n_max} en {t_gen:.2f}s")
        print(f"  [opción {option}] órbitas por k: " +
              ", ".join(f"k={k}:{len(classes[k])}" for k in ks if k in classes))

    resultados = {}
    for k in ks:
        if k not in classes:
            continue
        cells = Counter()
        examples = defaultdict(list)
        for ch in classes[k]:
            w = chain_to_word(ch)
            c = classify(w)
            cells[c] += 1
            if len(examples[c]) < 3:
                examples[c].append(w)
        n_orb = len(classes[k])
        n_nv = sum(1 for v in cells.values() if v)
        resultados[k] = {
            "orb": n_orb,
            "nv": n_nv,
            "cells": dict(cells),
            "examples": dict(examples),
        }
    return resultados


def imprimir_tabla(option, resultados):
    print()
    print(f"── Opción {option} ─────────────────────────────────────────")
    hdr = (f"{'k':>3} | {'órbitas':>8} | {'no vacías':>9} | "
           f"{'PP':>3} | {'Pp':>3} | {'pP':>3} | {'Ap':>3}")
    print(hdr); print("-" * len(hdr))
    for k in sorted(resultados):
        r = resultados[k]
        pp   = r["cells"].get("PP", 0)
        puro = r["cells"].get("Pp", 0)
        pal  = r["cells"].get("pP", 0)
        ap   = r["cells"].get("Ap", 0)
        print(f"{k:>3} | {r['orb']:>8} | {r['nv']:>9} | "
              f"{pp:>3} | {puro:>3} | {pal:>3} | {ap:>3}")


# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("=" * 90)
    print("PARTE A — Oscilación con la factorización de k (opción 1, PL)")
    print("=" * 90)

    print("\nGenerando opción 1 (PL) hasta k=11...")
    res_pl = tabla_para_opcion(1, list(range(2, 12)))
    imprimir_tabla(1, res_pl)

    print()
    print("Predicción: Pp no vacía ⇔ k tiene divisor propio d ∈ [3, k/2]")
    print("             (k compuesto, k ≥ 6, k ≠ 4)")
    for k in sorted(res_pl):
        pp_count = res_pl[k]["cells"].get("Pp", 0)
        pred = "no vacía" if pp_count > 0 else "vacía   "
        print(f"  k={k:>2}: Pp {pred}  (real: {pp_count})")

    print()
    print("=" * 90)
    print("PARTE B — Universalidad (opciones 2, 3, 4 para k=2..8)")
    print("=" * 90)

    todos = {1: res_pl}
    for option in [2, 3, 4]:
        # Opción 4 (BBU) tiene alfabeto q=12; k=5 ya son ~20k órbitas.
        # Más allá de k=5 es intratable en Python (se deja para Laminar/Rust).
        ks = list(range(2, 6)) if option == 4 else list(range(2, 9))
        print()
        print(f"### Generando opción {option} (k={ks[0]}..{ks[-1]})...")
        res = tabla_para_opcion(option, ks)
        imprimir_tabla(option, res)
        todos[option] = res

    print()
    print("=" * 90)
    print("PARTE C — Comparación de celdas no vacías entre opciones 1-4")
    print("=" * 90)
    print()
    print("Si el patrón es universal, la columna 'celdas no vacías' debe")
    print("coincidir entre opciones para cada k.")
    print()

    print(f"{'k':>3} | " + " | ".join(f"opción {o}" for o in [1, 2, 3, 4]))
    print("-" * 50)
    for k in range(2, 9):
        parts = []
        for opt in [1, 2, 3, 4]:
            r = todos[opt].get(k)
            if r is None:
                parts.append("—")
            else:
                parts.append(f"{r['nv']:>1} celdas")
        print(f"{k:>3} | " + " | ".join(parts))

    print()
    print("BONUS: ¿BPL (2) y BU (3) tienen la MISMA distribución por celda?")
    print("(predicción: sí, por Proposición 5 del paper)")
    print()
    for k in range(2, 9):
        r2 = todos[2].get(k)
        r3 = todos[3].get(k)
        if r2 is None or r3 is None:
            continue
        same = r2["cells"] == r3["cells"]
        print(f"  k={k:>2}: {'✓ iguales' if same else '✗ distintas'}")
