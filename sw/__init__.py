"""Shared helpers for the stacking-as-words experiments."""

from .common import (
    S3,
    THREE_CYCLES,
    apply_perm,
    is_s3_palindromic,
    is_periodic,
    is_strict_palindrome,
    is_3fold_screw,
    classify,
    chain_to_word,
    load_canonical,
    load_fibration,
    divisors,
    moebius,
)

from .provenance import (
    deps_report,
    format_deps,
    canonical_source,
    fibration_source,
)

__all__ = [
    "S3", "THREE_CYCLES",
    "apply_perm", "is_s3_palindromic", "is_periodic",
    "is_strict_palindrome", "is_3fold_screw", "classify",
    "chain_to_word", "load_canonical", "load_fibration",
    "divisors", "moebius",
    "deps_report", "format_deps", "canonical_source", "fibration_source",
]
