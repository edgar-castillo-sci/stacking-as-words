#!/usr/bin/env python3
"""
Test 16: estructura de las transiciones de celdas en el fibrado.

Profundiza en Test 6:
  - ¿Qué transiciones (padre → hijo) son imposibles (matriz con ceros)?
  - ¿La matriz se estabiliza para k grande?
  - Distribución condicional P(hijo | padre).
  - ¿Hay filas/columnas vacías?

Datos: datos/fibracion/fib_nk_nk+1.tsv.
"""

import csv
import os
from collections import Counter

from sw.common import chain_to_word, classify

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIB = os.path.join(ROOT, "datos", "fibracion")
CELLS = ["PP", "Pp", "pP", "Ap"]


def cargar_fibracion(n):
    path = os.path.join(FIB, f"fib_n{n}_n{n + 1}.tsv")
    if not os.path.exists(path):
        return None
    pairs = []
    with open(path) as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader)
        for row in reader:
            if len(row) == 2:
                pairs.append((row[0], row[1]))
    return pairs


def matriz(n):
    pairs = cargar_fibracion(n)
    if pairs is None:
        return None
    mat = Counter()
    for parent, child in pairs:
        cp = classify(chain_to_word(parent, convention="star_or_plus0"))
        cc = classify(chain_to_word(child, convention="star_or_plus0"))
        mat[(cp, cc)] += 1
    return mat


if __name__ == "__main__":
    print("=" * 100)
    print("TEST 16 — Transiciones prohibidas y estructura del fibrado")
    print("=" * 100)
    print()

    matrices = {}
    for n in range(1, 8):
        mat = matriz(n)
        if mat is not None:
            matrices[n] = mat

    # ── 1. ¿Qué celdas aparecen como padre o hijo? ──────────────────
    print("Celdas presentes como PADRE / HIJO por n:")
    print(f"{'n→n+1':>8} | {'padres':>40} | {'hijos':>40}")
    print("-" * 100)
    for n, mat in matrices.items():
        padres = sorted({cp for (cp, cc) in mat})
        hijos = sorted({cc for (cp, cc) in mat})
        print(f"{n}→{n+1:<3} | {', '.join(padres):>40} | "
              f"{', '.join(hijos):>40}")

   # ── 2. Transiciones prohibidas (ceros estructurales) ────────────
        print()
        print("Transiciones (padre → hijo) que NUNCA ocurren en n ≤ 7:")
        seen = {frozenset(m.items()) for m in matrices.values()}
        print(f"  matrices únicas para n=2..7: {len(seen)} de {len(matrices)}")
        all_pairs = {(cp, cc) for cp in CELLS for cc in CELLS}
        forbidden = all_pairs - {p for mat in matrices.values() for p in mat}
        for cp, cc in sorted(forbidden):
            print(f"  {cp} → {cc}")

    # ── 3. Distribución condicional P(hijo | padre) ─────────────────
    print()
    print("Distribución condicional P(hijo | padre), agregada sobre n ≤ 7:")
    agg = Counter()
    for mat in matrices.values():
        agg.update(mat)
    row_totals = Counter()
    for (cp, cc), v in agg.items():
        row_totals[cp] += v

    print(f"{'padre':>6} | " + " | ".join(f"{c:>6}" for c in CELLS) + " | total")
    print("-" * 60)
    for cp in CELLS:
        if row_totals[cp] == 0:
            continue
        row = []
        for cc in CELLS:
            v = agg.get((cp, cc), 0)
            row.append(f"{v / row_totals[cp]:>6.3f}")
        print(f"{cp:>6} | " + " | ".join(row) + f" | {row_totals[cp]:>5}")

    # ── 4. Matrices normalizadas para n y n+1: ¿estabiliza? ─────────
    print()
    print("Comparación P(hijo | padre) entre n y n+1 consecutivos:")
    for n in range(2, 7):
        if n not in matrices or n + 1 not in matrices:
            continue
        def cond(mat):
            tot = Counter()
            for (cp, cc), v in mat.items():
                tot[cp] += v
            out = {}
            for cp in CELLS:
                if tot[cp] == 0:
                    out[cp] = {cc: None for cc in CELLS}
                else:
                    out[cp] = {cc: mat.get((cp, cc), 0) / tot[cp]
                               for cc in CELLS}
            return out
        c1, c2 = cond(matrices[n]), cond(matrices[n + 1])
        same_count = sum(
            1 for cp in CELLS for cc in CELLS
            if c1[cp][cc] is not None and c2[cp][cc] is not None
            and abs(c1[cp][cc] - c2[cp][cc]) < 0.05
        )
        total_count = sum(
            1 for cp in CELLS for cc in CELLS
            if c1[cp][cc] is not None and c2[cp][cc] is not None
        )
        print(f"  n={n} vs n={n+1}: {same_count}/{total_count} entradas"
              f" dentro de ±0.05")

    print()
    print("=" * 100)
    print("LECTURA")
    print("=" * 100)
    print("""
- Las transiciones prohibidas son "ceros estructurales": sugieren
  restricciones del fibrado que valen la pena documentar.
- La distribución condicional muestra qué celdas son "estables" bajo
  apilar y cuáles son "transitorias".
- Si la matriz se estabiliza para n grande, hay una estructura
  asintótica interesante para el paper compañero (augmentation).
""")
