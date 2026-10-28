#!/usr/bin/env python3
"""
Test 7: densidad asintótica por celda.

Para cada k, reporta la fracción de órbitas en cada celda.
Predicción: la fracción de 'Ap' (aperiódica) tiende a 1 con k.
"""

from common import classify, chain_to_word, load_canonical

CELLS = ["PP", "Pp", "pP", "Ap"]


if __name__ == "__main__":
    print("=" * 100)
    print("TEST 7 — Densidad asintótica por celda (opción 1)")
    print("=" * 100)
    print()
    print(f"{'k':>3} | {'órb':>6} | " + " | ".join(f"{c:>6}" for c in CELLS) + " | Ap/%")
    print("-" * 100)

    for k in range(2, 12):
        try:
            chains = load_canonical(1, k)
        except FileNotFoundError:
            continue
        cells = {c: 0 for c in CELLS}
        for ch in chains:
            cells[classify(chain_to_word(ch))] += 1
        n = len(chains)
        fracs = {c: cells[c] / n for c in CELLS}
        ap_pct = 100 * fracs["Ap"]
        print(f"{k:>3} | {n:>6} | " +
              " | ".join(f"{fracs[c]:>6.3f}" for c in CELLS) +
              f" | {ap_pct:>6.2f}")

    print()
    print("Predicción: Ap → 1 exponencialmente con k.")
    print("El patrón es informativo como resumen grueso solo para k pequeño/intermedio.")
