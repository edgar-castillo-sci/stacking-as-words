#!/usr/bin/env python3
"""
Test 8: mapa de definiciones de R.

El paper dice que S3P es "incomparable con R". Test 5 mostró que bajo
la definición estándar (3-ciclo + rotación), R ⊆ S3P para k ≤ 8.

Este test explora varias definiciones plausibles de R y ve cuáles
tienen R \ S3P ≠ ∅ (i.e., cuáles salvan la incomparabilidad).
"""

from itertools import product
from sw.common import S3, apply_perm, is_s3_palindromic


def all_words(k):
    for tup in product("ABC", repeat=k):
        yield "".join(tup)


def rot(w, m):
    return w if m == 0 else w[m % len(w):] + w[:m % len(w)]


def rev(w):
    return w[::-1]


THREE_CYCLES = [("B", "C", "A"), ("C", "A", "B")]


def R_standard(w):
    """3-ciclo + rotación (definición del Test 5)."""
    k = len(w)
    for s in THREE_CYCLES:
        for m in range(k):
            if apply_perm(w, s) == rot(w, m):
                return True
    return False


def R_nontrivial(w):
    """Como R_standard pero excluyendo m=0."""
    k = len(w)
    for s in THREE_CYCLES:
        for m in range(1, k):
            if apply_perm(w, s) == rot(w, m):
                return True
    return False


def R_mirror(w):
    """3-ciclo + rotación + espejo: σ(w) = reverse(rot^m(w))."""
    k = len(w)
    for s in THREE_CYCLES:
        for m in range(k):
            if apply_perm(w, s) == rev(rot(w, m)):
                return True
    return False


def R_any_sigma(w):
    """Cualquier σ ∈ S3 + rotación (no solo 3-ciclos)."""
    k = len(w)
    for s in S3:
        for m in range(k):
            if apply_perm(w, s) == rot(w, m):
                return True
    return False


def R_period_power3(w):
    """Período d con k/d una potencia de 3 > 1."""
    k = len(w)
    for d in range(1, k):
        if k % d != 0:
            continue
        m = k // d
        if m < 2:
            continue
        mm = m
        while mm % 3 == 0:
            mm //= 3
        if mm == 1:
            if w == w[:d] * m:
                return True
    return False


DEFS = {
    "R_standard":      R_standard,
    "R_nontrivial":    R_nontrivial,
    "R_mirror":        R_mirror,
    "R_any_sigma":     R_any_sigma,
    "R_period_pow3":   R_period_power3,
}


if __name__ == "__main__":
    print("=" * 100)
    print("TEST 8 — Mapa de definiciones de R")
    print("=" * 100)
    print()

    for k in range(2, 9):
        words = list(all_words(k))
        s3p = {w for w in words if is_s3_palindromic(w)}
        print(f"\n── k = {k}  (|words| = {len(words)}, |S3P| = {len(s3p)}) ──")
        print(f"{'definición':>18} | {'|R|':>5} | {'|R∩S3P|':>8} | "
              f"{'|R\\S3P|':>8} | {'|S3P\\R|':>8}")
        print("-" * 70)
        for name, f in DEFS.items():
            r = {w for w in words if f(w)}
            inter = r & s3p
            r_only = r - s3p
            s_only = s3p - r
            flag = "◀" if r_only else " "
            print(f"{name:>18} | {len(r):>5} | {len(inter):>8} | "
                  f"{len(r_only):>8} {flag} | {len(s_only):>8}")

    print()
    print("=" * 100)
    print("LECTURA")
    print("=" * 100)
    print("""
- '|R\\S3P| > 0' (marcado con ◀) ⇒ R ⊄ S3P, hay incomparabilidad.
- Si NINGUNA definición da R\\S3P > 0, el paper debe cambiar
  "incomparable con R" por "más débil que R".
- Si alguna (probablemente R_mirror o R_any_sigma) da R\\S3P > 0,
  esa es la definición "correcta" para preguntarle a Jessica.
""")
