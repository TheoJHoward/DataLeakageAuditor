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

    X[n // 2:, 0] = X[n // 2:, 0] + 2.5           # test drawn from a shifted subpopulation
    X_train, X_test = X[: n // 2], X[n // 2:]
    y_train, y_test = y[: n // 2], y[n // 2:]
    model = LogisticRegression(max_iter=200).fit(X_train, y_train)
    print(model.score(X_test, y_test))


run()
