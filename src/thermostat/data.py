"""Synthetic data that follows the generative process of the original Excel model (docs/excel-model.xlsx).

A guest arrives at a hotel at a given hour. The room should be at a comfortable temperature on arrival,
so the AC setting is predicted from the weather at the destination, the guest's preferred temperature
and the part of the day the guest arrives.
"""
from __future__ import annotations

import numpy as np

FEATURES = ["temperature", "wind", "humidity", "preference", "morning", "noon", "evening"]


def daypart_flags(hour):
    """Return (morning, noon, evening) indicators for an hour of the day (0-23). Night is all zeros."""
    hour = np.asarray(hour)
    morning = ((hour >= 4) & (hour < 10)).astype(float)
    noon = ((hour >= 10) & (hour < 16)).astype(float)
    evening = ((hour >= 16) & (hour < 22)).astype(float)
    return morning, noon, evening


def simulate(n: int, seed: int = 0):
    """Draw ``n`` synthetic arrivals.

    Returns ``(X, y)`` where ``X`` has one column per entry of :data:`FEATURES` and ``y`` is the AC setting
    (larger means stronger cooling).
    """
    rng = np.random.default_rng(seed)
    hour = rng.integers(0, 24, size=n)
    morning, noon, evening = daypart_flags(hour)

    temperature = rng.normal(18, 5, n) + 16 * noon + 10 * morning + 6 * evening
    wind = np.clip(rng.normal(11, 7, n) + 4 * evening + 2 * morning, 0, None)
    humidity = np.clip(rng.normal(70, 15, n) + 4 * evening + 2 * morning - 2 * noon, 0, 100)
    preference = rng.normal(22, 5, n)

    # Discomfort grows with the gap to the preferred temperature and is amplified by wind and humidity.
    mean = (temperature - preference) * (wind / 100 + humidity / 100)
    y = rng.normal(mean, 4)

    X = np.column_stack([temperature, wind, humidity, preference, morning, noon, evening])
    return X, y
