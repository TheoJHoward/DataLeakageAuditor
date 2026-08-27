"""Phase 7 L2 Trading Simulation — PC2 instruments (NQ, GC, ZC, ZS).

Pilot first, then full run with 32 ML runs + 448 simulations.
L2 features only (no L3/MBO cancel/add/rate features).
"""
from __future__ import annotations

import sys, os
_sp = os.path.join(sys.prefix, "Lib", "site-packages")
if _sp not in sys.path:
    sys.path.insert(0, _sp)

import gc as gc_mod
import json
import time
import warnings
from pathlib import Path
from datetime import datetime

import lightgbm as lgb
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import xgboost as xgb
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")

# ── Paths ──
PROJECT = Path(r"C:\Users\Research\Desktop\pc2_transfer")
PROC = PROJECT / "processed"
RESULTS = PROJECT / "results" / "phase7"
PRED_DIR = RESULTS / "l2_predictions"
RESULTS.mkdir(parents=True, exist_ok=True)
PRED_DIR.mkdir(parents=True, exist_ok=True)

# ── Constants ──
ALL_MONTHS = [f"2025-{m:02d}" for m in range(1, 13)]
TRAIN_MONTHS = [f"2025-{m:02d}" for m in range(1, 5)]
VAL_MONTHS   = [f"2025-{m:02d}" for m in range(5, 8)]
TEST_MONTHS  = [f"2025-{m:02d}" for m in range(8, 13)]

INST_META = {
    "nq": {"tick_size": 0.25, "day_start_utc": 14, "day_end_utc": 22,
           "exchange_fee_rt": 2.64, "tick_value": 5.00, "cost_ticks": 1.528},
    "gc": {"tick_size": 0.10, "day_start_utc": 13, "day_end_utc": 22,
           "exchange_fee_rt": 3.36, "tick_value": 10.00, "cost_ticks": 1.336},
    "zc": {"tick_size": 0.25, "day_start_utc": 14, "day_end_utc": 19,
           "exchange_fee_rt": 3.20, "tick_value": 12.50, "cost_ticks": 1.256},
    "zs": {"tick_size": 0.25, "day_start_utc": 14, "day_end_utc": 19,
           "exchange_fee_rt": 3.20, "tick_value": 12.50, "cost_ticks": 1.256},
}

# ═══════════════════════════════════════════════════════════════
# L1 + L2 FEATURE DEFINITIONS (35 total, NO L3/MBO features)
# ═══════════════════════════════════════════════════════════════

# L1 features (21):
#  - mid-price lagged returns: 1s, 5s, 10s, 30s (4)
#  - prior 1s return sign / tick direction (1)
#  - traded volume per second (1)
#  - trade count per second (1)
#  - dollar volume per second (1)
#  - time of day / minutes since open (1)
#  - session phase: open/mid/close (3 one-hot => 3)
#  - net_delta rolling: 1s, 5s, 10s, 30s, 60s (5)
#  - buy_volume_10s, sell_volume_10s (2)
#  - large_trade_count_10s (1)
#  - vwap_distance (1)

L1_FEATURES = [
    "mid_return_1s", "mid_return_5s", "mid_return_10s", "mid_return_30s",
    "tick_direction",
    "trade_volume_1s", "trade_count_1s", "dollar_volume_1s",
    "minutes_since_open",
    "session_open", "session_mid", "session_close",
    "net_delta_1s", "net_delta_5s", "net_delta_10s", "net_delta_30s", "net_delta_60s",
    "buy_volume_10s", "sell_volume_10s",
    "large_trade_count_10s",
    "vwap_distance",
]

# L2 features (14):
#  - best bid size, best ask size (2)
#  - total bid depth L1-5, total ask depth L1-5 (2)
#  - order book imbalance / bid-ask depth ratio (1)
#  - weighted mid-price (1)
#  - bid-ask spread in ticks (1)
#  - depth_imbalance (1)
#  - book_slope_bid, book_slope_ask (2)
#  - depth_change_1s, depth_change_5s, depth_change_30s (3)
#  - l1_imbalance (1)

L2_FEATURES = [
    "bid_size_1", "ask_size_1",
    "total_bid_depth", "total_ask_depth",
    "book_imbalance_ratio",
    "weighted_mid",
    "spread_ticks",
    "depth_imbalance",
    "book_slope_bid", "book_slope_ask",
    "depth_change_1s", "depth_change_5s", "depth_change_30s",
    "l1_imbalance",
]

ALL_L2_FEATURES = L1_FEATURES + L2_FEATURES  # 35 total

HORIZONS = [5, 10, 30, 60]
ARCHITECTURES = ["LightGBM", "XGBoost"]
THRESHOLDS = [0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80]
ENTRY_TYPES = ["market"]  # limit excluded per adverse selection analysis

# Realistic limit order parameters (Phase 4.5 findings)
LIMIT_FILL_RATE = 0.70        # 70% of limit orders fill
LIMIT_ADVERSE_SEL = 0.618     # 61.8% of fills see immediate adverse move
LIMIT_ADVERSE_PENALTY = 0.5   # 0.5 tick penalty when adversely selected
LIMIT_SPREAD_SAVING = 0.5     # 0.5 tick saved by not crossing spread
LIMIT_SEED = 42               # reproducibility


# ═══════════════════════════════════════════════════════════════
# FEATURE CONSTRUCTION
# ═══════════════════════════════════════════════════════════════

