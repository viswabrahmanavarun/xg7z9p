# Renewable Generation Forecast Dashboard

## Overview

This repository contains a full‑stack web application that helps a UK energy utility team:
1. **View the latest national wind generation forecasts** (Elexon `WINDFOR` dataset) alongside actual wind generation (`FUELHH` dataset).
2. **Evaluate forecast accuracy** for a selected day (MAE, RMSE, bias) so the team can incorporate forecast error into day‑ahead market buying decisions.

The solution is built with:
- **React (TypeScript) + Vite** for the frontend UI.
- **Python FastAPI** for the backend API that fetches, caches, and aggregates the Elexon BMRS data.
- **Docker** for containerised development and production.
- **GitHub Actions** CI/CD that builds Docker images and deploys the backend to **Heroku** and the frontend to **Vercel**.
- A short demo video (unlisted YouTube) split into a client‑pitch and a technical‑review part.

> **AI‑assistance disclaimer**: This project scaffolding was generated with the assistance of the Antigravity AI coding assistant.

---
## Repository Structure

```
renewable-forecast-dashboard/
├─ backend/                # FastAPI backend
│  ├─ app/
│  │  ├─ __init__.py
│  │  ├─ main.py          # FastAPI entry point
│  │  ├─ fetcher.py       # Data fetching & caching
│  │  ├─ metrics.py       # Accuracy calculations
│  │  └─ models.py        # Pydantic schemas
│  ├─ requirements.txt
│  ├─ Dockerfile
│  └─ tests/               # pytest suite
│     └─ test_fetcher.py
│     └─ test_metrics.py
├─ frontend/               # React + Vite UI
│  ├─ src/
│  │  ├─ main.tsx
│  │  ├─ App.tsx
│  │  ├─ api.ts           # Backend API wrapper
│  │  └─ components/
│  │     ├─ Dashboard.tsx
│  │     └─ MetricsTable.tsx
│  ├─ index.html
│  ├─ vite.config.ts
│  ├─ package.json
│  └─ tsconfig.json
├─ docker-compose.yml       # Local development stack
├─ .github/
│  └─ workflows/
│     └─ ci.yml            # CI/CD workflow
├─ .gitignore
└─ README.md               # (this file)
```

---
## Getting Started (Local Development)

### Prerequisites
- Docker Desktop (or Docker Engine)
- Node.js ≥ 18
- Python ≥ 3.10

### Spin up the stack
```bash
# Clone the repo (replace with the actual URL once created)
git clone https://github.com/your‑org/kjhwr.git
cd kjhwr

# Build and run both services
docker compose up --build
```
The backend will be reachable at `http://localhost:8000` and the frontend at `http://localhost:5173`.

### Backend only
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
### Frontend only
```bash
cd frontend
npm install
npm run dev
```
---
## API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/forecasts?date=YYYY-MM-DD` | Returns 30‑min interval wind forecasts for the given day (UTC). |
| `GET` | `/actuals?date=YYYY-MM-DD` | Returns 30‑min interval actual wind generation for the day. |
| `GET` | `/metrics?date=YYYY-MM-DD` | Calculates MAE, RMSE and bias between forecast and actual for the day. |

All responses follow the schema defined in `backend/app/models.py`.
---
## Deployment
### Backend (Heroku)
1. Install the Heroku CLI and log in.
2. Create an app: `heroku create <app‑name>`
3. Push the Docker image:
   ```bash
   heroku container:login
   heroku container:push web -a <app‑name>
   heroku container:release web -a <app‑name>
   ```
4. Set env var `ELEXON_API_KEY` (if you have one) via `heroku config:set`.

### Frontend (Vercel)
1. Install Vercel CLI: `npm i -g vercel`
2. Inside `frontend` run `vercel` and follow the prompts.
3. Link the Vercel project to the GitHub repo for automatic deployments on push.
---
## Testing
### Backend
```bash
cd backend
pytest
```
### Frontend
```bash
cd frontend
npm test
```
---
## Demo Video
A short (≤10 min) video is hosted on YouTube (unlisted):
[Demo Video Link]([PLACEHOLDER_FOR_YOUTUBE_LINK])

---
## License
MIT License.

---
## Contact
For any questions or further customisation, please reach out to the development team.
