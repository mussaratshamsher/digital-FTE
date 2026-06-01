# Production Deployment Guide: Digital FTE Factory

This guide provides step-by-step instructions for deploying the **Digital FTE Factory SaaS** to the cloud using the VS Code Terminal.

## 1. Prerequisites
- Docker & Docker Compose installed.
- Cloud Provider CLI (e.g., `gcloud` for Google Cloud, `aws` for AWS, or `flyctl` for Fly.io).
- A valid `.env.production` file (see `deployment/.env.production.example`).

---

## 2. Local Production Testing
Before pushing to the cloud, verify the production build locally.

```powershell
# Navigate to deployment folder
cd phase-05/deployment

# Start production-ready containers
docker-compose -f docker-compose.prod.yml up --build
```

---

## 3. Cloud Deployment (Google Cloud Run Example)
Google Cloud Run is recommended for this project due to its excellent support for FastAPI and Next.js.

### A. Authenticate
```powershell
gcloud auth login
gcloud config set project [YOUR_PROJECT_ID]
```

### B. Deploy Backend (Phase-04)
```powershell
cd phase-04
gcloud builds submit --tag gcr.io/[PROJECT_ID]/fte-backend
gcloud run deploy fte-backend --image gcr.io/[PROJECT_ID]/fte-backend --platform managed
```

### C. Deploy Frontend (Phase-03)
*Note: Ensure `NEXT_PUBLIC_API_URL` in your env points to the Backend URL from Step B.*

```powershell
cd phase-03
gcloud builds submit --tag gcr.io/[PROJECT_ID]/fte-frontend
gcloud run deploy fte-frontend --image gcr.io/[PROJECT_ID]/fte-frontend --platform managed
```

---

## 4. Maintenance & Monitoring
- **Logs:** View logs directly in VS Code Terminal:
  `gcloud logs read --service fte-backend`
- **Updates:** Re-run the deploy commands; Cloud Run handles zero-downtime rollouts.
