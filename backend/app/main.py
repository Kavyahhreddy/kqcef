import os
from datetime import date
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from app.elexon import fetch_actuals, fetch_forecasts, ElexonError
from app.analysis import build_observations, calculate_metrics, iso_records, CUTOFF_HOURS

app = FastAPI(title="Wind Intelligence API", description="UK national wind forecast accuracy analysis.", version="1.0.0")
origins = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False, allow_methods=["GET"], allow_headers=["*"])

@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "wind-intelligence-api"}

async def _get_observations(start_date: date, end_date: date):
    if start_date < date(2026, 1, 1) or end_date > date(2026, 1, 31):
        raise HTTPException(status_code=400, detail="This challenge app is scoped to January 2026.")
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Start date must be on or before end date.")
    try:
        actuals = await fetch_actuals(start_date, end_date)
        forecasts = await fetch_forecasts(start_date, end_date)
        return build_observations(actuals, forecasts)
    except ElexonError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

@app.get("/api/observations")
async def observations(delivery_date: date = Query(..., alias="date", description="Delivery date, YYYY-MM-DD")):
    obs = await _get_observations(delivery_date, delivery_date)
    return {"date": delivery_date.isoformat(), "cutoff_hours_before_delivery": CUTOFF_HOURS, "count": len(obs), "observations": iso_records(obs)}

@app.get("/api/accuracy")
async def accuracy(start: date = Query(date(2026, 1, 1)), end: date = Query(date(2026, 1, 31))):
    obs = await _get_observations(start, end)
    return {"start": start.isoformat(), "end": end.isoformat(), "cutoff_hours_before_delivery": CUTOFF_HOURS, "metrics": calculate_metrics(obs), "observations": iso_records(obs)}

@app.get("/api/forecasts")
async def forecasts(delivery_date: date = Query(..., alias="date", description="Delivery date, YYYY-MM-DD")):
    obs = await _get_observations(delivery_date, delivery_date)
    return {"date": delivery_date.isoformat(), "cutoff_hours_before_delivery": CUTOFF_HOURS, "forecasts": iso_records(obs)}