# Wind Intelligence

A full-stack dashboard for analysing UK national wind generation forecasts against actual generation for January 2026. Built for a full-stack software engineering challenge.

## Stack

- **Frontend:** React, Vite, Recharts, Lucide
- **Backend:** Python, FastAPI, pandas, NumPy, httpx
- **Data source:** Elexon BMRS API (`WINDFOR` hourly wind forecasts matched to `FUELHH` half-hourly actual generation)
- **Local orchestration:** Docker Compose

## Run locally

1. Install and start Docker Desktop.
2. From the project root, run:

   ```bash
   docker compose up --build
   ```

3. Open the dashboard at **http://localhost:5173**.
4. Check API health at **http://localhost:8000/api/health** and interactive API docs at **http://localhost:8000/docs**.

To stop the services, run `docker compose down`.

## Project structure

```text
.
├── backend/
│   ├── app/
│   │   ├── analysis.py       # forecast selection and error metrics
│   │   ├── elexon.py         # Elexon API retrieval and validation
│   │   ├── main.py           # FastAPI endpoints
│   │   └── schemas.py
│   ├── tests/test_analysis.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # dashboard UI and visualisations
│   │   ├── api.js            # API client
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── Dockerfile
│   └── package.json
├── docs/
│   ├── DEMO_SCRIPT.md
│   └── SUBMISSION_CHECKLIST.md
├── docker-compose.yml
└── .env.example
```

## Analysis

The application compares Elexon's hourly `WINDFOR` national wind forecasts with `FUELHH` half-hourly actual generation. The data is matched on the forecast delivery start timestamps, so the hourly forecast cadence yields 24 expected matches per complete day (744 for the 31 days of January 2026). For each forecast timestamp, the analysis selects the latest forecast published at or before the configured cutoff, then reports mean absolute error (MAE), root mean square error (RMSE), signed bias, MAPE where actual values are non-zero, and the number of matched forecast/actual observations.

The default cutoff is **12 hours before delivery** and is an explicit analytical assumption for this challenge, not a claim about an official market deadline. Change `DECISION_CUTOFF_HOURS_BEFORE_DELIVERY` to configure it.

## API endpoints

- `GET /api/health` — service health
- `GET /api/accuracy?start=2026-01-01&end=2026-01-31` — metrics and matched time series
- `GET /api/observations?date=2026-01-15` — observations for a delivery date
- `GET /api/forecasts?date=2026-01-15` — matched series for a delivery date

## AI assistance disclosure

OpenAI ChatGPT was used to assist with project scaffolding, implementation drafting, test correction, and documentation. The project should be personally reviewed, run, and validated before submission.
