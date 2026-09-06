# Honda Tech Upgrade - MVP Spec

- **Date:** 2026-05-04
- **Legacy base:** `legacy-src/honda-boyz` (copied from D:\Affan\Coding\Django\un-zipped\Honda_Boyz)

## Goal

Create a presentable MVP for a vehicle maintenance tracker that allows users to log mileage, get maintenance reminders, and receive service suggestions.

## MVP user flow

1. User opens the application.
2. User enters VIN or manually selects vehicle make/model/year.
3. App decodes VIN (if provided) using NHTSA vPIC API or uses manual entry.
4. User logs current mileage.
5. App calculates service status based on mileage and recommended intervals.
6. App displays:
   - Vehicle profile (year, make, model, trim)
   - Current mileage
   - Next recommended service (type and mileage)
   - Service history/log
   - Reminders for upcoming maintenance
7. User can add service records with date, mileage, service type, and cost.
8. Data persists locally between sessions.

## Initial architecture

```text
frontend/          Simple web interface (HTML/CSS/JS or basic frontend framework)
backend/           API for VIN decoding, mileage logging, maintenance calculations
legacy-src/        Read-only imported HondaBoyz reference code
sample-data/       Sample vehicle data and maintenance intervals
```

## Recommended stack

Use a simple modern web stack when implementation starts:

- Frontend: Basic HTML/CSS/JS or Vue.js for reactivity
- Backend: FastAPI or Express.js for API endpoints
- Data: SQLite or JSON file storage locally first
- VIN decoding: NHTSA vPIC API (free)
- Storage: Local file or SQLite database

## `.env.example` variables to support

```env
APP_ENV=development
APP_BASE_URL=http://localhost:3000
DATABASE_URL=sqlite:///./local.db
NHTSA_API_BASE=https://vpic.nhtsa.dot.gov/api
MAINTENANCE_INTERVALS_FILE=./sample-data/maintenance_intervals.json
```

## Legacy code reuse plan

| Legacy source | Reuse | First action |
| --- | --- | --- |
| `Honda_Boyz` | Mileage/service logic concepts, table structures | Extract core calculation logic; avoid Django-first architecture |

## Constraints

- Do not use paid APIs in MVP without user approval.
- Do not commit `.env` or secret API keys.
- Keep sample data mode working without external APIs.
- Focus on Honda vehicles initially, but design for extensibility.

## First implementation slice

Create a local web interface that:
1. Accepts VIN or manual vehicle entry (year, make, model)
2. Uses sample data for maintenance intervals (no API calls in MVP)
3. Allows mileage logging and viewing
4. Calculates service status based on mileage vs. recommended intervals
5. Displays next service recommendation
6. Stores data in local JSON or SQLite

## Validation

Before marking implementation done:

```powershell
# For web stack: check that local server starts and basic endpoints work
# Expected: server starts, POST mileage log returns success, GET service status returns data
```

## Open questions

- Should we start with a web interface or a desktop application?
- How granular should service types be (oil change, tire rotation, inspection, etc.)?
- Should we include cost tracking for services?