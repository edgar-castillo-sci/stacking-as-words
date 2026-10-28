#!/usr/bin/env python3
"""Shared helpers for the stacking-as-words experiments."""

import os
from itertools import permutations

S3 = list(permutations("ABC"))
THREE_CYCLES = [("B", "C", "A"), ("C", "A", "B")]


def apply_perm(w, perm):
    """perm is a 3-tuple (image of A, image of B, image of C)."""
    mp = dict(zip("ABC", perm))
    return "".join(mp[c] for c in w)


def is_s3_palindromic(w):
    """Exists sigma in S3 such that sigma(w) = reverse(w)."""
    rw = w[::-1]
    return any(apply_perm(w, p) == rw for p in S3)


def is_periodic(w):
    """Exists u and n >= 2 with w = u^n."""
    n = len(w)
    for d in range(1, n):
        if n % d == 0 and w[:d] * (n // d) == w:
            return True
    return False


def is_strict_palindrome(w):
    """Ramsdell's H: w == reverse(w)."""
    return w == w[::-1]


def is_3fold_screw(w):
    """
    Ramsdell's R (combinatorial version):
    exists sigma a 3-cycle and m in {1, 2} such that sigma(w) = rot^m(w).
    """
    for m in (1, 2):
        rotated = w[m:] + w[:m]
        for sigma in THREE_CYCLES:
            if apply_perm(w, sigma) == rotated:
                return True
    return False


def classify(w):
    """Return PP, Pp, pP, or Ap."""
    p, q = is_s3_palindromic(w), is_periodic(w)
    if p and q:
        return "PP"
    if q:
        return "Pp"
    if p:
        return "pP"
    return "Ap"


# -- chain_to_word ------------------------------------------------------
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
    Project a canonical chain to its ABC word.

    convention:
      "plus0"         -> +0 (options 1-5, 7; fails on 6, 8)
      "star_or_plus0" -> *x if present, otherwise +0 (all options 1-8)
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
                f"row without distinguishable site: {row} in {chain} "
                f"(convention={convention})"
            )
        word.append(letter)
    return "".join(word)


# -- data loading -------------------------------------------------------
_poda_cache = {}
_data_sources = {}
_fib_sources = {}


def _data_roots():
    """Ordered list of candidate data roots."""
    here = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(here)
    roots = []
    env_dir = os.environ.get("SW_DATA_DIR")
    if env_dir:
        roots.append(env_dir)
    roots.append(os.path.join(repo_root, "data"))
    return roots


def load_canonical(option, k, return_source=False):
    """
    Load canonical chains for the given option and level k.

    Lookup order:
      1. $SW_DATA_DIR/n{k}/canonicas.txt                  (option == 1)
         $SW_DATA_DIR/opt{option}/n{k}/canonicas.txt      (option >= 2)
      2. ./data/n{k}/canonicas.txt                        (option == 1)
         ./data/opt{option}/n{k}/canonicas.txt            (option >= 2)
      3. regenerate with caugjam.generate_poda and cache in ./data/ (gitignored)

    If return_source=True, returns (chains, source) where source is one
    of "env", "cache", or "generated".
    """
    roots = _data_roots()
    env_dir = os.environ.get("SW_DATA_DIR")
    if option == 1:
        rel = os.path.join("n" + str(k), "canonicas.txt")
    else:
        rel = os.path.join("opt" + str(option), "n" + str(k), "canonicas.txt")

    for root in roots:
        path = os.path.join(root, rel)
        if os.path.exists(path):
            with open(path) as f:
                chains = [line.strip() for line in f if line.strip()]
            source = (
                "env"
                if env_dir and os.path.abspath(root) == os.path.abspath(env_dir)
                else "cache"
            )
            _data_sources[(option, k)] = source
            return (chains, source) if return_source else chains

    if option not in _poda_cache or max(_poda_cache[option]) < k:
        from caugjam import generate_poda
        print(f"  (generating pruning data, option {option} up to k={k}...)")
        _poda_cache[option] = generate_poda(k, option)

    chains = _poda_cache[option][k]
    path = os.path.join(roots[-1], rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        for ch in chains:
            f.write(ch + "\n")
    _data_sources[(option, k)] = "generated"
    return (chains, "generated") if return_source else chains



def load_fibration(option, k, return_source=False):
    """
    Load the (parent, child) pairs for the fibration k -> k+1.

    Lookup order:
      1. $SW_DATA_DIR/fibration/opt{option}/fib_n{k}_n{k+1}.tsv
      2. $SW_DATA_DIR/fibration/fib_n{k}_n{k+1}.tsv
      3. ./data/fibration/opt{option}/fib_n{k}_n{k+1}.tsv
      4. ./data/fibration/fib_n{k}_n{k+1}.tsv
      5. None if not found (source "missing").

    Fibration data is generated by caugJAM's scripts/fibration.py. To run
    the experiments that need it without running caugJAM, either copy
    the .tsv files under data/fibration/ here, or set $SW_DATA_DIR to a
    directory that contains both canonicas.txt and fibration/.

    If return_source=True, returns (pairs, source) where source is one
    of "env", "cache", or "missing".
    """
    fname = f"fib_n{k}_n{k + 1}.tsv"
    env_dir = os.environ.get("SW_DATA_DIR")
    candidates = []
    for root in _data_roots():
        candidates.append((os.path.join(root, "fibration", f"opt{option}", fname), root))
        candidates.append((os.path.join(root, "fibration", fname), root))

    for path, root in candidates:
        if os.path.exists(path):
            pairs = []
            with open(path) as f:
                next(f, None)  # skip header
                for line in f:
                    parts = line.rstrip("\n").split("\t")
                    if len(parts) >= 2:
                        pairs.append((parts[0], parts[1]))
            source = (
                "env"
                if env_dir and os.path.abspath(root) == os.path.abspath(env_dir)
                else "cache"
            )
            _fib_sources[(option, k)] = source
            return (pairs, source) if return_source else pairs

    _fib_sources[(option, k)] = "missing"
    return (None, "missing") if return_source else None



def divisors(n):
    """Positive divisors of n, in increasing order."""
    return [d for d in range(1, n + 1) if n % d == 0]


def moebius(n):
    """Moebius function mu(n)."""
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
