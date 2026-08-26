"""
case_defs.py -- C1..C8 of the PREREG.md 9.2 comparison set, plus their clean paired controls.

Specification source: killgate/CROSS_TOOL_COMPARISON.md 2.2 (the committed protocol's case table).
This module IMPLEMENTS that table; it does not alter it.

Every case exposes, for each of two sides ("contaminated" and "clean"):
  - raw            : the raw input frame a feature builder consumes
  - build(raw)     : the feature-construction callable (leak-detect's data_creation_func surface)
  - full           : the built frame (features + target + any group/time columns)
  - train_idx/test_idx : positional index arrays into `full`
  - meta           : feature cols, target col, group col, time col, ground truth

Determinism: every case seeds its own numpy Generator. No global seed state is relied on.

Ground-truth convention:
  side "contaminated" -> the leakage of the case's type IS present. A tool eligible for the
                         case SHOULD fire.
  side "clean"        -> the leakage is absent. A tool SHOULD be silent. Firing is a false alarm.
"""

import numpy as np
import pandas as pd

N = 400  # rows per case, before any split


# --------------------------------------------------------------------------------------
# C1 -- T1 / L1.1 : missing or overlapping declared evaluation split
# Trap: indices are INTERLEAVED, so min/max range-disjointness holds on both sides and only a
#       genuine set-intersection test separates them.
# --------------------------------------------------------------------------------------
def c1(side):
    rng = np.random.default_rng(101)
    x = rng.normal(size=(N, 4))
    y = (x[:, 0] + 0.5 * x[:, 1] + rng.normal(scale=0.5, size=N) > 0).astype(int)
    full = pd.DataFrame(x, columns=[f"f{i}" for i in range(4)])
    full["target"] = y

    train_idx = np.arange(0, N, 2)          # even rows
    test_idx = np.arange(1, N, 2)           # odd rows -> ranges fully interleaved
    if side == "contaminated":
        k = 20
        stolen = train_idx[:k]              # k train rows ALSO declared as test
        test_idx = np.sort(np.concatenate([test_idx, stolen]))
    return dict(
        full=full, raw=full, build=lambda d: d,
        train_idx=train_idx, test_idx=test_idx,
        meta=dict(features=[f"f{i}" for i in range(4)], target="target",
                  group=None, time=None,
                  truth="20 declared-test indices are also declared-train (set overlap)"
                        if side == "contaminated" else "disjoint declared split"),
    )


