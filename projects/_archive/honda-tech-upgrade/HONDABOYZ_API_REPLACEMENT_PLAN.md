# HondaBoyz API Replacement Plan

- **Date:** 2026-05-03
- **Legacy source:** `D:\Affan\Coding\Django\un-zipped\Honda_Boyz`
- **Goal:** Replace hardcoded mileage/service interval values with API-backed or data-backed vehicle maintenance logic.

## What HondaBoyz appears to do

The old Django app calculates how many times a Honda owner should have serviced the car based on current mileage. Current legacy model shape:

```text
TableItem.name
TableItem.MileConstant
Table.title
```

The main issue is that service intervals are manually stored and calculated. That makes it brittle and tied to a narrow Honda Civic use case.

## Recommended data strategy

Use a layered fallback:

| Layer | Source | Purpose | Cost posture |
| --- | --- | --- | --- |
| 1 | Local seed table | Fast MVP for Honda Civic/Accord common intervals | free |
| 2 | NHTSA vPIC API | VIN decode: year/make/model/trim | free public API |
| 3 | Maintenance API provider | OEM maintenance schedule by VIN/YMMT/mileage | likely paid/free trial |
| 4 | User-entered receipts/history | Personal maintenance log and reminders | app-owned data |

## API options

| API/source | Use | Notes |
| --- | --- | --- |
| NHTSA vPIC | VIN decoding and vehicle identity | Official/public; does **not** provide full service intervals. Good first API. |
| Edmunds Maintenance API | Maintenance schedule by model year ID | Strong conceptual match, but requires API key/availability check. |
| VehicleDatabases Maintenance API | OEM maintenance schedule by VIN | Commercial API; docs show maintenance schedule endpoint. |
| CarMD/CarScan maintenance endpoint | Maintenance by VIN or YMM + mileage | Commercial API; includes due mileage, cost, parts. |
| Vehicle Finder / Auto.dev / AutoAPI411 | Specs/maintenance/recalls options | Evaluate pricing, coverage, and reliability before implementation. |

## MVP recommendation

Do **not** start by wiring a paid API. Build this flow first:

1. VIN or manual vehicle entry.
2. Decode VIN with NHTSA vPIC when VIN is present.
3. Store vehicle profile locally.
4. Use local maintenance seed data for common Honda models.
5. Abstract a `MaintenanceProvider` interface so paid providers can plug in later.
6. Add API provider only after the UX proves useful.

## Source references

- NHTSA VIN decoder: https://www.nhtsa.gov/vin-decoder
- NHTSA vPIC API: https://vpic.nhtsa.dot.gov/api/Home/Index
- NHTSA vPIC about/API context: https://vpic.nhtsa.dot.gov/About
- Edmunds maintenance docs: https://developer.edmunds.com/api-documentation/vehicle/service_maintenance/v1/
- VehicleDatabases maintenance docs: https://vehicledatabases.com/docs/api-documentation/vehicle-maintenance/
- CarScan/CarMD maintenance docs: https://api.carmd.com/member/docs

## Next implementation slice

Copy `Honda_Boyz` into `honda-tech-upgrade/legacy-src/honda-boyz` after secret/local DB exclusion, then build a small Django/FastAPI service that exposes:

```text
POST /api/vehicle/decode-vin
POST /api/maintenance/estimate
GET /api/maintenance/providers
```
