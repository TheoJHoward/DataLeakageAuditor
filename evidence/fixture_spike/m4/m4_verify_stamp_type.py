"""M4 (independent re-derivation): per-stamp-type split of strict availability
violations, contaminated side vs decision time T.

MEASUREMENT ONLY.  Reads (read-only):
  fixture_spike/f2/out/contaminated_zc_2025-01_run1.pkl      (row stamps T)
  fixture_spike/t1/per_second_trades.parquet, per_second_mbo.parquet
  fixture_spike/t1/violation_table.csv                       (expected totals)
  C:\\Users\\ttbea\\OneDrive\\Desktop\\MBO_2025\\processed\\zc\\zc_trades_tagged_2025-01.parquet
  C:\\Users\\ttbea\\OneDrive\\Desktop\\MBO_2025\\processed\\zc\\zc_mbo_2025-01.parquet
Writes: only under fixture_spike/m4/.

Stamp type of a lattice row:
  integral-second  T == floor(T)   (ns-within-second == 0)
  mid-second       T >  floor(T)

Strict violation (contaminated / decision_T, t1 definition): at least one event of
the class with  T < ts_event < floor(T)+1s.  Equal-tie: ts_event == T exactly.

Two independent estimators, compared row-for-row for all 10 classes:
  RUNMAX  per-second last-stamp table built by run boundaries on the sorted event
          array (np.unique on the second index), mapped onto the row's own second
          with a pandas hashtable reindex.  strict <=> sec present and max_ts > T.
          Exact because every event of the row's own second lies in [fl, fl+1s).
  SSORT   searchsorted replication of t1_measure.py row_indicators().
Equal-tie is computed with a hashtable membership test (pd.Index.get_indexer),
a different code path from the searchsorted left/right pair used by t1.
"""
import hashlib
import json
import os
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

M4 = os.path.dirname(os.path.abspath(__file__))
SPIKE = os.path.dirname(M4)
F2_OUT = os.path.join(SPIKE, "f2", "out")
T1 = os.path.join(SPIKE, "t1")
RAW = r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025\processed\zc"
NS = 1_000_000_000

log_lines = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    log_lines.append(s)


# ---------------------------------------------------------------- provenance
pkl = os.path.join(F2_OUT, "contaminated_zc_2025-01_run1.pkl")
h = hashlib.sha256()
with open(pkl, "rb") as f:
    for chunk in iter(lambda: f.read(1 << 22), b""):
        h.update(chunk)
say(f"pkl file-bytes sha256 = {h.hexdigest()}")

# ---------------------------------------------------------------- row stamps
cont = pd.read_pickle(pkl)
say("contaminated pkl shape:", cont.shape)
# the sidecar .sha256 / meta.json field is the CANONICAL CSV digest, not the file
# bytes: run_fixture.py:28-31  df.to_csv(index=False, float_format="%.12g") -> sha256
_s = cont.to_csv(index=False, float_format="%.12g")
_d = hashlib.sha256(_s.encode("utf-8")).hexdigest()
_rec = open(pkl.replace(".pkl", ".sha256")).read().strip().split()[0]
_meta = json.load(open(pkl.replace(".pkl", ".meta.json")))
say(f"canonical_csv sha256 recomputed = {_d}  bytes={len(_s)}")
say(f"canonical_csv sha256 recorded   = {_rec}  bytes={_meta['canonical_csv_bytes']}"
    f"  match={_d == _rec and len(_s) == _meta['canonical_csv_bytes']}")
assert _d == _rec and len(_s) == _meta["canonical_csv_bytes"]
del _s
ts = pd.to_datetime(cont["timestamp"])
if ts.dt.tz is not None:
    ts = ts.dt.tz_localize(None)
