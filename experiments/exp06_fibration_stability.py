#!/usr/bin/env python3
"""
Test 6: estabilidad de la clasificación bajo la fibración.

Para cada transición n → n+1 (datos/fibracion/fib_nk_nk+1.tsv),
clasifica el padre y el hijo por celda, y construye la matriz de
transición (4x4).

Pregunta: ¿la celda del padre determina la celda del hijo?
  - Si sí: la clasificación es estable bajo la operación de apilar.
  - Si no: hay transiciones, y son interesantes para el paper compañero
    (canonical augmentation).
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


def matriz_transicion(n):
    pairs = cargar_fibracion(n)
    if pairs is None:
        return None
    mat = Counter()
    for parent, child in pairs:
        cp = classify(chain_to_word(parent))
        cc = classify(chain_to_word(child))
        mat[(cp, cc)] += 1
    return mat


def print_matriz(n, mat):
    print(f"\nn → {n + 1}")
    print(" " * 6 + " | " + " | ".join(f"{c:>4}" for c in CELLS) + " | total")
    print("-" * (6 + 4 * 7 + 9))
    for cp in CELLS:
        row = [mat.get((cp, cc), 0) for cc in CELLS]
        total = sum(row)
        if total == 0:
            continue
        print(f"{cp:>6} | " + " | ".join(f"{v:>4}" for v in row) + f" | {total}")


if __name__ == "__main__":
    print("=" * 80)
    print("TEST 6 — Estabilidad de la celda bajo fibración")
    print("=" * 80)
    print()
    print("Cada entrada (fila, col) = número de pares padre→hijo con")
    print("celda(padre) = fila y celda(hijo) = col.")

    for n in range(1, 8):
        mat = matriz_transicion(n)
        if mat is None:
            print(f"\nn → {n + 1}: (sin datos)")
            continue
        print_matriz(n, mat)

    print()
    print("=" * 80)
    print("LECTURA")
    print("=" * 80)
    print("""
- Matriz diagonal dominante ⇒ la celda es (casi) estable bajo fibración.
- Filas con entradas en varias columnas ⇒ la celda del padre no determina
  la del hijo; hay "transiciones" que valen la pena documentar.
- Filas vacías ⇒ la celda no aparece en este nivel.
""")
