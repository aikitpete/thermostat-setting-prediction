(function () {
    'use strict';

    var model = null;
    var form = document.getElementById('form');
    var out = document.getElementById('result');

    function daypart(hour) {
        return {
            morning: hour >= 4 && hour < 10 ? 1 : 0,
            noon: hour >= 10 && hour < 16 ? 1 : 0,
            evening: hour >= 16 && hour < 22 ? 1 : 0
        };
    }

    function predict(m, v) {
        var c = m.coefficients;
        var d = daypart(v.hour);
        var y = c.intercept
            + c.temperature * v.temperature + c.wind * v.wind + c.humidity * v.humidity + c.preference * v.preference
            + c.morning * d.morning + c.noon * d.noon + c.evening * d.evening;
        if (m.interaction) {
            y += c.comfort_gap_x_wind_humidity * (v.temperature - v.preference) * (v.wind + v.humidity) / 100;
        }
        return y;
    }

    function update() {
        if (!model || !form.checkValidity()) { out.textContent = '–'; return; }
        var f = new FormData(form);
        var time = String(f.get('time')).split(':');
        out.textContent = predict(model, {
            temperature: parseFloat(f.get('temperature')),
            wind: parseFloat(f.get('wind')),
            humidity: parseFloat(f.get('humidity')),
            preference: parseFloat(f.get('preference')),
            hour: parseInt(time[0], 10)
        }).toFixed(1);
    }

    form.addEventListener('input', update);
    fetch('model.json')
        .then(function (r) { return r.json(); })
        .then(function (m) { model = m; update(); })
        .catch(function () { out.textContent = 'model.json could not be loaded (serve this folder over HTTP)'; });
})();
