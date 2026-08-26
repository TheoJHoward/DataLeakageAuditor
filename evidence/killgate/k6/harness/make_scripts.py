"""Emit each case as a standalone .py script for the static analysers (OMDS, and the Yang engine
if it could be built).

Adapter judged SETUP under CROSS_TOOL_COMPARISON 2.6 item 4: a static analyser reads source, so
source is the only form in which a case can be presented to it. The construction expressed here
is the SAME construction `case_defs.py` performs -- pooled vs train-only preprocessing, overlapping
vs disjoint split indices, and so on. Nothing about what the case tests is changed.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "cases", "_scripts"))

HEAD = """import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def run():
    df = pd.read_csv("full.csv")
    y = df["target"].to_numpy()
    X = df.drop(columns=["target"]).to_numpy(dtype=float)
    n = len(df)
"""

BODY = {
    # C1 -- declared split: overlapping vs disjoint index sets
    ("C1", "contaminated"): """
    train_idx = np.arange(0, n, 2)
    test_idx = np.sort(np.concatenate([np.arange(1, n, 2), train_idx[:20]]))
    X_train, y_train = X[train_idx], y[train_idx]
    X_test, y_test = X[test_idx], y[test_idx]
    model = LogisticRegression(max_iter=200).fit(X_train, y_train)
    print(model.score(X_test, y_test))
""",
    ("C1", "clean"): """
    train_idx = np.arange(0, n, 2)
    test_idx = np.arange(1, n, 2)
    X_train, y_train = X[train_idx], y[train_idx]
    X_test, y_test = X[test_idx], y[test_idx]
    model = LogisticRegression(max_iter=200).fit(X_train, y_train)
    print(model.score(X_test, y_test))
""",
    # C2 -- scaler fitted on pooled train+test vs on train only
    ("C2", "contaminated"): """
    scaler = StandardScaler()
    X_all = scaler.fit_transform(X)              # FIT ON TRAIN+TEST
    X_tr, X_te, y_train, y_test = train_test_split(X, y, test_size=0.5, shuffle=False)
    X_train, X_test = X_all[: n // 2], X_all[n // 2:]
    model = LogisticRegression(max_iter=200).fit(X_train, y_train)
    print(model.score(X_test, y_test))
""",
    ("C2", "clean"): """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, shuffle=False)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)      # fit on train only
    X_test = scaler.transform(X_test)
    model = LogisticRegression(max_iter=200).fit(X_train, y_train)
    print(model.score(X_test, y_test))
""",
    # C3 -- selector fitted on pooled train+test vs on train only
    ("C3", "contaminated"): """
    selector = SelectKBest(f_classif, k=5)
    X_all = selector.fit_transform(X, y)         # SELECT ON TRAIN+TEST
    X_tr, X_te, y_train, y_test = train_test_split(X, y, test_size=0.5, shuffle=False)
    X_train, X_test = X_all[: n // 2], X_all[n // 2:]
    model = LogisticRegression(max_iter=200).fit(X_train, y_train)
    print(model.score(X_test, y_test))
""",
    ("C3", "clean"): """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, shuffle=False)
    selector = SelectKBest(f_classif, k=5)
    X_train = selector.fit_transform(X_train, y_train)   # select on train only
    X_test = selector.transform(X_test)
    model = LogisticRegression(max_iter=200).fit(X_train, y_train)
    print(model.score(X_test, y_test))