t_ns = ts.astype("int64").to_numpy()
n_rows = len(t_ns)
fl = (t_ns // NS) * NS
sec_end = fl + NS
off = t_ns - fl                     # ns offset inside the row's own second
integral = off == 0
mid = ~integral
n_int, n_mid = int(integral.sum()), int(mid.sum())
say(json.dumps({"rows": n_rows, "rows_integral(T==floor)": n_int,
                "rows_mid_second(T>floor)": n_mid,
                "monotone_strictly_increasing": bool(np.all(np.diff(t_ns) > 0))}))
assert n_int + n_mid == n_rows

# ------------------------------------------------------- raw archive classes
tr = pq.read_table(os.path.join(RAW, "zc_trades_tagged_2025-01.parquet"),
                   columns=["ts_event", "aggressor_side", "size"]).to_pandas()
tr["ts_event"] = pd.to_datetime(tr["ts_event"])
if tr["ts_event"].dt.tz is not None:
    tr["ts_event"] = tr["ts_event"].dt.tz_localize(None)
tr_ns = tr["ts_event"].astype("int64").to_numpy()
is_buy = tr["aggressor_side"].isin(["B", "Buy", "buy"]).to_numpy()

mbo = pq.read_table(os.path.join(RAW, "zc_mbo_2025-01.parquet"),
                    columns=["ts_event", "action", "side"]).to_pandas()
mbo["ts_event"] = pd.to_datetime(mbo["ts_event"])
if mbo["ts_event"].dt.tz is not None:
    mbo["ts_event"] = mbo["ts_event"].dt.tz_localize(None)
mbo_ns = mbo["ts_event"].astype("int64").to_numpy()
m_is_bid = mbo["side"].isin(["B", "b", "Buy", "bid"]).to_numpy()
m_act = mbo["action"].to_numpy()

classes = {
    "trades_all":     np.sort(tr_ns),
    "trades_buy":     np.sort(tr_ns[is_buy]),
    "trades_sell":    np.sort(tr_ns[~is_buy]),
    "trades_large":   np.sort(tr_ns[(tr["size"] >= 10).to_numpy()]),
    "mbo_all":        np.sort(mbo_ns),
    "mbo_bid_add":    np.sort(mbo_ns[(m_act == "A") & m_is_bid]),
    "mbo_ask_add":    np.sort(mbo_ns[(m_act == "A") & ~m_is_bid]),
    "mbo_bid_cancel": np.sort(mbo_ns[(m_act == "C") & m_is_bid]),
    "mbo_ask_cancel": np.sort(mbo_ns[(m_act == "C") & ~m_is_bid]),
    "mbo_cancel_any": np.sort(mbo_ns[(m_act == "C")]),
}
say("class event counts:", json.dumps({k: int(len(v)) for k, v in classes.items()}))

# ------------------------------------------------------------- expected (t1)
vt = pd.read_csv(os.path.join(T1, "violation_table.csv"))
m = vt[(vt.side == "contaminated") & (vt.boundary == "decision_T")]
EXP_S = m.groupby("event_class")["strictly_after_count"].max().to_dict()
EXP_E = m.groupby("event_class")["equal_count"].max().to_dict()
say("t1 expected strict:", json.dumps({k: int(v) for k, v in EXP_S.items()}))


# ------------------------------------------------------------- estimators
def per_second_runmax(a):
    """(unique second start ns, max event ts in that second) from sorted array a."""
    if len(a) == 0:
        z = np.zeros(0, dtype="int64")
        return z, z, z
    sec = (a // NS) * NS
    uniq, first = np.unique(sec, return_index=True)
    last = np.append(first[1:], len(a)) - 1
    return uniq, a[last], np.diff(np.append(first, len(a)))


def strict_runmax(a):
    uniq, mx, _ = per_second_runmax(a)
    row_max = pd.Series(mx, index=uniq).reindex(fl).to_numpy()   # NaN if empty sec
    ok = ~np.isnan(row_max)
    out = np.zeros(n_rows, dtype=bool)
    out[ok] = row_max[ok] > t_ns[ok]
    return out, ok, row_max


def strict_ssort(a):
    hi_b = np.searchsorted(a, t_ns, "right")
    lo_w = np.searchsorted(a, fl, "left")
    hi_w = np.searchsorted(a, sec_end, "left")
    return hi_w > np.maximum(hi_b, lo_w)


def equal_hash(a):
    return pd.Index(np.unique(a)).get_indexer(t_ns) >= 0


# t1 per-second parquets vs my recomputed tables (ties the t1 parquet inputs in)
for cname, pth in [("trades_all", "per_second_trades.parquet"),
                   ("mbo_all", "per_second_mbo.parquet")]:
    ps = pd.read_parquet(os.path.join(T1, pth))
    u, mx, cnt = per_second_runmax(classes[cname])
    same = (len(ps) == len(u)
            and np.array_equal(ps["sec_start_ns"].to_numpy(), u)
            and np.array_equal(ps["max_ts_ns"].to_numpy(), mx)
            and np.array_equal(ps["count"].to_numpy(), cnt))
    say(f"t1 {pth}: seconds={len(ps)} identical_to_recomputed={same}")
    assert same

# ------------------------------------------------------------- per class
rows_out, mism = [], 0
masks = {}
for cname, a in classes.items():
    s_run, sec_present, row_max = strict_runmax(a)
    s_ss = strict_ssort(a)
    d = int((s_run != s_ss).sum())
    e = equal_hash(a)
    n_s, n_e = int(s_ss.sum()), int(e.sum())
    ok_s, ok_e = n_s == EXP_S[cname], n_e == EXP_E[cname]
    if not (ok_s and ok_e):
        say(f"MISMATCH vs t1 [{cname}] strict {n_s} exp {EXP_S[cname]} / "
            f"equal {n_e} exp {EXP_E[cname]}")
        mism += 1
    say(f"{cname:15s} RUNMAX={int(s_run.sum()):7d} SSORT={n_s:7d} "
        f"row_disagreements={d} equal={n_e} matches_t1={ok_s and ok_e}")
    assert d == 0, f"estimators disagree on {cname}"
    masks[cname] = (s_ss, e, sec_present, row_max)
    si, sm = int((s_ss & integral).sum()), int((s_ss & mid).sum())
    ei, em = int((e & integral).sum()), int((e & mid).sum())
    rows_out.append(dict(
        event_class=cname, side="contaminated", boundary="decision_T",
        rows_total=n_rows, rows_integral=n_int, rows_mid_second=n_mid,
        strict_viol_integral=si, strict_viol_mid_second=sm, strict_viol_total=n_s,
        strict_total_matches_t1=ok_s,
        equal_tie_integral=ei, equal_tie_mid_second=em, equal_tie_total=n_e,
        equal_total_matches_t1=ok_e,
        viol_rate_integral=round(si / n_int, 6),
        viol_rate_mid_second=round(sm / n_mid, 6),
        rate_ratio_integral_over_mid=(round(( si / n_int) / (sm / n_mid), 3)
                                      if sm else np.nan),
        share_of_viol_on_integral=round(si / n_s, 6) if n_s else np.nan,
        share_of_rows_integral=round(n_int / n_rows, 6),
        # counterfactual: violation each row WOULD carry if its stamp were integral
        # (i.e. the row's own second contains any event strictly after floor(T))
        cf_integral_stamp_viol_rate_on_mid_rows=round(
            float(((~np.isnan(row_max)) & (row_max > fl) & mid).sum()) / n_mid, 6),
        cf_mid_rows_viol_if_stamp_were_integral=int(
            ((~np.isnan(row_max)) & (row_max > fl) & mid).sum()),
        cf_viol_total_if_all_stamps_integral=int(
            si + ((~np.isnan(row_max)) & (row_max > fl) & mid).sum()),
        estimators="RUNMAX(per-second run boundaries)==SSORT(t1 searchsorted), "
                   f"row_disagreements={d}",
    ))

out = pd.DataFrame(rows_out)
out.to_csv(os.path.join(M4, "stamp_type_breakdown.csv"), index=False)
say("\nstamp_type_breakdown.csv written:", out.shape, " classes mismatching t1:", mism)
say(out[["event_class", "strict_viol_integral", "strict_viol_mid_second",
         "strict_viol_total", "viol_rate_integral", "viol_rate_mid_second",
         "share_of_viol_on_integral",
         "cf_integral_stamp_viol_rate_on_mid_rows"]].to_string(index=False))

# --------------------------------------------- structure of mid-second stamps
say("\n--- mid-second stamp offsets (ns inside the second) ---")
vc = pd.Series(off[mid]).value_counts()
say("distinct offsets among mid-second rows:", len(vc))
top = vc.head(12)
say("offset_ms          rows   cum_share")
c = 0
for v, k in top.items():
    c += k
    say(f"{v/1e6:12.6f} {k:9d} {c/n_mid:10.4f}")

s_tr = masks["trades_all"][0]
s_mb = masks["mbo_all"][0]
say("\n--- violation rate by remaining-time-in-second bucket (1s - offset) ---")
rem_ms = (NS - off) / 1e6
edges = [0, 1, 10, 100, 250, 500, 750, 999, 1000.0001]
lab = ["(0,1]ms", "(1,10]", "(10,100]", "(100,250]", "(250,500]", "(500,750]",
       "(750,999]", "(999,1000]ms = integral stamps"]
bk = pd.cut(rem_ms, bins=edges, labels=lab, include_lowest=True)
# counterfactual indicator: violation this row WOULD carry with an integral stamp
cf_tr = (~np.isnan(masks["trades_all"][3])) & (masks["trades_all"][3] > fl)
cf_mb = (~np.isnan(masks["mbo_all"][3])) & (masks["mbo_all"][3] > fl)
tab = pd.DataFrame({"bucket": bk, "trades": s_tr, "mbo": s_mb, "integral": integral,
                    "cf_tr": cf_tr, "cf_mb": cf_mb}
                   ).groupby("bucket", observed=False).agg(
    rows=("trades", "size"), trades_viol=("trades", "sum"),
    mbo_viol=("mbo", "sum"), n_integral=("integral", "sum"),
    cf_trades_viol=("cf_tr", "sum"), cf_mbo_viol=("cf_mb", "sum"))
tab["trades_rate"] = (tab.trades_viol / tab.rows).round(6)
tab["cf_trades_rate"] = (tab.cf_trades_viol / tab.rows).round(6)
tab["mbo_rate"] = (tab.mbo_viol / tab.rows).round(6)
tab["cf_mbo_rate"] = (tab.cf_mbo_viol / tab.rows).round(6)
say(tab.to_string())
say("cf_* = same rows, counterfactual integral stamp (any event after floor(T)); "
    "gap between rate and cf_rate isolates the stamp-position effect from liquidity")

say("\n--- per distinct mid-second offset ---")
mo = pd.DataFrame({"offset_ms": (off / 1e6), "tr": s_tr, "mb": s_mb,
                   "cf_tr": cf_tr, "cf_mb": cf_mb,
                   "day": pd.to_datetime(fl[: len(fl)]).floor("D")})[mid]
g = mo.groupby("offset_ms").agg(rows=("tr", "size"), tr_viol=("tr", "sum"),
                                cf_tr_viol=("cf_tr", "sum"), mb_viol=("mb", "sum"),
                                cf_mb_viol=("cf_mb", "sum"),
                                first_day=("day", "min"), last_day=("day", "max"))
g["mb_rate"] = (g.mb_viol / g.rows).round(6)
g["cf_mb_rate"] = (g.cf_mb_viol / g.rows).round(6)
say(g.to_string())
g.to_csv(os.path.join(M4, "mid_second_offsets.csv"))
tab.to_csv(os.path.join(M4, "viol_rate_by_remaining_time.csv"))

say("\n--- counterfactual control (were the mid-second rows simply quiet?) ---")
for cname in ["trades_all", "mbo_all"]:
    s, e, present, row_max = masks[cname]
    cf = (~np.isnan(row_max)) & (row_max > fl)     # indicator if stamp were integral
    say(f"{cname}: mid-second rows whose own second is non-empty: "
        f"{int((present & mid).sum())}/{n_mid} = {(present & mid).sum()/n_mid:.4f}; "
        f"counterfactual integral-stamp viol rate on those same rows: "
        f"{(cf & mid).sum()/n_mid:.6f}; actual mid rate: {(s & mid).sum()/n_mid:.6f}; "
        f"actual integral rate: {(s & integral).sum()/n_int:.6f}")

with open(os.path.join(M4, "m4_verify_output.txt"), "w") as f:
    f.write("\n".join(log_lines) + "\nDONE\n")
say("DONE")
