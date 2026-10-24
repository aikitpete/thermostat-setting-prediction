import numpy as np

from thermostat import FEATURES, daypart_flags, fit, r2_score, rmse, simulate
from thermostat.cli import main
from thermostat.model import Model


def test_daypart_flags_cover_the_day_without_overlap():
    hours = np.arange(24)
    morning, noon, evening = daypart_flags(hours)
    assert (morning + noon + evening).max() == 1
    assert morning[4] == 1 and noon[10] == 1 and evening[16] == 1
    assert (morning + noon + evening)[[0, 3, 22, 23]].sum() == 0  # night


def test_simulation_is_reproducible_and_shaped():
    X1, y1 = simulate(500, seed=7)
    X2, y2 = simulate(500, seed=7)
    assert X1.shape == (500, len(FEATURES)) and y1.shape == (500,)
    assert np.array_equal(X1, X2) and np.array_equal(y1, y2)
    assert X1[:, 2].min() >= 0 and X1[:, 2].max() <= 100


def test_fit_recovers_a_known_linear_relationship():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(400, len(FEATURES)))
    true = np.array([2.0, 1.0, -0.5, 0.0, -1.2, 0.3, 0.0, 0.4])
    y = np.column_stack([np.ones(400), X]) @ true
    model = fit(X, y)
    assert np.allclose(model.coefficients, true, atol=1e-8)


def test_interaction_model_beats_linear_on_held_out_data():
    X, y = simulate(8000, seed=3)
    Xtr, Xte, ytr, yte = X[:6000], X[6000:], y[:6000], y[6000:]
    linear = rmse(yte, fit(Xtr, ytr).predict(Xte))
    interaction = rmse(yte, fit(Xtr, ytr, interaction=True).predict(Xte))
    assert interaction < linear
    assert r2_score(yte, fit(Xtr, ytr, interaction=True).predict(Xte)) > 0.8


def test_model_round_trips_through_json(tmp_path):
    X, y = simulate(1000, seed=5)
    model = fit(X, y, interaction=True)
    path = tmp_path / "model.json"
    model.save(path)
    loaded = Model.load(path)
    assert np.allclose(model.predict(X[:10]), loaded.predict(X[:10]))


def test_cli_train_and_predict(tmp_path, capsys):
    out = tmp_path / "model.json"
    assert main(["train", "--rows", "3000", "--out", str(out)]) == 0
    capsys.readouterr()
    assert main(["predict", "--model", str(out), "--temperature", "35", "--wind", "10", "--humidity", "70",
                 "--preference", "22", "--hour", "13"]) == 0
    hot = float(capsys.readouterr().out)
    assert main(["predict", "--model", str(out), "--temperature", "20", "--wind", "10", "--humidity", "70",
                 "--preference", "22", "--hour", "13"]) == 0
    mild = float(capsys.readouterr().out)
    assert hot > mild
