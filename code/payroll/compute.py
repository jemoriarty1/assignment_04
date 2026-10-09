"""
compute.py — Step 3 of the pipeline: pay, labels, and the file the provider wants.

Two element functions that need **two** values from a row, two DataFrame
functions that run them across every row with `DataFrame.apply(..., axis=1)`,
the function that chains all three steps into one call, and the export that
reshapes the result for the online payroll provider.

No walkthrough this time. You have `clean.py` and `join.py` beside you, the
docstrings say what each function must return, and `tests/test_unit.py` and
`tests/test_pipeline.py` say exactly how they will be checked.
"""

import pandas as pd

from .clean import add_hourly_rate, add_hours_worked
from .join import merge_employees

OVERTIME_THRESHOLD = 40.0   # weekly hours above this are paid at time-and-a-half
OVERTIME_MULTIPLIER = 1.5


def calc_gross_pay(hours: float, rate: float) -> float:
    """Gross pay for one employee-week, rounded to cents."""
    if pd.isna(rate):
        return 0.0

    if hours <= OVERTIME_THRESHOLD:
        gross_pay = hours * rate
    else:
        regular_pay = OVERTIME_THRESHOLD * rate
        overtime_pay = (hours - OVERTIME_THRESHOLD) * rate * OVERTIME_MULTIPLIER
        gross_pay = regular_pay + overtime_pay

    return round(gross_pay, 2)


def classify_pay(hours: float, rate: float) -> str:
    """One word the office manager can filter on: what kind of pay row is this?"""
    if pd.isna(rate):
        return "unmatched"
    elif hours > OVERTIME_THRESHOLD:
        return "overtime"
    else:
        return "regular"


def add_gross_pay(payroll: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with one new column, `gross_pay`: `calc_gross_pay` for every row."""
    out = payroll.copy()
    out["gross_pay"] = out.apply(
        lambda row: calc_gross_pay(row["hours_worked"], row["hourly_rate_usd"]),
        axis=1
    )
    return out


def add_pay_type(payroll: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with one new column, `pay_type`: `classify_pay` for every row."""
    out = payroll.copy()
    out["pay_type"] = out.apply(
        lambda row: classify_pay(row["hours_worked"], row["hourly_rate_usd"]),
        axis=1
    )
    return out

def build_payroll(timesheet: pd.DataFrame, employees: pd.DataFrame) -> pd.DataFrame:
    """The whole pipeline in one call: raw timesheet + raw roster -> payroll table."""
    timesheet_clean = add_hours_worked(timesheet)
    employees_clean = add_hourly_rate(employees)

    payroll = merge_employees(timesheet_clean, employees_clean)
    payroll = add_gross_pay(payroll)
    payroll = add_pay_type(payroll)

    return payroll


def payroll_export(payroll: pd.DataFrame) -> pd.DataFrame:
    """The file the online payroll provider imports — a NEW frame, not a renamed one."""
    export = payroll.loc[payroll["pay_type"] != "unmatched", [
        "payroll_date",
        "employee_id",
        "hours_worked",
        "hourly_rate_usd",
        "gross_pay"
    ]].copy()

    export.columns = [
        "payrolldate",
        "employeeid",
        "hours",
        "rate",
        "total"
    ]

    return export
