#!/usr/bin/env python3
"""
Test 9: análisis de escenarios para la convención del sitio distinguible.

Para las opciones 1-8, probamos varias convenciones y verificamos si
son S3-equivariantes:  π(σ·r) = σ·π(r)  para toda fila r y σ ∈ S3.

Las opciones 6 y 8 (1T, sin +0) son las problemáticas.
"""

from itertools import permutations
from sw.common import S3, apply_perm
from caugjam import rows_for_option


def letter_position_plus0(row):
    """El +0 es la letra."""
    for pos, tok in enumerate(row):
        if tok == "+0":
            return pos
    return None


def letter_position_star(row):
    """El *x es la letra. Si no hay *x, None."""
    for pos, tok in enumerate(row):
        if tok.startswith("*"):
            return pos
    return None


def letter_position_first_star_or_plus0(row):
    """Primero busca *x, si no hay, +0."""
    p = letter_position_star(row)
    if p is not None:
        return p
    return letter_position_plus0(row)


def letter_position_rarest(row):
    """El token que no se repite (el más raro)."""
    from collections import Counter
    c = Counter(row)
    rarest = min(c, key=lambda t: (c[t], t))
    return row.index(rarest)


CONVENTIONS = {
    "std (+0)":              letter_position_plus0,
    "star (*x)":              letter_position_star,
    "star_or_plus0":          letter_position_first_star_or_plus0,
    "rarest":                 letter_position_rarest,
}


def permute_token(tok, sigma):
    """Aplica σ a la letra del token (ignora el signo)."""
    if tok == "+0":
        return tok
    if tok[0] in "+-*":
        old = tok[1]
        if old in "ABC":
            new = apply_perm(old, sigma)
            return tok[0] + new
        return tok
    if tok.startswith("("):
        # par buckled: aplicar σ a ambos átomos
        inner = tok[1:-1]  # +k-l
        # naive: split by sign
        return tok  # placeholder
    return tok


def permute_row(row, sigma):
    """Aplica σ a las COLUMNAS (posiciones) de la fila."""
    # sigma es una tupla ('A','B','C') → mapea letra a letra
    mp = dict(zip("ABC", sigma))
    inv = {v: i for i, v in enumerate("ABC")}
    new_row = [None, None, None]
    for i, tok in enumerate(row):
        new_letter = mp["ABC"[i]]
        new_i = inv[new_letter]
        new_row[new_i] = tok
    return tuple(new_row)


def check_equivariance(option, convention):
    """Verifica π(σ·r) = σ·π(r) para todas las filas r y σ ∈ S3."""
    rows = rows_for_option(option)
    fails = []
    for r in rows:
        r = tuple(r)
        p = convention(r)
        if p is None:
            fails.append(("no-letter", r))
            continue
        sigma_p = "ABC"[p]
        for sigma in S3:
            r_perm = permute_row(r, sigma)
            p_after = convention(r_perm)
            if p_after is None:
                fails.append(("no-letter-after", r, sigma, r_perm))
                continue
            sigma_p_str = apply_perm(sigma_p, sigma)
            if "ABC"[p_after] != sigma_p_str:
                fails.append((r, sigma, sigma_p_str, r_perm, "ABC"[p_after]))
    return fails


if __name__ == "__main__":
    print("=" * 100)
    print("TEST 9 — Análisis de escenarios para la convención del sitio")
    print("=" * 100)
    print()
    print("Verificamos  π(σ·r) = σ·π(r)  para toda fila r y σ ∈ S3.")
    print("Una convención es S3-equivariante si pasa para todas las filas.")
    print()

    for option in range(1, 9):
        print(f"\n── Opción {option} ─────────────────────────────")
        for name, conv in CONVENTIONS.items():
            fails = check_equivariance(option, conv)
            if not fails:
                print(f"  {name:>16}: ✓ equivariante")
            else:
                print(f"  {name:>16}: ✗ {len(fails)} fallos")
                for f in fails[:2]:
                    print(f"                   {f}")