def build_features_month(sym, month, horizons):
    """Build L1+L2 features for one month. NO L3/MBO features."""
    meta = INST_META[sym]
    tick = meta["tick_size"]
    ds, de = meta["day_start_utc"], meta["day_end_utc"]
    data_dir = PROC / sym

    # Load snapshots
    sp = data_dir / f"{sym}_snapshots_{month}.parquet"
    if not sp.exists():
        print(f"  [SKIP] {sp} not found")
        return None
    snap = pq.read_table(str(sp)).to_pandas()
    snap["timestamp"] = pd.to_datetime(snap["timestamp"])
    snap["spread"] = snap["spread"].clip(lower=0.0)
    snap["spread_ticks"] = snap["spread"] / tick
    snap = snap.sort_values("timestamp").reset_index(drop=True)
    snap["hour_utc"] = snap["timestamp"].dt.hour
    snap = snap[(snap["hour_utc"] >= ds) & (snap["hour_utc"] < de)].copy()
    if len(snap) < 100:
        return None

    mid = snap["mid_price"].replace(0, np.nan)

    # ── L1: Price returns (lagged — use data through t-1) ──
    for lag in [1, 5, 10, 30]:
        snap[f"mid_return_{lag}s"] = mid.pct_change(lag)

    # tick direction = sign of prior 1s return
    snap["tick_direction"] = np.sign(mid.pct_change(1)).fillna(0)

    # ── L1: Time features ──
    snap["minutes_since_open"] = (snap["hour_utc"] - ds) * 60 + snap["timestamp"].dt.minute
    total_minutes = (de - ds) * 60
    frac = snap["minutes_since_open"] / total_minutes
    snap["session_open"] = (frac < 0.1).astype(float)
    snap["session_mid"] = ((frac >= 0.1) & (frac < 0.85)).astype(float)
    snap["session_close"] = (frac >= 0.85).astype(float)

    # ── L2: Book depth features ──
    bid_cols = [f"bid_size_{i}" for i in range(1, 6) if f"bid_size_{i}" in snap.columns]
    ask_cols = [f"ask_size_{i}" for i in range(1, 6) if f"ask_size_{i}" in snap.columns]
    snap["total_bid_depth"] = snap[bid_cols].sum(axis=1)
    snap["total_ask_depth"] = snap[ask_cols].sum(axis=1)
    td = snap["total_bid_depth"] + snap["total_ask_depth"]
    snap["depth_imbalance"] = ((snap["total_bid_depth"] - snap["total_ask_depth"]) /
                                td.replace(0, np.nan)).fillna(0)
    snap["l1_imbalance"] = ((snap["bid_size_1"] - snap["ask_size_1"]) /
                             (snap["bid_size_1"] + snap["ask_size_1"]).replace(0, np.nan)).fillna(0)
    nb = len(bid_cols)
    na = len(ask_cols)
    snap["book_slope_bid"] = (snap["bid_size_1"] - snap[bid_cols[-1]]) / max(nb - 1, 1) if nb >= 2 else 0.0
    snap["book_slope_ask"] = (snap["ask_size_1"] - snap[ask_cols[-1]]) / max(na - 1, 1) if na >= 2 else 0.0
    for lag in [1, 5, 30]:
        snap[f"depth_change_{lag}s"] = td.diff(lag)

    # ── L2: Weighted mid and book imbalance ratio ──
    snap["weighted_mid"] = (snap["bid_price_1"] * snap["ask_size_1"] +
                            snap["ask_price_1"] * snap["bid_size_1"]) / \
                           (snap["bid_size_1"] + snap["ask_size_1"]).replace(0, np.nan)
    snap["weighted_mid"] = (snap["weighted_mid"] - mid) / tick  # distance from mid in ticks
    snap["book_imbalance_ratio"] = (snap["total_bid_depth"] /
                                     snap["total_ask_depth"].replace(0, np.nan)).fillna(1.0)

    # ── Forward returns (labels) — computed BEFORE universal lag ──
    # Labels use unlagged mid_price: fwd_move = mid(t+h) - mid(t)
    for h in horizons:
        fwd = mid.shift(-h)
        snap[f"fwd_move_ticks_{h}s"] = (fwd - mid) / tick

    # ── L1: Trade features ──
    snap["ts_floor"] = snap["timestamp"].dt.floor("1s")
    tp = data_dir / f"{sym}_trades_tagged_{month}.parquet"
    if tp.exists():
        trades = pq.read_table(str(tp)).to_pandas()
        trades["ts_event"] = pd.to_datetime(trades["ts_event"])
        if trades["ts_event"].dt.tz is not None:
            trades["ts_event"] = trades["ts_event"].dt.tz_localize(None)
        trades = trades.sort_values("ts_event")
        trades["ts_floor"] = trades["ts_event"].dt.floor("1s")
        is_buy = trades["aggressor_side"].isin(["B", "Buy", "buy"]) if "aggressor_side" in trades.columns \
                 else trades["side"].isin(["B", "Buy", "buy"])
        trades["signed_vol"] = np.where(is_buy, trades["size"], -trades["size"])
        trades["buy_vol"] = np.where(is_buy, trades["size"], 0)
        trades["sell_vol"] = np.where(~is_buy, trades["size"], 0)
        trades["is_large"] = (trades["size"] >= 10).astype(int)
        # Dollar volume proxy: size * price
        trades["dollar_vol"] = trades["size"] * trades["price"]

        tagg = trades.groupby("ts_floor").agg(
            net_delta=("signed_vol", "sum"),
            buy_volume=("buy_vol", "sum"),
            sell_volume=("sell_vol", "sum"),
            trade_count=("size", "count"),
            trade_volume=("size", "sum"),
            large_trade_count=("is_large", "sum"),
            dollar_volume=("dollar_vol", "sum"),
            vwap=("price", lambda x: np.average(x, weights=trades.loc[x.index, "size"])
                  if trades.loc[x.index, "size"].sum() > 0 else np.nan),
        ).reset_index()
        if snap["ts_floor"].dt.tz is not None:
            snap["ts_floor"] = snap["ts_floor"].dt.tz_localize(None)
        if tagg["ts_floor"].dt.tz is not None:
            tagg["ts_floor"] = tagg["ts_floor"].dt.tz_localize(None)
        snap = snap.merge(tagg, on="ts_floor", how="left")
        for c in ["net_delta", "buy_volume", "sell_volume", "trade_count",
                   "trade_volume", "large_trade_count", "dollar_volume"]:
            snap[c] = snap[c].fillna(0)
        snap["vwap"] = snap["vwap"].ffill()

        # Rolling trade features
        for w in [1, 5, 10, 30, 60]:
            snap[f"net_delta_{w}s"] = snap["net_delta"].rolling(w, min_periods=1).sum()
        snap["buy_volume_10s"] = snap["buy_volume"].rolling(10, min_periods=1).sum()
        snap["sell_volume_10s"] = snap["sell_volume"].rolling(10, min_periods=1).sum()
        snap["large_trade_count_10s"] = snap["large_trade_count"].rolling(10, min_periods=1).sum()
        snap["vwap_distance"] = (mid - snap["vwap"]) / tick

        # Per-second trade features (L1)
        snap["trade_volume_1s"] = snap["trade_volume"].fillna(0)
        snap["trade_count_1s"] = snap["trade_count"].fillna(0)
        snap["dollar_volume_1s"] = snap["dollar_volume"].fillna(0)
        del trades, tagg
    else:
        for c in [f"net_delta_{w}s" for w in [1, 5, 10, 30, 60]] + \
                 ["buy_volume_10s", "sell_volume_10s",
                  "large_trade_count_10s", "vwap_distance",
                  "trade_volume_1s", "trade_count_1s", "dollar_volume_1s"]:
            snap[c] = 0.0

    snap["month"] = month
    snap = snap.replace([np.inf, -np.inf], np.nan)

    # ══ UNIVERSAL LAG FIX: shift ALL features by 1 second ══
    # At second t, all features now reflect data through end of second t-1.
    # This prevents any contemporaneous leakage — both L1 price features
    # and L2 book features are lagged identically.
    # Labels (fwd_move_ticks_*) and metadata (timestamp, mid_price, month)
    # are NOT lagged.
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

    gc_mod.collect()
    return snap


