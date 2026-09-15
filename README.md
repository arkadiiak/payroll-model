# 💰 Payroll Model — Main Location

## Project Overview
This payroll model was built to calculate bi-monthly staff compensation for a multi-department beauty salon in London. The model covers 27 staff members across 4 departments and processes approximately £22,500 per pay period.

## What This Model Does
- Calculates gross pay based on hourly rates and hours worked
- Tracks tips, bonuses, and KPI performance bonuses separately
- Applies deductions where applicable
- Summarises totals by department for finance reporting
- Links to payment details (sort code, account, invoice number) for payroll processing
- SQL schema and queries replicate this logic for scalable, database-driven reporting

## Departments Covered
| Department | Staff Count | Pay Structure |
|------------|-------------|---------------|
| Nail Artists | 20 | Hourly rate + tips + KPI bonus |
| Brow Artists | 3 | % commission of revenue |
| Admin | 2 | Hourly rate + KPI bonus |
| Cleaners | 2 | Daily rate |

## Key Metrics (1–15 May 2026 period)
- **Total Payroll:** £22,572.90
- **Nail Artists Total:** £17,803.94
- **KPI Bonuses Distributed:** £1,300.00
- **Pay Period:** Bi-monthly (1st–15th and 16th–end of month)

## Tools Used
- Google Sheets / Microsoft Excel
- Manual data entry from scheduling system (Zenoti)
- Formula-based calculations (SUMIF, conditional formatting)
- SQL (schema design, joins, window functions, aggregate queries)

## Skills Demonstrated
- Payroll data management
- Multi-department financial tracking
- KPI bonus calculation logic
- Structured data organisation
- Finance reporting for operations management
- SQL database design and query writing

## SQL Implementation
This project also includes a SQL version of the payroll logic (`schema.sql`, `queries.sql`), using synthetic data to demonstrate:
- Relational schema design for technicians and monthly payroll records
- Aggregate queries for department-level and location-level totals
- Window functions for ranking top performers by period
- Subqueries for identifying below-average performers
