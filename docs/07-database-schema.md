# 07 — Database Schema

## Database

- **Name:** `safraskin`
- **URL (internal Easypanel):** `postgres://postgres:s4eagoems3oueizu0h00@safraskin_database:5432/safraskin?sslmode=disable`

## Tables

### `products`

| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| slug | VARCHAR(50) UNIQUE | freshguard, heatshield, underguard |
| sku | VARCHAR(50) UNIQUE | |
| name_ar | TEXT | |
| name_en | TEXT | |
| description_ar | TEXT | |
| price_unit_sar | INT | 199 (reference — tier pricing separate) |
| is_active | BOOLEAN | default true |
| created_at | TIMESTAMPTZ | |

### `orders`

| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| order_number | VARCHAR(20) UNIQUE | SS-YYYYMMDD-XXXX |
| customer_name | VARCHAR(200) | |
| customer_phone | VARCHAR(20) | E.164 +966... |
| customer_phone_display | VARCHAR(20) | 05XXXXXXXX |
| tier_count | INT | 1, 2, or 3 |
| tier_total_sar | INT | 199/279/349 |
| upsell_accepted | BOOLEAN | |
| upsell_slug | VARCHAR(50) NULL | |
| upsell_price_sar | INT NULL | 99 |
| grand_total_sar | INT | |
| payment_method | VARCHAR(20) | `COD` |
| status | VARCHAR(30) | pending_confirmation, confirmed, shipped, delivered, cancelled |
| event_id | VARCHAR(36) | pixel dedup |
| utm_source | VARCHAR(100) | |
| utm_campaign | VARCHAR(100) | |
| fbc | TEXT | |
| fbp | TEXT | |
| ttclid | TEXT | |
| client_ip | INET | |
| user_agent | TEXT | |
| sheets_synced | BOOLEAN | default false |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

### `order_items`

| Column | Type | Notes |
|--------|------|-------|
| id | UUID PK | |
| order_id | UUID FK → orders | |
| product_slug | VARCHAR(50) | |
| sku | VARCHAR(50) | |
| quantity | INT | |
| unit_reference_price_sar | INT | 199 |

## Alembic Migration

Initial migration `001_initial_schema.py` creates all tables + seeds 3 products.

## Seed Data

```sql
INSERT INTO products (slug, sku, name_ar, name_en, price_unit_sar) VALUES
('freshguard', 'SS-FRESHGUARD-01', 'فريش‌گارد — بروتوكول النفس الواثق من الداخل', 'FreshGuard Oral Protocol', 199),
('heatshield', 'SS-HEATSHIELD-02', 'هيت‌شield — بودرة درع الحر للجسم', 'HeatShield Body Powder', 199),
('underguard', 'SS-UNDERGUARD-03', 'أندر‌گارد — نظام ثقة الإبط الطبيعي', 'UnderGuard Deodorant Duo', 199);
```

## Indexes

```sql
CREATE INDEX idx_orders_phone ON orders(customer_phone);
CREATE INDEX idx_orders_created ON orders(created_at DESC);
CREATE INDEX idx_orders_number ON orders(order_number);
CREATE INDEX idx_order_items_order ON order_items(order_id);
```

## Migration on Start

See [06-backend-spec.md](./06-backend-spec.md) — `alembic upgrade head` in lifespan.
