#!/usr/bin/env python3
"""
Test 3 extended:
  (A) k = 2..11 for option 1 (PL) - oscillation with the factorization of k.
  (B) k = 2..8 for options 2, 3, 4 - universality of the pattern.
  (C) comparison of nonempty cells across options.

Uses generate_poda (canonical augmentation) to generate canonical
representatives without enumerating all raw candidates, which is
prohibitive for k >= 7.
"""

from collections import Counter, defaultdict
from time import perf_counter

from caugjam import generate_poda
from sw.common import chain_to_word, is_periodic, is_s3_palindromic


def classify(w):
    p, q = is_s3_palindromic(w), is_periodic(w)
    if p and q: return "PP"
    if q:       return "Pp"
    if p:       return "pP"
    return              "Ap"


def table_for_option(option, ks, verbose=True):
    n_max = max(ks)
    t0 = perf_counter()
    classes = generate_poda(n_max, option)
    t_gen = perf_counter() - t0

    if verbose:
        print(f"  [option {option}] generation up to k={n_max} in {t_gen:.2f}s")
        print(f"  [option {option}] orbits per k: " +
              ", ".join(f"k={k}:{len(classes[k])}" for k in ks if k in classes))

    results = {}
    for k in ks:
        if k not in classes:
            continue
        cells = Counter()
        examples = defaultdict(list)
        for ch in classes[k]:
            w = chain_to_word(ch, convention="plus0")
            c = classify(w)
            cells[c] += 1
            if len(examples[c]) < 3:
                examples[c].append(w)
        n_orb = len(classes[k])
        n_nv = sum(1 for v in cells.values() if v)
        results[k] = {
            "orb": n_orb,
            "nv": n_nv,
            "cells": dict(cells),
            "examples": dict(examples),
        }
    return results


def print_table(option, results):
    print()
    print(f"-- Option {option} -----------------------------------------")
    hdr = (f"{'k':>3} | {'orbits':>8} | {'nonempty':>9} | "
           f"{'PP':>3} | {'Pp':>3} | {'pP':>3} | {'Ap':>3}")
    print(hdr); print("-" * len(hdr))
    for k in sorted(results):
        r = results[k]
        pp   = r["cells"].get("PP", 0)
        pure = r["cells"].get("Pp", 0)
        pal  = r["cells"].get("pP", 0)
        ap   = r["cells"].get("Ap", 0)
        print(f"{k:>3} | {r['orb']:>8} | {r['nv']:>9} | "
              f"{pp:>3} | {pure:>3} | {pal:>3} | {ap:>3}")


if __name__ == "__main__":

    print("=" * 90)
    print("PART A - Oscillation with the factorization of k (option 1, PL)")
    print("=" * 90)

    print("\nGenerating option 1 (PL) up to k=11...")
    res_pl = table_for_option(1, list(range(2, 12)))
    print_table(1, res_pl)

    print()
    print("Prediction: Pp nonempty iff k has a proper divisor d in [3, k/2]")
    print("            (k composite, k >= 6, k != 4)")
    for k in sorted(res_pl):
        pp_count = res_pl[k]["cells"].get("Pp", 0)
        pred = "nonempty" if pp_count > 0 else "empty   "
        print(f"  k={k:>2}: Pp {pred}  (actual: {pp_count})")

    print()
    print("=" * 90)
    print("PART B - Universality (options 2, 3, 4 for k=2..8)")
    print("=" * 90)

    all_results = {1: res_pl}
    for option in [2, 3, 4]:
        # Option 4 (BBU) has alphabet size q=12; k=5 is already ~20k orbits.
        # Beyond k=5 it is intractable in Python (leave for Laminar/Rust).
        ks = list(range(2, 6)) if option == 4 else list(range(2, 9))
        print()
        print(f"### Generating option {option} (k={ks[0]}..{ks[-1]})...")
        res = table_for_option(option, ks)
        print_table(option, res)
        all_results[option] = res

    print()
    print("=" * 90)
    print("PART C - Comparison of nonempty cells across options 1-4")
    print("=" * 90)
    print()
    print("If the pattern is universal, the 'nonempty cells' column must")
    print("match across options for each k.")
    print()

    print(f"{'k':>3} | " + " | ".join(f"option {o}" for o in [1, 2, 3, 4]))
    print("-" * 50)
    for k in range(2, 9):
        parts = []
        for opt in [1, 2, 3, 4]:
            r = all_results[opt].get(k)
            if r is None:
                parts.append("--")
            else:
                parts.append(f"{r['nv']:>1} cells")
        print(f"{k:>3} | " + " | ".join(parts))

    print()
    print("BONUS: do BPL (2) and BU (3) have the SAME distribution per cell?")
    print("(prediction: yes, by Proposition 5 of the paper)")
    print()
    for k in range(2, 9):
        r2 = all_results[2].get(k)
        r3 = all_results[3].get(k)
        if r2 is None or r3 is None:
            continue
        same = r2["cells"] == r3["cells"]
        print(f"  k={k:>2}: {'equal' if same else 'different'}")
