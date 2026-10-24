# Wind Intelligence — demo script (maximum 10 minutes)

Prepare the app before recording and keep the two requested sections within 10 minutes total.

## Part 1 — Customer overview (up to 5 minutes)

1. Introduce the challenge: compare UK national wind generation forecasts with actual wind output for January 2026.
2. Show the overview page and date period.
3. Explain the four headline measures: MAE is average absolute error; RMSE weights larger misses more heavily; bias indicates whether forecasts trend high or low; matched intervals shows the number of paired records.
4. Explain the line chart: forecast and actual generation are aligned by delivery interval.
5. Explain why a forecast publication cutoff is needed to avoid selecting a forecast published after the decision point.

## Part 2 — Technical handover (up to 5 minutes)

1. Show the repository structure: React + Vite + Recharts frontend, FastAPI backend, analysis logic, tests, and Docker Compose.
2. Walk through the Elexon data adapter and its validation of returned fields.
3. Explain that each forecast is selected by delivery time and publication time, then joined to actuals by startTime.
4. Show API routes: /api/health, /api/accuracy, /api/observations, and /api/forecasts. The OpenAPI page is available at /docs when backend is running locally.
5. Show the unit tests and Docker command: docker compose up --build.

## Before recording

- Verify actuals and forecasts are returned by the current Elexon API for January 2026.
- Confirm API filters and response schema against the current official API documentation; do not claim the live integration has been verified until you have checked it.
- Run backend tests and build the frontend.
- Use the deployed app, not localhost, for the customer segment.
- Keep total video under 10 minutes; upload as Unlisted and test playback in an incognito window.
- Do not claim the app is publicly deployed until a real public deployment URL exists.