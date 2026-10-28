#!/usr/bin/env python3
"""
Test 12: universalidad completa de las 4 celdas en las 8 opciones.

Usa la convención star_or_plus0 (S3-equivariante para las 8 opciones,
según Test 9). Compara celdas no vacías por k entre todas las opciones.
"""

from common import classify, chain_to_word, load_canonical

# k_max por opción, ajustado por el tamaño del alfabeto
OPTIONS = {
    1: 8, 2: 8, 3: 8, 4: 5,   # ya generadas en Test 3
    5: 8, 6: 8, 7: 5, 8: 5,   # nuevas; se generan en este test
}

CELLS = ["PP", "Pp", "pP", "Ap"]


def tabla_opcion(option, k_max):
    rows = []
    for k in range(2, k_max + 1):
        try:
            chains = load_canonical(option, k)
        except Exception as e:
            print(f"  ⚠ opción {option} k={k}: {e}")
            continue
        counts = {c: 0 for c in CELLS}
        for ch in chains:
            w = chain_to_word(ch, convention="star_or_plus0")
            counts[classify(w)] += 1
        rows.append({
            "k": k, "n": len(chains),
            "nv": sum(1 for v in counts.values() if v),
            "cells": dict(counts),
        })
    return rows


if __name__ == "__main__":
    print("=" * 100)
    print("TEST 12 — Universalidad de las 4 celdas en las 8 opciones")
    print("=" * 100)
    print()
    print("Convención: star_or_plus0 (S3-equivariante en las 8 opciones)")
    print()

    tablas = {}
    for option, k_max in OPTIONS.items():
        print(f"### Opción {option} (k=2..{k_max})...")
        tablas[option] = tabla_opcion(option, k_max)
        print(f"  {len(tablas[option])} niveles procesados")

    print()
    print("=" * 100)
    print("CELDAS NO VACÍAS POR OPCIÓN")
    print("=" * 100)
    print()
    print(f"{'k':>3} | " + " | ".join(f"op{o:>1}" for o in OPTIONS))
    print("-" * 60)
    k_global = sorted(set(r["k"] for tab in tablas.values() for r in tab))
    for k in k_global:
        parts = []
        for option in OPTIONS:
            row = next((r for r in tablas[option] if r["k"] == k), None)
            parts.append(str(row["nv"]) if row else "—")
        print(f"{k:>3} | " + " | ".join(f"{p:>3}" for p in parts))

    print()
    print("=" * 100)
    print("TABLAS COMPLETAS POR OPCIÓN")
    print("=" * 100)
    for option, tab in tablas.items():
        print()
        print(f"── Opción {option} ─────────────────────────────────────────")
        print(f"{'k':>3} | {'órb':>6} | {'celdas':>6} | "
              f"{'PP':>4} | {'Pp':>4} | {'pP':>4} | {'Ap':>5}")
        print("-" * 60)
        for r in tab:
            print(f"{r['k']:>3} | {r['n']:>6} | {r['nv']:>6} | "
                  f"{r['cells']['PP']:>4} | {r['cells']['Pp']:>4} | "
                  f"{r['cells']['pP']:>4} | {r['cells']['Ap']:>5}")

    print()
    print("=" * 100)
    print("LECTURA")
    print("=" * 100)
    print("""
- Si todas las columnas tienen el mismo 'celdas' para cada k,
  la universalidad queda confirmada en las 8 opciones.
- Si alguna difiere, investigar por qué (puede ser la convención o
  el alfabeto de la opción).
""")
