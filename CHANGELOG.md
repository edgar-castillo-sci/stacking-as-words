# Changelog

All notable changes to stacking-as-words are documented here. The
format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `CITATION.cff` (DOI will be added after Zenodo publication).
- `CHANGELOG.md` (this file).

## [0.1.0] - 2026-10-28

Initial release, accompanying the manuscript *Stacking as Words: The
combinatorial structure of JAM chains* (in preparation).

### Added

- `sw/common.py`: shared helpers for word classification and data
  loading: `is_s3_palindromic`, `is_periodic`, `is_strict_palindrome`,
  `is_3fold_screw`, `classify`, `chain_to_word`, `load_canonical`,
  `load_fibration`, `divisors`, `moebius`.
- `experiments/exp03..exp16`: 13 scripts that reproduce the empirical
  claims of the paper (base classification, Ramsdell refinement,
  fibration stability, asymptotic density, map of R definitions,
  site conventions, Venn diagram, closed form for |Pp(k)|,
  qualitative universality, generalized formula, canonical structure,
  random words, forbidden transitions).

### Verified

- Four-cell classification `(PP, Pp, pP, Ap)`, universal qualitatively
  across the 8 options (Test 3 and Test 12).
- Closed form for `|Pp(k)|` in PL via Möbius inversion, confirmed for
  k <= 15 including out-of-range predictions (k=13 -> 0, k=14 -> 169,
  k=15 -> 17).
- `(q/3)^k` generalization for options without buckled pairs
  (options 2, 3, 4, 6, 8), verified for k <= 9.
- Correction of Ramsdell's incomparability claim: `R` is a subset of
  `S3P`, not incomparable (Proposition 1 of the paper).
- Divergence of `kappa` (column-major) and `kappa^word` (row-major)
  from k=6 onward.

### Dependencies

- `caugjam` (installed from GitHub; pinned to v0.1.0).
- `numpy` (transitive, via caugjam).
- `canonjam` (transitive, via caugjam).

### Notes

- This is a pre-publication release. The DOI will be assigned by
  Zenodo after the corresponding manuscript is submitted.
