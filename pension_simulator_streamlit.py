import streamlit as st
import math

st.set_page_config(page_title="S&P 500 Pension Simulator", layout="centered")

st.title("📈 S&P 500 Pension Simulator")
st.write("Estimate your pension balance after years of saving with various return scenarios, based on your contributions and expected salary.")

# Input fields
years_until_retirement = st.number_input("Years until retirement:", min_value=1, max_value=70, value=41)
years_contributing = st.number_input("How many of those years will you be actively contributing?", min_value=0, max_value=70, value=39)
years_until_start = years_until_retirement - years_contributing

initial_balance = st.number_input("Current pension balance (NIS):", min_value=0.0, value=27500.0)
expected_salary = st.number_input("Expected gross monthly salary when working (NIS):", min_value=0.0, value=18000.0)

# Constants
management_fee = 0.007  # 0.7% annual management fee
monthly_contribution_rate = 0.18  # 18% of gross salary

# Return rates to simulate
return_scenarios = {
    "Very Optimistic (10%)": 0.10,
    "Optimistic (7%)": 0.07,
    "Realistic (6%)": 0.06,
    "Conservative (4%)": 0.04,
    "Minimum Scenario (3%)": 0.03
}

def simulate_pension(years, contribution_years, start_delay, current_balance, salary, annual_return):
    balance = current_balance
    for year in range(years):
        if year >= start_delay:
            annual_contribution = salary * monthly_contribution_rate * 12
        else:
            annual_contribution = 0
        balance = balance * (1 + annual_return - management_fee) + annual_contribution
    return balance

if "results" not in st.session_state:
    st.session_state["results"] = None

# Run simulation
if st.button("Run Simulation"):
    results = {}
    for label, rate in return_scenarios.items():
        final_balance = simulate_pension(
            years_until_retirement,
            years_contributing,
            years_until_start,
            initial_balance,
            expected_salary,
            rate
        )
        results[label] = round(final_balance, 2)
    st.session_state["results"] = results

# Display results if available
if st.session_state["results"]:
    st.subheader("📊 Estimated Total Pension Balance (after management fees):")
    for label, amount in st.session_state["results"].items():
        st.write(f"{label}: {amount:,.2f} NIS")

    # Monthly estimate checkbox
    if st.checkbox("Show estimated monthly pension"):
        use_custom = st.checkbox("I want to enter a custom annuity factor")
        if use_custom:
            annuity_factor = st.number_input("Enter your annuity factor (e.g. 205):", min_value=1.0, value=205.0)
        else:
            gender = st.radio("Your gender (for estimating annuity factor):", ["Male", "Female"])
            annuity_factor = 205 if gender == "Male" else 215

        st.subheader(f"💰 Estimated Monthly Pension (Annuity Factor = {annuity_factor}):")
        for label, total in st.session_state["results"].items():
            monthly = round(total / annuity_factor, 2)
            st.write(f"{label}: {monthly:,.2f} NIS/month")
