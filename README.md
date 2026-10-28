# stacking-as-words

*[Leer en español](README.es.md)*

Combinatorial structure of stacking configurations in honeycomb layered
materials, represented as JAM chains and projected onto words over a
three-letter alphabet `{A, B, C}`.

## Author

Edgar Castillo (Independent Researcher)

## Scientific basis

Builds on:

> Arcudia, J., Ortiz-Chi, F., Sanchez-Valenzuela, A., Aspuru-Guzik, A.,
> Merino, G. (2023). "Joining and arrangement of multilayers: A string
> representation for honeycomb layered materials." Matter, 6(5),
> 1503–1513. doi: 10.1016/j.matt.2023.02.014

and on the canonicalization (canonJAM) and canonical augmentation
(caugJAM) papers in preparation. The results here are the empirical
material for the manuscript *Stacking as Words: The combinatorial
structure of JAM chains* (in preparation).

## What it does

Each JAM chain projects to a word over `{A, B, C}`, where each letter
records the Wyckoff site of a distinguished token in the corresponding
layer. Two Boolean properties of the word — being **S3-palindromic**
and being **periodic** — partition the orbit space into four cells:

| Cell | S3-palindromic? | Periodic? |
|---|---|---|
| `PP` | yes | yes |
| `Pp` | no  | yes |
| `pP` | yes | no  |
| `Ap` | no  | no  |

The main results:

1. **Qualitative universality.** Which cells are nonempty depends only
   on the level `k`, not on the option (1–8). Verified empirically.
2. **Closed form for `|Pp(k)|` in PL.** Via Möbius inversion,
   `|Pp(k)| = Σ_{d|k, 3≤d<k} N'(d)`, confirmed for `k ≤ 15` including
   out-of-range predictions (`k=13 → 0`, `k=14 → 169`, `k=15 → 17`).
3. **`(q/3)^k` generalization.** For options without buckled pairs
   (2, 3, 4, 6, 8), `|Pp(k)|_op = |Pp(k)|_PL · (q/3)^k`. Verified
   empirically. Options 5 and 7 (with buckled pairs) break the pattern;
   the structural obstruction is identified.
4. **Correction to Ramsdell.** `R ⊆ S3P`, not "incomparable with R".
5. **`κ` vs `κ^word`.** The canonical representative `κ(a)` (column-major)
   and the canonical form of its word `κ^word(π(a))` (row-major) diverge
   from `k=6` onward — a structural caveat for downstream use.

## Contents

- `sw/` — shared helpers (`is_s3_palindromic`, `is_periodic`,
  `classify`, `chain_to_word`, `load_canonical`, `load_fibration`).
- `experiments/` — 13 standalone scripts, each reproducing one of the
  results above. Not pytest tests: run them with `python3`.
- `tests/` — fast pytest checks of the five main claims (used by CI).
- `outputs/` — captured output of the experiments, as evidence.
- `docs/research_notes.md` — the full exploratory notes (long form).

## Installation

Requires `caugjam` v0.1.0 or later:

```bash
pip install "caugjam @ git+https://github.com/edgar-castillo-sci/caugJAM.git@v0.1.0"
pip install -e ".[tests]"
```

## Quick run

```bash
# The fast CI suite (~5 seconds)
pytest -v

# The full experiments (minutes)
python3 experiments/exp13_generalized_formula.py
python3 experiments/exp14_canonical_structure.py
```

## Data

Large regenerable outputs (`data/**/canonicas.txt`, fibration `.tsv`)
are **not versioned**. They are regenerated on demand with
`caugjam.generate_poda`, or provided via the `$SW_DATA_DIR` environment
variable. Captured experiment outputs (`outputs/*.txt`) are versioned
as evidence.

## Citation

```bibtex
@software{stacking_as_words,
  author       = {Castillo, Edgar},
  title        = {{stacking-as-words: Combinatorial structure of JAM chains}},
  year         = {2026},
  publisher    = {Zenodo},
  howpublished = {\url{https://github.com/edgar-castillo-sci/stacking-as-words}},
  note         = {DOI to be assigned}
}
```

## License

MIT (see `LICENSE`).
