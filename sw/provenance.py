"""Data provenance tracking for the stacking-as-words experiments.

Makes the caugJAM dependency visible at runtime. Use `format_deps()` to
print the versions of the key dependencies, and `canonical_source` /
`fibration_source` to see where the data for a given (option, k) came
from.
"""

from .common import _data_sources, _fib_sources


def _pkg_version(name):
    """Return the __version__ of an installed package, or None."""
    try:
        mod = __import__(name)
    except ImportError:
        return None
    return getattr(mod, "__version__", "unknown")


def deps_report():
    """Return a dict with the versions of the key dependencies."""
    return {
        "caugjam": _pkg_version("caugjam"),
        "canonjam": _pkg_version("canonjam"),
        "numpy": _pkg_version("numpy"),
    }


def format_deps():
    """Human-readable dependency summary."""
    deps = deps_report()
    lines = ["Dependencies:"]
    for name, v in deps.items():
        if v is None:
            lines.append(f"  {name:10s}  MISSING")
        else:
            lines.append(f"  {name:10s}  {v}")
    return "\n".join(lines)


def canonical_source(option, k):
    """Return the source of canonical data for (option, k), if loaded.

    One of "env", "cache", "generated", or None (not loaded yet).
    """
    return _data_sources.get((option, k))


def fibration_source(option, k):
    """Return the source of fibration data for (option, k), if loaded.

    One of "env", "cache", "missing", or None (not loaded yet).
    """
    return _fib_sources.get((option, k))
