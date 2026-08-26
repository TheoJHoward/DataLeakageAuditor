# Phase 5 multi-architecture ML evaluation (5 architectures x 8 instruments) — last confirmed working 2026-04-05
"""Phase 5: Multi-Architecture ML Evaluation — All 8 Instruments."""
from __future__ import annotations

import sys, os
_sp = os.path.join(sys.prefix, "Lib", "site-packages")
if _sp not in sys.path:
    sys.path.insert(0, _sp)

import gc as gc_mod
import json
import time
import traceback
import warnings
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import xgboost as xgb
from scipy import stats as scipy_stats
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8")

# ── Deep learning imports (PyTorch) ──
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ── Paths ──
# [F2 FIXTURE EDIT] PROJECT/PROC unchanged in value (reads from archive processed\ are allowed);
# ALL write targets redirected to the f2 scratchpad so nothing can land in the archive.
PROJECT = Path(r"C:\Users\ttbea\OneDrive\Desktop\MBO_2025")   # unchanged (read-only source)
PROC = PROJECT / "processed"                                   # unchanged (read-only source)
LOCAL_DATA = Path(r"C:\MBO_data")                              # unchanged (does not exist; get_data_dir falls back to PROC)
_F2_SCRATCH = Path(__file__).resolve().parent                  # [F2 FIXTURE EDIT] added
RESULTS = _F2_SCRATCH / "results_phase5"                       # [F2 FIXTURE EDIT] was: PROJECT / "results" / "phase5"
RESULTS.mkdir(parents=True, exist_ok=True)                     # unchanged line, but now creates dir under f2 scratchpad, not archive

ALL_MONTHS = [f"2025-{m:02d}" for m in range(1, 13)]
TRAIN_MONTHS = [f"2025-{m:02d}" for m in range(1, 5)]
VAL_MONTHS   = [f"2025-{m:02d}" for m in range(5, 8)]
TEST_MONTHS  = [f"2025-{m:02d}" for m in range(8, 13)]

INST_META = {
    "es": {"tick_size": 0.25, "matching": "FIFO", "day_start_utc": 14, "day_end_utc": 22, "ct_ratio": 3.26},
    "nq": {"tick_size": 0.25, "matching": "FIFO", "day_start_utc": 14, "day_end_utc": 22, "ct_ratio": 7.84},
    "gc": {"tick_size": 0.10, "matching": "FIFO", "day_start_utc": 13, "day_end_utc": 22, "ct_ratio": 4.64},
    "cl": {"tick_size": 0.01, "matching": "FIFO", "day_start_utc": 13, "day_end_utc": 22, "ct_ratio": 4.14},
    "zs": {"tick_size": 0.25, "matching": "ProRata", "day_start_utc": 14, "day_end_utc": 19, "ct_ratio": 2.48},
    "zc": {"tick_size": 0.25, "matching": "ProRata", "day_start_utc": 14, "day_end_utc": 19, "ct_ratio": 1.53},
    "le": {"tick_size": 0.025, "matching": "ProRata", "day_start_utc": 14, "day_end_utc": 19, "ct_ratio": 2.54},
    "he": {"tick_size": 0.025, "matching": "ProRata", "day_start_utc": 14, "day_end_utc": 19, "ct_ratio": 2.02},
}

FULL_FEATURES = [
    "spread_ticks", "mid_return_1s", "mid_return_5s", "mid_return_10s",
    "mid_return_30s", "mid_return_60s", "mid_return_300s",
    "bid_size_1", "ask_size_1", "l1_imbalance",
    "volatility_30s", "volatility_300s", "range_60s", "range_300s",
    "minutes_since_open",
    "total_bid_depth", "total_ask_depth", "depth_imbalance",
    "book_slope_bid", "book_slope_ask",
    "depth_change_1s", "depth_change_5s", "depth_change_30s",
    "depth_pctile_60s", "depth_pctile_300s",
    "net_delta_1s", "net_delta_5s", "net_delta_10s",
    "net_delta_30s", "net_delta_60s",
    "buy_volume_10s", "sell_volume_10s",
    "trade_count_10s", "large_trade_count_10s",
    "vwap_distance",
    "bid_add_rate_5s", "ask_add_rate_5s",
    "bid_cancel_rate_5s", "ask_cancel_rate_5s",
    "bid_add_rate_10s", "ask_add_rate_10s",
    "bid_cancel_rate_10s", "ask_cancel_rate_10s",
    "cancel_ratio_asymmetry", "order_flow_accel",
]

PRICE_LAG_FEATURES = [
    "mid_return_1s", "mid_return_5s", "mid_return_10s",
    "mid_return_30s", "mid_return_60s", "mid_return_300s",
    "volatility_30s", "volatility_300s", "range_60s", "range_300s",
]

BOUNCE_FREE_FEATURES = [f for f in FULL_FEATURES if f not in PRICE_LAG_FEATURES]

HORIZONS = [5, 10, 30, 60]
ARCHITECTURES = ["XGBoost", "LogReg", "LSTM", "CNN", "Transformer"]
FEATURE_SETS = {"Full": FULL_FEATURES, "BFree": BOUNCE_FREE_FEATURES}

