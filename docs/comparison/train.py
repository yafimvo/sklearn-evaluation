# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.8.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
import importlib

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn import metrics
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# + tags=["parameters"]
model = "sklearn.ensemble.RandomForestRegressor"
params = {"min_samples_leaf": 1, "n_estimators": 50}

# + tags=["model_name"]
model
# -

d = fetch_california_housing()
X, y = d["data"], d["target"]

tokens = model.split(".")
name, module = tokens[-1], ".".join(tokens[:-1])
class_ = getattr(importlib.import_module(module), name)

# + tags=["feature_names"]
list(d["feature_names"])
# -

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42
)

model = class_(**params)

# + tags=["model_params"]
model.get_params()
# -

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# + tags=["plot"]
ax = plt.gca()
sns.scatterplot(x=y_pred, y=y_test, ax=ax)
ax.grid()
# -

metrics_ = {
    "mae": metrics.mean_absolute_error(y_test, y_pred),
    "mse": metrics.mean_squared_error(y_test, y_pred),
    "r2": metrics.r2_score(y_test, y_pred),
}

# + tags=["metrics"]
pd.DataFrame(metrics_, index=[0])
# -

df = pd.DataFrame(X_test)
df.columns = d["feature_names"]
df["y_true"] = y_test
df["y_pred"] = y_pred
df["error_abs"] = np.abs(y_test - y_pred)
df["error_sq"] = np.square(y_test - y_pred)

# + tags=["houseage"]
error_age = df.groupby("HouseAge")[["error_abs", "error_sq"]].mean()
error_age.columns = ["mae", "mse"]


def r2_score(df):
    return metrics.r2_score(df.y_true, df.y_pred)


r2 = pd.DataFrame(df.groupby("HouseAge").apply(r2_score))
r2.columns = ["r2"]

error_age.merge(r2, on="HouseAge")