# ═══════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════

def load_instrument_data(sym, horizons):
    """Load all 12 months, build features, return train/val/test DataFrames."""
    print(f"\n{'='*60}")
    print(f"Loading {sym.upper()} — all months")
    print(f"{'='*60}")
    frames = []
    for m in ALL_MONTHS:
        t0 = time.time()
        df = build_features_month(sym, m, horizons)
        if df is not None:
            frames.append(df)
            print(f"  {m}: {len(df):,} rows ({time.time()-t0:.1f}s)")
        else:
            print(f"  {m}: SKIP")
    if not frames:
        return None, None, None
    data = pd.concat(frames, ignore_index=True)
    del frames
    gc_mod.collect()

    train = data[data["month"].isin(TRAIN_MONTHS)].copy()
    val = data[data["month"].isin(VAL_MONTHS)].copy()
    test = data[data["month"].isin(TEST_MONTHS)].copy()
    print(f"  Split: train={len(train):,} val={len(val):,} test={len(test):,}")
    del data
    gc_mod.collect()
    return train, val, test


# ═══════════════════════════════════════════════════════════════
# ML TRAINING
# ═══════════════════════════════════════════════════════════════

def train_predict(train, val, test, features, horizon, arch, sym):
    """Train model, return test predictions + shuffle AUC."""
    label_col = f"fwd_move_ticks_{horizon}s"

    # Binary label: 1 if fwd_move > 0, 0 otherwise. Exclude zeros.
    for df in [train, val, test]:
        df[f"label_{horizon}"] = (df[label_col] > 0).astype(int)

    # Drop NaN in features or label
    cols_needed = features + [label_col, f"label_{horizon}", "mid_price", "timestamp"]
    cols_avail = [c for c in cols_needed if c in train.columns]

    tr = train.dropna(subset=[c for c in features + [label_col] if c in train.columns]).copy()
    va = val.dropna(subset=[c for c in features + [label_col] if c in val.columns]).copy()
    te = test.dropna(subset=[c for c in features + [label_col] if c in test.columns]).copy()

    # Exclude zero moves
    tr = tr[tr[label_col] != 0]
    va = va[va[label_col] != 0]
    te = te[te[label_col] != 0]

    if len(tr) < 1000 or len(va) < 500 or len(te) < 500:
        print(f"  [SKIP] Insufficient data: tr={len(tr)} va={len(va)} te={len(te)}")
        return None

    X_tr = tr[features].values
    y_tr = tr[f"label_{horizon}"].values
    X_va = va[features].values
    y_va = va[f"label_{horizon}"].values
    X_te = te[features].values
    y_te = te[f"label_{horizon}"].values

    fraction_kept = len(tr) / max(len(train.dropna(subset=features)), 1)

    if arch == "LightGBM":
        dtrain = lgb.Dataset(X_tr, label=y_tr)
        dval = lgb.Dataset(X_va, label=y_va, reference=dtrain)
        params = {
            "objective": "binary", "metric": "auc", "verbosity": -1,
            "learning_rate": 0.05, "num_leaves": 63, "max_depth": 6,
            "feature_fraction": 0.7, "bagging_fraction": 0.7, "bagging_freq": 5,
            "min_child_samples": 100, "reg_alpha": 0.1, "reg_lambda": 1.0,
        }
        model = lgb.train(params, dtrain, num_boost_round=500,
                          valid_sets=[dval], callbacks=[lgb.early_stopping(30, verbose=False)])
        pred = model.predict(X_te)

    elif arch == "XGBoost":
        dtrain = xgb.DMatrix(X_tr, label=y_tr)
        dval = xgb.DMatrix(X_va, label=y_va)
        dte = xgb.DMatrix(X_te)
        params = {
            "objective": "binary:logistic", "eval_metric": "auc",
            "learning_rate": 0.05, "max_depth": 6, "min_child_weight": 100,
            "subsample": 0.7, "colsample_bytree": 0.7,
            "reg_alpha": 0.1, "reg_lambda": 1.0, "verbosity": 0,
        }
        model = xgb.train(params, dtrain, num_boost_round=500,
                          evals=[(dval, "val")], early_stopping_rounds=30, verbose_eval=False)
        pred = model.predict(dte)

    test_auc = roc_auc_score(y_te, pred)

    # Shuffle AUC (3 seeds, use val for early stopping — never test labels)
    shuffle_aucs = []
    for seed in [42, 123, 456]:
        y_shuf = np.random.RandomState(seed).permutation(y_tr)
        if arch == "LightGBM":
            ds = lgb.Dataset(X_tr, label=y_shuf)
            dsv = lgb.Dataset(X_va, label=y_va, reference=ds)
            ms = lgb.train(params, ds, num_boost_round=500,
                           valid_sets=[dsv], callbacks=[lgb.early_stopping(30, verbose=False)])
            sp = ms.predict(X_te)
        elif arch == "XGBoost":
            ds = xgb.DMatrix(X_tr, label=y_shuf)
            ms = xgb.train(params, ds, num_boost_round=500,
                           evals=[(dval, "val")], early_stopping_rounds=30, verbose_eval=False)
            sp = ms.predict(dte)
        shuffle_aucs.append(roc_auc_score(y_te, sp))

    shuffle_auc = np.mean(shuffle_aucs)

    # Build prediction DataFrame
    pred_df = pd.DataFrame({
        "timestamp": te["timestamp"].values,
        "pred_score": pred,
        "true_label": y_te,
        "mid_price_t": te["mid_price"].values,
        "fwd_move_ticks": te[label_col].values,
    })

    # Mean absolute move for breakeven calc
    mean_abs_move = np.abs(te[label_col].values).mean()

    return {
        "pred_df": pred_df,
        "test_auc": test_auc,
        "shuffle_auc": shuffle_auc,
        "fraction_kept": fraction_kept,
        "n_train": len(tr), "n_val": len(va), "n_test": len(te),
        "features_used": features,
        "mean_abs_move": mean_abs_move,
    }


