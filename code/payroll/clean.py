import pandas as pd


def parse_hours(value) -> float:
    """Read a weekly-hours string the way a shift lead typed it; return a float."""
    if not isinstance(value, str):
        if value is None or pd.isna(value):
            return 0.0
        return float(value)

    text = value.strip()
    if not text:
        return 0.0

    if "h" not in text and "m" not in text:
        try:
            return float(text)
        except ValueError:
            return 0.0

    hours = 0.0
    for word in text.split():
        try:
            if word.endswith("h"):
                hours += float(word[:-1])
            elif word.endswith("m"):
                hours += float(word[:-1]) / 60
        except ValueError:
            return 0.0
    return hours

def clean_currency(value) -> float:
    """Read a dollar amount as HR typed it; return it as a float"""
    if value is None or (not isinstance(value, str) and pd.isna(value)):
      return 0.0
    
    text = str(value).replace("$", "").replace(",", "").strip()

    try:
        return float(text)
    except ValueError:
        return 0.0

def add_hours_worked(timesheet: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of the timesheet with one new column, `hours_worked` (float)."""
    out = timesheet.copy()
    out["hours_worked"] = out["hours"].apply(parse_hours)
    return out

def add_hourly_rate(employees: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of the roster with one new column, `hourly_rate_usd` (float)."""
    out = employees.copy()
    out["hourly_rate_usd"] = out["hourly_rate"].apply(clean_currency)
    return out

if __name__ == "__main__":
    for sample in ("38h 30m", "42h", "45m", "24.5", "", "forty"):
        print(repr(sample), "->", parse_hours(sample))
    print(clean_currency("$1,020.00"))