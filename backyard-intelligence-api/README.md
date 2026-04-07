# backyard-intelligence-api

Production-minded FastAPI service that estimates backyard geometry and landscaping sales opportunities from a US address.

## What this API does

- Validates and geocodes a US address (Google provider abstraction + deterministic dev fallback).
- Retrieves parcel/building data via county GIS provider abstraction (currently stub implementation).
- Retrieves nearest road geometry via OSM Overpass fallback.
- Infers front-vs-back orientation and estimates a backyard polygon.
- Returns an aerial/satellite imagery URL centered on estimated backyard centroid (ArcGIS or Mapbox).
- Computes uncertainty, confidence, and fallback warnings.
- Produces LOVING-oriented service scoring for turf, patio, drainage, lighting, pergola, outdoor kitchen, and planting.

> This service returns **aerial/satellite imagery URLs only**. It does not provide private/ground-level backyard photos.

---

## Tech stack

- Python 3.12
- FastAPI + Pydantic
- httpx
- SQLAlchemy
- PostgreSQL + PostGIS (docker-compose)
- pytest
- Docker

---

## Project layout

See the requested folder structure under:

- `app/` routers, services, providers, models, utils
- `tests/` route and business-logic coverage

---

## Setup

### 1) Local Python setup

```bash
cd backyard-intelligence-api
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### 2) Docker setup

```bash
cd backyard-intelligence-api
cp .env.example .env
docker compose up --build
```

API docs: `http://localhost:8000/docs`

---

## Environment variables

- `SERVICE_NAME`
- `APP_VERSION`
- `DEBUG`
- `DATABASE_URL`
- `GOOGLE_GEOCODING_API_KEY`
- `MAPBOX_API_TOKEN`
- `ARCGIS_API_KEY`
- `DEFAULT_IMAGERY_PROVIDER`

---

## Endpoints

1. `GET /health`
2. `POST /v1/backyard-image`
3. `POST /v1/parcel-lookup`
4. `POST /v1/backyard-polygon`
5. `POST /v1/property-analyze`
6. `GET /v1/providers/status`

### curl samples

```bash
curl -s http://localhost:8000/health
```

```bash
curl -s -X POST http://localhost:8000/v1/backyard-image \
  -H 'Content-Type: application/json' \
  -d '{"address":"123 Main St, Dallas, TX 75201","imagery_provider":"arcgis","zoom":20,"width":640,"height":640}'
```

```bash
curl -s -X POST http://localhost:8000/v1/property-analyze \
  -H 'Content-Type: application/json' \
  -d '{"address":"123 Main St, Dallas, TX 75201","requested_services":["drainage","patio","lighting","outdoor_kitchen"]}'
```

---

## Testing

```bash
cd backyard-intelligence-api
pytest -q
```


### Dockerized test run

```bash
cd backyard-intelligence-api
docker compose run --rm api pytest -q
```

---

## Confidence and honesty behavior

- Missing parcel/building/road data degrades confidence.
- Fallback mode sets `fallback_used=true` and provides warning reasons.
- Outputs include `data_quality_score` (0-100), `backyard_confidence`, and warnings.
- No fake precision claims are made for estimated geometry.

---

## Production-ready vs stubbed

### Production-ready in this repository

- FastAPI app structure with DI, clear provider/service abstraction, typed models.
- Core endpoint flows and uncertainty-aware responses.
- Deterministic fallback behavior useful for dev/test and demos.
- Basic unit/integration-ish tests for critical flows.
- Dockerized API + PostGIS infrastructure.

### Stubbed in this repository

- County parcel/building feeds are represented by synthetic stub polygons.
- No persistent write path for analysis records yet.
- No auth/rate limiting/tenant controls.

### Needed for nationwide high-accuracy rollout

- County-by-county GIS connectors or commercial parcel/building data vendor integration.
- Data freshness/versioning pipeline and jurisdiction coverage mapping.
- Better geospatial inference (driveway detection, frontage constraints, topo/water flow layers).
- Monitoring, retries, circuit breakers, caching, and cost governance for third-party APIs.
