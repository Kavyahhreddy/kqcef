# Wind Intelligence

A full-stack dashboard for analysing UK national wind generation forecasts against actual generation for January 2026.

## Project status

This repository is being populated with the project source. The app uses a React + Vite frontend and a FastAPI/Python backend that retrieves wind forecast and generation data from Elexon BMRS and calculates forecast error metrics.

## Run locally with Docker

1. Install and start Docker Desktop.
2. From the repository root run:

```bash
docker compose up --build
```

3. Open the frontend at http://localhost:5173 and the API docs at http://localhost:8000/docs.

## Structure

- `frontend/` — React, Vite and Recharts dashboard
- `backend/` — FastAPI API, Elexon data access, analysis and tests
- `docs/` — demo script and submission checklist
- `docker-compose.yml` — local multi-service setup

## Data and methodology

The dashboard compares national wind actuals with forecast values and reports metrics including MAE, RMSE, bias and MAPE. Forecast selection uses a configurable publish-time cutoff. The default cutoff is an application assumption for this analysis, not a claim about an official Elexon deadline.

## Validation before submission

Verify that live Elexon responses cover the requested January 2026 period, run the backend tests, build the frontend, and test both services before publishing a deployed URL. The deployed app URL and demo video are not included here until they have actually been published.

## Demo

See `docs/DEMO_SCRIPT.md` for a customer overview and technical handover outline (maximum 10 minutes total), and `docs/SUBMISSION_CHECKLIST.md` for the final checks.