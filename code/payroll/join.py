import pandas as pd


def merge_employees(timesheet: pd.DataFrame, employees: pd.DataFrame) -> pd.DataFrame:
    """Return the timesheet with every roster column added to each row."""
    out = pd.merge(timesheet, employees, on="employee_id", how="left")
    return out
