"""F2 fixture callables: fixture_contaminated (pre-fix phase5 builder, verbatim copy
with write paths redirected) and fixture_corrected (same builder + the universal
shift(1) lag exactly as applied inline by
results/pc2_all_phases/_scripts/scripts/phase7_l2_sim.py lines 260-276).

No post-fix phase5 builder exists in the archive (grep for _NO_LAG: no hits), so the
corrected side is assembled as builder-plus-shift wrapper, mirroring phase7_l2_sim.py's
exempt-column scope verbatim.
"""
import sys
from pathlib import Path

_F2 = Path(__file__).resolve().parent
if str(_F2) not in sys.path:
    sys.path.insert(0, str(_F2))

import phase5_ml_fixture as p5  # verbatim copy of archive phase5_ml.py, write paths redirected


def fixture_contaminated(sym, month):
    """Pre-fix feature frame: phase5_ml.build_features_month unchanged."""
    meta = p5.INST_META[sym]
    return p5.build_features_month(sym, month, meta, p5.HORIZONS)


def apply_universal_lag(snap):
    """Universal lag fix, transcribed from phase7_l2_sim.py lines 260-276.

    Verbatim scope from that file:
        EXEMPT_COLS = {"timestamp", "mid_price", "month", "ts_floor", "hour_utc"}
        label_cols  = {c for c in snap.columns if c.startswith("fwd_move_ticks_")}
        raw_book_cols = bid_price_1..5 | ask_price_1..5 | bid_size_2..5 | ask_size_2..5
                        | {"spread", "book_imbalance"}
        exempt = EXEMPT_COLS | label_cols | raw_book_cols
        feature_cols = [c for c in snap.columns if c not in exempt]
        snap[feature_cols] = snap[feature_cols].shift(1)

    Labels (fwd_move_ticks_*) and metadata are NOT lagged; bid_size_1/ask_size_1
    ARE lagged (they are features); raw book levels/spread/book_imbalance are exempt.
    """
    EXEMPT_COLS = {"timestamp", "mid_price", "month", "ts_floor", "hour_utc"}
    label_cols = {c for c in snap.columns if c.startswith("fwd_move_ticks_")}
    raw_book_cols = {f"bid_price_{i}" for i in range(1, 6)} | \
                    {f"ask_price_{i}" for i in range(1, 6)} | \
                    {f"bid_size_{i}" for i in range(2, 6)} | \
                    {f"ask_size_{i}" for i in range(2, 6)} | \
                    {"spread", "book_imbalance"}
    exempt = EXEMPT_COLS | label_cols | raw_book_cols

    feature_cols = [c for c in snap.columns if c not in exempt]
    snap[feature_cols] = snap[feature_cols].shift(1)
    return snap, feature_cols


def fixture_corrected(sym, month):
    """Post-fix feature frame: pre-fix builder output + universal shift(1) lag."""
    snap = fixture_contaminated(sym, month)
    if snap is None:
        return None
    snap, _ = apply_universal_lag(snap)
    return snap