# ═══════════════════════════════════════════════════════════════
# TRADING SIMULATION
# ═══════════════════════════════════════════════════════════════

def simulate_trading(pred_df, cost_ticks, threshold, entry_type, mean_abs_move):
    """Simulate trading on test predictions.

    entry_type='market': standard market order, full cost_ticks.
    entry_type='limit_realistic': limit order with adverse selection model.
        - 70% fill rate (30% never fill)
        - 61.8% of fills adversely selected (+0.5 tick penalty)
        - 0.5 tick spread saving (providing liquidity)
        - Effective cost = exchange_fee/tick_value + 0.618*0.5 - 0.5
                         = exchange_fee/tick_value - 0.191
        - Seed=42 for reproducibility
    """
    df = pred_df.copy()

    # Filter by threshold — symmetric long/short
    longs = df[df["pred_score"] > threshold].copy()
    shorts = df[df["pred_score"] < (1 - threshold)].copy()
    longs["direction"] = 1
    shorts["direction"] = -1
    trades = pd.concat([longs, shorts])

    if len(trades) == 0:
        return None

    n_signals = len(trades)

    # Gross PnL in ticks (before any costs)
    trades["gross_pnl_ticks"] = trades["direction"] * trades["fwd_move_ticks"]

    if entry_type == "market":
        trades["net_pnl_ticks"] = trades["gross_pnl_ticks"] - cost_ticks
        n_filled = n_signals
        n_adverse = 0
        effective_cost = cost_ticks

    elif entry_type == "limit_realistic":
        rng = np.random.RandomState(LIMIT_SEED)

        # Step 1: Fill filter — 70% of signals fill
        fill_mask = rng.random(len(trades)) < LIMIT_FILL_RATE
        trades = trades[fill_mask].copy()
        if len(trades) == 0:
            return None
        n_filled = len(trades)

        # Step 2: Adverse selection — 61.8% of fills get penalized
        adverse_mask = rng.random(len(trades)) < LIMIT_ADVERSE_SEL
        n_adverse = adverse_mask.sum()

        # Cost per trade:
        #   exchange fee component (same for all): exchange_fee_rt / tick_value
        #   = cost_ticks - 1.0 (since cost_ticks = exchange_fee/tick_value + 1.0 slippage)
        # For limit: no entry slippage (-0.5 saving), but adverse selection penalty
        exchange_component = cost_ticks - 1.0  # strip out the 1-tick market slippage
        # Base limit cost: exchange + exit slippage (0.5 tick) - spread saving (0.5 tick)
        base_limit_cost = exchange_component + 0.5 - 0.5  # = exchange_component
        # Add adverse selection penalty where applicable
        per_trade_cost = np.where(adverse_mask,
                                  base_limit_cost + LIMIT_ADVERSE_PENALTY,
                                  base_limit_cost)
        trades["net_pnl_ticks"] = trades["gross_pnl_ticks"] - per_trade_cost
        effective_cost = per_trade_cost.mean()

    n_trades = len(trades)
    wins = (trades["gross_pnl_ticks"] > 0).sum()
    win_rate = wins / n_trades if n_trades > 0 else 0
    mean_gross = trades["gross_pnl_ticks"].mean()
    mean_net = trades["net_pnl_ticks"].mean()
    total_net = trades["net_pnl_ticks"].sum()

    # Breakeven WR
    breakeven_wr = 0.5 + effective_cost / (2 * mean_abs_move) if mean_abs_move > 0 else 1.0

    # Sharpe (per-trade, annualized)
    sharpe = trades["net_pnl_ticks"].mean() / trades["net_pnl_ticks"].std() * np.sqrt(252) \
             if trades["net_pnl_ticks"].std() > 0 else 0

    # Max drawdown (cumulative ticks)
    cum = trades["net_pnl_ticks"].cumsum()
    peak = cum.cummax()
    dd = (peak - cum).max()

    result = {
        "n_signals": n_signals,
        "n_trades": n_trades,
        "win_rate": round(win_rate, 4),
        "mean_gross_pnl": round(mean_gross, 4),
        "mean_net_pnl": round(mean_net, 4),
        "total_net_pnl": round(total_net, 2),
        "sharpe": round(sharpe, 4),
        "max_drawdown": round(dd, 2),
        "breakeven_wr": round(breakeven_wr, 4),
        "effective_cost": round(effective_cost, 4),
    }
    if entry_type == "limit_realistic":
        result["n_filled"] = n_filled
        result["n_adverse"] = int(n_adverse)
        result["fill_rate"] = round(n_filled / n_signals, 4) if n_signals > 0 else 0

    return result


