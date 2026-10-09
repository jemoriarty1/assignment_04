import pandas as pd


def merge_employees(timesheet: pd.DataFrame, employees: pd.DataFrame) -> pd.DataFrame:
    out = pd.merge(timesheet, employees, on="employee_id", how="left")
    return out