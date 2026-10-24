"""Command line interface: ``thermostat train`` and ``thermostat predict``."""
from __future__ import annotations

import argparse

import numpy as np

from . import __version__
from .data import daypart_flags, simulate
from .model import Model, fit, r2_score, rmse


def train(args: argparse.Namespace) -> int:
    X, y = simulate(args.rows, seed=args.seed)
    split = int(len(X) * 0.8)
    X_train, X_test, y_train, y_test = X[:split], X[split:], y[:split], y[split:]

    print(f"{len(X_train)} training rows, {len(X_test)} held-out rows (seed {args.seed})")
    best = None
    for name, interaction in (("linear", False), ("linear + comfort-gap interaction", True)):
        model = fit(X_train, y_train, interaction)
        pred = model.predict(X_test)
        print(f"  {name:<34} R2 = {r2_score(y_test, pred):.3f}   RMSE = {rmse(y_test, pred):.2f}")
        best = model
    best.save(args.out)  # the interaction model is the last one fitted
    print(f"Saved model to {args.out}")
    return 0


def predict(args: argparse.Namespace) -> int:
    model = Model.load(args.model)
    morning, noon, evening = daypart_flags(args.hour)
    row = [args.temperature, args.wind, args.humidity, args.preference, float(morning), float(noon), float(evening)]
    print(f"{float(model.predict(np.array([row]))[0]):.1f}")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="thermostat", description=__doc__)
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_train = sub.add_parser("train", help="simulate data, fit and evaluate models, save the best one")
    p_train.add_argument("--rows", type=int, default=20000)
    p_train.add_argument("--seed", type=int, default=42)
    p_train.add_argument("--out", default="web/model.json")
    p_train.set_defaults(func=train)

    p_pred = sub.add_parser("predict", help="predict the AC setting for one arrival")
    p_pred.add_argument("--model", default="web/model.json")
    p_pred.add_argument("--temperature", type=float, required=True, help="outside temperature, deg C")
    p_pred.add_argument("--wind", type=float, required=True, help="wind speed")
    p_pred.add_argument("--humidity", type=float, required=True, help="relative humidity, %%")
    p_pred.add_argument("--preference", type=float, required=True, help="guest's preferred temperature, deg C")
    p_pred.add_argument("--hour", type=int, required=True, help="arrival hour, 0-23")
    p_pred.set_defaults(func=predict)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
