"""Ordinary least squares regression with an optional comfort-gap interaction term."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .data import FEATURES


def _design(X: np.ndarray, interaction: bool) -> np.ndarray:
    X = np.atleast_2d(np.asarray(X, dtype=float))
    cols = [np.ones(len(X)), *X.T]
    if interaction:
        temperature, wind, humidity, preference = X[:, 0], X[:, 1], X[:, 2], X[:, 3]
        cols.append((temperature - preference) * (wind + humidity) / 100)
    return np.column_stack(cols)


@dataclass
class Model:
    coefficients: list[float]  # intercept first, then FEATURES in order, then the interaction term if used
    interaction: bool = False

    def predict(self, X) -> np.ndarray:
        return _design(X, self.interaction) @ np.asarray(self.coefficients)

    def to_dict(self) -> dict:
        names = ["intercept", *FEATURES] + (["comfort_gap_x_wind_humidity"] if self.interaction else [])
        return {
            "interaction": self.interaction,
            "features": FEATURES,
            "coefficients": dict(zip(names, self.coefficients)),
        }

    def save(self, path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=2) + "\n")

    @classmethod
    def load(cls, path) -> "Model":
        data = json.loads(Path(path).read_text())
        return cls(list(data["coefficients"].values()), bool(data["interaction"]))


def fit(X, y, interaction: bool = False) -> Model:
    coefficients, *_ = np.linalg.lstsq(_design(X, interaction), np.asarray(y, dtype=float), rcond=None)
    return Model([float(c) for c in coefficients], interaction)


def r2_score(y_true, y_pred) -> float:
    y_true = np.asarray(y_true, dtype=float)
    residual = np.sum((y_true - np.asarray(y_pred)) ** 2)
    total = np.sum((y_true - y_true.mean()) ** 2)
    return float(1 - residual / total)


def rmse(y_true, y_pred) -> float:
    return float(np.sqrt(np.mean((np.asarray(y_true, dtype=float) - np.asarray(y_pred)) ** 2)))
