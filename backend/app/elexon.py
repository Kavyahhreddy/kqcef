import os
from datetime import date, datetime, timedelta, timezone
from typing import Any
import httpx
import pandas as pd

BASE_URL = os.getenv("ELEXON_BASE_URL", "https://data.elexon.co.uk/bmrs/api/v1").rstrip("/")
ACTUALS_PATH = os.getenv("ELEXON_ACTUALS_PATH", "/datasets/FUELHH/stream")
FORECASTS_PATH = os.getenv("ELEXON_FORECASTS_PATH", "/datasets/WINDFOR/stream")

class ElexonError(RuntimeError):
    pass

def _records(payload: Any) -> list[dict]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("data", "results", "result"):
            if isinstance(payload.get(key), list):
                return payload[key]
    raise ElexonError(f"Unexpected Elexon response shape: {type(payload).__name__}")

async def _get(path: str, params: dict) -> list[dict]:
    url = f"{BASE_URL}/{path.lstrip('/')}"
    try:
        async with httpx.AsyncClient(timeout=90, follow_redirects=True) as client:
            response = await client.get(url, params=params, headers={"Accept": "application/json"})
            response.raise_for_status()
            return _records(response.json())
    except httpx.HTTPStatusError as exc:
        raise ElexonError(f"Elexon returned HTTP {exc.response.status_code}: {exc.response.text[:300]}") from exc
    except (httpx.HTTPError, ValueError) as exc:
        raise ElexonError(f"Could not retrieve or parse Elexon data: {exc}") from exc

async def fetch_actuals(start_date: date, end_date: date) -> pd.DataFrame:
    rows = await _get(ACTUALS_PATH, {
        "settlementDateFrom": start_date.isoformat(),
        "settlementDateTo": end_date.isoformat(),
        "format": "json",
    })
    df = pd.DataFrame(rows)
    if df.empty:
        return pd.DataFrame(columns=["startTime", "actual"])
    if "fuelType" not in df.columns:
        raise ElexonError("FUELHH response has no fuelType field; inspect the live API response.")
    df = df[df["fuelType"].astype(str).str.upper().eq("WIND")].copy()
    if not {"startTime", "generation"}.issubset(df.columns):
        raise ElexonError("FUELHH response must contain startTime and generation.")
    df["startTime"] = pd.to_datetime(df["startTime"], utc=True, errors="coerce")
    df["actual"] = pd.to_numeric(df["generation"], errors="coerce")
    df = df.dropna(subset=["startTime", "actual"])
    return df[["startTime", "actual"]].groupby("startTime", as_index=False).mean()

async def fetch_forecasts(start_date: date, end_date: date) -> pd.DataFrame:
    start = datetime.combine(start_date - timedelta(days=1), datetime.min.time(), tzinfo=timezone.utc)
    end = datetime.combine(end_date + timedelta(days=1), datetime.min.time(), tzinfo=timezone.utc)
    rows = await _get(FORECASTS_PATH, {
        "from": start.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "to": end.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "format": "json",
    })
    df = pd.DataFrame(rows)
    if df.empty:
        return pd.DataFrame(columns=["startTime", "publishTime", "forecast"])
    required = {"startTime", "publishTime", "generation"}
    if not required.issubset(df.columns):
        raise ElexonError("WINDFOR response must include startTime, publishTime and generation; got: " + ", ".join(map(str, df.columns)))
    df["startTime"] = pd.to_datetime(df["startTime"], utc=True, errors="coerce")
    df["publishTime"] = pd.to_datetime(df["publishTime"], utc=True, errors="coerce")
    df["forecast"] = pd.to_numeric(df["generation"], errors="coerce")
    df = df.dropna(subset=["startTime", "publishTime", "forecast"])
    lower = pd.Timestamp(start_date, tz="UTC")
    upper = pd.Timestamp(end_date + timedelta(days=1), tz="UTC")
    df = df[(df["startTime"] >= lower) & (df["startTime"] < upper)]
    return df[["startTime", "publishTime", "forecast"]]