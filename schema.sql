-- Schema for a multi-location salon performance tracker
-- Designed for SQLite/PostgreSQL

CREATE TABLE IF NOT EXISTS technicians (
    technician_id   TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    location        TEXT NOT NULL,
    base_rate       NUMERIC(5,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS monthly_performance (
    id                          INTEGER PRIMARY KEY AUTOINCREMENT,
    technician_id               TEXT NOT NULL REFERENCES technicians(technician_id),
    month                       TEXT NOT NULL,
    hours_worked                NUMERIC(6,1),
    efficient_hours             NUMERIC(6,1),
    days_worked                 INTEGER,
    revenue                     NUMERIC(10,2),
    materials_cost              NUMERIC(10,2),
    total_clients               INTEGER,
    old_clients                 INTEGER,
    salary                      NUMERIC(10,2),
    profitability_pct           NUMERIC(5,2),
    client_retention_pct        NUMERIC(5,2),
    workload_pct                NUMERIC(5,2),
    workdays_utilization_pct    NUMERIC(5,2),
    pft_completion_pct          NUMERIC(5,2),
    final_score                 NUMERIC(5,1),
    tier                        TEXT,
    bonus_gbp                   NUMERIC(6,2)
);

CREATE INDEX IF NOT EXISTS idx_perf_technician ON monthly_performance(technician_id);
CREATE INDEX IF NOT EXISTS idx_perf_month ON monthly_performance(month);
