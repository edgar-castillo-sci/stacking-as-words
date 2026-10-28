# Roadmap

Status document for the `stacking-as-words` repository. Tracks what is
done, what is in progress, and what is planned, with a rationale for
each item and a clear definition of "done".

*Last updated: 2026-10-28*

## At a glance

| Phase | Status | Purpose |
|---|---|---|
| **Foundation** | done | Repository skeleton (code, tests, CI, docs) |
| **Rigor** | done | Reproducibility without caugJAM (v0.1.0, commit 1774cdf) |
| **Runtime visibility** | next | Show the caugJAM dependency at runtime |
| **Release v0.1.0** | planned | Tag, GitHub Release, Zenodo DOI |
| **Cross-links** | optional | Discoverability across the three JAM repositories |

Blocking items (require resolution before submitting the paper) are
marked with `[B]`. Non-blocking items are `[R]` (recommended) or `[O]`
(optional).

## What we have

### Code

- `sw/common.py` — shared helpers (`is_s3_palindromic`, `is_periodic`,
  `classify`, `chain_to_word`, `load_canonical`, `load_fibration`,
  `divisors`, `moebius`).
- `sw/provenance.py` — dependency report and data-source tracking.
- `sw/__init__.py` — public API for the helpers.
- `experiments/exp03..exp16` — 13 standalone scripts, all in English,
  each reproducing one result of the paper.
- `tests/test_paper_claims.py` — 5 fast pytest checks (one per main
  claim), ~15 s total.

### Infrastructure

- `.github/workflows/tests.yml` — CI on Python 3.10–3.14,
  `fail-fast: false`.
- `.pre-commit-config.yaml` — validates `requires-python` in
  `pyproject.toml` (the same hook used in `canonJAM` and `caugJAM`).
- `pyproject.toml` — name `stacking-as-words`, version `0.1.0`,
  dependency `caugjam @ v0.1.0`, `[tests]` extra.
- `CHANGELOG.md`, `CITATION.cff`, `LICENSE` (MIT).
- `.gitignore` — excludes `data/`, `__pycache__`, installed packages.

### Documentation

- `README.md` (English) and `README.es.md` (Spanish) — short, paper-forward.
- `docs/research_notes.md` — the original exploratory notes (Spanish),
  with a bilingual header.
- `outputs/` — captured experiment outputs (7 files).

### Data (versioned)

- `outputs/*.txt` — reproducible evidence of the 5 claims.

### Data (not versioned)

- `data/**/canonicas.txt` — regenerable, can exceed 100 MB at high `k`.
- `data/fibration/**/*.tsv` — not yet present; needed by `exp06` and
  `exp16`.

### Links

- GitHub: <https://github.com/edgar-castillo-sci/stacking-as-words\>
- CI: passing on `main`.
- Zenodo: pending (see **Release**).

## What we are going to do

### Phase A — Rigor (done)

Completed in commit `1774cdf`. Details below kept for reference.

| ID | Task | Priority | Estimate | Definition of done |
|---|---|---|---|---|
| A1 | `data/summary/*.tsv` — versioned summaries: class counts per `k` and option, `N'(d)` for PL, fibration summary if available | `[B]` | 30 min | Each `.tsv` has a header row, ≤ 50 KB, and is committed |
| A2 | `data/README.md` — describes each `.tsv`, which script generates it, with what caugJAM version, and how to verify against canonJAM | `[B]` | 15 min | File committed, referenced from main README |
| A3 | `experiments/verify_data.py` — loads the versioned `.tsv`, verifies against Burnside / published class counts; optional `--regenerate` recomputes with caugJAM and checks against canonJAM full method | `[B]` | 45 min | Runs in < 10 s; exits 0 on success |
| A4 | `README.md` / `README.es.md`: new section `## Dependencies` — what caugJAM is used for, what breaks without it | `[B]` | 15 min | Section between "Contents" and "Installation" in both READMEs |
| A5 | `README.md` / `README.es.md`: new section `## Data provenance` — points to `data/README.md`, `verify_data.py`, and the caugJAM version | `[B]` | 15 min | Section present in both READMEs |