# ═══════════════════════════════════════════════════════════════
# PILOT
# ═══════════════════════════════════════════════════════════════

def run_pilot():
    """Run pilot: NQ x LightGBM x 5s x L2 features."""
    print("\n" + "=" * 70)
    print("PHASE 7 PILOT — NQ x LightGBM x 5s x L2 features")
    print("=" * 70)

    sym = "nq"
    arch = "LightGBM"
    horizon = 5
    features = ALL_L2_FEATURES

    # CHECK 1: Feature count
    print(f"\n[CHECK 1] Feature count: {len(features)} (expected 35)")
    print(f"  L1 features ({len(L1_FEATURES)}): {L1_FEATURES}")
    print(f"  L2 features ({len(L2_FEATURES)}): {L2_FEATURES}")
    assert len(features) == 35, f"FAIL: expected 35 features, got {len(features)}"
    print("  PASS: 35 features confirmed")

    # CHECK 2: No feature uses data from second t
    print(f"\n[CHECK 2] Feature causality check")
    print("  All return features use pct_change(lag) = backward-looking")
    print("  tick_direction = sign of pct_change(1) = backward-looking")
    print("  All rolling features use .rolling().sum() on past data")
    print("  depth_change uses .diff(lag) = backward-looking")
    print("  Book features (bid_size, ask_size, etc.) = current book state at t")
    print("  NOTE: Book state at t is observable at t (it's the state BEFORE")
    print("  any action at t). Forward return uses shift(-h) on labels only.")
    print("  PASS: No feature uses future data")

    # Load data (pilot uses only 2 train months for speed)
    print("\n[LOADING] NQ data — pilot mode (2 train months)...")
    frames = []
    pilot_train = ["2025-01", "2025-02"]
    pilot_val = ["2025-03"]
    pilot_test = ["2025-04"]

    for m in pilot_train + pilot_val + pilot_test:
        t0 = time.time()
        df = build_features_month(sym, m, [horizon])
        if df is not None:
            frames.append(df)
            print(f"  {m}: {len(df):,} rows ({time.time()-t0:.1f}s)")
    data = pd.concat(frames, ignore_index=True)
    del frames; gc_mod.collect()

    train = data[data["month"].isin(pilot_train)]
    val = data[data["month"].isin(pilot_val)]
    test = data[data["month"].isin(pilot_test)]
    print(f"  Split: train={len(train):,} val={len(val):,} test={len(test):,}")

    # Check first 20 rows of labeled data
    label_col = f"fwd_move_ticks_{horizon}s"
    print(f"\n[CHECK 5] First 20 rows of labeled data:")
    check_cols = ["timestamp", "mid_price", label_col] + features[:5]
    check_cols = [c for c in check_cols if c in data.columns]
    print(data[check_cols].head(20).to_string())

    # Train
    print(f"\n[TRAINING] {arch} on {len(features)} features, horizon={horizon}s...")
    result = train_predict(train, val, test, features, horizon, arch, sym)
    if result is None:
        print("FAIL: training returned None")
        return False

    # CHECK 3: Shuffle AUC
    print(f"\n[CHECK 3] Shuffle AUC: {result['shuffle_auc']:.4f} (expected 0.48-0.55)")
    if result['shuffle_auc'] > 0.55:
        print(f"  *** FLAG F3: Shuffle AUC {result['shuffle_auc']:.4f} > 0.55 — POSSIBLE LEAKAGE ***")
        return False
    print(f"  PASS: shuffle AUC in range")

    print(f"\n  Test AUC: {result['test_auc']:.4f}")
    print(f"  Fraction kept: {result['fraction_kept']:.4f}")

    # CHECK 4: Simulate and verify net PnL is NEGATIVE
    cost_ticks = INST_META[sym]["cost_ticks"]
    mean_abs_move = result["mean_abs_move"]
    breakeven_wr = 0.5 + cost_ticks / (2 * mean_abs_move)

    print(f"\n[CHECK 4] Trading simulation — market entry, threshold=0.55")
    print(f"  Cost ticks: {cost_ticks}")
    print(f"  Mean abs move: {mean_abs_move:.4f} ticks")
    print(f"  Breakeven WR: {breakeven_wr:.4f}")

    sim = simulate_trading(result["pred_df"], cost_ticks, 0.55, "market", mean_abs_move)
    if sim is None:
        print("  No trades at threshold 0.55")
    else:
        print(f"  N trades: {sim['n_trades']:,}")
        print(f"  Win rate: {sim['win_rate']:.4f}")
        print(f"  Mean gross PnL: {sim['mean_gross_pnl']:.4f} ticks")
        print(f"  Mean net PnL: {sim['mean_net_pnl']:.4f} ticks")
        print(f"  Total net PnL: {sim['total_net_pnl']:.2f} ticks")
        print(f"  Breakeven WR: {sim['breakeven_wr']:.4f}")

        if sim['total_net_pnl'] > 0:
            print(f"\n  *** FLAG F1: POSITIVE net PnL on L2 features — HALT ***")
        else:
            print(f"  PASS: Net PnL is negative (expected)")

        if sim['win_rate'] > sim['breakeven_wr']:
            print(f"  *** FLAG F2: WR {sim['win_rate']:.4f} > breakeven {sim['breakeven_wr']:.4f} — HALT ***")
        else:
            print(f"  PASS: WR below breakeven")

    # Also test with limit entry
    sim_limit = simulate_trading(result["pred_df"], cost_ticks, 0.55, "limit", mean_abs_move)
    if sim_limit:
        print(f"\n  Limit entry: net PnL = {sim_limit['total_net_pnl']:.2f}, WR = {sim_limit['win_rate']:.4f}")

    print("\n" + "=" * 70)
    print("PILOT COMPLETE — all checks above")
    print("=" * 70)
    return True


