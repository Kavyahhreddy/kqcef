# Submission checklist

- [ ] Start Docker Desktop and run `docker compose up --build`.
- [ ] Check `http://localhost:8000/api/health`.
- [ ] Run backend tests with `pytest -q` from the backend directory.
- [ ] Run `npm install` and `npm run build` from the frontend directory.
- [ ] Verify Elexon FUELHH and WINDFOR endpoint parameters and data fields for January 2026.
- [ ] Confirm metrics are calculated from matched real values, not an empty response.
- [ ] Deploy the frontend and backend; configure `VITE_API_BASE_URL` and backend CORS origins.
- [ ] Test the public app in an incognito window.
- [ ] Record the customer overview (maximum 5 minutes) and technical handover (maximum 5 minutes).
- [ ] Upload the demo as Unlisted and test its URL in an incognito window.
- [ ] Update README with confirmed public URLs only.
- [ ] Submit the public GitHub repository URL, deployed app URL, and demo video URL.

Do not submit placeholder URLs. Check an item only after it has actually been verified.