**Why this phase is blocking:** without A1–A3, a reviewer cannot audit the
data without installing caugJAM (an unpublished piece of software) and
regenerating everything. With A1–A3, the reviewer runs
`python3 experiments/verify_data.py` and has reproducible evidence in
~10 s.

### Phase B — Runtime visibility (recommended)

| ID | Task | Priority | Estimate | Definition of done |
|---|---|---|---|---|
| B1 | `load_canonical(return_source=True)` and `load_fibration(return_source=True)` — record `"env" / "cache" / "generated" / "missing"` | `[R]` | 20 min | `sw.provenance.canonical_source(option, k)` returns the recorded source |
| B2 | `experiments/run_all.py` — pipeline entry point with `--deps`, `--list`, `--no-save` | `[R]` | 15 min | Runs in sequence, writes `outputs/<name>.txt` |
| B3 | `data/fibration/README.md` — how to obtain the `.tsv` from caugJAM, or point `$SW_DATA_DIR` at an existing directory | `[R]` | 10 min | File committed; `exp06`/`exp16` print a clear message when no data is available |

**Why this phase is recommended:** the runtime visibility makes the
`caugJAM` dependency explicit in every run, not just in the README.

### Phase C — Release v0.1.0 (in progress)

| ID | Task | Priority | Estimate | Definition of done |
|---|---|---|---|---|
| C1 | Tag `v0.1.0` with detailed message, GitHub Release, Zenodo record | `[B]` | 20 min | Release URL + Zenodo version DOI in hand |
| C2 | `CITATION.cff`: add the version DOI | `[B]` | 5 min | `doi:` field present |
| C3 | `README.md` / `README.es.md`: add badges (CI, DOI, Python, License) | `[R]` | 10 min | Badges render at the top |

### Phase D — Cross-links (optional)

| ID | Task | Priority | Estimate | Definition of done |
|---|---|---|---|---|
| D1 | `canonJAM/README.md`: mention `stacking-as-words` in "Related packages" | `[O]` | 5 min | One line added |
| D2 | `caugJAM/README.md`: already links to `stacking-as-words` (done in v0.1.0) | — | — | — |
| D3 | `canonJAM/CHANGELOG.md`, `caugJAM/CHANGELOG.md`: mention that `stacking-as-words` uses them | `[O]` | 5 min | One line each |

## Rigor rationale

The paper `Stacking as Words` cites Zenodo DOIs for `canonJAM` and
`caugJAM` (software), not published papers, and does not depend on the
theorems of `Growing as Pruning` (in preparation). It depends only on
the *output* of `caugJAM.generate_poda`, which is:

1. The same set `X_k/G` produced by the full method of `canonJAM`
   (verifiable at each `k`, see `experiments/verify_data.py`).
2. Archived as versioned `.tsv` in `data/summary/` (Phase A).
3. Reproducible in under a minute from the `.tsv` alone, without
   installing any JAM package (Phase A, A3).

A reviewer does not need to verify the pruning method or read the
companion paper to accept the empirical results. The data provenance
chain is: `canonJAM` (definition of `κ`) → `caugJAM` (generator) →
`data/summary/*.tsv` (archived evidence) → `verify_data.py`
(independent check).

## Out of scope (paper-level work)

The manuscript `Stacking_as_Words.tex` lives outside this repository.
Its remaining tasks (adding `canonJAM` / `caugJAM` bibliography
entries, `\paragraph{Data availability}`, and the `post_canonjam` →
`stacking_as_words` rename) are tracked separately.

## How to update this document

- Change `*Last updated*` at the top.
- Move items between **What we have** and **What we are going to do** as
  they are completed, or delete them entirely if they become obvious
  from the README.
- Keep the `[B]` / `[R]` / `[O]` priorities: they are the only thing a
  reader should scan before deciding what to do next.
- Do not add sub-items: if a task needs a checklist, put it in a
  separate `docs/<task>.md`.
