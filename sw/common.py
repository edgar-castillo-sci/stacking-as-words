#!/usr/bin/env python3
"""Utilidades compartidas para los tests de post_canonJAM."""

import os
from itertools import permutations

S3 = list(permutations("ABC"))
THREE_CYCLES = [("B", "C", "A"), ("C", "A", "B")]


def apply_perm(w, perm):
    """perm es una tupla (img de A, img de B, img de C)."""
    mp = dict(zip("ABC", perm))
    return "".join(mp[c] for c in w)


def is_s3_palindromic(w):
    """∃ σ ∈ S3 tal que σ(w) = reverse(w)."""
    rw = w[::-1]
    return any(apply_perm(w, p) == rw for p in S3)


def is_periodic(w):
    """∃ u, n≥2 con w = u^n."""
    n = len(w)
    for d in range(1, n):
        if n % d == 0 and w[:d] * (n // d) == w:
            return True
    return False


def is_strict_palindrome(w):
    """H de Ramsdell: w == reverse(w)."""
    return w == w[::-1]


def is_3fold_screw(w):
    """
    R de Ramsdell (versión combinatoria):
    ∃ σ 3-ciclo y ∃ m ∈ {1,2} tal que σ(w) = rot^m(w).
    """
    for m in (1, 2):
        rotated = w[m:] + w[:m]
        for sigma in THREE_CYCLES:
            if apply_perm(w, sigma) == rotated:
                return True
    return False


def classify(w):
    """Devuelve PP, Pp, pP o Ap."""
    p, q = is_s3_palindromic(w), is_periodic(w)
    if p and q:
        return "PP"
    if q:
        return "Pp"
    if p:
        return "pP"
    return "Ap"


# ── chain_to_word ────────────────────────────────────────────────────────
def _split_chain(chain):
    blocks = chain.split("/")
    cols = []
    for blk in blocks:
        toks, i = [], 0
        while i < len(blk):
            if blk[i] == "(":
                toks.append(blk[i:i + 6])
                i += 6
            else:
                toks.append(blk[i:i + 2])
                i += 2
        cols.append(toks)
    return cols


def chain_to_word(chain, convention="star_or_plus0"):
    """
    Proyecta una cadena canónica a su palabra ABC.

    convention:
      "plus0"         → +0 (opciones 1-5, 7; falla en 6, 8)
      "star_or_plus0" → *x si existe, si no +0 (opciones 1-8)
    """
    cols = _split_chain(chain)
    k = len(cols[0])
    word = []
    for i in range(k):
        row = [cols[c][i] for c in range(3)]
        letter = None
        for pos, tok in enumerate(row):
            if convention == "plus0" and tok == "+0":
                letter = "ABC"[pos]
                break
            elif convention == "star_or_plus0" and (
                tok.startswith("*") or tok == "+0"
            ):
                letter = "ABC"[pos]
                break
        if letter is None:
            raise ValueError(
                f"fila sin sitio distinguible: {row} en {chain} "
                f"(convention={convention})"
            )
        word.append(letter)
    return "".join(word)


# ── load_canonical con caché ────────────────────────────────────────────
_poda_cache = {}


def load_canonical(option, k):
    """
    Load canonical chains for the given option and level k.

    Lookup order:
      1. $SW_DATA_DIR/n{k}/canonicas.txt          (option == 1)
         $SW_DATA_DIR/opt{option}/n{k}/canonicas.txt  (option >= 2)
      2. ./data/n{k}/canonicas.txt                (same layout, repo-local)
      3. regenerate with caugjam.generate_poda and cache in ./data/ (gitignored)
    """
    here = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(here)

    env_dir = os.environ.get("SW_DATA_DIR")
    roots = []
    if env_dir:
        roots.append(env_dir)
    roots.append(os.path.join(repo_root, "data"))

    if option == 1:
        rel = os.path.join("n" + str(k), "canonicas.txt")
    else:
        rel = os.path.join("opt" + str(option), "n" + str(k), "canonicas.txt")

    for root in roots:
        path = os.path.join(root, rel)
        if os.path.exists(path):
            with open(path) as f:
                return [line.strip() for line in f if line.strip()]

    if option not in _poda_cache or max(_poda_cache[option]) < k:
        from caugjam import generate_poda
        print(f"  (generating pruning data, option {option} up to k={k}...)")
        _poda_cache[option] = generate_poda(k, option)

    chains = _poda_cache[option][k]
    path = os.path.join(roots[0], rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        for ch in chains:
            f.write(ch + "\n")
    return chains


def divisors(n):
    """Divisores positivos de n, en orden creciente."""
    return [d for d in range(1, n + 1) if n % d == 0]


def moebius(n):
    """Función de Möbius μ(n)."""
    if n == 1:
        return 1
    p, m, k = 2, n, 0
    while p * p <= m:
        if m % p == 0:
            m //= p
            if m % p == 0:
                return 0
            k += 1
        p += 1
    if m > 1:
        k += 1
    return (-1) ** k
