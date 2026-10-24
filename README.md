# Thermostat setting prediction

Context-aware AC setting prediction for hotels: have the room at the right temperature when the guest walks in.
The model combines the weather at the destination, the guest's preferred temperature and the arrival time of day.

[![CI](https://github.com/aikitpete/thermostat-setting-prediction/actions/workflows/ci.yml/badge.svg)](https://github.com/aikitpete/thermostat-setting-prediction/actions/workflows/ci.yml)

Originally built in 2015 on a hosted ML service, with the model prototyped in a spreadsheet ([`docs/excel-model.xlsx`](docs/excel-model.xlsx)).
This version is self-contained: a small Python package, a reproducible simulation and a static web demo.

## How it works

1. **Simulate** arrivals with the same generative process as the spreadsheet (`src/thermostat/data.py`): weather depends on the time of day, guests have a preferred temperature, and the AC setting grows with the gap between outside temperature and preference, amplified by wind and humidity.
2. **Fit** two least-squares models with NumPy (`src/thermostat/model.py`): a plain linear model and one with an extra comfort-gap interaction term.
3. **Evaluate** on a held-out 20 % split and save the better model as `web/model.json`.
4. **Predict** from the CLI or from the static web page, which evaluates the saved coefficients in the browser.

Example output of `thermostat train` (seed 42, 20,000 simulated rows):

```
16000 training rows, 4000 held-out rows (seed 42)
  linear                             R2 = 0.759   RMSE = 4.25
  linear + comfort-gap interaction   R2 = 0.788   RMSE = 3.99
```

The data is synthetic, so the scores describe how well the model recovers the simulated process and not real hotel guests.
Replacing `simulate()` with real arrival, weather and preference data is the intended next step.

## Usage

```bash
pip install -e ".[dev]"

thermostat train                                   # writes web/model.json
thermostat predict --temperature 33 --wind 10 --humidity 70 --preference 22 --hour 13

cd web && python -m http.server                    # demo at http://localhost:8000
pytest
```

## Layout

```
src/thermostat/   data simulation, model, CLI
tests/            pytest suite (simulation, fitting, serialisation, CLI)
web/              static demo (index.html, predict.js, model.json)
docs/             original spreadsheet model
```

MIT licence.
