import streamlit as st

from payroll import (
    build_payroll,
    load_employees,
    load_timesheet,
    payroll_export,
)


st.title("Salt City Coffee — Weekly Payroll")
st.write(
    "Upload this week's timesheet CSV to calculate payroll and "
    "download the payroll provider's file."
)

# The roster is loaded from data/, not uploaded.
roster = load_employees()

# The app waits here until the manager chooses a file.
uploaded_file = st.file_uploader(
    "Upload this week's timesheet CSV",
    type=["csv"],
    key="timesheet",
)

if uploaded_file is not None:
    # Load the uploaded timesheet and run the payroll pipeline.
    timesheet = load_timesheet(uploaded_file)
    payroll = build_payroll(timesheet, roster)

    # Display the pay period.
    payroll_date = payroll["payroll_date"].iloc[0]
    st.subheader(f"Pay period: {payroll_date}")

    # Separate matched employees from unmatched rows.
    unmatched = payroll[payroll["pay_type"] == "unmatched"]
    paid = payroll[payroll["pay_type"] != "unmatched"]
    overtime = payroll[payroll["pay_type"] == "overtime"]

    # Calculate the week's totals.
    employees_paid = len(paid)
    total_hours = payroll["hours_worked"].sum()
    total_gross_pay = payroll["gross_pay"].sum()
    overtime_weeks = len(overtime)

    # Display the four metric cards.
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Employees paid", employees_paid)
    col2.metric("Total hours", f"{total_hours:.2f}")
    col3.metric("Total gross pay", f"${total_gross_pay:,.2f}")
    col4.metric("Overtime weeks", overtime_weeks)

    # Warn about employee IDs that could not be matched to the roster.
    if len(unmatched) > 0:
        unmatched_ids = unmatched["employee_id"].unique().tolist()
        st.warning(
            "Unmatched employee ID(s): " + ", ".join(unmatched_ids)
        )
    else:
        st.success("All employee IDs matched the roster.")

    # Show the complete payroll table, including raw and computed columns.
    st.dataframe(payroll)

    # Prepare the payroll provider's CSV for download.
    export = payroll_export(payroll)
    csv_data = export.to_csv(index=False)

    st.download_button(
        label="Download payroll CSV",
        data=csv_data,
        file_name=f"payroll_{payroll_date}.csv",
        mime="text/csv",
        key="download",
    )