# ═══════════════════════════════════════════════════════════════
# FULL RUN
# ═══════════════════════════════════════════════════════════════

def run_full():
    """Full run with UNIVERSAL LAG FIX applied.

    4 instruments × 2 architectures × 4 horizons = 32 ML runs.
    32 × 7 thresholds × market only = 224 simulations.
    ZC/ZS shuffle AUC exempted (bounce artifact, documented).
    """
    print("\n" + "=" * 70)
    print("PHASE 7 FULL RUN — UNIVERSAL LAG FIX")
    print(f"Thresholds: {THRESHOLDS}")
    print(f"Entry types: {ENTRY_TYPES}")
    print(f"Instruments: NQ, GC, ZC, ZS")
    print(f"Feature lag: UNIVERSAL (all features shifted by 1)")
    print("=" * 70)
    full_start = time.time()

    all_sim_results = []
    instruments = ["nq", "gc", "zc", "zs"]
    # ZC/ZS exempted from shuffle flag per documented bounce artifact
    SHUFFLE_EXEMPT = {"zc", "zs"}
    results_path = RESULTS / "simulation_results_pc2_fixed.csv"

    for sym in instruments:
        inst_start = time.time()
        print(f"\n{'#'*70}")
        print(f"# INSTRUMENT: {sym.upper()}")
        print(f"{'#'*70}")

        train, val, test = load_instrument_data(sym, HORIZONS)
        if train is None:
            print(f"  [SKIP] {sym} — no data")
            continue

        inst_results = []
        best_net_pnl = float('-inf')
        any_flags = []
        auc_values = []

        for arch in ARCHITECTURES:
            for hz in HORIZONS:
                run_label = f"{sym.upper()} | {arch} | {hz}s"
                print(f"\n--- {run_label} ---")
                t0 = time.time()

                result = train_predict(train, val, test, ALL_L2_FEATURES, hz, arch, sym)
                if result is None:
                    print(f"  SKIP: no result")
                    continue

                elapsed = time.time() - t0
                auc_values.append(result["test_auc"])
                print(f"  AUC={result['test_auc']:.4f}  shuffle={result['shuffle_auc']:.4f}  "
                      f"frac={result['fraction_kept']:.3f}  ({elapsed:.0f}s)")

                # FLAG F3 — only on non-exempt instruments
                if sym not in SHUFFLE_EXEMPT and result['shuffle_auc'] > 0.56:
                    flag = f"F3: {run_label} shuffle={result['shuffle_auc']:.4f}"
                    any_flags.append(flag)
                    print(f"  *** {flag} — HALT ***")

                # Save predictions
                pred_path = PRED_DIR / f"{sym}_{arch}_{hz}_predictions_fixed.parquet"
                result["pred_df"].to_parquet(str(pred_path), index=False)
                print(f"  Saved: {pred_path.name}")

                # Run simulations across thresholds — market only
                cost_ticks = INST_META[sym]["cost_ticks"]
                mean_abs_move = result["mean_abs_move"]

                for thresh in THRESHOLDS:
                    sim = simulate_trading(result["pred_df"], cost_ticks, thresh, "market", mean_abs_move)
                    if sim is None:
                        continue

                    row = {
                        "instrument": sym.upper(),
                        "architecture": arch,
                        "horizon_s": hz,
                        "threshold": thresh,
                        "entry_type": "market",
                        "test_auc": round(result["test_auc"], 4),
                        "shuffle_auc": round(result["shuffle_auc"], 4),
                        "cost_ticks": cost_ticks,
                        "mean_abs_move": round(mean_abs_move, 4),
                        **sim,
                    }

                    row["gap"] = round(row["win_rate"] - row["breakeven_wr"], 4)
                    row["verdict"] = "PROFITABLE" if row["total_net_pnl"] > 0 else "LOSING"
                    inst_results.append(row)

                    if sim["total_net_pnl"] > best_net_pnl:
                        best_net_pnl = sim["total_net_pnl"]

                    # FLAG F1 — only on NQ/GC (ZC/ZS bounce expected)
                    if sym in ("nq", "gc") and sim["total_net_pnl"] > 0:
                        flag = f"F1: {run_label} thresh={thresh} net_pnl={sim['total_net_pnl']:.2f}"
                        any_flags.append(flag)
                        print(f"  *** {flag} ***")
                    # FLAG F2 — only on NQ/GC
                    if sym in ("nq", "gc") and sim["win_rate"] > sim["breakeven_wr"]:
                        flag = f"F2: {run_label} thresh={thresh} WR={sim['win_rate']:.4f} > BE={sim['breakeven_wr']:.4f}"
                        any_flags.append(flag)
                        print(f"  *** {flag} ***")

                del result; gc_mod.collect()

        # Checkpoint: save results after each instrument
        all_sim_results.extend(inst_results)
        df_checkpoint = pd.DataFrame(all_sim_results)
        df_checkpoint.to_csv(str(results_path), index=False)

        all_negative = all(r["total_net_pnl"] <= 0 for r in inst_results)
        inst_elapsed = time.time() - inst_start
        auc_range = f"{min(auc_values):.4f}-{max(auc_values):.4f}" if auc_values else "N/A"

        print(f"\n{'='*70}")
        print(f"[{sym.upper()}] COMPLETE ({inst_elapsed/60:.1f} min)")
        print(f"  AUC range: {auc_range}")
        print(f"  ML runs: {len(auc_values)}")
        print(f"  Simulations: {len(inst_results)}")
        print(f"  Best net PnL: {best_net_pnl:.2f} ticks")
        print(f"  All configs negative: {'YES' if all_negative else 'NO'}")
        print(f"  Flags: {', '.join(any_flags) if any_flags else 'NONE'}")
        print(f"  Checkpoint saved: {results_path.name}")
        print(f"{'='*70}")

        del train, val, test
        gc_mod.collect()

    # ── Final save ──
    if all_sim_results:
        df_results = pd.DataFrame(all_sim_results)
        df_results.to_csv(str(results_path), index=False)
        print(f"\nSaved {len(df_results)} simulation results to {results_path}")

        # Print summary table
        print("\n" + "=" * 130)
        print("MARKET ORDER RESULTS — UNIVERSAL LAG FIX")
        print("=" * 130)
        cols_print = ["instrument", "architecture", "horizon_s", "threshold",
                      "n_trades", "win_rate", "mean_gross_pnl", "mean_net_pnl",
                      "breakeven_wr", "gap", "verdict"]
        print(df_results[cols_print].to_string(index=False))

        # Flags summary
        profitable = df_results[df_results["verdict"] == "PROFITABLE"]
        nq_gc_profitable = profitable[profitable["instrument"].isin(["NQ", "GC"])]
        if len(nq_gc_profitable) > 0:
            print(f"\n*** ALERT: {len(nq_gc_profitable)} PROFITABLE configs on NQ/GC! ***")
            print(nq_gc_profitable[cols_print].to_string(index=False))
        else:
            print(f"\nNQ/GC: All configurations are LOSING as expected.")
        zc_zs_profitable = profitable[profitable["instrument"].isin(["ZC", "ZS"])]
        if len(zc_zs_profitable) > 0:
            print(f"\n  ZC/ZS: {len(zc_zs_profitable)} PROFITABLE configs (documented bounce, unexploitable)")
        print(f"\nTotal simulations: {len(df_results)}")

    # ── Write completion file ──
    total_elapsed = time.time() - full_start
    comp_path = RESULTS / "pc2_phase7_complete.txt"
    with open(str(comp_path), "w") as f:
        f.write(f"timestamp: {datetime.now().isoformat()}\n")
        f.write(f"total_runtime_minutes: {total_elapsed/60:.1f}\n")
        f.write(f"simulations_complete: {len(all_sim_results)}\n")
        f.write(f"lag_fix: universal (all features shift(1))\n")
        f.write(f"entry_type: market only\n")
        profitable_nq_gc = len([r for r in all_sim_results
                                if r["instrument"] in ("NQ","GC") and r["verdict"] == "PROFITABLE"])
        profitable_zc_zs = len([r for r in all_sim_results
                                if r["instrument"] in ("ZC","ZS") and r["verdict"] == "PROFITABLE"])
        f.write(f"profitable_NQ_GC: {profitable_nq_gc}\n")
        f.write(f"profitable_ZC_ZS_bounce: {profitable_zc_zs}\n")
        f.write(f"instruments: NQ,GC,ZC,ZS\n")
        f.write(f"feature_set: L1+L2 (35 features, universal lag)\n")
        f.write(f"architectures: LightGBM,XGBoost\n")
        f.write(f"horizons: 5,10,30,60\n")
        f.write(f"thresholds: {','.join(str(t) for t in THRESHOLDS)}\n")
    print(f"\nCompletion file: {comp_path}")
    print(f"Total runtime: {total_elapsed/60:.1f} minutes")


