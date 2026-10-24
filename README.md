# Wind Intelligence

A full-stack dashboard for analysing UK national wind generation forecasts against actual generation for January 2026. Built for a full-stack software engineering challenge.

## Stack

- **Frontend:** React, Vite, Recharts, Lucide
- **Backend:** Python, FastAPI, pandas, NumPy, httpx
- **Data source:** Elexon BMRS API
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

The application joins national wind actuals to forecasts using delivery start time. For each delivery interval, the analysis selects the latest forecast published at or before the configured cutoff, then reports mean absolute error (MAE), root mean square error (RMSE), signed bias, MAPE where actual values are non-zero, and the number of matched observations.

The default cutoff is **12 hours before delivery** and is an explicit analytical assumption for this challenge, not a claim about an official market deadline. Change `DECISION_CUTOFF_HOURS_BEFORE_DELIVERY` to configure it.

## API endpoints

- `GET /api/health` — service health
- `GET /api/accuracy?start=2026-01-01&end=2026-01-31` — metrics and matched time series
- `GET /api/observations?date=2026-01-15` — observations for a delivery date
- `GET /api/forecasts?date=2026-01-15` — matched series for a delivery date

## Verify before relying on results

Elexon data schemas and query parameters can evolve. Before final submission, confirm that the current FUELHH and WINDFOR endpoints return records for January 2026 and that the response fields match the adapter. Do not treat an empty dataset or an API error as evidence of zero wind generation. Run the tests and build the frontend before recording a demo.

Backend tests can be run locally from the `backend` directory:

```bash
python -m pip install -r requirements.txt
pytest -q
```

Frontend build can be checked from the `frontend` directory:

```bash
npm install
npm run build
```

## Deployment and demo

No live deployment URL or demo video is claimed by this repository yet. Add only real, tested public URLs here after deploying the frontend and backend and uploading the unlisted video.

- Live app: **pending deployment**
- Demo video: **pending recording and upload**

The recording guide in `docs/DEMO_SCRIPT.md` is designed for a customer overview (up to 5 minutes) followed by a technical handover (up to 5 minutes).

## AI assistance disclosure

OpenAI ChatGPT was used to assist with project scaffolding, implementation drafting, test correction, and documentation. The project should be personally reviewed, run, and validated before submission.
