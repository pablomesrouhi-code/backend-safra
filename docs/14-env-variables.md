# 14 — Environment Variables

## Frontend (`frontend/.env.example`)

Copy to Easypanel → frontend service env.

```bash
# Site
NEXT_PUBLIC_SITE_URL=https://safraskin.online
NEXT_PUBLIC_API_URL=https://api.safraskin.online

# Pixels (browser — public IDs only)
NEXT_PUBLIC_META_PIXEL_ID=
NEXT_PUBLIC_TIKTOK_PIXEL_ID=
NEXT_PUBLIC_SNAP_PIXEL_ID=

# Optional analytics
NEXT_PUBLIC_GA4_ID=

# Feature flags
NEXT_PUBLIC_UPSELL_TIMER_SECONDS=12
```

## Backend (`backend/.env.example`)

Copy to Easypanel → backend service env.

```bash
# Database (Easypanel internal)
DATABASE_URL=postgres://postgres:s4eagoems3oueizu0h00@safraskin_database:5432/safraskin?sslmode=disable

# Server
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=https://safraskin.online,https://www.safraskin.online

# Google Sheets webhook (Apps Script deployment URL — no secret)
# Sheet: https://docs.google.com/spreadsheets/d/12UOny_tW2vOVclTSe-jLoMeI_KqYZPGZ3TyfjyxBWWw/edit
GOOGLE_SHEETS_WEBHOOK_URL=https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec
ORDER_NUMBER_PREFIX=nama

# Meta Conversions API
META_PIXEL_ID=
META_ACCESS_TOKEN=
META_TEST_EVENT_CODE=

# TikTok Events API
TIKTOK_PIXEL_ID=
TIKTOK_ACCESS_TOKEN=

# Snapchat Conversions API
SNAP_PIXEL_ID=
SNAP_ACCESS_TOKEN=

# Order settings
ORDER_NUMBER_PREFIX=SS
UPSELL_PRICE_SAR=99
```

## Easypanel Notes

| Variable | Where |
|----------|-------|
| `DATABASE_URL` | Backend only — use **internal** hostname |
| `NEXT_PUBLIC_*` | Frontend — set at **build time** if using Docker build args |
| Secrets | Never commit real values — Easypanel secret store |

## Build Args (Frontend Docker)

```bash
docker build \
  --build-arg NEXT_PUBLIC_API_URL=https://api.safraskin.online \
  --build-arg NEXT_PUBLIC_SITE_URL=https://safraskin.online \
  -t safra-skin-frontend .
```
