"""B7 — the acceptance fixture as a `(raw, build)` pair.

THE PROBLEM. `fixture_corrected(sym, month)` reads its inputs from disk every
time it is called: a snapshots parquet, a trades parquet, and an MBO aggregate
built by scanning a ~182 MB file. The column probe calls `build` once per
strategy per column -- on the order of seventy times -- and re-reading those
inputs on every call makes the probe cost dominated by I/O that the probe is not
even perturbing.

THE APPROACH, AND WHY IT IS NOT A TRANSCRIPTION. The obvious lift is to copy the
builder's body into a function of three frames. That would produce a `build` that
is *like* the fixture's builder, and a dependency map for a pipeline that is not
the one under audit. The risk is not hypothetical: the builder is 100+ lines of
rolling windows and merges, and a single transcribed `min_periods` would move
results without moving anything a reader would notice.

**So the builder is not touched. Its I/O is.** `read_inputs` performs the three
reads once and returns them as the `raw` dict. `builder_for` returns a `build`
callable that runs the ORIGINAL `fixture_corrected` with those reads intercepted
and served from `raw`. What executes is the fixture's own code, byte for byte,
and `raw` is exactly what that code would otherwise have loaded.

WHAT THIS BUYS THE PROBE. Perturbing `raw["trades"]` and re-running `build` now
exercises the real `ts_floor` join -- the fixture's own headline availability
channel -- against the real aggregation. That is the thing worth probing, and a
transcribed builder would have been probing a copy of it.

THE EQUALITY CHECK IS AN INSTRUMENT, NOT A FORMALITY. `assert_matches_fixture`
compares the adapter's output to an unadapted `fixture_corrected` run, exact.
Its own known-positive lives in `tests/phase1/test_fixture_adapter.py`: the
adapter is deliberately corrupted and the check must FIRE. A check that has only
ever passed has not been shown to detect anything.
"""
from __future__ import annotations

import contextlib
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import pandas as pd

# The fixture's own code. It is imported, never copied: `fixture.py` defines
# fixture_corrected as the pre-fix builder plus the universal shift(1), and
# `phase5_ml_fixture.py` is a byte-verified copy of the archive builder with
# write paths redirected.
#
# THIS RESOLVES INSIDE THE REPOSITORY. Until R173 it was a hard-coded absolute
# path into one machine's session scratchpad, so four of this suite's tests could
# run on exactly one computer -- and the skip message told everyone else the code
# "is not part of this repository", which was not true. It is committed at
# evidence/fixture_spike/f2, byte-identical to the scratchpad copy, and
# INSTALL.md already named that location. The repository, the install document
# and the test now agree.
#
# LEAKAUDIT_F2_DIR overrides it, for running against a spike copy without
# editing source. The override is explicit and never the default.
_REPO_F2 = Path(__file__).resolve().parents[2] / "evidence" / "fixture_spike" / "f2"
F2_DIR = Path(os.environ.get("LEAKAUDIT_F2_DIR") or _REPO_F2)


class FixtureUnavailable(RuntimeError):
    """The fixture's code or inputs are not reachable from here."""


def _import_fixture():
    if not F2_DIR.exists():
        raise FixtureUnavailable(
            "the fixture's producing code is not at %s. The committed copy is at "
            "evidence/fixture_spike/f2; if this path is elsewhere, "
            "LEAKAUDIT_F2_DIR points at an override that does not exist, and "
            "unsetting it restores the committed copy." % F2_DIR)
    if str(F2_DIR) not in sys.path:
        sys.path.insert(0, str(F2_DIR))
    # NO BYTECODE INTO THE EVIDENCE TREE. F2_DIR now resolves inside
    # evidence/, and every file there is attested individually by
    # evidence/MANIFEST.sha256. Importing normally writes __pycache__/*.pyc
    # beside the sources, which the manifest does not list and the coverage
    # check reports as unattested files in the evidence tree -- measured, not
    # anticipated: the first repoint produced exactly two such findings. The
    # suppression is scoped to these two imports and restored afterwards.
    prior = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        import fixture as fx                  # noqa: PLC0415
        import phase5_ml_fixture as p5        # noqa: PLC0415
    finally:
        sys.dont_write_bytecode = prior
    return fx, p5


@dataclass(frozen=True)
class FixtureInputs:
    """The frames the builder reads, plus what identifies them.

    `frames` holds everything the capture saw. `raw` holds only what the builder
    actually reads WHEN SERVED FROM MEMORY, and the two differ by one entry:

    THE RAW MBO PARQUET IS CAPTURED AND DELIBERATELY NOT PROBED. `load_mbo_aggregated`
    scans an 8.2-million-row file to produce the 464k-row `magg` aggregate. Serving
    `magg` from memory means that scan never happens -- which is most of what the
    adapter is for. But it also means the raw frame is never read under the adapter,
    so a probe that perturbed its three columns would find no movement and record
    `observed_silence` on all three. **That silence would be a fact about the
    adapter, not about the pipeline**, and a dependency map is exactly the place
    where such an artifact would read as a finding. It is excluded from `raw` and
    retained in `frames` so the exclusion is visible rather than implicit.
    """
    sym: str
    month: str
    frames: dict[str, pd.DataFrame]

    @property
    def raw(self) -> dict[str, pd.DataFrame]:
        return {k: v for k, v in self.frames.items()
                if not k.startswith("other:") and v is not None}

    @property
    def not_probed(self) -> tuple[str, ...]:
        """Captured but outside the probe's surface, with the reason above."""
        return tuple(sorted(k for k in self.frames if k.startswith("other:")))


