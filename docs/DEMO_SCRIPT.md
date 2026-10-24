# Wind Intelligence — demo script (maximum 10 minutes)

The assignment asks for two sections: a customer overview (up to 5 minutes) and a technical handover (up to 5 minutes).

## Part 1 — Customer overview (up to 5 minutes)

1. Introduce the objective: compare UK national wind generation forecasts with actual wind output for January 2026.
2. Show the dashboard and the January 2026 reporting window.
3. Explain the headline measures:
   - **MAE:** average absolute forecast error.
   - **RMSE:** weighs larger errors more heavily.
   - **Bias:** indicates whether forecasts tend to be high or low.
   - **Matched intervals:** count of forecast/actual pairs.
4. Walk through the line chart and explain that both series are matched by delivery interval.
5. Explain why forecast publication time matters: a fair comparison should not use a forecast published after the assumed decision cutoff.

## Part 2 — Technical handover (up to 5 minutes)

1. Show the repository structure: React/Vite/Recharts frontend, FastAPI backend, analysis module, tests, and Docker Compose.
2. Walk through the Elexon adapter and its validation of the fields returned by the API.
3. Explain the forecast-selection rule: select the latest eligible publish time for each delivery start, then join to actuals.
4. Show `/api/health`, `/api/accuracy`, `/api/observations`, and `/api/forecasts`; the local OpenAPI page is `/docs`.
5. Show the tests and the startup command `docker compose up --build`.
6. Briefly describe limitations, including the configured cutoff assumption and the need to validate current live endpoint parameters.

## Before recording

- Verify Elexon actuals and forecast responses for January 2026.
- Run backend tests and the frontend production build.
- Confirm the deployed site loads and its API is reachable from an incognito window.
- Use the deployed application for the customer overview, not localhost.
- Keep the entire recording under 10 minutes, upload as **Unlisted**, and test playback in an incognito window.
- Do not claim the application is deployed until a real public URL exists.