""",
    # C4 -- duplicate rows across vs within the split boundary
    ("C4", "contaminated"): """
    X[n // 2: n // 2 + 25] = X[0:25]             # duplicates straddle the boundary
    y[n // 2: n // 2 + 25] = y[0:25]
    X_train, X_test = X[: n // 2], X[n // 2:]
    y_train, y_test = y[: n // 2], y[n // 2:]
    model = LogisticRegression(max_iter=200).fit(X_train, y_train)
    print(model.score(X_test, y_test))
""",
    ("C4", "clean"): """
    X[n // 4: n // 4 + 25] = X[0:25]             # duplicates stay inside train
    y[n // 4: n // 4 + 25] = y[0:25]
    X_train, X_test = X[: n // 2], X[n // 2:]
    y_train, y_test = y[: n // 2], y[n // 2:]
    model = LogisticRegression(max_iter=200).fit(X_train, y_train)
    print(model.score(X_test, y_test))
""",
    # C5 -- feature computed from the same-row label vs from the previous row's label
    ("C5", "contaminated"): """
    risk_score = y * 3.0                          # FEATURE READS ITS OWN ROW'S LABEL
    X = np.column_stack([X, risk_score])
    X_train, X_test = X[: n // 2], X[n // 2:]
    y_train, y_test = y[: n // 2], y[n // 2:]
    model = LogisticRegression(max_iter=200).fit(X_train, y_train)
    print(model.score(X_test, y_test))
""",
    ("C5", "clean"): """
    risk_score = np.concatenate([[0.0], y[:-1] * 3.0])   # previous row's label
    X = np.column_stack([X, risk_score])
    X_train, X_test = X[: n // 2], X[n // 2:]
    y_train, y_test = y[: n // 2], y[n // 2:]
    model = LogisticRegression(max_iter=200).fit(X_train, y_train)
    print(model.score(X_test, y_test))
""",
    # C6 -- trailing window including vs excluding the decision bar
    ("C6", "contaminated"): """
    x = df["x"].to_numpy(dtype=float) if "x" in df else X[:, 0]
    win5 = pd.Series(x).rolling(5, min_periods=5).mean().to_numpy()   # INCLUDES BAR t
    X = win5.reshape(-1, 1)
    ok = ~np.isnan(win5)
    X_train, X_test = X[ok][: n // 3], X[ok][n // 3:]
    y_train, y_test = y[ok][: n // 3], y[ok][n // 3:]
    model = LogisticRegression(max_iter=200).fit(X_train, y_train)
    print(model.score(X_test, y_test))
""",
    ("C6", "clean"): """
    x = df["x"].to_numpy(dtype=float) if "x" in df else X[:, 0]
    win5 = pd.Series(x).shift(1).rolling(5, min_periods=5).mean().to_numpy()   # ends at t-1
    X = win5.reshape(-1, 1)
    ok = ~np.isnan(win5)
    X_train, X_test = X[ok][: n // 3], X[ok][n // 3:]
    y_train, y_test = y[ok][: n // 3], y[ok][n // 3:]
    model = LogisticRegression(max_iter=200).fit(X_train, y_train)
    print(model.score(X_test, y_test))
""",
    # C7 -- random row split (groups straddle) vs split by group
    ("C7", "contaminated"): """
    gid = df["group_id"].to_numpy()
    perm = np.random.default_rng(7071).permutation(n)
    train_idx, test_idx = np.sort(perm[: n // 2]), np.sort(perm[n // 2:])
    X_train, y_train = X[train_idx], y[train_idx]
    X_test, y_test = X[test_idx], y[test_idx]
    model = LogisticRegression(max_iter=200).fit(X_train, y_train)
    print(model.score(X_test, y_test))
""",
    ("C7", "clean"): """
    gid = df["group_id"].to_numpy()
    train_idx = np.where(gid < 20)[0]
    test_idx = np.where(gid >= 20)[0]
    X_train, y_train = X[train_idx], y[train_idx]
    X_test, y_test = X[test_idx], y[test_idx]
    model = LogisticRegression(max_iter=200).fit(X_train, y_train)
    print(model.score(X_test, y_test))
""",
    # C8 -- test half from a shifted subpopulation vs the same distribution
    ("C8", "contaminated"): """
    X[n // 2:, 0] = X[n // 2:, 0] + 2.5           # test drawn from a shifted subpopulation
    X_train, X_test = X[: n // 2], X[n // 2:]
    y_train, y_test = y[: n // 2], y[n // 2:]
    model = LogisticRegression(max_iter=200).fit(X_train, y_train)
    print(model.score(X_test, y_test))
""",
    ("C8", "clean"): """
    X_train, X_test = X[: n // 2], X[n // 2:]
    y_train, y_test = y[: n // 2], y[n // 2:]
    model = LogisticRegression(max_iter=200).fit(X_train, y_train)
    print(model.score(X_test, y_test))
""",
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for (case, side), body in BODY.items():
        path = os.path.join(OUT, f"{case}_{side}.py")
        with open(path, "w") as f:
            f.write(HEAD + body + "\n\nrun()\n")
    print(f"wrote {len(BODY)} scripts to {OUT}")


if __name__ == "__main__":
    main()
