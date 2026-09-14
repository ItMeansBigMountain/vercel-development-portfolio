ALTER TABLE reminder_preferences ADD COLUMN quiet_start_hour INTEGER NOT NULL DEFAULT 22 CHECK(quiet_start_hour BETWEEN 0 AND 23);
ALTER TABLE reminder_preferences ADD COLUMN quiet_end_hour INTEGER NOT NULL DEFAULT 7 CHECK(quiet_end_hour BETWEEN 0 AND 23);

CREATE TABLE notification_deliveries (
  id TEXT PRIMARY KEY,
  vehicle_id TEXT NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
  dedupe_key TEXT NOT NULL,
  classification TEXT NOT NULL CHECK(classification IN ('overdue','upcoming')),
  channels_json TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('generated','cancelled')),
  generated_at TEXT NOT NULL,
  cancelled_at TEXT,
  UNIQUE(vehicle_id, dedupe_key)
);