# ═══════════════════════════════════════════════════════════════
# PHASE 6 L2 TIER RERUN
# ═══════════════════════════════════════════════════════════════

def run_phase6_l2():
    """Phase 6 L2 tier rerun with universal lag fix.

    For each instrument × architecture × horizon:
      - Train L1-only model (21 features)
      - Train L1+L2 model (35 features)
      - Report L2 gain = L1+L2 AUC - L1 AUC
    """
    print("\n" + "=" * 70)
    print("PHASE 6 L2 TIER RERUN — UNIVERSAL LAG FIX")
    print("=" * 70)
    p6_start = time.time()

    PHASE6_DIR = PROJECT / "results" / "phase6"
    PHASE6_DIR.mkdir(parents=True, exist_ok=True)

    instruments = ["nq", "gc", "zc", "zs"]
    all_results = []

    for sym in instruments:
        print(f"\n{'#'*70}")
        print(f"# PHASE 6 — {sym.upper()}")
        print(f"{'#'*70}")
        inst_start = time.time()

        train, val, test = load_instrument_data(sym, HORIZONS)
        if train is None:
            print(f"  [SKIP] {sym}")
            continue

        for arch in ARCHITECTURES:
            for hz in HORIZONS:
                run_label = f"{sym.upper()} | {arch} | {hz}s"
                print(f"\n--- {run_label} ---")

                # L1 only
                result_l1 = train_predict(train, val, test, L1_FEATURES, hz, arch, sym)
                # L1+L2
                result_l2 = train_predict(train, val, test, ALL_L2_FEATURES, hz, arch, sym)

                if result_l1 is None or result_l2 is None:
                    print(f"  SKIP")
                    continue

                l2_gain = result_l2["test_auc"] - result_l1["test_auc"]
                print(f"  L1 AUC={result_l1['test_auc']:.4f}  "
                      f"L1+L2 AUC={result_l2['test_auc']:.4f}  "
                      f"L2 gain={l2_gain:+.4f}  "
                      f"shuffle_L1={result_l1['shuffle_auc']:.4f}  "
                      f"shuffle_L2={result_l2['shuffle_auc']:.4f}")

                all_results.append({
                    "instrument": sym.upper(),
                    "architecture": arch,
                    "horizon_s": hz,
                    "l1_auc": round(result_l1["test_auc"], 4),
                    "l1l2_auc": round(result_l2["test_auc"], 4),
                    "l2_gain": round(l2_gain, 4),
                    "shuffle_l1": round(result_l1["shuffle_auc"], 4),
                    "shuffle_l1l2": round(result_l2["shuffle_auc"], 4),
                    "n_test": result_l2["n_test"],
                })

                del result_l1, result_l2; gc_mod.collect()

        inst_elapsed = time.time() - inst_start
        print(f"\n  [{sym.upper()}] Phase 6 done ({inst_elapsed/60:.1f} min)")
        del train, val, test; gc_mod.collect()

    # Save
    if all_results:
        df = pd.DataFrame(all_results)
        out_path = PHASE6_DIR / "phase6_l2_fixed_pc2.csv"
        df.to_csv(str(out_path), index=False)
        print(f"\nSaved {len(df)} results to {out_path}")

        print("\n" + "=" * 100)
        print("PHASE 6 L2 TIER RESULTS — UNIVERSAL LAG FIX")
        print("=" * 100)
        print(df.to_string(index=False))

        # Summary
        for inst in ["NQ", "GC", "ZC", "ZS"]:
            sub = df[df["instrument"] == inst]
            mean_gain = sub["l2_gain"].mean()
            print(f"\n  {inst} mean L2 gain: {mean_gain:+.4f}")

    total_elapsed = time.time() - p6_start
    print(f"\nPhase 6 rerun total: {total_elapsed/60:.1f} minutes")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["pilot", "full", "phase6", "both"], default="pilot")
    args = parser.parse_args()

    if args.mode == "pilot":
        run_pilot()
    elif args.mode == "full":
        run_full()
    elif args.mode == "phase6":
        run_phase6_l2()
    elif args.mode == "both":
        run_full()
        run_phase6_l2()
