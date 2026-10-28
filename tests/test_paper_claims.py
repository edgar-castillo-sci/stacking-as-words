"""
Fast checks of the five main empirical claims of the paper.

These tests run in a few seconds on a laptop and in CI. They do NOT
exhaustively verify every level mentioned in the paper; they check the
ranges that are cheap to reproduce:

  Claim 1 - four-cell classification is qualitatively universal.
  Claim 2 - closed form for |Pp(k)| in PL via Moebius inversion.
  Claim 3 - (q/3)^k generalization for options without buckled pairs.
  Claim 4 - kappa (column-major) diverges from kappa^word (row-major)
            from k=6 onward.
  Claim 5 - cell Pp is empty for prime k.

For the full experiments (k up to 15, all 8 options, transitions,
etc.), run the scripts in `experiments/`.
"""

from sw.common import (
    S3, apply_perm, classify, chain_to_word, divisors, is_periodic,
    is_s3_palindromic, load_canonical, moebius,
)

CELLS = ["PP", "Pp", "pP", "Ap"]


def _cell_counts(option, k):
    counts = {c: 0 for c in CELLS}
    for ch in load_canonical(option, k):
        counts[classify(chain_to_word(ch, convention="star_or_plus0"))] += 1
    return counts


def _nonempty_cells(option, k):
    return {c for c, v in _cell_counts(option, k).items() if v > 0}


# -- Claim 1: four-cell classification is qualitatively universal ---------
def test_claim1_universality():
    """Nonempty cells at k=2,3,4 are the same for all 8 options."""
    for k in (2, 3, 4):
        ref = _nonempty_cells(1, k)
        for option in range(2, 9):
            got = _nonempty_cells(option, k)
            assert got == ref, (
                f"k={k}, option {option}: nonempty cells {got} != {ref}"
            )


# -- Claim 2: closed form for |Pp(k)| in PL ------------------------------
def test_claim2_closed_form_pl():
    """|Pp(k)|_PL = sum_{d | k, 3 <= d < k} N'(d), verified k=2..8."""
    K_MAX = 8
    A = {}
    for d in range(2, K_MAX + 1):
        c = _cell_counts(1, d)
        A[d] = c["Pp"] + c["Ap"]
    N = {d: sum(moebius(d // e) * A[e] for e in divisors(d) if e >= 2)
         for d in range(2, K_MAX + 1)}
    for k in range(2, K_MAX + 1):
        pred = sum(N[d] for d in divisors(k) if 3 <= d < k and d >= 2)
        real = _cell_counts(1, k)["Pp"]
        assert pred == real, f"k={k}: formula predicts {pred}, actual {real}"


# -- Claim 3: (q/3)^k generalization -------------------------------------
def test_claim3_generalization():
    """|Pp(k)|_op = |Pp(k)|_PL * (q/3)^k for options without buckled pairs."""
    # Option -> (q, k_max). Options 5 and 7 are excluded (buckled pairs).
    specs = {2: (6, 6), 3: (6, 6), 4: (12, 4), 6: (6, 6), 8: (12, 4)}
    for option, (q, k_max) in specs.items():
        for k in range(2, k_max + 1):
            pl = _cell_counts(1, k)["Pp"]
            real = _cell_counts(option, k)["Pp"]
            expected = pl * (q // 3) ** k
            assert real == expected, (
                f"option {option}, k={k}: (q/3)^k predicts {expected}, "
                f"actual {real}"
            )


# -- Claim 4: kappa diverges from kappa^word from k=6 --------------------
def _orbit_words(w):
    """G-orbit of a word: S3 images and their reversals."""
    orbit = set()
    for p in S3:
        wp = apply_perm(w, p)
        orbit.add(wp)
        orbit.add(wp[::-1])
    return orbit


def test_claim4_kappa_vs_kappa_word():
    """There exists a canonical chain whose word is NOT the row-major min
    of its G-orbit, at k=6 (PL). Before k=6 the two coincide."""
    for k in range(2, 6):
        for ch in load_canonical(1, k):
            w = chain_to_word(ch, convention="star_or_plus0")
            assert w == min(_orbit_words(w)), (
                f"k={k}: kappa should agree with kappa^word before k=6"
            )
    # k=6: at least one divergence
    diverged = 0
    for ch in load_canonical(1, 6):
        w = chain_to_word(ch, convention="star_or_plus0")
        if w != min(_orbit_words(w)):
            diverged += 1
    assert diverged > 0, "k=6: expected at least one divergence"


# -- Claim 5: Pp is empty for prime k ------------------------------------
def test_claim5_pp_empty_for_prime_k():
    """Pp(k) is empty iff k is prime (k >= 3), or k=4, or k=5."""
    for k in (3, 4, 5, 7, 11):
        assert _cell_counts(1, k)["Pp"] == 0, (
            f"k={k}: Pp should be empty"
        )
    for k in (6, 8, 9, 10):
        assert _cell_counts(1, k)["Pp"] > 0, (
            f"k={k}: Pp should be nonempty"
        )