SEQ_LEN = 10  # Sequence length for deep learning models
N_SHUFFLE = 3  # Reduced from 5 to save time on DL models

# ── Counters ──
total_runs = 8 * len(ARCHITECTURES) * len(HORIZONS) * len(FEATURE_SETS)
completed_runs = 0
run_times = []
phase5_start = time.time()


def get_data_dir(sym):
    local = LOCAL_DATA / sym
    return local if local.exists() else PROC / sym


def load_mbo_aggregated(sym, month):
    agg_path = LOCAL_DATA / f"{sym}_mbo_agg" / f"{sym}_mbo_agg_{month}.parquet"
    if agg_path.exists():
        r = pq.read_table(str(agg_path)).to_pandas()
        r["ts_floor"] = pd.to_datetime(r["ts_floor"])
        return r
    path = get_data_dir(sym) / f"{sym}_mbo_{month}.parquet"
    if not path.exists():
        return None
    try:
        pf = pq.ParquetFile(str(path))
        n_rows = pf.metadata.num_rows
    except Exception:
        return None
    if n_rows > 50_000_000:
        all_ts, all_ba, all_aa, all_bc, all_ac = [], [], [], [], []
        for batch in pf.iter_batches(batch_size=10_000_000, columns=["ts_event", "action", "side"]):
            ts = batch.column("ts_event").cast('int64').to_numpy()
            act = batch.column("action").to_numpy(zero_copy_only=False).astype('U1')
            sid = batch.column("side").to_numpy(zero_copy_only=False).astype('U1')
            ts_floor = (ts // 1_000_000_000) * 1_000_000_000
            is_bid = (sid == 'B'); is_add = (act == 'A'); is_cancel = (act == 'C')
            all_ts.append(ts_floor)
            all_ba.append((is_add & is_bid).astype(np.int8))
            all_aa.append((is_add & ~is_bid).astype(np.int8))
            all_bc.append((is_cancel & is_bid).astype(np.int8))
            all_ac.append((is_cancel & ~is_bid).astype(np.int8))
        if not all_ts: return None
        df = pd.DataFrame({
            "ts_floor": np.concatenate(all_ts),
            "ba": np.concatenate(all_ba), "aa": np.concatenate(all_aa),
            "bc": np.concatenate(all_bc), "ac": np.concatenate(all_ac),
        })
        del all_ts, all_ba, all_aa, all_bc, all_ac; gc_mod.collect()
        result = df.groupby("ts_floor").agg(
            bid_adds=("ba","sum"), ask_adds=("aa","sum"),
            bid_cancels=("bc","sum"), ask_cancels=("ac","sum"),
        ).reset_index()
        result["total_events"] = result["bid_adds"] + result["ask_adds"] + result["bid_cancels"] + result["ask_cancels"]
        result["ts_floor"] = pd.to_datetime(result["ts_floor"], unit="ns")
        del df; gc_mod.collect()
        return result
    else:
        try:
            df = pq.read_table(str(path), columns=["ts_event","action","side"]).to_pandas()
        except Exception:
            return None
        df["ts_event"] = pd.to_datetime(df["ts_event"])
        if df["ts_event"].dt.tz is not None:
            df["ts_event"] = df["ts_event"].dt.tz_localize(None)
        df["ts_floor"] = df["ts_event"].dt.floor("1s")
        df["is_bid"] = df["side"].isin(["B","b","Buy","bid"])
        df["bid_add"] = ((df["action"]=="A") & df["is_bid"]).astype(int)
        df["ask_add"] = ((df["action"]=="A") & ~df["is_bid"]).astype(int)
        df["bid_cancel"] = ((df["action"]=="C") & df["is_bid"]).astype(int)
        df["ask_cancel"] = ((df["action"]=="C") & ~df["is_bid"]).astype(int)
        result = df.groupby("ts_floor").agg(
            bid_adds=("bid_add","sum"), ask_adds=("ask_add","sum"),
            bid_cancels=("bid_cancel","sum"), ask_cancels=("ask_cancel","sum"),
            total_events=("action","count"),
        ).reset_index()
        del df
        return result


def build_features_month(sym, month, meta, horizons):
    tick = meta["tick_size"]
    ds, de = meta["day_start_utc"], meta["day_end_utc"]
    data_dir = get_data_dir(sym)
    p = data_dir / f"{sym}_snapshots_{month}.parquet"
    if not p.exists(): return None
    snap = pq.read_table(str(p)).to_pandas()
    snap["timestamp"] = pd.to_datetime(snap["timestamp"])
    snap["spread"] = snap["spread"].clip(lower=0.0)
    snap["spread_ticks"] = snap["spread"] / tick
    snap = snap.sort_values("timestamp").reset_index(drop=True)
    snap["hour_utc"] = snap["timestamp"].dt.hour
    snap = snap[(snap["hour_utc"] >= ds) & (snap["hour_utc"] < de)].copy()
    if len(snap) < 100: return None

    snap["minutes_since_open"] = (snap["hour_utc"] - ds) * 60 + snap["timestamp"].dt.minute
    mid = snap["mid_price"].replace(0, np.nan)

    for lag in [1, 5, 10, 30, 60, 300]:
        snap[f"mid_return_{lag}s"] = mid.pct_change(lag)
    r1s = snap["mid_return_1s"]
    snap["volatility_30s"] = r1s.rolling(30, min_periods=10).std()
    snap["volatility_300s"] = r1s.rolling(300, min_periods=60).std()
    snap["range_60s"] = (mid.rolling(60, min_periods=10).max() - mid.rolling(60, min_periods=10).min()) / tick
    snap["range_300s"] = (mid.rolling(300, min_periods=60).max() - mid.rolling(300, min_periods=60).min()) / tick
    snap["l1_imbalance"] = ((snap["bid_size_1"] - snap["ask_size_1"]) /
                            (snap["bid_size_1"] + snap["ask_size_1"]).replace(0, np.nan))

    bid_cols = [f"bid_size_{i}" for i in range(1, 6) if f"bid_size_{i}" in snap.columns]
    ask_cols = [f"ask_size_{i}" for i in range(1, 6) if f"ask_size_{i}" in snap.columns]
    snap["total_bid_depth"] = snap[bid_cols].sum(axis=1)
    snap["total_ask_depth"] = snap[ask_cols].sum(axis=1)
    td = snap["total_bid_depth"] + snap["total_ask_depth"]
    snap["depth_imbalance"] = ((snap["total_bid_depth"] - snap["total_ask_depth"]) / td.replace(0, np.nan))
    nb, na = len(bid_cols), len(ask_cols)
    snap["book_slope_bid"] = (snap["bid_size_1"] - snap[bid_cols[-1]]) / max(nb-1,1) if nb >= 2 else 0.0
    snap["book_slope_ask"] = (snap["ask_size_1"] - snap[ask_cols[-1]]) / max(na-1,1) if na >= 2 else 0.0
    for lag in [1, 5, 30]:
        snap[f"depth_change_{lag}s"] = td.diff(lag)
    for win in [60, 300]:
        snap[f"depth_pctile_{win}s"] = td.rolling(win, min_periods=10).rank(pct=True)

    # Forward returns at ALL horizons
    for h in horizons:
        fwd = mid.shift(-h)
        snap[f"fwd_move_ticks_{h}s"] = (fwd - mid) / tick

    # Trades
    snap["ts_floor"] = snap["timestamp"].dt.floor("1s")
    tp = data_dir / f"{sym}_trades_tagged_{month}.parquet"
    if tp.exists():
        trades = pq.read_table(str(tp)).to_pandas()
        trades["ts_event"] = pd.to_datetime(trades["ts_event"])
        if trades["ts_event"].dt.tz is not None:
            trades["ts_event"] = trades["ts_event"].dt.tz_localize(None)
        trades = trades.sort_values("ts_event")
        trades["ts_floor"] = trades["ts_event"].dt.floor("1s")
        is_buy = trades["aggressor_side"].isin(["B","Buy","buy"]) if "aggressor_side" in trades.columns \
                 else trades["side"].isin(["B","Buy","buy"])
        trades["signed_vol"] = np.where(is_buy, trades["size"], -trades["size"])
        trades["buy_vol"] = np.where(is_buy, trades["size"], 0)
        trades["sell_vol"] = np.where(~is_buy, trades["size"], 0)
        trades["is_large"] = (trades["size"] >= 10).astype(int)
        tagg = trades.groupby("ts_floor").agg(
            net_delta=("signed_vol","sum"), buy_volume=("buy_vol","sum"),
            sell_volume=("sell_vol","sum"), trade_count=("size","count"),
            trade_volume=("size","sum"), large_trade_count=("is_large","sum"),
            vwap=("price", lambda x: np.average(x, weights=trades.loc[x.index,"size"])
                  if trades.loc[x.index,"size"].sum() > 0 else np.nan),
        ).reset_index()
        if snap["ts_floor"].dt.tz is not None:
            snap["ts_floor"] = snap["ts_floor"].dt.tz_localize(None)
        if tagg["ts_floor"].dt.tz is not None:
            tagg["ts_floor"] = tagg["ts_floor"].dt.tz_localize(None)
        snap = snap.merge(tagg, on="ts_floor", how="left")
        for c in ["net_delta","buy_volume","sell_volume","trade_count","trade_volume","large_trade_count"]:
            snap[c] = snap[c].fillna(0)
        snap["vwap"] = snap["vwap"].ffill()
        for w in [1, 5, 10, 30, 60]:
            snap[f"net_delta_{w}s"] = snap["net_delta"].rolling(w, min_periods=1).sum()
        snap["buy_volume_10s"] = snap["buy_volume"].rolling(10, min_periods=1).sum()
        snap["sell_volume_10s"] = snap["sell_volume"].rolling(10, min_periods=1).sum()
        snap["trade_count_10s"] = snap["trade_count"].rolling(10, min_periods=1).sum()
        snap["large_trade_count_10s"] = snap["large_trade_count"].rolling(10, min_periods=1).sum()
        snap["vwap_distance"] = (mid - snap["vwap"]) / tick
        del trades, tagg
    else:
        for c in [f"net_delta_{w}s" for w in [1,5,10,30,60]] + \
                 ["buy_volume_10s","sell_volume_10s","trade_count_10s",
                  "large_trade_count_10s","vwap_distance"]:
            snap[c] = 0.0

    # MBO
    magg = load_mbo_aggregated(sym, month)
    if magg is not None and len(magg) > 0:
        if magg["ts_floor"].dt.tz is not None:
            magg["ts_floor"] = magg["ts_floor"].dt.tz_localize(None)
        if snap["ts_floor"].dt.tz is not None:
            snap["ts_floor"] = snap["ts_floor"].dt.tz_localize(None)
        snap = snap.merge(magg, on="ts_floor", how="left")
        for c in ["bid_adds","ask_adds","bid_cancels","ask_cancels","total_events"]:
            snap[c] = snap[c].fillna(0)
        for w in [5, 10]:
            snap[f"bid_add_rate_{w}s"] = snap["bid_adds"].rolling(w, min_periods=1).sum()
            snap[f"ask_add_rate_{w}s"] = snap["ask_adds"].rolling(w, min_periods=1).sum()
            snap[f"bid_cancel_rate_{w}s"] = snap["bid_cancels"].rolling(w, min_periods=1).sum()
            snap[f"ask_cancel_rate_{w}s"] = snap["ask_cancels"].rolling(w, min_periods=1).sum()
        tc10 = snap["bid_cancel_rate_10s"] + snap["ask_cancel_rate_10s"]
        snap["cancel_ratio_asymmetry"] = ((snap["bid_cancel_rate_10s"] - snap["ask_cancel_rate_10s"]) /
                                          tc10.replace(0, np.nan)).fillna(0)
        snap["event_rate_10s"] = snap["total_events"].rolling(10, min_periods=1).sum()
        snap["order_flow_accel"] = snap["event_rate_10s"].diff(5)
        del magg
    else:
        for c in [f"bid_add_rate_{w}s" for w in [5,10]] + \
                 [f"ask_add_rate_{w}s" for w in [5,10]] + \
                 [f"bid_cancel_rate_{w}s" for w in [5,10]] + \
                 [f"ask_cancel_rate_{w}s" for w in [5,10]] + \
                 ["cancel_ratio_asymmetry","order_flow_accel"]:
            snap[c] = 0.0

    snap["month"] = month
    snap = snap.replace([np.inf, -np.inf], np.nan)
    gc_mod.collect()
    return snap


# ═══════════════════════════════════════════════════════════════
# DEEP LEARNING MODELS (PyTorch)
# ═══════════════════════════════════════════════════════════════

class LSTMModel(nn.Module):
    def __init__(self, n_features):
        super().__init__()
        self.lstm1 = nn.LSTM(n_features, 64, batch_first=True)
        self.drop1 = nn.Dropout(0.2)
        self.lstm2 = nn.LSTM(64, 32, batch_first=True)
        self.drop2 = nn.Dropout(0.2)
        self.fc1 = nn.Linear(32, 16)
        self.fc2 = nn.Linear(16, 1)

    def forward(self, x):
        x, _ = self.lstm1(x)
        x = self.drop1(x)
        x, _ = self.lstm2(x)
        x = self.drop2(x[:, -1, :])  # last timestep
        x = torch.relu(self.fc1(x))
        return torch.sigmoid(self.fc2(x)).squeeze(-1)


class CNNModel(nn.Module):
    def __init__(self, n_features):
        super().__init__()
        # Causal padding: pad left only
        self.conv1 = nn.Conv1d(n_features, 64, kernel_size=3, padding=0)
        self.conv2 = nn.Conv1d(64, 32, kernel_size=3, padding=0)
        self.pool = nn.AdaptiveMaxPool1d(1)
        self.fc1 = nn.Linear(32, 32)
        self.drop = nn.Dropout(0.2)
        self.fc2 = nn.Linear(32, 1)

    def forward(self, x):
        # x: (batch, seq_len, features) -> (batch, features, seq_len)
        x = x.permute(0, 2, 1)
        # Causal padding: pad left by (kernel_size - 1)
        x = nn.functional.pad(x, (2, 0))
        x = torch.relu(self.conv1(x))
        x = nn.functional.pad(x, (2, 0))
        x = torch.relu(self.conv2(x))
        x = self.pool(x).squeeze(-1)
        x = torch.relu(self.fc1(x))
        x = self.drop(x)
        return torch.sigmoid(self.fc2(x)).squeeze(-1)


class TransformerModel(nn.Module):
    def __init__(self, n_features, seq_len=10):
        super().__init__()
        self.pos_embedding = nn.Embedding(seq_len, n_features)
        self.attn = nn.MultiheadAttention(embed_dim=n_features, num_heads=4,
                                          batch_first=True, dropout=0.1)
        self.norm1 = nn.LayerNorm(n_features)
        self.ff = nn.Sequential(
            nn.Linear(n_features, 64), nn.ReLU(), nn.Linear(64, n_features)
        )
        self.norm2 = nn.LayerNorm(n_features)
        self.fc1 = nn.Linear(n_features, 32)
        self.drop = nn.Dropout(0.2)
        self.fc2 = nn.Linear(32, 1)
        self.seq_len = seq_len

    def forward(self, x):
        B, T, F = x.shape
        pos = self.pos_embedding(torch.arange(T, device=x.device)).unsqueeze(0).expand(B, -1, -1)
        x = x + pos
        # Causal mask
        mask = torch.triu(torch.ones(T, T, device=x.device), diagonal=1).bool()
        attn_out, _ = self.attn(x, x, x, attn_mask=mask)
        x = self.norm1(x + attn_out)
        ff_out = self.ff(x)
        x = self.norm2(x + ff_out)
        x = x.mean(dim=1)  # global average pool
        x = torch.relu(self.fc1(x))
        x = self.drop(x)
        return torch.sigmoid(self.fc2(x)).squeeze(-1)


def build_sequences(X, y, seq_len=10, max_seqs=200_000):
    """Build sequences using numpy stride tricks for speed. Cap at max_seqs."""
    n = len(X)
    nf = X.shape[1]
    if n < seq_len:
        return np.empty((0, seq_len, nf)), np.empty(0)
    n_seqs = n - seq_len + 1
    stride = max(1, n_seqs // max_seqs)
    # Use as_strided for zero-copy sliding window, then subsample
    X32 = np.ascontiguousarray(X, dtype=np.float32)
    from numpy.lib.stride_tricks import as_strided
    new_shape = (n_seqs, seq_len, nf)
    new_strides = (X32.strides[0], X32.strides[0], X32.strides[1])
    X_windows = as_strided(X32, shape=new_shape, strides=new_strides)
    # Subsample with stride and copy to own memory
    X_seq = np.array(X_windows[::stride], dtype=np.float32)
    y_seq = y[seq_len - 1::stride][:len(X_seq)]
    print(f"      build_seq: {n}->{len(X_seq)} (stride={stride})", flush=True)
    return X_seq, y_seq


def train_dl_model(model_class, X_train, y_train, X_val, y_val, X_test, y_test,
                   n_features, max_epochs=50, patience=5, batch_size=512):
    """Train a PyTorch deep learning model with early stopping on val AUC."""
    # Build sequences
    Xs_train, ys_train = build_sequences(X_train, y_train, SEQ_LEN)
    Xs_val, ys_val = build_sequences(X_val, y_val, SEQ_LEN)
    Xs_test, ys_test = build_sequences(X_test, y_test, SEQ_LEN)

    if len(Xs_train) < 100 or len(Xs_val) < 50:
        return None, None, None, ys_test

    train_ds = TensorDataset(torch.tensor(Xs_train), torch.tensor(ys_train, dtype=torch.float32))
    train_dl = DataLoader(train_ds, batch_size=batch_size, shuffle=True, drop_last=True)

    if model_class == TransformerModel:
        # Transformer needs embed_dim divisible by num_heads
        # Pad features to nearest multiple of 4
        pad_to = ((n_features + 3) // 4) * 4
        if pad_to != n_features:
            Xs_train = np.pad(Xs_train, ((0,0),(0,0),(0,pad_to-n_features)))
            Xs_val = np.pad(Xs_val, ((0,0),(0,0),(0,pad_to-n_features)))
            Xs_test = np.pad(Xs_test, ((0,0),(0,0),(0,pad_to-n_features)))
            train_ds = TensorDataset(torch.tensor(Xs_train), torch.tensor(ys_train, dtype=torch.float32))
            train_dl = DataLoader(train_ds, batch_size=batch_size, shuffle=True, drop_last=True)
            model = model_class(pad_to, SEQ_LEN).to(DEVICE)
        else:
            model = model_class(n_features, SEQ_LEN).to(DEVICE)
    else:
        model = model_class(n_features).to(DEVICE)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.BCELoss()

    def batched_predict(model, X_np, batch_sz=2048):
        """Run inference in batches to avoid GPU OOM."""
        preds = []
        for i in range(0, len(X_np), batch_sz):
            xb = torch.tensor(X_np[i:i+batch_sz]).to(DEVICE)
            preds.append(model(xb).cpu().numpy())
        return np.concatenate(preds)

    best_val_auc = 0
    best_state = None
    patience_counter = 0
    first_5_val_aucs = []

    for epoch in range(max_epochs):
        model.train()
        for xb, yb in train_dl:
            xb, yb = xb.to(DEVICE), yb.to(DEVICE)
            pred = model(xb)
            loss = criterion(pred, yb)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        # Validate
        model.eval()
        with torch.no_grad():
            val_pred = batched_predict(model, Xs_val)
            val_auc = roc_auc_score(ys_val, val_pred)

        if epoch < 5:
            first_5_val_aucs.append(val_auc)

        if val_auc > best_val_auc:
            best_val_auc = val_auc
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
            patience_counter = 0
        else:
            patience_counter += 1

        if patience_counter >= patience:
            break

    # Check convergence
    if len(first_5_val_aucs) >= 5:
        improvement = max(first_5_val_aucs) - first_5_val_aucs[0]
        if improvement < 0.001:
            # Non-convergent
            return None, None, "NON-CONVERGENT", ys_test

    # Load best and predict
    if best_state is not None:
        model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        test_pred = batched_predict(model, Xs_test)
        test_auc = roc_auc_score(ys_test, test_pred)

    return test_auc, best_val_auc, test_pred, ys_test


def run_shuffle_test_dl(model_class, X_train, y_train, X_val, y_val, X_test, y_test,
                        n_features, n_runs=N_SHUFFLE):
    """Shuffle test for deep learning models."""
    shuf_aucs = []
    for i in range(n_runs):
        np.random.seed(i * 1000 + 42)
        ys_t = np.random.permutation(y_train)
        ys_v = np.random.permutation(y_val)
        auc, _, pred, ys = train_dl_model(model_class, X_train, ys_t, X_val, ys_v, X_test, y_test,
                                          n_features, max_epochs=20, patience=3, batch_size=512)
        if auc is not None:
            shuf_aucs.append(auc)
    return shuf_aucs


# ═══════════════════════════════════════════════════════════════
# MAIN TRAINING LOOP
# ═══════════════════════════════════════════════════════════════

def train_one(arch, X_train, y_train, X_val, y_val, X_test, y_test, use_feats, tick):
    """Train one architecture, return dict of results."""
    n_features = X_train.shape[1]

    if arch == "XGBoost":
        model = xgb.XGBClassifier(
            n_estimators=1000, max_depth=6, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8, eval_metric="auc",
            early_stopping_rounds=50,
            use_label_encoder=False, random_state=42, verbosity=0, n_jobs=4,
        )
        model.fit(X_train, y_train, eval_set=[(X_val, y_val)],
                  verbose=False)
        pred_test = model.predict_proba(X_test)[:, 1]
        test_auc = roc_auc_score(y_test, pred_test)
        val_auc = roc_auc_score(y_val, model.predict_proba(X_val)[:, 1])

        # Feature importance
        imp = dict(zip(use_feats, model.feature_importances_.tolist()))
        top10 = sorted(imp.items(), key=lambda x: -x[1])[:10]

        # Shuffle test
        shuf_aucs = []
        for i in range(N_SHUFFLE):
            np.random.seed(i * 1000 + 42)
            ys_t = np.random.permutation(y_train)
            ys_v = np.random.permutation(y_val)
            ms = xgb.XGBClassifier(
                n_estimators=1000, max_depth=6, learning_rate=0.05,
                subsample=0.8, colsample_bytree=0.8, eval_metric="auc",
                early_stopping_rounds=50,
                use_label_encoder=False, random_state=42, verbosity=0, n_jobs=4,
            )
            ms.fit(X_train, ys_t, eval_set=[(X_val, ys_v)], verbose=False)
            ps = ms.predict_proba(X_test)[:, 1]
            shuf_aucs.append(roc_auc_score(y_test, ps))

        return {"test_auc": round(test_auc, 4), "val_auc": round(val_auc, 4),
                "shuffle_mean": round(np.mean(shuf_aucs), 4),
                "shuffle_std": round(np.std(shuf_aucs), 4),
                "top10": top10}

    elif arch == "LogReg":
        scaler = StandardScaler()
        Xs_train = scaler.fit_transform(X_train)
        Xs_val = scaler.transform(X_val)
        Xs_test = scaler.transform(X_test)

        best_c, best_val_auc = None, 0
        for C in [0.001, 0.01, 0.1, 1.0]:
            lr = LogisticRegression(solver="saga", max_iter=1000, C=C,
                                    penalty="l2", class_weight="balanced",
                                    random_state=42, n_jobs=4)
            lr.fit(Xs_train, y_train)
            va = roc_auc_score(y_val, lr.predict_proba(Xs_val)[:, 1])
            if va > best_val_auc:
                best_val_auc = va
                best_c = C

        lr = LogisticRegression(solver="saga", max_iter=1000, C=best_c,
                                penalty="l2", class_weight="balanced",
                                random_state=42, n_jobs=4)
        lr.fit(Xs_train, y_train)
        pred_test = lr.predict_proba(Xs_test)[:, 1]
        test_auc = roc_auc_score(y_test, pred_test)

        # Feature importance (absolute coefficients)
        coefs = dict(zip(use_feats, np.abs(lr.coef_[0]).tolist()))
        top10 = sorted(coefs.items(), key=lambda x: -x[1])[:10]

        # Shuffle
        shuf_aucs = []
        for i in range(N_SHUFFLE):
            np.random.seed(i * 1000 + 42)
            ys_t = np.random.permutation(y_train)
            ys_v = np.random.permutation(y_val)
            ms = LogisticRegression(solver="saga", max_iter=1000, C=best_c,
                                    penalty="l2", class_weight="balanced",
                                    random_state=42, n_jobs=4)
            ms.fit(Xs_train, ys_t)
            ps = ms.predict_proba(Xs_test)[:, 1]
            shuf_aucs.append(roc_auc_score(y_test, ps))

        return {"test_auc": round(test_auc, 4), "val_auc": round(best_val_auc, 4),
                "shuffle_mean": round(np.mean(shuf_aucs), 4),
                "shuffle_std": round(np.std(shuf_aucs), 4),
                "best_C": best_c, "top10": top10}

    elif arch in ("LSTM", "CNN", "Transformer"):
        # Scale features
        scaler = StandardScaler()
        Xs_train = scaler.fit_transform(X_train).astype(np.float32)
        Xs_val = scaler.transform(X_val).astype(np.float32)
        Xs_test = scaler.transform(X_test).astype(np.float32)

        model_class = {"LSTM": LSTMModel, "CNN": CNNModel, "Transformer": TransformerModel}[arch]
        test_auc, val_auc, pred_or_status, ys_test_seq = train_dl_model(
            model_class, Xs_train, y_train, Xs_val, y_val, Xs_test, y_test, n_features)

        if isinstance(pred_or_status, str) and pred_or_status == "NON-CONVERGENT":
            return {"test_auc": None, "val_auc": None, "status": "NON-CONVERGENT",
                    "shuffle_mean": None, "shuffle_std": None}

        if test_auc is None:
            return {"test_auc": None, "val_auc": None, "status": "FAILED",
                    "shuffle_mean": None, "shuffle_std": None}

        # Shuffle test (fewer runs for DL to save time)
        shuf_aucs = run_shuffle_test_dl(model_class, Xs_train, y_train, Xs_val, y_val,
                                        Xs_test, y_test, n_features, n_runs=N_SHUFFLE)

        return {"test_auc": round(test_auc, 4), "val_auc": round(val_auc, 4),
                "shuffle_mean": round(np.mean(shuf_aucs), 4) if shuf_aucs else None,
                "shuffle_std": round(np.std(shuf_aucs), 4) if shuf_aucs else None}

    return None


def process_instrument(sym):
    """Process all architectures × horizons × feature sets for one instrument."""
    global completed_runs
    meta = INST_META[sym]
    tick = meta["tick_size"]

    print(f"\n{'#'*70}", flush=True)
    print(f"  INSTRUMENT: {sym.upper()} (C/T={meta['ct_ratio']}, {meta['matching']})", flush=True)
    print(f"{'#'*70}", flush=True)

    # Check for existing checkpoint
    ckpt_path = RESULTS / f"checkpoint_{sym}.json"
    existing_results = {}
    if ckpt_path.exists():
        with open(ckpt_path) as f:
            existing_results = json.load(f)
        print(f"  Loaded {len(existing_results)} cached results from checkpoint", flush=True)

    # Build features
    print(f"  Building features...", flush=True)
    dfs = []
    for m in ALL_MONTHS:
        print(f"    {m}...", end=" ", flush=True)
        try:
            df = build_features_month(sym, m, meta, HORIZONS)
            if df is not None:
                dfs.append(df)
                print(f"{len(df):,}", flush=True)
            else:
                print("skip", flush=True)
        except Exception as e:
            print(f"ERR: {e}", flush=True)
        gc_mod.collect()

    feat_df = pd.concat(dfs, ignore_index=True)
    del dfs; gc_mod.collect()
    print(f"  Total rows: {len(feat_df):,}", flush=True)

    results = []

    for horizon in HORIZONS:
        ret_col = f"fwd_move_ticks_{horizon}s"
        if ret_col not in feat_df.columns:
            continue

        # Apply magnitude filter
        valid = feat_df.dropna(subset=[ret_col])
        valid = valid[valid[ret_col].abs() >= 2.0].copy()
        valid["target"] = (valid[ret_col] > 0).astype(int)

        train = valid[valid["month"].isin(TRAIN_MONTHS)]
        val = valid[valid["month"].isin(VAL_MONTHS)]
        test = valid[valid["month"].isin(TEST_MONTHS)]

        if len(train) < 500 or len(val) < 200 or len(test) < 200:
            print(f"  {horizon}s: insufficient data (train={len(train)}, val={len(val)}, test={len(test)})", flush=True)
            continue

        for fset_name, fset_features in FEATURE_SETS.items():
            use_feats = [f for f in fset_features if f in valid.columns]

            X_train = train[use_feats].fillna(0).values
            y_train = train["target"].values
            X_val = val[use_feats].fillna(0).values
            y_val = val["target"].values
            X_test = test[use_feats].fillna(0).values
            y_test = test["target"].values

            for arch in ARCHITECTURES:
                run_key = f"{sym}_{arch}_{horizon}s_{fset_name}"

                # Check checkpoint
                if run_key in existing_results:
                    r = existing_results[run_key]
                    results.append(r)
                    completed_runs += 1
                    print(f"  [{completed_runs}/{total_runs}] {run_key}: CACHED (AUC={r.get('test_auc', 'N/A')})", flush=True)
                    continue

                t0 = time.time()
                try:
                    r = train_one(arch, X_train, y_train, X_val, y_val, X_test, y_test, use_feats, tick)
                    if r is None:
                        r = {"test_auc": None, "status": "FAILED"}
                except Exception as e:
                    r = {"test_auc": None, "status": f"ERROR: {str(e)[:100]}"}
                    print(f"    ERROR: {e}", flush=True)

                elapsed = time.time() - t0
                r["instrument"] = sym.upper()
                r["architecture"] = arch
                r["horizon"] = f"{horizon}s"
                r["feature_set"] = fset_name
                r["n_features"] = len(use_feats)
                r["n_train"] = len(train)
                r["n_test"] = len(test)
                r["elapsed_s"] = round(elapsed, 1)
                results.append(r)

                # Save checkpoint
                existing_results[run_key] = r
                with open(ckpt_path, "w") as f:
                    json.dump(existing_results, f, indent=2,
                              default=lambda o: float(o) if isinstance(o, (np.floating,)) else
                                                int(o) if isinstance(o, (np.integer,)) else
                                                bool(o) if isinstance(o, (np.bool_,)) else
                                                o.tolist() if isinstance(o, np.ndarray) else o)

                completed_runs += 1
                run_times.append(elapsed)

                auc_str = f"{r['test_auc']:.4f}" if r.get('test_auc') else r.get('status', 'N/A')
                shuf_str = f"shuf={r.get('shuffle_mean', 'N/A')}" if r.get('shuffle_mean') else ""

                # Estimate remaining time
                if len(run_times) >= 3:
                    avg_time = np.mean(run_times)
                    remaining = (total_runs - completed_runs) * avg_time
                    eta = f"ETA: {remaining/60:.0f}min"
                else:
                    eta = ""

                print(f"  [{completed_runs}/{total_runs}] {run_key}: AUC={auc_str} {shuf_str} ({elapsed:.1f}s) {eta}", flush=True)

                # Flag checks
                if r.get('test_auc') and fset_name == "BFree" and r['test_auc'] > 0.70:
                    print(f"  *** FLAG F1: BFree AUC > 0.70! {run_key} ***", flush=True)
                if r.get('shuffle_mean') and r['shuffle_mean'] > 0.55:
                    print(f"  *** FLAG F3: Shuffle AUC > 0.55! {run_key} ***", flush=True)

                torch.cuda.empty_cache() if torch.cuda.is_available() else None
                gc_mod.collect()

    # Save instrument CSV
    inst_df = pd.DataFrame(results)
    inst_csv = RESULTS / f"phase5_{sym.upper()}_results.csv"
    inst_df.to_csv(inst_csv, index=False)
    print(f"\n  Saved: {inst_csv}", flush=True)

    del feat_df, valid; gc_mod.collect()
    return results


def main():
    args = sys.argv[1:]

    print("=" * 70, flush=True)
    print("PHASE 5 OBJECTIVE STATEMENT:", flush=True)
    print("This phase tests whether any standard ML architecture", flush=True)
    print("can find exploitable directional signal in CME futures", flush=True)
    print("microstructure at retail-accessible latency. A finding", flush=True)
    print("that no architecture succeeds is the expected and", flush=True)
    print("scientifically valid outcome. The paper does not require", flush=True)
    print("a positive result to be publishable — it requires an", flush=True)
    print("exhaustive, methodologically sound negative result.", flush=True)
    print("", flush=True)
    print("Every result is reported as-is. No architecture is", flush=True)
    print("favored. No result is suppressed.", flush=True)
    print("=" * 70, flush=True)

    print(f"\nDevice: {DEVICE}", flush=True)
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}", flush=True)

    print(f"\nFull features ({len(FULL_FEATURES)}): {FULL_FEATURES}", flush=True)
    print(f"\nPrice-lag features REMOVED for BFree set ({len(PRICE_LAG_FEATURES)}):", flush=True)
    print(f"  {PRICE_LAG_FEATURES}", flush=True)
    print(f"\nBounce-free features ({len(BOUNCE_FREE_FEATURES)}): {BOUNCE_FREE_FEATURES}", flush=True)
    print(f"\nArchitectures: {ARCHITECTURES}", flush=True)
    print(f"Horizons: {HORIZONS}", flush=True)
    print(f"Total runs: {total_runs}", flush=True)

    # Determine which instruments to run
    BATCH_A = ["zc", "zs", "he", "le"]
    BATCH_B = ["es", "cl", "gc", "nq"]

    if not args:
        instruments = BATCH_A + BATCH_B
    elif args[0] == "batchA":
        instruments = BATCH_A
    elif args[0] == "batchB":
        instruments = BATCH_B
    else:
        instruments = [a.lower() for a in args]

    print(f"\nInstruments: {[s.upper() for s in instruments]}", flush=True)

    all_results = []
    for sym in instruments:
        if sym not in INST_META:
            print(f"  Unknown: {sym}"); continue
        try:
            r = process_instrument(sym)
            all_results.extend(r)
        except Exception as e:
            print(f"  [{sym.upper()}] FAILED: {e}")
            traceback.print_exc()
        gc_mod.collect()

    # Save master table
    if all_results:
        master = pd.DataFrame(all_results)
        master_path = RESULTS / "phase5_master_partial.csv"
        master.to_csv(master_path, index=False)
        print(f"\nSaved master: {master_path}", flush=True)

    total_time = time.time() - phase5_start
    print(f"\nPhase 5 total time: {total_time/60:.1f} min", flush=True)
    print("Phase 5 batch complete!", flush=True)


if __name__ == "__main__":
    main()
