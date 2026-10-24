import pandas as pd
from app.analysis import select_forecasts, build_observations, calculate_metrics

def test_select_latest_eligible_forecast():
    forecasts = pd.DataFrame([
        {"startTime": "2026-01-02T12:00:00Z", "publishTime": "2026-01-01T00:00:00Z", "forecast": 100},
        {"startTime": "2026-01-02T12:00:00Z", "publishTime": "2026-01-02T01:00:00Z", "forecast": 200},
        {"startTime": "2026-01-02T12:00:00Z", "publishTime": "2026-01-02T03:00:00Z", "forecast": 300},
        {"startTime": "2026-01-02T12:00:00Z", "publishTime": "2026-01-02T05:00:00Z", "forecast": 400},
    ])
    selected = select_forecasts(forecasts, cutoff_hours=8)
    assert len(selected) == 1
    assert selected.iloc[0]["forecast"] == 300

def test_metrics():
    obs = pd.DataFrame([{"forecast": 110, "actual": 100}, {"forecast": 90, "actual": 100}])
    result = calculate_metrics(obs)
    assert result["mae"] == 10
    assert result["rmse"] == 10
    assert result["bias"] == 0
    assert result["observations"] == 2

def test_join_actuals():
    actuals = pd.DataFrame([{"startTime": "2026-01-02T12:00:00Z", "actual": 100}])
    forecasts = pd.DataFrame([{"startTime": "2026-01-02T12:00:00Z", "publishTime": "2026-01-01T00:00:00Z", "forecast": 110}])
    result = build_observations(actuals, forecasts, cutoff_hours=8)
    assert len(result) == 1
    assert result.iloc[0]["error"] == 10