# --------------------------------------------------------------------------------------
# C2 -- T2 / L1.2 : preprocessing fit on train+test
# The observable difference is in HOW the frame was produced, not only in the frame.
# --------------------------------------------------------------------------------------
def c2(side):
    rng = np.random.default_rng(202)
    x = rng.normal(loc=5.0, scale=3.0, size=(N, 4))
    x[N // 2:] += 4.0                       # test half is shifted, so a pooled fit differs
    y = (x[:, 0] - x[:, 0].mean() + rng.normal(scale=1.0, size=N) > 0).astype(int)
    cols = [f"f{i}" for i in range(4)]
    train_idx = np.arange(0, N // 2)
    test_idx = np.arange(N // 2, N)

    raw = pd.DataFrame(x, columns=cols)
    raw["target"] = y

    def build(d):
        v = d[cols].to_numpy(dtype=float)
        if side == "contaminated":
            mu, sd = v.mean(0), v.std(0)                       # POOLED fit: train+test
        else:
            mu, sd = v[:N // 2].mean(0), v[:N // 2].std(0)     # train-only fit
        out = pd.DataFrame((v - mu) / sd, columns=cols, index=d.index)
        out["target"] = d["target"].values
        return out

    full = build(raw)
    return dict(
        full=full, raw=raw, build=build,
        train_idx=train_idx, test_idx=test_idx,
        meta=dict(features=cols, target="target", group=None, time=None,
                  truth="StandardScaler fitted on pooled train+test"
                        if side == "contaminated" else "scaler fitted on train only"),
    )


# --------------------------------------------------------------------------------------
# C3 -- T3 / L1.3 : feature selection on train+test
# --------------------------------------------------------------------------------------
def c3(side):
    rng = np.random.default_rng(303)
    P = 30
    x = rng.normal(size=(N, P))
    y = (x[:, 0] + rng.normal(scale=2.0, size=N) > 0).astype(int)
    cols = [f"f{i}" for i in range(P)]
    train_idx = np.arange(0, N // 2)
    test_idx = np.arange(N // 2, N)

    raw = pd.DataFrame(x, columns=cols)
    raw["target"] = y

    def build(d):
        v = d[cols].to_numpy(dtype=float)
        t = d["target"].to_numpy()
        if side == "contaminated":
            sl = slice(None)                 # score on POOLED train+test
        else:
            sl = slice(0, N // 2)            # score on train only
        # univariate |corr| score, SelectKBest-shaped
        vv, tt = v[sl], t[sl]
        cc = np.array([abs(np.corrcoef(vv[:, j], tt)[0, 1]) for j in range(P)])
        keep = [cols[j] for j in np.argsort(-cc)[:5]]
        out = d[keep].copy()
        out["target"] = d["target"].values
        return out

    full = build(raw)
    return dict(
        full=full, raw=raw, build=build,
        train_idx=train_idx, test_idx=test_idx,
        meta=dict(features=[c for c in full.columns if c != "target"], target="target",
                  group=None, time=None,
                  truth="univariate feature selection scored on pooled train+test"
                        if side == "contaminated" else "selection scored on train only"),
    )


# --------------------------------------------------------------------------------------
# C4 -- T4 / L1.4a : exact duplicate rows ACROSS the split boundary
# Clean control keeps the same NUMBER of duplicate rows, but WITHIN one side only, so a
# generic "data duplicates" report cannot separate the sides -- only a cross-split test can.
# --------------------------------------------------------------------------------------
def c4(side):
    rng = np.random.default_rng(404)
    base = rng.normal(size=(N, 4)).round(4)
    y = (base[:, 0] + rng.normal(scale=0.5, size=N) > 0).astype(int)
    cols = [f"f{i}" for i in range(4)]
    full = pd.DataFrame(base, columns=cols)
    full["target"] = y

    train_idx = np.arange(0, N // 2)
    test_idx = np.arange(N // 2, N)
    k = 25
    v = full.to_numpy()
    if side == "contaminated":
        # copy k TRAIN rows onto k TEST rows -> exact duplication across the boundary
        v[N // 2: N // 2 + k] = v[0:k]
    else:
        # copy k TRAIN rows onto k OTHER TRAIN rows -> same duplicate count, within one side
        v[N // 4: N // 4 + k] = v[0:k]
    full = pd.DataFrame(v, columns=list(full.columns))
    full["target"] = full["target"].astype(int)
    return dict(
        full=full, raw=full, build=lambda d: d,
        train_idx=train_idx, test_idx=test_idx,
        meta=dict(features=cols, target="target", group=None, time=None,
                  truth=f"{k} exact duplicate rows spanning the train/test boundary"
                        if side == "contaminated" else f"{k} exact duplicate rows within train only"),
    )


# --------------------------------------------------------------------------------------
# C5 -- T5 / L2a : illegitimate feature computed from the label at the SAME row
# Deliberately easy, per the protocol: a miss is informative about the tool, not the threshold.
# --------------------------------------------------------------------------------------
def c5(side):
    rng = np.random.default_rng(505)
    x = rng.normal(size=(N, 3))
    y = (x[:, 0] + rng.normal(scale=0.8, size=N) > 0).astype(int)
    cols = ["f0", "f1", "f2"]
    raw = pd.DataFrame(x, columns=cols)
    raw["target"] = y
    train_idx = np.arange(0, N // 2)
    test_idx = np.arange(N // 2, N)

    # noise drawn ONCE, outside build(), so build() is a pure function of its argument.
    # leak-detect calls data_creation_func twice and compares the two outputs; a builder that
    # advanced RNG state between calls would not be a fair probe surface.
    noise = np.random.default_rng(5051).normal(scale=0.05, size=N)

    def build(d):
        out = d[cols].copy()
        t = d["target"].to_numpy(dtype=float)
        nz = noise[: len(d)]
        if side == "contaminated":
            # feature reads the label of its OWN row
            out["risk_score"] = t * 3.0 + nz
        else:
            # properly lagged label: row i uses the label of row i-1
            lag = np.concatenate([[0.0], t[:-1]])
            out["risk_score"] = lag * 3.0 + nz
        out["target"] = d["target"].values
        return out

    full = build(raw)
    return dict(
        full=full, raw=raw, build=build,
        train_idx=train_idx, test_idx=test_idx,
        meta=dict(features=cols + ["risk_score"], target="target", group=None, time=None,
                  truth="feature 'risk_score' is computed from the same-row label"
                        if side == "contaminated" else "feature 'risk_score' uses the previous row's label"),
    )


# --------------------------------------------------------------------------------------
# C6 -- T6 / L3.1 : features from unavailable cells -- ONE BAR OF REACH.  THE FLAGSHIP CASE.
#
# Declared per-cell availability model: the value x[t] of the decision bar t is NOT available
# at the moment the decision for bar t is made; it is only known once bar t has closed.
# Contaminated: trailing window mean over x[t-4 .. t]   -> INCLUDES the decision bar.
# Clean:        trailing window mean over x[t-5 .. t-1] -> excludes it.
#
# Both sides are strictly BACKWARD-looking in row position. No value from a row LATER than t is
# ever read. A detector that cuts on row position therefore sees no difference between the sides.
# --------------------------------------------------------------------------------------
def c6(side):
    rng = np.random.default_rng(606)
    n = N
    # x[t] carries a component that anticipates the forward move labelled at t
    shock = rng.normal(size=n)
    x = rng.normal(size=n) * 0.6 + shock * 0.8
    fwd = shock * 1.0 + rng.normal(scale=0.6, size=n)     # forward move decided at bar t
    y = (fwd > 0).astype(int)

    raw = pd.DataFrame({"t": np.arange(n), "x": x, "target": y})
    train_idx = np.arange(0, n // 2)
    test_idx = np.arange(n // 2, n)

    def build(d):
        s = pd.Series(d["x"].to_numpy(dtype=float))
        if side == "contaminated":
            w = s.rolling(5, min_periods=5).mean()          # x[t-4..t]  INCLUDES bar t
        else:
            w = s.shift(1).rolling(5, min_periods=5).mean()  # x[t-5..t-1] excludes bar t
        out = pd.DataFrame({"t": d["t"].values, "win5": w.to_numpy()}, index=d.index)
        out["target"] = d["target"].values
        return out

    full = build(raw)
    return dict(
        full=full, raw=raw, build=build,
        train_idx=train_idx, test_idx=test_idx,
        meta=dict(features=["win5"], target="target", group=None, time="t",
                  truth="trailing 5-bar mean INCLUDES the decision bar t, which the declared "
                        "availability model marks unavailable at decision time (one bar of reach)"
                        if side == "contaminated" else
                        "trailing 5-bar mean ends at t-1; every cell read is available at decision time"),
    )


# --------------------------------------------------------------------------------------
# C7 -- T7 / L3.2 : non-independence -- entity/group IDs on both sides of the split
# --------------------------------------------------------------------------------------
def c7(side):
    rng = np.random.default_rng(707)
    n_groups = 40
    gid = np.repeat(np.arange(n_groups), N // n_groups)
    geff = rng.normal(size=n_groups)[gid]
    x = rng.normal(size=(N, 3)) + geff[:, None] * 0.9
    y = (geff + rng.normal(scale=0.5, size=N) > 0).astype(int)
    cols = ["f0", "f1", "f2"]
    full = pd.DataFrame(x, columns=cols)
    full["group_id"] = gid
    full["target"] = y

    if side == "contaminated":
        # random row split -> the same group appears on both sides
        perm = np.random.default_rng(7071).permutation(N)
        train_idx, test_idx = np.sort(perm[:N // 2]), np.sort(perm[N // 2:])
    else:
        # split BY group -> no group spans the boundary
        train_idx = np.where(gid < n_groups // 2)[0]
        test_idx = np.where(gid >= n_groups // 2)[0]
    return dict(
        full=full, raw=full, build=lambda d: d,
        train_idx=train_idx, test_idx=test_idx,
        meta=dict(features=cols, target="target", group="group_id", time=None,
                  truth="group_id values appear in both train and test"
                        if side == "contaminated" else "split is by group_id; no group spans the split"),
    )


# --------------------------------------------------------------------------------------
# C8 -- T8 / L3.3 : sampling bias in the test set
# --------------------------------------------------------------------------------------
def c8(side):
    rng = np.random.default_rng(808)
    x = rng.normal(size=(N, 4))
    if side == "contaminated":
        # test half is drawn from a SHIFTED subpopulation
        x[N // 2:, 0] += 2.5
        x[N // 2:, 1] *= 2.0
    y = (x[:, 0] + rng.normal(scale=0.8, size=N) > 0).astype(int)
    cols = [f"f{i}" for i in range(4)]
    full = pd.DataFrame(x, columns=cols)
    full["target"] = y
    return dict(
        full=full, raw=full, build=lambda d: d,
        train_idx=np.arange(0, N // 2), test_idx=np.arange(N // 2, N),
        meta=dict(features=cols, target="target", group=None, time=None,
                  truth="test half drawn from a shifted subpopulation (mean +2.5, scale x2)"
                        if side == "contaminated" else "test half drawn from the same distribution"),
    )


CASES = dict(C1=c1, C2=c2, C3=c3, C4=c4, C5=c5, C6=c6, C7=c7, C8=c8)
SIDES = ("contaminated", "clean")

CASE_TYPE = dict(C1="T1", C2="T2", C3="T3", C4="T4", C5="T5", C6="T6", C7="T7", C8="T8")
CASE_ROW = dict(C1="L1.1", C2="L1.2", C3="L1.3", C4="L1.4a", C5="L2a", C6="L3.1",
                C7="L3.2", C8="L3.3")


def get(case, side):
    return CASES[case](side)
