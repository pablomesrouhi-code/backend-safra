# Easypanel — Fix 502 + Orders + Google Sheet

## المشكل
- `502` على `api.safraskin.online` = **backend ميت** (ما كيبداش)
- Site `safraskin.online` خدام = frontend OK

---

## الخطوات (بالترتيب)

### 1) Database service
- Easypanel → **safraskin_database** (Postgres) → **Running** (أخضر)
- Copy **Internal connection URL** (مثال):
  ```
  postgres://postgres:YOUR_PASSWORD@safraskin_database:5432/safraskin
  ```

### 2) Backend env (مهم)
Service **backend** → Environment:

```env
DATABASE_URL=postgres://postgres:YOUR_PASSWORD@safraskin_database:5432/safraskin?sslmode=disable
GOOGLE_SHEETS_WEBHOOK_URL=https://script.google.com/macros/s/XXXX/exec
ORDER_NUMBER_PREFIX=nama
CORS_ORIGINS=https://safraskin.online,https://www.safraskin.online
API_HOST=0.0.0.0
API_PORT=8000
```

- استبدل `YOUR_PASSWORD` بكلمة سر DB الحقيقية
- إذا password فيها `@` أو `#` → [URL encode](https://www.urlencoder.org/) (مثال `@` → `%40`)
- **Hostname** = `safraskin_database` (اسم service DB)، **ماشي** `localhost`

### 3) Backend deploy
| Setting | Value |
|---------|--------|
| Repo | `pablomesrouhi-code/backend-safra` |
| Branch | `main` |
| Dockerfile | `Dockerfile` |
| Port | **8000** |
| Domain | `api.safraskin.online` |

→ **Rebuild & Deploy** (ماشي restart فقط)

### 4) Frontend env
```env
NEXT_PUBLIC_API_URL=https://api.safraskin.online
API_URL=https://api.safraskin.online
```

→ Redeploy frontend

### 5) تحقق
افتح: `https://api.safraskin.online/health`

**لازم:**
```json
{
  "status": "ok",
  "database": true,
  "sheets_webhook_configured": true
}
```

| النتيجة | المعنى |
|---------|--------|
| 502 | Backend ma بداش — شوف Logs |
| `"database": false` | `DATABASE_URL` غلط |
| `"database": true` | جربي طلب من الموقع |

### 6) Google Sheet
- Apps Script: كود من `docs/sheets/google-apps-script.js`
- Deploy Web app → Anyone → URL `/exec`
- نفس URL في `GOOGLE_SHEETS_WEBHOOK_URL`

---

## Logs (Easypanel → backend → Logs)

**صح:**
```
Safra Skin API starting
DATABASE_URL (masked): postgresql+psycopg2://postgres:***@safraskin_database:5432/...
Database connected on attempt 1
```

**غلط:**
```
NoSuchModuleError: postgres  → Redeploy rebuild (psycopg2)
connection refused         → DATABASE_URL hostname غلط
password authentication    → password غلط
```
