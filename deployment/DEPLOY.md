# FirmVault Mission Control — Deployment Guide

## Architecture

```
┌─────────────────────┐     ┌──────────────────────────────┐
│   llm-lawyer.com    │     │  Render.com                  │
│   (Netlify)         │────▶│  MC Backend (FastAPI)        │
│   Next.js Frontend  │     │  PostgreSQL + Redis          │
└─────────────────────┘     └──────────────┬───────────────┘
                                           │
                                           │ API
                                           ▼
                            ┌──────────────────────────────┐
                            │  FirmVault repo (GitHub)     │
                            │  state.yaml ← engine         │
                            │  PHASE_DAG ← definitions     │
                            │  materializer bridge → MC    │
                            └──────────────────────────────┘
```

## Step 1: Fork Mission Control

Go to https://github.com/abhi1693/openclaw-mission-control and click **Fork**.
Name it `firmvault-mission-control` under your Whaleylaw account.

## Step 2: Deploy Backend on Render

1. Go to https://dashboard.render.com
2. Click **New** → **Blueprint**
3. Connect your `Whaleylaw/firmvault-mission-control` repo
4. Render will read the `render.yaml` below (add it to the repo root)
5. Fill in the environment variables when prompted
6. Click **Apply**

### render.yaml (add to repo root)

```yaml
services:
  - type: web
    name: firmvault-mc-backend
    runtime: docker
    dockerfilePath: backend/Dockerfile
    dockerContext: .
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: firmvault-mc-db
          property: connectionString
      - key: CORS_ORIGINS
        value: https://llm-lawyer.com
      - key: DB_AUTO_MIGRATE
        value: "true"
      - key: AUTH_MODE
        value: local
      - key: LOCAL_AUTH_TOKEN
        generateValue: true
      - key: BASE_URL
        sync: false  # set after deploy: https://firmvault-mc-backend.onrender.com
      - key: RQ_REDIS_URL
        fromService:
          name: firmvault-mc-redis
          type: redis
          property: connectionString
      - key: LOG_LEVEL
        value: INFO
    healthCheckPath: /health
    plan: starter

  - type: redis
    name: firmvault-mc-redis
    plan: starter
    maxmemoryPolicy: allkeys-lru

databases:
  - name: firmvault-mc-db
    plan: starter
    postgresMajorVersion: "16"
```

### After deploy, note:
- **Backend URL**: something like `https://firmvault-mc-backend.onrender.com`
- **LOCAL_AUTH_TOKEN**: Render auto-generated it. Copy it from the dashboard → Environment.

## Step 3: Deploy Frontend on Netlify (llm-lawyer.com)

1. Go to https://app.netlify.com
2. Create new site from GitHub → select your `firmvault-mission-control` fork
3. Set **Base directory**: `frontend`
4. Set **Build command**: `npm run build`
5. Set **Publish directory**: `frontend/.next`
6. Add environment variable:
   - `NEXT_PUBLIC_API_URL` = `https://firmvault-mc-backend.onrender.com`
7. Under **Domain management**, add your custom domain: `llm-lawyer.com`
8. Deploy

### netlify.toml (add to repo root)

```toml
[build]
  base = "frontend"
  command = "npm run build"
  publish = ".next"

[build.environment]
  NODE_VERSION = "22"

# Next.js SSR needs the Netlify Next.js plugin
[[plugins]]
  package = "@netlify/plugin-nextjs"
```

### Install the Netlify Next.js plugin

In the `frontend/` directory:
```bash
npm install -D @netlify/plugin-nextjs
```

## Step 4: Configure Auth

Mission Control uses `AUTH_MODE=local` with a bearer token. To access the UI:

1. Copy the `LOCAL_AUTH_TOKEN` from Render
2. In the browser, navigate to `https://llm-lawyer.com`
3. The UI should prompt for authentication — enter the token
4. Bookmark it / save in password manager

## Step 5: Wire the Engine Bridge

The materializer bridge runs as a cron job (Render Cron or GitHub Actions) that:
1. Clones/pulls FirmVault
2. Runs the engine to compute available work
3. POSTs tasks to Mission Control API
4. When MC tasks are approved, writes back to state.yaml and pushes

The bridge script lives at `skills.tools.workflows/runtime/mc_bridge.py` in FirmVault.

## Environment Variables Summary

| Where | Variable | Value |
|-------|----------|-------|
| Render Backend | `DATABASE_URL` | Auto from Render Postgres |
| Render Backend | `CORS_ORIGINS` | `https://llm-lawyer.com` |
| Render Backend | `AUTH_MODE` | `local` |
| Render Backend | `LOCAL_AUTH_TOKEN` | Auto-generated |
| Render Backend | `BASE_URL` | `https://firmvault-mc-backend.onrender.com` |
| Render Backend | `RQ_REDIS_URL` | Auto from Render Redis |
| Netlify Frontend | `NEXT_PUBLIC_API_URL` | `https://firmvault-mc-backend.onrender.com` |
