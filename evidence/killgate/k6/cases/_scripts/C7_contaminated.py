import numpy as np
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

    gid = df["group_id"].to_numpy()
    perm = np.random.default_rng(7071).permutation(n)
    train_idx, test_idx = np.sort(perm[: n // 2]), np.sort(perm[n // 2:])
    X_train, y_train = X[train_idx], y[train_idx]
    X_test, y_test = X[test_idx], y[test_idx]
    model = LogisticRegression(max_iter=200).fit(X_train, y_train)
    print(model.score(X_test, y_test))


run()
