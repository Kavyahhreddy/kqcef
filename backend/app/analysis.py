import os
import numpy as np
import pandas as pd

CUTOFF_HOURS = float(os.getenv("DECISION_CUTOFF_HOURS_BEFORE_DELIVERY", "12"))

def select_forecasts(forecasts: pd.DataFrame, cutoff_hours: float = CUTOFF_HOURS) -> pd.DataFrame:
    """Select latest forecast published at or before delivery start minus cutoff."""
    columns = ["startTime", "publishTime", "forecast"]
    if forecasts.empty:
        return pd.DataFrame(columns=columns)
    df = forecasts.copy()
    df["startTime"] = pd.to_datetime(df["startTime"], utc=True, errors="coerce")
    df["publishTime"] = pd.to_datetime(df["publishTime"], utc=True, errors="coerce")
    df["forecast"] = pd.to_numeric(df["forecast"], errors="coerce")
    df = df.dropna(subset=["startTime", "publishTime", "forecast"])
    df["decision_cutoff"] = df["startTime"] - pd.to_timedelta(cutoff_hours, unit="h")
    df = df[df["publishTime"] <= df["decision_cutoff"]]
    df = df.sort_values(["startTime", "publishTime"])
    return df.drop_duplicates(subset=["startTime"], keep="last")[columns]

def build_observations(actuals: pd.DataFrame, forecasts: pd.DataFrame, cutoff_hours: float = CUTOFF_HOURS) -> pd.DataFrame:
    columns = ["startTime", "publishTime", "forecast", "actual", "error"]
    selected = select_forecasts(forecasts, cutoff_hours)
    if actuals.empty or selected.empty:
        return pd.DataFrame(columns=columns)
    actual = actuals.copy()
    actual["startTime"] = pd.to_datetime(actual["startTime"], utc=True, errors="coerce")
    actual["actual"] = pd.to_numeric(actual["actual"], errors="coerce")
    actual = actual.dropna(subset=["startTime", "actual"])
    actual = actual.groupby("startTime", as_index=False)["actual"].mean()
    result = selected.merge(actual, on="startTime", how="inner")
    result["error"] = result["forecast"] - result["actual"]
    return result.sort_values("startTime").reset_index(drop=True)

def calculate_metrics(observations: pd.DataFrame) -> dict:
    if observations.empty:
        return {"mae": None, "rmse": None, "bias": None, "mape": None, "observations": 0}
    df = observations[["forecast", "actual"]].copy()
    df = df.replace([np.inf, -np.inf], np.nan).dropna()
    if df.empty:
        return {"mae": None, "rmse": None, "bias": None, "mape": None, "observations": 0}
    error = df["forecast"] - df["actual"]
    nonzero = df["actual"].abs() > 1e-9
    mape = float((error[nonzero].abs() / df.loc[nonzero, "actual"].abs()).mean() * 100) if nonzero.any() else None
    return {
        "mae": round(float(error.abs().mean()), 3),
        "rmse": round(float(np.sqrt((error ** 2).mean())), 3),
        "bias": round(float(error.mean()), 3),
        "mape": round(mape, 3) if mape is not None else None,
        "observations": int(len(df)),
    }

def iso_records(df: pd.DataFrame) -> list[dict]:
    if df.empty:
        return []
    out = df.copy()
    for col in ("startTime", "publishTime"):
        if col in out.columns:
            out[col] = pd.to_datetime(out[col], utc=True, errors="coerce").map(
                lambda value: value.isoformat().replace("+00:00", "Z") if pd.notna(value) else None
            )
    for col in ("forecast", "actual", "error"):
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    out = out.astype(object).where(pd.notna(out), None)
    return out.to_dict(orient="records")