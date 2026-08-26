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

    x = df["x"].to_numpy(dtype=float) if "x" in df else X[:, 0]
    win5 = pd.Series(x).shift(1).rolling(5, min_periods=5).mean().to_numpy()   # ends at t-1
    X = win5.reshape(-1, 1)
    ok = ~np.isnan(win5)
    X_train, X_test = X[ok][: n // 3], X[ok][n // 3:]
    y_train, y_test = y[ok][: n // 3], y[ok][n // 3:]
    model = LogisticRegression(max_iter=200).fit(X_train, y_train)
    print(model.score(X_test, y_test))


run()
