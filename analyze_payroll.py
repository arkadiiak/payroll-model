"""
Payroll Analysis (Python)
--------------------------
Generates a synthetic bi-monthly payroll dataset for a 27-person,
4-department salon team, loads it into SQLite, and uses pandas to
analyze department totals, bonus payouts, and pay period trends.

All data is synthetically generated - no real staff or financial data.
"""

import csv
import random
import sqlite3
from pathlib import Path

import pandas as pd

random.seed(11)

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "payroll_data.csv"
DB_PATH = BASE_DIR / "payroll.db"

DEPARTMENTS = {
    "Nail Artists": {"count": 20, "rate_range": (14, 18), "pay_type": "hourly"},
    "Brow Artists": {"count": 3, "rate_range": (0.55, 0.65), "pay_type": "commission"},
    "Admin": {"count": 2, "rate_range": (14, 16), "pay_type": "hourly"},
    "Cleaners": {"count": 2, "rate_range": (28, 32), "pay_type": "daily"},
}

FIRST_NAMES = ["Olena", "Maria", "Sofia", "Nadia", "Iryna", "Kateryna", "Anna",
               "Vika", "Diana", "Yana", "Alina", "Marta", "Lesia", "Halyna",
               "Tetiana", "Roksolana", "Solomiia", "Yaryna", "Bohdana", "Zoriana",
               "Khrystyna", "Oksana", "Nataliia", "Ulyana", "Oleksandra", "Vasylyna", "Ilona"]

PERIODS = ["1-15 May", "16-31 May", "1-15 Jun", "16-30 Jun"]


def generate_staff():
    staff = []
    idx = 0
    for dept, info in DEPARTMENTS.items():
        for _ in range(info["count"]):
            staff.append({
                "staff_id": f"S{idx+1:03d}",
                "name": f"{FIRST_NAMES[idx % len(FIRST_NAMES)]} {chr(65 + idx)}.",
                "department": dept,
                "pay_type": info["pay_type"],
                "rate": round(random.uniform(*info["rate_range"]), 2),
            })
            idx += 1
    return staff


def generate_payroll_rows(staff):
    rows = []
    for person in staff:
        for period in PERIODS:
            if person["pay_type"] == "hourly":
                hours = round(random.uniform(40, 110), 2)
                gross = round(hours * person["rate"], 2)
            elif person["pay_type"] == "commission":
                revenue = round(random.uniform(800, 2500), 2)
                gross = round(revenue * person["rate"], 2)
                hours = None
            else:  # daily
                days = random.randint(4, 15)
                gross = round(days * person["rate"], 2)
                hours = None

            tips = round(random.uniform(0, 60), 2) if person["pay_type"] == "hourly" else 0
            kpi_bonus = random.choice([0, 0, 0, 17.5, 39.0, 56.0])
            total = round(gross + tips + kpi_bonus, 2)

            rows.append({
                "staff_id": person["staff_id"],
                "name": person["name"],
                "department": person["department"],
                "pay_period": period,
                "hours_worked": hours,
                "gross_pay": gross,
                "tips": tips,
                "kpi_bonus": kpi_bonus,
                "total_pay": total,
            })
    return rows


def build_csv_and_db():
    staff = generate_staff()
    rows = generate_payroll_rows(staff)

    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    df = pd.read_csv(CSV_PATH)
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("payroll_records", conn, if_exists="replace", index=False)
    conn.commit()
    return conn, df


def department_totals(conn):
    query = """
        SELECT department,
               COUNT(DISTINCT staff_id) AS headcount,
               ROUND(SUM(total_pay), 2) AS total_paid,
               ROUND(AVG(total_pay), 2) AS avg_pay_per_period
        FROM payroll_records
        GROUP BY department
        ORDER BY total_paid DESC
    """
    return pd.read_sql(query, conn)


def bonus_summary(conn):
    query = """
        SELECT pay_period,
               ROUND(SUM(kpi_bonus), 2) AS total_kpi_bonus,
               SUM(CASE WHEN kpi_bonus > 0 THEN 1 ELSE 0 END) AS staff_who_earned_bonus
        FROM payroll_records
        GROUP BY pay_period
    """
    return pd.read_sql(query, conn)


def top_earners(conn, top_n=5):
    query = """
        SELECT name, department, ROUND(SUM(total_pay), 2) AS total_earned
        FROM payroll_records
        GROUP BY staff_id, name, department
        ORDER BY total_earned DESC
        LIMIT ?
    """
    return pd.read_sql(query, conn, params=(top_n,))


def plot_department_totals(dept_df):
    import matplotlib.pyplot as plt

    ax = dept_df.plot(kind="bar", x="department", y="total_paid", legend=False, figsize=(8, 5))
    ax.set_title("Total Payroll by Department (4 pay periods)")
    ax.set_ylabel("Total paid (£)")
    plt.tight_layout()
    plt.savefig(BASE_DIR / "payroll_by_department.png")
    print("Chart saved to payroll_by_department.png")


def main():
    conn, _ = build_csv_and_db()

    dept_df = department_totals(conn)
    print("\n=== Payroll totals by department ===")
    print(dept_df.to_string(index=False))

    print("\n=== KPI bonus summary by pay period ===")
    print(bonus_summary(conn).to_string(index=False))

    print("\n=== Top 5 earners ===")
    print(top_earners(conn).to_string(index=False))

    plot_department_totals(dept_df)
    conn.close()


if __name__ == "__main__":
    main()
