"""My pipeline. Written against `leakaudit --help` and `leakaudit schema` only.

GUESS RECORDED: `--pipeline module:function` says the build function takes "the
frames and returns the built output". `--frame name=path` is repeatable and
name-keyed, so I am assuming the argument is a dict keyed by those names. If it
is a positional list or keyword arguments instead, this will fail and I will find
out from the error.
"""
import pandas as pd


def build(frames):
    st = frames["stations"].copy()
    sc = frames["scans"].copy()

    st["timestamp"] = pd.to_datetime(st["timestamp"])
    sc["scanned_at"] = pd.to_datetime(sc["scanned_at"])

    # The decision row's own wall-clock second.
    st["sec"] = st["timestamp"].dt.floor("1s")
    sc["sec"] = sc["scanned_at"].dt.floor("1s")

    per_sec = sc.groupby("sec").agg(
        scan_count=("items", "count"),
        items_total=("items", "sum"),
        weight_total=("weight_kg", "sum"),
    ).reset_index()

    out = st.merge(per_sec, on="sec", how="left")
    for c in ("scan_count", "items_total", "weight_total"):
        out[c] = out[c].fillna(0)

    out["items_per_scan"] = out["items_total"] / out["scan_count"].replace(0, 1)
    out["load_index"] = out["queue_depth"] * out["belt_speed"]
    out["target"] = (out["items_total"] > 12).astype(int)

    return out[["timestamp", "queue_depth", "belt_speed", "scan_count",
                "items_total", "weight_total", "items_per_scan",
                "load_index", "target"]]