def read_inputs(sym: str, month: str) -> FixtureInputs:
    """Perform the builder's three reads ONCE, and return them as `raw`.

    The frames are captured by running the builder with its reads intercepted
    and recorded. Capturing them this way rather than reading the parquets
    directly means `raw` is definitionally what the builder loads -- including
    any column selection or dtype handling the builder's own read applies.
    """
    fx, p5 = _import_fixture()
    captured: dict[str, pd.DataFrame] = {}

    real_read = p5.pq.read_table
    real_mbo = p5.load_mbo_aggregated

    def spy_read(path, *a, **kw):
        table = real_read(path, *a, **kw)
        name = Path(str(path)).name
        key = "snap" if "_snapshots_" in name else (
            "trades" if "_trades_" in name else "other:" + name)
        captured.setdefault(key, table.to_pandas())
        return table

    def spy_mbo(s, m):
        out = real_mbo(s, m)
        captured["magg"] = None if out is None else out.copy(deep=True)
        return out

    p5.pq.read_table = spy_read
    p5.load_mbo_aggregated = spy_mbo
    try:
        if fx.fixture_contaminated(sym, month) is None:
            raise FixtureUnavailable(
                "the builder returned None for %s %s -- its inputs are not on "
                "this machine" % (sym, month))
    finally:
        p5.pq.read_table = real_read
        p5.load_mbo_aggregated = real_mbo

    if "snap" not in captured:
        raise FixtureUnavailable("no snapshots frame was read; the capture is empty")
    return FixtureInputs(sym, month, captured)


@contextlib.contextmanager
def _served_from(p5, frames: dict[str, pd.DataFrame]):
    """Serve the builder's reads from `frames` instead of from disk.

    Each served frame is COPIED on the way out. The builder mutates what it
    reads -- it assigns columns onto `snap` -- and handing it the caller's object
    would let one probe run alter the input of the next, which would show up as
    nondeterminism in a pipeline that is deterministic.
    """
    import pyarrow as pa                       # noqa: PLC0415

    real_read, real_mbo = p5.pq.read_table, p5.load_mbo_aggregated

    def served_read(path, *a, **kw):
        name = Path(str(path)).name
        key = "snap" if "_snapshots_" in name else (
            "trades" if "_trades_" in name else "other:" + name)
        if key in frames and frames[key] is not None:
            return pa.Table.from_pandas(frames[key].copy(deep=True),
                                        preserve_index=False)
        return real_read(path, *a, **kw)

    def served_mbo(s, m):
        if "magg" in frames:
            g = frames["magg"]
            return None if g is None else g.copy(deep=True)
        return real_mbo(s, m)

    p5.pq.read_table, p5.load_mbo_aggregated = served_read, served_mbo
    try:
        yield
    finally:
        p5.pq.read_table, p5.load_mbo_aggregated = real_read, real_mbo


def builder_for(inputs: FixtureInputs, side: str = "corrected") -> Callable:
    """Return `build(raw)` -- the fixture's OWN builder, served from memory.

    `side` selects `fixture_corrected` or `fixture_contaminated`. PREREG.md
    SC-7(d) makes one-side-at-a-time a hard sequencing rule, so a builder is
    bound to a single side and never switches.
    """
    if side not in ("corrected", "contaminated"):
        raise ValueError("side must be 'corrected' or 'contaminated', got %r" % side)
    fx, p5 = _import_fixture()
    fn = fx.fixture_corrected if side == "corrected" else fx.fixture_contaminated

    def build(raw: dict[str, pd.DataFrame]) -> pd.DataFrame:
        with _served_from(p5, raw):
            out = fn(inputs.sym, inputs.month)
        if out is None:
            raise FixtureUnavailable("the builder returned None under the adapter")
        return out

    build.__name__ = "fixture_%s_%s_%s" % (side, inputs.sym, inputs.month)
    return build


def unadapted(sym: str, month: str, side: str = "corrected") -> pd.DataFrame:
    """Run the fixture builder normally, reading from disk. The reference."""
    fx, _ = _import_fixture()
    fn = fx.fixture_corrected if side == "corrected" else fx.fixture_contaminated
    out = fn(sym, month)
    if out is None:
        raise FixtureUnavailable("the builder returned None for %s %s" % (sym, month))
    return out


def assert_matches_fixture(inputs: FixtureInputs, side: str = "corrected"):
    """Compare the adapter's output to an unadapted run, EXACT.

    Returns (ok, differing_columns, detail). Never raises on a mismatch: a
    mismatch is the result this instrument exists to produce, and a raise would
    lose the column list that says where the adapter diverged.
    """
    from .determinism import frames_equal      # noqa: PLC0415

    build = builder_for(inputs, side)
    adapted = build(inputs.raw)
    reference = unadapted(inputs.sym, inputs.month, side)
    return frames_equal(reference, adapted)
